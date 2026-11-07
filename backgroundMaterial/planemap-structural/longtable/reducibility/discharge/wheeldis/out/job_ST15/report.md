# ST-15: Studio second engine for W18 A-5 frame twins (7 Nov)
Inputs: 4435e084 ext_handoff_nov3/w18/a5/ (README_ST15.md, A5_twin_configs.tsv, A5_274_results.tsv, kill6C_p515.txt, t524.in, rules_c67fa1d1_plus_A5_twins.json 363dd708).

## Rule file
363dd708 (6,606) minus c67fa1d1 (6,444), as multisets: **exactly 162 added, 0 removed** (d8_w6 78, d7_w6 38, d7_w7 12+12, d9_w6 10, d8_w7 6+6),
and the 162 are exactly the twin / kill6_C-justified rules of A5_274_results.tsv (setcheck.txt). Matches the container.

## Engines (eng/verdicts.tsv; kc 07e79fae, dfast18 07cb1e0b, cfast de59e72f): **45 / 45 confirmed**
- 35 D twins (incl. tw_d7_w7_p1_524_fx_0 and tw_d7_w7_m1_1133_fx_0, r15): kc -C -s 60 -t 600 D and dfast18 D.
- 10 C (9 twins + W13 kill6_C b7_u.....65_.....66_p515): kc -C finds C; kc -C -x X: adm=yes, leftover 0; cfast --fixed X: leftover 0.
- **C admissibility in Lean** (lean/CA5C.lean, gen_ccover3 XRData with each X): XRData.ok, admissibleX (no loops / multiple edges after contraction,
  rim conditions) and foldSafeX **all proved** (exit 0, sorry 0). X: 9 twins one interior edge each (not rim-pinned); kill6_C X={I0-I1,I3-I5,R5-I1,R7-I5} is
  rim-pinned.

## Rules (rot/check_witness.py: rotation-preserving + explicit ZCONS; every placement; mirror covered by the global orientation sign)
| part | rules | PASS |
|---|---|---|
| (1) binding-row rules #392/#1154 (tw_..._392, C X={I1-I6}), #73/#1173, #443/#1128, #445/#1131, #765/#1178, #1005/#1083, #524/#1133 (D, r15) | 14 | **14 / 14** |
| (2) other twin-justified rules | 146 | **146 / 146** |
| (3) d7_w6\|0\|99 and \|1419 with the kill6_C witness (check_kill6C.tsv; their own twin tw_d7_w6_0_99 also PASS) | 2 | **2 / 2** |

**Verdict: all 162 A-5 rules are justified on the Studio engine; all 45 witnesses confirmed on two engines; all 10 C witnesses admissible in Lean.** Lean hC / hD of the twins: later.
