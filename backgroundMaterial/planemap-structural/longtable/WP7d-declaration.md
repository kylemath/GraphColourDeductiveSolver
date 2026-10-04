# WP7d declaration: structure of the order-17, graph-3 dead-end region, and a bounded-fibre charging candidate

Long Table, 4 October 2026. Committed **before** any WP7d test. This is open to revision by the math team, who are checking the network counts and traces and may propose an exact charging claim. Nothing below is run until that exchange settles.

**Inputs:**
- the math team's `breadcrumb-warning-traces.json`, hash-checked;
- per-root state data from `mass_core` at the named fixture only (order 17, graph 3, roots 3 and 13), as in `docs/deadend/data.js`.

No census, holdout or orders beyond 20.

## Part 1: description (root 3 in raw labels; root 13 stated separately)

These facts are already computed for the demo. They are listed so the test can re-derive them independently.

1. **The dead-end region D₃.** These are the colourings with no chain of strictly decreasing two-swap macros to a target that avoids the strict traps. It has 10 elements. Exactly 5 are strict two-swap traps (R 1842); the other 5, the *twins* (R 1850), each have a decreasing two-swap macro, but every such macro ends in a trap. D₃ equals the set of colourings warned in the frozen breadcrumb runs at root 3.
2. **Pits.** Within D₃, single swaps join each trap only to its own twin. That gives 5 *pits*, {trap, twin}. Each pair differs at the opposite hub 13 and one of its neighbours: {13,16}, {12,13}, {6,13}, {7,13} and {13,14} at root 3. At root 13 the opposite hub is 3: {3,10}, {3,9}, {3,4}, {0,3} and {2,3}. The test will identify the swapped component, meaning its colour pair and vertex set, rather than infer it from the difference.
3. **The rim.** The 20 states one swap from D₃ have R between 1866 and 1873, and none is a target. Ten *connectors* (R 1873) each touch two cyclically adjacent pits, crossing trap to twin. The other ten touch one pit.
4. **Symmetry.** The stabiliser of root 3 has order 10: 5 rotations and 5 reflections, all fixing vertex 13. The 5 traps form one orbit under it, and so do the 5 twins. No stabiliser element maps a trap to its own twin.
5. **Moves between pits.** No single decreasing swap leaves a pit. Two-swap macros pass from a twin over a connector into a neighbouring pit's trap. The test will list every such macro.
6. **Independent switches (the math team's concern).** For each pit, record the interior component whose swap toggles trap and twin. Then test whether toggles at two different pits can be applied together, starting from one state, to give another state in D₃ or on the rim. If they can, multiplicity can grow by combining switches, and the charging below is at risk.

## Part 2: charging candidate C7d (bounded fibre)

**Definitions.** For a warned colouring c at root r:
- Stab(r) is the group of automorphisms of T fixing r. It is computable in polynomial time, and |Stab(r)| ≤ 10: such a map is fixed by the image of one dart at r and an orientation.
- τ(c) ∈ {strict, non-strict} records whether c is strictly two-swap stuck. This is polynomial to check: at most (6n)² macros.
- Pat(c) is the WP7c pattern.
- **χ(c)** is the pair (Stab(r)-orbit of Pat(c), τ(c)). Stab(r) acts on boundary positions, and colours are renormalised after the action.

**Claim C7d.** In every breadcrumb run, any two warned colourings with equal χ lie in **one** Stab(r)-orbit of colourings, up to colour renaming.

**What it gives, and what it does not.**
- **The fibre is bounded by symmetry, not by pits.** The fibre of χ within a run has size at most |Stab(r)| ≤ 10. χ deliberately merges symmetric pits: at root 3, all 5 traps share one χ value. As the math team notes, the bound is on symmetries, not on the number of pits. A run that met 11 pits, or two non-symmetric pits with the same χ, would refute C7d.
- **A conditional warning bound.** If C7d held for every T, the warnings per run would be at most 10 × |{χ values}|. The number of χ values is a constant independent of n, so the warning bound would be constant. That is far stronger than needed, which is a reason to expect C7d to fail on larger graphs and to look for its first failure, not its confirmation.
- **Fixture evidence is only a sanity check.** The fixture traces contain at most 4 warnings per run, so passing them is weak evidence.

**Kill.** A run with two warned colourings that have equal χ and are not related by any element of Stab(r), with colour renaming allowed. We record both colourings, χ and the run.

## Part 3: what is reported

- the Part 1 facts, re-derived;
- the toggle components;
- the joint-switch results;
- C7d on all 39 warned runs (12 roots);
- the number of distinct χ values observed.

Any extension beyond the existing corpus, aimed at finding a C7d failure, requires joint agreement first.

## Amendment before running (after the math team's reply)

The math team independently confirmed the fixture counts: 5 trap/twin pairs, 10 crossed connectors at R = 1873, and 10 spurs at R = 1866. They also confirmed that one four-warning run warns three traps and one twin, so multiplicity is essential. The demo caption is corrected: the spurs are not dead ends.

**What C7d risks, stated explicitly.** Two finite-looking objects fail in opposite ways:
- **Stab(r)-orbits of complete colourings** have bounded size, at most 10, but **the number of orbits is not bounded**.
- **The boundary-pattern quotient Pat** has finitely many values, but **its fibres can contain arbitrarily many interior variants**.

C7d bets on a combination: χ takes finitely many values (from Pat, up to symmetry, plus τ), and **within one run** each χ-fibre of warned colourings lies in a **single** orbit. So C7d asserts that a run never warns two non-symmetric interior variants with the same χ.

That is exactly where the pattern quotient's unbounded fibres would show up. The order-17, graph-3 fixture is consistent with this only because its trap/twin variants differ in τ. Nothing here suggests the bet holds on larger graphs. Its failure would be a witness of non-symmetric interior variants within one run, which is the useful outcome.

The protocol is unchanged.
