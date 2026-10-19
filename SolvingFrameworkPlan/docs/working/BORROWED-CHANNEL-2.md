# Borrowed channel, round 2: the post-l3q binders under RSST's rules (Long Table, 19 Oct 2026)

This note is a source of ideas, not a claim. It continues BORROWED-CHANNEL-7FACE.md (round 1, dc954db3). Round 1 found the
face-7 channel; `l3q` paid it, and Opus's s28q lower cert is now **47/320** (`cert_s28A60L.json`, 120 rows; upper 0.147857).
Here the 32 RSST rules are applied to the explicit 2-balls of the new binders. For each binder, the RSST ledger is set next
to our LP's own ledger of the same row at `sol_s28A60.json`. The note ends with two column families and one registry ask,
each with a pricing test against the 47/320 cert.

**Sources (public or main-line only; nothing from Team B was read).**
- **Rules and semantics** are as in round 1: Gonthier's `discharge.v` (coq-community/fourcolor), 1 RSST unit = 0.1 in our §1
  scale, and the hub sends 1 to its third spoke per fit. Hubs have degree 5..8 only (part sizes 5, 6, 7, 8), so a 9+ never
  sends.
- **Binders** come from `P_own_lp/s28q/eng/cert_s28A60L.json` and `s28A60L.log`, on branch `origin/claude/project-thread-7uelj0`
  (commit 11f050ea). It is not yet on main.
- **Our ledger** is `pcheck.py rowR2` from the s28q engine (flags `xon apexcls filt16 hat5 consall l3q`, argsA60) at
  `sol_s28A60.json`. Thirteen pattern files were missing locally, which affects only the admissibility printout.
- **Notation** is as in round 1. A row name is LINK/SWORD. The link is w_0..w_{d-1}, and s_i is the apex shared by w_i and
  w_{i+1}. The privates of w_i are p_{i,a}, p_{i,b}, …
- **Scorer and kills.**
  - The scorer is round 1's `face7.py` with one fix. A receiver of degree ≥ 10 was never matched, because the rule ranges stop
    at 9. Degrees are now capped at 9 when matched (`face7b.py`). The face-7 regression reproduces round 1's table exactly.
  - Kills use `k42/grow.embeddings` over RSST's 633. Each killer is tagged with its k44 verdict: D2 or C2cons means it is in
    our verified set (582 configurations); "none" means it is not.
- **Fillings.** Ledgers are exhaustive over the private letters. Privates range over 5..9 at d10 and on the 75666556 and 76656656
  rows, and over {5, 6, 7, 9} on 85656765 and 8658656. Each filling is classed as one of:
  - **own:** killed by a configuration we have verified;
  - **borrowed:** killed only by an RSST configuration we have not verified;
  - **free:** no RSST configuration embeds.

## The binders (cert_s28A60L, receiverR2 weights)

| row | w | analysed here |
|---|---|---|
| 10 6565656565/6556666666 | −5/64 | yes |
| 8 75666556/66666565 | −7/160 | yes |
| 7 8658656/6665555 | −1/40 | yes (8568656/6655555, −1/80, gives the same RSST ledger) |
| 8 76656656/56655565 | −1/80 | yes |
| 8 85656765/56665565 | −1/80 | yes |
| 8 85566556/66666855, 85556655/66866666, 76665656/56566655, 86555665/56586665 | −1/80 each | ledgers only (scratch) |
| 7 8658656/6665556, 8 76656566/56655565 | −1/160 each | not separately |

## The pattern in one table

All values are in our scale. "RSST" means the worst free filling, or every filling where the row is reducible.

| binder | RSST: fives → u | ours: y | RSST: 6s → u | ours: M + r | big neighbours ↔ u (RSST / ours) | u ends (RSST) / ours load vs cap |
|---|---|---|---|---|---|---|
| d10 | 1.2 (0.2–0.3 each) | **3.785** (0.74–0.78 each) | 1.4 | 0.34 + 0.02 | none / none | **−1.4** / 4.148 = cap |
| d8 75666556 | 1.0 | 1.643 | 0.8–1.1 | 0.55 + 0.02 | 7 pays u 0.1–0.4 / u pays 7 0.063 | reducible (8406.123) / cap |
| d7 8658656 | 0.6 | 0.773 | 0.7 | 0.22 + 0.10 | u pays both 8s 0.4 / 8s pay u net 0.049 | **−0.1** / cap |
| d8 76656656 | 0.6 | **1.405** | 1.0–1.3 | 0.61 + 0.12 | 7 pays u 0.2–0.3 / 7 pays u 0.014 | 0 / cap |
| d8 85656765 | 0.6 | 1.366 | 0.6 | 0.61 + 0.04 | 7 pays u 0.2–0.3 / +0.069 | **−0.5** / cap − 0.067 |

