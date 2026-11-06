# KEYSPEC: generic 2-ball EDGE keys in the 5/6/7 world LP (W6 rounds 5-7)

This is the semantics used by `r5lib.py` / `grammar.py` / `r6_price.py` / `r6_cg.py` for the 87 keys of the round-6 relaxed
ceiling (`round6/keys/relax_ceiling_87keys.txt`, 47 with nonzero amount in `relax_ceiling_47nonzero.txt`).  It is meant to be
enough to re-implement the key columns without reading the code.

## 1. Letters and letter sets

* A letter is a degree class: 5, 6, 7, 8, 9 (9 means "9 or more").
* A letter set is a nonempty subset of {5,6,7,8,9}, written as `{567}`, or with the shorthands
  `5 6 7 8 9` (one letter), `S` = {5,6}, `B` = {7,8,9}; an unconstrained position is the wildcard (all five letters).

## 2. A key

`EDGE(u->v)[P1=X1 P2=X2 ...]`: payer letter u, payee letter v (each a letter or letter set), and a letter set for each
listed position; the positions are among the ten "payer 2-ball" positions S.L+1, S.L+2, S.L+3, S.L-1, S.L-2, S.L-3, S.A+1,
S.A-1, R.L+2, R.L-2; unlisted positions are wildcards.

Direction convention of the LP: a key `u->v` moves DEBT from u to v (it relieves the payer u's row and loads the payee v's
row); in charge terms charge moves from v to u.  (So `EDGE(5->7)` is the classical "a 7 gives charge to a neighbouring 5".)
Each key is one LP column x_E with bounds 0 <= x_E <= 3.

## 3. Positions on an oriented edge

Take an edge u v (u = payer, v = payee) and a chirality sg in {+1, -1}.  Let u's neighbours in cyclic (planar rotation) order
starting at v be SL[0] = v, SL[1], SL[2], ..., SL[d_u - 1], read in the direction sg (indices mod d_u, so SL[-1] = SL[d_u - 1]).

* `S.L+k` = SL[k], `S.L-k` = SL[-k] (k = 1, 2, 3).  S.L+1 and S.L-1 are the two common neighbours of u and v (the third
  vertices of the two triangles on u v); sg decides which one is "+".  S.L+2 is u's next neighbour after S.L+1 (moving away
  from v), S.L+3 the one after that; likewise on the - side.  For a payer of degree 5, S.L+3 = S.L-2 and S.L-3 = S.L+2; for
  degree 6, S.L+3 = S.L-3 (the vertex opposite v).
