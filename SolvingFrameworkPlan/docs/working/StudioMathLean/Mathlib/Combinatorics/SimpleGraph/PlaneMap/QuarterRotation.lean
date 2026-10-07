/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFloor

/-!
# The rotations `R₊₃` and `R₊₂` on unfilled states of a pentagonal hole

Conventions as in `QuarterFloor`: at repeat index `j`, `α = c (x j) = c (x (j+2))`,
`μ = c (x (j+1))`, `A = c (x (j+3))`, `B = c (x (j+4))`.

* `rot3 P c j` (`R₊₃`): swap the `{α, A}`-component `K` of `x (j+2)`. Since `x (j+3)` (colour `A`)
  is adjacent to `x (j+2)`, it always lies in `K`. When `x j ∉ K` (`Rot3Def`), the new link is
  `(α, μ, A, α, B)`, an unfilled state with repeat index `j + 3`.
* `rot2 P c j` (`R₊₂`): swap the `{α, B}`-component of `x j`. When `x (j+2)` is not in it
  (`Rot2Def`), the new link is `(B, μ, α, A, α)`, with repeat index `j + 2`.

Main results (all graph-theoretic, no planarity):
* `rot3_spec`: `R₊₃` is a Kempe step to a proper state with repeat index `j+3`, and
  `Lock1` of the image at `j+3` is equivalent to `Lock2` at `j` (same `{μ, B}` graph).
* `rot2_spec`: the mirror statement for `R₊₂`.
* `rot2_rot3`, `rot3_rot2`: the two rotations are mutually inverse.
* `rot3_bijOn`: `R₊₃` is a bijection from
  `{proper, repeat at j, lock 2 at j, x j ∉ K}` onto
  `{proper, repeat at j+3, lock 1 at j+3, R₊₂ defined at j+3}` with inverse `R₊₂`.

Planarity enters only through the definedness hypotheses: the hand dichotomy L2
("`R₊₃` is defined iff lock 2 holds", `MathQuarterFloorBijections.md` §1) uses the Jordan curve
theorem and is **not** proved here; `Rot3Def` (resp. `Rot2Def`) is carried as a hypothesis
alongside `Lock2` (resp. `Lock1`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill

variable {V : Type*} {G : SimpleGraph V} {h : V}

/-! ### General facts about swaps -/

section general
variable {C : Type*} [DecidableEq C]

lemma active_swap_same (c : V → C) (a b : C) (S : Set V) (v : V) :
    Active h (swap c a b S) a b v ↔ Active h c a b v := by
  classical
  unfold Active
  by_cases hv : v ∈ S
  · rw [swap_in hv]
    constructor
    · rintro ⟨h1, h2⟩
      refine ⟨h1, ?_⟩
      rcases h2 with h2 | h2
      · right; rw [Equiv.swap_apply_eq_iff, Equiv.swap_apply_left] at h2; exact h2
      · left; rw [Equiv.swap_apply_eq_iff, Equiv.swap_apply_right] at h2; exact h2
    · rintro ⟨h1, h2⟩
      refine ⟨h1, ?_⟩
      rcases h2 with h2 | h2
      · right; rw [h2, Equiv.swap_apply_left]
      · left; rw [h2, Equiv.swap_apply_right]
  · rw [swap_out hv]

/-- An `{a, b}`-swap leaves the `{a, b}` two-colour graph unchanged. -/
lemma pairGraph_swap_same (c : V → C) (a b : C) (S : Set V) :
    pairGraph G h (swap c a b S) a b = pairGraph G h c a b := by
  ext u v
  simp only [pairGraph, active_swap_same]

/-- An `{a, b}`-swap leaves an `{x, y}` two-colour graph unchanged when `{x, y}` avoids `a, b`. -/
lemma pairGraph_swap_other (c : V → C) (a b : C) (S : Set V) {x y : C}
    (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairGraph G h (swap c a b S) x y = pairGraph G h c x y := by
  ext u v
  simp only [pairGraph, Active, swap_preserves_eq hxa hxb, swap_preserves_eq hya hyb]

omit [DecidableEq C] in
lemma pairGraph_comm_gen (c : V → C) (a b : C) :
    pairGraph G h c a b = pairGraph G h c b a := by
  ext u v
  simp only [pairGraph, Active, or_comm]

/-- Swapping the same set twice is the identity. -/
lemma swap_swap (c : V → C) (a b : C) (S : Set V) : swap (swap c a b S) a b S = c := by
  classical
  funext v
  by_cases hv : v ∈ S
  · rw [swap_in hv, swap_in hv, Equiv.swap_apply_self]
  · rw [swap_out hv, swap_out hv]

end general

/-! ### Index arithmetic in `Fin 5` -/

private lemma f21 (j : Fin 5) : j + 2 + 1 = j + 3 := by revert j; decide
private lemma f22 (j : Fin 5) : j + 2 + 2 = j + 4 := by revert j; decide
private lemma f23 (j : Fin 5) : j + 2 + 3 = j := by revert j; decide
private lemma f24 (j : Fin 5) : j + 2 + 4 = j + 1 := by revert j; decide
private lemma f31 (j : Fin 5) : j + 3 + 1 = j + 4 := by revert j; decide
private lemma f32 (j : Fin 5) : j + 3 + 2 = j := by revert j; decide
private lemma f33 (j : Fin 5) : j + 3 + 3 = j + 1 := by revert j; decide
private lemma f34 (j : Fin 5) : j + 3 + 4 = j + 2 := by revert j; decide
private lemma f41 (j : Fin 5) : j + 4 + 1 = j := by revert j; decide

/-! ### The rotations -/

variable (P : Pent G h)

/-- `R₊₃` at `j`: swap the `{α, A}`-component of `x (j+2)`. -/
noncomputable def rot3 (c : V → Fin 4) (j : Fin 5) : V → Fin 4 :=
  swap c (c (P.x j)) (c (P.x (j + 3)))
    {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) v}

/-- `R₊₂` at `j`: swap the `{α, B}`-component of `x j`. -/
noncomputable def rot2 (c : V → Fin 4) (j : Fin 5) : V → Fin 4 :=
  swap c (c (P.x j)) (c (P.x (j + 4)))
    {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) v}

