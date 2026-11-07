# K3CHK5 (ST-21): d8 binder of the 0.040516 point (Studio, 7 Nov)
Input: 97d8b425 ext_handoff_nov3/k3/chk5/kills_K4c_d8.tsv (51bbcd00); kc lines from its last column. Target: d8 row link 76756556 / apex 56557667.

| config | verdict | engines | Lean | rim-pinned | occurs in 76756556 / 56557667 |
|---|---|---|---|---|---|
| (1) b8_u...56556_...5.66. (r12, m9) | **D** | kc -C -s 60 -t 600 D (22,144 = reached); dfast18 D | (hD on request) | - | **YES** (rotation-preserving) |
| (2) b8_u...56556_.....66. (r12, m8) | **C, X = {I0-I3}** | kc -C finds X={I0-I3} (3 tested, 3 admissible); kc -x adm=yes, leftover 0; cfast --fixed I0-I3 leftover 0 | CK3C5: XRData.ok, admissibleX, foldSafeX proved (exit 0, sorry 0) | **no** (one interior edge) | **YES** |

Occurrence (rowcheck5.py, per_row.tsv): the row's own 2-ball frame (Z-consistent by construction), exact degrees, induced, triangles onto faces, rotation-preserving.
