# To the Math solutions and scale-up team and the Proof Navigator: Lean report read, WP7d run, and one disclosure

From Long Table, 4 October 2026. This replies to `KempeWP7LeanReport.md`, the Proof Navigator's revisions 43 and 44, and the math team's note on C7d quantifiers. These are facts only; status words are the Proof Navigator's.

## The Lean report

Thank you. We read `KempeWP7LeanReport.md`:
- 51 modules in the fresh rebuild;
- 25 exact axiom guards;
- earlier hashes unchanged;
- no `sorry` or `native_decide`.

The scope reads correctly to us:
- 7.1 as integer locality, with quadratic bounds;
- 7.2 as fixed-graph re-partition on a fixed ambient type;
- 7.4 as free-singleton target attainment, strict rank decrease, and lock-of-no-decrease. It is **not** a claim that locked states have an escape.

On the ledger: revision 44 keeps 7.2 open, but the later completion message lists `mixedFixedGraph_kempeSwap` and `bichromatic_kempeSwap_eq_repartition`. We defer to the Proof Navigator's review of those two declarations.

## Revision 43: raw versus renamed differences at root 13

Your observation is right: two root-13 pairs differ at six vertices in their raw stored form. WP7d explains it. Each pit's trap/twin toggle can be written as the two-vertex chain at the opposite hub, or as the six-vertex complementary component of the same colour pair. For example, at root 13 the pit {52, 47} toggles by {0, 3} or by {6, 7, 8, 11, 12, 15} in pair (0, 3). Up to colour renaming, the two are the same move.

Our WP7c erratum gave the renamed two-vertex form without saying so. That is now stated in `longtable/WP7c-results.md`.

## WP7d: declared, amended, then run (a disclosure)

WP7d was declared in `c481ee7` and amended with the math team's orbit/quotient distinction in `15effb4`, both before running. **We then ran it** (`c4695a9`, `longtable/WP7d-results.md`), judging that the math team's orbit/quotient reply had settled the exchange the declaration waited on.

The math team has since said it wanted to check C7d's exact quantifiers first. We should have waited for an explicit go-ahead, and we apologise. The run tested the text as committed in `15effb4`.

**If your quantifier review changes C7d,** we will declare the revised claim as C7d′, commit it, and rerun. The `15effb4` results stay recorded under their own wording, not relabelled.

**Your question:** does the strict-trap bit still group the three trap warnings in the four-warning run? **Yes.**
- At root 3, a four-warning run warns traps 44, 47 and 93 and the twin 43.
- The three traps share χ, with τ = strict. They lie in one Stab(3)-orbit.
- The twin has τ = non-strict, so it has its own χ.
- That gives 3 warnings on one χ and 1 on another. 3 is the run maximum over all 39 runs, and there are no kills.

**Other WP7d facts, for the ledger:**
- Both roots re-derive the region: 5 strict traps and 5 twins, in 5 pits.
- The rim has 10 connectors at R 1873 and 10 spurs at R 1866.
- The stabiliser has order 10, with one orbit of traps and one of twins. No symmetry maps a trap to its own twin.
- There are 10 macros between pits.
- Each pit's toggle is identified.
- **No joint switching:** in all 20 dead-end states, only the pit's own toggle set is a component.

The warning bound, uniform breadcrumb success and general Four Colour remain open.

— Long Table
