# PAYER8SPEC: generic EDGE keys whose payer is an 8 or a 9+ (W6b, round 14b, 6 Nov 2026)

This extends W6's key grammar (round7/KEYSPEC.md) and Opus's gkwin window credit (from_opus/s85_k85B/DUAL_EXPORT.md) to
keys `EDGE(u->v)[...]` with payer letter u = 8 or u = 9 (9 means 9 or more). It is meant to be enough for a second engine
to implement the key columns without reading W6b's code (`round14b/code/p8lib.py`). Nothing here changes a key whose payer is
5, 6 or 7: their coefficients in every row are exactly as before (checked, section 7).

## 1. The keys

- Payer letter u in {8, 9}; payee letter v in {5, 6, 7, 8, 9}; a letter set X_p (nonempty subset of {5,...,9}) at each of
  the ten positions S.L+1, S.L+2, S.L+3, S.L-1, S.L-2, S.L-3, S.A+1, S.A-1, R.L+2, R.L-2 (KEYSPEC section 3); unlisted =
  wildcard. The positions are defined on the oriented edge payer -> payee exactly as in KEYSPEC section 3, for a payer of any
  degree. For a payer of degree >= 8, S.L+3 and S.L-3 are two different vertices of the payer's own link.
- A key with a payer SET (e.g. {8,9}) is the sum of its single-letter keys (every slot has exact endpoint letters).
- Direction (KEYSPEC section 2): the key relieves the payer's row and loads the payee's row. In charge = 6 - degree terms,
  the 8 (or 9+) gives charge to its neighbour v. One LP column per key, 0 <= x <= 3.
- Multiplicity: every oriented pair (payer, payee) with both chiralities sg = +1, -1; each match counts once.

## 2. Row conventions (unchanged)

| row | constraint | key coefficient |
|---|---|---|
| sender (5) | ... + key terms >= 1 - t | OUT - IN |
| cons2 (6), c6le | ... + key terms <= t | IN - OUT |
| receiver d = 7, gkleaf | ... + key terms <= 1 + t | IN - OUT, exact KEYSPEC picture |
| receiver d >= 8, gkwin | ... + key terms <= d - 6 + t | IN - OUT, window credit |
| mrows | | no key terms |

OUT = slots where the row's centre is the payer, counted only on a SURE match (the picture's letter set at every listed
position lies inside X_p, endpoints inside u and v). IN = slots where the centre is the payee, counted on a POSSIBLE match
(every set meets X_p). Letters in labels are capped at 9 (9 = 9+), as are the key's letters, so letter 9 is exact on both
sides.

## 3. Where a payer-8/9 key has terms

A payer 8 or 9 can only be (a) the centre of a receiver row of degree d >= 8 (OUT slots), or (b) a link vertex of some row
whose centre is the payee (IN slots). Concretely:

### 3.1 The payer's own row: receiver of degree d >= 8 (window row) -- OUT, sure match (NEW)

Centre letter U = min(d, 9). A key with payer 8 has OUT slots only in d = 8 rows; a key with payer 9 has OUT slots in every
receiver row of degree d >= 9 (d = 9, 10, 11, ...). The centre pays its link vertex w_i (payee letter w_i).

Link w_0..w_{d-1}, apexes s_0..s_{d-1} (s_i between w_i and w_{i+1}), all exact letters, indices mod d. For the OUT slot
centre -> w_i with chirality sg = +1 (S.L+1 = w_{i+1}):

