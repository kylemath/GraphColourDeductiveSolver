# Chain Disconnection Lemma — Formal Statement and Analysis

**Agent:** 0050-M2-S1
**Date:** 18 February 2026
**Iteration:** 2

---

## STATUS: DISPROVED (Strict Form)

M1's computational data has DISPROVED the strict Chain Disconnection Lemma. The data shows that safe-swaps-only (avoiding one protected colour) is insufficient starting at n=6, even with 5 preparatory swaps.

This document reformulates the question in light of this evidence.

---

## Original Conjecture (DISPROVED)

**Chain Disconnection Lemma (Strict).** Let $G$ be a planar triangulation with a proper 5-colouring $c$. Let $v_1$ be coloured $c_1 \in \{1,2,3,4\}$ and $v_2$ be coloured 5. Then for at least one colour $x \in \{1,2,3,4\} \setminus \{c_1\}$, there exists a sequence of Kempe swaps on pairs from $\{1,2,3,4\} \setminus \{c_1\}$ such that afterwards, the $(c_1, x)$-Kempe chain containing $v_2$'s colour-$c_1$ neighbour does NOT include $v_1$.

**Counterexample:** T_6_0 (the first 6-vertex triangulation), multiple 5-colourings. 48 vertex pairs (v,w) where no safe-swap sequence of any length disconnects the chain.

---

## Reformulated Conjectures

Given that the strict CDL fails, we pivot to three alternative formulations:

### Conjecture A: Unrestricted Sequential Elimination (Computational)

**Conjecture.** Let $G$ be a planar triangulation with proper 5-colouring $c$ and let $V_5$ be the set of vertices coloured 5. There exists an ordering of $V_5$ and a sequence of Kempe swaps such that each vertex in $V_5$ can be recoloured from 5 to some colour in $\{1,2,3,4\}$, resulting in a proper 4-colouring. The swaps need not avoid any previously assigned colours.

**Status:** Computationally verified for all triangulations on $n \leq 8$ (over 45,000 orderings tested with 0 failures). Unrestricted elimination succeeds for EVERY ordering tested, not just some orderings.

**Assessment:** Medium-High feasibility. The lack of any restriction makes this more likely to be true (and provable) than the strict CDL.

### Conjecture B: Linear Distance Bound

**Conjecture.** For any planar triangulation $G$ on $n$ vertices and any proper 5-colouring $c$, there exists a proper 4-colouring $c'$ such that $d_{\mathcal{R}(G,5)}(c, c') \leq n - 4$.

**Computational evidence:**

| $n$ | Max distance observed | Bound $n-4$ | Tight? |
|-----|----------------------|-------------|--------|
| 4   | 0                    | 0           | Yes    |
| 5   | 1                    | 1           | Yes    |
| 6   | 2                    | 2           | Yes    |
| 7   | 3                    | 3           | Yes    |
| 8   | 4                    | 4           | Yes    |

The bound appears TIGHT for $n = 4, \ldots, 8$. This is striking.

**Interpretation:** The number of Kempe swaps needed equals the number of "excess" vertices beyond 4 (the minimum for which 4-colouring is guaranteed). Each swap effectively "handles" one vertex's worth of colouring complexity.

**Assessment:** Medium feasibility. The tightness is suspicious — it could be coincidence at small $n$ or a deep structural fact. Proving this would immediately give a constructive 4CT proof with explicit swap bound.

### Conjecture C: Universal Unrestricted Success

**Conjecture.** For any planar triangulation $G$ on $n$ vertices, any proper 5-colouring $c$, and any ordering of the colour-5 vertices, unrestricted greedy sequential elimination always succeeds.

**Status:** Computationally verified for all orderings tested at $n \leq 8$.

**Assessment:** Medium-Low feasibility for proof. This is strictly stronger than Conjecture A (which only needs one ordering to work). If true, it would follow from a local argument — at each step, some swap always exists.

---

## Why the Strict CDL Fails — Structural Analysis

The failure occurs in graphs with degree-3 vertices adjacent to high-degree vertices (e.g., T_6_0 has degree sequence [3,3,4,4,4,4] for $K_{2,2,2}$ vs T_6_1's [3,3,4,4,4,4] — actually both n=6 triangulations have the same degree-count profile but different structure).

The obstruction mechanism: when $v_1$ is coloured $c_1$ and $v_2$ is coloured 5, and all four colours appear in $v_2$'s neighbourhood, the $(c_1, x)$-chains for ALL $x$ may pass through $v_1$. In a small graph with high connectivity, there's no "room" for the chains to route around $v_1$. Safe swaps (avoiding $c_1$) rearrange the $\{2,3,4\}$-chain landscape but cannot sever the connection between $v_1$ and $v_2$ through colour-$c_1$ chains.

**Key insight:** The obstruction is topological, not combinatorial. In a planar graph, chains must form paths/trees in the dual. When the dual graph is small enough, all $(c_1, x)$-chains are connected.

---

## Next Steps

1. Focus on Conjecture B (linear distance bound) — this has the strongest evidence and clearest path to proof
2. Explore whether the distance = n-4 bound follows from an inductive argument on vertex count
3. Study the "hardest" colourings (those at max distance) — what structural property makes them hard?

---

*0050-M2-S1 — 18 February 2026*