* `S.A+1` = the third vertex of the triangle on the edge (SL[1], SL[2]) that does not contain u ("the vertex across the
  payer's + face").  `S.A-1` = the third vertex of the triangle on (SL[-2], SL[-1]) not containing u.
* Let v's neighbours in cyclic order starting at u be RL[0] = u, RL[1], ..., read in the direction with RL[1] = SL[1] (the same
  + common neighbour).  `R.L+2` = RL[2] (v's next neighbour after S.L+1, moving away from u), `R.L-2` = RL[-2].

**Multiplicity.** A key is matched on every ORIENTED pair (payer u, payee v) with both chiralities sg = +1 and sg = -1; each
match counts once.  A key whose context is mirror-symmetric (+ and - swapped) therefore counts twice on an edge where it
matches.  Keys K and mirror(K) give the same column.

## 4. Row pictures and the sure / possible rule

Every LP row is the constraint of one centre vertex c, described by a *picture*: c, its link, its apexes, and the private
neighbours of its link vertices, each vertex carrying a letter set (exact letter = singleton).  Vertices outside the picture
are wildcards.  A slot is an oriented match position with c as an endpoint: c as payer to a link vertex (an OUT slot) or a
link vertex as payer to c (an IN slot); per link vertex there are 2 OUT and 2 IN slots (the two chiralities).  For a slot, each
position above is a vertex of the picture (or outside it) and carries the picture's letter set V_p there; the endpoints carry
their letters too (always exact in this world's pictures).

* OUT slot (c pays): counts iff it SURELY matches: payer letter set inside u, payee letter set inside v, and V_p inside the
  key's set X_p at every listed position.
* IN slot (c is paid): counts iff it POSSIBLY matches: every one of those sets meets the key's set (nonempty intersection).

The key's coefficient in c's row is

* sender rows (c = 5):              (# OUT slots that count) - (# IN slots that count)
* receiver and cons2 rows (c = 7, 6): (# IN slots that count) - (# OUT slots that count)

## 5. The world LP and where a key enters (variables t free, minimise t)

| row | constraint at the optimum | picture used for the key |
|---|---|---|
| sender (each admissible 5 label (w, H, F): 26,280) | base(y, g, r, rr, z, zr) + key terms + t >= 1 | link w_0..w_4 exact; apex h_k between w_k, w_{k+1}: S if H_k = 0, B if H_k = 1; a link 6 w_k has one private (its neighbour opposite the 5) with class S (F_k = 0) or B (F_k = 1); a link 7+ has d - 5 wildcard privates; nothing else |
| receiver (W16's 110,087 d = 7 world labels (w, s)) | base(y, M, Q7, lQ, lq, q, x, r, rr, z, zr) + key terms - t <= 1 | centre 7; link w_0..w_6 and apexes s_0..s_6 exact (s_j between w_j and w_{j+1}); a link 6 w_j has one private (its neighbour opposite c) with mask pmask(7, w_{j-2}, w_{j-1}, w_{j+1}, w_{j+2}, s_{j-2}, s_{j-1}, s_j, s_{j+1}) minus the f2b extra6 letters; a link 7 w_j has two privates (its 3rd neighbours from c): the one next to s_j gets MASK[(+1, w_{j+1}, s_j, w_{j+2}, w_{j+3}, w_{j+4}, s_{j-1})] minus the f2b extra7 letters when w_{j+1}, s_j are both <= 6, else the wildcard, and the one next to s_{j-1} likewise with (-1, w_{j-1}, s_{j-1}, w_{j-2}, w_{j-3}, w_{j-4}, s_j); a link 5 has no private.  pmask / MASK are the section-14' kill tables of the loaded stack (patched298) |
| cons2 (each 6 label (L, s): 1,424 non-R6 6-links x apex words over {5,7}: 81,136) | relaxed model c6le: sum g - sum h + key terms - t <= 0 (equality model: sum g - sum h + key terms = 0) | link L_0..L_5 exact (letters 5..9); apex s_i between L_i, L_{i+1}: S if s_i = 5 (the ap witness of {5,6}), B if s_i = 7 (witness of {7,8,9}); every private a wildcard |
| mrow (h <= M, q <= Q7, lq <= lQ; W16's closure over the base keys) | h - M <= 0 etc. | keys have NO terms in mrow rows and generate no mrow rows |

Here "base(...)" is W16's row (st21_w10 sender_row / recv_spec / cons2_row, family set `all` = rr z zr q Q7, with K* NOT as
W16's ('K', 0) column but as the key `KS`).  Caps: x, lq, z, zr, rr, q and every key at most 3; all variables >= 0.  Labels
whose rows are identical (same full coefficient vector, key terms included) are kept once.  Payee letters 8 and 9 never occur
for a 7 payer in this world (receiver links are in {5,6,7}); there are no rows for 8+ vertices.

In row terms, with the indices of the receiver picture (c = 7, link w_j, apex s_j), the positions are:

* OUT slot c -> w_i, sg = +1: S.L+k = w_{i+k}, S.L-k = w_{i-k}; S.A+1 = s_{i+1}; S.A-1 = s_{i-2}; R.L+2 = s_i; R.L-2 = s_{i-1}.
  (sg = -1: mirror: S.L+k = w_{i-k}, S.L-k = w_{i+k}, S.A+1 = s_{i-2}, S.A-1 = s_{i+1}, R.L+2 = s_{i-1}, R.L-2 = s_i.)
* IN slot w_i -> c, sg = +1 (S.L+1 = w_{i-1}): S.L+1 = w_{i-1}, S.L-1 = w_{i+1}, S.L+2 = s_{i-1}, S.L-2 = s_i, S.L+3 = w_i's
  private next to s_{i-1} (= s_i if w_i = 5), S.L-3 = w_i's private next to s_i (= s_{i-1} if w_i = 5; for w_i = 6 both are its
  single private), S.A+1 = w_{i-1}'s private next to s_{i-1} (= s_{i-2} if w_{i-1} = 5), S.A-1 = w_{i+1}'s private next to s_i
  (= s_{i+1} if w_{i+1} = 5), R.L+2 = w_{i-2}, R.L-2 = w_{i+2}.  (sg = -1 is the mirror.)

The same formulas hold in sender and cons2 pictures with their own degree (indices mod 5 or 6) and their apex classes /
private classes.

## 6. Worked examples (counts from the code; each was also checked by hand against section 5)

Coefficient = the key's entry in the row; "pay" = OUT slots that surely match, "get" = IN slots that possibly match.

**Receiver R7 w = 5575577, s = 5775777** (w_2, w_5, w_6 are 7s; their privates are wildcards because a neighbouring apex is 7):

| key | rule | pay | get | coefficient |
|---|---|---|---|---|
| A1 | EDGE(7->B)[S.L+1=S S.L+2=5 S.L-2=5 S.A+1=S] | 4 | 0 | -4 |
| gk00_10 | EDGE(7->7)[S.L+1=S S.L+3={567} S.L-1=S S.L-3={567} S.A+1=5 S.A-1=5 R.L+2={67} R.L-2={67}] | 2 | 0 | -2 |
| gk01_18 | EDGE(5->7)[S.L+1={67} S.L+2=7 S.L-1=5 S.L-3=7 S.A-1=B] | 0 | 4 | +4 |
| gk02_24 | EDGE(7->7)[S.L+1={67} S.L+2={67} S.L+3={567} S.L-1=S S.L-2=7 S.L-3={567} S.A+1={567} S.A-1=5 R.L+2={57}] | 0 | 2 | +2 |
| gk02_26 | EDGE(7->5)[S.L+1={5689} S.L+2={567} S.L+3={5678} S.L-1={5789} S.L-2=S S.L-3={5678} S.A+1=7 S.A-1={567} R.L-2=B] | 2 | 0 | -2 |

Hand check of A1's 4: OUT c -> w_2: sg = +1 gives S.L+1 = w_3 = 5, S.L+2 = w_4 = 5, S.L-2 = w_0 = 5, S.A+1 = s_3 = 5 (match);
sg = -1 gives w_1 = 5, w_0 = 5, w_4 = 5, s_0 = 5 (match).  c -> w_5: only sg = -1 (w_4, w_3, w_0, s_3).  c -> w_6: only sg = +1
(w_0, w_1, w_4, s_0).  IN slots: every link 7 has a 7 apex at S.L+2, so none can match: get = 0.

**Sender S w = 55777, H = 11011 (apex classes B B S B B), no link 6:**

| key | rule | pay | get | coefficient |
|---|---|---|---|---|
| gk01_18 | EDGE(5->7)[S.L+1={67} S.L+2=7 S.L-1=5 S.L-3=7 S.A-1=B] | 2 | 0 | +2 |
| gk02_26 | EDGE(7->5)[...as above...] | 0 | 1 | -1 |

Hand check of gk01_18: OUT c -> w_2 with sg = +1: S.L+1 = w_3 = 7, S.L+2 = w_4 = 7, S.L-1 = w_1 = 5, S.L-3 = w_4 = 7,
S.A-1 = apex(w_0, w_1) = h_0 = B (inside B): sure.  c -> w_4 with sg = -1: w_3 = 7, w_2 = 7, w_0 = 5, w_2 = 7, h_0 = B: sure.

**cons2 C L = 567767, s = 755555 (apex classes B S S S S S):**

| key | rule | pay | get | coefficient |
|---|---|---|---|---|
| gk04_45 | EDGE(6->5)[S.L+1={5789} S.L+2={567} S.L+3={5678} S.L-1={689} S.L-2={567} S.L-3={5678} S.A-1=S R.L-2=B] | 1 | 0 | -1 |
| gk02_82 | EDGE(6->5)[S.L+1={5689} S.L+2={567} S.L+3={567} S.L-1={6789} S.L-2=S S.L-3=7 S.A+1=S] | 1 | 0 | -1 |

Hand check of gk04_45: OUT c -> L_0 (the 5) with sg = -1: S.L+1 = L_5 = 7, S.L+2 = L_4 = 6, S.L+3 = L_3 = 7, S.L-1 = L_1 = 6,
S.L-2 = L_2 = 7, S.L-3 = L_3 = 7, S.A-1 = apex(L_2, L_1) = s_1 = S, R.L-2 = the 5's neighbour before L_1 = s_0 = B: sure;
sg = +1 fails at S.L+1 = L_1 = 6.

The base rows and pictures of these three labels are in `primal_t0_summary.json` (`examples`).

## 7. The t = 0 primal (round 7 export)

* `primal_t0_relaxed_float.json`: every variable of the solved LP (t = 0, 29,134 variables: g, h, M, q, Q7, lq, lQ, y, x, r,
  rr, z, zr and the 87 key amounts `E`), floats; variables absent are 0.
* `primal_t0_relaxed_rational.json`: every value rounded to n / 10^12 and clipped to its bounds.
* `primal_t0_summary.json`: md5s, the float and rational row violations by row type (all world rows at t = 0), the examples.
