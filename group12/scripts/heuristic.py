#!/usr/bin/env python3
"""Baseline Weight-Parallel Heuristic Trace Generator for OptiPIM.

Implements the weight-parallel mapping heuristic from the paper (Section 6.4.1):
"OptiPIM: Optimizing Processing-in-Memory Acceleration Using Integer Linear Programming"
(ISCA 2025).

Rules (Paper Sec. 6.4.1 & TEAM_TASKS.md Tasks 2.1, 2.2, 2.4):
1. Tile weights to SIMD-lane size (16 FP16 lanes on HBM-PIM, a full row on SIMDRAM).
2. Distribute tiles bank -> column -> row.
3. Output channels K (conv2d) / Q (gemm) mapped to Level 2 (banks) first:
   - For conv2d: K2 = min(K, num_banks)
   - For gemm: N2 = min(N, num_banks) (if N > 1, for batched gemm), Q2 = min(Q, num_banks // N2)
4. Every output accumulation stays within one bank (no cross-bank reduction for outputs).
5. Inputs and reduction loops (C, R, S for conv; R for gemm) streamed temporally at Level 0.
6. Flexible indexing uses stride-1 raster order:
   Coeff_X2,X0,X1 has c0 = 1, c1 = X0, c2 = X0 * X1.

Usage:
  # By benchmark operator ID (C1, C2, C3, M1, M2):
  python3 group12/scripts/heuristic.py C1 hbmpim > group12/mappings/hbmpim/C1/heuristic.trace
  python3 group12/scripts/heuristic.py M1 simdram > group12/mappings/simdram/M1/heuristic.trace

  # By MLIR file path:
  python3 group12/scripts/heuristic.py group12/operators/C1.mlir hbmpim

  # By custom/padded shape string (Task 2.4 support for Member 4):
  python3 group12/scripts/heuristic.py --shape 'matmul:P=197,Q=768,R=768' simdram
  python3 group12/scripts/heuristic.py --shape 'batch_matmul:N=12,P=197,Q=64,R=197' simdram
  python3 group12/scripts/heuristic.py --shape 'conv:K=64,C=3,P=55,Q=55,R=11,S=11,stride=4' hbmpim
"""

import argparse
import re
import sys
from pathlib import Path


# Standard benchmark operators (32 banks, 16-bit FP16)
KNOWN_OPS = {
    # Conv2D operators: (type, N, K, P, Q, C, R, S, stride, dilation)
    "C1": {
        "type": "conv2d",
        "N": 1,
        "K": 128,
        "P": 28,
        "Q": 28,
        "C": 128,
        "R": 3,
        "S": 3,
        "stride": 2,
        "dilation": 1,
        "desc": "ResNet-50 conv12 (3x3 conv, stride 2, paper Fig. 12)",
    },
    "C2": {
        "type": "conv2d",
        "N": 1,
        "K": 64,
        "P": 56,
        "Q": 56,
        "C": 64,
        "R": 3,
        "S": 3,
        "stride": 1,
        "dilation": 1,
        "desc": "ResNet-50 conv2 (3x3 conv, stride 1)",
    },
    "C3": {
        "type": "conv2d",
        "N": 1,
        "K": 64,
        "P": 56,
        "Q": 56,
        "C": 64,
        "R": 1,
        "S": 1,
        "stride": 1,
        "dilation": 1,
        "desc": "ResNet-50 conv1 (1x1 conv, stride 1)",
    },
    # GEMM operators (M1, M2)
    "M1": {
        "type": "gemm",
        "N": 1,
        "H": 1,
        "P": 128,
        "Q": 768,
        "R": 768,
        "stride": 1,
        "dilation": 1,
        "desc": "BERT fc0 (128x768 @ 768x768)",
    },
    "M2": {
        "type": "gemm",
        "N": 12,
        "H": 1,
        "P": 128,
        "Q": 64,
        "R": 128,
        "stride": 1,
        "dilation": 1,
        "desc": "BERT fc1 (batched 12x128x64 @ 64x128)",
    },
}

OP_RE = re.compile(
    r"linalg\.(conv_2d_nchw_fchw|matmul|batch_matmul)\s*\{(?P<attrs>.*?)\}\s*"
    r"ins\((?P<ins>.*?)\)\s*outs\((?P<outs>.*?)\)"
)
TENSOR_RE = re.compile(r"tensor<([0-9x]+)xf32>")


