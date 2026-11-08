# K3CHK10 (Studio, 8 Nov): the 8 kills of kills_K5c_0735.tsv (b3efa2c5, bdc9c8418) — 8 / 8 PASS
Procedure as K3CHK9 (k10chk.py = k9chk.py with paths/names changed; per-kill <tag>/report.md): config from kc line = window (iso, interior + degrees), engines, Lean admissibility (C),
rim pin (none: all X interior), rotation-preserving occurrence (K3CHK occurs) on EVERY claimed row.
| tag | kill | verdict | engines | Lean admissibility | claimed rows occurring |
|---|---|---|---|---|---|
| V1 | b8_u555..577_5....5.6 | D PASS | kc -C D, dfast18 D | (hD job) | 90/90 |
| V2 | b7_u555..58_75...56 | D PASS | kc -C D, dfast18 D | (hD job) | 8/8 |
| V3 | b7_u5..5677_5....55 X={I0-I4} | C PASS | kc -x adm=yes leftover 0; cfast C leftover 0 | CK5CV3 exit 0 | 3/3 |
| V4 | b8_u55557557_....676. | D PASS | kc -C D, dfast18 D | (hD job) | 3/3 |
| V5 | b7_u55775.._66.5... | D PASS | kc -C D, dfast18 D | (hD job) | 2/2 |
| V6 | b8_u56675..._..565... X={I2-I3} | C PASS | as V3 | CK5CV6 exit 0 | 2/2 |
| V7 | b7_u56785.._5.555.. X={I0-I3} | C PASS | as V3 | CK5CV7 exit 0 | 2/2 |
| V8 | b7_u56...58_6...556 X={I0-I3} | C PASS | as V3 | CK5CV8 exit 0 | 1/1 |

**Coverage of the 339 ST-46 tneg receiver rows** (cover339.py / cover339.tsv; every kill tested on every row of its degree): V1..V8 ∪ U1 ∪ U2 = **181** (d7 16/67, d8 95/196, d9 70/76).
Per kill: V1 90, V2 8, V3 3, V4 3, V5 2, V6 2, V7 2, V8 1, U1 66, U2 4. The 6 uncovered d9 rows are the ST-46 binding class (555557667/578566766 ...).
Lean jobs (drive_k5c.sh, start after out/job_K3CHK9/LEANDONE, ahead of HDK3b/HCK3C4/HDK3c/HOFFC7): HDK5c_V1, V2, V4, V5 (gen_hd f743a82d, MOD HDK5CVn, PFX hdk5cvn), HCK5c_V3, V6, V7, V8 (CK5CVn + K5CVnV00 + K5CVnVAll).
