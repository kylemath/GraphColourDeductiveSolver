import HDK3GXAll
import COccHK3GXD_00
import COccHK3GXD_01
import COccHK3GXD_02
import COccHK3GXD_03
import COccHK3GXD_04
import COccHK3GXD_05
import COccHK3GXD_06
import COccHK3GXD_07
import COccHK3GXD_08
import COccHK3GXD_09
import COccHK3GXD_10
import COccHK3GXD_11
import COccHK3GXD_12
import COccHK3GXD_13
import COccHK3GXD_14
import COccHK3GXD_15
import COccHK3GXD_16
import COccHK3GXD_17
import COccHK3GXD_18
import COccHK3GXD_19
import COccHK3GXD_20
import COccHK3GXD_21
import COccHK3GXD_22
import COccHK3GXD_23
import COccHK3GXD_24
import COccHK3GXD_25
import COccHK3GXD_26
import COccHK3GXD_27
import COccHK3GXD_28
import COccHK3GXD_29
import COccHK3GXD_30
import COccHK3GXD_31
import COccHK3GXD_32
import COccHK3GXD_33
import COccHK3GXD_34
import COccHK3GXD_35
import COccHK3GXD_36
import COccHK3GXD_37
import COccHK3GXD_38
import COccHK3GXD_39
import COccHK3GXD_40
import COccHK3GXD_41
import COccHK3GXD_42
import COccHK3GXD_43
import COccHK3GXD_44
import COccHK3GXD_45
import COccHK3GXD_46
import COccHK3GXD_47
import COccHK3GXD_48
import COccHK3GXD_49
import COccHK3GXD_50
import COccHK3GXD_51
import COccHK3GXD_52
import COccHK3GXD_53
import COccHK3GXD_54
import COccHK3GXD_55
import COccHK3GXD_56
import COccHK3GXD_57
import COccHK3GXD_58
import COccHK3GXD_59
import COccHK3GXD_60
import COccHK3GXD_61
import COccHK3GXD_62
import COccHK3GXD_63
import COccHK3GXD_64
import COccHK3GXD_65
import COccHK3GXD_66
import COccHK3GXD_67
import COccHK3GXD_68
import COccHK3GXD_69
import COccHK3GXD_70
import COccHK3GXD_71
import COccHK3GXD_72
import COccHK3GXD_73
import COccHK3GXD_74
import COccHK3GXD_75
import COccHK3GXD_76
import COccHK3GXD_77
import COccHK3GXD_78
import COccHK3GXD_79
import COccHK3GXD_80
import COccHK3GXD_81
import COccHK3GXD_82
import COccHK3GXD_83
import COccHK3GXD_84
import COccHK3GXD_85
import COccHK3GXD_86
import COccHK3GXD_87
import COccHK3GXD_88
import COccHK3GXD_89

/-! # HDK3GXOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK3GXV.hD_i` on `HDK3GX.hdk3gxConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK3GX.hdk3gxConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK3GXOcc

variable {n : ℕ}

