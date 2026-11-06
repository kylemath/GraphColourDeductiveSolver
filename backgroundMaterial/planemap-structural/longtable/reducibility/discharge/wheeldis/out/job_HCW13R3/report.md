# job HCW13R3: Lean hC and occurrence glue for the 27 swarm W13 round-3 C configurations (Studio, 6 Nov)

**Inputs:** md5 29efa850 (extra_hcW13r3.tsv); x1 split a3151887 = extra.tsv. There are 27 rows. By ring: 12: 4, 13: 16, 14: 7.

## Two engines (eng/verdicts.tsv; kc -t 600 -C -x X and cfast --fixed X; kc 07e79fae, cfast de59e72f)
**27 / 27 are C on both engines with the given X** (kc: adm=yes, leftover 0; cfast: C-REDUCIBLE, leftover 0).

| # | name | ring | X | kc | cfast |
|---|---|---|---|---|---|
| 0 | b7_u555.577_.....5. | 12 | {I0-I1} | C | C |
| 1 | b7_u555.577_.5...5. | 12 | {I0-I1} | C | C |
| 2 | b7_u555.577_5....5. | 12 | {I0-I1} | C | C |
| 3 | b7_u57575.._.55.5.. | 12 | {I0-I3} | C | C |
| 4 | b7_u556775._...5... | 13 | {I0-I5} | C | C |
| 5 | b7_u5665.67_.....5. | 13 | {I0-I1} | C | C |
| 6 | b7_u5556776_....5.. | 13 | {I0-I1} | C | C |
| 7 | b7_u5557577_.....5. | 13 | {I0-I1} | C | C |
| 8 | b7_u556775._..55... | 13 | {I0-I5} | C | C |
| 9 | b7_u556775._5..5... | 13 | {I0-I1} | C | C |
| 10 | b7_u57575.._755.... | 13 | {I0-I3} | C | C |
| 11 | b7_u555.577_5....57 | 13 | {I0-I1} | C | C |
| 12 | b7_u555.577_57...5. | 13 | {I0-I1} | C | C |
| 13 | b7_u555.577_75...5. | 13 | {I0-I1} | C | C |
| 14 | b7_u5556776_5...5.. | 13 | {I0-I1} | C | C |
| 15 | b7_u5557577_.5...5. | 13 | {I0-I1} | C | C |
| 16 | b7_u5557577_5....5. | 13 | {I0-I1} | C | C |
| 17 | b7_u556775._56.5... | 13 | {I0-I1} | C | C |
| 18 | b7_u57575.._.5575.. | 13 | {I0-I3} | C | C |
| 19 | b7_u575757._.55.5.. | 13 | {I0-I3} | C | C |
| 20 | b7_u55.5777_...5.5. | 14 | {I0-I5} | C | C |
| 21 | b7_u5566677_.....5. | 14 | {I0-I1} | C | C |
| 22 | b7_u55.5777_5..5.5. | 14 | {I0-I1} | C | C |
| 23 | b7_u5556777_...5.5. | 14 | {I0-I1} | C | C |
| 24 | b7_u5566677_5....5. | 14 | {I0-I1} | C | C |
| 25 | b7_u5556777_.5.5.5. | 14 | {I0-I1} | C | C |
| 26 | b7_u5566677_56...5. | 14 | {I0-I1} | C | C |

