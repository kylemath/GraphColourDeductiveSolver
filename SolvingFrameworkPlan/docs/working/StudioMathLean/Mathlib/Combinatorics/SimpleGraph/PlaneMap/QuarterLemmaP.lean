/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterExcursion

/-!
# Lemma P: the lock type of an unfilled state is its place in its unfilled run

Formalises "Lemma P" and "Corollary W′" of `NightSigmaImage.md` §1.

## Main results (sorry-free, no new axioms)

* (1) `unfilled_succ_iff_lock2`: at an unfilled state `U_j`, `π c` is unfilled iff `Lock2`
  (`π` is `R₊₃` exactly under `Lock2`, landing in `U_{j+3}`; otherwise `φ_B⁻¹` lands in `F`).
* (2) `unfilled_pred_iff_lock1`: `π⁻¹ c` is unfilled iff `Lock1` (`π⁻¹` is `R₊₂` exactly under
  `Lock1`, landing in `U_{j+2}`; otherwise `φ_A⁻¹` lands in `F`).
* (3) **`lemmaP`**, the four-way classification of an unfilled state `c` (repeat index `j`):
  doubly locked ⇔ both neighbours unfilled (interior of its run); `Lock2`-only ⇔ predecessor
  filled, successor unfilled (start of a run with `u ≥ 2`); `Lock1`-only ⇔ predecessor
  unfilled, successor filled (end of a run with `u ≥ 2`); lockless ⇔ both neighbours filled
  (`u = 1`). `lemmaP_excursion`: inside an excursion `(e, u, f)`, the state `π^k e` (`k < u`)
  has `Lock1 ⇔ 0 < k` and `Lock2 ⇔ k + 1 < u`. Also `dlState_iff`, `noLock_iff`, and
  `filled_succ_iff_m3long` (a filled state has a filled successor iff it is `M3`-long, i.e. its
  move is `τ`).
* (4) **`exact_identity`**: on any finite `π`-invariant set `S` of proper-off states (a `π`-orbit,
  a union of orbits, a Kempe class: `exact_identity_class`),
  `Σ_S λ = |DD| − 2·N₀ − E₂ − 3·τ`, where
  - `|DD| = #{c | DDStep c}` (both `c` and `π c` doubly locked: the `DL → DL` steps),
  - `N₀ = #{c | NoLock c}` (lockless states = excursions with `u = 1`),
  - `E₂ = #{c | E2Start c}` (`π⁻¹ c` filled, `c`, `π c` unfilled, `π² c` filled: the first
    states of excursions with `u = 2`),
  - `τ = #{c | TauStep c}` (`c` and `π c` filled; `= Σ (f − 1)` over excursions; equivalently
    filled `M3`-long states, `filled_succ_iff_m3long`).

  The proof is the short way via Lemma P: pointwise, with the telescoping term
  `g c = [Lock1-only c] − [Lock2-only c] − [lockless c]` (written through the fill pattern of
  `π⁻¹ c, c, π c`),
  `λ c = [DD c] − 2[N₀ c] − [E₂ c] − 3[τ c] + g (π c) − g c` (`lam_eq_exact`), checked over the
  16 fill patterns of `(π⁻¹ c, c, π c, π² c)` from `lam_eq`. Summing over `S`, the `g`-terms
  cancel (`sum_comp_piMove`). Compared with `sum_lam` (`Σλ = |S| − 4F`, `QuarterWinding`) this
  splits the same total by lock type; it is equivalent to `excursion_mass` summed over the
  excursions (`u − 3f = (u − 3) − 3(f − 1)` for `u ≥ 3`, `−1 − 3(f − 1)` for `u = 2`,
  `−2 − 3(f − 1)` for `u = 1`), and on a `Γ`-cycle (no filled state) it reads `Σλ = |DD|`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h}
  {c e : Fin n → Fin 4} {j : Fin 5}

/-! ### (1), (2) The successor / predecessor tests -/

