# job HCW13R4: Lean hC and occurrence glue for the 4 swarm W13 round-4 C configurations (Studio, 6 Nov)

**Inputs:** md5 3ea965c5 (extra_hcW13r4.tsv) = extra.tsv. There are 4 rows. By ring: 13: 1, 14: 1, 15: 2.

## Two engines (eng/verdicts.tsv; kc -t 600 -C -x X and cfast --fixed X; kc 07e79fae, cfast de59e72f)
**4 / 4 are C on both engines with the given X** (kc: adm=yes, leftover 0; cfast: C-REDUCIBLE, leftover 0).

| # | name | ring | X | kc | cfast |
|---|---|---|---|---|---|
| 0 | b7_u55766.._66.5... | 13 | {I0-I4} | C | C |
| 1 | b7_u5666.67_..5..5. | 14 | {I0-I1} | C | C |
| 2 | b7_u5677757_..5.55. | 15 | {I0-I1} | C | C |
| 3 | b7_u5677757_..5.555 | 15 | {I0-I1} | C | C |

## Lean hC (lean/; build ~/studio_lean_builds/rsst118_fb35d2d1, lean v4.35.0-rc3, no lake)
| module | exit | sorry | wall | peak RSS |
|---|---|---|---|---|
| CW4: XRData ok, admissibleX, foldSafeX | 0 | 0 | 5 s | 3.0 GB |
| W4V00: hC_0, b7_u55766.._66.5... (r13) | 0 | 0 | 324 s | 2.9 GB |
| W4V01: hC_1, b7_u5666.67_..5..5. (r14) | 0 | 0 | 1,719 s | 3.0 GB |
| W4V02: hC_2, b7_u5677757_..5.55. (r15) | 0 | 0 | 7,118 s | 3.0 GB |
| W4V03: hC_3, b7_u5677757_..5.555 (r15) | 0 | 0 | 5,879 s | 3.0 GB |
| W4VAll: hC_all (Fin 4) | 0 | 0 | 5 s | 2.9 GB |

Axioms (from `#print axioms` in the logs): propext, Classical.choice and Quot.sound, plus native_decide aux. sorryAx appears in 0 logs.

## Occurrence glue (Opus gen_occ_kc, 7c9f4f51; copied byte-identical into lean/; cmp in/glue vs lean/ is clean)
- HWR4_xx and COccHWR4_xx: 8 modules, all exit 0, sorry 0, error 0.
- HWR4Occ (md5 199a1d64): exit 0, sorry 0, error 0, 4 s wall, built after W4VAll.
- check_literals_c (f49a5b47): 0 mismatches (4 rows).

## Verdict
**HCW13R4: 4 / 4 C on kc and cfast, and 4 / 4 have Lean hC plus occurrence glue, sorry 0, across 15 module builds, all exit 0.**

**Independence:** the C verdicts come from Studio kc and cfast, our engines. hC is the repo cReducible18 kernel via our gen_ccover3.
Only the occurrence glue is Opus-generated; I compiled it unmodified. I read no Opus engine code.
