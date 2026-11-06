# job HCW13R2: Lean hC for the 45 swarm W13 round-2 C configurations (Studio, 6 Nov)

**Inputs:** 7dc38128 ext_handoff_nov3/w13r2/. extra_hcW13r2_ordered.tsv (a22b0076) and extra_hcW13r2.tsv (1437d398) match their
md5s. There are 45 rows, all with |X| = 1, interior, none rim-pinned. By ring: 12: 2, 13: 15, 14: 17, 15: 8, 16: 3. The D patterns
(pat_W13_D.out) are reference only; no hD was built.

**Split:** batch A = the 4 greedy-cover configs (extraA.tsv, ordered rows 1–4); batch B = the other 41 (extraB.tsv).

## Two engines (eng/verdicts.tsv; kc -t 600 -C -x X and cfast --fixed X; kc 07e79fae, cfast de59e72f)
**45 / 45 are C on both engines with the given X** (kc: adm=yes, leftover 0; cfast: C-REDUCIBLE, leftover 0). No config fails.

## Lean, batch A: the cover-4 (lean/; build ~/studio_lean_builds/rsst118_fb35d2d1/out_hcw13r2)
| module | exit | sorry | wall |
|---|---|---|---|
| CW2A: XRData ok, admissibleX, foldSafeX | 0 | 0 | 4 s |
| W2AV00: hC_0, b7_u567765._.55.... | 0 | 0 | 2,169 s |
| W2AV01: hC_1, b7_u5..5776_...55.5 | 0 | 0 | 341 s |
| W2AV02: hC_2, b7_u56.5776_5...5.5 | 0 | 0 | 256 s |
| W2AV03: hC_3, b7_u57575.._.5.65.. | 0 | 0 | 306 s |
| W2AVAll: hC_all (Fin 4) | 0 | 0 | 3 s |

Axioms: propext, Classical.choice and Quot.sound, plus native_decide aux. sorryAx appears 0 times.

## Lean, batch B (41): DONE
Build root ~/studio_lean_builds/rsst118_fb35d2d1/out_hcw13r2.

