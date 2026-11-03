#!/usr/bin/env python3
"""Plot analytical vs simulator correlation (reproducing paper Figure 9).

Task 3.4:
Evaluates the correlation between the Python analytical model and the Ramulator2
cycle-accurate simulator across all benchmark operators (C1-C5/M2 for both OptiPIM
and heuristic mappings) as well as the authors' validation datasets.
Generates a 2-panel log-log plot with linear regression and R^2 values.
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
COLORS = {"hbmpim": "#2a78d6", "simdram": "#eb6834"}
TITLES = {"hbmpim": "HBM-PIM (Near-Bank)", "simdram": "SIMDRAM (In-DRAM)"}


def style_ax(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.grid(True, which="both", color=GRID, linewidth=0.6, linestyle=":")
    ax.set_axisbelow(True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", default="group12/results/results.csv",
                        help="Path to group12 results.csv")
    parser.add_argument("--fig9-dir", default="exp_results/fig9",
                        help="Path to authors' fig9 validation directory")
    parser.add_argument("--out", default="group12/results/plots/fig9_correlation.png",
                        help="Output path for the figure")
    args = parser.parse_args()

    results_path = Path(args.results)
    if not results_path.exists():
        sys.exit(f"Results file not found: {results_path}")

    df_our = pd.read_csv(results_path)
    df_our["simulated_cycles"] = pd.to_numeric(df_our["simulated_cycles"], errors="coerce")
    df_our = df_our.dropna(subset=["simulated_cycles", "analytical_cycles"])

    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.0))

    for ax, dev in zip(axes, ["hbmpim", "simdram"]):
        sub = df_our[df_our["target"] == dev].copy()
        
        # Load authors' validation data if available
        auth_file = Path(args.fig9_dir) / f"validation_{dev}.csv"
        if auth_file.exists():
            df_auth = pd.read_csv(auth_file).dropna(subset=["Analytical", "Simulation"])
            # Sample for cleaner plotting if very large
            if len(df_auth) > 500:
                df_auth_sample = df_auth.sample(n=500, random_state=42)
            else:
                df_auth_sample = df_auth
            ax.scatter(df_auth_sample["Analytical"], df_auth_sample["Simulation"],
                       color="#c0c0c0", alpha=0.35, s=15, label="Authors' validation (random)", zorder=1)

        # Plot our benchmark mappings
        for mapper, marker, label in [("optipim", "o", "OptiPIM (Ours)"), ("heuristic", "s", "Heuristic (Ours)")]:
            m_sub = sub[sub["mapper"] == mapper]
            ax.scatter(m_sub["analytical_cycles"], m_sub["simulated_cycles"],
                       color=COLORS[dev], edgecolors=INK, linewidth=0.8,
                       marker=marker, s=55, alpha=0.9, label=label, zorder=3)
            # Label the points with operator name
            for _, r in m_sub.iterrows():
                ax.annotate(r["operator"], (r["analytical_cycles"], r["simulated_cycles"]),
                            xytext=(4, -3), textcoords="offset points", fontsize=7, color=INK)

        # Compute regression and R2 on our data
        x = sub["analytical_cycles"]
        y = sub["simulated_cycles"]
        log_x = np.log10(x)
        log_y = np.log10(y)
        slope, intercept, r_val, _, _ = stats.linregress(log_x, log_y)
        r2_log = r_val ** 2
        r2_linear = np.corrcoef(x, y)[0, 1] ** 2

        # Plot ideal y=x reference line
        all_vals = np.concatenate([x.values, y.values])
        min_v = 10 ** (np.floor(np.log10(all_vals.min())))
        max_v = 10 ** (np.ceil(np.log10(all_vals.max())))
        ax.plot([min_v, max_v], [min_v, max_v], "--", color="#888888", linewidth=1.0, label="Ideal y = x", zorder=2)

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(min_v * 0.5, max_v * 2.0)
        ax.set_ylim(min_v * 0.5, max_v * 2.0)
        ax.set_xlabel("Analytical Model Cycles (log)", fontsize=8.5, color=INK2)
        ax.set_ylabel("Ramulator2 Simulated Cycles (log)", fontsize=8.5, color=INK2)
        ax.set_title(f"{TITLES[dev]}\nBenchmark $R^2_{{\\log}} = {r2_log:.4f}$ ($R^2_{{\\text{{lin}}}} = {r2_linear:.4f}$)",
                     fontsize=9.5, color=INK)
        style_ax(ax)
        ax.legend(frameon=False, fontsize=7.5, loc="upper left")

    fig.tight_layout()
    out_p = Path(args.out)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_p, dpi=250)
    plt.close(fig)
    print(f"Generated Figure 9 correlation plot at: {out_p}")


if __name__ == "__main__":
    main()
