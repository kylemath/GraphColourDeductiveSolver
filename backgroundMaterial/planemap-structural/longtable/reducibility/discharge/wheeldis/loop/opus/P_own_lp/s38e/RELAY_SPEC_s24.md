# RELAY_SPEC §24: e87, a big pays an adjacent 7, keyed on the 8's whole second neighbourhood around the edge (Opus s38e)

> **Status: design and pricing only. Nothing here is in the solver, and no solve was run.**
> Priced against s28q/eng/cert_s28A62L.json. That cert is lowerR2 VALID at t ≥ 11/75 on registry 3cfd7f18, args s31/argsA62.txt,
> with the s28q engine flags of cmd_s28.sh REG=A62:
> `xon apexcls filt16 killtab=s31/f/kill/kill6 hat5 consall l3q l3qtab=s28q/tab62_±1.json lqcap=3 xcap=3`.
> Files: pricer s38e/pricer38.py, log s38e/pricer38.log, rc values s38e/rc38.json; masks s38e/mask38.py → masks38.json and mask38.log.
>
> **Provenance.** This is the channel of Steinberger's second discharging stage (R. Steinberger, arXiv:0905.0043, §4): an
> overcharged major pays an adjacent major, and every rule vertex lies within distance 2 of both source and sink. The cap of 1/2
> per column comes from his Lemma 4.4, which bounds the amount a 7 sends to a neighbour of degree ≥ 8; here we use the same
> bound for the reverse direction. The key, the mask and the LP amounts are our own (source: Long Table,
> SolvingFrameworkPlan/docs/working/LIT-DEG7-LEMMAS.md, origin/main 7cd4c080).

Everything in §1–§23 carries over unchanged. The existing x column `tau(U, 7, side(c, a, b)±)` is this channel at the E1
resolution below, with cap 3; it stays as it is.

## 24.1 Transfer and key
- **Payer** u is the centre of a receiverR2 row of degree d ≥ 8, with U = min(d, 9). **Payee** v = w_i is a link vertex of degree
  exactly 7. There is one transfer per edge, not one per side.
- **Side tuples**, read in u's row (link w, apexes s, with s_k the apex across (w_k, w_{k+1})):
  - side + : (c, a, b, e) = (w_{i+1}, w_{i+2}, s_i, s_{i+1});
  - side − : (c, a, b, e) = (w_{i−1}, w_{i−2}, s_{i−1}, s_{i−2}).
  - Together these are all of u's link letters and apexes within distance 2 of v: the 9-slot window at position i.
- **Key:** `K = (U, 7, min(T+, T−), max(T+, T−))`. Reflecting the embedding swaps the two sides, so this key is reflection-invariant.
- **Column:** `e87[K]`, with 0 ≤ e87 ≤ 1/2 (the cap is the flag `e87cap`, default 1/2). Under `keeppen` it carries the x penalty.

## 24.2 Payee reading and mask (strict §14′)
- v is the centre of a d = 7 receiverR2 row (L, t), and u = L_j has letter 8 or 9 (9 is never exact).
- v reads the following exactly:
  - side +: c = L_{j+1}, a = t_j, b = L_{j+2};
  - side −: c = L_{j−1}, a = t_{j−1}, b = L_{j−2}.
