# RELAY_SPEC s45: l3q extended to payees of degree 8 and 9 (option `l3qV=7,8,9`)

Opus, 21 Oct 2026. Written before any pricing. This is a delta on §21 (`P_own_lp/s28q/RELAY_SPEC_s21.md`), which is the
**V = 7** subfamily. Everything in §21 holds unchanged for V = 7. The engine copy is `P_own_lp/s45/eng` (s44/eng plus this
option). With the default `l3qV=7` it is s44/eng.

> **Provenance.** This is not an original rule.
> - **RSST rule 9** (Robertson, Sanders, Seymour and Thomas 1997; Gonthier's `drule9`) is
>   `Part $ 6- $ 6- $ 7+ $ * $ * $ * $ 5 $` at a hub of degree 7. Its payee letter is **7+**, so rule 9 already pays a link
>   neighbour of any degree ≥ 7. §21 restated only the 7 → 7 part. §45 adds the 7 → 8 and 7 → 9+ parts of the same channel.
> - **The 2026 set's rule:** the published-rules probe (`pubrules/FINDINGS_2026-10-21.md`, `REPORT_A78_A74.md`; a map, not a
>   claim) reports that on the face rows r58c = 7 8665556/7675865 and r58g = 7 8665566/6765765, both RSST and the 2026 rules
>   have the face 7 pay its link 8 (0.2–0.4 units). **Which 2026 rule it is (by name/number) is not recorded here yet.** The
>   shared folder returned I/O errors for the whole session, so the probe notes could not be read. A later commit will add
>   the name. Until then, l3qV numbers cite RSST rule 9 as the source.
> - The amounts are LP variables. The key, mask and credit are §21's own construction, unchanged except that V is in the key.
>   Any claim citing an l3qV number must name RSST rule 9 / drule9 (and the 2026 rule, once named) as the source.

