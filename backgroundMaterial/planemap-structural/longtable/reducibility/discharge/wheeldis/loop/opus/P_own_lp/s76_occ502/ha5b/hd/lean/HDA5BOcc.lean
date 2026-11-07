import HDA5BAll
import COccHA5BD_00
import COccHA5BD_01
import COccHA5BD_02
import COccHA5BD_03
import COccHA5BD_04
import COccHA5BD_05
import COccHA5BD_06
import COccHA5BD_07
import COccHA5BD_08
import COccHA5BD_09
import COccHA5BD_10
import COccHA5BD_11
import COccHA5BD_12
import COccHA5BD_13
import COccHA5BD_14
import COccHA5BD_15
import COccHA5BD_16
import COccHA5BD_17
import COccHA5BD_18
import COccHA5BD_19
import COccHA5BD_20
import COccHA5BD_21
import COccHA5BD_22
import COccHA5BD_23
import COccHA5BD_24
import COccHA5BD_25
import COccHA5BD_26
import COccHA5BD_27
import COccHA5BD_28
import COccHA5BD_29
import COccHA5BD_30
import COccHA5BD_31
import COccHA5BD_32
import COccHA5BD_33
import COccHA5BD_34
import COccHA5BD_35
import COccHA5BD_36
import COccHA5BD_37
import COccHA5BD_38
import COccHA5BD_39
import COccHA5BD_40
import COccHA5BD_41
import COccHA5BD_42
import COccHA5BD_43
import COccHA5BD_44

/-! # HDA5BOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDA5BV.hD_i` on `HDA5B.hda5bConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDA5B.hda5bConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDA5BOcc

variable {n : ℕ}

/-- Entry 0, `tw_d7_w6_0_1978_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HA5BD_00.dEntryOf HDA5BV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_00.colorable_of_occ_entry HDA5BV.hD_0 rfl htri h IH

/-- Entry 1, `tw_d7_w6_0_2033_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HA5BD_01.dEntryOf HDA5BV.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_01.colorable_of_occ_entry HDA5BV.hD_1 rfl htri h IH

/-- Entry 2, `tw_d7_w6_0_2034_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HA5BD_02.dEntryOf HDA5BV.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_02.colorable_of_occ_entry HDA5BV.hD_2 rfl htri h IH

/-- Entry 3, `tw_d7_w6_0_2051_fx_0` (ring 15, 12 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HA5BD_03.dEntryOf HDA5BV.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_03.colorable_of_occ_entry HDA5BV.hD_3 rfl htri h IH

/-- Entry 4, `tw_d7_w7_p1_1031_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HA5BD_04.dEntryOf HDA5BV.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_04.colorable_of_occ_entry HDA5BV.hD_4 rfl htri h IH

/-- Entry 5, `tw_d7_w7_p1_1299_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HA5BD_05.dEntryOf HDA5BV.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_05.colorable_of_occ_entry HDA5BV.hD_5 rfl htri h IH

/-- Entry 6, `tw_d7_w7_p1_237_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HA5BD_06.dEntryOf HDA5BV.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_06.colorable_of_occ_entry HDA5BV.hD_6 rfl htri h IH

/-- Entry 7, `tw_d7_w7_p1_501_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := HA5BD_07.dEntryOf HDA5BV.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_07.colorable_of_occ_entry HDA5BV.hD_7 rfl htri h IH

/-- Entry 8, `tw_d8_w6_0_1242_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := HA5BD_08.dEntryOf HDA5BV.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_08.colorable_of_occ_entry HDA5BV.hD_8 rfl htri h IH

/-- Entry 9, `tw_d8_w6_0_1281_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := HA5BD_09.dEntryOf HDA5BV.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_09.colorable_of_occ_entry HDA5BV.hD_9 rfl htri h IH

/-- Entry 10, `tw_d8_w6_0_1287_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := HA5BD_10.dEntryOf HDA5BV.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_10.colorable_of_occ_entry HDA5BV.hD_10 rfl htri h IH