/-- Entry 0, `b7_u.56.565_.5.56..` (ring 12, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK3GXD_00.dEntryOf HDK3GXV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HK3GXD_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_00.colorable_of_occ_entry HDK3GXV.hD_0 rfl htri h IH

/-- Entry 1, `b7_u.56.565_65.56..` (ring 13, 10 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HK3GXD_01.dEntryOf HDK3GXV.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_01.colorable_of_occ_entry HDK3GXV.hD_1 rfl htri h IH

/-- Entry 2, `b7_u.567755_..5.66.` (ring 14, 10 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HK3GXD_02.dEntryOf HDK3GXV.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_02.colorable_of_occ_entry HDK3GXV.hD_2 rfl htri h IH

/-- Entry 3, `b7_u.567755_.55.66.` (ring 14, 11 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HK3GXD_03.dEntryOf HDK3GXV.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_03.colorable_of_occ_entry HDK3GXV.hD_3 rfl htri h IH

/-- Entry 4, `b7_u.567755_555.66.` (ring 14, 12 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HK3GXD_04.dEntryOf HDK3GXV.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_04.colorable_of_occ_entry HDK3GXV.hD_4 rfl htri h IH

/-- Entry 5, `b7_u.57685._.5555..` (ring 14, 10 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HK3GXD_05.dEntryOf HDK3GXV.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_05.colorable_of_occ_entry HDK3GXV.hD_5 rfl htri h IH

/-- Entry 6, `b7_u.57685._55555..` (ring 14, 11 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HK3GXD_06.dEntryOf HDK3GXV.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_06.colorable_of_occ_entry HDK3GXV.hD_6 rfl htri h IH

/-- Entry 7, `b7_u85..575_5..5566` (ring 14, 11 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := HK3GXD_07.dEntryOf HDK3GXV.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_07.colorable_of_occ_entry HDK3GXV.hD_7 rfl htri h IH

/-- Entry 8, `b7_u85..575_55..566` (ring 14, 11 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := HK3GXD_08.dEntryOf HDK3GXV.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_08.colorable_of_occ_entry HDK3GXV.hD_8 rfl htri h IH

/-- Entry 9, `b7_u85..575_55.5566` (ring 14, 12 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := HK3GXD_09.dEntryOf HDK3GXV.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_09.colorable_of_occ_entry HDK3GXV.hD_9 rfl htri h IH

/-- Entry 10, `b8_u...56556_..55.66.` (ring 12, 10 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := HK3GXD_10.dEntryOf HDK3GXV.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_10.colorable_of_occ_entry HDK3GXV.hD_10 rfl htri h IH

/-- Entry 11, `b8_u.5556.56_65.5.56.` (ring 14, 12 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := HK3GXD_11.dEntryOf HDK3GXV.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_11.colorable_of_occ_entry HDK3GXV.hD_11 rfl htri h IH

/-- Entry 12, `b8_u.56.5556_56..5.5.` (ring 13, 11 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := HK3GXD_12.dEntryOf HDK3GXV.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_12.colorable_of_occ_entry HDK3GXV.hD_12 rfl htri h IH

/-- Entry 13, `b8_u.56.5556_56..585.` (ring 14, 12 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := HK3GXD_13.dEntryOf HDK3GXV.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_13.colorable_of_occ_entry HDK3GXV.hD_13 rfl htri h IH

/-- Entry 14, `b8_u.56.5756_.5.6555.` (ring 14, 12 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := HK3GXD_14.dEntryOf HDK3GXV.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_14.colorable_of_occ_entry HDK3GXV.hD_14 rfl htri h IH

/-- Entry 15, `b8_u.56.5756_55..555.` (ring 13, 12 interior vertices). -/
def dEntry_15 : ClaimGlue.DEntry := HK3GXD_15.dEntryOf HDK3GXV.hD_15 rfl

theorem colorable_15 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_15.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_15.colorable_of_occ_entry HDK3GXV.hD_15 rfl htri h IH

/-- Entry 16, `b8_u.56.5756_55.6555.` (ring 14, 13 interior vertices). -/
def dEntry_16 : ClaimGlue.DEntry := HK3GXD_16.dEntryOf HDK3GXV.hD_16 rfl

theorem colorable_16 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_16.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_16.colorable_of_occ_entry HDK3GXV.hD_16 rfl htri h IH

/-- Entry 17, `b8_u.56656.._..5665..` (ring 14, 10 interior vertices). -/
def dEntry_17 : ClaimGlue.DEntry := HK3GXD_17.dEntryOf HDK3GXV.hD_17 rfl

theorem colorable_17 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_17.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_17.colorable_of_occ_entry HDK3GXV.hD_17 rfl htri h IH

/-- Entry 18, `b8_u.56656.5_..566...` (ring 14, 10 interior vertices). -/
def dEntry_18 : ClaimGlue.DEntry := HK3GXD_18.dEntryOf HDK3GXV.hD_18 rfl

theorem colorable_18 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_18.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_18.colorable_of_occ_entry HDK3GXV.hD_18 rfl htri h IH

/-- Entry 19, `b8_u.5665675_..5...5.` (ring 14, 10 interior vertices). -/
def dEntry_19 : ClaimGlue.DEntry := HK3GXD_19.dEntryOf HDK3GXV.hD_19 rfl

theorem colorable_19 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_19.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_19.colorable_of_occ_entry HDK3GXV.hD_19 rfl htri h IH

/-- Entry 20, `b8_u.5665675_..5..5..` (ring 14, 10 interior vertices). -/
def dEntry_20 : ClaimGlue.DEntry := HK3GXD_20.dEntryOf HDK3GXV.hD_20 rfl

theorem colorable_20 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_20.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_20.colorable_of_occ_entry HDK3GXV.hD_20 rfl htri h IH

/-- Entry 21, `b8_u.5665675_..5..55.` (ring 14, 11 interior vertices). -/
def dEntry_21 : ClaimGlue.DEntry := HK3GXD_21.dEntryOf HDK3GXV.hD_21 rfl

theorem colorable_21 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_21.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_21.colorable_of_occ_entry HDK3GXV.hD_21 rfl htri h IH

/-- Entry 22, `b8_u.567575._...6555.` (ring 14, 11 interior vertices). -/
def dEntry_22 : ClaimGlue.DEntry := HK3GXD_22.dEntryOf HDK3GXV.hD_22 rfl

theorem colorable_22 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_22.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_22.colorable_of_occ_entry HDK3GXV.hD_22 rfl htri h IH

/-- Entry 23, `b8_u.567575._.5.655..` (ring 14, 11 interior vertices). -/
def dEntry_23 : ClaimGlue.DEntry := HK3GXD_23.dEntryOf HDK3GXV.hD_23 rfl

theorem colorable_23 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_23.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_23.colorable_of_occ_entry HDK3GXV.hD_23 rfl htri h IH

/-- Entry 24, `b8_u.567575._.5.6555.` (ring 14, 12 interior vertices). -/
def dEntry_24 : ClaimGlue.DEntry := HK3GXD_24.dEntryOf HDK3GXV.hD_24 rfl

theorem colorable_24 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_24.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_24.colorable_of_occ_entry HDK3GXV.hD_24 rfl htri h IH

/-- Entry 25, `b8_u.567575._55.655..` (ring 14, 12 interior vertices). -/
def dEntry_25 : ClaimGlue.DEntry := HK3GXD_25.dEntryOf HDK3GXV.hD_25 rfl

theorem colorable_25 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_25.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_25.colorable_of_occ_entry HDK3GXV.hD_25 rfl htri h IH

/-- Entry 26, `b8_u.567575._55.6555.` (ring 14, 13 interior vertices). -/
def dEntry_26 : ClaimGlue.DEntry := HK3GXD_26.dEntryOf HDK3GXV.hD_26 rfl

theorem colorable_26 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_26.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_26.colorable_of_occ_entry HDK3GXV.hD_26 rfl htri h IH

/-- Entry 27, `b8_u.5675756_...6555.` (ring 14, 12 interior vertices). -/
def dEntry_27 : ClaimGlue.DEntry := HK3GXD_27.dEntryOf HDK3GXV.hD_27 rfl

theorem colorable_27 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_27.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_27.colorable_of_occ_entry HDK3GXV.hD_27 rfl htri h IH

/-- Entry 28, `b8_u.5675756_.5..555.` (ring 14, 12 interior vertices). -/
def dEntry_28 : ClaimGlue.DEntry := HK3GXD_28.dEntryOf HDK3GXV.hD_28 rfl

theorem colorable_28 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_28.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_28.colorable_of_occ_entry HDK3GXV.hD_28 rfl htri h IH

/-- Entry 29, `b8_u.5675756_.5.6555.` (ring 14, 13 interior vertices). -/
def dEntry_29 : ClaimGlue.DEntry := HK3GXD_29.dEntryOf HDK3GXV.hD_29 rfl

theorem colorable_29 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_29.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_29.colorable_of_occ_entry HDK3GXV.hD_29 rfl htri h IH

/-- Entry 30, `b8_u.5675756_55..555.` (ring 14, 13 interior vertices). -/
def dEntry_30 : ClaimGlue.DEntry := HK3GXD_30.dEntryOf HDK3GXV.hD_30 rfl

theorem colorable_30 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_30.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_30.colorable_of_occ_entry HDK3GXV.hD_30 rfl htri h IH

/-- Entry 31, `b8_u.5675756_55.6555.` (ring 14, 14 interior vertices). -/
def dEntry_31 : ClaimGlue.DEntry := HK3GXD_31.dEntryOf HDK3GXV.hD_31 rfl

theorem colorable_31 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 14 → Fin n} (h : HK3GXD_31.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_31.colorable_of_occ_entry HDK3GXV.hD_31 rfl htri h IH

/-- Entry 32, `b8_u856.5556_56....5.` (ring 14, 11 interior vertices). -/
def dEntry_32 : ClaimGlue.DEntry := HK3GXD_32.dEntryOf HDK3GXV.hD_32 rfl

theorem colorable_32 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_32.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_32.colorable_of_occ_entry HDK3GXV.hD_32 rfl htri h IH

/-- Entry 33, `b8_u856.5556_56..5.5.` (ring 14, 12 interior vertices). -/
def dEntry_33 : ClaimGlue.DEntry := HK3GXD_33.dEntryOf HDK3GXV.hD_33 rfl

theorem colorable_33 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_33.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_33.colorable_of_occ_entry HDK3GXV.hD_33 rfl htri h IH

/-- Entry 34, `b8_u856.5656_56...55.` (ring 14, 12 interior vertices). -/
def dEntry_34 : ClaimGlue.DEntry := HK3GXD_34.dEntryOf HDK3GXV.hD_34 rfl

theorem colorable_34 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_34.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_34.colorable_of_occ_entry HDK3GXV.hD_34 rfl htri h IH

/-- Entry 35, `b8_u856.5756_55..555.` (ring 14, 13 interior vertices). -/
def dEntry_35 : ClaimGlue.DEntry := HK3GXD_35.dEntryOf HDK3GXV.hD_35 rfl

theorem colorable_35 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_35.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_35.colorable_of_occ_entry HDK3GXV.hD_35 rfl htri h IH

/-- Entry 36, `b9_u...575655_...55.65.` (ring 13, 11 interior vertices). -/
def dEntry_36 : ClaimGlue.DEntry := HK3GXD_36.dEntryOf HDK3GXV.hD_36 rfl

theorem colorable_36 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_36.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_36.colorable_of_occ_entry HDK3GXV.hD_36 rfl htri h IH

/-- Entry 37, `b9_u...575655_...55765.` (ring 14, 12 interior vertices). -/
def dEntry_37 : ClaimGlue.DEntry := HK3GXD_37.dEntryOf HDK3GXV.hD_37 rfl

theorem colorable_37 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_37.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_37.colorable_of_occ_entry HDK3GXV.hD_37 rfl htri h IH

/-- Entry 38, `b9_u..6575655_...5..65.` (ring 14, 11 interior vertices). -/
def dEntry_38 : ClaimGlue.DEntry := HK3GXD_38.dEntryOf HDK3GXV.hD_38 rfl

theorem colorable_38 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_38.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_38.colorable_of_occ_entry HDK3GXV.hD_38 rfl htri h IH

/-- Entry 39, `b9_u..6575655_...55.65.` (ring 14, 12 interior vertices). -/
def dEntry_39 : ClaimGlue.DEntry := HK3GXD_39.dEntryOf HDK3GXV.hD_39 rfl

theorem colorable_39 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_39.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_39.colorable_of_occ_entry HDK3GXV.hD_39 rfl htri h IH

/-- Entry 40, `b9_u..676565._..5555...` (ring 14, 11 interior vertices). -/
def dEntry_40 : ClaimGlue.DEntry := HK3GXD_40.dEntryOf HDK3GXV.hD_40 rfl

theorem colorable_40 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_40.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_40.colorable_of_occ_entry HDK3GXV.hD_40 rfl htri h IH

/-- Entry 41, `b9_u.5.575655_...5..65.` (ring 14, 11 interior vertices). -/
def dEntry_41 : ClaimGlue.DEntry := HK3GXD_41.dEntryOf HDK3GXV.hD_41 rfl

theorem colorable_41 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_41.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_41.colorable_of_occ_entry HDK3GXV.hD_41 rfl htri h IH

/-- Entry 42, `b9_u.5.575655_...55.65.` (ring 14, 12 interior vertices). -/
def dEntry_42 : ClaimGlue.DEntry := HK3GXD_42.dEntryOf HDK3GXV.hD_42 rfl

theorem colorable_42 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_42.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_42.colorable_of_occ_entry HDK3GXV.hD_42 rfl htri h IH

/-- Entry 43, `b9_u.565.5655_.5....65.` (ring 13, 11 interior vertices). -/
def dEntry_43 : ClaimGlue.DEntry := HK3GXD_43.dEntryOf HDK3GXV.hD_43 rfl

theorem colorable_43 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_43.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_43.colorable_of_occ_entry HDK3GXV.hD_43 rfl htri h IH

/-- Entry 44, `b9_u.565.5655_.5..5.65.` (ring 14, 12 interior vertices). -/
def dEntry_44 : ClaimGlue.DEntry := HK3GXD_44.dEntryOf HDK3GXV.hD_44 rfl

theorem colorable_44 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_44.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_44.colorable_of_occ_entry HDK3GXV.hD_44 rfl htri h IH

/-- Entry 45, `b9_u.565.5655_.5.5..65.` (ring 14, 12 interior vertices). -/
def dEntry_45 : ClaimGlue.DEntry := HK3GXD_45.dEntryOf HDK3GXV.hD_45 rfl

theorem colorable_45 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_45.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_45.colorable_of_occ_entry HDK3GXV.hD_45 rfl htri h IH

/-- Entry 46, `b9_u.56575655_....5....` (ring 14, 10 interior vertices). -/
def dEntry_46 : ClaimGlue.DEntry := HK3GXD_46.dEntryOf HDK3GXV.hD_46 rfl

theorem colorable_46 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_46.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_46.colorable_of_occ_entry HDK3GXV.hD_46 rfl htri h IH

/-- Entry 47, `b9_u.56575655_....5..5.` (ring 14, 11 interior vertices). -/
def dEntry_47 : ClaimGlue.DEntry := HK3GXD_47.dEntryOf HDK3GXV.hD_47 rfl

theorem colorable_47 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_47.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_47.colorable_of_occ_entry HDK3GXV.hD_47 rfl htri h IH

/-- Entry 48, `b9_u.56575655_....5.65.` (ring 14, 12 interior vertices). -/
def dEntry_48 : ClaimGlue.DEntry := HK3GXD_48.dEntryOf HDK3GXV.hD_48 rfl

theorem colorable_48 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_48.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_48.colorable_of_occ_entry HDK3GXV.hD_48 rfl htri h IH

/-- Entry 49, `b9_u.56575655_...5.....` (ring 14, 10 interior vertices). -/
def dEntry_49 : ClaimGlue.DEntry := HK3GXD_49.dEntryOf HDK3GXV.hD_49 rfl

theorem colorable_49 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3GXD_49.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_49.colorable_of_occ_entry HDK3GXV.hD_49 rfl htri h IH

/-- Entry 50, `b9_u.56575655_...5...5.` (ring 14, 11 interior vertices). -/
def dEntry_50 : ClaimGlue.DEntry := HK3GXD_50.dEntryOf HDK3GXV.hD_50 rfl

theorem colorable_50 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_50.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_50.colorable_of_occ_entry HDK3GXV.hD_50 rfl htri h IH

/-- Entry 51, `b9_u.56575655_...5..65.` (ring 14, 12 interior vertices). -/
def dEntry_51 : ClaimGlue.DEntry := HK3GXD_51.dEntryOf HDK3GXV.hD_51 rfl

theorem colorable_51 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_51.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_51.colorable_of_occ_entry HDK3GXV.hD_51 rfl htri h IH

/-- Entry 52, `b9_u.56575655_...55....` (ring 14, 11 interior vertices). -/
def dEntry_52 : ClaimGlue.DEntry := HK3GXD_52.dEntryOf HDK3GXV.hD_52 rfl

theorem colorable_52 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_52.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_52.colorable_of_occ_entry HDK3GXV.hD_52 rfl htri h IH

/-- Entry 53, `b9_u.56575655_...55..5.` (ring 14, 12 interior vertices). -/
def dEntry_53 : ClaimGlue.DEntry := HK3GXD_53.dEntryOf HDK3GXV.hD_53 rfl

theorem colorable_53 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_53.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_53.colorable_of_occ_entry HDK3GXV.hD_53 rfl htri h IH

/-- Entry 54, `b9_u.56575655_...55.65.` (ring 14, 13 interior vertices). -/
def dEntry_54 : ClaimGlue.DEntry := HK3GXD_54.dEntryOf HDK3GXV.hD_54 rfl

theorem colorable_54 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_54.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_54.colorable_of_occ_entry HDK3GXV.hD_54 rfl htri h IH

/-- Entry 55, `b9_u.56575655_.5....65.` (ring 14, 12 interior vertices). -/
def dEntry_55 : ClaimGlue.DEntry := HK3GXD_55.dEntryOf HDK3GXV.hD_55 rfl

theorem colorable_55 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_55.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_55.colorable_of_occ_entry HDK3GXV.hD_55 rfl htri h IH

/-- Entry 56, `b9_u.56575655_.5..5....` (ring 14, 11 interior vertices). -/
def dEntry_56 : ClaimGlue.DEntry := HK3GXD_56.dEntryOf HDK3GXV.hD_56 rfl

theorem colorable_56 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_56.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_56.colorable_of_occ_entry HDK3GXV.hD_56 rfl htri h IH

/-- Entry 57, `b9_u.56575655_.5..5..5.` (ring 14, 12 interior vertices). -/
def dEntry_57 : ClaimGlue.DEntry := HK3GXD_57.dEntryOf HDK3GXV.hD_57 rfl

theorem colorable_57 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_57.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_57.colorable_of_occ_entry HDK3GXV.hD_57 rfl htri h IH

/-- Entry 58, `b9_u.56575655_.5..5.65.` (ring 14, 13 interior vertices). -/
def dEntry_58 : ClaimGlue.DEntry := HK3GXD_58.dEntryOf HDK3GXV.hD_58 rfl

theorem colorable_58 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_58.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_58.colorable_of_occ_entry HDK3GXV.hD_58 rfl htri h IH

/-- Entry 59, `b9_u.56575655_.5.5.....` (ring 14, 11 interior vertices). -/
def dEntry_59 : ClaimGlue.DEntry := HK3GXD_59.dEntryOf HDK3GXV.hD_59 rfl

theorem colorable_59 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_59.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_59.colorable_of_occ_entry HDK3GXV.hD_59 rfl htri h IH

/-- Entry 60, `b9_u.56575655_.5.5...5.` (ring 14, 12 interior vertices). -/
def dEntry_60 : ClaimGlue.DEntry := HK3GXD_60.dEntryOf HDK3GXV.hD_60 rfl

theorem colorable_60 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_60.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_60.colorable_of_occ_entry HDK3GXV.hD_60 rfl htri h IH

/-- Entry 61, `b9_u.56575655_.5.5..65.` (ring 14, 13 interior vertices). -/
def dEntry_61 : ClaimGlue.DEntry := HK3GXD_61.dEntryOf HDK3GXV.hD_61 rfl

theorem colorable_61 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_61.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_61.colorable_of_occ_entry HDK3GXV.hD_61 rfl htri h IH

/-- Entry 62, `b9_u.56575655_.5.55....` (ring 14, 12 interior vertices). -/
def dEntry_62 : ClaimGlue.DEntry := HK3GXD_62.dEntryOf HDK3GXV.hD_62 rfl

theorem colorable_62 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_62.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_62.colorable_of_occ_entry HDK3GXV.hD_62 rfl htri h IH

/-- Entry 63, `b9_u.56575655_.5.55..5.` (ring 14, 13 interior vertices). -/
def dEntry_63 : ClaimGlue.DEntry := HK3GXD_63.dEntryOf HDK3GXV.hD_63 rfl

theorem colorable_63 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_63.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_63.colorable_of_occ_entry HDK3GXV.hD_63 rfl htri h IH

/-- Entry 64, `b9_u.56575655_.5.55.65.` (ring 14, 14 interior vertices). -/
def dEntry_64 : ClaimGlue.DEntry := HK3GXD_64.dEntryOf HDK3GXV.hD_64 rfl

theorem colorable_64 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 14 → Fin n} (h : HK3GXD_64.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_64.colorable_of_occ_entry HDK3GXV.hD_64 rfl htri h IH

/-- Entry 65, `b9_u.567656.._..5555...` (ring 14, 11 interior vertices). -/
def dEntry_65 : ClaimGlue.DEntry := HK3GXD_65.dEntryOf HDK3GXV.hD_65 rfl

theorem colorable_65 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_65.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_65.colorable_of_occ_entry HDK3GXV.hD_65 rfl htri h IH

/-- Entry 66, `b9_u.567656.._.55.55...` (ring 14, 11 interior vertices). -/
def dEntry_66 : ClaimGlue.DEntry := HK3GXD_66.dEntryOf HDK3GXV.hD_66 rfl

theorem colorable_66 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_66.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_66.colorable_of_occ_entry HDK3GXV.hD_66 rfl htri h IH

/-- Entry 67, `b9_u.567656.._.55555...` (ring 14, 12 interior vertices). -/
def dEntry_67 : ClaimGlue.DEntry := HK3GXD_67.dEntryOf HDK3GXV.hD_67 rfl

theorem colorable_67 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_67.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_67.colorable_of_occ_entry HDK3GXV.hD_67 rfl htri h IH

/-- Entry 68, `b9_u.567656.._55.555...` (ring 14, 12 interior vertices). -/
def dEntry_68 : ClaimGlue.DEntry := HK3GXD_68.dEntryOf HDK3GXV.hD_68 rfl

theorem colorable_68 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_68.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_68.colorable_of_occ_entry HDK3GXV.hD_68 rfl htri h IH

/-- Entry 69, `b9_u.567656.._555.55...` (ring 14, 12 interior vertices). -/
def dEntry_69 : ClaimGlue.DEntry := HK3GXD_69.dEntryOf HDK3GXV.hD_69 rfl

theorem colorable_69 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_69.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_69.colorable_of_occ_entry HDK3GXV.hD_69 rfl htri h IH

/-- Entry 70, `b9_u.567656.._555555...` (ring 14, 13 interior vertices). -/
def dEntry_70 : ClaimGlue.DEntry := HK3GXD_70.dEntryOf HDK3GXV.hD_70 rfl

theorem colorable_70 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_70.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_70.colorable_of_occ_entry HDK3GXV.hD_70 rfl htri h IH

/-- Entry 71, `b9_u.5676565._..5.55...` (ring 14, 11 interior vertices). -/
def dEntry_71 : ClaimGlue.DEntry := HK3GXD_71.dEntryOf HDK3GXV.hD_71 rfl

theorem colorable_71 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_71.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_71.colorable_of_occ_entry HDK3GXV.hD_71 rfl htri h IH

/-- Entry 72, `b9_u.5676565._..5555...` (ring 14, 12 interior vertices). -/
def dEntry_72 : ClaimGlue.DEntry := HK3GXD_72.dEntryOf HDK3GXV.hD_72 rfl

theorem colorable_72 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_72.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_72.colorable_of_occ_entry HDK3GXV.hD_72 rfl htri h IH

/-- Entry 73, `b9_u.5676565._.5.555...` (ring 14, 12 interior vertices). -/
def dEntry_73 : ClaimGlue.DEntry := HK3GXD_73.dEntryOf HDK3GXV.hD_73 rfl

theorem colorable_73 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_73.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_73.colorable_of_occ_entry HDK3GXV.hD_73 rfl htri h IH

/-- Entry 74, `b9_u.5676565._.55.55...` (ring 14, 12 interior vertices). -/
def dEntry_74 : ClaimGlue.DEntry := HK3GXD_74.dEntryOf HDK3GXV.hD_74 rfl

theorem colorable_74 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_74.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_74.colorable_of_occ_entry HDK3GXV.hD_74 rfl htri h IH

/-- Entry 75, `b9_u.5676565._.55555...` (ring 14, 13 interior vertices). -/
def dEntry_75 : ClaimGlue.DEntry := HK3GXD_75.dEntryOf HDK3GXV.hD_75 rfl

theorem colorable_75 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_75.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_75.colorable_of_occ_entry HDK3GXV.hD_75 rfl htri h IH

/-- Entry 76, `b9_u.5676565._55.555...` (ring 14, 13 interior vertices). -/
def dEntry_76 : ClaimGlue.DEntry := HK3GXD_76.dEntryOf HDK3GXV.hD_76 rfl

theorem colorable_76 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_76.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_76.colorable_of_occ_entry HDK3GXV.hD_76 rfl htri h IH

/-- Entry 77, `b9_u.5676565._555.55...` (ring 14, 13 interior vertices). -/
def dEntry_77 : ClaimGlue.DEntry := HK3GXD_77.dEntryOf HDK3GXV.hD_77 rfl

theorem colorable_77 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_77.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_77.colorable_of_occ_entry HDK3GXV.hD_77 rfl htri h IH

/-- Entry 78, `b9_u.5676565._555555...` (ring 14, 14 interior vertices). -/
def dEntry_78 : ClaimGlue.DEntry := HK3GXD_78.dEntryOf HDK3GXV.hD_78 rfl

theorem colorable_78 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 14 → Fin n} (h : HK3GXD_78.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_78.colorable_of_occ_entry HDK3GXV.hD_78 rfl htri h IH

/-- Entry 79, `b9_u75...5656_5...55..5` (ring 14, 11 interior vertices). -/
def dEntry_79 : ClaimGlue.DEntry := HK3GXD_79.dEntryOf HDK3GXV.hD_79 rfl

theorem colorable_79 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_79.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_79.colorable_of_occ_entry HDK3GXV.hD_79 rfl htri h IH

/-- Entry 80, `b9_u75...5656_55..55..5` (ring 14, 12 interior vertices). -/
def dEntry_80 : ClaimGlue.DEntry := HK3GXD_80.dEntryOf HDK3GXV.hD_80 rfl

theorem colorable_80 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_80.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_80.colorable_of_occ_entry HDK3GXV.hD_80 rfl htri h IH

/-- Entry 81, `b9_u75..65656_....55..5` (ring 14, 11 interior vertices). -/
def dEntry_81 : ClaimGlue.DEntry := HK3GXD_81.dEntryOf HDK3GXV.hD_81 rfl

theorem colorable_81 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HK3GXD_81.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_81.colorable_of_occ_entry HDK3GXV.hD_81 rfl htri h IH

/-- Entry 82, `b9_u75..65656_5...55..5` (ring 14, 12 interior vertices). -/
def dEntry_82 : ClaimGlue.DEntry := HK3GXD_82.dEntryOf HDK3GXV.hD_82 rfl

theorem colorable_82 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_82.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_82.colorable_of_occ_entry HDK3GXV.hD_82 rfl htri h IH

/-- Entry 83, `b9_u75..65656_55..55...` (ring 14, 12 interior vertices). -/
def dEntry_83 : ClaimGlue.DEntry := HK3GXD_83.dEntryOf HDK3GXV.hD_83 rfl

theorem colorable_83 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_83.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_83.colorable_of_occ_entry HDK3GXV.hD_83 rfl htri h IH

/-- Entry 84, `b9_u75..65656_55..55..5` (ring 14, 13 interior vertices). -/
def dEntry_84 : ClaimGlue.DEntry := HK3GXD_84.dEntryOf HDK3GXV.hD_84 rfl

theorem colorable_84 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_84.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_84.colorable_of_occ_entry HDK3GXV.hD_84 rfl htri h IH

/-- Entry 85, `b9_u756..5656_55...5..5` (ring 14, 12 interior vertices). -/
def dEntry_85 : ClaimGlue.DEntry := HK3GXD_85.dEntryOf HDK3GXV.hD_85 rfl

theorem colorable_85 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_85.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_85.colorable_of_occ_entry HDK3GXV.hD_85 rfl htri h IH

/-- Entry 86, `b9_u756..5656_55..55...` (ring 14, 12 interior vertices). -/
def dEntry_86 : ClaimGlue.DEntry := HK3GXD_86.dEntryOf HDK3GXV.hD_86 rfl

theorem colorable_86 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HK3GXD_86.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_86.colorable_of_occ_entry HDK3GXV.hD_86 rfl htri h IH

/-- Entry 87, `b9_u756..5656_55..55..5` (ring 14, 13 interior vertices). -/
def dEntry_87 : ClaimGlue.DEntry := HK3GXD_87.dEntryOf HDK3GXV.hD_87 rfl

theorem colorable_87 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_87.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_87.colorable_of_occ_entry HDK3GXV.hD_87 rfl htri h IH

/-- Entry 88, `b9_u756.65656_55..55...` (ring 14, 13 interior vertices). -/
def dEntry_88 : ClaimGlue.DEntry := HK3GXD_88.dEntryOf HDK3GXV.hD_88 rfl

theorem colorable_88 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HK3GXD_88.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_88.colorable_of_occ_entry HDK3GXV.hD_88 rfl htri h IH

/-- Entry 89, `b9_u756.65656_55..55..5` (ring 14, 14 interior vertices). -/
def dEntry_89 : ClaimGlue.DEntry := HK3GXD_89.dEntryOf HDK3GXV.hD_89 rfl

theorem colorable_89 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 14 → Fin n} (h : HK3GXD_89.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3GXD_89.colorable_of_occ_entry HDK3GXV.hD_89 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14, dEntry_15, dEntry_16, dEntry_17, dEntry_18, dEntry_19, dEntry_20, dEntry_21, dEntry_22, dEntry_23, dEntry_24, dEntry_25, dEntry_26, dEntry_27, dEntry_28, dEntry_29, dEntry_30, dEntry_31, dEntry_32, dEntry_33, dEntry_34, dEntry_35, dEntry_36, dEntry_37, dEntry_38, dEntry_39, dEntry_40, dEntry_41, dEntry_42, dEntry_43, dEntry_44, dEntry_45, dEntry_46, dEntry_47, dEntry_48, dEntry_49, dEntry_50, dEntry_51, dEntry_52, dEntry_53, dEntry_54, dEntry_55, dEntry_56, dEntry_57, dEntry_58, dEntry_59, dEntry_60, dEntry_61, dEntry_62, dEntry_63, dEntry_64, dEntry_65, dEntry_66, dEntry_67, dEntry_68, dEntry_69, dEntry_70, dEntry_71, dEntry_72, dEntry_73, dEntry_74, dEntry_75, dEntry_76, dEntry_77, dEntry_78, dEntry_79, dEntry_80, dEntry_81, dEntry_82, dEntry_83, dEntry_84, dEntry_85, dEntry_86, dEntry_87, dEntry_88, dEntry_89]

end HDK3GXOcc

#print axioms HDK3GXOcc.dEntry_0
#print axioms HDK3GXOcc.colorable_0
#print axioms HDK3GXOcc.dEntry_1
#print axioms HDK3GXOcc.colorable_1
#print axioms HDK3GXOcc.dEntry_2
#print axioms HDK3GXOcc.colorable_2
#print axioms HDK3GXOcc.dEntry_3
#print axioms HDK3GXOcc.colorable_3
#print axioms HDK3GXOcc.dEntry_4
#print axioms HDK3GXOcc.colorable_4
#print axioms HDK3GXOcc.dEntry_5
#print axioms HDK3GXOcc.colorable_5
#print axioms HDK3GXOcc.dEntry_6
#print axioms HDK3GXOcc.colorable_6
#print axioms HDK3GXOcc.dEntry_7
#print axioms HDK3GXOcc.colorable_7
#print axioms HDK3GXOcc.dEntry_8
#print axioms HDK3GXOcc.colorable_8
#print axioms HDK3GXOcc.dEntry_9
#print axioms HDK3GXOcc.colorable_9
#print axioms HDK3GXOcc.dEntry_10
#print axioms HDK3GXOcc.colorable_10
#print axioms HDK3GXOcc.dEntry_11
#print axioms HDK3GXOcc.colorable_11
#print axioms HDK3GXOcc.dEntry_12
#print axioms HDK3GXOcc.colorable_12
#print axioms HDK3GXOcc.dEntry_13
#print axioms HDK3GXOcc.colorable_13
#print axioms HDK3GXOcc.dEntry_14
#print axioms HDK3GXOcc.colorable_14
#print axioms HDK3GXOcc.dEntry_15
#print axioms HDK3GXOcc.colorable_15
#print axioms HDK3GXOcc.dEntry_16
#print axioms HDK3GXOcc.colorable_16
#print axioms HDK3GXOcc.dEntry_17
#print axioms HDK3GXOcc.colorable_17
#print axioms HDK3GXOcc.dEntry_18
#print axioms HDK3GXOcc.colorable_18
#print axioms HDK3GXOcc.dEntry_19
#print axioms HDK3GXOcc.colorable_19
#print axioms HDK3GXOcc.dEntry_20
#print axioms HDK3GXOcc.colorable_20
#print axioms HDK3GXOcc.dEntry_21
#print axioms HDK3GXOcc.colorable_21
#print axioms HDK3GXOcc.dEntry_22
#print axioms HDK3GXOcc.colorable_22
#print axioms HDK3GXOcc.dEntry_23
#print axioms HDK3GXOcc.colorable_23
#print axioms HDK3GXOcc.dEntry_24
#print axioms HDK3GXOcc.colorable_24
#print axioms HDK3GXOcc.dEntry_25
#print axioms HDK3GXOcc.colorable_25
#print axioms HDK3GXOcc.dEntry_26
#print axioms HDK3GXOcc.colorable_26
#print axioms HDK3GXOcc.dEntry_27
#print axioms HDK3GXOcc.colorable_27
#print axioms HDK3GXOcc.dEntry_28
#print axioms HDK3GXOcc.colorable_28
#print axioms HDK3GXOcc.dEntry_29
#print axioms HDK3GXOcc.colorable_29
#print axioms HDK3GXOcc.dEntry_30
#print axioms HDK3GXOcc.colorable_30
#print axioms HDK3GXOcc.dEntry_31
#print axioms HDK3GXOcc.colorable_31
#print axioms HDK3GXOcc.dEntry_32
#print axioms HDK3GXOcc.colorable_32
#print axioms HDK3GXOcc.dEntry_33
#print axioms HDK3GXOcc.colorable_33
#print axioms HDK3GXOcc.dEntry_34
#print axioms HDK3GXOcc.colorable_34
#print axioms HDK3GXOcc.dEntry_35
#print axioms HDK3GXOcc.colorable_35
#print axioms HDK3GXOcc.dEntry_36
#print axioms HDK3GXOcc.colorable_36
#print axioms HDK3GXOcc.dEntry_37
#print axioms HDK3GXOcc.colorable_37
#print axioms HDK3GXOcc.dEntry_38
#print axioms HDK3GXOcc.colorable_38
#print axioms HDK3GXOcc.dEntry_39
#print axioms HDK3GXOcc.colorable_39
#print axioms HDK3GXOcc.dEntry_40
#print axioms HDK3GXOcc.colorable_40
#print axioms HDK3GXOcc.dEntry_41
#print axioms HDK3GXOcc.colorable_41
#print axioms HDK3GXOcc.dEntry_42
#print axioms HDK3GXOcc.colorable_42
#print axioms HDK3GXOcc.dEntry_43
#print axioms HDK3GXOcc.colorable_43
#print axioms HDK3GXOcc.dEntry_44
#print axioms HDK3GXOcc.colorable_44
#print axioms HDK3GXOcc.dEntry_45
#print axioms HDK3GXOcc.colorable_45
#print axioms HDK3GXOcc.dEntry_46
#print axioms HDK3GXOcc.colorable_46
#print axioms HDK3GXOcc.dEntry_47
#print axioms HDK3GXOcc.colorable_47
#print axioms HDK3GXOcc.dEntry_48
#print axioms HDK3GXOcc.colorable_48
#print axioms HDK3GXOcc.dEntry_49
#print axioms HDK3GXOcc.colorable_49
#print axioms HDK3GXOcc.dEntry_50
#print axioms HDK3GXOcc.colorable_50
#print axioms HDK3GXOcc.dEntry_51
#print axioms HDK3GXOcc.colorable_51
#print axioms HDK3GXOcc.dEntry_52
#print axioms HDK3GXOcc.colorable_52
#print axioms HDK3GXOcc.dEntry_53
#print axioms HDK3GXOcc.colorable_53
#print axioms HDK3GXOcc.dEntry_54
#print axioms HDK3GXOcc.colorable_54
#print axioms HDK3GXOcc.dEntry_55
#print axioms HDK3GXOcc.colorable_55
#print axioms HDK3GXOcc.dEntry_56
#print axioms HDK3GXOcc.colorable_56
#print axioms HDK3GXOcc.dEntry_57
#print axioms HDK3GXOcc.colorable_57
#print axioms HDK3GXOcc.dEntry_58
#print axioms HDK3GXOcc.colorable_58
#print axioms HDK3GXOcc.dEntry_59
#print axioms HDK3GXOcc.colorable_59
#print axioms HDK3GXOcc.dEntry_60
#print axioms HDK3GXOcc.colorable_60
#print axioms HDK3GXOcc.dEntry_61
#print axioms HDK3GXOcc.colorable_61
#print axioms HDK3GXOcc.dEntry_62
#print axioms HDK3GXOcc.colorable_62
#print axioms HDK3GXOcc.dEntry_63
#print axioms HDK3GXOcc.colorable_63
#print axioms HDK3GXOcc.dEntry_64
#print axioms HDK3GXOcc.colorable_64
#print axioms HDK3GXOcc.dEntry_65
#print axioms HDK3GXOcc.colorable_65
#print axioms HDK3GXOcc.dEntry_66
#print axioms HDK3GXOcc.colorable_66
#print axioms HDK3GXOcc.dEntry_67
#print axioms HDK3GXOcc.colorable_67
#print axioms HDK3GXOcc.dEntry_68
#print axioms HDK3GXOcc.colorable_68
#print axioms HDK3GXOcc.dEntry_69
#print axioms HDK3GXOcc.colorable_69
#print axioms HDK3GXOcc.dEntry_70
#print axioms HDK3GXOcc.colorable_70
#print axioms HDK3GXOcc.dEntry_71
#print axioms HDK3GXOcc.colorable_71
#print axioms HDK3GXOcc.dEntry_72
#print axioms HDK3GXOcc.colorable_72
#print axioms HDK3GXOcc.dEntry_73
#print axioms HDK3GXOcc.colorable_73
#print axioms HDK3GXOcc.dEntry_74
#print axioms HDK3GXOcc.colorable_74
#print axioms HDK3GXOcc.dEntry_75
#print axioms HDK3GXOcc.colorable_75
#print axioms HDK3GXOcc.dEntry_76
#print axioms HDK3GXOcc.colorable_76
#print axioms HDK3GXOcc.dEntry_77
#print axioms HDK3GXOcc.colorable_77
#print axioms HDK3GXOcc.dEntry_78
#print axioms HDK3GXOcc.colorable_78
#print axioms HDK3GXOcc.dEntry_79
#print axioms HDK3GXOcc.colorable_79
#print axioms HDK3GXOcc.dEntry_80
#print axioms HDK3GXOcc.colorable_80
#print axioms HDK3GXOcc.dEntry_81
#print axioms HDK3GXOcc.colorable_81
#print axioms HDK3GXOcc.dEntry_82
#print axioms HDK3GXOcc.colorable_82
#print axioms HDK3GXOcc.dEntry_83
#print axioms HDK3GXOcc.colorable_83
#print axioms HDK3GXOcc.dEntry_84
#print axioms HDK3GXOcc.colorable_84
#print axioms HDK3GXOcc.dEntry_85
#print axioms HDK3GXOcc.colorable_85
#print axioms HDK3GXOcc.dEntry_86
#print axioms HDK3GXOcc.colorable_86
#print axioms HDK3GXOcc.dEntry_87
#print axioms HDK3GXOcc.colorable_87
#print axioms HDK3GXOcc.dEntry_88
#print axioms HDK3GXOcc.colorable_88
#print axioms HDK3GXOcc.dEntry_89
#print axioms HDK3GXOcc.colorable_89
