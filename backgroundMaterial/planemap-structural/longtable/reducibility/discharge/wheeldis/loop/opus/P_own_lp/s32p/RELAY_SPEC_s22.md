# RELAY_SPEC §22: signed five–big split Z± and reverse hat RR (stage 32 pricing, Opus s32p)

> **Status: design and pricing only. Nothing here is in the solver, and no solve was run.**
> Priced against s28q/eng/cert_s28A60L.json (lowerR2 VALID, t ≥ 47/320, registry 7360eb92, args s29/argsA60.txt, s28q engine flags
> `xon apexcls filt16 killtab=s29/f/kill/kill6 hat5 consall l3q`). Pricer: s32p/pricer32.py; log s32p/pricer32.log.

**Provenance.**
- **Z (five → adjacent big, split by the hat classes beside the big).** This is the shape of RSST's five-hub rules: drule1 plus
  its drule2/drule3 refinements, in Gonthier's `fourcolor` encoding, `theories/proof/discharge.v`. Those rules send from a degree-5
  hub to a big spoke, with conditions on the hub's other spokes and on the hats next to the receiving spoke (see the w3 → u and
  w4 → u rows of SolvingFrameworkPlan/docs/working/BORROWED-CHANNEL-7FACE.md, origin/main dc954db3).
  - Our key is the engine's stage-13 `zh` key, which keeps hat classes only, not RSST's exact ranges. The amounts are LP variables.
- **ZR (big → adjacent five, same key)** is our own column. RSST has no channel into a five ("a five never receives"). ZR is the
  signed half of the split.
- **RR (big hat → five across a diamond)** is our own §15r column (engine flag `hatrr`, stage 23). It is the reverse of the hat
  channel r of §15. It is not an RSST rule.

Everything in §1–§21 carries over unchanged: §1 scale (charge 6 − d), sender rows (outflow ≥ 1 − t), receiver rows
(load = inflow ≤ d − 6 + t), conservation and the mrow rows, l3q.

## 22.1 Z and ZR
**Key.** A five v is adjacent to a big b (letter B = min(deg b, 9)), and n = (B, n1, n2, n3, n4) is v's link read from b.
- hr = class (0 means ≤ 6, 1 means ≥ 7) of the hat between b and n1, i.e. the common neighbour of b and n1 other than v.
- hl = the class of the hat between n4 and b.
- `K = zkey(n, hr, hl) = min((B, n1, n2, n3, n4, hr, hl), (B, n4, n3, n2, n1, hl, hr))`. This is engine `prelay2.zkey`.

**Columns.** `z[K] ≥ 0` sends v → b. `zr[K] ≥ 0` sends b → v. Both have cap 3 and the x penalty under `keeppen`, like D and lq.

**Visibility at both ends**, exact at each row's resolution:
- **Sender row of v** (word w, hat classes H, fan classes Fn). For each j with w_j ≥ 7: n = (w_j, w_{j+1}, …, w_{j+4}),
  hr = H[j] and hl = H[j−1]. Under hat5 every hat class is enumerated, so H[j] and H[j−1] are always defined.
- **Receiver row of b** (centre, degree d, link w, apexes s). For each i with w_i = 5:
  n = (B, w_{i+1}, s_i, s_{i−1}, w_{i−1}), hr = c2(w_{i+2}) and hl = c2(w_{i−2}).
- **Physical test** (s32p/ztest32.py): explicit rotations of b with random mirror and offset, and v's link read off v's rotation.
  - 0 mismatches over 100,000 fives.
  - The broken control, where the receiver swaps hr and hl, gives 46,289 mismatches.

**Coefficients.** No other row type sees z or zr.

| row | z[K] | zr[K] |
|---|---|---|
| senderR2 of v (Σ out − Σ in + t ≥ 1) | +1 per big position j with key K | −1 per big position j with key K |
| receiverR2 of b (load − t ≤ d − 6) | +1 per five position i with key K | −1 per five position i with key K |

- Every row stays exact: the key is known at both ends. There is no mask, no signature variable and no mrow.
- z + zr on the same K is a free-sign correction to y[root(n)], split by (hr, hl).

**Separation (jsep window).**
- At a position with w_i = 5 the term `ZV[K] − ZRV[K]` depends only on (a, b, e, f, q, r) = (w_{i−2}, w_{i−1}, w_{i+1},
  w_{i+2}, s_{i−1}, s_i), so it fits the 9-slot window exactly. The engine adds ZV this way under `zh`; subtract ZRV in the
  same loop.
- The mode-2 class must separate (a, b, e, f, q, r) at c = 0. The `zh` branch of class_table_R2 already does this, so no new class
  is needed.
- No leaf correction is needed.

**lowerR2.** Rebuild z and zr coefficients from the row labels as above. A z or zr with rc < 0 is priced at its cap (3),
as x, D and lq are.

**upperR2.** Read z and zr from the solution, add `ZV − ZRV` to every window, and add `z − zr` to every sender row.

## 22.2 RR (reverse hat channel, §15r)
**Key.** The key is the §15 hat key, h5key, of the diamond (v, x, b, y): v is a five, x and y are consecutive spokes of v, and
b is the big hat across xy.
- The sender reads it as `h5_sender(w, H, Fn, k)`. The receiver reads it as
  `h5_recv(w_{i−1}, w_i, w_{i+1}, w_{i+2}, s_{i−1}, s_{i+1})` at an apex s_i = 5.
