import HDK5CV5All
import COccHK5CV5D_00

/-! # HDK5CV5Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK5CV5V.hD_i` on `HDK5CV5.hdk5cv5Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK5CV5.hdk5cv5Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK5CV5Occ

variable {n : ℕ}

/-- Entry 0, `b7_u55775.._66.5...` (ring 13, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK5CV5D_00.dEntryOf HDK5CV5V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HK5CV5D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK5CV5D_00.colorable_of_occ_entry HDK5CV5V.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK5CV5Occ

#print axioms HDK5CV5Occ.dEntry_0
#print axioms HDK5CV5Occ.colorable_0