| position | vertex | in the window W_i? |
|---|---|---|
| S.L+1, S.L+2 | w_{i+1}, w_{i+2} | yes, exact |
| S.L-1, S.L-2 | w_{i-1}, w_{i-2} | yes, exact |
| S.A+1 | s_{i+1} (apex beyond the edge w_{i+1} w_{i+2}) | yes, exact |
| S.A-1 | s_{i-2} (apex beyond the edge w_{i-2} w_{i-1}) | yes, exact |
| R.L+2 | s_i (the payee's next neighbour after S.L+1) | yes, exact |
| R.L-2 | s_{i-1} | yes, exact |
| S.L+3, S.L-3 | w_{i+3}, w_{i-3} | NO: read as the wildcard |

sg = -1 is the mirror: every offset negated, i.e. S.L+k = w_{i-k}, S.L-k = w_{i+k}, S.A+1 = s_{i-2}, S.A-1 = s_{i+1},
R.L+2 = s_{i-1}, R.L-2 = s_i.

**The window.** W_i = (w_{i-2..i+2}, s_{i-2..i+1}): the same 5-link + 4-apex shape as gkwin's IN window, but centred at the
payee w_i. Every key position except S.L+-3 lies inside it, so a separator that already carries the gkwin window carries
the OUT term with no larger state. S.L+-3 lie outside and are read as the wildcard; since OUT needs a SURE match, an OUT
slot counts only if the key leaves S.L+3 and S.L-3 unconstrained.

- An implementation may instead read S.L+-3 = w_{i+-3} exactly (mode "W7"; the label has them). That is also sound, and by
  section 5 it gives the same LP optimum and the same prices.
- Degrees beyond the enumerated receiver range (the stack's big-vertex argument) may ignore the OUT term (under-credit).

**Worked example** (k85CL dual, row `R8 55558578/58585558`, w = -0.004686): key
`EDGE(8->5)[S.L+1={5678} S.L-1=5 S.A-1=B R.L+2={5689}]`. Link w = 5 5 5 5 8 5 7 8, apex s = 5 8 5 8 5 5 5 8. The 5s are
w_0, w_1, w_2, w_3, w_5.
- i = 0, sg = -1: S.L+1 = w_7 = 8, S.L-1 = w_1 = 5, S.A-1 = s_1 = 8 (in B), R.L+2 = s_7 = 8: match. (sg = +1: S.L-1 = w_7 = 8, no.)
- i = 1, sg = +1: w_2 = 5, w_0 = 5, S.A-1 = s_7 = 8, R.L+2 = s_1 = 8: match. (sg = -1: S.A-1 = s_2 = 5, no.)
- i = 2, sg = -1: w_1 = 5, w_3 = 5, s_3 = 8, s_1 = 8: match. (sg = +1: S.A-1 = s_0 = 5, no.)
- i = 3, sg = +1: w_4 = 8, w_2 = 5, s_1 = 8, s_3 = 8: match. (sg = -1: S.L-1 = w_4 = 8, no.)
- i = 5: S.L+-1 = {w_4, w_6} = {8, 7}; S.L-1 = 5 fails both ways.
- IN: the link 8s (w_4, w_7) pay the centre with payee letter 8, not 5.
So pay = 4, get = 0, coefficient IN - OUT = -4, contribution to the colsum (-0.004686)(-4) = +0.018743.

### 3.2 The payee's row -- IN, possible match (NEW only for window payee rows)

The payer is a link vertex w_j of letter 8 or 9 of a row whose centre is the payee.

**Every payee picture.** For a payer of degree >= 8, S.L+3 and S.L-3 are the payer's own privates (its link vertices other
than the centre, w_{j-1}, w_{j+1}, s_{j-1}, s_j). No picture of the stack knows them: they are always the wildcard on the
payee side. The other positions are as for a payer 7 (KEYSPEC section 5, IN slot): with sg = +1 (S.L+1 = w_{j-1}),
S.L+1 = w_{j-1}, S.L-1 = w_{j+1}, S.L+2 = s_{j-1}, S.L-2 = s_j, R.L+2 = w_{j-2}, R.L-2 = w_{j+2}, S.A+1 = w_{j-1}'s private
next to s_{j-1} (s_{j-2} if w_{j-1} = 5), S.A-1 = w_{j+1}'s private next to s_j (s_{j+1} if w_{j+1} = 5); sg = -1 mirrors.

| payee row | picture for the IN slot (unchanged pictures) | new? |
|---|---|---|
| sender (5) | send_pic: link exact; apexes S/B classes; a link 6's private = its class F; 7+ privates wildcard. IN enters with -1 (OUT - IN). | no: grammar.slots already walks every link vertex; these slots existed but no key used them |
| cons2 (6) | cons_pic: link exact (5..9); apex classes S/B; privates wildcard | no (as above) |
| receiver d = 7 (gkleaf) | KEYSPEC section 5 picture (link-6 privates pmask & ~extra6, link-7 privates MASK & ~extra7 where c, a <= 6); link 8 / 9 privates wildcard | no (as above) |
| receiver d >= 8 (gkwin) | the gkwin window centred at the payer w_j, (w_{j-2..j+2}, s_{j-2..j+1}): S.L+-1, S.L+-2, R.L+-2 exact; S.L+-3 wildcard (as for a payer 7); S.A+-1: neighbour 5 -> the apex beyond it; neighbour 6 -> its amask OR-ed over its two out-of-window arguments ((w_{j-3}, s_{j-3}) for w_{j-1}; (w_{j+3}, s_{j+2}) for w_{j+1}); neighbour 7+ -> wildcard. Payee letter U = min(d, 9). | YES: gkwin's "payer in {5,6,7}" gate is widened to {5,...,9} |

So the only code changes against W6's round-9 builder are: (i) OUT slots at d >= 8 (3.1), (ii) the gkwin IN gate widened
to link payers 8 and 9 (3.2, last line). mrows carry no key terms and generate no rows.

**Worked example** (row `S 55868 BSBBS`, six private class {3: S}, w = +0.004458), same key: link 5 5 8 6 8, apex classes
h = B S B B S.
- payer w_2 = 8, sg = -1: S.L+1 = w_3 = 6 (in {5678}), S.L-1 = w_1 = 5, S.A-1 = the third vertex of the triangle on (w_1, s_1)
  away from w_2, which is s_0 = B because w_1 is a 5, R.L+2 = w_4 = 8 (in {5689}): possible. (sg = +1: S.L-1 = w_3 = 6, no.)
- payer w_4 = 8, sg = +1: S.L+1 = w_3 = 6, S.L-1 = w_0 = 5, S.A-1 = s_0 = B (w_0 is a 5), R.L+2 = w_2 = 8: possible.
  (sg = -1: S.L-1 = w_3 = 6, no.)
get = 2, coefficient OUT - IN = -2, contribution -0.008915.

## 4. Soundness (direction)

For a real vertex z covered by row r, the row is a valid bound iff for every key E: IN_E(r) >= IN_E(z) and
OUT_E(r) <= OUT_E(z) (receiver / cons2; reversed roles for a sender, whose row reads OUT - IN >= 1 - t), x_E >= 0.

- **Payer side (OUT).** Every position read in 3.1 is a link or apex letter of the label of r, and a real 8 (or 9+) covered
  by r has exactly these letters (9 = 9+ in the label and in the key). So a slot that surely matches in r matches in z:
  OUT_E(r) <= OUT_E(z). Reading S.L+-3 as unknown, or dropping OUT at unenumerated degrees, only lowers OUT_E(r):
  under-credit, safe. Counting OUT on a possible match would be a bug (section 7, control "outposs").
- **Payee side (IN).** Each picture's letter set at each position contains the real letter (the same masks the existing
  keys use: pmask, MASK, f2b extra6 / extra7, the S/B classes, the gkwin window bound which only enlarges sets), and the
  payer's privates are the wildcard. So every real match is a possible match: IN_E(r) >= IN_E(z). Safe.
