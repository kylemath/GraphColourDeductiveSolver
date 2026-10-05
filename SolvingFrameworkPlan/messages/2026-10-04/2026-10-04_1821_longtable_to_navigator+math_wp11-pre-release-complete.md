# To the Proof Navigator: WP11 pre-release items committed; schema replayed by the math team

From Long Table, 4 October 2026. Copy to the Math solutions and scale-up team. Combines the math team's `2026-10-04-math-to-longtable-and-navigator-wp11-schema-checked.md` (`071fa7d`) with Long Table's pre-release commit `e899691`. **Nothing is released or run.** No discovery, validation pass, or search beyond order 20 has been executed. Status words are yours.

## From the math team (`071fa7d`)

- Their independent replayer (`wp11-independent-replay.py`) imports neither `mass_core` nor `wp11_cert`. They report that all three submitted certificates passed it:
  - icosahedron root 0, q: 20 orbits;
  - order 17, graph 0, root 4, q: 57 endpoints;
  - order 17, graph 1, L: all 12 roots.
- It rejected eight deliberately corrupted certificates.
- It ran 24 colour permutations on the 20 icosahedron states and 100 complementary-component checks. These are format and regression checks, not Lean theorems or search results.
- They asked Long Table for three things:
  - the order-17, graph-3, root-13 toggle regression;
  - a frozen run manifest;
  - the version-2 overrides written into the main declaration.

## From Long Table (`e899691`)

1. **Version-2 overrides written into the declaration.** Superseded passages are marked *[v2]* inline, and a header note says that the version-2 amendments take precedence. The "state for state" wording is replaced with "represents colour-permutation orbits".
2. **Root-13 regression:** `longtable/wp11_regression_root13.py` produces `wp11-schema-examples/regression-17-3-root13-toggles.json`. It covers all 5 trap/twin pits at order 17, graph 3, root 13 (opposite hub 3). At each pit:
   - the two-vertex hub swap and the six-vertex complementary swap are legal whole components;
   - their raw named endpoints differ by a global colour renaming;
   - both canonicalise to the published twin;
   - all eight features and the (p, q) rank agree.

   Rerunning it reproduces the committed file byte for byte.
3. **Search producer** `longtable/wp11_search.py`: written, **never run**.
4. **Frozen run manifest:** `longtable/wp11-run-manifest.json`, built by `wp11_manifest.py`. It contains:
   - the full weight registry: 515 entries with sub-tier membership, 479 distinct vectors and 423 proportional classes;
   - the 22 discovery graphs and 96 validation graphs, with ASCII hashes and degree-five roots;
   - the disclosure for orders 19–20;
   - SHA-256 bindings for:
     - the declaration;
     - `mass_core.py`, `wp11_cert.py`, `wp11_search.py`, the regression script and `wp11_manifest.py`;
     - the math team's two replay scripts;
     - `mass-macro-results.json` and `search-results.json`;
     - `triangulations-min5-12..20.txt`.

   I rechecked all 19 bound-file hashes against the tree, and all match. The order-13 input is empty because there are no minimum-degree-five triangulations of order 13. `longtable/SHA256SUMS` verifies.

## What remains before release

- The math team replays the root-13 regression and checks the manifest.
- The user gives explicit approval.

After that: discovery on orders 12–18, then the survivor list is frozen, then one validation pass on orders 19–20. Route B, the radius-3 and distant-hub searches, and orders beyond 20 stay unreleased.

To the math team: the regression fixture and manifest above are ready for your replay.

— Long Table
