# L1 — Lean build of KempeReconfiguration

**Group:** L1 (M-Foundation). **Date:** 2 October 2026.
**Status:** the Kempe package builds. Tactic `sorry` count is \(0\). Chain Lifting as component equality is still not a theorem.

Toolchain `leanprover/lean4:v4.15.0` (`Lean (version 4.15.0, arm64-apple-darwin23.6.0, commit 11651562caae, Release)`). Mathlib checkout `.lake/packages/mathlib` at `9837ca9d65d9` (`v4.15.0` in `lake-manifest.json`). No `lake update`. No second clone. The cache binary was not rebuilt.

## 1. Definitions

All of these are in `lean4/KempeReconfiguration/` and were elaborated by the build in §3.

| Name | File | Line |
|---|---|---|
| `IsProperColouring` | `KempeReconfiguration/Basic.lean` | 28 |
| `bichromaticAdj` | same | 35 |
| `bichromaticSubgraph` | same | 40 |
| `inSameKempeChain` | same | 49 |
| `kempeSwap` | same | 54 |
| `Triangulation` | `KempeReconfiguration/Degree3NoMerge.lean` | 27 |
| `K4_explicit` | `lean4/FourColor/Foundation/F1_ColoringBasics.lean` | 72 |

`Basic.lean` imports `Mathlib.Combinatorics.SimpleGraph.Path`, not `Connectivity`. In this Mathlib tree `Connectivity.lean` does not exist; `Walk` is in `Walk.lean` and `Reachable` is `def Reachable (u v : V) : Prop := Nonempty (G.Walk u v)` in `Path.lean`.

`SimpleGraph.deleteVerts` does not occur in this checkout. Vertex deletion on a subgraph is `SimpleGraph.Subgraph.deleteVerts` (`Mathlib/Combinatorics/SimpleGraph/Subgraph.lean`, line 1136): `G'.induce (G'.verts \ s)`.

Paper colour \(5\) is `(4 : Fin 5)`, as in `backgroundMaterial/agent1701/groups/F2_spec.md`.

## 2. Statement

For the Lean package `KempeReconfiguration`, with `autoImplicit` false:

1. Every declaration in `Basic.lean`, `NeverRevert.lean`, `ChainLifting.lean`, `Degree3NoMerge.lean`, and `Main.lean` elaborates, and no proof contains the tactic `sorry`.
2. The three obligations of `F2_spec.md` §2, as they stand in these files:
   - **2.1.** For every `G`, proper colouring `c`, `a ≠ b`, and decidable `S` whose vertices are coloured `a` or `b` and which is closed under adjacency into `{a,b}`, `kempeSwap c S a b` is a proper colouring. Name: `kempeSwap_preserves_proper`.
   - **2.2.** For every `c`, decidable `S`, and `target ≠ a`, `target ≠ b`, `kempeSwap c S a b v = target ↔ c v = target`, and the corresponding set and cardinality forms. Names: `never_revert_pointwise`, `never_revert`, `never_revert_card`.
   - **2.3.** There is no theorem stating, for `c(v) = (4 : Fin 5)` and `a, b ≠ 4` and `u ≠ v`, equality of the `(a,b)`-components of `u` in `G` and in `G` with `v` deleted.

F1, elaborated against the same Mathlib oleans: for `n, m : ℕ`, `(⊤ : SimpleGraph (Fin n)).Colorable m ↔ n ≤ m`, and in particular `K₄` is \(4\)-colourable, not \(3\)-colourable, and has chromatic number \(4\).

## 3. Evidence

Authoritative Kempe build. Only the package build directory was removed. `.lake/packages/` was not touched.

```
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/KempeReconfiguration
rm -rf .lake/build
lake build
```

Wall clock \(10.047\,\mathrm{s}\), exit \(0\), 2 October 2026, 20:56:56Z–20:57:06Z. Log: `backgroundMaterial/agent1720/groups/L1_lake_build_clean.log`. Lake reported `Built` for `KempeReconfiguration.Basic`, `NeverRevert`, `ChainLifting`, `Degree3NoMerge`, `Main`, and the root `KempeReconfiguration`. Oleons:

- `.lake/build/lib/KempeReconfiguration.olean`
- `.lake/build/lib/KempeReconfiguration/Basic.olean`
- `.lake/build/lib/KempeReconfiguration/NeverRevert.olean`
- `.lake/build/lib/KempeReconfiguration/ChainLifting.olean`
- `.lake/build/lib/KempeReconfiguration/Degree3NoMerge.olean`
- `.lake/build/lib/KempeReconfiguration/Main.olean`

Source hashes at the start of that command equal the hashes after it. `Basic.lean` `6db7e1e4…`, `NeverRevert.lean` `274b359a…`, `ChainLifting.lean` `f12ecc08…`, `Degree3NoMerge.lean` `3c747d8f…`, `Main.lean` `ef68ed96…`, `KempeReconfiguration.lean` `88ed88f0…`.

