# V2ROW_SPEC: the KEYSPEC v2 receiver realisation row `('receiverV2', d, link, apex, rho)` (Opus s86 v2r)

Purpose: everything needed to rebuild (replay) a `receiverV2` row of an Opus v2r cert or dual export from its id alone, without
reading the Opus engine. Model: W6b `KEYSPEC2_RECEIVER.md` (md5 d5a6734b) section 3.1 (the exact row), written as one linear row
per realisation. Stack of the first v2r lane: args K3g bef43766 (restricted-LP checks) / K3gB5b 5e399535 (lane k86GV1), rules 2db75746
(`rules_c67fa1d1_plus_A5_twins.json`), rpatN3 + offc_K3g 2f4f0f02, flags `c6le f2b7` (+ `xon apexcls filt16 hat5 consall l3q
lqcap=3 l3qV=7,8`), generic keys `gkeys=` with `gkwin gkleaf`.

## 0. Summary

* A d = 7 / 8 receiver (centre c of degree d) has the v2 max-row  max over rho of value(rho; x) <= d - 6 + t  (KEYSPEC2 3.1).
* A v2r LP holds it as a set of linear rows, one per realisation rho it has met: `value(rho; x) - t <= d - 6`.
  Each such row is a valid row of the v2 family (the max-row implies it), so a lower LP / cert may contain any subset of them.
* value(rho; x) = fixed(x) + sum over link positions j of base_j(x_j, y_j)(x) + sum over keys K of (IN(K; rho) - OUT(K)) ks_K.
  All coefficients are integers.
* A v2r cert contains NO masked d = 7 / 8 receiver row (`receiverR2` with d = 7 or 8). That row is stronger than the v2 row
  (KEYSPEC2 4.5), so it is not a row of the v2 family; a replay must reject it. d >= 9 receivers stay `receiverR2` (gkwin window).
  Senders, cons2 and mrow rows are unchanged.

## 1. Encoding

### 1.1 Cert JSON (`cert_*.json`, exact `*_exb.json`)

One entry per row, `{"w": <weight>, "row": ["receiverV2", d, link, apex, rho]}`, field order fixed:

| field | type | content |
|---|---|---|
| 0 | string | `"receiverV2"` |
| 1 | integer | d, 7 or 8 (the centre's degree; also its letter U) |
| 2 | string, d chars | link w_0 .. w_{d-1}: the centre's neighbours in rotation order |
| 3 | string, d chars | apex s_0 .. s_{d-1}: s_j = the third vertex of the face on the edge w_j w_{j+1} (indices mod d) |
| 4 | string, 2d chars | rho = x_0 y_0 x_1 y_1 ... x_{d-1} y_{d-1} (section 2) |

* Letters are degrees `5 6 7 8 9`, and `9` means "9 or more" (9+) everywhere: link, apex and rho.
* `w` is a float in a float cert and an exact rational string (`"p/q"`) in an exact cert. Sign: receiver rows have w <= 0
  (the dual of `row - t <= d - 6`), like `receiverR2`.
* The label is used exactly as written: do NOT canonicalise (rotate / reflect) it, since rho's positions are tied to the label's
  positions. The label must pass the same admissibility filter as a `receiverR2` label of the same d.
* Several entries may share (d, link, apex) with different rho; each is its own row.

### 1.2 Dual export (`dual_rows_*.json`, written by `dualexport`)

A `receiverV2` row becomes

    {"w": w, ["w_exact": "p/q",] "type": "receiverV2", "d": d, "link": link, "apex": apex, "rho": rho, "credit": "v2",
     "privates": {"j": the 2-letter string x_j y_j, for every j with w_j != 5}, "link_has_8plus": bool, "apex_has_8plus": bool,
     "ks": {key name: IN(K; rho) - OUT(K), nonzero only}}

`meta["v2r"]` names the convention. `colsum[K]` = sum over rows of w * ks[K], as before. Pricing a NEW key K' on a receiverV2 row
uses the same reading: IN(K'; rho) - OUT(K') at this row's rho (exact; the row is linear in the keys).

## 2. Vertices and the realisation rho

Around w_j the rotation is c, w_{j+1}, s_j, [w_j's privates], s_{j-1}, w_{j-1} (back to c). The privates are the neighbours of w_j
that are not c, w_{j-1}, w_{j+1}, s_{j-1}, s_j: none for a 5, one for a 6, two for a 7, deg - 5 for an 8 / 9+.

* x_j = the vertex right after s_j in that rotation (w_j's private next to s_j; W6b a_j);
* y_j = the vertex right before s_{j-1} (w_j's private next to s_{j-1}; W6b b_{j-1}).

So: a 5 has x_j = s_{j-1} and y_j = s_j (its rotation is c, w_{j+1}, s_j, s_{j-1}, w_{j-1}); a 6 has x_j = y_j = p (its private);
a 7 has (x_j, y_j) = (p1, p2), p1 next to s_j and p2 next to s_{j-1}; an 8 / 9+ has its two end privates.
rho fixes one letter pair (x_j, y_j) per link position, chosen independently per j from the domain dom_j of section 3.

## 3. Domains dom_j (the replay must check (x_j, y_j) in dom_j for every j)

These are exactly the letter sets the masked `receiverR2` row's envelope terms range over, so a replay that already rebuilds
`receiverR2` rows has all ingredients. U = d. Masks are 5-bit, bit k = letter 5 + k (bit 4 = 9+).

| w_j | dom_j |
|---|---|
| 5 | {(s_{j-1}, s_j)} only |
| 6 | {(p, p) : p in P6}. sgM = sig2_of(U, w_{j+1}, s_j, s_{j-1}, w_{j-1}, w_{j+2}, w_{j-2}) + (amask(U, w_{j-2}, w_{j-1}, w_{j+1}, w_{j+2}, s_{j-2}, s_{j-1}, s_j, s_{j+1}) & ~extra6(d, w, s, j),), i.e. the signature of the row's own `('M', sgM)` column for this 6. P6 = {p in pallow(sgM) : not isR6((U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1}))}; pallow(sgM) = the letters whose bit is set in sgM's last entry; isR6(word) = canon(word) in R6 or the 6-cycle word has three cyclically consecutive 5s. Then {h2_of(.., p, ..) : p in P6} = sig2_keys(sgM). |
| 7 | {(p1, p2) : bit p1 in m1, bit p2 in m2, canon((U, w_{j+1}, s_j, p1, p2, s_{j-1}, w_{j-1})) not in RBIG}. Side +1 (p1): if w_{j+1} <= 6 and s_j <= 6, m1 = T[(+1, w_{j+1}, w_{j+2}, w_{j+3}, w_{j+4}, s_j, s_{j-1})] & ~extra7(d, w, s, j, +1), else m1 = 31 & ~extra7(d, w, s, j, +1). Side -1 (p2): if w_{j-1} <= 6 and s_{j-1} <= 6, m2 = T[(-1, w_{j-1}, w_{j-2}, w_{j-3}, w_{j-4}, s_{j-1}, s_j)] & ~extra7(d, w, s, j, -1), else 31 & ~extra7(d, w, s, j, -1). T = L3T (the l3q table) at d = 7, the l3qV = 8 table at d = 8. (m1, m2) are the masks of the row's own `('Q', q7sig(U, w_{j+1}, s_j, s_{j-1}, w_{j-1}, m1, m2))` column, and m1 / m2 are the masks of its `('lQ', ..)` columns. Then {qkey(..p1, p2..)} = q7keys(that sig). |
| 8, 9+ | all 25 pairs (no BALL2 position reads a middle private; the end privates are free) |

Stack facts relied on (the same ones the masked row already uses, nothing new): the kill tables KT behind amask (filt16), the f2b
rules file (extra6 / extra7; 2db75746), the l3q tables (L3T, l3qV = 8), the wheel verdicts R6 (studio17 `wheels17_verdicts.txt`,
D and C verdicts, EXCL6 excluded), the big-wheel list RBIG (`bigwheels_dfast.out`, D=true), canon = min over rotations and reflections.

* Empty product (some dom_j empty): the receiver cannot occur (all its private letters reducible), it has no v2 row, and an id
  with such a label is invalid.
* Check we run on every row: the multiset of `('M', sgM)` (one per 6 with a nonempty sig2_keys), `('Q', sig)` (one per 7 with a
  nonempty q7keys) and `('lQ', key)` (one per 7-side with c, apex <= 6) entries the domains imply equals the masked row's own M / Q /
  lQ entries, coefficients included.

## 4. The row

    row(rho) = fixed + sum_j base_j(x_j, y_j) + sum_K (IN(K; rho) - OUT(K)) * ('ks', K)        and the constraint   row(rho) - t <= d - 6

(t has coefficient -1; d = 7: <= 1 + t, d = 8: <= 2 + t.) Columns are named as in the masked rows: `('h', key)`, `('q', key)`,
`('lq', key)`, `('ks', name)`, and whatever the fixed part carries.

### 4.1 fixed

The masked `receiverR2` row for (d, link, apex), as built below the generic-key wrapper (so: no `('ks', .)` entries), minus every
`('M', .)`, `('Q', .)` and `('lQ', .)` entry. Every other entry is kept with its coefficient.

### 4.2 base_j (group j's copy for the chosen (x_j, y_j))

* w_j = 5: nothing.
* w_j = 6, private p: `+1 ('h', h2_of((U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1}), w_{j+2}, w_{j-2}))`, where
  h2_of(m, ar, al) = min(m + (ap(ar), ap(al)), (m0, m5, m4, m3, m2, m1) + (ap(al), ap(ar))) and ap(z) = 7 if z >= 7 else 5 (apexcls).
* w_j = 7, (p1, p2):
  * `+1 ('q', qkey((U, w_{j+1}, s_j, p1, p2, s_{j-1}, w_{j-1})))`, qkey(m) = min(m, (m0, m6, m5, m4, m3, m2, m1));
  * `+1 ('lq', V + (w_{j+1}, s_j, p1))` if w_{j+1} <= 6 and s_j <= 6 (side +1 reads p1 = x_j);
  * `+1 ('lq', V + (w_{j-1}, s_{j-1}, p2))` if w_{j-1} <= 6 and s_{j-1} <= 6 (side -1 reads p2 = y_j);
  * V = () at d = 7 and (8,) at d = 8. Equal columns add (coefficient 2).
* w_j = 8 or 9+: nothing.

The masked row had, per 6 / 7, the envelope `('M', sgM)` resp. `('Q', sig) + ('lQ', ..) + ('lQ', ..)` in their place.

### 4.3 keys

**Scope (amended 8 Nov 07:55Z after W6r's replay note).** Payer sets are subsets of {5, 6, 7}: the engine refuses any key whose payer
set meets {8, 9} (`assert not (um & 24)` in edge56 gk_write / gkwin), so KEYSPEC2 section 1's PAYER8SPEC case never arises and a centre of
degree 8 has OUT(K) = 0 for every key (consistent with "OUT = the masked row's sure count, 0 at d = 8"). Payee sets may contain 8 and 9.
Keys use only the 10 positions tabulated below. Both statements hold for the gate file cg_keys_r13w16_16fi.txt (56d144d5, 220 keys) and
for the GV1 file cg_keys_r13w16_16fik.txt (3d996dbb, 240 keys): payer sets {5}, {6}, {7} only; positions S.L+1 204, S.L-1 215, S.L+2 198,
S.L-2 181, S.L+3 166, S.L-3 171, S.A+1 121, S.A-1 183, R.L+2 133, R.L-2 121 occurrences in the 240-key file, no other position. A replay
should reject (not extend) any key outside this scope.


For every key K of the run's gkeys file (all keys, `NAME EDGE(Up->Vp)[POS=SET ...]`; letter sets as in KEYSPEC, positions not
listed are wildcards), coefficient IN(K; rho) - OUT(K) on column `('ks', NAME)`, omitted when 0. Every letter of the picture is
exact (link, apex, rho), so a slot either matches or not ("possible" = "sure"): a slot matches when the payer letter is in Up, the
payee letter is in Vp and every listed position's letter is in its SET. Letters >= 9 read as 9.

There are 2d OUT slots and 2d IN slots, (i, sg) for i = 0..d-1 and sg = +1, -1; indices mod d.

OUT(K) = number of matching OUT slots: payer c (letter d), payee w_i; positions:

| position | sg = +1 | sg = -1 |
|---|---|---|
| S.L+1 | w_{i+1} | w_{i-1} |
| S.L+2 | w_{i+2} | w_{i-2} |
| S.L+3 | w_{i+3} | w_{i-3} |
| S.L-1 | w_{i-1} | w_{i+1} |
| S.L-2 | w_{i-2} | w_{i+2} |
| S.L-3 | w_{i-3} | w_{i+3} |
| S.A+1 | s_{i+1} | s_{i-2} |
| S.A-1 | s_{i-2} | s_{i+1} |
| R.L+2 | s_i | s_{i-1} |
| R.L-2 | s_{i-1} | s_i |

IN(K; rho) = number of matching IN slots: payer w_i, payee c (letter d); positions (KEYSPEC2_RECEIVER section 2):

| position | sg = +1 | sg = -1 |
|---|---|---|
| S.L+1 | w_{i-1} | w_{i+1} |
| S.L+2 | s_{i-1} | s_i |
| S.L+3 | y_i | x_i |
| S.L-1 | w_{i+1} | w_{i-1} |
| S.L-2 | s_i | s_{i-1} |
| S.L-3 | x_i | y_i |
| S.A+1 | x_{i-1} | y_{i+1} |
| S.A-1 | y_{i+1} | x_{i-1} |
| R.L+2 | w_{i-2} | w_{i+2} |
| R.L-2 | w_{i+2} | w_{i-2} |

(W6b names: y_i = b_{i-1}, x_i = a_i, x_{i-1} = a_{i-1}, y_{i+1} = b_i. For a 5 at a private position the letter is its other apex,
as section 2 says: x_j = s_{j-1}, y_j = s_j.) OUT reads link and apex letters only, so it does not depend on rho (it is the masked
row's exact "sure" OUT count).

## 5. Why a subset of realisation rows is a valid lower-LP row set

* For any real configuration, its true private letters rho0 lie in the domain product (section 3: the domains are the stack's
  reducibility facts; two variables that are one vertex get one letter, still in the product). Its true row is value(rho0; x).
* The v2 family row is max over the product; each realisation row is implied by it. A lower LP (lext) built from any subset of
  realisation rows plus the other families' rows has t1 <= the v2 family optimum, so a cert of t1 > 0 over such rows is valid.
* The masked d = 7 / 8 row is >= every realisation row pointwise (envelopes M >= h, Q >= q, lQ >= lq via the mrow rows; current
  key coefficients >= IN(K; rho) - OUT(K)), i.e. stronger, so it is not in the family (section 0).

## 6. How the Opus engine finds the rows (for information; the replay needs none of it)

At an LP point (x, t) the max over rho is an exact max-plus product round the d-cycle of sites Q_j = (x_j, y_{j+1}) (25 states
each): factor i = base_i(x_i, y_i) (-inf off dom_i) + sum_K x_K [IN slot (i, +1) and (i, -1) of K match], which reads
(x_{i-1}, y_i, x_i, y_{i+1}) = (Q_{i-1}, Q_i). The argmax rho's row is added when it exceeds d - 6 + t by more than 1e-9. Candidates:
every d = 7 / 8 receiver the masked separators list (their envelope / current-key values are >= the v2 value, so they list a
superset of the v2-violated receivers, up to their top-K cap), plus a DP re-scan of every receiver already met. Ties: the first
maximiser in state order (deterministic).

## 7. Checks behind this spec (s86, v2r/NOTES.md)

* Unit (`v2rtest`, all 692 d = 7 / 8 receiver rows of the GL5 p1_00 cert def2afcc, 220 keys): W6b `test_vectors.json` 24 / 24; per (row, key)
  max / min IN and OUT = the single-row p1_r values on all 152,240 pairs; at random points the DP max = the rebuilt row's value at the
  argmax, no random realisation above it (138,400 samples), and = the exhaustive max on 108 small rows (93,642 realisations).
* Restricted LP on that cert's own rows (min t, columns within their caps), d = 7 / 8 receivers as realisation rows added until none
  is violated: v2 t = -0.076947399076 after 17 LP solves (4,790 realisation rows over 692 receivers), = W6b's v2all -0.0769473991;
  keys held at p1_r 0.001233311856 (= p1_r), at the current coefficients 0.001252703507 (= W6b v2base_all); the masked models give
  W6b's mask / p1r values.
* lowerR2 exactbasis on that LP's dual (997 receiverV2 rows): exact cert of 1,816 rows (980 receiverV2), every row rebuilt from its id
  alone: VALID t >= -0.076947399 (exact rational). The same exact cert rebuilt with planted bugs: every 6's h key with its two outer
  links swapped -> INVALID (239 h columns with negative reduced cost); every 7's two privates swapped -> the bound collapses to
  -1.0913 (the wrong q / lq / ks entries no longer cancel; lq and ks are capped, so they are priced, not refused). Without the v2r
  flag, or with masked d = 7 / 8 rows under v2r: INVALID.
* `spec_check.py` (this folder, pure python, no stack tables) re-derives the key OUT / IN counts from the two tables of 4.3, the copy
  terms from 4.2 and the full row from 4.1-4.3 for the five vectors below: all equal to the engine's output.

## 8. Test vectors

The five rows below are receiverV2 rows of that restricted-LP dual (`v2r/rlp/cert_rlp_v2.json`), built with the keys
`p1r/cg_keys_r13w16_16fi.txt` (md5 56d144d5, 220 keys) on args K3g (bef43766), rules 2db75746, rpatN3 + offc_K3g, c6le, f2b7. The full
decomposition (domains, removed envelope entries, fixed, copies, every key's OUT / IN with its spec, the row) is in
`V2ROW_vectors.json` (md5 b4b3eed4). Columns are written `[type, key]` (key = the integer tuple as a list, or the key name for `ks`);
"+c [col]" = coefficient c. The `r` / `rr` / `y` / `z` / `zr` / `lq` / `q` entries of "fixed" are the masked row's own non-envelope
terms (e.g. the centre's own outgoing 7-rules), unchanged. Letters in dom_j are written x_j y_j.

### 8.1  ["receiverV2", 7, "7665566", "6765776", "67776665576677"]

* bound: row - t <= 1
* masked row entries removed: +1 ["M",[7,5,6,7,6,5,7,30]], +1 ["M",[7,5,7,7,6,5,7,30]], +2 ["M",[7,6,7,6,7,5,5,30]], +1 ["Q",[7,6,6,6,6,30,30]], +2 ["lQ",[6,6,30]]
* fixed: -2 ["lq",[6,6,5]], -1 ["q",[7,6,6,5,5,6,6]], +1 ["r",[5,0,6,5,0,7]], -1 ["rr",[5,0,6,5,0,7]], +1 ["y",[7,5,5,6,6]], +1 ["y",[7,5,5,7,6]], +1 ["z",[7,5,5,6,6,0,0]], +1 ["z",[7,5,5,7,6,0,0]], -1 ["zr",[7,5,5,6,6,0,0]], -1 ["zr",[7,5,5,7,6,0,0]]
* j = 0, w_j = 7, (x_j, y_j) = 67, dom_j = {66 67 68 69 76 77 78 79 86 87 88 89 96 97 98 99}: +1 ["lq",[6,6,6]], +1 ["lq",[6,6,7]], +1 ["q",[7,6,6,6,7,6,6]]
* j = 1, w_j = 6, (x_j, y_j) = 77, dom_j = {66 77 88 99}: +1 ["h",[7,6,7,7,6,7,5,5]]
* j = 2, w_j = 6, (x_j, y_j) = 66, dom_j = {66 77 88 99}: +1 ["h",[7,5,6,6,7,6,5,7]]
* j = 5, w_j = 6, (x_j, y_j) = 66, dom_j = {66 77 88 99}: +1 ["h",[7,5,7,6,7,6,5,7]]
* j = 6, w_j = 6, (x_j, y_j) = 77, dom_j = {66 77 88 99}: +1 ["h",[7,6,7,7,6,7,5,5]]
* keys with OUT or IN > 0 (OUT / IN): gk00_5 8 / 0, gk03_35 2 / 0, gk04_44 1 / 0, gk00_58 0 / 1, gk01_69 1 / 0, gk02_80 1 / 0, gk02_85 0 / 1, gk02_86 0 / 1, cg00_9 8 / 0, cg12_76_0 8 / 0, w6b16_03 2 / 0, w6b16_04 0 / 1, w6b16_05 0 / 1, w6b16_06 0 / 1, w6b16f_c05 0 / 1, w6b16f_v09 0 / 1, w6b16i_01 0 / 1, w6b16i_15 3 / 0
* full row (34 entries; t has coefficient -1 and the bound is d - 6):

      [[["h",[7,5,6,6,7,6,5,7]],1],[["h",[7,5,7,6,7,6,5,7]],1],[["h",[7,6,7,7,6,7,5,5]],2],[["ks","cg00_9"],-8],[["ks","cg12_76_0"],-8],[["ks","gk00_5"],-8],[["ks","gk00_58"],1],[["ks","gk01_69"],-1],[["ks","gk02_80"],-1],[["ks","gk02_85"],1],[["ks","gk02_86"],1],[["ks","gk03_35"],-2],[["ks","gk04_44"],-1],[["ks","w6b16_03"],-2],[["ks","w6b16_04"],1],[["ks","w6b16_05"],1],[["ks","w6b16_06"],1],[["ks","w6b16f_c05"],1],[["ks","w6b16f_v09"],1],[["ks","w6b16i_01"],1],[["ks","w6b16i_15"],-3],[["lq",[6,6,5]],-2],[["lq",[6,6,6]],1],[["lq",[6,6,7]],1],[["q",[7,6,6,5,5,6,6]],-1],[["q",[7,6,6,6,7,6,6]],1],[["r",[5,0,6,5,0,7]],1],[["rr",[5,0,6,5,0,7]],-1],[["y",[7,5,5,6,6]],1],[["y",[7,5,5,7,6]],1],[["z",[7,5,5,6,6,0,0]],1],[["z",[7,5,5,7,6,0,0]],1],[["zr",[7,5,5,6,6,0,0]],-1],[["zr",[7,5,5,7,6,0,0]],-1]]

### 8.2  ["receiverV2", 7, "7666666", "6567656", "55775555555577"]

* bound: row - t <= 1
* masked row entries removed: +2 ["M",[7,6,5,6,6,7,5,31]], +2 ["M",[7,6,5,6,7,5,5,30]], +2 ["M",[7,6,6,7,6,5,5,31]], +1 ["Q",[7,6,6,6,6]], +2 ["lQ",[6,6,31]]
* fixed: -2 ["lq",[6,6,6]], -1 ["q",[7,6,6,6,6,6,6]], +2 ["r",[6,0,0,6,1,0]], -2 ["rr",[6,0,0,6,1,0]]
* j = 0, w_j = 7, (x_j, y_j) = 55, dom_j = {55 56 57 58 59 65 66 67 68 69 75 76 77 78 79 85 86 87 88 89 95 96 97 98 99}: +2 ["lq",[6,6,5]], +1 ["q",[7,6,6,5,5,6,6]]
* j = 1, w_j = 6, (x_j, y_j) = 77, dom_j = {66 77 88 99}: +1 ["h",[7,6,5,7,6,7,5,5]]
* j = 2, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,5,5,6,6,7,5]]
* j = 3, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,6,5,7,6,5,5]]
* j = 4, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,6,5,7,6,5,5]]
* j = 5, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,5,5,6,6,7,5]]
* j = 6, w_j = 6, (x_j, y_j) = 77, dom_j = {66 77 88 99}: +1 ["h",[7,6,5,7,6,7,5,5]]
* keys with OUT or IN > 0 (OUT / IN): gk00_5 8 / 0, gk00_10 2 / 0, gk00_12 0 / 2, cg00_9 8 / 0, cg12_76_0 4 / 0, w6b16i_01 0 / 8
* full row (15 entries; t has coefficient -1 and the bound is d - 6):

      [[["h",[7,6,5,5,6,6,7,5]],2],[["h",[7,6,5,7,6,7,5,5]],2],[["h",[7,6,6,5,7,6,5,5]],2],[["ks","cg00_9"],-8],[["ks","cg12_76_0"],-4],[["ks","gk00_10"],-2],[["ks","gk00_12"],2],[["ks","gk00_5"],-8],[["ks","w6b16i_01"],8],[["lq",[6,6,5]],2],[["lq",[6,6,6]],-2],[["q",[7,6,6,5,5,6,6]],1],[["q",[7,6,6,6,6,6,6]],-1],[["r",[6,0,0,6,1,0]],2],[["rr",[6,0,0,6,1,0]],-2]]

