# PlaneMap-to-Five-Colour Lean completion plan

**Date:** 3 October 2026  
**Scope:** finish the deductive Five Colour Theorem over the combinatorial
PlaneMap library. Preserve the Mathlib v4.15.0 Kempe package and test PlaneMap
against the current Mathlib checkout. This plan does not claim the Four Colour
Theorem.

## Completion gate

The general theorem now compiles in the authoritative checkout:

```lean
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem

example {n : ℕ} (M : SimpleGraph.PlaneMap n) : M.graph.Colorable 5 :=
  M.five_color_theorem
```

There are no additional face-length, triangulation, separation, or
connected-deletion premises. The guarded axiom audit reports only `propext`,
`Classical.choice`, and `Quot.sound`. This proves the theorem for generated
combinatorial PlaneMaps; arbitrary geometric planar-graph representation and
Mathlib contribution cleanup remain separate tasks.

## 1. Baseline and theorem boundary

The following targets compile in the authoritative checkout
`/Users/fulkanjou/mathlib4-planemap` without `sorry`, `admit`, axiom
declarations, or `native_decide`:

- `PlaneMap.lean`: Euler, edge bound, degree at most five, triangulation
  count, and neighbour rotation.
- `JordanEven.lean`: every even edge combination is a sum of face boundaries.
- `JordanCycle.lean`: cycle edges form such a face sum and the degree-five
  neighbours occupy opposite rotation sectors.
- `JordanTwoSides.lean`: face-sum sides are disjoint, have no cross edge, and
  are preserved by walks avoiding the cut.
- `JordanWalkParity.lean`: every closed walk's mod-two edge multiplicity is a
  face-boundary sum.
- `FiveColorSeparation.lean`: alternating avoiding walks intersect,
  `degree_five_neighbour_rotation`, and `heawood_hopposite`.
- `Coloring/Kempe.lean` and `Coloring/FiveColorExtension.lean`: the required
  graph-theoretic swaps and degree-five extension on current Mathlib.
- `PlaneMap/FiveColor.lean`: `five_color_extension`, with no separation,
  triangulation, or face-length premise.
- `DeleteVertex.lean`: deleted components are strictly smaller, their
  colourings assemble, and they imply a colouring of the original map.
- `FiveColorExamples.lean`: every `PlaneMap 6` is five-colourable.

The Heawood bridge and both induction interfaces are closed. The selected
carrier is `SphericalMap`: a finite rotation system with a mod-two filling
property, proved for every generated PlaneMap by `ofPlaneMap`. Edge deletion
preserves filling. Vertex deletion retains the deleted label as an isolated
vertex, so edge-count induction handles disconnected graphs directly without
reconstructing generated components or relabelling them. An unconditional
positive low-degree theorem follows from rank-nullity and face counting.

The current `CycleCut` may encode several disjoint cycles. Therefore a theorem
claiming `cycle_two_sides C` for every `CycleCut C` is rejected.

## 2. Design constraints

1. No change to the Kempe package's Lean/Mathlib v4.15.0 pin.
2. No copied Mathlib source inside the Kempe package.
3. No `sorry`, `admit`, `axiom`, or theorem represented only by a computation.
4. Every phase has its own `lake build` acceptance gate.
5. Keep graph-theoretic colouring lemmas independent of PlaneMap.
6. Do not call a universal five-to-four Kempe reduction a consequence of this
   work. Given Meyniel's theorem, that is a reformulation of 4CT.

## 3. Phase A — freeze and clean the green foundation

**Feasibility:** High.

### Work

- Keep `JordanSplit.lean` limited to the 390-line restriction API;
  `even_boundary_split` remains in `JordanEven.lean`.
- Put module docstrings immediately after imports.
- Replace deprecated `if_pos`/`if_neg` in touched files.
- Narrow `open Classical` where practical and remove unused arguments only
  when this does not destabilize downstream theorem signatures.
- Add an umbrella module importing the complete PlaneMap stack only after all
  downstream modules compile.

### Gate

```text
lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanTwoSides
```

Exit $0$, no forbidden placeholders, GraphColour and typecheck copies
byte-identical.

## 4. Phase B — closed-walk parity route

**Status:** Complete. **Feasibility:** High.

The earlier proposal to construct a `ConnectedCycleCut` is not needed for the
Five Colour application. `JordanWalkParity.lean` proves
`walkEdgeCoeff_is_face_sum` for an arbitrary closed walk. The closed walk

$$x,v_0 \;+\; P \;+\; v_2,x$$

already has the parity information needed at the middle boundary edge.

### Gate result

`JordanWalkParity.lean` compiles. The general `cycle_two_sides` theorem for a
possibly disconnected `CycleCut` remains outside this plan and is not claimed.

## 5. Phase C — alternating-walk separation

**Status:** Complete. **Feasibility:** High.

