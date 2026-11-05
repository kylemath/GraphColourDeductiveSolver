import HD30All
import COccH30_00
import COccH30_01
import COccH30_02
import COccH30_03
import COccH30_04
import COccH30_05
import COccH30_06
import COccH30_07
import COccH30_08
import COccH30_09
import COccH30_10
import COccH30_11
import COccH30_12
import COccH30_13
import COccH30_14
import COccH30_15
import COccH30_16
import COccH30_17
import COccH30_18
import COccH30_19
import COccH30_20
import COccH30_21
import COccH30_22
import COccH30_23
import COccH30_24
import COccH30_25
import COccH30_26
import COccH30_27
import COccH30_28
import COccH30_29

/-! # HD30Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HD30V.hD_i` on `HD30.hd30Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HD30.hd30Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HD30Occ

variable {n : ℕ}

/-- Entry 0, `nl2019_r13` (ring 13, 11 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := H30_00.dEntryOf HD30V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_00.colorable_of_occ_entry HD30V.hD_0 rfl htri h IH

/-- Entry 1, `nl2180_r13` (ring 13, 12 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := H30_01.dEntryOf HD30V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : H30_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_01.colorable_of_occ_entry HD30V.hD_1 rfl htri h IH

/-- Entry 2, `nl5592_r13` (ring 13, 10 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := H30_02.dEntryOf HD30V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_02.colorable_of_occ_entry HD30V.hD_2 rfl htri h IH

/-- Entry 3, `nl7576_r13` (ring 13, 9 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := H30_03.dEntryOf HD30V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : H30_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_03.colorable_of_occ_entry HD30V.hD_3 rfl htri h IH

/-- Entry 4, `nl5589_r13` (ring 13, 10 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := H30_04.dEntryOf HD30V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_04.colorable_of_occ_entry HD30V.hD_4 rfl htri h IH

/-- Entry 5, `nl6424_r13` (ring 13, 11 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := H30_05.dEntryOf HD30V.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_05.colorable_of_occ_entry HD30V.hD_5 rfl htri h IH

/-- Entry 6, `nl7285_r13` (ring 13, 10 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := H30_06.dEntryOf HD30V.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_06.colorable_of_occ_entry HD30V.hD_6 rfl htri h IH

/-- Entry 7, `nl7417_r13` (ring 13, 11 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := H30_07.dEntryOf HD30V.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_07.colorable_of_occ_entry HD30V.hD_7 rfl htri h IH

/-- Entry 8, `nl1745_r13` (ring 13, 9 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := H30_08.dEntryOf HD30V.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : H30_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_08.colorable_of_occ_entry HD30V.hD_8 rfl htri h IH

/-- Entry 9, `nl5506_r13` (ring 13, 10 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := H30_09.dEntryOf HD30V.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_09.colorable_of_occ_entry HD30V.hD_9 rfl htri h IH

/-- Entry 10, `nl3496_r14` (ring 14, 10 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := H30_10.dEntryOf HD30V.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_10.colorable_of_occ_entry HD30V.hD_10 rfl htri h IH

/-- Entry 11, `nl8088_r14` (ring 14, 12 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := H30_11.dEntryOf HD30V.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : H30_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_11.colorable_of_occ_entry HD30V.hD_11 rfl htri h IH

/-- Entry 12, `nl2362_r14` (ring 14, 10 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := H30_12.dEntryOf HD30V.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_12.colorable_of_occ_entry HD30V.hD_12 rfl htri h IH

/-- Entry 13, `nl3474_r14` (ring 14, 10 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := H30_13.dEntryOf HD30V.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : H30_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_13.colorable_of_occ_entry HD30V.hD_13 rfl htri h IH

/-- Entry 14, `nl7805_r14` (ring 14, 11 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := H30_14.dEntryOf HD30V.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_14.colorable_of_occ_entry HD30V.hD_14 rfl htri h IH

/-- Entry 15, `nl2992_r14` (ring 14, 11 interior vertices). -/
def dEntry_15 : ClaimGlue.DEntry := H30_15.dEntryOf HD30V.hD_15 rfl

theorem colorable_15 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_15.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_15.colorable_of_occ_entry HD30V.hD_15 rfl htri h IH

/-- Entry 16, `nl2215_r14` (ring 14, 11 interior vertices). -/
def dEntry_16 : ClaimGlue.DEntry := H30_16.dEntryOf HD30V.hD_16 rfl

theorem colorable_16 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_16.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_16.colorable_of_occ_entry HD30V.hD_16 rfl htri h IH

/-- Entry 17, `nl1094_r14` (ring 14, 11 interior vertices). -/
def dEntry_17 : ClaimGlue.DEntry := H30_17.dEntryOf HD30V.hD_17 rfl

theorem colorable_17 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_17.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_17.colorable_of_occ_entry HD30V.hD_17 rfl htri h IH

/-- Entry 18, `nl6629_r14` (ring 14, 12 interior vertices). -/
def dEntry_18 : ClaimGlue.DEntry := H30_18.dEntryOf HD30V.hD_18 rfl

theorem colorable_18 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : H30_18.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_18.colorable_of_occ_entry HD30V.hD_18 rfl htri h IH

/-- Entry 19, `nl3384_r14` (ring 14, 11 interior vertices). -/
def dEntry_19 : ClaimGlue.DEntry := H30_19.dEntryOf HD30V.hD_19 rfl

theorem colorable_19 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_19.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_19.colorable_of_occ_entry HD30V.hD_19 rfl htri h IH

/-- Entry 20, `nl7221_r15` (ring 15, 13 interior vertices). -/
def dEntry_20 : ClaimGlue.DEntry := H30_20.dEntryOf HD30V.hD_20 rfl

theorem colorable_20 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 13 → Fin n} (h : H30_20.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_20.colorable_of_occ_entry HD30V.hD_20 rfl htri h IH

/-- Entry 21, `nl3832_r15` (ring 15, 12 interior vertices). -/
def dEntry_21 : ClaimGlue.DEntry := H30_21.dEntryOf HD30V.hD_21 rfl

theorem colorable_21 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : H30_21.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_21.colorable_of_occ_entry HD30V.hD_21 rfl htri h IH

/-- Entry 22, `nl1121_r15` (ring 15, 11 interior vertices). -/
def dEntry_22 : ClaimGlue.DEntry := H30_22.dEntryOf HD30V.hD_22 rfl

theorem colorable_22 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_22.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_22.colorable_of_occ_entry HD30V.hD_22 rfl htri h IH

/-- Entry 23, `nl4615_r15` (ring 15, 12 interior vertices). -/
def dEntry_23 : ClaimGlue.DEntry := H30_23.dEntryOf HD30V.hD_23 rfl

theorem colorable_23 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : H30_23.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_23.colorable_of_occ_entry HD30V.hD_23 rfl htri h IH

/-- Entry 24, `nl1502_r15` (ring 15, 12 interior vertices). -/
def dEntry_24 : ClaimGlue.DEntry := H30_24.dEntryOf HD30V.hD_24 rfl

theorem colorable_24 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : H30_24.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_24.colorable_of_occ_entry HD30V.hD_24 rfl htri h IH

/-- Entry 25, `nl6881_r15` (ring 15, 15 interior vertices). -/
def dEntry_25 : ClaimGlue.DEntry := H30_25.dEntryOf HD30V.hD_25 rfl

theorem colorable_25 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 15 → Fin n} (h : H30_25.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_25.colorable_of_occ_entry HD30V.hD_25 rfl htri h IH

/-- Entry 26, `nl6613_r15` (ring 15, 11 interior vertices). -/
def dEntry_26 : ClaimGlue.DEntry := H30_26.dEntryOf HD30V.hD_26 rfl

theorem colorable_26 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_26.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_26.colorable_of_occ_entry HD30V.hD_26 rfl htri h IH

/-- Entry 27, `nl0776_r15` (ring 15, 11 interior vertices). -/
def dEntry_27 : ClaimGlue.DEntry := H30_27.dEntryOf HD30V.hD_27 rfl

theorem colorable_27 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_27.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_27.colorable_of_occ_entry HD30V.hD_27 rfl htri h IH

/-- Entry 28, `nl3781_r15` (ring 15, 11 interior vertices). -/
def dEntry_28 : ClaimGlue.DEntry := H30_28.dEntryOf HD30V.hD_28 rfl

theorem colorable_28 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_28.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_28.colorable_of_occ_entry HD30V.hD_28 rfl htri h IH

/-- Entry 29, `nl2247_r15` (ring 15, 11 interior vertices). -/
def dEntry_29 : ClaimGlue.DEntry := H30_29.dEntryOf HD30V.hD_29 rfl

theorem colorable_29 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : H30_29.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H30_29.colorable_of_occ_entry HD30V.hD_29 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14, dEntry_15, dEntry_16, dEntry_17, dEntry_18, dEntry_19, dEntry_20, dEntry_21, dEntry_22, dEntry_23, dEntry_24, dEntry_25, dEntry_26, dEntry_27, dEntry_28, dEntry_29]

end HD30Occ

#print axioms HD30Occ.dEntry_0
#print axioms HD30Occ.colorable_0
#print axioms HD30Occ.dEntry_1
#print axioms HD30Occ.colorable_1
#print axioms HD30Occ.dEntry_2
#print axioms HD30Occ.colorable_2
#print axioms HD30Occ.dEntry_3
#print axioms HD30Occ.colorable_3
#print axioms HD30Occ.dEntry_4
#print axioms HD30Occ.colorable_4
#print axioms HD30Occ.dEntry_5
#print axioms HD30Occ.colorable_5
#print axioms HD30Occ.dEntry_6
#print axioms HD30Occ.colorable_6
#print axioms HD30Occ.dEntry_7
#print axioms HD30Occ.colorable_7
#print axioms HD30Occ.dEntry_8
#print axioms HD30Occ.colorable_8
#print axioms HD30Occ.dEntry_9
#print axioms HD30Occ.colorable_9
#print axioms HD30Occ.dEntry_10
#print axioms HD30Occ.colorable_10
#print axioms HD30Occ.dEntry_11
#print axioms HD30Occ.colorable_11
#print axioms HD30Occ.dEntry_12
#print axioms HD30Occ.colorable_12
#print axioms HD30Occ.dEntry_13
#print axioms HD30Occ.colorable_13
#print axioms HD30Occ.dEntry_14
#print axioms HD30Occ.colorable_14
#print axioms HD30Occ.dEntry_15
#print axioms HD30Occ.colorable_15
#print axioms HD30Occ.dEntry_16
#print axioms HD30Occ.colorable_16
#print axioms HD30Occ.dEntry_17
#print axioms HD30Occ.colorable_17
#print axioms HD30Occ.dEntry_18
#print axioms HD30Occ.colorable_18
#print axioms HD30Occ.dEntry_19
#print axioms HD30Occ.colorable_19
#print axioms HD30Occ.dEntry_20
#print axioms HD30Occ.colorable_20
#print axioms HD30Occ.dEntry_21
#print axioms HD30Occ.colorable_21
#print axioms HD30Occ.dEntry_22
#print axioms HD30Occ.colorable_22
#print axioms HD30Occ.dEntry_23
#print axioms HD30Occ.colorable_23
#print axioms HD30Occ.dEntry_24
#print axioms HD30Occ.colorable_24
#print axioms HD30Occ.dEntry_25
#print axioms HD30Occ.colorable_25
#print axioms HD30Occ.dEntry_26
#print axioms HD30Occ.colorable_26
#print axioms HD30Occ.dEntry_27
#print axioms HD30Occ.colorable_27
#print axioms HD30Occ.dEntry_28
#print axioms HD30Occ.colorable_28
#print axioms HD30Occ.dEntry_29
#print axioms HD30Occ.colorable_29