def parse_mlir_file(path):
    """Parse operator parameters from an MLIR file."""
    text = Path(path).read_text(encoding="utf-8")
    m = OP_RE.search(text)
    if not m:
        raise ValueError(f"No conv_2d_nchw_fchw / matmul / batch_matmul found in {path}")
    op = m.group(1)
    attrs = m.group("attrs")
    shapes = [list(map(int, s.split("x"))) for s in TENSOR_RE.findall(m.group("ins") + m.group("outs"))]

    if op == "conv_2d_nchw_fchw":
        inp, fil, out = shapes[0], shapes[1], shapes[-1]
        stride_m = re.search(r"strides = dense<(\d+)>", attrs)
        dil_m = re.search(r"dilations = dense<(\d+)>", attrs)
        stride = int(stride_m.group(1)) if stride_m else 1
        dil = int(dil_m.group(1)) if dil_m else 1
        return {
            "type": "conv2d",
            "N": inp[0],
            "K": fil[0],
            "P": out[2],
            "Q": out[3],
            "C": inp[1],
            "R": fil[2],
            "S": fil[3],
            "stride": stride,
            "dilation": dil,
        }
    elif op == "matmul":
        a, w = shapes[0], shapes[1]
        return {
            "type": "gemm",
            "N": 1,
            "H": 1,
            "P": a[0],
            "Q": a[1],
            "R": w[1],
            "stride": 1,
            "dilation": 1,
        }
    else:  # batch_matmul
        a, w = shapes[0], shapes[1]
        return {
            "type": "gemm",
            "N": a[0],
            "H": 1,
            "P": a[1],
            "Q": a[2],
            "R": w[2],
            "stride": 1,
            "dilation": 1,
        }


def parse_shape_spec(spec):
    """Parse custom shape spec string like 'matmul:P=197,Q=768,R=768' (Task 2.4)."""
    kind, _, rest = spec.partition(":")
    kv = {k: int(v) for k, v in (x.split("=") for x in rest.split(","))}

    if kind in ("conv", "conv2d"):
        stride = kv.pop("stride", 1)
        dil = kv.pop("dil", kv.pop("dilation", 1))
        return {
            "type": "conv2d",
            "N": kv.get("N", 1),
            "K": kv["K"],
            "P": kv["P"],
            "Q": kv["Q"],
            "C": kv["C"],
            "R": kv["R"],
            "S": kv["S"],
            "stride": stride,
            "dilation": dil,
        }
    elif kind == "matmul":
        return {
            "type": "gemm",
            "N": 1,
            "H": 1,
            "P": kv["P"],
            "Q": kv["Q"],
            "R": kv["R"],
            "stride": 1,
            "dilation": 1,
        }
    elif kind == "batch_matmul":
        return {
            "type": "gemm",
            "N": kv["N"],
            "H": kv.get("H", 1),
            "P": kv["P"],
            "Q": kv["Q"],
            "R": kv["R"],
            "stride": 1,
            "dilation": 1,
        }
    else:
        raise ValueError(f"Unknown shape type in --shape: {spec}")


def normalize_device(target):
    target = target.lower()
    if target in ("hbm", "hbmpim", "nbp"):
        return "hbmpim"
    elif target in ("simdram", "pum", "dram"):
        return "simdram"
    else:
        raise ValueError(f"Unknown target device: {target}")


