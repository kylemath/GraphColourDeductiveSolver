# Compiled general M3 short-fill theorem

Math, 5 October 2026. Task A is complete. Both teams independently implemented and source-compiled the general theorem; Math reviewed their component and move semantics and adopted Team A's implementation under the canonical namespace `SimpleGraph.VacancyShortFill`.

## Result and exact scope

For any simple graph G, arbitrary vertex and colour types with decidable equality, an initially proper deletion colouring, and an actual mixed filling path of length n≤2, `short_fill` produces a fixed-original-hole Kempe-only filling path of length at most n. `optimal_short` proves exact minimum-distance equality when the mixed minimum is at most two. No finiteness, planarity, degree-five, fan or four-colour assumption is needed. Every finite graph with a finite palette is included.

The printed Lean statements are:

```lean
short_fill (G : SimpleGraph V) (hc : ProperOff G h c)
    (hn : n ≤ 2) (path : MixedPath G n (h, c) t)
    (filled : Target G t.1 t.2) : PureFill G h c n

optimal_short (G : SimpleGraph V) (hc : ProperOff G h c)
    (hn : n ≤ 2) (optimal : MixedOptimal G h c n) :
    PureOptimal G h c n
```

Here `PureFill G h c n` means there exists a pure path of length k≤n, ending with a missing neighbour colour at the original h. The exact machine-printed universally quantified statements are preserved in `short-fill-lean/printed-statements.txt`. Equality refers to minima; a nonminimal supplied path may shorten.

## Actual graph moves

`Whole` is an active seed together with an iff to reachability in the actual bichromatic deletion graph. A Kempe step swaps two distinct colours on exactly one such whole component. Initial properness implies properness after each move. A slide is the existing `VacancySlide.slide` on an adjacent uniquely coloured neighbour; the stored label of the hole is irrelevant. No premise assumes the desired path conversion.

`terminal_slide` constructs the singleton original-hole component. `slide_swap_same` collapses noncommuting slide/swap cases to one swap. The avoiding-colour case commutes, and `mixed_two` handles KK, KS, SS and SK. The path and optimality theorems follow from these proved cases.

## Acceptance checks

- A fresh isolated audit rebuilt **all 83 source modules**, the prior frozen 79 plus VacancySlide, VacancyShortFill and their two test modules. Every compile returned zero; source hashes were identical before and after. Audit time: 106.533 seconds.
- Cached custom artifacts, including team prototypes, were excluded. Only upstream artifacts were linked. The earlier 79 source hashes were checked unchanged before building.
- Exact `#guard_msgs` checks for terminal-slide, same-pair conversion, SK conversion, short-fill and minimum equality permit only `[propext, Classical.choice, Quot.sound]`.
- No placeholders, new axioms or `native_decide` occur in the theorem or tests.
- A degree-two/two-colour fixture compiles, with an unfilled start and an optimal one-move terminal slide. This checks the broader scope and the optimality statement.
- Team B's separate implementation also compiled and passed nine axiom guards; its independent review found no semantic gap in the adopted source.

## Reproducible artifacts

Canonical live source: `/Users/fulkanjou/mathlib4-planemap/Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFill.lean`. Test: `/Users/fulkanjou/mathlib4-planemap/MathlibTest/PlaneMapVacancyShortFill.lean`.

Committed snapshots of both new modules and tests are under `backgroundMaterial/planemap-structural/short-fill-lean/`, together with the 83-module manifest, source hashes, build output and printed statements. The script `longtable/audit/short_fill_source_audit.py` reconstructs the audit from the frozen baseline; choose a fresh output directory on rerun. `short-fill-lean/ARTIFACT-SHA256SUMS` binds the committed artifacts.

This completes the compiled short-fill task only. The unequal-pole belt walk remains separate work in progress. Universal vacancy and universal boundedness of m remain open. The exact-m=3 triangle-sum family is a separately reviewed hand theorem.
