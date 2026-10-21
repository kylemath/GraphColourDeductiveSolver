# s50: pricing radius-2 refinements of the generic families against existing certificates (no solves)

Opus, 21 Oct 2026. This is a pricing study only: no LP of the main problem was solved. The engine `s50/eng` is a byte copy
of `s44/eng` (md5s in `engine_src_md5.txt`; prelay2.py includes port_repair), run with fb off and the s42a flag set
`xon apexcls filt16 killtab hat5 consall l3q l3qtab lqcap=3 rpatN=s39o/rpatN3.txt xcap=3`,
exname `s40f/exname_rm128.txt`. Everything ran at nice 10, threads 1.

| cert | registry | rows (S / C / mR2 / mL / R) | lowerR2 (s50/eng) |
|---|---|---|---|
| (a) `s42a/run_A78/cert_q42aA78L.json` | reg_A78 | 22 / 86 / 29 / 5 / 13 | VALID 44/421 = 0.104513; `ctl_lower_A78.log` is byte-identical to `s42a/run_A78/lower.log` |
| (b) `s44/run_A83nf/cert_q44nfA83L.json` | reg_A83 | 41 / 120 / 47 / 15 / 33 | VALID 132/1301 = 0.101460; `ctl_lower_A83nf.log` is byte-identical to `s44/run_A83nf/lower.log` |

Files:
- `pricer50.py`: the pricer.
- `price_A78.log`, `price_A83nf.log`, `price_*.json`: the output, including the full top-10 lists with every contributing row.
- `handcheck50.py` / `handcheck50.out`: the hand check.
- `ctl_lower.sh`, `env50.sh`.

## 1. Method

**Rows.** The pricer execs the engine and runs its own `cmd_lowerR2`, patched only to capture `tot`, `tco` and D. Every
cert row is rebuilt from its label with the engine's functions: `R2_sender_rows`, `cons2_coef`, `recv_coef_R2` and the
mrow forms. Control 0 checks that the rebuilt ledger equals lowerR2's ledger exactly on every column (226 columns for A78,
358 for A83).

**Refined occurrences.** For the family being refined, the pricer re-derives each occurrence in each row with its own key
code, written from RELAY_SPEC §2/§12.2 and not from the engine's key functions. Each extra radius-2 letter is handled in
one of two ways:
- **Pinned:** the label shows the letter, so it is read directly.
- **Unseen:** the letter becomes a variable over its engine domain:
  - a link 6's private: the non-R6 letters ∩ the filt16 `amask`, shared by both sides of that 6;
  - a big link vertex's own unseen neighbour: 5..9;
  - the middle hat t_i of a five: 5..9;
  - sender hats and fans: their exact letters within the label's class bits, under the sender's six-admissibility test
    with the exact letters substituted.

**Coarsening check.** Every completion is coarsened back to the old key. The result must equal the engine's coefficients
for that family in that row. This is an assert, and it passed for every completion of every row.

**Spreading.** In the refined LP, a row with unseen letters becomes one row per compatible completion, which is
worst-case over the unseen letters exactly as the engine generates rows. Its old weight w may be spread convexly over
those completions (λ ≥ 0, Σλ = w).
- Unseen variables that no occurrence shares form separate components. Each component is enumerated as an exact product,
  and conv of a Minkowski sum is the sum of the convs, so this is exact. No component needed truncation.
- The largest LP had 405,753 spread variables (A83 y_hats).
- **Relabel freedom** is used too. These are other labels that give the identical old row, so they are genuine rows of the
  refined LP:
  - sender bit vectors with the same coefficients (A78: 1 row has 2; A83: 6 rows);
  - cons2 apex words s′ with `cons2_coef(L, s′) = cons2_coef(L, s)` (64 to 1,296 per row);
  - single-slot receiver relabels that keep the coefficients and admissibility (none exist; every receiver label is rigid).
- The **as-labelled** variant (no relabel freedom) is in the logs. It changes the counts only for h_apf.

**Pricing.** HiGHS (dual simplex) finds the spread that minimises Σ_k′ max(0, −rc_k′) over the refined columns. That
split is rationalised, renormalised and re-evaluated in exact Fractions, and the exact numbers are the ones reported.
The coarsened ledger of the split is asserted equal to lowerR2's. Spreading never changes a non-refined column, t's
coefficient or D.

**What the numbers mean.**
- If the minimum is 0, the old cert spread is a valid dual of the refined LP, so t* does not move at all. This is exact,
  not first order.
