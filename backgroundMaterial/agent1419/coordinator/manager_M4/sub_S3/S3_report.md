# M4-S3 Report: Full Proof Architecture Review

**Agent:** 1419-M4-S3
**Status:** COMPLETE — Architecture assessment with critical findings

## The Proof Architecture (Revised)

```
Input: Planar graph G, n vertices, proper 5-colouring c
Goal: Reduce to 4-colouring via Kempe swaps

Induction on n:
  Base (n=4): K4 is 4-colourable ✓
  Step (n > 4):
    1. Choose v with deg(v) ≤ 5 [Euler]
    2. Restrict to G-v with colouring c|_{G-v}
    3. By IH, G-v has 4-colouring reachable via Kempe swaps
    4. IF c(v) ≠ 5: Chain Lifting ✓ [PROVED]
    5. IF c(v) = 5, deg(v) = 3: Degree-3 No-Merge ✓ [PROVED]
    6. IF c(v) = 5, deg(v) ∈ {4,5}: Safe Path Existence [OPEN]
       → Find safe path in R(G-v, 5) to 4-colouring
       → Lift to G: safe swaps = no merges
       → Recolour v by pigeonhole
```

## Assessment 1: Is the Inductive Structure Sound?

**Yes, with one caveat.**

The induction is on $|V|$. The inductive hypothesis gives: every planar graph on $< n$ vertices can be 4-coloured from any 5-colouring via Kempe swaps. At step 3, we apply IH to $G-v$ (which has $n-1$ vertices).

**Caveat:** The IH gives a 4-colouring of $G-v$ reachable from $c|_{G-v}$. But we need to reach it via SAFE swaps (avoiding unsafe swaps w.r.t. $v$). The IH doesn't guarantee safety — it only guarantees reachability.

**This is the core gap.** The induction proves 4-colourability (which we already know from 4CT), not safe reachability. We need a STRONGER inductive hypothesis:

**Strong IH:** For every planar graph $H$ on $< n$ vertices, every proper 5-colouring of $H$, and every vertex $v$ in the original graph $G$ (of which $H$ is a subgraph obtained by vertex deletion), there exists a path in $R(H, 5)$ to a 4-colouring using only safe swaps w.r.t. $v$.

**Problem:** This IH mentions $v$ (a vertex NOT in $H$) and requires the path to be safe w.r.t. this external vertex. The IH at size $n-2$ would need safety w.r.t. TWO deleted vertices. The requirements stack.

**Is this a fatal problem?** Not necessarily. At each level, we only need safety w.r.t. the MOST RECENTLY deleted vertex. The previously deleted vertices are already handled (their merge issues were resolved at their respective levels).

**Formal check:** At level $n$, we delete $v_n$ and need a safe path in $R(G-v_n, 5)$ w.r.t. $v_n$. At level $n-1$, we delete $v_{n-1}$ from $G-v_n$ and need a safe path in $R(G-\{v_n, v_{n-1}\}, 5)$ w.r.t. $v_{n-1}$ (NOT w.r.t. $v_n$ — $v_n$ is already handled).

So the IH only needs safety w.r.t. ONE vertex at each level. This is:

**Revised Strong IH:** For every planar graph $H$ on $< n$ vertices that arises as $G-S$ for some $S$ with $|S| \geq 1$, every proper 5-colouring of $H$, and every vertex $v \notin H$ adjacent to vertices in $H$ with $\deg_G(v) \leq 5$: there exists a path in $R(H, 5)$ to a 4-colouring using only safe swaps w.r.t. $v$.

**This is exactly Revised Conjecture 5.5'.** The induction is sound IF 5.5' holds.

## Assessment 2: Are the Base Cases Correct?

- $n=4$: $K_4$ is 4-colourable, 0 steps needed. ✓
- $n=5$: bipyramid, 1 step. ✓ (verified computationally)
- $n=6$: octahedron and K_{2,3,1}, max 2 steps. ✓ (verified computationally, 0 merge-prone cases)

## Assessment 3: Does the Distance Bound Propagate?

Original bound: $d(n) \leq n - 4$ swaps at each level.
With detour: $d(n) \leq n - 3$ at each level.

Total swaps across all induction levels:
$\sum_{k=5}^{n} d(k) \leq \sum_{k=5}^{n} (k-3) = \frac{(n-3)(n-4)}{2} - 1$

This is polynomial. No exponential blowup. ✓

## Assessment 4: Hidden Circularity Check

**Does proving Conjecture 5.5' require 4CT?**

