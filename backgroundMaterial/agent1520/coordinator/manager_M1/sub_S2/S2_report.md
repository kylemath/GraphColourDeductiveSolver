# Sub-task S2 Report: Degree-5 Case Analysis for {1,2,3,4}-Swap Sufficiency

**Agent:** 1520-M1-S2  
**Date:** 20 February 2026  
**Task:** Exhaustive analysis of all colour types at degree-5 vertices; identification of hardest cases and proposed proof strategies.

---

## 1. Setup and Definitions

**Setting.** Let $G$ be a planar triangulation, $v$ a vertex with $\deg(v) = 5$ and $c(v) = 5$ in a proper 5-colouring. The link of $v$ is $\text{lk}(v) = C_5 = w_1 w_2 w_3 w_4 w_5 w_1$ (a 5-cycle). Since $c(v) = 5$ and the colouring is proper, each $w_i$ is coloured from $\{1,2,3,4\}$.

**Non-adjacent pairs in $C_5$:** $(w_1,w_3), (w_1,w_4), (w_2,w_4), (w_2,w_5), (w_3,w_5)$ — five non-adjacent pairs.

**Non-interleaving property (Theorem A).** For disjoint colour pairs $\{a,b\}$ and $\{c,d\}$, the corresponding Kempe chains do not interleave in the cyclic order of the planar embedding.

---

## 2. Colour Type Enumeration at Degree 5

The five neighbours $w_1, \ldots, w_5$ lie on $C_5$, coloured from $\{1,2,3,4\}$. By the pigeonhole principle, at least one colour is repeated.

### 2.1 Proper Colourings of $C_5$ with 4 Colours

In $C_5$, adjacent vertices must differ. The chromatic polynomial $P(C_5, k) = (k-1)^5 + (k-1)$. For $k = 4$: $P(C_5, 4) = 3^5 + 3 = 243 + 3 = 246$ proper colourings.

### 2.2 Abstract Types by Multiplicity Pattern

The possible multiplicity patterns of 5 elements drawn from {1,2,3,4} are:

| Pattern | Notation | Condition for proper colouring |
|---------|----------|-------------------------------|
| [1,1,1,1,1] | — | Impossible (5 items from 4 colours, pigeonhole) |
| [2,1,1,1] | One pair, three singletons | Pair must be on non-adjacent vertices |
| [2,2,1] | Two pairs, one singleton | Each pair on non-adjacent vertices |
| [3,1,1] | One triple, two singletons | Triple vertices pairwise non-adjacent? |
| [2,2,1] is already listed | — | — |
| [3,2] | One triple, one pair | Very constrained |
| [2,3] | — | Same as [3,2] |
| [4,1] | Four same, one different | Requires 4 vertices pairwise non-adjacent in $C_5$ |
| [5] | All same | Impossible (adjacent vertices share colour) |

**Feasibility check in $C_5$:**

- **[2,1,1,1]:** 2 vertices same colour, must be non-adjacent. In $C_5$, each vertex has 2 non-adjacent vertices. Feasible.

- **[2,2,1]:** Two pairs of same colour on non-adjacent vertices each. The two pairs use 4 vertices, leaving 1 singleton. In $C_5$, can we find two disjoint non-adjacent pairs? Yes: e.g., $(w_1,w_3)$ and $(w_2,w_5)$ — but $w_2$ and $w_5$ are adjacent! So not all disjoint non-adjacent pairs work. Valid disjoint non-adjacent pairs: $(w_1,w_3)$ and $(w_2,w_4)$? $w_2$ and $w_4$ are non-adjacent. ✓ And the remaining vertex $w_5$ gets the singleton colour. Feasible.

- **[3,1,1]:** 3 vertices same colour. In $C_5$, is there an independent set of size 3? The maximum independent set in $C_5$ has size 2. Wait — $C_5$ has independence number 2. So [3,1,1] is **IMPOSSIBLE**.

  Actually, let me recheck. $C_5 = w_1 w_2 w_3 w_4 w_5 w_1$. Edges: $(1,2),(2,3),(3,4),(4,5),(5,1)$. Independent sets: $\{w_1, w_3\}$ (size 2), $\{w_1, w_3, ??\}$ — $w_1$ is adjacent to $w_2, w_5$; $w_3$ is adjacent to $w_2, w_4$. So remaining candidates are just $w_4$ or $w_5$. But $w_3$ adj $w_4$, and $w_1$ adj $w_5$. No independent set of size 3 exists.

  **Correction:** $C_5$ has independence number 2. So [3,1,1], [3,2], [4,1], [5] are all impossible.

