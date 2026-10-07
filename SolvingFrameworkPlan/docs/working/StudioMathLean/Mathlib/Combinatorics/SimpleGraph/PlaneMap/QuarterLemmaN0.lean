/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLemmaP
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFlowIdentity

/-!
# Lemma N₀: lockless states need negative `λ`-mass

Formalises "Lemma N₀" of `NightImagesBoundary.md` §1. Pure bookkeeping from `exact_identity`
(`QuarterLemmaP`) and `sum_lam` (`QuarterWinding`); no geometry.

## Main results (sorry-free, no new axioms)

* `lemmaN0`: on a finite `π`-invariant set `S` of proper-off states,
  `2·N₀(S) ≤ |DD(S)| − Σ_S λ` (since `E₂, τ ≥ 0`).
* `orbFin_bijOn`, `lemmaN0_orbit`: the same for a single `π`-orbit `orbFin P c`.
* `lam_sum_eq_card_sub_four_filled`: `Σ_S λ = |S| − 4·F(S)` (`sum_lam`), hence
  `lemmaN0'`: `2·N₀(S) ≤ |DD(S)| − |S| + 4·F(S)`.
* `no_lockless_of_nonneg_lam`: if `Σ_S λ ≥ |DD(S)|` then `S` has no lockless state;
  `lockless_le_half_of_lam_zero`: if `Σ_S λ = 0` then `2·N₀(S) ≤ |DD(S)|`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h}
  {S : Finset (Fin n → Fin 4)}

open Classical in
/-- **Lemma N₀.** On a finite `π`-invariant set of proper-off states,
`2·N₀ ≤ |DD| − Σ λ`. -/
theorem lemmaN0 (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S) :
    2 * ((S.filter (NoLock P)).card : ℤ) ≤ (S.filter (DDStep P)).card - ∑ c ∈ S, lam P c := by
  rw [exact_identity hS hb]
  omega

/-- `π` is a bijection of the orbit `orbFin P c` of a proper-off state. -/
theorem orbFin_bijOn {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) :
    Set.BijOn (piMove P) ↑(orbFin P c) ↑(orbFin P c) := by
  have hm : Set.MapsTo (piMove P) ↑(orbFin P c) ↑(orbFin P c) :=
    fun _ hd => piMove_mem_orbFin hd
  refine ((orbFin P c).finite_toSet.injOn_iff_bijOn_of_mapsTo hm).1 ?_
  intro x hx y hy hxy
  have h1 := piInv_piMove (P := P) (properOff_of_mem_orbFin hc hx)
  have h2 := piInv_piMove (P := P) (properOff_of_mem_orbFin hc hy)
  rw [← h1, ← h2, hxy]

open Classical in
/-- **Lemma N₀ on a `π`-orbit** `T = orbFin P c`: `2·N₀(T) ≤ |DD_T| − Λ(T)`. -/
theorem lemmaN0_orbit {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) :
    2 * (((orbFin P c).filter (NoLock P)).card : ℤ) ≤
      ((orbFin P c).filter (DDStep P)).card - orbSum P (orbFin P c) :=
  lemmaN0 (fun _ hd => properOff_of_mem_orbFin hc hd) (orbFin_bijOn hc)

open Classical in
/-- `Σ_S λ = |S| − 4·F(S)` (`sum_lam`, Theorem W counting identity). -/
theorem lam_sum_eq_card_sub_four_filled (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) :
    ∑ c ∈ S, lam P c = (S.card : ℤ) - 4 * (S.filter (Target M.graph h)).card :=
  sum_lam hS hb

open Classical in
/-- **Lemma N₀, filled-count form.** `2·N₀(S) ≤ |DD(S)| − |S| + 4·F(S)`. -/
theorem lemmaN0' (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S) :
    2 * ((S.filter (NoLock P)).card : ℤ) ≤
      (S.filter (DDStep P)).card - S.card + 4 * (S.filter (Target M.graph h)).card := by
  have := lemmaN0 hS hb
  rw [lam_sum_eq_card_sub_four_filled hS hb] at this
  omega

open Classical in
/-- If `Σ_S λ ≥ |DD(S)|`, then `S` has no lockless state. -/
theorem no_lockless_of_nonneg_lam (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S)
    (hL : ((S.filter (DDStep P)).card : ℤ) ≤ ∑ c ∈ S, lam P c) :
    ∀ c ∈ S, ¬ NoLock P c := by
  have h0 := lemmaN0 hS hb
  have hz : (S.filter (NoLock P)).card = 0 := by omega
  intro c hc hN
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff] at hz
  exact hz hc hN

open Classical in
/-- If `Σ_S λ = 0`, then `2·N₀(S) ≤ |DD(S)|`. -/
theorem lockless_le_half_of_lam_zero (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) (hL : ∑ c ∈ S, lam P c = 0) :
    2 * (S.filter (NoLock P)).card ≤ (S.filter (DDStep P)).card := by
  have := lemmaN0 hS hb
  rw [hL] at this
  omega

end sphere

end SimpleGraph.QuarterFloor

/-! ### Axiom check -/
#print axioms SimpleGraph.QuarterFloor.lemmaN0
#print axioms SimpleGraph.QuarterFloor.orbFin_bijOn
#print axioms SimpleGraph.QuarterFloor.lemmaN0_orbit
#print axioms SimpleGraph.QuarterFloor.lam_sum_eq_card_sub_four_filled
#print axioms SimpleGraph.QuarterFloor.lemmaN0'
#print axioms SimpleGraph.QuarterFloor.no_lockless_of_nonneg_lam
#print axioms SimpleGraph.QuarterFloor.lockless_le_half_of_lam_zero
