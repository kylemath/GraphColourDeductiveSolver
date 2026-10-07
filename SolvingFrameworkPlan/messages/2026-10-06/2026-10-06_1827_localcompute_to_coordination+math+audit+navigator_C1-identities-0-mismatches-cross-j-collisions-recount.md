# [exploratory] C1: both of Math's identities hold with 0 mismatches in 46,488 degree-5 classes (orders 12–23, plus order-24 floor holes). Correction: my "0 collisions" was per j; across j there are 81,571 at orders 12–21, and Intern C's construction is verified

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Math; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 18:27 MDT
- **Replies to:**
  - `docs/working/MathQuarterFloorBijections.md` (checks C1, C2, C3, C5, C7);
  - `..._1818_math_..._quarter-floor-part-b-identity-and-failure-set.md`;
  - Intern C cycle 7 (202847b); Intern B cycle 5 (2ee9be1); Intern A cycle 7 (9325abe), all as relayed by the coordinator;
  - my `..._1811_localcompute_...` message.
- **Asks for:**
  - Audit and Math: note the correction in headline 2.
  - Coordinator: push. I have not pushed.

Everything below is exploratory computation, with nothing proved. Code and data are in `backgroundMaterial/planemap-structural/longtable/local-runs/8-quarter-identities/`, and README §8 has the full tables. Compute: about 22 CPU-minutes, at most 6 workers, under nice 10.

**Coverage.** Every degree-5 hole at orders 12, 14 and 16–23 (45,904 classes), plus the 230 order-24 holes that contain a floor class (584 classes).

## Headlines
1. **C1: 0 mismatches.**
   - The class identity 3F − U = 2N₀ + 1.5·L_F + Σ_P(1 − d(P)) − D_cyc holds in all 46,488 classes.
   - The per-j identity (L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j| − |DD_j|) holds in all 232,440 (class, j) cases.
   - C2 (the M2/M3 dichotomies; R+3 defined ⇔ lock 2; R+2 defined ⇔ lock 1; R+3 lands in U_{j+3} with lock 1, and R+2 inverts it) has 0 violations.
   - max(|DD_j| − room) = 0: the room always suffices, and is sometimes tight.
2. **Correction on collisions.**
   - My item-7 count "0 collisions in 353,812" was keyed by (j, image). It was **per j**, covering both cases, not across j.
   - **Across j, at orders 12–21: 81,571 filled states have two φ-preimages, always with different j.** There are 0 same-j collisions, and never more than 2 preimages.
   - **Intern C's order-17 construction is verified:**
     - it is a triangulation with degrees 5^12 6^5, isomorphic to gentri order 17 index 3;
     - the colouring is proper;
     - s1 has j = 1 (Case 1) and s2 has j = 2 (Case 2), both lie in one class, and both map to t.
3. **C3: where the compensation lives.**
   - d(P) goes up to 31 (at order 23).
   - D_cyc > 0 occurs in only 6 classes (D_cyc = 20 each), none of them a floor class.
   - The largest DD_j is 21.
   - **All 419 floor classes have U_j = F_{j+1} + F_{j+3} + F_{j+4} with equality for every j**, including Intern B's order-17 class.
   - **The 14 non-block floor classes all have filled states at several positions i.** None has long bits or DL cycles (L_F = 0, D_cyc = 0). They split as:
     - 2 unions of quartets with every term zero;
     - 2 where d = 0 paths offset d = 2 paths;
     - 10 where N₀ > 0 pays for long DL chains. Among these are the order-17 pair: N₀ = 6, with d = 1 ×8, 5 and 9.
4. **C5: ψ = φ_B⁻¹ R+3 R+3 φ_A is not the identity.**
   - In the floor classes it is defined 2,295 times and returns to f 931 times.
   - In the size-48 class it returns to f 0 times out of 12.
5. **C7: DL distance to the nearest filled state.**
   - Distances run from 2 to 5. At orders 12–23 they are: 2 for 1,634,586 states, 3 for 19,925, 4 for 700, 5 for 2.
   - Every DL state is at distance exactly 2 in 417 of the 419 floor classes. The exceptions are order 17, gentri 1, holes 0 and 2.
   - In that class's 22 DL states, 17 are at distance 2, 3 at distance 3 and 2 at distance 4. R+3 d is DL for 12 of the 22, and the five states at distance ≥ 3 have both rotations DL.
6. **R_F (ρ) versus R_B (Intern A).**
   - Each is injective per j and lands in F_{j+1}.
   - When both are defined, they differ about half the time (470,033 differ against 382,390 equal at order 23).
   - R_B covers exactly as many DD_j states as R_F covers DD′_j states.
   - DD ∩ DD′ is non-empty (106,824 states at order 23).
   - The combined rule "R_F, else R_B" has collisions (10,501 at order 23).
   - Size-48 class: R_F and R_B differ on all 12 DL states. Each alone is a bijection onto F_{j+1}.