## 45.1 Transfer
- A vertex u of degree exactly 7 sends `q[κ] ≥ 0` to each link neighbour v = w_i with letter V(v) ∈ `l3qV`, once per side σ.
  Here V = 8 means deg v = 8 exactly, and V = 9 means deg v ≥ 9 (the engine's letter 9).
- **Key.**
  - V = 7: `κ = (c, a, a2)`, stored as §21. It is byte-identical, so every old cert, row file and sol keeps its meaning.
  - V ∈ {8, 9}: `κ = (V, c, a, a2)`, where (c, a, a2) = (w_{i+σ}, w_{i+2σ}, w_{i+3σ}) in u's link, read as in §21.1.
  - The family is c, a ∈ {5, 6} and a2 ∈ 5..9, so **20 new columns per new V** (40 for 8, 9).
  - The sides are separate transfers, with no reflection min (§21.1). Cap `lqcap`, and the keeppen penalty, are as for V = 7.
- **Payee credit Q.** For V = 7 it is `lQ[(c, a, m)]` as §21. For V ∈ {8, 9} it is `lQ[(V, c, a, m)]`, with m the 5-bit mask
  of a2 letters from the **V-table** (§45.3).

## 45.2 Rows

| row | lq[(V, c, a, a2)], V ≥ 8 | lQ[(V, c, a, m)], V ≥ 8 |
|---|---|---|
| receiverR2, d = 7 (payer u) | −1 for each link position i with w_i = V and side σ with key (c, a, a2), c, a ≤ 6 | — |
| receiverR2, min(d, 9) = V (payee v) | — | +1 for each link 7 w_j and side σ with c = w_{j+σ}, a = apex across (w_j, w_{j+σ}) (s_j for +, s_{j−1} for −), both ≤ 6, m = T_V(σ, c, w_{j+2σ}, w_{j+3σ}, w_{j+4σ}, a, o) |
| mrowL, ≤ 0, dual ≤ 0, label `['mrowL', [V, c, a, m], [V, c, a, a2]]` | +1 | −1, for every a2 ∈ m |
| senderR2, cons2, mrowR2, mrowV, mrowQ | 0 | 0 |

- **What changes for V = 8.** New payer terms in d = 7 rows at every link 8. New payee terms in d = 8 rows: §21 left d = 8
  rows untouched, and they now credit Q at their link 7s. Indices are taken mod d = 8, so w_{j+4σ} = w_{j−4σ} (the antipode).
- **What changes for V = 9.** New payer terms in d = 7 rows at every link 9. New payee terms in every d ≥ 9 row, including
  the relaxed tail d ≥ 18, at their link 7s. Indices are mod d, and w_{j+4σ} is a distinct vertex.
- **Unchanged:** the V = 7 terms in d = 7 rows (both ends), and o = u's other apex (s_{j−1} for σ = +, s_j for σ = −).
- **Qeff** (the value of Q in the extended solution): `max(LP value, max_{a2 ∈ m} q[(V, c, a, a2)])` per V. This holds every
  mrowL row, as in §21.3.

## 45.3 Mask table T_V (strict, as §21.4)
- This is §21.4's window and strict rule, with the payee centre's degree and link length changed:
  - **V = 8:** link length D = 8, centre degree exactly 8.
  - **V = 9:** link length D = 9, centre degree 99 (never exact, the engine's rule for letter 9). An embedding may not use the
    centre v.
  - Every other window vertex is as §21.4. Known: u = w_0 (7), c, w2, w3, w4, a, o. Free: a2. Unknown (99, strict): all others.
- **A letter is killed** only by an embedding that *uses a2* (§21.4 reading (A)). This is unchanged.
- **Why one table serves all d ≥ 9 (V = 9).** The kill embeddings use only {u, c, w2, w3, w4, a, o, a2}, and v is excluded.
  The induced subgraph on these vertices, and the faces among them, do not depend on d once d ≥ 9 (w4 = w_{j+4σ} is then
  never adjacent to w_{j−σ}...w_{j−3σ}). So an embedding found at D = 9 exists at every d ≥ 9, and the mask is sound for
  the whole letter class.
- **Builder:** `s45/l3qtabV.py` (§21's `l3qtab.py` with D and the centre degree as parameters; V = 7 reproduces it). It writes
  `tabV{8,9}_{1,-1}.json` with the same key format. A `keys=` option builds only the masks a given row set needs, for exact
  pricing. Every mask a cert row uses is then checked against the full table when that exists.

## 45.4 Soundness
1. **Both ends read the same key.** §21.5's argument never uses deg v.
   - c is the common neighbour of u and v on the σ side.
   - a is the third vertex of the face (u, c, ·) other than v, i.e. v's apex across (u, c).
   - a2 is u's link vertex after a, moving away from c, i.e. v's private of u adjacent to a.
   - V is v's letter, which u reads exactly (8 exact, 9 meaning ≥ 9 at both ends).
   So each transfer is −q at u's d = 7 row and is covered by +Q[(V, c, a, m)] at v's row, provided a2 ∈ m.
2. **a2 ∈ m.** A letter is removed from m only if an embedding of a forbidden (reducible) configuration uses the vertex
   a2 at that letter, plus known vertices at their exact degrees. In a minimal counterexample that letter cannot occur.
   Q ≥ q[(V, c, a, a2)] for all a2 ∈ m (mrowL / Qeff), so v's credit is at least its true inflow.
3. **Coverage.** u's real 2-ball is a d = 7 receiver row, so its payment is in that row. v's real 2-ball is a receiver row of
   degree d with min(d, 9) = V, so the credit is in that row.
4. **No double counting with §21.** The V = 7 keys are 3-tuples and the V ≥ 8 keys are 4-tuples with V first, so the families
   are disjoint. Every physical (u, v, σ) transfer is in exactly one family, chosen by deg v.

## 45.5 Engine scope (this round: pricing only)
- `l3qV=7,8,9` (any set containing 7), `l3qtab8=…,…`, `l3qtab9=…,…`.
- Built: the row coefficients (`recv_coef_R2`), mrowL generation and the lowerR2 checks for V ≥ 8 rows.
- **Not built:** separation and upper checks for V ≥ 8. jsep's window term at a link 8/9 of a d = 7 row, and the payee leaf
  correction at d = 8/9, are missing. `solveR2` and `upperR2` therefore **refuse** l3qV ≠ 7 (exit 7). No V ≥ 8 number can
  come from a solve until those are built.
- **Default l3qV=7:** the code path is identical to s44/eng. Control: lowerR2 VALID 44/421 on `s42a/run_A78/cert_q42aA78L.json`.

## 45.6 Pricing (step 3)
- The new columns are added and no row is changed, so the cert's dual prices them exactly: rc = −(Σ_rows w·coef)/tco.
- **lq (V ≥ 8):** it touches only d = 7 receiverR2 rows (w ≤ 0, coef −1), so rc ≤ 0.
- **lQ (V ≥ 8):** it touches d = 8 / d ≥ 9 rows (coef +1), so rc ≥ 0.
- **Bundle price.** The cert has no V ≥ 8 mrowL rows (dual 0). Raising q forces Qeff up on every mask that contains a2. The
  *bundle* rc is rc(lq κ) + Σ_{lQ keys (V, c, a, m) in cert rows, a2 ∈ m} rc(lQ). It is reported beside the raw rc, and the
  bundle is the honest first-order number.
- **Gain:** first-order Σ max(0, −rc)·cap at caps 0.05 and 0.1, both raw and bundle.
- **Compared with fb6** on the same cert (`s44/pricer44_q42a.out`): fb6 (7,6,5755,6680) is −36/421, touching r58c and r58g.
