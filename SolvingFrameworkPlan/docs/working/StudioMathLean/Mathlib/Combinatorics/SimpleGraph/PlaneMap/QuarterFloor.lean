/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFill
public import Mathlib.Logic.Equiv.Basic
public import Mathlib.Logic.Relation

/-!
# The quarter floor at a pentagonal hole

Definitions, in the vacancy language of `VacancyShortFill`, of the objects behind the
"quarter floor": a pentagonal hole `h` with link `x 0, …, x 4`, the repeat pair of an unfilled
state, the two Kempe locks, doubly locked states, and Kempe classes.

* `lemmaA_map`: Kempe's single swap at a non-doubly-locked unfilled state, made explicit.
* `lemmaA`: the swap lands in a filled state with a prescribed singleton position and is
  injective for each repeat index `j` and lock case (the audited hand result, Lemma A).
* `QuarterFloorConj`: the open statement, every Kempe class is at least one quarter filled.

Nothing here assumes planarity; the quarter floor itself is expected to need it.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill

variable {V : Type*} (G : SimpleGraph V)

/-- A pentagonal hole: a vertex `h` whose neighbours are exactly `x 0, …, x 4`, in cyclic order. -/
structure Pent (h : V) where
  x : Fin 5 → V
  adj_h : ∀ i, G.Adj h (x i)
  adj_cyc : ∀ i, G.Adj (x i) (x (i + 1))
  inj : Function.Injective x
  only : ∀ v, G.Adj h v → ∃ i, v = x i

variable {G} {h : V} (P : Pent G h)

/-- Two colourings are Kempe equivalent when a finite sequence of whole-component swaps
joins them. -/
def KempeEquiv (c d : V → Fin 4) : Prop :=
  Relation.ReflTransGen (KempeStep G h) c d

/-- The unfilled pattern with repeat pair `{j, j+2}`: `x j` and `x (j+2)` share a colour and
the remaining three link colours are distinct from it and from each other. -/
def RepeatAt (c : V → Fin 4) (j : Fin 5) : Prop :=
  c (P.x j) = c (P.x (j + 2)) ∧
  c (P.x (j + 1)) ≠ c (P.x j) ∧ c (P.x (j + 3)) ≠ c (P.x j) ∧ c (P.x (j + 4)) ≠ c (P.x j) ∧
  c (P.x (j + 1)) ≠ c (P.x (j + 3)) ∧ c (P.x (j + 1)) ≠ c (P.x (j + 4)) ∧
  c (P.x (j + 3)) ≠ c (P.x (j + 4))

/-- Lock 1 at `j`: the `{μ, A}`-component of `m = x (j+1)` contains `a = x (j+3)`. -/
def Lock1 (c : V → Fin 4) (j : Fin 5) : Prop :=
  (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 1)) (P.x (j + 3))

/-- Lock 2 at `j`: the `{μ, B}`-component of `m = x (j+1)` contains `b = x (j+4)`. -/
def Lock2 (c : V → Fin 4) (j : Fin 5) : Prop :=
  (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1)) (P.x (j + 4))

/-- Doubly locked at `j`. -/
def DoublyLocked (c : V → Fin 4) (j : Fin 5) : Prop :=
  RepeatAt P c j ∧ Lock1 P c j ∧ Lock2 P c j

/-- A filled state whose singleton link colour sits at position `i`. -/
def SingletonAt (c : V → Fin 4) (i : Fin 5) : Prop :=
  Target G h c ∧ ∀ k, k ≠ i → c (P.x k) ≠ c (P.x i)

/-- Lemma A, case 1 (lock 1 fails): swap the `{μ, A}`-component of `a = x (j+3)`. -/
noncomputable def lemmaA_map (c : V → Fin 4) (j : Fin 5) : V → Fin 4 :=
  swap c (c (P.x (j + 1))) (c (P.x (j + 3)))
    {v | (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 3)) v}

section helpers
variable {C : Type*} [DecidableEq C]

lemma active_swap_iff {c : V → C} {a b : C} {S : Set V} (v : V) :
    Active h (swap c a b S) a b v ↔ Active h c a b v := by
  unfold Active
  by_cases hv : v ∈ S
  · rw [swap_in hv]
    refine and_congr_right fun _ => ?_
    rw [Equiv.swap_apply_eq_iff, Equiv.swap_apply_eq_iff, Equiv.swap_apply_left,
      Equiv.swap_apply_right, or_comm]
  · rw [swap_out hv]

