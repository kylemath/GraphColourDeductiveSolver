# Q: the next rule class after rule T (18 Oct 2026, 18:00-19:15Z) [hand + jsep2 caps]

**Recommendation: build S-lite first (no engine cost), then P6.** Rule T already takes R*'s row out of first-order
binding; every new route target (s1, p1, p5) can be made exactly 7/27-tight by the adversary, so beyond T, R* gains
only second order.

## Ranking
1. **S-lite**: rule S restricted to routes A (= rule T) and O (the fan) through a 6 next to the five's big root. Same
   5^9 jsep2 window and DP state; only new columns and per-window terms.
2. **S + P6**: adds route C (far hat; rule H is a case) and carries each link 6's private p_j as a state letter.
   w alphabet 5 -> 9 symbols; table 9^5 * 5^4 = 36.9M doubles (295 MB); bound kept on 3,125 states with p relaxed; DFS
   up to 5x per link 6. Value: exactness (round 42's forced private letters enter receiver rows; T inflow exact in p).
3. **7 -> 7 / 7 -> 8+ transfers reading through a 6** (L2 side codes plus s_{i+1}, s_{i-2}): fits the window; gain
   unknown (L2 gave 0 with T = 0); only once Job 30 A+B shows which tight bigs need an outlet.
4. **RSST-style 6-decides relays**: new 6-centred row family and a second separator; same flows as S, far higher cost.

## First-order caps at R*(6,6) (Studio's round-13 7/27 y, full registry, jsep2 with the frame imposed; `cap.log`)
| target | route | cap |
|---|---|---|
| w2 | T | 0.796 at p1 = 7, 8, 9 (worst frame 7667575/5755577, with round 42's p2a >= 6, (p2a,p2b) != (6,5)) |
| p1 | C | 0 at d = 7 (tight row 5666558/7576568); 0.295 at d = 8 |
| p5 | - | 0 at d = 7; 0.102 at d = 8 |
| s1 | O | 0 at d = 7 and 8 |

With round 42 loaded, rule T alone leaves R*'s row with no floor (0.7 - 2(0.796) < 0); explore's 0.2778 cap at w2
predates those letters.

Hand check at (6,6): u takes no S inflow (I1-I5 below), so every S variant voids 1.7(1-t) <= 1+t without a
self-paired cancellation; S-lite does it only through T. Without P6, p5 = 5 is allowed and gives an O inflow at u: a
leak, not a pairing. **New self-pair at s1 >= 7:** w0's O route (root u, via w1, to s1) is the same variable as p1's O
route (root s1, via w1, to u) when p1 = 5, p1's other two neighbours are 5 and s0's wheel 5 6 5 5 o2 5 is non-R6
(true for o2 = 8, 9). So O cancels at s1 = 7, and helps at s1 in {8, 9} only with exact target letters (option F).

## Spec for S (S-lite = S with the C slot off)
Geometry: five v (non-R5), spokes l0..l4 cyclic; hat h_k = common neighbour of l_k, l_{k+1} other than v; fan f_k (for
a 6-spoke l_k) = vertex opposite v in l_k's wheel (v, l_{k+1}, h_k, f_k, h_{k-1}, l_{k-1}). Root B = l_j (big), raw
word (B, a, b, c, e). For a side x in {a, e} with x = 6, read x's wheel from v as (v, B, A, O, C, y): A = hat(B, x)
(T target), O = fan of x, C = hat(x, y). Route (side, pos): v pays S to the target at pos in {A, O, C} through x when
the target is big; the 6 forwards all of it (nets 0, no 6 rows).

Key (extends tkey): Y(raw, Fa, Fe), S(raw, Fa, Fe, side, pos); F_side = (lam A, lam O, lam C) if that spoke is 6, else
'-' (lam exact for option F, small/big for B; S-lite: C slot '-'). Canonicalise with rv = (B, e, c, b, a): if rv < raw,
(raw, Fa, Fe, side) <- (rv, Fe, Fa, swap(side)); if raw == rv, take lexicographic min of (Fa, Fe, side) and
(Fe, Fa, swap(side)). pos labels unchanged by reflection. Risk (G erratum class): not swapping the flag tuples with the
side in the palindromic case. Required test: for every physical five, root, side, pos, the key read clockwise equals
the key read anticlockwise.

Sender rows: enumerate spokes, every hat next to a 6-spoke and every fan of a 6-spoke over 5..9; admissible iff the
five-word is non-R5 and every (now determined) 6-spoke wheel is non-R6. Row: sum over big roots j of [Y(key_j) + sum
of S(key_j, side, pos) over routes with a big target] >= 1 - t; dedupe by projected key.

Receiver rows (receiver R, letter U; w_i, s_i; p_j for each w_j = 6):
- Outflow at a link five w_i: + Y(key), exact; raw = (U, w_{i+1}, s_i, s_{i-1}, w_{i-1}); Fa = (w_{i+2}, s_{i+1},
  p_{i+1}) if w_{i+1} = 6; Fe = (w_{i-2}, s_{i-2}, p_{i-1}) if w_{i-1} = 6. These are jsep2's window letters
  (w_{i-2..i+2}, s_{i-2..i+1}); S-lite needs no p.
- Inflow through a link 6 x = w_j (wheel (R, w_{j+1}, s_j, p_j, s_{j-1}, w_{j-1})), all at window j:

| source | root B | R is | F_x in v's key | v's raw word |
|---|---|---|---|---|
| I1: s_j = 5 | w_{j+1} big | A | (U, w_{j-1}, s_{j-1}) | (w_{j+1}, 6, p_j, m, n) |
| I2: s_{j-1} = 5 | w_{j-1} big | A | mirror of I1 | mirror of I1 |
| I3: p_j = 5 | s_j or s_{j-1} big | O | (w_{j+1}, U, w_{j-1}) from root s_j | (s_j, 6, s_{j-1}, m, n) |
| I4: s_j = 5 | p_j big | C | (s_{j-1}, w_{j-1}, U) | (p_j, 6, w_{j+1}, n, m); n = s_{j+1} / p_{j+1} / unseen for w_{j+1} = 5 / 6 / big |
| I5: s_{j-1} = 5 | p_j big | C | mirror of I4 | mirror of I4 |

  m, n are outside the window: take the max over them. Without P6 add max over p_j (non-R6 wheel at j) of
  [I1 + I2 + I3]; exact in p_j, conservative only in m, n and the other side's flags. R takes no S inflow through a 6
  outside its link (a target is always adjacent to x). S-lite turns I4, I5 off.
- P6 engine changes: w symbols 5, 6/p5..6/p9, 7, 8, 9; bound over (w, s, w, s, w) with p relaxed, exact at leaves;
  Karp tail 405 states (was 125); old masks map bit 6 to all five 6/p symbols; round-42 letters become P6 masks.
- Validation: S = 0 with C off must reproduce Job 30 B's T optimum; the orientation test; plant one S > 0 in a known
  row and check the target sees the inflow.

Not done: no LP with S. Round-42 letters applied only in the w2 and p1 frames. Files: capcheck.py, cap.log, r6.py.
