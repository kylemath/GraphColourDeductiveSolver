/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterWinding

/-!
# Theorem F5: the quarter floor at an icosahedral hole

Formalises Theorem F5 of `NightFloorAtEasyHoles.md` (commit 6826897): at a pentagonal hole
whose five link vertices have degree five, with the outer ring of the 2-ball as in Theorem H,
every Kempe class satisfies `Σ λ ≤ 0`, i.e. it is at least a quarter filled.

## The hypothesis

`IcoBallP P w` is the library's `VacancyIcosahedral.IcoBall` (the hypothesis of `ico_fill`)
restated in the `Pent` coordinates used by `π`: the neighbours of `x t` are exactly
`h, x (t-1), x (t+1), w (t-1), w t`, the `w t` form a cycle, and they are off the closed
neighbourhood of `h`. The orientation of `P` is arbitrary (no reflection is used).

## Main results (sorry-free)

* `lam_le_pot`: the pointwise form of **Lemma 1**:
  `λ c ≤ [DD c] − 2 [N₀ c] + g (π c) − g c`, with the potential
  `g = +1` on `U` with `Lock1 ∧ ¬Lock2`, `−1` on `U` with `¬Lock1`, `0` otherwise.
* `sum_lam_le` (**Lemma 1**): `Σ_S λ ≤ |DD ∩ S| − 2 |N₀ ∩ S|` on any finite `π`-invariant `S`.
* `ring_type`: at a doubly locked state the outer ring has type `R1`, `R2` or `R3`
  (Theorem H, Step 1).
* `dd_r3` (**Lemma 2**, Theorem H Steps 2 and 4 applied to `π = R₊₃`): every `DD` step has an
  endpoint of type `R3` (the start, or the image at `j + 3`).
* `sigSwap_spec`, `sigSwap_inj` (**Lemma 3**): at an `R3` state, swapping the `{α, μ}`-component
  of `x (j+1)` (which is `{x j, x (j+1), x (j+2)}`) is a Kempe step to a state with neither
  lock, and this map is injective.
* `dd_le_two_noLock`: `|DD| ≤ 2 N₀` in every Kempe class.
* `sum_lam_class_nonpos`, `quarterFloor_of_icoBall` (**Theorem F5**).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Finite facts about `Fin 4` -/

lemma f4_cover {α μ A B : Fin 4} (h1 : μ ≠ α) (h3 : A ≠ α) (h4 : B ≠ α) (h13 : μ ≠ A)
    (h14 : μ ≠ B) (h34 : A ≠ B) (x : Fin 4) : x = α ∨ x = μ ∨ x = A ∨ x = B := by
  revert α μ A B x; decide

/-- The three outer-ring words compatible with both locks (Theorem H, Step 1), in the colours
`α, μ, A, B` of the link word `(α, μ, α, A, B)`. -/
lemma ring_types {α μ A B a0 a1 a2 a3 a4 : Fin 4}
    (h1 : μ ≠ α) (h3 : A ≠ α) (h4 : B ≠ α) (h13 : μ ≠ A) (h14 : μ ≠ B) (h34 : A ≠ B)
    (n0a : a0 ≠ α) (n0m : a0 ≠ μ) (n1m : a1 ≠ μ) (n1a : a1 ≠ α) (n2a : a2 ≠ α) (n2A : a2 ≠ A)
    (n3A : a3 ≠ A) (n3B : a3 ≠ B) (n4B : a4 ≠ B) (n4a : a4 ≠ α)
    (r01 : a0 ≠ a1) (r12 : a1 ≠ a2) (r23 : a2 ≠ a3) (r34 : a3 ≠ a4)
    (E3 : a2 = μ ∨ a3 = μ) (E4 : a3 = μ ∨ a4 = μ) :
    (a0 = A ∧ a1 = B ∧ a2 = μ ∧ a3 = α ∧ a4 = μ) ∨
    (a0 = B ∧ a1 = A ∧ a2 = μ ∧ a3 = α ∧ a4 = μ) ∨
    (a0 = B ∧ a1 = A ∧ a2 = B ∧ a3 = μ ∧ a4 = A) := by
  have cov := f4_cover h1 h3 h4 h13 h14 h34
  rcases cov a0 with e0 | e0 | e0 | e0
  · exact absurd e0 n0a
  · exact absurd e0 n0m
  · have e1 : a1 = B := by
      rcases cov a1 with e | e | e | e
      · exact absurd e n1a
      · exact absurd e n1m
      · exact absurd (e0.trans e.symm) r01
      · exact e
    have e2 : a2 = μ := by
      rcases cov a2 with e | e | e | e
      · exact absurd e n2a
      · exact e
      · exact absurd e n2A
      · exact absurd (e1.trans e.symm) r12
    have e3 : a3 = α := by
      rcases cov a3 with e | e | e | e
      · exact e
      · exact absurd (e2.trans e.symm) r23
      · exact absurd e n3A
      · exact absurd e n3B
    have e4 : a4 = μ := by
      rcases E4 with e | e
      · exact absurd (e3.symm.trans e) h1.symm
      · exact e
    exact Or.inl ⟨e0, e1, e2, e3, e4⟩
  · have e1 : a1 = A := by
      rcases cov a1 with e | e | e | e
      · exact absurd e n1a
      · exact absurd e n1m
      · exact e
      · exact absurd (e0.trans e.symm) r01
    rcases cov a2 with e2 | e2 | e2 | e2
    · exact absurd e2 n2a
    · have e3 : a3 = α := by
        rcases cov a3 with e | e | e | e
        · exact e
        · exact absurd (e2.trans e.symm) r23
        · exact absurd e n3A
        · exact absurd e n3B
      have e4 : a4 = μ := by
        rcases E4 with e | e
        · exact absurd (e3.symm.trans e) h1.symm
        · exact e
      exact Or.inr (Or.inl ⟨e0, e1, e2, e3, e4⟩)
    · exact absurd e2 n2A
    · have e3 : a3 = μ := by
        rcases E3 with e | e
        · exact absurd (e2.symm.trans e) h14.symm
        · exact e
      have e4 : a4 = A := by
        rcases cov a4 with e | e | e | e
        · exact absurd e n4a
        · exact absurd (e3.trans e.symm) r34
        · exact e
        · exact absurd e n4B
      exact Or.inr (Or.inr ⟨e0, e1, e2, e3, e4⟩)

