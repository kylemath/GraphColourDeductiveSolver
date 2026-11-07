import HDK3All
import COccHK3D_00
import COccHK3D_01
import COccHK3D_02
import COccHK3D_03
import COccHK3D_04
import COccHK3D_05

/-! # HDK3Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK3V.hD_i` on `HDK3.hdk3Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK3.hdk3Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK3Occ

variable {n : ℕ}

/-- Entry 0, `b8_u.56.5656_56...55.` (ring 13, 11 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK3D_00.dEntryOf HDK3V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3D_00.colorable_of_occ_entry HDK3V.hD_0 rfl htri h IH

/-- Entry 1, `b9_u...575655_...5..65.` (ring 13, 10 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HK3D_01.dEntryOf HDK3V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3D_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3D_01.colorable_of_occ_entry HDK3V.hD_1 rfl htri h IH

/-- Entry 2, `b8_u.56656.._..566...` (ring 13, 9 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HK3D_02.dEntryOf HDK3V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HK3D_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3D_02.colorable_of_occ_entry HDK3V.hD_2 rfl htri h IH

/-- Entry 3, `b8_u.56.5556_56....5.` (ring 13, 10 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HK3D_03.dEntryOf HDK3V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3D_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3D_03.colorable_of_occ_entry HDK3V.hD_3 rfl htri h IH

/-- Entry 4, `b8_u.56.5756_.5..555.` (ring 13, 11 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HK3D_04.dEntryOf HDK3V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3D_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3D_04.colorable_of_occ_entry HDK3V.hD_4 rfl htri h IH

/-- Entry 5, `b9_u75..65656_5...55...` (ring 14, 11 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HK3D_05.dEntryOf HDK3V.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3D_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3D_05.colorable_of_occ_entry HDK3V.hD_5 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5]

end HDK3Occ

#print axioms HDK3Occ.dEntry_0
#print axioms HDK3Occ.colorable_0
#print axioms HDK3Occ.dEntry_1
#print axioms HDK3Occ.colorable_1
#print axioms HDK3Occ.dEntry_2
#print axioms HDK3Occ.colorable_2
#print axioms HDK3Occ.dEntry_3
#print axioms HDK3Occ.colorable_3
#print axioms HDK3Occ.dEntry_4
#print axioms HDK3Occ.colorable_4
#print axioms HDK3Occ.dEntry_5
#print axioms HDK3Occ.colorable_5
