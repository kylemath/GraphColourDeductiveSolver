/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaPrime
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLemmaP

/-!
# The per-group budget `B′` and the implication `B′ ⇒ SigmaUnionC`

Formalises `NightBudget.md` §1 (Lemma B0, Lemma B1 (i)–(iii)). Fix a pentagonal hole `P` and a
predicate `T` on states (the "`R3` type"; F5's instance is `T d := ∃ j, R3At P w d j`, the
Studio's degree-6 convention is another; every result below holds for any `T`).

On a finite `π`-invariant set `S` of proper-off states (a `σ`-group, a `σ ∪ σ′`-group, a class):

* `budgetRho P T d` (`ρ`): F5's charging map with fallback, `ρ d = d` if `T d`, else `π d` if
  `T (π d)`, else `d`. So `ρ d ∈ {d, π d}` and `ρ` is at most 2-to-1.
* `budgetR P T S` (`R = ρ(DD(S))`): every member is a doubly locked `DD` endpoint in `S`.
* `budgetSigma P r` (`σ`): `sigSwap P r j` at a doubly-locked index `j` of `r` (chosen).
* `budgetRMinus` (`R⁻`): `r ∈ R` with `σ r` not lockless; `budgetRPlus` (`R⁺`): the rest.
* `budgetN0Free` (`N₀ᶠ = N₀(S) ∖ σ(R)`).
* **`BudgetB' P T S`**: `2|R⁻| ≤ 2|N₀ᶠ| + E₂ + 3τ`.

## Main results (sorry-free, no new axioms)

* `budgetR_split`: `|R| = |R⁺| + |R⁻|`.
* `dd_le_two_budgetR`: `|DD(S)| ≤ 2|R|` (`ρ` is at most 2-to-1; no ball hypothesis).
* `budgetSigma_injOn`: `σ` is injective on `R` (`sigSwap_inj'`).
* `noLock_split`: if `σ(R) ⊆ S`, then `N₀(S) = |R⁺| + |N₀ᶠ|`; hence `|R⁺| ≤ N₀ − |N₀ᶠ|`
  (`rplus_add_nofree_le`). (The factor is 1, not 2: `σ` is injective; the 2 sits in
  `|DD| ≤ 2|R|`.)
* `budgetB'_iff`: `B′ ⇔ 2|R| ≤ 2N₀ + E₂ + 3τ` (Lemma B1 (i): `B′` is a pure count).
* `sum_lam_eq_budget`: `Σ_S λ = (|DD| − 2|R|) − slack_B′` (Lemma B1 (ii)).
* **`sum_lam_le_of_budget`**: `B′(S) ⇒ Σ_S λ ≤ 0`.
* `budgetSigma_mem_linkGroup`: on an `L`-group with `L ⊇ σ`, `σ(R) ⊆ group`.
* **`sigmaUnionC_of_budget`**: `B′` on every `σ ∪ σ′`-group ⇒ `SigmaUnionC P`
  (Lemma B1 (iii)); `quarterFloor_of_budget`; and `sigmaC_of_budget` for `σ`-groups.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-! ### Definitions -/

section defs
variable (P : Pent M.graph h) (T : (Fin n → Fin 4) → Prop)

open Classical in
/-- `ρ`: F5's charging map with fallback (`NightBudget.md` §1). -/
noncomputable def budgetRho (d : Fin n → Fin 4) : Fin n → Fin 4 :=
  if T d then d else if T (piMove P d) then piMove P d else d

open Classical in
/-- `σ`: the swap `sigSwap P r j` at a (chosen) doubly-locked index `j`; the identity off `DL`. -/
noncomputable def budgetSigma (r : Fin n → Fin 4) : Fin n → Fin 4 :=
  if hx : DLState P r then sigSwap P r hx.choose else r

open Classical in
/-- `R = ρ(DD(S))`. -/
noncomputable def budgetR (S : Finset (Fin n → Fin 4)) : Finset (Fin n → Fin 4) :=
  (S.filter (DDStep P)).image (budgetRho P T)

open Classical in
/-- `R⁻`: the states of `R` whose `σ`-image is not lockless. -/
noncomputable def budgetRMinus (S : Finset (Fin n → Fin 4)) : Finset (Fin n → Fin 4) :=
  (budgetR P T S).filter (fun r => ¬ NoLock P (budgetSigma P r))

open Classical in
/-- `R⁺`: the states of `R` whose `σ`-image is lockless. -/
noncomputable def budgetRPlus (S : Finset (Fin n → Fin 4)) : Finset (Fin n → Fin 4) :=
  (budgetR P T S).filter (fun r => NoLock P (budgetSigma P r))

open Classical in
/-- `N₀ᶠ = N₀(S) ∖ σ(R)`: the lockless states not hit by `σ` from `R`. -/
noncomputable def budgetN0Free (S : Finset (Fin n → Fin 4)) : Finset (Fin n → Fin 4) :=
  (S.filter (NoLock P)) \ (budgetR P T S).image (budgetSigma P)

open Classical in
/-- **The budget `B′`** (`NightBudget.md` §1): `2|R⁻| ≤ 2|N₀ᶠ| + E₂ + 3τ` on `S`. -/
def BudgetB' (S : Finset (Fin n → Fin 4)) : Prop :=
  2 * (budgetRMinus P T S).card ≤
    2 * (budgetN0Free P T S).card + (S.filter (E2Start P)).card + 3 * (S.filter (TauStep P)).card

end defs

variable {P : Pent M.graph h} {T : (Fin n → Fin 4) → Prop} {S : Finset (Fin n → Fin 4)}
  {c₀ c d r : Fin n → Fin 4}

/-! ### Basic facts on `ρ` and `σ` -/

lemma budgetRho_eq (d : Fin n → Fin 4) :
    budgetRho P T d = d ∨ budgetRho P T d = piMove P d := by
  classical
  unfold budgetRho
  split_ifs <;> simp

/-- Members of `R` lie in `S` and are doubly locked `DD` endpoints. -/
lemma mem_budgetR (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S)
    (hr : r ∈ budgetR P T S) : r ∈ S ∧ DDEnd P r ∧ DLState P r := by
  classical
  unfold budgetR at hr
  obtain ⟨d, hd, rfl⟩ := Finset.mem_image.1 hr
  obtain ⟨hdS, hdd⟩ := Finset.mem_filter.1 hd
  rcases budgetRho_eq (P := P) (T := T) d with e | e <;> rw [e]
  · exact ⟨hdS, Or.inl hdd, hdd.1⟩
  · exact ⟨hb.mapsTo hdS, Or.inr (by rw [piInv_piMove (hS d hdS)]; exact hdd), hdd.2⟩

lemma budgetSigma_of_dl (hx : DLState P r) : budgetSigma P r = sigSwap P r hx.choose :=
  dite_eq_left hx

/-- At a doubly locked `DD` endpoint, `r ↦ σ r` is a `σ`-link (Lemma B0 (c)). -/
lemma sigmaLink_budgetSigma (hE : DDEnd P r) (hx : DLState P r) :
    sigmaLink P r (budgetSigma P r) :=
  ⟨hE, hx.choose, hx.choose_spec, budgetSigma_of_dl hx⟩

/-- **`σ` is injective on `R`** (no ball hypothesis; `sigSwap_inj'`). -/
theorem budgetSigma_injOn (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) :
    Set.InjOn (budgetSigma P) ↑(budgetR P T S) := by
  intro r hr r' hr' E
  obtain ⟨hrS, -, hx⟩ := mem_budgetR hS hb (Finset.mem_coe.1 hr)
  obtain ⟨hrS', -, hx'⟩ := mem_budgetR hS hb (Finset.mem_coe.1 hr')
  rw [budgetSigma_of_dl hx, budgetSigma_of_dl hx'] at E
  exact (sigSwap_inj' (hS r hrS) hx.choose_spec.1 (hS r' hrS') hx'.choose_spec.1 E).1

/-! ### The counts -/

open Classical in
/-- `|R| = |R⁺| + |R⁻|`. -/
theorem budgetR_split :
    (budgetR P T S).card = (budgetRPlus P T S).card + (budgetRMinus P T S).card := by
  unfold budgetRPlus budgetRMinus
  exact (Finset.card_filter_add_card_filter_not _).symm

open Classical in
/-- **`|DD(S)| ≤ 2|R|`**: `ρ` is at most 2-to-1 (`ρ d ∈ {d, π d}`), for any `T`. -/
theorem dd_le_two_budgetR (hS : ∀ c ∈ S, ProperOff M.graph h c) :
    (S.filter (DDStep P)).card ≤ 2 * (budgetR P T S).card := by
  refine Finset.card_le_mul_card_image_of_maps_to (f := budgetRho P T)
    (fun d hd => Finset.mem_image_of_mem _ hd) 2 ?_
  intro r _
  refine (Finset.card_le_card ?_).trans (Finset.card_le_two (a := r) (b := piInv P r))
  intro d hd
  obtain ⟨hdD, hfd⟩ := Finset.mem_filter.1 hd
  have hp := hS d (Finset.mem_filter.1 hdD).1
  rcases budgetRho_eq (P := P) (T := T) d with e | e <;> rw [e] at hfd
  · simp [hfd]
  · have : d = piInv P r := by rw [← hfd, piInv_piMove hp]
    simp [this]

open Classical in
/-- **`N₀(S) = |R⁺| + |N₀ᶠ|`**, when `σ` maps `R` into `S` (Lemma B1 (i)): `σ` is injective on `R`
and `σ(R) ∩ N₀(S) = σ(R⁺)`. -/
theorem noLock_split (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S)
    (hσ : ∀ r ∈ budgetR P T S, budgetSigma P r ∈ S) :
    (S.filter (NoLock P)).card = (budgetRPlus P T S).card + (budgetN0Free P T S).card := by
  have hsub : budgetRPlus P T S ⊆ budgetR P T S := Finset.filter_subset _ _
  have e : S.filter (NoLock P) =
      (budgetRPlus P T S).image (budgetSigma P) ∪ budgetN0Free P T S := by
    ext x
    simp only [Finset.mem_union, Finset.mem_image, budgetN0Free, Finset.mem_sdiff,
      Finset.mem_filter, budgetRPlus]
    constructor
    · rintro ⟨hxS, hxN⟩
      by_cases hx : ∃ r ∈ budgetR P T S, budgetSigma P r = x
      · obtain ⟨r, hr, rfl⟩ := hx
        exact Or.inl ⟨r, ⟨hr, hxN⟩, rfl⟩
      · exact Or.inr ⟨⟨hxS, hxN⟩, hx⟩
    · rintro (⟨r, ⟨hr, hN⟩, rfl⟩ | ⟨hx, -⟩)
      · exact ⟨hσ r hr, hN⟩
      · exact hx
  have hdis : Disjoint ((budgetRPlus P T S).image (budgetSigma P)) (budgetN0Free P T S) := by
    rw [Finset.disjoint_left]
    intro x hx hx'
    obtain ⟨r, hr, rfl⟩ := Finset.mem_image.1 hx
    exact (Finset.mem_sdiff.1 hx').2 (Finset.mem_image_of_mem _ (hsub hr))
  rw [e, Finset.card_union_of_disjoint hdis,
    Finset.card_image_of_injOn ((budgetSigma_injOn hS hb).mono (Finset.coe_subset.2 hsub))]

open Classical in
/-- `|R⁺| + |N₀ᶠ| ≤ N₀(S)` (in fact equal, `noLock_split`). -/
theorem rplus_add_nofree_le (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) (hσ : ∀ r ∈ budgetR P T S, budgetSigma P r ∈ S) :
    (budgetRPlus P T S).card + (budgetN0Free P T S).card ≤ (S.filter (NoLock P)).card :=
  (noLock_split hS hb hσ).ge

open Classical in
/-- **`B′` is a pure count** (Lemma B1 (i)): `B′(S) ⇔ 2|R| ≤ 2N₀ + E₂ + 3τ`. -/
theorem budgetB'_iff (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S)
    (hσ : ∀ r ∈ budgetR P T S, budgetSigma P r ∈ S) :
    BudgetB' P T S ↔ 2 * (budgetR P T S).card ≤ 2 * (S.filter (NoLock P)).card +
      (S.filter (E2Start P)).card + 3 * (S.filter (TauStep P)).card := by
  have a := budgetR_split (P := P) (T := T) (S := S)
  have b := noLock_split hS hb hσ
  unfold BudgetB'
  omega

open Classical in
/-- **The exact identity split by the budget** (Lemma B1 (ii)):
`Σ_S λ = (|DD| − 2|R|) − (2|N₀ᶠ| + E₂ + 3τ − 2|R⁻|)`. -/
theorem sum_lam_eq_budget (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) (hσ : ∀ r ∈ budgetR P T S, budgetSigma P r ∈ S) :
    ∑ c ∈ S, lam P c = (((S.filter (DDStep P)).card : ℤ) - 2 * (budgetR P T S).card) -
      (2 * (budgetN0Free P T S).card + (S.filter (E2Start P)).card +
        3 * (S.filter (TauStep P)).card - 2 * (budgetRMinus P T S).card) := by
  rw [exact_identity hS hb]
  have a := budgetR_split (P := P) (T := T) (S := S)
  have b := noLock_split hS hb hσ
  have a' : ((budgetR P T S).card : ℤ) = (budgetRPlus P T S).card + (budgetRMinus P T S).card := by
    exact_mod_cast a
  have b' : ((S.filter (NoLock P)).card : ℤ) =
      (budgetRPlus P T S).card + (budgetN0Free P T S).card := by exact_mod_cast b
  rw [a', b']
  ring

open Classical in
/-- **`B′ ⇒ Σ λ ≤ 0`** on a finite `π`-invariant set with `σ(R) ⊆ S`. -/
theorem sum_lam_le_of_budget (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) (hσ : ∀ r ∈ budgetR P T S, budgetSigma P r ∈ S)
    (hB : BudgetB' P T S) : ∑ c ∈ S, lam P c ≤ 0 := by
  rw [sum_lam_eq_budget hS hb hσ]
  have d := dd_le_two_budgetR (P := P) (T := T) hS
  have d' : ((S.filter (DDStep P)).card : ℤ) ≤ 2 * (budgetR P T S).card := by exact_mod_cast d
  have hB' : (2 * (budgetRMinus P T S).card : ℤ) ≤ 2 * (budgetN0Free P T S).card +
      (S.filter (E2Start P)).card + 3 * (S.filter (TauStep P)).card := by
    unfold BudgetB' at hB; exact_mod_cast hB
  omega

/-! ### Groups -/

variable {L : (Fin n → Fin 4) → (Fin n → Fin 4) → Prop}

/-- On an `L`-group with `L ⊇ σ`, `σ` maps `R` into the group (Lemma B0 (c)). -/
theorem budgetSigma_mem_linkGroup (hL : ∀ c d, sigmaLink P c d → L c d) :
    ∀ r ∈ budgetR P T (linkGroup P L c₀ c), budgetSigma P r ∈ linkGroup P L c₀ c := by
  intro r hr
  obtain ⟨hrS, hE, hx⟩ := mem_budgetR linkGroup_properOff linkGroup_piInvariant hr
  have hl := sigmaLink_budgetSigma hE hx
  exact link_mem_linkGroup hrS (sigmaLink_mem_kclass (linkGroup_subset_kclass hrS) hl) (hL _ _ hl)

/-- **`B′` on an `L`-group (`L ⊇ σ`) gives `Σ λ ≤ 0` there.** -/
theorem sum_lam_linkGroup_le_of_budget (hL : ∀ c d, sigmaLink P c d → L c d)
    (hB : BudgetB' P T (linkGroup P L c₀ c)) : ∑ d ∈ linkGroup P L c₀ c, lam P d ≤ 0 :=
  sum_lam_le_of_budget linkGroup_properOff linkGroup_piInvariant
    (budgetSigma_mem_linkGroup hL) hB

variable (P T) in
/-- `B′` on every `σ ∪ σ′`-group of every Kempe class at the hole `P`. -/
def BudgetUnion : Prop :=
  ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ →
    ∀ c ∈ kclass M h c₀, BudgetB' P T (sigmaUnionGroup P c₀ c)

/-- **`B′` on every `σ ∪ σ′`-group implies `SigmaUnionC`** (Lemma B1 (iii)), for any `T`. -/
theorem sigmaUnionC_of_budget (H : BudgetUnion P T) : SigmaUnionC P :=
  fun c₀ h₀ c hc => sum_lam_linkGroup_le_of_budget (fun _ _ => Or.inl) (H c₀ h₀ c hc)

/-- `B′` on every `σ ∪ σ′`-group gives the quarter floor at the hole. -/
theorem quarterFloor_of_budget (H : BudgetUnion P T) :
    QuarterFloorConj (G := M.graph) (h := h) :=
  sigmaUnionC_imp_quarterFloor (sigmaUnionC_of_budget H)

/-- `B′` on every `σ`-group implies `σC` (the stronger hypothesis; `NightBudget.md` §0 item 4
records that it is false in the data). -/
theorem sigmaC_of_budget
    (H : ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ →
      ∀ c ∈ kclass M h c₀, BudgetB' P T (linkGroup P (sigmaLink P) c₀ c)) : SigmaC P :=
  fun c₀ h₀ c hc => sigmaGroup_eq_linkGroup (P := P) ▸
    sum_lam_linkGroup_le_of_budget (fun _ _ => id) (H c₀ h₀ c hc)

end sphere

end SimpleGraph.QuarterFloor

/-! ### Axiom check -/
#print axioms SimpleGraph.QuarterFloor.budgetR_split
#print axioms SimpleGraph.QuarterFloor.dd_le_two_budgetR
#print axioms SimpleGraph.QuarterFloor.budgetSigma_injOn
#print axioms SimpleGraph.QuarterFloor.noLock_split
#print axioms SimpleGraph.QuarterFloor.budgetB'_iff
#print axioms SimpleGraph.QuarterFloor.sum_lam_eq_budget
#print axioms SimpleGraph.QuarterFloor.sum_lam_le_of_budget
#print axioms SimpleGraph.QuarterFloor.sigmaUnionC_of_budget
#print axioms SimpleGraph.QuarterFloor.quarterFloor_of_budget
#print axioms SimpleGraph.QuarterFloor.sigmaC_of_budget
