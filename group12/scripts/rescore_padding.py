#!/usr/bin/env python3
"""Rescore all padding results with the authors' validated analytical cost model.

Reads:
  results/padding/<layer>/<device>/<variant>/Group.txt
  results/padding/padding.csv (for metadata like mac_overhead, solver_seconds)

Writes:
  results/padding/padding_analytical_all.csv       (detailed scores for all variants)
  results/padding/padding_analytical_summary.csv   (summary table for report)
  results/padding/padding_analytical_speedup.png   (speedup bar chart)
  results/padding/padding_analytical_tradeoff.png  (overhead vs speedup scatter)
"""
import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

# Insert validation folder for analytical modeling
sys.path.insert(0, "validation")
from analytical_modeling.analytical import ArchInfo, cal_performance_conv2D, cal_performance_FC
from analytical_modeling.parser_trace import TraceParser

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ARCH = {
    "hbmpim": ("data/hbm_pim.json", 1),
    "simdram": ("data/dram.json", 0)
}

COLORS = {"simdram": "#2a78d6", "hbmpim": "#eb6834"}
LABELS = {"simdram": "SIMDRAM", "hbmpim": "HBM-PIM"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def score_trace(trace_path, device, arch_info, dev_type):
    p = TraceParser(str(trace_path))
    if p.operation_type == "conv2d":
        ds = p.dilation_stride
        # pim-opt writes dilation, dilation, stride, stride
        dilation, stride = ds[0], ds[2]
        perf = cal_performance_conv2D(arch_info, p.get_loop_bounds(), p.get_trans_coeff(), stride, dilation, dev_type)
        n = 7
    else:
        perf = cal_performance_FC(arch_info, p.get_loop_bounds(), dev_type)
        n = 5

    banks = 1
    for b in p.bound[:n]:
        banks *= b

    return {
        "analytical_cost": perf.finalPerformance,
        "banks_used": banks,
        "inLoadingCost": getattr(perf, "inLoadingCost", 0),
        "outTransCost": getattr(perf, "outTransCost", 0),
        "numFilPELoading": getattr(perf, "numFilPELoading", 0),
    }


def main():
    root = Path("results/padding")
    csv_file = root / "padding.csv"
    if not csv_file.exists():
        sys.exit(f"Cannot find {csv_file}")

    # Load metadata from padding.csv
    meta = {}
    with open(csv_file, newline="") as f:
        for r in csv.DictReader(f):
            meta[(r["layer"], r["device"], r["variant"])] = r

    archs = {d: ArchInfo(f) for d, (f, _) in ARCH.items()}

    all_scored = []
    # Discover all Group.txt files
    for trace_file in sorted(root.glob("*/*/*/Group.txt")):
        parts = trace_file.parts
        # results/padding/<layer>/<device>/<variant>/Group.txt
        layer, device, variant = parts[-4], parts[-3], parts[-2]
        if device not in ARCH:
            continue

        arch_info, dev_type = archs[device], ARCH[device][1]
        try:
            scores = score_trace(trace_file, device, arch_info, dev_type)
        except Exception as e:
            print(f"Error scoring {trace_file}: {e}")
            continue

        m = meta.get((layer, device, variant), {})
        row = {
            "layer": layer,
            "device": device,
            "variant": variant,
            "analytical_cost": scores["analytical_cost"],
            "real_cost": m.get("real_cost", ""),
            "mac_overhead": m.get("mac_overhead", "0.0"),
            "banks_used": scores["banks_used"],
            "inLoadingCost": scores["inLoadingCost"],
            "outTransCost": scores["outTransCost"],
            "solver_seconds": m.get("solver_seconds", ""),
            "trace_path": str(trace_file),
        }
        all_scored.append(row)

    # Write all scored variants
    all_out = root / "padding_analytical_all.csv"
    if all_scored:
        with open(all_out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(all_scored[0].keys()))
            w.writeheader()
            w.writerows(all_scored)
        print(f"Wrote {len(all_scored)} scored variants to {all_out}")

    # Group by (layer, device)
    groups = defaultdict(list)
    for r in all_scored:
        groups[(r["layer"], r["device"])].append(r)

    summary = []
    scatter = defaultdict(list)

    for (layer, dev), rows in sorted(groups.items()):
        # Filter out invalid variants with non-positive cost
        valid_rows = [r for r in rows if r["analytical_cost"] > 0]
        if not valid_rows:
            print(f"Warning: {layer} on {dev} has no valid variants with cost > 0.")
            continue

        unpadded = [r for r in valid_rows if r["variant"] == "unpadded"]
        if not unpadded:
            print(f"Notice: {layer} on {dev} has no unpadded variant.")
            # If no unpadded (e.g. alexnet.l0 on simdram), take best padded and report unpadded as N/A
            best = min(valid_rows, key=lambda x: x["analytical_cost"])
            summary.append({
                "layer": layer,
                "device": dev,
                "unpadded_analytical_cost": "N/A",
                "best_variant": best["variant"],
                "best_analytical_cost": f"{best['analytical_cost']:.6e}",
                "mac_overhead": best["mac_overhead"],
                "speedup": "N/A",
                "gurobi_best_variant": meta.get((layer, dev, "best"), {}).get("best_variant", "")
            })
            continue

        base_cost = unpadded[0]["analytical_cost"]
        # Find best variant according to analytical cost!
        best = min(valid_rows, key=lambda x: x["analytical_cost"])
        speedup = base_cost / best["analytical_cost"]

        summary.append({
            "layer": layer,
            "device": dev,
            "unpadded_analytical_cost": f"{base_cost:.6e}",
            "best_variant": best["variant"],
            "best_analytical_cost": f"{best['analytical_cost']:.6e}",
            "mac_overhead": best["mac_overhead"],
            "speedup": f"{speedup:.4f}",
            "gurobi_best_variant": meta.get((layer, dev, "best"), {}).get("best_variant", "")
        })

        for r in valid_rows:
            if r["variant"] != "unpadded":
                ovh = 100 * float(r["mac_overhead"])
                sp = base_cost / r["analytical_cost"]
                scatter[dev].append((ovh, sp))

    summary_out = root / "padding_analytical_summary.csv"
    with open(summary_out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)
    print(f"Wrote analytical summary to {summary_out}")

    # Plot 1: Analytical Speedup Bar Chart
    valid_summary = [s for s in summary if s["speedup"] != "N/A"]
    layers = sorted({s["layer"] for s in valid_summary})
    devs = [d for d in COLORS if any(s["device"] == d for s in valid_summary)]
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    width = 0.8 / len(devs)
    for i, d in enumerate(devs):
        vals = {s["layer"]: float(s["speedup"]) for s in valid_summary if s["device"] == d}
        xs = [j + (i - (len(devs) - 1) / 2) * width for j in range(len(layers))]
        ys = [vals.get(l, float("nan")) for l in layers]
        ax.bar(xs, ys, width - 0.04, color=COLORS[d], label=LABELS[d], edgecolor="white", linewidth=1)
        for x, y in zip(xs, ys):
            if y == y and y > 1.005:
                ax.text(x, y + 0.015, f"{y:.2f}x", ha="center", va="bottom", fontsize=8, color=INK, fontweight="bold")
            elif y == y:
                ax.text(x, y + 0.015, f"{y:.2f}x", ha="center", va="bottom", fontsize=8, color=INK2)

    ax.axhline(1.0, color=INK2, linewidth=1, linestyle="--")
    ax.set_xticks(range(len(layers)))
    ax.set_xticklabels(layers, rotation=25, ha="right", fontsize=8.5)
    ax.set_ylabel("Speedup vs Unpadded\n(Validated Analytical Model)", color=INK, fontsize=9.5)
    ax.set_ylim(0.85, max(float(s["speedup"]) for s in valid_summary) * 1.15)
    style(ax)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(root / "padding_analytical_speedup.png", dpi=250)

    # Plot 2: Trade-off Scatter Plot
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    for d in devs:
        if scatter[d]:
            xs, ys = zip(*scatter[d])
            ax.scatter(xs, ys, s=32, color=COLORS[d], label=LABELS[d], edgecolors="white", linewidths=0.8, alpha=0.85)
    ax.axhline(1.0, color=INK2, linewidth=1, linestyle="--")
    ax.set_xlabel("Extra MACs from Padding (%)", color=INK, fontsize=9.5)
    ax.set_ylabel("Analytical Model Speedup vs Unpadded", color=INK, fontsize=9.5)
    style(ax)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(root / "padding_analytical_tradeoff.png", dpi=250)
    print("Plots saved successfully!")


if __name__ == "__main__":
    main()