private lemma fne13 (j : Fin 5) : j + 1 ≠ j + 3 := by revert j; decide
private lemma fne14 (j : Fin 5) : j + 1 ≠ j + 4 := by revert j; decide
private lemma fne42 (j : Fin 5) : j + 4 ≠ j + 2 := by revert j; decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- The icosahedral 2-ball around the hole, in `Pent` coordinates (the data of
`VacancyIcosahedral.IcoBall`): `x t` has exactly the neighbours `h, x (t-1), x (t+1),
w (t-1), w t`; the outer vertices `w t` form a cycle and avoid `N[h]`. -/
structure IcoBallP (P : Pent M.graph h) (w : Fin 5 → Fin n) : Prop where
  nbr : ∀ t u, M.graph.Adj (P.x t) u ↔
    u = h ∨ u = P.x (t + 4) ∨ u = P.x (t + 1) ∨ u = w (t + 4) ∨ u = w t
  ring : ∀ t, M.graph.Adj (w t) (w (t + 1))
  off : ∀ t i, w t ≠ P.x i
  offh : ∀ t, w t ≠ h

variable {P : Pent M.graph h} {w : Fin 5 → Fin n}

/-! ### Neighbour lists relative to the repeat index -/

lemma IcoBallP.nbr1 (B : IcoBallP P w) (j : Fin 5) (u : Fin n) :
    M.graph.Adj (P.x (j + 1)) u ↔
      u = h ∨ u = P.x j ∨ u = P.x (j + 2) ∨ u = w j ∨ u = w (j + 1) := by
  have e := B.nbr (j + 1) u
  simp only [add_assoc, Fin.reduceAdd, add_zero] at e
  exact e

lemma IcoBallP.nbr2 (B : IcoBallP P w) (j : Fin 5) (u : Fin n) :
    M.graph.Adj (P.x (j + 2)) u ↔
      u = h ∨ u = P.x (j + 1) ∨ u = P.x (j + 3) ∨ u = w (j + 1) ∨ u = w (j + 2) := by
  have e := B.nbr (j + 2) u
  simp only [add_assoc, Fin.reduceAdd] at e
  exact e

lemma IcoBallP.nbr3 (B : IcoBallP P w) (j : Fin 5) (u : Fin n) :
    M.graph.Adj (P.x (j + 3)) u ↔
      u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3) := by
  have e := B.nbr (j + 3) u
  simp only [add_assoc, Fin.reduceAdd] at e
  exact e

lemma IcoBallP.nbr4 (B : IcoBallP P w) (j : Fin 5) (u : Fin n) :
    M.graph.Adj (P.x (j + 4)) u ↔
      u = h ∨ u = P.x (j + 3) ∨ u = P.x j ∨ u = w (j + 3) ∨ u = w (j + 4) := by
  have e := B.nbr (j + 4) u
  simp only [add_assoc, Fin.reduceAdd, add_zero] at e
  exact e

/-- The ten link–ring adjacencies, relative to `j`. -/
lemma IcoBallP.adjs (B : IcoBallP P w) (j : Fin 5) :
    M.graph.Adj (P.x j) (w j) ∧ M.graph.Adj (P.x (j + 1)) (w j) ∧
    M.graph.Adj (P.x (j + 1)) (w (j + 1)) ∧ M.graph.Adj (P.x (j + 2)) (w (j + 1)) ∧
    M.graph.Adj (P.x (j + 2)) (w (j + 2)) ∧ M.graph.Adj (P.x (j + 3)) (w (j + 2)) ∧
    M.graph.Adj (P.x (j + 3)) (w (j + 3)) ∧ M.graph.Adj (P.x (j + 4)) (w (j + 3)) ∧
    M.graph.Adj (P.x (j + 4)) (w (j + 4)) ∧ M.graph.Adj (P.x j) (w (j + 4)) := by
  refine ⟨(B.nbr j _).2 ?_, (B.nbr1 j _).2 ?_, (B.nbr1 j _).2 ?_, (B.nbr2 j _).2 ?_,
    (B.nbr2 j _).2 ?_, (B.nbr3 j _).2 ?_, (B.nbr3 j _).2 ?_, (B.nbr4 j _).2 ?_,
    (B.nbr4 j _).2 ?_, (B.nbr j _).2 ?_⟩ <;> simp

