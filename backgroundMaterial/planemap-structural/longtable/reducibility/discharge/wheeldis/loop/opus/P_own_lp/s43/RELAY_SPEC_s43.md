# RELAY_SPEC s43: fy cluster level 2 (flag `fy2`): the face apex's private t enters the z key

Opus, 20 Oct 2026. Written before any fy2 pricing or solve. This is a delta on `P_own_lp/s25c/RELAY_SPEC_s20.md` §20.1–§20.3
(fy, level 1) as ported in `s40f/RELAY_SPEC_s40f.md`. Everything not named here is s40f's engine (`s40f/eng`, flags
FQ + `rpatN=s39o/rpatN3.txt` + `fy`). Engine copy: `P_own_lp/s43/eng`. Sign convention as §20: a five starts at +1 and
sends; a receiver u of degree d has inflow capped at d − 6 + t.

Notation (as §20.1 and §4.1). u is the receiver, of degree d, U = min(d, 9). Its link is w_0..w_{d−1} in rotation order.
The apex s_i is the common neighbour of w_i and w_{i+1} other than u. Indices are mod d. Letters are 5, 6, 7, 8, 9, where
9 means degree ≥ 9. c2(x) = 0 if x ∈ {5, 6} and 1 if x ≥ 7. CLS2[0] = {5, 6}, CLS2[1] = {7, 8, 9}. For a link five
v = w_i, its link read from u is n = (U, n1, n2, n3, n4) = (U, w_{i+1}, s_i, s_{i−1}, w_{i−1}). Its five hats are
h_k = the vertex other than v on the face beyond the edge n_k n_{k+1} (n_0 = u, n_5 = n_0).

## 43.1 Faces and t (what is new)

A **face at u** is an index i with w_i = w_{i+1} = s_i = 5: the 5-5-5 face (w_i, w_{i+1}, s_i) shares the edge w_i w_{i+1}
with the face (u, w_i, w_{i+1}). Its **apex private** is

    t_i = the neighbour of s_i that is not w_i, w_{i+1}, s_{i+1}, s_{i−1}.

**Lemma 1 (the rotation of s_i).** If i is a face at u, s_i has the rotation (w_i, w_{i+1}, s_{i+1}, t_i, s_{i−1}).

Proof. w_{i+1} is a five with rotation (u, w_{i+2}, s_{i+1}, s_i, w_i). So (w_{i+1}, s_{i+1}, s_i) is a face and s_{i+1} is
the neighbour of s_i after w_{i+1}. Likewise w_i has rotation (u, w_{i+1}, s_i, s_{i−1}, w_{i−1}). So (w_i, s_i, s_{i−1}) is
a face and s_{i−1} is the neighbour of s_i before w_i. s_i has degree 5, so exactly one neighbour is left, between
s_{i+1} and s_{i−1}. That neighbour is t_i. □

**Lemma 2 (h2 is t).** Let i be a face at u.
- For v = w_i: n1 = n2 = 5 and h2(v) = t_i.
- For v = w_{i+1}: n4 = n3 = 5 and h2(v) = t_i.

Proof.
- For v = w_i, (n2, n3) = (s_i, s_{i−1}). The two faces on the edge s_i s_{i−1} are (w_i, s_i, s_{i−1}) and, by Lemma 1,
  (s_i, t_i, s_{i−1}). So the hat beyond n2 n3 is t_i.
- For v = w_{i+1}, (n2, n3) = (s_{i+1}, s_i). The faces on the edge s_{i+1} s_i are (w_{i+1}, s_{i+1}, s_i) and, by
  Lemma 1, (s_i, s_{i+1}, t_i). So the hat is t_i again. □

**Lemma 3 (no five is in two faces).** If w_i is in faces i − 1 and i, then its link from u is (U, 5, 5, 5, 5). That link
is R5 for every U (`isR5((U,5,5,5,5))` is True for U = 5..9). Such a w_i is already −∞ in the window (R5 at a link five)
and inadmissible in `admissible`. So every face has exactly two fives, w_i and w_{i+1}, and t is shared by exactly those
two. The engine asserts this on every receiver row it builds.