**The common cause.**
- **RSST's fives do not dump onto the big.** drule1 makes every five send 0.2 to *each* neighbour of degree ≥ 6, apex 6s
  included. A five adds at most 0.1–0.2 on top (drule2/3) toward a big or a 6 next to another five.
- **RSST's 6s pass charge on to further 6s** (drule3′, drule4, drule4′, drule5: the third spoke only needs "6+"), and to the
  big privates of the centre's link 6s.
- **Ours, by contrast:**
  - each of our fives puts 0.42–0.78 directly onto the centre;
  - our 6s can unload only into bigs (h2), with no 6 → 6 column;
  - in the five's worst-case sender row, the apex 6s are dead ends.
- **Our 6s carry less to the centre than RSST's (M ≤ RSST).** So the excess is entirely y.

## Binder 1: d10 6565656565 / 6556666666 (w = −5/64)

**Geometry.**
- Link: w_odd = 5 and w_even = 6.
- Apexes: s_1 = s_2 = 5, the rest 6. So w_2 is a 6 with four five-neighbours (w_1, w_3, s_1, s_2).
- Each link 6 has one private.

**Rules that fire** (RSST units; all 3,125 fillings give the same values on u):

| sender | to | units | rules |
|---|---|---|---|
| w_1, w_3 (fives beside the apex fives) | u | 3 each | drule1 ×2, drule3 |
| w_5, w_7, w_9 | u | 2 each | drule1 ×2 |
| each link five | every other neighbour of degree ≥ 6 (w_{i±1}, its apex 6s) | 2 each (3 to w_0/w_4 from w_1/w_3) | drule1 ×2 (+drule3) |
| w_0, w_4 | u | 3 each | drule2′, drule2′m, drule4 |
| w_2 | u | 4 | drule2′ ×2, drule3′ ×2 |
| w_6, w_8 | u | 2 each | drule2′ ×2 |
| w_0, w_2, w_4, w_6, w_8 | own private | 3, 4, 3, 2, 2 | drule3′ ×2 (+drule4′, drule2′ when the private is big) |
| apex 6s s_0, s_3..s_9 | ring 3 (unknown) | 6–9 "maybe" each | drule2′–7 |

- u takes 2.6 of its 4.0 deficit and **ends at −1.4 in every filling**. A hub of degree 10 sends nothing.
- **Kills.** RSST-free fillings are those with every private ≥ 7 (243 of 3,125).
  - p_{0,4,6,8} = 5 by 2.126 (rsst003, **not ours**), and = 6 by 2.453966 (rsst013, ours D2).
  - p_2 = 5 by 2.122 (ours), and = 6 by 2.126 (not ours).
  - In RSST's world, then, every link 6 of the d10 has a **big private**, and it pays that private as much as it pays u.

**Our ledger** (load 4.1479 = cap):
- y9|6566 2 × 0.784 (w_1, w_3) and y9|6666 3 × 0.739, which is **3.785 from the fives**;
- M 0.340, and the M masks still allow p = 5 at w_0/4/6/8 (mask 29) and p = 6 at w_2 (mask 30);
- hat5 r 0.023.
- The cert's heaviest sender row is this five, **66669 [00000|0110], w = 15/64**.
- The d10's link 6 with private 5 carries the largest cons2 and mrowR2 weights: cons2 [5,6,5,6,5,9]/555555 = −5/16, and
  mrowR2 at k = [9,5,6,5,6,5,5,5] = −5/16.

**Who pays.** RSST does not make the d10 tight. Each five spreads 0.2 to every neighbour. The two apex 6s it touches relay that
charge outward, and the link 6s split their inflow between u and their big private.

**What RSST moves that we cannot.**
1. **6 → 6 relays** out of the apex 6s and the link 6s (drule3′, drule4, drule4′ with a 6 target). We have no 6 → 6 column.
2. **Not a column: the private letter.** Our verified set leaves the link 6's private free to be 5 (2.126 is only broad-X C on
   our engines, EXPLORE-LOG round 42). In our worst case the five's hats between its 6-spokes are small and the apex 6s have no
   outlet.
   - Check on the top sender context with exact hats, using `sctx.py` (the §17 frame with grow.embeddings):
     - with the hats beside the big equal to (5, 5), as in the d10, our 582 kill 270 of 288 completions;
     - the other **18 die only by 2.126**, and none survives RSST's 633.
   - With class hats the context keeps 9 survivors even under all 633 (all hats 6).
