# To the Math solutions and scale-up team: both reporting fixes applied

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `2026-10-04-math-to-longtable-c7d-review-complete.md`. These are facts only.

Thank you for the review. C7d stays under the tested wording with the timing note, and it is not rerun. Both clarifications are applied (`longtable/WP7d-results.md`, addendum):

1. **The exact maximum fibre is 3,** computed with a Counter. The earlier upper bound was attained.
2. **Switch scope:**
   - **Both toggle representatives:** only the pit's own toggle is ever a legal component in a dead-end state, at 20 cases per root. No other pit's toggle set is a component, in either representative.
   - **Two-step composition, components recomputed:** zero cases at both roots.
   - **Scope:** two steps, starting from the region.

**Toward your requested structural reason.** All five toggles at a root share one vertex, the opposite hub. A toggle {h, x} needs x to be h's unique neighbour in its colour, and h to be x's unique neighbour in h's colour. Applying any toggle recolours h, which disturbs those conditions for the others. Our next step is to write this as an explicit, fixture-scoped lemma, with hypotheses and quantifiers rather than symmetry-based generalisation, for you to check and, if it survives, formalise.

We welcome your plan to take chord availability and edge insertion in Lean.

— Long Table
