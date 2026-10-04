# L-chain — bichromatic reachability after deleting an off-colour vertex

**Group:** L-chain (M-Foundation). **Date:** 2 October 2026.
**Status:** proved. Tactic `sorry` count in the new file is \(0\).

Toolchain `leanprover/lean4:v4.15.0`. Mathlib at `v4.15.0`. No `lake update`. The Mathlib `cache` binary was not rebuilt.

## 1. Definitions

| Name | File | Role |
|---|---|---|
| `bichromaticAdj` | `KempeReconfiguration/Basic.lean`, line 35 | Edge of \(B_{a,b}(G,c)\): a \(G\)-edge whose ends are coloured \(a\) or \(b\) |
| `bichromaticSubgraph` | same, line 40 | That relation as a `SimpleGraph V` |
| `inSameKempeChain` | same, line 49 | `(bichromaticSubgraph G c a b).Reachable` |
| `vertex_not_in_bichromatic` | `KempeReconfiguration/ChainLifting.lean`, line 27 | If \(c(v)\notin\{a,b\}\) then \(v\) has no \(B_{a,b}\)-edge |
| `SimpleGraph.induce` | Mathlib `Maps.lean`, line 178 | Induced subgraph on a set; vertex type is the subtype |
| `SimpleGraph.Subgraph.deleteVerts` | Mathlib `Subgraph.lean`, line 1136 | `G'.induce (G'.verts \ s)` |

`SimpleGraph.deleteVerts` does not occur in this Mathlib checkout. `colour5_isolated_in_bichromatic_14` is isolation of paper colour \(5\), encoded as `(4 : Fin 5)`. `bichromatic_adj_delete_irrelevant` is `rfl` and both sides are `bichromaticAdj G c a b u w`. Those two declarations are not the theorem below.

## 2. Statement

Let \(V\) be finite with decidable equality, \(G\) a simple graph on \(V\) with decidable adjacency, \(c : V \to \mathrm{Fin}\, k\), and \(a,b\in\mathrm{Fin}\, k\). Let \(v\in V\) satisfy \(c(v)\neq a\) and \(c(v)\neq b\).

For all \(u,w\in V\) with \(u\neq v\) and \(w\neq v\),

\[
w \text{ reaches } u \text{ in } B_{a,b}(G,c)
\quad\Longleftrightarrow\quad
\langle w\rangle \text{ reaches } \langle u\rangle \text{ in } B_{a,b}\bigl(G[V\setminus\{v\}],\, c|_{V\setminus\{v\}}\bigr).
\]

In Lean this is `bichromatic_reachable_iff_induce_delete`: the right-hand graph is `bichromaticSubgraph (G.induce (({v} : Set V)ᶜ)) (fun x => c x.val) a b`, and reachability is `SimpleGraph.Reachable`. The same biconditional written with `inSameKempeChain` is `inSameKempeChain_iff_induce_delete`.

The set form `bichromatic_reachableSet_eq_induce_delete`, for \(u\neq v\), equates \(\{w \mid u\text{ reaches }w\text{ in }B_{a,b}(G,c)\}\) with the set of \(w\neq v\) whose subtype is reachable from \(u\) in \(B_{a,b}(G[V\setminus\{v\}])\).

The colour-\(5\) case `colour5_bichromatic_reachable_iff_induce_delete` specialises to \(c(v)=(4:\mathrm{Fin}\, 5)\) and \(a\neq 4\), \(b\neq 4\).

On the same vertex type, `bichromaticSubgraph_eq_deleteVerts_spanningCoe` says \(B_{a,b}(G,c)\) equals the spanning graph of \((\top : B_{a,b}.\mathrm{Subgraph}).\mathrm{deleteVerts}\,\{v\}\). `bichromatic_reachable_iff_deleteVerts` is the resulting equality of `Reachable` for every pair of vertices.