### 2.3 The Two Feasible Structural Types

**Type I: [2,1,1,1]** — One colour appears twice (on a non-adjacent pair), three colours appear once each. All 4 colours from $\{1,2,3,4\}$ are used.

**Type II: [2,2,1]** — Two colours each appear twice (on non-adjacent pairs), one colour appears once. Only 3 of the 4 colours from $\{1,2,3,4\}$ are used.

### 2.4 Concrete Colour Multisets

**Type I:** Choose the repeated colour (4 choices), choose the non-adjacent pair (5 pairs in $C_5$), choose which 3 of remaining colours go to the 3 singletons (3! = 6 arrangements). Accounting for proper colouring constraint on $C_5$: the two non-adjacent positions $w_i, w_j$ get colour $a$; the 3 remaining positions $w_k, w_l, w_m$ (forming a path of length 3 or a $P_3$ in $C_5$) must get 3 distinct colours from $\{1,2,3,4\} \setminus \{a\}$ properly. This is always possible since a path on 3 vertices with 3 colours always has a proper colouring.

As sorted multisets over colours, the concrete multisets are of the form $(a, a, b, c, d)$ with $\{a,b,c,d\} = \{1,2,3,4\}$.

Number of sorted multisets: $\binom{4}{1} = 4$ choices for $a$; the remaining 3 colours are always $\{1,2,3,4\}\setminus\{a\}$. So 4 distinct sorted multisets:
- $(1,1,2,3,4)$, $(1,2,2,3,4)$, $(1,2,3,3,4)$, $(1,2,3,4,4)$

**Type II:** Choose 2 colours for the pairs (choose 2 from 4: $\binom{4}{2} = 6$), the third colour is the singleton. This gives sorted multisets like $(a, a, b, b, c)$.

Number of sorted multisets: We pick which 2 of 4 colours are doubled, then the singleton is one of the remaining 2 colours. Wait — with 5 positions and 2 pairs + 1 singleton, we use 3 colours total. Choose 2 colours for the pairs: $\binom{4}{2} = 6$. The singleton must be one of the remaining 2 colours: 2 choices. But as sorted multisets, $(a,a,b,b,c)$ is determined by specifying which 2 colours are doubled and which is the singleton. So 6 × 2 / ... actually there's no overcounting. Let me enumerate:

- Pairs (1,2), singleton from {3,4}: $(1,1,2,2,3)$ and $(1,1,2,2,4)$
- Pairs (1,3), singleton from {2,4}: $(1,1,2,3,3)$ and $(1,1,3,3,4)$
- Pairs (1,4), singleton from {2,3}: $(1,1,2,4,4)$ and $(1,1,3,4,4)$
- Pairs (2,3), singleton from {1,4}: $(1,2,2,3,3)$ and $(2,2,3,3,4)$
- Pairs (2,4), singleton from {1,3}: $(1,2,2,4,4)$ and $(2,2,3,4,4)$
- Pairs (3,4), singleton from {1,2}: $(1,3,3,4,4)$ and $(2,3,3,4,4)$

That's **12 sorted multisets** for Type II.

**Total: 4 + 12 = 16 sorted multisets.**

But structurally, the merge analysis depends on which colour is repeated and where. For the purpose of proof, we abstract:

**Type I has 1 merge-prone colour** (the repeated one).
**Type II has 2 merge-prone colours** (the two repeated ones).

Under colour-label symmetry, there are **2 genuinely distinct proof cases** (one-pair and two-pair), matching the degree-4 analysis.

The task brief mentions "7 non-trivial colour types." This likely refers to:
- Type I with 4 choices for the repeated colour → 4 subtypes
- Type II with $\binom{4}{2} = 6$ choices for the pair of doubled colours, but these are equivalent under relabeling → however, the specific identity matters for merge analysis
- Or a different classification system

