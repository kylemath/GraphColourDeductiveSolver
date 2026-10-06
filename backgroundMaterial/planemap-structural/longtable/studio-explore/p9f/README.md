# [exploratory] P9-F (Math path 9, MathPath9StuckClass.md section 8), Mac Studio

`p9f.py` is a fresh stdlib script. DL is as in kempe.cpp / radius.py. "Link moves" are swaps of two-colour components that meet the link (for a DL state these are the 8 link components of the note's section 1 table); "silent" moves are the rest.

Depth sets:
- D0 = DL.
- D1 = DL states whose link-move images are all DL.
- D1p = D1 with all silent images DL.
- D2 = D1 states whose link-move images are all in D1.
- Dinf = the largest subset of DL closed under link moves.

Pattern key: frame-normalised degrees d_0..d_4 (capped at 8) and the colour words of R_0..R_4 in a (alpha), m (mu), A, B. Boolean features: "d_t=k", "R_t has c", "R_t starts c", "R_t ends c", "|R_t|=k".

Coverage:
- every degree-5 hole orbit of plantri -m5 -c4, orders 12-20 (`p9f-N.jsonl`);
- the four radius-5 certificates at their certified holes (`p9f-certs.jsonl`).

| set | holes | D0 | D1 | D1p | D2 | Dinf |
|---|---|---|---|---|---|---|
| order 17 | 19 | 292 | 62 | 62 | 15 (7 holes) | 0 |
| order 18 | 53 | 473 | 7 | 7 | 0 | 0 |
| order 19 | 179 | 2093 | 27 | 26 | 0 | 0 |
| order 20 | 622 | 11828 | 272 | 250 | 4 (4 holes) | 0 |
| 91a307 h22 | 1 | 247 | 27 | 25 | 7 | 0 |
| 8a23ee h23 | 1 | 195 | 9 | 9 | 4 | 0 |
| 62661a h23 | 1 | 195 | 9 | 9 | 4 | 0 |
| 80b930 h23 | 1 | 734 | 27 | 19 | 7 | 0 |

Orders 12-16 have no D1 states.

**Dinf = empty at every hole**, as the calibration predicted.

**The one question:** is some feature forced at depth 2 but not at depth 1?
- **No.** Pooled over all 440 D1 and 41 D2 states, the features at 100% of D2 are exactly six: R0 has A, R1 has A, R1 has B, R2 has B, R3 has m, R4 has m.
- These are the starvation set, and they already hold at 100% of D1. The census and the certificates give the same answer separately.
- Keys killed between D1 and D2 at the certificates: 6, 3, 3, 11. Full per-feature counts are in `p9f-agg-*.json`.
- FM1-FM4 were not separately evaluated here.
