# Triangulation completion, checked in Lean

4 October 2026. Long Table, at the user's request, while the math team was away. This supersedes `ChordInsertionReport.md` for status; that file remains the record of the first two commits. The Proof Navigator assigns ledger statuses. The work is in the `mathlib4-planemap` checkout (Lean `v4.35.0-rc3`): five local commits, none pushed to the backup.

## Result

> **`SphericalMap.exists_triangulated_completion`.** On a nonempty carrier, a spherical map whose vertices all have degree at least two embeds, on the same labels, in a **connected** spherical map whose faces are all **triangles**.
>
> **`exists_triangulated_completion_min_five`.** Under minimum degree five the completion also has minimum degree five. That is the Gate-D triangulation class.

This closes the triangulation-completion obligation of `TriangulationCompletionObligation.md` at the level of existence. The nonempty-carrier correction requested by the math team is built into the statement.

## How it is built (each piece compiled, with guarded axiom reports)

| Step | Declaration | Module | Commit |
|---|---|---|---|
| 1. Chord availability | `exists_face_chord` (math team) | `FaceChord` | `7b02203` |
| 2. Raw insertion helpers | successor-swap algebra, face-value transport, edge bookkeeping, face-boundary parity (math team) | `InsertPermutation`, `RotationInsert`, `RotationSplit`, `RotationBoundary` | `7b02203`, including the one-step `RotationBoundary` repair |
| 3a. A chord preserves filling | `split_fills`, `split_out_ne_back_face` | `RotationSplitFills` | `be4a0df` |
| 3a′. A spherical chord insertion exists | `exists_fills_chord`, `exists_spherical_chord` | `SphericalChordInsert` | `be4a0df` |
| 3b. A bridge preserves filling | `split_fills_bridge`, `bridge_coeff_zero`, `reachable_iff_of_faceRelation`, `exists_spherical_bridge` | `RotationBridgeFills` | `5f54113` |
| 4. Assembly | `exists_triangulated_completion`, `..._min_five` | `SphericalCompletion` | `5f54113` |

**Proof ideas:**
- **Chord:** if the coefficient on the chord is 0, restrict and lift the old potential with `splitFaceFunction`. Otherwise first add the boundary of the new outgoing face.
- **Bridge:**
  - the bridge coefficient is 0, since summing the even condition over one component counts old edges twice and the bridge once;
  - face orbits stay in one component, so shifting the old potential by a constant on one component changes no edge sum and makes the two corner faces agree;
  - then lift.
- **Assembly:** strong induction on missing vertex pairs, the gap between n(n−1)/2 and the edge count, measured with `Nat.card` to avoid instance mismatches.
  - If the map is disconnected, bridge two components. Every vertex has a dart because its degree is at least 2.
  - If it is connected with some face of length ≠ 3, `FaceCorner` gives length ≥ 4, so insert a chord.
  - Otherwise it is done.

## Validation

- A fresh unified source rebuild passed **67/67** modules and tests, with **667** cached custom artifacts excluded.
- All earlier source hashes are unchanged; `PlaneMapFourColorAudit.sha256` lists 67 sources.
- Every new guarded axiom report is within `propext`, `Classical.choice` and `Quot.sound`. There is no `sorry`, `admit` tactic, `native_decide` or new axiom.
- Records are in `backgroundMaterial/planemap-structural/completion-source-audit.json`, `completion-source-audit-output.txt` and `completion-source-SHA256SUMS`, with hashes in `completion-SHA256SUMS`.

## Scope and what remains open

- **This is existence, not an executable relabeller or algorithm.** It is classical, like `SupportTransport`.
- **Still open:** composing completion with support transport, deletion and colour restriction into the general argument; Gate D (the degree-five reduction); breadcrumb descent's warning bound; and the general Four Colour Theorem.
- **Completion does not preserve Kempe components.** Colourings transport by restriction along `M.graph ≤ T.graph`.
- **The math team should review all Long Table changes on their return,** especially the `RotationBoundary` repair.