def generate_conv2d_trace(op_cfg, target, num_banks=32):
    """Generate mapping trace for a Conv2D operator using the weight-parallel heuristic."""
    N = op_cfg["N"]
    K = op_cfg["K"]
    P = op_cfg["P"]
    Q = op_cfg["Q"]
    C = op_cfg["C"]
    R = op_cfg["R"]
    S = op_cfg["S"]
    stride = op_cfg.get("stride", 1)
    dilation = op_cfg.get("dilation", 1)

    device = normalize_device(target)

    # 1. Level 2 (Banks):
    # Output channels (K) assigned to banks first.
    K2 = 1
    for d in range(min(K, num_banks), 0, -1):
        if K % d == 0:
            K2 = d
            break

    N2, P2, Q2, C2, R2, S2 = 1, 1, 1, 1, 1, 1
    K_rem = K // K2

    # 2. Level 1 (Columns) & Level 0 (Time):
    if device == "hbmpim":
        # HBM-PIM: PE SIMD width is 16 lanes.
        # Weights partitioned across columns. Output height P mapped to columns.
        # Output width Q is tiled to columns (Q1 = 4 if divisible, else largest divisor <= 4).
        K1 = K_rem
        P1 = P
        Q1 = 1
        for d in [4, 2, 1]:
            if Q % d == 0:
                Q1 = d
                break
        N1, C1, R1, S1 = 1, 1, 1, 1

        # Level 0 (Time): inputs and reductions streamed sequentially
        N0 = 1
        K0 = 1
        P0 = 1
        Q0 = Q // Q1
        C0 = C
        R0 = R
        S0 = S

        loop_line = "Loop: N,K,P,Q,C,R,S,N,K,P,Q,C,R,S,N,K,P,Q,C,R,S"

    else:
        # SIMDRAM: Entire DRAM row (8192 columns / 16 bits = 512 elements) available.
        # Full Q is mapped across columns (Q1 = Q), so Q0 = 1.
        K1 = K_rem
        P1 = P
        Q1 = Q
        N1, C1, R1, S1 = 1, 1, 1, 1

        # Level 0 (Time)
        N0 = 1
        K0 = 1
        P0 = 1
        Q0 = 1
        C0 = C
        R0 = R
        S0 = S

        # Reference SIMDRAM loop order:
        # For 1x1 conv (C3): innermost loop ends with R,S,C; for 3x3 conv (C1, C2): ends with R,C,S
        if R == 1 and S == 1:
            loop_line = "Loop: N,K,P,Q,C,R,S,N,K,P,Q,C,R,S,N,K,P,Q,R,S,C"
        else:
            loop_line = "Loop: N,K,P,Q,C,R,S,N,K,P,Q,C,R,S,N,K,P,Q,R,C,S"

    # Verify factorization
    assert N2 * N0 * N1 == N
    assert K2 * K0 * K1 == K
    assert P2 * P0 * P1 == P
    assert Q2 * Q0 * Q1 == Q
    assert C2 * C0 * C1 == C
    assert R2 * R0 * R1 == R
    assert S2 * S0 * S1 == S

    # Build Bound list: Level 2, Level 0, Level 1
    b_l2 = [N2, K2, P2, Q2, C2, R2, S2]
    b_l0 = [N0, K0, P0, Q0, C0, R0, S0]
    b_l1 = [N1, K1, P1, Q1, C1, R1, S1]
    bound_values = b_l2 + b_l0 + b_l1

    # Coefficients for flexible indexing (stride-1 raster order)
    # c0 = 1, c1 = X0, c2 = X0 * X1
    dims = [
        ("N", N0, N1),
        ("K", K0, K1),
        ("P", P0, P1),
        ("Q", Q0, Q1),
        ("C", C0, C1),
        ("R", R0, R1),
        ("S", S0, S1),
    ]
    coeff_lines = []
    for name, x0, x1 in dims:
        c0 = 1
        c1 = x0
        c2 = x0 * x1
        coeff_lines.append(f"Coeff_{name}2,{name}0,{name}1: {c2},{c0},{c1}")

    lines = [
        "conv2d",
        f"Problem: {N},{K},{P},{Q},{C},{R},{S}",
        f"DilationStride: {stride},{stride},{dilation},{dilation}",
        loop_line,
        f"Bound: {','.join(str(v) for v in bound_values)}",
        "Tag: P,P,P,P,P,P,P,T,T,T,T,T,T,T,P,P,P,P,P,P,P",
        "StartBankRow: 0,0",
    ]
    lines.extend(coeff_lines)
    lines.append("end")

    return "\n".join(lines) + "\n"


