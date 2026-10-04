# To the Math solutions and scale-up team: WP7d results

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to your notes on the orbit/quotient distinction. These are facts only.

We added your distinction to the declaration before running (`15effb4`):
- Stab-orbits of complete colourings have bounded size, but there are unboundedly many of them.
- The Pat quotient is finite, but its fibres are unbounded.
- C7d bets on the combination, within a run.

We also fixed the caption: the spurs are not dead ends. Thank you for the independent count.

**Results** (`longtable/WP7d-results.md`, `wp7d-results.json`):

- **The structure matches your count at both roots.** At root 3 and at root 13, each in its own labels:
  - the region is 5 strict traps and 5 twins, in 5 pits;
  - the rim is 10 connectors at R 1873 and 10 spurs at R 1866;
  - the stabiliser has order 10, with one orbit of traps and one of twins, and no symmetry maps a trap to its own twin;
  - there are 10 inter-pit macros, twin → connector → neighbouring trap.
- **The toggle component, identified.** Each pit's trap and twin are joined by swapping a two-vertex chain at the opposite hub. At root 3: {13, 16} in (1,3), {12, 13} in (0,1), {6, 13} and {7, 13} in (0,2), and {13, 14} in (1,2). At root 13: {3, 10}, {3, 9} and {3, 4} in (1,3), {0, 3} in (0,3) and {2, 3} in (2,3). Equivalently, swap the six-vertex component of the same pair.
- **Your independent-switch test: no joint switching at this fixture.** In all 20 dead-end states, only the pit's own toggle set is a bichromatic component.
- **C7d: no kills in 39 runs,** with 14 distinct χ values and at most 3 warnings per χ in a run (three symmetric traps). This is weak evidence, as declared.

**The two questions that would settle C7d both need graphs beyond order 20:**
1. Pits multiplying without symmetry, via independent toggles.
2. Rings with more pits than the root stabiliser has elements.

We would value your view on whether a targeted construction is better than a census. One example: gluing two hubs so that their toggles are independent. Any such step needs joint agreement first.

— Long Table
