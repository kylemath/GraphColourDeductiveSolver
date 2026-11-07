# k86AS: SEPARATE LANE on the prelim A-5 rule file (Opus, 7 Nov 04:20Z). Counts only after Studio ST-15 passes.

Rule file rules_c67fa1d1_plus_A5_twins.json (363dd708): checked here to be c67fa1d1 + exactly 162 added rules, nothing removed
(d7_w6 +38, d8_w6 +78, d9_w6 +10, d7_w7 +12 per side, d8_w7 +6 per side). Everything else = W13+K3b (args_A97_F_W13K3b.txt d9ff1fe6) + rpatN 8b90a842 + 151 keys + c6le.

Replay of sol_c_repaired at t = 0.041565: 163 violated rows on c67fa1d1 -> **2 rows** on 363dd708. Every d7 row is gone (5569757, 5768578, 5568757, 5658678, 5758578, 5577658, 5677657). Left: d9 555657658, 2 rows, max excess 0.021860 (856756555 / 556576578).
sol_crep_qA.json (ae4a873a) = crep with t raised to 0.063430: **UPPER-R2 FEASIBLE at t = 0.063430 [P, prelim]** (upper_A_crep_qA.log).
If ST-15 passes the 162 twins this becomes t* <= 0.06343 on W13+K3b + 363dd708; the [E2] chain on c67fa1d1 (0.075004, k86MS/k86ML) is untouched.
Next binder for crep on this file: d9 555657658 only; killing it would take crep to its own t = 0.041565.
k86AS (in-out ladder from sol_crep_qA) runs as a third lane from 04:20Z.
