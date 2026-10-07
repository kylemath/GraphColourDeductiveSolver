# Night of 6–7 October 2026: morning summary

For the project owner. Written 05:35 MDT from `NightF6Status.md` and the Night log through "05:33 — Full regression PASSES". All Night notes are exploratory and unreviewed; Lean results are recompiled by the coordinator.

## What the night produced

42 sorry-free Lean night modules (66 with the earlier PlaneMap modules): Theorem W (3F − U = −5·winding), Theorem F5 (the quarter floor at (5,5,5,5,5) holes), the exact class identity Σλ = |DD| − 2N₀ − E₂ − 3τ, the group flow identity and the charge-back assignment certificate for σC, Γ-cycle time reversal, the exact pair dualities, the pocket and crossing lemmas, and the new weak-F6 theorems `pureClean_of_hole6`, `pureClean_of_hole4` and `pureClean_of_degrees` (every Kempe class at a (5,5,5,5,6) hole, or one with four consecutive degree-5 link vertices, contains a filled state). Around them, about 55 Studio jobs on orders 12–27 (plus constructed 37-vertex graphs) and a large set of hand notes. No new theorem of 4CT strength.

## Two honest verdicts

1. **The strong per-Γ-cycle chain is false at degree 6.** A₃₄′, W2, W2\* and Lemma S_Γ fail on 61 constructed 37-vertex graphs (Job AW, two independent engines, `jobaw/`); they held on the whole census (orders ≤ 27). The floor held on the three counterexample families reported. The group-level statements, σC with the assignment certificate (`sigmaC_of_assignment_groups`) and `SigmaUnionCConj`, have no known failure (0 failing groups in ~368M at order 27; Job BI: 284/284 hit-graph Γ-cycle records pass the weakest per-cycle statements). But σC, σ′C and charge-back P₁ were group-checked on only 3 of the 61 graphs; Job BJ backfills them. About twenty jobs and most hand effort went into the chain that Job AW then refuted.
2. **The weak-F6 theorems sit in reducible territory and do not move 4CT.** A hole with four consecutive degree-5 link vertices contains a Birkhoff diamond, which is formally reducible and excluded from minimal counterexamples (NightWeakForm). F5 and weak F6 are true theorems about configurations the frame already excludes. Frame-class holes have no three 5s in a row, so any unavoidable set must contain (6,6,6,6,6). **The honest open gap is G66: the weak form (no all-DL π-orbit) at (6,6,6,6,6) on the frame class, plus a discharging set of patterns where it holds.** Every σ-exit lemma needs three consecutive 5s and gives nothing there.

## Running or queued this morning

- Studio Job BJ: adversarial search on SigmaUnionC, on statement (c) (some σ-image of a Γ-cycle Z lands on T with Λ(T) ≤ −Λ(Z)) and on the floor; Job BK: (c) and the giant negative cycle over the whole census.
- G66: Studio Jobs BL (which link patterns get PureClean), BO (DL run lengths and lock-death rules at all-6 holes), BP (a σ-analogue at all-6 holes); hand agents NightG66, NightBudget (B′), NightStatementC; Lean `QuarterHole66.lean` (DD-step table at the all-6 hole).
- Not yet formal: the degree bridge for d ≥ 7 (`Hole6Gen` from degrees).

## Recommended next moves (NightPostAW, NightWeakForm)

1. Attack G66 directly: data and a hand/Lean argument at (6,6,6,6,6) (Jobs BO, BP, NightG66), since everything proved so far lives away from it.
2. Adversarially search SigmaUnionC and statement (c) (Job BJ) before investing in any proof: treat every census-only regularity as provisional until a flip search has tried to break it.
3. Consolidate in Lean: state the per-group budget B′ and the exact conjecture being tested, and pair the discharging argument with an unavoidable set. Do not resume A₃₄′, W2, two-pocket, potential or bounded-distance work.

## Reproducibility

`SolvingFrameworkPlan/docs/working/StudioMathLean/check.sh [built-checkout] [scratch-dir]`. The coordinator's full run (947697a0, 05:33): 66/66 modules compile (42 night modules plus 24 earlier PlaneMap modules, against `$HOME/mathlib4-planemap`), 0 errors, 0 `sorryAx` in 199 `#print axioms` lines, standard axioms only; log at the coordinator's scratchpad `check-full4.log`. I did not rerun it. Full detail, counts and killed routes: `NightF6Status.md`; day-by-day record: `NightLog-2026-10-06.md`.