### 8.3  ["receiverV2", 8, "55558578", "58585558", "8558855855555755"]

* bound: row - t <= 2
* masked row entries removed: +1 ["Q",[8,5,5,5,8,30,31]], +1 ["lQ",[8,5,5,30]]
* fixed: +2 ["r",[5,0,8,5,1,8]], +1 ["r",[5,1,5,7]], +1 ["r",[5,1,5,8]], +1 ["r",[7,8]], -2 ["rr",[5,0,8,5,1,8]], -1 ["rr",[5,1,5,7]], -1 ["rr",[5,1,5,8]], -1 ["rr",[7,8]], +1 ["x",16075], -1 ["x",48825], +1 ["x",62765], -1 ["x",62885], -1 ["x",62925], +1 ["x",64425], +2 ["y",[8,5,5,8,5]], +2 ["y",[8,5,5,8,8]], +1 ["y",[8,7,5,5,8]], +2 ["z",[8,5,5,8,5,1,0]], +1 ["z",[8,5,5,8,8,0,0]], +1 ["z",[8,5,5,8,8,0,1]], +1 ["z",[8,7,5,5,8,1,0]], -2 ["zr",[8,5,5,8,5,1,0]], -1 ["zr",[8,5,5,8,8,0,0]], -1 ["zr",[8,5,5,8,8,0,1]], -1 ["zr",[8,7,5,5,8,1,0]]
* j = 4, w_j = 8, (x_j, y_j) = 55, dom_j = all 25 pairs: no terms
* j = 6, w_j = 7, (x_j, y_j) = 57, dom_j = {56 57 58 59 66 67 68 69 76 77 78 79 86 87 88 89 96 97 98 99}: +1 ["lq",[8,5,5,7]], +1 ["q",[8,5,5,7,5,5,8]]
* j = 7, w_j = 8, (x_j, y_j) = 55, dom_j = all 25 pairs: no terms
* keys with OUT or IN > 0 (OUT / IN): A1 0 / 1, cg12_58_0 0 / 2, w6b16f_c14 0 / 1
* full row (30 entries; t has coefficient -1 and the bound is d - 6):

      [[["ks","A1"],1],[["ks","cg12_58_0"],2],[["ks","w6b16f_c14"],1],[["lq",[8,5,5,7]],1],[["q",[8,5,5,7,5,5,8]],1],[["r",[5,0,8,5,1,8]],2],[["r",[5,1,5,7]],1],[["r",[5,1,5,8]],1],[["r",[7,8]],1],[["rr",[5,0,8,5,1,8]],-2],[["rr",[5,1,5,7]],-1],[["rr",[5,1,5,8]],-1],[["rr",[7,8]],-1],[["x",16075],1],[["x",48825],-1],[["x",62765],1],[["x",62885],-1],[["x",62925],-1],[["x",64425],1],[["y",[8,5,5,8,5]],2],[["y",[8,5,5,8,8]],2],[["y",[8,7,5,5,8]],1],[["z",[8,5,5,8,5,1,0]],2],[["z",[8,5,5,8,8,0,0]],1],[["z",[8,5,5,8,8,0,1]],1],[["z",[8,7,5,5,8,1,0]],1],[["zr",[8,5,5,8,5,1,0]],-2],[["zr",[8,5,5,8,8,0,0]],-1],[["zr",[8,5,5,8,8,0,1]],-1],[["zr",[8,7,5,5,8,1,0]],-1]]

