# 21-theta-s6: decisive test of NightThetaAttempt.md section 6 [exploratory, computed]

Run: `nice -n 10 python3 s6.py N` for N = 16..20 (single core, AC power, total under 10 s). Outputs: `out-N.json` (summary + meander-key tables), `log-N.txt`.

## What was done (my reading of section 6)
- All degree-5 holes of all gentri graphs tri16..tri20 (3, 4, 12, 23, 73 graphs). States are canonical 4-colourings of T - v (engine `common/kempe_py.py`, `Space`). Ground truth DL, R+3 and DD come from vertex Kempe swaps (K = comp_{alpha,A}(x_{j+2})), lock 1 and lock 2 as in MathQuarterFloorBijections section 0.
- Tait picture computed independently from the dual cubic graph of T - v (edge colour = XOR of Z2^2 vertex colours, alpha=0, mu=p, A=q, B=r). B1 = (p,r)-path from stub e_{j+1} to e_{j+3} (asserted for every DL state). C = (q,r)-path from e_{j+2} to e_{j+4} (asserted). r-edges of B1 in order, k of them.
- Two-curve case: every r-edge of B1 lies on C. Meander key = (k, order in which C visits the r-edges with its direction relative to B1, the side (Heawood sign) of the q-stub at both ends of each r-edge). The test: is DD a function of the key; list DD vs non-DD keys.
- Extra record per DL state: `extra` = number of distinct (q,r)-components other than C that contain an r-edge of B1 (0 = two-curve case). Histograms for DD and non-DD in out-N.json.
- Sanity: DD counts match the note (554 at orders 16-18, 1129 at 16-19, 395 two-curve DD).

## Findings
1. **Section 6's model as stated is incomplete.** The vertex swap of K swaps p<->r on all of the boundary of K, not just on B1: boundary of K can include extra (p,r)-cycles (holes of K). Predicting DD by swapping B1 only (the section 6 "reconnection model") disagrees with the truth on many states (order 20: 2,932 states in all, of which 606 are two-curve; see `predB_mismatch*` in out-N.json), even for some two-curve states. Predicting by the true swap of the whole boundary of K agrees with DD in every state at all five orders (0 mismatches; `predK_mismatch`): the criterion "(q,r)-chain from e_{j+2} ends at e_{j+3}" is exact.
2. **Literal test: DD is NOT a function of the two-curve meander key.** Mixed keys (same key, both DD and non-DD): 0 at orders 16, 17, 18; 2 at order 19; 22 at order 20.
3. **Corrected test: DD IS a function of the meander key in the "pure" two-curve case** (every r-edge of B1 on C and the boundary of K equal to B1, no extra (p,r)-cycle): 0 mixed keys at all orders 16-20, and the B1-only prediction has 0 mismatches there.

## Counts (DL states; two-curve = extra == 0; pure = also boundary of K is B1 only)
| order | graphs | holes | DL | DD | two-curve DD | two-curve non-DD | pure two-curve DD | pure two-curve non-DD | distinct keys (DD only / non-DD only / mixed) | pure keys (DD only / non-DD only / mixed) |
|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 3 | 38 | 144 | 36 | 4 | 4 | 4 | 0 | 2 (1/1/0) | 1 (1/0/0) |
| 17 | 4 | 49 | 775 | 340 | 149 | 157 | 131 | 115 | 105 (40/65/0) | 77 (32/45/0) |
| 18 | 12 | 156 | 1345 | 178 | 58 | 288 | 58 | 196 | 130 (16/114/0) | 88 (16/72/0) |
| 19 | 23 | 306 | 3523 | 575 | 184 | 753 | 165 | 480 | 471 (64/405/2) | 293 (54/239/0) |
| 20 | 73 | 1001 | 17979 | 3922 | 1139 | 3941 | 980 | 2630 | 2129 (340/1767/22) | 1446 (266/1180/0) |

Two-curve frequency among DD states: 11.1%, 43.8%, 32.6%, 32.0%, 29.0% at orders 16..20 (order 16-19: 395/1129 = 35.0%). Number of other (q,r)-chains meeting B1's r-edges among DD states (0/1/2/3): order 20: 1139 / 2017 / 753 / 13; order 19: 184 / 251 / 132 / 8; order 18: 58/95/25/0; order 17: 149/130/61/0; order 16: 4/20/12/0. Non-DD histograms in out-N.json (`extra_hist_nonDD`).

Caveats: the keys are compared across graphs assuming one orientation convention (gentri output); orders 21+ not run (cap). Meander key lists are in out-N.json under `keys` and `pure_keys` ([DD count, non-DD count] per key).
