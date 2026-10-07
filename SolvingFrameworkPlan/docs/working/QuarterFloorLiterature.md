# The "quarter floor": literature check (Long Table, 6 Oct 2026, evening)

**Observed** (localcompute 1805 and 1811; Math 1813; exhaustive at orders 12–24, [computed, these orders only]): every Kempe class of T − v at a degree-5 vertex has at least 1/4 of its states filled. So, per hole, P(T,4)/P(T − v,4) ≥ 1/4. No such floor holds at degree 6 or 7 (1/8, 2/17).

Read marks: **full** (text read), **abstract** (abstract or summary read), **search** (seen only in search snippets), **unchecked** (from memory).

## 1. Verdict: nothing found

I found no statement in the literature, as a theorem, conjecture or counterexample, of a bound P(T,4) ≥ c·P(T − v,4) for a degree-5 vertex v of a planar triangulation, nor of any Kempe-class version. Searches covered chromatic-polynomial ratios under vertex deletion, Birkhoff–Lewis, Jackson's survey, the Tutte upper-bound and golden-ratio literature, and the Kempe-class literature. This is not exhaustive: I could not open Birkhoff–Lewis 1946 or Woodall's papers in full.

## 2. What exists nearby

| Source | Relevance | Read |
|---|---|---|
| G. D. Birkhoff, D. C. Lewis, "Chromatic polynomials", *Trans. AMS* 60 (1946) 355–451 | Proved P(G,q) > 0 for planar G and real q ≥ 5. Conjectured the same for q ≥ 4 (the Birkhoff–Lewis conjecture, still open; an ε below 5 is not known). Reduction formulas for small rings. I recall, **unchecked**, that their q ≥ 5 proof goes through the explicit lower bound P(G,q) ≥ q(q−1)(q−2)(q−3)^{n−3} for near-triangulations, built up vertex by vertex. That is a per-vertex multiplicative bound of the kind asked about, but at q ≥ 5, not q = 4. | search (theorem and conjecture); the bound is **unchecked** |
| B. Jackson, "Zeros of chromatic and flow polynomials of graphs" (survey), arXiv:math/0205047 | Theorem 9 (q ≥ 5 positivity) and Conjecture 10 (q ≥ 4). **No vertex-deletion ratio bounds** and nothing specific at q = 4. | summary of the ar5iv text |
| Tutte's golden identity and the upper bound \|P(T, τ+1)\| ≤ (τ−1)^{n−5}; Shrock and collaborators, arXiv:1110.5883, 1201.4200 | Evaluations at τ+1 and τ+2, not at 4. No ratio bound at q = 4. | abstract and search |
| Mohar 2006; Feghali 2022; Tilley 2017 (D-resolvability); Tilley a-graphs (DAM 217, 2017) | Kempe classes. **No proportion-of-filled statements** found. Tilley's D-resolvability (= R\*) asks only that each class contain *one* filled state. The quarter floor is a quantitative strengthening of it. | as in \`wsk-ergodicity-literature.md\` |

## 3. Hand observations [hand, unreviewed]

1. **An exact identity.** Let G = T − v with link x0..x4, and let G_i = G with x_i and x_{i+2} identified. A proper colouring of the 5-cycle using 3 colours has exactly two equal non-adjacent pairs, and one using 4 colours has exactly one. So Σ_i P(G_i,4) = 2·F + U, where F = P(T,4) counts filled colourings and U unfilled ones, and P(G,4) = F + U. Hence
   **P(T,4) = Σ_{i=0}^{4} P(G_i,4) − P(T − v,4)**, and the quarter floor is **Σ_i P(G_i,4) ≥ (5/4)·P(T − v,4)**: the five fan contractions together have at least 5/4 as many colourings as T − v. This is the Birkhoff–Lewis style 5-ring relation at q = 4.
2. **Baseline.** For a free 5-cycle, 120 of the 240 proper 4-colourings use 3 colours: 1/2. So the floor 1/4 is half of the "independent ring" value. Correlations through the triangulation can halve the fraction but, on the data, never more.
3. **Strength.** A floor c > 0 at some degree-5 vertex of every core triangulation would imply the 4CT by induction, through the contraction route. So any such bound for all planar triangulations is **at least as hard as 4CT**, like Birkhoff–Lewis at q = 4. The *class* version (each Kempe class ≥ 1/4 filled) implies R\* (Tilley's conjecture) and is stronger still.
4. **Degree comparison.** No floor at degree 6 or 7 (1/8 and 2/17 observed) is consistent with the free-ring baselines falling, and suggests the degree-5 floor comes from the 5-cycle's odd-cycle structure. That is a guess, not checked.

## 4. Suggested next reading (not done)

- Birkhoff–Lewis 1946 §§ on the q ≥ 5 proof, to see whether their per-vertex inequality has a q = 4 analogue with a constant like 1/4.
- D. R. Woodall's papers on chromatic polynomials of near-triangulations (*J. Combin. Theory B*, 1990s), and his Birkhoff–Lewis-type inequalities.
- Thomassen, "The zero-free intervals for chromatic polynomials of graphs" (*Combin. Probab. Comput.* 1997), and his τ+2 positivity proof, for its ratio technique.
