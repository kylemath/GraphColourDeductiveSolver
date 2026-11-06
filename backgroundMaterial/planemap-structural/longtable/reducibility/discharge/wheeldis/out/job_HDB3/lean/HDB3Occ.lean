import HDB3All
import COccHB3_00
import COccHB3_01
import COccHB3_02
import COccHB3_03

/-! # HDB3Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDB3V.hD_i` on `HDB3.hdb3Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDB3.hdb3Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDB3Occ

variable {n : ℕ}

/-- Entry 0, `b7_u7577575_.5.5.55` (ring 14, 12 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HB3_00.dEntryOf HDB3V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HB3_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HB3_00.colorable_of_occ_entry HDB3V.hD_0 rfl htri h IH

/-- Entry 1, `b7_u7577575_.555.55` (ring 14, 13 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HB3_01.dEntryOf HDB3V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HB3_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HB3_01.colorable_of_occ_entry HDB3V.hD_1 rfl htri h IH

/-- Entry 2, `b7_u7577575_.565.55` (ring 15, 13 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HB3_02.dEntryOf HDB3V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 13 → Fin n} (h : HB3_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HB3_02.colorable_of_occ_entry HDB3V.hD_2 rfl htri h IH

/-- Entry 3, `b7_u7577575_.5.5755` (ring 15, 13 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HB3_03.dEntryOf HDB3V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 13 → Fin n} (h : HB3_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HB3_03.colorable_of_occ_entry HDB3V.hD_3 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3]

end HDB3Occ

#print axioms HDB3Occ.dEntry_0
#print axioms HDB3Occ.colorable_0
#print axioms HDB3Occ.dEntry_1
#print axioms HDB3Occ.colorable_1
#print axioms HDB3Occ.dEntry_2
#print axioms HDB3Occ.colorable_2
#print axioms HDB3Occ.dEntry_3
#print axioms HDB3Occ.colorable_3
