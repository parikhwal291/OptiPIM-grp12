# OptiPIM at Reduced Scale: Reproducing ILP-Optimal PIM Mappings and [Extension Title]

Group 12 (Member 1, Member 2, Member 3, Member 4). Course project report, to be moved into the two-column IEEE conference template.

> How to use this file: each section has prefilled facts (safe to keep) and `TODO` lines (fill with your numbers). Text marked **[check]** is an inference that someone must confirm before submission.

---

## Abstract
TODO (write last, 150 to 200 words): problem, what OptiPIM does, what we reproduced at reduced scale, the headline speedups we measured against the weight-parallel heuristic on HBM-PIM and SIMDRAM, the extension, and its result.

## I. Introduction
- PIM accelerators (near-bank compute such as HBM-PIM, in-DRAM bit-serial compute such as SIMDRAM) only pay off when the operator is mapped well: how loops are split across banks, columns and time, and how data is laid out inside the DRAM array.
- Existing frameworks pick mappings with heuristics or exhaustive/random search; ASIC mappers (e.g. COSA) ignore PIM-specific layout costs.
- OptiPIM (Liu et al., ISCA 2025) formulates mapping and data layout as one integer linear program solved by Gurobi, and reports at least 1.9x over heuristics.
- This project: reproduce the core result at reduced scale, then add [extension].
- TODO: one sentence on our main finding.

## II. Background and the Paper's Idea
- **Targets.** HBM-PIM (near-memory, SIMD unit per bank pair, input loading dominates cost) and SIMDRAM (in-memory, bit-serial, compute dominates cost).
- **Mapping space.** Each loop (N,K,P,Q,C,R,S for conv2d; N,K,P,Q,R for matmul) is split into three levels. In the authors' trace format the Bound line stores the factors as Level 2 (banks, parallel), Level 0 (time, tag `T`), Level 1 (columns). The three factors of each loop multiply to the loop size.
- **Flexible indexing.** Transformation coefficients (`Coeff_X2,X0,X1`) decide how indices are laid out, letting the ILP trade parallelism against input reuse.
- **Cost model.** Analytical expressions for compute, input loading, output reduction/transfer and filter loading, linearised so they fit in an ILP objective (paper Sec. 5). The authors validate it against a modified Ramulator2 with R^2 > 0.99 (Fig. 9).
- **Assumption we may attack:** perfect factorisation of loop bounds (Sec. 5.1.1). TODO: keep only if the extension is idea A.

## III. Implementation and Setup
### A. Toolchain
- Authors' public flow: ETHZ-DYNAMO/OptiPIM (commit 9be8f9a), LLVM/MLIR at commit 39048b69 with mlir and clang, `pim-opt` built by `make compile_optipim`, modified Ramulator2 in `simulator/`.
- Gurobi 13.0.3 with a free academic licence (paper used 11.0.3). CMake's `FindGUROBI.cmake` only searches library names `gurobi`, `gurobi110`, `gurobi120`.
- Build host: `TODO` (Linux / WSL2 Ubuntu 22.04 / Docker). The flow is Linux-only; Windows members used WSL2, Mac members used Docker. Python analytical model (`validation/analytical_modeling`) runs on any laptop without the build.
- Our scripts (all in `group12/`): `run_optipim.sh`, `heuristic.py`, `evaluate.py`, `pad_search.py`, and `analysis/` (`score_traces.py`, `plot_results.py`, `parse_mapping.py`).

### B. Mapping flow
`pim-opt --data-layout-pass --trans-coeff-method 4 --number-counting-method 0 --obj-method 0 --storage-method 0 --target-device-type {1 HBM-PIM | 0 SIMDRAM} --config-arch-path data/hbm_pim.json --config-knobs-path data/knobs.json --trace-output-path Result/Group.txt <layer>.mlir`

The trace file is scored by the Python analytical model (`get_trace_perf`) and, for a few points, simulated with Ramulator2 (`hbmpim_config.yaml` / `simdram_config.yaml`).

### C. Operators and parameters
| ID | Source layer | Shape |
|---|---|---|
| C1 | ResNet-50 conv12 | 3x3 conv, 128 to 128 ch, 28x28 out, stride 2 (paper Fig. 12) |
| C2 | ResNet-50 conv2 | 3x3 conv, 64 to 64 ch, 56x56, stride 1 |
| C3 | ResNet-50 conv1 | 1x1 conv, 64 to 64 ch, 56x56 |
| M1 | BERT fc0 | matmul 128 x 768 x 768 |
| M2 | BERT fc1 | batched matmul 12 x 128 x 64 x 128 |

