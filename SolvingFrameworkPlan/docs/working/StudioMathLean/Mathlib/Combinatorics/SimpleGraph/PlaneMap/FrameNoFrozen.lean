module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameF3
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterBitDynamics

/-!
# `RStarFrame` from the absence of frozen `π`-orbits

Track C, 7 Oct 2026 (Corollary 7 of `TrackD/PartialResultsPaper.md`). Wrappers composing
`pureClean_of_no_allDL_orbit` (resp. `pureClean_of_images`) with the frame-class reduction
`four_color_of_RStarFrame`.

## Main results (sorry-free, no new axioms)

* `rStarFrame_of_no_allDL_orbit`: if every frame-class triangulation (connected, triangulated,
  minimum degree five, `NoSep`, `DiamondFree`, `Conf2122Free`) has a degree-five vertex `v` with a
  pentagonal link `P` at which every `π`-orbit of proper states of `T - v` contains a state that
  is not doubly locked, then `RStarFrame`.
* `four_color_of_no_allDL_orbit_frame`: the same hypothesis gives four colours.
* `rStarFrame_of_images`, `four_color_of_images_frame`: the same with `GammaImages P`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- The hypothesis of Corollary 7: every frame-class triangulation has a degree-five vertex with
a pentagonal link at which no `π`-orbit is all doubly locked. -/
def NoFrozenFrame : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) → NoSep T → DiamondFree T → Conf2122Free T →
    ∃ v, T.graph.degree v = 5 ∧ ∃ P : Pent T.graph v,
      ∀ c : Fin m → Fin 4, ProperOff T.graph v c → ∃ k, ¬ DLState P ((piMove P)^[k] c)

/-- **`rStarFrame_of_no_allDL_orbit`.** No frozen (all-DL) `π`-orbit at some degree-five vertex
of every frame-class triangulation implies `RStarFrame`. -/
theorem rStarFrame_of_no_allDL_orbit (H : NoFrozenFrame) : RStarFrame := by
  intro m T hm hconn htri hdeg hns hD hC
  obtain ⟨v, hv, P, hP⟩ := H m T hm hconn htri hdeg hns hD hC
  exact ⟨v, hv, pureClean_of_no_allDL_orbit P hP⟩

/-- Four colours from `NoFrozenFrame`. -/
theorem four_color_of_no_allDL_orbit_frame (H : NoFrozenFrame) {n : ℕ} (M : SphericalMap n) :
    M.graph.Colorable 4 :=
  four_color_of_RStarFrame (rStarFrame_of_no_allDL_orbit H) M

/-- `RStarFrame` from `GammaImages` at some degree-five vertex of every frame-class
triangulation. -/
theorem rStarFrame_of_images
    (H : ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) → NoSep T → DiamondFree T → Conf2122Free T →
      ∃ v, T.graph.degree v = 5 ∧ ∃ P : Pent T.graph v, GammaImages P) :
    RStarFrame := by
  intro m T hm hconn htri hdeg hns hD hC
  obtain ⟨v, hv, P, hP⟩ := H m T hm hconn htri hdeg hns hD hC
  exact ⟨v, hv, pureClean_of_images hP⟩

/-- Four colours from `GammaImages` in the frame class. -/
theorem four_color_of_images_frame
    (H : ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) → NoSep T → DiamondFree T → Conf2122Free T →
      ∃ v, T.graph.degree v = 5 ∧ ∃ P : Pent T.graph v, GammaImages P)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4 :=
  four_color_of_RStarFrame (rStarFrame_of_images H) M

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.rStarFrame_of_no_allDL_orbit
#print axioms SimpleGraph.QuarterFloor.four_color_of_no_allDL_orbit_frame
#print axioms SimpleGraph.QuarterFloor.rStarFrame_of_images
#print axioms SimpleGraph.QuarterFloor.four_color_of_images_frame
