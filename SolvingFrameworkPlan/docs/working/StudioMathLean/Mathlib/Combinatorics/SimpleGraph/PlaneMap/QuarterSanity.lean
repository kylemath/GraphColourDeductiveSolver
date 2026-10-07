/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFloorH
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron

/-!
# Sanity check: the quarter-floor hypotheses are satisfiable

At vertex `0` of the icosahedron, the link in rotation order is `1, 5, 11, 7, 8`, and the outer
ring is `6, 4, 10, 9, 2`. We exhibit the `Pent` and `IcoBallP` and obtain `QuarterFloorConj`
from `quarterFloor_of_icoBall`, so `Pent`/`IcoBallP` are not vacuous hypotheses.
-/

@[expose] public section

namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

namespace Icosahedron
open SimpleGraph.Icosahedron

/-- The pentagonal hole at vertex `0` of the icosahedron. -/
def pent : Pent sphericalMap.graph 0 where
  x := ![1, 5, 11, 7, 8]
  adj_h := by
    show ∀ i : Fin 5, graph.Adj 0 (![1, 5, 11, 7, 8] i)
    decide
  adj_cyc := by
    show ∀ i : Fin 5, graph.Adj (![1, 5, 11, 7, 8] i) (![1, 5, 11, 7, 8] (i + 1))
    decide
  inj := by
    intro i j hij
    revert i j; decide
  only := by
    show ∀ v : Fin 12, graph.Adj 0 v → ∃ i : Fin 5, v = ![1, 5, 11, 7, 8] i
    decide

/-- The outer ring. -/
def ring : Fin 5 → Fin 12 := ![6, 4, 10, 9, 2]

theorem icoBallP : IcoBallP pent ring where
  nbr := by
    show ∀ (t : Fin 5) (u : Fin 12), graph.Adj (![1, 5, 11, 7, 8] t) u ↔
      u = 0 ∨ u = ![1, 5, 11, 7, 8] (t + 4) ∨ u = ![1, 5, 11, 7, 8] (t + 1) ∨
        u = ring (t + 4) ∨ u = ring t
    decide
  ring := by
    show ∀ t : Fin 5, graph.Adj (ring t) (ring (t + 1))
    decide
  off := by
    show ∀ (t i : Fin 5), ring t ≠ ![1, 5, 11, 7, 8] i
    decide
  offh := by
    show ∀ t : Fin 5, ring t ≠ 0
    decide

example : QuarterFloorConj (G := sphericalMap.graph) (h := (0 : Fin 12)) :=
  quarterFloor_of_icoBall icoBallP

end Icosahedron
end SimpleGraph.QuarterFloor