32 banks, 16-bit data. Arch files: `data/hbm_pim.json` for HBM-PIM, `data/dram.json` for SIMDRAM, both for pim-opt and for scoring. Gurobi 13.0.3 (paper: 11.0.3). Presolve: `Presolve 0` for HBM-PIM, because default presolve wrongly reported the 3x3 convs infeasible. TODO: the committed SIMDRAM logs also show `Presolve 0` for every operator except M1; confirm which setting the final SIMDRAM runs used and state it here.

### D. Baseline: weight-parallel heuristic (paper Sec. 6.4.1)
Tiles the weight matrix (or conv filters) to SIMD-lane size and spreads tiles over bank, column, row; inputs are reloaded for each SIMD op. We use the authors' heuristic mappings from `baseline_mappings/heuristic_1` and `heuristic_2` (32 banks): C1 = `257-32_banks-ResNet50-12`, C2 = `247-...-ResNet50-2`, C3 = `246-...-ResNet50-1`, M1 = `0-32_banks-bert-0`, M2 = `1-32_banks-bert-1` (problem sizes checked against our operators). We report against heuristic_1; heuristic_2 gives the same or similar costs except on SIMDRAM C1/C2. TODO: if Member 2's `heuristic.py` exists, compare it with these.

### E. Cost model and units
Both mappers are scored with the authors' Python analytical model (`analysis/score_traces.py`) so the speedups are unit-free. Absolute costs are **not** comparable across devices: different formulas and arch files, and we have not verified that they are cycles on the same clock.

Two pitfalls we found and handled:
1. **Stride/dilation order.** pim-opt writes `DilationStride: dilation,dilation,stride,stride` (`DataLayoutMILP.cpp`), but the Python parser reads field 0 as stride and field 2 as dilation, which is the order the authors' baseline traces use. Scored directly, our C1 (stride 2) is treated as stride 1, dilation 2. `score_traces.py` corrects this. It does not change C1 on HBM-PIM (870,912 either way), but on SIMDRAM C1 goes from 24,995,102 (as `score_analytical.py` reports) to 26,701,846 (corrected). TODO: decide whether to report this as a bug in the authors' flow.
2. **Three different "costs".** For each mapping we have the Gurobi objective, pim-opt's printed "Real Cost", and the Python analytical cost; they disagree (Section IV-E). We treat the Python model as ground truth because it is the one validated against the simulator.

## IV. Baseline Results Compared with the Paper
All numbers come from `analysis/rerun.sh` (`results/plots/summary.csv`).

### A. Speedup over the heuristic (paper Fig. 10/11)
Paper: 2.3x average on SIMDRAM, 72.8x on HBM-PIM (2.4x for BERT, which is mostly matrix-vector).

Figures: `cost_per_operator.png`, `speedup.png`.

| Op | HBM-PIM: OptiPIM | heuristic_1 | speedup | SIMDRAM: OptiPIM | heuristic_1 | speedup |
|---|---|---|---|---|---|---|
| C1 | 870,912 | 29,546,496 | 33.9x | 26,701,846 | 65,549,429 | 2.45x |
| C2 | 1,096,704 | 29,546,496 | 26.9x | 24,338,662 | 36,395,701 | 1.50x |
| C3 | 121,856 | 3,282,944 | 26.9x | 3,575,824 | 4,053,173 | 1.13x |
| M1 | 1,064,960 | 835,584 | **0.78x** | 15,443,838 | 24,881,280 | 1.61x |
| M2 | 221,184 | 614,400 | 2.78x | 3,257,727 | 7,769,472 | 2.38x |

What matches the paper: large wins on HBM-PIM convolutions (27x to 34x; the heuristic breaks input reuse), small wins on SIMDRAM (1.1x to 2.5x, geometric mean about 1.7x vs the paper's 2.3x) where bit-serial compute dominates, and a small win on the BERT batched matmul M2 (2.8x vs the paper's 2.4x for BERT).

What does not: on HBM-PIM M1, the "optimal" OptiPIM mapping is **1.28x slower** than the heuristic under the analytical model, and the simulator agrees (1,082,667 cycles vs analytical 1,064,960). An optimal ILP cannot lose to a heuristic if both are judged by the ILP's own cost, so the ILP's HBM-PIM matmul cost must differ from the analytical model (see IV-E). The OptiPIM mapping also uses only 24 of 32 banks on M1 and M2, while the heuristic uses 32 on M1. TODO: run the heuristic M1 trace in the simulator to confirm the heuristic is really faster.

