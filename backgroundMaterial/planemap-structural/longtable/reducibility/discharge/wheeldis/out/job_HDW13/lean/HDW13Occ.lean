import HDW13All
import COccHWD_00
import COccHWD_01
import COccHWD_02
import COccHWD_03
import COccHWD_04
import COccHWD_05
import COccHWD_06
import COccHWD_07
import COccHWD_08
import COccHWD_09
import COccHWD_10
import COccHWD_11
import COccHWD_12
import COccHWD_13
import COccHWD_14
import COccHWD_15
import COccHWD_16
import COccHWD_17
import COccHWD_18
import COccHWD_19
import COccHWD_20
import COccHWD_21
import COccHWD_22
import COccHWD_23
import COccHWD_24
import COccHWD_25
import COccHWD_26

/-! # HDW13Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDW13V.hD_i` on `HDW13.hdw13Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDW13.hdw13Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDW13Occ

variable {n : ℕ}

/-- Entry 0, `b7_u55575.._576....` (ring 11, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HWD_00.dEntryOf HDW13V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HWD_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_00.colorable_of_occ_entry HDW13V.hD_0 rfl htri h IH

/-- Entry 1, `b7_u555755._576....` (ring 11, 10 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HWD_01.dEntryOf HDW13V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_01.colorable_of_occ_entry HDW13V.hD_1 rfl htri h IH

/-- Entry 2, `b7_u55575.._5766...` (ring 12, 10 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HWD_02.dEntryOf HDW13V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_02.colorable_of_occ_entry HDW13V.hD_2 rfl htri h IH

/-- Entry 3, `b7_u555755._5766...` (ring 12, 11 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HWD_03.dEntryOf HDW13V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_03.colorable_of_occ_entry HDW13V.hD_3 rfl htri h IH

/-- Entry 4, `b7_u5557557_576....` (ring 12, 11 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HWD_04.dEntryOf HDW13V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_04.colorable_of_occ_entry HDW13V.hD_4 rfl htri h IH

/-- Entry 5, `b7_u5..5776_5..55.5` (ring 13, 10 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HWD_05.dEntryOf HDW13V.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_05.colorable_of_occ_entry HDW13V.hD_5 rfl htri h IH

/-- Entry 6, `b7_u5556..6_776...6` (ring 13, 10 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HWD_06.dEntryOf HDW13V.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_06.colorable_of_occ_entry HDW13V.hD_6 rfl htri h IH

/-- Entry 7, `b7_u556775._5.55...` (ring 13, 10 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := HWD_07.dEntryOf HDW13V.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_07.colorable_of_occ_entry HDW13V.hD_7 rfl htri h IH

/-- Entry 8, `b7_u557666._56..5..` (ring 13, 10 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := HWD_08.dEntryOf HDW13V.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_08.colorable_of_occ_entry HDW13V.hD_8 rfl htri h IH

/-- Entry 9, `b7_u5556667_75....6` (ring 13, 11 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := HWD_09.dEntryOf HDW13V.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_09.colorable_of_occ_entry HDW13V.hD_9 rfl htri h IH

/-- Entry 10, `b7_u5557557_...676.` (ring 13, 11 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := HWD_10.dEntryOf HDW13V.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_10.colorable_of_occ_entry HDW13V.hD_10 rfl htri h IH

/-- Entry 11, `b7_u556775._5655...` (ring 13, 11 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := HWD_11.dEntryOf HDW13V.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_11.colorable_of_occ_entry HDW13V.hD_11 rfl htri h IH

/-- Entry 12, `b7_u56.5776_5..55.5` (ring 13, 11 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := HWD_12.dEntryOf HDW13V.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_12.colorable_of_occ_entry HDW13V.hD_12 rfl htri h IH

/-- Entry 13, `b7_u555755._57667..` (ring 13, 12 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := HWD_13.dEntryOf HDW13V.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HWD_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_13.colorable_of_occ_entry HDW13V.hD_13 rfl htri h IH

/-- Entry 14, `b7_u5557557_5..676.` (ring 13, 12 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := HWD_14.dEntryOf HDW13V.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HWD_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_14.colorable_of_occ_entry HDW13V.hD_14 rfl htri h IH

/-- Entry 15, `b7_u5557557_576...7` (ring 13, 12 interior vertices). -/
def dEntry_15 : ClaimGlue.DEntry := HWD_15.dEntryOf HDW13V.hD_15 rfl

theorem colorable_15 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HWD_15.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_15.colorable_of_occ_entry HDW13V.hD_15 rfl htri h IH

/-- Entry 16, `b7_u5557557_576..6.` (ring 13, 12 interior vertices). -/
def dEntry_16 : ClaimGlue.DEntry := HWD_16.dEntryOf HDW13V.hD_16 rfl

theorem colorable_16 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HWD_16.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_16.colorable_of_occ_entry HDW13V.hD_16 rfl htri h IH

/-- Entry 17, `b7_u5557557_5766...` (ring 13, 12 interior vertices). -/
def dEntry_17 : ClaimGlue.DEntry := HWD_17.dEntryOf HDW13V.hD_17 rfl

theorem colorable_17 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HWD_17.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_17.colorable_of_occ_entry HDW13V.hD_17 rfl htri h IH

/-- Entry 18, `b7_u5..5777_...5555` (ring 14, 10 interior vertices). -/
def dEntry_18 : ClaimGlue.DEntry := HWD_18.dEntryOf HDW13V.hD_18 rfl

theorem colorable_18 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_18.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_18.colorable_of_occ_entry HDW13V.hD_18 rfl htri h IH

/-- Entry 19, `b7_u5666.67_..5..55` (ring 14, 10 interior vertices). -/
def dEntry_19 : ClaimGlue.DEntry := HWD_19.dEntryOf HDW13V.hD_19 rfl

theorem colorable_19 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HWD_19.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_19.colorable_of_occ_entry HDW13V.hD_19 rfl htri h IH

/-- Entry 20, `b7_u5666677_5....55` (ring 14, 11 interior vertices). -/
def dEntry_20 : ClaimGlue.DEntry := HWD_20.dEntryOf HDW13V.hD_20 rfl

theorem colorable_20 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HWD_20.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_20.colorable_of_occ_entry HDW13V.hD_20 rfl htri h IH

/-- Entry 21, `b7_u5666677_55...55` (ring 14, 12 interior vertices). -/
def dEntry_21 : ClaimGlue.DEntry := HWD_21.dEntryOf HDW13V.hD_21 rfl

theorem colorable_21 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HWD_21.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_21.colorable_of_occ_entry HDW13V.hD_21 rfl htri h IH

/-- Entry 22, `b7_u5557557_5..6767` (ring 14, 13 interior vertices). -/
def dEntry_22 : ClaimGlue.DEntry := HWD_22.dEntryOf HDW13V.hD_22 rfl

theorem colorable_22 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HWD_22.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_22.colorable_of_occ_entry HDW13V.hD_22 rfl htri h IH

/-- Entry 23, `b7_u5557557_57.676.` (ring 14, 13 interior vertices). -/
def dEntry_23 : ClaimGlue.DEntry := HWD_23.dEntryOf HDW13V.hD_23 rfl

theorem colorable_23 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HWD_23.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_23.colorable_of_occ_entry HDW13V.hD_23 rfl htri h IH

/-- Entry 24, `b7_u5557557_5766..7` (ring 14, 13 interior vertices). -/
def dEntry_24 : ClaimGlue.DEntry := HWD_24.dEntryOf HDW13V.hD_24 rfl

theorem colorable_24 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HWD_24.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_24.colorable_of_occ_entry HDW13V.hD_24 rfl htri h IH

/-- Entry 25, `b7_u5557557_57667..` (ring 14, 13 interior vertices). -/
def dEntry_25 : ClaimGlue.DEntry := HWD_25.dEntryOf HDW13V.hD_25 rfl

theorem colorable_25 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HWD_25.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_25.colorable_of_occ_entry HDW13V.hD_25 rfl htri h IH

/-- Entry 26, `b7_u5757677_555..55` (ring 14, 13 interior vertices). -/
def dEntry_26 : ClaimGlue.DEntry := HWD_26.dEntryOf HDW13V.hD_26 rfl

theorem colorable_26 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HWD_26.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HWD_26.colorable_of_occ_entry HDW13V.hD_26 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14, dEntry_15, dEntry_16, dEntry_17, dEntry_18, dEntry_19, dEntry_20, dEntry_21, dEntry_22, dEntry_23, dEntry_24, dEntry_25, dEntry_26]

end HDW13Occ

#print axioms HDW13Occ.dEntry_0
#print axioms HDW13Occ.colorable_0
#print axioms HDW13Occ.dEntry_1
#print axioms HDW13Occ.colorable_1
#print axioms HDW13Occ.dEntry_2
#print axioms HDW13Occ.colorable_2
#print axioms HDW13Occ.dEntry_3
#print axioms HDW13Occ.colorable_3
#print axioms HDW13Occ.dEntry_4
#print axioms HDW13Occ.colorable_4
#print axioms HDW13Occ.dEntry_5
#print axioms HDW13Occ.colorable_5
#print axioms HDW13Occ.dEntry_6
#print axioms HDW13Occ.colorable_6
#print axioms HDW13Occ.dEntry_7
#print axioms HDW13Occ.colorable_7
#print axioms HDW13Occ.dEntry_8
#print axioms HDW13Occ.colorable_8
#print axioms HDW13Occ.dEntry_9
#print axioms HDW13Occ.colorable_9
#print axioms HDW13Occ.dEntry_10
#print axioms HDW13Occ.colorable_10
#print axioms HDW13Occ.dEntry_11
#print axioms HDW13Occ.colorable_11
#print axioms HDW13Occ.dEntry_12
#print axioms HDW13Occ.colorable_12
#print axioms HDW13Occ.dEntry_13
#print axioms HDW13Occ.colorable_13
#print axioms HDW13Occ.dEntry_14
#print axioms HDW13Occ.colorable_14
#print axioms HDW13Occ.dEntry_15
#print axioms HDW13Occ.colorable_15
#print axioms HDW13Occ.dEntry_16
#print axioms HDW13Occ.colorable_16
#print axioms HDW13Occ.dEntry_17
#print axioms HDW13Occ.colorable_17
#print axioms HDW13Occ.dEntry_18
#print axioms HDW13Occ.colorable_18
#print axioms HDW13Occ.dEntry_19
#print axioms HDW13Occ.colorable_19
#print axioms HDW13Occ.dEntry_20
#print axioms HDW13Occ.colorable_20
#print axioms HDW13Occ.dEntry_21
#print axioms HDW13Occ.colorable_21
#print axioms HDW13Occ.dEntry_22
#print axioms HDW13Occ.colorable_22
#print axioms HDW13Occ.dEntry_23
#print axioms HDW13Occ.colorable_23
#print axioms HDW13Occ.dEntry_24
#print axioms HDW13Occ.colorable_24
#print axioms HDW13Occ.dEntry_25
#print axioms HDW13Occ.colorable_25
#print axioms HDW13Occ.dEntry_26
#print axioms HDW13Occ.colorable_26
