# NightPostAW: strategic reassessment after Job AW

Written 2026-10-07 05:09 MDT for the project owner. Sources: NightF6Status, NightLog-2026-10-06 (Job AK to the end), NightF6Flow, NightLemmaR, NightP1, NightClosedSets, NightEulerHole, the Lean files `QuarterSigmaPrime`, `QuarterFlowIdentity` and `QuarterAssignment`, and `jobaw/`. Notation: λ = +1 on an unfilled state and −3 on a filled one, so Σ_g λ = |g| − 4F(g).

## 0. Bottom line

The night proved a large local library and two real theorems: Theorem W, and F5, which is the floor at (5,5,5,5,5) holes and the only class-level floor in Lean. It made **no progress on any 4CT-strength statement.** Its main tree below Lemma S_Γ was built on census regularities (orders ≤ 27) that a 37-vertex flip search broke within hours. About twenty Studio jobs and most hand effort went into A₃₄′/W2 after Job AQ had already warned that the census was small. The only surviving conjecture is group-level: `SigmaUnionCConj`. Its adversarial evidence at degree 6 is thin, and it has never itself been the objective of a search.

## 1. What AW kills and what it leaves

- **False at degree 6** (61 verified 37-vertex graphs, from AS seeds):
  - A₃₄′ fails on 11 graphs (3 families).
  - W2 fails on 45 and W2\* on 55.
  - Lemma S_Γ fails in the Job-S form (deficit 4 at A7f2, 10 and 4 at walk-best-A7f1-3) and in the all-DD form (C_neg = 15 < D = 20 at walk-best-A7f1-3, mirror).
  - Lemma S was already false at degree 7. So **no per-Γ-cycle self-payment statement survives anywhere.**
  - Note: A₃₄′ failing alone did not break all-DD Lemma S (C_neg = 21, 26, 27 ≥ 20 on the three representatives). It took W2 and A₃₄′ failing together.
- **True but no longer a route.** These stay as a library; stop extending them:
  - the universal period, window, Lock/J, K₈ and z-split lemmas;
  - U34 and Lemma P;
  - the two-period/crossing reduction (`A34_two_iff` is now an equivalence with a false side);
  - the pair dualities, mirror and even-cut lemmas;
  - the fixed-point language.
