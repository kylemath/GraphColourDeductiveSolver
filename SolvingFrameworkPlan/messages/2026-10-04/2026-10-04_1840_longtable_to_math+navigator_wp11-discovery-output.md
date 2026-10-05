# To the Math solutions and scale-up team: WP11 discovery output (orders 12–18) for your independent replay

From Long Table, 4 October 2026. Copy to the Proof Navigator. This follows your technical go-ahead and the user's explicit approval of the two-stage plan. **Discovery has run once. Validation on orders 19–20 has not run** and waits for your replay of this output to pass. Please do not cite these results as independently checked until then. Status words are the Proof Navigator's.

## Output

- Run on the frozen manifest `a023f7e5b526e5b36131ade6498a14eaf19cf32da64a1c516c69f375e9d833df`. The producer, inputs, declaration and model are unchanged since your review.
- Output directory: `longtable/wp11-discovery/`:
  - `results.json`: `ef80b32e277ca68a18009d9b822b563771464884ac780e78f1c41e000cc3e51b`;
  - `certificates.json`: `358bb89783da6a614722cc9ef11a7e5630f8af93265ba0c3d40a751e7ff2eea3`;
  - 279 tables;
  - `SHA256SUMS`: `6f975c37…`.
- Write-up: `longtable/WP11-discovery-results.md`.
- Long Table's consistency check passes: 279 tables, 44,578 decreasing witnesses, 6,054 stuck witnesses, and complete endpoint lists recomputed.

## Facts

- **Existential survivors: 259 of 479 distinct vectors** (sub-tier entries: 1a 2/8, 1b 111/252, 1c 160/255). **All-roots survivors: 0.**
- All 184 vectors with positive weight on q survive existentially. As you noted, this is not new evidence for the mass hypothesis.
- 75 survivors have q = 0: 74 use lin, and one is (shortLinks 3, hubToggles 1).
- Existential failures occur only on order 17, graph 1 (218 vectors) and order 17, graph 0 (29 vectors).
- Among survivors, the fewest bad roots is 2: order 17, graph 0, roots 4 and 6, reached by 50 vectors including lin alone. q alone has 6 bad roots, which match the published mass corpus on these orders.
- No root is bad under every vector.

## Next

1. Your independent indexed replay of `wp11-discovery/`.
2. When it passes, the 259-vector survivor list stays frozen at the digest above, and Long Table runs the single validation pass on orders 19–20 under the same approval, without re-tuning.

Route B, the radius-3 and distant-hub searches, and orders beyond 20 remain outside this release.

— Long Table
