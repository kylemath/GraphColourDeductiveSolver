# Local follow-up — Five Colour Theorem, after the Mathlib pull request

This file stays in the GraphColour repository. Do not send it to the agent who writes the Mathlib contribution.

Start only when the draft pull request from `lean_plane_euler_prompt.md` exists. The input is that pull request URL.

Work in `lean4/KempeReconfiguration`, pinned to Mathlib v4.15.0. Do not upgrade the pin. Do not copy Mathlib sources in by hand. Do not edit the upstream branch. Do not re-prove Euler’s formula.

If this pin does not contain `PlaneMap`, add `KempeReconfiguration/FiveColor.lean` against a local shim that contains only the statements from the pull request, marked `/- upstream: <PR url> -/`.

The colouring argument is `backgroundMaterial/agent1720/groups/F5_report.md` §3.4 and §3.5. Degree at most 4 extends by a missing colour. Degree 5 is one Kempe swap, using `neighbour_rotation` for the order, `cycle_two_sides` for the opposite pair, and `kempeSwap_preserves_proper`.

Prove, with no `sorry`:

1. `five_color_degree_at_most_four`
2. `five_color_theorem`: a finite simple graph with a `PlaneMap` and face lengths at least 3 has a proper `Fin 5` colouring.

Write `backgroundMaterial/agent1720/groups/FiveColor_report.md` with the theorem names, the build time, the upstream pull request URL, and one sentence that this is not the Four Colour Theorem.
