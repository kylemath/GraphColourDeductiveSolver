# Stage 0 result (12 Nov 2026): imitation of the forward rules by a small integer attention step

One tool, CPU only, about 2 minutes total. Code here: gen.py (data), model.py (bit-mask features, integer perceptron),
model2.py (dense, pair features), prune.py (dedupe, dead-column removal, 6-bit rounding, magnitude pruning).
Run gen.py from a folder holding the fable code (see FABLE_IDEAS.md), the others from this folder with ../code on the path.

Task: on 4,928 concrete hub neighbourhoods drawn inside the 493 added push parts (10 per part), predict exactly
which neighbours receive the forwarded charge and how much (units of 3/60). Held out by mirror-pair family (248 families, 5 folds).

| model | numbers | train exact | held-out exact | held-out units placed |
|---|---|---|---|---|
| most slack takes all | 0 | | 0.179 | |
| two most slack share | 0 | | 0.342 | |
| linear attention, pooled bits | 55 | 0.485 | 0.442 | |
| linear, left/right one-hot | 78 | 0.493 | 0.447 | |
| pair features | 1,151 | 0.888 | 0.718 | 0.839 |
| pair, pruned | 400 | 0.897 | 0.747 | 0.859 |
| pair, pruned | 200 | 0.876 | **0.757** | 0.863 |
| pair, pruned | 100 | 0.829 | 0.714 | 0.846 |
| pair, pruned | 50 | 0.682 | 0.607 | 0.791 |
| pair, pruned | 12 | 0.400 | 0.400 | 0.703 |

Pass line was 95% with at most 200 numbers: NOT MET (76%).
Scrambled-rule comparison is not usable: scrambled parts never pair up, so every push is a single receiver and the task is easier (0.70 to 0.72 linear).
Reading: the receiver choice is partly lawful (76% vs 18 to 34% for slack rules) and pruning helps (72% -> 76% at 200),
but a quarter of pushes are not predicted, and even 1,151 features fit only 89% of the training set.
Either the features miss information or the solver's receiver choice is partly arbitrary. The engine test of
alternative receivers (is another receiver also feasible?) separates the two.
