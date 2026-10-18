# H: independent check of explore round 36's rule-T floor (18 Oct 2026) [hand + frame.py]

Question: does explore's second-order floor t >= 1.1/7.1 at filling (6,6) hold for rule T without L2 transfers?
Guess: yes. Plan-changer: an error would reopen rule T as a route below 0.155 through this row.

**Verdict: holds at every step, and is a floor for the whole rule-T LP class (not first order)**, provided there is
no L2 or other big-to-big transfer out of w2/w4 and four arrangements stay unforbidden: u's row at R*(6,6), w2's worst
frame, its mirror at w4, and w6's sender row with z-letters (w4, p5) = (7, 7).

- Patch consistent (`frame.py`, oriented triangles: each directed edge once, each closed vertex's link one cycle of
  its degree). w2: link 7665575 (u, w1, s1, e, e', s2, w3), s-word 5.65677 (w0, p1, x2, x3, x4, s3, w4); e, e', x3 a
  triangle of fives. No five-wheel reducible; w1, w5 6-wheels non-reducible for every p1, p5. Minor: s1's 6-wheel is
  reducible when p1 = 5 and s1's outer letter <= 6; the floor uses p1 = 7, so unaffected.
- e's neighbours: w2 = 7, s1 = 6, x2 = 6, x3 = 5, e' = 5; its only 6 beside w2 is s1, and the face (w2, s1) has
  third vertex w1 = 6, so rule T gives e no route. e and w0 share the rooted word 7|6655; only the z-flag differs.
- w2's row: e pays >= 1 - t, w3 (one variable over its five rootings) >= (1 - t)/5, e' >= 0, one T inflow (from
  w0): T0 <= 1 + t - 1.2(1 - t) = 2.2t - 0.2. Mirror: T6 <= 2.2t - 0.2 at w4.
- u's row: w6's payment to u at big z = w4 is the same variable as in w6's sender row with p5 = 7 (admissible), so
  Y_u(w6) >= (1 - t)/2 - T6. u has no inflow at (6,6): 2.7t >= 1.1 - 4.4t, so **t >= 11/71 = 0.1549** (exact).
- Uses only sender-row lower bounds, nonnegativity and these receiver rows, so it holds for every admissible y.
  k36's 0.1506 / 0.148 are first-order with y fixed.
- Breaks only with: a transfer out of w2/w4, a kill of one of the four arrangements, or a richer rule giving e a
  route (e.g. rule H over s1, x2; inferred that the small-hat case still leaves a valid row).
- Not done: sep3 / w2load.py not rerun; w2's frame passing the c-check is k36's result; R*(6,6) passing the c-check
  at u is the coordinator's premise (k36 checked R only at s1 = s4 = 5).