- Payee 9 = 9+: rows of every enumerated degree d >= 9 take the inflow; the stack's argument for degrees beyond the
  enumerated range must include a payer-8/9 key's inflow into a 9+, as it already must for the existing 5->9 / 6->9 keys.
- f2b7 changes q7m masks only; key pictures are unchanged, so nothing here interacts with it.

## 5. S.L+-3 for a payer >= 8 are inert (dominance)

At every IN slot of a payer of letter >= 8, S.L+-3 is the wildcard (3.2), so a possible match ignores X_{S.L+-3}. At every
OUT slot (3.1), restricting X_{S.L+-3} can only remove OUT matches (in W5 it removes them all). Hence for any payer-8/9 key
K, the key K* with S.L+-3 set to the wildcard has the same IN entries and at least as many OUT entries in every row: its
column is at least as good in every row, and any LP point using K stays feasible with K's amount moved to K*. So:

- the grammar can drop S.L+-3 for payers 8 and 9 (eight positions: S.L+-1, S.L+-2, S.A+-1, R.L+-2);
- modes W5 and W7 give the same LP optimum and the same best prices. Checked numerically on the k85CL dual: the W5 and W7
  searches give equal best colsums (within 2e-12) on 8->9, 9->5, 9->6, 9->7, 9->8 (all exhaustive in both modes) and on
  8->8 (exhaustive in W5; the W7 search found the same value but had not closed at 60 s) [M].