| module | exit | sorry | wall | peak RSS |
|---|---|---|---|---|
| CW2B: XRData ok, admissibleX, foldSafeX | 0 | 0 | 5 s | 3.0 GB |
| W2BV00: hC_0, b7_u5556677_.5...5. | 0 | 0 | 245 s | 2.9 GB |
| W2BV01: hC_1, b7_u5556677_...6.5. | 0 | 0 | 1,204 s | 3.0 GB |
| W2BV02: hC_2, b7_u5556677_.5.6.5. | 0 | 0 | 1,125 s | 3.0 GB |
| W2BV03: hC_3, b7_u5556677_.57..5. | 0 | 0 | 1,155 s | 3.0 GB |
| W2BV04: hC_4, b7_u5556677_75...5. | 0 | 0 | 1,150 s | 3.0 GB |
| W2BV05: hC_5, b7_u55575.._576...7 | 0 | 0 | 245 s | 3.0 GB |
| W2BV06: hC_6, b7_u555755._576...7 | 0 | 0 | 218 s | 3.0 GB |
| W2BV07: hC_7, b7_u555755._576.7.. | 0 | 0 | 216 s | 2.9 GB |
| W2BV08: hC_8, b7_u55575.._5766..7 | 0 | 0 | 1,188 s | 3.0 GB |
| W2BV09: hC_9, b7_u555755._5766..7 | 0 | 0 | 1,024 s | 3.0 GB |
| W2BV10: hC_10, b7_u5557557_576.7.. | 0 | 0 | 1,102 s | 3.0 GB |
| W2BV11: hC_11, b7_u555755._576..7. | 0 | 0 | 917 s | 3.0 GB |
| W2BV12: hC_12, b7_u5557557_576..7. | 0 | 0 | 1,081 s | 3.0 GB |
| W2BV13: hC_13, b7_u555755._576..6. | 0 | 0 | 208 s | 3.0 GB |
| W2BV14: hC_14, b7_u.557755_.5.5... | 0 | 0 | 69 s | 2.9 GB |
| W2BV15: hC_15, b7_u.557755_.5.5.5. | 0 | 0 | 58 s | 2.9 GB |
| W2BV16: hC_16, b7_u.5775.5_.555... | 0 | 0 | 406 s | 2.9 GB |
| W2BV17: hC_17, b7_u7557755_...5... | 0 | 0 | 369 s | 2.9 GB |
| W2BV18: hC_18, b7_u.557755_.575... | 0 | 0 | 297 s | 2.9 GB |
| W2BV19: hC_19, b7_u7557755_.5.5... | 0 | 0 | 289 s | 2.9 GB |
| W2BV20: hC_20, b7_u.557755_.575.5. | 0 | 0 | 252 s | 3.0 GB |
| W2BV21: hC_21, b7_u7557755_.5.5.5. | 0 | 0 | 246 s | 2.9 GB |
| W2BV22: hC_22, b7_u.557755_75.5... | 0 | 0 | 1,476 s | 3.0 GB |
| W2BV23: hC_23, b7_u.557755_75.5.5. | 0 | 0 | 1,305 s | 3.0 GB |
| W2BV24: hC_24, b7_u7557755_.575... | 0 | 0 | 1,342 s | 3.0 GB |
| W2BV25: hC_25, b7_u7557755_75.5... | 0 | 0 | 1,345 s | 3.0 GB |
| W2BV26: hC_26, b7_u.557755_.57575. | 0 | 0 | 1,169 s | 3.0 GB |
| W2BV27: hC_27, b7_u7557755_.575.5. | 0 | 0 | 1,157 s | 3.0 GB |
| W2BV28: hC_28, b7_u7557755_75.5.5. | 0 | 0 | 1,153 s | 3.0 GB |
| W2BV29: hC_29, b7_u.557755_7575... | 0 | 0 | 6,972 s | 3.0 GB |
| W2BV30: hC_30, b7_u.557755_75.575. | 0 | 0 | 5,865 s | 3.0 GB |
| W2BV31: hC_31, b7_u.557755_7575.5. | 0 | 0 | 5,974 s | 3.0 GB |
| W2BV32: hC_32, b7_u7557755_7575... | 0 | 0 | 6,448 s | 3.0 GB |
| W2BV33: hC_33, b7_u7557755_.57575. | 0 | 0 | 5,540 s | 3.0 GB |
| W2BV34: hC_34, b7_u7557755_75.5.57 | 0 | 0 | 5,770 s | 3.0 GB |
| W2BV35: hC_35, b7_u7557755_75.575. | 0 | 0 | 5,574 s | 3.0 GB |
| W2BV36: hC_36, b7_u7557755_7575.5. | 0 | 0 | 5,742 s | 3.0 GB |
| W2BV37: hC_37, b7_u.557755_757575. | 0 | 0 | 27,640 s | 3.1 GB |
| W2BV38: hC_38, b7_u7557755_7575.57 | 0 | 0 | 28,841 s | 3.1 GB |
| W2BV39: hC_39, b7_u7557755_757575. | 0 | 0 | 28,243 s | 3.1 GB |
| W2BV40: hC_40, b7_u5...577_...6555 | 0 | 0 | 404 s | 2.9 GB |
| W2BVAll: hC_all (Fin 41) | 0 | 0 | 4 s | 3.0 GB |

Axioms (from `#print axioms` in the logs): propext, Classical.choice and Quot.sound, plus native_decide aux. sorryAx appears in 0 logs.

## Occurrence glue (Opus gen_occ_kc, 7c9f4f51; copied byte-identical into lean/; cmp in/glue vs lean/ is clean)
- Per-config modules HW2A_xx, COccHW2A_xx, HW2B_xx and COccHW2B_xx: 90 modules, all exit 0, sorry 0, error 0.
- HW2AOcc (md5 eea2c2ca): exit 0, sorry 0, error 0, 5 s wall, built after W2AVAll.
- HW2BOcc (md5 36769e33): exit 0, sorry 0, error 0, 3 s wall, built after W2BVAll.
- check_literals_c (earlier, f49a5b47): 0 mismatches (R2A 4, R2B 41).

## Verdict
**HCW13R2: 45 / 45 C on kc and cfast, and 45 / 45 have Lean hC plus occurrence glue, sorry 0, across 141 module builds, all exit 0.**
Peak wall: W2BV38 (ring 16) took 28,841 s.

**Independence:** the C verdicts come from Studio kc (07e79fae) and cfast (de59e72f), our engines. hC is the repo cReducible18 kernel,
generated by our gen_ccover3. Only the occurrence glue is Opus-generated; I compiled it unmodified. I read no Opus engine code.
