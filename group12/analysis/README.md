# group12/analysis

Copy this folder into the repo as `group12/analysis/`. Everything runs with the
`optipim_env` venv (pandas, matplotlib); no build needed, only the authors'
OptiPIM checkout for its Python analytical model and heuristic traces.

## Rerun everything

From the group repo root:

```
bash group12/analysis/rerun.sh ~/OptiPIM . group12/results/plots
```

This scores every trace in `manifest.csv` (OptiPIM `group12/mappings/<target>/<op>/optipim.trace`
and the authors' heuristic_1/heuristic_2 traces for C1 to M2), then draws all
figures from `scores.csv`, `group12/results/solve_times.csv` and
`group12/results/sim_check.csv` (a figure is skipped if its input is missing).
After a new solve or simulation, just run it again. On Windows without WSL,
run the two `python` lines inside `rerun.sh` by hand.

Outputs in `group12/results/plots/`: `scores.csv`, `summary.csv`,
`cost_per_operator.png`, `speedup.png`, `analytical_vs_sim.png`,
`objective_vs_model.png`.

## Files

| File | What it does |
|---|---|
| `manifest.csv` | Which traces to score: operator, device, mapper, path. Heuristic layers: C1 = ResNet50-12, C2 = ResNet50-2, C3 = ResNet50-1, M1 = bert-0, M2 = bert-1. |
| `score_traces.py` | Scores traces with the authors' model (hbm_pim.json for HBM-PIM, dram.json for SIMDRAM) and fixes pim-opt's stride/dilation order (see below). |
| `plot_results.py` | The four figures and `summary.csv`. |
| `parse_mapping.py` | L0/L1/L2 tile factors per loop from trace files or pim-opt logs, plus banks used. |
| `REPORT_SKELETON.md` | Report outline with the current numbers and TODOs. |
| `sample/` | Output of a test run on the member1 branch (commit fabfae7) with the simulator numbers from Shreya. |

## Things to know

- **Stride/dilation order.** pim-opt writes `DilationStride` as dilation,dilation,stride,stride; the authors' Python parser reads field 0 as stride. So `scripts/score_analytical.py` scores C1 as stride 1, dilation 2. `score_traces.py` corrects it for `optipim` rows. Effect: HBM-PIM C1 unchanged (870,912); SIMDRAM C1 24,995,102 becomes 26,701,846.
- **Three costs disagree.** Gurobi objective, pim-opt's "Real Cost" and the Python model all differ; on HBM-PIM matmuls by 73x to 108x. We treat the Python model as ground truth because it matches the simulator on HBM-PIM within about 2%.
- **HBM-PIM M1:** OptiPIM's mapping is 0.78x the heuristic's speed under the model (and the simulator agrees with the model on OptiPIM). The cause is guessed, not verified: see the report skeleton, Section IV-E.
- **SIMDRAM model vs simulator:** off by 1.4x to 1.8x for C3, M1 and M2. Unexplained.
- **Gurobi 13.0.3 presolve:** default presolve wrongly reports the HBM-PIM 3x3 convs infeasible; `Presolve 0` fixes it.

## Untested

- The heuristic traces have not been run in the simulator, so the M1 heuristic win rests on the analytical model alone.
- `sim_check.csv` was not on the branch; the sample uses the cycle counts Shreya reported (C3, M1, M2 only).
- Nothing here has run on Windows or macOS directly; on Linux it was tested end to end.
