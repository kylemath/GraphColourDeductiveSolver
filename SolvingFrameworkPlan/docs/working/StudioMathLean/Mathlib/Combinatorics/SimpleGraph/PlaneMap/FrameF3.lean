module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.DiamondMOcc
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.DiamondPOcc
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.C2122MOcc
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.C2122POcc

/-!
# The minimal-counterexample frame with the Birkhoff diamond and RSST 2.122 excluded

`RStarFrame`: every connected spherical triangulation of minimum degree five, with no separating
triangle, that is `Occ`-free (no `Occ` of the Birkhoff diamond or of RSST 2.122, in either
orientation) has a pure-clean vertex of degree five.

`four_color_of_RStarFrame`: `RStarFrame` implies that every spherical map is four-colourable.
The separating triangle is reduced by gluing (F1); each configuration occurrence is reduced by its
compiled D-reducibility certificate (F3); otherwise the pure-clean vertex is coloured last (F4).

An occurrence is the audit's rotation-based `Occurs` (2026-10-06 15:20, §2): injective ring,
injective interior, disjoint, free-completion degrees and rotations at the interior vertices; ring
chords allowed. Passing from the RSST notion "appears" (induced, faces, degrees) to an occurrence
with a distinct ring is not formalised here.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill

variable {n : ℕ}

/-- `Occ`-free for the Birkhoff diamond: no `Occ`, in either orientation. -/
def DiamondFree (T : SphericalMap n) : Prop :=
  (¬ ∃ ring int, DiamondM.Occ T ring int) ∧ (¬ ∃ ring int, DiamondP.Occ T ring int)

/-- `Occ`-free for RSST 2.122: no `Occ`, in either orientation. -/
def Conf2122Free (T : SphericalMap n) : Prop :=
  (¬ ∃ ring int, C2122M.Occ T ring int) ∧ (¬ ∃ ring int, C2122P.Occ T ring int)

/-- R\* for the frame class. -/
def RStarFrame : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) → NoSep T → DiamondFree T → Conf2122Free T →
    ∃ v, T.graph.degree v = 5 ∧ PureClean T v

/-- **R\* for `Occ`-free triangulations (diamond and 2.122, both orientations) with no separating
triangle implies the Four Colour Theorem.** -/
theorem four_color_of_RStarFrame (hR : RStarFrame) {n : ℕ} (M : SphericalMap n) :
    M.graph.Colorable 4 := by
  refine four_color_of_smaller_gate (fun m T hm hconn htri hdeg IH => ?_) M
  classical
  by_cases hns : NoSep T
  · by_cases h1 : ∃ ring int, DiamondM.Occ T ring int
    · obtain ⟨ring, int, h⟩ := h1; exact DiamondM.colorable_of_occ htri h IH
    by_cases h2 : ∃ ring int, DiamondP.Occ T ring int
    · obtain ⟨ring, int, h⟩ := h2; exact DiamondP.colorable_of_occ htri h IH
    by_cases h3 : ∃ ring int, C2122M.Occ T ring int
    · obtain ⟨ring, int, h⟩ := h3; exact C2122M.colorable_of_occ htri h IH
    by_cases h4 : ∃ ring int, C2122P.Occ T ring int
    · obtain ⟨ring, int, h⟩ := h4; exact C2122P.colorable_of_occ htri h IH
    obtain ⟨v, hv5, hpc⟩ := hR m T hm hconn htri hdeg hns ⟨h1, h2⟩ ⟨h3, h4⟩
    apply extend_of_pureClean T v hpc
    have hvs : v ∈ T.graph.support := (T.graph.degree_pos_iff_mem_support v).mp (by omega)
    obtain ⟨N, hN, _⟩ := T.isolate_closed v (by omega)
    obtain ⟨cN⟩ := IH m N (by rw [hN]; exact T.isolate_support_card_lt v hvs)
    exact ⟨SimpleGraph.Coloring.mk (fun z => cN z.val) (fun {u w} huw =>
      cN.valid (by rw [hN]; exact ⟨huw, u.property, w.property⟩))⟩
  · simp only [NoSep, not_forall] at hns
    obtain ⟨x, y, z, hxy, hyz, hzx, hnf⟩ := hns
    exact colorable_of_separating_triangle htri hxy hyz hzx hnf IH

/-- The frame hypothesis is weaker than the earlier one. -/
theorem rStarFrame_of_noSepTri (hR : RStarNoSepTri) : RStarFrame :=
  fun m T hm hconn htri hdeg hns _ _ => hR m T hm hconn htri hdeg hns

end SimpleGraph.SphericalMap
