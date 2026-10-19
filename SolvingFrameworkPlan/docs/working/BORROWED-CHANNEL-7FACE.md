# Borrowed channel: who pays the 5-5-5 face of the binding 7 under RSST's rules (Long Table, 19 Oct 2026)

This note is a source of ideas, not a claim. It applies the 32 published RSST discharging rules to the explicit 2-ball of the
K = 2 binder, and then restates the one channel that matters as a column family in our own LP class (RELAY_SPEC §12 + §14′ + §15).
Opus can then price that family against cert_st24bL.

**Sources (public or main-line only; nothing from Team B was read).**
- **Rules.** The RSST 32 rules as Gonthier's machine-checked encoding, `fourcolor` `theories/proof/discharge.v`
  (coq-community/fourcolor master, md5 5b8491c3…; `part.v` md5 67f83608…). The file holds `drule1..drule32` and
  `base_drules` (38 parts with multiplicity), and gives 71 parts after `symmetrize_drules`.
  - Thomas's `https://thomas.math.gatech.edu/FC/rules` could not be fetched: the proxy returned 403.
  - No local copy of `discharge.v` exists. Studio's `studio/rsst_rules/` reads it from an opam install that is not on this machine.
  - The rule numbers below are Gonthier's `drule` numbers. They are the 32 rules of Robertson, Sanders, Seymour and Thomas
    (1997), with drule2′/3′/4′/10′/31′ as Gonthier's hub-arity and symmetry specialisations.
- **Semantics** (part.v, discharge.v):
  - Charge is 10(6 − d). A part fits at hub h when deg h equals the part size and every spoke, hat and fan range holds.
  - Each fit moves **1 RSST unit from the hub to its third spoke**. drule1 is listed twice, so it moves 2.
  - **1 RSST unit = 0.1 in our §1 scale** (charge 6 − d).
  - The sender is always the hub. Every rule's receiver has degree ≥ 6, so a five never receives.
- **Geometry and containment.**
  - The scorer is our own (scratch `face7.py`). It builds the 2-ball explicitly (u, link w_i, apexes s_i, privates, fresh
    ring 3) and uses Studio's fit semantics from `studio/rsst_rules/rsst_score.py`.
  - Single-slot kills use `loop/k42/grow.py` embeddings over RSST's 633 (`studiointel/routeb/rsst/unavoidable.conf`, md5 26aeba66…).
  - Validation: on the sibling 7665566/6675666 the per-slot kills reproduce RELAY_SPEC §14′ check 4 exactly (p01, p02
    rsst180; p11 rsst052; p21 rsst025/050; p51 5 and 6; p61 rsst052).
- **Binder.** cert_st24bL (md5 51055fe3…, the same file Studio checked) has receiverR2 7 **7665566 / 6675676** at weight
  −6/26. The other two receivers are the d = 10 rows.
  - Link: w0 = 7, w1 = w2 = 6, w3 = w4 = 5, w5 = w6 = 6.
  - Apexes: s0 = 6, s1 = 6, s2 = 7, s3 = 5, s4 = 6, s5 = 7, s6 = 6.
  - **Face:** the triangle (w3, w4, s3), three fives, adjacent to the triangle (u, w3, w4).
  - Ring 2 in cyclic order: p0a p0b s0 p1 s1 p2 s2 s3 s4 p5 s5 p6 s6.
  - s3 has exactly one ring-3 neighbour, T, which is adjacent to s2 and s4.

## Rules that fire

