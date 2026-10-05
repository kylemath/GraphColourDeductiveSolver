# WP7 chain-mass lemmas checked in Lean

4 October 2026. Lemmas 7.1, 7.2 and 7.4 now have compiled statements in the authoritative mathlib4-planemap checkout. No spherical hypothesis is used. The Proof Navigator assigns ledger statuses.

## Statements and scope

- `SimpleGraph.Kempe.pairMass`: sum of squared exterior sizes of distinct active bichromatic components meeting B. Boundary representatives are deduplicated; inactive isolated vertices are excluded. `pairMass_swap_pair` and `pairMass_swap_disjoint` prove locality, and `sixPairMass_swap_change` gives the integer four-mixed-term identity for any four distinct Fin 4 colours. `pairMass_le_card_sq` and `sixPairMass_le_six_card_sq` prove the quadratic bounds.
- `SimpleGraph.Kempe.mixedFixedGraph_kempeSwap` and `bichromatic_kempeSwap_eq_repartition` prove the fixed-graph and active-set statements of 7.2. The ambient vertex type stays fixed, retaining isolated vertices. Mixed-subgraph coverage uses properness. Arbitrary swap sets need properness supplied for both colourings where required; the existing component-swap theorem provides it for legal moves.
- `SimpleGraph.Kempe.singleton_chain_proper_target` proves a free singleton component gives a proper colouring with at most three boundary colours. `singleton_chain_rank_decreases` proves strict decrease of the actual six-pair mass rank. `singleton_locked_of_no_rank_decrease` proves that no one-swap decrease forces every singleton to be linked to another boundary vertex in every pair. The rank carries an explicit n ≥ card V, allowing n to be the order before deletion. This is 7.4, not a claim that locked states have an escape.

Sources are `Mathlib/Combinatorics/SimpleGraph/Coloring/KempeMass.lean`, `KempeRepartition.lean`, and `KempeBoundary.lean` in mathlib4-planemap. Tests are the corresponding `MathlibTest/PlaneMapKempe*.lean` files. Mass is noncomputable; these are mathematical lemmas rather than an executable mass evaluator.

## Validation

The fresh dependency-ordered rebuild passed all **51** custom modules and tests, excluding **532** cached custom artifacts. All earlier 45 source hashes are unchanged. The three new test modules contain **25 exact axiom guards**, each reporting only a subset of `propext`, `Classical.choice`, and `Quot.sound`. A combined-import regression checks compatibility of the three modules.

Fixtures verify component deduplication with actual mass 4, mixed-edge transfer and an isolated active vertex, and a legal swap through an interior vertex that removes a singleton boundary colour and strictly lowers the actual rank. Compiler output and source hashes are in `backgroundMaterial/planemap-structural/kempe-wp7-source-audit.json`, `kempe-wp7-source-audit-output.txt`, and `kempe-wp7-source-SHA256SUMS` (source paths relative to mathlib4-planemap). The audit script now explicitly includes these modules, preventing cached custom imports from substituting for them.

No `sorry`, `admit`, new axiom, `unsafe`, or `native_decide` was introduced. General Four Colour, uniform breadcrumb success, a polynomial warning bound, recursive certificates, and chord availability remain open. The static and dynamic WP7 counterexamples are not contradicted by these lemmas.
