#!/usr/bin/env bash
# Copy the authors' heuristic_1 mappings for C1..M2 to where sim_check.sh looks:
#   group12/mappings/<hbmpim|simdram>/<op>/heuristic.trace
# Usage (from the group repo root): bash group12/analysis/prepare_heuristic_traces.sh
# Then: bash group12/scripts/sim_check.sh heuristic M1 M2 C3
set -euo pipefail
cd "$(dirname "$0")/../.."
H=${1:-heuristic_1}
copy() {  # op, directory name of the layer in baseline_mappings
  for pair in "hbmpim hbm_baseline" "simdram simdram_baseline"; do
    set -- $pair "$@"; T=$1; D=$2; shift 2
    SRC=baseline_mappings/$H/$D/$LAYER/0.trace
    [ -f "$SRC" ] || { echo "missing $SRC"; exit 1; }
    mkdir -p group12/mappings/$T/$OP
    cp "$SRC" group12/mappings/$T/$OP/heuristic.trace
    echo "$OP $T <- $SRC"
  done
}
OP=C1 LAYER=257-32_banks-ResNet50-12 copy
OP=C2 LAYER=247-32_banks-ResNet50-2  copy
OP=C3 LAYER=246-32_banks-ResNet50-1  copy
OP=M1 LAYER=0-32_banks-bert-0        copy
OP=M2 LAYER=1-32_banks-bert-1        copy
