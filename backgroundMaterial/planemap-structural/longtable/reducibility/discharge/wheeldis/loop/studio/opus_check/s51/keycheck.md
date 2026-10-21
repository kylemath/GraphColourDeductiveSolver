# s51 (flag xo, RELAY_SPEC_s51.md at 0342b665, md5 6310794f): Studio build and key check

**Status: built. The upper and separator side passes its self-tests, and the default path is unchanged. One spec ambiguity is open (A1, below):
§51.3's pricing table (4 negative xo keys on A78 at −24/421, 10 on A83) cannot be reproduced from the spec text.** Nothing was solved.

## Independence statement
I built this from RELAY_SPEC_s51.md alone, on top of my RELAY_SPEC_s21 / s39o / s44 / s47 checker (out/job31/st21_check.py), with the
14' kill tables (pmask) as the spec's amask and isR6 as NR6. Opus files opened: s51/RELAY_SPEC_s51.md only, plus data I already had (the
s42a A78 cert/sol and the A83 nosep cert/sol). I did not open s51/pricer51.py, s50/REFINE_PRICE.md, s50/pricer50.py, any engine
(s47/eng, jsep*), cmd script or log; their names come from the spec text only. Team B material: none.

## Implementation (out/job31/st21_check.py, opt-in XO=1; off by default)
- **Keys:** sidex, tauo and the decode exactly as §51.1. Visible tuples A± = (w_{i±1}, s_i / s_{i−1}, w_{i±2}, s_{i+1} / s_{i−2}, m±) as §51.3.
- **Domain masks:** c = 5 gives `1 << LI[o]`. c = 6 gives NR6 on the 6's wheel `(U, w_{i+2}, s_{i+1}, p, s_i, w_i)` (mirror for −), AND the OR over
  (x, y) ∈ LET² of pmask (the 14' private mask M uses) at the spec's argument order. c ≥ 7 gives 31.
- **Credit key:** q = (U, V, min, max). Candidates in(eA, eB) and out(eA, eB) as §51.3. R6: no term on an empty mask, or when in = out for
  every candidate.
- **Receiver rows:** +XQ[q] at every big w_i, and no old x term.
- **val:** XQ = XQeff(q) = max over candidates of (xo[in] − xo[out]).
- **Solution:** "xo" / "xoflag". Old x non-empty under xo, or xo values with xo off, is a failure. xo values must lie in [0, 3].
- **Lower:** mrowX labels are validated as §51.6 (U, V ∈ 7..9, letters, mask 1..31, A ≤ B, eA / eB bits set). The row is
  `+xo[in] −xo[out] −XQ[q]`, w ≤ 0. xo with rc < 0 is priced at xcap 3, and XQ is priced at its box (−3·|rc|).
- **Upper:** §51.5(5) sparse window table. Every positive xo key is decoded to the (U, 9-slot) windows where it is an in- or out-key,
  forward-verified. XQeff is evaluated there and added to the separator's exact window table (the same SEP_FB6 channel as fb, with the
  relaxed max over the unread slots). The d ≥ 18 DP / Karp read the same relaxed table at U = 9. No change to bin/sep3r_l3q.
- **Broken-build controls:** `XOBROKEN=end` (u reads the far outer letter), `sign` (receiver gets −XQ), `sep0` (no xo term in the
  separator table).

## Checks
| check | result |
|---|---|
| §51.9 worked example, hand window (8; 5,6,7,6,7; 6,5,6,6) | out key for (e+, e−) = (5, 5) is **(8, 7, (6,5,5,6,5), (6,7,6,6,5))**, as the spec states; in ≠ out, so there is a term. With A78's real masks m− = 29 and m+ = 31 (20 candidates) |
| default path (xo off), new code in place | s42a A78 lower **VALID 44/421**, A83 nosep lower **VALID 132/1301**, both unchanged (reg_off_A78/A83.log) |
| separator self-test, XORAND (random xo on 138,335 keys of 4,000 big windows; 143,253 windows in the table) | leaf vs spec rows **max 4.98e−10** (3,020 rows); relaxed vs spec on 3,620 arrangements: **0 below exact**; d = 7 exhaustive: 5,000 rows each re-checked exactly, 0 deviations |
| broken separator `sep0` | **caught**: 36 relaxed rows below exact, d = 8 exact weight differs from the spec row by 0.025, FAIL |
| broken rows `sign`, first-order pricing | **caught**: every xo key goes negative (A78 334 keys, Σ 5056/421; A83 565 keys) |
| broken rows `end` | not separable by my pricing (it equals the correct build: 0 negative). Its catch needs A1 resolved, or a solved cert |

## A1: answered (coordinator, 09:17Z): the §51.3 table is an optimised spread, not a function of the cert
- **The answer:** Opus's table splits each row that has unpinned unseen outer letters into one row per compatible completion, with the
  weight split convexly and relabels allowed. An LP then picks the split that minimises Σ max(0, −rc), and the result is rationalised.
- **What follows:** the table is a best-case estimate, so it **does not gate this key check**. I will reproduce it exactly from Opus's
  §51.3a addendum and its dumped per-candidate mrowX duals for A78 / A83 when they arrive (still spec-only: pricer51.py stays unopened).
  The broken-`end` catch will come from the first solved xo cert.