## Lean hC (lean/; build ~/studio_lean_builds/rsst118_fb35d2d1, lean v4.35.0-rc3, no lake)
| module | exit | sorry | wall | peak RSS |
|---|---|---|---|---|
| CW3: XRData ok, admissibleX, foldSafeX | 0 | 0 | 5 s | 3.0 GB |
| W3V00: hC_0, b7_u555.577_.....5. (r12) | 0 | 0 | 71 s | 2.9 GB |
| W3V01: hC_1, b7_u555.577_.5...5. (r12) | 0 | 0 | 62 s | 2.9 GB |
| W3V02: hC_2, b7_u555.577_5....5. (r12) | 0 | 0 | 63 s | 2.9 GB |
| W3V03: hC_3, b7_u57575.._.55.5.. (r12) | 0 | 0 | 63 s | 2.9 GB |
| W3V04: hC_4, b7_u556775._...5... (r13) | 0 | 0 | 736 s | 3.0 GB |
| W3V05: hC_5, b7_u5665.67_.....5. (r13) | 0 | 0 | 522 s | 2.9 GB |
| W3V06: hC_6, b7_u5556776_....5.. (r13) | 0 | 0 | 277 s | 2.9 GB |
| W3V07: hC_7, b7_u5557577_.....5. (r13) | 0 | 0 | 296 s | 3.0 GB |
| W3V08: hC_8, b7_u556775._..55... (r13) | 0 | 0 | 297 s | 2.9 GB |
| W3V09: hC_9, b7_u556775._5..5... (r13) | 0 | 0 | 442 s | 2.9 GB |
| W3V10: hC_10, b7_u57575.._755.... (r13) | 0 | 0 | 378 s | 3.0 GB |
| W3V11: hC_11, b7_u555.577_5....57 (r13) | 0 | 0 | 310 s | 3.0 GB |
| W3V12: hC_12, b7_u555.577_57...5. (r13) | 0 | 0 | 265 s | 3.0 GB |
| W3V13: hC_13, b7_u555.577_75...5. (r13) | 0 | 0 | 267 s | 2.9 GB |
| W3V14: hC_14, b7_u5556776_5...5.. (r13) | 0 | 0 | 252 s | 2.9 GB |
| W3V15: hC_15, b7_u5557577_.5...5. (r13) | 0 | 0 | 267 s | 2.9 GB |
| W3V16: hC_16, b7_u5557577_5....5. (r13) | 0 | 0 | 268 s | 2.9 GB |
| W3V17: hC_17, b7_u556775._56.5... (r13) | 0 | 0 | 247 s | 3.0 GB |
| W3V18: hC_18, b7_u57575.._.5575.. (r13) | 0 | 0 | 266 s | 2.9 GB |
| W3V19: hC_19, b7_u575757._.55.5.. (r13) | 0 | 0 | 260 s | 2.9 GB |
| W3V20: hC_20, b7_u55.5777_...5.5. (r14) | 0 | 0 | 2,782 s | 3.0 GB |
| W3V21: hC_21, b7_u5566677_.....5. (r14) | 0 | 0 | 1,650 s | 3.0 GB |
| W3V22: hC_22, b7_u55.5777_5..5.5. (r14) | 0 | 0 | 1,638 s | 3.0 GB |
| W3V23: hC_23, b7_u5556777_...5.5. (r14) | 0 | 0 | 1,267 s | 3.0 GB |
| W3V24: hC_24, b7_u5566677_5....5. (r14) | 0 | 0 | 1,468 s | 3.0 GB |
| W3V25: hC_25, b7_u5556777_.5.5.5. (r14) | 0 | 0 | 1,149 s | 3.0 GB |
| W3V26: hC_26, b7_u5566677_56...5. (r14) | 0 | 0 | 1,113 s | 3.0 GB |
| W3VAll: hC_all (Fin 27) | 0 | 0 | 5 s | 3.0 GB |

Axioms (from `#print axioms` in the logs): propext, Classical.choice and Quot.sound, plus native_decide aux. sorryAx appears in 0 logs.

## Occurrence glue (Opus gen_occ_kc, 7c9f4f51; copied byte-identical into lean/; cmp in/glue vs lean/ is clean)
- HWR3_xx and COccHWR3_xx: 54 modules, all exit 0, sorry 0, error 0.
- HWR3Occ (md5 118318be): exit 0, sorry 0, error 0, 4 s wall, built after W3VAll.
- check_literals_c (f49a5b47): 0 mismatches (27 rows).

## Verdict
**HCW13R3: 27 / 27 C on kc and cfast, and 27 / 27 have Lean hC plus occurrence glue, sorry 0, across 84 module builds, all exit 0.**

**Independence:** the C verdicts come from Studio kc and cfast, our engines. hC is the repo cReducible18 kernel via our gen_ccover3.
Only the occurrence glue is Opus-generated; I compiled it unmodified. I read no Opus engine code.
