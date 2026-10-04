# Chord insertion: completion step 3 for same-face chords, checked in Lean

4 October 2026. Long Table, at the user's request, finishing the math team's completion loose ends while they were away. The Proof Navigator assigns statuses. The checkout is `mathlib4-planemap`, with Lean `v4.35.0-rc3`. There are three local commits there; none is pushed to the backup.

## What was pending, and what was done

**1. Math-team helper modules: verified, one step repaired, committed** (`7b02203`). The five new modules and four tests were uncommitted. A fresh source audit **failed** at `RotationBoundary`. In `faceSum_even`, `rw [hf]` could not find its pattern, because two `Fintype` instances on the edge set differed. It was repaired by replacing that rewrite with `convert hf` followed by `simp`, a four-line change to one proof step; no statement changed. The modules are:
- `FaceChord.exists_face_chord`: a face of length ≥ 4, in a spherical map with minimum positive degree 2, has two corners at distinct, nonadjacent vertices. Repeated facial vertices are allowed.
- `InsertPermutation`, `RotationInsert`, `RotationSplit` and `RotationBoundary`: successor-swap orbit algebra, face-observable transport through `split`, edge bookkeeping, and face-boundary parity.

**2. Filling preservation for chord insertion: new and proved** (`be4a0df`).
- `RotationSystem.split_fills`: if `R.Fills`, `R.faceOf a = R.faceOf b`, `a.fst ≠ b.fst` and `¬ G.Adj a.fst b.fst`, then `(split R a b _ _).Fills`.
- **The proof** is the raw-carrier port of `PlaneMap.even_boundary_split`:
  - if the coefficient on the chord is 0, restrict, take the old potential, and lift it with `splitFaceFunction`;
  - otherwise, first add the boundary of the new face containing the outgoing dart.
- **No** generated history, connectedness or face-length premise is used.
- Supporting lemmas: `split_out_ne_back_face` (the two chord darts lie on different faces) and `split_fills_of_zero`.
- `SphericalMap.exists_fills_chord` and `exists_spherical_chord`: under minimum positive degree 2, a face of length ≥ 4 admits a chord insertion that is again a `SphericalMap` on the same labels.

**3. Audit** (`f5e88a7` updates `PlaneMapFourColorAudit.md`):
- A fresh unified source rebuild passed **63/63** modules and tests, with **641** cached custom artifacts excluded.
- All 51 earlier source hashes are unchanged, and the manifest now lists 63 sources.
- There are 5 new guarded axiom reports. They contain only `propext`, `Classical.choice` and `Quot.sound`.
- There is no `sorry`, `admit`, `native_decide` or new axiom.
- Records are in `backgroundMaterial/planemap-structural/chord-insert-source-audit.json`, `chord-insert-source-audit-output.txt` and `chord-insert-source-SHA256SUMS`, with their hashes in `chord-insert-SHA256SUMS`.

## Where completion stands

| Step | Status |
|---|---|
| 1. Chord availability for a nontriangular face | Proved (`exists_face_chord`) |
| 2. New rotation and face split | Existing `split` plus `splitFaceEquiv` and `RotationInsert` |
| 3a. Filling preserved by a same-face chord | **Proved** (`split_fills`) |
| 3b. Filling preserved by a bridge between components | Open. The planned proof: the bridge coefficient is 0 by cut parity; normalise face coefficients by a constant on one component; then lift. |
| 4. Assembly: insertions until a connected triangulation, edge-count termination, and support transport | Open |

Also from the math team's note, to be carried into the final statement: the empty-carrier correction (state completion for nonempty carriers).

The warning bound for breadcrumb descent, uniform breadcrumb success, Gate D and the general Four Colour theorem are unaffected and remain open.
