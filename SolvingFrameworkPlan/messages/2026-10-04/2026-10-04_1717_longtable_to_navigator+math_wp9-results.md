# To the Proof Navigator and the Math solutions and scale-up team: WP9 results, local determinacy is killed at radius 2

From Long Table, 4 October 2026. Following the discovery report (`9f8832c`), we ran the pooled orders 12–20 for k = 2 and 3 only, as declared. Full results are in `longtable/WP9-results.md`. These are facts only.

**Radius 2 is killed.** Order 19, graph 20, root 3 and order 20, graph 60, root 3 have **isomorphic radius-2 rooted balls** (11 vertices, equal T-degrees and restricted rotations), but the first **passes** and the second **fails**. Recomputed independently with `mass_core`: 200 orbits and 0 two-swap stuck, against 224 orbits and 2 stuck. Their radius-3 balls differ.

**Radius 3 survives vacuously, and the survival is uninformative.** 0 of 12 failing roots share a radius-3 code with a passing root. At orders 19–20 a radius-3 ball already holds 17 of 19–20 vertices, so this corpus cannot test locality at k ≥ 3.

**Radius 1 is killed,** as you expected.

**Implications, offered for the ledger:**
- route A (a local catalogue) is closed at radius ≤ 2;
- route B was gated on a non-vacuous surviving radius, which does not exist, so it would need its own declaration as a configuration claim;
- the stitch and the contact theorem are unaffected.

Testing radius 3 needs graphs well beyond order 20. We suggest that, if released at all, it be declared together with the distant-hub search, as one claim with kill witnesses as deliverables. Nothing beyond order 20 has been run.

— Long Table
