# Alternative Proof Architectures

**Agent:** 0050-M2-S3
**Date:** 18 February 2026
**Iteration:** 2

---

## Architecture Comparison

The CDL disproval forces a rethinking of Plan 2's proof structure. Three alternative architectures are analyzed.

---

## Alt A: Bounded Distance in R(G,5)

### Statement
For any planar triangulation $G$ on $n$ vertices and any proper 5-colouring $c$, there exists a proper 4-colouring $c'$ such that $d_{\mathcal{R}(G,5)}(c, c') \leq n - 4$.

### Why This Works as a Proof Architecture
If proven, this directly implies 4CT:
1. Every planar graph is 5-colourable (Five Colour Theorem)
2. From any 5-colouring, reach a 4-colouring in $\leq n-4$ Kempe swaps
3. Therefore every planar graph is 4-colourable

This is a non-constructive existence proof (we know a path exists, not which one) but with an explicit bound.

### Proof Approaches

**Induction on n:** Remove a vertex $v$ of degree $\leq 5$. By induction, the remaining graph has a 4-colouring reachable from any 5-colouring in $\leq (n-1) - 4 = n-5$ swaps. Add $v$ back, 5-colour it, then use $\leq 1$ more swap. Total: $\leq n - 4$.

**Gap in this approach:** Adding $v$ back requires that the 4-colouring of $G - v$ extends to a 5-colouring of $G$ (trivially, since $\deg(v) \leq 5$ and we have 5 colours), and then we need one more swap to eliminate the new colour-5 vertex. But the existing 4-colouring of $G-v$ becomes a partial colouring of $G$ after adding $v$. The swap needed for $v$ might disrupt the 4-colouring of $G-v$... but by the Never-Revert Lemma, no vertex goes back to colour 5. So we'd need the disrupted colouring to still be a 4-colouring.

Actually: after the swap, the colouring uses colours from $\{1,2,3,4,5\}$, with $v$ now using a colour from $\{1,2,3,4\}$. The only remaining colour-5 vertices are those that were coloured 5 before (none, since the induction gave a 4-colouring of $G-v$ and $v$ was the only new colour-5 vertex).

Wait — the induction gives a 4-colouring of $G-v$. We then colour $v$ with colour 5 (or with a free colour from $\{1,2,3,4\}$ if available). If $v$ gets a free colour, we're done (distance 0 for this step). If $v$ must be coloured 5, we need 1 swap to eliminate it. This swap uses colours from $\{1,2,3,4\}$ and might change other vertices' colours within $\{1,2,3,4\}$ — but none go to 5.

**THIS ARGUMENT WORKS** if we can show the single-vertex recolouring from the degree-5 classification applies. The vertex $v$ has degree $\leq 5$, so the classification guarantees a freeing swap. Total distance: at most $n - 4$ by induction.

**POTENTIAL THEOREM:**

**Theorem.** For any planar triangulation $G$ on $n \geq 4$ vertices and any proper 5-colouring $c$, there exists a proper 4-colouring $c'$ with $d_{\mathcal{R}(G,5)}(c, c') \leq n - 4$.

**Proof by strong induction on $n$.**

Base: $n = 4$ ($K_4$). Every proper 5-colouring of $K_4$ uses at most 4 colours (since $K_4$ has only 4 vertices and no colour appears more than once, but with 5 colours available, some colour may be unused). Actually, $K_4$ has $\binom{5}{4} \cdot 4! = 120$ proper 5-colourings, all using exactly 4 colours. Distance = 0. Bound: $n - 4 = 0$. CHECK.

Induction: Assume the theorem holds for all planar triangulations on $< n$ vertices. Let $G$ have $n$ vertices.

Step 1: $G$ has a vertex $v$ of degree $\leq 5$ (every planar graph does).

Step 2: Consider $G' = G - v$ (not necessarily a triangulation, but planar). Actually for the induction to work cleanly, we may need to triangulate $G'$... This gets complicated if $G - v$ isn't a triangulation.

**Refinement needed:** The induction should work with planar GRAPHS, not just triangulations. Or we need a different base structure.

### Assessment: Medium-High feasibility

The inductive argument is ALMOST complete. The gap is in ensuring that the sub-problem ($G - v$) is itself a triangulation (or that the argument extends to non-triangulations). If we prove it for all planar graphs (not just triangulations), this gap disappears.

---

## Alt B: Unrestricted Swaps with Damage Repair

### Statement
For any planar graph $G$ with proper 5-colouring $c$:
1. Pick any vertex $v$ coloured 5
2. Use any Kempe swap to free a colour for $v$
3. Recolour $v$
4. The "damage" (other vertices changed colour) is automatically OK because the Never-Revert Lemma ensures no vertex goes back to 5

