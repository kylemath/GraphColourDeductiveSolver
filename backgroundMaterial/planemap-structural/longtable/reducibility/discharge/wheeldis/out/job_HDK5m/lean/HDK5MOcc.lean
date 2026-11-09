import HDK5MAll
import COccHK5MD_00

/-! # HDK5MOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK5MV.hD_i` on `HDK5M.hdk5mConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK5M.hdk5mConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK5MOcc

variable {n : ℕ}

/-- Entry 0, `b9_u555665..._....55...` (ring 12, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK5MD_00.dEntryOf HDK5MV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HK5MD_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK5MD_00.colorable_of_occ_entry HDK5MV.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK5MOcc

#print axioms HDK5MOcc.dEntry_0
#print axioms HDK5MOcc.colorable_0
