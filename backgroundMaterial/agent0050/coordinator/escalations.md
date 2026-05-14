# Escalations — Agent 0050-C

**Agent:** 0050-C
**Date:** 18 February 2026

---

## Escalation 1: Potential Circularity of Plan 2

**Source:** M2-S3 (Colour Elimination Lemma attempt)
**Severity:** High
**Status:** Open

### Issue

The Colour Elimination Lemma (if proved) would give a constructive proof of 4CT. But the key missing piece — the Chain Disconnection Lemma — might itself require 4CT or be of equivalent difficulty.

Specifically: the Chain Disconnection Lemma says that "safe" Kempe swaps (avoiding one protected colour) always suffice to prepare the chain landscape for a "final" swap. Proving this for ALL planar graphs might require understanding the global structure of Kempe chains to a depth that is essentially equivalent to proving 4CT by other means.

### Assessment

**M2's view:** Speculative — the conjecture has a reconfigurability flavour that's different from colourability, so a direct proof might exist.

**M1's view:** No computational counterexample found for $n \leq 6$, but the tested range is very small.

**Coordinator's view:** This is a genuine risk. If the Chain Disconnection Lemma turns out to be equivalent to 4CT, Plan 2 hasn't "reduced" the problem — it's just reformulated it. However, even a reformulation can be valuable if it suggests new attack vectors.

### Recommendation

1. Computationally test the Chain Disconnection Lemma for $n = 7, 8, 9$
2. If no counterexample: attempt a proof via structural induction on the triangulation
3. If a counterexample is found: Plan 2 needs revision (possibly adding more operations beyond Kempe swaps)
4. In parallel: explore whether the Las Vergnas-Meyniel connectivity of R(G,5) can be leveraged more directly

### Decision Needed

Should the project continue investing in Plan 2, or should effort shift to alternative approaches?

**My recommendation:** Continue for one more iteration. The computational extension to $n = 7, 8$ will either reveal hard cases (informing the theory) or extend the evidence base (encouraging the proof). This is the highest-value next step regardless of the answer.

---

## Escalation 2: Computational Scaling

**Source:** M1-S1, M1-S2
**Severity:** Medium
**Status:** Informational

### Issue

The current implementation enumerates all proper $k$-colourings via backtracking. For $n = 8$ triangulations:
- Number of 5-colourings could be $\sim 10^4 - 10^5$
- Building $\mathcal{R}(G, 5)$ requires $O(|V(R)|^2)$ edge checks
- Total compute time might be hours for $n = 8$

### Recommendation

For $n = 7$: should be feasible with current code (minutes).
For $n = 8$: may need optimization (parallel enumeration, smarter BFS, or sampling).
For $n \geq 9$: likely impractical with current approach. Consider:
- Sampling random 5-colourings instead of exhaustive enumeration
- Using Markov chain Monte Carlo on $\mathcal{R}(G, 5)$
- Focusing on specific "hard" triangulations rather than all triangulations

---

*0050-C — 18 February 2026*

---

## Escalation 3: CDL Disproved — Proof Architecture Pivot Required

**Source:** M1 (CDL computational testing, iteration 2)
**Severity:** High — but POSITIVE
**Status:** Resolved by M2's pivot

### Issue

The strict Chain Disconnection Lemma — the primary theoretical target of iteration 1 — is computationally FALSE starting at n=6. Safe-swaps-only (avoiding one protected colour) is insufficient even with 5 preparatory swaps.

### Resolution

M2 identified the "Never-Revert Lemma" (swaps on {1,2,3,4} never produce colour 5) which eliminates the need for the strict CDL. Unrestricted sequential elimination is provably monotone (colour-5 count can only decrease).

### Impact on Plan 2

Plan 2's proof strategy has pivoted from:
- OLD: Prove CDL → use safe swaps to sequentially eliminate colour 5
- NEW: Use unrestricted swaps (Never-Revert Lemma guarantees monotonicity) → prove distance bound via induction

The new approach is strictly stronger and simpler.

---

