# K3CHK4 (ST-20): the d8 binder of the 0.040940 point (ST-19) — Studio, 7 Nov
Input: 50c78448 ext_handoff_nov3/k3/chk4/kills_d8_rep2_0925.tsv (6bd0778d); kc lines from its last column.
Binder rows (ST-19 control): d8 link 56656757 / apex 66665576 and link 56657576 / apex 66667556 (the same picture up to symmetry).

| config | verdict | engines | Lean | rim-pinned | occurs in row 1 | occurs in row 2 |
|---|---|---|---|---|---|---|
| (1) b8_u.5665675_.....55. (r14, m10) | **D** | kc -C -s 60 -t 600 D (199,291 = reached); dfast18 D | (hD later) | - | **YES** (1 embedding, rotation-preserving) | **YES** |
| (2) b8_u.56656.._...66... (r13, m8) | **C, X = {I2-I3}** | kc -C finds X={I2-I3} (7 tested, 7 admissible); kc -x adm=yes, leftover 0; cfast --fixed I2-I3 leftover 0 | CK3C4: XRData.ok, admissibleX, foldSafeX proved (exit 0, sorry 0) | **no** (one interior edge) | **YES** | **YES** |

Occurrence (rowcheck4.py, per_row.tsv): frame = the row's own 2-ball (Z-consistent by construction); exact degrees, induced, triangles onto faces,
rotation-preserving (rot/rotcheck.py). Both configs kill both binder rows.
