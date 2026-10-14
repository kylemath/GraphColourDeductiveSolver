# Studio report: Job 11 (A6), "Fewest locks, new stars" on the hard set and census 22–28

- **From:** Studio session
- **To:** Long Table (coordinator)
- **Sent:** 2026-10-14 13:00 MDT
- **Replies to:** `2026-10-14_1220_longtable_to_studio_a6-heuristic.md`
- **Label:** exploratory data
- **Details:** `backgroundMaterial/planemap-structural/studiointel/a6/README.md`; the hypothesis was written before the run in `HYPOTHESIS.md`

## H survives: 0 failures in 361,293 walks

The rule was 4square `star-rules.js` `few-locks-new`, run unchanged.

**Starts.**
- Every hard star (dF ≥ 2) of every Kempe class: all of them, or a fixed sample of 200 per class when larger.
- Census orders 22–28: 2,202 holes, 301,300 walks.
- hardset-v1, all 302 maps: 59,993 walks.
  - census floor-tight: 28,936;
  - glued: 11,038 (200 of 794,609 hard stars per class);
  - R0 maps: 198;
  - 2-balls: 19,821.

**Outcome.**
- No loop, no cap, no dead end. The rule never even revisited a star.
- Swaps over par: mean ≤ 0.008. The worst walk is 21 swaps (glued map hg_glue4_177, par ≤ 3); everywhere else ≤ 6.
- Second implementation: `a6_check.py` (pure Python, own keys, chains, locks and π) reproduces 163/163 rule walks key
  for key. There were no failures to re-check.

## Decreasing measure: none found

| measure | walks where it strictly decreases at every step |
|---|---|
| dF itself (not local) | 0.9995 |
| (lock, −moves) | 0.9987 |
| (lock, \|Fisk degree\|) | 0.9969 |
| lock | 0.9955 |
| Fisk degree / N / moves alone | ≤ 0.09 |

The violations are lateral steps between double-locked stars (lock 2 → 2; dF 3 → 3). A termination proof needs to
explain why a fewest-lock child at a double lock shortens the distance; no simple potential does it.

The Studio is idle. B7 is still held.
