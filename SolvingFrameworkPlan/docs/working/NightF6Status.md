# Theorem F6: status at 04:05 MDT, 7 October 2026 (updated 04:45 with the log entries through Job AZ and QuarterLemmaP)

Status page for the night's F6 programme. Everything below is taken from `NightLog-2026-10-06.md` and the Night notes it cites; nothing here is new mathematics. Labels: **formal** = in Lean, 0 sorry, standard axioms (coordinator recompile); **hand** = proved by hand in a Night note (unreviewed unless stated); **data** = Studio or local computation, with the exact count; **killed** = refuted, reason on record. All Night notes are exploratory (Night swarm outputs: leads, not evidence, until re-checked).

## 1. Statement and why it matters

**Theorem F6 (target):** at a degree-5 hole of a core triangulation whose link vertices have degrees (5,5,5,5,6) (in cyclic order, up to rotation and reflection), every Kempe class has Σλ ≤ 0, i.e. at least a quarter of its states are filled (F ≥ |class|/4). The chain is: SigmaUnionC (join π-cycles by σ- and σ′-links; Σλ ≤ 0 on every group) ⇒ the quarter floor ⇒ R\* ⇒ 4CT. F5 (the same floor at (5,5,5,5,5) holes) is **formal** (`quarterFloor_of_fiveLink`, `QuarterFloorHBridge.lean`) and is the base case of SigmaUnionC. F6 is the next pattern: the first one where F5's charging fails (174/400 DD steps lack the exit) and the pattern is only F6-type (needs the 3·#τ term; Job D, 112 link patterns, orders 24–26; confirmed at order 27: 31 F5-type, 14 F6-type, 80 need E₂). Status: **not proved**. The reduction below is exact; two lemmas remain, and both are Γ-closure statements.

## 2. Proof architecture

```
F6 at (5,5,5,5,6)        [floor on every class]
 └─ σC on every σ-group  [QuarterAssignment: sigmaC_of_assignment_groups; QuarterSigmaGroups]
     └─ group flow identity   Σ_g λ = Σ_{Z>0} def(Z) + Σ_{T≤0} rem(T)   [FORMAL: QuarterFlowIdentity.flow_identity]
         ├─ Γ-cycles (all-DL π-cycles; debtors, no filled state, rem = Λ for sinks)
         │    └─ Lemma S_Γ: lockless σ-exits cover the debt D = L on every Γ-cycle
         │         │  credit of a hit = 3f − 1 = λ-mass of the hit excursion  [FORMAL: QuarterExcursion]
         │         │  arithmetic: 5s₃ + 8s₄ + 2a₀₁₂ ≥ L   [hand, NightF6Flow §1, with the F₄ caveat]
         │         └─ over the universal 10-step period [FORMAL: QuarterGammaPeriod.gamma_period_ten]:
         │              A₃₄′  (k = 3, 4 side: never two consecutive step-8 breaks)   OPEN
         │            + W2    (k ≤ 2 side: not all of R3k2, R3k1, R3k0 σ-fixed)     OPEN
         │            + W4 / F₄ caveats (F₄ is FALSE once at order 27: k = 4 credit ≥ 2, not 8)
         │            (Lemma W = one window credit ≥ 10 replaces A₃₄′ + F₀₁₂′; W1 + W2 + W4 + F₄ ⇒ W)
         └─ non-Γ positive cycles
              └─ charge-back P₁ (rem > 0 charged back to hitting sources; each def′ > 0 assigned
                  to ONE nonpositive σ-neighbour with rem < 0)   [data, 0 failures; formal certificate]
                  reduces to P₁^str (every positive Z has a σ-neighbour T with −rem(T) ≥ 5w(Z))   [hand + data]
                  P₁ on non-Γ cycles is vacuous in a minimal counterexample (NightP1): the 4CT-strength of F6
                  sits entirely in Lemma S_Γ.
```

The two open lemmas are the only places where the closure of the orbit (an all-DL cycle never leaves DL) enters. Everything else on the tree is formal, hand-proved, or data with 0 failures.

## 3. Named statements

