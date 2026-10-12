module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.DiamondAppears
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.C2122Appears
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarSanity

/-!
# The frame stated with appearances

`RStarFrameApp` asks R\* for connected triangulations of minimum degree five with no separating
triangle, in which every appearance of the Birkhoff diamond or of RSST 2.122 has unclean tips:
the two tips share a neighbour other than the centres.

That condition gives a separating 4-cycle `x – tip – centre – tip`. So under "no separating
4-cycle" (F2) the class is exactly the RSST class: no appearance at all.
`rStarFrame_of_app` shows `RStarFrameApp → RStarFrame`, so `RStarFrameApp` implies the Four Colour
Theorem.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap

variable {n : ℕ}

/-- Every appearance of the diamond and of 2.122 has unclean tips. -/
def AppearFree (T : SphericalMap n) : Prop :=
  (∀ int, Appears ![5, 5, 5, 5] T int → ¬ TipsClean T int) ∧
  (∀ int, Appears ![6, 5, 5, 5] T int → ¬ TipsClean T int)

/-- R\* for the appearance form of the frame class. -/
def RStarFrameApp : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) → NoSep T → AppearFree T →
    ∃ v, T.graph.degree v = 5 ∧ PureClean T v

/-- An appearance with clean tips is an occurrence, so occurrence-free maps are appearance-free. -/
theorem appearFree_of_free {T : SphericalMap n} (htri : T.Triangulated) (hns : NoSep T)
    (hD : DiamondFree T) (hC : Conf2122Free T) : AppearFree T := by
  refine ⟨fun int A htip => ?_, fun int A htip => ?_⟩
  · rcases DiamondAppears.occ_of_appears htri hns A htip with ⟨r, h⟩ | ⟨r, h⟩
    · exact hD.1 ⟨r, int, h⟩
    · exact hD.2 ⟨r, int, h⟩
  · rcases C2122Appears.occ_of_appears htri hns A htip with ⟨r, h⟩ | ⟨r, h⟩
    · exact hC.1 ⟨r, int, h⟩
    · exact hC.2 ⟨r, int, h⟩

theorem rStarFrame_of_app (hR : RStarFrameApp) : RStarFrame :=
  fun m T hm hconn htri hdeg hns hD hC =>
    hR m T hm hconn htri hdeg hns (appearFree_of_free htri hns hD hC)

/-- **R\* for the appearance form of the frame class implies the Four Colour Theorem.** -/
theorem four_color_of_RStarFrameApp (hR : RStarFrameApp) {n : ℕ} (M : SphericalMap n) :
    M.graph.Colorable 4 :=
  four_color_of_RStarFrame (rStarFrame_of_app hR) M

end SimpleGraph.SphericalMap

namespace SimpleGraph.Icosahedron
open SphericalMap

/-- The diamond appears in the icosahedron with clean tips (sanity check of `Appears`). -/
theorem appears_diamond : Appears ![5, 5, 5, 5] sphericalMap ![0, 1, 8, 7] ∧
    TipsClean sphericalMap ![0, 1, 8, 7] := by
  refine ⟨⟨by decide, show graph.Adj 0 1 by decide, show graph.Adj 0 8 by decide,
    show graph.Adj 0 7 by decide, show graph.Adj 1 8 by decide, show graph.Adj 8 7 by decide,
    show ¬ graph.Adj 1 7 by decide, fun a => by rw [sphericalMap_degree]; revert a; decide⟩, ?_⟩
  have h : ∀ x : Fin 12, graph.Adj 1 x → graph.Adj 7 x → x = 0 ∨ x = 8 := by decide
  exact h

end SimpleGraph.Icosahedron