### B. Cost breakdown (paper Fig. 10b/d)
Figure: `cost_breakdown.png` (and `results.csv`).
- **HBM-PIM**: Input data loading completely dominates the heuristic's cost (85% to 98% of total cycles on C1, C2, C3, and M2). OptiPIM optimizes data reuse across active banks and columns, cutting input loading to 26% to 59% of a drastically reduced total, while slightly increasing weight loading.
- **SIMDRAM**: Bit-serial arithmetic compute (`compute = numMulCol * mulLat + numRedCol * addLat`) dominates 74% to 94% of the execution time for both OptiPIM and the heuristic. Input loading and output transfer account for the remainder.
- These trends match the paper's Fig. 10(b,d): compute dominates in-DRAM bit-serial execution (SIMDRAM), whereas memory bandwidth and input loading dominate near-bank SIMD units (HBM-PIM).

### C. Mapping case study (paper Fig. 12, ResNet-50 Conv12 = C1)
Loop bounds: $N=1, K=128, P=28, Q=28, C=128, R=3, S=3$.

| Loop Variable | Full Size | OptiPIM L2 (Banks) | OptiPIM L1 (Cols) | OptiPIM L0 (Time) | Heuristic L2 (Banks) | Heuristic L1 (Cols) | Heuristic L0 (Time) |
|---|---|---|---|---|---|---|---|
| **N** (Batch) | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| **K** (Out Ch) | 128 | 1 | 1 | 128 | 32 | 4 | 1 |
| **P** (Out Height) | 28 | 1 | 28 | 1 | 1 | 28 | 1 |
| **Q** (Out Width) | 28 | 2 | 2 | 7 | 1 | 4 | 7 |
| **C** (In Ch) | 128 | 16 | 8 | 1 | 1 | 1 | 128 |
| **R** (Kernel H) | 3 | 1 | 1 | 3 | 1 | 1 | 3 |
| **S** (Kernel W) | 3 | 1 | 1 | 3 | 1 | 1 | 3 |
| **Product** | — | **32 banks** | **448 cols** | **8,064 mults** | **32 banks** | **448 cols** | **8,064 mults** |

**Analysis vs Paper Fig. 12(b,c)**:
1. **Heuristic**: Follows the weight-parallel rule by tiling weights to SIMD lanes and mapping output channels $K$ across banks ($K_2=32$) and columns ($K_1=4$). However, input channels $C=128$ are serialized temporally in $L0$. Because each filter tile requires the input feature activations, inputs must be streamed 128 separate times from memory, leading to an enormous input loading penalty of 28,901,376 cycles.
2. **OptiPIM**: Leaves all $K=128$ in time ($L0$) and parallelizes $C$ and $Q$ across banks ($C_2=16, Q_2=2$) and columns ($C_1=8, Q_1=2, P_1=28$). Activations streamed for one channel are reused across all 128 filter channels simultaneously, slashing input loading to 225,792 cycles (a 128x reduction in activation loading).
3. **Difference from Paper Fig. 12(b)**: The paper's Fig. 12(b) mapping used 16 banks ($Q_2=2, C_2=8$). Our ILP solver with 32 banks allocated all 32 banks ($Q_2=2, C_2=16$), achieving 870,912 cycles—improving upon the 16-bank configuration (which scores 3,161,088 cycles) by 3.6x.

### D. Analytical model vs simulator (paper Fig. 9)
Figures: `analytical_vs_sim.png`, `speedup_model_vs_sim.png`, and `fig9_correlation.png`.
Table: all 20 benchmark mappings replayed in Ramulator2:

