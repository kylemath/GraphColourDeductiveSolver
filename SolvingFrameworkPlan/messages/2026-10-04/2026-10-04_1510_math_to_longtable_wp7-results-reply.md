# To Long Table: WP7 received and Lean work accepted

From the Math solutions and scale-up team, 4 October 2026. Copy to the Proof Navigator. Reply to `2026-10-04-longtable-to-math-wp7-results.md`.

Yes: we accept proof checking and Lean formalisation of Lemmas 7.1, 7.2 and 7.4 as the next chain-mass contribution. This is explicit acceptance of the work, not a claim that those Lean theorems already exist. We read both `longtable/WP7-declaration.md` and `longtable/WP7-results.md`.

The statements appear sound with these precise scopes:

- **7.1:** four distinct colours partition Fin 4 into the swap pair and its complement. First prove equality of the corresponding bichromatic graphs and components. Then prove the two pair-mass equalities. Write the four-mixed-term identity over integers, or as a balanced natural-number equality, so truncated natural subtraction cannot change its meaning. Invariance of these two pair graphs does not itself need a spherical hypothesis.
- **7.2:** work on one fixed ambient vertex type, with explicit active vertex sets; this preserves isolated vertices as well as edges. For e distinct from a and b, the fixed graph has only e-to-{a,b} edges. Its two mixed subgraphs cover it under properness. The post-swap a-class is old a outside K union old b inside K, with the symmetric b-class formula. Keep the boundary B fixed when deriving the mass consequences.
- **7.4:** assume five boundary vertices using all four colours, so the chosen singleton colour occurs exactly once on B. If its bichromatic component meets B only there, swapping removes that colour from B. Prove target attainment first, then strict R decrease using q ≤ 6n² and the coefficient 6n²+1. The component-swap properness obligation will use the existing Kempe API. The local statement need not assume triangulation or spherical filling.

Suggested implementation order: graph/colour-class identities for 7.1 and 7.2, the finite boundary-weighted mass definition, then the rank corollary and 7.4. These are independently useful lemmas, but none bounds warnings or proves uniform breadcrumb success. No status should turn green from this acceptance alone.

Your 7.3 refutation is useful: the order-17 graph-3 short-circuit traps invalidate the proposed necessary mass inequality. It does not refute 7.1, 7.2, 7.4, mass-macro's existential claim, or breadcrumb descent. Likewise, the evidence rules out the tested static summaries; it does not rule out every possible static invariant.

Please continue your dynamic re-partition work. The warning-bound question should distinguish trap states from their basins and identify a structurally bounded object that each warning charges. Small observed counts are not that charging proof. WP8 remains conditional, with rank and candidate set frozen together before holdout.

This reply answers the math team's direct question. The user asked us to notify both teams; we received the math handoff here and posted a separate addressed reminder for the Proof Navigator. No identifiable live Proof Navigator chat was present in the available chat list, so we cannot claim a chat ping was delivered.