/-- Entry 11, `tw_d8_w6_0_1294_fx_0` (ring 15, 12 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := HA5BD_11.dEntryOf HDA5BV.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_11.colorable_of_occ_entry HDA5BV.hD_11 rfl htri h IH

/-- Entry 12, `tw_d8_w6_0_136_fx_0` (ring 14, 12 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := HA5BD_12.dEntryOf HDA5BV.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_12.colorable_of_occ_entry HDA5BV.hD_12 rfl htri h IH

/-- Entry 13, `tw_d8_w6_0_137_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := HA5BD_13.dEntryOf HDA5BV.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_13.colorable_of_occ_entry HDA5BV.hD_13 rfl htri h IH

/-- Entry 14, `tw_d8_w6_0_1415_fx_0` (ring 16, 12 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := HA5BD_14.dEntryOf HDA5BV.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 16 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_14.colorable_of_occ_entry HDA5BV.hD_14 rfl htri h IH

/-- Entry 15, `tw_d8_w6_0_1512_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_15 : ClaimGlue.DEntry := HA5BD_15.dEntryOf HDA5BV.hD_15 rfl

theorem colorable_15 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_15.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_15.colorable_of_occ_entry HDA5BV.hD_15 rfl htri h IH

/-- Entry 16, `tw_d8_w6_0_190_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_16 : ClaimGlue.DEntry := HA5BD_16.dEntryOf HDA5BV.hD_16 rfl

theorem colorable_16 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_16.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_16.colorable_of_occ_entry HDA5BV.hD_16 rfl htri h IH

/-- Entry 17, `tw_d8_w6_0_344_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_17 : ClaimGlue.DEntry := HA5BD_17.dEntryOf HDA5BV.hD_17 rfl

theorem colorable_17 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_17.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_17.colorable_of_occ_entry HDA5BV.hD_17 rfl htri h IH

/-- Entry 18, `tw_d8_w6_0_403_fx_0` (ring 14, 12 interior vertices). -/
def dEntry_18 : ClaimGlue.DEntry := HA5BD_18.dEntryOf HDA5BV.hD_18 rfl

theorem colorable_18 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_18.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_18.colorable_of_occ_entry HDA5BV.hD_18 rfl htri h IH

/-- Entry 19, `tw_d8_w6_0_407_fx_0` (ring 15, 13 interior vertices). -/
def dEntry_19 : ClaimGlue.DEntry := HA5BD_19.dEntryOf HDA5BV.hD_19 rfl

theorem colorable_19 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 13 → Fin n} (h : HA5BD_19.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_19.colorable_of_occ_entry HDA5BV.hD_19 rfl htri h IH

/-- Entry 20, `tw_d8_w6_0_413_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_20 : ClaimGlue.DEntry := HA5BD_20.dEntryOf HDA5BV.hD_20 rfl

theorem colorable_20 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_20.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_20.colorable_of_occ_entry HDA5BV.hD_20 rfl htri h IH

/-- Entry 21, `tw_d8_w6_0_512_fx_0` (ring 14, 13 interior vertices). -/
def dEntry_21 : ClaimGlue.DEntry := HA5BD_21.dEntryOf HDA5BV.hD_21 rfl

theorem colorable_21 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HA5BD_21.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_21.colorable_of_occ_entry HDA5BV.hD_21 rfl htri h IH

/-- Entry 22, `tw_d8_w6_0_569_fx_0` (ring 14, 12 interior vertices). -/
def dEntry_22 : ClaimGlue.DEntry := HA5BD_22.dEntryOf HDA5BV.hD_22 rfl

theorem colorable_22 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_22.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_22.colorable_of_occ_entry HDA5BV.hD_22 rfl htri h IH

/-- Entry 23, `tw_d8_w6_0_572_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_23 : ClaimGlue.DEntry := HA5BD_23.dEntryOf HDA5BV.hD_23 rfl

theorem colorable_23 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5BD_23.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_23.colorable_of_occ_entry HDA5BV.hD_23 rfl htri h IH

/-- Entry 24, `tw_d8_w6_0_573_fx_0` (ring 16, 13 interior vertices). -/
def dEntry_24 : ClaimGlue.DEntry := HA5BD_24.dEntryOf HDA5BV.hD_24 rfl

theorem colorable_24 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 16 → Fin n}
    {int : Fin 13 → Fin n} (h : HA5BD_24.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_24.colorable_of_occ_entry HDA5BV.hD_24 rfl htri h IH

/-- Entry 25, `tw_d8_w6_0_610_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_25 : ClaimGlue.DEntry := HA5BD_25.dEntryOf HDA5BV.hD_25 rfl

theorem colorable_25 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_25.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_25.colorable_of_occ_entry HDA5BV.hD_25 rfl htri h IH

/-- Entry 26, `tw_d8_w6_0_67_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_26 : ClaimGlue.DEntry := HA5BD_26.dEntryOf HDA5BV.hD_26 rfl

theorem colorable_26 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_26.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_26.colorable_of_occ_entry HDA5BV.hD_26 rfl htri h IH

/-- Entry 27, `tw_d8_w6_0_69_fx_0` (ring 16, 14 interior vertices). -/
def dEntry_27 : ClaimGlue.DEntry := HA5BD_27.dEntryOf HDA5BV.hD_27 rfl

theorem colorable_27 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 16 → Fin n}
    {int : Fin 14 → Fin n} (h : HA5BD_27.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_27.colorable_of_occ_entry HDA5BV.hD_27 rfl htri h IH

/-- Entry 28, `tw_d8_w6_0_70_fx_0` (ring 16, 13 interior vertices). -/
def dEntry_28 : ClaimGlue.DEntry := HA5BD_28.dEntryOf HDA5BV.hD_28 rfl

theorem colorable_28 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 16 → Fin n}
    {int : Fin 13 → Fin n} (h : HA5BD_28.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_28.colorable_of_occ_entry HDA5BV.hD_28 rfl htri h IH

/-- Entry 29, `tw_d8_w7_p1_177_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_29 : ClaimGlue.DEntry := HA5BD_29.dEntryOf HDA5BV.hD_29 rfl

theorem colorable_29 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_29.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_29.colorable_of_occ_entry HDA5BV.hD_29 rfl htri h IH

/-- Entry 30, `tw_d8_w7_p1_179_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_30 : ClaimGlue.DEntry := HA5BD_30.dEntryOf HDA5BV.hD_30 rfl

theorem colorable_30 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_30.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_30.colorable_of_occ_entry HDA5BV.hD_30 rfl htri h IH

/-- Entry 31, `tw_d8_w7_p1_265_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_31 : ClaimGlue.DEntry := HA5BD_31.dEntryOf HDA5BV.hD_31 rfl

theorem colorable_31 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_31.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_31.colorable_of_occ_entry HDA5BV.hD_31 rfl htri h IH

/-- Entry 32, `tw_d8_w7_p1_330_fx_0` (ring 16, 12 interior vertices). -/
def dEntry_32 : ClaimGlue.DEntry := HA5BD_32.dEntryOf HDA5BV.hD_32 rfl

theorem colorable_32 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 16 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_32.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_32.colorable_of_occ_entry HDA5BV.hD_32 rfl htri h IH

/-- Entry 33, `tw_d8_w7_p1_400_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_33 : ClaimGlue.DEntry := HA5BD_33.dEntryOf HDA5BV.hD_33 rfl

theorem colorable_33 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_33.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_33.colorable_of_occ_entry HDA5BV.hD_33 rfl htri h IH

/-- Entry 34, `tw_d8_w7_p1_402_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_34 : ClaimGlue.DEntry := HA5BD_34.dEntryOf HDA5BV.hD_34 rfl

theorem colorable_34 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_34.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_34.colorable_of_occ_entry HDA5BV.hD_34 rfl htri h IH

/-- Entry 35, `tw_d8_w7_p1_404_fx_0` (ring 14, 13 interior vertices). -/
def dEntry_35 : ClaimGlue.DEntry := HA5BD_35.dEntryOf HDA5BV.hD_35 rfl

theorem colorable_35 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 13 → Fin n} (h : HA5BD_35.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_35.colorable_of_occ_entry HDA5BV.hD_35 rfl htri h IH

/-- Entry 36, `tw_d8_w7_p1_419_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_36 : ClaimGlue.DEntry := HA5BD_36.dEntryOf HDA5BV.hD_36 rfl

theorem colorable_36 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_36.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_36.colorable_of_occ_entry HDA5BV.hD_36 rfl htri h IH

/-- Entry 37, `tw_d8_w7_p1_423_fx_0` (ring 15, 12 interior vertices). -/
def dEntry_37 : ClaimGlue.DEntry := HA5BD_37.dEntryOf HDA5BV.hD_37 rfl

theorem colorable_37 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_37.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_37.colorable_of_occ_entry HDA5BV.hD_37 rfl htri h IH

/-- Entry 38, `tw_d8_w7_p1_425_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_38 : ClaimGlue.DEntry := HA5BD_38.dEntryOf HDA5BV.hD_38 rfl

theorem colorable_38 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_38.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_38.colorable_of_occ_entry HDA5BV.hD_38 rfl htri h IH

/-- Entry 39, `tw_d8_w7_p1_43_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_39 : ClaimGlue.DEntry := HA5BD_39.dEntryOf HDA5BV.hD_39 rfl

theorem colorable_39 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_39.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_39.colorable_of_occ_entry HDA5BV.hD_39 rfl htri h IH

/-- Entry 40, `tw_d8_w7_p1_593_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_40 : ClaimGlue.DEntry := HA5BD_40.dEntryOf HDA5BV.hD_40 rfl

theorem colorable_40 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_40.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_40.colorable_of_occ_entry HDA5BV.hD_40 rfl htri h IH

/-- Entry 41, `tw_d8_w7_p1_621_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_41 : ClaimGlue.DEntry := HA5BD_41.dEntryOf HDA5BV.hD_41 rfl

theorem colorable_41 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_41.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_41.colorable_of_occ_entry HDA5BV.hD_41 rfl htri h IH

/-- Entry 42, `tw_d8_w7_p1_693_fx_0` (ring 15, 12 interior vertices). -/
def dEntry_42 : ClaimGlue.DEntry := HA5BD_42.dEntryOf HDA5BV.hD_42 rfl

theorem colorable_42 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_42.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_42.colorable_of_occ_entry HDA5BV.hD_42 rfl htri h IH

/-- Entry 43, `tw_d8_w7_p1_725_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_43 : ClaimGlue.DEntry := HA5BD_43.dEntryOf HDA5BV.hD_43 rfl

theorem colorable_43 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5BD_43.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_43.colorable_of_occ_entry HDA5BV.hD_43 rfl htri h IH

/-- Entry 44, `tw_d8_w7_p1_729_fx_0` (ring 15, 12 interior vertices). -/
def dEntry_44 : ClaimGlue.DEntry := HA5BD_44.dEntryOf HDA5BV.hD_44 rfl

theorem colorable_44 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5BD_44.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5BD_44.colorable_of_occ_entry HDA5BV.hD_44 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14, dEntry_15, dEntry_16, dEntry_17, dEntry_18, dEntry_19, dEntry_20, dEntry_21, dEntry_22, dEntry_23, dEntry_24, dEntry_25, dEntry_26, dEntry_27, dEntry_28, dEntry_29, dEntry_30, dEntry_31, dEntry_32, dEntry_33, dEntry_34, dEntry_35, dEntry_36, dEntry_37, dEntry_38, dEntry_39, dEntry_40, dEntry_41, dEntry_42, dEntry_43, dEntry_44]

end HDA5BOcc

#print axioms HDA5BOcc.dEntry_0
#print axioms HDA5BOcc.colorable_0
#print axioms HDA5BOcc.dEntry_1
#print axioms HDA5BOcc.colorable_1
#print axioms HDA5BOcc.dEntry_2
#print axioms HDA5BOcc.colorable_2
#print axioms HDA5BOcc.dEntry_3
#print axioms HDA5BOcc.colorable_3
#print axioms HDA5BOcc.dEntry_4
#print axioms HDA5BOcc.colorable_4
#print axioms HDA5BOcc.dEntry_5
#print axioms HDA5BOcc.colorable_5
#print axioms HDA5BOcc.dEntry_6
#print axioms HDA5BOcc.colorable_6
#print axioms HDA5BOcc.dEntry_7
#print axioms HDA5BOcc.colorable_7
#print axioms HDA5BOcc.dEntry_8
#print axioms HDA5BOcc.colorable_8
#print axioms HDA5BOcc.dEntry_9
#print axioms HDA5BOcc.colorable_9
#print axioms HDA5BOcc.dEntry_10
#print axioms HDA5BOcc.colorable_10
#print axioms HDA5BOcc.dEntry_11
#print axioms HDA5BOcc.colorable_11
#print axioms HDA5BOcc.dEntry_12
#print axioms HDA5BOcc.colorable_12
#print axioms HDA5BOcc.dEntry_13
#print axioms HDA5BOcc.colorable_13
#print axioms HDA5BOcc.dEntry_14
#print axioms HDA5BOcc.colorable_14
#print axioms HDA5BOcc.dEntry_15
#print axioms HDA5BOcc.colorable_15
#print axioms HDA5BOcc.dEntry_16
#print axioms HDA5BOcc.colorable_16
#print axioms HDA5BOcc.dEntry_17
#print axioms HDA5BOcc.colorable_17
#print axioms HDA5BOcc.dEntry_18
#print axioms HDA5BOcc.colorable_18
#print axioms HDA5BOcc.dEntry_19
#print axioms HDA5BOcc.colorable_19
#print axioms HDA5BOcc.dEntry_20
#print axioms HDA5BOcc.colorable_20
#print axioms HDA5BOcc.dEntry_21
#print axioms HDA5BOcc.colorable_21
#print axioms HDA5BOcc.dEntry_22
#print axioms HDA5BOcc.colorable_22
#print axioms HDA5BOcc.dEntry_23
#print axioms HDA5BOcc.colorable_23
#print axioms HDA5BOcc.dEntry_24
#print axioms HDA5BOcc.colorable_24
#print axioms HDA5BOcc.dEntry_25
#print axioms HDA5BOcc.colorable_25
#print axioms HDA5BOcc.dEntry_26
#print axioms HDA5BOcc.colorable_26
#print axioms HDA5BOcc.dEntry_27
#print axioms HDA5BOcc.colorable_27
#print axioms HDA5BOcc.dEntry_28
#print axioms HDA5BOcc.colorable_28
#print axioms HDA5BOcc.dEntry_29
#print axioms HDA5BOcc.colorable_29
#print axioms HDA5BOcc.dEntry_30
#print axioms HDA5BOcc.colorable_30
#print axioms HDA5BOcc.dEntry_31
#print axioms HDA5BOcc.colorable_31
#print axioms HDA5BOcc.dEntry_32
#print axioms HDA5BOcc.colorable_32
#print axioms HDA5BOcc.dEntry_33
#print axioms HDA5BOcc.colorable_33
#print axioms HDA5BOcc.dEntry_34
#print axioms HDA5BOcc.colorable_34
#print axioms HDA5BOcc.dEntry_35
#print axioms HDA5BOcc.colorable_35
#print axioms HDA5BOcc.dEntry_36
#print axioms HDA5BOcc.colorable_36
#print axioms HDA5BOcc.dEntry_37
#print axioms HDA5BOcc.colorable_37
#print axioms HDA5BOcc.dEntry_38
#print axioms HDA5BOcc.colorable_38
#print axioms HDA5BOcc.dEntry_39
#print axioms HDA5BOcc.colorable_39
#print axioms HDA5BOcc.dEntry_40
#print axioms HDA5BOcc.colorable_40
#print axioms HDA5BOcc.dEntry_41
#print axioms HDA5BOcc.colorable_41
#print axioms HDA5BOcc.dEntry_42
#print axioms HDA5BOcc.colorable_42
#print axioms HDA5BOcc.dEntry_43
#print axioms HDA5BOcc.colorable_43
#print axioms HDA5BOcc.dEntry_44
#print axioms HDA5BOcc.colorable_44
