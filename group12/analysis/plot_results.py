#!/usr/bin/env python3
"""Figures and a summary table for the 5-operator baseline (C1 C2 C3 M1 M2).

Inputs
  --scores       output of score_traces.py: operator,device,mapper,cost,...
                 (OptiPIM and heuristic traces, same cost model)  [required]
  --solve-times  group12/results/solve_times.csv:
                 operator,target,arch,wall_seconds,gurobi_seconds,objective,status
  --sim          group12/results/sim_check.csv:
                 operator,target,mapper,simulated_cycles,sim_seconds
  Missing optional files only skip the figures that need them.

Outputs (in --outdir)
  cost_per_operator.png  one panel per device, bars per mapper, log y-axis
  speedup.png            heuristic cost / OptiPIM cost (above 1 = OptiPIM faster)
  analytical_vs_sim.png  simulator cycles / analytical cost, per operator
  objective_vs_model.png analytical cost / Gurobi objective, per operator
  summary.csv            every number above in one table

Absolute costs are never compared across devices (different formulas and
arch files; units not verified to be the same clock), so those figures use
one panel per device or unit-free ratios.

Example:
    python plot_results.py --scores scores.csv \
        --solve-times ../results/solve_times.csv --sim ../results/sim_check.csv \
        --outdir ../results/plots
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

OPS = ["C1", "C2", "C3", "M1", "M2"]
DEVICES = ["hbmpim", "simdram"]
DEVICE_LABEL = {"simdram": "SIMDRAM", "hbmpim": "HBM-PIM"}
# Fixed colours: a mapper / device keeps its colour in every figure.
MAPPER_COLOR = {"optipim": "#2a78d6", "heuristic_1": "#eb6834",
                "heuristic_2": "#1baf7a"}
DEVICE_COLOR = {"hbmpim": "#2a78d6", "simdram": "#eb6834"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def order(ops):
    known = [o for o in OPS if o in ops]
    return known + sorted(o for o in ops if o not in OPS)


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def grouped_bars(ax, table, colors, labels=None, fmt=None):
    """table: index = x categories, columns = series."""
    n = len(table.columns)
    w = 0.8 / max(n, 1)
    for i, col in enumerate(table.columns):
        xs = [j + (i - (n - 1) / 2) * w for j in range(len(table.index))]
        ax.bar(xs, table[col], width=w * 0.92, color=colors.get(col, "#6250d6"),
               label=(labels or {}).get(col, col))
        if fmt:
            for xv, v in zip(xs, table[col]):
                if pd.notna(v):
                    ax.annotate(fmt(v), (xv, v), xytext=(0, 2),
                                textcoords="offset points", ha="center",
                                fontsize=6.5, color=INK)
    ax.set_xticks(range(len(table.index)))
    ax.set_xticklabels(table.index)


def ratio_figure(table, ylabel, title, path, ref=1.0, log=False, fmt="{:.2f}"):
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    grouped_bars(ax, table, DEVICE_COLOR, DEVICE_LABEL, fmt=lambda v: fmt.format(v))
    if ref is not None:
        ax.axhline(ref, color=INK2, linestyle="--", linewidth=1)
    if log:
        ax.set_yscale("log")
    ax.set_ylabel(ylabel, color=INK2, fontsize=8)
    ax.set_title(title, color=INK, fontsize=9.5)
    style(ax)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


PART_COLOR = {"input loading": "#6250d6", "weight loading": "#e87ba4",
              "output": "#008300", "compute": "#eda100"}


def breakdown(row):
    """Split the model's total the way analytical.py adds it up.
    HBM-PIM: input loading + weight (filter) loading + row activations (compute).
    SIMDRAM: input loading + output transfer + bit-serial mul/add (compute)."""
    inp = row["inLoadingCost"]
    if row["device"] == "hbmpim":
        w, o = row["numFilPELoading"], 0.0
    else:
        w, o = 0.0, row["outTransCost"]
    return {"input loading": inp, "weight loading": w, "output": o,
            "compute": row["cost"] - inp - w - o}


def plot_breakdown(sc, ops, baseline, path):
    sel = sc[sc["mapper"].isin(["optipim", baseline])].copy()
    parts = pd.DataFrame([breakdown(r) for _, r in sel.iterrows()], index=sel.index)
    sel = pd.concat([sel, parts], axis=1)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4), sharey=True)
    for ax, dev in zip(axes, DEVICES):
        d = sel[sel["device"] == dev]
        xs, labels = [], []
        for j, op in enumerate(ops):
            for k, m in enumerate(["optipim", baseline]):
                r = d[(d["operator"] == op) & (d["mapper"] == m)]
                if r.empty:
                    continue
                r = r.iloc[0]
                x = j * 2.6 + k * 1.05
                bottom = 0.0
                for p, c in PART_COLOR.items():
                    share = 100 * r[p] / r["cost"]
                    ax.bar(x, share, bottom=bottom, width=0.95, color=c,
                           edgecolor="white", linewidth=0.6,
                           label=p if (j == 0 and k == 0) else None)
                    bottom += share
                xs.append(x)
                labels.append(f"{op}\n{'Opt' if m == 'optipim' else 'Heu'}")
        ax.set_xticks(xs)
        ax.set_xticklabels(labels, fontsize=6.5)
        ax.set_ylim(0, 100)
        ax.set_title(DEVICE_LABEL[dev], color=INK, fontsize=10)
        style(ax)
    axes[0].set_ylabel("share of analytical cost (%)", color=INK2, fontsize=8)
    handles, names = axes[0].get_legend_handles_labels()
    fig.legend(handles, names, loc="lower center", ncol=4, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scores", required=True)
    ap.add_argument("--solve-times")
    ap.add_argument("--sim")
    ap.add_argument("--baseline", default="heuristic_1",
                    help="mapper to compute speedup against (default %(default)s)")
    ap.add_argument("--outdir", default="plots")
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    sc = pd.read_csv(args.scores)
    sc["device"] = sc["device"].str.lower()
    piv = sc.pivot_table(index=["operator", "device"], columns="mapper",
                         values="cost", aggfunc="first")
    summary = piv.add_prefix("cost_")
    ops = order(sc["operator"].unique())

    # 1. cost per operator, one panel per device
    mappers = ["optipim"] + sorted(m for m in piv.columns if m != "optipim")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.3))
    for ax, dev in zip(axes, DEVICES):
        t = piv.xs(dev, level="device").reindex(ops)[[m for m in mappers if m in piv]]
        grouped_bars(ax, t, MAPPER_COLOR)
        ax.set_yscale("log")
        ax.set_title(DEVICE_LABEL[dev], color=INK, fontsize=10)
        ax.set_ylabel("analytical-model cost (log)", color=INK2, fontsize=8)
        style(ax)
    axes[-1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "cost_per_operator.png", dpi=200)
    plt.close(fig)

    # 2. speedup over the heuristic
    if args.baseline in piv and "optipim" in piv:
        sp = (piv[args.baseline] / piv["optipim"]).rename("speedup")
        summary[f"speedup_vs_{args.baseline}"] = sp
        ratio_figure(sp.unstack("device").reindex(ops)[DEVICES],
                     f"{args.baseline} cost / OptiPIM cost (log)",
                     "OptiPIM speedup over the heuristic (above 1 = OptiPIM faster)",
                     out / "speedup.png", log=True, fmt="{:.2f}x")

    # 3. analytical vs simulator
    if args.sim and Path(args.sim).exists():
        sim = pd.read_csv(args.sim).rename(columns={"target": "device"})
        sim = sim[sim["mapper"] == "optipim"].dropna(subset=["simulated_cycles"])
        sim = sim.set_index(["operator", "device"])["simulated_cycles"]
        summary["simulated_cycles"] = sim
        r = (sim / piv["optipim"]).dropna().rename("sim_over_analytical")
        summary["sim_over_analytical"] = r
        t = r.unstack("device").reindex([o for o in ops if o in r.index.get_level_values(0)])
        ratio_figure(t.reindex(columns=DEVICES), "simulator cycles / analytical cost",
                     "Analytical model vs Ramulator2 (1 = exact)",
                     out / "analytical_vs_sim.png")
    else:
        print(f"note: no simulator file ({args.sim}); skipped analytical_vs_sim.png")

    # 4. Gurobi objective vs analytical model
    if args.solve_times and Path(args.solve_times).exists():
        st = pd.read_csv(args.solve_times).rename(columns={"target": "device"})
        st = st.set_index(["operator", "device"])
        summary["gurobi_objective"] = st["objective"]
        summary["gurobi_seconds"] = st["gurobi_seconds"]
        r = (piv["optipim"] / st["objective"]).dropna()
        summary["analytical_over_objective"] = r
        ratio_figure(r.unstack("device").reindex(ops)[DEVICES],
                     "analytical cost / Gurobi objective (log)",
                     "Solver objective vs analytical model (1 = agree)",
                     out / "objective_vs_model.png", log=True, fmt="{:.3g}")
    else:
        print(f"note: no solve-times file ({args.solve_times}); "
              "skipped objective_vs_model.png")

    # 5. cost breakdown (share of total), OptiPIM vs the baseline heuristic
    if {"inLoadingCost", "outTransCost", "numFilPELoading"} <= set(sc.columns):
        plot_breakdown(sc, ops, args.baseline, out / "cost_breakdown.png")

    summary = summary.reset_index()
    summary["_o"] = summary["operator"].map({o: i for i, o in enumerate(ops)})
    summary = summary.sort_values(["_o", "device"]).drop(columns="_o")
    summary.to_csv(out / "summary.csv", index=False, float_format="%.6g")
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(summary.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    print(f"figures and summary.csv written to {out}/")


if __name__ == "__main__":
    main()
