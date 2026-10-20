#!/usr/bin/env python3
"""Score mapping trace files with the authors' Python analytical model.

Use this for BOTH mappers so OptiPIM and the heuristic are costed by the
same formula and the same arch file.

Input is a manifest CSV with columns:
    operator,device,mapper,trace[,ds_order]
  operator  C1, C2, ... (must match the names used elsewhere)
  device    simdram or hbmpim
  mapper    optipim, heuristic_1, heuristic_2, ...
  trace     path to a trace file; relative paths are tried against
            --optipim-root, then --repo-root
  ds_order  how the DilationStride line is written (optional):
              dilation_first  pim-opt output (DataLayoutMILP.cpp writes
                              dilation,dilation,stride,stride)
              stride_first    the authors' baseline_mappings traces, and what
                              validation/analytical_modeling/get_trace_perf.py
                              assumes (stride = field 0, dilation = field 2)
            default: dilation_first for mapper optipim*, else stride_first.
            This only matters for strided or dilated convs (C1 here). Scoring
            a pim-opt trace with get_trace_perf directly treats C1 as stride 1,
            dilation 2.

Arch files follow group12/scripts/score_analytical.py:
    hbmpim -> data/hbm_pim.json (device type 1)
    simdram -> data/dram.json   (device type 0)

Example (from group12/analysis, venv active):
    python score_traces.py --optipim-root ~/OptiPIM --repo-root ../.. \
        --manifest manifest.csv --out scores.csv
"""
import argparse
import csv
import sys
from pathlib import Path

ARCH = {"hbmpim": ("data/hbm_pim.json", 1), "simdram": ("data/dram.json", 0)}

FIELDS = ["operator", "device", "mapper", "cost", "banks_used", "stride",
          "dilation", "inLoadingCost", "outTransCost", "numFilPELoading",
          "trace"]


def resolve(p, roots):
    p = Path(p).expanduser()
    if p.is_absolute():
        return p
    for r in roots:
        if r is not None and (r / p).exists():
            return r / p
    raise FileNotFoundError(p)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--optipim-root", required=True,
                    help="path to the authors' OptiPIM checkout")
    ap.add_argument("--repo-root", default=None,
                    help="path to the group repo (for group12/mappings/... paths)")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out", default="scores.csv")
    args = ap.parse_args()

    root = Path(args.optipim_root).expanduser().resolve()
    repo = Path(args.repo_root).expanduser().resolve() if args.repo_root else None
    sys.path.insert(0, str(root / "validation"))
    from analytical_modeling.analytical import (ArchInfo, cal_performance_conv2D,
                                                cal_performance_FC)
    from analytical_modeling.parser_trace import TraceParser

    archs = {d: ArchInfo(str(root / f)) for d, (f, _) in ARCH.items()}
    rows = []
    with open(args.manifest, newline="") as f:
        for m in csv.DictReader(f):
            if m["operator"].lstrip().startswith("#"):
                continue
            dev = m["device"].strip().lower()
            mapper = m["mapper"].strip()
            trace = resolve(m["trace"], [root, repo])
            order = (m.get("ds_order") or "").strip() or (
                "dilation_first" if mapper.startswith("optipim") else "stride_first")
            p = TraceParser(str(trace))
            ds = p.dilation_stride
            if order == "dilation_first":
                dilation, stride = ds[0], ds[2]
            else:
                stride, dilation = ds[0], ds[2]
            arch, dev_type = archs[dev], ARCH[dev][1]
            if p.operation_type == "conv2d":
                perf = cal_performance_conv2D(arch, p.get_loop_bounds(),
                                              p.get_trans_coeff(), stride,
                                              dilation, dev_type)
                n = 7
            else:
                perf = cal_performance_FC(arch, p.get_loop_bounds(), dev_type)
                n = 5
            banks = 1
            for b in p.bound[:n]:  # Level-2 group = banks
                banks *= b
            rows.append({
                "operator": m["operator"], "device": dev, "mapper": mapper,
                "cost": perf.finalPerformance, "banks_used": banks,
                "stride": stride, "dilation": dilation,
                "inLoadingCost": perf.inLoadingCost,
                "outTransCost": perf.outTransCost,
                "numFilPELoading": perf.numFilPELoading,
                "trace": m["trace"],
            })
            print(f"{m['operator']:4s} {dev:8s} {mapper:12s} cost={perf.finalPerformance:.6g} "
                  f"banks={banks} stride={stride} dilation={dilation}")

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
