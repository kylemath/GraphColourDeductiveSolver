module

import Mathlib.Combinatorics.SimpleGraph.PlaneMap.BeltDWalkTeamA

open SimpleGraph
open SimpleGraph.VacancySlide
open SimpleGraph.BeltVacancyTeamA

-- The neighbour characterizations are derived from the actual graph.
example {n : Nat} (hn : 5 ≤ n) (i : ZMod n) (x : Vertex n) :
    (graph n).Adj (.u i) x ↔
    x=.a ∨ x=.u (i+1) ∨ x=.v i ∨ x=.v (i-1) ∨ x=.u (i-1) := adj_u hn i x

#print axioms SimpleGraph.BeltVacancyTeamA.adj_u
#print axioms SimpleGraph.BeltVacancyTeamA.adj_v
#print axioms SimpleGraph.BeltVacancyTeamA.doubled_one_first
#print axioms SimpleGraph.BeltVacancyTeamA.doubled_one_return
#print axioms SimpleGraph.BeltVacancyTeamA.a_tau_return
#print axioms SimpleGraph.BeltVacancyTeamA.SlidePath.proper

#print axioms SimpleGraph.BeltVacancyTeamA.a_rho_fill
#print axioms SimpleGraph.BeltVacancyTeamA.a_rho_return
#print axioms SimpleGraph.BeltVacancyTeamA.b_tau_return
#print axioms SimpleGraph.BeltVacancyTeamA.s_zero_fill
#print axioms SimpleGraph.BeltVacancyTeamA.s_zero_return
#print axioms SimpleGraph.BeltDWalkTeamA.doubled_one_walk
#print axioms SimpleGraph.BeltDWalkTeamA.doubled_one_opening_fills
