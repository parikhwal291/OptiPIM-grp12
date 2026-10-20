Hi all, Pari here (Member 1). Status update and everyone's tasks until 4 Nov. Please read your section fully. Dates are internal deadlines from our project plan.

==================================================
1. WHERE WE ARE (Mon 19 Oct)
==================================================
- Repo: github.com/parikhwal291/OptiPIM-grp12 (our fork of ETHZ-DYNAMO/OptiPIM). My work is on branch "member1". All our files live under group12/. Never open pull requests against ETHZ-DYNAMO, only inside our repo (base: parikhwal291/OptiPIM-grp12, main).
- The flow is built on my laptop (WSL2 Ubuntu 22.04, LLVM build about 4 h 15 min, Gurobi 13.0.3; the paper used 11.0.3). Only my machine has pim-opt and the Ramulator2 simulator right now. You do NOT need the build for Python work: the analytical model and all plots run on any laptop.
- Operators (all 32 banks, 16-bit), files in group12/operators/:
  C1 = ResNet-50 conv12, 3x3 conv, 128->128 ch, 28x28 out, stride 2 (the paper's Fig. 12 layer)
  C2 = ResNet-50 conv2, 3x3 conv, 64->64 ch, 56x56, stride 1
  C3 = ResNet-50 conv1, 1x1 conv, 64->64 ch, 56x56
  M1 = BERT fc0, matmul 128 x 768 x 768
  M2 = BERT fc1, batched matmul 12 x 128 x 64 x 128
- DONE: OptiPIM (ILP) mappings for all 5 operators on HBM-PIM and SIMDRAM = 10 mappings, in group12/mappings/<hbmpim|simdram>/<op>/optipim.trace with the Gurobi log next to each. Solve times 1.1 to 181 s (group12/results/solve_times.csv). Analytical-model scores: group12/results/analytical_check_<target>.csv. Simulator cycles for C3, M1, M2: group12/results/sim_check.csv.

First results (authors' Python analytical model; heuristic = the authors' shipped heuristic_1 traces in baseline_mappings/):
  HBM-PIM: OptiPIM beats the heuristic 33.9x (C1), 26.9x (C2), 26.9x (C3), 2.8x (M2), but LOSES on M1 (0.78x). Cause of the M1 loss is NOT known yet.
  SIMDRAM: OptiPIM wins 2.45x (C1), 1.50x (C2), 1.13x (C3), 1.61x (M1), 2.38x (M2). Paper: about 2.3x avg on SIMDRAM, 72.8x on HBM-PIM.
  Model vs simulator: HBM-PIM within 2% (C3, M1, M2). SIMDRAM: simulator 1.4x to 1.8x HIGHER than the model, cause unknown. C1, C2 not simulated yet (slow).

Rules everyone must follow (we learned these the hard way):
  a) Compare mappers ONLY by the Python analytical cost or simulator cycles. Never by the Gurobi objective or pim-opt's "Real Cost": on HBM-PIM they are 2-3x (convs) and 73-108x (matmuls) below the model.
  b) Gurobi 13 bug: default presolve wrongly says C1/C2 are "infeasible" on HBM-PIM at 32 banks. Fix: a file gurobi.env with the line "Presolve 0" in the working dir. run_optipim.sh does this automatically for HBM-PIM only. Do NOT use it for SIMDRAM (it broke M1 there).
  c) Stride/dilation order: pim-opt writes "DilationStride: dil,dil,stride,stride", the authors' Python parser reads stride first. Our scorers (score_analytical.py, analysis/score_traces.py) fix this for optipim traces. If you write your own scorer, apply the same fix, or C1 (stride 2) is scored wrong.
  d) Arch files: HBM-PIM = data/hbm_pim.json, SIMDRAM = data/dram.json, for solving AND scoring.
  e) Folder layout, trace format and results.csv columns are in group12/README.md ("Agreements"). Change them only if all 4 agree.

Setup for all of you (Windows: WSL2 Ubuntu 22.04; Mac: native Python is fine for analysis):
  git clone https://github.com/parikhwal291/OptiPIM-grp12.git && cd OptiPIM-grp12
  git checkout member1        # until my PR is merged into main
  make python_env && source optipim_env/bin/activate     # Python packages only, no LLVM
  git checkout -b member<N>   # your own branch; PR into main with one reviewer
