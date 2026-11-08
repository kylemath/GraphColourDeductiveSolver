import HDOF7All
import COccHOF7_00
import COccHOF7_01
import COccHOF7_02
import COccHOF7_03
import COccHOF7_04
import COccHOF7_05
import COccHOF7_06
import COccHOF7_07
import COccHOF7_08
import COccHOF7_09
import COccHOF7_10
import COccHOF7_11
import COccHOF7_12
import COccHOF7_13
import COccHOF7_14
import COccHOF7_15
import COccHOF7_16
import COccHOF7_17
import COccHOF7_18
import COccHOF7_19
import COccHOF7_20
import COccHOF7_21
import COccHOF7_22
import COccHOF7_23
import COccHOF7_24
import COccHOF7_25
import COccHOF7_26
import COccHOF7_27
import COccHOF7_28
import COccHOF7_29
import COccHOF7_30
import COccHOF7_31
import COccHOF7_32
import COccHOF7_33
import COccHOF7_34
import COccHOF7_35
import COccHOF7_36
import COccHOF7_37
import COccHOF7_38
import COccHOF7_39
import COccHOF7_40
import COccHOF7_41
import COccHOF7_42
import COccHOF7_43
import COccHOF7_44
import COccHOF7_45
import COccHOF7_46
import COccHOF7_47
import COccHOF7_48
import COccHOF7_49
import COccHOF7_50
import COccHOF7_51
import COccHOF7_52
import COccHOF7_53
import COccHOF7_54
import COccHOF7_55
import COccHOF7_56
import COccHOF7_57
import COccHOF7_58
import COccHOF7_59
import COccHOF7_60
import COccHOF7_61
import COccHOF7_62
import COccHOF7_63
import COccHOF7_64

/-! # HDOF7Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDOF7V.hD_i` on `HDOF7.hdof7Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDOF7.hdof7Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDOF7Occ

variable {n : ℕ}