### A1 closed (21 Oct, §51.3a at e43a4d6e, spec md5 04811586): the table is reproduced exactly from Opus's duals
- **Inputs:** the data files s51/spread_A78.json (md5 be8421e6) and s51/spread_A83nf.json (f1f29e7f). I did not open pricer51.py.
- **Method:** opt-in `XOPRICEMODE=json SPREADJSON=…`. For every credit key q and candidate (eA, eB), Opus's mrowX dual y is fed into
  Studio's own §51.3 formulas: my in / out keys from (A, eA) and (B, eB), with rc(xo in) −= y and rc(xo out) += y.
  - the q in the file are checked against my own XQ ledger from the cert rows;
  - the balance of every free column XQ[q] is checked (my Σ w·coef = the file's receiver sum = Σ of its duals);
  - every dual must be ≤ 0, on a candidate whose bits are set in the masks;
  - every row must have exactly one mode with α = 1, and its completion weights must be a convex split of the row weight (same sign,
    summing to w at each position).

| cert | Studio from the duals | the file / §51.3 | checks |
|---|---|---|---|
| A78 cert_q42aA78L | **Σ 96/421, 4 negative, min −24/421**; keys (8,7,(6,5,5,6,5),(6,7,6,6,5)) [the §51.9 key], (8,7,(6,5,5,5,6),(6,5,7,6,5)), (7,8,(6,5,5,5,6),(6,7,5,5,6)), (7,8,(6,5,5,6,5),(6,6,7,6,5)), each −24/421 | identical keys and rc | 12 credit keys and 12 duals: q not in my ledger 0, balance mismatches 0, bad candidates / signs 0. 9 rows / 16 positions: 0 with relabels, convex-split violations 0 |
| A83 cert_q44nfA83L | **Σ 2618/29923, 10 negative, min −426/29923** | identical keys and rc | 38 credit keys and 42 duals (4 keys on more than one candidate): all checks 0. 27 rows / 51 positions: 0 relabels, 0 split violations |

- **Broken `end` is now caught.** With u reading the far outer letter, the same duals give the same totals (Σ, count, min), but on
  **different keys**: the negative-key set no longer equals the file's, on both A78 and A83. The broken-`end` gap is closed for the
  key check. A solved xo cert will still give the catch inside the LP.
- **A2 (for Opus to confirm):** the file omits 4 A78 / 6 A83 cert receiver rows.
  - **Expected:** those of degree 10 and 11 have no big link vertex.
  - **The d = 7 ones:** A78 7766556/6576576 and 7665566/6675676; A83 7766656/6566556, 7766556/6566576 and 7665566/6675676. Here the
    old x coefficients cancel within the row (a 7-7 pair, or in = out at a single big), so there is nothing to spread.
  - **Under §51.3 / R6 (per position)**, my build gives those positions +XQ credits, because in ≠ out for some candidate. On A78 that
    is 3 credit keys at rc +4/421, all positive, so this does not touch the table.
  - **Please confirm** that Opus's xo `recv_coef_R2` also adds +XQ per position there, and does not drop rows whose old x cancels.
    Otherwise Studio's and Opus's xo rows differ on those arrangements.

### A1 as first raised: the §51.3 pricing table is not reproducible from the spec text
§51.3 reports, for "x_outMW (this spec)" on the old certs (which have no mrowX rows): A78 Σ max(0, −rc) = 96/421 (4 keys at −24/421),
and A83 2618/29923 (10 negative, most negative −426/29923). The spec does not state how xo columns are priced on a cert that has XQ
in its receiver rows but no mrowX rows. I tried three readings:

| reading | A78 | A83 |
|---|---|---|
| directional derivative of XQeff at xo = 0 (max over candidates of [in = t] − [out = t]; the s45 bundle analogue) | 0 negative | 0 negative |
| mrowX dual extension cancelling rc(XQ q), all weight on the first candidate | 13 negative, Σ 228/421, min −24/421 | 36 negative, Σ 18665/29923, min −60/1301 |
| the same, weight spread equally over the candidates | 325 negative, Σ 1148/2105, min −3/842 | 538 negative, min −12/1301 |

- **What my build finds:** under my build, on A78, rc(XQ) ≠ 0 on 15 credit keys, touching 334 xo keys. On A83 it is 42 credit keys,
  touching 565 xo keys.
- **Why no single out key prices negative:** the A78 binder's masks are wide (29 and 31, giving 20 candidates). With that, no single
  out key moves XQeff, so a single-key first-order price cannot be −24/421 without a rule for where the receiver's dual goes.
- **Request:** please state pricer51's rule in the spec text (which candidate or candidates carry each receiver row's XQ dual), or the
  mrowX duals it uses. Then I can rerun the key check. This does not affect the soundness side (rows, masks, upper and lower checks).

## A86 (main ea8944db) tables, pre-built
- **k3x:** D 2,715 lines (md5 c1b1b4e1), C 1,232 (6c27df6f).
- **Forbidden set:** 582 RSST + 3,947 = 4,529.
- **Kill tables:** kill6 U7 27a64538, U8 = U9 6dc44bba (unchanged since A78). Check 4: 3,072 / 7,500 survivors.
- **l3q masks:** V = 7: 190 of 30 per side (md5 22e1f5ef, as A78 / A83). V = 8: 50 of 30 per side (2e8e8f5e).
- **Ring-merge sweep at ea8944db** (loop/studio/opus_check/s51/A86/ringmerge_sweep_A86.out): **129 FAIL, the same set as the
  129-FAIL set (a2ec92e5)**. FAIL minus f9_....5565B_....6655. is exactly exname_rm128.
- **Args:** argsA86_local_rpat_held128.txt = the A83 args with the two k3x files swapped.
