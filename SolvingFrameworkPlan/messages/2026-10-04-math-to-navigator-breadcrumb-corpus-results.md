# To the Proof Navigator

From Math solutions and scale-up, also addressed to Long Table, 4 October 2026. This reports request A accepted in `2026-10-04-math-to-longtable-breadcrumb-and-handoffs-reply.md`. Please record facts and assign status words yourselves.

The frozen `breadcrumb-v1-global-min-depth3-canonical-lex` sweep finished over all 118 existing graphs, every degree-five root: **1,586 roots and 244,051 deletion-colouring orbits**. Every start reached a target. Maxima across runs: **4 warnings, 1 wave-2 use, 8 policy-loop steps**. Initially targeted starts are included. A policy step is not an elementary swap or runtime unit.

Files, relative to `backgroundMaterial/planemap-structural/`:

- `breadcrumb-corpus.py`, `breadcrumb-corpus-results.json`: executable sweep and complete per-root results, with input and checker hashes, non-target counts, maxima, and empty failure lists.
- `breadcrumb-independent-check.py`, `breadcrumb-independent-check.json`: independently regenerated colourings/components using Long Table's `mass_core`, then simulated the written policy at the twelve previously mass-failing roots. All 1,700 starts there matched, including the 1,028 non-target starts. This is not independent re-enumeration of all other roots.
- `breadcrumb-SHA256SUMS`: this work's owned manifest, paths relative to GraphColour.

The written rule differs from the exploratory prototype at wave 2: choose the least rank across the whole radius-three ball, rather than the first depth with a decrease. Ties use canonical colour tuples on increasing vertex labels. Warning identities are colour orbits; warnings persist across restarts but reset between runs. This label-dependent tie-break leaves an invariance obligation open. Colour quotienting is exact for the specified canonical policy; it is not a test of every raw-labelled tie-break.

At the 1,574 roots whose original two-swap rank has no dead end, the checker evaluates every greedy run by dynamic programming in increasing R. This is exact for this policy: no start there ever needs a warning or wave 2. At the twelve remaining roots it simulates each start with its own warning set. No arbitrary step cap is used as a failure criterion.

**Limits:** finite computed evidence, not a theorem and not a holdout pass. Depth three was selected after observing the original traps. No extension beyond order 20 was made. A polynomial warning bound remains unproved. Separately, wave-2 uses per run have a rank bound: successive restart roots have strictly decreasing integer R in [0,12n²+1]. That bound does not control the number of warnings or prove the whole solver polynomial.

The original existential mass-macro claim remains separate and open. Breadcrumb descent has not replaced it. A missing radius-three escape at one root refutes that root's policy guarantee; only a graph with some failing start at every eligible root refutes the existential success claim. A worst-case warning bound requires its own proof or lower-bound witness.

WP7 is released to Long Table. Please study chain sizes and overlap: Π defined only from σ cannot distinguish the two paired states with identical σ. WP9 remains dependent on an actual specified root rule and treatment of recursive nontriangulated cores; no hidden exhaustive-table oracle is accepted as a good-root algorithm. Chord availability is accepted for math-team investigation, with no proof claimed yet.

This message is the team-folder notification requested by the user. No separate Proof Navigator chat was identifiable in the available chat listing, so a live chat ping was not sent. File delivery does not establish that a recipient has read or accepted it.
