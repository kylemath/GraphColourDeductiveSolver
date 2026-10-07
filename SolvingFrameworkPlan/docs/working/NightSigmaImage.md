# NightSigmaImage: Lemma S_Γ seen through the σ-image set

[exploratory] Night swarm note, 7 October 2026, 04:36 MDT. These are leads, not evidence, until someone re-checks them. Scripts and outputs are in `backgroundMaterial/planemap-structural/longtable/local-runs/32-nightsigmaimage/`. Engine: `uv_lib.Hole` (the independent Python engine of Jobs U and V), run on the MacBook on AC power with one core.

**Data used.** The (5,5,5,5,6) Γ-cycles that can be rebuilt locally are those whose rotation systems ship in the repo: the 27 holes × 2 orientations of `jobak-66dump.json`, plus `jobu-p27-133619-h21.json`. They give **64 Γ-cycles (orders 25–27), all of length L = 20**. Every Γ-cycle at those holes is included, not only the 54 dumped ones. The gentri graphs of orders 17–24 (both orientations, every (5,5,5,5,6) hole whose 6-vertex ring is a chordless cycle) contain **no** Γ-cycle, so they serve only as an "all states / open runs" control. Caveats: the dump was selected by Job AK as "rank-sum-1 periods", so the sample is biased, and no L = 40 or 60 cycle can be rebuilt locally.

Notation: Z is a Γ-cycle, r ∈ Z, s = σ(r), where σ is sigSwap, the swap of the {α,μ}-component of x_{j+1}. Period positions 0–9 start at R3k4. R3 states sit at positions 0, 2, 4, 6, 8 (k = 4, 3, 2, 1, 0) and R1 states at 1, 3, 5, 7, 9. Lemma S_Γ uses the σ-images of the R3 states.

## 1. Exact (hand) results

**Lemma P (where a lock type sits in its excursion).** Let s be any unfilled state.
- s has Lock2 ⇔ π(s) is unfilled.
- s has Lock1 ⇔ π⁻¹(s) is unfilled.

Hence:

| lock type of s | position of s in its unfilled run |
|---|---|
| DL | interior of a run |
| Lock2-only | first state of a run with u ≥ 2 |
| Lock1-only | last state of a run with u ≥ 2 |
| lockless | the whole run (u = 1) |

*Proof.* The first equivalence is the π-table (`QuarterPi`): a state with Lock2 moves by R₊₃ to an unfilled state, one without Lock2 moves by φ_B⁻¹ to a filled state. For the second: every unfilled state is the π-image of either an unfilled Lock2 state (by R₊₃, and the image has Lock1) or a filled state (by φ_A, and the image has ¬Lock1). These are `rot3_move` and `phiA_spec`, and π is a bijection. ∎

Corollaries, valid for any finite π-invariant set:
- #Lock2-only = #Lock1-only = E_{≥2}, the number of excursions with u ≥ 2.
- #DL = Σ_{u≥2} (u − 2).
- The number of DL→DL π-steps is Σ_{u≥3} (u − 3).

**Corollary W′ (a hand proof of the class identity).** Combine Lemma P with `excursion_mass` (the mass of an excursion is u − 3f). The mass equals −2 − 3(f−1) when u = 1, equals −1 − 3(f−1) when u = 2, and equals (u−3) − 3(f−1) when u ≥ 3. Summing over excursions gives

Σλ = |DD| − 2N₀ − E₂ − 3#τ,

where |DD| is the number of DL→DL π-steps and #τ = Σ(f − 1). A Γ-cycle has no excursions and gives Σλ = L = |DD|. This is the "exact class identity" that `NightF6Status` §3 lists as **data**. It is now a two-line consequence of formal lemmas. Formalising it means summing `lam_eq` over excursions; that is not done here.

**Reading for Lemma S.** Every non-fixed σ-image s of Z starts an excursion, ends one, or is interior to one. Its λ-mass is exact by Lemma P. A Lock2-only image (the k = 4 failure) is the *first state of a run of length ≥ 2*. A Lock1-only image (the k = 3 failure) is the *last state* of such a run. The no-double-hit property (σ is injective, there is one start and one end per run) extends to these: distinct r give distinct starts, and distinct ends.

## 2. Classification of σ(Z) (64 Γ-cycles, 640 R3 images, 640 R1 images; `summary.txt`)

R3 images, by period position:

| k (pos) | lockless | fixed (σ r = r) | Lock2-only | Lock1-only | DL, not fixed |
|---|---|---|---|---|---|
| 4 (0) | 119 | 0 | 9 | 0 | 0 |
| 3 (2) | 119 | 0 | 0 | 9 | 0 |
| 2 (4) | 78 | 48 | 2 | 0 | 0 |
| 1 (6) | 46 | 82 | 0 | 0 | 0 |
| 0 (8) | 78 | 48 | 0 | 2 | 0 |

- **σ never maps an R3 state of Z to a DL state, except as a fixed point.** No non-fixed R3 image is DL, so none lies on any Γ-cycle (0/640). The answer to "can σ map a DL state of Z to a DL state of Z?" is: **at R3, only as a fixed point**.
- **At R1 it can, rigidly.** R1 images are DL in 434/640 cases (426/620 on the 62 dump cycles that `r1img.py` covers). They always sit at the **same period position**. If one lies on Z, then σ(r) = π¹⁰(r) (136/136; here also π^{L/2}). Otherwise it lies on one other "twin" Γ-cycle (each Z hits 0 or 1 such cycle; 160 images) or on an open DL run (130 images) (`r1img-out.txt`). Ten Kempe swaps composing to the single σ-swap is a strong rigidity. It has not been checked at L = 40 or 60.
- **Targets.** Every non-fixed R3 image lies on a cycle T with W(T) < 0. The exceptions are 4 Lock1-only k = 3 images on W = 0 cycles of length 12.
- **The k ≤ 2 failures are fixed points, apart from Job U's hole.** 4 single-lock k ≤ 2 images occur, all at p27 #133619 h21 (both orientations): a Lock2-only image at k = 2 starting a (u, f) = (6, 4) excursion (mass −6, so it would *pay* 6), and a Lock1-only image at k = 0 ending a (6, 1) run (mass +3). "k ≤ 2 images are fixed or lockless" is therefore false on Γ-cycles, and it is far from true on open DL states (`low-20-22.txt`: single-lock and DL images occur at k ≤ 2).

## 3. The failure images at k = 3, 4

**Placement on Γ (9 + 9 images).**
- Each k = 4 failure image s starts an excursion with **(u, f) = (4, 1)**: s (Lock2-only), then two DL states, then Lock1-only, then one filled state. Its mass is +1, and it has exactly one DD step.
- Each k = 3 failure image is the **last** state of a (4, 1) run.
- In the same period, the k = 4 and k = 3 failure images land on *different* cycles T, so there is no shared excursion.

**Conjecture U34 (local, all states; `failexc-20-22.txt`).** On all 8,204 strict-R3 k = 4 states at orders 20–22 (DL or not), a Lock2-only σ-image (2,847 of them) starts a run with **u ∈ {3, 4}** (2,240 have u = 3 and 607 have u = 4), and **u = 4 forces f = 1** (607/607). The k = 3 statement is the mirror image (2,847/2,847). If U34 holds, a failure image's mass is at most +1, so a k = 4 failure "costs" at most one unit of λ against the cycle it hits. This is a run-local statement and a reasonable candidate for a hand or Lean proof via the period tables, since s is an R2-type state with the same ring as r.

**The R1k1 fixed point (Γ-only).** On Γ periods, a failure occurs at position 0 or 2 **if and only if σ is a fixed point at position 1** (R1, k = 1). This holds in 124/124 rebuilt Γ periods plus the 4 periods of the Job U hole:
- 8 periods have both failures,
- 1 has only the k = 4 failure,
- 1 has only the k = 3 failure,
- 114 have no failure and no fixed point at position 1.

By Lemma Fix (general form), "σ fixed at R1k1" means the {μ, A}-graph of π(r) is a forest, in the labels of r at position 0. The k = 4 failure criterion is "w₄ ∉ K_{μ,A}(x_{j+1})" (`sigma_exit_criterion_k4'`). Both are statements about the same colour pair.

This equivalence is **false on open DL windows** (`pos1-out.txt`, gentri 20–23 and the dump holes):
- 50 windows have a failure without a fixed point at position 1,
- 64 have a fixed point at position 1 without a failure,
- 368 of the 482 open windows agree.

