import HDR5All
import COccHR_00
import COccHR_01
import COccHR_02
import COccHR_03
import COccHR_04

/-! # HDR5Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDR5V.hD_i` on `HDR5.hdr5Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDR5.hdr5Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDR5Occ

variable {n : ℕ}

/-- Entry 0, `rsst001_2o122` (ring 7, 4 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HR_00.dEntryOf HDR5V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 7 → Fin n}
    {int : Fin 4 → Fin n} (h : HR_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HR_00.colorable_of_occ_entry HDR5V.hD_0 rfl htri h IH

/-- Entry 1, `rsst004_0o453962` (ring 8, 5 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HR_01.dEntryOf HDR5V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 5 → Fin n} (h : HR_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HR_01.colorable_of_occ_entry HDR5V.hD_1 rfl htri h IH

/-- Entry 2, `rsst006_2o7566` (ring 9, 5 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HR_02.dEntryOf HDR5V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 5 → Fin n} (h : HR_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HR_02.colorable_of_occ_entry HDR5V.hD_2 rfl htri h IH

/-- Entry 3, `rsst024_122o442802` (ring 9, 7 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HR_03.dEntryOf HDR5V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 7 → Fin n} (h : HR_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HR_03.colorable_of_occ_entry HDR5V.hD_3 rfl htri h IH

/-- Entry 4, `rsst026_122o363` (ring 9, 6 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HR_04.dEntryOf HDR5V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 6 → Fin n} (h : HR_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HR_04.colorable_of_occ_entry HDR5V.hD_4 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4]

end HDR5Occ

#print axioms HDR5Occ.dEntry_0
#print axioms HDR5Occ.colorable_0
#print axioms HDR5Occ.dEntry_1
#print axioms HDR5Occ.colorable_1
#print axioms HDR5Occ.dEntry_2
#print axioms HDR5Occ.colorable_2
#print axioms HDR5Occ.dEntry_3
#print axioms HDR5Occ.colorable_3
#print axioms HDR5Occ.dEntry_4
#print axioms HDR5Occ.colorable_4
