# PlaneEven slip

- `euler_sphere`, `edge_bound`, `exists_degree_le_five`, `triangulation_edge_count`, `neighbour_rotation` are theorems in `SimpleGraph/PlaneMap.lean`. Tetrahedron and `cycleMap` checks are in `PlaneMap/Examples.lean`.
- `face_boundary_even` and `even_add_face` compile in `PlaneMap/JordanFace.lean`. Split restriction through `even_restrict_split` compiles in frozen `JordanSplit.lean`.
- `even_boundary_grow` is public in `Jordan.lean`. `even_is_face_sum` compiles in `JordanEven.lean` (`lake build Mathlib.Combinatorics.SimpleGraph.PlaneMap.JordanEven` exit 0).
- `cycle_two_sides` holds for `cycleMap` and a tetrahedron facial triangle in `JordanSides.lean`. `cycleEdgeCoeff_is_face_sum` compiles in `JordanCycle.lean`. `no_cross_edge_sum_sides` and `walk_stays_on_sum_side` compile in `JordanTwoSides.lean`. A general cut may be several cycles, so the global reachability partition is still open.
- `FiveColor.lean` (Mathlib v4.15.0) has the degree-`≤ 4` extension and component swap. `FiveColorDeg5.lean` has the degree-5 swap under `hopposite`. No `five_color_theorem`. This is not the Four Colour Theorem.
