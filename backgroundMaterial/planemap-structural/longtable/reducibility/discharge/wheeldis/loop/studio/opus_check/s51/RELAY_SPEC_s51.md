# RELAY_SPEC s51: "x-outer" (flag `xo`), the L2 big → big family x with outer second-ring side letters

s51, 21 Oct 2026. Written **before any engine code**. It is a delta on RELAY_SPEC §2.2 (x key), §4 (receiver rows) and §12
(R6x2 mode), on top of the s47 engine (`s47/eng`: l3qV, jsep7, fb code, the §44.8 lowerR2 repair). The motivation and the
exact source definition of the outer letters is `s50/REFINE_PRICE.md` / `s50/pricer50.py` (refinement `x_out`).

With `xo` **off** nothing changes (the old x of §2.2 is the default). With `xo` **on**, the old x columns are not used at
all; they are replaced by the refined columns `xo` and the credit columns `XQ` below. `xo` requires `xon`.

Notation as in RELAY_SPEC: `LET = (5,6,7,8,9)`, `LI[l] = l − 5`, letter 9 = degree ≥ 9, big = ≥ 7. A receiver u of degree d
has letter `U = min(d, 9)`, link `w_0..w_{d−1}`, second ring `s_0..s_{d−1}` (`s_i` = common neighbour of `w_i`, `w_{i+1}`
other than u). Indices mod d. The 9-slot window at position i is
`(a, b, c, e, f; p, q, r, s) = (w_{i−2}, w_{i−1}, w_i, w_{i+1}, w_{i+2}; s_{i−2}, s_{i−1}, s_i, s_{i+1})`.

---------------------------------------------------------------------------------------------------------------

## 51.1 The refined key (physical definition)

`xo[τo]` is the amount a big `fl` sends to an adjacent big `tl` (as x). The edge (fl, tl) has two sides. For a side with
common neighbour c, the old x reads `(c, a, b)`:
- `a` = the other common neighbour of c and **fl**;
- `b` = the other common neighbour of c and **tl**.

The refined side is the 5-tuple `(c, a, b, ea, eb)`:
- `ea` = the neighbour of c that follows a in c's rotation, going away from fl (the vertex of c's link adjacent to a, other than fl);
- `eb` = the neighbour of c that follows b in c's rotation, going away from tl (adjacent to b in c's link, other than tl).

So c's link reads, cyclically, `(tl, fl, a, ea, …, eb, b)`. If deg c = 5 then `ea = eb` (c's link is `(tl, fl, a, ea, b)`).
If deg c = 6 then `ea` and `eb` are the two link vertices of c opposite the edge, adjacent to each other. These are the
"outer (second-ring) letters" of s50: c's two second-ring neighbours, one next to a, one next to b. (R1)

```
sidex(c, a, b, ea, eb) = (((LI[c]*5 + LI[a])*5 + LI[b])*5 + LI[ea])*5 + LI[eb]                       (0..3124)
tauo(fl, tl, S1, S2)   = (((LI[fl]-2)*3 + (LI[tl]-2))*3125 + min(S1,S2))*3125 + max(S1,S2)            (0..87,890,624)
```

The two sides are unordered (reflection canonicalisation, as x). Coarsening to the old key drops `ea, eb`:
`tau(fl, tl, side(c,a,b), side(c',a',b'))`. Bounds `0 <= xo <= xcap`, **xcap = 3** (the same option and default as x). JSON
key `str(tauo)`. Decode: `hi = τ % 3125`, `lo = (τ // 3125) % 3125`, `(fi, ti) = divmod(τ // 3125², 3)`, `fl = 7+fi`,
`tl = 7+ti`; a side code `S` gives `(c, a, b, ea, eb)` = base-5 digits of S (most significant first) + 5.

## 51.2 Which end reads which letter

In receiver u, a big link vertex `w_i` (letter V) is at the other end of the edge u–w_i. Its two sides are
c⁺ = `w_{i+1}` and c⁻ = `w_{i−1}`. Read from u:

| side | c | common nbr of c and w_i | common nbr of c and u | outer letter next to `w_{i±2}` | outer letter next to `s_i` / `s_{i−1}` |
|---|---|---|---|---|---|
| + | `w_{i+1}` | `s_i` | `w_{i+2}` | `s_{i+1}` (**seen** by u) | `e⁺` (**unseen** by u unless c⁺ = 5) |
| − | `w_{i−1}` | `s_{i−1}` | `w_{i−2}` | `s_{i−2}` (**seen**) | `e⁻` (**unseen** unless c⁻ = 5) |

