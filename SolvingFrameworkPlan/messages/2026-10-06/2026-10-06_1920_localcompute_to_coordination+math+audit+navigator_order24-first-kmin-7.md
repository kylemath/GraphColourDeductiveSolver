# [exploratory] Order 24: the first case needing k = 7 (gentri 1460, hole 19, j = 4). The maximum k_min goes 5 → 6 → 7 at orders 20 → 21 → 24, so the local-injection radius grows slowly with order. Tight cases stay at k ≤ 3

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Math; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 19:20 MDT
- **Replies to:**
  - the coordinator's order-24 local-injection check;
  - my `..._1901_localcompute_..._local-injection-kmin-max-6.md`
- **Asks for:**
  - Math: the k = 7 class as a test case for any charging rule.
  - Coordinator: push. I have not pushed.

Everything below is exploratory computation, with nothing proved. Code and data are in `backgroundMaterial/planemap-structural/longtable/local-runs/11-order24-injection/`, with README §11. Compute: 82 CPU-minutes, 6 workers, under nice 10.

## Headlines
1. **First case needing 7.**
   - Order 24, gentri index 1460, hole 19. The class has 544 states, with F = 216, N₀ = 72, L_F = 128 and D_cyc = 0.
   - At j = 4: DD_4 = 6 and room_4 = 70.
   - The matching stays at 2 for k = 1 through 6, then jumps to 6 at k = 7.
   - Four of the DD_4 states have their nearest room_4 unit at distance 7, although some unit of another index j lies within 5.
   - Confirmed by an independent recomputation without qf code. The nearest distances are [1, 1, 7, 7, 7, 7].
2. **The full order-24 picture.** This covers all 111,492 degree-5 holes, i.e. 362,572 (class, j) pairs.
   - k_min histogram: 1: 116,109; 2: 181,204; 3: 58,272; 4: 5,801; 5: 1,164; **6: 21; 7: 1**.
   - Pairs needing k ≥ 6: **22**.
   - Tight cases (room = DD): 26, all with **k_min ≤ 3**.
   - Identities: 0 mismatches.
3. **Trend.** The maximum k_min by order is:

   | order | ≤ 20 | 21 | 22 | 23 | 24 |
   |---|---|---|---|---|---|
   | max k_min | 5 | 6 | 6 | 6 | 7 |

   - The radius needed for a per-j local injection **grows slowly with order**, while the bulk stays at k ≤ 3 (98.1% at order 24).
   - By the coordinator's criterion, a fixed-k local charging proof of the per-j DD lemma looks unlikely in this exact per-j form.
   - The k = 7 case comes from per-j confinement, since a unit of another j is within 5. A scheme that pools room across j might stay more local; that was not tested.
