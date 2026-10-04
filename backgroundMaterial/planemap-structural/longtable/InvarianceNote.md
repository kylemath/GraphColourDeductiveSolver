# Invariance of mass-macro descent

Long Table WP1, 4 October 2026. This is a written argument submitted for the math team's quantifier review. It is not a Lean theorem, and it assigns no status.

## Statement

Let T and T′ be finite simple graphs. Let φ : V(T) → V(T′) be a graph isomorphism, and let π be a permutation of the colours {0, 1, 2, 3}. Let r be a vertex of degree five in T and put r′ = φ(r). For a proper four-colouring c of T − r, define c′ = π ∘ c ∘ φ⁻¹ on T′ − r′.

Then:

1. c′ is proper.
2. R(c′) = R(c), where R is computed at r′ in T′.
3. The legal moves from c correspond bijectively to the legal moves from c′, and this correspondence commutes with applying a move.

Consequently Good(T, r) ⇔ Good(T′, r′). Any failure witness at (T, r) maps to a failure witness at (T′, r′) of the same rank.

**Corollaries.**
- **Automorphisms.** Taking T′ = T and φ an automorphism shows that the set of good roots {r ∈ D(T) : Good(T, r)} is a union of Aut(T)-orbits.
- **Isomorphic copies.** Two isomorphic triangulations have good-root sets that correspond under the isomorphism.

## Proof

- **Neighbourhoods and degrees.** φ preserves adjacency, so φ restricts to an isomorphism T − r → T′ − r′. It maps B = N_T(r) onto B′ = N_{T′}(r′) and preserves vertex degrees, so r′ is degree five and n′ = n.
- **Properness.** If uv is an edge of T − r, then c′(φu) = π(c(u)) ≠ π(c(v)) = c′(φv), because π is injective.
- **Bichromatic components.** For a colour pair {a, b}, a vertex u has c(u) ∈ {a, b} exactly when c′(φu) ∈ {π(a), π(b)}. The {a,b}-subgraph of c therefore maps isomorphically onto the {π(a),π(b)}-subgraph of c′, and φ sends each component K to a component φ(K). As {a, b} ranges over the six pairs, so does {π(a), π(b)}.
- **The rank.** K meets B exactly when φ(K) meets B′, and |K ∖ B| = |φ(K) ∖ B′|. So q(c) = q(c′). The number of colours on B equals the number on B′, because π is a bijection on colours, so p(c) = p(c′). With n′ = n this gives R(c) = R(c′). In particular, c is a target (p = 0) exactly when c′ is.
- **Moves.** Exchanging a and b on K, then transporting, gives the same colouring as exchanging π(a) and π(b) on φ(K) in c′. On φ(K) both read π(b) where c read a and π(a) where c read b; elsewhere both read π ∘ c ∘ φ⁻¹. So the transport map sends the move set of c bijectively onto the move set of c′ and commutes with each move.
- **Macros.** By induction on macro length, every sequence of at most two moves from c, with components recomputed after the first, corresponds to a sequence from c′ with identical ranks at every step. A decreasing macro exists at c exactly when one exists at c′. Because the transport is a bijection on deletion colourings, Good(T, r) ⇔ Good(T′, r′).
- **Colour classes.** The quotient by global colour renaming is respected: π acts on whole classes, and canonical representatives map to canonical representatives after re-canonicalisation.

## Remarks on scope

- **The rotation is never used.** The contract depends only on the graph, the root and the colouring. Invariance therefore holds for all graph isomorphisms, including orientation-reversing ones. The rotation enters only through the class definition: being a spherical triangulation is itself preserved by such isomorphisms.
- **Consequence for candidate sets.** For a candidate set S(T) ⊆ D(T) that is equivariant under isomorphism, "every member of S(T) is good" is now a property of the isomorphism class, so evaluating it on the Plantri corpus is well-posed. A label-based tie-break only affects which good-or-bad member gets chosen, not the every-member guarantee.
- **What this note does not claim:**
  - that the good-root set is nonempty (MMD-exists);
  - that it can be found efficiently (MMD-select);
  - that equivariant candidate sets exist that avoid bad roots.

## The (σ, β) game is not covered

The fixed observation game uses three label-dependent conventions:
- the boundary is rotated to start at its minimum label;
- colours are canonicalised boundary-first from that start;
- β refers to the minimum remaining label and to the canonical colour pair {1, 3}.

None of these is preserved by an arbitrary relabelling, so the argument above does not apply. The regression run confirms this behaviour. In 3 of 6 seeded random relabellings of graph 36 (order 20), at least one of the eight exterior roots changed its (σ, β) outcome. Over the same six relabellings, the root-8 mass-macro counts (198 / 131 / 3 / 0) and the full rank multiset were unchanged. See `regressions.json`, `sigma_beta_relabelling_diagnostic`.

**Implication:** a candidate set should state which check it targets. Mass-macro goodness is structural. A (σ, β) win is a fact about one labelling.
