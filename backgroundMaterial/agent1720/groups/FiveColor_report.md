# FiveColor — Heawood lemmas in Lean 4.15, no plane map

**Group:** FiveColor, manager M-Foundation
**Date:** 3 October 2026
**Status:** the graph-theoretic five-colour lemmas that do not need a plane map are theorems. Tactic `sorry` count in the new file is $0$. This is not the Four Colour Theorem. The degree-$5$ opposite-pair case is waiting on `PlaneMap.JordanSides`.

## 1. Definitions

| Name | File | Line |
|---|---|---|
| `IsProperColouring` | `lean4/KempeReconfiguration/KempeReconfiguration/Basic.lean` | 28 |
| `bichromaticSubgraph` | same | 40 |
| `kempeSwap` | same | 54 |
| `kempeSwap_preserves_proper` | same | 100 |
| `kempeChain` | `lean4/KempeReconfiguration/KempeReconfiguration/Degree4Extend.lean` | 33 |
| `exists_missing_colour` | `lean4/KempeReconfiguration/KempeReconfiguration/FiveColor.lean` | 34 |
| `exists_missing_colour_on` | same | 48 |
| `neighbourColourFinset` | same | 56 |
| `kempeComponent` | same | 92 |
| `kempeSwap_component_preserves` | same | 115 |
| `five_color_degree_at_most_four` | same | 137 |
| `five_color_degree_at_most_four_subtype` | same | 179 |
| `five_colorable_of_card_le_five` | same | 208 |

`neighbourColourFinset G x c` is the Finset `(G.neighborFinset x).image c`. It is equal, as a set, to $c''N_G(x)$ (`coe_neighbourColourFinset`). `kempeComponent G c a b u` is the `ConnectedComponent.supp` of `u` in `bichromaticSubgraph G c a b`. That set equals `kempeChain`.

The colouring of $G-x$ is `IsProperColouring` of `G.induce {v | v ≠ x}`, with `c` evaluated on the subtype. That is the local predicate from `Basic.lean`, not Mathlib `SimpleGraph.Coloring`.

`Degree4Extend.lean` was not edited. The Mathlib pin remains `v4.15.0`. No `PlaneMap` sources were copied. `docs/navigator/` was not edited.

## 2. Statement

Let $G$ be a simple graph on a finite decidable vertex type $V$, and let $x\in V$.

1. **Missing colour.** Any `Finset (Fin 5)` of size at most $4$ omits a colour. Name: `exists_missing_colour`. If a finite set of vertices is coloured with at most four values in `Fin 5`, some colour is unused on that set. Name: `exists_missing_colour_on`.
2. **Degree $\le 4$ extension.** If $c:V\to\mathrm{Fin}\,5$ is a proper colouring of the induced subgraph $G-x$, and either $\deg(x)\le 4$ or $|(G.\mathrm{neighborFinset}\,x).\mathrm{image}\,c|\le 4$, then there is a proper $5$-colouring $c'$ of $G$ with $c'(v)=c(v)$ for every $v\neq x$. Name: `five_color_degree_at_most_four`. The subtype form, where $c$ is defined only on $\{v\mid v\neq x\}$, is `five_color_degree_at_most_four_subtype`.
3. **Component swap.** If $c$ is a proper $k$-colouring, $a\neq b$, and $c(u)=a$, then the Kempe swap of the connected component of $u$ in the $(a,b)$-subgraph is a proper colouring. Name: `kempeSwap_component_preserves`. The proof quotes `kempeSwap_preserves_proper` after the component is shown to be $\{a,b\}$-coloured and edge-closed.
4. **At most five vertices.** If $|V|\le 5$, then $G$ has a proper $5$-colouring, by injecting $V$ into `Fin 5`. Name: `five_colorable_of_card_le_five`. Planarity is not used.

There is no declaration `five_color_theorem`. The file carries the comment

```
/- upstream PlaneMap: cycle_two_sides + exists_degree_le_five + neighbour_rotation -/
```

## 3. Evidence

```
export PATH="$HOME/.elan/bin:$PATH"
cd /Users/fulkanjou/GraphColour/lean4/KempeReconfiguration
lake build
```

Wall clock $2.11\,\mathrm{s}$ (`real 2.11`, `user 1.21`, `sys 1.19`), exit $0$, 3 October 2026. Lake reported `Built KempeReconfiguration.FiveColor` and `Built KempeReconfiguration`. `Degree4Extend` was `Replayed`, not rebuilt. An earlier `lake build` in the same session exited $1$ on proof errors in `FiveColor.lean` (`subst` erased `x`, `Fin.castLE_injective` applied to a disequality, `simp` loop on `degree`). Those errors are not in the file that built.

No tactic `sorry`, `admit`, or `axiom` in `FiveColor.lean`. The word `sorry` occurs once, in the header comment that forbids it.

## 4. Result

Proved, in `FiveColor.lean`, imported from `KempeReconfiguration.lean`. The extension across a degree-$\le 4$ vertex is the missing-colour argument of Heawood / Diestel 5.1.2, without an embedding. The swap of a named bichromatic component is proper by the existing `kempeSwap_preserves_proper`.

This is not the Four Colour Theorem.

## 5. Kill criterion

For `five_color_degree_at_most_four`: a finite simple graph, a vertex $x$ of degree at most $4$ (or with at most four colours on $N(x)$), and a proper $5$-colouring of $G-x$ that does not extend to $G$. **Not met.**

For an unguarded `five_color_theorem` in this pin: reject, because the degree-$5$ opposite-pair step needs `cycle_two_sides`. That claim was not made.

## 6. Not proved

Not proved: the Five Colour Theorem; existence of a vertex of degree at most $5$; a rotation of the link; that a cycle has two sides; that a degree-$5$ vertex whose neighbours use all five colours admits a chain-separated opposite pair. Those are the contents of `exists_degree_le_five`, `neighbour_rotation`, and `cycle_two_sides`. They are being written in `SimpleGraph/PlaneMap`, including `JordanSides.lean`, and target Lean 4.35. This package is pinned to Mathlib v4.15.0 and does not import that tree.

The Four Colour Theorem is not proved. A global “every graph of maximum degree $\le 4$ is $5$-colourable” induction, which would iterate `five_color_degree_at_most_four` and still not need planarity, is not packaged as one theorem.

## 7. Feasibility

Quoting `five_color_degree_at_most_four` and `kempeSwap_component_preserves` from a later `five_color_theorem` once `cycle_two_sides` supplies a separated opposite pair: **High**.

Proving `five_color_theorem` against this Mathlib v4.15.0 pin, without a plane map: **Low**. The missing lemmas are not in the pin.

## 8. Next steps

1. Leave `five_color_theorem` undeclared until `PlaneMap.JordanSides.cycle_two_sides` (and a degree-$\le 5$ vertex, and the link rotation) can be imported without raising the v4.15.0 pin.
2. When that import exists, run Heawood’s degree-$5$ case as: if the opposite pair of colours $a,b$ is chain-separated, apply `kempeSwap_component_preserves` on $G-x$ and then `five_color_degree_at_most_four`; if not, `cycle_two_sides` moves the swap to the other opposite pair.
3. Do not treat this file as a proof of the Four Colour Theorem.