Both endpoints must lie off \(v\) in the `induce` form, because \(V\setminus\{v\}\) does not contain \(v\). The `deleteVerts` form has no such restriction: the two graphs on \(V\) are equal.

## 3. Evidence

Proof file: `lean4/KempeReconfiguration/KempeReconfiguration/ChainEquality.lean`. Imported from `KempeReconfiguration.lean`.

The off-colour vertex is isolated by `vertex_not_in_bichromatic`. `eq_induce_spanningCoe_of_isolated` identifies a graph in which \(v\) is isolated with the spanning graph of its induced subgraph on \(V\setminus\{v\}\). `reachable_spanningCoe_iff` moves `Reachable` across that spanning graph by `Relation.ReflTransGen` along `Function.Embedding.subtype`. `simpa using` that equivalence is the script of `bichromatic_reachable_iff_induce_delete`. The `deleteVerts` equality is `ext` on adjacency; the colour hypotheses are used to keep edges off \(v\).

Timed package build, after that file elaborated:

```
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/KempeReconfiguration
lake build
```

Wall clock \(0.91\,\mathrm{s}\) (`/usr/bin/time -p`, `real`), exit \(0\), 2 October 2026, 21:18:57Z–21:18:58Z. Lake reported `Built KempeReconfiguration`. Diagnostics on that run are the pre-existing unused-section warnings in `Basic.lean`, `NeverRevert.lean`, `ChainLifting.lean`, and `Degree3NoMerge.lean`. `ChainEquality.lean` contributed none.

The word `sorry` occurs in `ChainEquality.lean` only in the header comment “Target: 0 sorry” (line 10). No proof uses the tactic.

Cache binary before and after: inode `13055368`, mtime `1790973707`, size `87178856`, sha256 `c68da8b82cdfe1b7118de3da70dc112492a8854b1015952c49a673436cb171a5`. It was not replaced.

## 4. Result

Proved, with the proof in `ChainEquality.lean`. The theorem that states the induced-graph reachability biconditional is `bichromatic_reachable_iff_induce_delete`.

## 5. Kill criterion

The statement is false if there exist \(G\), \(c\), \(a\), \(b\), and vertices \(v,u,w\) with \(c(v)\notin\{a,b\}\), \(u\neq v\), and \(w\neq v\), such that \(u\) is reachable from \(w\) in \(B_{a,b}(G,c)\) and not in \(B_{a,b}(G[V\setminus\{v\}])\), or the converse. That criterion was not met. Lean accepted the biconditional with no `sorry`.

## 6. Not proved

This is not the Five Colour Theorem, and it is not a Kempe swap. `Main.lean` still has no colouring theorem. `bichromatic_adj_delete_irrelevant` is unchanged and still does not delete a vertex. There is no bundled graph isomorphism `≃g`, and no lemma that `kempeSwap` along the chain of \(u\) in \(G\) agrees with the swap read on \(G[V\setminus\{v\}]\). `bichromaticSubgraph` still has no `DecidableRel` instance, so the reachable set is not yet a `DecidablePred` for `kempeSwap`.

## 7. Feasibility

High for the swap-agreement lemma. The reachable sets are already equal, and Mathlib’s `DecidableRel G.Reachable` sits in `Connectivity/WalkCounting.lean` once adjacency is decidable and \(V\) is finite. What is missing is the instance for `bichromaticSubgraph`.

## 8. Next steps

1. Add `DecidableRel (bichromaticSubgraph G c a b).Adj` from `DecidableRel G.Adj`, import `WalkCounting`, and take the reachable set of \(u\) as the swap set.
2. Prove that `kempeSwap` on that set, for \(c(v)\notin\{a,b\}\) and \(u\neq v\), agrees at every vertex of \(V\) with the colouring obtained from the induced graph.
3. Keep citing `bichromatic_reachable_iff_induce_delete` for chain equality. Do not cite `colour5_isolated_in_bichromatic_14` or `bichromatic_adj_delete_irrelevant` as that equality.
