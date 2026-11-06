# job HDB3: Lean hD and occurrence glue for the 4 route-F D windows (Studio, 6 Nov 00:46Z)

**Result:** all 4 windows are D on kc, dfast18 and cfast, and have Lean hD plus occurrence glue. Every module exits 0 with sorry 0;
sorryAx appears 0 times.

## Inputs
- **EXTRAFILE:** D_b3.tsv (5c284e10). gen_hd f743a82d, MOD HDB3, PFX hdb3, batch 1. module_split.tsv was pushed first at
  2011563a.
- **Glue:** 12e4d607, s76_occ502/hdb3/lean/. **All 9 files are byte-identical and match the expected md5s:**
  - HB3_00..03: be8716f2, fe8c40f2, 7e3da19b, 79f673fa
  - COccHB3_00..03: f678824e, 2f63b5d2, 694a359d, c40ae76b
  - HDB3Occ: dc832f92

## Engines (eng/; kc 07e79fae, dfast18 07cb1e0b, cfast de59e72f)
| window | ring | kc -C -s 60 -t 600 | dfast18 | cfast | classes = reached |
|---|---|---|---|---|---|
| b7_u7577575_.5.5.55 | 14 | D | D | D | 199,291 |
| b7_u7577575_.555.55 | 14 | D | D | D | 199,291 |
| b7_u7577575_.565.55 | 15 | D | D | D | 597,871 |
| b7_u7577575_.5.5755 | 15 | D | D | D | 597,871 |

## Lean (lean/status.txt; HDB3V00 built first)
| module | exit | sorry | CPU |
|---|---|---|---|
| HDB3 (data) | 0 | 0 | – |
| HDB3V00 (hD_0, ring 14) | 0 | 0 | 864 s |
| HDB3V01 (hD_1, ring 14) | 0 | 0 | 757 s |
| HDB3V02 (hD_2, ring 15) | 0 | 0 | 4,515 s |
| HDB3V03 (hD_3, ring 15) | 0 | 0 | 4,554 s |
| HDB3All (hD_all : Fin 4) | 0 | 0 | 2 s |
| HB3_00..03 | 0 | 0 | about 10 s each |
| COccHB3_00..03 | 0 | 0 | about 4 s each |
| **HDB3Occ** | **0** | **0** | 4 s |

**Axioms** (HDB3All, and HDB3Occ's 8 prints for dEntry_i / colorable_i): only propext, Classical.choice and Quot.sound, plus
native_decide auxiliaries (hD_i, hdb3Confs_length, and DCheck.R1/Meet checks for colorable_i).
