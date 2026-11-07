# ST-18: Studio check of W18 A-5 FINAL (lead 7 Nov 06:37Z; ahead of Lean)

W18 final (swarm round6/W18-rule-audit/A5/final/, 06:25Z): all 274 face-set rejects re-justified, 272 by twins (97 twin configs:
79 D, 18 C in A5_twin_configs.tsv acd16d6e) + 2 by kill6_C p515 (checked in ST-15).
rules_c67fa1d1_plus_A5_twins.json FINAL = 2db75746, 6,718 rules = 363dd708 (ST-15) + exactly 112 new
(container check: d8_w6 56, d8_w7 17+17, d7_w6 8, d7_w7 7+7; 0 removed). Re-check on the Mac.

Do: (1) diff A5_twin_configs.tsv against ST-15's 45 witnesses; for every twin config not yet checked: D -> kc -C + dfast18;
C -> kc -C, kc -x X, cfast --fixed X, Lean admissibility (CA-style ok/admissibleX/foldSafeX), rim-pinned?
(2) rot/check_witness.py (rotation + explicit ZCONS) on every one of the 112 new rules with its twin (A5_274_results.tsv; mirror on -1 side).
Optionally re-run all 274 for a full-set statement. (3) 2db75746 - 363dd708 = exactly 112.
Output: out/job_ST18/ on main.