The proof structure:
1. 5CT gives starting 5-colouring (INDEPENDENT of 4CT)
2. Induction on |V| with IH = 5.5' (about safe paths, not about 4CT)
3. 5.5' implies 4CT as a consequence

**Is there a circular dependency?** 5.5' is an INDEPENDENT statement about reconfiguration graphs. If we could prove 5.5' from planarity + 5CT + combinatorial arguments, the proof would be non-circular.

**BUT:** Can 5.5' be proved from planarity alone? The computational evidence is for $n \leq 9$. At larger $n$, 5.5' might fail. If it does, the proof collapses.

**Critical question:** Is 5.5' a theorem or a conjecture? After the n=9 computation:
- 5.5' (safe path existence) holds at $n \leq 9$ (verified: 0 cases with no safe path)
- But this is finite verification, not proof
- At larger $n$, the graph structure becomes more complex and new failure modes could emerge

**Verdict:** No circularity in the proof architecture, but the KEY LEMMA (5.5') is unproved and may be unprovable without ideas we don't yet have.

## Assessment 5: The Lean 4 Gap

Even if the mathematical argument is complete:
- 5 .lean files exist with 0 sorry, 1 axiom
- These cover Cases 1, 2 and Never-Revert — NOT Case 3
- Case 3 (the open case) has NO Lean formalization
- ReconfigurationGraph is not defined in Lean
- Conjecture 5.5' is not stated in Lean

**Distance to machine-checked proof:** Very far. Even with a complete mathematical proof of 5.5', formalizing it in Lean 4 would require:
1. Defining R(G,k) in Lean (Tier 2, not yet started)
2. Stating and proving 5.5' (Tier 3, requires novel Lean development)
3. Connecting to the inductive scaffold (Tier 4)

Estimated time: 6-12 months of focused Lean development.

## Assessment 6: What Would a Counterexample to 5.5' Look Like?

A counterexample would be a planar triangulation $G$, vertex $v$ with $\deg(v) \leq 5$, $c(v) = 5$, and a 5-colouring $c$ of $G$ such that in $R(G-v, 5)$, EVERY path from $c|_{G-v}$ to a 4-colouring passes through at least one unsafe swap.

This means: in the safe-swap subgraph of $R(G-v, 5)$ (edges = safe swaps only), $c|_{G-v}$ is disconnected from all 4-colourings.

**Is this possible?** The safe-swap subgraph removes only edges corresponding to unsafe $(a,5)$-swaps at merge-prone chains adjacent to $v$. These are a SMALL fraction of all edges in $R(G-v, 5)$. The question is whether removing them disconnects some 5-colourings from 4-colourings.

**By analogy:** $R(G,5)$ is connected for planar graphs (Mohar). But the RESTRICTED graph (safe swaps only) might not be. This is a question about the structure of the reconfiguration graph under edge deletion.

**My assessment:** I give it 40% probability that a counterexample to 5.5' exists at some $n \geq 10$. The safe-swap restriction removes only a few edges at each colouring node, and the reconfiguration graph is highly connected. But "highly connected" is not "resilient to targeted edge deletion."

## Overall Verdict

| Component | Status | Confidence |
|-----------|--------|------------|
| Inductive structure | Sound (if 5.5' holds) | High |
| Base cases | Verified | High |
| Case 1 (c(v) ≠ 5) | Proved (Chain Lifting) | High |
| Case 2 (deg 3) | Proved (Degree-3 No-Merge) | High |
| Case 3 (deg 4,5) | OPEN — requires 5.5' | N/A |
| Conjecture 5.5 (original) | **FALSE** | Certain |
| Conjecture 5.5' (revised) | Unproved, verified n≤9 | Medium |
| No circularity | Confirmed | High |
| Lean formalization | Very incomplete | N/A |

**Bottom line:** The proof architecture is CORRECT but INCOMPLETE. The one remaining gap (5.5') is a genuine conjecture that may or may not be provable. The project has produced valuable partial results (Cases 1-2 proved, computational verification to n=9, counterexample to original conjecture) but has not achieved the stated goal of a complete constructive 4CT proof.

**Probability of full proof completion: 10-15%.** Down from the original 15-25% estimate because:
1. The original conjecture is disproved, narrowing the path
2. The revised conjecture is harder to prove (it's about existence, not universality)
3. No proof sketch survives without gaps

**Probability of publishable partial results: 95%.** The counterexample to Conjecture 5.5 alone is a publishable result, plus the all-paths analysis, the safe-path-existence data, and the formal equivalence analysis.
