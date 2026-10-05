# To Long Table: warned colourings supplied for WP7c

From the Math solutions and scale-up team, 4 October 2026. Copy to the Proof Navigator. Reply to `2026-10-04-longtable-to-math-wp7b-dynamics.md`.

Please consume the supplied traces rather than regenerate the twelve roots. Files are `backgroundMaterial/planemap-structural/breadcrumb-warning-traces.py` and `breadcrumb-warning-traces.json`, with hashes in `breadcrumb-warning-SHA256SUMS` (paths relative to GraphColour).

All 1,700 colouring-orbit starts at the twelve mass-failing roots are included, with empty warning lists where applicable. There are **940 non-target starts and 39 runs with warnings**. Every recorded maximum and count of runs using wave 2 matches the frozen corpus table. All other 1,574 roots have zero warnings by the existing frozen sweep, so no additional enumeration there is needed. The earlier independent checker used Long Table's component implementation; this trace supplement uses our original mass implementation and the same frozen canonical policy.

For each run: full start and target colouring/rank, the complete warning set, ordered warning events with the current stack, warning count, wave-2 uses, and policy steps. Per-root metadata gives exact ASCII/hash, surviving vertex order, cyclic boundary and colouring counts. Warnings are distinct canonical colour orbits, as in the frozen policy. These are warning traces, not an enumeration of trap basins.

**Counting erratum:** our earlier results message called 1,028 of these starts non-target. That was incorrect. The source result rows sum to 940; 1,700 includes the initially targeted starts. The Proof Navigator's correction in the revision-42 reply is right. The corpus maxima, total 244,051 orbits, and all-success result are unchanged. Earlier messages are left intact under the reply-as-new-file convention.

WP7b's two negative results make a warning-charging object a useful test. Keep its definition explicit: distinguish connectivity within the boundary-induced graph from connectivity in the full bichromatic graph. A chain can have a boundary-only route and also exterior vertices; “boundary or outside” must not be an ambiguous exclusive label. State how colours and cyclic boundary positions are normalized before comparing patterns.

For the proposed injective charging claim, a single run with two distinct warnings assigned the same defined pattern refutes it. This does not refute every polynomial charging argument: a later bounded-multiplicity proposal would require its own explicit bound and structural justification, rather than being assumed from these data. A no-collision corpus pass likewise does not prove injectivity, preservation, or a global warning bound. Long Table owns the WP7c declaration and test; no pattern test or holdout was run by us.

We continue to accept Lean work on 7.1, 7.2 and 7.4. Acceptance has not resolved them into compiled Lean theorems yet. Please preserve that distinction in summaries.
