# RELAY_SPEC section 20: Stage 25, face-cluster columns (flag `fy`; cluster levels 2-3 priced only)

Opus, 19 Oct 2026. Written before the solve result. Engine copy: `P_own_lp/s25c/` (s24d's `pcheck.py` + `prelay2.py`;
backup `prelay2_st24_backup.py`; md5s in `engine_md5_orig.txt` (as copied) and `engine_md5.txt` (with `fy`)). The only
change to `pcheck.py` is a `price25` command that execs a pricing script (`pfile=`, default `pricer25.py`).
Base class: st24b (`xon apexcls filt16 killtab=s25/f/kill/kill6 hat5 consall`, `s25/argsA59.txt` = 0125c46b),
t* = 2/13. Section 1 sign convention throughout: a five starts at +1 and sends; a big's load (inflow) is capped at
d - 6 + t. In the FINDINGS mirror ("the 7 pays its fives") every transfer below reads as "a big adjacent to the face
pays into the face".

## 20.1 The cluster

Let u be a big and F = (a, b, c) a 5-5-5 face. F's surrounding ring is the 6-cycle

```
R(F) = (e_ab, k_b, e_bc, k_c, e_ca, k_a)
e_xy = the third vertex of the other face on edge xy;   k_x = x's one neighbour adjacent to neither face-mate
```

Every ring vertex is adjacent to a face five (e's to two, k's to one). A big ring vertex is a big "adjacent to the
face". In the binder 7665566/6675676 (u = 7, face (w3, w4, s3)), R(F) = (u, w5, s4, t, s2, w2) = (7, 6, 6, t, 7, 6),
where t = s3's private (the vertex adjacent to s2, s3, s4; Explore 8d59c29e's "ring-3 apex").

What u's receiver row reads of R(F), and of the hats of a link five v = w_i (hats h0..h4 of v, h_k between v's spokes
n_k and n_{k+1}, read from u: n0 = u, n1 = w_{i+1}, n2 = s_i, n3 = s_{i-1}, n4 = w_{i-1}):