Below, privates are taken as 6 (and, for u's ledger, everything that holds whenever no private is 5). Amounts are in RSST units.
"m" marks the mirror image across the third spoke.

| sender (hub) | dist from u, deg | receiver | units | rules |
|---|---|---|---|---|
| w3 (face five) | 1, d5 | u (7) | 4 | drule1 ×2, drule2m, drule3m |
| w3 | 1, d5 | s2 (apex 7) | 4 | drule1 ×2, drule2, drule3 |
| w3 | 1, d5 | w2 (6) | 2 | drule1 ×2 |
| w4 (face five) | 1, d5 | u | 4 | drule1 ×2, drule2, drule3 |
| w4 | 1, d5 | w5 (6) | 3 | drule1 ×2, drule3m |
| w4 | 1, d5 | s4 (6) | 3 | drule1 ×2, drule3m |
| s3 (far face five) | 2, d5 | s2 | 4 (+1 if T = 5) | drule1 ×2, drule2m, drule3m |
| s3 | 2, d5 | s4 | 3 | drule1 ×2, drule3 |
| s3 | 2, d5 | T (ring 3) | 3 if T ≥ 6 | drule1 ×2, drule3 |
| w5 (6 next to the face) | 1, d6 | u | 3 | drule2′, drule4 (reads hat s3 = 5), drule6 (reads hats s3, w3) |
| w2 (6) | 1, d6 | u | 1 (2 if p2 = 5) | drule2′m (+drule4′) |
| w2 | 1, d6 | s2 | 1 | drule2′ |
| s4 (6) | 2, d6 | w5 | 2 | drule3′, drule4 (6 → 6) |
| s4 | 2, d6 | p5 | 1 | drule3′ (6 → 6) |
| w5 | 1, d6 | p5 | 2 | drule3′m, drule4′m (6 → 6) |
| **u (the 7)** | 0, d7 | **w0 (7)** | **2** | **drule9 and drule9m** |
| w0 | 1, d7 | u | 1 per private of w0 that is 5 | drule9 (reverse) |
| w1 | 1, d6 | u | 1 if p1 = 5 | drule4′ |

**drule9** is `Part $ 6- $ 6- $ 7+ $ * $ * $ * $ 5 $` at a hub of degree exactly 7. Read along u's link, it says:
a 7 sends 1 to a big link neighbour v = w_i when **w_{i∓1} ≤ 6, w_{i∓2} ≤ 6 and w_{i∓3} = 5**, once per side.
- Here both sides hold: (w6, w5, w4) = (6, 6, 5) and (w1, w2, w3) = (6, 6, 5).
- The 5 that triggers the rule is a face five, at link distance 3 from w0.

**u's RSST ledger** (exhaustive over the 5^6 private fillings, all exact):
- Inflow is 4 + 4 + 3 + 1 = 12, and outflow is 2. So u ends at −10 + 12 − 2 = **0** in 6,400 of the 15,625 fillings:
  exactly those with p0a, p0b, p1, p2 ≠ 5.
- In every other filling u ends at +1..+4, and each of those fillings contains an RSST configuration in the 2-ball.
  The single-slot kills are p0a = 5 and p0b = 5 by **rsst180**, p1 = 5 by rsst052, p2 = 5 by rsst025/rsst050, and p5 = 5 by rsst003.
- **rsst180** (RSST 122.61866, interior degrees 7,7,6,6,6,5,5,5) is drule9 seen from both ends of the edge:
  - u, w0, w6, w5, s6, and the face fives w4, w3;
  - plus w0's private p0a = 5 (p0b by the mirror).
  - It is in our forbidden set as C2cons (§14′ census killers).

The same picture holds across the face family. drule9 and its relatives drule8 (5 at link distance 2) and drule21 fire out of u
into a big link neighbour in every row checked:
- 7665566 / 6675666, 6765766, 6665766;
- 7665567 / 6765756;
- 7655667 / 6756656;
- 7676556 / 7759565;
- 7766556 / 6566575, 6576576, 6567566.

## Who pays the face

The face holds 30 RSST units (3.0 in our scale). Under RSST it goes:

| taker | direct from the face fives | ours |
|---|---|---|
| u, the 7 | 8 (w3 4, w4 4) | 0.8 |
| s2, the apex 7 on the face's far side (adjacent to w3 and s3) | 8 (w3 4, s3 4) | 0.8 |
| the 6s w2, w5, s4 | 2 + 3 + 6 = 11 | 1.1 |
| T (ring 3, s3's last neighbour) | 3 | 0.3 |

The 6s relay that charge onward:
- back into u: w5 3, w2 1;
- to s2: w2 1;
- 6 → 6 toward w5's private: w5 2, s4 1. This continues to s5 (7) and to ring 3.

**So RSST does not take the face off the 7.** u absorbs 12 units, 1.2 in our scale, which is more than u's 1 + 2/13 load in st24b.
What keeps u at 0 is **one outflow: drule9, 0.1 on each side, to its 7-neighbour w0.** The reverse transfer w0 → u is excluded
because rsst180 forbids a 5 at w0's private. In other words, RSST's 7 "pays the whole face" exactly as ours does, but it is
allowed to pass 0.2 on to w0, and 0.2 > 2/13.

**Why our LP cannot do this.**
- The L2 column x (§2.2) on the edge u → w0 reads sides (w6, w5, s6) = (6, 6, 6) and (w1, w2, s0) = (6, 6, 6).
- The reverse direction w0 → u reads the same six letters, so tau_in = tau_out and the coefficient is 0. This is the
  self-pairing recorded since round 12.
- The only letters that break the symmetry lie at distance 3 from the edge's far end:
  - u's face fives w3 and w4, which w0 sees only as u's privates;
  - w0's privates p0a and p0b, which u does not see.
- The §19 D/O families are distance-2 transfers and stop short of these letters. That is why stage 24 priced nothing into the face 7.

A secondary RSST channel does not relieve u but explains where the far five s3 goes: **6 → 6 relays** (drule3′/4/4′: s4 → w5,
s4 → p5, w5 → p5). Our class has no 6 → 6 column; this is §18.3 (b), still unscreened.

## Proposed own-rule column family

**q (flag `l3q`): big → adjacent big, keyed on the payer's link out to distance 3, with payee credit through a private mask.**
This is written in RELAY_SPEC terms (§1 convention: a big's load is its inflow, capped at d − 6 + t).

**Transfer.** A big u with U = min(d, 9) sends `q[κ] ≥ 0` to a big link neighbour v = w_i, once **per side** σ ∈ {+, −}.
- **Key:** `κ = (U, V, c, a, a2) = (U, min(deg v, 9), w_{i+σ}, w_{i+2σ}, w_{i+3σ})`. All letters are exact, 5..9.
- **Sides are separate transfers.** The key is a directed path along u's link going away from v, so no reflection min is
  needed; reflecting u's link swaps the two sides.
- **First family (minimal):** U = 7 only (drule9's hub arity), V ∈ {7, 8, 9}, c, a ∈ {5, 6}, a2 ∈ 5..9. That is 60 q columns.
  - The full family is U ∈ {7, 8, 9} with c, a, a2 ∈ 5..9.
  - For U = 7, w_{i+3} and w_{i−3} are distinct and adjacent. For U ≥ 8, a2 is the next link vertex after a.

**What each end reads.**
- **Payer u.** It reads its own link, so κ is exact. Its row is debited `−q[κ]` for each big w_i and each side.
- **Payee v.** u = w'_j is a big link vertex of v.
  - c = w'_{j+σ'} is in v's link (exact).
  - a = the apex across (w'_j, w'_{j+σ'}), i.e. s'_j or s'_{j−1}, is exact.
  - a2 is **u's private** relative to v, the one adjacent to a. It is unseen.
  - So v reads only the signature `κ' = (U, V, c, a)` plus a **mask** of allowed letters for a2.

**Mask** (an extension of §14′ to the privates of a **big** spoke).
- In the payee's receiverR2 arrangement (link and apex word fixed), make that one private the only free vertex. Set every
  other unknown to 99, and use the strict unknown-vertex rule.
- A letter is killed when some configuration of the current forbidden set embeds using it. Use the full 2,009+ set; the
  RSST 633 alone is enough at the binder.
- **Window:** the mask needs v, u = w'_j, w'_{j+σ'..j+4σ'} and s'_{j−1}, s'_j. rsst180 uses link distance 4 on the payee
  side. This is wider than the 9-slot window (see the separator note below).

**Columns and rows.**

| row | q[κ] | Q[κ', mask] (new, ≥ 0) |
|---|---|---|
| receiverR2 of payer u | −1 per (i, σ) with key κ | 0 |
| receiverR2 of payee v | 0 | +1 per (j, σ′) with signature κ′ and that mask |
| mrowQ (new) | −1 | +1: `Q[κ', mask] − q[(κ', a2)] ≥ 0` for every a2 ∈ mask |
| senderR2, cons2, mrowR2, mrowV | 0 | 0 |

**Soundness.**
- Each transfer is one edge of charge u → v under a key that u computes exactly.
- v credits at least the true inflow, because Q is at least the max over every a2 still possible.
- This is the payer-forced, payee-possible asymmetry that §19.4 already uses for O.
- With the mask off (all of 5..9 allowed), the class contains the current one (q = Q = 0) and is sound but useless at the
  binder (see the control below).
- **RSST's own value** is q = 0.1 on keys (7, ≥7, ≤6, ≤6, 5) and 0 elsewhere. A cap of 3 (as for x) and a penalty of 1e−3
  keep it from circulating (lesson from st24d).

**Separator.**
- The payer term at a big position i reads w_{i±3}.
- The payee term at a big position j reads w'_{j±1}, s'_{j−1}, s'_j and, through the mask, w'_{j±2..j±4}.
- Both terms leave the 9-slot window. d = 7..17 exhaustive separation needs either an 11-slot window, or the q/Q terms
  enumerated per row as in §15's tail argument. The tail d ≥ 18 is linear in W9 as before.

## Pricing test for Opus

**Hypothesis.** At cert_st24bL (t = 2/13, tco = 1), the composite column q̂ = q[(7, 7, 6, 6, 5)] has a negative reduced cost.
Here Q is set to its mrowQ minimum, so q's coefficient in a row is −(payer positions) + (payee positions whose mask contains a2 = 5).

**Expected arithmetic** (rc = −(Σ w·coef)/tco, as in §19.6):
- **Face 7 row, 7665566/6675676 (w = −6/26).**
  - Payer positions: 2, both w0 sides.
  - Payee positions from w0: 2, with signatures (7, 7, 6, s6 = 6) and (7, 7, 6, s0 = 6).
  - Their masks for p0a and p0b are {6, 7, 8, 9}, because rsst180 kills 5 single-slot.
  - So coef = −2, and **rc(q̂) = −((−6/26)(−2)) = −6/13 ≈ −0.4615.**
- **The two d = 10 rows** have no 7 in their links, so coef = 0. Sender, cons2 and mrowR2 rows have coef 0.
- So the 2/13 cert is **not** valid for the `l3q` class.
- The only other first-family keys that touch the cert are q[(7, 7, 6, 6, a2 ≥ 6)]. They enter through the payee credit
  (+2 at the face row) and price positive (+6/13).

**Required controls.**
1. **Mask off** (all a2 allowed): composite coef at the face row = −2 + 2 = 0, so rc = 0. This reproduces the self-pairing.
   If Opus gets rc < 0 here, the payee credit is wrong.
2. **Side test of the mask.** This binder is symmetric, so a mask read on the wrong side (s0 vs s6) goes unnoticed here.
   Test the sides on 7665567/6765756 instead. There our run kills p0b = 5 (rsst180) but not p0a = 5. The composite
   coefficients must follow the mask side by side, and a swapped-side control must change them.
3. **Physical test** (as §15/§19.3): random u–v edges with explicit rotations, payer key and payee signature + mask read
   by the generic neighbour rule. 0 mismatches over 100,000 is required; a broken-key control must show mismatches.
4. **Mask table:** recompute single-slot kills on the binder's 2-ball with the full forbidden set. The p0a = 5 and
   p0b = 5 kills (rsst180) must reproduce. Our run: 7665566/6675676 kills p0a, p0b = 5 (rsst180), p1 = 5 (rsst052),
   p2 = 5 (rsst025, rsst050) and p5 = 5 (rsst003); none at p6.

**Kill line.**
- **Priced:** composite reduced cost **rc(q̂) ≥ 0** on cert_st24bL for every first-family key means a kill. Report the
  family dead and run no solve.
- **If priced negative, then solve** on 0125c46b with the st24b flags + `l3q` (dcap-style cap 3, penalty 1e−3, consall,
  4 threads, 3 h cap). Kill if the gain over 2/13 is under 0.005, or if q enters with total weight under 1e−3.
  - Expected new binders are 7s like w0 (link 7 6 6 p p 6 6), which now take the conservative Q credit, and the two
    d = 10 rows, which q does not touch.
  - A gain is plausible only up to the d = 10 floor. This note does not predict t* ≤ 0.

Scratch only, not committed: `face7.py` (RSST flow scorer on an explicit 2-ball) and `slotkill.py` (single-slot RSST kills
via k42/grow.py). Both are in the session scratchpad and can be rebuilt from this note.