- If the minimum is > 0, the negative rc are the first-order potential, priced as Σ max(0, −rc)·cap at caps 0.05, 0.1
  and 0.3, as in s44 §44.6.
- For x, which has a real cap of 3, the logs also give the valid bound D of the split cert with x priced at cap 3.

**Interpretation of the asked refinements.**
- **y_ap (y + both apex letters exact):** the hats w_{i+2}, w_{i−2} that the receiver sees beside u (zkey's slots, with
  exact letters).
- **y_hats:** all five hats exact. h1/h3 are visible if the neighbouring link vertex is a five; otherwise each is a
  6-private (shared with the five on the other side) or a big's unseen neighbour. h2 = t_i is always unseen.
- **x_out:** each side (c, a, b) is extended by c's two second-ring neighbours (ea next to a, eb next to b). The receiver
  sees one of them, s_{i±1} (both if c = 5). The other is the 6's private, or the big c's unseen neighbour, and it is
  shared by the in and out keys at that position.
- **h_ap:** h2 with exact apex letters s_j, s_{j−1}.
- **h_apf:** h_ap + "the 6's opposite private". The 6's link letter opposite the big, m3, is already exact in h2, so I read
  this as the two apexes across the edges at m3: s_{j+2} and s_{j+3}. They are pinned by cons2 labels and unseen from M.
  M (sig2) is not refined in either h variant.
- **g_hf:** g2 with exact hat, fan, hat (n2..n4).

## 2. Controls

1. **No refinement.** The level-0 versions (y0, x0, h0, g0) go through the same machinery, with my key code and all rows
   pinned. Every column's rc equals lowerR2's rc exactly:
   - A78: 14 y, 12 x, 92 h, 53 g;
   - A83: 27 y, 30 x, 128 h, 68 g. My x0 lists 2 more keys whose in and out terms cancel inside a row, with rc 0.

   There are 0 negative uncapped columns, as lowerR2 says (VALID).
2. **Hand check** of the refined column y_ap key `(7,5,5,6,6 | hr 6, hl 7)` on A78, by `handcheck50.py`, which shares no
   code with the pricer.
   - **Receivers on root 7|5566.** From their labels:
     - 7766556/6567568 (w −24/421) has its five at w5 with hats (w0, w3) = (7, 6), so key …,6,7;
     - 7766556/6576576 (−4), 7665566/6675676 (−4) and 8665566/6765765 (−12) all give …,6,6. That is −20 in total.
   - **Senders 55667 with hl big.** Three rows have this:
     - 00010|11 (w 4);
     - 01010|10 (w 20);
     - 01010|11 (w 16).

     Their admissible exact (hr, hl) are {5,6} × {7,8,9}, so all 40/421 must land on keys …,hr,hl with hl ≥ 7. The only
     such key with receiver weight is (6, 7), at −24.
   - **The fourth sender,** 00100|01 (w 4), allows {5,6}², which fits the −20 on (6, 6).
   - **Result:** an excess of 40 − 24 = 16/421 is unavoidable. The pricer gives exactly rc = −16/421 on this key, with the
     same four rows as drivers.

## 3. Results

Columns:
- "refined cols" counts refined keys present in some completion of some cert row, with the old column count in brackets.
- "binder" counts negative keys whose ledger includes a receiverR2 row, with their Σ max(0, −rc).

### (a) A78 cert q42aA78L (44/421 = 0.104513, tco 1)

| refinement | refined cols | rc < 0 | most negative rc | Σ max(0,−rc)·cap at 0.05 / 0.1 / 0.3 | binder: n, Σ |
|---|---|---|---|---|---|
| y + both apex letters exact | 93 (14) | 6 | −16/421 = −0.0380 | 0.0074 / 0.0147 / 0.0442 | 2, 0.0475 |
| y + five's 5 hats exact | 1,464 (14) | 13 | −36/421 = −0.0855 | 0.0207 / 0.0413 / 0.1240 | 0, 0 |
| x sides + outer letters | 514 (12) | 4 | −24/421 = −0.0570 | 0.0114 / 0.0228 / 0.0684 | 4, 0.2280 |
| h2 apexes exact | 500 (92) | **0** | 0 | 0 / 0 / 0 (t* unchanged, exact) | 0 |
| h2 apexes exact + opposite-private apexes | 9,102 (92) | 62 | −84/421 = −0.1995 | 0.1430 / 0.2860 / 0.8580 | 0, 0 |
| g2 hats and fan exact | 336 (53) | 42 | −80/421 = −0.1900 | 0.1259 / 0.2518 / 0.7553 | 0, 0 |