For our analysis, we work with the 2 structural types.

---

## 3. Merge Geometry at Degree 5

### 3.1 Non-Adjacent Pair Analysis

In $C_5$, the 5 non-adjacent pairs are:

| Pair | Vertices | Cyclic gap |
|------|----------|------------|
| 1 | $(w_1, w_3)$ | 2 |
| 2 | $(w_1, w_4)$ | 2 (going the other way: 3) |
| 3 | $(w_2, w_4)$ | 2 |
| 4 | $(w_2, w_5)$ | 2 (going the other way: 3) |
| 5 | $(w_3, w_5)$ | 2 |

Every non-adjacent pair has cyclic gap 2 (from one side). Note that ALL non-adjacent pairs are at the same "distance" in the cycle, unlike $C_4$ where we distinguish gap-2 (opposite) from gap-1 (adjacent).

### 3.2 Degree-5 Merge Geometry

**Key difference from degree 4:** In $C_4$, adjacent vertices share an edge → same chain (proved). In $C_5$, adjacent vertices also share an edge → same chain. BUT in $C_5$, there are MORE non-adjacent pairs (5 vs 2), and different non-adjacent pairs can INTERFERE.

**Lemma (Degree-5 Adjacent Same-Chain).** If $w_i$ and $w_{i+1}$ (cyclically adjacent in $C_5$) are both in $B_{a,5}(G-v)$, they are in the same $(a,5)$-chain in $G-v$.

*Proof.* Identical to degree-4: $w_i$ and $w_{i+1}$ are adjacent in $G$ (link of $v$ in a triangulation), both coloured $a$, so connected in the bichromatic subgraph. $\square$

**Corollary.** Merges at degree-5 can only occur between non-adjacent pairs in $C_5$.

### 3.3 Merge Geometry Constraints from Planarity

For Type I ($a$ appears on $w_i, w_j$ non-adjacent): the merge analysis is identical to degree-4 Type B. Two neighbours coloured $a$ on a non-adjacent pair may be in different $(a,5)$-chains. Adding $v$ back (coloured 5) would merge them.

For Type II ($a$ on $w_i, w_j$ and $b$ on $w_k, w_l$): BOTH colours are merge-prone. The non-interleaving property constrains the arrangement:

**Constraint from non-interleaving:** If $\{a, 5\}$ and $\{b, 5\}$ share colour 5, the non-interleaving theorem (for disjoint pairs) doesn't directly apply. However, a weaker form holds: planarity prevents the $(a,5)$- and $(b,5)$-chains from "crossing" in an incompatible way.

**Key observation:** In Type II, the two non-adjacent pairs $(w_i, w_j)$ for colour $a$ and $(w_k, w_l)$ for colour $b$ must be disjoint (different vertices — the 4 vertices form two pairs, leaving 1 singleton). This constrains which non-adjacent pair combinations are feasible:

Valid disjoint non-adjacent pair assignments in $C_5$:
- $(w_1,w_3)$ for $a$ and $(w_2,w_4)$? No — remaining vertex $w_5$ is adjacent to both $w_4$ and $w_1$, which is fine, it just needs a colour different from both its neighbours.
  Actually we need to check: can $(w_1,w_3)$ and $(w_2,w_4)$ be non-adjacent pairs? $w_1,w_3$: non-adjacent ✓. $w_2,w_4$: non-adjacent ✓. They share no vertices ✓.

The complete list of disjoint non-adjacent pair combinations:

| Pair A | Pair B | Remaining vertex |
|--------|--------|-----------------|
| $(w_1,w_3)$ | $(w_2,w_4)$ | $w_5$ |
| $(w_1,w_3)$ | $(w_2,w_5)$ | $w_4$ — but $w_2,w_5$ are adjacent! ✗ |
| $(w_1,w_3)$ | $(w_4,w_5)$ | — $w_4,w_5$ are adjacent! ✗ |
| $(w_1,w_4)$ | $(w_2,w_5)$ | $w_3$ — but $w_2,w_5$ adj and $w_1,w_4$? $w_1$ adj $w_2,w_5$; $w_4$ adj $w_3,w_5$. $w_1,w_4$: non-adj ✓. $w_2,w_5$: adj ✗ |
| $(w_1,w_4)$ | $(w_3,w_5)$ | $w_2$. $w_1,w_4$ non-adj ✓. $w_3,w_5$ non-adj ✓. ✓ |
| $(w_2,w_4)$ | $(w_3,w_5)$ | $w_1$. Both non-adj ✓. ✓ |
| $(w_2,w_5)$ | ... | $w_2,w_5$ are adjacent ✗ |

