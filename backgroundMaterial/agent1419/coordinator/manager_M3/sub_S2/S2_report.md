# M3-S2 Report: Confinement Factoring + Chain Size Bound

**Agent:** 1419-M3-S2
**Status:** COMPLETE — Partial results with key open question

## Approach C: Confinement Factoring

### Theorem B (Confinement) recap
In a planar graph, for disjoint colour pairs $\{a,b\}$ and $\{c,d\}$, the $(a,b)$-Kempe chains and $(c,d)$-Kempe chains do not interleave in the planar embedding. This limits how chains can "wrap around" each other.

### Application to safe path existence

**Claim:** If an $(a,5)$-chain $K$ adjacent to $v$ is merge-prone, confinement constrains the topology enough that an alternative safe swap must exist.

**Argument:**

Let $v$ have degree $\leq 5$ with $c(v) = 5$. Consider the merge-prone situation: $v$ has neighbours $u_i, u_j$ coloured $a$, in distinct $(a,5)$-chains $K_i, K_j$ in $G-v$.

By planarity, the bichromatic subgraph $B_{a,5}(G-v)$ is planar. The chains $K_i$ and $K_j$ are connected components of $B_{a,5}(G-v)$.

**Key observation:** $K_i$ and $K_j$ are separated by $v$ (since $v$ is removed and adding $v$ back would merge them). In the planar embedding of $G-v$, $K_i$ and $K_j$ are "nearly adjacent" — they would be connected through $v$.

Now consider the reconfiguration graph $R(G-v, 5)$. At the current colouring, swapping $K_i$ or $K_j$ is unsafe. But other swaps are available:

1. **Swap a different $(a,5)$-chain** $K'$ not adjacent to $v$: This is safe. By planarity, such chains exist whenever $B_{a,5}$ has components beyond $K_i, K_j$ in the neighbourhood of $v$.

2. **Swap a $(b,5)$-chain** for $b \neq a$: This changes colour 5 vertices but not in the $(a,5)$ subgraph. It may create new reduction paths.

3. **Swap a $\{b,c\}$-chain** for $b,c \in \{1,2,3,4\}$: Safe by definition (Never-Revert lemma). Rearranges colours 1-4 without affecting colour 5 vertices.

**The question is:** Does at least one of these alternatives advance toward a 4-colouring?

### Analysis of why the 1-step detour works

In the counterexample at n=9, the optimal path has distance 2. The safe path has distance 3. What happens in the extra step?

**Hypothesis:** The safe path takes a "preparatory swap" — a $\{b,c\}$-swap or safe $(a,5)$-swap that rearranges the colouring so that at the NEXT step, the merge-prone chain is no longer merge-prone (or a different reduction path opens up).

This is consistent with the data: the alternative swap classification shows safe $(a,5)$-swaps (not adjacent to $v$) are used, not $\{1,2,3,4\}$-swaps.

### Confinement argument for safe detour existence

**Theorem attempt:** In a planar graph, if $(a,5)$-chains $K_i$ and $K_j$ are separated by $v$, then there exists an $(a,5)$-chain $K'$ with:
- $K' \neq K_i$ and $K' \neq K_j$
- $K'$ is not adjacent to any neighbour of $v$
- Swapping $K'$ produces a colouring from which a safe optimal path exists

**Status:** NOT PROVED. The existence of $K'$ is verified computationally but the planarity argument is incomplete. The key difficulty is: what if $K_i \cup K_j$ constitutes ALL of $B_{a,5}(G-v)$? Then no $K'$ exists for colour $a$.

In that case, we'd need to use a different colour pair or a $\{b,c\}$-swap.

## Approach D: Chain Size Bound

### Computational evidence

From M1 data across n=6,7,8:
- Mean merge-prone chain size: 1.27 vertices
- Max observed: 3 vertices
- 72% are single vertices

### Why small chains matter

If merge-prone chains are small (size $\leq s$), they affect a bounded region of the graph. The rest of $B_{a,5}(G-v)$ is unaffected. This means:

1. The reconfiguration graph has high local connectivity around the current colouring
2. Many alternative paths exist that route around the small merge-prone region
3. The probability of ALL paths being forced through the merge-prone chain decreases exponentially with the number of available alternatives

### Size bound attempt

**Claim:** Merge-prone $(a,5)$-chains adjacent to $v$ have size $\leq n/3$.

**Proof attempt:**
- A merge-prone chain touches $v$'s neighbourhood at 2+ points
- By planarity, the chain lies in the planar embedding near $v$
- The chain is bounded by the "wedge" between two paths from $v$'s neighbours
- In a triangulation, this wedge contains at most $O(n)$ vertices

This is too weak — we need a CONSTANT bound (like $\leq 3$) to be useful.

**Revised claim:** Merge-prone chains at degree-4 vertices have size $\leq 1$ (single vertices).

**Evidence:** At degree 4, merge-prone requires opposite pairs in $C_4$. Opposite neighbours are not adjacent, so if both are coloured $a$, each forms its own chain of size $\geq 1$. The chain might extend, but the degree-4 constraint limits extension. Data shows degree-4 merge-prone chains are predominantly single vertices.

**Status:** Evidence strong at degree 4, weaker at degree 5 where chains can reach size 3.

## Combined verdict

Neither Approach C nor Approach D yields a complete proof. But together they provide:
1. **Confinement** limits where chains can go (topology)
2. **Size bounds** limit how large problematic chains are (combinatorics)
3. **Together:** the merge-prone region is small and topologically constrained, leaving room for safe alternatives

The gap: translating "leaves room" into a formal existence proof for safe paths.

## Self-Assessment (Tripartite)

**Craftsperson:** The confinement framework is sound. Planarity genuinely constrains chain topology. The size bound data is robust. The combined approach is the strongest path to a proof.

**Skeptic:** "Leaves room" is not a proof. Every argument here has a gap: the existence of $K'$ in Approach C, the constant bound in Approach D, and the translation from "room exists" to "safe path exists." The counterexamples at n=9 show that "room" doesn't guarantee optimal paths; can we guarantee ANY path?

**Mover:** The proof isn't done, but the ingredients are identified. Recommend: (1) prove the constant chain size bound formally at degree 4, (2) use it to show safe alternatives exist by explicit construction, (3) handle degree 5 separately. This is a 3-month research programme, not a 1-hour proof.