`FiveColorSeparation.lean` proves that face coefficients are constant along a
walk disjoint from the closed walk and change across the required odd edge.
Consequently `alternating_walks_intersect` rules out two disjoint alternating
connections. This directly supplies the Heawood contradiction without a
global cycle-side partition.

### Gate result

`closed_walk_separates`, `alternating_walks_intersect`, and
`degree_five_neighbour_rotation` compile.

## 6. Phase D — local five-colour extension

**Status:** Complete. **Feasibility:** High.

`FiveColorSeparation.heawood_hopposite` handles actual bichromatic induced
reachability after deleting the centre. Current-Mathlib ports in
`Coloring/Kempe.lean` and `Coloring/FiveColorExtension.lean` consume this
separation theorem. `PlaneMap/FiveColor.lean` then proves:

```lean
theorem five_color_extension (x : Fin n) (hdeg : M.graph.degree x ≤ 5)
    (hcolour : (M.graph.induce {z | z ≠ x}).Colorable 5) :
    M.graph.Colorable 5
```

The extension may recolour a Kempe component of the deleted graph.
The original Lean 4.15 package remains unchanged.

## 7. Phase E — deletion and the induction carrier

**Status:** Complete.

The graph-level `DeleteVertex` API remains available. The final induction uses
an alternative carrier with a proved connection to PlaneMap:

- `SphericalMap.ofPlaneMap` derives filling from `JordanEven`.
- `ErasePermutation` bypasses removed points in cyclic permutations.
- `RotationDelete.eraseRotation` restricts rotations after deleting both darts
  of an edge and proves vertex cyclicity.
- `SphericalDelete.fills_eraseRotation` proves preservation of filling, including
  bridge deletion.
- `SphericalMap.subgraph_closed` supplies any spanning subgraph.
- `SphericalMap.isolate_closed` removes all edges at a nonisolated vertex and
  proves strict edge-count decrease, retaining the vertex label.
- `SphericalDegree.exists_pos_degree_le_five` supplies a positive low-degree
  vertex whenever a dart exists, without a face-length premise.

Deletion may disconnect the graph. The carrier and proof allow this. No
`delete_component_has_plane_map` theorem or new generatedness axiom is used.
The low-degree proof restricts incidence to nonisolated vertices, uses the
filling property for a rank-nullity inequality, and derives the required
face-length bound only inside the contradiction where all degrees are at
least six.

### Gate result

The deletion, degree, and final theorem modules build. Guarded axiom audits
cover spanning-subgraph closure, vertex isolation, and the low-degree theorem.
Applications cover paths, cycles, the tetrahedron, and deletion disconnecting
a three-vertex path. A negative sanity check excludes the complete six-vertex
graph from this carrier.

## 8. Phase F — assemble the Five Colour Theorem

**Status:** Complete.

`SphericalFiveColor` extends the proved closed-walk/Kempe argument to the
spherical carrier. `FiveColorTheorem` uses strong induction on edge count:

1. Colour an edgeless graph constantly.
2. Select a positive-degree vertex of degree at most five.
3. Isolate it using the proved deletion closure, strictly decreasing edges.
4. Colour that spherical map by induction and restrict away from the vertex.
5. Apply the local Kempe extension to colour the original graph.
6. Transfer the result through `SphericalMap.ofPlaneMap`.

```lean
theorem five_color_theorem (M : PlaneMap n) : M.graph.Colorable 5
```

`exists_five_colouring` provides the corresponding function-valued statement.

### Gate result

```text
lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem MathlibTest.PlaneMapFiveColor
```

Exit 0. Final theorem and closure/degree audits depend only on the standard
three axioms. No `hopposite`, `IsPlanar`, `Triangulation`, `cycle_two_sides`,
or face-length assumption remains. The original v4.15 Kempe package is
unchanged. This is the Five Colour Theorem, with no four-colour claim.

## 9. Phase G — Mathlib contribution cleanup

**Feasibility:** Medium.

After the theorem stack is stable:

- separate public APIs from proof-internal transport lemmas;
- resolve style warnings;
- add module documentation and examples;
- decide whether Jordan/FiveColor belongs in the first contribution or a
  follow-up;
- run `lake exe mk_all` only in a proper Mathlib contribution workflow.

Do not open a pull request from the present repository.

## 10. Five colours to four

**Feasibility:** Low with the current mathematical input.

Completing Phase F validates the plane-map and Kempe infrastructure. It does
not make four colours a routine final phase. The following existing targets
must remain labelled as reformulations or stronger statements:

- every planar five-colouring Kempe-reduces to a four-colouring;
- universal KC5 at every degree-five vertex;
- non-strict monotone elimination of colour five;
- non-vanishing of the Tait/Penrose count.

A four-colour phase starts only after a new structural lemma has a precise
statement, a kill criterion, and evidence beyond the finite census.

## 11. Follow-up tasks

The requested mathematical theorem is complete. Preserve the compiled proof
and axiom regression tests. Phase G remains the contribution-preparation
workstream; no pull request is requested or opened here. Any four-colour work
requires the new mathematical input described above.
