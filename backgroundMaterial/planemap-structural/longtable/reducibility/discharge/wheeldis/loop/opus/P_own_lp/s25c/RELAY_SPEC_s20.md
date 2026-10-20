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

## 20.9 Conditioning on Explore's survivor region (rounds 8d59c29e and 53 / 337c5d8b)

Explore's survivor region for the face binder: apex t >= 6, all six privates >= 6 (here p01, p02 of w0, and the 6s'
privates). Restricting the cluster contexts to that region removes contexts and never adds any:
- level 1 (`fy`): the negative columns (-3/13, -1/13) come from the cert's SENDER contexts (far e-vertex small) against
  the binder's own s2 = 7; neither reads a private or t, so they are unchanged under any restriction of the receiver's
  contexts;
- levels 2-3: the lifting LP only loses binder contexts (t = 5 was already excluded by R5 at s3), so it stays infeasible;
- F6: every lifting with p1, p6 in {6..9} is in the feasible list of 20.8, so F6 stays null.

---------------------------------------------------------------------------------------------------------------

## §s25c-g: reading g7_ names

Source: the 10 names of explore's round-53 held set on row 7 7665566/6765766 (c9cb6184), as copied by Studio in
dc1ff9f9 (`loop/studio/sender_held/g7_53/held53_7_7665566_6765766.txt`; 4 D, 6 C, two engines). They are copied to
`s25c/g7_names.txt` (first field of each data line). Code: `s25c/pricer25g7.py` (pricing) and the `g7` flag in
`s25c/prelay2.py` (rows). Nothing below needs that code.

### g.1 The cluster frame of a d = 7 row (w, s)

u (letter 7), link w_0..w_6, apexes s_0..s_6 (s_I adjacent to w_I and w_{I+1}), as in §4.1. Ring 2 is the s_I plus the
**privates**: w_I has deg(w_I) - 5 privates p_{I1}, p_{I2}, ..., its neighbours not adjacent to u, listed in ring-2
order from s_{I-1} to s_I (so the ring-2 cycle is ... s_{I-1}, p_{I1}, ..., p_{Ik}, s_I, ...). A five has none, a 6 has
p_{I1}, a 7 has p_{I1}, p_{I2}. **Ring-3 vertices** are named by the set of their ring-2 neighbours: t(a/b/..) is the
vertex outside the 2-ball adjacent to exactly the ring-2 vertices a, b, .. . (For a five apex s_I whose two ring-2
neighbours are s_{I-1} and s_{I+1}, its private is t(s_{I-1}/s_I/s_{I+1}).) This is the frame of §14′/§17
(`rings.Layered`), and the 2-ball is assumed to be this disc.

### g.2 The name

```
g7_<C><W>_<S>_<T>
C  = 'u' : the centre is a vertex of the configuration, of degree 7;  '-' : the centre is not in it (any degree)
W  = 7 chars, w_0..w_6;  S = 7 chars, s_0..s_6;  T = 10 chars, the slots in this fixed order:
     p01 p02 p11 p21 p51 p61 t(p21/s2) t(s2/s3/s4) t(s4) t(p51/s4)
each char: a letter 5..8 = that vertex is an interior vertex of the configuration with exactly that degree;
           '.' = not an interior vertex (unconstrained)
```

The coordinates are those of the name's own row R* = 7 7665566/6765766 (w = 7665566, s = 6765766). The name lists every
interior vertex of the configuration (Studio's frame check: degrees equal the kc line's, and every adjacency the frame
forces is present). A name is therefore a partial assignment N: {frame vertex -> exact degree}.

### g.3 Match rule (kills a cell)

A **cell** of a row is an assignment of letters to frame vertices: u, w, s from the row label, and the enumerated
privates and ring-3 letters. A name N kills a cell iff there is a symmetry g of the frame carrying R*'s labelled frame
onto the row's (g in the 14 rotations/reflections of the 7-cycle, applied to w, s, privates and t's together) such that
for **every** vertex x in N:
1. g(x) is a vertex the cell has a letter for: an **unknown** (not enumerated: outside the cell, a private of a >= 9
   spoke, the centre when C = 'u' and u has degree >= 8) **never matches**, whatever N[x] is;
2. that letter is exact and equals N[x]. Letter 9 means degree >= 9 and **never equals** N[x] (names hold 5..8 only);
3. if C = 'u', the centre has degree exactly 7.
'.' slots impose nothing. This is §14′'s strict rule: a constrained vertex on an unknown is no match.