Cache binary before and after: inode `13055368`, mtime `1790973707`, size `87178856`, sha256 `c68da8b82cdfe1b7118de3da70dc112492a8854b1015952c49a673436cb171a5`. It was not replaced. `lake build mathlib/cache` was not run.

Diagnostics on that build are warnings, not errors. `linter.unusedSectionVars` on `kempeSwap_colour_cases` (line 64), `kempeSwap_preserves_other` (77), `kempeSwap_outside` (86), `kempeSwap_preserves_proper` (100), `never_revert_card` (62), `vertex_not_in_bichromatic` (27), `bichromatic_adj_delete_irrelevant` (43), `colour5_isolated_in_bichromatic_14` (60), `adj_same_chain` (36). `linter.unusedVariables` on `bichromatic_adj_delete_irrelevant`: `hva`, `hvb`, `hu`, `hw` (lines 46–47). Those four hypotheses are unused because both sides of the `↔` are `bichromaticAdj G c a b u w` and the proof is `rfl`. The statement does not mention `deleteVerts`.

F1, same environment, no FourColor package configure and no second Mathlib checkout:

```
export PATH="$HOME/.elan/bin:$PATH"
cd lean4/KempeReconfiguration
lake env lean -DautoImplicit=false \
  /Users/fulkanjou/GraphColour/lean4/FourColor/Foundation/F1_ColoringBasics.lean
```

Wall clock \(0.876\,\mathrm{s}\), exit \(0\), 20:58:58Z. Log: `backgroundMaterial/agent1720/groups/L1_f1_lean2.log`. File sha256 `c00d2eb0c5b42856f54a8a5854422d046223b6ceab67965401eab4ddef27eb37`, unchanged during the run. Lean printed no diagnostics. Cache sha256 unchanged.

**Errors on sources that were replaced before the successful build.** They are not errors in the tree that produced the oleans above.

| When | Command | Time | Error |
|---|---|---|---|
| 20:48:41Z | `lake build` | \(2\,\mathrm{s}\), exit 1 | missing `KempeReconfiguration/KempeReconfiguration.lean` under the old `srcDir` (`L1_lake_build.log`) |
| 20:49:54Z | `lake build +KempeReconfiguration.Main` | \(5\,\mathrm{s}\), exit 1 | no `Mathlib/Combinatorics/SimpleGraph/Connectivity.lean`; bad import in the then-current `Basic.lean` (`L1_lake_modules.log`) |
| 20:51:37Z | `lake build` | \(8\,\mathrm{s}\), exit 1 | `kempeSwap_preserves_proper` unsolved goals at lines 118, 119, 127, 128, 136, 137 (`L1_lake_build2.log`). That `Basic.lean` hash is not `6db7e1e4` |
| 20:52:39Z | `lake build` | \(8.054\,\mathrm{s}\), exit 1 | `Basic.lean:119` no goals; `:121` `Ne.symm hab` has type `b ≠ a` but a conjunction was expected (`L1_lake_build3.log`) |
| 20:53:36Z | `lake build` | \(8.046\,\mathrm{s}\), exit 1 | `Basic.lean` replayed with no error. `ChainLifting.lean:28` and `:44` unknown identifier `k`. `Degree3NoMerge.lean:30` failed to synthesize `Fintype (G.neighborSet v)`; `:37` and `:64` unknown `k`; `:42` `SimpleGraph.Reachable.intro` is not a constructor (`Reachable` is a `def`). `NeverRevert.lean:38`, `:40`, `:44`, `:45` type mismatches in `never_revert_pointwise` (`L1_lake_build4.log`) |
| 20:57:37Z | `lake env lean` on F1 sha256 `67b7866c…` | \(8.043\,\mathrm{s}\), exit 1 | `:59` unknown tactic `norm_num`, goal `3 < 4`; `:69` no `Colorable.card_le_of_pairwise_adj`; `:74` `![0,1,2,3]` type mismatch; `:79` `decide` stuck (`L1_f1_lean.log`) |

The files named in the last two rows were edited after those logs. The successful commands in the first part of this section are the ones that match the sources on disk.

**`sorry`.** No tactic `sorry` in any project `.lean` file under `lean4/KempeReconfiguration/` or in `F1_ColoringBasics.lean`. The word occurs only in comments:

| File | Line | Role |
|---|---|---|
| `Basic.lean` | 12 | “Target: 0 sorry” |
| `NeverRevert.lean` | 14 | “Target: 0 sorry” |
| `ChainLifting.lean` | 14 | “Target: 0 sorry” |
| `Degree3NoMerge.lean` | 16 | “Target: ≤ 2 sorry (planarity axioms)” |
| `Degree3NoMerge.lean` | 28 | comment `TODO: sorry — Mathlib lacks a full planar graph API.` The next field is `link_degree3_complete`, a typeclass assumption |
| `Degree3NoMerge.lean` | 75 | “0 explicit sorry statements” (the word twice) |
| `Degree3NoMerge.lean` | 79 | “rather than a sorry” |
| `Main.lean` | 7, 30 | comments. `Main.lean` declares no theorem |
| `F1_ColoringBasics.lean` | 11 | “target: 0 sorry” |

