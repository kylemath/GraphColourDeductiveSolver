/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLemmaP
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaGroups
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame

/-!
# A non-doubly-locked `σ`-image gives a filled state; no all-DL class implies R\*

Formalises the reduction of `NightPostAW.md` §2 ("4CT analysis"): *every `Γ`-cycle has a
`σ`-image that is not doubly locked* implies R\*. Fix a pentagonal hole `P` at `h` on a spherical
map `M`; states are proper colourings of `M - h`, classes are `kclass M h c₀`.

## Main results (sorry-free, no new axioms)

* `filled_in_class_of_nonDL`: an unfilled state of a class that is not doubly locked has a
  filled `π`-neighbour in the class (`Lock2` fails ⇒ `π c` filled; `Lock1` fails ⇒ `π⁻¹ c`
  filled; Lemma P). `filled_in_class_of_not_dl` drops the "unfilled" hypothesis.
* `allDL_of_targetless` (Lemma C1, class form): a class with no filled state is all-DL.
* `filled_in_class_of_sigma_nonDL`: if some DL state `r` of a class has `σ r` not DL, the class
  has a filled state (`σ` is a Kempe step, so `σ r` is in the class).
* `GammaImages P`: every `Γ`-cycle (a `π`-orbit all of whose states are DL) has a state `r`,
  DL at `j`, with `σ r = sigSwap P r j` not DL.
* `no_allDL_class_of_images`, `filled_in_class_of_images`: under `GammaImages P` no class is
  all-DL, so every class has a filled state.
* `pureClean_of_every_class_filled`, `pureClean_of_images`: "every class has a filled state" is
  exactly the library's `PureClean M h` (Kempe equivalence ⇒ a `PurePath`).
* `rStarNoSepTri_of_images`, `rStarCore_of_images`, `four_color_of_images`: the bridges to the
  library's R\* statements (`RStarNoSepTri`, `RStarCore`) and to four colours, from the
  hypothesis that each triangulation of the class has a degree-five vertex `v` with a
  pentagonal link `P` satisfying `GammaImages P`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- Kempe equivalence gives a pure Kempe path. -/
theorem purePath_of_kempeEquiv {V : Type*} {G : SimpleGraph V} {h : V} {c d : V → Fin 4}
    (H : KempeEquiv (G := G) (h := h) c d) : ∃ m, PurePath G h m c d := by
  induction H using Relation.ReflTransGen.head_induction_on with
  | refl => exact ⟨0, .nil _⟩
  | head st _ ih =>
    obtain ⟨m, p⟩ := ih
    exact ⟨m + 1, .cons st p⟩

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

variable (P : Pent M.graph h) in
/-- Every `Γ`-cycle has a non-DL `σ`-image: if every state of the `π`-orbit of `c` is doubly
locked, some state `r = π^k c` of the orbit, doubly locked at `j`, has `σ r = sigSwap P r j`
not doubly locked. -/
def GammaImages : Prop :=
  ∀ c : Fin n → Fin 4, ProperOff M.graph h c → (∀ k : ℕ, DLState P ((piMove P)^[k] c)) →
    ∃ (k : ℕ) (j : Fin 5), DoublyLocked P ((piMove P)^[k] c) j ∧
      ¬ DLState P (sigSwap P ((piMove P)^[k] c) j)

variable {P : Pent M.graph h} {c₀ c : Fin n → Fin 4}

lemma self_mem_kclass (hc₀ : ProperOff M.graph h c₀) : c₀ ∈ kclass M h c₀ :=
  mem_kclass_iff.2 ⟨hc₀, Relation.ReflTransGen.refl⟩

lemma piInv_mem_kclass (hc : c ∈ kclass M h c₀) : piInv P c ∈ kclass M h c₀ := by
  obtain ⟨hp, he⟩ := mem_kclass_iff.1 hc
  exact mem_kclass_iff.2 ⟨piInv_properOff hp, he.tail (piInv_kempeStep hp)⟩

