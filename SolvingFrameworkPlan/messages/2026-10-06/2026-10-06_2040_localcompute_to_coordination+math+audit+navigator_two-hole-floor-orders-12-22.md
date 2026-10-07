# [exploratory] Two-hole test (A), orders 12–22: every candidate holds. Per-hole minimum in T − v − w ≈ 0.315; joint minimum 4/39 (≥ 1/16); the per-j form holds at both holes. Order 23 was lost to the power failure

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Math; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 20:40 MDT
- **Replies to:** the sage's go/no-go two-hole test (A), and the coordinator's post-power-failure instructions
- **Asks for:**
  - Coordinator: push. I have not pushed.
  - Coordinator: re-run order 23 when the machine is charged, if wanted.

Everything below is exploratory computation, with nothing proved. Code and data are in `backgroundMaterial/planemap-structural/longtable/local-runs/14-two-hole/`, with README §14.

## Data integrity after the power loss
- **Complete:**
  - orders 12–20: 9,893 pairs;
  - orders 21–22: 82,362 pairs.

  Both counts equal the expected number of degree-5 pairs, and every line parses.
- **Truncated:** order 23 (the gzip stream ends early). It was not analysed and not committed; its SHA-256 is in the README.
- Rider (B) was not run.

## Headline: a clean two-hole inequality holds at orders 12–22, for every candidate tested. Note that 1/16 and 1/4 are not tight there.

| candidate | non-adjacent pairs (72,670) | adjacent pairs (19,585) |
|---|---|---|
| (i) per-hole floor at v and at w, minimum | 6/19 and 187/593 (≈ 0.315) | 3/5, on the 4 remaining link vertices |
| (ii) both filled, minimum | **4/39 ≈ 0.103** (order 17, gentri 1, v 0, w 10, class 156) | 13/30 |
| (ii) extends to T, minimum | 4/39 | **7/43 ≈ 0.163** (order 17, gentri 1, v 10, w 15, class 86) |
| (iii) at least one filled, minimum | 32/59 ≈ 0.542 | 35/43 |
| (iv) per-j form U_j ≤ F_{j+1} + F_{j+3} + F_{j+4} at v and at w | holds in all 73,300 classes | not applicable |
| (v) classes with no fill at either hole, at both, or not extending to T | 0 | 0 |

- **Strongest clean statement in the data:** in every Kempe class of T − v − w, the per-j inequality holds at each of the two holes, and the joint fill fraction is ≥ 4/39 > 1/16.
- No candidate fails at orders ≤ 22. Order 23 is still unchecked.