`F2_spec.md` §4 placed the Degree-3 TODO comment at line 27. In the file that built, that comment is line 28, because `variable {k : ℕ}` was inserted above the class. The other comment lines in that table still match.

## 4. Result

Computed as a successful build, not as a new proof. Exit \(0\), \(10.047\,\mathrm{s}\). Every declaration that exists in the five Kempe modules compiled:

- `Basic.lean`: `IsProperColouring`, `bichromaticAdj`, `bichromaticSubgraph`, `inSameKempeChain`, `kempeSwap`, `kempeSwap_colour_cases`, `kempeSwap_preserves_other`, `kempeSwap_outside`, `kempeSwap_preserves_proper`.
- `NeverRevert.lean`: `never_revert_pointwise`, `never_revert`, `never_revert_card`.
- `ChainLifting.lean`: `vertex_not_in_bichromatic`, `bichromatic_adj_delete_irrelevant`, `colour5_isolated_in_bichromatic_14`.
- `Degree3NoMerge.lean`: `Triangulation`, `adj_same_chain`, `degree3_no_merge`.
- `Main.lean`: imports only.

F1, exit \(0\), \(0.876\,\mathrm{s}\): `top_colorable_self`, `top_coloring_injective`, `top_not_colorable_of_lt`, `top_colorable_iff`, `K4_colorable_four`, `K4_not_colorable_three`, `K4_chromaticNumber`, `K4_not_colorable_three'`, `K4_explicit`, `K4_explicit_proper`.

Against `F2_spec.md`:

- §2.1 compiled. The bare `Ne.symm` goals F2 recorded at the old lines 147, 152, and 153 are not in the `Basic.lean` that built, and `kempeSwap_preserves_proper` produced no error.
- §2.2 compiled, all three forms.
- §2.3 did not compile, because there is still no such theorem. The three lemmas in `ChainLifting.lean` compiled. `colour5_isolated_in_bichromatic_14` includes `hv5 ▸ rfl` and elaborated; the term-mode `▸` failure predicted in F2 §10 did not occur. `bichromatic_adj_delete_irrelevant` compiled and is still not a `deleteVerts` lemma (unused-hypothesis warnings).
- `degree3_no_merge` compiled from `Triangulation.link_degree3_complete`. That field is not a `sorry`.
- No `*Five*` file under `lean4/`. F2 §5 still holds: there is no Five Colour Theorem in this Lean tree.
- F2’s acceptance test (§6) fails item 3. Citing the isolation lemmas does not close Tier-1.

## 5. Kill criterion

For “Tier-1 is closed”: reject the claim if the evidence is only `colour5_isolated_in_bichromatic_14`, `vertex_not_in_bichromatic`, or `bichromatic_adj_delete_irrelevant`, or a comment in `Main.lean`, or a comment containing the word `sorry`. **Met as a rejection of that claim.** The build does not supply a component-equality theorem.

For “the package does not build”: one error in `lake build` on these sources. **Not met.**

## 6. Not proved

Not proved: equality of `(a,b)`-Kempe chains in `G` and in the graph with a colour-\(5\) vertex deleted; any reading of `bichromatic_adj_delete_irrelevant` as deletion; planarity of `Triangulation.link_degree3_complete`; the Five Colour Theorem; any \(4\)-colouring theorem (`Main.lean` has none). F1 was elaborated as one file through the Kempe Mathlib path. It was not built as the `FourColor` Lake package, and that package’s `lakefile.lean` still requires Mathlib from git.

## 7. Feasibility

Stating and proving the component equality with `SimpleGraph.Subgraph.deleteVerts`, without `sorry`, now that the package builds: **High**. The isolation lemmas already compile. The work is the identification of walks in the bichromatic subgraph with walks after `Subgraph.deleteVerts`, which this Mathlib does have. It does not need a planar embedding.

Uncertainty, not a lower rating: `deleteVerts` returns a `Subgraph`, not a `SimpleGraph` on a subtype, so the equality has to say which vertex types are identified. That is a writing task. It is not a reason to compile a different project first.

## 8. Next steps

1. Add one theorem whose statement is the component equality in `F2_spec.md` §2.3, using `SimpleGraph.Subgraph.deleteVerts` (there is no `SimpleGraph.deleteVerts` here). Do not discharge it with `sorry`, and do not mark it done by citing `colour5_isolated_in_bichromatic_14`.
2. Leave the Five Colour Theorem unformalized until that equality is a compiled theorem. This build did not create an `F5` file.
3. The `FourColor` Lake package was not configured. A path dependency on `.lake/packages/mathlib` is unnecessary for elaborating `F1_ColoringBasics.lean`: `lake env lean` from `KempeReconfiguration` already did it in under a second.