| Statement | Status | Where |
|---|---|---|
| Lemma A (Kempe single swap lands in a filled state, injective) | formal | `QuarterFloor.lean` `lemmaA` |
| Rotation bijection R₊₃/R₊₂, planarity discharged, Hex dichotomy | formal | `QuarterRotation`, `QuarterRotationPlanar` |
| No doubly locked state is frozen | formal | `NoFrozen.lean` |
| Lemma Π (π permutes every Kempe class) | formal | `QuarterPi.lean` |
| Theorem W (3F − U = −5·winding; 5 ∣ 3F − U; floor ⇔ Σλ ≤ 0 per class) | formal | `QuarterWinding.lean` |
| Theorem F5 (floor at (5,5,5,5,5) holes), from triangulation + degree-5 link | formal (hand review: PASS, `NightF5Review.md`) | `quarterFloor_of_icoBall` (`QuarterFloorH`), `quarterFloor_of_fiveLink` (`QuarterFloorHBridge`) |
| Exact class identity Σλ = \|DD\| − 2N₀ − E₂ − 3#τ | **formal**: `exact_identity` / `exact_identity_class` (93ec143), from the pointwise `lam_eq_exact`; also data: 0 failures (Job D, ~4.2M classes; reviewer's script on 270 holes) | `QuarterLemmaP.lean`; F5 review, Job D |
| Lemma 3′ (exact σ-exit condition, (w₀,w₁,w₂,w₄) = (B,A,B,A)) | formal | `QuarterSigmaExit.lean` |
| σ-exit criteria at k = 3, 4 (never DL; lockless ⇔ reachability; f ≥ 2 at k = 3) | formal (f ≥ 2 at k = 4 NOT proved, false by Job R) | `QuarterSigmaK34`, `QuarterJordanDual` (`sigma_exit_f_ge_two_k3'`) |
| Jordan duality (D) at k = 3, 4 | formal | `QuarterJordanDual.lean` |
| One-question lemma (lockless ⇔ y ~ z in {c(y),c(z)} ⇔ pm bridge) | hand; data 280/280 (Job N); formal as `k4_exit_period` / `J_iff_*` for the period form | NightF6Flow §2.1; `QuarterPeriodJ`, `QuarterLockJ` |
| Universal 10-step period of a Γ-cycle | formal (`gamma_period_ten`); data 140/140 and 412/412 periods (Jobs O, R), 406/406 at (5,5,5,5,7) (Job AC) | `QuarterGammaPeriod.lean` |
| Period lemma for J (J changes only at steps 0, 1, 3, 8; k = 4 failure ⇔ step-8 break) | formal | `QuarterPeriodJ.lean` |
| Lock-membership form of J (Lemma 5.1) | formal | `QuarterLockJ.lean` |
| Exact excursion accounting (credit 3f − 1 = λ-mass; no double hit; σ involution) | formal | `QuarterExcursion.lean`, NightLemmaR |
| Group flow identity; σC from def ≤ 0 and rem ≤ 0 | formal | `QuarterFlowIdentity.lean` |
| σC from a charge-back single-target assignment (certificate), and P₁^str form | formal | `QuarterAssignment.lean` |
| Lemma Fix (σ fixed ⇔ {A,B}-subgraph a forest) at R3, k ≤ 2 | formal | `QuarterSigmaFix.lean` `lemmaFix` |
| Fan lemma; W2′ ⇒ W2 in lean form (y or z has an α/μ-neighbour outside K_σ) | formal; W2′ itself open | `QuarterFan.lean`, `QuarterW2Frame.lean` |
| Six-pair Euler identity (Σ rank = Σ components − 8; ΣC ≥ 8 at DL states) | formal; data 0 failures on ~635,000 states | `QuarterEuler.lean` |
| Mirror reverses π on DL states (Γ-cycle time reversal) | formal; data 1,364/1,364 Γ-cycles (Job AJ) | `QuarterMirror.lean` |
| Window bookkeeping, step 8 far, pocket and window lemmas | formal (`bookkeeping`, `step8_far`, `window_forced`, `k4_failure_iff_z_split`, `k3_failure_iff_y_split`, 80f22dd); data: window partition 0 exceptions (Job AM: {y w₂ z} ×533 / split ×19 at degree 6, 837/79 at degree 7) | `QuarterWindow.lean`; NightA34 §1–§3 |
| Conjecture Σ (after a double break the step-0/1 far swap recolours the first break's gate) | killed: holds in 36/73 open double breaks (predicted 73/73) and after 18/19 single breaks (predicted mostly empty); not the Lock2-killing mechanism | Job AM |
| No separating potential (20 potentials on 670 Γ-records, 54 rebuilt Γ-cycles, 318 open runs) | data: none decreases over every window with a step-8 break; obstruction in §4 | `NightPotential.md` (5e49e39) |
| ρ = σ^{L/10} (colour rotation per period) | formal: `period_colour_rotation`, `closing_perm` (π^L s = s ⇒ 30 ∣ L for a colouring-closed orbit; a Γ-cycle of canonical states with L ≢ 0 mod 30 lifts to a colouring orbit of length 3L; db5ce19). Data: 2,728 Γ-cycle records, orders 25–27: ρ a 3-cycle for L = 20 (2,544) / 40 (136), identity for L = 60 (48) | `QuarterWindow.lean`; Job AN |
| Γ-cycle length L | data: only 20 (2,566), 40 (136), 60 (48) over ALL core triangulations of orders 12–27 (Job AO), but **not a law**: adversarial graphs have L = 800 (A7), 660 (A6_chain), 80, 60 (Job AQ). NightGammaLength (f3637ef): L = 10m, ρ = σ^m proved by hand; 20 ∣ L is a CONJECTURE (0 exceptions, 2,750 cycles + A7); L ≤ 60 killed | Jobs AO, AQ; `NightGammaLength.md` |
| Lemma chain beyond the census (Job AQ, with Studio correction) | data: on adversarial Γ-cycles (A6_chain, A7_exc incl. L = 800, hog1152, r5; both orientations) Lemma S holds with C_pos = 0 and C_neg/D = 4.0 exactly on all (5,5,5,5,5) and A7 cycles (r5: 2.0 and 4.0), universal period on all 80 periods of L = 800, A₃₄′, W2, σC, σ′C, charge-back P₁ 0 failures, floor on every class. **No adversarial graph has a (5,5,5,5,6) hole with a Γ-cycle**, so this is not a degree-6 test (Job AS is building one) | Job AQ |
| z's split component avoids the hole; a far vertex is needed | formal: `zsplit_no_hole_vertex`, `zsplit_hole_boundary`, `gate_swaps_miss`, `xplus_cannot_heal`, **`far_vertex_needed`** (1334936); NightA34 §7.1 | `QuarterZsplit.lean` |
| Long degree-6 Γ-cycles (Jobs AS, AT) | data: A7_exc plus edge flips give (5,5,5,5,6) holes with L = 80 (17 variants), 120, 180, 200 (40 constructions, L = 40–200); every Γ length a multiple of 20; Lemma S C_pos = 0, C_neg/D 2.45–3.87; universal period; **no k = 3/4 failures at all**; W2, W2*, σC, σ′C, P₁, floor hold. Chain survives; A₃₄′ is not stressed there | Job AS |
| Cut parity (even-cut lemma; 20 ∣ L) | formal: `closed_orbit_cut_sum`, `piMove_cut_sum`, `allDL_ring_cut_count` (each of the 22 ring edges cut exactly 4 times per period), `relabel_closed_cut_sum`, `three_cycle_cut_nonempty` (de98be8, c723a31). Data (Job AT): every edge cut an even number of times over a closed cycle (2,728/2,728 + 26/26); D_b (far edges cut an odd number of times in period b) nonempty every period (|D_b| 8–36), identical across periods in 2,548/2,728; **XOR of D over any odd number of consecutive periods never empty (0 records)** ⇒ 20 ∣ L in all data; why is open | `QuarterEvenCut.lean`; Job AT |
| A₃₄′ at degree 6 is a two-period (L = 20) statement | data (Job AU): census 256 Γ-cycles at L = 20, 4 at 40, 4 at 60; all 19 k = 4 and all 19 k = 3 failures are on L = 20 cycles (18 cycles fail k = 4 then k = 3 two steps later; one each only at k = 4 / only at k = 3); the 40 AS constructions and L = 40/60 census cycles have none; 32/256 L = 20 cycles at holes with a reflection automorphism, 8 time-reversal symmetric, none of those 8 breaks; all 19 breaking cycles at holes with no reflection; the breaking period is the one with larger \|K(p)\| in 18/19 (exception p25m #16945 h3: 9 vs 10) | Job AU |
| Step-8 component K₈ ⊇ {x₂, x₃, w⁺}, avoids {p, m, y, z} | formal: `K8_contains_x2_x3_wplus`, `K8_avoids_pmyz`, `K8_meets_hole_exactly` (hole ∩ K₈ = {x₂, x₃, w⁺}), `consecutive_K8_share_hole` (0afc704); data 896/896 periods (Job AV). K₈ ∩ K₁₈ never empty (always ⊇ {x₂,x₃,w⁺}, always a far vertex too), carries no breaking signal | `QuarterK8.lean`; Job AV |
| Job AV two-period dump | data: `jobav/jobav-cycles.jsonl`, 304 degree-6 Γ-cycles (256 at L = 20, 4 at 40, 4 at 60, 40 constructions), all replay and close with 0 errors; step-8 break in period b ⇔ k = 4 failure at R3k4 of b+1; k4fail = k3fail in every period except p25 #16945 h3 | Job AV (41c9496) |
| Lemma P (lock type fixes place in the unfilled run: DL interior, Lock2-only start u ≥ 2, Lock1-only end u ≥ 2, lockless u = 1) | **formal**: `lemmaP`, `lemmaP_excursion`, `unfilled_succ_iff_lock2`, `unfilled_pred_iff_lock1`, `dlState_iff`, `noLock_iff` (93ec143); hand proof in NightSigmaImage 182d62a | `QuarterLemmaP.lean` |
| Γ-only equivalence: a k = 3 or k = 4 failure in a period ⇔ σ fixed at R1k1 | data, **not exact** (Job AY): 550/552 degree-6 census periods (the 2 exceptions are p26 #87942 h22: k = 4 and k = 3 failures with no position-1 fixed point); degree 7 858/916; fails on open windows (114/482). Job AZ: in the exception the failing period's R1k1 σ-image is DL (a DL state on another cycle), so "fixed" was a proxy for "σ-image locked". The faithful statement remains the break/J one. Structure retained: the σ pair at each position is forced (1:12, 3:13, 4:12, 5:14, 6:13, 7:12, 8:14, 9:13 in the p=1, m=2, y=3, z=4 frame); positions 0 and 2 are never fixed; 19 distinct 10-bit fixed-point patterns at degree 6 (0000000000 ×374); no consecutive position-1 fixed points, W2/W2* hold in all 896 periods; degree 7: 20 consecutive position-1 fixed pairs, A₃₄′ fails on 7/406 cycles, W2 and W2* fail in 14 periods each | NightSigmaImage; Jobs AY, AZ |
| Conjecture U34 (u ∈ {3,4}, u = 4 ⇒ f = 1 at a k = 4 failure image) | data: 0 exceptions, 2,847 states (local) | NightSigmaImage |
| 20 ∣ L reduced to the u* alternation (NightCutParity) | reduction proved (S_b = A_b △ A_{b+1}, ω = α in every swap; XOR of D over b..b+k−1 empty ⇔ A_{b+k} = A_b); **alternation killed by Job AX**: u* in exactly one of K₀, K₇ in 728/896 degree-6 periods (census 384/552, constructions 344/344), failures always "neither"; A_b never recurs at odd distance in any cycle at any pattern, so 20 ∣ L holds in data; **parked as a conjecture** with the exact reformulation A_{b+k} ≠ A_b for odd k, no single-vertex mechanism | NightCutParity (11fac71); Job AX (9e26749) |
| Lemma S_Γ (lockless σ-exits cover D on every Γ-cycle) | data only: 0 failures, min C_neg/D = 1.55 (62 + 6 records, 25–26; Job L), 1.95 at (5,5,5,5,6) order 27 (202 records); all-DD-endpoint form min 1.8–2.0 (Job Z) | Jobs L, R, Z |
| A₃₄′ (no two consecutive step-8 breaks on a Γ-cycle) | **open**; data: 0 double failures on Γ-cycles at 25–27 (73 double failures on open runs, none closed: Job X), 62/62, 230/230; |R_b| = 2 at every degree-6 break (Job AM) | §4 below |
| W2 (not all of R3k2, R3k1, R3k0 σ-fixed on a Γ-cycle) | **open**; data: 0/552 Γ periods (Job AH), W2*, W2″, R 0 failures on Γ periods (Job AK) | §4 below |
| Lemma W (window credit ≥ 10) | open; data: 0 failures in 12+12, 58+58, 206+206 Γ windows (Job W/AA); false on open runs (credit < 10 in ≈ 510 of 1,946 windows at order 27) | Job AA, NightF012 |
| F₄ (f = 3 at every k = 4 lockless exit) | killed: fails once (p27 #133619 h21, 2 of 400 exits f = 1); gap located by Job U (isolated K_σ, M3 short); replace by credit ≥ 2 | Job R, U |
| F₀₁₂′ (k ≤ 2 credit ≥ 7L/20 per cycle) | per-cycle average only (min exactly 1.000 at p25m #16945 h3, p27 #273919 h26); per-period forms killed (13/140, 11/412 fail) | Jobs P, R; NightF012 |
| Lemma R (target remainder ≤ 0) | killed: fails at order 27 (12 of 732 hit nonpositive targets, all at (5,5,5,5,6)); replaced by charge-back | Job S, NightLemmaR |
| Charge-back P₁ (def′ > 0 assigned to one nonpositive neighbour) | data: 0 failures at every hole, orders 25–27, both orientations; also (5,5,5,6,6); fails at 19 holes of other patterns for σ-only, σ∪σ′ 19/19 (Job AF) | Studio fbc093c, 9185ca4; Jobs Z, AF |
| P₁^str on non-Γ positives | data 407/407 holes at (5,5,5,5,6) and (5,5,5,6,6) (Job AF); 246/246 at 25–27, 209/209 at ≤ 24, min ratio 1.25 | NightP1; Job AD, AF |
| σC at (5,5,5,5,6) and three-consecutive-5s | data: 0 failing groups among ~7.5M (Job E); universal σC FALSE once (p26 #70869 h11, ~114M groups, Job F) | Jobs E, F |
| σ′C / SigmaUnionC | data: 0 failing groups, ~100M at orders 24–26, ~368M at order 27 (Jobs H, J); formal statement and F5 base case | `QuarterSigmaPrime.lean`; Jobs H, J |
| Transport T | data: holds at all positive holes (Hall ratio ≥ 3 adversarial, 35,701 at ipr #265); unproved | Jobs B, C; W7/W8 |
| Conjecture P ("no positive cycle" in configuration-free graphs) | killed: 32 positive holes in 28 IPR graphs; second regime at n = 58, 60 | Studio IPR, bigsample |
| C1Γ, Conjecture G (as universal), per-block Lemma S, excursion self-payment, Lemma R per target, per-cycle bounds | killed (Jobs E, G, M, AB, S; NightFloorHP2) | Night log |

## 4. The two open closure lemmas

**A₃₄′ (k = 3, 4 side).** *Reduction achieved* (all formal unless noted): on an all-DL orbit at a Hole6, a k = 4 failure is exactly a step-8 break of J = "y ~ z in {c(y),c(z)}" (`k4_failure_iff_break`); J changes only at steps 0, 1, 3, 8 (`period_J`); every break is undone by R3k2 (NightLemmaS §0, formal in `QuarterPeriodJ`); J is a lock-membership question at R1k2, R3k4, R3k3 (`QuarterLockJ`); step 8 is far (NightA34 §2.1, hand); window lemma (DL forces y ~ w₂ at positions 9, 0 and z ~ w₂ at 2, 3; hand). So **A₃₄′ ⇔ "the R3k0 swap never breaks J in two consecutive periods"** and Job AE data say: after a break z re-enters the Lock2 witness two states later (98/98; the probe `QuarterRestore` shows this particular fact carries no information), and one period later 19/19 at degree 6 (65/79 at degree 7).
**Killed routes:** every healing-gate route (NightA34 §7, Jobs AP, AR): R_b ∩ hole = {x⁺} is proved (the near vertex is always x⁺, which cannot heal; at least one far vertex is needed), but |R_b| = 2 is NOT a ring identity (2 in 40/53 local runs, 4 in 10, 3 in 3); "one far vertex ⇒ no second break" is false on open runs (24 #3131, #3175); **G2 fails** (of the 14 degree-7 consecutive-break periods neither branch in 11; of 27 open degree-6 double breaks reaching R3k3^{b+2}, neither in 8; 16 have |R_b| = |R_{b+1}| = 2, e.g. p25 #1557 h16, p26m #21951 h22, p27 #162314 h4); on degree-6 single breaks the far gate has the same role α at R3k4^{b+1} and R3k4^{b+2} (19/19), so no colour-only exclusion exists; "a second break needs a second hole gate" (Job AR: gates ({x⁺}, {x⁺, M_z}) ×6, ({x⁺, M_z}, {x⁺}) ×6, ({x⁺}, {x⁺}) ×2 at degree 7; the extra gate M_z is equally likely at either break, so hole gates do not separate degree 6 from 7); run-local bounded distance (Job X: the double-break run end is within 15 at orders 25–26 but order 27 gives 9/9; Job AL: a window failure's distance to the first non-DL state has max 29 at order 27, no uniform bound, no single leaving rule); the single-state crossing argument (the Lock2 chain leaves the second pocket through z–m; NightA34 §4); "K′ meets the Lock2 witness at R3k0" (disjoint colours); "Lock2 dies within periods b+1, b+2" (p26m #21951 h22 stays DL to position 5 of b+3); the coupling "k = 4 failure ⇒ k ≤ 2 credit ≥ 2" (3/7, 0/7). A double break exists in a run (24 #3611 h0: DL run of 18 with two consecutive k = 4 failures), so the lemma is **unprovable inside a run** and is a Γ-closure statement. Conjecture Σ (after a double break the step-0/1 far swap recolours a vertex of the first break's gate or of Z_b) is now **killed** (Job AM: holds in 36/73 open double breaks, 18/19 single breaks). Job AM confirms the window lemma with 0 exceptions (now formal in `QuarterWindow`: `k4_failure_iff_z_split`, `k3_failure_iff_y_split`) and gives a rigid signature: |R_b| is exactly 2 on every degree-6 Γ-cycle break (far part 1), 2–5 at degree 7, 2–7 on open double breaks; candidate lemma (unexamined): |R_b| = 2 forces restoration by the same far vertex both times, which by time reversal forbids a second break. **NightPotential, structural obstruction:** the mirror maps a step-8 break to a step-3 restore and J is a state function, so on any closed orbit #breaks = #restores; any per-step inequality cancels to a tautology or becomes window-local (false on open runs). A₃₄′ is a SPACING constraint (no two breaks in consecutive periods), not a counting one, so a potential must be two-period in scope or carry a phase. Total rank is not a failure signal (per-step change ±1 or ±3 on all 4,450 steps; reaches 0 at non-failing states).

**W2 (k ≤ 2 side).** *Reduction achieved:* colour bookkeeping at positions 4–8 (hand, NightW2 §1; formal in `QuarterW2Frame`); the three fixed points are F₄, F₆, F₈ (acyclicity of {3,4}, {2,4}, {2,3}); Lemma Fix (formal); fan lemma (formal): u lies on an {A,B}-cycle ⇔ one of its {α,μ}-neighbours lies outside K_σ, so W2′ (y or z on an {A,B}-cycle at some k ≤ 2 state) has a duality-free form and W2′ ⇒ W2; ring candidates w₃ at R3k2 and w₀ at R3k0 are never recoloured; swap-cut reduction (hand): the ring part of W2″ fails only if K₄ cuts w₃ from x₁ in {1,2} **and** K₇ joins w₀ to x₃ in {1,4}; sub-statement R: w₃ ∉ K_σ(R3k2) or w₀ ∉ K_σ(R3k0). Euler identity (formal): the total six-pair cycle rank is ≥ 0 at DL states. Data: W2″ 552/552 on Γ periods; R3k1 never needed; Job AI: fixed points are made by one swap each.
**Killed routes:** a ring/2-ball {A,B}-cycle (Job AG: at (5,5,5,5,6) the {A,B}-subgraph on the 2-ball is always acyclic at k ≤ 2, 1,656 states; the cycles run outside it); L-death (Job AL addendum: 11/711, 35/2,376, 106/10,813 all-three-fixed open windows have DL R1 states on both sides, first p25 #733 h17); single-state crossing; "K₄ creates the cycle" (19/60 already have one); the position-5 cycle through p; hand proof of W2**(a). W2\* (R3k2 and R3k0 of one period never both fail) is 0/552 on Γ periods but fails across period boundaries.

**Why both are Γ-closure statements.** Job AK: on every Γ period (552) W2\*, W2″, R have 0 failures; on open DL-run windows (3,977 / 14,136 / 72,643 per orientation at orders 25 / 26 / 27) they fail 884 / 2,924 / 13,629 (W2\*), 1,334 / 4,729 / 23,390 (W2″), 1,707 / 6,125 / 31,569 (R). First W2\* counterexample p25 #668 h18 (R3k2, R3k1, R3k0 all fixed; the DL run is exactly the five-state window). A₃₄′ has the open-run counterexample 24 #3611 h0. Lemma W fails on open runs too. Both statements are true exactly when the orbit closes, with no bounded-distance escape, which is why they carry the 4CT-strength (NightP1 §5).

**Γ-cycle length (Jobs AN, AO, AQ; NightGammaLength).** The closing colour permutation is ρ = σ^{L/10}, a 3-cycle fixing the repeat colour α (not c(p); at the R3k4 anchor p has colour B) and rotating the other three (formal: `period_colour_rotation`, `closing_perm`: 30 ∣ L for colouring-closed orbits). The census lengths L ∈ {20, 40, 60} are a small-order artefact: the adversarial graph A7 has a Γ-cycle with L = 800, so "L ≤ 60" is **killed** and the closure lemmas cannot be reduced to a fixed finite window. 20 ∣ L (m even) remains a conjecture; ring-local parity is killed (every ring edge is cut 4 times per period, every ring face touched 6 times, so any obstruction to odd m is on far edges).

## 5. Degree 7 comparison

Same universal period (406/406 periods, Job AC), same skeleton (k = 4 fails only Lock2-only, k = 3 only Lock1-only, k ≤ 2 mostly fixed points), higher failure rate (79/916 vs 7/140 at orders 25–26; 8.6% vs 3.4% over 25–27) and more f = 1 at k = 4. Lemma S_Γ **fails** at (5,5,5,5,7) (Cr as low as 10 vs D = 20; 15 failure records; Job Z), also at (5,5,5,6,7), (5,5,5,6,8+), (5,5,5,7,7), (5,5,6,6,7), (5,5,6,5,7). Lemma W fails on every one of the 15 records; in every period k = 2 and k = 1 are fixed points (W2 fails), plus consecutive k = 4 breaks or f = 1 at k = 4 with k = 3 failing. Job AH: the A/B rank at positions 4, 6, 8 is never (0,0,0) at degree 6 (0/552) and is (0,0,0) in 14/916 periods at degree 7 (12 inside the failure records). Job AE: consecutive-period step-8 breaks never occur at degree 6 (0/19) and do at degree 7 (14 periods, all plantri orientation; in the mirror orientation Lemma S fails at 6 degree-7 holes with no consecutive breaks, cause unchecked). Conclusion on record: the degree-6 vs degree-7 difference is quantitative, not structural; W2 is the exact dividing line in the Γ-cycle data. So the lemmas are not purely local ring facts: the degree enters through how the swaps at positions 4, 6, 8 move A/B edges.

## 6. Lean inventory (night modules)

All under `SolvingFrameworkPlan/docs/working/StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/`. Directory recount at 04:44: 30 `Quarter*.lean` + `NoFrozen.lean` = 31 night modules (matches the log's "31 night modules"; the 04:39 count of 30 was before `QuarterLemmaP`). All are committed and recompiled with standard axioms per the log. A text search finds no `sorry` in code in the modules checked at 04:05; the newer ones were not re-searched. `QuarterFixR1.lean` is not in the tree.

- `QuarterFloor`: definitions (Pent, locks, DL, classes), Lemma A, `QuarterFloorConj`.
- `QuarterRotation`: R₊₃ and R₊₂ rotations on unfilled states.
- `NoFrozen`: no doubly locked state is frozen (sphere).
- `QuarterRotationPlanar`: rotation definedness from planarity; the Hex dichotomy.
- `QuarterPi`: Lemma Π, the forward move π permutes every class (1,076 lines).
- `QuarterWinding`: Theorem W.
- `QuarterFloorH`: Theorem F5 from `IcoBallP`.
- `QuarterFloorHBridge`: F5 from triangulation + degree-5 link vertices.
- `QuarterSigmaExit`: Lemma 3′, exact σ-exit condition.
- `QuarterSigmaGroups`: σ-groups and Conjecture σC; σC at the all-5 hole.
- `QuarterSigmaPrime`: σ′-links, `SigmaUnionC`, its base case at the all-5 hole.
- `QuarterSanity`: icosahedron instance of the F5 hypotheses.
- `QuarterSigmaK34`: σ-exit facts at k = 3, 4.
- `QuarterJordanDual`: Jordan duality (D) at k = 3, 4; f ≥ 2 at k = 3.
- `QuarterGammaPeriod`: the universal 10-step period of a Γ-cycle.
- `QuarterExcursion`: exact excursion accounting; no double hit.
- `QuarterPeriodJ`: period lemma for J; k = 4 failure ⇔ step-8 break.
- `QuarterFlowIdentity`: group flow identity; `rem_eq_unhit_mixed`.
- `QuarterSigmaFix`: Lemma Fix.
- `QuarterAssignment`: σC from a charge-back single-target assignment.
- `QuarterLockJ`: lock-membership form of J.
- `QuarterRestore`: probe: z ∈ Lock2 witness at R1k1 is a ring identity.
- `QuarterMirror`: mirror orientation reverses π on DL states.
- `QuarterW2Frame`: W2 frame at positions 4–8, fixed-point conditions.
- `QuarterFan`: fan lemma, W2′ in duality-free form.
- `QuarterEuler`: six-pair Euler identity.
- `QuarterZsplit`: z's split component avoids the hole; `far_vertex_needed`.
- `QuarterEvenCut`: even-cut lemma; ring edge cut count 4; relabelled closure; 3-cycle cut non-emptiness.
- `QuarterLemmaP`: Lemma P and the exact identity Σλ = |DD| − 2N₀ − E₂ − 3τ.
- `QuarterK8`: the step-8 component, hole ∩ K₈ = {x₂, x₃, w⁺}.
- `QuarterWindow`: NightA34 §1–§3 period bookkeeping (`bookkeeping`, lock/J as joins), `step8_far`, `window_forced`, `k4_failure_iff_z_split`, `k3_failure_iff_y_split`.

`check.sh` (in `StudioMathLean/`) names the `Quarter*` modules plus `NoFrozen`, including `QuarterWindow`, `QuarterZsplit`, `QuarterEvenCut` and `QuarterK8` (`QuarterK8` and `QuarterLemmaP` seen in `check.sh` at 04:44; the count there was not redone); a full regression needs the snapshot build `$HOME/mathlib4-planemap-build`, which is absent on this MacBook, so modules were recompiled individually against `$HOME/mathlib4-planemap` (log, 03:28 note).

## 7. Studio data inventory

All files under `backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/` (script `jobX.py`, summary `jobX-summary.txt` or similar, C++ engine `picyc.cpp` with variants `picyc.<letter>`). Counts are from the log.

- **L**: Lemma S on 62 + 6 Γ-cycle records: C_neg ≥ D, min 1.55, C_pos = 0 (`jobl-*`).
- **M**: 140 blocks of 10 from R3k4; 139/140 ≥ 10, min block credit 8 once (p26 #87942 h22) (`jobm-*`).
- **N**: one-question lemma 280/280; 14 failures (`jobn-*`).
- **O**: universal period 140/140; break/restore mechanism, steps 8, 0, 1, 3 (`jobo-*`).
- **P**: k ≤ 2 exits; F₀₁₂′ min exactly 1.000; one-edge rule; breaking swap cuts the y–z path (`jobp-*`).
- **Q**: k ≤ 2 fixed points are a different mechanism from the y ~ z breaks (`jobq-*`).
- **R** (with **J**): order 27, all 320,133 core triangulations, 11,304,648 classes; σ′C 0 failures among ~368M groups; F₄ fails once; (5,5,5,6,6) Lemma S fails once (`jobj-*`, `jobr27`, `jobr.sh`).
- **S**: Lemma R per target fails at order 27 (12 of 732), holds at 25–26 (210/210); P₁ holds everywhere (`jobs-*`).
- **T**: smallest window with credit ≥ 10w is w = 2 (`jobt-*`).
- **U** and **V**: F₄ gap located at p27 #133619 h21; (5,5,5,6,6) failure p27 #316043 h18 repaired by an R1 exit (`jobuv/`).
- **W**: Lemma W on all maximal DL runs; Γ windows 0 failures, open runs fail (`jobw-*`).
- **X**: consecutive k = 4 failures never on a Γ-cycle; run ends within 15 at 25–26 (`jobx-*`).
- **Y**: the rem > 0 sits in the target's own positive excursion (p27 #68456 h19) (no separate file listed; see NightLemmaR / `28-lemmaR/`).
- **Z**: σ-flow closes exactly on (5,5,5,5,6) and (5,5,5,6,6), fails at several degree-7 patterns; P₁ fails at 19 holes of other patterns (`jobz-*`).
- **AA**: 73 double k = 4 failures, all the step-8 far (p,y) swap, one rule 73/73 (companion of Job W; outputs `out/`, `picyc.*`).
- **AB**: excursion-level self-payment false (~48% of positive-mass excursions) (`jobab-summary.txt`).
- **AC**: σ′ lockless credit covers 8 of 22 failure records; charge-back P₁ holds in all 22; (5,5,5,5,7) period 406/406 (`out/`, `picyc.*`).
- **AD**: P₁ neighbour profile; 75 def′ > 0 cycles, min ratio 1.25 (`jobad-*`).
- **AE**: Lock1/Lock2 component sizes; z re-enters the Lock2 witness 2 states after a break (98/98) (`out/`, `picyc.*`).
- **AF**: P₁ forms; undirected σ P₁ 407/407; the ρ = 1.25 case; degree-7 failure tuples (`out/`).
- **AG**: W2 is non-local; Lemma Fix 0 exceptions (462 fixed points) (`nightw2/`).
- **AH**: A/B rank along Γ-cycles; (0,0,0) never at degree 6, 14/916 at degree 7 (`nightw2/`).
- **AI** and **AJ**: A/B cycle bases (W2″ 552/552); exact time reversal 1,364/1,364 (`nightw2/`).
- **AK**: W2\*, W2″, R are Γ-closure statements (0 failures on Γ periods, many on open windows); counterexample p25 #668 h18 (`jobak-summary.txt`, `picyc.ak`, `nightw2/`).
- **AL**: no uniform bound on run-end distance; no single leaving rule (`jobal-summary.txt`, `jobal-addendum.txt`, `picyc.al`, `picyc.al2`).
- **AM**: window lemma 0 exceptions; conjecture Σ killed; |R_b| = 2 at degree 6 (merged 58a2019).
- **AS** and **AT**: long degree-6 Γ-cycles (L up to 200) and cut parity (`jobas/`, merged c927af2).
- **AU**: A₃₄′ failures all on L = 20 cycles; breaking period by |K(p)| 18/19 (merged 88da5e6).
- **AV**: two-period dump; K₈ ⊇ {x₂, x₃, w⁺} 896/896 (`jobav/`, merged 41c9496).
- **AX**: u* alternation killed; 20 ∣ L parked (merged 9e26749).
- **AY**: fixed-point form 550/552, not exact; forced σ pair per position (merged 488da21).
- **AZ**: the exception cycle p26 #87942 h22 in full (`jobaz/`, merged e6282b4).
- **AW**: adversarial double-break search, still running; no result in the log.
- **AN**: ρ = σ^{L/10}, L ∈ {20, 40, 60} on 2,728 Γ-cycle records (merged 3c53c99).

Earlier jobs for context: A, A2, B (positive-cycle census, transport), C ((5,5,5,5,5) positives), D (`jobd-summary.txt`), E (`jobe-*`), F (`jobf-summary.txt`, `witness-sigC-p26-70869-h11.json`), G (`jobg-*`), H (`jobh-summary.txt`), I (`jobi-*`), K (`jobk-*`), cb (`jobcb-*`). IPR witness: `witness-ipr265-h43.json`. Job letters whose files sit under other subdirectories: `nightf012/`, `nightw2/`, `jobuv/`, `jobr27/`.

## 8. Suggested next steps

1. **A₃₄′ at degree 6 as a two-period statement (new framing).** In all data the k = 3/4 failures live only on L = 20 cycles, a finite object (20 canonical states, 60 colourings, π^20 s = σ² s). Target: on an L = 20 all-DL orbit at a Hole6 the two k = 4 visits cannot both fail ("the two step-8 (p,y) far components cannot both cut y from z"). Under hand attack (NightA34Two.md, in progress; data `jobav/` and `jobaz/`); the Job AV dump (`jobav/jobav-cycles.jsonl`) is in. Longer cycles need no extra work in the data (Job AS). Earlier general advice stays: **A₃₄′ on Γ-cycles.** Every local handle tried tonight (crossing, gate, Σ, G2, hole gates, potential, bounded distance, L ≤ 60) is closed; what remains is a global closure invariant. Search for one that uses closure: an all-DL orbit visits each state once per L steps, so a double break at b, b+1 must be incompatible with a return; candidates are the total cycle rank (`QuarterEuler`) and the time-reversal symmetry (`QuarterMirror`: one orientation suffices, step 8 and step 7 are the same event read backwards).
2. **Fixed-point language (second live line).** On Γ-cycles at degree 6 a k = 3/4 failure ⇔ σ fixed at R1k1 (128/128), and the k ≤ 2 failures are fixed points, so Lemma S_Γ is the statement about WHERE in the 10-step period σ is fixed: A₃₄′ = not fixed at R1k1 in two consecutive periods, W2 = not fixed at all of R3k2, R3k1, R3k0. Tools: Lemma Fix, the fan lemma, the six-pair Euler identity (all formal). Status after Jobs AY/AZ: this is **structure, not mechanism** (550/552, and the exception's R1k1 image is DL), so it is a bookkeeping language, not a live attack; A₃₄′ stays stated as "no consecutive step-8 breaks". 20 ∣ L is parked (Job AX).
3. **W2 on Γ-cycles, via the Euler identity** (NightW2Euler.md, in progress per the coordinator; not checked here). Also: prove W2\*\* (a) and (b) or R by a swap-cut argument that uses the Lock1/Lock2 chains at positions 4–8; the missing ingredient is how K₄ meets the Lock1 {2,3}-chain x₁ → x₃. The Lean state is `not_all_fixed_iff`, `w2'_iff`; a formal W2′ needs escapes outside the 2-ball and so a global argument.
4. **Replace F₄** by "credit ≥ 2 at k = 4" and re-run the arithmetic of NightF6Flow §1 with actual credits (Lemma S holds with ratio ≥ 1.95 on 202 records at order 27); state the sufficient form as a lemma and check it formally.
5. **Non-Γ half.** State P₁^str as a Lean certificate on every σ-group (the formal `AssignmentStr` exists); decide whether the hand proof is a global count over T (NightP1 addendum says yes).
6. **Degree-6 adversarial test.** Job AQ found no (5,5,5,5,6) hole with a Γ-cycle on the adversarial graphs; the coordinator reports Job AS is building one. Until it runs, the lemma chain is untested beyond the census at degree 6 (no counterexample anywhere). Also: decide the 20 ∣ L conjecture only if it helps closure; the far-edge parity test is NightGammaLength §2.
7. **Housekeeping.** Confirm `QuarterWindow` is in `check.sh`, obtain the missing snapshot build for a full regression, and commit remaining untracked files.
8. **Review gates.** The Night notes (NightF6Flow, NightLemmaS, NightF012, NightLemmaR, NightP1, NightW2, NightA34) are unreviewed; request an adversarial review of the flow identity and the period lemma before citing them, and a re-check of the Studio-only claims by the independent Python engine (done for Jobs U, V and the F-island, not for all).
9. **Outside F6.** (5,5,5,6,6) needs σ′ (as SigmaUnionC says); degree 7 and above are not Γ-flow theorems on σ alone. Do not spend further effort on bounded-distance or ring-local routes (§4).
