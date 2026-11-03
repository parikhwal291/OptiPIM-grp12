#!/usr/bin/env python3
"""Turn OptiPIM / heuristic mappings into a CSV of loop tile factors per level.

Accepts two kinds of input file, detected automatically:
  1. trace files: pim-opt's --trace-output-path (e.g. Result/Group.txt) and the
     authors' baseline_mappings/**/0.trace. These start with `conv2d` or `gemm`
     and store Bound as three groups in the order Level 2, Level 0, Level 1.
  2. pim-opt stdout logs (save with `pim-opt ... | tee run.log`). These hold
     one "[OPTIMIZED OPERATOR RESULTS]" block per operator with
     "[Level 0 (Inner Most)]", "[Level 1]", "[Level 2 (Outter Most)]" and one
     "N: 4" / "FC_N: 4" line per loop, plus "Real Cost: ...".

Output: one row per (file, op, loop) with the factor at each level:
    file,op,op_type,device,loop,L0,L1,L2,full,real_cost
full = L0*L1*L2 (should equal the layer size). In the authors' trace format
Level 2 is the bank level, so the product of L2 over all loops is the number
of banks used; it is printed per file as a sanity check.

Example:
    python parse_mapping.py Result/*.Group.txt run.log -o mappings.csv
"""
import argparse
import csv
import re
import sys
from math import prod

LEVEL_RE = re.compile(r"^\s*\[(Level\s+(\d)[^\]]*)\]:\s*$")
LOOP_RE = re.compile(r"^\s*([A-Z_]+):\s*(-?\d+)\s*$")
HEADER_RE = re.compile(r"Op ID:\s*(\d+);\s*Type:\s*(\w+);\s*Target Device:\s*([^;]+);")
COST_RE = re.compile(r"Real Cost:\s*([-+0-9.eE]+)")

FIELDS = ["file", "op", "op_type", "device", "loop", "L0", "L1", "L2", "full",
          "real_cost"]


def parse_trace(path, lines):
    op_type, loops, bound = None, [], []
    for line in lines:
        s = line.strip()
        if s.lower() in ("conv2d", "gemm"):
            op_type = s.lower()
        elif s.startswith(("Loop:", "Loops:")):
            loops = [x.strip() for x in s.split(":", 1)[1].split(",")]
        elif s.startswith("Bound:"):
            bound = [int(x) for x in s.split(":", 1)[1].split(",")]
        elif s.lower() == "end":
            break
    n = len(bound) // 3
    if not op_type or n == 0:
        raise ValueError("no conv2d/gemm Bound found")
    names = loops[:n] if loops else [f"loop{i}" for i in range(n)]
    if op_type == "gemm":
        names = [x if x.startswith("FC_") else f"FC_{x}" for x in names]
    rows = []
    for i, name in enumerate(names):
        l2, l0, l1 = bound[i], bound[i + n], bound[i + 2 * n]
        rows.append({"file": path, "op": 0, "op_type": op_type, "device": "",
                     "loop": name, "L0": l0, "L1": l1, "L2": l2,
                     "full": l0 * l1 * l2, "real_cost": ""})
    return rows


def parse_log(path, lines):
    ops, cur, level = [], None, None
    for line in lines:
        if "[OPTIMIZED OPERATOR RESULTS]" in line:
            cur = {"op": len(ops), "op_type": "", "device": "", "levels": {},
                   "real_cost": ""}
            ops.append(cur)
            level = None
            continue
        if cur is None:
            continue
        m = HEADER_RE.search(line)
        if m:
            cur["op"], cur["op_type"], cur["device"] = int(m[1]), m[2], m[3].strip()
            continue
        m = LEVEL_RE.match(line)
        if m:
            level = int(m[2])
            cur["levels"].setdefault(level, {})
            continue
        m = COST_RE.search(line)
        if m:
            cur["real_cost"] = float(m[1])
            level = None
            continue
        m = LOOP_RE.match(line)
        if m and level is not None:
            # only the first value per loop and level (later lines are checks)
            cur["levels"][level].setdefault(m[1], int(m[2]))
        elif line.strip().startswith("[") and level is not None:
            level = None  # left the loop-bound section
    rows = []
    for op in ops:
        names = list(dict.fromkeys(k for lv in op["levels"].values() for k in lv))
        for name in names:
            f = [op["levels"].get(l, {}).get(name, 1) for l in (0, 1, 2)]
            rows.append({"file": path, "op": op["op"], "op_type": op["op_type"],
                         "device": op["device"], "loop": name, "L0": f[0],
                         "L1": f[1], "L2": f[2], "full": prod(f),
                         "real_cost": op["real_cost"]})
    return rows


def parse_file(path):
    with open(path, errors="replace") as fh:
        lines = fh.readlines()
    first = next((l.strip().lower() for l in lines if l.strip()), "")
    if first in ("conv2d", "gemm"):
        return parse_trace(path, lines)
    if any("[OPTIMIZED OPERATOR RESULTS]" in l for l in lines):
        return parse_log(path, lines)
    raise ValueError("neither a trace file nor a pim-opt log")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", default="-", help="CSV path (default stdout)")
    args = ap.parse_args()

    rows = []
    for p in args.files:
        try:
            r = parse_file(p)
        except Exception as e:  # keep going over the other files
            print(f"skip {p}: {e}", file=sys.stderr)
            continue
        for op in sorted({x["op"] for x in r}):
            sel = [x for x in r if x["op"] == op]
            print(f"{p} op {op}: banks used (product of L2) = "
                  f"{prod(x['L2'] for x in sel)}", file=sys.stderr)
        rows += r

    out = sys.stdout if args.out == "-" else open(args.out, "w", newline="")
    w = csv.DictWriter(out, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
    if out is not sys.stdout:
        out.close()
        print(f"wrote {len(rows)} rows to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