/-- `R₊₃` is defined at `j`: the `{α, A}`-component of `x (j+2)` misses `x j`.
(By the planar dichotomy L2 this is equivalent to `Lock2`; not formalised.) -/
def Rot3Def (c : V → Fin 4) (j : Fin 5) : Prop :=
  ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x j)

/-- `R₊₂` is defined at `j`: the `{α, B}`-component of `x j` misses `x (j+2)`.
(By the planar dichotomy L1 this is equivalent to `Lock1`; not formalised.) -/
def Rot2Def (c : V → Fin 4) (j : Fin 5) : Prop :=
  ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) (P.x (j + 2))

variable {P}

lemma Pent.x_ne_h (i : Fin 5) : P.x i ≠ h := (P.adj_h i).ne'

section rot3
variable {c : V → Fin 4} {j : Fin 5}

/-- `x (j+3)` always lies in the `{α, A}`-component of `x (j+2)`. -/
lemma rot3_reach (hr : RepeatAt P c j) :
    (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x (j + 3)) := by
  have e := P.adj_cyc (j + 2)
  rw [f21] at e
  exact Adj.reachable ⟨e, ⟨P.x_ne_h _, Or.inl hr.1.symm⟩, ⟨P.x_ne_h _, Or.inr rfl⟩⟩

/-- The link after `R₊₃`: `(α, μ, A, α, B)`. -/
lemma rot3_values (hr : RepeatAt P c j) (hK : Rot3Def P c j) :
    rot3 P c j (P.x j) = c (P.x j) ∧ rot3 P c j (P.x (j + 1)) = c (P.x (j + 1)) ∧
      rot3 P c j (P.x (j + 2)) = c (P.x (j + 3)) ∧ rot3 P c j (P.x (j + 3)) = c (P.x j) ∧
      rot3 P c j (P.x (j + 4)) = c (P.x (j + 4)) := by
  have hreach := rot3_reach hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  refine ⟨swap_out hK, swap_other h1 h13, ?_, ?_, swap_other h4 h34.symm⟩
  · unfold rot3
    rw [swap_in (show P.x (j + 2) ∈ {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) v} from Reachable.refl _), ← h02,
      Equiv.swap_apply_left]
  · unfold rot3
    rw [swap_in (show P.x (j + 3) ∈ {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) v} from hreach), Equiv.swap_apply_right]

/-- `R₊₃` is a Kempe step to a proper unfilled state with repeat index `j + 3`, and lock 1 of
the image at `j + 3` is lock 2 of the original at `j`. -/
theorem rot3_spec (hc : ProperOff G h c) (hr : RepeatAt P c j) (hK : Rot3Def P c j) :
    KempeStep G h c (rot3 P c j) ∧ ProperOff G h (rot3 P c j) ∧
      RepeatAt P (rot3 P c j) (j + 3) ∧ (Lock1 P (rot3 P c j) (j + 3) ↔ Lock2 P c j) := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values hr hK
  have hW := whole_component G h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))
    ⟨P.x_ne_h _, Or.inl hr.1.symm⟩
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  refine ⟨⟨_, _, _, h3.symm, hW, rfl⟩, properOff_swap G hc hW, ?_, ?_⟩
  · unfold RepeatAt
    rw [f32, f31, f33, f34, v0, v1, v2, v3, v4]
    exact ⟨rfl, h4, h1, h3, h14.symm, h34.symm, h13⟩
  · have hpg : pairGraph G h (rot3 P c j) (c (P.x (j + 4))) (c (P.x (j + 1))) =
        pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 4))) :=
      (pairGraph_swap_other _ _ _ _ h4 h34.symm h1 h13).trans (pairGraph_comm_gen _ _ _)
    unfold Lock1 Lock2
    rw [f31, f33, v4, v1, hpg]
    exact ⟨Reachable.symm, Reachable.symm⟩

