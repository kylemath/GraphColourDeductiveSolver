# Lean claim-glue build (Long Table 19 Oct 19:00Z), Mac Studio

Source: `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/ClaimGlue.lean` at 93797745, built in a
separate detached worktree (scratchpad), never in k19's checkout or its `.lake`. No lake, no download, no install.
Toolchain elan `leanprover/lean4:v4.35.0-rc3`; Mathlib `~/mathlib4-planemap-build` at
300d0e535721bc098547106fc297d8ba2a63f6bb, oleans reused read-only (copy-on-write clone, as build_r2.sh does). nice 19.
Driver: `glue.sh` (build_r2.sh, then DCheckPinch, DCheckPinchGeom, DCheckOccWalk, ClaimGlue, each `lean -o` from dcheck/).

## Result on the file as committed (93797745): FAILS (kill line met)
- build_r2.sh: exit 0 (`build_r2.log`). DCheckPinch, DCheckPinchGeom, DCheckOccWalk: exit 0, warnings only.
- ClaimGlue: exit 1 (`ClaimGlue.log`), verbatim:
  `ClaimGlue.lean:1:0: error: import DCheckPinchGeom failed, environment already contains 'SimpleGraph.SphericalMap.Cyc.rec' from SepAll`
  Cause: `structure SimpleGraph.SphericalMap.Cyc` is declared twice, identically (fields three/per/adj/inj), at
  `DCheckPinchGeom.lean:24` and `SepAll.lean:15`; ClaimGlue imports both (`SepAll`, and `DCheckOccWalk` -> `DCheckPinchGeom`).
- (`glue_driver_try1.log`: first launch, every lean call refused "input file must be contained in root directory",
  because the driver did not cd into dcheck/; fixed in glue.sh, not a source problem.)

## Diagnostic only (scratch copy, not a verdict on the committed file)
1. `diag_SepAll.patch`: rename SepAll's `Cyc` to `SepCyc` (21 lines). SepAll then builds; ClaimGlue gets one error
   (`diag_ClaimGlue.log`): line 91:62, `C : T.Cyc r ρ` expected `T.SepCyc ?m ?m` in `colorable_of_short_separating_cycle C`.
2. `diag2_ClaimGlue.patch`: pass `⟨C.three, C.per, C.adj, C.inj⟩` there. ClaimGlue then builds: exit 0, 0 errors, no
   `sorry`; `#print axioms four_color_of_unavoidable` (`diag2_ClaimGlue.log`): propext, Classical.choice, Quot.sound and
   the native_decide auxiliary axioms DCheck.Meet.{check4_true,check5_true,size4,size5} and DCheck.R1.check{4..9}
   (`._native.native_decide.ax_1_1`: v4.35's form of the checker's native_decide trust, in place of Lean.ofReduceBool).
   No sorryAx, no other axiom. The proper fix is one shared `Cyc` (e.g. SepAll importing it), for the owner of the files.