### 8.4  ["receiverV2", 7, "7665566", "7795676", "76775595566677"]

* bound: row - t <= 1
* masked row entries removed: +1 ["M",[7,5,6,7,6,5,7,30]], +1 ["M",[7,5,9,7,6,5,7,31]], +1 ["M",[7,6,7,6,7,5,5,30]], +1 ["M",[7,6,7,7,7,5,5,31]], +1 ["Q",[7,6,6,7,6,30,31]], +1 ["lQ",[6,6,30]]
* fixed: -2 ["lq",[6,6,5]], -1 ["q",[7,6,6,5,5,6,6]], +1 ["r",[5,0,6,5,0,9]], -1 ["rr",[5,0,6,5,0,9]], -1 ["x",3907], +1 ["x",3911], +1 ["y",[7,5,5,6,6]], +1 ["y",[7,5,5,9,6]], +1 ["z",[7,5,5,6,6,0,0]], +1 ["z",[7,5,5,9,6,0,0]], -1 ["zr",[7,5,5,6,6,0,0]], -1 ["zr",[7,5,5,9,6,0,0]]
* j = 0, w_j = 7, (x_j, y_j) = 76, dom_j = {56 57 58 59 66 67 68 69 76 77 78 79 86 87 88 89 96 97 98 99}: +1 ["lq",[6,6,6]], +1 ["q",[7,6,6,6,7,7,6]]
* j = 1, w_j = 6, (x_j, y_j) = 77, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,7,7,7,7,5,5]]
* j = 2, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,5,9,5,7,6,5,7]]
* j = 5, w_j = 6, (x_j, y_j) = 66, dom_j = {66 77 88 99}: +1 ["h",[7,5,6,6,7,6,5,7]]
* j = 6, w_j = 6, (x_j, y_j) = 77, dom_j = {66 77 88 99}: +1 ["h",[7,6,7,7,6,7,5,5]]
* keys with OUT or IN > 0 (OUT / IN): gk00_5 6 / 0, gk04_44 1 / 0, gk01_69 1 / 0, gk02_75 1 / 0, gk02_79 1 / 0, gk02_80 1 / 0, cg00_9 6 / 0, cg12_76_0 8 / 0, w6b16_03 1 / 0, w6b16_04 0 / 1, w6b16_05 0 / 1, w6b16_06 0 / 1, w6b16f_c07 1 / 0, w6b16f_v01 1 / 0, w6b16f_v03 1 / 0, w6b16f_v08 1 / 0, w6b16i_01 0 / 1, w6b16i_15 2 / 0, w6b16i_16 1 / 0, w6b16i_18 1 / 0
* full row (38 entries; t has coefficient -1 and the bound is d - 6):

      [[["h",[7,5,6,6,7,6,5,7]],1],[["h",[7,5,9,5,7,6,5,7]],1],[["h",[7,6,7,7,6,7,5,5]],1],[["h",[7,6,7,7,7,7,5,5]],1],[["ks","cg00_9"],-6],[["ks","cg12_76_0"],-8],[["ks","gk00_5"],-6],[["ks","gk01_69"],-1],[["ks","gk02_75"],-1],[["ks","gk02_79"],-1],[["ks","gk02_80"],-1],[["ks","gk04_44"],-1],[["ks","w6b16_03"],-1],[["ks","w6b16_04"],1],[["ks","w6b16_05"],1],[["ks","w6b16_06"],1],[["ks","w6b16f_c07"],-1],[["ks","w6b16f_v01"],-1],[["ks","w6b16f_v03"],-1],[["ks","w6b16f_v08"],-1],[["ks","w6b16i_01"],1],[["ks","w6b16i_15"],-2],[["ks","w6b16i_16"],-1],[["ks","w6b16i_18"],-1],[["lq",[6,6,5]],-2],[["lq",[6,6,6]],1],[["q",[7,6,6,5,5,6,6]],-1],[["q",[7,6,6,6,7,7,6]],1],[["r",[5,0,6,5,0,9]],1],[["rr",[5,0,6,5,0,9]],-1],[["x",3907],-1],[["x",3911],1],[["y",[7,5,5,6,6]],1],[["y",[7,5,5,9,6]],1],[["z",[7,5,5,6,6,0,0]],1],[["z",[7,5,5,9,6,0,0]],1],[["zr",[7,5,5,6,6,0,0]],-1],[["zr",[7,5,5,9,6,0,0]],-1]]