`e⁺` is c⁺'s neighbour after `s_i` going away from `w_i`: c⁺'s private `p_{i+1}` if c⁺ = 6, c⁺'s own unseen neighbour if c⁺ is
big, and `s_{i+1}` itself if c⁺ = 5. Mirror for `e⁻`.

The two terms of position i (exactly s50's `fin` / `fout`):

```
in  (w_i -> u):  tauo(V, U, (w_{i+1}, s_i, w_{i+2}, e+, s_{i+1}),   (w_{i-1}, s_{i-1}, w_{i-2}, e-, s_{i-2}))
out (u -> w_i):  tauo(U, V, (w_{i+1}, w_{i+2}, s_i, s_{i+1}, e+),   (w_{i-1}, w_{i-2}, s_{i-1}, s_{i-2}, e-))
```

So **u reads eb of the in-key and ea of the out-key** (the outer letter on u's side, next to `w_{i±2}`); the far end w_i reads the
other one (next to `s_i`, `s_{i−1}`), which is in w_i's own second ring. Both ends therefore compute the same physical key from
different visible letters, and the transfer is antisymmetric and conserved exactly as for x. (R2)

## 51.3 Unseen letters: the M-style credit XQ and its bound rows mrowX

**Visible side tuple.** Position i of receiver u gives two visible tuples

```
A+ = (w_{i+1}, s_i,     w_{i+2}, s_{i+1}, m+)       A- = (w_{i-1}, s_{i-1}, w_{i-2}, s_{i-2}, m-)
```

where `m±` is the **domain mask** of `e±` (bit k = letter LET[k] allowed):
- c = 5: `m = 1 << LI[o]` with `o` = the seen outer letter (`s_{i+1}`, resp. `s_{i−2}`): `e` is that letter. (R5)
- c = 6: `m = AU & NR6`, where (R3)
  - `NR6` = { p : not isR6(wheel) }, wheel = `(U, w_{i+2}, s_{i+1}, p, s_i, w_i)` for +, `(U, w_i, s_{i−1}, p, s_{i−2}, w_{i−2})` for −;
  - `AU` = 31 if `filt16` is off; with `filt16`, the OR over the two letters outside the window of the engine's
    `amask` of that 6 (the same function and kill table as M uses):
    - +: `OR_{x, y in LET} amask(U, w_{i−1}, w_i, w_{i+2}, x, s_{i−1}, s_i, s_{i+1}, y)` (x = `w_{i+3}`, y = `s_{i+2}`);
    - −: `OR_{x, y in LET} amask(U, x, w_{i−2}, w_i, w_{i+1}, y, s_{i−2}, s_{i−1}, s_i)` (x = `w_{i−3}`, y = `s_{i−3}`).
    This is window-local by construction (it never reads the actual `w_{i±3}`, `s_{i+2}`, `s_{i−3}`, even when d is small).
- c ≥ 7: `m = 31` (all letters; no filter on the big's own link). (R4)

**Credit key.** `q = (U, V, min(A+, A-), max(A+, A-))` (tuple order). JSON: `[U, V, [5-list], [5-list]]`.
Write q = (U, V, A, B) with `A = (cA, aA, bA, oA, mA)`, `B` likewise.

**Candidates of q.** For every `eA` with bit `LI[eA]` of mA set and every `eB` with bit `LI[eB]` of mB set:

```
in(eA, eB)  = tauo(V, U, sidex(cA, aA, bA, eA, oA), sidex(cB, aB, bB, eB, oB))
out(eA, eB) = tauo(U, V, sidex(cA, bA, aA, oA, eA), sidex(cB, bB, aB, oB, eB))
```

(The formula is symmetric in A ↔ B, so it does not matter which side of the window became A.)

**Receiver term.** At a big `w_i` the receiver row gets `+1 · XQ[q]` (repeats add), **unless** mA = 0 or mB = 0, or
`in = out` for every candidate; then the position contributes nothing (R6). No old x term is added under xo.

**mrowX rows.** For every q used by some receiver row and every candidate pair (eA, eB):

```
xo[in(eA,eB)] − xo[out(eA,eB)] − XQ[q] <= 0        label ["mrowX", [U, V, A, B], [eA, eB]]
```

(if `in = out` the row is `−XQ[q] <= 0`.) So `XQ[q] >= max over candidates of (xo[in] − xo[out])`: the receiver credits the
worst case over the letters it cannot see, exactly as M credits max over cand2. All candidate rows of q are added the first
time a receiver row uses q (as mrowR2). (R11)

**XQ bounds.** `−xcap <= XQ <= xcap`. This changes nothing: every candidate difference lies in [−xcap, xcap]. No cost. (R7)

**Granularity (R2b).** One credit per (receiver, big link position), joint over the in and out terms and over both sides'
unseen letters. Unseen letters are **not** coupled across positions: in a pattern big–6–big the 6's private is maximised
separately in the two x terms (and separately again in the 6's own M term, as before). Pricing this exact family against the
s50 certs (`s51/pricer51.py`, refinement `x_outMW` = this spec; `x_outM` = the same with s50's exact amask domain):

| cert | s50 x_out (row-level, privates shared) | x_outM (per position, exact amask) | **x_outMW (this spec)** |
|---|---|---|---|
| A78 q42aA78L | Σ max(0,−rc) 96/421 = 0.228, 4 neg, all binders | 0.228, same 4 keys | **0.228, same 4 keys, rc −24/421 each** |
| A83 q44nfA83L | 6016/29923 = 0.201, 15 neg | 2618/29923 = 0.087, 10 neg | **2618/29923 = 0.087, 10 neg, most negative −426/29923** |

The window-local domain costs nothing against the exact amask domain on either cert; the per-position max costs 0.114 of
the A83 first-order potential (the top two A83 binders' keys need the shared private). Logs: `s51/price51_A78.log`,
`s51/price51_A83nf.log`.

## 51.4 Rows and coefficients

| row | change under xo |
|---|---|
| senderR2 | none (x never appears in sender rows) |
| cons2 | none (x never appears in 6-centred conservation) |
| mrowR2, mrowL, mrowV, mrowQ, mrowZ | none |
| receiverR2 | at each big `w_i`: `+XQ[q_i]` (51.3) instead of `+x[τin] − x[τout]`; every other term unchanged (y, M with filt16 mask, h5 r/rr, l3q lq/lQ, fb, …) |
| mrowX (new) | `+1 xo[in] −1 xo[out] −1 XQ[q] <= 0`, w <= 0 |

Columns: `xo` ∈ [0, xcap] (cost xpen while the keeppen/xpen penalty is on, reset to 0 with the other capped families when the
penalty is removed — exactly where x was), `XQ` ∈ [−xcap, xcap], cost 0 (R9). No old `x` columns exist under xo (R8).

## 51.5 Primal check (upperR2) under xo

1. The solution JSON must have `"xoflag": true` and a field `"xo": {str(tauo): value}`; with xo on, a non-empty `"x"` is an error;
   with xo off, a non-empty `"xo"` is an error. Every xo value must be in [0, xcap + 1e−9].
2. **XQ is not stored.** The checker sets `XQ[q] = XQeff(q) = max over the candidates of (xo[in] − xo[out])` (missing keys = 0),
   the smallest value the mrowX rows allow. It lies in [−xcap, xcap], so the XQ bounds hold.
3. Senders and conservation: unchanged (§12.7).
4. Receivers: at every window with a big centre (c index 2..4), the window value gets `+XQeff(q(window))`, or 0 when the
   position has no term (51.3, R6). q depends only on the 9 window slots and U, so the window stays exact and the
   exhaustive separator d = 7..17 (jsep3/5/7, mode 0) is exact. The relaxed DP d = 18..30 and Karp use the same window
   table, so they remain upper bounds. No leaf change.
5. A window whose xo keys are all absent has XQeff = 0 (every candidate gives 0 − 0); only windows touched by a positive xo
   key (as an in or out key, either side as A) are evaluated explicitly.

## 51.6 Certificate check (lowerR2) under xo

| label | sign of w | bound b | accepted when |
|---|---|---|---|
| mrowX `[U, V, A, B], [eA, eB]` | w <= 0 | 0 | U, V ∈ {7,8,9}; A, B are 5-lists with letters in LET at positions 0..3 and a mask in 1..31 at position 4; A <= B (tuple order); bit LI[eA] of A[4] and bit LI[eB] of B[4] are set |
| receiverR2 | w <= 0 | d − 6 | admissible (unchanged); coefficients rebuilt by recv_coef_R2 with the xo terms of 51.3 |
| all others | unchanged | | |

Pricing (`D` as §12.8): `xo` columns with rc < 0 are priced at xcap (`D += rc·xcap`), as x. `XQ` columns are priced at their
box: `D −= xcap·|rc|` for any rc ≠ 0 (min over v ∈ [−xcap, xcap] of rc·v). A receiver XQ[q] whose q has no mrowX row in the
cert is just a column with rc > 0 → priced −xcap·rc. Every other family as before. The §44.8 repair treats mrowX as an mrow
(w may move only while it stays < 0).

## 51.7 Separation (solveR2) under xo

- The window term of 51.5(4) with XOV = the LP's xo values. XQ's own LP value is not used (XQeff is the minimal feasible value).
- **Class table (mode 2 distinctness).** Under xo a big centre's class is `1 + 625 + 390625 + (c−2)·390625 + idx8`, where idx8
  is the base-5 index of the other 8 window slots `(a, b, e, f, p, q, r, s)`, because q reads all of them. Classes of 5- and
  6-centres are unchanged. With hat5 the r-term fold uses stride 2,000,000 instead of 500,000 (153 hat5 ids, so max
  < 3.1·10^8 < 10^9, below jsep's l3q row ids). The class file name gets the suffix `o`.
- mrowX rows are added when a receiver row first uses q (all candidates).
- The solution JSON gains `"xo"` and `"xoflag"`; `"x"` is empty.

## 51.8 Reading choices

- **R1** Outer letters = s50's: `ea` next to a, `eb` next to b, in c's rotation (51.1).
- **R2** u reads eb of the in-key / ea of the out-key; the far end reads the other one (51.2).
- **R2b** M-style credit per receiver position, joint over in/out and both sides; not coupled across positions (51.3 table).
- **R3** 6-private domain = non-R6 on the 6's wheel ∩ OR of amask over the two letters outside u's window at i (window-local).
  It contains the exact domain, so it is sound; pricing shows no loss against the exact domain.
- **R4** A big c's unseen neighbour has domain all of 5..9.
- **R5** c = 5: the outer letter is seen (`e = o`), mask is that single letter.
- **R6** No receiver term when a mask is empty (the arrangement cannot occur: no allowed private), or when in = out for
  every candidate (the terms cancel, as zero x coefficients are dropped).
- **R7** XQ ∈ [−xcap, xcap]; lowerR2 prices it at the box.
- **R8** Under xo the old x family is off entirely (no mixing of x and xo).
- **R9** xpen (keeppen) applies to xo exactly as to x; XQ has no cost.
- **R10** JSON: sol `"xo": {str(tauo): v}`, `"xoflag": true`; cert mrowX label as 51.6.
- **R11** All candidate mrowX rows of q are added at first use, including in = out rows (`−XQ <= 0`).
- **R12** Nothing else changes: y, g2, h2, M/sig2 (with its filt16 mask), hat5, l3q/l3qV, fb, senders, cons2, patterns, RBIG,
  admissibility, DP to 30, Karp.
- **R13** Cap: **xcap = 3** for xo (the run uses `xcap=3`).

## 51.9 Worked example (A78 binder, hand)

Receiver `R 8 76765656/66565565`: d = 8, U = 8, w = (7,6,7,6,5,6,5,6), s = (6,6,5,6,5,5,6,5). Bigs at i = 0 and i = 2.

Position i = 0 (V = 7): window (a,b,c,e,f; p,q,r,s) = (w6,w7,w0,w1,w2; s6,s7,s0,s1) = (5,6,7,6,7; 6,5,6,6).
- + side: c⁺ = w1 = 6, `s_0` = 6, `w_2` = 7, seen outer `s_1` = 6 → A⁺ = (6,6,7,6,m⁺); m⁺ from the wheel (8, 7, 6, p, 6, 7) ∩ AU⁺.
- − side: c⁻ = w7 = 6, `s_7` = 5, `w_6` = 5, seen outer `s_6` = 6 → A⁻ = (6,5,5,6,m⁻); wheel (8, 7, 5, p, 6, 5).
- out key for (e⁺, e⁻) = (5, 5): `tauo(8, 7, (6,7,6,6,5), (6,5,5,6,5))` — s50's top A78 x_out key
  `(8, 7, (6,5,5,6,5), (6,7,6,6,5))`, rc −24/421, driven by this row's out-term. The in key is
  `tauo(7, 8, (6,6,7,e⁺,6), (6,5,5,e⁻,6))` ≠ out, so the position has the term `+XQ[(8, 7, min, max)]`.

---------------------------------------------------------------------------------------------------------------

Controls planned (§51.10 will be filled in after the build): (a) default flags reproduce `s42a/run_A78/upper.log` and the
s42a lowerR2 log byte for byte (timings stripped); (b) hand check of one refined key's reduced cost on the A78 cert against
s50's −24/421; (c) broken builds (`xobroken=end`: u reads the far outer letter; `xobroken=sign`: receiver gets −XQ) caught by
upperR2 / lowerR2; (d) smoke solve uses xo columns.
