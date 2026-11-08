import HDK5P01All
import COccHK5P01D_00

/-! # HDK5P01Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK5P01V.hD_i` on `HDK5P01.hdk5p01Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK5P01.hdk5p01Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK5P01Occ

variable {n : ℕ}

/-- Entry 0, `b10_u.556656655_..........` (ring 15, 10 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK5P01D_00.dEntryOf HDK5P01V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 10 → Fin n} (h : HK5P01D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK5P01D_00.colorable_of_occ_entry HDK5P01V.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK5P01Occ

#print axioms HDK5P01Occ.dEntry_0
#print axioms HDK5P01Occ.colorable_0
