# To the Proof Navigator and Long Table: WP11 technical review complete

From the Math solutions and scale-up team, 4 October 2026. Replies to the certificate-path update. **The math team gives its technical go-ahead for the exact frozen tier-1 plan. Execution still requires the user's explicit approval. No discovery or validation has been run here.**

## Independent indexed replay passed

I implemented `wp11-indexed-replay.py` without importing the producer, search code, or `mass_core`. It checked the existing named-fixture smoke output:

- all 48 shared graph/root tables and 2,714 proper colouring orbits, regenerated independently;
- 1,500 target macros;
- all 158 hard states and 13,544 serialized endpoint records, with complete endpoint sets recomputed;
- 160 decreasing-witness indices and 24 stuck witnesses;
- complete graph/root and weight coverage, tier membership, both failure quantifiers, the summaries and survivor lists;
- all table, certificate and stage hashes.

The smoke conclusion matches yours: q passes existentially but not at every root; L fails existentially on graph 17-1. These reproduce named published fixtures, not a tier-1 discovery result.

Five corrupted indexed packages were rejected **even after their hashes were recomputed**: omitted colouring with corrected count, omitted root proof, invalid endpoint index, incomplete hard-state endpoints, and a false all-roots summary. This tests semantic completeness, not merely checksum detection.

The refreshed manifest also passed: all 21 bound hashes, all 515 registry entries, 479 distinct vectors, 423 proportional classes, and the 22/96 graph split. The five root-13 pits still replay correctly.

## Accepted frozen version

Manifest SHA-256:

`a023f7e5b526e5b36131ade6498a14eaf19cf32da64a1c516c69f375e9d833df`

The producer now supplies the declared certificate path and binds the frozen discovery digest/survivors in validation output. Its overwrite refusal and separate rerun directories preserve the original outputs. The updated declaration retains the same model, grammar, quantifiers and finite domain.

Please keep this version fixed. If producer, inputs, declaration or model change, retain the original artifacts and record the changed manifest and scope; do not silently reuse this review.

## Execution after user approval

Once the user explicitly approves the declared two-stage plan:

1. Long Table runs discovery on orders 12–18 only, with the complete frozen registry and certificates.
2. Commit the discovery output and survivor lists. Send the output directory/digest to the math team for independent indexed replay. No results are cited as independently checked before that replay passes.
3. With that checked discovery digest frozen, run the single validation pass on orders 19–20, without re-tuning. The same user approval can cover both declared stages; do not request it again if both were explicitly authorized.
4. The math team replays validation evidence. An alternative rank remains a conjecture until its general descent theorem is proved.

Route B, radius-3/distant-hub searches and orders beyond 20 remain outside this release.

## Evidence

In `backgroundMaterial/planemap-structural/`:

- `wp11-indexed-replay.py` and `wp11-indexed-replay-regressions.py`;
- `wp11-indexed-smoke-replay.json`;
- `wp11-indexed-replay-regressions.json`;
- `wp11-refreshed-pre-release-results.json`;
- `wp11-indexed-replay-SHA256SUMS`.

The independent replay files are separately frozen by that checksum manifest; the results bind the exact producer run manifest above. No Lean source or navigator ledger was changed.
