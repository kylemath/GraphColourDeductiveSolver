# L-deg4 — Degree-$\le 4$ Kempe extension

**Group:** L-deg4 (M-Foundation). **Date:** 2 October 2026.
**Status:** the graph-theoretic core is a theorem. Tactic `sorry` count in the new file is $0$. Existence of a chain-separated pair is not proved: this Mathlib has no planar embedding.

`kempeSwap_preserves_proper` was not edited. No `lake update`. The Mathlib `cache` binary was not relinked (inode `13055368`, mtime `1790973707`, size `87178856`, sha256 `c68da8b82cdfe1b7118de3da70dc112492a8854b1015952c49a673436cb171a5`, same as `groups/L1_report.md`).

## 1. Definitions

| Name | File | Line |
|---|---|---|
| `IsProperColouring` | `KempeReconfiguration/Basic.lean` | 28 |
| `bichromaticSubgraph` | same | 40 |
| `inSameKempeChain` | same | 49 |
| `kempeSwap` | same | 54 |
| `kempeSwap_preserves_proper` | same | 100 |
| `kempeChain` | `KempeReconfiguration/Degree4Extend.lean` | 33 |
| `apexAdj`, `apexGraph` | same | 373, 395 |

`kempeChain G c a b u` is the set of vertices reachable from $u$ in $B_{a,b}(G,c)$. The external vertex is `none : Option V`, which is not a vertex of $H$.

## 2. Statement

Let $H$ be a simple graph on a finite decidable vertex type $V$, and let $c : V \to \mathrm{Fin}\, 4$ be a proper colouring. Let $n_0,n_1,n_2,n_3$ be distinct vertices, and suppose every colour in $\mathrm{Fin}\, 4$ equals $c(n_i)$ for some $i$.

1. **Not a clique.** If those four vertices are not pairwise adjacent, then two of them are distinct and non-adjacent. Name: `exists_nonadj_of_not_pairwise` (line 167).
2. **Separation frees a colour.** Suppose $c(n_0)=a$, $c(n_1)=b$, and $n_1$ is not in the $(a,b)$-Kempe chain of $n_0$. Let $c'$ be the Kempe swap of that chain. Then $c'$ is a proper $4$-colouring of $H$, $n_0$ is not adjacent to $n_1$, $c'(n_0)=c'(n_1)=b$, $c'(n_0)\neq a$, colour $a$ is missing from $\{c'(n_0),c'(n_1),c'(n_2),c'(n_3)\}$, and that set has size at most $3$. Name: `degree4_kempe_frees_colour` (line 451). The swap is proper because the chain is $\{a,b\}$-coloured and edge-closed, so `kempeSwap_preserves_proper` applies (`kempeSwap_chain_proper`, line 111).
3. **External vertex.** The same $c'$, extended by sending `none` to $a$, is a proper $4$-colouring of the graph obtained by joining a new vertex to exactly those four neighbours. Name: `degree4_apex_extension` (line 521).
4. **Case split, separation assumed.** If the chain of $n_0$ in colours $(c(n_0),c(n_2))$ misses $n_2$, or the chain of $n_1$ in colours $(c(n_1),c(n_3))$ misses $n_3$, then one of those two swaps is proper and changes the source colour. Name: `degree4_frees_of_some_separated_pair` (line 568).
5. **Degree $\le 3$.** Any subset of $\mathrm{Fin}\, 4$ of size at most $3$ omits a colour (`exists_free_colour_of_card_le_three`, line 357). No swap is required.

If the chain does contain the other vertex, the swap exchanges $a$ and $b$ on the pair (`kempeSwap_same_chain_keeps_both`, line 156). An edge between a vertex of colour $a$ and a vertex of colour $b$ puts them in one chain (`adjacent_ab_same_chain`, line 93), so a separated pair is non-adjacent (`separated_chain_not_adj`, line 102).

## 3. Evidence

```
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/KempeReconfiguration
lake build
```

Wall clock $2.08\,\mathrm{s}$ (`real 2.08`, `user 1.46`, `sys 0.89`), exit $0$, 2 October 2026, 21:26:48Z–21:26:50Z. Lake reported `Built KempeReconfiguration.Degree4Extend` and `Built KempeReconfiguration`. `Basic` was `Replayed`, not rebuilt.

An earlier `lake build` at 21:23:17Z exited $1$ on proof errors in `Degree4Extend.lean`. Those errors are not in the file that built.

No tactic `sorry` in `Degree4Extend.lean`. The word occurs once, in the header comment at line 18. Diagnostics on the new file are `linter.unusedSectionVars` warnings, the same class already reported for `Basic.lean`.

## 4. Result

Proved, in `Degree4Extend.lean`, imported from `KempeReconfiguration.lean`. The properness of the swapped colouring is `kempeSwap_preserves_proper` applied to one Kempe chain. The file does not axiomatize planarity.

## 5. Kill criterion

For “every proper $4$-colouring that uses all four colours on four vertices admits a freeing Kempe swap, with no separation hypothesis”: reject if an $(a,b)$-edge keeps both colours on the pair. **Met as a rejection of that unguarded claim.** `adjacent_ab_same_chain` and `kempeSwap_same_chain_keeps_both` are the witness. On a $K_4$ every pair is adjacent, so `exists_nonadj_of_not_pairwise` does not apply. This does not kill the planar Kempe step. It shows the step needs a missing edge whose chain does not meet the other end.

For the theorems that assume chain separation: a counterexample would be a separated chain whose swap is improper or leaves colour $a$ on $n_0$. **Not met.**

## 6. Not proved

Not proved: that a separated pair exists; that the non-adjacent pair from `exists_nonadj_of_not_pairwise` is chain-separated; any fact that uses a planar embedding, a rotation of the link, or non-crossing of Kempe chains. `degree4_frees_of_some_separated_pair` takes that separation as a hypothesis. The Four Colour Theorem is not proved. `kempeSwap_preserves_proper` is unchanged.

## 7. Feasibility

Supplying the missing hypothesis the way `Triangulation.link_degree3_complete` supplies the degree-$3$ link, namely “in a triangulation the link of a degree-$4$ vertex is a $4$-cycle, and at least one opposite pair is chain-separated”, and then quoting `degree4_frees_of_some_separated_pair`: **High**. The case split is already compiled.

Proving that hypothesis from a planar embedding in this Mathlib: **Low**. There is still no planar embedding API, as in `Degree3NoMerge.lean`.

## 8. Next steps

1. Add a named hypothesis for the degree-$4$ link (a $4$-cycle, and at least one opposite pair chain-separated). Discharge `degree4_frees_of_some_separated_pair` from that hypothesis. Do not use `sorry`, and do not treat `exists_nonadj_of_not_pairwise` as a substitute for chain separation.
2. Leave the embedding proof until Mathlib has embeddings. Non-adjacency alone does not free a colour: an $(a,b)$-path can still join the pair.
