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

## Reconciliation with I_route_e (10:45Z): 1/21 stands

I's cancellation (x4's T into w2 through y equal to e's T out) needs x4's word rooted at s2 to equal e's word rooted
at w2. That forces e's neighbour e''s private pi = x3, and e lone forces x3 <= 6. e''s 6-wheel is then
(7, 5, x3, x3, 5, 7): at x3 = 5 four fives in a row (2.122, reducible); at x3 = 6 it is c6_566577, C in Job 17's
verdict file (ring 12, X = {I0-I1}, not in the uncertain list). So the self-paired arrangement is inadmissible and the
floor at (6,6) is **1/21**; 11/71 would return only if C wheels were dropped.

## The floor as a function of the surviving frame set (`floor.py`)

`python3 -I floor.py WHEELDIS_DIR [KILLFILE] [no37] [nopair] [nochain]`, ~7 s; WHEELDIS_DIR is a wheeldis tree with
`bin/sep3` built. Kill lines: dfast/kc/cfast lines, bare `f7_L_S` names (5-8 exact, B = any >= 7, '.' free), or
`LINK SWORD` in frame coordinates. A kill removes every w2, w4 or s2 frame that some rotation/reflection of the
window matches at all its fixed letters; round 37's window is always added unless `no37`. Validated: no extra kills
-> 1/21; `no37` -> 11/71; a test kill of the binding s2 frame plus frame 7667575/5557777 -> 1/21 at the next s2
frame (5765557 / 7575767).

- Each surviving s1 = 6 frame at w2 (mirror at w4) bounds T <= alpha + beta t through guaranteed payment shares (units
  of 1 - t) of w2's link fives, valid for every feasible (Y, T, t): a lone five with no T route, or all routes
  self-paired (slot five = 5, z = 7, wheel (7,5,a,a,5,7) not reducible), pays 1; a five whose bigs all carry the
  same rooted word and no 6 next to a big pays 1/#bigs; any other five pays 0. c = the frame's total share.
- No chain: (alpha, beta) = (1 - c, 1 + c). One lone five with a single unpaired route to s2: (alpha, beta) =
  (1 - c - c2, 3 + c + c2), c2 = best guaranteed share over surviving c-check-admissible s2 frames (link
  w3 w2 e' x4 q1 q2 s3, s-word u e pi r1 r2 r3 w4).
- Floor = max over (w2, w4) frame pairs of (0.7 - alpha0 - alpha6) / (2.7 + beta0 + beta6). c = 6/5 gives 11/71;
  c = 1/5 with c2 = 7/10 gives 1/21.
- Binding now: c = 1/5 at w2 frame 7665675 / 5555577 (only w3 pays); c2 = 7/10 at s2 frame 5765557 / 7575757 (w3 pays
  1/5, q1 pays 1/2). Same at the w4 mirror.
