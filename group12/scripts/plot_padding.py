#!/usr/bin/env python3
"""Plots for the padding extension, made only from padding.csv.

  python3 group12/scripts/plot_padding.py results/padding/padding.csv --out results/padding

Writes:
  padding_speedup.png   best padded variant vs unpadded, per layer and device
  padding_tradeoff.png  every candidate: extra MACs vs speedup
  padding_summary.csv   one row per (layer, device): unpadded cost, best variant, speedup
"""
import argparse
import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COLORS = {"simdram": "#2a78d6", "hbmpim": "#eb6834"}   # fixed order: series 1, series 2
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()

    # Keep the last run of each (layer, device, variant) in case of reruns;
    # if that last run failed (no Real Cost), the variant is dropped, not
    # replaced by an older result.
    rows = {}
    for r in csv.DictReader(open(a.csv)):
        rows[(r["layer"], r["device"], r["variant"])] = r
    rows = {k: r for k, r in rows.items() if r["real_cost"]}
    groups = defaultdict(list)
    for (layer, dev, _), r in rows.items():
        groups[(layer, dev)].append(r)

    summary, scatter = [], defaultdict(list)
    for (layer, dev), rs in groups.items():
        base = [r for r in rs if r["variant"] == "unpadded"]
        if not base:
            continue
        c0 = float(base[0]["real_cost"])
        best = min(rs, key=lambda r: float(r["real_cost"]))
        summary.append(dict(layer=layer, device=dev, unpadded_cost=f"{c0:.6e}",
                            best_variant=best["variant"], best_cost=f"{float(best['real_cost']):.6e}",
                            mac_overhead=best["mac_overhead"], speedup=f"{c0 / float(best['real_cost']):.4f}"))
        for r in rs:
            if r["variant"] != "unpadded":
                scatter[dev].append((100 * float(r["mac_overhead"]), c0 / float(r["real_cost"])))

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "padding_summary.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(sorted(summary, key=lambda s: (s["layer"], s["device"])))

    # Figure 1: grouped bars, speedup of the best variant (1.0 = padding not chosen)
    layers = sorted({s["layer"] for s in summary})
    devs = [d for d in COLORS if any(s["device"] == d for s in summary)]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    width = 0.8 / len(devs)
    for i, d in enumerate(devs):
        vals = {s["layer"]: float(s["speedup"]) for s in summary if s["device"] == d}
        xs = [j + (i - (len(devs) - 1) / 2) * width for j in range(len(layers))]
        ys = [vals.get(l, float("nan")) for l in layers]
        ax.bar(xs, ys, width - 0.04, color=COLORS[d], label=LABELS[d], edgecolor="white", linewidth=1)
        for x, y in zip(xs, ys):
            if y == y and y > 1.005:
                ax.text(x, y + 0.01, f"{y:.2f}x", ha="center", va="bottom", fontsize=8, color=INK)
    ax.axhline(1.0, color=INK2, linewidth=1, linestyle="--")
    ax.set_xticks(range(len(layers)))
    ax.set_xticklabels(layers, rotation=25, ha="right")
    ax.set_ylabel("Speedup vs unpadded\n(analytical Real Cost)", color=INK, fontsize=9)
    lo = min(0.9, min(float(s["speedup"]) for s in summary) - 0.05)
    ax.set_ylim(lo, max(1.1, max(float(s["speedup"]) for s in summary) + 0.1))
    style(ax)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(os.path.join(a.out, "padding_speedup.png"), dpi=200)

    # Figure 2: trade-off of every padded candidate
    fig, ax = plt.subplots(figsize=(5, 3.2))
    for d in devs:
        if scatter[d]:
            xs, ys = zip(*scatter[d])
            ax.scatter(xs, ys, s=28, color=COLORS[d], label=LABELS[d], edgecolors="white", linewidths=1)
    ax.axhline(1.0, color=INK2, linewidth=1, linestyle="--")
    ax.set_xlabel("Extra MACs from padding (%)", color=INK, fontsize=9)
    ax.set_ylabel("Speedup vs unpadded", color=INK, fontsize=9)
    style(ax)
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(a.out, "padding_tradeoff.png"), dpi=200)
    print(f"[plot_padding] wrote padding_speedup.png, padding_tradeoff.png, padding_summary.csv to {a.out}")


if __name__ == "__main__":
    main()
