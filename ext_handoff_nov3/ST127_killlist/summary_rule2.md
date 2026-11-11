**The 426 leaves** (W6b cf_still.tsv, read into the spec window): d6 T (9+ far link neighbour): 197; d6 distance 2 only: 148; d7 T2 (9+ gap): 75; d7 distance 2 only: 6. Charges and contained configurations reproduce W6b exactly (d6: lo = hi = 2, only 2.126; d7: lo = hi = 1, only 128.1324802).

**Refinements of the 154 distance-2 leaves.** Two kill sets: (P) the proof set: 582 proved + the 184 SUB/SUB2 substitutes + nl2208_r13 (`proofset185_kc.txt`); (B) the broad pool: 582 proved + 2026 set (8,200) + all 310 W6b C/D windows (`pool310_kc.txt`).

| target set of the rule (9-valued variables of the leaf) | leaves | refinements with every target at 5..8 | not killed (P) | leaves with one (P) | not killed (B) | leaves with one (B) |
|---|---|---|---|---|---|---|
| every vertex adjacent to the occurrence | 154 | 3952 | 1408 | 49 | 875 | 35 |
| the partner b's three far neighbours (2.126) | 148 | 2368 | 616 | 43 | 107 | 29 |
| the vertex opposite u in b's rotation (2.126) | 148 | 592 | 592 | 148 | 592 | 148 |
| apexes next to the gap spokes (128.1324802) | 6 | 126 | 126 | 6 | 120 | 6 |

Every 2-ball variable at 5..8 (DFS with kill pruning), kill set (P): **49 of 154 leaves** keep a refinement that nothing kills (d6: 43 of 148, so 105 d6 leaves are killed in every refinement; d7: 6 of 6), 0 capped. The witnesses are verified on pubrules + rsst_rows (`results/witnesses_proofset.tsv`): lo = hi = e, no proved configuration and nothing from the kill set contained, only none configurations, no 9+ vertex in u's 2-ball. With N2 added, the d7 witnesses have hi <= -1.

Every 2-ball variable at 5..8 (DFS with kill pruning), kill set (B): **35 of 154 leaves** keep a refinement that nothing kills (d6: 29 of 148, so 119 d6 leaves are killed in every refinement; d7: 6 of 6), 0 capped. The witnesses are verified on pubrules + rsst_rows (`results/witnesses_pool310.tsv`): lo = hi = e, no proved configuration and nothing from the kill set contained, only none configurations, no 9+ vertex in u's 2-ball. With N2 added, the d7 witnesses have hi <= -1.

**Receivers u of degree d >= 9** (d9bb_r2; old = d9plus, 71 parts only; kills K582 in the engine, +2.126 for the N2-only variant; survivors = leaves the substitute pool does not kill):

| d | old: no kills / K582 | variant | no kills, only where a new part fits | K582 max (all states / where a new part fits) | survivors of the pool |
|---|---|---|---|---|---|
| 9 | 24 / 7 | T1/T1b/T2 (target 9+; W6b) | 24 | 14 / 14 | 327 of 3000 (sample of 987768), search incomplete; max hi 6 |
| 9 | 24 / 7 | N1 + N2 (narrow) | 20 | 9 / 9 | - |
| 9 | 24 / 7 | N2 only, with 2.126 as a kill | 14 | 6 / 1 | 0 of 12040 |
| 10 | 20 / 3 | T1/T1b/T2 (target 9+; W6b) | 20 | 12 / 12 | - |
| 10 | 20 / 3 | N1 + N2 (narrow) | 16 | - / - | - |
| 10 | 20 / 3 | N2 only, with 2.126 as a kill | 10 | 3 / <= 0 | 0 of 136 |
| 11 | 16 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 16 | 8 / 8 | - |
| 11 | 16 / <= 0 | N2 only, with 2.126 as a kill | 6 | <= 0 / <= 0 | - |
| 12 | 12 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 12 | 4 / 4 | 0 of 83 |
| 12 | 12 / <= 0 | N2 only, with 2.126 as a kill | 2 | <= 0 / <= 0 | - |
| 13 | 8 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 8 | <= 0 / <= 0 | - |
| 13 | 8 / <= 0 | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 14 | 4 / <= 0 | T1/T1b/T2 (target 9+; W6b) | 4 | <= 0 / <= 0 | - |
| 14 | 4 / <= 0 | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 15 | - / - | T1/T1b/T2 (target 9+; W6b) | <= 0 | <= 0 / <= 0 | - |
| 15 | - / - | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 16 | - / - | T1/T1b/T2 (target 9+; W6b) | <= 0 | <= 0 / <= 0 | - |
| 16 | - / - | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |
| 17 | - / - | T1/T1b/T2 (target 9+; W6b) | <= 0 | <= 0 / <= 0 | - |
| 17 | - / - | N2 only, with 2.126 as a kill | <= 0 | <= 0 / <= 0 | - |

**Full world d6..d8** (fw_bb_r2; old = fullworld/, 71 parts; K582 leaves = positive states the in-engine kills leave):

| d | variant | K582 leaves: old / new (max hi) | survivors of the pool |
|---|---|---|---|
| 5 | N2 only, with 2.126 as a kill | 0 / 0 | - |
| 6 | T1/T1b >= 7, T2 >= 8 (link variant) | 3917 / 1282 (9) | 0 of 1282 |
| 6 | N1 + N2 (narrow) | 3917 / 2316 (9) | 0 of 2316 |
| 6 | N2 only, with 2.126 as a kill | 3917 / 0 | - |
| 7 | T1/T1b >= 7, T2 >= 8 (link variant) | 84292 / 1540391 (8) | 58 of 4000 (sample of 1540391); max hi 2 |
| 7 | N1 + N2 (narrow) | 84292 / 290715 (6) | 651 of 20000 (sample of 290715); max hi 3 |
| 7 | N2 only, with 2.126 as a kill | 84292 / 60349 (3) | 0 of 60349 |
| 8 | N2 only, with 2.126 as a kill | 55752 / 44470 (8) | 0 of 44470 |

**Tail d >= 15** (max mean of c+ over cyclic link words, Karp; charge <= 10(6 - d) + d * mean):

| tables | max c+ at a 6 / 7 hub | max mean c+ per link edge | bound <= 0 for all d >= |
|---|---|---|---|
| 71 parts (d9plus) | 6 / 6 | 6.0000 | 15 |
| + T1/T1b/T2 (d9tables) | 10 / 6 | 6.6667 | 18 |
| + N1/N2 (d9tables_n) | 7 / 6 | 6.0000 | 15 |
| + N2 only (d9tables_n2) | 6 / 6 | 6.0000 | 15 |

**Substitutes the N2-only variant uses** (RSST-SUB/SUB2 set of 184 tried first, `results/subsub2_set.txt`): 158 distinct (d7 72, d8 67, d9 35, d10 8). Outside that set: nl2208_r13 (1 leaf). Windows: fw_f7c75a21e2 144, fix_63c8a193fe 46, fw_980b7e87e4 35; all are in SUB2's checked set (P20 = fix_63c8a193fe already proved).
