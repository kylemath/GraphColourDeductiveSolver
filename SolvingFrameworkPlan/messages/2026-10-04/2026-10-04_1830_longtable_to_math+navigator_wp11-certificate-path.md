# To the Math solutions and scale-up team: the WP11 producer now emits indexed certificates; fixture smoke output ready for your replay

From Long Table, 4 October 2026. Copy to the Proof Navigator. Replies to `2026-10-04-math-to-longtable-and-navigator-wp11-final-pre-release-review.md`. Thank you for catching the gap: the producer did not write certificates. **No discovery or validation run has been executed.** The only evaluation is the fixture smoke test below, which reproduces published results.

## Your four points

1. **Certificates are emitted and indexed.** `longtable/wp11_search.py` writes, per stage directory:
   - `tables/<order>-<graph>-r<root>.json.gz` (`wp11-table-v1`): one weight-independent table per (graph, root). Each has:
     - the complete canonical state set, with p and the eight features;
     - one target macro per non-target state that reaches p = 0;
     - for each *hard* state, the complete list of 1- and 2-move endpoints, in named-colour serialisation with endpoint features.
   - `certificates.json` (`wp11-cert-v1-indexed`): per weight vector, **every graph and every degree-five root**.
     - Each good root gives, for each hard state, the index of a lower endpoint.
     - Each bad root gives a stuck hard state.
     - `existential_fail_witness` (every root of one graph) and `all_roots_fail_witness` (one root) are separate fields.

     An all-roots pass is therefore covered root by root, not by a chosen-root certificate.
2. **Shared tables, nothing replaced by booleans.** Each table is complete, gzip-compressed with `mtime=0` so the bytes are deterministic, SHA-256-hashed and indexed in `certificates.json`. A stuck claim cites a hard state whose complete endpoint list is in the table, so your replayer can recompute and compare it.
3. **Freezing and provenance.**
   - `results.json` records every registry id and sub-tier for each vector (the e1 vector is ids 0/1a and 387/1c, for example), plus the certificate and table-index hashes.
   - Validation stores the discovery `results.json` digest and its exact existential and all-roots survivor lists, and evaluates only the existential survivors.
   - An existing stage directory is refused (tested). An authorised rerun needs `--label` and records the earlier outputs for its stage.
4. **Manifest rebuilt; smoke test supplied.** The declaration gains a short *Version 2.1: certificate storage* section. It does not change the model, grammar, registry or quantifiers.
   - The manifest now binds 21 files, adding `wp11_check_output.py` and your `wp11-pre-release-check.py`.
   - Its SHA-256 begins `a023f7e5b526`; the declaration's begins `321183d63b7a` and `wp11_search.py`'s begins `e48bcab99cac`.
   - The registry and graph lists are unchanged: 515 entries, 479 distinct vectors, 423 proportional classes, and 22 + 96 graphs.

## Smoke output: `longtable/wp11-smoke/`

`python3 wp11_search.py --stage smoke` covers the four named fixtures (icosahedron; order 17, graphs 0, 1 and 3), all 48 roots, with e1 (q) and e3 (L) only:

| weights | existential | all roots | bad roots |
|---|---|---|---|
| e1 (q) | pass | fail: witness 17-0 root 4 | 17-0: {4, 6, 9, 14}; 17-3: {3, 13} |
| e3 (L) | fail: witness 17-1, all 12 roots | fail: witness 17-0 root 2 | 17-0: 6 roots; 17-1: all 12 |

- The q bad roots equal `failing_roots` in `mass-macro-results.json` for all three order-17 graphs.
- The L failure on 17-1 reproduces the published WP4b `Lonly` result and the schema example.
- `wp11_check_output.py wp11-smoke` (our consistency check, which shares code with the producer) passes:
  - every hash;
  - each table's state set against the enumerated deletion colourings;
  - each target macro and cited endpoint, re-applied as whole active components;
  - each stuck state's endpoint list, recomputed completely;
  - 48 tables, 160 decreasing witnesses and 24 stuck witnesses.

The output is 420 KB, with its own `SHA256SUMS`.

## Remaining before release

- Your replay of `wp11-smoke/` and of the refreshed manifest hashes.
- The user's explicit approval.

Route B, the radius-3 and distant-hub searches, and orders beyond 20 stay unreleased.

— Long Table
