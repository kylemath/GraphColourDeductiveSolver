# NightPotential — a potential for Γ-closure? (exploratory)

Written 2026-10-07 04:05 MDT. Long Table, potential angle (the A₃₄′ crossing argument and the W2 mechanism are with the other two agents).

Scripts and outputs: `backgroundMaterial/planemap-structural/longtable/local-runs/31-nightpotential/`. One core, AC power, every run under 4 min.

## Verdict

- **No tested potential closes Γ-closure.** I tested 20 state potentials:
  - the lock-witness sizes;
  - the six pair cycle ranks and their sums, including the total rank Σ rank = Σ comp − 8;
  - the K_σ, K_step and K_yz sizes;
  - the K_σ-escape count at y, z;
  - the crossing counts between K_step and the locks.

  The test sets were all 670 Γ-records of Jobs AH/AE, 54 Γ-cycles regenerated locally, and 318 open DL runs (gentri 22–24). No potential has a per-step or per-window sign that separates failing windows from the rest. Each one that seems to separate on a sample fails on the full set.
- **Structural reason (§4).** Every state function has Σ_cycle ΔΦ = 0 trivially. The mirror orientation reverses each Γ-cycle (formal, QuarterMirror) and maps a step-8 break to a step-3 restore. J is a state function, so #breaks = #restores on any closed orbit. So a per-step inequality of the form "failure steps cost, other steps are bounded" either counts breaks against restores, which is a tautology, or has to be window-local, and window-local statements are false on open runs (Jobs AA/AK/AL).
- **What is proved here:**
  - (i) the six-pair identity and Rtot ≥ 0 at DL states;
  - (ii) ΔRtot is **odd** at every DL→DL R₊₃ step (a parity argument, modulo a duality formula that is checked as data);
  - (iii) the Lock2 witness of s *is* the Lock1 witness of π s.
- **One new global fact [data, 54/54 cycles]:** the closing colour permutation ρ (c_L = ρ(c₀)) is a 3-cycle that fixes c(p) = α(R3k2) and rotates {μ, A, B}. It permutes exactly the three α-free pairs of W2.

## 1. Total rank (the coordinator's candidate) [proved / data]

**Identity [proved].** Each edge of T − h lies in exactly one pair graph, and each vertex in three. So Σ_pairs rank = E − 3V + Σ_pairs C.

For T on n vertices and deg h = 5: E = 3n − 11 and V = n − 1, so E − 3V = **−8**. Hence

  **Rtot := Σ rank = N − 8**, where N is the total number of Kempe components.

- [data] It holds on all 10,674 colourings at the degree-5 holes of gentri orders 12–17 (`identity.py`).
- [data] It holds on all 1,080 states of the 54 Γ-cycles.

**Floor [proved].** At a DL state:
- Lock1 ∪ h is a closed {μ,A}-curve that separates x_{j+2} from x_{j+4}, so C_{αB} ≥ 2.
- Lock2 ∪ h separates x_{j+2} from x_j, so C_{αA} ≥ 2.

So N ≥ 8 and **Rtot ≥ 0**.

**Duality at DL states [data, 1,080/1,080 Γ states; consistent with all 3,370 open-run steps through (ii)].**

  rank_ab = C_cd − 1 − [ab ∈ {μA, μB}]

Here cd is the complementary pair. The two lock pairs carry a −1 because their two link arcs are joined. In particular rank_AB = C_αμ − 1, which gives Lemma Fix again.

**Parity [proved from the duality].** Write C_ab + C_cd ≡ E_ab + V_ab + 1 + δ_ab and sum over the three pairs through a colour c. This gives:
- N ≡ V + D_c + 1 for c ∈ {α, μ};
- N ≡ V + D_c for c ∈ {A, B};

where D_c is the sum of deg_{T−h} over the vertices coloured c.

An R₊₃ step swaps {α,A}, so the μ-vertices are untouched. The old μ becomes the new A′ (x_{j+1} = x_{j′+3}). Hence N′ − N ≡ 1.

- [data] ΔRtot ∈ {±1, ±3} at every step: Γ 1,080/1,080, open 3,370/3,370.
- [data] A generic Kempe swap has either parity (`parity2.py`), so the oddness is specific to the R₊₃ step.

**Floor ≠ failure [data].**
- Rtot = 0 occurs at 20 non-failing Γ R3k0 states.
- Break periods have Rtot(R3k0) = 1–2.
- W2* (F4 and F8 in the same period) failure windows on open runs have Rtot at positions 4/6/8 mostly (1,1,1), the same as 22 non-failing windows.
- At the p25 #668 counterexample, Rtot = 0 at R3k2 (all six pairs forests). Rtot then *rises* 0, 1, 2, 3, 4 across the window, and Lock2 dies next (R1k2, L10).