**Allowed classes.** For a face i, its allowed class set is

    A_i = { c ∈ {0, 1} : some letter x ∈ CLS2[c] has isR5((5, 5, s_{i+1}, x, s_{i−1})) False }.

That five-word is the degree word of s_i's link in rotation order (Lemma 1). If A_i is empty, set A_i = {0, 1}. This
fallback means fy2 never removes a receiver row: a row whose apex is R5 for every t stays, with both cells. That is
sound, since adding cells only adds constraints, and it keeps fy2 ⊇ fy ⊇ base exactly. isR5 is the engine's own (wheel
verdicts + fans), with letter 9 handled as at the link fives.

## 43.2 The z key at level 2

z[K] ≥ 0 is the charge a five v sends to a big neighbour u, in addition to y. It is the same column family as fy, with a
finer key:

    vis2(n) = (True, n1 = 5, (n1, n2) = (5, 5) or (n4, n3) = (5, 5), n4 = 5, True)
    hm_k    = h_k if vis2(n)_k else 2                      (h_k = c2 of hat k)
    K2(n,h) = min( n + hm, (U, n4, n3, n2, n1) + reversed(hm) )

This is §20.2's formula at L = 2, without the level-3 (k-vertex) term. It differs from level 1 (`fykey`) only in hm_2,
which is unmasked exactly when vis2(n)_2 holds. The mask depends on n alone, so both ends know whether h2 is read. Keys
are 10-tuples as at level 1. A level-1 key with hm_2 = 2 and no visible face is also a level-2 key, identical in both.

**Refinement.** Every level-1 key K1 is the image of the level-2 keys that refine it: replace hm_2 by 2 when vis2 holds.
Setting z2[K2] = z1[K1(K2)] reproduces any fy solution. So t*(fy2) ≤ t*(fy) ≤ t*(base), and with all z2 = 0 the
class is exactly the base class.

**Both ends compute K2.**

| entry | five v (senderR2 context: canonical word w, hat classes H, u = w_j) | big u (receiver row (d, w, s), cell τ, v = w_i) |
|---|---|---|
| n | (w_j, w_{j+1}, .., w_{j+4}) | (U, w_{i+1}, s_i, s_{i−1}, w_{i−1}) |
| h0, h1, h3, h4 | H[j], H[j+1], H[j+3], H[j+4] (as fy) | c2(w_{i+2}), c2(s_{i+1}) iff n1 = 5, c2(s_{i−2}) iff n4 = 5, c2(w_{i−2}) (as fy) |
| h2 (iff vis2) | H[j+2], the five's hat between n2 and n3 | τ_i if (w_{i+1}, s_i) = (5, 5) (face i); τ_{i−1} if (w_{i−1}, s_{i−1}) = (5, 5) (face i−1) |

τ_f = c2(t_f) is the cell's class for face f (§43.3). By Lemma 2, the two h2 columns name the same vertex. By Lemma 3, at
most one of the two receiver cases holds.

## 43.3 Rows

**senderR2.** The rows are the s40f rows (`R2_sender_rows`: every hat class enumerated, under hat5) with
`fy_sender_key(w, H, j)` replaced by K2 at every big spoke j. The coefficient dedupe (`seen`) runs on the new
coefficient rows, so contexts that differ only in the h2 class at a face are now separate rows. No context is added
or dropped. The row label is unchanged: (word, hat bits | fan bits).

