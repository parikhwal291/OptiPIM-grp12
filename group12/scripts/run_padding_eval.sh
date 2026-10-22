#!/usr/bin/env bash
# Group 12 padding extension: run the whole evaluation.
# Run from the OptiPIM repo root, with the venv active and Gurobi licensed.
#   bash group12/scripts/run_padding_eval.sh            # everything
#   bash group12/scripts/run_padding_eval.sh quick      # AlexNet + ViT attention only
set -u
PAD="python3 group12/scripts/pad_search.py --banks 32"
L=nn_models/alexnet/single_layers/16banks
OUT=results/padding
mkdir -p "$OUT"

# Gurobi 13 workaround is handled inside pad_search.py: presolve is turned off
# (gurobi.env "Presolve 0") for HBM-PIM runs only. Override with
#   OPTIPIM_PRESOLVE_FIX=0 (never) or =1 (all devices).

for DEV in simdram hbmpim; do
  # Control group: AlexNet (awkward spatial bounds 55/27/13, but smooth channels)
  $PAD $L/layerinfo.alexnet.l0.conv0.linalg.mlir --device $DEV --out $OUT
  $PAD $L/layerinfo.alexnet.l2.conv2.linalg.mlir --device $DEV --out $OUT
  # Workload where perfect factorization fails: ViT-B/16 has 197 tokens (prime)
  $PAD --shape 'batch_matmul:N=12,P=197,Q=64,R=197' --name vit.attn_qk --device $DEV --out $OUT
  [ "${1:-}" = quick ] && continue
  $PAD $L/layerinfo.alexnet.l1.conv1.linalg.mlir --device $DEV --out $OUT
  $PAD $L/layerinfo.alexnet.l5.fc0.linalg.mlir   --device $DEV --out $OUT
  $PAD --shape 'matmul:P=197,Q=768,R=2304'  --name vit.qkv      --device $DEV --out $OUT
  $PAD --shape 'matmul:P=1,Q=768,R=50257'   --name gpt2.lm_head --device $DEV --out $OUT
  $PAD --shape 'conv:K=512,C=512,P=7,Q=7,R=3,S=3' --name resnet50.conv5 --device $DEV --out $OUT
done

python3 group12/scripts/plot_padding.py $OUT/padding.csv --out $OUT
