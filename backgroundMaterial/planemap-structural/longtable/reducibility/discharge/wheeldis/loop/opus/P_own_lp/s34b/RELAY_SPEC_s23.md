# RELAY_SPEC §23: z6, a 6 relays to an adjacent 6 (flag `l6r`), solver-ready addendum (Opus s34b)

> **Status: design and pricing only. Nothing here is in the solver, and no solve was run.**
> Source: Long Table, SolvingFrameworkPlan/docs/working/BORROWED-CHANNEL-2.md, family A (origin/main 2417a735). It is RSST's
> drule3′/4/4′/5 with a 6 target, which is §18.3 (b).
> Priced against s28q/eng/cert_s28A60L.json. That cert is lowerR2 VALID at t ≥ 47/320 on registry 7360eb92, args s29/argsA60.txt,
> with s28q engine flags `xon apexcls filt16 killtab=s29/f/kill/kill6 hat5 consall l3q`.
> Pricer: s34b/pricer34.py. Log: s34b/pricer34.log. rc values: s34b/rc34_z6.json.

Everything in §1–§22 carries over unchanged. This includes the §12 cons2 convention: for each 6-type (L, s), Σ in − Σ out = 0,
with L an exact canonical 6-word and s the apex classes 5/7, s_j being the apex beyond the edge (L_j, L_{j+1}).

## 23.1 Columns and keys

**Transfer.** A 6, x, with link L and apex classes s sends `z6[K] ≥ 0` to each link neighbour y = L_j of degree exactly 6.

**Payer key** (x reads it exactly):
- a = (L_{j+1}, ap(L_{j+2}), L_{j+3}, ap(L_{j+4}), L_{j+5}, s_j, s_{j−1});
- K = min(a, ρ7(a)), where ρ7(a, A1, P, A2, b, cr, cl) = (b, A2, P, A1, a, cl, cr).

Here ap is the engine's `prelay2.ap`: a letter ≥ 7 maps to 7, otherwise to 5. P = L_{j+3} is x's vertex opposite y. In the
pricer the key function is `zkey6`.

**Payee signature** (y reads it from its own label (L′, s′) at the position k with L′_k = x):
- g = (L′_{k+1}, s′_k, s′_{k−1}, L′_{k−1}, ap(L′_{k+2}), ap(L′_{k−2}));
- σ = min(g, ρ6(g)), where ρ6(a, A1, A2, b, cr, cl) = (b, A2, A1, a, cl, cr).

σ(K) is K with P removed, then canonicalised by ρ6. It is the same thing the payee reads: the pricer functions `sig_of_key`
and `sig_payee`.

**First family.** The payer link L is a canonical non-R6 6-word that contains a five. Over all 1,424 non-R6 words, every
position with L_j = 6 and every pair of classes for (s_j, s_{j−1}) gives:
- 886 z6 keys;
- 210 payee signatures σ.

Counts are from s34b/famsize34.py.

**Variables.**
- `z6[K] ∈ [0, 3]`, with penalty 1e−3 under `keeppen`, as for x, D and lq.
- `Z6[σ] ≥ 0`, uncapped.

**New row mrowZ[K]:** `z6[K] − Z6[σ(K)] ≤ 0`. There is one row per first-family key.
- P is fixed inside K, so the payee's "every admissible P" condition is exactly one mrowZ row per K.
- A registry mask on P, as in filt16, is a later refinement and is not used here.

## 23.2 Coefficients

| row | z6[K] | Z6[σ] |
|---|---|---|
| cons2 (L, s), x as payer (only if 5 ∈ L) | −1 per position j with L_j = 6 and zkey6(L, s, j) = K | — |
| cons2 (L′, s′), y as payee (any L′) | — | +1 per position k with L′_k = 6 and sig_payee(L′, s′, k) = σ |
| mrowZ[K] (≤ 0) | +1 | −1 at σ = σ(K) |
| senderR2, receiverR2, mrowR2, mrowL | 0 | 0 |

- A cons2 row whose L contains two 6s, and some contain several, can be payer and payee at once. Both terms are added.
- No sender row, receiver row, window or tail term changes, so jsep is untouched.

## 23.3 Soundness

- Each transfer runs along one 6–6 edge, under a key the payer reads exactly.
- The payee credits Z6[σ] ≥ z6[K] for every K it might receive under σ, so it credits at least its true inflow. It must
  pass all of it on, because cons2 is an equality.