So there are exactly **3 valid combinations** of disjoint non-adjacent pairs in $C_5$:
1. $(w_1,w_3)$ and $(w_2,w_4)$, remaining $w_5$
2. $(w_1,w_4)$ and $(w_3,w_5)$, remaining $w_2$
3. $(w_2,w_4)$ and $(w_3,w_5)$, remaining $w_1$

**These 3 configurations (up to rotation/reflection of $C_5$) are the possible Type II merge geometries.**

Actually, by rotation symmetry of $C_5$, these 3 are all equivalent (each is a rotation of the others). So there is essentially **one Type II merge geometry** up to symmetry.

---

## 4. Analysis per Type

### 4.1 Type I: One Repeated Colour (e.g., $a$ on $w_i, w_j$ non-adjacent)

**Merge analysis:** Identical structurally to degree-4 Type B. Colour $a$ is merge-prone; colours $b, c, d$ (the three singletons) are safe.

**{1,2,3,4}-swap alternatives:** At a merge-prone $(a,5)$-step, the following safe swaps are available:
- $(b,c)$, $(b,d)$, $(c,d)$-swaps (three $\{1,2,3,4\}$-pairs not involving $a$)
- $(a,b)$, $(a,c)$, $(a,d)$-swaps (three $\{1,2,3,4\}$-pairs involving $a$ — these change $a$'s chain structure but don't involve colour 5)

**Claim:** The BFS-optimal path can always be rerouted through $\{1,2,3,4\}$-swaps at Type I merge-prone steps.

**Evidence:** 100% avoidance at $n \leq 8$ (668/668 degree-5 merge-prone cases). All cases used $\{1,2,3,4\}$-swaps as alternatives.

**Difficulty relative to degree 4:** The degree-5 link is $C_5$ (5 vertices) vs $C_4$ (4 vertices). The chain structure in $G - v$ is potentially more complex because $v$ has more neighbours, but the proof argument is the same: at a merge-prone step, safe alternatives exist.

### 4.2 Type II: Two Repeated Colours (e.g., $a$ on $w_i,w_j$ and $b$ on $w_k,w_l$)

**Merge analysis:** BOTH $a$ and $b$ are merge-prone simultaneously. This creates a "double-merge" scenario where two different $(a,5)$- and $(b,5)$-swaps are dangerous.

**{1,2,3,4}-swap alternatives:**
- $(a,b)$-swap: exchanges the two merge-prone colours. Still a $\{1,2,3,4\}$-swap (safe). This is particularly useful as it can break the double-merge structure.
- $(a,c)$, $(b,c)$-swaps (where $c$ is the singleton colour)
- Swaps involving the unused colour $d$

**Key insight:** Even with TWO merge-prone colours, the $\{1,2,3,4\}$-swap alternatives are abundant. There are $\binom{4}{2} = 6$ colour pairs, and only 2 of them involve colour 5 (i.e., $(a,5)$ and $(b,5)$). The other 4 are safe.

**Hardest sub-case:** When the BFS-optimal path requires an $(a,5)$-swap at a step where an $(a,b)$-swap doesn't achieve the same distance reduction. This is the scenario that would break the conjecture.

**Difficulty relative to Type I:** Higher merge rate (both colours contribute), more constrained chain topology. From Agent 1210's data, Type II has the highest merge rate among degree-5 configurations.

---

## 5. The Hardest Colour Types

### 5.1 Candidate: Type II with Maximum Chain Overlap

The hardest configuration for the conjecture is when:
1. Both repeated colours are merge-prone (Type II)
2. The merge-prone chains are LARGE (spanning much of the graph)
3. $\{1,2,3,4\}$-swaps offer limited distance reduction

