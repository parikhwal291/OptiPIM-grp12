#!/usr/bin/env python3
"""Score every mapping trace and produce the unified results.csv.

Task 3.2 Evaluation Script:
Scores all benchmark mappings (optipim and baseline heuristic, both HBM-PIM and SIMDRAM)
using the authors' analytical model (with the stride/dilation fix for C1), and merges
cycle counts from the Ramulator2 simulator and solver times from Gurobi into
group12/results/results.csv.

Cost model mapping (see group12/README.md for details):
  SIMDRAM:
    - compute: bit-serial mul + add latency (numMulCol * mulLat + numRedCol * addLat)
    - input_loading: inLoadingCost
    - weight_loading: 0 (stationary in DRAM array)
    - output: outTransCost
  HBM-PIM:
    - compute: row activation latency (num_mul_col * rowActLat)
    - input_loading: inLoadingCost (streaming inputs)
    - weight_loading: numFilPELoading (filter/weight loading to PEs)
    - output: outTransCost (0 / negligible)

Usage (from repo root):
  python3 group12/scripts/evaluate.py [--repo-root PATH] [--out PATH]
"""

import argparse
import csv
import sys
from pathlib import Path

# Operator and hardware configurations
OPS = ["C1", "C2", "C3", "M1", "M2"]
TARGETS = ["hbmpim", "simdram"]
ARCH_CONFIG = {
    "hbmpim": ("data/hbm_pim.json", 1),
    "simdram": ("data/dram.json", 0),
}

REF_HEURISTIC_DIRS = {
    "hbmpim": {
        "C1": "baseline_mappings/heuristic_1/hbm_baseline/257-32_banks-ResNet50-12/0.trace",
        "C2": "baseline_mappings/heuristic_1/hbm_baseline/247-32_banks-ResNet50-2/0.trace",
        "C3": "baseline_mappings/heuristic_1/hbm_baseline/246-32_banks-ResNet50-1/0.trace",
        "M1": "baseline_mappings/heuristic_1/hbm_baseline/0-32_banks-bert-0/0.trace",
        "M2": "baseline_mappings/heuristic_1/hbm_baseline/1-32_banks-bert-1/0.trace",
    },
    "simdram": {
        "C1": "baseline_mappings/heuristic_1/simdram_baseline/257-32_banks-ResNet50-12/0.trace",
        "C2": "baseline_mappings/heuristic_1/simdram_baseline/247-32_banks-ResNet50-2/0.trace",
        "C3": "baseline_mappings/heuristic_1/simdram_baseline/246-32_banks-ResNet50-1/0.trace",
        "M1": "baseline_mappings/heuristic_1/simdram_baseline/0-32_banks-bert-0/0.trace",
        "M2": "baseline_mappings/heuristic_1/simdram_baseline/1-32_banks-bert-1/0.trace",
    },
}

COLUMNS = [
    "operator",
    "target",
    "mapper",
    "banks",
    "precision",
    "analytical_cycles",
    "simulated_cycles",
    "compute",
    "input_loading",
    "weight_loading",
    "output",
    "solve_seconds",
]


def score_trace(trace_path, target, mapper, arch_info, dev_type):
    """Parse trace file and calculate performance components using analytical model."""
    from analytical_modeling.parser_trace import TraceParser
    from analytical_modeling.analytical import cal_performance_conv2D, cal_performance_FC

    p = TraceParser(str(trace_path))
    order = "dilation_first" if mapper.startswith("optipim") else "stride_first"
    ds = p.dilation_stride
    if order == "dilation_first":
        dilation, stride = ds[0], ds[2]
    else:
        stride, dilation = ds[0], ds[2]

    if p.operation_type == "conv2d":
        perf = cal_performance_conv2D(
            arch_info, p.get_loop_bounds(), p.get_trans_coeff(), stride, dilation, dev_type
        )
        n_bounds = 7
    else:
        perf = cal_performance_FC(arch_info, p.get_loop_bounds(), dev_type)
        n_bounds = 5

    banks = 1
    for b in p.bound[:n_bounds]:
        banks *= b

    # Decompose costs based on architecture
    inp = perf.inLoadingCost
    if target == "hbmpim":
        weight = perf.numFilPELoading
        out = 0.0
        compute = perf.finalPerformance - inp - weight
    else:
        weight = 0.0
        out = perf.outTransCost
        compute = perf.finalPerformance - inp - out

    return {
        "analytical_cycles": perf.finalPerformance,
        "banks": banks,
        "compute": compute,
        "input_loading": inp,
        "weight_loading": weight,
        "output": out,
    }


