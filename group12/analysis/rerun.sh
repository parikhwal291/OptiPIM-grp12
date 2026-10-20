#!/usr/bin/env bash
# Re-score every trace in manifest.csv and redraw all figures.
# Usage: bash rerun.sh <optipim_root> <group_repo_root> [outdir]
#   e.g. (from the group repo root)
#   bash group12/analysis/rerun.sh ~/OptiPIM . group12/results/plots
# Reads group12/results/solve_times.csv and sim_check.csv if they exist.
set -euo pipefail
ROOT=${1:?path to the authors OptiPIM checkout}
REPO=${2:?path to the group repo root}
OUT=${3:-$REPO/group12/results/plots}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"

python3 "$HERE/score_traces.py" --optipim-root "$ROOT" --repo-root "$REPO" \
    --manifest "$HERE/manifest.csv" --out "$OUT/scores.csv"
python3 "$HERE/plot_results.py" --scores "$OUT/scores.csv" \
    --solve-times "$REPO/group12/results/solve_times.csv" \
    --sim "$REPO/group12/results/sim_check.csv" --outdir "$OUT"
