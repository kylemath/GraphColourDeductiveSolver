# Long Table report 1: regression checkpoint, invariance note, adversary

4 October 2026. To the Proof Navigator group and the Math solutions and scale-up team. This reports facts only; status words are the navigator's to assign. All files are in `backgroundMaterial/planemap-structural/longtable/`, hashed in its own `SHA256SUMS`. The shared manifest is untouched.

## 1. Regression checkpoint: all named fixtures reproduce

`regressions.py` is an independent standard-library implementation (`mass_core.py`). It does not import or execute the existing scripts. It reproduces every named fixture, with 32 of 32 checks passing in under one second (`regressions.json`):

- **Inputs:**
  - The order-20 file hash equals the census `input_sha256`.
  - The graph-36 ASCII (zero-based index) equals the census, `afternoon-checks.json` and `component-mass-results.json` records.
- **(σ, β) on the eight exterior roots of anchor 0** (8, 10, 11, 13, 14, 15, 16, 19): boundary, orbits, groups, losing groups and winning rounds all equal the published rows. Only root 8 loses, with 5 of 55 groups losing.
- **Mass macro at root 8:**
  - 198 orbits, 131 non-target, vertex order identical.
  - 3 one-swap stuck orbits, as the identical set of colourings.
  - The first stuck orbit is at (1,190), with successor ranks {(1,190), (1,206), (1,207), (1,211), (1,228)}.
  - 0 two-swap stuck orbits.
  - The published two-swap escapes replay as legal macros that lower the rank.
  - Closure checks pass: properness, move closure and reversibility.
- **Icosahedron:** 20 orbits at each of the 12 roots, target within one swap, and every root good under the two-swap macro.

**Permutation regressions:**
- **Mass macro, vertex relabelling:** under six seeded random relabellings, the counts at the image root stayed 198 / 131 / 3 / 0, and the full rank multiset was unchanged.
- **Mass macro, colour permutation:** R was unchanged on 25 states under 4 colour permutations each.
- **(σ, β) diagnostic:** in 3 of the 6 relabellings, at least one exterior root changed its (σ, β) outcome. This is expected, since the game depends on labels by construction. It is a direct observation of correction 3 from the revision-39 review.

**Format question for the math team (regression checkpoint).** Our per-root result records carry:
- `root`, `coloring_orbits`, `non_target`;
- `empty_family`, `vacuous_non_target`;
- `one_swap_stuck`, `two_swap_stuck`, `good_macro2`;
- the full witnesses described in the joint plan.

The adversary reads your corpus table if it has the census layout (`orders[].graphs_checked[].{graph_index, ascii, roots[]}`) with a boolean per-root field, set by `--mass-good-field`. Please use whatever names you prefer, and we will adapt. One request: include every degree-five root, because the loader asserts that each graph's roots equal D(T).

## 2. WP1: invariance argument, for quantifier review

`InvarianceNote.md` argues the following. For a graph isomorphism φ and a colour permutation π, the transport c ↦ π∘c∘φ⁻¹:
- preserves properness, B, bichromatic components and their sizes, and therefore p, q and R;
- commutes with every single-component move, and therefore with every macro of length at most two.

So Good(T, r) ⇔ Good(T′, φr), and the good-root set is a union of Aut(T)-orbits. The rotation is never used, so the argument covers orientation-reversing isomorphisms as well. The note states plainly that (σ, β) is not covered. We would be grateful for the math team's review of the quantifiers.

## 3. WP3: the adversary, run on the published (σ, β) table

`adversary.py` loads the corpus with whole-file hash checks and an ASCII match for each graph. It reads a published per-root table and classifies each rule by the four outcomes in the joint plan. The tie-break is the smallest label. The sets were declared before evaluation: S0 = D(T), S1± = the arg max/min over D(T) of the number of degree-five neighbours, and the label-based anchor rule kept as a regression.

| Rule | Graphs | Set contains a failing root | Tie-break picks a failing root | All of D(T) fail | First tie-break failure |
|---|---:|---:|---:|---:|---|
| S0 | 118 | 23 | 8 | 0 | order 17, graph 0, root 0 |
| S1+ | 118 | 10 | 8 | 0 | order 17, graph 0, root 0 |
| S1− | 118 | 4 | 2 | 0 | order 20, graph 14, root 4 |
| anchor (label-based) | 118 | 8 | 1 | 0 | order 20, graph 36, root 8 |

**Regression agreement:**
- The anchor rule's only tie-break failure is the published one, order 20, graph 36, root 8.
- The table contains 46 failing root instances, matching `anchor-rule-results.json`.
- S0's first failure equals the published first failing-root fixture, order 17, graph 0, root 0.

**Reading these results:** this is (σ, β), a label-sensitive check, so these numbers describe the Plantri labelling, not the graphs. They are regression and plumbing evidence, not candidate-set findings. S1−'s low count is suggestive at most; we will not cite it until it is evaluated against the mass-macro table. The real WP4 evaluation of S0 and S1± runs as soon as the corpus team publishes its mass table:

```bash
python3 adversary.py --check mass --mass-table <published table>
```

For later rules, descriptive statistics will use orders 12–18 only (`--max-order 18`). Any rule found that way is frozen in writing before it is evaluated on orders 19–20.

## 4. WP6: our errata, done

- **The Long Table:** Kamper now catches the Catalan error herself, since shared-colour chains can cross. The plan napkin requires a definition for chains that share a colour.
- **The Afternoon Call:** interior swaps are "narrower, not dead." "Only live shape" is now "one live shape." A postscript records the graph-36 answer, the result that root 8 passes the two-swap mass macro, and the label sensitivity of (σ, β).
- Both plays remain labelled fiction. The pages on the site have been rebuilt.

## Waiting on

The corpus team's per-root mass-macro table, and the navigator's revision 39. We will not run a whole-corpus enumeration ourselves.

— The Long Table authors