/-- Entry 0, `f8_...55755_...56B5.` (ring 11, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HOF7_00.dEntryOf HDOF7V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_00.colorable_of_occ_entry HDOF7V.hD_0 rfl htri h IH

/-- Entry 1, `f8_...55755_...5675.` (ring 12, 10 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HOF7_01.dEntryOf HDOF7V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_01.colorable_of_occ_entry HDOF7V.hD_1 rfl htri h IH

/-- Entry 2, `f8_...55755_...56B6.` (ring 12, 9 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HOF7_02.dEntryOf HDOF7V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_02.colorable_of_occ_entry HDOF7V.hD_2 rfl htri h IH

/-- Entry 3, `f8_...55755_...5766.` (ring 13, 10 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HOF7_03.dEntryOf HDOF7V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_03.colorable_of_occ_entry HDOF7V.hD_3 rfl htri h IH

/-- Entry 4, `f7_..55755_..5B66.` (ring 11, 9 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HOF7_04.dEntryOf HDOF7V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_04.colorable_of_occ_entry HDOF7V.hD_4 rfl htri h IH

/-- Entry 5, `f7_..55755_..5657.` (ring 11, 10 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HOF7_05.dEntryOf HDOF7V.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_05.colorable_of_occ_entry HDOF7V.hD_5 rfl htri h IH

/-- Entry 6, `f8_...55755_...5667.` (ring 13, 10 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HOF7_06.dEntryOf HDOF7V.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_06.colorable_of_occ_entry HDOF7V.hD_6 rfl htri h IH

/-- Entry 7, `f7_..55755_..56BB.` (ring 10, 8 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := HOF7_07.dEntryOf HDOF7V.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_07.colorable_of_occ_entry HDOF7V.hD_7 rfl htri h IH

/-- Entry 8, `f7_..55755_..565B.` (ring 10, 9 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := HOF7_08.dEntryOf HDOF7V.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_08.colorable_of_occ_entry HDOF7V.hD_8 rfl htri h IH

/-- Entry 9, `f7_..55755_..575B.` (ring 11, 9 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := HOF7_09.dEntryOf HDOF7V.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_09.colorable_of_occ_entry HDOF7V.hD_9 rfl htri h IH

/-- Entry 10, `f8_...55755_...566B.` (ring 12, 9 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := HOF7_10.dEntryOf HDOF7V.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_10.colorable_of_occ_entry HDOF7V.hD_10 rfl htri h IH

/-- Entry 11, `f8_...55756_...5665.` (ring 12, 10 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := HOF7_11.dEntryOf HDOF7V.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_11.colorable_of_occ_entry HDOF7V.hD_11 rfl htri h IH

/-- Entry 12, `f8_...55756_...5675.` (ring 13, 10 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := HOF7_12.dEntryOf HDOF7V.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_12.colorable_of_occ_entry HDOF7V.hD_12 rfl htri h IH

/-- Entry 13, `f7_..55756_..5766.` (ring 13, 10 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := HOF7_13.dEntryOf HDOF7V.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_13.colorable_of_occ_entry HDOF7V.hD_13 rfl htri h IH

/-- Entry 14, `f8_...55756_...5756.` (ring 13, 10 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := HOF7_14.dEntryOf HDOF7V.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_14.colorable_of_occ_entry HDOF7V.hD_14 rfl htri h IH

/-- Entry 15, `f8_...55756_...5B56.` (ring 12, 9 interior vertices). -/
def dEntry_15 : ClaimGlue.DEntry := HOF7_15.dEntryOf HDOF7V.hD_15 rfl

theorem colorable_15 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_15.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_15.colorable_of_occ_entry HDOF7V.hD_15 rfl htri h IH

/-- Entry 16, `f7_..55755_..665B.` (ring 11, 9 interior vertices). -/
def dEntry_16 : ClaimGlue.DEntry := HOF7_16.dEntryOf HDOF7V.hD_16 rfl

theorem colorable_16 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_16.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_16.colorable_of_occ_entry HDOF7V.hD_16 rfl htri h IH

/-- Entry 17, `f7_..55756_..565B.` (ring 11, 9 interior vertices). -/
def dEntry_17 : ClaimGlue.DEntry := HOF7_17.dEntryOf HDOF7V.hD_17 rfl

theorem colorable_17 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_17.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_17.colorable_of_occ_entry HDOF7V.hD_17 rfl htri h IH

/-- Entry 18, `f7_..55757_..5655.` (ring 11, 10 interior vertices). -/
def dEntry_18 : ClaimGlue.DEntry := HOF7_18.dEntryOf HDOF7V.hD_18 rfl

theorem colorable_18 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_18.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_18.colorable_of_occ_entry HDOF7V.hD_18 rfl htri h IH

/-- Entry 19, `f7_..55755_..B55B.` (ring 10, 8 interior vertices). -/
def dEntry_19 : ClaimGlue.DEntry := HOF7_19.dEntryOf HDOF7V.hD_19 rfl

theorem colorable_19 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_19.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_19.colorable_of_occ_entry HDOF7V.hD_19 rfl htri h IH

/-- Entry 20, `f8_...55756_...6B65.` (ring 13, 9 interior vertices). -/
def dEntry_20 : ClaimGlue.DEntry := HOF7_20.dEntryOf HDOF7V.hD_20 rfl

theorem colorable_20 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_20.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_20.colorable_of_occ_entry HDOF7V.hD_20 rfl htri h IH

/-- Entry 21, `f8_...55756_...6665.` (ring 13, 10 interior vertices). -/
def dEntry_21 : ClaimGlue.DEntry := HOF7_21.dEntryOf HDOF7V.hD_21 rfl

theorem colorable_21 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_21.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_21.colorable_of_occ_entry HDOF7V.hD_21 rfl htri h IH

/-- Entry 22, `f8_...55756_...6765.` (ring 14, 10 interior vertices). -/
def dEntry_22 : ClaimGlue.DEntry := HOF7_22.dEntryOf HDOF7V.hD_22 rfl

theorem colorable_22 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_22.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_22.colorable_of_occ_entry HDOF7V.hD_22 rfl htri h IH

/-- Entry 23, `f8_...55756_...B565.` (ring 12, 9 interior vertices). -/
def dEntry_23 : ClaimGlue.DEntry := HOF7_23.dEntryOf HDOF7V.hD_23 rfl

theorem colorable_23 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_23.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_23.colorable_of_occ_entry HDOF7V.hD_23 rfl htri h IH

/-- Entry 24, `f8_...55756_...B665.` (ring 13, 9 interior vertices). -/
def dEntry_24 : ClaimGlue.DEntry := HOF7_24.dEntryOf HDOF7V.hD_24 rfl

theorem colorable_24 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_24.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_24.colorable_of_occ_entry HDOF7V.hD_24 rfl htri h IH

/-- Entry 25, `f8_...55756_...B575.` (ring 13, 9 interior vertices). -/
def dEntry_25 : ClaimGlue.DEntry := HOF7_25.dEntryOf HDOF7V.hD_25 rfl

theorem colorable_25 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_25.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_25.colorable_of_occ_entry HDOF7V.hD_25 rfl htri h IH

/-- Entry 26, `f7_..65756_..5556.` (ring 11, 10 interior vertices). -/
def dEntry_26 : ClaimGlue.DEntry := HOF7_26.dEntryOf HDOF7V.hD_26 rfl

theorem colorable_26 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_26.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_26.colorable_of_occ_entry HDOF7V.hD_26 rfl htri h IH

/-- Entry 27, `f7_..65756_..5566.` (ring 12, 10 interior vertices). -/
def dEntry_27 : ClaimGlue.DEntry := HOF7_27.dEntryOf HDOF7V.hD_27 rfl

theorem colorable_27 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_27.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_27.colorable_of_occ_entry HDOF7V.hD_27 rfl htri h IH

/-- Entry 28, `f7_..65756_..5766.` (ring 14, 10 interior vertices). -/
def dEntry_28 : ClaimGlue.DEntry := HOF7_28.dEntryOf HDOF7V.hD_28 rfl

theorem colorable_28 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_28.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_28.colorable_of_occ_entry HDOF7V.hD_28 rfl htri h IH

/-- Entry 29, `f7_..65756_..5B66.` (ring 13, 9 interior vertices). -/
def dEntry_29 : ClaimGlue.DEntry := HOF7_29.dEntryOf HDOF7V.hD_29 rfl

theorem colorable_29 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_29.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_29.colorable_of_occ_entry HDOF7V.hD_29 rfl htri h IH

/-- Entry 30, `f7_..65756_..5B57.` (ring 13, 9 interior vertices). -/
def dEntry_30 : ClaimGlue.DEntry := HOF7_30.dEntryOf HDOF7V.hD_30 rfl

theorem colorable_30 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_30.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_30.colorable_of_occ_entry HDOF7V.hD_30 rfl htri h IH

/-- Entry 31, `f8_...55756_...6656.` (ring 13, 10 interior vertices). -/
def dEntry_31 : ClaimGlue.DEntry := HOF7_31.dEntryOf HDOF7V.hD_31 rfl

theorem colorable_31 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_31.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_31.colorable_of_occ_entry HDOF7V.hD_31 rfl htri h IH

/-- Entry 32, `f8_...55756_...6666.` (ring 14, 10 interior vertices). -/
def dEntry_32 : ClaimGlue.DEntry := HOF7_32.dEntryOf HDOF7V.hD_32 rfl

theorem colorable_32 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_32.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_32.colorable_of_occ_entry HDOF7V.hD_32 rfl htri h IH

/-- Entry 33, `f7_.65755B_.6557B.` (ring 12, 10 interior vertices). -/
def dEntry_33 : ClaimGlue.DEntry := HOF7_33.dEntryOf HDOF7V.hD_33 rfl

theorem colorable_33 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_33.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_33.colorable_of_occ_entry HDOF7V.hD_33 rfl htri h IH

/-- Entry 34, `f7_..65756_..555B.` (ring 11, 9 interior vertices). -/
def dEntry_34 : ClaimGlue.DEntry := HOF7_34.dEntryOf HDOF7V.hD_34 rfl

theorem colorable_34 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_34.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_34.colorable_of_occ_entry HDOF7V.hD_34 rfl htri h IH

/-- Entry 35, `f7_..55756_..B556.` (ring 11, 9 interior vertices). -/
def dEntry_35 : ClaimGlue.DEntry := HOF7_35.dEntryOf HDOF7V.hD_35 rfl

theorem colorable_35 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_35.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_35.colorable_of_occ_entry HDOF7V.hD_35 rfl htri h IH

/-- Entry 36, `f7_..55756_..B656.` (ring 12, 9 interior vertices). -/
def dEntry_36 : ClaimGlue.DEntry := HOF7_36.dEntryOf HDOF7V.hD_36 rfl

theorem colorable_36 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_36.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_36.colorable_of_occ_entry HDOF7V.hD_36 rfl htri h IH

/-- Entry 37, `f7_..55756_..B566.` (ring 12, 9 interior vertices). -/
def dEntry_37 : ClaimGlue.DEntry := HOF7_37.dEntryOf HDOF7V.hD_37 rfl

theorem colorable_37 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_37.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_37.colorable_of_occ_entry HDOF7V.hD_37 rfl htri h IH

/-- Entry 38, `f8_...55756_...B566.` (ring 13, 9 interior vertices). -/
def dEntry_38 : ClaimGlue.DEntry := HOF7_38.dEntryOf HDOF7V.hD_38 rfl

theorem colorable_38 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_38.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_38.colorable_of_occ_entry HDOF7V.hD_38 rfl htri h IH

/-- Entry 39, `f7_..65756_..5B5B.` (ring 12, 8 interior vertices). -/
def dEntry_39 : ClaimGlue.DEntry := HOF7_39.dEntryOf HDOF7V.hD_39 rfl

theorem colorable_39 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_39.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_39.colorable_of_occ_entry HDOF7V.hD_39 rfl htri h IH

/-- Entry 40, `f7_..65757_..5555.` (ring 11, 10 interior vertices). -/
def dEntry_40 : ClaimGlue.DEntry := HOF7_40.dEntryOf HDOF7V.hD_40 rfl

theorem colorable_40 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_40.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_40.colorable_of_occ_entry HDOF7V.hD_40 rfl htri h IH

/-- Entry 41, `f7_..55757_..6656.` (ring 13, 10 interior vertices). -/
def dEntry_41 : ClaimGlue.DEntry := HOF7_41.dEntryOf HDOF7V.hD_41 rfl

theorem colorable_41 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_41.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_41.colorable_of_occ_entry HDOF7V.hD_41 rfl htri h IH

/-- Entry 42, `f7_..55756_..665B.` (ring 12, 9 interior vertices). -/
def dEntry_42 : ClaimGlue.DEntry := HOF7_42.dEntryOf HDOF7V.hD_42 rfl

theorem colorable_42 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_42.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_42.colorable_of_occ_entry HDOF7V.hD_42 rfl htri h IH

/-- Entry 43, `f7_..55757_..7655.` (ring 13, 10 interior vertices). -/
def dEntry_43 : ClaimGlue.DEntry := HOF7_43.dEntryOf HDOF7V.hD_43 rfl

theorem colorable_43 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_43.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_43.colorable_of_occ_entry HDOF7V.hD_43 rfl htri h IH

/-- Entry 44, `f7_..55757_..B555.` (ring 11, 9 interior vertices). -/
def dEntry_44 : ClaimGlue.DEntry := HOF7_44.dEntryOf HDOF7V.hD_44 rfl

theorem colorable_44 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_44.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_44.colorable_of_occ_entry HDOF7V.hD_44 rfl htri h IH

/-- Entry 45, `f7_..55757_..B565.` (ring 12, 9 interior vertices). -/
def dEntry_45 : ClaimGlue.DEntry := HOF7_45.dEntryOf HDOF7V.hD_45 rfl

theorem colorable_45 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_45.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_45.colorable_of_occ_entry HDOF7V.hD_45 rfl htri h IH

/-- Entry 46, `f7_..65757_..6555.` (ring 12, 10 interior vertices). -/
def dEntry_46 : ClaimGlue.DEntry := HOF7_46.dEntryOf HDOF7V.hD_46 rfl

theorem colorable_46 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_46.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_46.colorable_of_occ_entry HDOF7V.hD_46 rfl htri h IH

/-- Entry 47, `f7_..55757_..B556.` (ring 12, 9 interior vertices). -/
def dEntry_47 : ClaimGlue.DEntry := HOF7_47.dEntryOf HDOF7V.hD_47 rfl

theorem colorable_47 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_47.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_47.colorable_of_occ_entry HDOF7V.hD_47 rfl htri h IH

/-- Entry 48, `f7_...5556_...676.` (ring 11, 8 interior vertices). -/
def dEntry_48 : ClaimGlue.DEntry := HOF7_48.dEntryOf HDOF7V.hD_48 rfl

theorem colorable_48 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_48.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_48.colorable_of_occ_entry HDOF7V.hD_48 rfl htri h IH

/-- Entry 49, `f7_..65756_..6557.` (ring 13, 10 interior vertices). -/
def dEntry_49 : ClaimGlue.DEntry := HOF7_49.dEntryOf HDOF7V.hD_49 rfl

theorem colorable_49 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_49.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_49.colorable_of_occ_entry HDOF7V.hD_49 rfl htri h IH

/-- Entry 50, `f7_..65756_..655B.` (ring 12, 9 interior vertices). -/
def dEntry_50 : ClaimGlue.DEntry := HOF7_50.dEntryOf HDOF7V.hD_50 rfl

theorem colorable_50 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_50.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_50.colorable_of_occ_entry HDOF7V.hD_50 rfl htri h IH

/-- Entry 51, `f7_..65757_..6556.` (ring 13, 10 interior vertices). -/
def dEntry_51 : ClaimGlue.DEntry := HOF7_51.dEntryOf HDOF7V.hD_51 rfl

theorem colorable_51 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HOF7_51.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_51.colorable_of_occ_entry HDOF7V.hD_51 rfl htri h IH

/-- Entry 52, `e7_B5555.._B5B5..._1111100` (ring 8, 7 interior vertices). -/
def dEntry_52 : ClaimGlue.DEntry := HOF7_52.dEntryOf HDOF7V.hD_52 rfl

theorem colorable_52 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_52.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_52.colorable_of_occ_entry HDOF7V.hD_52 rfl htri h IH

/-- Entry 53, `e7_B5555.._B5BB..._1111100` (ring 8, 6 interior vertices). -/
def dEntry_53 : ClaimGlue.DEntry := HOF7_53.dEntryOf HDOF7V.hD_53 rfl

theorem colorable_53 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 8 → Fin n}
    {int : Fin 6 → Fin n} (h : HOF7_53.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_53.colorable_of_occ_entry HDOF7V.hD_53 rfl htri h IH

/-- Entry 54, `e7_B5555.._B5B6..._1111100` (ring 9, 7 interior vertices). -/
def dEntry_54 : ClaimGlue.DEntry := HOF7_54.dEntryOf HDOF7V.hD_54 rfl

theorem colorable_54 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_54.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_54.colorable_of_occ_entry HDOF7V.hD_54 rfl htri h IH

/-- Entry 55, `e7_B5555.._65BB..._1111100` (ring 9, 7 interior vertices). -/
def dEntry_55 : ClaimGlue.DEntry := HOF7_55.dEntryOf HDOF7V.hD_55 rfl

theorem colorable_55 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_55.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_55.colorable_of_occ_entry HDOF7V.hD_55 rfl htri h IH

/-- Entry 56, `e7_B5556.._B5B5..._1111100` (ring 9, 7 interior vertices). -/
def dEntry_56 : ClaimGlue.DEntry := HOF7_56.dEntryOf HDOF7V.hD_56 rfl

theorem colorable_56 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_56.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_56.colorable_of_occ_entry HDOF7V.hD_56 rfl htri h IH

/-- Entry 57, `e7_B5555B._B5B56.._1111110` (ring 9, 8 interior vertices). -/
def dEntry_57 : ClaimGlue.DEntry := HOF7_57.dEntryOf HDOF7V.hD_57 rfl

theorem colorable_57 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_57.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_57.colorable_of_occ_entry HDOF7V.hD_57 rfl htri h IH

/-- Entry 58, `e7_B5555B._BBB6B.._1111110` (ring 9, 6 interior vertices). -/
def dEntry_58 : ClaimGlue.DEntry := HOF7_58.dEntryOf HDOF7V.hD_58 rfl

theorem colorable_58 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 9 → Fin n}
    {int : Fin 6 → Fin n} (h : HOF7_58.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_58.colorable_of_occ_entry HDOF7V.hD_58 rfl htri h IH

/-- Entry 59, `e7_B5555.._B6B6..._1111100` (ring 10, 7 interior vertices). -/
def dEntry_59 : ClaimGlue.DEntry := HOF7_59.dEntryOf HDOF7V.hD_59 rfl

theorem colorable_59 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_59.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_59.colorable_of_occ_entry HDOF7V.hD_59 rfl htri h IH

/-- Entry 60, `e7_B5556.._65B5..._1111100` (ring 10, 8 interior vertices). -/
def dEntry_60 : ClaimGlue.DEntry := HOF7_60.dEntryOf HDOF7V.hD_60 rfl

theorem colorable_60 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_60.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_60.colorable_of_occ_entry HDOF7V.hD_60 rfl htri h IH

/-- Entry 61, `e7_B5556.._B6B5..._1111100` (ring 10, 7 interior vertices). -/
def dEntry_61 : ClaimGlue.DEntry := HOF7_61.dEntryOf HDOF7V.hD_61 rfl

theorem colorable_61 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_61.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_61.colorable_of_occ_entry HDOF7V.hD_61 rfl htri h IH

/-- Entry 62, `e7_B5555B._65B56.._1111110` (ring 10, 9 interior vertices). -/
def dEntry_62 : ClaimGlue.DEntry := HOF7_62.dEntryOf HDOF7V.hD_62 rfl

theorem colorable_62 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 9 → Fin n} (h : HOF7_62.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_62.colorable_of_occ_entry HDOF7V.hD_62 rfl htri h IH

/-- Entry 63, `e7_B5555B._B6B56.._1111110` (ring 10, 8 interior vertices). -/
def dEntry_63 : ClaimGlue.DEntry := HOF7_63.dEntryOf HDOF7V.hD_63 rfl

theorem colorable_63 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 8 → Fin n} (h : HOF7_63.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_63.colorable_of_occ_entry HDOF7V.hD_63 rfl htri h IH

/-- Entry 64, `e7_...6556_...5B5._0001111` (ring 10, 7 interior vertices). -/
def dEntry_64 : ClaimGlue.DEntry := HOF7_64.dEntryOf HDOF7V.hD_64 rfl

theorem colorable_64 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : HOF7_64.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HOF7_64.colorable_of_occ_entry HDOF7V.hD_64 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14, dEntry_15, dEntry_16, dEntry_17, dEntry_18, dEntry_19, dEntry_20, dEntry_21, dEntry_22, dEntry_23, dEntry_24, dEntry_25, dEntry_26, dEntry_27, dEntry_28, dEntry_29, dEntry_30, dEntry_31, dEntry_32, dEntry_33, dEntry_34, dEntry_35, dEntry_36, dEntry_37, dEntry_38, dEntry_39, dEntry_40, dEntry_41, dEntry_42, dEntry_43, dEntry_44, dEntry_45, dEntry_46, dEntry_47, dEntry_48, dEntry_49, dEntry_50, dEntry_51, dEntry_52, dEntry_53, dEntry_54, dEntry_55, dEntry_56, dEntry_57, dEntry_58, dEntry_59, dEntry_60, dEntry_61, dEntry_62, dEntry_63, dEntry_64]

end HDOF7Occ

#print axioms HDOF7Occ.dEntry_0
#print axioms HDOF7Occ.colorable_0
#print axioms HDOF7Occ.dEntry_1
#print axioms HDOF7Occ.colorable_1
#print axioms HDOF7Occ.dEntry_2
#print axioms HDOF7Occ.colorable_2
#print axioms HDOF7Occ.dEntry_3
#print axioms HDOF7Occ.colorable_3
#print axioms HDOF7Occ.dEntry_4
#print axioms HDOF7Occ.colorable_4
#print axioms HDOF7Occ.dEntry_5
#print axioms HDOF7Occ.colorable_5
#print axioms HDOF7Occ.dEntry_6
#print axioms HDOF7Occ.colorable_6
#print axioms HDOF7Occ.dEntry_7
#print axioms HDOF7Occ.colorable_7
#print axioms HDOF7Occ.dEntry_8
#print axioms HDOF7Occ.colorable_8
#print axioms HDOF7Occ.dEntry_9
#print axioms HDOF7Occ.colorable_9
#print axioms HDOF7Occ.dEntry_10
#print axioms HDOF7Occ.colorable_10
#print axioms HDOF7Occ.dEntry_11
#print axioms HDOF7Occ.colorable_11
#print axioms HDOF7Occ.dEntry_12
#print axioms HDOF7Occ.colorable_12
#print axioms HDOF7Occ.dEntry_13
#print axioms HDOF7Occ.colorable_13
#print axioms HDOF7Occ.dEntry_14
#print axioms HDOF7Occ.colorable_14
#print axioms HDOF7Occ.dEntry_15
#print axioms HDOF7Occ.colorable_15
#print axioms HDOF7Occ.dEntry_16
#print axioms HDOF7Occ.colorable_16
#print axioms HDOF7Occ.dEntry_17
#print axioms HDOF7Occ.colorable_17
#print axioms HDOF7Occ.dEntry_18
#print axioms HDOF7Occ.colorable_18
#print axioms HDOF7Occ.dEntry_19
#print axioms HDOF7Occ.colorable_19
#print axioms HDOF7Occ.dEntry_20
#print axioms HDOF7Occ.colorable_20
#print axioms HDOF7Occ.dEntry_21
#print axioms HDOF7Occ.colorable_21
#print axioms HDOF7Occ.dEntry_22
#print axioms HDOF7Occ.colorable_22
#print axioms HDOF7Occ.dEntry_23
#print axioms HDOF7Occ.colorable_23
#print axioms HDOF7Occ.dEntry_24
#print axioms HDOF7Occ.colorable_24
#print axioms HDOF7Occ.dEntry_25
#print axioms HDOF7Occ.colorable_25
#print axioms HDOF7Occ.dEntry_26
#print axioms HDOF7Occ.colorable_26
#print axioms HDOF7Occ.dEntry_27
#print axioms HDOF7Occ.colorable_27
#print axioms HDOF7Occ.dEntry_28
#print axioms HDOF7Occ.colorable_28
#print axioms HDOF7Occ.dEntry_29
#print axioms HDOF7Occ.colorable_29
#print axioms HDOF7Occ.dEntry_30
#print axioms HDOF7Occ.colorable_30
#print axioms HDOF7Occ.dEntry_31
#print axioms HDOF7Occ.colorable_31
#print axioms HDOF7Occ.dEntry_32
#print axioms HDOF7Occ.colorable_32
#print axioms HDOF7Occ.dEntry_33
#print axioms HDOF7Occ.colorable_33
#print axioms HDOF7Occ.dEntry_34
#print axioms HDOF7Occ.colorable_34
#print axioms HDOF7Occ.dEntry_35
#print axioms HDOF7Occ.colorable_35
#print axioms HDOF7Occ.dEntry_36
#print axioms HDOF7Occ.colorable_36
#print axioms HDOF7Occ.dEntry_37
#print axioms HDOF7Occ.colorable_37
#print axioms HDOF7Occ.dEntry_38
#print axioms HDOF7Occ.colorable_38
#print axioms HDOF7Occ.dEntry_39
#print axioms HDOF7Occ.colorable_39
#print axioms HDOF7Occ.dEntry_40
#print axioms HDOF7Occ.colorable_40
#print axioms HDOF7Occ.dEntry_41
#print axioms HDOF7Occ.colorable_41
#print axioms HDOF7Occ.dEntry_42
#print axioms HDOF7Occ.colorable_42
#print axioms HDOF7Occ.dEntry_43
#print axioms HDOF7Occ.colorable_43
#print axioms HDOF7Occ.dEntry_44
#print axioms HDOF7Occ.colorable_44
#print axioms HDOF7Occ.dEntry_45
#print axioms HDOF7Occ.colorable_45
#print axioms HDOF7Occ.dEntry_46
#print axioms HDOF7Occ.colorable_46
#print axioms HDOF7Occ.dEntry_47
#print axioms HDOF7Occ.colorable_47
#print axioms HDOF7Occ.dEntry_48
#print axioms HDOF7Occ.colorable_48
#print axioms HDOF7Occ.dEntry_49
#print axioms HDOF7Occ.colorable_49
#print axioms HDOF7Occ.dEntry_50
#print axioms HDOF7Occ.colorable_50
#print axioms HDOF7Occ.dEntry_51
#print axioms HDOF7Occ.colorable_51
#print axioms HDOF7Occ.dEntry_52
#print axioms HDOF7Occ.colorable_52
#print axioms HDOF7Occ.dEntry_53
#print axioms HDOF7Occ.colorable_53
#print axioms HDOF7Occ.dEntry_54
#print axioms HDOF7Occ.colorable_54
#print axioms HDOF7Occ.dEntry_55
#print axioms HDOF7Occ.colorable_55
#print axioms HDOF7Occ.dEntry_56
#print axioms HDOF7Occ.colorable_56
#print axioms HDOF7Occ.dEntry_57
#print axioms HDOF7Occ.colorable_57
#print axioms HDOF7Occ.dEntry_58
#print axioms HDOF7Occ.colorable_58
#print axioms HDOF7Occ.dEntry_59
#print axioms HDOF7Occ.colorable_59
#print axioms HDOF7Occ.dEntry_60
#print axioms HDOF7Occ.colorable_60
#print axioms HDOF7Occ.dEntry_61
#print axioms HDOF7Occ.colorable_61
#print axioms HDOF7Occ.dEntry_62
#print axioms HDOF7Occ.colorable_62
#print axioms HDOF7Occ.dEntry_63
#print axioms HDOF7Occ.colorable_63
#print axioms HDOF7Occ.dEntry_64
#print axioms HDOF7Occ.colorable_64
