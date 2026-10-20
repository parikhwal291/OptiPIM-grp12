# Extension: padding loop bounds that do not factorize well

Group 12, OptiPIM (ISCA 2025). Design note for the "add something new" part.

## 1. The assumption we attack

OptiPIM splits every loop bound `B` of an operator into three tiles, one per
memory level: banks (level 2), time (level 0) and columns (level 1), with
`b2 * b0 * b1 = B` exactly (paper Sec. 5.1.1 assumes perfect factorization).
In the code this is a one-hot choice over the exact divisors of `B`:

- `lib/Analysis/DataLayout/DataLayoutConv2D.cpp`, `buildConv2DOpConstants()`
  calls `getAllDivisors(loopBound)` for N, K, P, Q, C, R, S.
- `lib/Analysis/DataLayout/DataLayoutFC.cpp` does the same for matmul P, Q, R.
- `getAllDivisors()` (end of `DataLayoutConv2D.cpp`) returns only exact divisors.
- The bounds come straight from the operand types of the `linalg` op
  (`DataLayoutPass.cpp`, `parseConv2D` / `parseFC`): output P, Q; filter K, R, S;
  input N, C. The input's H and W are never read.

So a prime bound such as 13 can only go whole into one level, and a bound such
as 197 or 50257 cannot be spread across 16 banks or 8192 SIMDRAM columns at all.
Hardware lanes then sit idle, and the optimum the ILP finds is only optimal
among exact factorizations.

## 2. Which layers have awkward bounds

| Layer | Bounds | Awkward part |
| --- | --- | --- |
| alexnet.l0.conv0 | K64 C3 P55 Q55 R11 S11, stride 4 | 55 = 5·11, C = 3 |
| alexnet.l1.conv1 | K192 C64 P27 Q27 R5 S5 | 27 = 3³ |
| alexnet.l2/l3/l4 | K256–384 C192–384 P13 Q13 R3 S3 | 13 is prime |
| alexnet.l5.fc0 | P1 Q9216 R4096 | none (control) |
| resnet50 stage 5 | K512 C512 P7 Q7 R3 S3 | 7 is prime |
| ViT-B/16 attention QKᵀ | 12 × 197 × 64 × 197 | 197 tokens is prime |
| ViT-B/16 QKV projection | 197 × 768 × 2304 | 197 |
| GPT-2 LM head | 1 × 768 × 50257 | 50257 = 29 · 1733 |

AlexNet is awkward only in the spatial dims; its channel counts are powers of
two times 3, so the ILP can still fill banks and columns from K and C. The
transformer shapes are awkward in a dim that must be parallelised.

## 3. What padding changes

We zero-pad one or more bounds to a nearby "smooth" size (no prime factor above
7), e.g. 197 → 200, 50257 → 50400, 55 → 56. Results stay exact:

- padded output dims (P, Q, K, matmul P/R): extra outputs are computed on zeros
  and thrown away;
- padded reduction dims (C, matmul Q): zeros are added to the sum.

**Why it can help.** The padded bound has many more divisors, so the ILP can
use more banks / columns at once and needs fewer sequential steps.

**Why it can hurt.** Every padded element is real work and real data: more
MACs, more input loading, more output traffic, and more columns used. The
padded ILP also has more one-hot variables and may solve slower or hit the
400 s Gurobi limit.

Because pim-opt computes the Real Cost of the padded problem, the extra work is
already inside the number we compare. We do not add a separate penalty. Not
counted: the host's cost of writing zeros into the padded region (weights can be
padded offline; input zero-fill is an extra memset).

## 4. Method (no C++ change)

`pad_search.py` reads a layer `.mlir`, lists padded variants, writes each one
as a small verifier-clean `.mlir` holding only the operator, runs the unchanged
`pim-opt` on it, and keeps the lowest Real Cost (the unpadded file is always one
of the candidates, so the search never loses).

Candidate rules (all flags): each dim grows at most 25 %, total MACs grow at
most 30 %, sizes must be 7-smooth; for conv, P and Q are padded together and
R, S, N are never padded. Up to 8 candidates per layer are solved, ordered by a
cheap prescreen: padded MACs divided by the largest bank × lane product that
exact divisors allow (16 banks × 8192 lanes on SIMDRAM, 16 banks × 16 lanes on
HBM-PIM). The prescreen is our own rough compute-only proxy, not the paper's
cost model; it only decides the order of the ILP runs.

## 5. What we expect (prescreen only, not yet confirmed by the ILP)

The prescreen does not use Gurobi, so these numbers do not change with the
presolve setting; only the ILP results can.

| Layer | SIMDRAM proxy | HBM-PIM proxy |
| --- | --- | --- |
| AlexNet l0, l1, l2 | no gain | ~1.03× on l0 (P56), else none |
| ViT attention QKᵀ | 1.64× (197→200, +1.5 % MACs) | none |
| ViT QKV | 1.14× (P 197→200) | none |
| GPT-2 LM head | 1.16× (R 50257→50400) | none |
| ResNet50 stage 5 | no gain | none |

Hypothesis for the report: the perfect-factorization assumption is mostly
harmless for CNNs with power-of-two channels, but costs real performance on
SIMDRAM for transformer shapes with prime sequence lengths or vocabulary sizes,
because SIMDRAM has 131 072 lanes to fill. HBM-PIM has few lanes and saturates
anyway, so padding should rarely help there. The ILP runs decide whether this
holds; if they disagree with the proxy (data movement terms are not in the
proxy), report that and explain from the cost breakdown in `pim-opt.log`.

## 6. Limits to state in the report

- Solver setting: Gurobi 13.0.3 (the paper used 11.0.3). HBM-PIM runs turn
  presolve off (`Presolve 0` in `gurobi.env`) because presolve wrongly reported
  some 3x3 conv models infeasible; SIMDRAM runs keep the defaults because
  presolve off made a SIMDRAM matmul stop without solving. Presolve does not
  change the optimum when a solve finishes. Padded and unpadded costs are
  always compared under the same setting, and runs with no printed objective
  are reported as failed.

- Padding is searched outside the ILP; a proper fix would let the ILP choose
  non-divisor tiles with ceiling division (future work, needs C++ changes).
- Costs are OptiPIM's analytical Real Cost. Checking a few padded traces in the
  simulator is optional (the trace is a valid trace of the padded problem).
- Shapes outside AlexNet are written by hand from the published model configs
  (ViT-B/16, GPT-2 small, ResNet50), one layer each, single batch.
