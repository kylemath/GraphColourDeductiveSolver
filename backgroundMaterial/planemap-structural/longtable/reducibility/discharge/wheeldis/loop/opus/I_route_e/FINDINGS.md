# I: a rule that gives five e a route away from w2 (18 Oct 2026) [hand; E first-order with y fixed at 7/27]

Question: is there a sound rule letting a five whose only big is w2 route charge away, breaking the rule-T floor?
Guess: yes via a 6-relay, but the charge lands on a tight big. Plan-changer: a route to a slack big would cut the floor.

**Rule S (6-relay):** a five v with a 6-neighbour x and a big z adjacent to x but not to v sends S[class of v's
2-ball, z] to x, and x passes it all to z (every 6 nets 0). Sender row Y + S >= 1 - t; z's row gains one inflow per
five at distance 2 reaching it through a shared 6. Rules T and H are special cases.

**New frame (w2 link 7665675 = u, w1, s1, e, y, s2, w3; s-word 5.66577):**
- w3 (77777): no route of any kind.
- e (lone, link 7 6 6 6 6) has a T route e -> y -> s2. But x4 (a five between y and s2) sends T into w2 through y, and
  the reflection through y can make x4's class equal e's; the two cancel at w2 and T0 <= 2.2t - 0.2 returns, so the
  floor is **11/71 again** [hand]. (This conflicts with H round 2's 1/21, which dropped x4's inflow as >= 0; to be
  reconciled in floor.py.)
- Unpaired route: all 7,631 admissible 2-balls around e have >= 2 bigs at distance 2 [E]. b (past e's consecutive 6s
  x3, y) is forced big, since y's 6-wheel is reducible for b <= 6: this is rule H. No self-pairing (reflection through
  y sends e's flow to x3, a 6); w2 and u get no H inflow.
- Rows: T0 <= 2.2t - 0.2 + H_e at w2; 7.1t >= 1.1 - H_e - H_E at u (H_E the w4 mirror).
- Where it lands [E, first order]: at b = 7 some c-check-admissible rows are exactly 7/27-tight (e.g. link 6658556,
  s 5786566), so H_e's cap is 0: no first-order gain.

**Old frame 7665575 (killed), for the record:** e -> x2 -> r works (r forced big); first-order cap 0.0525, t ~ 0.140;
the rule must read x4.

**Kill target:** u's row at (6,6) + w2 frame 7665675/5.66577 + b's tight row (6658556 / 57865xx, 57875xx), mirror at
w4. If D or C, rerun hload.py; else rule H/S columns go into the sep3x job beside T.

Not done: hat rows at d = 8, 9; the second forced big's row; any LP. No all-y floor proved (b's link fives have routes).
Scripts: load.py, eroute.py, eroute2.py, zload.py, hload.py; outputs zload7*.txt, hload7.txt.