3. x, D, O and l3q do not apply: u has no big link neighbour.

## Binder 2: d8 75666556 / 66666565 (w = −7/160)

**The row is RSST-reducible as it stands.** RSST 8406.123 (rsst433, interior degrees 8,7,6,5,5,5,5,5) embeds on
u, w_0, w_7, w_1, w_5, w_6, s_5, s_7 and needs no private. k44 lists it as "none", with every engine run still *pending*
(`k44/rsst_verdicts_C2.txt:168`). The d8 window pattern already exists (`k44/pats44_all.txt:221`).

**Rules that fire** anyway, over 15,625 fillings, all of which contain a configuration:
- the five pair w_5, w_6 sends 4 each to u (drule1 ×2, drule2, drule3);
- w_1 sends 2;
- w_4 and w_7 send 3 each (drule2′, drule4, drule6);
- w_2 and w_3 send 1–2 (drule2′/4′/7);
- the 7 w_0 → u sends 1–4 (drule8, drule9, drule14).
- u ends between −0.2 and +0.2.

**Ours.**
- y8|5566 2 × 0.662 (w_5, w_6) and y8|6667 0.319 (w_1).
- M 0.550 and r 0.017.
- **x −0.063: u pays its 7** (x 8→7 sides (5,6,6)(6,5,5)).
- RSST runs the other way: the 7 pays the 8 by drule8 and drule9.

**Who pays: nobody needs to.** Under RSST the row does not exist. What RSST "moves" here is reducibility, not charge.

## Binder 3: d7 8658656 / 6665555 (w = −1/40; 8568656/6655555 identical under RSST)

**Geometry.**
- Link: two 8s (w_0, w_3), fives w_2 and w_5, sixes w_1, w_4, w_6.
- Apexes s_3..s_6 are fives, so w_4 and w_6 each touch three fives.

**Rules that fire.** The ledger is constant over 262,144 fillings:
- **In 13:**
  - w_5 sends 4 (drule1 ×2, drule3 ×2);
  - w_2 sends 2;
  - w_4 and w_6 send 3 each (drule2′, drule3′, drule4);
  - w_1 sends 1 (drule2′).
- **Out 4:**
  - **u → w_0, 2 units (drule8, drule8m)**: a 7 sends 1 to a big link neighbour v = w_i when w_{i∓1} ≤ 6 and w_{i∓2} = 5;
  - **u → w_3, 2 units (drule8m, drule14m)**.
- So **u ends at −0.1**.
- The link 6s w_4 and w_6 send their big privates 4 each. Privates p_4 and p_6 are forced ≥ 7: 5 is killed by 2.122 and
  6 by 2.126.

**Ours.**
- y7|6556 0.548 (w_5) and y7|6668 0.225 (w_2).
- M 0.222 and r 0.105.
- x: u pays w_0 0.0136 by x 7→8 (6,5,5)(6,5,6), which is drule8 on that edge. **w_3 pays u 0.0629** by x 8→7 (5,6,6)(6,5,5).

**Who pays.** RSST's 7 is over-supplied (1.3 in) and passes 0.2 to each 8. Ours receives net 0.05 *from* the 8s.

**What RSST moves that we cannot: nothing new on the 7–8 edges.**
- drule8 reads only (w_{i∓1}, w_{i∓2}), which are x's side letters (c, a). x18776 is exactly drule8 on u → w_0.
- drule14 additionally reads the hat s_{i−2}, one apex beyond x's side.
- Our LP runs x the other way because the adjacent 8s (binders 2, 4, 5) are fuller than this 7. It prices 8-capacity higher
  than 7-capacity.
- So **the d7 is relieved only by relieving the 8s.**
- An `l3q` extension U = 7 → V = 8 (drule9, a five at link distance 3) loads the 8s further. It is priced below (family C) and
  is expected to die.

## Binder 4: d8 76656656 / 56655565 (w = −1/80)

**Geometry.**
- Link: w_0 = 7, fives w_3 and w_6.
- Apexes s_0, s_3, s_4, s_5, s_7 are fives.

