# Config cover for tables + 868 rules (5 Nov 2026) [P, reconciled with Studio job P870]

**Result: 502 configurations (380 D, 122 C), ring-weighted Lean cost 137.75 h, exact optimum (HiGHS status 0).**
The min-cost and min-count optima coincide (both 502). The 502 are a subset of the old 527.

## Why 527 was too many
The old cover (cover_final870.tsv) covered s63 prov.pkl *requirement boxes*. A box is a product set of kill-table cells
(or l3q a2 bits); a cell lying in several boxes can be justified by any one of them. Covering every box is
conservative. The exact model covers every killed cell / cleared bit:
- KT7: 84,396 cells -> 285 distinct justifier sets; KT9 (U8 = U9): 73,342 cells -> 39 sets. Cell counts equal Studio's.
- l3q: 400 V7 + 100 V8 cleared a2 bits (mask 30) of s64_keep95p131f/tab -> 12 + 12 + 10 + 10 sets.
- Rules: the 868 = final870 (bothok.json) minus the d8_w7 mirror pair ids 7612 / 9031 (Studio ctrl 81 / 82).

## Check against Studio (out/job_P870 on main 04f2d297)
- With all 870 rules this model gives **503 (381 D, 122 C), forced 398**: the same size and forced count as Studio's 503.
- Studio's 503 covers every per-cell KT row (0 uncovered). Under the old box model it left 80 boxes uncovered, all
  boxes whose cells other chosen configs also kill.
- Dropping the mirror pair removes nl2306_r13 (its only use), giving 502.

## Names dropped from the 527 (25)
nl0044_r9 nl0059_r10 nl0060_r10 nl0146_r11 nl0148_r11 nl0169_r12 nl0298_r11 nl0333_r12 nl0428_r12 nl0429_r12 nl0431_r12
nl0432_r12 nl0433_r12 nl0436_r12 nl0440_r12 nl0584_r13 nl0585_r13 nl0591_r13 nl2306_r13 nl2927_r12 nl2935_r13
nl3409_r13 nl3436_r13 nl3698_r14 q7-_....556_....56._::::::5

## Effect on the joint headline (1,178)
W1's joint optimum treated the 527 as paid and uses 1,299 extra rules. 92 of those are justified only by the 25
names above, so 502 + 651 does not stand on its own: putting the 92 rules back needs all 25 names again (exact
set cover). The joint must be re-solved with the base as a variable. Until then **1,178 stays the total**.

## Files
- cells/build_cells.py -> cells/percell_all.pkl (md5 43b64342): cover rows. Run from P_own_lp.
- scripts/cover73pb.py SET.json OUT.tsv (env COUNT=1 for min-count).
- sets/final868.json (c69baa8f): ids into the rules_drop276 universe.
- run/cover_pb868.tsv (8e63a7b3), run/cover_pb868_count.tsv, run/cover_pb870.tsv, run/cover_pb*.log.
- run/cover_final868*.tsv: the old box model with 868 rules (526), kept for comparison.

## Measured Lean weights (Studio job_HD0, main a6ed90d5)
With hD medians 223 s / 1151 s / 6412 s for ring 13 / 14 / 15 (WMEAS=1), the optimum is **the same 502 set**
(run/cover_pb868_meas.tsv). D-side hD is about 113 CPU-h, of which ring 15 (38 configs) is about 68 h.

## Joint optimum check (swarm W1 round 8, joint868/) [E2 with W1's stock sep3r_f2bS]
- run/fR3.log: rules_R3_2095.json (a6f73d2a) + k95f_patterns/R3 (D a5a8e8e6, C 8fc9245e, rpatN 9cfb7fb2, rpat 0757785d), sol_c_repaired:
  **UPPER-R2 FEASIBLE at 0.041565**; senders 0, cons 0, d = 7..17 0 violated (exhaustive), Karp 0.5217.
- run/fN8.log: rules_868_W1.json (a972c89a, = our final868) + k95f_patterns/N8: FEASIBLE at 0.041565, same clean lines.
- Negative control (run/negR3_drop_e7_56656.log): R3 without D pattern e7_56656.6_6.6B..6_1111101 -> INFEASIBLE (10 at d = 7).
- Load: R3 C_patterns.cfast lists f7_...5566_.....5. twice (184 lines, 183 unique); the loader dedups.
- So **1,145 configurations (864 D, 281 C)** carry the fixed solution with 2,095 rules; the tables + 868 rules part is the 502.