- **e** (u's apex beyond c) is c's private adjacent to a. One exception: when c = 5 it is exact, with e = t_{j+1} on side + and
  t_{j−2} on side −, because a degree-5 c has no private.
- **Free slots:** the e of every side with c ≥ 6, so at most 2 slots.
- **Mask:** the allowed completions are those not killed, under these rules:
  - every other private is unknown (degree 99), and an embedding that touches one is no match;
  - letter 9 is never exact, so a requirement of 9 never kills;
  - only an embedding that uses at least one free slot kills;
  - a kill is a partial assignment, and it removes every completion that extends it.
- **Containment:** k42 `grow.embeddings`.
- **Forbidden set:** ex62 + s31/k3x_{D,C}_3cfd7f18, which is 3,989 configurations.
- **Two variants of the known set:**
  - **win:** v, u, c±, L_{j±2}, t_{j−2..j+1}. This is exactly the payee's 9-slot window at j, so the payee term is a window function.
  - **full:** the whole d = 7 row. This is valid only at the jsep5 leaf, where the row is complete.
- **Payee credit:** `+1 · E87Q[(σ, m)]`, where σ is the exact part and m is the set of allowed keys (equivalently, a bitmask over the
  ≤ 25 completions). In the extended solution its value is `Qeff(σ, m) = max(LP value, max_{K ∈ m} e87[K])`, as in §21.3.

## 24.3 Row coefficients

| row | e87[K] | E87Q[(σ, m)] |
|---|---|---|
| receiverR2, d ≥ 8 (payer centre u) | −1 for each link position i with w_i = 7 and key K | — |
| receiverR2, d = 7 (payee centre v) | — | +1 for each link position j with L_j ≥ 8 whose exact part is σ and mask is m |
| **mrowE** (new, ≤ 0, dual ≤ 0) | +1 | −1: `e87[K] − E87Q[(σ, m)] ≤ 0` for every K ∈ m |
| senderR2, cons2, mrowR2, mrowV, mrowQ, mrowL | 0 | 0 |

- A d = 7 row with an 8 in its link is a payee only. A d = 8 row is a payer only (V = 7 subfamily), and so is any d ≥ 9 row.
- **Separation, payer:** the term −e87[K] reads (w_{i±1}, w_{i±2}, s_{i−2..i+1}), which is the 9-slot window at a 7.
  - The mode-2 class must separate all 8 window letters at a link 7 for d ≥ 8. Today it separates only (b, e, q, r) there.
  - That means a class split; fold a K id into the class, as the DD branch does.
  - The term is ≤ 0, so leaving it out of the d ≥ 18 tail bound is sound.
- **Separation, payee (win masks):** at a link letter ≥ 8 in a d = 7 row, add `Qeff(σ, m_win(window))`. This is a pure window
  function, so no leaf correction is needed.
  - Compute masks lazily: only windows whose σ matches the exact part of some e87 with value > 0 need a mask, because Qeff = 0
    otherwise.
- **Separation, payee (full masks):** the window adds UB(σ) = max_m Qeff. The leaf adds `Qeff(σ, m_full(row)) − UB(σ) ≤ 0`, as in
  §21.6. This needs a new jsep5 input with the per-row masks.
- **lowerR2:**
  - rebuild the e87 and E87Q coefficients from the row labels as above;
  - check each mrowE row: σ canonical, K ∈ m, and w ≤ 0;
  - an e87 with rc < 0 is priced at its cap, `D += rc · 1/2`;
  - an E87Q with rc < 0 makes the certificate invalid.
- **upperR2:** read e87 and E87Q from the solution, apply Qeff, add the payer and payee window terms, and add the leaf
  correction if full masks are used. Every other d is unchanged.
- **Optional Lemma 4.4 guard (not priced):** per big–7 edge, Σ x(U→7) + e87 ≤ 1/2. Its dual can only lower the bound, so this is a
  check row, not a gain.

## 24.4 Pricing against cert_s28A62L (exact; tco = 1)

| family | variant | payer keys | payee items | rc < 0 (singles) | best composite | composite keys |
|---|---|---|---|---|---|---|
| E1 (= x, exact) | — | 5 | 7 | 0 | 0 | — |
| **E2** | full | 6 | 7 | 3 at −1/75 | **−1/25** | the 3 below |
| **E2** | win | 6 | 7 | 2 at −1/75 | **−2/75** | K1, K3 |
| E2 | no mask | 6 | 7 | 0 | 0 | — |
| E3 = E2 + a2 = w_{i±3} | full / win / none | 6 | 7 | 3 / 2 / 0 | −1/25 / −2/75 / 0 | same as E2: a2 adds nothing |
| LG8 (l3q shape, U = 8, V = 7, letters 5..9) | full / win / none | 6 | 14 | 0 | 0 | — |

- **K1 = (8, 7, (5,6,6,6), (6,5,5,6)).**
  - Payer: d8 **75666556/66666565** at w0 (dual −1/15, gain 1/15).
  - Payees: d7 8658656/6665556 at w3 and d7 8658656/7665555 at w3 (−2/75 each).
  - The third E1 payee, d7 8556856/7565666 at w4, drops out: it has e− = 6, and rsst006_2o7566 kills that in both variants.
  - rc −1/75.
- **K2 = (8, 7, (5,7,5,5), (6,5,6,6)).**
  - Payer: d8 76556675/66665555 at w0 (gain 1/75).
  - Its only E1 payee, d7 **8666655/5677657** at w0 (the face binder), drops out with full masks only: e+ ∈ {5, 6} is killed by
    rsst101_126o25866 and rsst109_126o36666.
  - rc −1/75 with full masks, 0 with win masks.
- **K3 = (8, 7, (6,5,5,5), (6,7,5,5)).**
  - Payer: d8 76765656/55556665 at w2 (gain 1/75). It has no payee in the cert, though its E1 key had d7 8658656/7665555 at w0.
  - rc −1/75.
- **Rows touched.** Payers: the d8 binders 75666556 (−1/15), 76556675 (−1/75) and 76765656 (−1/75). Costs: the d7 rows
  8658656/6665556 and 8658656/7665555. d8 76656566 has its own E2 key at rc 0, and the d10 row 6565656565 is untouched.
- **Payer degree.** "Payer any degree ≥ 8" gives the same result on this cert as "payer exactly 8" (pricer38_u8only.log): no
  d ≥ 9 cert row has a link 7, and no d7 cert row has a 9.
- **First-order projection at cap 1/2:** the full composite moves lowerR2 by −1/25 · 1/2 = −0.020, and the win composite by
  −2/75 · 1/2 = −0.0133.
  - Two of the three keys gain only because their payee rows are not in the cert yet. A re-solve will generate them: d7 rows with an
    8 whose e on that side is not killed.
  - So expect much less than the projection.
- **Kill line** (every key rc ≥ 0): **not met for E2 or E3.** It is met for LG8, E1 and every unmasked variant.

## 24.5 Controls (pricer38.log)
- **Flag-off reproduction:** the pricer's own rebuild gives Dn/tco = 11/75. No capped column has rc < 0, and no other rc < 0.
  The engine's lowerR2 on the same cert gives VALID t ≥ 11/75 (s38e/lower_flagoff.log).
- **E1 against the engine's x:** every E1 key equals x tau(8, 7, ·)'s rc exactly (all 0). The sign-flipped E1 equals
  x tau(7, 8, ·) with sides (c, b, a) exactly. That is 0 mismatches over 5 keys.
- **Sign flip on E2/E3/LG8:** the reversed column's rc is −rc for every key. The reversed best is −1/75 (E2/E3) and −2/25 (LG8).
  This is the 7 → 8 direction at these keys, against s34b's dead l3q 7 → 8; it would need the 7 to see e, which it does not.
- **Physical both-end test:** 100,000 random edges, with u of degree 8–12 and v of degree 7, explicit rotations, and a random
  offset and mirror at both ends.
  - The E3 key (which implies E2 and E1) and both LG8 side keys: 0 mismatches.
  - Broken control (the payee reads e from the wrong side): 76,763 mismatches.
- **Non-vacuity:**
  - With the payee rows dropped, the pure payer gain prices at −11/75 (E2, E3) and −22/75 (LG8).
  - The strict masks kill something at 6 of 7 E2 payee items and 5 of 14 LG8 items.
  - The negative rc comes from the masks alone: with no mask, every family is at 0.

## 24.6 Long Table asks (reported separately)
**(A) H-L8, on 8666655/5677657 (dual −1/75): the w0 (8) → s6 (7) column in the l3q shape, big letters allowed, cap 1/2.**
- That transfer has coefficient 0 on u's row, because neither endpoint is u. The rows centred at w0 and s6 are not in the cert.
- The whole LG8 block (U = 8, V = 7, c, a, a2 ∈ 5..9, payee a2 under a strict mask) has **every rc ≥ 0, best 0**.
- The key that names the row, (8, 7, 5, 7, 6), touches 8666655/5677657 only as a payee: u is paid by its w0 on the w6 side.
  Its payer is d8 76556675 (w0−, w6+). rc 0.
- **H-L8 in its LG form is killed.**
- What does relieve this row is E2's K2, but only with full-row masks: the 8 → 7 column of 76556675 no longer has to be credited
  by u, because e+ ∈ {5, 6} is reducible there. That is a projected 1/150 at cap 1/2, which is above the 0.002 kill line, with the
  caveat in §24.4.

**(B) H-R67, on the p41 = 5 residue: r67o, w4 (6) → s3 (7), paid only when all of s3's outer contacts are ≥ 9.**
- w4's 6-type is L = (5, 6, 5, 7, 6, 7), with L0 = p41, L3 = u and L5 = s3.
- (b) forces s4 = p31 ≥ 9 and s5 ≥ 9, which means apex classes (., ., 5, 5, 7, 7). The only cert cons2 row with this L has
  s = (5, 5, 5, 5, 5, 5), with dual −1/150.
- So the (b) type is not in the cert. Its dual is 0, and **rc(r67o) = 0 exactly**: the kill line is met.
  - The existing h key from w4 into u, (7, 5, 6, 5, 7, 6, 5, 5), is at rc 0. Its mrowR2 dual is −1/75, which is the route this
    row already uses.
- The generic r67o family behaves differently. The split h = all≥9 rows take the parent cons2 dual; no cert d7 row has a 9, so
  the payee cost is 0.
  - It has 3 first-order negative keys on other 6-types:
    - (5,6,6,7,7,6)/(7,5,5,7,7,7) at j = 4: −1/75;
    - (5,6,6,7,7,6)/(7,5,7,7,5,7) at j = 3: −1/75;
    - (5,7,6,7,6,7)/(5,7,5,5,7,7) at j = 5: −1/150.
  - None of them is on 8666655/5677657. All three have absent payee rows.
  - This is not specced here. Price it again once a solver with the cons2 h-split exists.

## 24.7 Suggested next step (not done)
- Solve with `e87` (win masks, so no jsep5 change), cap 1/2, keeppen, on 3cfd7f18, warm from rows_s28A62L.
- Kill line: a gain under 0.002 against 11/75.
- If win gains, add full masks (the jsep5 leaf correction) for K2's relief of 8666655/5677657.
