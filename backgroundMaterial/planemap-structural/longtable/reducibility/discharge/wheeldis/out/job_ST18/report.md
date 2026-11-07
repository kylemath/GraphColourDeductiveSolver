# ST-18: Studio check of W18 A-5 FINAL (rules 2db75746) — 7 Nov
Inputs: 338ac11c ext_handoff_nov3/w18/a5final/ (README_ST18.md, A5_twin_configs.tsv 97 twins, A5_274_results.tsv, rules_c67fa1d1_plus_A5_twins.json 2db75746).

## (3) Rule file (setcheck.txt)
- 2db75746 (6,718) minus 363dd708 (6,606): **exactly 112 added, 0 removed** — d8_w6 56, d8_w7 17+17, d7_w6 8, d7_w7 7+7 (matches the container).
- 2db75746 minus c67fa1d1: exactly the 274 face-set rejects, 0 removed.

## (1) Witnesses (eng/verdicts.tsv; kc 07e79fae, dfast18 07cb1e0b, cfast de59e72f)
- 98 witnesses (97 twins + kill6_C p515); 44 were checked in ST-15 (same name, kc line and X); **54 new: 54 / 54 confirmed**
  (D: kc -C -s 60 -t 600 D + dfast18 D; C: kc -C finds C, kc -C -x X adm=yes leftover 0, cfast --fixed X leftover 0).
- **Lean C admissibility** for all 19 C witnesses (lean/CA5F.lean, gen_ccover3 XRData with each X): XRData.ok, admissibleX, foldSafeX **proved** (exit 0, sorry 0).
  Rim-pinned: **tw_d8_w6_0_1278_fx_0** (X={I5-I8,R6-I8}, new) and kill6_C p515 (X={I0-I1,I3-I5,R5-I1,R7-I5}); the other 17 are interior-only.

## (2) Rules (rot/check_witness.py: rotation-preserving + explicit ZCONS, every placement, mirror via the orientation sign)
**All 274 face-set rejects PASS with their W18 witness (274 / 274)**: the 112 new rules 112 / 112 and the 162 of ST-15 162 / 162 (check_witness.tsv).
So every rule of 2db75746 outside c67fa1d1 is justified on the Studio engine by a two-engine-confirmed, (for C) Lean-admissible witness.
