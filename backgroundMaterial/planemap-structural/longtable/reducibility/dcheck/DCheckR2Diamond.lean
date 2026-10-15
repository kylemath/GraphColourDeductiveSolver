import Mathlib.Combinatorics.SimpleGraph.PlaneMap.DiamondMOcc
import DCheckR2D

/-! Job 19 end-to-end check: the Birkhoff diamond (orientation −1) reduced through the DCheck chain
(`dReducible` → `colorable_of_dReducible`) instead of the generated certificate `DiamondMCert`.
The `Conf` below is the diamond's free-completion tables (`DiamondM.ringList`/`intList`). -/

namespace DCheck.R2.DiamondE2E
open SimpleGraph SimpleGraph.SphericalMap VacancySlide

/-- The diamond as a DCheck configuration (ring 6, 4 interior vertices). -/
def cfD : Conf where
  name := "diamond"
  r := 6
  m := 4
  ringAdj := #[#[0, 1], #[1, 2, 3], #[3, 4], #[0, 4, 5]]
  intAdj := #[#[1, 2, 3], #[0, 2], #[0, 1, 3], #[0, 2]]

/-- `run` uses a `while` loop (`Lean.Loop`), which the kernel cannot unfold, so this is evaluated by
`native_decide`, as for the other DCheck certificates. -/
theorem cfD_dReducible : dReducible cfD = true := by native_decide

theorem intAdjOf_cfD : intAdjOf cfD = DiamondM.intAdj := by
  funext a b
  change Fin 4 at a b
  fin_cases a <;> fin_cases b <;> simp [intAdjOf, cfD, DiamondM.intAdj, DiamondM.intList]

theorem ringAdjOf_cfD : ringAdjOf cfD = DiamondM.ringAdj := by
  funext a t
  change Fin 4 at a
  fin_cases a <;> simp [ringAdjOf, cfD, DiamondM.ringAdj, DiamondM.ringList]

theorem cfD_sym : ∀ a b, intAdjOf cfD a b = true → intAdjOf cfD b a = true := by
  rw [intAdjOf_cfD]; unfold DiamondM.intAdj DiamondM.intList; decide
theorem cfD_loop : ∀ a, intAdjOf cfD a a = false := by
  rw [intAdjOf_cfD]; unfold DiamondM.intAdj DiamondM.intList; decide

/-- **End to end.** A triangulation containing the diamond (orientation −1) is 4-colourable when
every smaller spherical map is; the reduction step is `colorable_of_dReducible`. -/
theorem colorable_of_occ {n : ℕ} {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 6 → Fin n}
    {int : Fin 4 → Fin n} (h : DiamondM.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨G, O, hlt⟩ := DiamondM.configOcc htri h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  rw [← intAdjOf_cfD, ← ringAdjOf_cfD] at O
  exact ConfigOcc.colorable_of_dReducible (T := T) (G := G) cfD cfD_dReducible (by decide) (by decide)
    cfD_sym cfD_loop O (c := cG) (fun x y e _ _ => cG.valid e)

end DCheck.R2.DiamondE2E

#print axioms DCheck.R2.DiamondE2E.colorable_of_occ