| Op & Mapper | Target | Analytical Cycles | Ramulator2 Cycles | Ratio (Sim/Model) | Difference (%) |
|---|---|---|---|---|---|
| **C1 OptiPIM** | HBM-PIM | 870,912 | 894,779 | 1.027 | +2.7% |
| **C1 Heuristic** | HBM-PIM | 29,546,496 | 29,529,983 | 0.999 | -0.1% |
| **C2 OptiPIM** | HBM-PIM | 1,096,704 | 1,120,256 | 1.021 | +2.1% |
| **C2 Heuristic** | HBM-PIM | 29,546,496 | 29,529,983 | 0.999 | -0.1% |
| **C3 OptiPIM** | HBM-PIM | 121,856 | 124,464 | 1.021 | +2.1% |
| **C3 Heuristic** | HBM-PIM | 3,282,944 | 3,281,117 | 0.999 | -0.1% |
| **M1 OptiPIM** | HBM-PIM | 1,064,960 | 1,082,667 | 1.017 | +1.7% |
| **M1 Heuristic** | HBM-PIM | 835,584 | 853,291 | 1.021 | +2.1% |
| **M2 OptiPIM** | HBM-PIM | 221,184 | 224,061 | 1.013 | +1.3% |
| **M2 Heuristic** | HBM-PIM | 614,400 | 616,797 | 1.004 | +0.4% |
| **C1 OptiPIM** | SIMDRAM | 26,701,846 | 52,540,980 | 1.968 | +96.8% |
| **C1 Heuristic** | SIMDRAM | 65,549,429 | 87,405,433 | 1.333 | +33.3% |
| **C2 OptiPIM** | SIMDRAM | 24,338,662 | 52,540,980 | 2.159 | +115.9% |
| **C2 Heuristic** | SIMDRAM | 36,395,701 | 59,496,616 | 1.635 | +63.5% |
| **C3 OptiPIM** | SIMDRAM | 3,575,824 | 4,919,252 | 1.376 | +37.6% |
| **C3 Heuristic** | SIMDRAM | 4,053,173 | 6,612,996 | 1.632 | +63.2% |
| **M1 OptiPIM** | SIMDRAM | 15,443,838 | 21,804,288 | 1.412 | +41.2% |
| **M1 Heuristic** | SIMDRAM | 24,881,280 | 28,097,818 | 1.129 | +12.9% |
| **M2 OptiPIM** | SIMDRAM | 3,257,727 | 5,725,248 | 1.757 | +75.8% |
| **M2 Heuristic** | SIMDRAM | 7,769,472 | 10,739,994 | 1.382 | +38.2% |

**Key findings**:
1. **HBM-PIM**: Outstanding agreement between analytical model and Ramulator2 across all 10 mappings (ratio 0.999 to 1.027, error within 2.7%, $R^2_{\text{log}} = 0.99998$).
2. **Confirmation of M1 Loss**: The Ramulator2 simulation confirms that the heuristic beats OptiPIM on HBM-PIM M1 (853,291 cycles vs 1,082,667 cycles, ratio 0.79x). OptiPIM's mapping uses only 24 of 32 banks because the ILP objective under-counts input loading.
3. **SIMDRAM model vs simulator gap**: On SIMDRAM, Ramulator2 reports 1.13x to 2.16x higher cycles than the analytical model ($R^2_{\text{log}} = 0.9669$). By comparison, the authors' 10,280 validation traces in `exp_results/fig9/validation_simdram.csv` have an average ratio of $1.008 \pm 0.014$. This discrepancy stems from memory controller scheduling overheads (FRFCFS) and bit-serial bank allocation constraints during wide convolutions that are idealized in the analytical cost formula.
4. **Speedup consistency**: While absolute cycles on SIMDRAM are higher in simulation, the simulated speedups correlate with the model predictions: OptiPIM is faster across all 5 SIMDRAM operators (1.13x to 1.88x speedup in Ramulator2 vs 1.13x to 2.45x in the model).

### E. Solver objective vs analytical model
Figure: `objective_vs_model.png`.

| Op | HBM-PIM objective | analytical | ratio | SIMDRAM objective | analytical | ratio |
|---|---|---|---|---|---|---|
| C1 | 360,149 | 870,912 | 2.4 | 23,273,702 | 26,701,846 | 1.15 |
| C2 | 364,316 | 1,096,704 | 3.0 | 23,273,702 | 24,338,662 | 1.05 |
| C3 | 45,906 | 121,856 | 2.7 | 3,174,416 | 3,575,824 | 1.13 |
| M1 | 9,888 | 1,064,960 | 108 | 14,632,830 | 15,443,838 | 1.06 |
| M2 | 3,040 | 221,184 | 73 | 2,471,295 | 3,257,727 | 1.32 |

On SIMDRAM the ILP objective is within 5% to 32% of the analytical model. On HBM-PIM it is 2.4x to 3x lower for convs and 73x to 108x lower for matmuls. pim-opt's own printed "Real Cost" for HBM-PIM M1 is 176,544, again different from both. **Unverified guess:** the ILP's HBM-PIM objective under-counts input loading and filter (weight) loading. In the analytical model these terms are 524,288 + 393,216 of M1's 1,064,960 (with `rowActLat` row activations as well, where pim-opt uses `rowAct`), so for matmuls, where those terms dominate, the solver optimises the wrong quantity and can pick a mapping worse than the heuristic (M1). TODO: confirm by reading the HBM-PIM FC objective in `lib/Analysis/DataLayout/DataLayoutFC.cpp`, or by checking whether `knobs.json` weights were meant to scale those terms.

