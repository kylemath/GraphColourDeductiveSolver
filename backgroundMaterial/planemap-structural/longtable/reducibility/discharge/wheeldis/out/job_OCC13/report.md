# job OCC13: compiling Opus Team C's kc-line → occurrence Lean glue (ring-13 calibration) (Studio, 5 Nov)

**Result: everything compiles cleanly.** All of the following exit 0 with sorry 0, and `#print axioms` shows only propext,
Classical.choice, Quot.sound and native_decide auxiliaries; sorryAx appears 0 times:
- H13_00..09
- COccH13_00..09
- the gen_hd ring-13 modules HD13 / HD13V00..09 / HD13All
- **HD13Occ**

**None of the README fallbacks was needed.** In `occursCXR_of_occ` the first route of the `first` block succeeds; the linter
reports the other two as "never executed". **No file needed patching:** every compiled .lean is byte-identical to the 714ea779
copy, so patched/ is empty.

## Source and setup
- **Source:** claude/project-thread-7uelj0 at 714ea779, P_own_lp/s74_leanglue/, copied read-only into in/. README.md was read
  first.
- **No Python was run from it.** The committed .lean files did not need regenerating, so gen_occ_kc.py was not run either.
- **Build:** ~/studio_lean_builds/rsst118_fb35d2d1, the dcheck chain at fb35d2d1, with Lean v4.35.0-rc3, the mathlib oleans
  read-only, no lake and nice 15. The new modules went into occ13/.
- **COccBridge** was not yet in our build. I compiled it from a byte copy of dcheck/COccBridge.lean (md5 c6537 5f6…, identical to
  the tree's) into dc/; exit 0, 9 s.
  - Lean refuses a source outside its working root, which is why a copy was used.
- **Step 1, gen_hd:** gen_hd.py c1c30c9a, run on calib13/calib13_extra.tsv with MOD HD13 / PFX hd13 and batch 1, one entry per
  module, as the README asks.
  - c1c30c9a is the 0604923f version plus the HD0 import fix in the All module.
  - Batch 1 only changes module file names. The namespace HD13V and the theorems `HD13V.hD_i` are the ones HD13Occ uses.

## Per module (lean/status.txt)
| module | exit | sorry | wall | CPU | RSS |
|---|---|---|---|---|---|
| COccBridge (Studio build) | 0 | 0 | 9 s | – | 3.1 GB |
| HD13 (data) | 0 | 0 | 1 s | – | 0.5 GB |
| HD13V00..09, the hD_0..9 by native_decide | 0 (all) | 0 | 188–267 s each | 187–267 s | 0.52 GB |
| HD13All | 0 | 0 | 2 s | – | 1.5 GB |
| H13_00..09 | 0 (all) | 0 | 6–8 s each | 5.5–7 s | 3.2–3.3 GB |
| COccH13_00..09 | 0 (all) | 0 | 4–5 s each | about 1.1 s | 3.05 GB |
| **HD13Occ** | **0** | **0** | 4 s | 0.8 s | 3.0 GB |

**Ring-13 hD calibration:** the 10 hD take **188–267 s of CPU each, median about 235 s**. This matches HD0's ring-13 figure
(median 223 s).

## Axioms (final theorems)
- **`HD13Occ.dEntry_i`:** propext, Classical.choice, Quot.sound, HD13.hd13Confs_length._native… and HD13V.hD_i._native….
- **`HD13Occ.colorable_i`:** the same, plus DCheck.R1.check4..9._native… (DCheckOccWalk's reducer aux).
- **`H13_kk.colorable_of_occ_entry`** (in COccH13_kk): propext, Classical.choice, Quot.sound and the DCheck.R1.check* native aux.
- **Theorems present:**
  - H13_kk: colorable_of_occ_dred, colorable_of_mirror_occ_dred.
  - COccH13_kk: local_facts_of_occ, occursW_of_occ, dEntryOf, colorable_of_occ_entry, colorable_of_mirror_occ_entry,
    occursCXR_of_occ, occursCXF_of_occ, colorable_of_occ_centry, colorable_of_mirror_occ_centry.

## Elaboration failures
None in their files.

Two failures on our side, both fixed before the final run:
1. COccBridge's source had to be inside the Lean root (the copy described above).
2. The first HD13Occ attempt ran before HD13All had been built ("unknown module prefix 'HD13All'"). That was an ordering problem
   between two overlapping drive runs of mine, not their file. On the clean re-run, HD13All was built first and HD13Occ exited 0.

## nl0245_r13 (index 4, the interior vertex touching two non-adjacent ring vertices)
- **H13_04 (Occ, face-walk form):** exit 0, sorry 0, 7 s. It proves configOcc, cf_sym, cf_loop and colorable_of_occ_dred.
- **COccH13_04 (bridge + registry glue):** exit 0, sorry 0.
- **HD13V04 (hD_4):** exit 0, 238 s.
- **HD13Occ.dEntry_4 / colorable_4:** compiled.
- So the face-walk occurrence handles a vertex with two non-adjacent ring neighbours without assumptions. `ring_dinj` is
  derived, not assumed.
