# M3-S3 Report: Degree-5 Specific Analysis

**Agent:** 1419-M3-S3
**Status:** COMPLETE — Degree 5 confirmed as the harder case

## Why Degree 5 is Different

### Structural differences (C_5 vs C_4 link)

| Property | Degree 4 (C_4 link) | Degree 5 (C_5 link) |
|----------|---------------------|---------------------|
| Non-adjacent pairs | 2 (opposite pairs) | 5 pairs |
| Merge-prone rate | 10.6% at n=9 | 22.8% at n=9 |
| Counterexample CEs | T_9_35 v=6 (24 CEs) | T_9_25 v=3 (24 CEs) |
| Chain size range | [1, 2] observed | [1, 3] observed |
| Non-interleaving constraint | Strong (only 2 arrangements) | Weaker (5 arrangements) |

The C_5 link has 5 non-adjacent pairs vs 2 for C_4. This means:
- More configurations can be merge-prone
- Non-interleaving provides weaker constraints
- The "bottleneck" topology that forces unsafe swaps has more room to emerge

### Analysis of T_9_25 (degree-5 counterexample)

Graph structure:
```
Vertex 0 (deg 7): hub, connected to all except 1
Vertex 3 (deg 5, counterexample vertex): connected to 0,1,2,4,6
Link of v=3: {0,1,2,4,6} — should form C_5
Adjacency: 0-1? No. 0-2? Yes. 0-4? Yes. 0-6? Yes. 1-2? Yes. 1-4? Yes. 2-6? Yes. 4-6? No.
```

Actually checking: the neighbours of v=3 are {0,1,2,4,6}.
- 0-1: not directly in the edge list... wait, 0 connects to [2,3,4,5,6,7,8], so 0-1 is NOT an edge.
- 1-2: 1 connects to [2,3,4,5], so YES
- 2-6: 2 connects to [0,1,3,5,6,7], so YES
- 0-4: 0 connects to [2,3,4,5,6,7,8], so YES
- 4-6: 4 connects to [0,1,3,5], 6 connects to [0,2,3,7,8], so NO
- 0-6: YES (both in adjacency list)
- 1-4: 1 connects to [2,3,4,5], so YES

So in the link of v=3: edges are 1-2, 2-6, 6-0, 0-4, 4-1. This IS a C_5: 1-2-6-0-4-1.

The non-adjacent pairs in this C_5:
- (1,6), (1,0), (2,0), (2,4), (6,4)

These 5 pairs can be in different chains, giving much more merge-prone potential.

### Does the degree-4 proof generalize?

**Short answer: No, not directly.**

At degree 4, the merge geometry constrains merges to opposite pairs (exactly 2 pairs). The proof attempt in S1 exploits this to limit the number of problematic configurations.

At degree 5, there are 5 non-adjacent pairs. The merge geometry is richer:
- Multiple colours can simultaneously be merge-prone
- Chains can interleave in more complex patterns
- The "prepare then reduce" strategy (1-step detour) needs more alternatives

### Degree-5-specific approach

**Vertex selection strategy:** Instead of proving safe paths exist for ALL degree-5 vertices, prove that the graph always has ENOUGH degree-≤4 vertices (or safe degree-5 vertices) to remove.

**Euler formula argument:**
- In a triangulation on $n$ vertices: $|E| = 3n - 6$
- Sum of degrees: $2|E| = 6n - 12$
- Average degree: $6 - 12/n < 6$
- If average degree < 6, there must be many vertices with degree ≤ 5

More precisely, by a counting argument:
- Let $n_d$ = number of vertices with degree $d$
- $\sum n_d = n$, $\sum d \cdot n_d = 6n - 12$
- This gives: $n_3 + 2n_4 + n_5 - n_7 - 2n_8 - \ldots = 12$

So $n_3 + 2n_4 + n_5 \geq 12$. There are at least 12 "units" of low-degree vertices. Even if some are problematic, there should be enough safe ones.

**But:** This only helps with the "choose a different vertex" strategy. It doesn't directly prove safe path existence for a GIVEN vertex.

### Potential degree-5 proof ingredients

1. **C_5 chain structure:** In the C_5 link, non-adjacent pairs at distance 2 in the cycle have a specific geometric relationship. Chains connecting them must pass through a "narrow corridor" in the planar embedding.

2. **Non-interleaving + 5 colours:** With 5 colours and 5 neighbours, the pigeonhole principle is tight. At most 1 colour can appear twice (since $v$ has 5 neighbours in $\{1,2,3,4\}$... wait, 5 neighbours with 4 available colours means at least one colour appears twice). So EXACTLY one colour appears twice and three appear once, OR one appears 3 times and two appear once, etc.

3. **The "two-step" mechanism:** At n=9, safe paths need distance opt+1 = 3 instead of 2. This suggests a universal mechanism:
   - Step 1: Safe preparatory swap (rearranges chains)
   - Step 2: The previously merge-prone chain is no longer merge-prone
   - Step 3: Direct reduction to 4-colouring

## Conclusion

Degree-5 requires its own argument. The most promising paths:

1. **Vertex selection:** Prove that among $\geq 12$ low-degree vertices, at least one has safe BFS paths. This doesn't require understanding degree-5 chain structure.

2. **Two-step mechanism:** Prove that a single preparatory safe swap always exists that "de-merges" the problematic chain. This is a local structural argument.

3. **Computational extension:** Push to n=10-12 to check whether the pattern (safe non-optimal paths exist) continues. This doesn't prove anything but determines feasibility.

**Feasibility rating for degree-5 proof: Medium-Low.** The structural constraints are weaker and the counterexamples show the problem is real. A complete proof for degree-5 would be a significant result.
