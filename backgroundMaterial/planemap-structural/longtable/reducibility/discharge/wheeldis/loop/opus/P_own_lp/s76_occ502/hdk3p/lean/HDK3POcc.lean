import HDK3PAll
import COccHK3P_00
import COccHK3P_01

/-! # HDK3POcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK3PV.hD_i` on `HDK3P.hdk3pConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK3P.hdk3pConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK3POcc

variable {n : ℕ}

/-- Entry 0, `q7-_....556_....56._::::::5` (ring 8, 6 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK3P_00.dEntryOf HDK3PV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 6 → Fin n} (h : HK3P_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3P_00.colorable_of_occ_entry HDK3PV.hD_0 rfl htri h IH

/-- Entry 1, `q7-_....556_....56._::::::5_s5/p6L1=5` (ring 8, 7 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HK3P_01.dEntryOf HDK3PV.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 7 → Fin n} (h : HK3P_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3P_01.colorable_of_occ_entry HDK3PV.hD_1 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1]

end HDK3POcc

#print axioms HDK3POcc.dEntry_0
#print axioms HDK3POcc.colorable_0
#print axioms HDK3POcc.dEntry_1
#print axioms HDK3POcc.colorable_1
