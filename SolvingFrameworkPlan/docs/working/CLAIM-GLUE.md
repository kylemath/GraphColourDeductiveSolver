# Claim glue: reducibility + unavoidability ⇒ 4-colourable (Long Table, 19 Oct 2026)

The 24 Oct gate text says the Lean step from the reducibility results to a colourability theorem
had not been written. It is written now:
`backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/ClaimGlue.lean`, namespace
`SimpleGraph.SphericalMap.ClaimGlue`. It is a plain dcheck file, like `SepAll.lean`. It imports
`MinimalFrame` (StudioMathLean), `SepAll` and `DCheckOccWalk`. It does not go in `lean4/FourColor`:
that package pins Mathlib v4.15 and has no PlaneMap library, so none of the results below can be
imported there.

## Statement

```lean
theorem four_color_of_unavoidable (R : Registry) (hU : Unavoidable R) (hC : CGlue R.C)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4
theorem four_color_of_unavoidable_D (Ds : List DEntry) (hU : Unavoidable ⟨Ds, []⟩)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4          -- no C-glue needed
theorem four_color_of_unavoidable_planeMap ... (M : PlaneMap n) : M.graph.Colorable 4
theorem MinimalCounterexample.avoids (R : Registry) (hC : CGlue R.C)
    (hT : MinimalCounterexample T) (htri : T.Triangulated) : ¬ R.Contains T
```

The module also defines or proves the following:

- **Definitions.**
  - `MinimalCounterexample T`: `T` is not 4-colourable, and every map of smaller support is.
  - `Internally6 T`: `T` is connected and triangulated, with minimum degree 5 and `NoSep`. It
    also satisfies `NoShortSepCycle`: no separating 3- or 4-cycle, and no separating 5-cycle
    except one around a single vertex.
- **Properties of a minimal counterexample, from existing results.**
  - `noSep` follows from F1, `colorable_of_separating_triangle`.
  - `noShortSep` follows from B2, `colorable_of_short_separating_cycle` (Job 25).
  - `internally6` combines the two.
- **Registry entries.**
  - `DEntry` holds a `DCheck18.Conf`, its verdict `hD : dReducible cf = true`, the bound
    `2 ≤ r ≤ 19`, and `hsym`/`hloop`.
  - `DEntry.colorable` is D-soundness through `ConfigOccW.colorable_of_dReducible18`. That
    theorem combines the checker soundness of Jobs 19 and 23 with the face-walk ring of Job 26,
    so folded and pinched rings are covered.
- **Occurrence.** `OccursW`/`OccursC` is the reduction-ready occurrence: a deleted map of
  strictly smaller support whose face walk is the ring.
  - Orientation needs no separate case: `T.mirror` has the same graph, and the orientation is
    carried by the deleted map's rotation.
  - `occursW_of_configOcc` connects the per-key `K<ii>.configOcc` (occ24) to `OccursW`.
- **Proof.** `four_color_of_smaller_gate` reduces to a connected min-degree-5 triangulation
  whose smaller maps are all colourable. If that triangulation is not colourable, it is a
  minimal counterexample, so it is `Internally6`. `Unavoidable` then gives an occurrence, and
  `avoids` rules the occurrence out.
- **Axiom footprint.** The module adds no `sorry` and no `axiom`. It inherits the
  `native_decide` auxiliary axioms of the checker-soundness chain (`DCheckR1` `check4..8`,
  `DCheckRingMeet`), each per-key `hD`, and Lean's standard axioms.

## Open hypotheses (exactly two, both explicit)

1. **`Unavoidable R`**: every `Internally6` triangulation contains an `OccursW`/`OccursC` of some
   entry of R. This is what the discharging LP supplies at t\* ≤ 0. It includes the
   appearance → occurrence bridge (Job 26 step (iii): extract the face walk of an appearing
   2-ball). `unavoidable_of_appears` records that split as `hLP` (the census) plus `hBridge`. With
   K = 2 at t\* = 2/13 [E2], this hypothesis is not available yet.
2. **`CGlue R.C`**: C-reducibility soundness for the C entries. The C computations are in Lean
   (`C66666.lean`, `CWheels.lean`, native_decide), but the reduction glue is not. That glue has
   to build the contracted map, show it is smaller, pull its colouring back to a ring colouring
   that satisfies the reducer constraint (`extX`), and connect `runGood`'s good bits to `Good`.
   - For a D-only registry, `four_color_of_unavoidable_D` needs no `CGlue`.
   - The current K = 2 registries are about 45% C (for example 869 D / 658 C on 5fa0adb0).

The per-key verdicts `hD` are fields of `DEntry`, not hypotheses. Building the concrete
registry `R` from the 2,855 + 49 key modules is bookkeeping that remains: one `DEntry` per key,
with `hD` from Job 24b or studio14c.

## Build status

This container has no elan, lake or lean, and the Mathlib olean cache (`cache.mathlib.org`) is
blocked by the egress policy. Lean v4.35.0-rc3, Mathlib 300d0e5 and the PlaneMap overlay 8299419
were fetched, and the Mathlib closure was built from source on 4 cores, with a 40 min cap.

**Result: not compiled here.** The cap was reached with 2,371 of at least 2,415 Lake jobs built and
0 errors. The PlaneMap, StudioMathLean and dcheck modules (33 files, from `DCheck` to `ClaimGlue`)
were not reached, so `ClaimGlue.lean` has not been type-checked. **Studio should compile it.** Use
`build_r2.sh`'s recipe, then add `DCheckPinch DCheckPinchGeom DCheckOccWalk ClaimGlue` after
`SepAll`, and check the `#print axioms` lines at the end of the file. The proofs are short and copy
the patterns of `FrameF3.lean` and `occ24/K09.lean`. The likeliest trouble spots are
elaboration details, such as the `ProperOff` binder in `DEntry.colorable` and the `simp only
[NoSep, not_forall]` destructuring copied from FrameF3. A wrong statement is less likely.

## What remains

- Prove `Unavoidable R` for the final registry: the LP at t\* ≤ 0 for K = 2, and the Job 26 (iii)
  bridge.
- Prove `CGlue` (C-glue), or drop the C entries the LP needs.
- Instantiate `R` with the Lean-checked keys.
