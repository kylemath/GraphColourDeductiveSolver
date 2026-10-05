# L3 compiled: the obstruction beyond short fills

Math, 5 October 2026. Review of Long Table's counterexample-analysis message and its general Lemma L3.

**[compiled] L3(a).** On any simple graph and arbitrary colour type with decidable equality, if a proper deletion start has no pure fill within three swaps, a target-reaching mixed path of length three must start with a legal singleton slide. Any Kempe-first path has a pure replacement of length at most three, by M3 on its final two moves.

**[compiled] L3(b).** After such a slide h→u carrying colour σ, any two-swap fill at u must first use a pair containing σ. If the pair avoids σ, its whole component agrees before and after the slide, the swap commutes before the slide and preserves its uniqueness, and M3 converts the remaining slide/swap into at most two original-hole swaps. This would give three swaps in total, contrary to the premise.

These two theorems imply the submitted formulation ℓ=3<κ. The Lean statements use the stronger direct premise `¬PureFill G h c 3`; they do not assume an oracle for distances, planarity, fan admissibility, degree-five or four colours. `first_is_slide` and `first_pair_contains_slide_colour` are in `SimpleGraph.VacancyThreeMoveObstruction`.

The printed statements are preserved in `three-move-lean/printed-statements.txt`. Whole components and slide semantics are exactly those of the accepted M3 module. Team B independently reviewed the actual source and found no semantic gap.

**Audit.** All 85 source/test modules rebuilt in a fresh overlay excluding cached custom artifacts, with the previous 83 hashes unchanged and all source hashes stable through the run. Four exact axiom guards passed and allow only propext, Classical.choice and Quot.sound. No placeholders or new axioms. The first audit attempt caught a test-output formatting mismatch and an unsupported pretty-printing option; these were corrected, the exact guards passed, and the whole fresh 85-module audit was rerun successfully. Neither error affected the theorem proofs.

Source snapshots, full audit metadata/hashes and output are under `backgroundMaterial/planemap-structural/three-move-lean/`; `longtable/audit/three_move_source_audit.py` reproduces the source build. The separate counterexample-analysis script also reproduced Long Table's saved output byte for byte. That reproduction corroborates its saved-graph descriptions, not a new general theorem.

L3 gives necessary conditions for a strict three-move advantage. It proves no bridge-face necessity and no bound beyond short fills. The belt walk remains separately in progress.
