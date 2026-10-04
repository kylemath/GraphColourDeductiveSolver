/-
  F1_ColoringBasics.lean — navigator node `f1`.

  Agent 1720, M-Foundation, group L2.

  Sanity layer over Mathlib's colouring API
  (`Mathlib/Combinatorics/SimpleGraph/Coloring.lean`):
  * `SimpleGraph.Coloring G α` is a graph hom `G →g (⊤ : SimpleGraph α)`;
  * `SimpleGraph.Colorable G n` is `Nonempty (G.Coloring (Fin n))`.

  Main results (target: 0 sorry):
  * `K4_colorable_four`      : (⊤ : SimpleGraph (Fin 4)).Colorable 4
  * `K4_not_colorable_three` : ¬ (⊤ : SimpleGraph (Fin 4)).Colorable 3
  * `K4_chromaticNumber`     : (⊤ : SimpleGraph (Fin 4)).chromaticNumber = 4
  and the general versions for `K_n`.
-/

import Mathlib.Combinatorics.SimpleGraph.Coloring

namespace FourColor.Foundation

open SimpleGraph

/-- The complete graph on `n` vertices is `n`-colourable: colour each vertex by itself. -/
theorem top_colorable_self (n : ℕ) : (⊤ : SimpleGraph (Fin n)).Colorable n :=
  ⟨(⊤ : SimpleGraph (Fin n)).selfColoring⟩

/-- Any colouring of a complete graph is injective: distinct vertices are adjacent. -/
theorem top_coloring_injective {V α : Type*} (C : (⊤ : SimpleGraph V).Coloring α) :
    Function.Injective C := by
  intro u v h
  by_contra hne
  exact C.valid ((top_adj u v).mpr hne) h

/-- The complete graph on `n` vertices is not `m`-colourable for `m < n`
    (pigeonhole via injectivity of the colouring). -/
theorem top_not_colorable_of_lt {n m : ℕ} (hmn : m < n) :
    ¬ (⊤ : SimpleGraph (Fin n)).Colorable m := by
  rintro ⟨C⟩
  have hcard := Fintype.card_le_of_injective C (top_coloring_injective C)
  simp only [Fintype.card_fin] at hcard
  omega

/-- `K_n` is `m`-colourable iff `n ≤ m`. -/
theorem top_colorable_iff (n m : ℕ) : (⊤ : SimpleGraph (Fin n)).Colorable m ↔ n ≤ m := by
  constructor
  · intro h
    by_contra hlt
    exact top_not_colorable_of_lt (Nat.lt_of_not_le hlt) h
  · intro h
    exact (top_colorable_self n).mono h

/-- **F1 (a).** `K₄` is 4-colourable. -/
theorem K4_colorable_four : (⊤ : SimpleGraph (Fin 4)).Colorable 4 :=
  top_colorable_self 4

/-- **F1 (b).** `K₄` is not 3-colourable. -/
theorem K4_not_colorable_three : ¬ (⊤ : SimpleGraph (Fin 4)).Colorable 3 :=
  top_not_colorable_of_lt (by decide)

/-- **F1 (c).** The chromatic number of `K₄` is 4 (Mathlib's `chromaticNumber_top`). -/
theorem K4_chromaticNumber : (⊤ : SimpleGraph (Fin 4)).chromaticNumber = 4 := by
  rw [chromaticNumber_top, Fintype.card_fin]
  rfl

/-- Cross-check of (b). Mathlib v4.15 has no `Colorable.card_le_of_pairwise_adj`,
    so this uses the same pigeonhole as `top_not_colorable_of_lt`. -/
theorem K4_not_colorable_three' : ¬ (⊤ : SimpleGraph (Fin 4)).Colorable 3 :=
  top_not_colorable_of_lt (by decide)

/-- An explicit proper 4-colouring of `K₄` as a function, checked by `decide`. -/
def K4_explicit : Fin 4 → Fin 4 := fun i => i

theorem K4_explicit_proper :
    ∀ u v : Fin 4, (⊤ : SimpleGraph (Fin 4)).Adj u v → K4_explicit u ≠ K4_explicit v := by
  simp only [top_adj]
  decide

end FourColor.Foundation
