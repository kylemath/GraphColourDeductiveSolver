import Mathlib.Combinatorics.SimpleGraph.PlaneMap.ChainF
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameWit22
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameScope
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameNoFrozen

/-!
# Audit 2026-10-08: non-vacuity of the 7-8 Oct headline hypotheses

Written by the audit (not part of the library). On the order-22 frame-class witness
`FrameWit22.sphericalMap`, at the degree-5 vertex `0` with link `1,2,3,4,5`, we exhibit:
* the hypotheses `Triangulated`, no isolated vertex, `Pent` of `conjectureF` /
  `chainParityLaw_sphere` / `rigid_isolation` / `remark7`;
* a proper colouring of `T - 0` that is unfilled in frame `j = 2` (`RepeatAt`) and doubly locked
  (`Lock1`, `Lock2`, by explicit Kempe paths found by the audit's script), so the formula and the
  law are instantiated at a genuine state;
* `LinkTipsClean` at some `j`, so `no_555_run` / `no_565_run` are not vacuous in the class.
-/

open SimpleGraph SimpleGraph.QuarterFloor VacancyShortFill VacancySlide

namespace AuditNV
open SimpleGraph.FrameWit22

def P : Pent sphericalMap.graph 0 where
  x := ![1, 2, 3, 4, 5]
  adj_h := by
    show ∀ i : Fin 5, graph.Adj 0 (![1, 2, 3, 4, 5] i)
    decide
  adj_cyc := by
    show ∀ i : Fin 5, graph.Adj (![1, 2, 3, 4, 5] i) (![1, 2, 3, 4, 5] (i + 1))
    decide
  inj := by
    intro i j hij
    revert i j; decide
  only := by
    show ∀ v : Fin 22, graph.Adj 0 v → ∃ i : Fin 5, v = ![1, 2, 3, 4, 5] i
    decide

theorem hiso : ∀ v, ∃ w, sphericalMap.graph.Adj v w := by
  show ∀ v : Fin 22, ∃ w, graph.Adj v w
  decide

theorem deg0 : sphericalMap.graph.degree 0 = 5 := by
  rw [sphericalMap_degree]; rfl

def c : Fin 22 → Fin 4 := ![0, 3, 2, 1, 0, 1, 0, 1, 0, 2, 3, 1, 2, 3, 1, 3, 2, 3, 0, 2, 0, 0]

theorem hc : ProperOff sphericalMap.graph 0 c := by
  have h : ∀ u v : Fin 22, graph.Adj u v → u ≠ 0 → v ≠ 0 → c u ≠ c v := by decide
  intro u v e hu hv
  exact h u v e hu hv

theorem hr : RepeatAt P c 2 := by
  unfold RepeatAt
  decide

theorem pA {a b : Fin 4} {u v : Fin 22}
    (h : graph.Adj u v ∧ (u ≠ 0 ∧ (c u = a ∨ c u = b)) ∧ (v ≠ 0 ∧ (c v = a ∨ c v = b))) :
    (pairGraph sphericalMap.graph 0 c a b).Adj u v := h

/-- Lock 1 in frame 2: `{c 4, c 1} = {0, 3}`-path 4-10-18-17-21-15-6-1. -/
theorem l1 : Lock1 P c 2 := by
  show (pairGraph sphericalMap.graph 0 c 0 3).Reachable 4 1
  exact ((((((((pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 4 10).reachable.trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 10 18).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 18 17).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 17 21).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 21 15).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 15 6).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 3).Adj 6 1).reachable))

/-- Lock 2 in frame 2: `{c 4, c 2} = {0, 2}`-path 4-12-20-19-18-9-8-2. -/
theorem l2 : Lock2 P c 2 := by
  show (pairGraph sphericalMap.graph 0 c 0 2).Reachable 4 2
  exact ((((((((pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 4 12).reachable.trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 12 20).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 20 19).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 19 18).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 18 9).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 9 8).reachable).trans
    (pA (by decide) : (pairGraph sphericalMap.graph 0 c 0 2).Adj 8 2).reachable))

theorem hd : DoublyLocked P c 2 := ⟨hr, l1, l2⟩

/-- The chain-count formula, instantiated at a genuine unfilled state. -/
def F_inst := chainFormulaF sphericalMap_triangulated hiso P c 2 hc hr

/-- The chain-parity law, instantiated at a genuine doubly locked state. -/
def law_inst := chainParityLaw_sphere sphericalMap_triangulated hiso P c hc ⟨2, hd⟩

/-- Lemma 3 at the same state. -/
def eight_inst := eight_le_nChains sphericalMap_triangulated P hd

/-- Lock parity at the same state. -/
def lp_inst := (lock2_iff_odd_boundary sphericalMap_triangulated P hc hr).1 l2

/-- Lemma W at pi at the same state. -/
def w_inst := cw_piMove sphericalMap_triangulated P hc hd

/-- `conjectureF` applies to this map and hole. -/
theorem conjF_inst : ChainFormulaF sphericalMap P :=
  conjectureF 22 sphericalMap 0 P sphericalMap_triangulated hiso

/-- `LinkTipsClean` holds at every `j` on this frame-class member, so `no_555_run`/`no_565_run`
are not vacuous inside the frame class. -/
theorem tips (j : Fin 5) : SphericalMap.FrameScope.LinkTipsClean P j := by
  unfold SphericalMap.FrameScope.LinkTipsClean
  revert j
  show ∀ (j : Fin 5) (y : Fin 22), graph.Adj (![1, 2, 3, 4, 5] j) y →
    graph.Adj (![1, 2, 3, 4, 5] (j + 2)) y → y = 0 ∨ y = ![1, 2, 3, 4, 5] (j + 1)
  decide

def no555_inst := SphericalMap.FrameScope.no_555_run P sphericalMap_triangulated noSep
  diamondFree deg0 0 (tips 0)

/-- The hypothesis shape of `NoFrozenFrame` is met at this member: degree-5 vertex with a `Pent`. -/
example : ∃ v, sphericalMap.graph.degree v = 5 ∧ Nonempty (Pent sphericalMap.graph v) :=
  ⟨0, deg0, ⟨P⟩⟩

end AuditNV

#print axioms AuditNV.F_inst
#print axioms AuditNV.law_inst
#print axioms AuditNV.eight_inst
#print axioms AuditNV.lp_inst
#print axioms AuditNV.w_inst
#print axioms AuditNV.conjF_inst
#print axioms AuditNV.tips
#print axioms AuditNV.no555_inst