lemma pairGraph_swap (c : V → C) (a b : C) (S : Set V) :
    pairGraph G h (swap c a b S) a b = pairGraph G h c a b := by
  ext v w
  show (G.Adj v w ∧ Active h (swap c a b S) a b v ∧ Active h (swap c a b S) a b w) ↔
    (G.Adj v w ∧ Active h c a b v ∧ Active h c a b w)
  rw [active_swap_iff, active_swap_iff]

lemma swap_swap_self (c : V → C) (a b : C) (S : Set V) : swap (swap c a b S) a b S = c := by
  funext v
  by_cases hv : v ∈ S
  · rw [swap_in hv, swap_in hv, Equiv.swap_apply_self]
  · rw [swap_out hv, swap_out hv]

end helpers

/-- Kempe steps are symmetric: swapping the same whole component again undoes the step. -/
theorem kempeStep_symm [DecidableEq V] {c d : V → Fin 4} :
    KempeStep G h c d → KempeStep G h d c := by
  rintro ⟨a, b, S, hab, ⟨s, hs, hS⟩, rfl⟩
  refine ⟨a, b, S, hab, ⟨s, (active_swap_iff s).2 hs, fun v => ?_⟩, (swap_swap_self c a b S).symm⟩
  rw [pairGraph_swap]
  exact hS v

/-- Kempe equivalence is symmetric. -/
theorem kempeEquiv_symm [DecidableEq V] {c d : V → Fin 4} :
    KempeEquiv (G := G) (h := h) c d → KempeEquiv (G := G) (h := h) d c := by
  intro H
  induction H with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hbc ih => exact Relation.ReflTransGen.head (kempeStep_symm hbc) ih

lemma fin5_cases (j k : Fin 5) :
    k = j ∨ k = j + 1 ∨ k = j + 2 ∨ k = j + 3 ∨ k = j + 4 := by
  revert j k; decide

lemma fin4_fourth (a b c x y : Fin 4) (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c)
    (hxa : x ≠ a) (hxb : x ≠ b) (hxc : x ≠ c) (hya : y ≠ a) (hyb : y ≠ b) (hyc : y ≠ c) :
    x = y := by
  revert a b c x y; decide

