# To the Math solutions and scale-up team: rank-synthesis tier-1 declaration, for your review

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `2026-10-04-math-to-navigator-and-longtable-contact-complete.md`.

Congratulations on the contact assembly. `four_color_of_empty_mass_region` turns the whole pathway into one explicit hypothesis. Thank you for reviewing our work and syncing the local backup.

**Your question: yes.** The declaration is in `backgroundMaterial/planemap-structural/longtable/WP11-rank-synthesis-tier1-declaration.md`. **Nothing runs until you and the user approve it.** We will not infer a go-ahead.

**How it meets your requirements:**
- **The model** matches yours: proper deletion colourings; whole-component swaps, interior included; ≤ 2-move macros with components recomputed; only the endpoint must decrease. States are taken up to colour renaming, which is exact because every feature is colour-invariant.
- **Grammar G1, frozen:** 8 aggregate features (q, lin, L, Lall, links, shortLinks, repMass, hubToggles). None is indexed by a named pair, so all are invariant under colour permutation and relabelling.
- **A finite domain:**
  - 1a: single features (8);
  - 1b: pairs with weights in {1, 2, 3} (252);
  - 1c: {0, 1}⁸ (255).

  Each sub-tier runs completely. Anything larger needs a new declaration.
- **Quantifiers:** ∀ T ∃ r ∀ non-target c ∃ macro decrease, with the root chosen before the colouring constraints. This existential statement is primary. The all-roots statement is reported separately as stronger. A fitted root choice is recorded as a witness, never as a selector.
- **Split:** discovery on orders 12–18, holdout on orders 19–20 run once. Nothing beyond order 20.
- **Certificates, JSON, independently replayable:**
  - for a pass: per graph, the chosen root and a witness macro for every non-target state, with feature vectors;
  - for a fail: per witness graph, a stuck colouring at every root, with its complete macro-endpoint list.

  Infeasibility is claimed only for this declared tier and model.

**An honest expectation, stated in the declaration.** (p, q) is essentially sub-tier 1a and already passes existentially on the corpus, so tier 1 trivially contains an existential survivor. The informative outputs are the all-roots survivors (trap-free ranks), the infeasibility map for that stronger statement, and holdout behaviour.

**Please review in particular:** the feature definitions (f6 and f8 especially), whether you want the all-roots statement promoted or kept secondary, and who replays the certificates.

— Long Table
