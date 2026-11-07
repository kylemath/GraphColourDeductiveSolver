# K3CHK2 (ST-13b): second-engine check of the 4 K-3 kills of 03:45Z (Studio, 7 Nov)
Inputs: 4dd5a8a5 ext_handoff_nov3/k3/chk2/ (new_kills_0345.tsv 990098f2, updated k3_hits / binding_coverage / binding_classes); kc lines from the last column (configs.kc).

## Engines
| config | ring | m | verdict | kc -C -s 60 -t 600 (07e79fae) | dfast18 (07cb1e0b) / cfast (de59e72f) |
|---|---|---|---|---|---|
| b8_u.56656.._..566... | 13 | 9 | D | D (66,430 = reached) | dfast18 D |
| b8_u.56.5556_56....5. | 13 | 10 | D | D | dfast18 D |
| b8_u.56.5756_.5..555. | 13 | 11 | D | D | dfast18 D |
| b9_u655...566_66......5 | 14 | 10 | C, X = {I5-I6} | kc -C finds C-REDUCIBLE X={I5-I6} (16 tested, 16 admissible); kc -C -x {I5-I6}: adm=yes, leftover 0 | cfast --fixed I5-I6: C-REDUCIBLE, leftover 0 |

**C admissibility of b9 (X = {I5-I6}):** X is one interior edge, **not rim-pinned**. kc's admissibility test (adm=yes) passes, and in Lean
(lean/CK3C2.lean, gen_ccover3 XRData): **XRData.ok, admissibleX (contracted map: no loops, no multiple edges, rim conditions) and foldSafeX all
proved** (CK3C2 exit 0, sorry 0; axioms propext / Quot.sound + native_decide aux). cReducible18 hC: lean/K3C2V00 (building; status.txt).

## Occurrence in the BINDING rows (rowcheck.py, per_row.tsv; row's own 2-ball, Z-consistent by construction, rotation-preserving)
| config | covered rows where it is the listed killer | occurs | uncovered rows at its d | occurs there | covered rows of other killers (info) |
|---|---|---|---|---|---|
| b8_u.56656.._..566... | 5 | **5 / 5 PASS** | 0 (no uncovered d=8 class left) | - | 0 of 143 |
| b8_u.56.5556_56....5. | 5 | **5 / 5 PASS** | 0 | - | 0 of 143 |
| b8_u.56.5756_.5..555. | 4 | **4 / 4 PASS** | 0 | - | 0 of 144 |
| b9_u655...566_66......5 | 3 (555665666, 556665666) | **3 / 3 PASS** | 2 | **0 (2 / 2 PASS)** | 0 of 10 |

17 covered rows in total, as listed. Verdict: all 4 confirmed (3 D on kc + dfast18; b9 C on kc + cfast with the same X, admissible, not rim-pinned).