def generate_gemm_trace(op_cfg, target, num_banks=32):
    """Generate mapping trace for a GEMM operator using the weight-parallel heuristic."""
    N = op_cfg["N"]
    H = op_cfg.get("H", 1)
    P = op_cfg["P"]
    Q = op_cfg["Q"]
    R = op_cfg["R"]
    stride = op_cfg.get("stride", 1)
    dilation = op_cfg.get("dilation", 1)

    device = normalize_device(target)

    # 1. Level 2 (Banks):
    # If batched (N > 1), distribute batch across banks first.
    # Then distribute output features Q across remaining banks.
    if N > 1:
        N2 = min(N, num_banks)
        banks_for_Q = num_banks // N2
    else:
        N2 = 1
        banks_for_Q = num_banks

    # Q2 is the largest divisor of Q that is <= banks_for_Q
    Q2 = 1
    for d in range(min(Q, banks_for_Q), 0, -1):
        if Q % d == 0:
            Q2 = d
            break

    H2, P2, R2 = 1, 1, 1

    # 2. Level 1 (Columns) & Level 0 (Time):
    # Output features remaining per bank map to Level 1
    Q1 = Q // Q2
    Q0 = 1

    # Sequence length P maps to Level 0 (sequential batches)
    P0 = P
    P1 = 1

    N0, N1 = 1, N // N2
    H0, H1 = 1, 1

    # Reduction dimension R:
    if device == "hbmpim":
        # HBM-PIM: weights tiled to 16 FP16 SIMD lanes
        R1 = 1
        for d in [16, 8, 4, 2, 1]:
            if R % d == 0:
                R1 = d
                break
        R0 = R // R1
    else:
        # SIMDRAM: weights tiled to full row / power of 2 sub-array width
        # For M1 (R=768): R1 = 256; for M2 (R=128): R1 = 128
        if R % 256 == 0:
            R1 = 256
        else:
            R1 = min(R, 256)
            while R % R1 != 0 and R1 > 1:
                R1 //= 2
        R0 = R // R1

    # Verify factorization
    assert N2 * N0 * N1 == N
    assert H2 * H0 * H1 == H
    assert P2 * P0 * P1 == P
    assert Q2 * Q0 * Q1 == Q
    assert R2 * R0 * R1 == R

    # Format trace:
    # Loop order:
    # Level 2: N, H, Q, P, R
    # Level 0: N, H, P, Q, R
    # Level 1: N, H, Q, R, P
    loop_line = "Loop: N,H,Q,P,R,N,H,P,Q,R,N,H,Q,R,P"

    # Bound line: Level 2, Level 0, Level 1
    b_l2 = [N2, H2, Q2, P2, R2]
    b_l0 = [N0, H0, P0, Q0, R0]
    b_l1 = [N1, H1, Q1, R1, P1]
    bound_values = b_l2 + b_l0 + b_l1

    # Tag line: 5 P's, 5 T's, 5 P's
    tag_line = "Tag: P,P,P,P,P,T,T,T,T,T,P,P,P,P,P"

    # Coefficients for flexible indexing (stride-1 raster order)
    # In order: N, H, P, Q, R
    dims = [
        ("N", N0, N1),
        ("H", H0, H1),
        ("P", P0, P1),
        ("Q", Q0, Q1),
        ("R", R0, R1),
    ]
    coeff_lines = []
    for name, x0, x1 in dims:
        c0 = 1
        c1 = x0
        c2 = x0 * x1
        coeff_lines.append(f"Coeff_{name}2,{name}0,{name}1: {c2},{c0},{c1}")

    lines = [
        "gemm",
        f"Problem: {N},{H},{P},{Q},{R}",
        f"DilationStride: {stride},{stride},{dilation},{dilation}",
        loop_line,
        f"Bound: {','.join(str(v) for v in bound_values)}",
        tag_line,
        "StartBankRow: 0,0",
    ]
    lines.extend(coeff_lines)
    lines.append("end")

    return "\n".join(lines) + "\n"


def generate_trace(op_name_or_cfg, target, num_banks=32):
    """Dispatcher to generate mapping trace for an operator."""
    if isinstance(op_name_or_cfg, str):
        op_key = op_name_or_cfg.upper()
        if op_key in KNOWN_OPS:
            op_cfg = KNOWN_OPS[op_key]
        elif Path(op_name_or_cfg).exists():
            op_cfg = parse_mlir_file(op_name_or_cfg)
        else:
            raise ValueError(f"Unknown operator or file: {op_name_or_cfg}. Supported: {list(KNOWN_OPS.keys())}")
    else:
        op_cfg = op_name_or_cfg

    if op_cfg["type"] == "conv2d":
        return generate_conv2d_trace(op_cfg, target, num_banks)
    elif op_cfg["type"] == "gemm":
        return generate_gemm_trace(op_cfg, target, num_banks)
    else:
        raise ValueError(f"Unsupported operation type: {op_cfg['type']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("operator", nargs="?", default=None,
                        help="Operator ID (e.g. C1, C2, C3, M1, M2) or path to .mlir file")
    parser.add_argument("target", choices=["hbmpim", "simdram", "hbm", "pum"], help="Target architecture")
    parser.add_argument("--shape", type=str, default=None,
                        help="Custom shape spec (e.g. 'matmul:P=197,Q=768,R=768' for Task 2.4)")
    parser.add_argument("--banks", type=int, default=32, help="Number of banks (default: 32)")
    parser.add_argument("--out", type=str, default=None, help="Output file path (default: stdout)")

    args = parser.parse_args()

    if args.shape:
        op_cfg = parse_shape_spec(args.shape)
    elif args.operator:
        if args.operator.upper() in KNOWN_OPS:
            op_cfg = KNOWN_OPS[args.operator.upper()]
        elif Path(args.operator).exists():
            op_cfg = parse_mlir_file(args.operator)
        else:
            print(f"Error: unknown operator '{args.operator}'. Supported: {list(KNOWN_OPS.keys())}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Error: must provide either operator argument or --shape", file=sys.stderr)
        sys.exit(1)

    try:
        trace_content = generate_trace(op_cfg, args.target, args.banks)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(trace_content, encoding="utf-8")
        print(f"Wrote trace to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(trace_content)


if __name__ == "__main__":
    main()