def load_sim_cycles(sim_path):
    """Load simulated cycles from sim_check.csv."""
    sim_data = {}
    if not sim_path.exists():
        return sim_data
    with open(sim_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            op = row["operator"].strip()
            tgt = row["target"].strip().lower()
            mapper = row["mapper"].strip().lower()
            cycles = int(row["simulated_cycles"]) if row["simulated_cycles"] else None
            # Normalize heuristic mapper naming
            norm_mapper = "heuristic" if mapper in ("heuristic", "heuristic_1") else mapper
            sim_data[(op, tgt, norm_mapper)] = cycles
    return sim_data


def load_solve_times(solve_path):
    """Load Gurobi solve times from solve_times.csv."""
    times = {}
    if not solve_path.exists():
        return times
    with open(solve_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            op = row["operator"].strip()
            tgt = row["target"].strip().lower()
            sec = float(row.get("gurobi_seconds") or row.get("wall_seconds") or 0.0)
            times[(op, tgt)] = sec
    return times


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", default=None, help="Root path of the repository")
    parser.add_argument("--sim", default=None, help="Path to sim_check.csv")
    parser.add_argument("--solve-times", default=None, help="Path to solve_times.csv")
    parser.add_argument("--out", default=None, help="Output path for results.csv")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parent.parent.parent
    sim_path = Path(args.sim) if args.sim else repo_root / "group12" / "results" / "sim_check.csv"
    solve_path = Path(args.solve_times) if args.solve_times else repo_root / "group12" / "results" / "solve_times.csv"
    out_path = Path(args.out) if args.out else repo_root / "group12" / "results" / "results.csv"

    sys.path.insert(0, str(repo_root / "validation"))
    from analytical_modeling.analytical import ArchInfo

    archs = {tgt: (ArchInfo(str(repo_root / cfg)), dev_type) for tgt, (cfg, dev_type) in ARCH_CONFIG.items()}
    sim_cycles = load_sim_cycles(sim_path)
    solve_times = load_solve_times(solve_path)

    rows = []
    for op in OPS:
        for tgt in TARGETS:
            arch_info, dev_type = archs[tgt]
            for mapper_name in ["optipim", "heuristic"]:
                if mapper_name == "optipim":
                    trace_path = repo_root / "group12" / "mappings" / tgt / op / "optipim.trace"
                else:
                    # Prefer generated heuristic trace, fallback to baseline_mappings
                    trace_path = repo_root / "group12" / "mappings" / tgt / op / "heuristic.trace"
                    if not trace_path.exists():
                        trace_path = repo_root / REF_HEURISTIC_DIRS[tgt][op]

                if not trace_path.exists():
                    print(f"Warning: Trace {trace_path} not found, skipping...")
                    continue

                scored = score_trace(trace_path, tgt, mapper_name, arch_info, dev_type)
                sim_val = sim_cycles.get((op, tgt, mapper_name))
                solve_sec = solve_times.get((op, tgt), "") if mapper_name == "optipim" else ""

                row = {
                    "operator": op,
                    "target": tgt,
                    "mapper": mapper_name,
                    "banks": scored["banks"],
                    "precision": 16,
                    "analytical_cycles": scored["analytical_cycles"],
                    "simulated_cycles": sim_val if sim_val is not None else "",
                    "compute": scored["compute"],
                    "input_loading": scored["input_loading"],
                    "weight_loading": scored["weight_loading"],
                    "output": scored["output"],
                    "solve_seconds": solve_sec,
                }
                rows.append(row)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully evaluated {len(rows)} mappings. Wrote {out_path}\n")
    print(f"{'Op':<4} {'Target':<8} {'Mapper':<10} {'Banks':<6} {'Analytical':<14} {'Simulated':<14} {'Compute':<12} {'InLoad':<12} {'WeightLoad':<12} {'Out':<10} {'Solve(s)':<8}")
    print("-" * 105)
    for r in rows:
        sim_str = f"{r['simulated_cycles']:,}" if r['simulated_cycles'] != "" else "N/A"
        solve_str = f"{r['solve_seconds']:.2f}" if isinstance(r['solve_seconds'], (int, float)) else str(r['solve_seconds'])
        print(f"{r['operator']:<4} {r['target']:<8} {r['mapper']:<10} {r['banks']:<6} {r['analytical_cycles']:<14.1f} {sim_str:<14} {r['compute']:<12.1f} {r['input_loading']:<12.1f} {r['weight_loading']:<12.1f} {r['output']:<10.1f} {solve_str:<8}")


if __name__ == "__main__":
    main()