## 2. Per-step bounds [data]

All are DL→DL R-steps, with pairs named by the pre-step roles (swap {α,A}, `pairdelta.py`).

| pair | Γ (1,080) | open (3,370) |
|---|---|---|
| {α,A}, {μ,B} | 0 (trivially: the swapped pair and its complement) | 0 |
| {A,B} | −3…+2 | −3…+1 |
| {μ,A} | −2…+3 | −1…+3 |
| {α,μ}, {α,B} | −2…+2 | −2…+2 |
| Rtot | ±1, ±3 | ±1, ±3 |
| α-free sum (role) | −3…+3 | −4…+4 |

**Best per-step bound:**
- |ΔRtot| ≤ 3, and ΔRtot is odd;
- |Δ rank_ab| ≤ 3 for each pair, with two pairs fixed.

A step can raise Rtot by 3 (118/1,080 Γ-steps). The break step 8 raises it, by +3 in 8/9 breaks and +1 in 1/9. So "steps rise ≤ 1, failures need a drop ≥ 2" is false in both halves.

**Γ-only sign facts [data].**
- On Γ-cycles, step 3 always lowers Rtot and step 8 always raises it.
- On open runs each has 20 exceptions.

These are another closure-only phenomenon, and are mirror images of each other (step 8 ↔ step 3 under reversal).

## 3. Candidates tested

**Gamma deg6/deg7** = Jobs AH+AE, 264 + 406 records. **54** = the cycles regenerated from `jobak-66dump.json` (rotation + pos-4 colouring, traced by π; every state DL; positions 5–8 match the dump up to colour relabelling).

"Monotone in period" = Φ(s_{10b}) is constant along the cycle. On a closed cycle that is the only way a period-monotone potential can exist.

| potential | monotone in period | Σ ΔΦ = 0 | separates failing windows? |
|---|---|---|---|
| L1, L2 (lock witness sizes) | 32/54, 23/54 | trivially | **step-8 ΔL2 ≤ −3 in 19/19 deg-6 breaks**, but also −3 in 40 non-breaks. ΔL2 ≤ −4 ⇒ break (15/15). L2 recovers within the same period (mean 8.1 → 11.2 → 13.0), so it carries no debt into the next period. |
| L1 + L2 | 24/54 | trivially | no |
| AB, μA, μB; α-free sum R3 | 39, 45, 43, 31 /54 | trivially | R3 over the window at phases 1 and 4: negative in 9/9 breaks of the 54, but **2/19 positive at deg 6 on the full set**. Killed. |
| αμ, αA, αB | 33, 31, 45 /54 | trivially | no |
| Rtot = N − 8 | 39/54 | trivially | no (§1) |
| \|K_σ\| | 54/54 | trivially | **trivial**: at R3k4/R3k3, K_σ is the bare triple x_j x_{j+1} x_{j+2} by the R3 ring colours (p is outside the triple). |
| \|K_step\|, \|K_step ∩ Lock1\| | 1/54, 0/54 | trivially | no. K_step ∩ Lock2 = ∅ always (disjoint pairs), trivially. |
| esc (α/μ-neighbours of y, z outside K_σ) | 28/54 | trivially | 9/9 breaks have esc(R3k0) = 0, because those 9 are all F8. But on the full set 7/19 breaks are not F8. Killed. |
| K_yz size, J | 32/54, 45/54 | trivially | J is the definition |

Window-sign test (`windowsign.py`): for every potential and every phase t₀, I looked at the sign of ΔΦ over the 10-step window containing a step-8 break. A potential whose sign is negative in every break window would prove A₃₄′ on L = 20 cycles by closure, since the two windows' changes sum to 0. **None qualifies** on deg-6 Γ (all 9 potentials of AH/AE), deg-7 Γ, or open runs.