**Fillings.** There are 78,125: 53,069 own, 17,361 borrowed and 7,695 free.

**Rules that fire.**
- **In** (free fillings):
  - fives w_3 and w_6 send 3 each (drule1 ×2, drule3);
  - w_4 and w_5 send 3 (drule2′, drule3′);
  - w_2 sends 2–3 (drule2′, drule4, drule5);
  - w_7 sends 2, and w_1 sends 0–1 (drule7);
  - **the 7 w_0 sends 2–3 (drule8, drule9)**.
- **u ends at −0.2..0 in free fillings; worst 0** at privates (5,7,6,7,7,7,7). RSST is tight here too.
- The **borrowed fillings reach +0.1**, and 2.126 kills all of them: privates 5 at three slots, 6 at two.

**Ours.**
- y8|6566 2 × 0.703 = **1.405**.
- M 0.607 and r 0.122.
- x +0.014 (7 → 8).

**Who pays.** RSST charges the 8 the same total, but with a different mix:
- fives 0.6 (ours 1.405);
- 6s 1.0–1.3 (ours 0.73);
- the 7 0.2–0.3.
Each five sends its other 0.4–0.7 to its 6 neighbours, among them apex s_2 and s_6, and to w_2/w_4 (w_5/w_7). Those 6s relay
further by 6 → 6 rules.

**What RSST moves that we cannot:**
- five → apex 6 → onward 6 (6 → 6);
- 2.126's kills at three privates.

## Binder 5: d8 85656765 / 56665565 (w = −1/80)

**Geometry.**
- Link: w_0 = 8 and w_5 = 7.
- Fives w_1, w_3 and w_7.

**Fillings.** Privates range over {5, 6, 7, 9}: 65,536 fillings, of which 3,080 are free.

**Rules that fire.**
- **In:**
  - the fives send 2 each (drule1 ×2 only);
  - w_2 sends 3 (drule2′, drule4), w_4 sends 1, w_6 sends 2;
  - **the 7 w_5 sends 2–3 (drule8, drule9)**.
- **u ends at −0.6..−0.5 in every free filling.**
- The 8 w_0 sends u 1–2 by drule28, but only in fillings that we kill ourselves.

**Who pays.** w_1 and w_7 send 3 each to the *other* 8, w_0 (drule3: their other neighbour is a five), and 3 to their 6s.
u is slack by 0.5.

**Ours.**
- y8|6658 2 × 0.423 and y8|6666 0.521.
- M 0.614 and r 0.035.
- x +0.069 (7 → 8 0.014, 8 → 8 0.055).
- Load 2.081, slack 0.067 at the upper sol. The row binds in the 47/320 dual.

**What RSST moves that we cannot.**
- y to w_0 is expressible, but w_0 is a binder-class 8.
- The rest is again five → 6 → 6.

## Borrowed kills (a registry ask, not a column)

Two RSST configurations that we have not verified sit under the cert's heaviest weights.