/-- After `R₊₃`, `R₊₂` is defined at `j + 3`. -/
theorem rot3_rot2Def (hr : RepeatAt P c j) (hK : Rot3Def P c j) :
    Rot2Def P (rot3 P c j) (j + 3) := by
  obtain ⟨-, -, v2, v3, -⟩ := rot3_values hr hK
  have hsame : pairGraph G h (rot3 P c j) (c (P.x j)) (c (P.x (j + 3))) =
      pairGraph G h c (c (P.x j)) (c (P.x (j + 3))) := pairGraph_swap_same _ _ _ _
  have hreach := rot3_reach hr
  unfold Rot2Def
  rw [f34, f32, v3, v2, hsame]
  exact fun r => hK (hreach.trans r)

/-- `R₊₂` undoes `R₊₃`. -/
theorem rot2_rot3 (hr : RepeatAt P c j) (hK : Rot3Def P c j) :
    rot2 P (rot3 P c j) (j + 3) = c := by
  obtain ⟨-, -, v2, v3, -⟩ := rot3_values hr hK
  have hsame : pairGraph G h (rot3 P c j) (c (P.x j)) (c (P.x (j + 3))) =
      pairGraph G h c (c (P.x j)) (c (P.x (j + 3))) := pairGraph_swap_same _ _ _ _
  have hreach := rot3_reach hr
  unfold rot2
  rw [f34, v3, v2, hsame]
  have hset :
      {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 3)) v} =
        {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) v} := by
    ext v
    exact ⟨fun r => hreach.trans r, fun r => hreach.symm.trans r⟩
  rw [hset]
  exact swap_swap _ _ _ _

end rot3

section rot2
variable {c : V → Fin 4} {j : Fin 5}

/-- `x (j+4)` always lies in the `{α, B}`-component of `x j`. -/
lemma rot2_reach (_hr : RepeatAt P c j) :
    (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) (P.x (j + 4)) := by
  have e := P.adj_cyc (j + 4)
  rw [f41] at e
  exact Adj.reachable ⟨e.symm, ⟨P.x_ne_h _, Or.inl rfl⟩, ⟨P.x_ne_h _, Or.inr rfl⟩⟩

/-- The link after `R₊₂`: `(B, μ, α, A, α)`. -/
lemma rot2_values (hr : RepeatAt P c j) (hK : Rot2Def P c j) :
    rot2 P c j (P.x j) = c (P.x (j + 4)) ∧ rot2 P c j (P.x (j + 1)) = c (P.x (j + 1)) ∧
      rot2 P c j (P.x (j + 2)) = c (P.x j) ∧ rot2 P c j (P.x (j + 3)) = c (P.x (j + 3)) ∧
      rot2 P c j (P.x (j + 4)) = c (P.x j) := by
  have hreach := rot2_reach hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  refine ⟨?_, swap_other h1 h14, by rw [h02]; exact swap_out hK, swap_other h3 h34, ?_⟩
  · unfold rot2
    rw [swap_in (show P.x j ∈ {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) v} from Reachable.refl _), Equiv.swap_apply_left]
  · unfold rot2
    rw [swap_in (show P.x (j + 4) ∈ {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) v} from hreach), Equiv.swap_apply_right]

/-- `R₊₂` is a Kempe step to a proper unfilled state with repeat index `j + 2`, and lock 2 of
the image at `j + 2` is lock 1 of the original at `j`. -/
theorem rot2_spec (hc : ProperOff G h c) (hr : RepeatAt P c j) (hK : Rot2Def P c j) :
    KempeStep G h c (rot2 P c j) ∧ ProperOff G h (rot2 P c j) ∧
      RepeatAt P (rot2 P c j) (j + 2) ∧ (Lock2 P (rot2 P c j) (j + 2) ↔ Lock1 P c j) := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot2_values hr hK
  have hW := whole_component G h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)
    ⟨P.x_ne_h _, Or.inl rfl⟩
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  refine ⟨⟨_, _, _, h4.symm, hW, rfl⟩, properOff_swap G hc hW, ?_, ?_⟩
  · unfold RepeatAt
    rw [f22, f21, f23, f24, v0, v1, v2, v3, v4]
    exact ⟨rfl, h3, h4, h1, h34, h13.symm, h14.symm⟩
  · have hpg : pairGraph G h (rot2 P c j) (c (P.x (j + 3))) (c (P.x (j + 1))) =
        pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 3))) :=
      (pairGraph_swap_other _ _ _ _ h3 h34 h1 h14).trans (pairGraph_comm_gen _ _ _)
    unfold Lock1 Lock2
    rw [f21, f24, v3, v1, hpg]
    exact ⟨Reachable.symm, Reachable.symm⟩

