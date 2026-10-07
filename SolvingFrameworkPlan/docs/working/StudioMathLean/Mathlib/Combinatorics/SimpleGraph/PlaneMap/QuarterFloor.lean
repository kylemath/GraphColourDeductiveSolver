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

/-- Lemma A, case 1: at an unfilled proper state with repeat pair `{j, j+2}` whose lock 1
fails, the swap is a Kempe step to a filled state with singleton at `j + 4`. -/
theorem lemmaA_step (c : V → Fin 4) (j : Fin 5)
    (hc : ProperOff G h c) (hr : RepeatAt P c j) (hl : ¬ Lock1 P c j) :
    KempeStep G h c (lemmaA_map P c j) ∧ ProperOff G h (lemmaA_map P c j) ∧
      SingletonAt P (lemmaA_map P c j) (j + 4) := by
  sorry

/-- Lemma A, case 1, injectivity: the swap is undone by swapping the same component in the
image, so two states with the same repeat index and failing lock 1 that map to the same
filled state are equal. -/
theorem lemmaA_injective (c c' : V → Fin 4) (j : Fin 5)
    (hc : ProperOff G h c) (hr : RepeatAt P c j) (hl : ¬ Lock1 P c j)
    (hc' : ProperOff G h c') (hr' : RepeatAt P c' j) (hl' : ¬ Lock1 P c' j)
    (heq : lemmaA_map P c j = lemmaA_map P c' j) : c = c' := by
  sorry

/-- The quarter floor (open): in every Kempe class of proper colourings of `G - h`, at least a
quarter of the colourings are filled. Stated for finite `V` with classes as finsets. -/
def QuarterFloorConj [Fintype V] : Prop :=
  ∀ c₀ : V → Fin 4, ProperOff G h c₀ →
    4 * Nat.card {c : V → Fin 4 // KempeEquiv (G := G) (h := h) c₀ c ∧ Target G h c} ≥
      Nat.card {c : V → Fin 4 // KempeEquiv (G := G) (h := h) c₀ c}

end SimpleGraph.QuarterFloor