So it is one more Γ-closure statement, but it **unifies the two halves of Lemma S_Γ**. On Γ-cycles every failure of Lemma S, at any k, is a σ-fixed point (an acyclic two-colour pair) at some R-state of the period: position 1 for k = 3, 4 and positions 4, 6, 8 for k ≤ 2. The only exceptions are the Job U hole's single-lock images. Under this equivalence, A₃₄′ (no two consecutive step-8 breaks) becomes "no fixed points at position 1 in two consecutive periods". W2 is "not all of positions 4, 6, 8 fixed". Both are spacing constraints on acyclic pairs. In the data a period with failures also has position 4 fixed in 9/10 cases.

## 4. Fixed points and the Euler identity

- Per Γ-cycle (L = 20, R3 k ≤ 2), the number of fixed points is 0 (10 cycles), 2 (6), 3 (26), or 4 (22). Over positions 4, 6, 8 the fixed points come in the patterns (–,F,F), (F,F,–), (–,–,F), (–,F,–) and (F,–,–). **(F,–,F) and (F,F,F) never occur** (W2 and W2*).
- Fixed points at R1 states (64 cycles): 10 at position 1 (all tied to failures, §3), and 3, 2, 2, 3 at positions 3, 5, 7, 9.
- Euler (`gamma54.json` of NightPotential, 54 cycles): Rtot = 0 forces a fixed point (78 R3 states). However, **no linear identity** was found between the fixed-point count of Z and the per-cycle sums of the six ranks, of Σ rank at R3 or R1, or of AB ranks. For example, S₁ − S₃ (the rank sum over R1 states minus that over R3 states) takes the values 8, 10, 12 and 14. On a closed orbit S₁ − S₃ = 10 + 2#(+3 steps) − 2#(−1 steps) − 4#(−3 steps) over the R3→R1 steps. This is a tautology, by NightPotential's obstruction.
- The step R3k4 → R1k1 lowers Rtot (Δ = −1) in 9 of the 10 periods with a fixed point at position 1, against 14 of 98 otherwise. This is a correlation, not an identity.

## 5. Identities sought for task (3), and what is killed

- **Exact (§1):** credit(s) = −mass(e(s)) = 3τ_e + 2[u=1] + [u=2] − DD_e for every non-fixed image s, with no double counting. Lemma S_Γ is therefore exactly "Σ over the excursions hit by σ(R3(Z)) of (3τ − DD + 2N₀ + E₂) ≥ L + (failure corrections)". This restates the problem; it does not reduce it.
- **Killed: "#(Lock2-only images of Z) = #(DD endpoints of a given type on the cycles hit)".** The failure images form a small subset of the (4, 1) excursions (`exc4-20-22.txt`). At orders 20–22, (4, 1) excursions start at R1, R2 and R3 states of every k. The σ-partner of a (4, 1) start is a strict R3k4 state only for the 607 R2k4 starts, and that bijection is just σ² = id. No count of DD endpoints on the hit cycles controls the failures.
- **Killed: "k ≤ 2 Γ images are only fixed or lockless"** (p27 #133619 h21; 4/384).
- **Killed: "k = 4 failure ⇒ σ fixed at π(r)" as a local lemma** (`fixlink-out.txt`, orders 20–22 plus the dump holes, all strict R3k4 states with Lock2: 115 states have a failure but no fixed point at π(r), 86 of them with r DL; P(fixed at π r) is 91% given a failure and 78% otherwise).

## 6. Suggested next steps

1. **Prove Conjecture U34** (u ∈ {3, 4}, and f = 1 when u = 4, for a Lock2-only k = 4 image). It is local. It caps the cost of a failure at +1 and makes "failure images start (4, 1) excursions" a theorem on Γ.
2. **Studio check at scale.** Run `simg.py` and `pos1.py` on all 202 order-27 Γ records and on L = 40 and 60 cycles. Test:
   - "failure ⇔ fixed point at position 1" (§3),
   - "σ(r) = π¹⁰(r) for R1 images on Z" (§2): is the offset 10 or L/2?
   - the degree-7 comparison: does the equivalence break exactly at the Lemma S_Γ failures of Job Z?
3. If the position-1 equivalence survives, **restate A₃₄′ as a fixed-point spacing lemma**. Lemma S_Γ then reads "acyclic pairs at positions 1, 4, 6, 8 obey spacing rules on a closed orbit". The closure argument could then target forests of the three α-free pairs, which ρ = σ^{L/10} permutes cyclically (Job AN, `closing_perm`).