/-- **Lemma P (forward).** At an unfilled state, `π c` is unfilled iff `Lock2`. -/
theorem unfilled_succ_iff_lock2 (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    ¬ Target M.graph h (piMove P c) ↔ Lock2 P c j := by
  rw [piMove_rep hr]
  by_cases hl : Lock2 P c j
  · rw [ite_eq_left hl]
    exact ⟨fun _ => hl, fun _ => rep_not_target (rot3_move hc hr hl).2.2.1⟩
  · rw [ite_eq_right hl]
    exact ⟨fun hu => absurd (phiBinv_spec hc hr hl).2.2.1.1 hu, fun h' => absurd h' hl⟩

/-- **Lemma P (backward).** At an unfilled state, `π⁻¹ c` is unfilled iff `Lock1`. -/
theorem unfilled_pred_iff_lock1 (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    ¬ Target M.graph h (piInv P c) ↔ Lock1 P c j := by
  rw [piInv_rep hr]
  by_cases hl : Lock1 P c j
  · rw [ite_eq_left hl]
    exact ⟨fun _ => hl, fun _ => rep_not_target (rot2_move hc hr hl).2.2.1⟩
  · rw [ite_eq_right hl]
    exact ⟨fun hu => absurd (phiAinv_spec hc hr hl).2.2.1.1 hu, fun h' => absurd h' hl⟩

/-- At a filled state, `π c` is filled iff the state is `M3`-long (its move is `τ`). -/
theorem filled_succ_iff_m3long (hc : ProperOff M.graph h c) {i : Fin 5}
    (hs : SingletonAt P c i) : Target M.graph h (piMove P c) ↔ ¬ M3Short P c i := by
  rw [piMove_single hc hs]
  by_cases hm : M3Short P c i
  · rw [ite_eq_left hm]
    exact ⟨fun ht => absurd ht (rep_not_target (phiA_spec hc hs hm).2.2.1), fun h' => absurd hm h'⟩
  · rw [ite_eq_right hm]
    exact ⟨fun _ => hm, fun _ => (tau_spec hc hs hm).2.2.1.1⟩

/-! ### (3) Lemma P: the four-way classification -/

/-- **Lemma P.** The lock type of an unfilled state `U_j` fixes its place in its unfilled run. -/
theorem lemmaP (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    (Lock1 P c j ∧ Lock2 P c j ↔
      ¬ Target M.graph h (piInv P c) ∧ ¬ Target M.graph h (piMove P c)) ∧
    (¬ Lock1 P c j ∧ Lock2 P c j ↔
      Target M.graph h (piInv P c) ∧ ¬ Target M.graph h (piMove P c)) ∧
    (Lock1 P c j ∧ ¬ Lock2 P c j ↔
      ¬ Target M.graph h (piInv P c) ∧ Target M.graph h (piMove P c)) ∧
    (¬ Lock1 P c j ∧ ¬ Lock2 P c j ↔
      Target M.graph h (piInv P c) ∧ Target M.graph h (piMove P c)) := by
  have a := unfilled_pred_iff_lock1 hc hr
  have b := unfilled_succ_iff_lock2 hc hr
  refine ⟨?_, ?_, ?_, ?_⟩ <;> rw [← a, ← b] <;> simp only [not_not]

/-- **Lemma P in excursion form.** In an excursion `(e, u, f)`, the unfilled state `π^k e`
(`k < u`) has `Lock1` iff it is not the first state, and `Lock2` iff it is not the last
unfilled state. So: doubly locked ⇔ `0 < k < u − 1`; `Lock2`-only ⇔ `k = 0 < u − 1`;
`Lock1`-only ⇔ `0 < k = u − 1`; lockless ⇔ `k = 0 = u − 1`. -/
theorem lemmaP_excursion {u f k : ℕ} (E : Excursion P e u f) (hk : k < u)
    (hr : RepeatAt P ((piMove P)^[k] e) j) :
    (Lock1 P ((piMove P)^[k] e) j ↔ 0 < k) ∧ (Lock2 P ((piMove P)^[k] e) j ↔ k + 1 < u) := by
  have hp := iter_properOff (P := P) E.proper
  refine ⟨?_, ?_⟩
  · rw [← unfilled_pred_iff_lock1 (hp k) hr]
    rcases k with _ | k
    · simp only [Function.iterate_zero, id, lt_irrefl, iff_false, not_not]
      exact E.prev
    · rw [Function.iterate_succ_apply', piInv_piMove (hp k)]
      exact ⟨fun _ => Nat.succ_pos k, fun _ => E.unf k (by omega)⟩
  · rw [← unfilled_succ_iff_lock2 (hp k) hr, ← Function.iterate_succ_apply' (piMove P)]
    constructor
    · intro hu
      by_contra hl
      exact hu (E.fil (k + 1) (by omega) (by have := E.f_pos; omega))
    · intro hl
      exact E.unf (k + 1) hl

/-- A doubly locked state is an unfilled state with both neighbours unfilled. -/
theorem dlState_iff (hc : ProperOff M.graph h c) :
    DLState P c ↔ ¬ Target M.graph h c ∧ ¬ Target M.graph h (piInv P c) ∧
      ¬ Target M.graph h (piMove P c) := by
  constructor
  · rintro ⟨j, hr, l1, l2⟩
    exact ⟨rep_not_target hr, (unfilled_pred_iff_lock1 hc hr).2 l1,
      (unfilled_succ_iff_lock2 hc hr).2 l2⟩
  · rintro ⟨hu, a, b⟩
    rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
    · exact ⟨j, hr, (unfilled_pred_iff_lock1 hc hr).1 a, (unfilled_succ_iff_lock2 hc hr).1 b⟩
    · exact absurd hs.1 hu

/-- A lockless state is an unfilled state with both neighbours filled. -/
theorem noLock_iff (hc : ProperOff M.graph h c) :
    NoLock P c ↔ ¬ Target M.graph h c ∧ Target M.graph h (piInv P c) ∧
      Target M.graph h (piMove P c) := by
  constructor
  · intro hN
    exact ⟨noLock_unfilled hN, noLock_prev_filled hc hN, noLock_next_filled hc hN⟩
  · rintro ⟨hu, a, b⟩
    rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
    · refine ⟨j, hr, fun l => ?_, fun l => ?_⟩
      · exact (unfilled_pred_iff_lock1 hc hr).2 l a
      · exact (unfilled_succ_iff_lock2 hc hr).2 l b
    · exact absurd hs.1 hu

/-! ### (4) The exact identity -/

variable (P) in
/-- `c` is the first state of an excursion with `u = 2`. -/
def E2Start (c : Fin n → Fin 4) : Prop :=
  Target M.graph h (piInv P c) ∧ ¬ Target M.graph h c ∧ ¬ Target M.graph h (piMove P c) ∧
    Target M.graph h (piMove P (piMove P c))

variable (P) in
/-- A `τ` step: `c` and `π c` both filled (`τ = Σ (f − 1)` over excursions). -/
def TauStep (c : Fin n → Fin 4) : Prop :=
  Target M.graph h c ∧ Target M.graph h (piMove P c)

variable (P) in
open Classical in
/-- The telescoping term `g = [Lock1-only] − [Lock2-only] − [lockless]`, through the fill
pattern (Lemma P). -/
noncomputable def gLP (c : Fin n → Fin 4) : ℤ :=
  if ¬ Target M.graph h c ∧ ¬ Target M.graph h (piInv P c) ∧ Target M.graph h (piMove P c) then 1
  else if ¬ Target M.graph h c ∧ Target M.graph h (piInv P c) then -1 else 0

open Classical in
/-- **Pointwise exact identity.**
`λ c = [DD c] − 2[N₀ c] − [E₂ c] − 3[τ c] + g (π c) − g c`. -/
theorem lam_eq_exact (hc : ProperOff M.graph h c) :
    lam P c = (if DDStep P c then 1 else 0) - 2 * (if NoLock P c then 1 else 0)
      - (if E2Start P c then 1 else 0) - 3 * (if TauStep P c then 1 else 0)
      + gLP P (piMove P c) - gLP P c := by
  have hc1 := piMove_properOff (P := P) hc
  have hdd : DDStep P c ↔ ¬ Target M.graph h (piInv P c) ∧ ¬ Target M.graph h c ∧
      ¬ Target M.graph h (piMove P c) ∧ ¬ Target M.graph h (piMove P (piMove P c)) := by
    unfold DDStep
    rw [dlState_iff hc, dlState_iff hc1, piInv_piMove hc]
    tauto
  rw [lam_eq hc]
  unfold gLP filledZ E2Start TauStep
  rw [piInv_piMove hc, noLock_iff hc]
  simp only [hdd]
  by_cases a : Target M.graph h (piInv P c) <;> by_cases b : Target M.graph h c <;>
    by_cases d : Target M.graph h (piMove P c) <;>
    by_cases e : Target M.graph h (piMove P (piMove P c)) <;>
    simp [a, b, d, e]

variable {S : Finset (Fin n → Fin 4)}

open Classical in
/-- **The exact identity** (`NightSigmaImage.md`, Corollary W′): on a finite `π`-invariant set of
proper-off states (e.g. a `π`-orbit), `Σ λ = |DD| − 2 N₀ − E₂ − 3 τ`. -/
theorem exact_identity (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S) :
    ∑ c ∈ S, lam P c = ((S.filter (DDStep P)).card : ℤ) - 2 * (S.filter (NoLock P)).card
      - (S.filter (E2Start P)).card - 3 * (S.filter (TauStep P)).card := by
  rw [Finset.sum_congr rfl fun c hc => lam_eq_exact (P := P) (hS c hc)]
  simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum,
    sum_comp_piMove hb (gLP P), Finset.sum_boole]
  ring

open Classical in
/-- The exact identity on a Kempe class. -/
theorem exact_identity_class (c₀ : Fin n → Fin 4) :
    ∑ c ∈ kclass M h c₀, lam P c =
      (((kclass M h c₀).filter (DDStep P)).card : ℤ) - 2 * ((kclass M h c₀).filter (NoLock P)).card
      - ((kclass M h c₀).filter (E2Start P)).card
      - 3 * ((kclass M h c₀).filter (TauStep P)).card :=
  exact_identity (kclass_properOff c₀) (kclass_bijOn c₀)

end sphere

end SimpleGraph.QuarterFloor

/-! ### Axiom check -/
#print axioms SimpleGraph.QuarterFloor.unfilled_succ_iff_lock2
#print axioms SimpleGraph.QuarterFloor.unfilled_pred_iff_lock1
#print axioms SimpleGraph.QuarterFloor.lemmaP
#print axioms SimpleGraph.QuarterFloor.lemmaP_excursion
#print axioms SimpleGraph.QuarterFloor.exact_identity
#print axioms SimpleGraph.QuarterFloor.exact_identity_class
