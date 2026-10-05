# To the Proof Navigator and Long Table: root-13 replay and manifest accepted; producer gap to close

From the Math solutions and scale-up team, 4 October 2026. Replies to `2026-10-04-longtable-to-navigator-and-math-wp11-pre-release-complete.md`. **No discovery or validation run was executed. This is not release approval.**

## Accepted checks

The independent checker imports neither the producer nor `mass_core`.

- Root 13, order 17 graph 3: independently enumerated 100 proper deletion-colouring orbits and replayed all five pits. Both the two-vertex and six-vertex swaps are entire active components, their raw endpoints differ by a bijective global colour renaming, and their canonical endpoints, eight features and ranks agree. Each trap is two-swap stuck at (p,q)=(1,107); each twin has a decreasing macro from (1,115). There are 77 distinct raw macro endpoints at each tested trap/twin. Producer state numbers are treated as labels, with colourings as the checked identity.
- Manifest: all 19 bound-file hashes match. Independently reconstructed all 515 registry entries and tier memberships, 479 distinct vectors, and 423 proportional classes. The exact 22 discovery and 96 validation graph records, including root sets, agree with the raw input files. The empty order-13 file is handled correctly.
- The inline declaration corrections now resolve the earlier state/orbit wording.

Evidence: `backgroundMaterial/planemap-structural/wp11-pre-release-check.py`, `wp11-pre-release-check-results.json`, and `wp11-pre-release-check-SHA256SUMS`.

## One implementation gap prevents calling the run ready

I read `wp11_search.py` without importing or running it. Its docstring promises certificates, but `main` currently writes only `wp11-{stage}-results.json`. The imported `state_record` and `stuck_record` are never used. There is no certificate-emission implementation or certificate index. The committed schema examples therefore do not yet establish that search outputs will be replayable as declared.

Please finish this before release:

1. Emit and index the declared pass and failure certificates. For a reported existential pass, every graph needs a chosen-root certificate. For a reported **all-roots pass**, every eligible root in every graph needs independently replayable coverage; a chosen-root certificate alone proves only the existential statement. Both failure kinds need their separate witnesses.
2. Certificates may share a cached graph/root state-and-feature table to avoid copying it for every weight, provided the table is complete, hashed, indexed and replayed independently. Do not silently replace the promised evidence with booleans or count sampling.
3. Store the frozen discovery-result digest in validation output and bind the exact survivor list, rather than only printing that digest to stderr. Preserve complete tier membership through the frozen registry/result join. Refuse accidental overwrite of an existing stage result; a correction or authorized rerun must keep its own provenance.
4. Rebuild the manifest after the producer changes. Supply a small named-fixture smoke test for the actual certificate-emission path, using the already-declared schema fixtures, not a discovery run. I will replay that output and check the refreshed hashes.

These requests enforce the existing declaration, not a new mathematical search. The root-13 regression and manifest checks themselves are now complete. The remaining release gates are this producer/evidence wiring and the user's explicit approval. Route B and searches beyond order 20 remain unreleased.
