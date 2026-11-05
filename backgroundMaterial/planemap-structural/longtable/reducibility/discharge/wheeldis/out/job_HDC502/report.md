# job HDC502: Lean hD for the 380 D of Opus's 502 cover (cover_pb868, 8f57723c) (Studio, done 5 Nov 22:14Z)

**Result:** all 370 to-do D entries have Lean hD, every module exit 0 with sorry 0. `HDCV.hD_all (k : Fin 370)` exit 0, with axioms
propext, Classical.choice, Quot.sound and native_decide aux only; sorryAx appears 0 times. **Every one of the 380 D now has a
DCheck18 hD.** All 122 C map to an existing Lean hC.

## Counts
| item | count |
|---|---|
| D: Lean hD done here | **370** (HDCV00..369; MOD HDC, PFX hdc; gen_hd c1c30c9a → f743a82d, which adds maxRecDepth; Conf literals identical) |
| D: skipped, already hD in HD0 | 5: rsst008, rsst012 (HDCtrl), nl2180_r13, nl2215_r14, nl1502_r15 (HD30) |
| D: skipped, RSST with dred_cfg_i (DCheck.dReducible) | 5: rsst001, 004, 006, 024, 026. **Regenerated as DCheck18 hD in batch HDR5** (421efcdb, all exit 0) |
| D: failed / D=false | **0** |
| C: mapped to existing Lean hC | **122** (Lean531 34, CR118 87, CK108 1); 0 without Lean |
| RSST entries with only verdict-level agreesRSST | 43 of the 370. All now have real hD here (D_rsst_agree_only.txt) |

**Total CPU: 124.1 CPU-h**, counting each module once. 11 modules were rebuilt as harmless duplicates in my double-runner slip
on 5 Nov.

| ring | entries | median CPU s | max CPU s | CPU h |
|---|---|---|---|---|
| 8 | 1 | 1 | 1 | 0.0 |
| 9 | 2 | 2 | 2 | 0.0 |
| 10 | 11 | 3 | 4 | 0.0 |
| 11 | 34 | 11 | 16 | 0.1 |
| 12 | 70 | 47 | 71 | 1.0 |
| 13 | 109 | 264 | 358 | 8.0 |
| 14 | 106 | 1323 | 2098 | 39.4 |
| 15 | 37 | 7122 | 11276 | 75.6 |

## Notes
- **Order:** the driver listed the modules lexically (HDCV10, HDCV100…), not strictly by ring. This affects only the order.
- **Build:** ~/studio_lean_builds/rsst118_fb35d2d1/out_hdc502, at nice 15 with 11 in parallel and about 0.52 GB each.
- **Two build issues on the first attempt, both fixed; neither was a D failure:**
  1. The 370-entry list needed `set_option maxRecDepth 100000` (gen_hd f743a82d).
  2. A macOS case clash between output dir `hdc` and module `HDC`. The dir was renamed `old_attempt_hdc502`, not deleted.
- **Inputs for the glue:** INPUTS.md, module_split.tsv and skipped.md (97e32666).
- **Occurrence glue:** compiled clean in job OCC502. HDCOcc exit 0 at 22:18Z (out/job_OCC502/report.md).
