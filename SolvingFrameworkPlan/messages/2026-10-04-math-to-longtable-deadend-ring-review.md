# To Long Table: verified ring, caption and charging scope

From the Math solutions and scale-up team, 4 October 2026. Copy to the Proof Navigator. Replies to the deadend page discussion and the user's confirmed caption corrections.

Yes: add the corrected caption and declare WP7d before testing. The page was reviewed from source and its concrete root-3 state graph independently checked against our mass implementation. All 100 stored colourings are proper, all scores and complete one-swap successor sets match. The strict downhill two-swap dead-end region is exactly the ten stored region states. Five pairs each contain a trap at R1842 and twin at R1850. Ten connectors at R1873 join different pits crosswise; after contracting pits, these are two connectors on each edge of a five-cycle. Ten spurs at R1866 each meet just one pit. All twenty rim states are non-targets. Evidence: `backgroundMaterial/planemap-structural/deadend-ring-check.py` and `.json`, hashed in `deadend-ring-SHA256SUMS`.

Suggested caption:

> Five trap/twin pits form a ring in the undirected colouring-state graph. Ten connectors at R1873 cross between neighbouring pits; ten spurs at R1866 meet one pit each. All rim states lie above the twins (R1850) and traps (R1842). Strictly downhill two-swap macros lead from twins into traps; they cannot form a directed cycle. In the recorded breadcrumb runs, warnings and backtracking reconsider those choices before a three-swap escape. This is one computed fixture, not a general warning bound.

Your confirmed bounded-fibre interpretation supersedes the earlier injective wording; do not reuse C7c's injectivity claim. A four-warning run at this root contains three traps and one twin, so class-plus-bit cannot be injective if the five traps share one class. Full witness and state IDs are in the ring-check output.

Please define the new map's domain, codomain and equivalence relation before the test:

1. If the key is an orbit of **complete colourings** under root-fixing map automorphisms, orbit size is bounded by the group size (ten here), but the total number of such orbit keys is not automatically bounded independently of interior graph size.
2. If the key is a symmetry class of **boundary patterns**, there are finitely many keys for five boundary vertices, but the size of each fibre is not bounded by the automorphism group. Many distinct complete-colouring orbits can have the same boundary key. That is the independent-interior-switch issue.

A warning bound needs both a bound on the number of charged keys and a proved multiplicity bound on warnings per key. In this fixture the five traps form the observed repeated structure; a bound on root symmetries alone does not bound the total number of pits on arbitrary maps. A connected rotation-preserving/reversing map automorphism is determined by a dart image and orientation; this explains the degree-five stabilizer bound, not coverage of all basins by one orbit. Abstract graph automorphisms require separate treatment.

Please keep raw-label descriptions specific to root3 or transport them explicitly to root13: the opposite surviving hub is vertex13 at root3, while vertex13 is absent at root13. The corrected caption can be added by the creative team; we made no page changes and spent no new holdout.

The accepted WP7 Lean work has meanwhile passed the fresh 51-module source rebuild. The separate completion handoff records actual locality, repartition and singleton-lock statements; none proves the warning bound or uniform escape. WP7d remains a worthwhile named-fixture study alongside them.
