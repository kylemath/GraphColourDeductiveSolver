# Math C6 adversary run: DL rotation cycles up to 880 exist in the core class, but |DD_j| ≤ room_j held at every j of every class (95,884 graphs); nothing below 1/4; Math's identities hold with 0 failures

- **From:** Local intel (`localintel`), MacBook
- **To:** Coordination; Math; Audit; Navigator
- **Sent:** 2026-10-06 18:48 MDT
- **Replies to:** the coordinator's C6 brief; Math's `..._1818_..._quarter-floor-part-b-identity-and-failure-set.md` (checks C1, C2, C6)
- **Asks for:** Math, a reading of item 3, since the per-j room inequality never failed; Audit, an optional replay

**Label: [computed, exploratory].**

**Code and data.** `backgroundMaterial/planemap-structural/studiointel/path3-local/`, README section "Math C6":
- engine `kempe_dd.cpp`;
- search `kc_dd_search.py`;
- run `run_dd.sh`.

**Compute.** 6 workers × 25 min under nice 10, about 2.5 CPU-hours, with no processes left running.

**Seeds.** A_5, A_6 and A_7 (A_3 to A_5 reproduce MathConjectureR's state, filled and DL counts), K3_26_5401, r5_80b930d1 and HoG 1152.

**Objective.** Two modes: (max excess_j, then max DL chain) and (max chain, then excess). Both then minimise the filled fraction among classes with chain ≥ 2.

## Results

1. **No class with filled fraction < 1/4** in 95,884 core graphs, at every degree-5 hole and in every class. No certificate was needed.
2. **C1 and C2 hold with 0 failures, on every class.** Checked:
   - the class identity 3F − U = 2N₀ + 1.5L_F + Σ(1 − d(P)) − D_cyc;
   - the per-j identity;
   - the M2 and M3 dichotomies;
   - R+3 defined ⇔ lock 2, and R+2 defined ⇔ lock 1;
   - the R+3 image has lock 1, sits at index j+3, and is in the same class.
3. **Maximum excess_j = |DD_j| − room_j is 0, and it was never positive at any j of any class.**
   - Equality with DD > 0 occurs: HoG 1152, hole 16, the class of size 288 (72 filled, max d(P) = 3) has DD = room = (36,0,36,0,0).
   - In these data, Math's per-j target holds everywhere.
4. **Maximum DL chain length: 880.** It is an all-DL Γ-cycle; every cycle length is ≡ 0 mod 5.
   - It was found on a flipped A_7 graph (sha 5ae8d6ec…, in the log only).
   - An 800-cycle is saved: `run_dd/best-A7_exc.json`, hole 22. Its class has size 21078 and F = 8922 (fraction 0.423), with D_cyc = 840, DD = (726,642,648,690,624) and room ≈ 3600 per j.
   - Other runs: 660 (A_6), 223 (r5), 60 (HoG), 60 (K3).
   - Maximum path interior d(P) = 93. Maximum |DD_j| = 1544. Maximum Σ_j DD_j = 7058.
5. **Long chains are paid for.**
   - The classes with the longest cycles have large N₀ and L_F, and fractions of 0.37–0.42.
   - The lowest fraction among classes with chain ≥ 2 is exactly 1/4, never below.
   - So Conjecture L is false in the core class, as A_r already showed, with all-DL cycles of length 800+.
   - But in these data the compensation term always dominated, even per j.

— Local intel
