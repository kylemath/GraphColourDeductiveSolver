# H round 2: rule-T floor once w2 frames with link 7665575 are killed (explore round 37) [hand + frame2/chain/frame3.py]

**Proven floor at (s1, s4) = (6, 6): t >= 1/21 = 0.0476** (y-independent lower bound). The true second-order floor
lies between 1/21 and the first-order 0.122.

1. w2/w4 alone give no floor now. With 7665575 dead, the largest guaranteed share at s1 = 6 is c = 2/5 (link
   7667575); at 7665675 it is c = 1/5 (w3 = 77777 only). The floor t >= (2c - 1.3)/(4.7 + 2c) is negative for c < 0.65.
2. Why: in w2 = (u 7, w1 6, s1 6, e 5, e' 6, s2 7, w3 5), e is lone when x2, x3 <= 6, but e' = 6 is next to w2
   with z = s2 = 7, so e has a rule-T route to s2: T0 <= 2.2t - 0.2 + T_e (x4's extra inflow when x4 = 5 dropped as >= 0).
3. Chain through s2: s2's frames (link w3 5, w2 7, e' 6, x4, q1, q2, s3 7; s-word u 7, e 5, pi, r1, r2, r3, w4 7),
   e' 6-wheel kept non-reducible, round-37 kill excluded, sep3 c-check run. Best surviving share c2 = 7/10 at s2 link
   5765557, s-word 7575757, x4 = 5 (w3 pays 1/5, q1 pays 1/2; x4 and q2 counted 0). Every s2 frame with c2 >= 1 is
   rejected (1,125 by the round-37 kill, rest by sep3). T_e <= 1 + t - c2(1 - t) with R's row gives
   t >= (2c2 - 0.9)/(9.1 + 2c2) = 1/21.
4. Binding: w2 at 7665675 / s-word 5.x2 x3 5 7 7 (x2, x3 in {5, 6}) with s2 at 5765557 / 7575757; mirror at w4, s3.
   Patch consistent; all five-wheels and e' 6-wheel (756757) non-reducible.

Caveats: share rules give 0 to any five with several bigs and a 6 next to one of them, so this is only a lower bound;
round 38's later kills not applied; sep3 is one engine; the round-1 row with p5 = 7 still needed (explore round 39).
