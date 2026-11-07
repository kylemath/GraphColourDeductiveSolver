# ST-15: Studio second engine for W18 A-5 "frame twins" (lead, 7 Nov 04:14Z; HIGH priority)

A twin = a face-set-rejected rule's own 2-ball config rebuilt with the true rotation at the cut vertex; if reducible and it embeds
in the rule's frame under the rotation reading, the rule is sound. W18 [P] files (this folder, from swarm round6/W18-rule-audit/A5/prelim/):
- A5_twin_configs.tsv (210a7303): 43 twin configs (34 D, 9 C) with kc lines, verdict, X, W18's second engine.
- A5_274_results.tsv (4a1d400f): per-rule detail of the 274 rejects; frame_twin / twin_witness(es) columns; 160 rules justified by twins
  ("(mirror)" = mirror image of the named twin for the -1 side).
- d7_w6|0|99 and d7_w6|0|1419: justified by W13 kill6_C config b7_u.....65_.....66_p515, C X={I0-I1,I3-I5,R5-I1,R7-I5}.
- rules_c67fa1d1_plus_A5_twins.json (363dd708, 6,606 = c67fa1d1 + 162). Container check (Studio thread): multiset difference is exactly
  162 rules (d8_w6 78, d7_w6 38, d7_w7 12+12, d9_w6 10, d8_w7 6+6), 0 removed. Please re-check on the Mac.

Order: (1) twins of the 14 binding-row rules first: #392/#1154 (tw_d7_w7_p1_392_fx_0, r13 m10, C X={I1-I6}: KEY, fires on all 65 rows of
d7 5569757, binder of the 0.075004 point), #73/#1173, #443/#1128, #445/#1131, #765/#1178, #1005/#1083, #524/#1133 (D twin, r15; t524.in).
(2) the other twins, then the kill6_C witness.
Per twin: D -> kc -C + dfast18; C -> kc -C, kc -x X, cfast --fixed X, admissibility (contracted map no loops / multi-edges, rim conditions, rim-pinned?).
Per justified rule: rot/check_witness.py (rotation + explicit ZCONS) of the twin in that rule (mirror for -1 side). Lean hC later.