**receiverR2, split by cells.** For an admissible (d, w, s), let F = (f_1 < .. < f_m) be its faces. Its cells are
τ ∈ A_{f_1} × .. × A_{f_m} (with m = 0 there is one cell, the empty one). Each cell is a row:

    load(d, w, s) [as s40f, with every five's fy key replaced by K2 read with τ]  −  t  ≤  d − 6

Only the z terms of the 2m face fives depend on τ. Every other coefficient, and the row's other columns, are s40f's.

The cert/info label is ('receiverR2', d, link, sv, cell). cell = ',' joined 'f:c' over the faces in increasing f, or ''
when m = 0. Example: '4:1' for 7766556/6567566 with t_4 big.

**Solve (`solveR2`).** When the separator returns (d, w, s), every cell of it is added (at most 2^m rows; m ≤ 2 at
d = 7). The `have` dedupe is per cell coefficient row. Warm files keep the 'R d link sv' format, and every cell of a warm
row is added.

**Window (separator, d = 7..17, exact).** At a five position (c = 0), with a..f = w_{i−2..i+2} and p, q, r, s = s_{i−2..i+1}:
- If vis2 is false, W += z[K2] as fy.
- If vis2 is true, W += UB_i = max over τ ∈ A of z[K2(τ)]. A is the five's face's allowed set, computable in the
  window:
  - right face (e, r) = (5, 5): s_i's link is (5, 5, s, ·, q);
  - left face (b, q) = (5, 5): s_{i−1}'s link is (b, c, r, ·, p) = (5, 5, s_i, ·, s_{i−2}).

The window is then an upper bound on every cell's load: each face's two fives are maximised separately. The new binary
jsep6 adds the exact coupling at the leaf. Here jsep6 = jsep5 with argv[7] (l3q file) allowed to be 'none', plus
argv[8] = the face file ZT, 2·5^9 doubles:
- ZT[2·idx + τ] = z[K2(τ)] at window index idx when that window is a five with vis2 true and τ ∈ A;
- ZT[2·idx + τ] = −1e300 otherwise.

At the leaf, for every face i (W(i) = W(i+1) = S(i) = letter index 0):

    corr_i = max over τ of (ZT[2·idx_i + τ] + ZT[2·idx_{i+1} + τ])  −  max_τ ZT[2·idx_i + τ]  −  max_τ ZT[2·idx_{i+1} + τ]

This is ≤ 0, since both windows see the same A (it depends only on s_{i−1}, s_{i+1}). tot += Σ corr_i, and the cut is
re-tested. All DFS bounds use WIN, which holds UB, so they stay valid upper bounds. A leaf's tot is therefore exactly
max over cells of the cell's load. Mode 0 (upperR2) is exhaustive and exact. Mode 2 returns (w, s) rows whose best cell
is violated.
- Mode 2 distinctness keeps the class table of fy unchanged. That table does not encode which fives pair into a face
  or the exact A. So two rows can share a signature and differ in their cells. This affects only which K rows one
  iteration returns, because the representative is the row's maximum, never whether a violated row exists.
- jsep6 is used for every d when fy2 is on, with BONUS and CLS as before and l3q at d = 7 only.

**Tail d ≥ 18.** Relaxed DP and Karp on W9, which holds UB: an upper bound, so sound, as in s40f.

**Conservation rows (cons2, mrowR2, mrowL).** These are unchanged. z appears only in senderR2 and receiverR2: no 6-centred
row and no M/h/lq row reads a z column. Charge conservation of z is the edge argument in §43.4.

**lowerR2.**
- A receiverR2 cert row must carry a cell, and the cell must be one of that row's cells (faces and A recomputed from
  the label).
- Its coefficients are the cell's. A missing or foreign cell is 'BAD CELL', which makes the cert INVALID.
- senderR2 rows are looked up by label in the fy2 sender rows.
- z is uncapped and priced as before: any z with rc < 0 makes the cert INVALID, or with ucap= it is priced at the cap.

**upperR2.**
- The sol JSON carries 'fy2': true.
- upperR2 refuses when the sol's fy2 flag differs from the run's, because level-1 and level-2 keys differ in h2.
- Sender rows are checked with K2.
- Receivers d = 7..17 are checked by jsep6 mode 0, exact over the cells. The tail is checked as above.

