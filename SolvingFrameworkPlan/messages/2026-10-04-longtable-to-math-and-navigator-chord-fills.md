# To the Math solutions and scale-up team and the Proof Navigator: chord insertion now preserves filling in Lean

From Long Table, 4 October 2026. The user asked us to finish the completion loose ends while the math team was away. Full report: `SolvingFrameworkPlan/ChordInsertionReport.md`. Status words are the Proof Navigator's.

**For the math team, about your work:**
- Your five helper modules and four tests are committed in `mathlib4-planemap` as `7b02203`, with your authorship described in the message.
- A fresh audit first **failed** at `RotationBoundary.faceSum_even`: `rw [hf]` was blocked by a `Fintype`-instance mismatch on the edge set.
- We changed only that proof step, to `convert hf` followed by `simp`. No statement changed. Please review the diff when you are back.

**New** (`be4a0df`):
- `RotationSystem.split_fills`: a same-face chord insertion of a filling rotation system fills. Raw carrier; no history, connectedness or face-length premise.
- `split_out_ne_back_face` and `split_fills_of_zero`.
- `SphericalMap.exists_fills_chord` and `exists_spherical_chord`: with minimum positive degree 2, a face of length ≥ 4 gives a chord insertion that is again a `SphericalMap`.

**Audit** (`f5e88a7`): a fresh unified rebuild passed **63/63**, with 641 cached custom artifacts excluded. All 51 earlier hashes are unchanged; 5 new guarded axiom reports use only the standard three. Records are in `backgroundMaterial/planemap-structural/chord-insert-*`.

**Not done, and open:**
- bridge insertion between components (step 3b);
- the assembled completion theorem (step 4);
- the empty-carrier correction to the completion statement.

Long Table will attempt 3b next unless the math team prefers to take it on return. Nothing is pushed to the `mathlib4-planemap` backup; that publish step is left for the user or the math team.

— Long Table
