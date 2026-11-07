import HDW18NAll
import COccHWN_00
import COccHWN_01
import COccHWN_02
import COccHWN_03
import COccHWN_04
import COccHWN_05
import COccHWN_06
import COccHWN_07
import COccHWN_08
import COccHWN_09
import COccHWN_10
import COccHWN_11
import COccHWN_12
import COccHWN_13
import COccHWN_14

/-! # HDW18NOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDW18NV.hD_i` on `HDW18N.hdw18nConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDW18N.hdw18nConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDW18NOcc

variable {n : ℕ}

/-- Entry 0, `nl0065_r10` (ring 10, 7 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HWN_00.dEntryOf HDW18NV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : HWN_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_00.colorable_of_occ_entry HDW18NV.hD_0 rfl htri h IH

/-- Entry 1, `nl0181_r12` (ring 12, 9 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HWN_01.dEntryOf HDW18NV.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HWN_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_01.colorable_of_occ_entry HDW18NV.hD_1 rfl htri h IH

/-- Entry 2, `nl0258_r13` (ring 13, 9 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HWN_02.dEntryOf HDW18NV.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HWN_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_02.colorable_of_occ_entry HDW18NV.hD_2 rfl htri h IH

/-- Entry 3, `nl0319_r12` (ring 12, 8 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HWN_03.dEntryOf HDW18NV.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : HWN_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_03.colorable_of_occ_entry HDW18NV.hD_3 rfl htri h IH

/-- Entry 4, `nl0510_r13` (ring 13, 9 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HWN_04.dEntryOf HDW18NV.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HWN_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_04.colorable_of_occ_entry HDW18NV.hD_4 rfl htri h IH

/-- Entry 5, `nl0826_r13` (ring 13, 9 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HWN_05.dEntryOf HDW18NV.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HWN_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_05.colorable_of_occ_entry HDW18NV.hD_5 rfl htri h IH

/-- Entry 6, `nl1756_r13` (ring 13, 10 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HWN_06.dEntryOf HDW18NV.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HWN_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_06.colorable_of_occ_entry HDW18NV.hD_6 rfl htri h IH

/-- Entry 7, `nl2873_r12` (ring 12, 9 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := HWN_07.dEntryOf HDW18NV.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HWN_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_07.colorable_of_occ_entry HDW18NV.hD_7 rfl htri h IH

/-- Entry 8, `nl2880_r12` (ring 12, 9 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := HWN_08.dEntryOf HDW18NV.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HWN_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_08.colorable_of_occ_entry HDW18NV.hD_8 rfl htri h IH

/-- Entry 9, `nl2987_r14` (ring 14, 11 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := HWN_09.dEntryOf HDW18NV.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HWN_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_09.colorable_of_occ_entry HDW18NV.hD_9 rfl htri h IH

/-- Entry 10, `nl2998_r14` (ring 14, 11 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := HWN_10.dEntryOf HDW18NV.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HWN_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_10.colorable_of_occ_entry HDW18NV.hD_10 rfl htri h IH

/-- Entry 11, `nl3687_r14` (ring 14, 10 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := HWN_11.dEntryOf HDW18NV.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HWN_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_11.colorable_of_occ_entry HDW18NV.hD_11 rfl htri h IH

/-- Entry 12, `nl5277_r13` (ring 13, 10 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := HWN_12.dEntryOf HDW18NV.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HWN_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_12.colorable_of_occ_entry HDW18NV.hD_12 rfl htri h IH

/-- Entry 13, `nl6028_r14` (ring 14, 10 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := HWN_13.dEntryOf HDW18NV.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HWN_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_13.colorable_of_occ_entry HDW18NV.hD_13 rfl htri h IH

/-- Entry 14, `nl6417_r14` (ring 14, 10 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := HWN_14.dEntryOf HDW18NV.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HWN_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWN_14.colorable_of_occ_entry HDW18NV.hD_14 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14]

end HDW18NOcc

#print axioms HDW18NOcc.dEntry_0
#print axioms HDW18NOcc.colorable_0
#print axioms HDW18NOcc.dEntry_1
#print axioms HDW18NOcc.colorable_1
#print axioms HDW18NOcc.dEntry_2
#print axioms HDW18NOcc.colorable_2
#print axioms HDW18NOcc.dEntry_3
#print axioms HDW18NOcc.colorable_3
#print axioms HDW18NOcc.dEntry_4
#print axioms HDW18NOcc.colorable_4
#print axioms HDW18NOcc.dEntry_5
#print axioms HDW18NOcc.colorable_5
#print axioms HDW18NOcc.dEntry_6
#print axioms HDW18NOcc.colorable_6
#print axioms HDW18NOcc.dEntry_7
#print axioms HDW18NOcc.colorable_7
#print axioms HDW18NOcc.dEntry_8
#print axioms HDW18NOcc.colorable_8
#print axioms HDW18NOcc.dEntry_9
#print axioms HDW18NOcc.colorable_9
#print axioms HDW18NOcc.dEntry_10
#print axioms HDW18NOcc.colorable_10
#print axioms HDW18NOcc.dEntry_11
#print axioms HDW18NOcc.colorable_11
#print axioms HDW18NOcc.dEntry_12
#print axioms HDW18NOcc.colorable_12
#print axioms HDW18NOcc.dEntry_13
#print axioms HDW18NOcc.colorable_13
#print axioms HDW18NOcc.dEntry_14
#print axioms HDW18NOcc.colorable_14
