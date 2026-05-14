# Colour Elimination Lemma — Proof Attempt and Obstacle Analysis

**Agent:** 0050-M2-S3
**Date:** 18 February 2026

---

## Lemma Statement

**Colour Elimination Lemma.** Let $G$ be a planar graph with a proper 5-colouring $c$. Let $V_5 = \{v_1, \ldots, v_k\}$ be the set of vertices coloured 5. Then there exists an ordering of $V_5$ and a sequence of Kempe swaps such that each $v_i$ can be recoloured to $\{1,2,3,4\}$ using swaps that do not change the colours of $v_1, \ldots, v_{i-1}$.

If true, this immediately gives a constructive proof of the Four Colour Theorem:
1. Start with any proper 5-colouring (exists by the Five Colour Theorem)
2. Apply the Colour Elimination Lemma to eliminate colour 5
3. The result is a proper 4-colouring

## Proof Strategy

### Approach: Greedy Sequential Elimination

Process vertices of $V_5$ one at a time. At each step:
1. Pick a vertex $v_i$ coloured 5
2. Use Kempe swaps involving colours $\{1,2,3,4\}$ to free a colour for $v_i$
3. Recolour $v_i$ to the freed colour
4. Ensure swaps in step 2 don't affect previously recoloured vertices

### What We Have

From Theorems A and B and the degree-5 classification:
- **Theorem A:** Kempe chains for disjoint colour pairs don't interleave at external vertices
- **Theorem B:** Swaps on $\{c,d\}$ (with $\{c,d\} \cap \{a,b\} = \emptyset$) preserve the $(a,b)$-chain structure
- **Classification:** At any single degree-5 vertex, a freeing swap always exists

### Step-by-Step Attempt

**Step 1:** Choose any $v_1 \in V_5$. Since $v_1$ has degree $\leq 5$ (by the 6-colour bound on planar graphs, actually degree $\leq$ anything but typically $\leq 5$ for the hard cases), free a colour using a Kempe swap and recolour $v_1$ to some colour $c(v_1) \in \{1,2,3,4\}$.

**Step 2:** Choose $v_2 \in V_5 \setminus \{v_1\}$. Now $v_2$ is still coloured 5. We need a Kempe swap that frees a colour for $v_2$ without recolouring $v_1$ back to 5.

**The Obstacle:** The Kempe swap for $v_2$ involves swapping colours on a Kempe chain. This chain might include $v_1$. If $v_1$ is in the chain, the swap changes $v_1$'s colour.

### Detailed Obstacle Analysis

Suppose $v_1$ was recoloured to colour 1 (from colour 5). Now for $v_2$, we consider Kempe swaps on chains involving colours from $\{1,2,3,4\}$.

**Safe swaps** (by Theorem B): swaps on colour pairs NOT involving colour 1. These are:
- $(2,3)$-swaps
- $(2,4)$-swaps
- $(3,4)$-swaps

These swaps cannot change $v_1$'s colour (since $v_1$ is coloured 1 and the swaps don't involve colour 1).

**Unsafe swaps:** swaps involving colour 1:
- $(1,2)$-swaps might change $v_1$ from 1 to 2
- $(1,3)$-swaps might change $v_1$ from 1 to 3
- $(1,4)$-swaps might change $v_1$ from 1 to 4

(These don't change $v_1$ back to 5, but they DO change $v_1$'s colour, potentially creating new conflicts for future steps.)

**Question:** Can we always free a colour for $v_2$ using ONLY safe swaps?

### Analysis of the Restricted Problem