The symmetry g maps: w_I -> w_{g(I)}; s_I -> s_I' where s_I' is the apex of the image edge; under a reflection
I -> -I, s_I -> s_{-I-1}, and a 7-spoke's privates swap order (p_{I1} <-> p_{(-I)2}); t(a/b/..) -> t(g(a)/g(b)/..).

A cell of a row is **forbidden** if some name kills it. A row whose every cell is forbidden is dropped; otherwise the
row's terms that read a private or a ring-3 letter are evaluated on the surviving cells only.

### g.4 Worked example

Name `g7_-..655.._..65..._...5......` (Studio: D, kc + dfast18, ring 8, m = 6).
- C = '-': the centre is not in it. W = `..655..`: w2 = 6, w3 = 5, w4 = 5. S = `..65...`: s2 = 6, s3 = 5.
  T = `...5......`: the 4th slot, p21 = 5.
- N = {w2: 6, w3: 5, w4: 5, s2: 6, s3: 5, p21: 5}: the 6 at w2 with private 5, its two five neighbours on the w3 side,
  the apex s2 = 6 between w2 and w3 and the apex s3 = 5 between the fives. A five, a five, an apex five: a 5-5-5 face
  (w3, w4, s3) next to the 6 w2 whose private is 5.
- On R* (identity g): w2 = 6, w3 = w4 = 5, s2 = 6, s3 = 5 hold, so every cell with p21 = 5 is killed.
- On the cert binder of st24bL, 7 7665566/6675676, the identity fails (s2 = 7). The reflection I -> -I gives
  w2 -> w5 (6), w3 -> w4 (5), w4 -> w3 (5), s2 -> s4 (6), s3 -> s3 (5), p21 -> p51: all hold, so **p51 = 5 is
  forbidden** (the 6 w5's private).
- The name constrains only the 6's window plus its private, with no centre, so it is LP-visible: for any receiver of
  any degree and a 6 at w_j, p_j = 5 is killed when (w_{j+1}, w_{j+2}, s_j, s_{j+1}) = (5, 5, 6, 5), or mirrored
  (w_{j-1}, w_{j-2}, s_{j-1}, s_{j-2}) = (5, 5, 6, 5). That is the `g7` flag's whole effect on the amask (§14′ use).

### g.5 The 10 names on the st24bL binder (reflection, our coordinates)

| name | kills (cell constraints) | LP-visible (one 6's window + its private)? |
|---|---|---|
| g7_-..655.._..65..._...5...... | p51 = 5 | **yes** (`g7` flag) |
| g7_u76.5566_6..5..._..5....... | p61 = 5 | no: needs w2, w3, s3, centre |
| g7_-..655.._..65..._...5..5... | p51 = 5, t(p51/s4) = 5 | no (ring 3); subsumed by the first on cells |
| g7_u..655.._..65..._...5..5... | p51 = 5, t(p51/s4) = 5 | no; subsumed |
| g7_-..655.._..657.._...5.....5 | p51 = 5, t(p21/s2) = 5 (s2 = 7) | no; subsumed |
| g7_-..655.._..657.._...5....5. | p51 = 5, t(s2) = 5 (s2 = 7) | no; subsumed |
| g7_-.6655.._..65..._..55...... | p61 = p51 = 5 | no (two privates); subsumed |
| g7_-..655.._.765..._..55...... | p61 = p51 = 5 | subsumed |
| g7_-.6655.._.765..._..55...... | p61 = p51 = 5 | subsumed |
| g7_u7665566_6.65..._..5...5... | p61 = 5, t(p51/s4) = 5 | no; subsumed by the second |

On private cells (ring-3 letters left free, so a kill that needs a ring-3 five leaves the cell alive through the other
ring-3 letters) the 10 names forbid exactly p51 = 5 and p61 = 5. Together with filt16's p21 != 5: the survivors have
p21, p51, p61 >= 6, which is Explore's round-53 region on the 6-spokes.

### g.6 Pricing against cert_st24bL, without and with g7 (exact; `pricer25_g7.log`, `pricer25_g7_fy.log`)

Cluster rows with exact privates: the binder's weight 3/13 is spread over its private cells, and in a cell its four M
terms are the exact h2 of the cell's privates (the two U = 7 mrowR2 rows of the cert, used only by the binder, get weight 0).

| class | without g7 | with g7 |
|---|---|---|
| existing columns only (cluster rows read the privates) | **lifting feasible: null** (cell p11, p21, p51, p61 = 5, 6, 5, 5 reproduces the cert: its mrow chain used h at p51 = 5) | **infeasible: h(7,5,6,5,7,6,5,7), the 6 w5 paying with private 5, has rc -3/13 under every lifting** |
| + fy (z, level 1) | infeasible, z (7,5,5,6,6;0,0,*,*,0) -3/13, z (9,..) -1/13 | infeasible, same z columns and the h above |
| Explore's region (all privates >= 6), existing columns | infeasible, h above -3/13 | same |

So g7 alone breaks cert_st24bL: the cert's binder load needs the w5 6 to pay with private 5 (M[7566657] >= h at p = 5),
and g7_-..655.._..65..._...5...... forbids exactly that. The engine's own check agrees: lowerR2 with `g7` on
cert_st24bL is INVALID (`lower_oldcert_g7.log`): M at the binder's old mask-31 signature, now unused, rc -3/13; the
binder's signature becomes mask 30, whose candidate set has no p = 5 key. (Two U = 9 signatures of the d = 10 rows
change the same way, rc -1/26 each.)

## 20.10 Column "t pays s3" (coordinator, from s26r's census), priced

In the binder, t = t(s2/s3/s4) = s3's private, adjacent to the face five s3; s26r finds t is the one forced big when
the privates are 6 and ring 3 is otherwise small. In section 1 terms the column is the five s3 sending z to its big
spoke t, the face (w3, w4) being OPPOSITE t in s3's link: s3's link read from t is n = (T, s4, w4, w3, s2), with
(n2, n3) = (5, 5). That is exactly the k-vertex case of the z key (level 3: h2 = the face's far e-vertex u, which t
reads only through a cluster row; h0, h4 = the hats of s3 next to t, i.e. t's link vertices beside s2 and s4, read
by s3 as classes). Keying it on more of t's own link refines the key only on t's side, which s3 cannot read beyond
those two hats, so the key cannot be finer than level 3's on the five's side.

Pricing (cert_st24bL, level 3 run, `pricer25_L3.log`): the only cert sender with a big opposite its face is 55696
[0,0,0,0,0|0,0] (weight 1/13), whose opposite big is a 9 (t >= 9). Its column z(9,6,5,5,6; 0,*,0,*,0) has no weighted
receiver: **rc = -1/13**, in the apex >= 6 region (t = 9). For t = 7 and t = 8 no cert row touches the column:
**rc = 0** (null at this dual). Any refinement by t's link letters keeps the -1/13 (a sender weight with no matching
receiver stays unmatched under any split).

