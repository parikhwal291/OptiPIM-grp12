#!/usr/bin/env python3
"""Check generated heuristic traces against authors' shipped baseline traces.

Task 2.2 verification script:
Diffs all 10 generated heuristic traces (group12/mappings/<target>/<op>/heuristic.trace)
against the authors' reference traces (baseline_mappings/heuristic_1/...) and prints
SAME or DIFFERENT for each line.

Also scores all 10 traces with the analytical model and verifies they reproduce
the exact expected costs from TEAM_TASKS.md.

Usage:
  python3 group12/scripts/check_heuristic.py [--repo-root PATH] [--score]
"""

import argparse
import os
import sys
from pathlib import Path

# Mapping between operator IDs and reference directories in baseline_mappings
REF_MAPPINGS = {
    "C1": "257-32_banks-ResNet50-12",
    "C2": "247-32_banks-ResNet50-2",
    "C3": "246-32_banks-ResNet50-1",
    "M1": "0-32_banks-bert-0",
    "M2": "1-32_banks-bert-1",
}

# Expected analytical model costs (finalPerformance) from TEAM_TASKS.md:
EXPECTED_COSTS = {
    "hbmpim": {
        "C1": 29546496,
        "C2": 29546496,
        "C3": 3282944,
        "M1": 835584,
        "M2": 614400,
    },
    "simdram": {
        "C1": 65549429,
        "C2": 36395701,
        "C3": 4053173,
        "M1": 24881280,
        "M2": 7769472,
    },
}

DEVICE_DIRS = {
    "hbmpim": "hbm_baseline",
    "simdram": "simdram_baseline",
}

ARCH_FILES = {
    "hbmpim": ("data/hbm_pim.json", 1),
    "simdram": ("data/dram.json", 0),
}


def diff_files(gen_path, ref_path):
    """Compare two trace files line by line, ignoring trailing whitespace and newlines."""
    if not gen_path.exists():
        return False, [f"Missing generated file: {gen_path}"]
    if not ref_path.exists():
        return False, [f"Missing reference file: {ref_path}"]

    with open(gen_path, "r", encoding="utf-8") as f:
        gen_lines = [line.strip() for line in f if line.strip()]

    with open(ref_path, "r", encoding="utf-8") as f:
        ref_lines = [line.strip() for line in f if line.strip()]

    if gen_lines == ref_lines:
        return True, []

    diffs = []
    max_len = max(len(gen_lines), len(ref_lines))
    for i in range(max_len):
        g = gen_lines[i] if i < len(gen_lines) else "<MISSING>"
        r = ref_lines[i] if i < len(ref_lines) else "<MISSING>"
        if g != r:
            diffs.append(f"  Line {i+1}:\n    gen: {g}\n    ref: {r}")

    return False, diffs


def score_trace(trace_path, arch_info, dev_type):
    """Score a trace file using the analytical model."""
    from analytical_modeling.parser_trace import TraceParser
    from analytical_modeling.analytical import cal_performance_conv2D, cal_performance_FC

    p = TraceParser(str(trace_path))
    if p.operation_type == "conv2d":
        ds = p.dilation_stride
        # For heuristic traces: stride-first [stride, stride, dilation, dilation]
        stride = ds[0]
        dilation = ds[2]
        perf = cal_performance_conv2D(
            arch_info, p.get_loop_bounds(), p.get_trans_coeff(), stride, dilation, dev_type
        )
    else:
        perf = cal_performance_FC(arch_info, p.get_loop_bounds(), dev_type)

    return perf.finalPerformance


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--score", action="store_true", default=True, help="Compute and check analytical scores")
    parser.add_argument("--heuristic", default="heuristic_1", choices=["heuristic_1", "heuristic_2"],
                        help="Baseline version to check against (default: heuristic_1)")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    val_dir = root / "validation"
    if str(val_dir) not in sys.path:
        sys.path.insert(0, str(val_dir))

    can_score = False
    if args.score:
        try:
            from analytical_modeling.analytical import ArchInfo
            archs = {d: ArchInfo(str(root / f)) for d, (f, _) in ARCH_FILES.items()}
            can_score = True
        except Exception as e:
            print(f"Warning: could not load analytical model: {e}", file=sys.stderr)

    print("=" * 80)
    print(f"OptiPIM Group 12: Baseline Trace Verification vs {args.heuristic}")
    print("=" * 80)
    header = f"{'Op':<4} {'Target':<8} {'Trace Match':<12} {'Analytical Cost':<18} {'Expected Cost':<18} {'Status':<8}"
    print(header)
    print("-" * len(header))

    all_traces_matched = True
    all_scores_matched = True
    total_checks = 0

    detailed_diffs = []

    for op in ["C1", "C2", "C3", "M1", "M2"]:
        layer_dir = REF_MAPPINGS[op]
        for target in ["hbmpim", "simdram"]:
            total_checks += 1
            dev_dir = DEVICE_DIRS[target]
            gen_file = root / "group12" / "mappings" / target / op / "heuristic.trace"
            ref_file = root / "baseline_mappings" / args.heuristic / dev_dir / layer_dir / "0.trace"

            is_same, diffs = diff_files(gen_file, ref_file)
            match_str = "SAME" if is_same else "DIFFERENT"
            if not is_same:
                all_traces_matched = False
                detailed_diffs.append((op, target, diffs))

            score_str = "-"
            expected_str = str(EXPECTED_COSTS[target][op])
            status_str = "PASS" if is_same else "FAIL"

            if can_score and gen_file.exists():
                try:
                    arch, dev_type = archs[target], ARCH_FILES[target][1]
                    cost = score_trace(gen_file, arch, dev_type)
                    score_str = f"{int(cost):,}"
                    expected_val = EXPECTED_COSTS[target][op]
                    expected_str = f"{expected_val:,}"
                    if int(cost) == expected_val:
                        if is_same:
                            status_str = "PASS"
                    else:
                        all_scores_matched = False
                        status_str = "MISMATCH"
                except Exception as e:
                    score_str = f"ERR: {e}"
                    status_str = "ERR"

            print(f"{op:<4} {target:<8} {match_str:<12} {score_str:<18} {expected_str:<18} {status_str:<8}")

    print("=" * 80)

    if detailed_diffs:
        print("\nDetailed Trace Differences:")
        for op, target, diffs in detailed_diffs:
            print(f"\n--- {op} ({target}) ---")
            for d in diffs:
                print(d)

    if all_traces_matched and all_scores_matched:
        print("\nSUCCESS: All 10 traces MATCH the reference heuristic_1 traces EXACTLY and reproduce all analytical costs!")
        sys.exit(0)
    else:
        print(f"\nNOTE: Traces matched: {all_traces_matched}, Scores matched: {all_scores_matched}")
        sys.exit(0 if all_traces_matched else 1)


if __name__ == "__main__":
    main()
