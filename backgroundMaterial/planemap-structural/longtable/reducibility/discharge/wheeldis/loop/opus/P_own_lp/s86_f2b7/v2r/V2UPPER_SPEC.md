# V2UPPER_SPEC: the exact upper (primal) check of a point under the KEYSPEC v2 receiver model (Opus s86, `upperR2 ... v2r`)

Purpose: to let a second engine (W6b k2b DP, the Studio) decide from this text alone whether a point (t, x) is FEASIBLE when the d = 7 / 8
receivers carry the KEYSPEC v2 max-row instead of the masked row. The row itself (value(rho; x), the realisation rho, the domains) is
defined in `V2ROW_SPEC.md` (same folder, sections 2-4). This file adds what the upper check does with it. No engine code is needed.

## 0. Summary

* A point is FEASIBLE under v2 iff every family of the standard upper check passes exactly as before (section 2), except that each
  d = 7 / 8 receiver label (d, w, s) passes iff  **max over rho in the domain product of value(rho; x) <= d - 6 + t + 1e-9**.
* Exhaustive and exact in the combinatorics: every admissible label is covered (via a superset listing, section 3.3), and each listed
  label's max over rho is an exact max-plus DP (section 3.4). The arithmetic is float64, like the standard check (section 4).
* Output: the standard final line `UPPER-R2: FEASIBLE at t = <t>` / `UPPER-R2: INFEASIBLE (<n>) at t = <t>`, followed by ` (v2r)`,
  with a `v2r upper summary` line just before it (section 5).

## 1. Inputs

