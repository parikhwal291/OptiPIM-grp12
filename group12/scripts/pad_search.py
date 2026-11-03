#!/usr/bin/env python3
"""Padding search for OptiPIM (Group 12 extension).

OptiPIM only lets a loop be split across banks / time / columns by exact
divisors of its bound (DataLayoutMILP::getAllDivisors). A bound like 13 or 27
therefore leaves hardware idle. This script tries zero-padding the awkward
bounds to friendlier sizes, re-runs the unchanged pim-opt ILP on each padded
layer, and keeps the variant with the lowest Real Cost.

Padding is semantics-preserving: extra output pixels / channels / matrix
columns are computed on zeros and discarded; padded reduction dims (C, matmul
Q) add zeros to the sum. The Real Cost that pim-opt reports for a padded layer
already includes the extra work and data, so it is compared directly with the
unpadded Real Cost.

No C++ change and no rebuild: we only write new .mlir files.

Usage (from the OptiPIM repo root):
  python3 group12/scripts/pad_search.py \
      nn_models/alexnet/single_layers/16banks/layerinfo.alexnet.l2.conv2.linalg.mlir \
      --device simdram
  python3 group12/scripts/pad_search.py LAYER.mlir --device hbmpim --dry-run
  python3 group12/scripts/pad_search.py --shape 'matmul:P=197,Q=768,R=768' --name vit.fc_qkv --device simdram
"""
import argparse
import csv
import itertools
import math
import os
import re
import subprocess
import sys
import time

DEVICES = {
    # name: (--target-device-type, arch json, lanes per bank for the prescreen)
    "simdram": (0, "data/dram.json", 8192),   # bit-serial PUM: one lane per column
    "hbmpim": (1, "data/hbm_pim.json", 16),   # 256-bit PE / 16-bit data
}

OP_RE = re.compile(
    r"linalg\.(conv_2d_nchw_fchw|matmul|batch_matmul)\s*\{(?P<attrs>.*?)\}\s*"
    r"ins\((?P<ins>.*?)\)\s*outs\((?P<outs>.*?)\)")
TENSOR_RE = re.compile(r"tensor<([0-9x]+)xf32>")


# ---------------------------------------------------------------- parsing
DEFAULT_ATTRS = "global_layer_idx = 0 : i32, layer_group = 0 : i32, num_banks = 16 : i32, type_layer_idx = 0 : i32"


def layer_from_shape(spec):
    """'matmul:P=197,Q=768,R=768'  or  'conv:K=64,C=3,P=55,Q=55,R=11,S=11,stride=4'."""
    kind, _, rest = spec.partition(":")
    kv = {k: int(v) for k, v in (x.split("=") for x in rest.split(","))}
    if kind == "conv":
        s, d = kv.pop("stride", 1), kv.pop("dil", 1)
        b = dict(N=kv.get("N", 1), K=kv["K"], P=kv["P"], Q=kv["Q"], C=kv["C"], R=kv["R"], S=kv["S"])
        attrs = f"dilations = dense<{d}> : vector<2xi64>, {DEFAULT_ATTRS}, strides = dense<{s}> : vector<2xi64>"
        return dict(op="conv_2d_nchw_fchw", attrs=attrs, bounds=b, extra=dict(H=0, W=0, stride=s, dil=d))
    if kind == "matmul":
        return dict(op="matmul", attrs=DEFAULT_ATTRS, bounds=dict(P=kv["P"], Q=kv["Q"], R=kv["R"]), extra={})
    if kind == "batch_matmul":
        return dict(op="batch_matmul", attrs=DEFAULT_ATTRS,
                    bounds=dict(N=kv["N"], P=kv["P"], Q=kv["Q"], R=kv["R"]), extra={})
    sys.exit(f"[pad_search] bad --shape {spec}")


def parse_layer(path):
    text = open(path).read()
    m = OP_RE.search(text)
    if not m:
        sys.exit(f"[pad_search] no conv_2d_nchw_fchw / matmul / batch_matmul in {path}")
    op = m.group(1)
    attrs = m.group("attrs")
    shapes = [list(map(int, s.split("x"))) for s in TENSOR_RE.findall(m.group("ins") + m.group("outs"))]
    if op == "conv_2d_nchw_fchw":
        inp, fil, out = shapes[0], shapes[1], shapes[-1]
        stride = int(re.search(r"strides = dense<(\d+)>", attrs).group(1))
        dil = int(re.search(r"dilations = dense<(\d+)>", attrs).group(1))
        b = dict(N=inp[0], K=fil[0], P=out[2], Q=out[3], C=inp[1], R=fil[2], S=fil[3])
        extra = dict(H=inp[2], W=inp[3], stride=stride, dil=dil)
    elif op == "matmul":
        a, w = shapes[0], shapes[1]
        b = dict(P=a[0], Q=a[1], R=w[1])          # same names pim-opt uses (FC_P, FC_Q, FC_R)
        extra = {}
    else:
        a, w = shapes[0], shapes[1]
        b = dict(N=a[0], P=a[1], Q=a[2], R=w[2])
        extra = {}
    return dict(op=op, attrs=attrs, bounds=b, extra=extra)


