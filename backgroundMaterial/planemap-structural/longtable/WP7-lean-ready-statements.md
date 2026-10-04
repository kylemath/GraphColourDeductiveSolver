# Lean-ready statements for Lemma W and Lemma S

Long Table, 4 October 2026. This is prepared for the math team's return, to shorten formalisation. These are hand arguments only, not compiled; status words are the Proof Navigator's. They restate [WP7g](WP7g-warning-reduction.md) and [WP7e](WP7e-shared-hub-lemma.md) in the most abstract form we can.

## Lemma W, abstractly: no spherical or colouring content at all

**Data:**
- a finite type X (deletion colouring orbits);
- `rank : X → ℕ`;
- a set `Tgt ⊆ X` (targets);
- a relation `M2 : X → X → Prop`, meaning "reachable by a macro of at most two moves". Nothing about M2 is used except that it is a relation.

**Definition (good).** `Good : X → Prop` is the least predicate such that:
- `x ∈ Tgt → Good x`;
- `M2 x z → rank z < rank x → Good z → Good x`.

As an inductive predicate this is well-founded via `rank`. Call x a *dead end* if `¬ Good x`.

**The policy step, abstracted.** A policy state carries a finite warning set `W : Finset X`. The only transitions that touch W are of this form:

> **(warn)** `W ↦ insert c W`, permitted only when `c ∉ Tgt` and `∀ z, M2 c z → rank z < rank c → z ∈ W`.

The frozen breadcrumb policy warns only under exactly this condition: wave 1 found no unwarned decreasing candidate. Its other transitions (move, back, wave-2 restart) leave W unchanged.

**Lemma W1 (invariant).** If `∀ w ∈ W, ¬ Good w` and a (warn) step adds c, then `¬ Good c`.

**Proof.** Suppose `Good c`. Since `c ∉ Tgt`, the second constructor gives z with `M2 c z`, `rank z < rank c` and `Good z`. The warn condition gives `z ∈ W`, so `¬ Good z`. Contradiction. ∎

This needs no minimality or induction on rank beyond the definition of Good.

**Corollary W2.** Start with `W = ∅`. Every reachable policy state satisfies `W ⊆ {x | ¬ Good x}`. Since W is a Finset and warned elements are never warned again (the policy excludes W from every candidate set, so `insert` on a member never arises), the number of warn steps in a run is at most `card {x | ¬ Good x}`.

**Connection to mass-macro descent.** `{x | ¬ Good x} = ∅` exactly when every non-target x has a decreasing M2-successor. That is mass-macro Good(T, r) at the root, by induction on rank.

**Suggested Lean shape:**
- an `inductive Good` over a `Fintype X`;
- W1 as a one-line lemma;
- W2 via an invariant on a structure `PolicyState := (W : Finset X) …`, with the step relation as a disjunction of four constructors, only one of which changes W.

## Lemma S, with the link-cycle extraction spelled out

**Data:**
- a rotation system on a finite simple graph G, in which every face is a triangle;
- a vertex r, and H = G − r;
- a vertex h with `h ≠ r`, `¬ G.Adj h r`, and `deg h = d ≥ 5`;
- a proper colouring `c : V(H) → Fin 4`.

**Step 1 (link cycle).** Let `x₀, …, x_{d−1}` be the neighbours of h in rotation order at h. They are distinct because the graph is simple and the rotation is a cyclic permutation of the darts at h. With the repository convention `faceNext = rotation.next ∘ reverse`, the face containing the dart h → xᵢ is a triangle. Its third vertex is the rotation-neighbour of xᵢ at h, either x_{i+1} or x_{i−1} depending on orientation, and the face's third edge joins xᵢ to it. Hence **xᵢ and x_{i+1} are adjacent for every i, indices mod d.** This is the only fact used. No chord-freeness is needed. None of the xᵢ is r, because `¬ G.Adj h r`, so these adjacencies survive in H.

**Step 2 (independence bound).** Any set S ⊆ {x₀, …, x_{d−1}} with no two cyclically consecutive elements has `card S ≤ d / 2`, using natural-number division. This is a pure statement about `Fin d`. Each colour class of c on the link is such a set, by properness and Step 1.

**Step 3 (at most one singleton colour).** The link colours avoid `c h`, so the three remaining colours have class sizes summing to d, each at most `d / 2`. If two classes had size 1, the third would have size d − 2 > d / 2, since d ≥ 5. Contradiction.

**Step 4 (the toggle is pinned).** If `{h, x}` is a component of the `{c h, c x}`-subgraph with `x ∈ N(h)`, then no other neighbour of h has colour `c x`. So `c x` is a singleton colour on the link, and by Step 3, x is unique. Hence at most one two-vertex component contains h. ∎

**Suggested Lean shape.** The heart is a `Fin d` combinatorial lemma: no two consecutive elements in a set implies `card ≤ d / 2`. Step 1 is plausibly the existing face-triangle API, together with the new `FaceCorner` lemmas on face length. Step 4 is close to the reasoning in `KempeBoundary.singleton_chain_proper_target`, applied at an interior vertex.

## What these would and would not give, once compiled

- **W1/W2:** the breadcrumb warning count per run is at most |D_r|.
- **S:** at most one two-vertex toggle per hub outside N[r].

Neither bounds |D_r|. That is the remaining open quantity for breadcrumb descent's complexity, and it is now the precise form of the warning-bound obligation.