x_out at its real cap 3: the split cert gives only D = −244/421. The cert therefore does not survive this refinement, and
cap 3 is far looser than the amounts x actually takes.

### (b) A83 fb-off nosep cert q44nfA83L (132/1301 = 0.101460)

| refinement | refined cols | rc < 0 | most negative rc | Σ max(0,−rc)·cap at 0.05 / 0.1 / 0.3 | binder: n, Σ |
|---|---|---|---|---|---|
| y + both apex letters exact | 215 (27) | 20 | −2232/29923 = −0.0746 | 0.0156 / 0.0312 / 0.0937 | 1, 0.0746 |
| y + five's 5 hats exact | 4,289 (27) | 31 | −4573/29923 = −0.1528 | 0.0218 / 0.0436 / 0.1308 | 0, 0 |
| x sides + outer letters | 888 (32) | 15 | −60/1301 = −0.0461 | 0.0101 / 0.0201 / 0.0603 | 15, 0.2010 |
| h2 apexes exact | 710 (128) | **0** | 0 | 0 / 0 / 0 (t* unchanged, exact) | 0 |
| h2 apexes exact + opposite-private apexes | 12,546 (128) | 91 | −3498/29923 = −0.1169 | 0.1044 / 0.2088 / 0.6263 | 0, 0 |
| g2 hats and fan exact | 468 (68) | 55 | −3498/29923 = −0.1169 | 0.1107 / 0.2215 / 0.6645 | 0, 0 |

x_out at cap 3: D = −15012/29923.

**Which labels pin what.** This is the same for both certs.
- **y_ap:** receiverR2 pins (rows 12/12 and 33/33). senderR2 never pins: classes only, so it is spread within class.
- **y_hats:** nothing pins. Senders are spread within class; receivers spread t_i always, and h1/h3 unless the neighbour
  is a five.
- **x_out:** receivers pin one outer letter per side. The other is pinned only at c = 5 sides.
- **h_ap and h_apf:** cons2 pins s exactly, but the relabel class lets any s′ with the same old row be used. mrowR2 never
  pins: its apexes are classes, and its far apexes are unseen.
- **g_hf:** cons2 pins (L is exact). Senders are spread.

### Top 10 negative refined keys and their drivers

Contributions are w·coef/tco; + means the row pushes rc down. R = receiverR2 (binder row), S = senderR2, C = cons2.

**A78**

| refinement | key | rc | driving rows |
|---|---|---|---|
| x_out | (8,7,(6,5,5,6,5),(6,7,6,6,5)) | −24/421 | R 8 76765656/66565565 (+0.0570, out-term) |
| x_out | (8,7,(6,5,5,5,6),(6,5,7,6,5)) | −24/421 | R 8 76567656/76675555 |
| x_out | (7,8,(6,5,5,5,6),(6,7,5,5,6)) | −24/421 | R 7 8677656/5566555 |
| x_out | (7,8,(6,5,5,6,5),(6,6,7,6,5)) | −24/421 | R 7 8665556/7675865 |
| y_ap | (7,5,5,6,6\|6,7) | −16/421 | S 55667 01010\|10 +0.0475, \|11 +0.0380, 00010\|11 +0.0095; R 7 7766556/6567568 −0.0570 |
| y_ap | (7,5,8,6,6\|5,5) | −16/421 | S 57668 00010\|11 |
| y_ap | (8,6,5,6,6\|7,5) | −12/421 | S 56686 10010\|000 |
| y_ap | (8,5,7,6,6\|6,7) | −4/421 | S 57668 00010\|11 +0.0380; R 8 76555566/66757666 −0.0285 |
| g_hf / h_apf | (6,5,5,7,8,7,7) etc. | −80/421, −84/421 | cons2 only: C 556587/777757, C 566588/555757, C 556697/775557 |

The y_hats top keys are all sender-only. The worst is (7,5,5,6,6 | 5,5,7,5,7) at −36/421, from S 55667 01010|10 and |11.

**A83**