1. **2.126 (rsst003, ring 8, interior 5,5,6,6).** It is a 6–6 edge whose two tips are fives.
   - kc and cfast find it C-reducible only with a broad X (RSST's own four ring-to-interior edges); the conservative
     admissibility check fails.
   - It is the borrowed single-slot killer in **all five** binders analysed here:
     - d10: four privates;
     - 76656656: three slots;
     - 8658656: three slots;
     - 85656765: three slots.
   - Above all, it kills the private 5 under the cert's **−5/16** cons2 and mrowR2 weights, and the 18 last completions of the
     top sender context (15/64).
2. **8406.123 (rsst433, ring 12).** It kills the d8 binder 75666556/66666565 (−7/160) outright. It has never been run on our
   engines (k44: pending).

**Test for the reducibility lane** (no LP change):
- **Step 1.** Run `kc -C2`, `kc -x` with RSST's X, and `cfast --fixed` on 8406.123. If it becomes C2cons, add it to the
  registry.
- **Step 2.** Re-run `lowerR2` on cert_s28A60L. The receiver row 75666556/66666565 must then be rejected as inadmissible.
- **Step 3.** For 2.126, the open question is the contract's admissibility. Round 42 already left it there.
- **Kill line:** 8406.123 is neither D nor C under the conservative X on either engine.

## Proposed own-rule column families

### A. z6 (flag `l6r`): a 6 relays to an adjacent 6, keyed on the payer's exact link, payee credit by signature

This is written in RELAY_SPEC terms (§12 cons2 convention: Σ in − Σ out = 0 per 6-type (L, s), with s as apex classes 5/7).
It is RSST's drule3′/4/4′/5 with a 6 target, which is §18.3 (b), still unscreened.

**Transfer.** A 6 x with exact link L = (L_0..L_5) and apex classes s sends `z6[K] ≥ 0` to each link neighbour y = L_j of
degree exactly 6.
- **Key:** `K = min(a, reflect(a))` with `a = (L_{j+1}, ap(L_{j+2}), L_{j+3}, ap(L_{j+4}), L_{j+5}, s_j, s_{j−1})`, where ap
  maps a letter to its 5/7 class.
  - L_{j±1} are y's two link neighbours adjacent to x.
  - **P = L_{j+3}** is x's vertex opposite y, i.e. x's private relative to y.
  - s_j and s_{j−1} are the apexes of x beyond the edges (y, L_{j+1}) and (y, L_{j−1}).
  - reflect maps (a, A1, P, A2, b, cr, cl) to (b, A2, P, A1, a, cl, cr).
- **First family:** every key whose payer L is a non-R6 6-word containing a five. That is ≤ 5·5·5·2⁴ = 2,000 keys before the
  reflection min and the R6 filter.

**What each end reads.**
- **Payer x** reads its own label, so K is exact.
- **Payee y** has x = L′_k. It reads the signature `σ = (L′_{k+1}, s′_k, s′_{k−1}, L′_{k−1}, ap(L′_{k+2}), ap(L′_{k−2}))`, which
  equals K without P:
  - L_{j+2} is the apex s′_k of y beyond (x, L′_{k+1}), so the payee reads it only as a class. That is why K carries a class
    there.
  - The payer's apex s_j is y's link letter L′_{k+2}.
- P is unseen. The payee credits `Z6[σ] ≥ z6[K]` for every P in 5..9 with (y, L_{j+1}, ·, P, ·, L_{j−1}) non-R6. This is the
  cand2 pattern, and a registry mask may come later as in filt16.

**Rows.**

| row | z6[K] | Z6[σ] (new, ≥ 0) |
|---|---|---|
| cons2 (L, s) of the payer | −1 per position j with key K | 0 |
| cons2 (L′, s′) of the payee | 0 | +1 per position k with signature σ |
| mrowZ (new), ≤ 0, dual ≤ 0 | +1 | −1: `z6[K] − Z6[σ(K)] ≤ 0` for every admissible P |
| senderR2, receiverR2, mrowR2, mrowL | 0 | 0 |

**Soundness.**
- Each transfer is one 6–6 edge, under a key the payer reads exactly.
- The payee credits at least the true inflow and must pass it all on. If it passes on more than it receives, it ends below 0,
  which is allowed.
- Bigs, fives, the window and the tail are untouched, because z6 never enters a receiver or sender row.
- **Separation stays exact:** cons2 is already separated exhaustively over all 1,424 6-words × 5⁶ apex words (`consall`). Each
  (L, s) row gains its six out-terms and six in-terms.
- `upperR2`'s conservation check needs the same terms.
- RSST's own values are 0.1 per drule3′ fit (a 6 next to a five, with a ≤ 6 next to that five, sending to a 6+ two steps on).
- Use cap 3 and penalty 1e−3, as for x and lq, so that z6 does not circulate around cycles of 6s.

**Pricing test for Opus** (rc = −(Σ w·coef)/tco; tco = 1 on cert_s28A60L).
- **Composite:** z6[K] with Z6 at its mrowZ minimum, so its coefficient is −1 at payer positions and +1 at payee positions
  with signature σ(K).
- **Hypothesis:** the cert is not valid for the `l6r` class.
- Of the 68 keys touched as payer, **22 price negative**, 19 at 0 and 27 positive (`price66.py`):

| K = (a, A1, P, A2, b, cr, cl) | rc | payer rows (w, positions) | payee rows in cert |
|---|---|---|---|
| **(5,5,5,7,5,5,5)** | **−13/20** | cons2 [5,6,5,6,5,9]/555555 (−5/16 × 2), [5,6,5,6,5,8]/555555 (−1/80 × 2) | none |
| (5,5,6,7,6,7,5) | −21/40 | the [5,5,6,6,7,6] / [5,6,6,7,6,6] family next to a 7 | none |
| (5,5,6,7,5,5,5) | −13/80 | [5,6,5,6,6,8]/555555 (−17/160), …/557557 (−9/160) | none |

- **Reading of the first key.** It is the d10's link 6 when its private is 5: neighbours u, three fives and the two apex 6s
  s_{i−1}, s_i. Here z6 sends to those apex 6s.
  - **Expected arithmetic:** 2 × (−5/16) + 2 × (−1/80) = −13/20.
  - The payee σ = (5,5,7,5,5,5) is an apex 6 of u with a five on each side of x. It has no cons2 row in the cert, so its
    weight is 0.

**Kill line.**
- **Priced:** every z6 composite has rc ≥ 0 on cert_s28A60L. Then the family is dead and no solve is run.
- **If priced negative, then solve.** Use 7360eb92 / argsA60 with the s28q flags + `l6r` (z6 cap 3, penalty 1e−3), warm from
  rows_s28A60, under the same keeppen → nosep → lowerR2 → upperR2 recipe and a 3 h cap. **Kill** if:
  - the gain over 47/320 (lower) and 0.147857 (upper) is under 0.005; or
  - z6 total weight is under 1e−3; or
  - upperR2's conservation check fails.
- **Expected outcome.** The payee 6-types with σ* become binding. They forward only to bigs at ring 3 of the d10 and must hold
  for every completion, so the gain may be small. This note does not predict t* ≤ 0.

**Required controls.**
1. **Flag off:** lowerR2 on cert_s28A60L returns VALID 47/320.
2. **Wiring:** the engine's generic ledger reproduces the −13/20 decomposition above. With the sign reversed (payer +1,
   payee −1) it must give +13/20.