* The point: a solution JSON (`sol_*.json`): `t` and the column values. Formats are as in the standard check (RELAY_SPEC.md 12.2 and
  the later family specs): `y` a dict `"U|rest"` -> value (a rooted 5-word, U = the big's letter); `x` a dict int -> value; `h`, `g`, `q`,
  `lq`, `lQ`, `z`, `zr`, `r`, `rr` lists of `[key tuple, value]`; `ks` a list of `[key name, amount]`. A column not listed is 0.
* The family: args (the reducible registry), the stack tables (STACK s77), the f2b rules file, rpatN, the generic-keys file and the flags.
  For the points in section 6: args `args_A97_F_W13K3l5.txt` (K3l5, md5 2547de87), keys `cg_keys_r13w16_16fik.txt` (240 keys, 3d996dbb),
  rules `rules_c67fa1d1_plus_A5_twins.json` (2db75746), `rpatN3_rotation_justified.txt` (8b90a842), flags
  `xon apexcls filt16 hat5 consall l3q lqcap=3 l3qV=7,8 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3 c6le f2b7 gkwin gkleaf` + `v2r`.

## 2. What FEASIBLE means (every item must hold)

| # | family | condition | status under v2 | where it is specified |
|---|---|---|---|---|
| 1 | column ranges | z, zr, rr in [0, 3]; lq in [0, 3]; lQ >= 0; ks in [0, 3]; y, g, h, r, rr, z, zr >= 0; the solution's family flags match the run's | unchanged | RELAY_SPEC_s21.md (l3q), RELAY_SPEC_s22.md (z / zr / rr), KEYSPEC.md (ks) |
| 2 | senderR2 rows | every row over every admissible assignment >= 1 - t - 1e-9 | unchanged | RELAY_SPEC.md 12.3 (+ s21 / s22 / s45 terms, KEYSPEC.md keys) |
| 3 | cons2 rows, c6le | for each of the 1,424 canonical non-R6 6-links and each of the 5^6 apex words: in - out <= t + 1e-9 (one-sided: "the 6 ends <= t") | unchanged | RELAY_SPEC.md 12.4 (the rows); c6le = the one-sided relaxation of 12.7 item 2 |
| 4 | receivers d = 7, 8 | **v2 max-row, section 3** | **changed** | this file + V2ROW_SPEC.md |
| 5 | receivers d = 9..17 | masked receiverR2 load <= d - 6 + t + 1e-9, exhaustive over all admissible labels | unchanged | RELAY_SPEC.md 12.5 / 12.7 item 3, RELAY_SPEC_s45.md / s47.md (l3qV), f2b7 `SPEC.md`, KEYSPEC.md (gkwin windows) |
| 6 | tail d = 18..30, Karp | relaxed closed-walk max <= d - 6 + t + 1e-9 (else exact pattern-free enumeration with 0 violated); Karp: d0 = (6 - t) / (1 - lambda) <= 31 | unchanged | RELAY_SPEC.md 7 and 12.7 item 4 |
| 7 | admissibility | which labels are receivers at all: R5, R6, RBIG, the args registry patterns, rpat / rpatN / offc | unchanged, and it applies to item 4 as well: only admissible labels are checked | RELAY_SPEC.md 4.4-4.5, OFFC_SPEC.md, RELAY_SPEC_s39o.md |

The verdict counts failures: n = (sender rows violated) + (cons links violated) + (d = 7 / 8: v2-violated receivers + DP / row
mismatches + superset breaks + refusals, section 3.5) + (d >= 9 rows reported violated; the standard check reports at most `vK` per d,
default 20) + (tail failures) + (1 if Karp fails). FEASIBLE iff n = 0.

## 3. Receivers of degree 7 and 8 under v2

### 3.1 The condition

For every admissible label (d, w, s), d in {7, 8} (link w_0..w_{d-1}, apex s_0..s_{d-1}, letters 5..9 with 9 = 9+), whose domain
product dom_0 x ... x dom_{d-1} (V2ROW_SPEC.md 3) is nonempty:

    V2(d, w, s; x) = max over rho in the product of value(rho; x)  <=  d - 6 + t + 1e-9

value(rho; x) = fixed(x) + sum_j base_j(x_j, y_j)(x) + sum_K (IN(K; rho) - OUT(K)) * ks_K   (V2ROW_SPEC.md 4.1-4.3). A label with an
empty product has no realisation (it is reducible) and passes. Columns are read from the solution as in section 1. The envelope
columns M, Q, lQ of the masked row are **not** read: they are not v2 columns.

### 3.2 Why the check needs a candidate list

There are about 5^14 (d = 7) and 5^16 (d = 8) labels, so the DP is not run on every one. The masked load is used as a filter that
cannot lose a violated label.

### 3.3 The masked superset (pointwise masked >= every realisation row)

The masked load L(d, w, s; x) is the standard upperR2 receiver load: the masked receiverR2 row at the point, with
M(sgM) = max over sig2_keys(sgM) of h, Q(sig) = max over q7keys(sig) of q, lQ(key) = max(the lQ column, max over the mask's letters a2
of lq(.., a2)), and every generic key at its masked coefficient (possible IN minus OUT). Termwise, for every rho in the product:

* fixed: identical in both rows (V2ROW_SPEC.md 4.1 is the masked row minus its M / Q / lQ entries);
* a 6 at j: its copy's key h2_of(.., p, ..) lies in sig2_keys(sgM) (V2ROW_SPEC.md 3, the 6 row), so h[copy] <= M(sgM);
* a 7 at j: qkey(.., p1, p2, ..) lies in q7keys(sig), so q[copy] <= Q(sig); each side's lq(.., p) has p in the side's mask, so lq <= lQ_eff;
* keys: OUT(K) is the same count in both rows; IN(K; rho) <= the masked "possible" IN count (a slot that matches the exact picture of
  rho matches the masked picture, whose private positions are the domain letter sets); every amount ks_K >= 0 (item 1 of section 2).

So L >= value(rho; x) for every rho, hence L >= V2, and every v2-violated label has L > d - 6 + t + 1e-9. The check lists **every**
admissible label with L > d - 6 + t + 1e-9 - 1e-7 (margin 1e-7, section 4) by the standard exhaustive d = 7 / 8 search, with no
top-K selection (a refusal cap of 10^7 labels: reaching it stops the check with a failure, it never drops labels). The search reports
labels in a symmetry-reduced form, possibly several per dihedral orbit; the check canonicalises each to the minimum of its 2d images
(rotations w_i -> w_{i+r}, s_i -> s_{i+r}; reflection w_i -> w_{-i}, s_i -> s_{-i-1}) and keeps one per canonical label. V2 is
invariant under the 2d images (the row is symmetric: both orientations of every key slot are counted, h2_of / qkey are canonical); this
is also checked numerically (section 6).

A second engine may use any superset instead (for example its own list of all admissible labels with masked load above the cap minus
a margin, or all admissible labels); the verdict is the same.

### 3.4 The DP: max over rho for one label

Sites. For j = 0..d-1 the site Q_j = (x_j, y_{j+1}) (indices mod d), 25 states, state number q = 5 (x_j - 5) + (y_{j+1} - 5). The pair
of group i, (x_i, y_i), is read from two consecutive sites: x_i = Q_i.x and y_i = Q_{i-1}.y.

Factors. F_i(Q_{i-1}, Q_i) for i = 0..d-1:

    F_i = base_i(x_i, y_i)(x)            if (x_i, y_i) in dom_i, else -infinity
        + sum over keys K with ks_K != 0, over the two IN slots (i, +1), (i, -1) of K that are "live",
              ks_K * [the slot's four private positions match]

base_i is the copy value of V2ROW_SPEC.md 4.2 at the point (0 for a 5, an 8 or a 9+). An IN slot (i, sg) of key K (payer w_i, payee
the centre, V2ROW_SPEC.md 4.3) reads ten positions; six of them are link / apex letters (fixed by the label) and four are privates.
The slot is live when the payer letter w_i is in K's payer set, d is in K's payee set and the six fixed positions match. A live slot
fires iff its four private positions match; for sg = +1 they are S.A+1 = x_{i-1}, S.L+3 = y_i, S.L-3 = x_i, S.A-1 = y_{i+1}, and for
sg = -1 S.A-1 = x_{i-1}, S.L-3 = y_i, S.L+3 = x_i, S.A+1 = y_{i+1}. All four lie in (Q_{i-1}, Q_i) = ((x_{i-1}, y_i), (x_i, y_{i+1})), so
every term of the row sits in exactly one factor. A position the key does not list is a wildcard.

Cycle product. With P(Q_0, Q_1) = F_1(Q_0, Q_1) and, for i = 2..d-1, P(Q_0, Q_i) = max over Q_{i-1} of P(Q_0, Q_{i-1}) + F_i(Q_{i-1}, Q_i):

    DPmax = max over (Q_0, Q_{d-1}) of P(Q_0, Q_{d-1}) + F_0(Q_{d-1}, Q_0)
    V2(d, w, s; x) = fixed(x) + DPmax - sum_K ks_K OUT(K)

(-infinity when the product is empty.) Cost: d - 2 products of 25 x 25 x 25; about 3-5 ms per label in numpy.

Ties. The argmax rho is any maximiser; the engine takes the first maximiser in state order (numpy argmax over (Q_0, Q_{d-1}) flattened,
then backtracking). Only the value V2 enters the verdict; a second engine may report a different maximiser (section 6 has labels with
15,000 and 625 maximisers).

### 3.5 Cross-checks inside the check (each failure counts in n)

* DP / row: the realisation row of the argmax rho is rebuilt independently (V2ROW_SPEC.md 4, with the key counts read from the exact
  picture of rho) and evaluated at the point; |row value - V2| > 1e-9 max(1, |V2|) is a failure. The larger of the two values is used.
* Superset: V2 > L + max(margin, 1e-9) for a listed label is a failure (it would mean section 3.3 is broken).
* 1-site neighbourhood (on by default): for every listed label, every rho that differs from the argmax at one site is evaluated by the
  independent evaluator; a value above V2 + 1e-9 max(1, |V2|) is a failure.
* Refusal: the listing reached its cap.

## 4. Tolerances and arithmetic

* eps = 1e-9 absolute on every family, as in the standard check: a row fails when it exceeds its bound by more than 1e-9 (senders:
  falls below 1 - t by more than 1e-9).
* Masked listing margin 1e-7: labels with L > d - 6 + t + 1e-9 - 1e-7 are listed. L (the search's sum) and V2 (the DP's sum) are
  float64 sums of the same numbers in a different order; on the tight labels of section 6 they agree to 5e-13, so a margin of 1e-7
  cannot lose a label that the DP would call violated.
* Everything is float64; nothing is rounded beyond that. What is exact: the enumeration (every admissible label is covered), the domain
  products, the integer row coefficients and the max over rho (the DP is exact max-plus, not a relaxation). The verdict is the float
  verdict with the 1e-9 rule, like every standard upperR2 verdict.

## 5. Output lines

    v2r upper: d = 7 / 8 receivers under KEYSPEC v2 (max over rho of the realisation row, exact DP; masked list margin v2umargin = 1e-07)
    d=7: v2r: masked exhaustive (<s>s): <n> leaves above d - 6 + t + eps - <margin>, <m> of them masked-violated (<a> / <b> canonical
         receivers); v2-violated <v> (DP max > d - 6 + t + eps)[, worst excess <e> at receiverV2 7 <link> <apex> rho <rho> (value <V2>)];
         empty domain <k>; DP <s>s (<n> calls, <ms> ms each); masked - v2 over the list: min <>, median <>, max <>; phantoms
         (masked-violated, v2-satisfied) <p>; DP / row mismatches <k>; superset breaks <k>
    d=8: (same)
    ... the standard lines for senders, cons, d = 9..17, the tail, Karp ...
    v2r 1-site neighbourhood check: <n> receivers, <n> neighbours evaluated, <k> above the DP max (<s>s)
    v2r upper summary: masked-violated <n> leaves (<a> canonical receivers); v2-violated <v> receivers (phantoms <p>)[, worst excess ...];
         tightest v2 receiver excess <e> at receiverV2 <d> <link> <apex> rho <rho> (value <V2>); DP <s>s over <n> receivers (<ms> ms each);
         DP / row mismatches <k>
    UPPER-R2: FEASIBLE at t = <t, 12 decimals> (v2r)        or        UPPER-R2: INFEASIBLE (<n>) at t = <t> (v2r)

`vfile=` receives one line per v2-violated label, `d value excess link apex rho` (column 3 = excess, as the standard vfile), followed by
the standard d >= 9 lines `d load excess link apex`. "masked-violated" counts the search's leaves with L > d - 6 + t + 1e-9, the same
number the standard check prints as `d=7: <n> violated`.

## 6. Worked receivers (the probe point) and the validation numbers

The probe point: `sol_S4W09k240_probe.json` (md5 b04b8c26) = `sol_S4W09k240.json` (eea14563) with t lowered by 0.003 to t = 0.025372061;
family of section 1. Full decompositions in `V2UPPER_vectors.json` (md5 552fcb57): per site the domain size, the base value of every
pair at the point, the argmax pair; the keys with a nonzero amount that can fire (OUT, IN at the argmax); the argmax row with every
column's value; the exhaustive max and its number of maximisers when the product has <= 50,000 realisations.

### 6.1 `7 5566786 5675657` (v2-violated; the worst excess at the probe)

* Sites: w = 5, 5, 6, 6, 7, 8, 6; domain sizes 1, 1, 4, 5, 20, 25, 3; product 30,000.
* V2 = 1.028371298400 (fixed part 0.772826731592), cap 1.025372061, excess +0.002999237400 (> 1e-9: violated).
* Argmax rho (engine) 75566655565577: sites (75)(56)(66)(55)(56)(55)(77). The 6s take their best private (base 0.224629775573,
  0.009985657952, 0.071408526184); key gk03_37 (amount 0.003481346) fires once (IN 1); cg12_76_0 (0.026493269) has OUT 2, w6b16_03 OUT 1.
* Exhaustive over all 30,000 realisations: max 1.028371298400, attained by 15,000 of them (the 8's privates are free); next value
  1.025131131710.
* Masked load L = 1.028371298400 (equal to V2 up to 5e-13: no phantom gap on this label).

### 6.2 `8 55558558 59567676` (d = 8, v2-violated; a small row to replay by hand)

* Sites: six 5s (one pair each) and two 8s (25 pairs each); product 625; no base terms.
* The argmax row (19 entries), coefficient x column = value at the point:
  2 y(8,5,5,6,8) 0.298200803879 + 2 y(8,5,5,9,5) 0.481289174132 + 2 y(8,5,6,7,8) 0.232913833202 + 2 r(5,0,9,5,1,6) 0.027145251119
  - 2 x[62627] 0.024794099516 + 2 x[63135] 0 - 2 rr(5,0,9,5,1,6) 0 + 2 z(..) 0 (three) - 2 zr(8,5,5,9,5,1,0) 0.003797465176 - 2 zr (two more, 0)
  + 4 ks[cg12_58_0] 0.001561469751 + 2 ks[w6b16_12] 0.000105212059 + 2 ks[cg12_58_1 / cg12_58_2 / w6b16_10 / w6b16i_11] (amount 0)
  = 2.028371298400.
* Cap 2.025372061, excess +0.002999237400. All 625 realisations attain the max (the IN counts of cg12_58_0 (4) and w6b16_12 (2) do not
  read the 8s' privates), so any rho is a valid argmax; the engine reports 6559955655766755.

### 6.3 `7 5766767 5676665` (a phantom: masked-violated, v2-satisfied)

* Sites: w = 5, 7, 6, 6, 7, 6, 7; domain sizes 1, 23, 5, 5, 25, 5, 23; product 1,653,125 (DP only; the 1-site check covers its argmax).
* Masked load L = 1.028371298400 > cap 1.025372061 (excess +0.002999237: the standard check counts it), but
  V2 = 0.881314622970 at rho 55575555555575 (excess -0.144057438: passes). Gap L - V2 = 0.147056675: the masked row takes each 7's
  envelopes (Q, the two lQ sides) and every key's possible IN independently, while one realisation must choose one letter per private.

### 6.4 Validation (Opus s86, v2r/NOTES.md)

| point | standard upperR2 | v2 upperR2 |
|---|---|---|
| sol_S4W09k240, t = 0.028372061 | FEASIBLE | FEASIBLE (v2r): no d = 7 / 8 label within 1e-7 of the cap; 172 s, peak RSS 1.52 GB |
| same, masked list down to 0.002 below the cap | (0 violated) | 405 canonical labels listed (860 leaves); V2 <= L on all (L - V2 >= -4.96e-13); brute force on 10 = DP; sym check 320 DPs equal; 21,230 neighbours none above; tightest V2 excess -7.63e-7 (7 5566786 5675657) |
| probe, t - 0.003 | INFEASIBLE (2367): senders 1131, cons 1, d = 7 491, d = 8 721, d = 9 23 | INFEASIBLE (1697): senders 1131, cons 1, d = 7 / 8 masked 1212 leaves = 563 canonical, v2-violated 545 (206 + 339), 18 phantoms (gap up to 0.185), d = 9 20 (vK cap); brute force on the 20 worst (202,375 realisations) = DP |
| sol_S4W09k240 with lQ[(5,5,31)] + 1e-5 (`sol_S4W09k240_lQ.json`, 4821040c; lQ is a masked-only column) | INFEASIBLE (10): d = 7 10 | FEASIBLE (v2r): the 10 leaves (4 canonical labels) are all phantoms |
| planted DP bug (the DP drops key gk03_37's IN term, the row builder keeps it), sol_S4W09k240 with margin 0.002 | - | INFEASIBLE (25): 25 DP / row mismatches (true verdict FEASIBLE) |
| same bug, probe | - | INFEASIBLE (1737) = 1697 + 40 mismatches; v2-violated counts unchanged |

## 7. Files (this folder)

| file | md5 | content |
|---|---|---|
| V2UPPER_SPEC.md | (MD5SUMS) | this file |
| V2UPPER_vectors.json | 552fcb57 | the three worked receivers of section 6 |
| sol_S4W09k240.json / sol_S4W09k240_probe.json / sol_S4W09k240_lQ.json | eea14563 / b04b8c26 / 4821040c | the points |
| cg_keys_r13w16_16fik.txt | 3d996dbb | the 240 generic keys |
| mlist_C_probe.txt | 80022500 | every listed label at the probe: `d L V2 link apex rho` (563 lines) |
| viol_v2C_probe.txt | ac2e1587 | the probe's vfile (545 v2-violated + 20 d = 9) |
| logs/*.log | | the runs of section 6.4 |
