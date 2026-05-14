# Theorem B — Confinement of Kempe Chains Under Swaps

**Agent:** 0050-M2-S1
**Date:** 18 February 2026

---

## Precise Statement

**Theorem B (Confinement).** Let $T$ be a planar triangulation with a proper $k$-colouring $c$ ($k \geq 4$). Let $\{a,b\}$ and $\{c,d\}$ be disjoint colour pairs. Suppose an $(a,b)$-Kempe chain $K_{ab}$ topologically separates two vertices $u$ and $w$ in the plane — i.e., $u$ and $w$ lie in different connected components of $\mathbb{R}^2 \setminus K_{ab}$ (viewing $K_{ab}$ as drawn in the planar embedding).

Then for any sequence of Kempe swaps $\sigma_1, \sigma_2, \ldots, \sigma_m$ where each $\sigma_i$ is a swap on a $(c', d')$-Kempe chain with $\{c', d'\} \cap \{a, b\} = \emptyset$: in the resulting colouring $c' = \sigma_m \circ \cdots \circ \sigma_1(c)$, the $(a,b)$-Kempe chain structure is unchanged. In particular, $K_{ab}$ still separates $u$ from $w$.

## Proof

### Invariance of the $(a,b)$-subgraph

A Kempe swap on a $(c', d')$-chain (with $\{c', d'\} \cap \{a,b\} = \emptyset$) only changes the colours of vertices in the chain, swapping $c' \leftrightarrow d'$.

**Key observation:** no vertex in the chain has colour $a$ or $b$ (since the chain only contains vertices coloured $c'$ or $d'$, and $c', d' \notin \{a, b\}$). Therefore:
- No vertex changes TO colour $a$ or $b$ (they only swap between $c'$ and $d'$)
- No vertex changes FROM colour $a$ or $b$ (they weren't coloured $a$ or $b$ to begin with)

The set of vertices coloured $a$ or $b$ is therefore unchanged, and the edges between them are unchanged (since the vertex set of $H_{ab}$ is invariant). Therefore the $(a,b)$-bichromatic subgraph $H_{ab}$ is identical before and after the swap.

By induction on $m$: after any sequence of swaps on colours disjoint from $\{a,b\}$, the subgraph $H_{ab}$ is preserved vertex-for-vertex and edge-for-edge.

### Topological separation is preserved

Since $H_{ab}$ is unchanged and $K_{ab}$ is a connected component of $H_{ab}$, the chain $K_{ab}$ is identical in the original and modified colourings. Its drawing in the planar embedding is unchanged. Therefore the topological separation of $u$ and $w$ by $K_{ab}$ is preserved. $\blacksquare$

## Strength and Limitations

### What Theorem B gives us

Theorem B says that $(a,b)$-barriers are **indestructible** by swaps on other colour pairs. This is crucial for the proof strategy because it means:

1. **Confinement regions are stable:** if we identify a region bounded by $(a,b)$-chains, vertices inside that region stay "trapped" — no swap on $\{c,d\}$, $\{c,e\}$, etc. can move them out.

2. **Sequential recolouring is safe:** when recolouring vertex $v_i$ using swaps on $\{c,d\}$, we don't disturb any $(a,b)$-barriers that protect previously recoloured vertices $v_1, \ldots, v_{i-1}$.

### What Theorem B does NOT give us

1. **It does not prevent the $(c,d)$-chains from changing.** After swapping a $(c,d)$-chain to recolour one vertex, OTHER $(c,d)$-chains might merge or split. This changes the $(c,d)$-chain structure and could affect later recolouring steps.

2. **It does not address chains sharing a colour.** If we swap a $(b,c)$-chain, this DOES affect the $(a,b)$-subgraph (since vertex colours change between $b$ and $c$, which changes the set of $b$-coloured vertices). Theorem B only applies to DISJOINT colour pairs.

3. **It does not provide constructive swap sequences.** Knowing that barriers are stable is necessary but not sufficient for the proof strategy. We still need to show that the right swap sequences exist.

## Nested Regions

**Corollary.** If $K_{ab}^{(1)}$ and $K_{ab}^{(2)}$ are two $(a,b)$-chains that create nested regions (one inside the other), and a vertex $w$ is in the inner region, then $w$ is confined to the inner region under any swaps on colours disjoint from $\{a,b\}$.

*Proof.* Both chains are preserved (by Theorem B). The nested region structure is topological and determined by the chains' embedding. Since both chains are unchanged, the nested regions are unchanged, and $w$ remains confined. $\square$

## Relationship to Theorem A

Theorems A and B are complementary:
- **Theorem A** constrains how chains for disjoint colour pairs are arranged (non-interleaving)
- **Theorem B** constrains how chains evolve under swaps (barriers are stable)

Together, they imply that at a degree-5 vertex $v$ (coloured 5 in a 5-colouring), the barrier structure created by the Kempe chains of colours $\{1,2,3,4\}$ is both **topologically constrained** (Theorem A) and **dynamically stable** (Theorem B).

## Feasibility Assessment

**High.** Theorem B is straightforward — the key insight (disjoint swaps don't affect the bichromatic subgraph) is simple but powerful. The proof is complete and rigorous.

## Concrete Next Steps

1. Characterise which $(a,b)$-chains actually SEPARATE vertices in practice (for small triangulations)
2. Quantify the "dynamic stability budget": how many swap steps are needed before we exhaust the available barrier-preserving operations?
3. Identify the obstruction more precisely: when does the Colour Elimination strategy fail because the needed swap is NOT on a disjoint colour pair?

---

*0050-M2-S1 — 18 February 2026*