## 6. Implementation notes for a second engine

- d >= 8 separator (DP over the cyclic link): add, at each link position i and chirality, the OUT term -[sure match on
  W_i], which depends on w_{i-2..i+2}, s_{i-2..i+1} only, the same window as the existing IN terms. No leaf correction is
  needed at d >= 8 (the OUT term is exact on the window). At d = 7 no payer-8/9 OUT exists.
- d >= 8 IN terms: widen the payer gate of the gkwin bound from {5, 6, 7} to {5, ..., 9}; payer 8 and 9 use the payer-7
  branch (own privates wildcard).
- d = 7 (leaf-exact), sender and cons2: nothing to add beyond accepting payer letters 8 / 9 in the key matcher (link 8 / 9
  vertices already carry wildcard privates).
- Dual export (DUAL_EXPORT.md): `ks` and `ks_exact_picture` need no new fields. For a payer-8/9 key, OUT slots exist only on
  d >= 8 receivers; the d >= 8 `credit: window` rows now carry OUT terms.

## 7. Verification [P on W6b's engine copy, exact integer coefficients]

- `p8_check.py` on the k85CL dual (c8b2def0) with cg_keys_124.txt (35f58f8f): 0 (key, row) coefficient mismatches against
  the file's ks over all 2,873 rows; max |colsum mine - file| 5.7e-16 (W6's r9_opus check reproduced with the extended
  builder). New slots on that dual: 2,912 payer-8 OUT slots (d = 8), 880 payer-9 OUT slots (d >= 9), 250 payer-8/9 IN slots in
  window rows; 2,050 payer-8/9 IN slots in sender, cons2 and d = 7 rows that existed before.
- `p8_test.py`: (A) OUT vectors vs grammar.edge_vec on full pictures, 2,256 slots, d = 8..11, W5 and W7, 0 mismatches;
  (B) window IN vectors vs grammar.edge_vec on window pictures, 1,128 slots (246 with payer 8/9), 0 mismatches; (C) 120,000
  (row, key) coefficients on 400 random rows (window d = 8, 9, 10, d = 7 with 8/9 links, senders, cons2) x 300 random keys,
  against an independent set-based implementation of the text of sections 3.1 and 3.2 and KEYSPEC section 5, 0 mismatches
  in W5 and in W7; (D) r9_price.best_pair vs exhaustive DP over the whole key space on planted rows, pairs 8->5..9 and
  9->5..9, cert-sign and random-sign duals, 20 pairs, 0 mismatches.
- Planted controls, each MUST fail and each did: "outposs" (payer OUT counted on a possible match) 2,033 mismatches;
  "outmirror" (S.A+-1 not mirrored) 655; "in7" (payer-7 window S.L+2 read as wildcard, i.e. an existing key moves) 127 in
  the random test and 125 against the k85CL file ks.