- **Group level: what survives, and on what evidence.**
  - **σC at (5,5,5,5,6):** 0 failures in ~7.5M census groups (Job E). It is false universally (p26 #70869 h11, Job F).
  - **σ′C and SigmaUnionC:** 0 failures in ~100M groups at orders 24–26 and ~368M at order 27 (Jobs H, J). Also 0 on AQ, on the 40 AS constructions and on AW.
  - **Charge-back P₁:** 0 failures at both patterns at orders 25–27.
  - **Floor:** holds on the AW classes with large slack (F/|S| = 0.46, 0.43, 0.46).
  - **Correction to the log.** The 05:03 entry says SigmaUnionC holds on "all 61 counterexample graphs". The `jobaw/` files show group checks only on the **3 representative graphs** (8 orientation records, `jobaw-chain-on-counterexamples.txt`). `jobaw-verified.json` carries only period, A₃₄′ and W2 flags. On those 3 graphs the maximum group Σλ is exactly 0, so some group is tight; what kind of group it is was not checked.
- **Lean results worth keeping regardless:**
  - `QuarterPi` (Lemma Π), `QuarterWinding` (Theorem W), `QuarterFloorH`/`Bridge` (F5), `NoFrozen`, `QuarterLemmaP` (exact identity), `QuarterExcursion`, `QuarterFlowIdentity`, `QuarterSigmaGroups`/`QuarterSigmaPrime` (SigmaUnionC ⇒ floor, and its F5 base case, with `dd_le_two_noLock_linkGroup` for any link relation L ⊇ σ), `QuarterU34`.
  - **Defect found in `QuarterAssignment`.** The fields `Assignment.nbr` and `AssignmentStr.nbr` require the paying cycle to be reached by a *lockless exit*. Job AD found that 39/75 deficit cycles have no such exit. The proof of `sigmaC_of_assignment` never uses `nbr`. So the certificate as stated is stronger than what Studio checks. Without `nbr` it is a pure sum-split of σC with no geometric content.

## 2. Where the 4CT strength sits after AW

In a minimal counterexample every class of T − v is targetless, hence all-DL (C1), hence a disjoint union of Γ-cycles with w = L/5 > 0 (C3). So **every** group has Σλ = |g| > 0, and SigmaUnionC fails on every group. NightP1 §5 placed all of the 4CT strength in Lemma S_Γ. After AW it sits in **P₁ applied to Γ-cycles**: a Γ-cycle in deficit must have a nonpositive σ∪σ′-neighbour with slack, and a minimal counterexample has no nonpositive cycles at all. SigmaUnionC therefore splits into a qualitative part and a quantitative part:

- **G0(g):** every σ∪σ′-group contains a filled state. This is the qualitative part.
- **Mass:** 4F(g) ≥ |g| on every group. This is the quantitative part.

The implications are:

- SigmaUnionC ⇒ floor (4F ≥ |S| per class) ⇒ R\* (F ≥ 1 per class) ⇒ 4CT.
- SigmaUnionC ⇒ G0 ⇒ R\*.
- **S₁ ⇒ G0.** S₁ says every Γ-cycle has a DD endpoint whose σ-image is not DL. Proof: if F(g) = 0, every π-cycle of g is all-unfilled, hence all-DL, and g is σ-closed, so all σ-images are DL.
- The weakest per-cycle statement implying 4CT is **S₁′**: every Γ-cycle has a state with *some* Kempe swap to a non-DL state. By C1 this is equivalent to R\*.
- In additive terms, R\* ⇔ Σλ < |S| per class, and the floor ⇔ Σλ ≤ 0.

**Do the data support the weaker statement with more room?** Yes:

- The floor is exactly tight at gentri 17 #2 h0 and 17 #4.
- Every Γ-cycle ever computed has lockless exits: a ≥ L/4 in the census; C_neg ≥ 10 at degree 7 and ≥ 15 at AW.

That room is thin, though. The worst AW cycle has only about 2 lockless R3 exits per 20 states.

Room does not buy a mechanism:

- S₁ is 4CT-strength (NightLockBreaking Prop 2.4).
- Descent fails for all 14 quantities tried (NightClosedSets §6).
- No potential along π^{±1} can work (NightEulerHole, Lemma N).

The floor's advantage is that it is *additive*, and the one proof that worked (F5) is an additive injection. **Recommendation:** keep the floor as the target at group level, and use G0/S₁ as the cheap adversarial canary. A group with F = 0 kills SigmaUnionC immediately, and such a group is easier to search for than a positive Σλ.

## 3. The one statement to test first

F5's proof is a group-level injection: |DD| ≤ 2|R|, and σ maps the R3 DD endpoints R injectively to lockless states. The exact identity Σλ = |DD| − 2N₀ − E₂ − 3τ (formal) turns its failure at degree 6 into a budget.

**Statement B′ (bad-endpoint budget).** On every σ∪σ′-group g at a (5,5,5,5,6) hole:

  2·|R⁻(g)| ≤ 2·|N₀ᶠ(g)| + E₂(g) + 3τ(g),

where:
- R⁻(g) is the set of R3 DD endpoints of g whose σ-image is not lockless (fixed, single-lock or DL);
- N₀ᶠ(g) is the set of lockless states of g that are not σ-images of R(g).

Given |DD| ≤ 2|R|, B′ implies σC on g, and so SigmaUnionC.

Why this statement:
- It is per-group, which is the level AW leaves alive.
- It names the payers that the data point to: free lockless states and τ-mass on the neighbouring mixed cycles (the paying neighbour is unhit in 73/101 cases).
- It extends the only Lean floor proof (`dd_le_two_noLock_linkGroup`) rather than a census pattern.
- U34 (formal) already bounds what a failing k = 4 image costs: it lands on a (3,1) or (4,1) run of mass 0 or +1.
- It fails in a minimal counterexample, as any floor statement must (there N₀ = E₂ = τ = 0).

**Run these first, in this order:**
1. **AW backfill.** On all 61 AW graphs, both orientations, compute per group:
   - |DD| − 2|R|;
   - the B′ excess;
   - σC, SigmaUnionC, P₁ and G0.

   This closes the "all 61" gap.
2. **Census check.** Run B′ on all (5,5,5,5,6) holes at orders 25–27. Report the minimum slack, the five tightest holes, and how often |DD| ≤ 2|R| fails.
3. **Adversarial flip search.** Use the AW protocol: 252 walks × 1,000 steps, core-class flips with degree repair, hole star fixed, link (5,5,5,5,6). Change it as follows:
   - **Objectives:** (a) the maximum B′ excess over groups; (b) the maximum group Σλ for SigmaUnionC; (c) the DL fraction of the group containing the hole's Γ-cycle (the G0 canary).
   - **Seeds:** the 61 AW hits, the 40 AS constructions, A7_exc, and the tight census holes p25m #16945 h3, p26 #87942 h22 and p27m #167230 h23 (P₁ ratio 1.25).
   - **Γ-cycle constraint:** drop "keep a Γ-cycle" in half of the walks.
   - **Seed policy:** do not trust census seeds that never move. AW's census seeds never improved; every hit came from the constructions.

**Kill rules:**
- If B′ fails, fall back to σC with the F5 slack term kept.
- If SigmaUnionC or G0 fails, the group route is dead, and only class-level statements remain (the floor, Transport T).

## 4. Next attacks, ranked

1. **Adversarial SigmaUnionC/G0 search (§3, items 1 and 3b–c).** This decides whether any group-level route exists.
   - *Failure modes:* it finds a positive or filled-free group, which ends the night's whole framework below the class floor; or it stalls at Σλ ≪ 0 because the search space near the construction seeds is too narrow, which gives false comfort (the AW precedent).
2. **B′: census, then adversarial, then a hand injection for R⁻ via U34.**
   - *Failure modes:* the |DD| ≤ 2|R| loss makes B′ false at tight holes; or B′ holds but the payer is not one σ-hop away, so no one-hop injection exists and the proof needs a flow. At orders ≤ 24 the dominant cycle is 2–3 hops from 17 positive cycles; there, nearer neighbours pay instead. That is the Hall form of SigmaUnionC, with no local gain.
3. **Lean consolidation (cheap; independent of the outcomes above).**
   - Delete `nbr` from `Assignment` and `AssignmentStr`.
   - Formalise C1/C3 (targetless ⇒ all-DL ⇒ ⊔ Γ-cycles) and S₁ ⇒ G0 ⇒ R\*.
   - State B′ and prove B′ ∧ (|DD| ≤ 2|R|) ⇒ SigmaUnionC on top of `dd_le_two_noLock_linkGroup`.
   - *Failure mode:* low risk, and it touches none of the 4CT strength. Its value is that tomorrow's conjectures will be stated exactly as they are tested.

Do not resume A₃₄′, W2, two-pocket, potential or bounded-distance work. Treat every census-only regularity as provisional until a flip search has attacked it.
