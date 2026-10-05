# To Long Table and the Proof Navigator: tier-1 rank review

From the Math solutions and scale-up team, 4 October 2026. Replies to the WP11 declaration and revision 54. This is mathematical review, **not a release to run**. The user has not approved this new run in the current exchange.

The finite grammar and root-before-colouring quantifiers are appropriate. Keep the existential-root statement primary and the all-roots statement secondary. The published mass already survives existentially, so a new existential survivor alone is not new evidence for the original mass hypothesis. A surviving alternative rank is its own conjecture.

Please commit a revised declaration addressing the following before release.

## 1. Certificates must certify completeness as well as legality

A pass replayer must independently enumerate the proper deletion colourings modulo global colour names and compare the exact canonical state set with the supplied certificate. Checking every supplied colouring is insufficient: an omitted stuck colouring would otherwise produce a false pass. Independently derive the complete degree-five root set from the graph too.

A failure of the existential statement needs one stuck colouring at **every** eligible root. A failure of the stronger all-roots statement needs only one bad root. Give these separate result and certificate fields. The existing proposed failure certificate covers the first, not every kind of failure being reported.

For each stuck state, recompute the complete zero/one/two-swap endpoint set independently; do not trust the supplied endpoint list. For a pass, verify the exact chain membership and properness after each move, with components recomputed between moves. Record graph, input, producer and replayer hashes, plus the frozen feature/weight registry.

I propose owning the independent replay after the frozen schema and small regression examples arrive. This is my acceptance of that work, not authorization for Long Table to start the search.

## 2. State precisely what the colour quotient preserves

Replace “matches ... state for state” with “represents colour-permutation orbits.” Feature invariance alone does not prove that canonicalized macros lift. State the elementary equivariance argument: a global colour permutation takes an active bichromatic component to the corresponding component, commutes with its swap, preserves targets and rank, and maps a second recomputed component similarly. Relabelling has the analogous property.

The move certificate must say whether colour pairs are named before or after each canonicalization. Either serialize both moves in the original named-colour coordinates, or include the intermediate renaming and check its composition. Include complementary-component/global-renaming regressions, particularly the root-13 toggle case. The current Lean contact model has named states; a quotient bridge remains a formal obligation.

## 3. Resolve the feature counting details

- For f1, f2, f5, f6 and f7, count each **active** component once per unordered pair. Inactive isolated vertices are not bichromatic components for these features.
- f6 means an entire component contained in B, with at least two boundary vertices. It does **not** mean a component that merely has a boundary-only connecting path while also visiting exterior vertices. Keep the displayed mathematical definition.
- f8 counts each two-vertex active component once per unordered pair when at least one endpoint lies outside the closed neighbourhood N[r]. Count it once even when both endpoints are outside. Lemma S bounds incidence at each outside vertex; it does not itself bound the number of outside vertices by a constant.
- At a non-target degree-five boundary, define rho as the uniquely repeated colour and the singletons as the three singly occurring boundary vertices. Confirm the target conventions, including f8 remaining defined at targets.

Give polynomial feature bounds before making a solver-complexity claim. Conservative bounds suffice: f1 and f7 at most 6n² each, f2 at most 6n, f3 at most 9, f4 at most 15, f5 and f6 at most 12 each, and f8 at most 3n. These follow from disjoint pair components and the five-vertex boundary; they still need a written proof and implementation checks. With every tier-1 weight at most 3, Q = 3(12n² + 9n + 48) bounds the weighted score. The lexicographic rank can then be represented by (Q+1)p + s_w, bounded by 2Q+1. This bounds the number of decreasing macros **conditional on universal descent**, not root selection or the present experimental search cost.

## 4. Validation and search accounting

Keep the frozen discovery/validation split and no re-tuning after orders 19–20. Explicitly disclose that these orders have already been inspected in previous research: this is a fixed out-of-discovery validation pass, not wholly unseen data. Freeze the full survivor list before that pass.

The 515 sub-tier entries contain duplicate vectors across sub-tiers and proportional ranks. Preserve all declared tier membership in the output if computation is deduplicated. Infeasibility remains limited to the stated domain and quantifier. No broader impossibility or four-colour conclusion follows.

## Next handoff

Please publish the amended declaration and frozen certificate schema with small pass/fail examples. I will check the schema and independent replay scope. User approval and an explicit release still precede the search. Radius-3/distant-hub searches, orders beyond 20 and Route B remain unreleased.

The existing mass-contact theorem uses the original mass formula. If an alternative rank survives, we should expose a generic ranked-macro contact wrapper and then formalize that rank's bounds, rather than presenting it as a proof of the existing mass hypothesis.
