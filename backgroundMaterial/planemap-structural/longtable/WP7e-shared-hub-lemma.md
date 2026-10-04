# WP7e: the shared-hub lemma (why interior toggles at one hub cannot accumulate)

Long Table, 4 October 2026. This is a statement with a hand proof, submitted for the math team's checking and, if they choose, formalisation. **No test is run for this note.** Status words are the Proof Navigator's.

## Setting

- T is a finite simple spherical triangulation with minimum degree ≥ 5.
- r is a vertex; H = T − r; c is any proper colouring of H with colours in Fin 4.
- A **toggle at h** is a bichromatic component of c with exactly two vertices, {h, x}, where x ∈ N(h). Its colour pair is {c(h), c(x)}.

## Lemma S (one toggle per hub)

Let h be a vertex of H with h ∉ N(r), so that h keeps its full neighbourhood in H. Then in every proper colouring c of H, **at most one** toggle contains h.

**Proof.**
1. **The link is a cycle.** Since T is a triangulation and h ≠ r with h ∉ N(r), the neighbours of h in H are all of N_T(h). They induce, along the rotation at h, a cycle C of length d = deg_T(h) ≥ 5. The cycle's edges are edges of T between consecutive neighbours, and they survive in H because neither endpoint is r. C may have chords; only its cycle edges are used below.
2. **Each colour is used at most ⌊d/2⌋ times on C.** Every vertex of C has a colour other than c(h), so C uses at most three colours. Each colour class is an independent set in C, and an independent set of a d-cycle has at most ⌊d/2⌋ vertices.
3. **At most one colour is used exactly once on C.** Suppose two colours each appeared exactly once. The third colour would then occupy the remaining d − 2 vertices. For d ≥ 5 we have d − 2 > ⌊d/2⌋, which contradicts step 2.
4. **The toggle's x is pinned down.** If {h, x} is a {c(h), c(x)}-component, then x is the only neighbour of h coloured c(x), since any other would join the component. So c(x) is used exactly once on C, and by step 3 there is at most one such colour. Hence x is determined, and at most one toggle contains h. ∎

**Remarks.**
- **Degree 5 gives exactly one candidate.** For d = 5 the counts must be (2, 2, 1): an odd cycle needs all three colours, each used at most twice. So exactly one neighbour x* has a unique colour. A toggle at h exists only if, in addition, h is the only neighbour of x* coloured c(h).
- **The hypothesis d ≥ 5 is sharp.** For d = 4, counts (2, 1, 1) allow two singleton colours, and the lemma fails.
- **Only cycle edges are used.** Chords of C can only shrink the independent sets, so they don't affect the argument.
- **No symmetry, no spherical filling.** Beyond "the link of h is a cycle in H", the lemma uses neither. In Lean, a rotation system with each face a triangle supplies that hypothesis.

## Corollary at the named fixture (order 17, graph 3)

- **Root 3, opposite hub 13.** Vertex 13 is not adjacent to 3 and has degree 5. The five WP7d toggles are {13, 16}, {12, 13}, {6, 13}, {7, 13} and {13, 14}. They all contain 13, and they use the five *different* neighbours of 13. By Lemma S, in any colouring at most one of them is a toggle.
- **What distinguishes the pits.** Each pit is labelled by *which* neighbour of the hub carries the unique colour. Passing from one pit to another requires changing that neighbour. That is consistent with the WP7d findings that pits are not joined by single swaps, and that other pits' toggle sets never appear as components.
- **Root 13** is the same, with hub 3 and toggles {3, 10}, {3, 9}, {3, 4}, {0, 3} and {2, 3}.

## What Lemma S does and does not give

**It does give an exact mechanism for C7d at this fixture.** Two-vertex interior variants that share a hub can never coexist in one colouring. The WP7d no-joint-switching observation is therefore a theorem for toggles at a common hub, not an accident of symmetry.

**It does not give:**
- **Toggles at different hubs.** These can coexist. Accumulation of independent interior variants would need **toggles at several disjoint hubs**, each outside N(r). That is exactly the configuration that could break C7d.
- **Larger toggles.** The lemma says nothing about interior variants made of components larger than two vertices.
- **A warning bound.** It bounds, per hub, the number of *simultaneously available* two-vertex toggles. It does not bound how many pits a run visits.

## Proposed next step (a proposal only; not run without explicit agreement)

**Targeted constructions instead of a census.** Look for triangulations with min degree 5 containing **two or more degree-five hubs, far apart and both outside N(r)**, each of which could host a pit structure. Then ask whether breadcrumb runs there warn on colourings that differ by toggles at different hubs and share χ. That would refute C7d.

**Two possible routes**, both needing joint agreement because they go beyond order 20:
- **Plantri at order 21–22,** filtered for roots with two distant degree-five hubs.
- **Explicit gluing:** two copies of the order-17, graph-3 hub region, joined along a band of degree-six vertices.

The adversary (WP3) would run the frozen breadcrumb policy and the C7d check on the result.
