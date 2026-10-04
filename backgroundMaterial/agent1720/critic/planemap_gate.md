# PlaneMap verification gate

Date: 2026-10-03

## Build evidence

The authoritative checkout is `/Users/fulkanjou/mathlib4-planemap` on
Lean 4.35.0-rc3. The application and axiom-audit targets compile:

```text
cd /Users/fulkanjou/mathlib4-planemap
lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem \
  MathlibTest.PlaneMapFiveColor
exit 0

lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanTwoSides
exit 0
```

The pinned colouring package also builds:

```text
cd /Users/fulkanjou/GraphColour/lean4/KempeReconfiguration
lake build
exit 0, real 0.53 s
```

## Module verdicts

- `PlaneMap`, `RotationSystem`, `Construction`, `Examples`: **PASS**.
- `Jordan`, `JordanFace`, frozen `JordanSplit`: **PASS**.
- `JordanEven`, including `even_is_face_sum`: **PASS**.
- `JordanSides`, including the cycle-map and tetrahedron checks: **PASS**.
- `JordanCycle`, including `cycleEdgeCoeff_is_face_sum`: **PASS**.
- `JordanTwoSides`, including no-cross-edge and walk preservation: **PASS**.
- `JordanWalkParity`, including every closed walk as a face sum: **PASS**.
- `FiveColorSeparation`, including `degree_five_neighbour_rotation` and
  `heawood_hopposite`: **PASS**.
- Current-Mathlib `Coloring/Kempe` and `Coloring/FiveColorExtension`: **PASS**.
- PlaneMap `FiveColor`, including `five_color_extension`: **PASS**.
- `DeleteVertex`, including strict component size and colouring assembly:
  **PASS**.
- `FiveColorExamples`, including `five_colorable_six_vertices`: **PASS**.
- `ErasePermutation`, `RotationDelete`, and `SphericalMap`: **PASS**.
- `SphericalDelete`, including edge-deletion filling preservation,
  spanning-subgraph closure, and vertex isolation: **PASS**.
- `SphericalDegree`, including the unconditional positive low-degree theorem:
  **PASS**.
- `SphericalFiveColor` and `FiveColorTheorem`: **PASS**.
- Symbolic paths/cycles, tetrahedron, disconnected deletion, and six-clique
  exclusion regressions: **PASS**.

No new proof source uses `sorry`, `admit`, an axiom declaration, or
`native_decide`. The audit regression reports only `propext`,
`Classical.choice`, and `Quot.sound`.
The builds emit style warnings, chiefly broad `open Classical`, unused
arguments, and older deprecated `if_pos`/`if_neg` uses. They are not proof
failures, but they must be cleaned before an upstream Mathlib submission.

## Mathematical gate

**PASS:** the complete Lean Five Colour Theorem for every generated
combinatorial PlaneMap, with no additional face-length, triangulation,
separation, or connected-deletion premise. The proved spherical carrier
replaces generated-component reconstruction for induction. Vertex isolation
strictly decreases edges and permits disconnected graphs. Rank-nullity and
face counting supply the unconditional positive low-degree interface.

The final theorem, closure, and degree results pass guarded axiom audits
using only the standard three axioms. This is not a representation theorem
for every geometrically planar graph.

The connected-cycle API and a global `cycle_two_sides` theorem are unnecessary
for this application and remain unclaimed.

## Four-colour boundary

The Four Colour Theorem is not proved. A universal theorem reducing arbitrary
planar five-colourings to four by Kempe swaps is a reformulation of 4CT given
Meyniel's theorem; finite computations do not discharge it.

## Gate result

The requested mathematical completion gate is passed by compilation and
axiom regression. Preserve the checked proof stack. Mathlib contribution
cleanup remains separate; no PR was opened. No generated-component closure
or four-colour theorem is claimed.
