# W12 separator pre-check bug: Studio check (6 Nov)

**Result: the bug is real in our separator, and no verdict flips.**
- With the fix, every replayed FEASIBLE verdict stays FEASIBLE with 0 exact violators: f2b041 Tier A, keep95p131f full rules,
  and P870 (870 rules).
- The regression arrangement is lost in 4 of 14 start states by the old code and found in 14 of 14 by the fixed code.

## 1. The bug in our code
- **Where:** `sep3r_f2bS.cpp:361`, identical in `sep3r_l3q.cpp` and `sep3r_ak`. It is the first pruning test of a transition in
  `dfs()`:
  ```
  if (nw + b + (d - NRES[i + 1]) * XINMAX <= curThr() + 1e-9) continue;   // l.361
  ...
  if (HASX) { for (int j : RES[i]) nw += contrib(j);                       // l.364: RES[i] terms added only now
      if (nw + b + (d - NRES[i + 1]) * XINMAX <= curThr() + 1e-9) continue; }   // l.365: correct
  ```
- **Why it is wrong:** at line 361 the positions in RES[i] have not had their transfer terms added to `nw`, yet the bound counts
  only `d − NRES[i+1]` unresolved positions. It drops up to |RES[i]|·XINMAX of possible positive x-inflow, so a branch can be
  pruned although it contains an arrangement above the threshold.
- **When it applies:** only when HASX holds (positive x values). Otherwise XINMAX = 0 and the two tests coincide.
- **Status: confirmed.**

## 2. Search mode of each verdict
Every Studio separator run starts from **all start states a whose bound exceeds the threshold** whenever x terms are present
(`anyStartR = HASX || RMAXV > 0 || HASR || (HASL && d == 7) || HASFB`, l.517). Each arrangement is therefore searched once per
rotation, and reflections are separate arrangements. We never use one-rotation-per-class, slot masks or any symmetry reduction.
So all the listed verdicts ran in **all-rotations mode**:

| verdict | solution, tables | mode | replayed with the fix |
|---|---|---|---|
| f2b041 80287bd3 | sol_c_repaired, Tier A + outside rules | all rotations | **yes: FEASIBLE**, d = 7..17 all 0 (fixTA_d*.log) |
| keep95p131_upper fb35d2d1 | sol_c_repaired, keep95p131 | all rotations | covered by keep95p131f below (a subset forbidden set, so harder) |
| keepleak keep95p131f 55cfd103 | sol_c_repaired, keep95p131f | all rotations | **yes: FEASIBLE** (fixKF_d*.log) |
| P870 04f2d297 | sol_c_repaired, keep95p131f + 870 rules | all rotations | **yes: FEASIBLE** (fixP870_d*.log) |
| exact17_409 96a67ddd | the 17/409 files, Tier A | all rotations | not replayed; a float-tolerance verdict, rechecked exactly |
| A83 upper 0.105883918 (f9dc12ca) | A83 stack | all rotations | not replayed |
| s53 A97 0.098789 (19e90dc3) | A97 stack | all rotations | not replayed |

None ran in a restricted mode, so the coordinator's rule ("replay the restricted ones") selects none. The three replays above
cover the current 0.041565 line. A83 and A97 can be replayed on request: about 1 h each on 4 cores.

## 3. Fix and regression
- **Fix:** `sep3r_f2bS_fix.cpp` → `bin/sep3r_f2bS_fix`. The first test uses `d − NRES[i]`; `SEP_OLDPRUNE=1` restores the old line.
  A test-only command `s <a>` restricts the search to one start state. The diff against sep3r_f2bS.cpp is these lines only.
- **Regression** on the W12 example, d = 7, link 5566997 / s 5696767, keep95p131f + sol_c_repaired:
  - Its exact load is 1.041564792, a tight row.
  - For each of the 7 rotations × 2 reflections, the search was restricted to that rotation's start state, at threshold load −
    1e-7 (SEPREG in st21_check_f2b.py; reg_old1.log, reg_old0.log).

  | code | found in | lost |
  |---|---|---|
  | **old (SEP_OLDPRUNE=1)** | 10 of 14 | 4: rot 0, rot 1, rot 2 refl, rot 3 refl |
  | **fixed** | **14 of 14** | 0 |

## 4. Replays with the fixed separator (sol_c_repaired at 0.041565, receivers d = 7..17)
| run | d=7 | d=8 | d=9 | d=10..17 | DP 18..30 | Karp λ | verdict |
|---|---|---|---|---|---|---|---|
| P870 (final870 rules) on keep95p131f | 0 | 0 | 0 | 0 | clean | 0.633626 | **FEASIBLE** |
| keep95p131f full rules | 0 | 0 | 0 | 0 | clean | 0.633626 | **FEASIBLE** |
| f2b041 Tier A (outside rules, f2bA tables) | 0 | 0 | 0 | 0 | clean | 0.633626 | **FEASIBLE** |

**Class counts:**
- At the real thresholds, old and fixed both report **0 rows / 0 classes at every d** (SEPCLASS).
- A near-threshold diagnostic at d = 7 (SEPEPS −0.02, rows within 0.02 below the bound) hit the 200,000-row cap in both runs, so its
  class counts (old 14,335, fixed 14,296) come from truncated top-200k sets and cannot be compared. **It is inconclusive.** Exact
  violators were 0 in both.
- W12's 28,150 (the d = 7 class count) is not a quantity our runs report; I did not reproduce it.

## Recommendation
Use `bin/sep3r_f2bS_fix` (SEPBIN=sep3r_f2bS_fix) for all future Studio upper checks.
