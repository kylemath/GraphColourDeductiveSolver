module
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFillTeamB

open SimpleGraph SimpleGraph.VacancySlide SimpleGraph.VacancyShortFillTeamB

-- The palette is an unrestricted type; no four-colour or degree-5 parameter is hidden.
example {V C : Type*} [DecidableEq V] (G : SimpleGraph V) {r : V} {c : V → C}
    {t : V × (V → C)} {n : ℕ} (hc : ProperOff G r c)
    (hp : MixedPath G (r,c) t n) (hn : n ≤ 2) (ht : Target G t.1 t.2) :
    ∃ k, k ≤ n ∧ ∃ d, ProperOff G r d ∧ PurePath G r c d k ∧ Target G r d :=
  short_fill_proper G hc hp hn ht

-- In K2 the original stored hole colour equals the unique neighbour colour.
-- It is irrelevant to properness; the terminal slide still yields a legal singleton swap.
private def fixtureGraph : SimpleGraph (Fin 2) := ⊤
private def fixtureColour : Fin 2 → Fin 2 := fun _ => 0
private theorem fixtureProper : ProperOff fixtureGraph 0 fixtureColour := by
  intro u v huv hu hv
  have hu1 : u = 1 := by omega
  have hv1 : v = 1 := by omega
  subst u; subst v
  exact (huv.ne rfl).elim
private theorem fixtureUnique : UniqueAt fixtureGraph 0 1 fixtureColour := by
  intro v hv _
  have hv0 : v ≠ 0 := hv.ne.symm
  omega
private theorem fixtureTarget : Target fixtureGraph 1 (slide 0 1 fixtureColour) := by
  refine ⟨1,?_⟩
  intro v hv
  simp [fixtureColour,slide]
example : ∃ d, KempeStep fixtureGraph 0 fixtureColour d ∧ Target fixtureGraph 0 d := by
  exact terminal_slide fixtureGraph fixtureProper (by simp [fixtureGraph]) fixtureUnique fixtureTarget

/-- info: 'SimpleGraph.VacancyShortFillTeamB.terminal_slide' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms terminal_slide
/-- info: 'SimpleGraph.VacancyShortFillTeamB.properOff_swap' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms properOff_swap
/-- info: 'SimpleGraph.VacancyShortFillTeamB.sk_pair_fill' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms sk_pair_fill
/-- info: 'SimpleGraph.VacancyShortFillTeamB.sk_fill' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms sk_fill
/-- info: 'SimpleGraph.VacancyShortFillTeamB.two_step_fill' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms two_step_fill
/-- info: 'SimpleGraph.VacancyShortFillTeamB.short_fill' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms short_fill
/-- info: 'SimpleGraph.VacancyShortFillTeamB.short_fill_proper' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms short_fill_proper
/-- info: 'SimpleGraph.VacancyShortFillTeamB.short_minimum_eq' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms short_minimum_eq
/-- info: 'SimpleGraph.VacancyShortFillTeamB.short_minimum_exists' depends on axioms: [propext, Classical.choice, Quot.sound] -/
#guard_msgs in
#print axioms short_minimum_exists
