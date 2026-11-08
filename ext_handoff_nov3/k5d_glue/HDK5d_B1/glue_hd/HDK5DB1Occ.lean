import HDK5DB1All
import COccHK5DB1D_00

/-! # HDK5DB1Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK5DB1V.hD_i` on `HDK5DB1.hdk5db1Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK5DB1.hdk5db1Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK5DB1Occ

variable {n : ℕ}

/-- Entry 0, `b9_u555557667_5..56...6` (ring 15, 14 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK5DB1D_00.dEntryOf HDK5DB1V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 14 → Fin n} (h : HK5DB1D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK5DB1D_00.colorable_of_occ_entry HDK5DB1V.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK5DB1Occ

#print axioms HDK5DB1Occ.dEntry_0
#print axioms HDK5DB1Occ.colorable_0