| refinement | key | rc | driving rows |
|---|---|---|---|
| x_out | (7,7,(5,6,5,5,5),(6,6,7,9,6)) | −60/1301 | R 7 7667565/7966555 (top binder, w −0.0461) |
| x_out | (7,7,(5,5,6,5,5),(6,7,6,6,7)) | −60/1301 | R 7 7676655/6667656 (top binder) |
| x_out | (7,9,(6,5,5,5,6),(6,5,5,6,5)) | −426/29923 | R 7 9657656/5666555, R 7 9657656/5667555 |
| x_out | (9,7,(6,5,5,6,5),(6,5,5,6,5)) | −426/29923 | R 9 755676556/756556665 |
| x_out | (7,9,(5,7,5,5,5),(6,5,5,5,6)) | −288/29923 | R 7 9656775/5556655 +0.0239; R 9 755676556/756556665 −0.0142 |
| y_ap | (7,5,5,6,6\|6,6) | −2232/29923 | S 55667 01000\|11 +0.1404, 01000\|01 +0.0125; R 7 7665566/7765766 −0.0461, R 7 7665566/6675676 −0.0258, R 7 7665567/5765765 −0.0078 |
| y_ap | (7,6,5,6,7\|5,7) | −60/1301 | S 56776 10101\|00 |
| y_ap | (9,5,5,6,6\|5,5) | −852/29923 | S 55669 01000\|00 |
| y_ap | (7,5,5,9,7\|5,5), (7,7,5,5,9\|5,6) | −714/29923 | S 55779 00000\| |
| g_hf / h_apf | (5,7,8,5,6,5,5), (8,5,6,6,5,8,5,5,5,5), … | −3498/29923 | cons2 only: C 556587/555555, C 566588/555555, C 556697/775557 |

The y_hats worst is (7,5,5,6,6 | 5,5,7,6,5) at −0.1528, sender-only (S 55667 01000|11).

**Reading.**
- **x_out:** every negative column sits on a binder row, and on A83 the top two are two of the three heaviest binders (tied at w −60/1301). The
  two ends of one physical 6 side cannot agree on the outer letter. For example, on A78 the 6's private would have to be
  6, and its amask/R6 domain excludes 6. So the binder rows lose their x cancellation.
- **y_ap and y_hats:** these are almost entirely sender excess. Sender weight in a hat context that no cert receiver
  carries becomes free to collect. The amount usable is limited by receivers outside the cert, which a pricing cannot see.
- **g_hf and h_apf:** the large sums are purely cons2-against-cons2. Exact hats and fan (or far apexes) split the old g2/h2
  column across 6-types (e.g. 556587 vs 556597) that previously cancelled. No binder row is involved. Σ max(0, −rc)·cap
  at cap 0.05 already exceeds t* itself, so the linearisation is meaningless here. The real effect is bounded by the
  conservation rows at all other apex words, which carry zero dual and are not priced.

## 4. Verdict

1. **Not worth building:**
   - h2 with exact apexes gives exactly 0: the old certs stay valid, so t* is unchanged on both A78 and A83.
   - g2 with exact hats and fan, and h2 + opposite-private apexes, show large first-order numbers (Σ|rc| 2.1–2.9), but
     these come only from conservation rows decoupling 6-types. They touch no binder, so they are not a credible t-drop.
   - y + all five hats adds little over y + apexes, and none of it is on binders.
2. **The one widening worth building as a generic column family is x with outer (second-ring) side letters.**
   - Each end sees one outer letter, so it needs a max/min credit on the unseen one. That is an M-style mrow, as for h2/M.
   - It is the only refinement whose negative reduced costs all sit on binder rows: 4/4 on A78 and 15/15 on A83, Σ|rc|
     0.228 and 0.201.
   - y + both apex letters exact (zkey with exact letters) comes second: binder share 0.047 / 0.075.
3. **Honest first-order estimate of the t drop:**
   - x_out: about 0.010–0.011 at cap 0.05 and about 0.020–0.023 at cap 0.1;
   - y_ap: binder-only 0.002–0.004 at cap 0.05, and 0.007–0.016 for all columns, which is an upper envelope;
   - so roughly **0.01–0.02 in t** from x_out (+y_ap), against t* ≈ 0.10.

   These are first-order upper estimates, not bounds. With x at its real cap 3, the split cert's bound collapses below 0,
   so a re-solve is the only way to know the realised drop.

**Caveats.**
- The refined engine is assumed to use today's admissibility: sixes' non-R6 for senders, the 6-private amask, and no new
  R5 tests on exact hats.
- The spread is convex. A free-sign split of cons2 weights was tried for h and changed nothing.
- M is not refined in the h variants.
- Receiver relabel freedom was searched one slot at a time only.