def set_banks(attrs, banks):
    if banks is None:
        return attrs
    return re.sub(r"num_banks = \d+ : i32", f"num_banks = {banks} : i32", attrs)


# ---------------------------------------------------------------- MLIR writer
def t(dims):
    return "tensor<" + "x".join(str(d) for d in dims) + "xf32>"


def write_mlir(layer, b, banks):
    """Return a minimal, verifier-clean .mlir holding only the operator.

    pim-opt reads the loop bounds from the op's operand types only, so the
    bias / pad / transpose ops of the original file are not needed.
    """
    attrs = set_banks(layer["attrs"], banks)
    op = layer["op"]
    if op == "conv_2d_nchw_fchw":
        e = layer["extra"]
        need_h = (b["P"] - 1) * e["stride"] + (b["R"] - 1) * e["dil"] + 1
        need_w = (b["Q"] - 1) * e["stride"] + (b["S"] - 1) * e["dil"] + 1
        H, W = max(e["H"], need_h), max(e["W"], need_w)
        A, F, O = t([b["N"], b["C"], H, W]), t([b["K"], b["C"], b["R"], b["S"]]), t([b["N"], b["K"], b["P"], b["Q"]])
        body = (f"    %0 = linalg.conv_2d_nchw_fchw {{{attrs}}} ins(%arg0, %arg1 : {A}, {F}) "
                f"outs(%arg2 : {O}) -> {O}\n")
    elif op == "matmul":
        A, F, O = t([b["P"], b["Q"]]), t([b["Q"], b["R"]]), t([b["P"], b["R"]])
        body = f"    %0 = linalg.matmul {{{attrs}}} ins(%arg0, %arg1 : {A}, {F}) outs(%arg2 : {O}) -> {O}\n"
    else:
        A, F, O = t([b["N"], b["P"], b["Q"]]), t([b["N"], b["Q"], b["R"]]), t([b["N"], b["P"], b["R"]])
        body = f"    %0 = linalg.batch_matmul {{{attrs}}} ins(%arg0, %arg1 : {A}, {F}) outs(%arg2 : {O}) -> {O}\n"
    return ("module {\n"
            f"  func.func @forward(%arg0: {A}, %arg1: {F}, %arg2: {O}) -> {O} {{\n"
            + body +
            f"    return %0 : {O}\n  }}\n}}\n")


# ---------------------------------------------------------------- candidates
PADDABLE = {
    # R, S (kernel) and batch N are never padded.
    "conv_2d_nchw_fchw": ["PQ", "K", "C"],   # P and Q are padded together
    "matmul": ["P", "Q", "R"],
    "batch_matmul": ["P", "Q", "R"],
}


def largest_prime_factor(n):
    p, best = 2, 1
    while p * p <= n:
        while n % p == 0:
            best, n = p, n // p
        p += 1
    return max(best, n) if n > 1 else best


def dim_candidates(v, max_dim_pad, max_prime):
    """v itself plus every larger 'smooth' size within the per-dim limit."""
    if v <= 1:
        return [v]
    hi = math.floor(v * (1 + max_dim_pad))
    if v < 8:
        hi = max(hi, v + 1)  # tiny dims (C=3) may still go up by one
    out = [v] + [x for x in range(v + 1, hi + 1) if largest_prime_factor(x) <= max_prime]
    return out


def macs(b):
    return math.prod(b.values())