## 43.4 Soundness

1. **Each z2 charge is a discharging rule.** The rule is: "a five v sends z2[K] to each neighbour u of degree ≥ 7, with
   K = K2 of the edge (v, u)". K2 is a function of the planar graph, the degrees of v's link and of v's five hats. At
   v's end it is read from v's 2-ball (§43.2, five column). At u's end it is read from u's 2-ball plus t_i, a vertex at
   distance 3 from u (§43.2, big column). By Lemma 2 the h2 entries name the same vertex at both ends. The other
   entries are fy's, which are proved equal in §20.2 and by the s25c physical test. The mask depends only on n. So in
   any triangulation each transfer has a single amount, which both ends' rows count with opposite sign. Total charge
   is conserved.
2. **Every vertex is covered by a row that holds.**
   - A five's real context (its link word and its five hat classes) is one of the enumerated sender contexts. hat5
     enumerates all 2^5 hat classes, and the fan/R6 filters are s40f's. Its row is satisfied.
   - A receiver's real (d, w, s) is an admissible row (separation is exhaustive for d ≤ 17, and the relaxed tail is an
     upper bound for d ≥ 18). Its real τ (τ_i = c2(deg t_i)) lies in A_i:
     - if τ_i ∉ A_i, every letter of its class would make s_i's link R5, and s_i is a real five, which cannot be;
     - with the fallback A_i = {0, 1}, every τ is a cell.
     So the real cell is a row of the LP family, and its inequality holds.
   - The 6-vertices and conservation rows are unchanged. z never touches them.
3. **Nothing is assumed about t beyond its degree class and the R5 filter at s_i.** t may coincide with a vertex of u's
   2-ball. Lemma 1 still names it as s_i's fourth neighbour, so the reading and the R5 filter are unchanged.

## 43.5 Pricing against cert_q39n3A74L (step 3; `s43/pricer43.py`)

The cert comes from the class with no z. The lifting LP of §20.4 is over the cert's senderR2 and receiverR2 rows only.
- Each sender row's weight may be spread over the sender contexts of its word whose **no-fy** coefficient row equals
  the label context's.
- Each receiver row's weight may be spread over its fy2 cells.
- All other cert rows are unchanged, and their columns are unchanged.

Since old columns have identical coefficients across a row's split, they keep their reduced costs. The only test is
rc(z2[K]) ≥ 0 for every K2. Here rc = −(Σ_S λ coef − Σ_R λ coef) / tco, with tco = Σ_S w − Σ_R w.
- **(P1) lifting LP:** minimise the worst violation.
- **(P2) face-restricted lifting:** require rc ≥ 0 only for the z2 keys that occur in a cell of one of the 5 face rows.
- **Kill line:** at least one negative reduced cost on a face receiver row means (P2) is infeasible. That is, under
  every lifting some z2 column with a coefficient in a face row has rc < 0.
  - If (P2) is feasible, stop and report what h2 still cannot see.
  - If (P2) is infeasible, report the most negative columns at the (P1) optimum, the rows they touch, and the
    first-order gain Σ max(0, −rc)·cap at caps 0.05 and 0.1.

## 43.6 Results (written after the runs; the spec above was committed first, ccb15e11)

**Engine.** `s43/eng` = `s40f/eng` + `s43/port_fy2.py` (prelay2.py, pcheck.py) + `bin/jsep6` (from `jsep6.cpp`).
md5s are in `s43/engine_src_md5.txt`.

**Control (a): fy2 off reproduces s39o (A74).**
- lowerR2 on cert_q39n3A74L: **VALID 20/183**, log byte-identical to `s39o/run_n3_A74/lower.log` (`ctl_lower_off.log`).
- upperR2 nomax on sol_q39n3A74: **FEASIBLE 1/9**, identical modulo timings (`ctl_upper_off.log`).