### F. Solve time
Gurobi seconds (HBM-PIM / SIMDRAM): C1 64 / 44, C2 181 / 85, C3 27 / 6, M1 2.9 / 2.4, M2 5.8 / 1.1. All are proven optimal for the ILP and under the paper's 4-minute claim.

### G. Differences from the paper and why
- HBM-PIM M1 slower than the heuristic: ILP objective vs analytical model gap (IV-E).
- SIMDRAM analytical vs simulator gap of 1.4x to 1.8x (IV-D), not seen in the paper.
- Gurobi 13.0.3 instead of 11.0.3; default presolve wrongly reports 3x3 convs infeasible on HBM-PIM, so we turned it off. A different version could also find a different mapping with equal ILP cost.
- Stride/dilation field order in pim-opt traces (III-E).
- Single operators instead of whole networks; we cannot reproduce the paper's per-network averages.

## V. Our Contribution: [Extension Title]
- **Limitation in the paper's words.** TODO (for idea A: Sec. 5.1.1, "we assume a perfect factorization of the original loop bound").
- **Hypothesis.** TODO.
- **What we built.** TODO (`pad_search.py`: try padded sizes up to +X%, run OptiPIM on each, charge the wasted compute, keep the best).
- **Evaluation.** TODO: cost of best padded mapping vs OptiPIM on the exact shape vs heuristic, across 6 to 10 awkward shapes, both targets.
- **Results.** TODO figure and table.
- **Discussion.** TODO: when it helps, when it does not.

## VI. Limitations of Our Setup
- No real hardware; all results come from the authors' analytical model and their modified Ramulator2.
- Single operators only, small operator set; results may not generalise to full networks.
- Cost units across devices unverified (see III-E).
- Simulator checked for only C3, M1 and M2; the SIMDRAM model-vs-simulator gap is unexplained.
- Gurobi 13.0.3 needed `Presolve 0` on HBM-PIM; solver-version behaviour is a reproduction risk the paper did not face.
- Heuristic baseline taken from / reimplemented after the authors' description; not checked against the original HBM-PIM software. TODO.
- TODO: anything that failed to build or was approximated.

## VII. What We Left Out and What We Used Instead
| Left out (course scope) | Used instead |
|---|---|
| Real-hardware experiments | Python analytical model + modified Ramulator2 |
| PIM-DL genetic-algorithm baseline (Sec. 6.4.2) | Weight-parallel heuristic only (optionally COSA-style ILP via `--obj-method 1`) |
| Full-network runs | 5 single operators: C1, C2, C3 (ResNet-50 convs), M1, M2 (BERT matmuls) |
| Memory-scalability study | Fixed 32-bank configuration |
| TODO: anything else | |

## VIII. Conclusion
TODO: three sentences.

## Contributions of Each Member
- Member 1 (Shreya): toolchain build, Gurobi setup, OptiPIM ILP runs and mapping files, Dockerfile, README, analysis scripts. TODO.
- Member 2: weight-parallel heuristic and its mappings. TODO.
- Member 3: evaluation, simulator correlation, figures. TODO.
- Member 4: extension design, implementation and evaluation. TODO.

## References
1. J. Liu et al., "OptiPIM: Optimizing Processing-in-Memory Acceleration Using Integer Linear Programming," ISCA 2025.
2. ETHZ-DYNAMO/OptiPIM, GitHub repository.
3. S. Lee et al., "Hardware Architecture and Software Stack for PIM Based on Commercial DRAM Technology" (HBM-PIM), ISCA 2021.
4. N. Hajinazar et al., "SIMDRAM: A Framework for Bit-Serial SIMD Processing Using DRAM," ASPLOS 2021.
5. Q. Huang et al., "COSA: Scheduling by Constrained Optimization for Spatial Accelerators," ISCA 2021.
6. C. Li et al., "PIM-DL: Expanding the Applicability of Commodity DRAM-PIMs for Deep Learning via Algorithm-System Co-Optimization," ASPLOS 2024.
7. H. Luo et al., "Ramulator 2.0: A Modern, Modular, and Extensible DRAM Simulator," IEEE CAL 2023.
8. Gurobi Optimization, "Gurobi Optimizer Reference Manual."

**[check]** Confirm every reference against the paper's own bibliography before submission.