This corresponds to the "forced bottleneck" adversarial attack from Agent 1210, which tested 25,968 cases where ALL $(a,5)$-chains are adjacent to $v$. Even in these extreme cases, BFS found $\{1,2,3,4\}$-alternatives.

### 5.2 Why Degree 5 is Harder than Degree 4

Three structural reasons:

1. **Higher merge rate:** 30.9% vs 17.4% (from Agent 1210 data). More situations are merge-prone.

2. **More neighbours → more chain interactions:** 5 neighbours (vs 4) means more potential $(a,5)$-chains touch $v$'s neighbourhood. The "chain landscape" is richer and more constrained.

3. **Non-interleaving provides weaker constraints:** In $C_5$, the non-interleaving property constrains chain topology but doesn't fully determine it. In $C_4$, the simpler structure (only 2 non-adjacent pairs) makes the geometry more tractable.

### 5.3 Why the Proof Might Still Work

Despite being harder, degree 5 has a compensating advantage:

**More $\{1,2,3,4\}$-swap options.** With 5 neighbours, there are more $\{1,2,3,4\}$-chains touching $v$'s neighbourhood. This means MORE safe swap alternatives, partially offsetting the increased merge risk.

Specifically: at degree 4, the $C_4$ link has 4 edges and 4 vertices. At degree 5, $C_5$ has 5 edges and 5 vertices. The number of Kempe chains intersecting the neighbourhood grows with the neighbourhood size, providing more "escape routes" from merge-prone steps.

---

## 6. Non-Interleaving Analysis

### 6.1 Theorem A Application

Theorem A (Non-Interleaving): For a planar graph $G$ with proper $k$-colouring and two disjoint colour pairs $\{a,b\}$ and $\{c,d\}$: the Kempe chains of these two pairs do not interleave in the cyclic order around any face or vertex.

At a degree-5 vertex $v$, the cyclic order of neighbours $w_1, \ldots, w_5$ is determined by the planar embedding. Non-interleaving constrains how chains of different colour pairs can connect the neighbours.

### 6.2 Impact on Type II

For Type II with pairs $\{a,5\}$ and $\{b,5\}$: these share colour 5, so Theorem A (which requires DISJOINT pairs) does NOT directly apply.

However, for the $\{1,2,3,4\}$-swap alternatives: pairs like $\{a,b\}$ and $\{c,d\}$ (where $\{a,b,c,d\} = \{1,2,3,4\}$) ARE disjoint, and Theorem A applies fully. This constrains the topology of the safe swaps.

### 6.3 Chain Separation Property

**Observation.** In $C_5$, an $(a,b)$-chain connecting $w_i$ to $w_k$ separates the remaining neighbours into two groups. If $w_j$ and $w_l$ are on opposite sides of this separating chain, no $(c,d)$-chain (for $\{c,d\}$ disjoint from $\{a,b\}$) can connect $w_j$ to $w_l$ without crossing the $(a,b)$-chain.

This separation property limits the ways chains can interact, which could be leveraged in a proof of swap sufficiency: if a merge-prone $(a,5)$-chain separates certain vertices, the $\{1,2,3,4\}$-swaps in the separated regions can be analyzed independently.

---

## 7. Proposed Proof Strategies

### 7.1 Strategy A: Restricted Reconfiguration (same as degree 4)

Prove that $d_{\mathcal{R}_{\text{safe}}}(\chi, \chi') = d_{\mathcal{R}}(\chi, \chi')$ where $\mathcal{R}_{\text{safe}}$ removes merge-prone edges.

**Feasibility for degree 5:** Medium. The restricted graph removes a larger fraction of edges (30.9% merge rate vs 17.4%), so the connectivity argument is harder.

### 7.2 Strategy B: Chain Topology Argument

Use planarity + non-interleaving to show that merge-prone $(a,5)$-chains are always "bypassable":

1. A merge-prone $(a,5)$-chain connects two non-adjacent neighbours of $v$ in $G - v$.
2. By planarity, this chain separates the plane into regions.
3. Show that $\{1,2,3,4\}$-swaps in one region can achieve the same BFS distance reduction.