Coupling side-results (`couple.py`; these are in the other agents' lanes, recorded only as killed):
- "break ⇒ F8 in the same period" (12/19 at deg 6);
- "break ⇒ F4 in the next period" (11/19).

## 4. Why closure plus a potential does not suffice as posed [sketch]

1. Σ over a closed orbit of ΔΦ = 0 holds for every state function. A bound on failures needs a per-step **inequality** whose failure steps are strict.
2. By `gammaOrbit_mirror` the mirror reads each Γ-cycle backwards, with (type, k) ↦ (type, 2 − k). So step 8 (R3k0 → R1k2) read backwards is R1k0 → R3k2, which is step 3, the restore. Breaks and restores are swapped.
3. J is a state function, so #breaks = #restores on any closed orbit.
4. An inequality charged at breaks therefore has a twin charged at restores. Summing over the cycle pairs each break with the restore at most 5 steps later (step 8 → step 3 of the next period, Corollary P3). That makes the argument window-local, and window-local statements fail on open runs:
   - Job AA: double breaks;
   - Job AK: W2* failures;
   - Job AL: distance to lock death up to 29.
5. A working potential must therefore see something a window cannot. On L = 20 cycles the only extra information is that the run returns to the same canonical state after two periods.

**The closing permutation [data, `rho.py`].** On the 54 regenerated cycles, c_L = ρ(c₀), where ρ is a 3-cycle that fixes α(R3k2) = c(p) (colour 1 of NightW2 §1) and rotates {2,3,4}.
- So the three α-free pair graphs {3,4}, {2,4}, {2,3} are the forest pairs of F4, F6, F8 respectively, and the lock pairs of the other two states (NightW2 §2).
- ρ permutes these three pair graphs cyclically per lap, and per period as well (ρ_period = ρ² at L = 20). This matches the rotating pairing of NightLemmaS §0.

For role-relative potentials this adds nothing beyond canonical closure. For the **vector** of the three absolute α-free ranks it does:

  (r₃₄, r₂₄, r₂₃)(s_{t+L}) = ρ · (r₃₄, r₂₄, r₂₃)(s_t).

## 5. What remains to prove, and the best candidate

- **Best potential (for the record):** Rtot = N − 8. It is the only candidate with all of: a proved floor (≥ 0 at DL); a proved parity rule (odd per R-step); a uniform per-step bound (|Δ| ≤ 3); and a Γ-only sign rule (step 8 up, step 3 down). It does **not** separate failures.
- **Open:** a vector potential using ρ. Track the three absolute α-free ranks across one period, R3k2 → R3k1 → R3k0 → (next) R3k2. W2 says the diagonal entries (r₃₄ at pos 4, r₂₄ at pos 6, r₂₃ at pos 8) are not all 0. Closure says the period map is the 3-cycle up to the per-step changes in §2.
- **Next test (Studio, Job AL-style):** on all Γ periods and open runs, record the absolute α-free rank vector at positions 4, 6, 8 and 14. Check whether "diagonal all 0" forces a fixed sign on the off-diagonal sum, and whether the period map of the vector is ρ plus a non-negative correction on Γ but not on open runs.
- **Prove the DL duality formula of §1.** It is a planar duality with the pentagonal hole face; the −1 counts the lock chain closing through h. Then the parity rule is fully proved.

## 6. Addendum: forest counts and the coordinator's identities (`forests.py`) [data]

- **Forest count does not track fixed points.** I counted the forest pair graphs over all six pairs and all states of each cycle (54 cycles, L = 20). The count ranges 66–84 per cycle and is not an affine function of the number of fixed-point visits (2–4):
  - forests − 6·fixed takes 10 different values (44–64);
  - Σ Rtot + forests takes 8 values (125–144).

  So there is no exact forest/fixed-point identity at the level of whole cycles.
- **Forest profile.** Here is the number of forests by role pair and position, out of 108 periods:

  | role pair | positions 0–9 |
  |---|---|
  | {A,B} | 0 10 0 1 48 0 82 0 48 1 |
  | {α,μ} | 59 0 59 0 81 92 86 92 81 0 |
  | {μ,A} | 97 97 97 97 41 58 99 99 58 41 |
  | {α,A} | 72 72 79 106 102 83 83 102 106 79 |

  So the Γ pair graphs are mostly forests. The fixed points (an {A,B} forest at positions 4/6/8) are the exception, not the floor of a potential.
- **The forest profile is mirror-symmetric**: position i ↔ 12 − i mod 10, with {μ,A} ↔ {μ,B} and {α,A} ↔ {α,B}. This is time reversal again, so forests at position 4 pair with forests at position 8, as the coordinator expected.
- **Winding.** On Γ-cycles U = L, so w = L/5. I found no second exact identity that ties failures to w. The σ-image identities (NightLemmaR) count credits, not breaks.
- **Studio Job AL addendum (relayed).** The six-pair identity holds on about 635k states, and lemma L-death fails (p25 #733 h17). Together with §4 this leaves the global route without a candidate potential. The ρ-vector of §5 is the one untested idea that uses information a window cannot see.