- If the payee passes on more than it truly receives, its true final charge is below 0. That is allowed, because 6s only need
  final ≤ 0.
- Fives, bigs and the tail are untouched.

**Physical test** (pricer34.py `phys`). 100,000 random 6–6 edges, built as an explicit disc: x, its link V0..V5, apexes A_i
on (V_i, V_{i+1}), and y = V_j's opposite vertex Q. Both links are read off the triangle list with a random rotation and a
random reflection at each end.
- 0 σ mismatches.
- 0 P mismatches: P = x's vertex opposite y, never in y's closed 1-ball.
- The broken control, where the payee swaps s′_k and s′_{k−1}, gives 42,986 mismatches.

## 23.4 solveR2 (separation)

- **cons2** stays exact: `consall` already separates over all 1,424 6-words × 5⁶ apex words.
  - In `cons2_delta(L, ...)`, add one 5×5 table per term, exactly like the h tables.
  - Payer terms, for j with L_j = 6 and 5 ∈ L: `T[a,b] = −ZV6[zkey6(L, (…s_j = LET[a], s_{j−1} = LET[b]…), j)]` at
    (SALL[:, j], SALL[:, j−1]).
  - Payee terms, for k with L_k = 6: `T[a,b] = +ZW6[sig_payee(L, (…s_k = LET[a], s_{k−1} = LET[b]…), k)]` at
    (SALL[:, k], SALL[:, k−1]).
  - The apex letters are mapped through ap, as with every other apex read.
  - Add the same terms to `cons2_block` with signs −1 and +1. The rank and basis code (`consbasisR2`) then picks them up.
- **mrowZ:** add all mrowZ rows and both column sets up front. That is only 886 + 210 columns and 886 rows. Otherwise add them
  lazily when a key first appears in a cons2 row of the model.

## 23.5 lowerR2

- **Rebuild coefficients** from the row labels:
  - cons2 (L, s): add −1·w to `tot[('z6', K)]` for each payer position (when 5 ∈ L), and +1·w to `tot[('Z6', σ)]` for each
    payee position.
  - mrowZ (K): `tot[('z6', K)] += w` and `tot[('Z6', σ(K))] −= w`, with the same sign convention as mrowR2's (h, M) pair.
    Its dual must be ≤ 0, as for mrowR2.
- **Row admissibility:** reject an mrowZ[K] if K is not a first-family key, meaning no canonical non-R6 L with a five realises K.
- **Pricing:**
  - A z6 with rc < 0 is priced at its cap of 3, as for x, D and lq.
  - Z6 has no cap, so any rc(Z6) < 0 makes the cert INVALID.
  - Without the flag, nothing changes. Control: the s28q lowerR2 on cert_s28A60L gives VALID 47/320
    (s34b/lower_s28A60L_flagoff.log).

## 23.6 upperR2

- Read `'z6': [[K, v], ...]` and `'Z6': [[σ, v], ...]` from the solution JSON. Check 0 ≤ z6 ≤ cap and Z6 ≥ 0.
- **Conservation:** `cons2_delta` with the z6 and Z6 terms over all 1,424 L × 5⁶ apex words. Every |Δ| must be ≤ 1e−9.
- **mrowZ:** check z6[K] ≤ Z6[σ(K)] + 1e−9 for every K.
- Sender rows, receiver rows (jsep d = 7..17), the tail and Karp are unchanged, because z6 never enters a window.

## 23.7 Pricing on cert_s28A60L (exact; rc = −Σ w·coef / tco, tco = 1)

**Composite z6[K] with Z6[σ(K)] = z6[K]** (coefficient −1 at payer positions, +1 at payee positions with σ(K)).
- There are 68 payer keys in the 67 cert cons2 rows, all in the first family.
- **22 have rc < 0, 19 have rc = 0 and 27 have rc > 0.** This is exactly Long Table's hypothesis.

