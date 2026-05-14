# Multi-Vertex Interaction Analysis

**Agent:** 0050-M2-S3
**Date:** 18 February 2026
**Iteration:** 2

---

## Interference Radius — Formal Definition

**Definition.** For a proper 5-colouring $c$ of a planar graph $G$ and two vertices $v_i, v_j$ both coloured 5, define the **interference radius** $\rho(v_i, v_j, c)$ as the minimum over all colour pairs $(a, b) \subseteq \{1,2,3,4\}$ of the graph distance from $v_i$ to the nearest vertex in the $(a,b)$-Kempe chain containing $v_j$'s neighbourhood.

If $\rho(v_i, v_j, c) \geq 2$, then a Kempe swap at $v_j$ on the pair $(a,b)$ does not change any neighbour of $v_i$, and therefore $v_i$'s local configuration is preserved.

## Interference Radius — Computational Evidence

From M1's data, the CDL failure pattern shows:
- T_6_0 (6 vertices): failures occur when $v_i$ and $v_j$ are at distance 2 in the graph
- T_7_0 (7 vertices, degrees [3,3,4,4,4,6,6]): failures involve the degree-6 vertices, which are at distance 1 from many colour-5 vertices
- T_7_3 (degrees [3,4,4,4,5,5,5]), T_7_4 (degrees [4,4,4,4,4,5,5]): NO failures — more uniform degree means larger effective interference radius

**Observation:** Interference is bounded by $1/\delta_{\min}$ — in graphs where minimum degree is 4 or 5, Kempe chains are "thinner" (fewer vertices per chain component), reducing the chance of long-range interference.

## Chain Count Bound

**Proposition.** In a planar graph $G$, for any proper $k$-colouring $c$ and colour pair $(a,b)$, the number of $(a,b)$-Kempe chains is at most $n/2$ (since each chain contains at least 2 vertices: one coloured $a$, one coloured $b$, though chains can have 1 vertex if a colour appears isolated from the other).

Actually: a Kempe chain is a maximal connected component of the subgraph induced on vertices coloured $a$ or $b$. It can have just 1 vertex (if that vertex has no neighbours coloured $a$ or $b$). The number of chains is at most the number of vertices coloured $a$ or $b$.

**Planar bound:** Each $(a,b)$-chain induces a connected subgraph of $G$, which has a spanning tree. In a planar graph, the total number of edges in all chains is at most $3n - 6$. This limits how "interconnected" the chains can be.

## The "Never Revert to 5" Lemma

**Lemma (Trivial but Crucial).** A Kempe swap on colour pair $(a,b)$ with $a, b \in \{1,2,3,4\}$ never changes any vertex's colour to 5 or from 5.

**Proof.** A Kempe swap on $(a,b)$ only changes vertices in an $(a,b)$-chain, which by definition only contains vertices coloured $a$ or $b$. Vertices coloured 5 are not in any $(a,b)$-chain for $a, b \in \{1,2,3,4\}$, so they are unchanged. Vertices in the chain switch between $a$ and $b$, both of which are in $\{1,2,3,4\}$.

**Corollary.** If a vertex has been recoloured from 5 to some $c \in \{1,2,3,4\}$, no subsequent Kempe swap on pairs within $\{1,2,3,4\}$ will ever revert it to 5.

## Multi-Vertex Cascade Analysis

When we perform an unrestricted Kempe swap to help recolour vertex $v_j$ (coloured 5):
1. The swap changes some vertices' colours from $a$ to $b$ and vice versa
2. Previously recoloured vertices may change colour (e.g., $v_i$ from 1 to 2)
3. But they NEVER revert to 5
4. The set of colour-5 vertices is monotonically shrinking or stable

**Question:** Can the set of colour-5 vertices GROW after a Kempe swap on $(a,b) \subseteq \{1,2,3,4\}$?

**Answer:** NO. By the Never-Revert Lemma, no vertex gains colour 5 from such a swap. And the swap doesn't change colour-5 vertices. So $|V_5|$ is non-increasing under swaps on $\{1,2,3,4\}$ pairs.

**But:** We also need swaps involving colour 5 — i.e., $(5,x)$-swaps — to potentially help. A $(5,x)$-swap would change some colour-5 vertices to colour $x$ and some colour-$x$ vertices to 5. This INCREASES $|V_5|$ at some vertices while decreasing at others.

For the sequential elimination strategy, we DON'T use $(5,x)$-swaps. We only use swaps on pairs from $\{1,2,3,4\}$. So $|V_5|$ is non-increasing.

**This means sequential elimination with swaps on $\{1,2,3,4\}$ only is monotone:** each successful recolouring decreases $|V_5|$ by 1, and swaps never increase it. 

## Formalized Elimination Theorem (Partial)

**Theorem (Partial).** Let $G$ be a planar triangulation with proper 5-colouring $c$, and let $V_5 = \{v : c(v) = 5\}$. Suppose every vertex in $V_5$ has degree $\leq 5$. Then there exists a sequence of at most $|V_5|$ Kempe swaps on pairs from $\{1,2,3,4\}$, followed by direct recolourings, that produces a proper 4-colouring.

**Proof sketch:**
1. Pick any $v \in V_5$. By the degree-5 classification (iteration 1), there exists a Kempe swap on some pair $(a,b) \subseteq \{1,2,3,4\}$ that frees a colour for $v$. (The classification allows $(a,b)$ involving any colours in $\{1,2,3,4\}$, including the colours of previously recoloured vertices — this is the unrestricted case.)
2. Perform the swap. By the Never-Revert Lemma, no vertex returns to colour 5.
3. Recolour $v$ from 5 to the freed colour. Now $|V_5|$ decreases by 1.
4. Repeat until $V_5 = \emptyset$.

**Gap:** Step 1 requires degree $\leq 5$ for the vertex being processed. If all remaining colour-5 vertices have degree $\geq 6$, the classification doesn't apply.

## Closing the Degree Gap

**Approach 1: Process minimum-degree-first.**
At each step, choose $v \in V_5$ with minimum degree. In a planar graph, $\sum_v \deg(v) = 2|E| \leq 2(3n-6) = 6n-12$, so average degree < 6. There must be vertices of degree $\leq 5$. But are any of them coloured 5?

Not necessarily. After several swaps, the colour-5 vertices might all be high-degree.

**Approach 2: Swap to move colour 5 to low-degree vertices.**
Before processing, use $(a,b)$-swaps (with $a,b \in \{1,2,3,4\}$) to change the landscape so that colour 5 appears at low-degree vertices. But these swaps don't change colour-5 vertices at all! The $(a,b)$-swaps only affect vertices coloured $a$ or $b$.

**Approach 3: Use the full R(G,5) structure.**
Instead of sequential elimination, simply observe that BFS in $\mathcal{R}(G,5)$ finds a 4-colouring at distance $\leq n-4$ (conjectured from data). This bypasses the local argument entirely.

**Assessment:** The degree gap is a real obstacle for the sequential approach but irrelevant for the distance-in-R(G,5) approach. Recommend pivoting to the distance bound.

---

*0050-M2-S3 — 18 February 2026*
