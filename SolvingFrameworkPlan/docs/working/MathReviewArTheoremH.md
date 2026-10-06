# Independent review: Theorem H (MathRadiusGeometry.md) and Long Table's A_r structure results

Reviewer worker, 6 October 2026. I did not write these claims. Hand re-derivation of every step plus my own code (`rev.py`, `steps.py` in the session scratchpad; own graph builder, own DL/F/Kempe code, exhaustive over all colourings, canonical ring 0, r = 3..9, about 3 CPU-min total). No file of others edited, nothing committed.

## A. Theorem H

Verdicts per statement.

1. **Step 1 (DL forces ring-1 pattern R1/R2/R3): CORRECT.** Each deduction rechecked: {w0,w1} = {g,d} from the leaving edges of P1, P2 (x_1's non-link neighbours are only w_0, w_1 because x_1 has degree 5); b in {w2,w3} and b in {w3,w4} from the entering edges (degree 5 of x_3, x_4); the case analysis gives exactly R1 = (g,d,b,a,b), R2 = (d,g,b,a,b), R3 = (d,g,d,b,g). Computed: all DL states of A_3..A_9 have exactly these patterns (counts for r=3..7: 30, 80, 530, 2450, 13300 DL classes, all three patterns only).
   Assumption not spelled out: the w_t are five distinct vertices and w_t ~ w_{t+1}. This follows from planarity plus degree 5 of every x_t, and distinctness needs no vertex of degree 3 / no separating triangle (true under the min-degree-5 setting). Fine, but it should be stated as a hypothesis.
2. **Step 2 (R2: F(s) is not DL): CORRECT.** w_1 = g is adjacent to x_2 = a so it is in K_F and becomes a; x_2 (now g) has neighbours b, a, a, b (and v): no d, so lock 2 of F(s) (path from x_4 to x_2 in {d,g}) fails. Uses degree 5 of x_2 only. Computed: R2 -> non-DL for all R2 states, r = 3..7 (320, 1680, 8800 at r = 5, 6, 7).
3. **Step 3 (R3: one swap breaks the lock): CORRECT, and it is a legal single whole-component swap.** The {a,b}-component of x_1 is exactly {x_0,x_1,x_2} (its non-link neighbours w_4,w_0,w_1,w_2 are g,d,g,d; degrees of x_0,x_1,x_2 are 5), so "recolour a,b,a to b,a,b" is the whole-component Kempe swap, not a composition. In s' = (b,a,b,g,d) x_3 has no a-neighbour, so lock 1 (now an {a,g}-path) fails; s' still has 4 link colours, so a further swap fills. Computed: K has size 3 and s' is non-DL for every R3 state, r = 3..7. Nothing beyond ring 1 and the degree of x_3 is used.
4. **Step 4 (F(R1) is non-DL or has pattern R3): CORRECT.** Link of F(s) = (a,b,g,a,d), repeat index 3, relabelling gives (alpha',beta',gamma',delta') = (a,d,b,g); ring read from w_3 is (g,b,g,d,b) = (delta',gamma',delta',beta',gamma') = R3. I recomputed this relabelling by hand and by code (r = 3..7: F(s) differs from s on exactly x_2, x_3, w_3, and when DL has pattern R3 in 10, 10, 60, 200, 1000 cases; the rest non-DL).
   Imprecision (not a gap): the Verdict item 1 says the proof uses "no lock path beyond its first and last vertex". Step 4 does use the existence of P2 as a Jordan curve (v, x_1, P2, x_4 is a {b,d} cycle separating x_0 from x_2,x_3), to prove x_0 is not in K_F; this is needed because w_0 may have further neighbours outside ring 1 whose degrees are unconstrained. The use is legitimate (planarity, P2 exists by DL, only its colours matter) and uses no A_r structure, but the sentence should read "uses only the existence of P2 as a separating curve". Also note that only the ring-1 colours of F(s) matter for the R3 conclusion, so F(s) need not even be known to be DL.
5. **Theorem H (radius <= 3 for every DL state at a degree-5 vertex with five degree-5 neighbours; <= 2 unless R1 with F(s) DL): CORRECT.** The bookkeeping radius <= 1 + d(s, non-DL) is valid because from a non-DL state with four link colours one swap of the failing pair's component fills (the only link vertices of the two colours are the two endpoints). Exhaustive recomputation of d(s, non-DL) by BFS: A_3: radius 3 for 10 of 30 DL classes, all others radius 2; A_4..A_9: radius 2 for all 80, 530, 2450, 13300, 68390, 360090 DL classes. Hidden uses of A_r structure or of degrees beyond ring 1: none beyond the Jordan-curve remark above. The claim "radius <= 3 on A_r for every r" is therefore a theorem, independent of r. Not rederived: the 50 flipped-graph test (script `thmH_independent_check.py`, 420 s limit) and T4 (section 4); UNVERIFIED by me, but not needed for the proof.
6. **"Infinite orbits are harmless / every second state breakable": CORRECT** (follows from Steps 3, 4: types alternate R1, R3 and R3 is one swap from non-DL).
7. **"Radius exactly 2 for r >= 4" (a computed claim, not part of Theorem H): CONFIRMED computationally** for r = 4..9 (every DL class), still not proved for all r, as the document says.
8. Section 4 (T4) and section 3 claims about holes with a degree-6 neighbour: UNVERIFIED (not examined).

## B. Long Table's A_r results

1. **Lemma A (equivariance): CORRECT.** Orientation-preserving automorphism fixing v and colour renamings commute with the DL test and F. (Also my code found F^4 s = pi s sigma_3 for all infinite classes, which uses the same equivariance.)
2. **Lemma B (closing criterion): CORRECT as a conditional statement.** F^{4+n} s = pi F^n(s) sigma by Lemma A, then induction; F^{4k} s = pi^k s sigma^k, sigma^5 = id (rotation by 15 = 0 mod 5), pi^15 = id for a 3-cycle, so raw period 60. Convention check j(s sigma_3) = j - 3 = j + 12 mod 5: fine. The content lives in the hypothesis F^4 s = pi s sigma, which is only computed. Lemma B says nothing about existence for general r.
3. **r = 2 has no first lock (hand proof, section 3 of a-structure.md): CORRECT.** Recomputed the allowed sets for w_0..w_4 and both cases; in the case (w0,w1) = (g,d) ring 1 uses four colours so the cap has none; in the other case the two sub-cases give an isolated x_3 or a component {x_1,w_1}. Computed as well (my code: no DL state at r = 2 is implied by their count; I did not rerun r = 2 separately, but the hand proof is complete).
4. **Census (infinite-chain classes), my own recomputation, all proper colourings with a 4-coloured link, ring 0 canonical, exhaustive:**

| r | states | DL | infinite classes | 20 J_(r-2) |
|---|---|---|---|---|
| 3 | 60 | 30 | 20 | 20 |
| 4 | 320 | 80 | 20 | 20 |
| 5 | 1680 | 530 | 60 | 60 |
| 6 | 8800 | 2450 | 100 | 100 |
| 7 | 46080 | 13300 | 220 | 220 |
| 8 | 241280 | 68390 | 420 | 420 |
| 9 | 1263360 | 360090 | 860 | 860 |

   CORRECT for r = 3..8 (agrees with Long Table: 20, 20, 60, 100, 220, 420). **New: r = 9 gives 860 = 20 J_7 (J_7 = 43), which Long Table did not compute and which matches the Jacobsthal formula as a prediction.** Direct DL counts also agree with Math's (30, 80, 530, 2450). For every infinite class at every r = 3..9, F^4 s = pi s sigma_k holds with k = 3 only (so C1 holds through r = 9). I did not check "pi is a 3-cycle" or period 20; not needed.
5. **Dependence on r = 3..5:** the claims about all r are NOT proved by anything in these documents: Conjecture J (walk on K3, count 4 J_(r-2) >= 1), existence of an infinite orbit for r >= 9 (they say so) remain [conjecture]. After my run the data support the Jacobsthal count and the Lemma B hypothesis through r = 9, so they no longer rest on r = 3..5, but it is still finite evidence. The part of A-structure's text that is a theorem for all r is: Lemma A, Lemma B (conditional), r = 2 non-existence, and, from Theorem H, radius <= 3.
6. **Radius statements** ("exactly 2 on A_4..A_8 for every colouring"): CONFIRMED by BFS for every DL class (not only the infinite ones), r = 4..9. The A_3 value 3 for 10 of 30 DL classes confirmed (Long Table tested only 4 colourings).
7. **Small slip in a-structure.md, section 1:** "the graph was checked equal to A3_FACES with ring i vertex t = 1+5i+t": consistent with Math's builder; no discrepancy found. Header counts "colourings with 4-colour link (x0 = 0)" 60, 360, 1920, 10080, 52800, 276480, 1447680 equal 6 x my canonical counts for r = 2..8 (60 at r=2 I did not rerun; r = 3..8 match).
8. **Not verified:** the K3 layer / window-2 locality claims (r = 4..8), the delay-line observation, the 95 s run times; none enter Theorem H.

## C. Bottom line

Theorem H: no gap found; the only edit I would ask for is the sentence about lock paths (P2 existence is used as a Jordan curve) and an explicit hypothesis that the w_t are distinct (no separating triangle). Long Table's Lemma A, B and r = 2 argument are correct; their all-r claims (existence of infinite orbits for every r, Conjecture J) remain open, with new supporting data at r = 9.
