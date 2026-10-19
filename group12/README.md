# Group 12: OptiPIM reproduction

This folder holds everything Group 12 adds on top of the authors' OptiPIM repo
(ETHZ-DYNAMO/OptiPIM). We do not edit the authors' files; all our scripts,
inputs and results live under `group12/`.

**Goal:** reproduce OptiPIM (ISCA 2025) at reduced scale. We compare optimal ILP
mappings with the weight-parallel heuristic for 2D convolution and matrix
multiply on HBM-PIM and SIMDRAM, check the analytical cost model against the
simulator, and add one improvement of our own.

**Left out (course scope):** real hardware, the PIM-DL genetic baseline, full
networks, and the memory scalability study.

## Team and roles

| Member | Role | Owns |
| --- | --- | --- |
| Member 1 (Shreya) | Toolchain and ILP | Build, Gurobi, `scripts/run_optipim.sh`, all `optipim.trace` files, Dockerfile, top-level README |
| Member 2 | Baseline heuristic | `scripts/heuristic.py`, all `heuristic.trace` files |
| Member 3 | Evaluation and figures | `scripts/evaluate.py`, `results/results.csv`, all plots |
| Member 4 | Extension | `scripts/pad_search.py`, extension inputs and results |

## Deadlines

| Date | Checkpoint |
| --- | --- |
| Wed 21 Oct | Gate 1: `make test` passes, simulator built, first C1 mappings pushed |
| Mon 26 Oct | Gate 2: baseline complete (all operators, both targets, both mappers, scored) |
| Sat 31 Oct | Gate 3: all results and figures frozen |
| Wed 4 Nov | Gate 4: report, slides and code submitted |

## Agreement 1: folder layout

```
group12/
  README.md                         this file
  operators/                        layer files we solve (num_banks = 32)
    C1.mlir ... M2.mlir
  mappings/
    hbmpim/<op>/optipim.trace       Member 1 (OptiPIM ILP)
    hbmpim/<op>/heuristic.trace     Member 2 (weight-parallel heuristic)
    simdram/<op>/optipim.trace
    simdram/<op>/heuristic.trace
  scripts/
    run_optipim.sh                  Member 1
    heuristic.py                    Member 2
    evaluate.py                     Member 3
    pad_search.py                   Member 4
  results/
    results.csv                     one row per scored mapping (Member 3)
    solve_times.csv                 ILP solve times (Member 1)
    plots/                          every figure in the report
  docs/                             notes for the report
```

Do not name any folder so that it ends in `32banks`, because the authors'
`.gitignore` ignores those.

## Operators

All use 32 banks and 16-bit data. Source files are in the authors'
`nn_models/` folder. To make our copy, change `num_banks = 16` to
`num_banks = 32`.

| ID | Source file | What it is |
| --- | --- | --- |
| C1 | `resnet50/single_layers/16banks/layerinfo.resnet50.l12.conv12.linalg.mlir` | 3x3 conv, 128 to 128 channels, 56x56 to 28x28, stride 2 (paper Fig. 12) |
| C2 | `resnet50/single_layers/16banks/layerinfo.resnet50.l2.conv2.linalg.mlir` | 3x3 conv, 64 to 64 channels, 56x56, stride 1 |
| C3 | `resnet50/single_layers/16banks/layerinfo.resnet50.l1.conv1.linalg.mlir` | 1x1 conv, 64 to 64 channels, 56x56 |
| M1 | `bert/single_layers/16banks/layerinfo.bert.l0.fc0.linalg.mlir` | matmul 128 x 768 x 768 |
| M2 | `bert/single_layers/16banks/layerinfo.bert.l1.fc1.linalg.mlir` | batched matmul 12 x 128 x 64 x 128 |

If time runs short, C3 and M2 are dropped first.

## Agreement 2: mapping file format

Both mappers write the authors' trace format, which the analytical model and
the simulator already read. Example: the heuristic mapping for C1, taken from
`baseline_mappings/heuristic_1/hbm_baseline/257-32_banks-ResNet50-12/0.trace`.