Send me your GitHub username so I can add you as a collaborator.

==================================================
2. MEMBER 2: BASELINE HEURISTIC (weight-parallel, paper Sec. 6.4.1)
==================================================
Why: the course says "implement the baseline". The authors ship heuristic results only as trace files, not code, so we must write the generator ourselves and show it reproduces their files.

Inputs: group12/README.md (Agreement 2: trace format), group12/operators/*.mlir, baseline_mappings/heuristic_1/{hbm_baseline,simdram_baseline}/ (C1 = 257-32_banks-ResNet50-12, C2 = 247-32_banks-ResNet50-2, C3 = 246-32_banks-ResNet50-1, M1 = 0-32_banks-bert-0, M2 = 1-32_banks-bert-1; each has 0.trace), paper Sec. 6.4.1, plan PDF Sec. 3 Step 2.

Task 2.1, due Wed 21 Oct (Gate 1): group12/scripts/heuristic.py for conv2d.
  Rule: tile weights to SIMD-lane size (16 FP16 lanes on HBM-PIM, a full row on SIMDRAM); spread tiles bank -> column -> row; K (output channels) goes to level 2 (banks) first; every output stays in one bank; inputs streamed at level 0; stride-1 indexing only.
  Usage to aim for: python3 group12/scripts/heuristic.py C1 hbmpim > group12/mappings/hbmpim/C1/heuristic.trace
  Check: must match the shipped C1 HBM-PIM trace exactly: Level 2 K=32; Level 1 K=4 P=28 Q=4; Level 0 Q=7 C=128 R=3 S=3.
    diff <(grep -E 'Bound|Coeff|Tag' group12/mappings/hbmpim/C1/heuristic.trace) <(grep -E 'Bound|Coeff|Tag' baseline_mappings/heuristic_1/hbm_baseline/257-32_banks-ResNet50-12/0.trace)
    python3 group12/scripts/score_analytical.py hbmpim group12/mappings/hbmpim/C1/heuristic.trace   # expect finalPerformance 29546496
  Output: heuristic.py + C1 heuristic.trace for both targets, pushed on branch member2.

Task 2.2, due Sat 24 Oct: add gemm (M1) and batched matmul (M2), plus C2, C3. Write group12/scripts/check_heuristic.py that diffs all 10 of your traces against the shipped heuristic_1 files and prints same/DIFFERENT. Every difference is either a bug or a documented choice (write it down). Note: heuristic_1 and heuristic_2 differ on SIMDRAM C1/C2; find out what rule each one follows.
  Expected heuristic_1 costs to reproduce (analytical model): HBM-PIM C1 29,546,496, C2 29,546,496, C3 3,282,944, M1 835,584, M2 614,400; SIMDRAM C1 65,549,429, C2 36,395,701, C3 4,053,173, M1 24,881,280, M2 7,769,472.
  Output: 10 heuristic.trace files in group12/mappings/<target>/<op>/, check_heuristic.py, PR into main.

Task 2.3, due Mon 26 Oct (Gate 2): notes on the baseline method for the report (1/2 page: the rule, how our code implements it, which files it matches, any differences). Also review my member1 pull request this week (Files changed -> Review -> Approve or comment).
  Extra if time: read the HBM-PIM matmul cost in lib/Analysis/DataLayout/DataLayoutFC.cpp and tell Member 3 whether it leaves out input/weight loading (our guess for why OptiPIM loses on M1).

Task 2.4, due Fri 30 Oct: extension support for Member 4: make heuristic.py work on the padded/awkward shapes (e.g. 197x768x2304) so the extension can be compared against the heuristic too, and run the SIMDRAM side (or idea E, lower precision, if the team picks it).

Task 2.5, due Sat 31 Oct: report sections "Background and the paper's idea" + "Baseline method" + related work (IEEE two-column, Overleaf). Start from group12/analysis/REPORT_SKELETON.md sections II and III-D.
Task 2.6, due Mon 2 Nov: slides on the paper's key idea (3-level loop split, flexible indexing, ILP with PIM costs).
Hand to: Member 3 (your heuristic traces), Member 4 (heuristic on padded shapes), Pari (report text).

==================================================
3. MEMBER 3: EVALUATION AND FIGURES
==================================================
Inputs: group12/analysis/ (score_traces.py, plot_results.py, parse_mapping.py, rerun.sh, manifest.csv, REPORT_SKELETON.md, README.md; I am pushing this folder now), group12/results/*.csv, group12/scripts/score_analytical.py and sim_check.sh, validation/ (authors' analytical model and validation.py).

Task 3.1, due Tue 20 Oct: run the existing scorer and reproduce our numbers.
  bash group12/analysis/rerun.sh . . group12/results/plots     # args: <optipim_root> <group_repo_root> <outdir>; both are our repo
  Check group12/results/plots/summary.csv against the table in section 1. Fix the results CSV schema (README Agreement 3) with the team.

Task 3.2, due Thu 22 Oct: group12/scripts/evaluate.py = one command that scores every trace (optipim + heuristic, both targets) with the analytical model and merges simulator cycles from sim_check.csv into group12/results/results.csv (columns: operator,target,mapper,banks,precision,analytical_cycles,simulated_cycles,compute,input_loading,output,solve_seconds). Reuse score_traces.py (it already has the stride/dilation fix). Find which model fields make up compute vs input loading vs output (look at validation/analytical_modeling/analytical.py; inLoadingCost, outTransCost, numFilPELoading are there) and write the mapping in the README.

Task 3.3, due Sun 25 Oct: speedup bars and cost-breakdown stacks per operator and target, compared with paper Figs. 10-11; C1 case-study table (OptiPIM vs heuristic L0/L1/L2 factors with parse_mapping.py) compared with paper Fig. 12. Note: our C1 mapping differs from Fig. 12(b) (we use all 32 banks: Q=2, C=16 on banks) and that is fine, but say so.

Task 3.4, due Mon 26 Oct (Gate 2): analytical vs simulator correlation (paper Fig. 9) on about 20 mappings per target: our 10 + heuristic traces + random valid traces from validation/ (validation.py calls generate_random_traces(32, device_tag, 0, 40, trace_path, "data/dram.json")). Plot log-log, report R^2. Must-do points:
  - simulate the HBM-PIM M1 heuristic trace (to confirm OptiPIM really loses on M1, today it rests on the model only);
  - simulate C1 and C2 (slow, run overnight with nohup);
  - investigate the SIMDRAM 1.4-1.8x model/sim gap: run the authors' validation on a few of their own SIMDRAM traces and compare with exp_results/fig9/validation_simdram.csv.
  The simulator needs a build. Either build only Ramulator2 in simulator/ on WSL/Linux (lighter than LLVM; check build_optipim.sh for the exact cmake steps, untested by us), or send me the trace list and I run: bash group12/scripts/sim_check.sh <optipim|heuristic> <ops>

Task 3.5, due Sat 31 Oct (Gate 3): all figures frozen, every figure generated from results.csv by one command (make figures or rerun.sh).
Task 3.6, due Mon 2 Nov: report section "Baseline results compared with the paper" (REPORT_SKELETON.md section IV already has the numbers and open questions) + slides "baseline vs paper".
Hand to: everyone (results.csv and plots), Member 4 (evaluator for padded shapes), Pari (numbers for the final consistency pass).

==================================================
4. MEMBER 4: EXTENSION ("add something new")
==================================================
Chosen idea A: padding loop bounds that do not factorize well. The paper assumes perfect factorization (Sec. 5.1.1: loop tiles must be exact divisors), so a prime size like 197 (ViT tokens) or 50257 (GPT-2 vocab) cannot be spread across banks/columns. We zero-pad to a nearby smooth size (197 -> 200), solve with unchanged pim-opt, and keep the cheapest. Backup idea E: lower precision (8/4-bit) on SIMDRAM.

Inputs (I am pushing these now): group12/docs/padding/DESIGN.md (read first), group12/docs/padding/README.md (how to run), group12/scripts/pad_search.py, run_padding_eval.sh, plot_padding.py. pad_search.py needs only Python 3 standard library; the plot needs matplotlib.
Status: scripts written and checked with a fake solver (all 109 generated .mlir files pass the MLIR verifier), but NOT yet run with real pim-opt/Gurobi. Expected (rough prescreen, not ILP): SIMDRAM gains ~1.64x ViT attention, ~1.14x ViT QKV, ~1.16x GPT-2 LM head; no gain on AlexNet or HBM-PIM.

Task 4.1, due Tue 20 Oct: read DESIGN.md and the paper Sec. 5.1.1; confirm the list of awkward shapes (AlexNet l0/l1/l2/l5 as control, ViT attention 12x197x64x197, ViT QKV 197x768x2304, GPT-2 LM head 1x768x50257, ResNet-50 7x7 stage-5 conv). Operator files at 32 banks already exist (group12/operators/).

Task 4.2, due Sun 25 Oct: prototype run.
  a) On your laptop, no solver needed: python3 group12/scripts/pad_search.py --shape 'batch_matmul:N=12,P=197,Q=64,R=197' --name vit.attn_qk --device simdram --banks 32 --dry-run   (lists candidates, writes .mlir files)
  b) Real runs need pim-opt + Gurobi: on my machine (send me the commands) or your own build. First the 2-minute sanity check in README step 2. Its expected numbers (SIMDRAM 6.498367e+07, HBM-PIM 8.189120e+05) come from my old 16-bank AlexNet smoke run with default presolve; HBM-PIM may differ slightly now because pad_search.py turns presolve off on HBM-PIM (compare with OPTIPIM_PRESOLVE_FIX=0).
  c) Then: bash group12/scripts/run_padding_eval.sh quick
  Important: pad_search.py ranks variants by pim-opt's "Real Cost", which is NOT the analytical model (rule a above). Re-score the best and unpadded traces (results/padding/<layer>/<device>/<variant>/Group.txt) with Member 3's scorer before claiming any gain. Use --banks 32 for the final runs so results match the baseline.

Task 4.3, due Mon 26 Oct (Gate 2): final extension idea agreed by the team (A, or A + E).
Task 4.4, due Thu 29 Oct: idea A results on both targets (the plan said HBM-PIM first, but the design predicts gains mostly on SIMDRAM, so run both). Compare: best padded vs unpadded OptiPIM vs heuristic (Member 2's heuristic.py on the same shape). Include the cases where padding does not help. Decide whether to add idea E.
Task 4.5, due Sat 31 Oct (Gate 3): extension results and plots frozen (padding_summary.csv, padding_speedup.png, padding_tradeoff.png); simulate at least one padded trace to show the gain holds in Ramulator2.
Task 4.6, due Mon 2 Nov: report sections "Problem and motivation" + "Our contribution and results"; slides for the same.
Hand to: Member 3 (padded traces for scoring), Pari (any shape to solve: put group12/operators/<ID>.mlir with num_banks = 32, I run bash group12/scripts/run_optipim.sh <ID> <target>).

==================================================
5. MEMBER 1 (ME) STILL TO DO
==================================================
- now: PR member1 -> main inside our repo, add you as collaborators
- Mon 26 Oct (Gate 2): fresh-clone rerun: bash group12/scripts/gate2_fresh_clone.sh https://github.com/parikhwal291/OptiPIM-grp12.git
- Fri 30 Oct: root README pointer to group12/docs/SETUP.md, Docker build test (needs 40 GB free)
- any time: run solver/simulator jobs you send me
- Mon 2 Nov: slide "Tools and setup"; Tue 3 Nov: final consistency pass of the whole report (same names C1..M2, units, every number from the CSVs)

==================================================
6. TEAM DATES
==================================================
Wed 21 Oct  Gate 1: tools work, heuristic C1 matches
Mon 26 Oct  Gate 2: baseline complete (all 5 ops, both targets, both mappers, scored + simulator check)
Sat 31 Oct  Gate 3: all results and figures frozen
Mon 2 Nov   report sections + slides done (each person writes their own part on Overleaf, IEEE two-column)
Tue 3 Nov   rehearse presentation together
Wed 4 Nov   Gate 4: submit report, slides, code
Short daily check-in until 26 Oct, then every other day. If you are blocked for more than a day, say so in the group.

Report: each person writes the sections for their own module, plus one line for "what each member did". Overleaf link: [I will share].