/-- After `R₊₂`, `R₊₃` is defined at `j + 2`. -/
theorem rot2_rot3Def (hr : RepeatAt P c j) (hK : Rot2Def P c j) :
    Rot3Def P (rot2 P c j) (j + 2) := by
  obtain ⟨v0, -, v2, -, -⟩ := rot2_values hr hK
  have hsame : pairGraph G h (rot2 P c j) (c (P.x j)) (c (P.x (j + 4))) =
      pairGraph G h c (c (P.x j)) (c (P.x (j + 4))) := pairGraph_swap_same _ _ _ _
  have hreach := rot2_reach hr
  unfold Rot3Def
  rw [f23, f22, v2, v0, hsame]
  exact fun r => hK (hreach.trans r)

/-- `R₊₃` undoes `R₊₂`. -/
theorem rot3_rot2 (hr : RepeatAt P c j) (hK : Rot2Def P c j) :
    rot3 P (rot2 P c j) (j + 2) = c := by
  obtain ⟨v0, -, v2, -, -⟩ := rot2_values hr hK
  have hsame : pairGraph G h (rot2 P c j) (c (P.x j)) (c (P.x (j + 4))) =
      pairGraph G h c (c (P.x j)) (c (P.x (j + 4))) := pairGraph_swap_same _ _ _ _
  have hreach := rot2_reach hr
  unfold rot3
  rw [f23, f22, v2, v0, hsame]
  have hset :
      {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x (j + 4)) v} =
        {v | (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) v} := by
    ext v
    exact ⟨fun r => hreach.trans r, fun r => hreach.symm.trans r⟩
  rw [hset]
  exact swap_swap _ _ _ _

end rot2

/-! ### The bijection -/

variable (P)

/-- Domain of `R₊₃` at `j`: proper, repeat at `j`, lock 2 at `j`, and `R₊₃` defined. -/
def Dom3 (j : Fin 5) : Set (V → Fin 4) :=
  {c | ProperOff G h c ∧ RepeatAt P c j ∧ Lock2 P c j ∧ Rot3Def P c j}

/-- Domain of `R₊₂` at `j`: proper, repeat at `j`, lock 1 at `j`, and `R₊₂` defined. -/
def Dom2 (j : Fin 5) : Set (V → Fin 4) :=
  {c | ProperOff G h c ∧ RepeatAt P c j ∧ Lock1 P c j ∧ Rot2Def P c j}

/-- `R₊₃` is a bijection from `Dom3 j` onto `Dom2 (j+3)`, with inverse `R₊₂`. -/
theorem rot3_bijOn (j : Fin 5) :
    Set.BijOn (fun c => rot3 P c j) (Dom3 P j) (Dom2 P (j + 3)) := by
  refine Set.InvOn.bijOn (f' := fun d => rot2 P d (j + 3)) ⟨?_, ?_⟩ ?_ ?_
  · intro c hc
    exact rot2_rot3 hc.2.1 hc.2.2.2
  · intro d hd
    have := rot3_rot2 hd.2.1 hd.2.2.2
    rw [f32] at this
    exact this
  · intro c hc
    obtain ⟨hp, hr, hl, hK⟩ := hc
    obtain ⟨-, hp', hr', hl'⟩ := rot3_spec hp hr hK
    exact ⟨hp', hr', hl'.mpr hl, rot3_rot2Def hr hK⟩
  · intro d hd
    obtain ⟨hp, hr, hl, hK⟩ := hd
    obtain ⟨-, hp', hr', hl'⟩ := rot2_spec hp hr hK
    have hD := rot2_rot3Def hr hK
    rw [f32] at hr' hl' hD
    exact ⟨hp', hr', hl'.mpr hl, hD⟩

/-- Injectivity of `R₊₃` on its domain. -/
theorem rot3_injOn (j : Fin 5) : Set.InjOn (fun c => rot3 P c j) (Dom3 P j) :=
  (rot3_bijOn P j).injOn

end SimpleGraph.QuarterFloor
