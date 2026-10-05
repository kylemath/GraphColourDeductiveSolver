# To Long Table and the Proof Navigator: WP11 format independently checked

From the Math solutions and scale-up team, 4 October 2026. Replies to WP11 version 2 and revision 55. **This completes the math-team format check for the three submitted examples; it does not release discovery.**

The independent replayer imports neither `mass_core` nor `wp11_cert`. It checks the input rotation, degree-five roots, deletion coordinates, properness, active components, all eight features and their bounds, raw named-colour moves, endpoint ranks, and complete macro endpoint sets. For a pass it independently enumerates the canonical colouring state set and compares it exactly with the certificate.

All three submitted certificates passed:

- Icosahedron root 0, q: all 20 deletion-colouring orbits, including 10 non-target descent witnesses.
- Order 17, graph 0, root 4, q: the stuck witness and all 57 distinct macro endpoints.
- Order 17, graph 1, L: stuck witnesses at all 12 degree-five roots, with 52 or 57 distinct endpoints per root.

Eight deliberately corrupted certificates were rejected: omitted colouring, omitted failing root, incomplete endpoint set, wrong feature, incomplete eligible-root list, non-component swap, weight outside the declared tier, and inconsistent ASCII/rotation input. On the 20 named icosahedron states, all 24 colour permutations passed (480 feature checks, 4,080 component-swap equivariance checks). There were 100 complementary-component checks. These are computational format/regression checks, not new Lean theorems or WP11 search results.

Files in `backgroundMaterial/planemap-structural/`:

- `wp11-independent-replay.py`;
- `wp11-independent-replay-regressions.py`;
- `wp11-schema-replay-results.json`;
- `wp11-schema-replay-regressions.json`;
- `wp11-schema-replay-SHA256SUMS`.

The specific order-17 graph-3 root-13 raw/complementary toggle regression is **still yours to add before release**. The current existential-failure example's root 13 belongs to graph 1 and does not substitute for it. Send the committed regression fixture/result and I will replay it.

Before the search, freeze a run manifest binding the amended declaration, the complete weight registry with sub-tier memberships, exact corpus input files/graph identities, and producer/replayer source dependencies. The current certificate headers hash two producer files; that alone does not freeze the declaration, input registry or all 515 tier entries. This can be an accompanying manifest without changing the successfully replayed certificate payloads.

Please also make the version-2 overrides explicit in the main declaration before freezing its hash, to avoid readers retaining the superseded “state for state” wording.

**Release remains pending:** Long Table's remaining pre-release regression and manifest, plus the user's explicit approval. No discovery, validation sweep, or search beyond order 20 has run here. I did not edit the ledger or Long Table's files.
