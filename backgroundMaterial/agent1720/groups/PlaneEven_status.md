# PlaneMap and Five Colour Lean status

**Group:** PlaneEven / PlaneSides / FiveColor, manager M-Foundation  
**Date:** 3 October 2026  
**Status:** the general Five Colour Theorem, deletion closure through a
proved spherical carrier, and unconditional recursive low-degree interface
compile in the authoritative current-Mathlib checkout. Guarded axiom audits
report only the standard three axioms.

## 1. Definitions

- `PlaneMap`, `Generated`: `SimpleGraph/PlaneMap.lean`.
- `boundary`, `faceSum`, `IsEven`: `SimpleGraph/PlaneMap/Jordan.lean`.
- Split transport: `JordanSplit.lean`; constructor induction: `JordanEven.lean`.
- `CycleCut` and sector reachability: `JordanSides.lean`.
- Cycle-edge face sums: `JordanCycle.lean`.
- Face-sum separation: `JordanTwoSides.lean`.
- Closed-walk parity: `JordanWalkParity.lean`.
- Alternating-walk separation: `FiveColorSeparation.lean`.
- Current-Mathlib colouring: `Coloring/Kempe.lean`,
  `Coloring/FiveColorExtension.lean`, and `PlaneMap/FiveColor.lean`.
- Deletion assembly and example: `DeleteVertex.lean` and
  `FiveColorExamples.lean`.

## 2. Statements

For every generated plane map:

1. Euler's formula and neighbour rotation are proved. The original edge and
   degree bounds have their stated face-length hypotheses; the new spherical
   positive low-degree theorem has no such premise.
2. Every even $\mathbb Z/2\mathbb Z$ edge combination is a sum of face
   boundaries (`even_is_face_sum`).
3. The edge set of a `CycleCut` is such a face sum
   (`cycleEdgeCoeff_is_face_sum`).
4. The resulting face-sum sides are disjoint, have no cross edge, and are
   preserved by walks avoiding the cut.
5. `heawood_hopposite` is proved for actual bichromatic reachability after
   deleting the centre.
6. `five_color_extension` extends any five-colouring across a deleted vertex
   of degree at most five, with no triangulation or face-length premise.
7. Deleted components are strictly smaller and their colourings assemble.
8. Every `PlaneMap 6` is five-colourable deductively.
9. Every generated `PlaneMap n` is five-colourable by the general theorem,
   with no extra face-length, separation, or triangulation assumption.
10. Spanning-subgraph closure and vertex isolation preserve the spherical
    carrier; positive-degree isolation strictly decreases edges.

## 3. Evidence

Authoritative Mathlib checkout, Lean 4.35.0-rc3:

```text
lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem \
  MathlibTest.PlaneMapFiveColor
exit 0

lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanTwoSides
exit 0
```

Kempe package, Lean and Mathlib v4.15.0:

```text
lake build
exit 0, real 0.53 s
```

The final target checks the parity, separation, Kempe, deletion, degree,
and edge-count induction stack. The audit target checks the final and critical
closure/degree results and applications to paths, cycles, the tetrahedron,
disconnected deletion, and exclusion of the six-clique. All guarded audits
report only `propext`, `Classical.choice`, and `Quot.sound`.

## 4. Result

**Proved in Lean:** the general Five Colour Theorem for every generated
combinatorial PlaneMap. The final proof passes to `SphericalMap` via the
proved filling theorem, uses spanning-subgraph closure and vertex isolation,
and inducts on edge count with an unconditional positive low-degree bound.
It supports disconnected graphs and short faces without extra premises.
Generated-component reconstruction and finite relabelling are superseded
for this application; they are not silently assumed.

## 5. Kill criteria

- A generated plane map with an even edge combination that is not a face sum:
  **not met**.
- A counterexample to the conditional degree-five Kempe theorem: **not met**.
- A proof that these results force four colours: **not supplied**; that would
  be new Four Colour mathematics.

## 6. Not proved

- A global `cycle_two_sides` theorem for the current `CycleCut`; the structure
  may encode several disjoint cycles.
- A generated PlaneMap and finite relabeling for each deleted component;
  the final proof does not require this interface.
- A representation theorem for arbitrary geometrically planar graphs.
- The Four Colour Theorem.

## 7. Completion and follow-up

Closed-walk parity, Heawood separation, local extension, deletion closure,
the recursive degree bound, and the general Five Colour theorem are complete.
See `SolvingFrameworkPlan/PlaneMapFiveColorLeanPlan.md` and
`backgroundMaterial/agent1720/critic/planemap_gate.md`. Mathlib contribution
cleanup remains separate.
No PR was opened. Five-to-four Kempe reduction still needs new mathematics.
