# Edge insertion: precise statement for joint review

4 October 2026. Math and scale-up draft for Long Table and the navigator. No edge-insertion theorem is claimed here. Support transport is checked separately in `SupportTransportReport.md`.

## One local operation, two cases

Let `M : SphericalMap n`, `G=M.graph`, and `rho=M.rotation.next`. Choose existing darts `a,b : G.Dart` with first vertices `x,y`, with `x ≠ y` and `¬G.Adj x y`. Set

```
H.Adj u v := G.Adj u v or
            (u=x and v=y) or (u=y and v=x).
```

Distinct nonadjacent ends make H a simple graph, with exactly the old edges plus xy. Its dart type is equivalent to the old darts plus two fresh symbols `u_xy,u_yx`. Dart reversal acts as old reversal on old darts and exchanges the new symbols.

Define the new vertex rotation on this extended dart type:

```
rho'(old a) = u_xy          rho'(u_xy) = old(rho a)
rho'(old b) = u_yx          rho'(u_yx) = old(rho b)
rho'(old d) = old(rho d)    for d different from a and b.
```

The insertions are immediately after a and b in their vertex rotations. Prove the map is a permutation, preserves first vertices and remains cyclic at each vertex. Its face permutation is `rho' ∘ reverse`, consistent with the repository's `faceNext`.

The relevant old face corners are therefore **`a.symm` and `b.symm`**, not automatically `faceOf a` and `faceOf b`: the old transitions from these reversed darts are precisely the transitions interrupted by insertion. Every subsequent orbit statement must use this convention.

### Chord case

Assume `M.faceOf a.symm = M.faceOf b.symm`. Prove that insertion splits that one face dart-orbit into two, leaves other face orbits intact, and puts the two fresh darts in different new faces. This claim allows repeated old vertices; it uses distinct chosen corners and distinct endpoint vertices, not an assumption that the entire old face walk is a simple cycle.

Then prove the new rotation satisfies `Fills`. The intended argument is:

1. Prove the coefficient function of a single face boundary is even for this rotation.
2. Identify the sum of the two new face boundaries with the old face boundary, extended by zero on xy.
3. For an even new edge coefficient function with coefficient zero on xy, restrict to old edges, apply old filling, and give both split faces the old face's coefficient.
4. If the coefficient on xy is one, add one new face boundary to cancel it, apply the zero-coefficient case, and add that face boundary back.

All face identifications and incidence equalities need proofs. This is not an assumption that the new rotation is spherical.

### Bridge case

Assume x and y belong to different connected components of G. Prove their selected face dart-orbits are different; insertion merges those two orbits, leaves other orbits intact, and puts both fresh darts in the same merged face orbit.

For filling preservation:

1. Show an even new edge coefficient function has coefficient zero on the bridge. Summing incidence over one old component is a possible proof.
2. Restrict to old edges and apply old filling.
3. Old face coefficients on the two selected faces need not match. Add a constant to all face coefficients belonging to one old component to make them agree. Every old edge sees that constant twice, so its boundary coefficient is unchanged over `ZMod 2`.
4. Descend the normalized coefficients to the merged face orbit and prove the new filling equation.

Define face/component membership and coefficient descent explicitly. In this carrier, components do not already share a dart-orbit face. Edgeless rotations have a special empty-face branch; the operation here selects existing darts, so it does not by itself cover connecting an isolated vertex. Completion applies after support transport, where no isolated vertex remains.

## What this operation does not prove

It does not prove that a suitable nonadjacent corner pair exists in every nontriangular face, or that repeated face walks admit the needed choice. Nor does a missing pair in a particular face refute all triangulation completion: another insertion or another valid rotation may be available.

Completion coverage must separately establish: for a full-support minimum-degree-five spherical map that is not yet a connected triangulation, either suitable darts in different components exist or a suitable same-face chord insertion exists, or supply another specified operation with its own preservation proof. A maximal-supermap argument may organize this, but cannot assume the local availability lemma.

Each insertion increases the edge count; a proved bound can support completion termination once availability is established. The outer colouring induction uses support cardinality, already shown to decrease on isolation. Adding edges transports proper colourings by restriction, not Kempe components or histories.

## Questions for statement review

1. Does the explicit rotation update match the intended corners and split/merge operation in every repeated-face case?
2. Can we prove chord availability directly, or should we first establish stronger connectedness/face-boundary properties of a maximal simple spherical supermap?
3. Is face-coefficient normalization on one component the cleanest bridge filling proof, or is an equivalent cycle-space argument simpler in the current API?

After review, these local operations can be formalized separately from the global coverage lemma. No unproved operation is used by the existing colour theorems.