lemma IcoBallP.rings (B : IcoBallP P w) (j : Fin 5) :
    M.graph.Adj (w j) (w (j + 1)) ∧ M.graph.Adj (w (j + 1)) (w (j + 2)) ∧
    M.graph.Adj (w (j + 2)) (w (j + 3)) ∧ M.graph.Adj (w (j + 3)) (w (j + 4)) := by
  have e1 := B.ring (j + 1)
  have e2 := B.ring (j + 2)
  have e3 := B.ring (j + 3)
  simp only [add_assoc, Fin.reduceAdd] at e1 e2 e3
  exact ⟨B.ring j, e1, e2, e3⟩

/-- The last step of a two-colour path into `t` comes from a neighbour of the other colour. -/
lemma lock_end {d : Fin n → Fin 4} (hd : ProperOff M.graph h d) {a b : Fin 4} {s t : Fin n}
    (r : (pairGraph M.graph h d a b).Reachable s t) (hst : s ≠ t) (ht : d t = b) :
    ∃ u, M.graph.Adj t u ∧ u ≠ h ∧ d u = a := by
  obtain ⟨p⟩ := r.symm
  cases p with
  | nil => exact (hst rfl).elim
  | cons e _ =>
    refine ⟨_, e.1, e.2.2.1, ?_⟩
    rcases e.2.2.2 with hu | hu
    · exact hu
    · exact absurd (ht.trans hu.symm) (hd e.1 e.2.1.1 e.2.2.1)

/-! ### States and the potential -/

variable (P) in
/-- Doubly locked (at its repeat index). -/
def DLState (c : Fin n → Fin 4) : Prop := ∃ j, DoublyLocked P c j

variable (P) in
/-- Unfilled with neither lock (`N₀`). -/
def NoLock (c : Fin n → Fin 4) : Prop := ∃ j, RepeatAt P c j ∧ ¬ Lock1 P c j ∧ ¬ Lock2 P c j

variable (P) in
/-- A `DD` step: `c` and `π c` are both doubly locked. -/
def DDStep (c : Fin n → Fin 4) : Prop := DLState P c ∧ DLState P (piMove P c)

variable (P) in
open Classical in
/-- The telescoping potential of Lemma 1. -/
noncomputable def gpot (c : Fin n → Fin 4) : ℤ :=
  if ∃ j, RepeatAt P c j ∧ Lock1 P c j ∧ ¬ Lock2 P c j then 1
  else if ∃ j, RepeatAt P c j ∧ ¬ Lock1 P c j then -1 else 0

variable {c : Fin n → Fin 4} {j : Fin 5}

