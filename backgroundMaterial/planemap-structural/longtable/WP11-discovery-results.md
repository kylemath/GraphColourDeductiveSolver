# WP11 discovery results: rank synthesis, tier 1, orders 12–18

Long Table, 4 October 2026. This is the declared discovery stage, run once on the frozen manifest `a023f7e5b526e5b36131ade6498a14eaf19cf32da64a1c516c69f375e9d833df`. The user approved it explicitly, after the math team's technical go-ahead (`2026-10-04-math-to-longtable-and-navigator-wp11-technical-go-ahead.md`). **These are facts only; the Proof Navigator assigns statuses.** The results are **not yet independently replayed**. Validation on orders 19–20 has not run.

## Run

- `python3 wp11_search.py --stage discovery` took 47 s and produced `wp11-discovery/`:
  - `results.json`, SHA-256 `ef80b32e277ca68a18009d9b822b563771464884ac780e78f1c41e000cc3e51b`;
  - `certificates.json`, SHA-256 `358bb89783da6a614722cc9ef11a7e5630f8af93265ba0c3d40a751e7ff2eea3`;
  - 279 per-root tables;
  - `SHA256SUMS`.
- This is the first and only discovery output; there is no label and no earlier output.
- Domain: the 22 Plantri minimum-degree-five triangulations of orders 12–18, with all 279 degree-five roots, and all 479 distinct vectors of the 515-entry registry.
- Long Table's consistency check, `wp11_check_output.py wp11-discovery`, passes. It shares code with the producer, so it shows consistency only. It covers:
  - 279 tables;
  - 44,578 decreasing-endpoint witnesses;
  - 6,054 stuck witnesses;
  - complete endpoint lists, recomputed for every hard state.

## Survivors

| | vectors | existential survivors | all-roots survivors |
|---|---|---|---|
| sub-tier 1a (single features) | 8 | 2 (q, lin) | 0 |
| sub-tier 1b (pairs, weights 1–3) | 252 | 111 | 0 |
| sub-tier 1c (0/1 subsets) | 255 | 160 | 0 |
| **distinct vectors** | **479** | **259** | **0** |

Sub-tier counts are by registry entry; a vector in two sub-tiers counts in each. The exact survivor lists, with every registry id and sub-tier, are in `results.json`.

## Facts about the survivors

- **Every one of the 184 vectors with positive weight on q survives existentially.** The math team noted that the published mass already survives existentially, so this is not new evidence for the mass hypothesis.
- **75 survivors have zero weight on q.**
  - 74 of them have positive weight on lin.
  - One has neither: (shortLinks 3, hubToggles 1).
  - Of the 112 vectors with lin > 0 and q = 0, 74 survive. All 38 that fail have positive weight on repMass, or on hubToggles at weight 3, as in (lin 1, hubToggles 3).
- **Existential failures** occur on two graphs only:
  - order 17, graph 1: every root bad for 218 vectors;
  - order 17, graph 0: for 29 vectors.
- **No vector survives at every root.** Among existential survivors, the total number of bad roots ranges from 2 to 20. The minimum, 2 bad roots (order 17, graph 0, roots 4 and 6), is reached by 50 vectors, including lin alone. *[Erratum, 4 October: an earlier version also listed q + lin here; `[1,1,0,0,0,0,0,0]` has 4 bad roots (order 17, graph 0, roots 4 and 6; graph 3, roots 3 and 13). Found by the math team's review; the JSON was correct.]* q alone has 6 bad roots, matching the published mass corpus restricted to orders 12–18.
- **No root is bad under every vector.**

## Scope

- These facts concern only the declared grammar, registry, two-move macros, and the domain of orders 12–18.
- An existential survivor is a conjecture-shaped candidate for its own rank. It would need its own contact wrapper and descent theorem, and it is not evidence for the original mass hypothesis.
- The empty all-roots survivor list is limited to this registry and domain.

## Next

1. The math team replays `wp11-discovery/` independently.
2. Once that replay passes, the 259-vector existential survivor list (digest above) stays frozen, and the single validation pass on orders 19–20 runs under the same user approval, without re-tuning. Orders 19–20 were inspected in earlier research.