def best_lanes(bounds, banks, lanes_per_bank):
    """Largest bank*column parallelism reachable with exact divisors."""
    states = {(1, 1)}
    for v in bounds:
        divs = [d for d in range(1, v + 1) if v % d == 0]
        nxt = set()
        for (bp, cp) in states:
            for db in divs:
                if bp * db > banks:
                    break
                for dc in divs:
                    if (v // db) % dc:
                        continue
                    if cp * dc > lanes_per_bank:
                        break
                    nxt.add((bp * db, cp * dc))
        states = nxt
    return max(bp * cp for bp, cp in states)


def prescreen(b, banks, lanes_per_bank):
    """Rough compute-only proxy: sequential steps = padded MACs / usable lanes.

    Not the paper's cost model; it only ranks candidates so we spend ILP runs
    on promising ones.
    """
    return macs(b) / best_lanes(list(b.values()), banks, lanes_per_bank)


def candidates(layer, args, banks, lanes_per_bank):
    b0 = layer["bounds"]
    keys = PADDABLE[layer["op"]]
    opts = []
    for k in keys:
        base = b0["P"] if k == "PQ" else b0[k]
        opts.append(dim_candidates(base, args.max_dim_pad, args.max_prime))
    seen, cands = set(), []
    for combo in itertools.product(*opts):
        b = dict(b0)
        for k, v in zip(keys, combo):
            if k == "PQ":
                # keep the P/Q ratio for non-square outputs
                b["P"], b["Q"] = v, max(b0["Q"], round(v * b0["Q"] / b0["P"]))
            else:
                b[k] = v
        overhead = macs(b) / macs(b0) - 1
        if overhead > args.max_overhead + 1e-9:
            continue
        key = tuple(sorted(b.items()))
        if key in seen:
            continue
        seen.add(key)
        cands.append(dict(bounds=b, overhead=overhead, proxy=prescreen(b, banks, lanes_per_bank)))
    base = cands[0]          # combo of all first options == unpadded
    rest = sorted(cands[1:], key=lambda c: (c["proxy"], c["overhead"]))
    return [base] + rest[: args.top]


def tag(b0, b):
    diff = [f"{k}{b[k]}" for k in b if b[k] != b0[k]]
    return "unpadded" if not diff else "pad_" + "_".join(diff)


# ---------------------------------------------------------------- running
COST_RE = re.compile(r"Real Cost:\s*([-+0-9.eE]+)")


def run_pimopt(args, device, mlir_path, run_dir):
    dev_id, arch, _ = DEVICES[device]
    cmd = [args.pim_opt, "--data-layout-pass",
           "--trace-output-path", os.path.join(run_dir, "Group.txt"),
           "--model-debug-file", os.path.join(run_dir, "model.lp"),
           "--trans-coeff-method", "4",
           "--target-device-type", str(dev_id),
           "--number-counting-method", "0", "--obj-method", "0", "--storage-method", "0",
           "--config-arch-path", arch,
           "--config-knobs-path", args.knobs,
           mlir_path]
    # Gurobi 13 workaround: its presolve wrongly reports some HBM-PIM conv
    # models infeasible (3x3 conv at 32 banks), but turning presolve off made a
    # SIMDRAM matmul stop without solving. So by default "Presolve 0" is written
    # to gurobi.env (read from the working directory) for HBM-PIM runs only.
    # OPTIPIM_PRESOLVE_FIX: auto (default, HBM-PIM only) | 1 (all) | 0 (never).
    # An existing gurobi.env is never touched.
    for stale in ("Group.txt", "model.lp"):
        if os.path.exists(os.path.join(run_dir, stale)):
            os.remove(os.path.join(run_dir, stale))   # never reuse an old run's output
    mode = os.environ.get("OPTIPIM_PRESOLVE_FIX", "auto")
    want_off = mode == "1" or (mode == "auto" and device == "hbmpim")
    env_file, made_env = "gurobi.env", False
    if os.path.exists(env_file):
        print(f"[pad_search] note: using existing ./gurobi.env: {open(env_file).read().strip()!r}")
    elif want_off:
        with open(env_file, "w") as f:
            f.write("Presolve 0\n")
        made_env = True
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
        log = p.stdout + p.stderr
        status = "ok" if p.returncode == 0 else f"exit{p.returncode}"
    except subprocess.TimeoutExpired as e:
        log = (e.stdout or "") if isinstance(e.stdout, str) else ""
        log += "\n[pad_search] TIMEOUT\n"
        status = "timeout"
    finally:
        if made_env:
            os.remove(env_file)
    secs = time.time() - t0
    presolve = "off (gurobi.env)" if made_env else ("existing gurobi.env" if os.path.exists(env_file) else "Gurobi default")
    open(os.path.join(run_dir, "pim-opt.log"), "w").write(f"# presolve: {presolve}\n" + " ".join(cmd) + "\n\n" + log)
    costs = COST_RE.findall(log)
    if not costs:
        # No objective printed (e.g. "not proceeding further", infeasible):
        # the run failed, whatever trace file may exist.
        if status == "ok":
            status = "no_objective"
        trace = os.path.join(run_dir, "Group.txt")
        if os.path.exists(trace):
            os.rename(trace, trace + ".failed")
        return None, secs, status, presolve
    return float(costs[-1]), secs, status, presolve


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("layer", nargs="?", help="layer .mlir file (authors' nn_models/... format)")
    ap.add_argument("--shape", help="build the layer from a shape instead of a file, e.g. "
                    "'matmul:P=197,Q=768,R=768' or 'conv:K=64,C=3,P=55,Q=55,R=11,S=11,stride=4'")
    ap.add_argument("--name", help="layer name in the CSV (default: from the file name or the shape)")
    ap.add_argument("--device", choices=DEVICES, required=True)
    ap.add_argument("--banks", type=int, default=None, help="override num_banks (default: keep the file's value)")
    ap.add_argument("--max-dim-pad", type=float, default=0.25, help="max growth of one dim (0.25 = +25%%)")
    ap.add_argument("--max-overhead", type=float, default=0.30, help="max growth of total MACs")
    ap.add_argument("--max-prime", type=int, default=7, help="padded sizes must have no prime factor above this")
    ap.add_argument("--top", type=int, default=8, help="padded candidates to solve, best prescreen first")
    ap.add_argument("--pim-opt", default="./build/bin/pim-opt")
    ap.add_argument("--knobs", default="./data/knobs.json")
    ap.add_argument("--out", default="results/padding", help="output folder")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per pim-opt run")
    ap.add_argument("--dry-run", action="store_true", help="write .mlir files and list candidates, do not solve")
    args = ap.parse_args()

    if bool(args.layer) == bool(args.shape):
        sys.exit("[pad_search] give either a layer .mlir file or --shape")
    if args.shape:
        layer = layer_from_shape(args.shape)
        name = args.name or re.sub(r"[^A-Za-z0-9=]+", "_", args.shape)
    else:
        layer = parse_layer(args.layer)
        name = args.name or re.sub(r"^layerinfo\.|\.linalg\.mlir$", "", os.path.basename(args.layer))
    file_banks = int(re.search(r"num_banks = (\d+)", layer["attrs"]).group(1))
    banks = args.banks or file_banks
    lanes = DEVICES[args.device][2]
    b0 = layer["bounds"]
    print(f"[pad_search] {name} {layer['op']} bounds={b0} banks={banks} device={args.device}")

    cands = candidates(layer, args, banks, lanes)
    csv_path = os.path.join(args.out, "padding.csv")
    os.makedirs(args.out, exist_ok=True)
    new_file = not os.path.exists(csv_path)
    rows = []
    for c in cands:
        b = c["bounds"]
        variant = tag(b0, b)
        run_dir = os.path.join(args.out, name, args.device, variant)
        os.makedirs(run_dir, exist_ok=True)
        mlir_path = os.path.join(run_dir, "layer.mlir")
        open(mlir_path, "w").write(write_mlir(layer, b, args.banks))
        if args.dry_run:
            cost, secs, status, presolve = None, 0.0, "dry_run", ""
        else:
            cost, secs, status, presolve = run_pimopt(args, args.device, mlir_path, run_dir)
        row = dict(layer=name, device=args.device, variant=variant,
                   real_cost="" if cost is None else f"{cost:.6e}", solver_seconds=f"{secs:.0f}",
                   banks=banks, bounds=" ".join(f"{k}={v}" for k, v in b.items()),
                   mac_overhead=f"{c['overhead']:.4f}", proxy_steps=f"{c['proxy']:.1f}",
                   status=status, presolve=presolve)
        rows.append(row)
        print(f"  {variant:28s} +MACs {100*c['overhead']:5.1f}%  proxy {c['proxy']:10.1f}  "
              f"real_cost {row['real_cost'] or '-':>14s}  {secs:5.0f}s  {status}")

    with open(csv_path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new_file:
            w.writeheader()
        w.writerows(rows)

    solved = [r for r in rows if r["real_cost"]]
    if solved and rows[0]["real_cost"]:
        base = float(rows[0]["real_cost"])
        best = min(solved, key=lambda r: float(r["real_cost"]))
        print(f"[pad_search] best: {best['variant']}  cost {float(best['real_cost']):.4e}  "
              f"speedup vs unpadded {base / float(best['real_cost']):.3f}x")
    elif not args.dry_run:
        print(f"[pad_search] WARNING: unpadded run failed ({rows[0]['status']}); no speedup computed. "
              "See pim-opt.log in each run folder")
    failed = [r["variant"] for r in rows if r["status"] not in ("ok", "dry_run")]
    if failed:
        print(f"[pad_search] FAILED runs (no Real Cost): {', '.join(failed)}")
    print(f"[pad_search] rows appended to {csv_path}")


if __name__ == "__main__":
    main()