### 8.5  ["receiverV2", 7, "7675666", "6755676", "56777655665555"]

* bound: row - t <= 1
* masked row entries removed: +1 ["M",[7,5,5,6,6,7,5,30]], +1 ["M",[7,6,6,7,6,5,7,31]], +1 ["M",[7,6,7,6,7,5,5,31]], +1 ["M",[7,7,6,7,7,5,5,31]], +1 ["Q",[7,5,5,7,6]], +1 ["Q",[7,6,6,6,6,30,31]], +1 ["lQ",[5,5,31]], +1 ["lQ",[6,6,30]], +1 ["lQ",[6,6,31]]
* fixed: -1 ["lq",[5,6,6]], -1 ["lq",[6,6,6]], -1 ["q",[7,5,6,6,6,7,6]], -1 ["q",[7,6,6,6,5,7,6]], +1 ["r",[5,0,5,7]], +1 ["r",[5,1,5,6,0,0]], -1 ["rr",[5,0,5,7]], -1 ["rr",[5,1,5,6,0,0]], +1 ["x",162], +1 ["x",3907], -1 ["x",3911], -1 ["x",662], +1 ["y",[7,6,5,5,7]], +1 ["z",[7,6,5,5,7,0,0]], -1 ["zr",[7,6,5,5,7,0,0]]
* j = 0, w_j = 7, (x_j, y_j) = 56, dom_j = {56 57 58 59 66 67 68 69 76 77 78 79 86 87 88 89 96 97 98 99}: +1 ["lq",[6,6,5]], +1 ["lq",[6,6,6]], +1 ["q",[7,6,6,5,6,6,6]]
* j = 1, w_j = 6, (x_j, y_j) = 77, dom_j = {55 66 77 88 99}: +1 ["h",[7,7,6,7,7,7,5,5]]
* j = 2, w_j = 7, (x_j, y_j) = 76, dom_j = {56 57 58 59 65 66 67 68 69 75 76 77 78 79 85 86 87 88 89 95 96 97 98 99}: +1 ["lq",[5,5,7]], +1 ["q",[7,5,5,7,6,7,6]]
* j = 4, w_j = 6, (x_j, y_j) = 66, dom_j = {66 77 88 99}: +1 ["h",[7,5,5,6,6,6,7,5]]
* j = 5, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,6,5,7,6,5,7]]
* j = 6, w_j = 6, (x_j, y_j) = 55, dom_j = {55 66 77 88 99}: +1 ["h",[7,6,7,5,6,7,5,5]]
* keys with OUT or IN > 0 (OUT / IN): gk00_5 7 / 0, gk00_12 0 / 1, gk02_28 0 / 1, gk03_36 0 / 1, gk04_44 1 / 0, gk00_61 1 / 0, gk01_68 0 / 1, gk02_75 0 / 1, gk02_79 0 / 1, cg00_8 1 / 0, cg00_9 7 / 0, cg12_76_0 6 / 0, w6b16_16 1 / 1, w6b16_17 1 / 1, w6b16i_01 0 / 2, w6b16i_12 1 / 1, w6b16i_17 1 / 0
* full row (36 entries; t has coefficient -1 and the bound is d - 6):

      [[["h",[7,5,5,6,6,6,7,5]],1],[["h",[7,6,6,5,7,6,5,7]],1],[["h",[7,6,7,5,6,7,5,5]],1],[["h",[7,7,6,7,7,7,5,5]],1],[["ks","cg00_8"],-1],[["ks","cg00_9"],-7],[["ks","cg12_76_0"],-6],[["ks","gk00_12"],1],[["ks","gk00_5"],-7],[["ks","gk00_61"],-1],[["ks","gk01_68"],1],[["ks","gk02_28"],1],[["ks","gk02_75"],1],[["ks","gk02_79"],1],[["ks","gk03_36"],1],[["ks","gk04_44"],-1],[["ks","w6b16i_01"],2],[["ks","w6b16i_17"],-1],[["lq",[5,5,7]],1],[["lq",[5,6,6]],-1],[["lq",[6,6,5]],1],[["q",[7,5,5,7,6,7,6]],1],[["q",[7,5,6,6,6,7,6]],-1],[["q",[7,6,6,5,6,6,6]],1],[["q",[7,6,6,6,5,7,6]],-1],[["r",[5,0,5,7]],1],[["r",[5,1,5,6,0,0]],1],[["rr",[5,0,5,7]],-1],[["rr",[5,1,5,6,0,0]],-1],[["x",162],1],[["x",3907],1],[["x",3911],-1],[["x",662],-1],[["y",[7,6,5,5,7]],1],[["z",[7,6,5,5,7,0,0]],1],[["zr",[7,6,5,5,7,0,0]],-1]]

