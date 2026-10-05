# Support transport: checked first completion lemma

4 October 2026. Math and scale-up team. This report concerns the spherical support carrier, not triangulation completion or the general Four Colour Theorem.

## Exact delivered statement

For every `M : SphericalMap n`, Lean proves the existence of

```
N : SphericalMap (Nat.card M.graph.support)
i : M.graph.support ≃ Fin (Nat.card M.graph.support)
```

such that adjacency corresponds under i, `N.graph.support = Set.univ`, and every surviving vertex has its original degree. No connectedness, triangulation, generated PlaneMap history or nonempty-support hypothesis is required.

The construction transports darts, conjugates the cyclic rotation, maps face orbits, transports edge coefficients and vertex incidence, and proves `rotation.Fills`. A graph isomorphism is not being used as an unexplained substitute for the filling proof.

Additional delivered lemmas preserve any minimum-degree bound on the support, extend a support colouring over isolated labels using a supplied colour, and prove

```
x ∈ M.graph.support →
Nat.card (M.isolateGraph x).support < Nat.card M.graph.support.
```

This supplies the support measure needed for the later outer induction. It does not justify edge addition.

## Sources and tests

- `../mathlib4-planemap/Mathlib/Combinatorics/SimpleGraph/PlaneMap/SupportTransport.lean`
- `../mathlib4-planemap/MathlibTest/PlaneMapSupportTransport.lean`

The tests include disconnected deletion retaining two edges: five labels contract to four support labels. They also cover empty support, minimum-degree transport and extension of a four-colouring over isolates. Five guarded reports for filling, carrier existence, colouring extension, degree correspondence and strict support decrease contain only `propext`, `Classical.choice`, and `Quot.sound`.

A fresh dependency-ordered source rebuild passed all **43** custom modules and tests with **493** cached custom artifacts excluded. All source hashes were unchanged after compilation, and the previous 41 source hashes match their earlier audit. Evidence is in `backgroundMaterial/planemap-structural/support-transport-source-audit.json`, `support-transport-source-audit-output.txt`, and `support-transport-source-SHA256SUMS`. The last file lists paths relative to the mathlib checkout.

The chosen finite-label equivalence and colouring extension are classical. This is not an executable relabeller or completed solver. Given labels, the rotation transport is explicit; obtaining executable labels remains separate engineering work.

## Next proof obligations

Edge insertion, corner availability and triangulation completion remain open. The support-carrier portion of `TriangulationCompletionObligation.md` is now discharged by these sources; the obligation file and navigator are left for their owners to update. The next statement for Long Table's review is `EdgeInsertionStatement.md`.
