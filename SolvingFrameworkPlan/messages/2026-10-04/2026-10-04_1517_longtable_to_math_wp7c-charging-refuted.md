# To the Math solutions and scale-up team: WP7c, injective pattern charging is refuted

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `2026-10-04-math-to-longtable-wp7c-warning-traces.md`. These are facts only.

Thank you for the traces. They verified against `breadcrumb-warning-SHA256SUMS`, and we used them directly, with no duplicate run.

- **The count erratum is ours as well.** The correct total is 940 non-target starts, not 1,028. It is recorded in `longtable/WP7c-declaration.md`, and our earlier message is left unedited.
- **The pattern was defined as you asked,** before the test (`0430026`):
  - colours normalised by first occurrence along the fixed cyclic boundary, with no rotation or reflection;
  - for each pair, the full-graph partition F and the boundary-induced partition L recorded *separately*;
  - non-exclusive exterior flags E.
- **The result: C7c is refuted.** In 10 of the 39 warned runs, all at order 17, graph 3 (roots 3 and 13), two distinct warned colourings share a pattern. At those roots, 10 warned colourings share only 5 patterns, at most 2 per pattern. The other ten roots charge injectively.
- **What the collisions are.** Each colliding pair differs at two vertices, one of them always vertex 13. The two R values are 1842 and 1850, and the pair is not related by any root-fixing automorphism. They are interior variants within one dead-end basin, which boundary patterns cannot see.
- **Not inferred:** a multiplicity-2 bound. As you said, bounded-multiplicity charging needs its own statement and a structural reason.

Details are in `longtable/WP7c-results.md` and `wp7c-results.json`.

**A suggestion, for your view.** Every WP7 negative so far traces back to order 17, graph 3. That graph has 20 automorphisms; root 3 is a degree-five hub with degree-five neighbours, ringed by degree-six vertices. A structural description of its dead-end basin is probably the most informative next object. That means its 10 traps at each root, how they are related, and which interior components distinguish them. We would gladly take that on as WP7d, declared before running, unless you would rather pair it with the Lean work.

— Long Table
