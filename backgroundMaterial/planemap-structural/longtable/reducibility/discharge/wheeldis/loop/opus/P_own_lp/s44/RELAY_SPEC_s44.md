# RELAY_SPEC s44: fb, a face-keyed transfer out of the face big to its k-vertex neighbour (flag `fb`)

Opus, 20 Oct 2026. Written before any fb pricing or solve. This is a delta on s43 (`P_own_lp/s43/RELAY_SPEC_s43.md`) and
s40f. The engine copy is `P_own_lp/s44/eng`, which is s43/eng plus the patch `s44/port_fb.py`. With `fb` off it is s43/eng.
The cert class is FQ + `rpatN=s39o/rpatN3.txt`, with fy/fy2 off. Notation is §43's: u is a receiver of degree d with
U = min(d, 9), link w_0..w_{d−1}, and apexes s_i (the common neighbour of w_i, w_{i+1} other than u). Letters are 5..9,
and 9 means degree ≥ 9.

## 44.1 Which neighbour, and why only it

A face at u is i with w_i = w_{i+1} = s_i = 5 (§43.1). Its surrounding ring is (§20.1)
(u, w_{i+2}=k, s_{i+1}=e, t_i=k, s_{i−1}=e, w_{i−1}=k). Of these, only u and the two **k-vertices** w_{i−1} and w_{i+2} are
neighbours of u. The e-vertices s_{i±1} and t_i are not adjacent to u.

A transfer "out of the face big, keyed on the face" must be readable at the receiving end, so the receiver must see the
face. The neighbours of u that see the whole face (w_i, w_{i+1}, s_i) in their own 2-ball reading are exactly the
k-vertices. X = w_{i−1} reads w_i as a link vertex, w_{i+1} as its apex across (u, w_i), and s_i as its apex across
(w_i, s_{i−1}), which exists because w_i is a five (Lemma 44.1). Every other link vertex of u misses at least s_i.
- A big link neighbour that is not a k-vertex (w_0 and w_1 in 7766556/6567566) cannot read the face. A transfer to it
  keyed on the face would need a max-signature credit on the receiver (an upper bound over all u). That is §24-style,
  not this spec.
- **fb therefore has two directions, split by the receiver's letter:**
  - **fb6 ("7→6"):** u pays its k-vertex X when X is a 6. X's credit enters its 6-centred conservation rows (cons2), and
    X passes the charge on through its existing h outflows.
  - **fb7 ("7→7"):** u pays its k-vertex X when X is big (≥ 7). X's credit enters X's receiverR2 row.