lemma iterate_mem_kclass (hc : c ∈ kclass M h c₀) (k : ℕ) :
    (piMove P)^[k] c ∈ kclass M h c₀ := by
  induction k with
  | zero => exact hc
  | succ k ih => rw [Function.iterate_succ_apply']; exact piMove_mem_kclass ih

/-- **(1)** An unfilled state of a class that is not doubly locked has a filled `π`-neighbour in
the class: if `Lock2` fails `π c` is filled, if `Lock1` fails `π⁻¹ c` is filled. -/
theorem filled_in_class_of_nonDL (hc : c ∈ kclass M h c₀) (hu : ¬ Target M.graph h c)
    (hnd : ¬ DLState P c) : ∃ d ∈ kclass M h c₀, Target M.graph h d := by
  have hp := (mem_kclass_iff.1 hc).1
  rcases classify (P := P) hp with ⟨j, hr⟩ | ⟨i, hs⟩
  · by_cases l2 : Lock2 P c j
    · have l1 : ¬ Lock1 P c j := fun l1 => hnd ⟨j, hr, l1, l2⟩
      refine ⟨piInv P c, piInv_mem_kclass hc, ?_⟩
      by_contra ht
      exact l1 ((unfilled_pred_iff_lock1 hp hr).1 ht)
    · refine ⟨piMove P c, piMove_mem_kclass hc, ?_⟩
      by_contra ht
      exact l2 ((unfilled_succ_iff_lock2 hp hr).1 ht)
  · exact absurd hs.1 hu

/-- A state of a class that is not doubly locked gives a filled state in the class. -/
theorem filled_in_class_of_not_dl (hc : c ∈ kclass M h c₀) (hnd : ¬ DLState P c) :
    ∃ d ∈ kclass M h c₀, Target M.graph h d := by
  by_cases ht : Target M.graph h c
  · exact ⟨c, hc, ht⟩
  · exact filled_in_class_of_nonDL hc ht hnd

/-- **Lemma C1 (class form).** A class with no filled state is all doubly locked. -/
theorem allDL_of_targetless (H : ∀ d ∈ kclass M h c₀, ¬ Target M.graph h d) :
    ∀ c ∈ kclass M h c₀, DLState P c := by
  intro c hc
  by_contra hnd
  obtain ⟨d, hd, ht⟩ := filled_in_class_of_not_dl (P := P) hc hnd
  exact H d hd ht

/-- **(2)** If a doubly locked state `r` of a class has a `σ`-image that is not doubly locked,
the class has a filled state. -/
theorem filled_in_class_of_sigma_nonDL {r : Fin n → Fin 4} {j : Fin 5}
    (hr : r ∈ kclass M h c₀) (hd : DoublyLocked P r j) (hσ : ¬ DLState P (sigSwap P r j)) :
    ∃ d ∈ kclass M h c₀, Target M.graph h d :=
  filled_in_class_of_not_dl (sigSwap_mem_kclass hr hd) hσ

/-- **(3)** Under `GammaImages P`, no class is all doubly locked. -/
theorem no_allDL_class_of_images (H : GammaImages P) (hc₀ : ProperOff M.graph h c₀) :
    ¬ ∀ c ∈ kclass M h c₀, DLState P c := by
  intro hall
  have h0 := self_mem_kclass hc₀
  obtain ⟨k, j, hd, hσ⟩ := H c₀ hc₀ fun k => hall _ (iterate_mem_kclass h0 k)
  exact hσ (hall _ (sigSwap_mem_kclass (iterate_mem_kclass h0 k) hd))

/-- Under `GammaImages P`, every class has a filled state. -/
theorem filled_in_class_of_images (H : GammaImages P) (hc₀ : ProperOff M.graph h c₀) :
    ∃ d ∈ kclass M h c₀, Target M.graph h d := by
  by_contra hno
  push Not at hno
  exact no_allDL_class_of_images H hc₀ (allDL_of_targetless hno)

variable (M h) in
/-- "Every Kempe class at `h` has a filled state" is the library's `PureClean M h`. -/
theorem pureClean_of_every_class_filled
    (H : ∀ c₀, ProperOff M.graph h c₀ → ∃ d ∈ kclass M h c₀, Target M.graph h d) :
    PureClean M h := by
  intro c hc
  obtain ⟨d, hd, ht⟩ := H c hc
  obtain ⟨m, p⟩ := purePath_of_kempeEquiv (mem_kclass_iff.1 hd).2
  exact ⟨m, m, le_rfl, d, p, ht⟩

/-- Under `GammaImages P`, the hole is pure-clean. -/
theorem pureClean_of_images (H : GammaImages P) : PureClean M h :=
  pureClean_of_every_class_filled M h fun _ hc₀ => filled_in_class_of_images H hc₀

end sphere

/-! ### Bridges to the library's R\* -/

/-- `RStarNoSepTri` (`MinimalFrame`) from `GammaImages` at some degree-five vertex of each
minimum-degree-five triangulation with no separating triangle. -/
theorem rStarNoSepTri_of_images
    (H : ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) → NoSep T →
      ∃ v, T.graph.degree v = 5 ∧ ∃ P : Pent T.graph v, GammaImages P) :
    RStarNoSepTri := by
  intro m T hm hconn htri hdeg hns
  obtain ⟨v, hv, P, hP⟩ := H m T hm hconn htri hdeg hns
  exact ⟨v, hv, pureClean_of_images hP⟩

/-- `RStarCore` (`RStarCore`) from `GammaImages` at some degree-five vertex off the protected
face of each core triangulation. -/
theorem rStarCore_of_images
    (H : ∀ (m : ℕ) (T : SphericalMap m) (p q r : Fin m), T.graph.Connected → T.Triangulated →
      T.Adj p q → T.Adj q r → T.Adj r p → Facial T p q r → NoSep T →
      (∀ x, x ≠ p → x ≠ q → x ≠ r → 5 ≤ T.graph.degree x) →
      ∃ v, v ≠ p ∧ v ≠ q ∧ v ≠ r ∧ T.graph.degree v = 5 ∧ ∃ P : Pent T.graph v, GammaImages P) :
    RStarCore := by
  intro m T p q r hc ht hpq hqr hrp hf hns hdeg
  obtain ⟨v, h1, h2, h3, hv, P, hP⟩ := H m T p q r hc ht hpq hqr hrp hf hns hdeg
  exact ⟨v, h1, h2, h3, hv, pureClean_of_images hP⟩

/-- Four colours from `GammaImages` at a degree-five vertex of each minimum-degree-five
triangulation with no separating triangle. -/
theorem four_color_of_images
    (H : ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) → NoSep T →
      ∃ v, T.graph.degree v = 5 ∧ ∃ P : Pent T.graph v, GammaImages P)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4 :=
  four_color_of_RStar_noSepTri (rStarNoSepTri_of_images H) M

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.filled_in_class_of_sigma_nonDL
#print axioms SimpleGraph.QuarterFloor.no_allDL_class_of_images
#print axioms SimpleGraph.QuarterFloor.rStarCore_of_images
#print axioms SimpleGraph.QuarterFloor.four_color_of_images
