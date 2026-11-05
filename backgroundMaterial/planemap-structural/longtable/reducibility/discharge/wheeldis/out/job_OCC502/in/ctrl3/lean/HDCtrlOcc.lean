import HDCtrlAll
import COccHK_00
import COccHK_01
import COccHK_02

/-! # HDCtrlOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDCtrlV.hD_i` on `HDCtrl.hdcConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDCtrl.hdcConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDCtrlOcc

variable {n : ℕ}

/-- Entry 0, `rsst008_3o460806` (ring 10, 7 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK_00.dEntryOf HDCtrlV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : HK_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK_00.colorable_of_occ_entry HDCtrlV.hD_0 rfl htri h IH

/-- Entry 1, `rsst009_3o1306806` (ring 10, 7 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HK_01.dEntryOf HDCtrlV.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : HK_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK_01.colorable_of_occ_entry HDCtrlV.hD_1 rfl htri h IH

/-- Entry 2, `rsst012_2o22086` (ring 10, 6 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HK_02.dEntryOf HDCtrlV.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 6 → Fin n} (h : HK_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK_02.colorable_of_occ_entry HDCtrlV.hD_2 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2]

end HDCtrlOcc

#print axioms HDCtrlOcc.dEntry_0
#print axioms HDCtrlOcc.colorable_0
#print axioms HDCtrlOcc.dEntry_1
#print axioms HDCtrlOcc.colorable_1
#print axioms HDCtrlOcc.dEntry_2
#print axioms HDCtrlOcc.colorable_2