- **In all 5 cert face rows both k-vertices are 6s:**
  - 7766556/*: w3 and w6;
  - 7665566/*: w2 and w5.

  So **fb7 has no coefficient in any face row**, and on these rows the kill line can only be carried by fb6. fb7 is
  built and priced anyway, as asked.
- **The payer** is the centre u of any receiverR2 row, of any degree. "A 7 on a face" is the case U = 7. Allowing any
  big payer only adds columns; the key carries U.

**Lemma 44.1 (the k-vertex's reading).** Let X = w_j be a link vertex of u, of any degree. X's rotation contains
u, w_{j+1}, s_j consecutively, and w_{j−1}, s_{j−1} on the other side of u. Let L be X's link with u = L_k, oriented so
L_{k+1} = w_{j+1}. Let t_m be X's apex across (L_m, L_{m+1}). Then:
- L_{k+1} = w_{j+1}, L_{k+2} = s_j, L_{k−1} = w_{j−1}, L_{k−2} = s_{j−1};
- t_k = w_{j+2} and t_{k−1} = w_{j−2};
- if w_{j+1} = 5, then t_{k+1} = s_{j+1}; if w_{j−1} = 5, then t_{k−2} = s_{j−2}.

Proof.
- (X, u, w_{j+1}) and (X, w_{j+1}, s_j) are faces, the second being u's apex face. So u, w_{j+1}, s_j are consecutive in
  X's rotation, and the mirror holds on the other side.
- The apex across (u, w_{j+1}) is their common neighbour other than X, which is w_{j+2} (u's rotation).
- If w_{j+1} is a five, its rotation is (u, w_{j+2}, s_{j+1}, s_j, X). The common neighbour of w_{j+1} and s_j other
  than X is s_{j+1}. □

When w_{j+1} ≥ 6, t_{k+1} is w_{j+1}'s private, which u does not read. That is why e is masked then.

## 44.2 Key

At u's link position j, with X = w_j, the two side tuples are

    T+ = (w_{j+1}, s_j, w_{j+2}, e+),   e+ = s_{j+1} if w_{j+1} = 5 else 0 (masked)
    T− = (w_{j−1}, s_{j−1}, w_{j−2}, e−), e− = s_{j−2} if w_{j−1} = 5 else 0
    σ  = (U, X, min(T+, T−), max(T+, T−))

These are the same slots as e87's side tuples (§24.1), except that e is masked unless the link neighbour is a five.

A side is a **face side** iff (c, b, e) = (5, 5, 5), with c the first entry, b the third and e the fourth. Equivalently,
(w_{j±1}, w_{j±2}, s_{j±1 or j−2}) is the face (w_{j+1}, w_{j+2}, s_{j+1}) at u, or its mirror.
- **The column fb[σ] ≥ 0 exists iff σ has at least one face side and X ≥ 6.** fb6 when X = 6, fb7 when X ≥ 7.
- Both faces at one k-vertex, which needs fives on both sides of X, give one key and one transfer per edge.
- Reflecting the embedding swaps T+ and T−, so σ is reflection-invariant.

**Both ends read σ exactly** (Lemma 44.1). u reads it from its 9-slot window at j: (a, b, c, e, f, p, q, r, s) =
(w_{j−2}, w_{j−1}, w_j, w_{j+1}, w_{j+2}, s_{j−2}, s_{j−1}, s_j, s_{j+1}). X reads it from its own row at u's position k:
- U = L_k;
- T+ = (L_{k+1}, L_{k+2}, t_k, t_{k+1} if L_{k+1} = 5);
- T− = (L_{k−1}, L_{k−2}, t_{k−1}, t_{k−2} if L_{k−1} = 5).

For a 6, its row is the cons2 row (L, s). For a big, its row is receiverR2 (L, t), read from X's 9-slot window at k.

## 44.3 Rows

| row | fb[σ] coefficient |
|---|---|
| receiverR2 of u (payer, any d) | −1 for each link position j with w_j ≥ 6 and σ(j) having a face side |
| receiverR2 of X (fb7 payee, any d) | +1 for each link position k with L_k ≥ 7, X ≥ 7, and the σ read at k having a face side |
| cons2 (L, s) of a 6 X (fb6 payee) | +1 (inflow, the same sign as g) for each k with L_k ≥ 7 and the σ read at k having a face side |
| senderR2, mrowR2, mrowL | 0 |

There are no mrow rows: both ends read the same exact key, so no max or min signature is needed.
- **Window (separator):** window slots (a, b, c, e, f, p, q, r, s) at position j of the centre's row, with centre letter
  U. Link vertices and apexes swap roles between the two ends: w_{j+2} is u's link vertex but X's apex, and s_j is u's
  apex but X's link vertex. So the two readings of one physical tuple use different slots:
  - **payer term** (the centre pays c, when c ≥ 6): T+ = (e, r, f, s if e = 5 else 0), T− = (b, q, a, p if b = 5 else 0),
    key (U, c, T±). W −= fb[key] if a side is a face side.
  - **payee term** (the centre is X ≥ 7, receiving from c ≥ 7): T+ = (e, f, r, s if e = 5 else 0),
    T− = (b, a, q, p if b = 5 else 0), key (c, U, T±). W += fb[key] if a side is a face side.

  Both terms are window-local, so jsep3/5/6 are unchanged and separation stays exact.
  - Tail d ≥ 18: relaxed DP/Karp on W9, as before.
  - cons2 (6 X, link L, apex word s, u = L_k): T+ = (L_{k+1}, L_{k+2}, s_k, s_{k+1} if L_{k+1} = 5),
    T− = (L_{k−1}, L_{k−2}, s_{k−1}, s_{k−2} if L_{k−1} = 5).
- **Mode-2 class:** this is unchanged. At c ≥ 2 the class does not separate p and s, so two rows can share a signature
  and differ in fb. As with fy2, this affects only which K rows one iteration returns, never exhaustiveness.
- **cons2 separation (`cons2_delta`) and the upperR2 conservation check:** + fb[σ] at every k with L_k ≥ 7, evaluated
  over all 5^6 apex words via a 5^4 table in (t_k, t_{k−1}, t_{k+1}, t_{k−2}). cons2_coef carries the same term, so
  lowerR2 re-derives it from the label.
- **Bounds:** fb is uncapped in the LP family. The cap `fbcap` is optional, default none. Under keeppen it carries the
  x penalty, like lq.
- **Sub-flags:** `fbdir=6`, `fbdir=7` or `fbdir=67` (default 67) restrict the family.
- **Sol JSON:** carries 'fb': [[σ, value], ...]. upperR2 refuses fb values without the flag.

## 44.4 Soundness

1. **Rule.** "A vertex u of degree ≥ 7 sends fb[σ] to each neighbour X of degree ≥ 6 at which σ(u, X) has a face side."
   σ is a function of the triangulation: the degrees of u, X, the two common neighbours w_{j±1} of u and X, the apexes
   s_j and s_{j−1}, the next link vertices w_{j±2}, and, when w_{j±1} is a five, s_{j+1} or s_{j−2}.
   - By Lemma 44.1, X reads the same vertices at the same tuple positions.
   - The orientation is fixed by the canonical min, which is the same at both ends.
   So each transfer has one amount, counted −1 in u's row and +1 in X's row.
2. **Coverage.** u's real 2-ball is an admissible receiver row (exhaustive for d ≤ 17, relaxed tail beyond), so its
   payment is in its row. X's real 2-ball is:
   - for a 6, a cons2 arrangement (L, s), and cons2 holds for every non-R6 L and every apex word (upperR2 checks all 5^6);
   - for a big, a receiver row.
   So the inflow is counted.
3. **The 6 stays at 0.** cons2 is the equality Σ g + Σ fb − Σ h (− the other families' terms) = 0, so the 6 ends at
   charge 0 whatever it receives. No new row type is needed.
4. **Exact letters.** Letters are the engine's (9 means ≥ 9) at both ends. U = 9 in the key means deg u ≥ 9 for both.

## 44.5 Relation to l3q, e87, x, v6, fy (nothing is double counted)

Columns of different families on the same edge are separate transfers, each counted once at each end. "Not double
counting" here means fb is not one of these columns renamed. Each comparison below shows that.

- **l3q (RSST rule 9, `l3q`):** a 7 pays an adjacent **7** v. It is keyed on the payer's link going away from v,
  (c, a, a2) = (w_{i±1}, w_{i±2}, w_{i±3}) with c, a ≤ 6, and the payee is credited by a masked Q. It is d = 7 rows only.
  fb pays a **k-vertex of a face** (a 6, or a big), keyed on the face. The payee is exact and any degree is allowed. l3q
  never reads s_{j±1}, and its payee is never a 6.
- **e87 (§24, s38e; designed, never built):** a big of degree **≥ 8** pays an adjacent **7**. The key is the same side
  tuples, with e unmasked at the payer and a masked completion at the payee. Its payer and payee letters differ from fb7's
  in general. fb has no face-free columns and masks e unless c = 5, so the payee needs no mask. e87 is not in any engine.
- **x (`xon`, L2 tau):** big ↔ big keyed on (fl, tl, side(c, a, b) ±), without e. fb7 is at a finer resolution (with e
  at a five) and exists only on face sides. It is a separate column, like zh beside y. x never pays a 6.
- **v6 (stage 15, not in FQ):** a 6 next to a 7 *receives* v keyed on the 6's whole link at u (including its private p)
  and the apex classes beside u. The 7 pays the min-signature V, since it cannot read p. v6 never reads s_{j+1} or s_{j−2},
  so it cannot see the face. fb6 drops p (u cannot read it) and adds the face apex, with an exact key at both ends.
- **fy/fy2 (z):** five → big. fb's payer is the big, and its payee is never a five.

## 44.6 Pricing against cert_q39n3A74L (step 3; `s44/pricer44.py`)

fb adds columns only: no row is split, and none is added. So the cert stays valid iff every fb column has
rc = −(Σ_rows w · coef) / tco ≥ 0, summed over the cert's receiverR2 and cons2 rows. This is exact; there is no lifting.
- It is priced with the engine's own lowerR2 (flag `fb`, with `fbdir=6`, `7` and `67`), printing every negative column.
- For each negative column it lists the cert rows it touches.
- **Kill line:** some column with rc < 0 has a nonzero coefficient in one of the 5 face rows.
- **Gain:** first-order, Σ max(0, −rc)·cap at caps 0.05 and 0.1, both for all columns and for the face-row columns only.

## 44.7 Results (written after the runs; the spec above was committed first, def18bc8)

**Engine.** `s44/eng` = `s43/eng` + `s44/port_fb.py`. md5s are in `s44/engine_src_md5.txt`. jsep binaries are unchanged
from s43.

**Control (a): fb off, A74.**
- lowerR2 on cert_q39n3A74L: **VALID 20/183**, log byte-identical to `s39o/run_n3_A74/lower.log`.
- upperR2 nomax on sol_q39n3A74: **FEASIBLE 1/9**, identical modulo timings (`ctl_*_off.log`).

**Control (b).**
- **`phys44.py` (`phys44.log`):** explicit rotation systems. The independent key is read from vertex identities, as
  common neighbours from every rotation that holds the pair, and compared with the engine's payer key (u's row, random
  orientation) and payee key (X's own row, random orientation, plus cons2_coef for a 6).
  - **167,586 (u, X) pairs, 63,518 with a face side (31,761 six payees, 31,757 big payees): 0 mismatches.**
  - Broken control (payee read with the payer's slot map): 58,051 of 63,518 mismatch.
- **`sepfb44chk.py` (`sepfb44chk.log`):** with random fb values, the window terms (separator output at d = 7, 8, 9, and
  random rows summed over the window) were checked against recv_coef_R2, **6,312 rows, 0 mismatches**. cons2_delta was
  checked against cons2_coef, **198,800 (L, s), 0 mismatches**.

**Pricing (`pricer44.py`; `pricer44_6.out`, `pricer44_7.out`, `pricer44_67.out`; exact via the engine's lowerR2, with no
row split).**
- **fb7 (fbdir=7): no fb7 key occurs in any cert row**: no rc < 0 and nothing touches a face row. Every face row's
  k-vertices are 6s.
- **fb6 (fbdir=6) and both together (fbdir=67) are identical:** 8 negative columns, 4 of them on face rows.
  **KILL LINE PASSED by fb6.**

  | fb6 key σ = (U, X, T_min, T_max) | rc | cert rows |
  |---|---|---|
  | (7,6, 5655, 7670) | **−18/183** | 7766556/6567566 (face) |
  | (7,6, 5755, 6670) | **−10/183** | 7766556/6567566, 7665566/6675676 (face); cons2 576667/575575 (w −5/183, ×2) |
  | (7,6, 5755, 7670) | **−10/183** | 7766556/6566576, 7766556/6576576 (face); cons2 577677/577775 (w −1/61, ×2) |
  | (7,6, 5755, 6770) | −1/183 | 7665566/6775676 (face); cons2 576767/577775 |
  | (9,6, 5655, 7550) | −8/183 | cons2 only (556597, 567579 ×2) |
  | (8,6, 5655, 7550) | −4/183 | cons2 556587/555555 |
  | (9,6, 5655, 9550) | −2/183 | cons2 566599/555555 |
  | (7,6, 5555, 9670) | −2/183 | cons2 556697/555775 |

  All 5 face rows carry at least one negative column. 7766556/6567566 carries two (−18/183 and −10/183).
- **First-order gain Σ max(0, −rc)·cap:**

  | cap | all fb6 columns | face-row columns only |
  |---|---|---|
  | 0.05 | 0.0150 | 0.0107 |
  | 0.1 | 0.0301 | 0.0213 |

  These are dual-side estimates at the current cert, not a new bound.

**Step 4: no solve was run.** As asked, it is reported first.

## 44.8 lowerR2 INVALID on cert_q44fbA78L: float noise, and an exact repair (s44 cont.)

**Why it failed.** `lowerR2` on the A78 fb6 nosep cert (1118 rows: 70 senderR2, 884 cons2, 100 mrowR2, 16 mrowL, 48 receiverR2)
found 87 uncapped columns with negative reduced cost, all g (45) and h (42), the worst −5.6e−13, total 5.8e−12.
- **fb was not the cause.** No fb column is negative. fb is priced at cap 3 (both ends: payer −1 in u's receiver row, payee +1 in the 6's cons2 row).
  The check and the solve build cons2 from the same `cons2_coef`.
- **The dual is clean.** LP status Optimal, t* = 0.093306161292. The bound before the noise was 0.093306161289.
- **The cause is rational recovery.** Each weight is rationalised on its own (`limit_denominator(1e7)`). On 884 free cons2 rows this leaves residuals around 1e−13 on reduced costs that are 0 in the LP. Taking the floats exactly (wden 1e12, 1e18) does not help: residuals of 1e−14 remain, spread over g, h, r, y and M.
- The receiverR2 count (48) and the weight on 7766556/6567566 in the report are just the cert's rows and weights. They are not failures.
- Earlier certs (s42a, 155 rows, few cons2 rows) never had enough free rows to show this.

**Fix (engine s44/eng/prelay2.py, `port_repair.py`).** The check itself is unchanged: rows are re-derived from labels, signs are enforced, capped families are priced at cap, and any negative uncapped column makes the cert INVALID. Two additions:
1. A weight given as the string "p/q" is taken exactly. Float weights are rationalised as before.
2. **Repair.** It runs only when nothing else failed and every negative column is uncapped with |rc| ≤ reptol (default 1e−9).
   - Only free cons2 weights and strictly negative mrow* weights move. Those touch neither t's coefficient nor D.
   - An exact sparse rational solve sets the negative columns' reduced cost to exactly 0. Columns pushed negative by a round are added in the next round.
   - The solve is refused if a weight would move by more than repmax (1e−6) or an mrow weight would change sign.
   - The repaired cert is written next to the input as `*_rep.json`, with exact string weights. The full check then reruns from that file with `norepair`.
   - The final `LOWER-R2:` line is the verdict on that file. The first pass is labelled `(unrepaired)`.
   - Soundness rests only on the unchanged checker applied to the written file. The repair never decides validity.

**Results.**

| cert | before | repair | after |
|---|---|---|---|
| A78 cert_q44fbA78L | INVALID, 87 g/h, worst −5.6e−13 | 9 rounds, 379 columns pinned, 342 weights moved by ≤ 6.6e−13 | **VALID t ≥ 0.093306161279** (exact, denominator 137 digits) |
| control G: own nosep solve, fb6 cap 3, warm = the 48 receiver rows of that cert (reg_A78) | INVALID, 91 g/h, all noise | 9 rounds, ≤ 7.0e−12 | **VALID 0.093306161** (1049 rows) |
| control M2: same solve, payer sign flipped in the solve only (eng_mis2), fb uncapped | INVALID, 93 columns, fb down to −0.194 | refused (beyond reptol) | **INVALID** (inflated LP t* 0.093350740 > true 0.093306161) |
| control M: cons2 inflow sign flipped in the solve only (eng_mis), fb uncapped | VALID −5/7 | none | VALID −0.714 |
| control (a) rerun: fb off, A74 n3 cert | VALID 20/183 | none | log byte-identical to s39o |

- Control M is a weak bound, but a genuine one. The mis-signed LP is looser than the true LP (t* −5/7), so its dual stays feasible in the true LP and the exact check accepts it. M2 is the mis-signing that inflates t, and the check rejects it.
- The A78 nosep lower bound 0.0933061613 sits below the keeppen upper bound 0.109439356774. The nosep LP covers only the warm rows.
- A83 (`run44c.sh`) runs `pcheck.py lowerR2` from s44/eng in its L stage, which had not started when this was patched, so it picks the repair up. Its repaired cert lands at s44/eng/cert_q44fbA83L_rep.json.