### Analysis
This is essentially Strategy A from the proof_strategies.md document. The key insight is that "damage repair" is UNNECESSARY because:
- Swaps on $\{1,2,3,4\}$ pairs never produce colour 5
- So the set of colour-5 vertices can only shrink
- Each step removes one colour-5 vertex
- After $|V_5|$ steps, we have a 4-colouring

The only gap is the degree-5 requirement: the vertex being processed must have degree $\leq 5$ for the classification to guarantee a freeing swap exists.

### When Does the Degree Gap Bite?

In a 5-colouring of a planar graph, the vertices coloured 5 could ALL have degree $\geq 6$. Example: take a planar triangulation with $n = 100$ where 10 vertices have degree 8 and are all coloured 5. The degree-5 classification doesn't apply to any of them.

**However:** In the greedy sequential approach, we have FREEDOM to choose WHICH vertex to process first. If there's a colour-5 vertex of degree $\leq 5$, process it. If not... we're stuck with the current approach.

**Key question:** In a proper 5-colouring of a planar graph, must there exist a vertex coloured 5 with degree $\leq 5$?

**Answer: NO.** Consider a planar graph where the subgraph induced on "high-degree" vertices can be 4-coloured, and the remaining "low-degree" vertices are coloured with $\{1,2,3,4\}$. Then colour-5 vertices are exactly the high-degree vertices.

**But:** After some Kempe swaps, colour 5 might "move" to lower-degree vertices. We don't directly swap colour 5 (we only swap pairs from $\{1,2,3,4\}$), so colour-5 vertices are FIXED. They never change. This means the degree-5 gap is real.

### Assessment: Medium for degree-5 vertices, unresolved for general case

---

## Alt C: Fisk Homology Connection

### Statement
All 4-colourings of a sphere triangulation are in one Fisk class. Can this help?

### Analysis
Fisk's theorem (1977) shows that for a triangulation of the 2-sphere, any two proper 4-colourings are connected by Kempe swaps. The proof uses the $\mathbb{Z}_2$-homology of the colouring complex.

**Relevance to 5→4 reduction:** Fisk tells us about the STRUCTURE of the 4-colouring space. Every 4-colouring is equivalent (reachable from every other). So the "target" for our reduction is a single connected component of $\mathcal{R}(G,4) \subseteq \mathcal{R}(G,5)$.

**Possible use:** If we can show that the 4-colouring component of $\mathcal{R}(G,5)$ is "large" (has large neighbourhood in $\mathcal{R}(G,5)$), then any 5-colouring is close to a 4-colouring.

**Quantitative version:** The 4-colourings form a connected subgraph $\mathcal{R}_4$ of $\mathcal{R}(G,5)$. The boundary $\partial \mathcal{R}_4$ (5-colourings adjacent to a 4-colouring) has size proportional to $|\mathcal{R}_4|$. If $\mathcal{R}(G,5)$ is connected and $\mathcal{R}_4$ is large relative to $|\mathcal{R}(G,5)|$, then expansion properties might bound the max distance.

**Problem:** We don't know the expansion constant of $\mathcal{R}(G,5)$ for general planar graphs. This approach would need graph-theoretic results about reconfiguration graph expansion.

### Assessment: Low feasibility (too abstract, insufficient tools)

---

## Comparison and Recommendation

| Architecture | Feasibility | Gap | Would Prove |
|-------------|-------------|-----|-------------|
| Alt A (distance bound) | **Medium-High** | G-v may not be a triangulation | Constructive 4CT with explicit bound |
| Alt B (unrestricted + no repair) | Medium | Degree-5 requirement | Constructive 4CT for deg-5 coloured-5 vertices |
| Alt C (Fisk expansion) | Low | Need expansion bounds | Non-constructive 4CT |

**Recommendation: Alt A is the most promising.** The inductive argument is nearly complete. The gap (G-v triangulation) can likely be handled by:
1. Working with all planar graphs (not just triangulations)
2. Or by retriangulating $G-v$ and showing this doesn't affect the argument

Alt B is the "applied" version: it describes the actual ALGORITHM that M1's data shows works. Alt A is the "structural" version: it bounds the distance without specifying the path.

**Combined approach:** Use Alt B's Never-Revert insight to justify the algorithm, and Alt A's induction to bound the distance. The degree-5 gap in Alt B is automatically handled by Alt A's induction (since the vertex we remove has degree $\leq 5$).

---

*0050-M2-S3 — 18 February 2026*
