import HDK5P16All
import COccHK5P16D_00

/-! # HDK5P16Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK5P16V.hD_i` on `HDK5P16.hdk5p16Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK5P16.hdk5p16Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK5P16Occ

variable {n : ℕ}

/-- Entry 0, `b8_u5565.577_..5..55.` (ring 14, 11 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK5P16D_00.dEntryOf HDK5P16V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK5P16D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK5P16D_00.colorable_of_occ_entry HDK5P16V.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK5P16Occ

#print axioms HDK5P16Occ.dEntry_0
#print axioms HDK5P16Occ.colorable_0