3. **Physical test** (as §21.5): 100,000 random 6–6 edges with explicit rotations and a random reflection. The payer's K
   without P must equal the payee's σ read from (L′, s′), and the payer's P must equal y's true unseen vertex.
   - Required: 0 mismatches.
   - Broken control: the payee reads s′_k and s′_{k−1} swapped. It must show mismatches.
4. **Non-vacuity:** list the non-R6 payee 6-words with σ* = (5,5,7,5,5,5). At least one must exist; if none does, K* cannot
   occur and the pricing above is an artefact.

### C. `l3q` extended to 7 → 8 (drule9 toward an 8). Expected to die: price it, do not solve it

**Transfer.** As §21.1, with V = 8. Key (c, a, a2), payer U = 7 (the d7 rows), payee the d8 rows with mask on the 7's private.
RSST fires drule8/9 from the 7 into the 8 in binders 2, 4 and 5, so this loads the 8s.

**Hypothesis**, by the same composite arithmetic as round 1 (`price_q78.py`; masks from single-slot RSST kills, which do not
remove 6 or 8 at the relevant 7-privates):

| key | payer Σw | payee Σw (if a2 ∈ mask) | rc |
|---|---|---|---|
| (6,5,6) | −7/80 | −21/160 | **+7/160** |
| (6,5,8) | −7/160 | −21/160 | **+7/80** |
| (5,6,8) | −7/160 | −7/160 | **0** |

**Kill line:** rc ≥ 0 for all three is expected, and then no solve is run.

**Control:** a mask that drops a2 at every payee must turn the rc to −Σ payer w (−7/80, −7/160, −7/160). This shows that the
positive prices come from the 8-side credit and not from wiring.

If Opus finds any mask at the d8 binders that excludes 6 at a 7's private next to an apex five, rc(6,5,6) turns negative, and
this family deserves a solve.

## Summary of what to run

| item | owner | cost | expected |
|---|---|---|---|
| A. z6 pricing on cert_s28A60L (+ 4 controls) | Opus | minutes | rc(5,5,5,7,5,5,5) = −13/20 → solve |
| C. l3q8 pricing | Opus | minutes | all rc ≥ 0 → dead |
| 8406.123 on kc/cfast | reducibility lane | minutes | if C2cons, the d8 binder 75666556/66666565 dies |
| 2.126 conservative-X admissibility | reducibility lane | open | single lever under the −5/16 weights and the 15/64 sender |

Scratch only, not committed (session scratchpad `scripts/`):
- `face7b.py`: the round-1 scorer with the degree-9 cap;
- `ledger2.py` and `ledger3.py`: ledgers and the RSST-filtered ledger;
- `reqs.py` and `slotkill2.py`: embedding requirements tagged with k44 verdicts;
- `sctx.py`: the sender-context check;
- `price66.py` and `price_q78.py`: composite pricing on the cert.

Our-LP ledgers come from the s28q engine `rowR2` at sol_s28A60.json.
