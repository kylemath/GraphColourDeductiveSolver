# FiveColor degree-5 report

Implemented in `lean4/KempeReconfiguration/KempeReconfiguration/FiveColorDeg5.lean`:

- `five_color_degree_five_swap`
- `five_color_degree_five_separated`
- `five_color_degree_five`

The first two theorems expose the proper Kempe-swapped colouring of $G-x$, the
freed neighbour colour, and the resulting proper `Fin 5` colouring of $G$.
The final theorem uses the stated `hopposite` hypothesis; the upstream
`PlaneMap.cycle_two_sides` result is intended to supply that implication.

`lake build` exited 0 in 2.29 seconds (`real` time). The source has sorry count
0 and introduces no `admit` or `axiom`. The package remains pinned to Lean and
Mathlib v4.15.0.

This is not the Four Colour Theorem.

Feasibility: High (completed and package build verified).

## Next steps

- Supply `hopposite` from the upstream PlaneMap Jordan separation theorem.
- Keep that topological bridge outside this pinned graph-theoretic package.