**Feasibility:** Medium-High. This leverages the specific topology of planar graphs, which is the right approach for a 4CT-related result.

### 7.3 Strategy C: Induction on Path Length

Induct on the BFS distance $d$ from the current colouring to the target:
- Base: $d = 1$ (one swap to a 4-colouring). Show a safe swap exists.
- Step: If a safe path exists from distance $d-1$, show it can be extended from distance $d$.

**Feasibility:** Low-Medium. The inductive step is the hard part — we'd need to show that safe swap alternatives preserve BFS optimality, which is essentially the full conjecture.

### 7.4 Strategy D: Finite Case Analysis + Computation

For each of the finitely many colour types (2 structural types × specific non-adjacent pair assignments), computationally verify swap sufficiency at small $n$ and attempt to generalize.

**Feasibility:** High for computation, Medium for generalization. Works as a "pre-proof" that builds confidence and identifies any obstacle cases.

---

## 8. Computational Evidence Summary

From Agent 1210 (n ≤ 8):

| $n$ | Degree-5 $(a,5)$-swaps | Merge-prone | BFS avoided | Rate |
|-----|------------------------|-------------|-------------|------|
| 7 | 120 | 72 | 72 | 100% |
| 8 | 3,212 | 596 | 596 | 100% |
| **Total** | **3,332** | **668** | **668** | **100%** |

Chain size distribution for merge-prone chains at degree 5:

| Size | Fraction |
|------|----------|
| 1 | 73.6% |
| 2 | 25.3% |
| 3 | 1.1% |

Mean merge-prone chain size: 1.27. Merge-prone chains are overwhelmingly small, which supports the conjecture — small chains leave more "room" for alternative swaps.

---

## 9. Summary and Assessment

### Key Findings

1. **Two structural types** at degree 5: Type I (one pair) and Type II (two pairs). Both are merge-prone but with different geometries.

2. **Non-interleaving constrains but doesn't drive avoidance.** The main mechanism is the same as degree 4: $\{1,2,3,4\}$-swap sufficiency.

3. **Degree 5 is harder** due to higher merge rate (30.9% vs 17.4%), more complex link topology ($C_5$ vs $C_4$), and more chain interactions. But it has MORE safe alternatives (5 neighbours = more $\{1,2,3,4\}$-chains).

4. **The hardest sub-case** is Type II with large merge-prone chains for both repeated colours. This is where any proof would face the most resistance.

### Hardest Colour Types (ordered by difficulty)

| Rank | Type | Pattern | Why hard |
|------|------|---------|----------|
| 1 | II | $(a,a,b,b,c)$ with both pairs merge-prone | Double merge risk, most constrained |
| 2 | I | $(a,a,b,c,d)$ with pair merge-prone and large chains | Single merge risk but potentially blocking |
| 3 | I | $(a,a,b,c,d)$ with pair merge-prone and small chains | Easiest — small chains are easily bypassed |

### Proposed Proof Path

**Recommended strategy:** B (Chain Topology Argument) combined with D (Finite Case Analysis).

1. For each of the 3 Type II non-adjacent pair configurations (all equivalent by rotation), analyze the chain separation topology.
2. Show that the separating $(a,5)$-chain creates regions where $\{1,2,3,4\}$-swaps suffice.
3. Verify computationally at $n = 9, 10$.
4. If the argument holds for all finite configurations, attempt generalization via planarity + Jordan curve theorem.

### Risk Assessment

**Craftsperson:** The degree-5 analysis parallels degree 4. The non-interleaving property and chain separation give us structural tools. The computational evidence is overwhelming.

**Skeptic:** The 30.9% merge rate is almost double the degree-4 rate. "More alternatives" is hand-waving — we haven't shown these alternatives achieve the SAME BFS distance. The chain topology argument is a research program, not a proof. We might be underestimating the difficulty.

**Mover:** The degree-5 case uses the same mechanism as degree 4. A unified proof via $\{1,2,3,4\}$-swap sufficiency is more efficient than separate analyses. Focus on the restricted reconfiguration argument (Strategy A) as it's the most direct path.

---

*Agent 1520-M1-S2 — Degree-5 Case Analysis*  
*20 February 2026*
