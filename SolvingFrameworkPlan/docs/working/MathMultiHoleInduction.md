# Multi-hole floor hypotheses and the fan identity: does an induction close?

Math lead, 6 October 2026. Hand only; Math's own analysis, **unreviewed**. Data: local compute 43378e7 (message 2040, `local-runs/14-two-hole/`), the two-hole test at orders 12–22.

**Verdict up front: a clear no.** The fan identity at one hole is exact bookkeeping and cannot supply the inequality at that hole. The induction hypothesis on the smaller graph gives information only about the *other* holes. Moving between Kempe classes of T − S and of the reduced graph runs into Kempe's two-vertex interference. The strongest clean multi-hole hypothesis is written down below as a statement worth recording. It does not reduce to smaller cases.

## 1. The hypothesis H_k

**Setting.**
- T is a triangulation, S = {h₁, …, h_k} a set of degree-5 vertices, pairwise non-adjacent, with no separating triangle through any hᵢ.
- A **state** is a proper 4-colouring of T − S.
- At each hole h ∈ S define, inside a Kempe class C of T − S:
  - F^h_i: states whose link at h is filled with singleton at i;
  - U^h_j: states whose link at h is unfilled with repeat pair {j, j+2};
  - D^h_j ⊆ U^h_j: the doubly locked ones, with the locks read in T − S.

> **H_k.** For every such T and S with |S| = k, every Kempe class C of T − S, every h ∈ S and every j:
>   |U^h_j ∩ C| ≤ |F^h_{j+1} ∩ C| + |F^h_{j+3} ∩ C| + |F^h_{j+4} ∩ C|.

- **H_1 is the strong per-j quarter-floor conjecture** (`MathQuarterFloorFinal.md`). It is at least as strong as 4CT.
- The data at k = 2 support it at orders 12–22: 92,255 pairs, 0 violations of the per-j inequality at each hole. Both holes are filled in at least 4/39 of every class, and every class contains states filled at some hole.
- A natural strengthening, H_k^joint, would add joint bounds (for example, both holes filled in ≥ 1/16 of every class). The data support that too (minimum 4/39).

## 2. The attempted reduction: the fan identity at one hole, inside a class

Fix h ∈ S and a legal fan τ at h. Let T\* = T\*_τ (delete h, add τ's two chords) and S′ = S ∖ {h}. Then:

- (a) **Colourings.** A colouring of T\* − S′ is a state of T − S whose link at h has the apex x_τ as a singleton (τ admits it). Conversely every such state is a colouring of T\* − S′.
- (b) **Classes map one way only [hand].** A Kempe swap in T\* − S′ restricts to T − S as a sequence of swaps of the pieces into which deleting the two chords splits the component. So each Kempe class of T\* − S′ maps into one Kempe class of T − S. This is the restriction lemma of Math's b66801f. The converse fails: a class C of T − S can contain τ-admitted states from several classes of T\* − S′, and states that τ does not admit (only 3 of the 5 fans admit a given unfilled state).
- (c) **What H_{k−1} on T\* gives.** T\* is smaller, and the holes S′ keep degree 5. (The chords touch only h's link vertices. If two of them both lie in the link of another hole w, a chord would close a separating triangle at w; that case must be excluded or handled.) So H_{k−1} applies inside classes of T\* − S′, and gives per-j inequalities **at the holes of S′ only**. **It says nothing about h**, because h is not a hole of T\*.
- (d) **What the fan identity gives at h.** The class identity at h (`MathQuarterFloorBijections.md` §2) holds inside C, read in T − S:

  3F^h − U^h = 2N₀^h + 1.5 L^h + Σ_paths (1 − d(P)) − D^h_cyc.

  It is **exact bookkeeping**. The inequality at h is equivalent to the right side being non-negative (Math, afaa460), which is H_1-type content at h. **Nothing in H_{k−1} on T\* touches it.**

**First failure point.** The inequality at the hole used for the reduction is never supplied by the smaller instance. An induction would need that inequality as an input, i.e. H_1 at h inside classes of T − S, which is the original 4CT-strength statement.

## 3. The reverse direction: from H_{k+1} at T to H_k at T

Add a hole: S⁺ = S ∪ {w}, with w non-adjacent to S.
- Restriction maps each class C of T − S into one class C⁺ of T − S⁺, and H_{k+1} holds in C⁺.
- To transfer the inequality at h back to C, we must know that the states of C⁺ counted by H_{k+1} come from C. They need not.
  - A state of C⁺ that is filled at w extends to a state of T − S, but possibly in a **different** class of T − S.
  - A state of C⁺ that is unfilled at w does not extend at all.
- Deciding which class of T − S a lift lies in is Kempe's two-vertex interference: whether chains through w's link merge components of T − S. Heawood's example shows this can fail.

**Second failure point.** Lifting from T − S⁺ to T − S. It is the same obstacle as for the distant-holes lemma (b66801f).

## 4. Where exactly more than the hypothesis is needed

1. **At the reduction hole**, an inequality inside classes of T − S that the smaller instance cannot see (§2, the first failure point).
2. **Comparing classes** of T − S, T\* − S′ and T − S⁺. Restriction goes one way (it merges classes, never splits them). Every inequality would need to be transported **backwards**, against the merge, i.e. lifted.
3. **The separating-triangle side condition** when two holes share link vertices (§2(c)). This is a technical gap, not the main one.

**What the data do say.** The floor survives adding a second hole: no class is pushed down to 1/4 by the second deletion, and joint fill fractions stay well above product bounds. **H_2 is therefore a robust, well-tested strengthening, recorded as a conjecture.** In the minimal-counterexample frame, H_k for any k ≥ 1 implies 4CT, so no form of H_k is easier than H_1 as a statement. An induction on k cannot start, because the reduction never produces the inequality at the hole it removes.

## 5. Status for the ledger

- **Recorded conjectures [computed, exploratory, orders 12–22].** H_2 (per hole, per j, inside classes of T − {v, w}, for non-adjacent v, w) and H_2^joint (both holes filled in ≥ 1/16 of every class; observed minimum 4/39).
- **Killed: "induction on k via the fan identity".** Each reduction needs the inequality at the removed hole as input, and classes do not transfer back against restriction.
