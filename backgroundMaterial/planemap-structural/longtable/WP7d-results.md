# WP7d results: the order-17, graph-3 dead-end region, and C7d

Long Table, 4 October 2026. This follows [WP7d-declaration.md](WP7d-declaration.md), declared in `c481ee7` and amended in `15effb4`, both before the run. The run is `wp7d_test.py`, which writes `wp7d-results.json`. These are facts, not status claims. Root 3 and root 13 are reported in their own raw labels.

## Part 1: structure, re-derived

| | Root 3 | Root 13 |
|---|---|---|
| Dead-end region | 10 = 5 strict two-swap traps + 5 twins | same |
| Pits (single-swap components of the region) | 5, each {trap, twin} | 5 |
| Rim | 20 states = 10 connectors at R 1873 (each touches two pits) + 10 spurs at R 1866 (each touches one) | same |
| Root stabiliser | order 10; traps form one orbit of 5; twins one orbit of 5 | same |
| Trap mapped to its own twin by a symmetry | never | never |
| Two-swap macros between pits | 10, each twin → connector → neighbouring pit's trap, R 1850 → 1842 | 10 |

This agrees with the math team's independent count.

**The toggle component.** In each pit, the trap and twin are joined by swapping a **two-vertex chain at the opposite hub**. Equivalently, one can swap the six-vertex component of the same colour pair; the two give the same colouring up to renaming. At root 3 the chains are:
- {13, 16} in the (1,3) pair;
- {12, 13} in (0,1);
- {6, 13} in (0,2);
- {7, 13} in (0,2);
- {13, 14} in (1,2).

At root 13 they are {3, 10}, {3, 9} and {3, 4} in (1,3), {0, 3} in (0,3) and {2, 3} in (2,3).

**Independent switches: none at this fixture.** In every one of the 20 dead-end states, the only toggle set that is a bichromatic component is that pit's own. The other four pits' toggle sets never form components there. So toggles cannot be combined: a dead-end state offers exactly one toggle, and it leads to its pit partner. That is the math team's main obstruction to extrapolating a constant multiplicity, and it does not arise here. It may well arise on larger or less symmetric graphs.

## Part 2: C7d

The claim: within a run, warned colourings with equal χ, where χ = (Stab(r)-orbit of Pat, strict or not), lie in one Stab(r)-orbit.

- **No kills** in any of the 39 warned runs at the 12 roots.
- 14 distinct χ values were observed.
- The most warnings sharing one χ in a run is **3**: the three symmetric traps of the four-warning runs at order 17, graph 3. Their twin has a different τ.

**Reading the result.** This is weak evidence. Every run has at most 4 warnings, and away from order 17, graph 3, every warned set is a single colouring or a pair with distinct patterns. As the amended declaration says, C7d bets that a run never warns two *non-symmetric* interior variants with the same χ. If true for all T, that would give a constant warning bound, so we expect it to fail on larger graphs. Its first failure is the useful output.

## What WP7 now offers the warning-bound problem

**A concrete mechanism at the only multi-pit fixture.** There is a ring of symmetric pits. Each pit is a locked boundary plus one interior two-vertex toggle at the opposite hub. The pits are linked by connectors above them. No independent switching is possible.

**Two open questions, both needing graphs beyond this corpus**, which require joint agreement:
1. Can pits multiply without symmetry, through independent interior toggles? That would break C7d.
2. Can a ring contain more pits than the root stabiliser has elements? That would break any symmetry-based bound.

## Addendum: the math team's two reporting clarifications

The math team's review (`2026-10-04-math-to-longtable-c7d-review-complete.md`) keeps the C7d result under the declaration and amendment actually tested, with the timing disclosure. No rerun of C7d is needed. Two reporting fixes are applied in `wp7d_test.py`, and `wp7d-results.json` is regenerated.

1. **Exact fibre size.** The maximum number of warnings sharing one χ in a run is now computed directly, with a Counter. Before, it was the upper bound warnings − distinct χ + 1. The exact maximum is **3**, the same value: the three-trap witness attains it.
2. **Switch scope.** The earlier check used only the first stored representative of each pit's toggle. It now tests both representatives, the two-vertex chain at the opposite hub and its complementary six-vertex component, and adds a two-step composition test:
   - **Fixed-set availability, both representatives:** in all 10 dead-end states at each root, the only toggle set that is a legal component is the pit's own. That is 20 cases per root, two representatives each. **No other pit's toggle set is a component, in either representative.**
   - **Two-step composition, recomputed:** from every dead-end state, after *every* legal first move with components recomputed, no other pit's toggle representative is a legal second move. That is **0 cases** at both roots.

**Scope.** The composition test covers two steps starting from the dead-end region. It does not cover longer sequences, or switches started from the rim.

**A candidate structural reason, as a hypothesis only.** All five toggles at a root pass through the **same vertex**, the opposite hub. A toggle {h, x} is a two-vertex component in some pair exactly when x is the only neighbour of h in its colour, and h is the only neighbour of x in h's colour. Toggles of different pits use different neighbours x of the same h. Applying any of them recolours h, which changes the uniqueness conditions the others depend on.

If that is the mechanism, interior variants at this fixture cannot accumulate because their switches **share a vertex**. Independent accumulation would need toggles on disjoint vertex sets. The precise hypotheses, and whether they can be stated without the fixture's symmetry, are the next thing to write down. Per the math team's guidance, they will be recorded as hypotheses, not generalised by symmetry.
