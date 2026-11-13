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

## Wider data (13 Nov, k: "throw more data at it", include the simpler rules)

47,248 hub balls: 10,000 random per hub degree 5..8 plus 3 inside each of the 604 parts. Target: the amount the hub
sends on every edge, for every rule kind (RSST push, added push, tunnel). gen_all.py, wide.py, wide_prune.py.
Model: 21 categorical positions around the edge, single + pair features (7,686), integer multi-class perceptron,
6-bit weights. Test: 10,000 unseen random balls + balls inside held-out part families.

| rule kind | edge exact | exact on edges that carry charge | false alarms | non-zero weights |
|---|---|---|---|---|
| RSST push (single features only) | 0.893 | 0.617 | 0.017 | 666 |
| RSST push | 0.989 | 0.959 (n=18,391) | 0.001 | 27,224 |
| added push | 0.990 | 0.746 (n=1,812) | 0.004 | 17,605 |
| tunnel | 0.9997 | 0.948 (n=96) | 0.0003 | 15,565 |

Whole hub right on every edge and kind: 93.2% of random balls, 57.1% of balls inside held-out parts.
Pruning without retraining: RSST head keeps 0.912 at 11,492 weights, falls to 0.58 at 5,595.
Reading: with the simple rules in the data the model learns them (96%) and the tunnels (95%); the added pushes stay
at about 75%, the same wall as Stage 0. The flat pair model needs ~10,000 weights, more than the rules it imitates
(604 parts, 9,908 conditions), so it shows learnability, not compactness.
