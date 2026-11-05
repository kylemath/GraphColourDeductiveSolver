import HDK7All
import COccHQ_00
import COccHQ_01
import COccHQ_02
import COccHQ_03
import COccHQ_04
import COccHQ_05
import COccHQ_06

/-! # HDK7Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK7V.hD_i` on `HDK7.hdk7Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK7.hdk7Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK7Occ

variable {n : ℕ}

/-- Entry 0, `b7_u...5566_...576._p516` (ring 12, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HQ_00.dEntryOf HDK7V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HQ_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_00.colorable_of_occ_entry HDK7V.hD_0 rfl htri h IH

/-- Entry 1, `b7_u65...65_6....67_p015` (ring 12, 9 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HQ_01.dEntryOf HDK7V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HQ_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_01.colorable_of_occ_entry HDK7V.hD_1 rfl htri h IH

/-- Entry 2, `b7_u5656..._576...5_p116` (ring 12, 10 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HQ_02.dEntryOf HDK7V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HQ_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_02.colorable_of_occ_entry HDK7V.hD_2 rfl htri h IH

/-- Entry 3, `b7_u5656..._576...._p116` (ring 12, 9 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HQ_03.dEntryOf HDK7V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HQ_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_03.colorable_of_occ_entry HDK7V.hD_3 rfl htri h IH

/-- Entry 4, `b7_u...5566_...5765_p516` (ring 13, 10 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HQ_04.dEntryOf HDK7V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HQ_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_04.colorable_of_occ_entry HDK7V.hD_4 rfl htri h IH

/-- Entry 5, `b7_u56656.._..76..._p215` (ring 13, 9 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HQ_05.dEntryOf HDK7V.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HQ_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_05.colorable_of_occ_entry HDK7V.hD_5 rfl htri h IH

/-- Entry 6, `b7_u65...65_6....67_p016` (ring 13, 9 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HQ_06.dEntryOf HDK7V.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HQ_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HQ_06.colorable_of_occ_entry HDK7V.hD_6 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6]

end HDK7Occ

#print axioms HDK7Occ.dEntry_0
#print axioms HDK7Occ.colorable_0
#print axioms HDK7Occ.dEntry_1
#print axioms HDK7Occ.colorable_1
#print axioms HDK7Occ.dEntry_2
#print axioms HDK7Occ.colorable_2
#print axioms HDK7Occ.dEntry_3
#print axioms HDK7Occ.colorable_3
#print axioms HDK7Occ.dEntry_4
#print axioms HDK7Occ.colorable_4
#print axioms HDK7Occ.dEntry_5
#print axioms HDK7Occ.colorable_5
#print axioms HDK7Occ.dEntry_6
#print axioms HDK7Occ.colorable_6
