# Padding extension: how to run it

Files in this folder:

| File | What it does |
| --- | --- |
| `DESIGN.md` | Why padding, where OptiPIM factorizes, expected results, limits |
| `pad_search.py` | Pads one layer, runs `pim-opt` per candidate, appends to `padding.csv` |
| `run_padding_eval.sh` | Runs the full evaluation (8 layers × 2 devices) and the plots |
| `plot_padding.py` | Makes `padding_speedup.png`, `padding_tradeoff.png`, `padding_summary.csv` |

Only Python 3 standard library is needed for `pad_search.py`; the plot needs
matplotlib (already in the authors' `requirements.txt`).

## 1. Copy into your repo (WSL)

```bash
cd ~/OptiPIM-grp12
mkdir -p group12/scripts
cp /path/to/padding/pad_search.py /path/to/padding/plot_padding.py \
   /path/to/padding/run_padding_eval.sh group12/scripts/
cp /path/to/padding/DESIGN.md group12/docs/padding_design.md   # optional
source optipim_env/bin/activate
```

All commands below run from the repo root, where `./build/bin/pim-opt`,
`./data/` and `./nn_models/` are.

## 2. Sanity check first (2 minutes)

The script rewrites each layer into a minimal `.mlir` file. Check that the
unpadded rewrite gives the same cost as your baseline run:

```bash
python3 group12/scripts/pad_search.py \
  nn_models/alexnet/single_layers/16banks/layerinfo.alexnet.l2.conv2.linalg.mlir \
  --device simdram --top 0
```

The `unpadded` line must show `real_cost 6.498367e+07` (your baseline). Do the
same with `--device hbmpim` (expect `8.189120e+05`). If it differs, stop and
look at `results/padding/alexnet.l2.conv2/simdram/unpadded/pim-opt.log`.

`--dry-run` lists the candidates and writes the files without solving.

### Gurobi 13 workaround (HBM-PIM only)

With Gurobi 13.0.3, presolve wrongly reports some HBM-PIM 3x3 conv models
infeasible (seen at 32 banks). Turning presolve off fixes that, but on SIMDRAM
it made a BERT matmul stop with "not proceeding further" and no solve. So
`pad_search.py` writes a `gurobi.env` file containing `Presolve 0` in the repo
root before each **HBM-PIM** `pim-opt` call and deletes it afterwards; SIMDRAM
runs use Gurobi's defaults. If you already have a `gurobi.env` there, it is
used as is and never deleted.

`OPTIPIM_PRESOLVE_FIX` changes this: `auto` (default, HBM-PIM only), `1`
(all devices), `0` (never). Each `pim-opt.log` starts with a `# presolve:`
line, and `padding.csv` has a `presolve` column saying which setting ran.

Your HBM-PIM baseline was solved with presolve on. If the step 2 HBM-PIM check
differs slightly, rerun it with `OPTIPIM_PRESOLVE_FIX=0` to see whether
presolve explains the gap. Always compare padded and unpadded runs under the
same setting.

### Failed runs

A run counts as failed when `pim-opt` prints no `Real Cost` (for example
"not proceeding further", infeasible, or a timeout). It gets an empty
`real_cost` and a `status` such as `no_objective`, `timeout` or `exit1` in
`padding.csv`, and the script lists it at the end. Old `Group.txt`/`model.lp`
files in a run folder are deleted before each solve, and a trace left by a
failed run is renamed `Group.txt.failed`, so a stale trace is never mistaken
for a result. The plot uses only the latest row per variant, so a failed rerun
drops that variant rather than falling back to an older number.

## 3. Run the evaluation

```bash
bash group12/scripts/run_padding_eval.sh quick   # AlexNet l0, l2 + ViT attention, both devices
bash group12/scripts/run_padding_eval.sh         # all 8 layers, both devices
```

Each layer solves up to 9 ILPs (unpadded + 8 padded). Most finish in seconds;
Gurobi stops any one at 400 s. A rerun appends new rows; the plot keeps the
last row per variant. Delete `results/padding/` for a clean start.

Outputs in `results/padding/`:

- `padding.csv`: one row per solved variant. First columns match your
  baseline CSV (`layer,device,...,real_cost,solver_seconds`), plus `variant`,
  `banks`, `bounds`, `mac_overhead`, `proxy_steps`.
- `padding_summary.csv`: per layer and device, unpadded cost, best variant,
  speedup. This is the table for the report.
- `padding_speedup.png`, `padding_tradeoff.png`: figures for the report.
- `<layer>/<device>/<variant>/`: `layer.mlir`, `Group.txt` trace, `model.lp`,
  `pim-opt.log` (with the cost breakdown).

Useful flags: `--banks 32` (match the group's 32-bank setting),
`--max-overhead 0.5`, `--max-prime 3`, `--top 4`, `--shape 'matmul:P=..,Q=..,R=..'`.

## 4. Evaluation plan

1. **Control:** AlexNet l0, l1, l2, l5 on both devices. Expect little or no
   gain (channels are already smooth); l5 has no awkward dim at all.
2. **Stress workloads:** ViT-B/16 attention (197 tokens), ViT QKV, GPT-2 LM
   head (vocab 50257), ResNet50 stage 5 (7×7).
3. **Metric:** speedup = unpadded Real Cost / best padded Real Cost, plus
   extra MACs and solver time. Report the trade-off plot to show that some
   padding choices hurt.
4. **Optional:** rerun the stress workloads with `--banks 32` to see whether
   more banks make padding matter more; simulate one padded trace to show the
   analytical gain holds in Ramulator2.

## 5. What is untested

Written without access to Gurobi or a built `pim-opt`. Checked here:

- every generated `.mlir` (109 files, all 8 AlexNet layers and the extra
  shapes) parses and passes the MLIR verifier (checked with the MLIR Python
  bindings from `iree-base-compiler`);
- the run, CSV and plot path works end to end with a stand-in `pim-opt` that
  prints a fake `Real Cost`.
- the `gurobi.env` workaround is applied to HBM-PIM only by default, to all or
  none with `OPTIPIM_PRESOLVE_FIX=1/0`, and removed after each run; a run with
  no printed `Real Cost` is marked failed and its stale trace is not reused
  (same stand-in).

Not checked: that `pim-opt` solves the minimal files (step 2 tests this), that
`linalg.batch_matmul` goes through the ILP the same way as `matmul` (the pass
parses it, but the authors' examples mostly use matmul), and solve times for
large padded bounds such as 50400. If the batched ViT layer fails, use
`--shape 'matmul:P=197,Q=64,R=197'` (one head) instead.