## 20.11 Results (written after the runs)

| run | flags (on top of st24b's) | keeppen at the 3 h cap | nosep LOWER-R2 | upper |
|---|---|---|---|---|
| st25y | `fy` | 14 iterations, t = 0.147708 (iter 12-13), still adding ~450 rows/iter, worst violation 0.19 | **VALID 226/1531 = 0.147616** (182 rows) | none: not converged, so no sol and no upperR2 |
| st25yg | `fy g7` | 14 iterations, t = 6/43 from iter 7 on, worst violation 0.25 | **VALID 6/43 = 0.139535** (58 rows) | none |

- Regression with the new flags off: LOWER-R2 VALID 2/13 on cert_st24bL (`val_off_lower.log`).
- So t*(fy) is in [226/1531, 2/13] and t*(fy + g7) in [6/43, 2/13]. The lower ends allow gains of up to 0.00623 and
  0.0143, both above the 0.005 kill line, but neither is shown: without a converged upper bound there is no gain.
- cert_st25yL is INVALID once g7 is on (`lower_st25yL_g7.log`): it too pays the binder with a 6 whose private is 5.
- cert_st25ygL (6/43) is VALID with `g7` alone and with `fy` alone (`lower_st25ygL_g7only.log`, `lower_st25ygL_fyonly.log`).
  It does not use z, so it is the lower bound of a partial row set, not a property of either column.
- Binders of cert_st25yL: the face 7 7665566/6675676 at 0.094 (it was 0.231), then 7 8565666/5676655 and
  7 7665566/6675666 at 0.038, and d = 8, 9, 10 rows. Senders: face fives 55667 [1,0,0,0,0|1,1], 55767, 55669 [1,0,1,0,0], 55668, 66669.
- Binders of cert_st25ygL: no face 7 row at all. Receivers: 8 86555665/56866665, 8 85566556/66666855, 10 6565656565/6556666666
  (0.070 each), 9 655666566/666556655. Senders: 66669, 56696, 56668, 56688, 56858.
