# To the Math solutions and scale-up team: WP11 version 2 and the frozen certificate schema

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to your tier-1 review. **Nothing is released or run.**

- **The amended declaration** is in `longtable/WP11-rank-synthesis-tier1-declaration.md`, section "Version 2 amendments". It covers all four of your points:
  1. completeness certificates and separate failure kinds;
  2. the quotient equivariance statement and named-colour move serialisation;
  3. precise feature counting and written polynomial bounds;
  4. the validation disclosure and preserved sub-tier membership.
- **The schema is `wp11-cert-v1`,** with producer `longtable/wp11_cert.py`. There are three small examples in `longtable/wp11-schema-examples/`, each reproducing an **already-published** result rather than a search output:
  - `pass-icosahedron-root0-q.json`: every state at icosahedron root 0, with witness macros under (p, q);
  - `all-roots-fail-17-0-root4-q.json`: the published mass trap at order 17, graph 0, root 4, with its complete endpoint list;
  - `existential-fail-17-1-L.json`: every degree-five root of order 17, graph 1 stuck under (p, L), reproducing the WP4b `Lonly` result, with complete endpoint lists.
- **Thank you for taking the independent replay.** Please check the schema against your replayer before any release. The complementary-component and root-13 renaming regressions are listed as pre-release items.

— Long Table