lemma ex_rep (hr : RepeatAt P c j) (X : Fin 5 → Prop) :
    (∃ j', RepeatAt P c j' ∧ X j') ↔ X j :=
  ⟨fun ⟨_, hr', hx⟩ => rep_unique hr hr' ▸ hx, fun hx => ⟨j, hr, hx⟩⟩

lemma dl_rep (hr : RepeatAt P c j) : DLState P c ↔ Lock1 P c j ∧ Lock2 P c j :=
  ex_rep hr (fun j => Lock1 P c j ∧ Lock2 P c j)

lemma noLock_rep (hr : RepeatAt P c j) : NoLock P c ↔ ¬ Lock1 P c j ∧ ¬ Lock2 P c j :=
  ex_rep hr (fun j => ¬ Lock1 P c j ∧ ¬ Lock2 P c j)

lemma dl_filled (ht : Target M.graph h c) : ¬ DLState P c :=
  fun ⟨_, hr, _⟩ => rep_not_target hr ht

lemma noLock_filled (ht : Target M.graph h c) : ¬ NoLock P c :=
  fun ⟨_, hr, _⟩ => rep_not_target hr ht

lemma gpot_filled (ht : Target M.graph h c) : gpot P c = 0 := by
  unfold gpot
  rw [ite_eq_right (fun ⟨_, hr, _⟩ => rep_not_target hr ht),
    ite_eq_right (fun ⟨_, hr, _⟩ => rep_not_target hr ht)]

lemma gpot_10 (hr : RepeatAt P c j) (h1 : Lock1 P c j) (h2 : ¬ Lock2 P c j) : gpot P c = 1 := by
  unfold gpot; rw [ite_eq_left ⟨j, hr, h1, h2⟩]

lemma gpot_11 (hr : RepeatAt P c j) (h1 : Lock1 P c j) (h2 : Lock2 P c j) : gpot P c = 0 := by
  unfold gpot
  rw [ite_eq_right (fun hx => ((ex_rep hr (fun j => Lock1 P c j ∧ ¬ Lock2 P c j)).1 hx).2 h2),
    ite_eq_right (fun hx => ((ex_rep hr (fun j => ¬ Lock1 P c j)).1 hx) h1)]

lemma gpot_0 (hr : RepeatAt P c j) (h1 : ¬ Lock1 P c j) : gpot P c = -1 := by
  unfold gpot
  rw [ite_eq_right (fun hx => h1 ((ex_rep hr (fun j => Lock1 P c j ∧ ¬ Lock2 P c j)).1 hx).1),
    ite_eq_left ⟨j, hr, h1⟩]

/-! ### Lemma 1 -/

open Classical in
/-- **Lemma 1, pointwise.** `λ c ≤ [DD c] − 2 [N₀ c] + g (π c) − g c` on every proper-off state
(any spherical map, no ball hypothesis). -/
theorem lam_le_pot (hc : ProperOff M.graph h c) :
    lam P c ≤ (if DDStep P c then 1 else 0) - 2 * (if NoLock P c then 1 else 0)
      + gpot P (piMove P c) - gpot P c := by
  rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · rw [lam_rep hr]
    by_cases hl : Lock2 P c j
    · obtain ⟨-, -, r', l', -⟩ := rot3_move hc hr hl
      have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hr, ite_eq_left hl]
      have hN : ¬ NoLock P c := fun hx => ((noLock_rep hr).1 hx).2 hl
      rw [ite_eq_left hl, ite_eq_right hN]
      unfold DDStep
      rw [hπ]
      by_cases h1 : Lock1 P c j
      · by_cases h2 : Lock2 P (rot3 P c j) (j + 3)
        · rw [ite_eq_left ⟨(dl_rep hr).2 ⟨h1, hl⟩, (dl_rep r').2 ⟨l', h2⟩⟩, gpot_11 r' l' h2,
            gpot_11 hr h1 hl]; norm_num
        · rw [ite_eq_right (fun hx => h2 ((dl_rep r').1 hx.2).2), gpot_10 r' l' h2,
            gpot_11 hr h1 hl]; norm_num
      · rw [ite_eq_right (fun hx => h1 ((dl_rep hr).1 hx.1).1), gpot_0 hr h1]
        by_cases h2 : Lock2 P (rot3 P c j) (j + 3)
        · rw [gpot_11 r' l' h2]; norm_num
        · rw [gpot_10 r' l' h2]; norm_num
    · obtain ⟨-, p', s', -, -⟩ := phiBinv_spec hc hr hl
      have hπ : piMove P c = phiBinv P c j := by rw [piMove_rep hr, ite_eq_right hl]
      rw [ite_eq_right hl]
      unfold DDStep
      rw [hπ, ite_eq_right (fun hx => hl ((dl_rep hr).1 hx.1).2), gpot_filled s'.1]
      by_cases h1 : Lock1 P c j
      · rw [ite_eq_right (fun hx => ((noLock_rep hr).1 hx).1 h1), gpot_10 hr h1 hl]; norm_num
      · rw [ite_eq_left ((noLock_rep hr).2 ⟨h1, hl⟩), gpot_0 hr h1]; norm_num
  · rw [lam_single hc hs, ite_eq_right (show ¬ DDStep P c from fun hx => dl_filled hs.1 hx.1),
      ite_eq_right (show ¬ NoLock P c from noLock_filled hs.1),
      gpot_filled hs.1, piMove_single hc hs]
    by_cases hm : M3Short P c i
    · obtain ⟨-, -, r', l', -⟩ := phiA_spec hc hs hm
      rw [ite_eq_left hm, ite_eq_left hm, gpot_0 r' l']; norm_num
    · obtain ⟨-, -, s', -, -⟩ := tau_spec hc hs hm
      rw [ite_eq_right hm, ite_eq_right hm, gpot_filled s'.1]; norm_num

variable {S : Finset (Fin n → Fin 4)}

open Classical in
/-- **Lemma 1.** On a finite `π`-invariant set of proper-off states,
`Σ λ ≤ |DD| − 2 N₀`. -/
theorem sum_lam_le (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S) :
    ∑ c ∈ S, lam P c ≤ ((S.filter (DDStep P)).card : ℤ) - 2 * (S.filter (NoLock P)).card := by
  calc ∑ c ∈ S, lam P c
      ≤ ∑ c ∈ S, ((if DDStep P c then 1 else 0) - 2 * (if NoLock P c then 1 else 0)
          + gpot P (piMove P c) - gpot P c) :=
        Finset.sum_le_sum fun c hc => lam_le_pot (hS c hc)
    _ = _ := by
      rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.sum_sub_distrib,
        sum_comp_piMove hb (gpot P), ← Finset.mul_sum, Finset.sum_boole, Finset.sum_boole]
      ring

/-! ### Local types and Lemma 2 -/

variable (P w) in
/-- Type `R3` at `j`: doubly locked, with outer ring `(B, A, B, μ, A)` from `w j`. -/
def R3At (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  DoublyLocked P c j ∧ c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
    c (w (j + 2)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x (j + 1)) ∧
    c (w (j + 4)) = c (P.x (j + 3))

/-- **Theorem H, Step 1.** At a doubly locked state the outer ring is `R1 = (A,B,μ,α,μ)`,
`R2 = (B,A,μ,α,μ)` or `R3 = (B,A,B,μ,A)`. -/
theorem ring_type (B : IcoBallP P w) (hc : ProperOff M.graph h c) (hd : DoublyLocked P c j) :
    (c (w j) = c (P.x (j + 3)) ∧ c (w (j + 1)) = c (P.x (j + 4)) ∧
      c (w (j + 2)) = c (P.x (j + 1)) ∧ c (w (j + 3)) = c (P.x j) ∧
      c (w (j + 4)) = c (P.x (j + 1))) ∨
    (c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
      c (w (j + 2)) = c (P.x (j + 1)) ∧ c (w (j + 3)) = c (P.x j) ∧
      c (w (j + 4)) = c (P.x (j + 1))) ∨
    (c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
      c (w (j + 2)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x (j + 1)) ∧
      c (w (j + 4)) = c (P.x (j + 3))) := by
  obtain ⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, l1, l2⟩ := hd
  have pw : ∀ i t, M.graph.Adj (P.x i) (w t) → c (w t) ≠ c (P.x i) :=
    fun i t e => (hc e (P.x_ne_h i) (B.offh t)).symm
  obtain ⟨a0, a1, a2, a3, a4, a5, a6, a7, a8, a9⟩ := B.adjs j
  obtain ⟨g0, g1, g2, g3⟩ := B.rings j
  have rw' : ∀ {s t}, M.graph.Adj (w s) (w t) → c (w s) ≠ c (w t) :=
    fun e => hc e (B.offh _) (B.offh _)
  have E3 : c (w (j + 2)) = c (P.x (j + 1)) ∨ c (w (j + 3)) = c (P.x (j + 1)) := by
    obtain ⟨u, hu, huh, hcu⟩ := lock_end hc l1 (fun e => fne13 j (P.inj e)) rfl
    rcases (B.nbr3 j u).1 hu with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl huh
    · exact absurd (h02.trans hcu) h1.symm
    · exact absurd hcu.symm h14
    · exact Or.inl hcu
    · exact Or.inr hcu
  have E4 : c (w (j + 3)) = c (P.x (j + 1)) ∨ c (w (j + 4)) = c (P.x (j + 1)) := by
    obtain ⟨u, hu, huh, hcu⟩ := lock_end hc l2 (fun e => fne14 j (P.inj e)) rfl
    rcases (B.nbr4 j u).1 hu with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl huh
    · exact absurd hcu.symm h13
    · exact absurd hcu.symm h1
    · exact Or.inl hcu
    · exact Or.inr hcu
  exact ring_types h1 h3 h4 h13 h14 h34 (pw _ _ a0) (pw _ _ a1) (pw _ _ a2)
    (by rw [h02]; exact pw _ _ a3) (by rw [h02]; exact pw _ _ a4) (pw _ _ a5) (pw _ _ a6)
    (pw _ _ a7) (pw _ _ a8) (pw _ _ a9) (rw' g0) (rw' g1) (rw' g2) (rw' g3) E3 E4

/-- **Lemma 2** (Theorem H, Steps 2 and 4, applied to `π = R₊₃`). If `c` is doubly locked at
`j` and `π c` is doubly locked, then `c` is of type `R3` at `j` or `π c` is of type `R3` at
`j + 3`. (`R2` has no `DD` step; an `R1` `DD` step lands in `R3`.) -/
theorem dd_r3 (B : IcoBallP P w) (hc : ProperOff M.graph h c) (hd : DoublyLocked P c j)
    (hd' : DLState P (piMove P c)) : R3At P w c j ∨ R3At P w (piMove P c) (j + 3) := by
  have hd0 := hd
  obtain ⟨hr, l1, l2⟩ := hd
  obtain ⟨-, hp', r', -, -⟩ := rot3_move hc hr l2
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hr, ite_eq_left l2]
  rw [hπ] at hd' ⊢
  obtain ⟨l1', l2'⟩ := (dl_rep r').1 hd'
  have hK := rot3Def_of_lock2 P hr l2
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values hr hK
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨a0, a1, a2, a3, a4, a5, a6, a7, a8, a9⟩ := B.adjs j
  have hW := whole_component M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))
    ⟨P.x_ne_h _, Or.inl h02.symm⟩
  have x2K : P.x (j + 2) ∈ {v | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
      (P.x (j + 2)) v} := Reachable.refl _
  have x3K : P.x (j + 3) ∈ {v | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
      (P.x (j + 2)) v} := rot3_reach ⟨h02, h1, h3, h4, h13, h14, h34⟩
  have rin : ∀ v, v ∈ {v | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
      (P.x (j + 2)) v} → rot3 P c j v = Equiv.swap (c (P.x j)) (c (P.x (j + 3))) (c v) :=
    fun v hv => swap_in hv
  have roth : ∀ v, c v ≠ c (P.x j) → c v ≠ c (P.x (j + 3)) → rot3 P c j v = c v :=
    fun v ha hb => swap_other ha hb
  rcases ring_type B hc hd0 with ⟨e0, e1, e2, e3, e4⟩ | ⟨e0, e1, e2, e3, e4⟩ | R3
  · -- R1: the image is R3 at `j + 3`
    right
    have w3K := whole_closed M.graph hW x3K a6 ⟨B.offh _, Or.inl e3⟩
    have w0K : w j ∉ {v | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
        (P.x (j + 2)) v} := fun hin =>
      hK (whole_closed M.graph hW hin a0.symm ⟨P.x_ne_h _, Or.inl rfl⟩)
    have d3 : rot3 P c j (w (j + 3)) = c (P.x (j + 3)) := by
      rw [rin _ w3K, e3, Equiv.swap_apply_left]
    have d0 : rot3 P c j (w j) = c (P.x (j + 3)) := by rw [← e0]; exact swap_out w0K
    have d4 : rot3 P c j (w (j + 4)) = c (P.x (j + 1)) := by
      rw [roth _ (by rw [e4]; exact h1) (by rw [e4]; exact h13), e4]
    have d1 : rot3 P c j (w (j + 1)) = c (P.x (j + 4)) := by
      rw [roth _ (by rw [e1]; exact h4) (by rw [e1]; exact h34.symm), e1]
    have d2 : rot3 P c j (w (j + 2)) = c (P.x (j + 1)) := by
      rw [roth _ (by rw [e2]; exact h1) (by rw [e2]; exact h13), e2]
    unfold R3At
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    exact ⟨⟨r', l1', l2'⟩, by rw [d3, v2], by rw [d4, v1], by rw [d0, v2], by rw [d1, v4],
      by rw [d2, v1]⟩
  · -- R2: lock 2 of the image dies
    exfalso
    have w1K := whole_closed M.graph hW x2K a3 ⟨B.offh _, Or.inr e1⟩
    have L := l2'
    unfold Lock2 at L
    simp only [add_assoc, Fin.reduceAdd] at L
    obtain ⟨u, hu, huh, hcu⟩ := lock_end hp' L (fun e => fne42 j (P.inj e)) rfl
    rw [v4] at hcu
    rcases (B.nbr2 j u).1 hu with rfl | rfl | rfl | rfl | rfl
    · exact huh rfl
    · rw [v1] at hcu; exact h14 hcu
    · rw [v3] at hcu; exact h4 hcu.symm
    · rw [rin _ w1K, e1, Equiv.swap_apply_right] at hcu; exact h4 hcu.symm
    · rw [roth _ (by rw [e2]; exact h1) (by rw [e2]; exact h13), e2] at hcu; exact h14 hcu
  · exact Or.inl ⟨hd0, R3⟩

/-! ### Lemma 3: the `σ`-exit -/

variable (P) in
/-- `σ` at `j`: swap the `{α, μ}`-component of `m = x (j+1)`. -/
noncomputable def sigSwap (c : Fin n → Fin 4) (j : Fin 5) : Fin n → Fin 4 :=
  kswap M.graph h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 1))

/-- **Lemma 3.** At an `R3` state, `σ` is a Kempe step to an unfilled state with repeat index
`j` and neither lock; it exchanges the colours of `x j` and `x (j+1)`. The swapped component
is `{x j, x (j+1), x (j+2)}` (it misses `w (j+3)`). -/
theorem sigSwap_spec (B : IcoBallP P w) (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    KempeStep M.graph h c (sigSwap P c j) ∧ ProperOff M.graph h (sigSwap P c j) ∧
      RepeatAt P (sigSwap P c j) j ∧ ¬ Lock1 P (sigSwap P c j) j ∧
      ¬ Lock2 P (sigSwap P c j) j ∧
      sigSwap P c j (P.x j) = c (P.x (j + 1)) ∧ sigSwap P c j (P.x (j + 1)) = c (P.x j) := by
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -, -⟩, e0, e1, e2, e3, e4⟩ := hR
  have step : KempeStep M.graph h c (sigSwap P c j) :=
    kswap_step h1.symm (P.x_ne_h _) (Or.inr rfl)
  have hp := kempe_proper M.graph hc step
  have hAB : ∀ {v}, c v = c (P.x (j + 3)) ∨ c v = c (P.x (j + 4)) →
      ¬ (c v = c (P.x j) ∨ c v = c (P.x (j + 1))) := by
    rintro v (e | e) (f | f)
    · exact h3 (e.symm.trans f)
    · exact h13 (f.symm.trans e)
    · exact h4 (e.symm.trans f)
    · exact h14 (f.symm.trans e)
  have closed : ∀ u v, (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Adj u v →
      (u = P.x j ∨ u = P.x (j + 1) ∨ u = P.x (j + 2)) →
      (v = P.x j ∨ v = P.x (j + 1) ∨ v = P.x (j + 2)) := by
    intro u v e hu
    have hv := e.2.2
    rcases hu with rfl | rfl | rfl
    · rcases (B.nbr j v).1 e.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl hv.1
      · exact absurd hv.2 (hAB (Or.inr rfl))
      · exact Or.inr (Or.inl rfl)
      · exact absurd hv.2 (hAB (Or.inl e4))
      · exact absurd hv.2 (hAB (Or.inr e0))
    · rcases (B.nbr1 j v).1 e.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl hv.1
      · exact Or.inl rfl
      · exact Or.inr (Or.inr rfl)
      · exact absurd hv.2 (hAB (Or.inr e0))
      · exact absurd hv.2 (hAB (Or.inl e1))
    · rcases (B.nbr2 j v).1 e.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl hv.1
      · exact Or.inr (Or.inl rfl)
      · exact absurd hv.2 (hAB (Or.inl rfl))
      · exact absurd hv.2 (hAB (Or.inl e1))
      · exact absurd hv.2 (hAB (Or.inr e2))
  have w3out : ¬ (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable
      (P.x (j + 1)) (w (j + 3)) := by
    intro r
    rcases reachable_invariant closed (Or.inr (Or.inl rfl)) r with e | e | e <;>
      exact B.off _ _ e
  have adj12 := P.adj_cyc (j + 1)
  simp only [add_assoc, Fin.reduceAdd] at adj12
  have rj : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable
      (P.x (j + 1)) (P.x j) :=
    Adj.reachable ⟨(P.adj_cyc j).symm, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨P.x_ne_h _, Or.inl rfl⟩⟩
  have rj2 : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable
      (P.x (j + 1)) (P.x (j + 2)) :=
    Adj.reachable ⟨adj12, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨P.x_ne_h _, Or.inl h02.symm⟩⟩
  have s0 : sigSwap P c j (P.x j) = c (P.x (j + 1)) := kswap_mem rj rfl
  have s1 : sigSwap P c j (P.x (j + 1)) = c (P.x j) := kswap_mem' (Reachable.refl _) rfl
  have s2 : sigSwap P c j (P.x (j + 2)) = c (P.x (j + 1)) := kswap_mem rj2 h02.symm
  have s3 : sigSwap P c j (P.x (j + 3)) = c (P.x (j + 3)) := kswap_other h3 h13.symm
  have s4 : sigSwap P c j (P.x (j + 4)) = c (P.x (j + 4)) := kswap_other h4 h14.symm
  have sw2 : sigSwap P c j (w (j + 2)) = c (P.x (j + 4)) := by
    rw [← e2]; exact kswap_other (by rw [e2]; exact h4) (by rw [e2]; exact h14.symm)
  have sw3 : sigSwap P c j (w (j + 3)) = c (P.x (j + 1)) := by
    rw [← e3]; exact kswap_out w3out
  have sw4 : sigSwap P c j (w (j + 4)) = c (P.x (j + 3)) := by
    rw [← e4]; exact kswap_other (by rw [e4]; exact h3) (by rw [e4]; exact h13.symm)
  obtain ⟨b0, -, -, -, -, b5, b6, b7, b8, -⟩ := B.adjs j
  refine ⟨step, hp, rep_of_vals s0 s1 s2 s3 s4 h1.symm h13.symm h14.symm h3.symm h4.symm h34,
    ?_, ?_, s0, s1⟩
  · intro L
    unfold Lock1 at L
    rw [s1, s3] at L
    obtain ⟨u, hu, huh, hcu⟩ := lock_end hp L (fun e => fne13 j (P.inj e)) s3
    rcases (B.nbr3 j u).1 hu with rfl | rfl | rfl | rfl | rfl
    · exact huh rfl
    · rw [s2] at hcu; exact h1 hcu
    · rw [s4] at hcu; exact h4 hcu
    · rw [sw2] at hcu; exact h4 hcu
    · rw [sw3] at hcu; exact h1 hcu
  · intro L
    unfold Lock2 at L
    rw [s1, s4] at L
    obtain ⟨u, hu, huh, hcu⟩ := lock_end hp L (fun e => fne14 j (P.inj e)) s4
    rcases (B.nbr4 j u).1 hu with rfl | rfl | rfl | rfl | rfl
    · exact huh rfl
    · rw [s3] at hcu; exact h3 hcu
    · rw [s0] at hcu; exact h1 hcu
    · rw [sw3] at hcu; exact h1 hcu
    · rw [sw4] at hcu; exact h3 hcu

/-- `σ` is undone by swapping the same component of the image. -/
theorem sigSwap_inv (B : IcoBallP P w) (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    c = kswap M.graph h (sigSwap P c j) (sigSwap P c j (P.x (j + 1))) (sigSwap P c j (P.x j))
      (P.x (j + 1)) := by
  obtain ⟨-, -, -, -, -, s0, s1⟩ := sigSwap_spec B hc hR
  rw [s1, s0]
  exact (kswap_inv (G := M.graph) (h := h) (c := c) (a := c (P.x j)) (b := c (P.x (j + 1)))
    (s := P.x (j + 1))).symm

/-- **Lemma 3, injectivity.** `σ` is injective on `R3` states (over all repeat indices). -/
theorem sigSwap_inj (B : IcoBallP P w) {c' : Fin n → Fin 4} {j' : Fin 5}
    (hc : ProperOff M.graph h c) (hR : R3At P w c j)
    (hc' : ProperOff M.graph h c') (hR' : R3At P w c' j')
    (E : sigSwap P c j = sigSwap P c' j') : c = c' := by
  obtain ⟨-, -, r, -⟩ := sigSwap_spec B hc hR
  obtain ⟨-, -, r', -⟩ := sigSwap_spec B hc' hR'
  rw [← E] at r'
  obtain rfl := rep_unique r r'
  rw [sigSwap_inv B hc hR, sigSwap_inv B hc' hR', E]

/-! ### Counting and Theorem F5 -/

open Classical in
private lemma mem_kclass {c₀ d : Fin n → Fin 4} :
    d ∈ kclass M h c₀ ↔ ProperOff M.graph h d ∧ KempeEquiv (G := M.graph) (h := h) c₀ d := by
  unfold kclass; simp

open Classical in
/-- `|DD| ≤ 2 N₀` in every Kempe class at an icosahedral hole. -/
theorem dd_le_two_noLock (B : IcoBallP P w) (c₀ : Fin n → Fin 4) :
    ((kclass M h c₀).filter (DDStep P)).card ≤ 2 * ((kclass M h c₀).filter (NoLock P)).card := by
  set S := kclass M h c₀ with hSdef
  let R := S.filter (fun c => ∃ j, R3At P w c j)
  have hb := kclass_bijOn (P := P) c₀
  -- each DD step to its R3 endpoint: at most two DD steps per R3 state
  have h1 : (S.filter (DDStep P)).card ≤ 2 * R.card := by
    let f : (Fin n → Fin 4) → (Fin n → Fin 4) :=
      fun c => if ∃ j, R3At P w c j then c else piMove P c
    refine Finset.card_le_mul_card_image_of_maps_to (f := f) ?_ 2 ?_
    · intro c hc
      obtain ⟨hcS, ⟨j, hd⟩, hd'⟩ := Finset.mem_filter.1 hc
      have hp := (mem_kclass.1 hcS).1
      by_cases hx : ∃ j, R3At P w c j
      · simp only [f, ite_eq_left hx]
        exact Finset.mem_filter.2 ⟨hcS, hx⟩
      · simp only [f, ite_eq_right hx]
        refine Finset.mem_filter.2 ⟨hb.mapsTo hcS, ?_⟩
        rcases dd_r3 B hp hd hd' with h' | h'
        · exact absurd ⟨j, h'⟩ hx
        · exact ⟨_, h'⟩
    · intro r _
      refine (Finset.card_le_card ?_).trans (Finset.card_le_two (a := r) (b := piInv P r))
      intro c hc
      obtain ⟨hcD, hfc⟩ := Finset.mem_filter.1 hc
      have hp := (mem_kclass.1 (Finset.mem_filter.1 hcD).1).1
      by_cases hx : ∃ j, R3At P w c j
      · simp only [f, ite_eq_left hx] at hfc
        simp [hfc]
      · simp only [f, ite_eq_right hx] at hfc
        have : c = piInv P r := by rw [← hfc, piInv_piMove hp]
        simp [this]
  -- σ is an injection from R3 states into lockless states
  have h2 : R.card ≤ (S.filter (NoLock P)).card := by
    let g : (Fin n → Fin 4) → (Fin n → Fin 4) :=
      fun c => if hx : ∃ j, R3At P w c j then sigSwap P c hx.choose else c
    have gval : ∀ c (hx : ∃ j, R3At P w c j), g c = sigSwap P c hx.choose :=
      fun c hx => dite_eq_left hx
    refine Finset.card_le_card_of_injOn g ?_ ?_
    · intro c hc
      obtain ⟨hcS, hx⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hc)
      obtain ⟨hp, he⟩ := mem_kclass.1 hcS
      obtain ⟨st, hp', r', n1, n2, -⟩ := sigSwap_spec B hp hx.choose_spec
      rw [Finset.mem_coe, gval c hx]
      exact Finset.mem_filter.2 ⟨mem_kclass.2 ⟨hp', Relation.ReflTransGen.tail he st⟩,
        ⟨_, r', n1, n2⟩⟩
    · intro c hc c' hc' E
      obtain ⟨hcS, hx⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hc)
      obtain ⟨hcS', hx'⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hc')
      rw [gval c hx, gval c' hx'] at E
      exact sigSwap_inj B (mem_kclass.1 hcS).1 hx.choose_spec (mem_kclass.1 hcS').1
        hx'.choose_spec E
  omega

/-- **Theorem F5.** At an icosahedral hole every Kempe class has `Σ λ ≤ 0`. -/
theorem sum_lam_class_nonpos (B : IcoBallP P w) (c₀ : Fin n → Fin 4) :
    ∑ c ∈ kclass M h c₀, lam P c ≤ 0 := by
  classical
  have h1 := sum_lam_le (P := P) (kclass_properOff c₀) (kclass_bijOn c₀)
  have h2 := dd_le_two_noLock B c₀
  have h2' : (((kclass M h c₀).filter (DDStep P)).card : ℤ) ≤
      2 * ((kclass M h c₀).filter (NoLock P)).card := by exact_mod_cast h2
  omega

open Classical in
/-- **Theorem F5, counting form.** `3F − U ≥ 0` in every Kempe class. -/
theorem three_F_sub_U_class_nonneg (B : IcoBallP P w) (c₀ : Fin n → Fin 4) :
    0 ≤ 3 * (((kclass M h c₀).filter (Target M.graph h)).card : ℤ) -
      ((kclass M h c₀).filter (fun c => ¬ Target M.graph h c)).card := by
  rw [three_F_sub_U_class (P := P) c₀]
  have := sum_lam_class_nonpos B c₀
  omega

/-- **Theorem F5, quarter-floor form.** At an icosahedral hole every Kempe class is at least a
quarter filled. -/
theorem quarterFloor_of_icoBall (B : IcoBallP P w) : QuarterFloorConj (G := M.graph) (h := h) :=
  (quarterFloor_iff_lam P).2 fun c₀ _ => sum_lam_class_nonpos B c₀

end sphere

end SimpleGraph.QuarterFloor
