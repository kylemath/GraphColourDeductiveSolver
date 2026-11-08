# K3CHK9 (Studio, 8 Nov): the 5 kills of kills_K5b_0525.tsv (dd5a0e7f, 4f25deb7c) — 5 / 5 PASS
Procedure as K3CHK8 (k9chk.py; per-kill reports in <tag>/report.md): config from kc line = window (iso, interior + degrees), engines, Lean admissibility (C), rim pin (none: all X interior), rotation-preserving occurrence (K3CHK occurs) on every claimed row.
| tag | kill | verdict | engines | Lean admissibility | claimed rows occurring |
|---|---|---|---|---|---|
| L1 | b7_u86..665_5...555 X={I0-I1} | PASS | kc -x adm=yes leftover 0; cfast --fixed C, leftover 0 | CK5BL1 exit 0 | 1/1 (7/8676665/5667555) |
| L2 | b7_u5656777_5...5.5 X={I0-I1} | PASS | same | CK5BL2 exit 0 | 1/1 (7/5656777/5676575) |
| L3 | b8_u755..556_66...5.. D | PASS | kc -C D; dfast18 D | (hD job) | 1/1 (8/75576556/66666566) |
| U1 | b9_u5555...57_5.......6 X={I0-I1} | PASS | kc -x adm=yes leftover 0; cfast C, leftover 0 | CK5BU1 exit 0 | 84/84 |
| U2 | b9_u5565.55.6_5....5..6 X={I0-I1} | PASS | same | CK5BU2 exit 0 | 4/4 |

**Coverage of the 94 ST-44 tneg d9 violators** (cover94.py / cover94.tsv; occurrence tested on all 94 rows, not only the claimed ones): U1 84, U2 4, U1 ∪ U2 = 88.
The 6 not covered are exactly the ST-44 binding d9 class (load 3.029833245): 555557569/958587755, 555559657/585955778, 555575695/585877559,
555596575/859557785, 555756955/858775595, 555965755/595577858.

Lean jobs (drive_k5b.sh, start after HCK5H01 GLUEDONE, ahead of HDK3b/HCK3C4/HDK3c/HOFFC7): HCK5b_L1, HCK5b_L2, HCK5b_U1, HCK5b_U2 (CK5B<tag> + K5B<tag>V00 + K5B<tag>VAll),
HDK5b_L3 (gen_hd f743a82d: HDK5BL3 + HDK5BL3V00 + HDK5BL3All).
