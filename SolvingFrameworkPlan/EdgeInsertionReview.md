# Review of the edge-insertion statement

4 October 2026. Long Table, WP5 statement review of [EdgeInsertionStatement.md](EdgeInsertionStatement.md), for the math team. This is informal mathematics, offered for checking, and it claims no Lean result. Short version: the statement is correct as far as we can verify. We suggest two simplifications and one reuse of a proved lemma.

## Question 1: the rotation update realises the intended split and merge

With faceNext′ = ρ′ ∘ reverse, the update gives:

```
a.symm → u_xy → ρ(b)        (old: a.symm → ρ(a))
b.symm → u_yx → ρ(a)        (old: b.symm → ρ(b))
```

with every other face transition unchanged. Apart from the two fresh darts, this exchanges the successors of a.symm and b.symm in the face permutation. Exchanging the successors of two elements of one cycle splits that cycle into two; doing so for two different cycles merges them. So the corners are exactly `a.symm` and `b.symm`, as the statement says.

**Chord.** Write the old orbit as a.symm → ρ(a) → … → b.symm → ρ(b) → … → a.symm. The new orbits are:
- **A** = (a.symm, u_xy, ρ(b), …, up to a.symm), which contains u_xy;
- **B** = (b.symm, u_yx, ρ(a), …, up to b.symm), which contains u_yx.

The fresh darts lie in different faces, and each new face contains the chord exactly once. That is the fact step 4 of the filling argument needs.

**Repeated vertices are harmless.** The argument concerns darts, not vertices, so repeated vertices on the old walk change nothing. Only a.symm ≠ b.symm is used, and it follows from x ≠ y.

**Non-adjacency also rules out digons.** Face B has length 2 exactly when ρ(a) = b.symm. Then b.symm starts at x, so b is a dart y → x and x is adjacent to y, which is excluded. The same holds for face A. So the hypothesis ¬G.Adj x y already guarantees both new faces have length at least 3. That may be worth stating as a lemma, since triangulation completion will want face lengths.

**Bridge.** The face successor ρ ∘ reverse never leaves a connected component, so darts in different components lie in different face orbits. The exchange therefore merges them, and both fresh darts land in the merged orbit, as stated.

## Question 2: availability

**The bridge case needs no availability lemma.** After support transport there are no isolated vertices, so every component has a dart. Take any dart in each of two components: the endpoints are automatically distinct and non-adjacent. Repeated bridge insertion therefore reaches a connected map with no further argument, and the edge count rises by components − 1.

**The chord case is the real lemma.** On a connected full-support map, any face of length ≥ 4 needs two corners at distinct, non-adjacent vertices. The classical route:
- Take consecutive corners v0, v1, v2, v3 on the face walk.
- If v0 ≠ v2 and the two are not adjacent, insert v0v2.
- Otherwise use v1v3. The diagonals v0v2 and v1v3 cannot both be edges, because they would have to cross outside the face.

The crossing step is exactly what a combinatorial Jordan argument provides. The navigator records "Even sets and local combinatorial Jordan separation" as proved, and Gate A's `alternating_walks_intersect` is a separation result of the same kind. We suggest checking whether one of these, applied to the face boundary rather than to a vertex star, already gives "both diagonals cannot exist" before proving anything new.

The cases v0 = v2 and v1 = v3, which are repeated vertices on short stretches of the walk, need explicit handling and are where we would expect the Lean work to concentrate.

We agree that a maximal-supermap argument can organise completion but cannot replace this local availability lemma.

## Question 3: a counting alternative to coefficient descent

Your face-coefficient normalisation for the bridge is sound. Adding 1 to every face coefficient of one component changes no edge's boundary coefficient, because both darts of each such edge lie in faces of that component. After normalisation the merged face's boundary is ∂F_a + ∂F_b, since the bridge is counted twice and vanishes over ZMod 2.

There may be a cheaper route. If the existing rank lemmas extend to the following characterisation, both preservation proofs reduce to arithmetic:

> Fills ⇔ s − e + f = 2·c, where c counts connected components of the support.

**Why the characterisation should hold:**
- Over ZMod 2, the cycle space has dimension e − s + c.
- If the kernel of the face-boundary map consists exactly of the functions that are constant on each component, its image has dimension f − c.
- Filling says the image equals the cycle space. That is f − c = e − s + c.

Gate B already uses the constant face function lying in the boundary kernel. The missing piece is the converse: that the kernel is no larger. That is face-connectivity within a component.

**Arithmetic once that holds:**
- **Chord:** e and f each rise by 1, c is unchanged, so the identity is preserved.
- **Bridge:** e rises by 1, f falls by 1 (two faces merge), and c falls by 1. The left side drops by 2, and so does 2c.

Whether this is cheaper depends on how much of the rank machinery is reusable. We offer it as an option, not a recommendation over your plan.

## Smaller notes

- **The permutation lemma.** "ρ′ is a permutation, preserves first vertices and stays cyclic at each vertex" could be stated once as a general dart-insertion lemma, then used for both cases.
- **Termination.** The edge bound for termination can come from Gate B's e + 2 ≤ s + f together with 3f ≤ 2e once all faces have length ≥ 3, which gives e ≤ 3s − 6. The digon observation above supplies "all faces have length ≥ 3" for every face created by insertion. Faces that already existed before completion still need the statement for themselves.
- **Colourings and Kempe components.** We agree that colourings transport by restriction and that Kempe components do not. Nothing in mass-macro descent is evaluated on N; it is evaluated on the completed T.

— The Long Table authors
