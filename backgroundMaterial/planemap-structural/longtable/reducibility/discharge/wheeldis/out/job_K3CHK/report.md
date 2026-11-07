# K3CHK (ST-13 step 1): second-engine check of the two new K-3 D configurations (Studio, 7 Nov)
Inputs: 6b552b03 ext_handoff_nov3/k3/ (k3_hits.tsv 2f4aec4e, binding_coverage.tsv 19e1680e, binding_classes.tsv); kc lines from k3_hits.tsv's last column (configs.kc).

## Engines (engines.out)
| config | ring | m | kc -C -s 60 -t 600 (07e79fae) | dfast18 (07cb1e0b) |
|---|---|---|---|---|
| b8_u.56.5656_56...55. | 13 | 11 | D (classes = reached = 66,430) | D |
| b9_u...575655_...5..65. | 13 | 10 | D (66,430) | D |

## Occurrence in the BINDING rows (rowcheck.py, per_row.tsv)
Frame = grow.build2 of each row itself (u degree d, its link and apex letters; privates / ring 3 unknown, letter 9 never exact), so the
structure agrees with every w letter (ZCONS by construction). A configuration occurs iff some grow.embeddings embedding into {u, w, s}
(exact degrees, induced, interior triangles onto faces) is rotation-preserving (rot/rotcheck.py).

| config | rows listed for it (covered, best killer) | occurs (rotation-preserving) | rows of the uncovered classes at its d | occurs there |
|---|---|---|---|---|
| b8_u.56.5656_56...55. | 134 (56568567 89, 56568568 31, 56568569 14) | **134 / 134 PASS** | 14 | **0 (14 / 14 PASS)** |
| b9_u...575655_...5..65. | 10 (556575657 8, 556575658 2) | **10 / 10 PASS** | 5 | **0 (5 / 5 PASS)** |

Verdict: both are D on two engines, and each kills exactly its listed binding rows under the rotation-preserving, Z-consistent reading.
