module

import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyEasyNeighbour

open SimpleGraph
open SimpleGraph.VacancySlide SimpleGraph.VacancyShortFill
open SimpleGraph.VacancyEasyNeighbour

namespace VacancyEasyNeighbourTest

/-- A five-leaf star whose initial link displays all four colours. -/
def star : SimpleGraph (Fin 6) where
  Adj x y := x ≠ y ∧ (x = 0 ∨ y = 0)
  symm := ⟨fun _ _ h => ⟨h.1.symm,h.2.symm⟩⟩
  loopless := ⟨fun _ h => h.1 rfl⟩

instance : DecidableRel star.Adj := fun _ _ =>
  inferInstanceAs (Decidable (_ ≠ _ ∧ (_ = 0 ∨ _ = 0)))

def colours (v : Fin 6) : Fin 4 :=
  if v = 3 then 1 else if v = 4 then 2 else if v = 5 then 3 else 0

lemma proper : ProperOff star 0 colours := by unfold ProperOff; decide
lemma not_target : ¬ Target star 0 colours := by unfold Target Missing; decide
lemma unique_three : UniqueAt star 0 3 colours := by unfold UniqueAt; decide
lemma not_unique_one : ¬ UniqueAt star 0 1 colours := by unfold UniqueAt; decide

example : PureFill star 0 colours 2 :=
  singleton_easy star proper (u := 3) (by decide) unique_three
    (easy_of_degree_le_three star 3 (by decide))

noncomputable def prepared : Fin 6 → Fin 4 := swap colours 0 1 {2}

lemma prepare : KempeStep star 0 colours prepared := by
  refine ⟨0,1,{2},by decide,?_,rfl⟩
  apply whole_singleton star (u := 2) ⟨by decide,Or.inl rfl⟩
  intro v edge outside
  have zero : v = 0 := by simpa [star] using edge.2
  exact (outside zero).elim

lemma prepared_unique : UniqueAt star 0 1 prepared := by
  intro v edge same
  fin_cases v <;> simp [prepared,swap,colours,star] at *

example : PureFill star 0 colours 3 :=
  mobility_easy star proper (u := 1) (by decide)
    (Or.inr ⟨prepared,prepare,prepared_unique⟩)
    (easy_of_degree_le_three star 1 (by decide))

example : PureFill star 0 colours 1 :=
  singleton_small star proper (u := 3) (by decide) unique_three (by decide)

example : PureFill star 0 colours 2 :=
  mobility_small star proper (u := 1) (by decide)
    (Or.inr ⟨prepared,prepare,prepared_unique⟩) (by decide)

/-- The auxiliary easy neighbour is protected; the final actual pure path is not. -/
example : ∃ n, n ≤ 3 ∧ ∃ d, PurePath star 0 n colours d ∧
    SimpleGraph.VacancyCliqueLift.ProtectedPath star Set.univ {1} n (0,colours) (0,d) ∧
      ProperOff star 0 d ∧ Target star 0 d :=
  mobility_easy_protected star proper (by simp) (u := 1) (by decide)
    (Or.inr (Or.inr ⟨prepared,prepare,prepared_unique⟩))
    (easy_of_degree_le_three star 1 (by decide))

end VacancyEasyNeighbourTest

/--
info: 'SimpleGraph.VacancyEasyNeighbour.singleton_easy' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.singleton_easy
/--
info: 'SimpleGraph.VacancyEasyNeighbour.mobility_easy' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.mobility_easy
/--
info: 'SimpleGraph.VacancyEasyNeighbour.mobility_alternative_easy' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.mobility_alternative_easy
/--
info: 'SimpleGraph.VacancyEasyNeighbour.mobility_easy_protected' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.mobility_easy_protected
/--
info: 'SimpleGraph.VacancyEasyNeighbour.target_of_degree_le_three' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.target_of_degree_le_three
/--
info: 'SimpleGraph.VacancyEasyNeighbour.easy_of_degree_le_three' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.easy_of_degree_le_three
/--
info: 'SimpleGraph.VacancyEasyNeighbour.singleton_small' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.singleton_small
/--
info: 'SimpleGraph.VacancyEasyNeighbour.mobility_small' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms SimpleGraph.VacancyEasyNeighbour.mobility_small

#print SimpleGraph.VacancyEasyNeighbour.singleton_easy
#print SimpleGraph.VacancyEasyNeighbour.mobility_easy_protected
#print SimpleGraph.VacancyEasyNeighbour.easy_of_degree_le_three
#print SimpleGraph.VacancyEasyNeighbour.OneSwapAt
#print SimpleGraph.VacancyEasyNeighbour.EasyAt
#print SimpleGraph.VacancyEasyNeighbour.SlideAccess