| hat of v | vertex | u's standard row (st24b) | cluster level 2 | cluster level 3 |
|---|---|---|---|---|
| h0 = hat(u, n1) | w_{i+2} | exact (link) | | |
| h4 = hat(n4, u) | w_{i-2} | exact (link) | | |
| h1 = hat(n1, n2) | s_{i+1} if n1 = 5 (n1's whole link is known); else n1's private | exact iff n1 = 5 | | |
| h3 = hat(n3, n4) | s_{i-2} if n4 = 5 | exact iff n4 = 5 | | |
| h2 = hat(n2, n3) | if (n1, n2) = (5, 5): the private t of the face apex five s_i; if (n4, n3) = (5, 5): the private of s_{i-1} | unseen | **read** (new row type: the face apex five's own link) | read |
| h2, k-vertex case | if (n2, n3) = (5, 5): e of the face (v, s_i, s_{i-1}) | unseen | unseen | **read** (new row type) |

So the cluster row of level 2 is the receiver row plus, for each 5-5-5 face at u (consecutive link fives w_i, w_{i+1}
with s_i = 5), the private t of s_i: exactly "the face's full surrounding ring" of the coordinator's steer, with t the
one ring vertex the standard row misses. Level 3 adds, for each face at which u is the k-vertex, the face's far
e-vertex. The five's own sender row reads all five hats as classes (hat5), so every level is visible from the five's end
as a class.

## 20.2 Column family z (flag `fy`): five -> big spoke, keyed on the face ring both ends read

z[K] >= 0 is charge a five v sends to a big spoke u, **in addition to** y[root] (it is stage 13's zh column with a finer
key). Its key, at level L:

```
n  = v's link read from u: (U, n1, n2, n3, n4), U = min(deg u, 9)
h  = (c2(h0), c2(h1), c2(h2), c2(h3), c2(h4)),  c2: {5,6} -> 0, {7,8,>=9} -> 1
vis(n) = (True, n1 = 5, L >= 2 and ((n1,n2) = (5,5) or (n4,n3) = (5,5)) [or L >= 3 and (n2,n3) = (5,5)], n4 = 5, True)
hm_k = h_k if vis(n)_k else 2 (masked)
K  = min( n + hm,  (U, n4, n3, n2, n1) + reversed(hm) )            (reflection canonical)
```

The mask is a function of the five's link n alone, so both ends know which entries are read. The engine flag `fy`
implements **level 1** (`fykey`, `fy_sender_key`, `fy_recv_key` in s25c/prelay2.py). Levels 2 and 3 are priced only
(20.5), for the reason in 20.6. Level 0 (h1, h2, h3 all masked) is stage 13's zh key.

**Both ends read K (level 1).**

| entry | five v (senderR2 context: canonical word w, hat classes H; u = w_j) | big u (receiverR2 (d, w, s), v = w_i) |
|---|---|---|
| n | (w_j, w_{j+1}, ..., w_{j+4}) exact | (U, w_{i+1}, s_i, s_{i-1}, w_{i-1}) exact |
| h0 | H[j] | c2(w_{i+2}) |
| h1 (iff n1 = 5) | H[j+1] | c2(s_{i+1}): w_{i+1} = 5 has link (u, w_{i+2}, s_{i+1}, s_i, w_i), so its other common neighbour with w_{i+2} is s_{i+1} = v's hat between w_{i+1} and s_i |
| h3 (iff n4 = 5) | H[j+3] | c2(s_{i-2}), the mirror |
| h4 | H[j+4] | c2(w_{i-2}) |

**Physical test** (`phys25.py`, log `phys25.log`): random planar 2-balls around a five v with a big spoke u of degree
7..10, explicit rotation lists for v's small spokes and for u, every reading made by one generic rule (the common
neighbour of two adjacent vertices other than a third, taken from a rotation list); the five's word and hats are
canonicalised exactly as `SENDERS`/`R2_sender_rows`, u's link is read in a random orientation and rotation.
**179,455 (five, big) pairs, 0 mismatches. Broken-key control (u reads s_{i+2} for s_{i+1}): 25,794 mismatches.**

## 20.3 Rows (level 1, flag `fy`; everything not listed is st24b)

- **senderR2**: + sum over big spokes j of z[fy_sender_key(w, H, j)]. hat5 already enumerates every hat class, so no
  context is added; fewer contexts collapse in the coefficient dedupe.
- **receiverR2** (every d): load + sum over link fives w_i of z[fy_recv_key(...)].
- **Window**: at a five position, `W[a, b, 0, e, f, p, q, r, s] += z[fy_recv_key(U, a, b, e, f, p, q, r, s)]` (a..f =
  w_{i-2..i+2}, p, q, r, s = s_{i-2..i+1}). All slots are 9-slot window slots, so d = 7..17 stays exhaustive and exact.
- **Class table** (jsep3, solver only): c = five class = 470000 + ((b*5+e)*5+q)*80 + r*16 + bits(c2 a, c2 f, c2 p if b = 5,
  c2 s if e = 5); max 479,999, disjoint from the other classes (<= 469,375) and below the hat5 fold base 500,000.
- **Tail** d >= 18: z is part of W9's load; relaxed DP and Karp as before.
- **lowerR2/upperR2**: z goes through the generic ledger and the stored `z` field, as zh did.
- **Soundness**: each z transfer is one amount on one five -> big edge under a key both ends compute identically (table
  and physical test); every five is in an enumerated sender row and every big in a receiver row, so charge is conserved.
  With z = 0 the class is st24b's, so t*(fy) <= 2/13. Regression with the flag off: s25c engine gives LOWER-R2 VALID
  2/13 on cert_st24bL (`val_off_lower.log`).

## 20.4 Restructuring note (why the old cert must change)

z is an extra column on existing rows, not a new row with zero dual, so the old cert is tested directly: it stays valid
iff every z column has rc >= 0. For cluster levels 2-3 the receiver rows are SPLIT by the hidden ring letters
(t, or the far e); the old cert is then valid iff it can be lifted: each cert row's weight spread over its split rows
(and each sender's weight over the class contexts with the same old coefficient row) so that every z key balances.
That is a small LP (`pricer25.py`); infeasible means no lifting exists and the old cert cannot survive.

## 20.5 Pricing (exact; `pricer25_*.log`, and the engine's own lowerR2 in `lower_oldcert_fy.log`)

**cert_st24bL (2/13, argsA59):**

| level | z keys touched | lifting | columns with rc < 0 (rc) |
|---|---|---|---|
| 0 (zh) | 7 | feasible: **null** | none |
| 1 (`fy`) | 9 | infeasible | (7,5,5,6,6; 0,0,*,*,0) **-3/13**; (9,5,5,6,6; 0,0,*,*,0) -1/13 |
| 2 (+ t) | 14 | infeasible | (7,5,5,6,6; 0,0,1,*,0) -2/13; (7,5,5,6,6; 0,0,0,*,0) -1/13; (9,5,5,6,6; 0,0,0,*,0) -1/13; (9,5,5,9,5; 0,0,0,0,0) -1/13 |
| 3 (+ far e) | 15 | infeasible | level 2's four, plus (9,6,5,5,6; 0,*,0,*,0) -1/13 |

(* = masked.) lowerR2 of the s25c engine with `fy` on cert_st24bL: INVALID with exactly the two level-1 columns at
-3/13 and -1/13 (`lower_oldcert_fy.log`).

**The binder, read off level 1.** The receiver 7 7665566/6675676 (weight 3/13) takes y[7|5566] from its face five w4.
In u's row, w4's hat h1 (between face-mate w3 and the face apex s3) is s2, the other e-vertex of the face, and s2 = 7.
Every cert sender that pays y[7|5566] (55667 [0,1,0,0,0|0,1] weight 2/13, 55667 [0,0,0,0,0|1,1] weight 1/13) has that
hat **small**. So the cert pays the binder with fives from faces whose far e-vertex is small, while the binder's own
face has it big. z with h1 separates the two: the senders' key (7,5,5,6,6;0,0,*,*,0) has no receiver weight at all
(rc = -3/13), and the binder's key (7,5,5,6,6;0,1,*,*,0) has no sender weight. The same split happens for the 9: 55669
[0,0,1,0,0|0,0] pays y[9|5566] with that hat small. No lifting fixes it: every cert sender has a single class context.

Level 2 adds t: the 55667 [0,1,0,0,0|0,1] context has H1 = 1, i.e. t big (in canonical coordinates H0 is the far e-vertex and H1 = t, Explore's "all slots >= 7" survivors); its key
then also misses the binder unless the binder takes t big. t = 5 never occurs (s3's link (5,5,6,5,7) is R5, the rsst001
kill); the lifting may put the binder on t = 6 or t big, and no split balances.

**Older certs (level 1, argsA55, `s22/f/kill/kill6`; receivers at their labels only):**

| cert | t | z rc < 0 | most negative |
|---|---|---|---|
| cert_st20xL | 16/101 | 7 | (9,5,5,7,6;0,0,*,*,0) -7/303, on 55769 vs the d = 9 rows 655665556/657565955, 655566556/657656575 |
| cert_st23rL | 16/101 | 11 | (7,5,5,9,6;0,1,*,*,1) -13/303 (55769 [1,0,1,0,0]); (7,5,5,9,5;0,0,*,0,0) -4/101 (55759) |

## 20.6 What is not built, and why

- **Level 2/3 (t, far e) in the engine.** t is shared by the two face fives w_i, w_{i+1}, so the window would need the
  pair (or a per-face max, which is sound but makes the separator return rows the LP already satisfies). Level 1
  already carries the largest negative column (-3/13 on the binder), so level 1 is the minimal version.
- **Big adjacent to the 7, not the face (u -> w0 in the binder).** The existing x on edge (u, w0) has equal in and out
  keys in the binder (both sides read (6,6,6)), so it cancels. A face-aware x needs w0's row to read u's face, at
  distance 2-3 from w0: a row that reads a big spoke's whole link plus that spoke's face. Priced analytically: the out
  column would have coefficient -1 only in the binder (weight 3/13) and no weighted receiver, so rc = -3/13 too; not built.

## 20.7 Run and kill line

`cmd_st25.sh`: solveR2 keeppen (xpen 1e-3, warm = s22h, s23h, st24b run1 and final rows, 3 h cap), solveR2 nosep,
lowerR2 on the nosep cert, upperR2 nomax on the keeppen solution (all 1,424 conservation types). Kill line: gain below
0.005, i.e. the upper bound on the solution itself is not <= 2/13 - 0.005 = 0.148846.

## 20.8 Variant F6: the far-side 6 (coordinator steer, priced before any solve of it)

Unit widened across the 7: the cluster row of the binder 7665566/6675676 also reads its two 6s next to the big spoke w0,
opposite the face (w1 and w6), exactly, with their privates p1 and p6; their M terms become the exact h2 of the actual
private. The far-side 6s' other outer neighbours (s0, s1, s5, s6, w0, w2/w5) are already in u's row.
Pricing (`pricer25f6.py`, `pricer25_F6.log`): the filt16 mask allows every private (31) at both 6s; **every one of the 25
liftings (p1, p6) keeps all reduced costs >= 0**, so cert_st24bL stays valid and F6 is null. Reason: the cert never loads
these two M terms (no mrowR2 row on their signatures; their rc is +3/13), so making them exact only adds load where
the dual already has slack. On the five's side the far-side 6 is the face five's hat h4 (= w_{i-2}), already read as a
class in the z key; a five cannot read its letter or private. A transfer keyed on the far-side 6 and its private would
need a row type at distance 3 from the face fives.
