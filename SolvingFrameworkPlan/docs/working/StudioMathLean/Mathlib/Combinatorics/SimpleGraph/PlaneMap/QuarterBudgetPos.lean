/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterBudget
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFlowIdentity

/-!
# `B′` is only needed on groups with a positive orbit

Studio Job BV (`NightLog-2026-10-06.md`, 07:05) found that the universal budget `B′` fails, but
only on `σ ∪ σ′`-groups with **no positive `π`-orbit** (and `Σ λ = 0`). Such groups need no
budget at all: the orbits partition the group (`sum_lam_eq_sum_orbits`), so if every orbit has
`Λ ≤ 0` then `Σ_g λ ≤ 0`.

## Main results (sorry-free, no new axioms)

* `sum_lam_le_of_no_pos`: a finite `π`-invariant set of proper-off states with no positive orbit
  has `Σ λ ≤ 0`.
* **`sigmaUnionC_of_budget_pos`**: `B′` on every `σ ∪ σ′`-group that contains a positive orbit
  implies `SigmaUnionC P` (any `T`).
* `quarterFloor_of_budget_pos`, `sigmaC_of_budget_pos` (for `σ`-groups).
* `sigmaUnionC_iff_pos`: `SigmaUnionC P ⇔ Σ λ ≤ 0` on every `σ ∪ σ′`-group with a positive orbit.
  So the reduction to positive-orbit groups is an equivalence, whereas `B′` on those groups is
  only a **sufficient certificate** for `Σ λ ≤ 0` (`sum_lam_le_of_budget`), not equivalent to it.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {T : (Fin n → Fin 4) → Prop} {g : Finset (Fin n → Fin 4)}

/-- **No positive orbit ⇒ `Σ λ ≤ 0`**: the orbits partition `g`. -/
theorem sum_lam_le_of_no_pos (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hinv : Set.MapsTo (piMove P) (g : Set _) g) (h0 : posOrbits P g = ∅) :
    ∑ d ∈ g, lam P d ≤ 0 := by
  classical
  rw [sum_lam_eq_sum_orbits hp hinv]
  refine Finset.sum_nonpos fun Z hZ => ?_
  by_contra hlt
  have : Z ∈ posOrbits P g := by
    unfold posOrbits
    exact Finset.mem_filter.2 ⟨hZ, lt_of_not_ge hlt⟩
  simp [h0] at this

/-- On a group (finite, `π`-invariant, proper-off), `Σ λ ≤ 0` follows from `B′` whenever the
group has a positive orbit. -/
theorem sum_lam_le_of_budget_pos (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hb : Set.BijOn (piMove P) ↑g ↑g) (hσ : ∀ r ∈ budgetR P T g, budgetSigma P r ∈ g)
    (hB : (posOrbits P g).Nonempty → BudgetB' P T g) : ∑ d ∈ g, lam P d ≤ 0 := by
  rcases (posOrbits P g).eq_empty_or_nonempty with h0 | hne
  · exact sum_lam_le_of_no_pos hp hb.mapsTo h0
  · exact sum_lam_le_of_budget hp hb hσ (hB hne)

variable (P T) in
/-- `B′` on every `σ ∪ σ′`-group that contains a positive `π`-orbit. -/
def BudgetUnionPos : Prop :=
  ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ →
    ∀ c ∈ kclass M h c₀, (posOrbits P (sigmaUnionGroup P c₀ c)).Nonempty →
      BudgetB' P T (sigmaUnionGroup P c₀ c)

/-- `B′` on every group is in particular `B′` on the groups with a positive orbit. -/
lemma BudgetUnion.pos (H : BudgetUnion P T) : BudgetUnionPos P T :=
  fun c₀ h₀ c hc _ => H c₀ h₀ c hc

/-- **`B′` on the `σ ∪ σ′`-groups with a positive orbit implies `SigmaUnionC`**, for any `T`.
Groups without a positive orbit (where Job BV found `B′` to fail) are handled by
`sum_lam_le_of_no_pos`. -/
theorem sigmaUnionC_of_budget_pos (H : BudgetUnionPos P T) : SigmaUnionC P :=
  fun c₀ h₀ c hc => sum_lam_le_of_budget_pos linkGroup_properOff linkGroup_piInvariant
    (budgetSigma_mem_linkGroup fun _ _ => Or.inl) (H c₀ h₀ c hc)

/-- `B′` on the `σ ∪ σ′`-groups with a positive orbit gives the quarter floor at the hole. -/
theorem quarterFloor_of_budget_pos (H : BudgetUnionPos P T) :
    QuarterFloorConj (G := M.graph) (h := h) :=
  sigmaUnionC_imp_quarterFloor (sigmaUnionC_of_budget_pos H)

/-- `B′` on the `σ`-groups with a positive orbit implies `σC`. -/
theorem sigmaC_of_budget_pos
    (H : ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ → ∀ c ∈ kclass M h c₀,
      (posOrbits P (linkGroup P (sigmaLink P) c₀ c)).Nonempty →
        BudgetB' P T (linkGroup P (sigmaLink P) c₀ c)) : SigmaC P :=
  fun c₀ h₀ c hc => sigmaGroup_eq_linkGroup (P := P) ▸
    sum_lam_le_of_budget_pos linkGroup_properOff linkGroup_piInvariant
      (budgetSigma_mem_linkGroup fun _ _ => id) (H c₀ h₀ c hc)

/-- **`SigmaUnionC` only concerns groups with a positive orbit**: `SigmaUnionC P` holds iff
`Σ λ ≤ 0` on every `σ ∪ σ′`-group that has a positive orbit. (`B′` on those groups is a
sufficient certificate for the right-hand side, not an equivalent one.) -/
theorem sigmaUnionC_iff_pos : SigmaUnionC P ↔
    ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ → ∀ c ∈ kclass M h c₀,
      (posOrbits P (sigmaUnionGroup P c₀ c)).Nonempty →
        ∑ d ∈ sigmaUnionGroup P c₀ c, lam P d ≤ 0 := by
  refine ⟨fun H c₀ h₀ c hc _ => H c₀ h₀ c hc, fun H c₀ h₀ c hc => ?_⟩
  rcases (posOrbits P (sigmaUnionGroup P c₀ c)).eq_empty_or_nonempty with h0 | hne
  · exact sum_lam_le_of_no_pos linkGroup_properOff linkGroup_piInvariant.mapsTo h0
  · exact H c₀ h₀ c hc hne

end sphere

end SimpleGraph.QuarterFloor

/-! ### Axiom check -/
#print axioms SimpleGraph.QuarterFloor.sum_lam_le_of_no_pos
#print axioms SimpleGraph.QuarterFloor.sum_lam_le_of_budget_pos
#print axioms SimpleGraph.QuarterFloor.sigmaUnionC_of_budget_pos
#print axioms SimpleGraph.QuarterFloor.quarterFloor_of_budget_pos
#print axioms SimpleGraph.QuarterFloor.sigmaC_of_budget_pos
#print axioms SimpleGraph.QuarterFloor.sigmaUnionC_iff_pos