## Escalation 4: Inductive Proof Gap — Kempe Chain Correspondence

**Source:** M2-S3 (Alternative Architectures, iteration 2)
**Severity:** High
**Status:** Open

### Issue

M2's inductive proof of the distance bound (max R(G,5) distance to 4-colouring <= n-4) has a gap:

When we remove a degree-5 vertex v from G, the Kempe chain structure of G-v is different from G. A swap sequence that works in R(G-v, 5) may not directly correspond to a valid swap sequence in R(G, 5), because v's edges create new chain connections.

### Assessment

This gap could be:
(a) Closable with a "surgery" lemma for Kempe chains when adding a degree-5 vertex — **optimistic**
(b) As hard as 4CT itself (the gap IS the difficulty of 4CT, reformulated) — **pessimistic**
(c) Closable by working with general planar graphs instead of triangulations — **alternative**

### Recommendation

1. M1 should computationally test the inductive step: for each n=8 triangulation, remove a min-degree vertex, test both G-v and G, verify the distance relationship
2. M2 should attempt the surgery lemma for small cases (degree-3 and degree-4 vertices first, then degree-5)
3. Both teams should consider whether the gap is avoidable by a completely different argument

### Decision Needed

How much additional effort should be invested in closing this gap vs exploring other proof architectures? The risk of circularity remains.

**My recommendation:** One more iteration focused 50% on the gap and 50% on computational extension to n=9. The n=9 data will tell us whether the distance = n-4 pattern holds with 50 triangulations. If it holds, the inductive argument gains strong support. If it breaks, we need to rethink.

**Update (iteration 3):** n=9 computation COMPLETED. Bound holds (max=4 ≤ 5). Tightness breaks. See Escalation 5.

---

*0050-C — 18 February 2026*

---

## Escalation 5: The (a,5)-Chain Merge Gap — FINAL OPEN QUESTION

**Source:** M1 (chain merge analysis, iteration 3) + M2 (Chain Lifting Lemma, iteration 3)
**Severity:** High
**Status:** Open — the ONE remaining gap in the proof

### Issue

The inductive proof of the distance bound $d \leq n-4$ is complete EXCEPT for one unproved conjecture: that BFS-optimal reduction paths in $\mathcal{R}(G-v, 5)$ use $(a,5)$-Kempe chains that don't merge when vertex $v$ (colour 5, degree $\leq 5$) is added back to $G$.

### Evidence

- 42,168 colourings tested at n=8: zero merge failures in inductive lift
- 518 specific $(a,5)$-swaps examined in BFS paths: zero merges
- General $(a,5)$-chain merge rate when $c(v)=5$: ~12%
- But BFS paths NEVER use chains from that 12%

### Structural Hypotheses

1. **BFS prefers small chains.** Singleton $(a,5)$-chains (recolouring one vertex) can only merge with another chain if $v$ is adjacent to BOTH the singleton vertex and a vertex in another chain. For degree-$\leq$5 vertices, this constrains the geometry.

2. **Planar embedding constrains merges.** The non-interleaving property (Theorem A) limits how $(a,5)$-chains can be arranged around $v$'s neighbours.

3. **Ordering effect.** BFS processes colourings in distance order from 4-colourings. The closest 5-colourings to 4-colourings tend to have simple chain structures.

### Recommendation

This is the SINGLE open problem for the project. To close it:

1. **Prove Conjecture 5.4 directly** — show degree-$\leq$5 geometry prevents BFS-path chain merges.
2. **Bypass the conjecture** — find a path in $G$ directly instead of lifting from $G-v$.
3. **Extend computation** — n=10 (233 triangulations) would provide even stronger evidence.

### Decision Needed

Should the project invest in a 4th iteration focused on Conjecture 5.4, or declare current results as the final deliverable?

**My recommendation:** The current deliverable (draft paper + 23 tests + 280K verified colourings) is substantial and publishable as a partial result. A 4th iteration should only proceed if a clear attack vector for Conjecture 5.4 is identified.

---

*0050-C — 18 February 2026*