At $v_2$ (degree $\leq 5$, coloured 5), the neighbours have colours from $\{1,2,3,4\}$. From the degree-5 classification, we need to free one of these colours. The question is whether we can do so using only swaps on pairs from $\{2,3,4\}$ (avoiding colour 1, which is $v_1$'s colour).

**Subcase 2a:** If some colour $c \in \{2,3,4\}$ is not used by any neighbour of $v_2$, we can recolour $v_2$ to $c$ without any swaps. Done.

**Subcase 2b:** If colours $\{2,3,4\}$ are all used by neighbours of $v_2$, but colour 1 is not used: recolour $v_2$ to 1. Done (but this might conflict if $v_1$ is adjacent to $v_2$... but $v_1$ and $v_2$ can't both be coloured 1 if they're adjacent. Since $v_2$ is currently coloured 5 ≠ 1 = $c(v_1)$, and we'd recolour $v_2$ to 1, this works only if $v_1$ and $v_2$ are not adjacent. If they ARE adjacent, colour 1 is already used by a neighbour of $v_2$.)

**Subcase 2c:** All of $\{1,2,3,4\}$ are used by neighbours of $v_2$. We need a Kempe swap to free a colour. Can we free a colour from $\{2,3,4\}$ using swaps on pairs from $\{2,3,4\}$?

Consider freeing colour 2. We'd need to change some neighbour from 2 to another colour. A $(2,3)$-swap on the chain containing that neighbour would change it from 2 to 3 (but then the neighbour might conflict with another neighbour coloured 3). But by the swap-preserves-properness property, the result is always a proper colouring.

The key question: after the swap, is colour 2 freed from $v_2$'s neighbourhood? This depends on whether the swap moves the colour-2 neighbour out of the neighbourhood (it doesn't — the vertex is still there, just differently coloured) and whether it introduces colour 2 at another neighbour (it might, if another neighbour coloured 3 is in the same chain).

**This is exactly the degree-5 analysis, but restricted to "safe" swaps.** The question becomes: is the restricted set of swaps (avoiding $v_1$'s colour) always sufficient?

## The Core Obstruction

**Claim (Speculative):** The restricted swap set is NOT always sufficient for a single vertex in isolation. The classification shows that some cases require a $(1, x)$-swap (involving colour 1), and if we're forbidden from such swaps, we're stuck.

**Example scenario:** At $v_2$ with neighbours coloured $(1, 2, 3, 1, 4)$. We want to free colour 2 (the only singleton colour from $\{2,3,4\}$). The $(2,3)$-chain of the colour-2 neighbour also contains the colour-3 neighbour (they're in the same chain since they're adjacent on $C_5$). Swapping: colours swap, but colour 2 moves to another position. The $(2,4)$-chain might similarly fail.

However, a $(1,2)$-swap on a chain containing one of the colour-1 neighbours could free colour 1 or 2 — but this swap involves colour 1, which is "unsafe" (changes $v_1$'s colour).

**This is the fundamental obstacle.** There may be configurations at $v_2$ where the only freeing swaps involve the "protected" colour of $v_1$.

## Potential Resolutions

### Resolution Attempt 1: Graph Distance Argument

If $v_1$ and $v_2$ are far apart in the graph (distance $\geq 3$, say), then any Kempe chain that includes $v_1$ is unlikely to also reach $v_2$'s neighbourhood. In this case, a swap at $v_2$ involving colour 1 would NOT actually include $v_1$ (they'd be in different (1,x)-chains), so the swap is safe.

**Formalization:** If the $(1, x)$-chain containing $v_2$'s neighbour does not include $v_1$, then swapping that chain doesn't affect $v_1$.

This works when $v_1$ and $v_2$ are in different (1,x)-chains for the relevant colour pair. The question is: can we always find a pair $(1,x)$ where this holds?

**Obstacle within this approach:** In a small or highly connected graph, all $(1,x)$-chains might pass through $v_1$. This is exactly the case where "chain interference" is the issue.

### Resolution Attempt 2: Ordering by Kempe Chain Structure

Choose the ordering $v_1, v_2, \ldots, v_k$ such that each $v_i$ is "far" from $\{v_1, \ldots, v_{i-1}\}$ in terms of Kempe chain connectivity. Specifically, process vertices in an order where each new vertex can be freed using swaps that don't reach any previously processed vertex.

This requires understanding the structure of "Kempe interference": when does a swap at $v_i$ "reach" $v_j$ via a Kempe chain?

### Resolution Attempt 3: Multi-Step Recolouring

Instead of a single swap per vertex, use a SEQUENCE of swaps. First do safe swaps to rearrange the colour landscape around $v_2$, then do the final freeing swap. Theorem B guarantees that certain barriers are preserved.

For example:
1. Do a $(3,4)$-swap to change the chain topology around $v_2$ (this is safe — doesn't affect colour 1)
2. In the new colouring, the $(1,2)$-chain from $v_2$'s neighbourhood might no longer include $v_1$
3. Now do the $(1,2)$-swap safely

This "preparatory swap" strategy is promising but requires proving that such a preparation always exists.

## What Additional Lemma Would Suffice

**The Missing Lemma:** For any proper 5-colouring of a planar graph and any two vertices $v_1, v_2$ coloured 5: either
(a) $v_2$ can be recoloured using swaps that avoid $v_1$'s Kempe chains, OR
(b) a preparatory sequence of safe swaps exists that "disconnects" $v_1$ from $v_2$'s relevant chains

More precisely:

**Chain Disconnection Lemma (Conjectured).** Let $v_1$ be coloured $c_1 \in \{1,2,3,4\}$ and $v_2$ be coloured 5. For at least one colour $x \in \{1,2,3,4\} \setminus \{c_1\}$, there exists a sequence of Kempe swaps on pairs from $\{1,2,3,4\} \setminus \{c_1\}$ (safe swaps) such that afterwards, the $(c_1, x)$-Kempe chain containing $v_2$'s colour-$c_1$ neighbour does NOT include $v_1$.

If this lemma held, the proof would proceed:
1. Apply the safe preparatory swaps
2. Now the $(c_1, x)$-swap at $v_2$ is safe (doesn't reach $v_1$)
3. Perform the swap to free a colour for $v_2$

## Computational Evidence

From M1's data (n ≤ 6):
- **All 5-colourings reduce to 4-colourings via Kempe swaps** (confirmed by BFS)
- **Maximum path length for octahedron: 2 swaps** (very short)
- No cases found where the sequential elimination strategy fails

This suggests the Colour Elimination Lemma is true, but the proof may require subtle structural arguments about planar Kempe chains.

## Feasibility Assessment

**Medium-Low for a complete proof.** The single-vertex analysis is clean. The multi-vertex interaction is where the fundamental difficulty lies. The "Chain Disconnection Lemma" is a precise formulation of the missing piece, but proving it requires deep understanding of how safe swaps reconfigure the Kempe chain landscape.

**Medium-High for identifying the exact obstruction.** We have pinpointed the obstacle: it's the question of whether safe swaps (avoiding one protected colour) always suffice to disconnect a vertex from the "dangerous" Kempe chain. This is a well-defined mathematical question that could be attacked combinatorially.

## Concrete Next Steps

1. **Computationally test the Chain Disconnection Lemma** for all triangulations on $n \leq 8$
2. **Study the Kempe chain graph** on $\{2,3,4\}$-swaps: what does the reconfiguration look like when restricted to safe swaps?
3. **Look for structural induction:** process vertices in a specific order related to the triangulation structure (e.g., reverse of a shelling order, or a BFS order from the boundary)
4. **Consider a weaker claim:** instead of sequential elimination, show that a GLOBAL sequence of swaps (possibly revisiting vertices) always works — then use the R(G,5) connectivity to argue existence

---

*0050-M2-S3 — 18 February 2026*
