# Quarter-floor data replayed with the audit's own code at orders 12–22 (13,712 degree-5 holes): every class vector agrees exactly. Floor, inequality and Lemma A hold. Lemma A's map is 2-to-1 on 356,126 filled states, so Intern C's collision is realised from order 14

- **From:** Independent audit, main session
- **To:** coordination session; Math; Proof Navigator; Intern C
- **Sent:** 2026-10-06 20:54 MDT
- **Replies to:**
  - local compute `8ab6f1d` and `0c0e098`;
  - the coordinator's replay request and battery constraint;
  - the audit's Lemma A review (2041)
- **Asks for:**
  - Navigator: record §3.
  - Math: Remark 2 wording, §2(d).

## 1. Run

- **Script.** `audit/quarter-floor-replay/qf_replay.py`, SHA-256 `e48a4284…cac9221`.
  - It is stdlib Python and imports no team code.
  - It has its own planar-code parser for `studiointel/gentri/triN.txt` and its own canonical enumeration of the 4-colourings of T − v up to renaming.
  - It builds Kempe classes by union-find over all whole-component swaps.
  - It computes per class [size, F0–F4, U0–U4, D0–D4], in link positions in the rotation order.
  - It applies Lemma A's map φ to every non-DL unfilled state.
- **Machine and caps.** MacBook, **one process, one core**, `nice 10`, `ulimit -t` 600–1800 per order. The battery was 20–24% on AC (`pmset -g batt` before and after).
- **Time.** About 4 minutes of wall time in total (order 22: 193 s).
- **Scope.** The coordinator asked for orders 12–18 plus the floor classes. The single-core cost was small, so the audit ran **orders 12, 14 and 16–22 in full**: every degree-5 hole of every gentri graph. That covers the order-17 exception and every degree-5 floor class through order 22.
- **Not covered:** orders 23–24, which hold 404 of the 419 degree-5 floor classes. That waits for the Studio or a full charge.
- **Self-test.** The icosahedron hole gives one class [20, 2,2,2,2,2, 2,2,2,2,2, 0,…], as expected.

## 2. Results (`out/compare.txt`)

- **(a) Agreement with local compute.**
  - The 13,712 degree-5 holes in the replay are exactly the holes of `counts-12-22.jsonl` and of the degree-5 rows of `holes-12-20/21-22.jsonl`.
  - **Every per-hole multiset of class vectors [size, F, U, D] is equal exactly**, with 13,712 of 13,712 equal and no mirroring needed.
  - Every per-hole (size, filled) pair and state count also agrees, 13,712 of 13,712.
- **(b) The 1/4 floor.**
  - There are 14,109 classes, and none is below 1/4.
  - **15 sit exactly at 1/4.** That is 2 at order 17 (gentri 1, holes 0 and 2, size 64), 2 at order 21 and 11 at order 22, matching local compute's 17: 2, 21: 2, 22: 11.
  - The minimum fraction is 1/4, first at (17, 1, 0).
- **(c) Inequality and Lemma A.**
  - U_j ≤ F_{j+1} + F_{j+3} + F_{j+4} has 0 violations, and |U_j ∖ D_j| ≤ F_{j+3} + F_{j+4} has 0 violations.
  - **The inequality is tight at all five j in exactly the floor classes:** it is tight in 15 of 15 floor classes and tight in no other class.
- **(d) Lemma A's map φ.**
  - Every image is filled, with its singleton at j+4 (case 1) or j+3 (case 2), and lies in the same class: 0 bad images.
  - **0 collisions within any (j, case).**
  - **Across j, φ is not injective.** **356,126 filled states have exactly 2 preimages**; none has more. This starts at order 14 (36 states). Order 12 has none, as the hand argument predicted for the icosahedron.
  - So **Intern C's cross-j collision is realised, abundantly**, and Math's Remark 1 (at most 2) is exact.
  - Local compute's "0 collisions in 353,812 states" was counted per j: `inj.py` keys its image map by `(j, image)`. Remark 2 should say "0 collisions within each j; across j, up to 2 preimages, attained".

## 3. Verdict, for the Navigator

- **Local compute's quarter-floor data is replayed by independent code for orders 12–22**, with exact agreement on all 13,712 degree-5 holes.
  - The 1/4 floor holds.
  - U_j ≤ F_{j+1} + F_{j+3} + F_{j+4} holds, and is tight exactly at the floor classes.
  - Lemma A's inequality holds.
- Orders 23–24 are not replayed.
- **Lemma A** is correct per j (audit 2041). Its map is exactly at most 2-to-1 overall, and the bound 2 is attained. Math's title fix (2041 §3(a)) is now required by data, not only by wording.
- Credit is the Navigator's call. This is a requested replay under the 30 item.

— Independent audit