```
conv2d
Problem: 1,128,28,28,128,3,3
DilationStride: 2,2,1,1
Loop: N,K,P,Q,C,R,S,N,K,P,Q,C,R,S,N,K,P,Q,C,R,S
Bound: 1,32,1,1,1,1,1,1,1,1,7,128,3,3,1,4,28,4,1,1,1
Tag: P,P,P,P,P,P,P,T,T,T,T,T,T,T,P,P,P,P,P,P,P
StartBankRow: 0,0
Coeff_N2,N0,N1: 1,1,1
Coeff_K2,K0,K1: 4,1,1
Coeff_P2,P0,P1: 28,1,1
Coeff_Q2,Q0,Q1: 28,1,7
Coeff_C2,C0,C1: 128,1,128
Coeff_R2,R0,R1: 3,1,3
Coeff_S2,S0,S1: 3,1,3
end
```

- `Problem` lists the layer sizes in the order N,K,P,Q,C,R,S for conv2d.
  For matmul the first line is `gemm` and there are 5 loops: N,K,P,Q,R.
- `Bound` holds three groups, each in loop order: level 2 (banks), then
  level 0 (time, tag `T`), then level 1 (columns). For every loop, the three
  numbers multiply to the full size.
- `Coeff_X2,X0,X1` gives how the indices of loop X are numbered (the paper's
  flexible indexing).
- A new mapper is correct only if its file scores without errors in
  `validation/analytical_modeling/get_trace_perf.py`.

## Agreement 3: results file

`results/results.csv` has one row per (operator, target, mapper, setting).
Every plot in the report is made from this file only.

```
operator,target,mapper,banks,precision,analytical_cycles,simulated_cycles,compute,input_loading,output,solve_seconds
C1,hbmpim,optipim,32,16,,,,,,
C1,hbmpim,heuristic,32,16,,,,,,
```

| Column | Values |
| --- | --- |
| operator | C1, C2, C3, M1, M2, or an extension shape ID such as A1 |
| target | `hbmpim` or `simdram` |
| mapper | `optipim`, `heuristic`, or an extension name such as `optipim_pad` |
| banks | 32 unless stated |
| precision | bits per value, 16 unless stated |
| analytical_cycles | `finalPerformance` from the Python analytical model |
| simulated_cycles | `memory_system_cycles` from Ramulator2 (empty if not simulated) |
| compute, input_loading, output | cost breakdown from the analytical model |
| solve_seconds | ILP solve time; empty for the heuristic |

## Settings we use

| Setting | Value |
| --- | --- |
| `pim-opt` flags | `--data-layout-pass --trans-coeff-method 4 --number-counting-method 0 --obj-method 0 --storage-method 0` |
| Target flag | `--target-device-type 1` for HBM-PIM, `0` for SIMDRAM |
| Arch file | `data/hbm_pim.json` (to be confirmed at Gate 1; record the final choice here) |
| Knobs file | `data/knobs.json` |
| Simulator, HBM-PIM | `simulator/hbmpim_config.yaml`, `alloc_method=new` |
| Simulator, SIMDRAM | `simulator/simdram_config.yaml`, `alloc_method=simdram` |
| Gurobi version | fill in at Gate 1 (paper used 11.0.3) |

## How to run

Full build steps (packages, Gurobi licence, environment variables) are in the
authors' top-level README. In short, on Linux (WSL2 or a Linux server):

```
make python_env && source optipim_env/bin/activate
make compile_optipim                                    # hours, once
make test                                               # smoke test

# one operator on one target
bash group12/scripts/run_optipim.sh C1 hbmpim

# all OptiPIM mappings
for OP in C1 C2 C3 M1 M2; do
  for T in hbmpim simdram; do bash group12/scripts/run_optipim.sh $OP $T; done
done
```

The heuristic and the evaluation scripts are plain Python and run on any
laptop with the venv active. Their usage goes here once they exist.

## Git rules

- Work on your own branch (`member1`, `member2`, ...), and open a pull request
  into `main`. One teammate reviews it before merging.
- Never commit `llvm-project/`, `build/`, `optipim_env/`, `Debug/` or `Result/`.
- Commit mapping files and `results.csv`, so everyone can plot without
  rerunning the solver.
- Change one of the three agreements only after the whole team agrees, and
  update this file in the same pull request.
