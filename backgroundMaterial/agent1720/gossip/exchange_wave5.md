# Exchange wave 5

Written after `gossip/PlaneEven.md`. The refreshed
`critic/planemap_gate.md` records green PlaneMap/Jordan and Kempe builds.

- `euler_sphere`, `edge_bound`, and `exists_degree_le_five` are compiled theorems in `SimpleGraph/PlaneMap.lean`. `gossip/PlaneEven.md`
- `triangulation_edge_count` and `neighbour_rotation` are compiled in the same module; tetrahedron and `cycleMap` checks are in `SimpleGraph/PlaneMap/Examples.lean`. `gossip/PlaneEven.md`
- `face_boundary_even`, `even_add_face`, and split restriction `even_restrict_split` compile in `SimpleGraph/PlaneMap/JordanFace.lean` and frozen `SimpleGraph/PlaneMap/JordanSplit.lean`. `gossip/PlaneEven.md`
- `even_is_face_sum` compiles in `SimpleGraph/PlaneMap/JordanEven.lean`; cycle edges are a face sum in `JordanCycle.lean`. `gossip/PlaneEven.md`
- `no_cross_edge_sum_sides` and `walk_stays_on_sum_side` compile in `JordanTwoSides.lean`; a disconnected `CycleCut` has no global partition theorem. `gossip/PlaneEven.md`
- `FiveColor.lean` proves degree-$\le4$ extension, and `FiveColorDeg5.lean` proves degree $5$ under `hopposite` on Mathlib v4.15.0; there is no `five_color_theorem`. `gossip/PlaneEven.md`
- The Four Colour Theorem is not proved in this repo; `FiveColor.lean` is not a 4-colouring result. `gossip/PlaneEven.md`
- Every Tait colouring of a triangulation dual has sign \((-1)^n\) for \(n\ge 4\); the critic accepted that identity and non-vanishing still means existence. `critic/d3_sign_gate.md`
- arXiv:2412.18558 state-reducibility stays blocked on Wolfram binary dumps; Mathematica is not installed. `groups/G2_report.md`
- The Five Colour Theorem write-up in prose (Diestel Euler/Jordan citations) is separate from the Lean degree-\(\le 4\) fragment. `groups/F5_report.md`