| K = (a, A1, P, A2, b, cr, cl) | rc | payer cert rows (w × positions) | payee rows with σ(K) |
|---|---|---|---|
| **(5,5,5,7,5,5,5)** | **−13/20** | cons2 565659/555555 (−5/16 ×2), 565658/555555 (−1/80 ×2) | none |
| (5,5,6,7,6,7,5) | −21/40 | 566766/555557 (−37/80), 566766/755557 (−1/40 ×2), 556676/575555 (+1/40), 556676/775575, 556686/775557, 556696/575555 (−1/80 each) | none |
| (5,5,6,7,5,5,5) | −13/80 | 565668/555555 (−17/160), 565668/557557 (−9/160) | none |
| (5,5,7,7,6,7,5) | −5/32 | 556697/775557 (−1/10), 566776/755777, 566776/757757 (−9/320 each) | none |
| (5,5,5,7,6,5,5) | −17/160 | 565668/555555 (−17/160) | none |
| (5,5,9,5,5,7,7) | −5/64 | 556559/577555 (−5/64) | none |

The remaining 16 negative keys run from −3/40 to −1/160; all are listed in pricer34.log. Only three of the 22 have any payee
weight in the cert:
- (5,5,6,5,7,5,5) at −1/40, whose payer part is 0;
- (5,5,8,5,5,5,5) at −1/80;
- (5,7,8,5,6,7,5) at −1/160.

**Composite per payee signature.** One Z6[σ] can serve every K with the same σ. All payer keys with a negative payer part
then share one payee credit.
- σ = (5,5,7,5,5,5) gives **rc −141/160**, with K over P ∈ {5, 6, 8, 9}.
- σ = (5,5,7,6,7,5) gives rc −121/160.

**Controls.**
- **Flag off:** 47/320, with no existing column at rc < 0.
- **Wiring:** K* decomposes as 2·(−5/16) + 2·(−1/80) = −13/20. Flipping the sign gives +13/20.
- **Physical:** 0 mismatches, against 42,986 in the broken control.

**Non-vacuity**, with s34b `realise`: non-R6 canonical words, including the 2.122 three-fives rule.
- K* has payer words 565658 and 565659 with (s_j, s_{j−1}) = (5, 5). 565659 is the d10's link 6 when its private is 5; 565658 is the same shape with an 8 centre.
- σ* = (5,5,7,5,5,5) has 14 payee words, for example 556558, 556559 and 556568, with (s′_k, s′_{k−1}) = (5, 7) or (7, 5).
  These are an apex 6 of u, with a five on each side of x.
- Every one of the first six negative keys has both payer and payee words.

**Ring-merge suspect.**
- No negative key depends on rows killed only by f7_..56757_...5.... z6 touches cons2 rows only, and they do not depend on the
  registry.
- The cert's own rows stay admissible when that C entry is held, because removing a C only adds rows.

**Kill line not met:** the family prices negative. Solve per the note, folded into the stacked solve:
- registry 7360eb92 / argsA60, or the current head;
- s28q flags + `l6r`, with z6 cap 3 and penalty 1e−3;
- the keeppen → nosep → lowerR2 → upperR2 recipe.

Kill the solve if any of these holds:
- the gain over 47/320 (lower) and 0.147857 (upper) is under 0.005;
- the total z6 weight is under 1e−3;
- upperR2 conservation fails.

## 23.8 Family C (l3q extended to 7 → 8): dead, as expected

The key is (c, a, a2); the payer is a d7 row with link letter 8; the payee is a d8 row with link letter 7, credited when a2 is
in the mask of the 7's private. This is LG of s32p restricted to (U, V) = (7, 8).

| key | payer −Σw | payee cost (a2 ∈ mask) | rc | rc with the payee mask dropped (control) |
|---|---|---|---|---|
| (6,5,6) | 7/80 | 21/160 | **+7/160** | −7/80 |
| (6,5,8) | 7/160 | 21/160 | **+7/80** | −7/160 |
| (5,6,8) | 7/160 | 7/160 | **0** | −7/160 |

- **Payers:** R7 8658656/6665555 (−1/40), 8658656/6665556 (−1/160) and 8568656/6655555 (−1/80).
- **Payees:** R8 75666556/66666565 (−7/160), 76656656, 85656765, 76665656 (−1/80 each) and 76656566 (−1/160).
- **Masks:** the rc are identical with no mask (31) and with the s32p masks32 win and full masks, with or without
  f7_..56757_...5.... Those masks remove only the letter 5, never 6 or 8, at these 7-privates.
- The rc ≥ 0 kill line is met, so no solve is run.