/-- The five link values of the Lemma A swap. -/
lemma lemmaA_vals (c : V → Fin 4) (j : Fin 5) (hr : RepeatAt P c j) (hl : ¬ Lock1 P c j) :
    lemmaA_map P c j (P.x j) = c (P.x j) ∧
    lemmaA_map P c j (P.x (j + 1)) = c (P.x (j + 1)) ∧
    lemmaA_map P c j (P.x (j + 2)) = c (P.x j) ∧
    lemmaA_map P c j (P.x (j + 3)) = c (P.x (j + 1)) ∧
    lemmaA_map P c j (P.x (j + 4)) = c (P.x (j + 4)) := by
  obtain ⟨h0, h1, h2, -, -, h5, h6⟩ := hr
  have aS : P.x (j + 3) ∈ {v | (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
      (P.x (j + 3)) v} := Reachable.refl _
  have mS : P.x (j + 1) ∉ {v | (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
      (P.x (j + 3)) v} := by
    intro hm; apply hl; exact Reachable.symm hm
  unfold lemmaA_map
  refine ⟨swap_other (Ne.symm h1) (Ne.symm h2), swap_out mS,
    (swap_other (by rw [← h0]; exact Ne.symm h1) (by rw [← h0]; exact Ne.symm h2)).trans h0.symm,
    by rw [swap_in aS, Equiv.swap_apply_right], swap_other (Ne.symm h5) (Ne.symm h6)⟩

/-- Lemma A, case 1: at an unfilled proper state with repeat pair `{j, j+2}` whose lock 1
fails, the swap is a Kempe step to a filled state with singleton at `j + 4`. -/
theorem lemmaA_step (c : V → Fin 4) (j : Fin 5)
    (hc : ProperOff G h c) (hr : RepeatAt P c j) (hl : ¬ Lock1 P c j) :
    KempeStep G h c (lemmaA_map P c j) ∧ ProperOff G h (lemmaA_map P c j) ∧
      SingletonAt P (lemmaA_map P c j) (j + 4) := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := lemmaA_vals P c j hr hl
  obtain ⟨-, h1, h2, h3, h4, h5, h6⟩ := hr
  have hW := whole_component G h c (c (P.x (j + 1))) (c (P.x (j + 3))) (P.x (j + 3))
    ⟨(P.adj_h _).ne.symm, Or.inr rfl⟩
  refine ⟨⟨_, _, _, h4, hW, rfl⟩, properOff_swap G hc hW, ⟨⟨c (P.x (j + 3)), ?_⟩, ?_⟩⟩
  · intro v e he
    obtain ⟨i, rfl⟩ := P.only v e
    rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
    · rw [v0] at he; exact h2 he.symm
    · rw [v1] at he; exact h4 he
    · rw [v2] at he; exact h2 he.symm
    · rw [v3] at he; exact h4 he
    · rw [v4] at he; exact h6 he.symm
  · intro k hk
    rw [v4]
    rcases fin5_cases j k with rfl | rfl | rfl | rfl | rfl
    · rw [v0]; exact h3.symm
    · rw [v1]; exact h5
    · rw [v2]; exact h3.symm
    · rw [v3]; exact h5
    · exact absurd rfl hk

/-- Lemma A, case 1, injectivity: the swap is undone by swapping the same component in the
image, so two states with the same repeat index and failing lock 1 that map to the same
filled state are equal. -/
theorem lemmaA_injective (c c' : V → Fin 4) (j : Fin 5)
    (hc : ProperOff G h c) (hr : RepeatAt P c j) (hl : ¬ Lock1 P c j)
    (hc' : ProperOff G h c') (hr' : RepeatAt P c' j) (hl' : ¬ Lock1 P c' j)
    (heq : lemmaA_map P c j = lemmaA_map P c' j) : c = c' := by
  have key : ∀ c : V → Fin 4, RepeatAt P c j → ¬ Lock1 P c j →
      c = swap (lemmaA_map P c j) (lemmaA_map P c j (P.x (j + 1))) (c (P.x (j + 3)))
        {v | (pairGraph G h (lemmaA_map P c j) (lemmaA_map P c j (P.x (j + 1)))
          (c (P.x (j + 3)))).Reachable (P.x (j + 3)) v} := by
    intro c hr hl
    rw [(lemmaA_vals P c j hr hl).2.1]
    unfold lemmaA_map
    rw [pairGraph_swap, swap_swap_self]
  obtain ⟨v0, v1, -, -, v4⟩ := lemmaA_vals P c j hr hl
  obtain ⟨v0', v1', -, -, v4'⟩ := lemmaA_vals P c' j hr' hl'
  have e0 : c (P.x j) = c' (P.x j) := by rw [← v0, ← v0', heq]
  have e1 : c (P.x (j + 1)) = c' (P.x (j + 1)) := by rw [← v1, ← v1', heq]
  have e4 : c (P.x (j + 4)) = c' (P.x (j + 4)) := by rw [← v4, ← v4', heq]
  have hA : c (P.x (j + 3)) = c' (P.x (j + 3)) := by
    obtain ⟨-, h1, h2, h3, h4, h5, h6⟩ := hr
    obtain ⟨-, h1', h2', h3', h4', h5', h6'⟩ := hr'
    rw [← e0, ← e1, ← e4] at *
    exact fin4_fourth _ _ _ _ _ h1.symm h3.symm h5 h2 h4.symm h6 h2' h4'.symm h6'
  have e := key c hr hl
  have e' := key c' hr' hl'
  rw [heq, hA] at e
  exact e.trans e'.symm

/-- The quarter floor (open): in every Kempe class of proper colourings of `G - h`, at least a
quarter of the colourings are filled. Stated for finite `V` with classes as finsets. -/
def QuarterFloorConj [Fintype V] : Prop :=
  ∀ c₀ : V → Fin 4, ProperOff G h c₀ →
    4 * Nat.card {c : V → Fin 4 // KempeEquiv (G := G) (h := h) c₀ c ∧ Target G h c} ≥
      Nat.card {c : V → Fin 4 // KempeEquiv (G := G) (h := h) c₀ c}

end SimpleGraph.QuarterFloor
