module

import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltVacancyHyp

open SimpleGraph SimpleGraph.VacancyHyp

-- Guard: the definition is literally the conclusion of the compiled belt theorem.
example (n : ℕ) (hn : 5 ≤ n) (h : TwoPoleBelt.Vertex n) :
    VacancyAt (TwoPoleBelt.graph n) (6 * n) h :=
  fun c hc => TwoPoleBeltPoleHole.belt_theorem_all_holes hn h c hc

#print axioms SimpleGraph.VacancyHyp.VacancyAt.colouring
#print axioms SimpleGraph.VacancyHyp.VacancyAt.of_iso
#print axioms SimpleGraph.VacancyHyp.VacancyHyp.of_iso
#print axioms SimpleGraph.TwoPoleBeltVacancyHyp.vacancyAt_belt
#print axioms SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_belt
#print axioms SimpleGraph.TwoPoleBeltVacancyHyp.belt_colouring
#print axioms SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_of_iso_belt
#print axioms SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_sphericalMap_of_iso
#print axioms SimpleGraph.TwoPoleBeltVacancyHyp.belt_path_protected_trivial
set_option pp.proofs.withType false
#print SimpleGraph.VacancyHyp.VacancyAt
#print SimpleGraph.VacancyHyp.VacancyHyp
#check @SimpleGraph.TwoPoleBeltVacancyHyp.vacancyAt_belt
#check @SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_belt
#check @SimpleGraph.TwoPoleBeltVacancyHyp.belt_colouring
#check @SimpleGraph.TwoPoleBeltVacancyHyp.vacancyHyp_sphericalMap_of_iso
