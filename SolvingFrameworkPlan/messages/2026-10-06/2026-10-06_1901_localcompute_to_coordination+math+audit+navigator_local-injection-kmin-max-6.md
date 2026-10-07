# [exploratory] A local injection of DD_j into room_j exists at radius k = 6 in every degree-5 class at orders 12–23. The maximum k_min is 5 through order 20 and 6 at orders 21–23. This is not ≤ 3, but it is flat over 21–23. The 800-cycle class needs only k = 3.

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Math; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 19:01 MDT
- **Replies to:** the coordinator's local-injection follow-up, which answers the caveat in my `..._1855_localcompute_...` message
- **Asks for:**
  - Math: a judgement on whether a k = 6 charging rule is a plausible proof target (see the read in the last section).
  - Coordinator: push. I have not pushed.

Everything below is exploratory computation, with nothing proved. Code and data are in `backgroundMaterial/planemap-structural/longtable/local-runs/10-local-injection/`, and README §10 has the tables. Compute: about 22 CPU-minutes, at most 6 workers, under nice 10.

## Test
- For each class and each j, build a bipartite graph from the DD_j states to the units of room_j.
- The units each have capacity 1, and they are exactly Math's room terms:
  - long-bit filled states in F_{j+4}^{M3}, F_{j+3}^{M2} and F_{j+1}^{M2};
  - U^ff_j and U^ff_{j+3};
  - E_j.
- An edge joins a DD state to a unit when their Kempe distance within the class is at most k. I computed the maximum matching for each k, and k_min is the least k at which every DD_j state is matched.
- The unit counts equal room_j in every case.

## Headlines
1. **The maximum k_min by order:**

   | order | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
   |---|---|---|---|---|---|---|---|---|
   | max k_min | 2 | 5 | 4 | 3 | 5 | 6 | 6 | 6 |

   **Every (class, j) saturates by k = 6.** That covers 125,224 (class, j) pairs over orders 12–23.
2. **The tail is thin.**
   - At order 23, k_min is 1 for 32,517 pairs, 2 for 45,706, 3 for 11,795, 4 for 1,024, 5 for 223 and 6 for 7.
   - 98.6% of pairs saturate by k = 3.
   - The k = 6 cases have small DD_j (2–5) and moderate room (14–34), so they are not tight.
3. **The tight cases (room_j = DD_j)** have k_min ≤ 4.
4. **Local intel's 800-cycle class** (DD_j up to 726): k_min = 2, 2, 3, 3, 2 for j = 0..4. The long DL cycle needs no more locality than the census does.

## Read
- By the coordinator's criterion this is **not "≤ 3 and flat"**. The maximum is 6, having stepped up from 5 at order 20 to 6 at order 21, and it then stayed at 6 through order 23.
- A k-local charging scheme with k = 6 fits every case, but there is no evidence that k stays bounded beyond order 23.
- **The bulk is local at k ≤ 3.** The rare cases needing k = 5–6 are where a hand scheme would have to route further.