**Control (b): keys and coupling.**
- `phys43.py` (`phys43.log`) builds explicit rotation systems around u, and every hat is read by a generic rule from
  both rotations that contain the pair. An independent key is checked against the engine's sender key and against the
  engine's receiver cell keys.
  - **253,282 (five, big) pairs on 67,603 rows (39,366 with a face), 0 mismatches. Lemma 2 checked on 95,984 face fives.**
  - Broken control (t read as s_{i+1}'s letter): 18,353 of 66,850 rows mismatch.
- `sep43chk.py` (`sep43chk.log`): jsep6 mode 2 at d = 7 and 8 with random z2.
  - Each returned load is compared with an independent Python max over cells.
  - **800 rows, all with a face, 0 mismatches.**
  - The decoupled UB (face file 'none') is strictly larger on 206 of them.

**Pricing (step 3, `pricer43.py` → `pricer43.out`, `why43.out`): kill line NOT passed.**
- Lifting LP over the 15 sender and 10 receiver rows of cert_q39n3A74L. The 5 face rows split into 2 cells each (t small
  or big, both allowed).
  - **(P2) is feasible with worst face-key rc = 0.**
  - The lifting puts every face row in its t-small cell (cells 4:0 and 3:0).
- The face rows' 8 z2 keys then have rc:
  - (7,5,5,6,6;0,1,0,·,0) +2/183;
  - (7,5,5,6,6;0,1,0,·,1), (7,5,5,7,6;0,0,0,·,0) and (7,5,5,7,6;0,0,0,·,1) exactly 0;
  - the four t-big keys 0 (untouched).
- Every cert sender that pays a face key has h2 = 0, i.e. t small:
  - 55667 [1,0,0,1,0|1,0];
  - 55667 [1,0,1,0,0|0,·];
  - 55767 [0,0,0,0,0], [0,0,0,1,0], [0,0,1,1,0].
  So t does not separate the face receivers from their payers.
- (P1) is INVALID with the 4 sender-only columns of s40f, now at level 2. None touches a receiver row:
  - z(7,6,6,6,6;0,·,·,·,1) −10/183;
  - z(7,5,5,6,6;0,0,1,·,0) −2/183 (55667 [0,1,0,0,0|1,1], the one paying sender with t big);
  - z(7,6,5,6,6;0,·,·,·,1) −2/183;
  - z(7,6,5,5,6;1,·,·,·,1) −2/183.
  First-order gain if capped at 0.05 / 0.1: 0.0044 / 0.0087, all from sender-only columns and none from the face rows.

**What level 2 still cannot see (exploratory pricing, `pricer43p.py`; not specified or built).**
- After t, the only masked hat of both face keys is h3, the private of the far-side 6 (w3 or w6). u's row knows it
  only through filt16's allowed-private mask.
- Unmasking it, with receiver cells over the 6's private classes allowed by amask ("2P", `pricer43p.out`): **(P2) is
  still feasible, rc 0.**
- Adding the fan class of a link-6 spoke as well, which u reads exactly as s_{i+1} or s_{i−2} ("2P+fan",
  `pricer43pf.out`): **(P2) is still feasible.**
- At 2P+fan the face five's z key is its whole sender context (n, all five hats, the visible fan). The only exception is
  the fan of the apex 6 (n3), which is at ring 3 from u.
- The cert pays each face row with fives whose own context is exactly that face five's context. Any five→big column
  keyed on the five's view therefore has equal sender and receiver weight on the face rows (rc = 0), at every cluster
  level.
- The face rows can only move with something that is not a five→big refinement. Two candidates:
  - a transfer out of the face 7 itself (big→big or 7→6, keyed on its face);
  - exact letters (5 vs 6 for t or the private), but the sender's hat5 rows read classes only, so the five end cannot
    match exact letters.

**Step 4 (A78 warm solve) was not run:** the kill line failed.