- These are the engine functions, unchanged.

**Column.** `rr[K] ≥ 0` sends b → v. It has cap 3 and the x penalty under `keeppen`. In the engine, flag `hatrr` leaves rr
uncapped, and lowerR2 has no rr branch: add one that prices rc < 0 at the cap.

| row | r[K] (existing) | rr[K] |
|---|---|---|
| senderR2 of v, at each big hat H[k] = 1 with key K | +1 | −1 |
| receiverR2 of b, at each apex s_i = 5 with key K | +1 | −1 |

- So rc(rr[K]) = −rc(r[K]) exactly, against any certificate.
- **Separation.** RR fits the hat5 window and class unchanged: the window adds `RV − RRV`, which the engine already does under
  `hatrr`.
- **Physical test** (engine `hat5_selftest` with hatrr, run by s32p/ztest32.py):
  - 0 mismatches over 100,000 diamonds, covering the key and the r/rr signs;
  - the broken control gives 15,898 mismatches.

## 22.3 Pricing against cert_s28A60L (exact, tco = 1)

| family | keys the cert touches | rc < 0 | most negative columns (rc) | cert rows they touch |
|---|---|---|---|---|
| Z | 26 | 8 | (8,5,5,6,6,0,0) −9/160; (8,5,6,6,6,0,1) −1/40; (8,6,5,6,6,0,1) −3/160; (8,5,8,6,6,0,1) −3/160; (8,5,6,8,5,0,0) −1/80 | senders 55668 (both bit rows), 56668, 56686, 58668, 56858; d8 75666556, 76656656 as payee |
| ZR | 26 | 8 | (8,5,5,6,6,0,1) −9/160; (8,5,6,6,6,1,0) −1/40; (8,5,8,6,6,0,0) −3/160; (8,6,6,6,6,0,1), (8,5,6,8,5,1,0), (8,6,5,6,6,1,0) −1/80 | d8 75666556, 86555665, 85566556, 85556655, 85656765, 76665656 as payer |
| RR | 11 | 3 | (5,0,6,5,0,6) −7/160; (5,0,6,8) −3/80; (5,0,6,5,0,8) −1/80 | d8 75666556, 85656765 (×2), 86555665 as payer |

- **Every negative column is centred on an 8** (B = 8, or an 8 hat). The rows they relieve are the d8 binders: 75666556 at
  −0.044 and the six d8 rows at −0.0125.
- **None of them touches a d7 row or the d10 row.** On the d7-with-8 rows (8658656/6665555, 8658656/6665556, 8568656/6655555),
  every candidate column with a nonzero coefficient there has rc ≥ 0. Most sit at exactly 0 (YR, Z/ZR on the 7's roots, VG,
  LG); O and O5F are positive.
- **Suspect C entry f7_..56757_...5....** It is a d = 7 pattern, so it only filters d = 7 receiver rows.
  - No negative column above touches a d = 7 row. Z and ZR are B = 8 keys. The RR keys are degree-free, but their cert payers are
    all d8.
  - Sender rows are not filtered by patterns.
  - Restoring rows that only that entry kills could add payer gain to RR (making it more negative), but it cannot remove the
    negativity.
  - The LG masks (mask32.py) never have that entry as their only killer.

## 22.4 Families priced and found ≥ 0 (kill line met for these)
- **YR**, big → adjacent five keyed on the five's root (the reverse of y): 16 keys, all at rc 0 (rc(YR) = −rc(y) = 0).
- **Family (a)**, the 8 → 5 adjacent channel keyed on the 8's exact letters near the five. The payee five reads w_{i±2} only as
  classes (it must credit the max), so the best composite of this family is ZR. It adds nothing beyond ZR.
- **Family (b)**, 8 → 5 at distance 2.
  - Across a diamond, this is RR (above).
  - Opposite across a 6-spoke, **O5** (big → five, pays only when the private mask is {5}): 3 keys, all rc > 0. **O5F** (five → big
    direct): 4 keys, rc ≥ 0.
  - Through a common 7 (link distance 3): neither end sees the other, so this is not a column under strict §14′.
- **Family (c)**, big–big.
  - x (existing): 12 keys, all at 0.
  - **D** (diamond apex): 3 keys at 0. **O** (opposite across a 6): 15 keys, all > 0.
  - **LG**, the l3q shape (drule9) generalised to any U, V ∈ {7, 8, 9} with key (U, V, c, a, a2) and payee mask. It was priced with
    no mask, with the win and full masks from mask32.py, and with and without the suspect entry. All 8 signatures have best
    composite rc exactly 0.
    - The masks only ever kill a2 = 5. The 7 → 8 payer keys out of the d7 rows have a2 ∈ {6, 8}.
- **Family (d)**, d8-centred, the 8 → adjacent fives keyed on the five's other neighbours: this is ZR at the visible resolution.
- **VG**, big → adjacent 6, relayed by the 6's h (the v6 key generalised to U = 7, 8, 9): 33 payer signatures, singles and
  pairs, min rc exactly 0.

## 22.5 Suggested next step (not done)
- Solve with `zh` + ZR + `hatrr` (all capped at 3, with keeppen) on 7360eb92, warm from rows_s28A60L. Kill line: a gain under
  0.005 against 47/320.
- Expect the gain, if there is any, to stop at the d7 and d10 rows: they price at 0 under every family here.
