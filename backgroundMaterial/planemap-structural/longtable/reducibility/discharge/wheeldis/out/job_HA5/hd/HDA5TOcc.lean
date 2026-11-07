import HDA5TAll
import COccHA5D_00
import COccHA5D_01
import COccHA5D_02
import COccHA5D_03
import COccHA5D_04
import COccHA5D_05
import COccHA5D_06
import COccHA5D_07
import COccHA5D_08
import COccHA5D_09
import COccHA5D_10
import COccHA5D_11
import COccHA5D_12
import COccHA5D_13
import COccHA5D_14
import COccHA5D_15
import COccHA5D_16
import COccHA5D_17
import COccHA5D_18
import COccHA5D_19
import COccHA5D_20
import COccHA5D_21
import COccHA5D_22
import COccHA5D_23
import COccHA5D_24
import COccHA5D_25
import COccHA5D_26
import COccHA5D_27
import COccHA5D_28
import COccHA5D_29
import COccHA5D_30
import COccHA5D_31
import COccHA5D_32
import COccHA5D_33
import COccHA5D_34

/-! # HDA5TOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDA5TV.hD_i` on `HDA5T.hda5tConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDA5T.hda5tConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDA5TOcc

variable {n : ℕ}

/-- Entry 0, `tw_d7_w6_0_16_fx_0` (ring 12, 10 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HA5D_00.dEntryOf HDA5TV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_00.colorable_of_occ_entry HDA5TV.hD_0 rfl htri h IH

/-- Entry 1, `tw_d7_w6_0_190_fx_0` (ring 13, 9 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := HA5D_01.dEntryOf HDA5TV.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HA5D_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_01.colorable_of_occ_entry HDA5TV.hD_1 rfl htri h IH

/-- Entry 2, `tw_d7_w6_0_191_fx_0` (ring 13, 9 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := HA5D_02.dEntryOf HDA5TV.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HA5D_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_02.colorable_of_occ_entry HDA5TV.hD_2 rfl htri h IH

/-- Entry 3, `tw_d7_w6_0_28_fx_0` (ring 13, 11 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := HA5D_03.dEntryOf HDA5TV.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_03.colorable_of_occ_entry HDA5TV.hD_3 rfl htri h IH

/-- Entry 4, `tw_d7_w6_0_29_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := HA5D_04.dEntryOf HDA5TV.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_04.colorable_of_occ_entry HDA5TV.hD_4 rfl htri h IH

/-- Entry 5, `tw_d7_w6_0_31_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := HA5D_05.dEntryOf HDA5TV.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_05.colorable_of_occ_entry HDA5TV.hD_5 rfl htri h IH

/-- Entry 6, `tw_d7_w6_0_38_fx_0` (ring 12, 10 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := HA5D_06.dEntryOf HDA5TV.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_06.colorable_of_occ_entry HDA5TV.hD_6 rfl htri h IH

/-- Entry 7, `tw_d7_w6_0_474_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := HA5D_07.dEntryOf HDA5TV.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_07.colorable_of_occ_entry HDA5TV.hD_7 rfl htri h IH

/-- Entry 8, `tw_d7_w6_0_477_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := HA5D_08.dEntryOf HDA5TV.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_08.colorable_of_occ_entry HDA5TV.hD_8 rfl htri h IH

/-- Entry 9, `tw_d7_w6_0_659_fx_0` (ring 14, 10 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := HA5D_09.dEntryOf HDA5TV.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_09.colorable_of_occ_entry HDA5TV.hD_9 rfl htri h IH

/-- Entry 10, `tw_d7_w6_0_662_fx_0` (ring 13, 9 interior vertices). -/
def dEntry_10 : ClaimGlue.DEntry := HA5D_10.dEntryOf HDA5TV.hD_10 rfl

theorem colorable_10 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HA5D_10.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_10.colorable_of_occ_entry HDA5TV.hD_10 rfl htri h IH

/-- Entry 11, `tw_d7_w6_0_683_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_11 : ClaimGlue.DEntry := HA5D_11.dEntryOf HDA5TV.hD_11 rfl

theorem colorable_11 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_11.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_11.colorable_of_occ_entry HDA5TV.hD_11 rfl htri h IH

/-- Entry 12, `tw_d7_w6_0_689_fx_0` (ring 14, 11 interior vertices). -/
def dEntry_12 : ClaimGlue.DEntry := HA5D_12.dEntryOf HDA5TV.hD_12 rfl

theorem colorable_12 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_12.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_12.colorable_of_occ_entry HDA5TV.hD_12 rfl htri h IH

/-- Entry 13, `tw_d7_w6_0_733_fx_0` (ring 14, 9 interior vertices). -/
def dEntry_13 : ClaimGlue.DEntry := HA5D_13.dEntryOf HDA5TV.hD_13 rfl

theorem colorable_13 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 9 → Fin n} (h : HA5D_13.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_13.colorable_of_occ_entry HDA5TV.hD_13 rfl htri h IH

/-- Entry 14, `tw_d7_w6_0_99_fx_0` (ring 13, 11 interior vertices). -/
def dEntry_14 : ClaimGlue.DEntry := HA5D_14.dEntryOf HDA5TV.hD_14 rfl

theorem colorable_14 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_14.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_14.colorable_of_occ_entry HDA5TV.hD_14 rfl htri h IH

/-- Entry 15, `tw_d7_w7_p1_236_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_15 : ClaimGlue.DEntry := HA5D_15.dEntryOf HDA5TV.hD_15 rfl

theorem colorable_15 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_15.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_15.colorable_of_occ_entry HDA5TV.hD_15 rfl htri h IH

/-- Entry 16, `tw_d7_w7_p1_478_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_16 : ClaimGlue.DEntry := HA5D_16.dEntryOf HDA5TV.hD_16 rfl

theorem colorable_16 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_16.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_16.colorable_of_occ_entry HDA5TV.hD_16 rfl htri h IH

/-- Entry 17, `tw_d7_w7_p1_496_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_17 : ClaimGlue.DEntry := HA5D_17.dEntryOf HDA5TV.hD_17 rfl

theorem colorable_17 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_17.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_17.colorable_of_occ_entry HDA5TV.hD_17 rfl htri h IH

/-- Entry 18, `tw_d7_w7_p1_524_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_18 : ClaimGlue.DEntry := HA5D_18.dEntryOf HDA5TV.hD_18 rfl

theorem colorable_18 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_18.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_18.colorable_of_occ_entry HDA5TV.hD_18 rfl htri h IH

/-- Entry 19, `tw_d7_w7_p1_69_fx_0` (ring 13, 11 interior vertices). -/
def dEntry_19 : ClaimGlue.DEntry := HA5D_19.dEntryOf HDA5TV.hD_19 rfl

theorem colorable_19 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_19.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_19.colorable_of_occ_entry HDA5TV.hD_19 rfl htri h IH

/-- Entry 20, `tw_d8_w6_0_21_fx_0` (ring 13, 9 interior vertices). -/
def dEntry_20 : ClaimGlue.DEntry := HA5D_20.dEntryOf HDA5TV.hD_20 rfl

theorem colorable_20 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HA5D_20.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_20.colorable_of_occ_entry HDA5TV.hD_20 rfl htri h IH

/-- Entry 21, `tw_d8_w6_0_329_fx_0` (ring 12, 11 interior vertices). -/
def dEntry_21 : ClaimGlue.DEntry := HA5D_21.dEntryOf HDA5TV.hD_21 rfl

theorem colorable_21 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_21.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_21.colorable_of_occ_entry HDA5TV.hD_21 rfl htri h IH

/-- Entry 22, `tw_d8_w6_0_343_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_22 : ClaimGlue.DEntry := HA5D_22.dEntryOf HDA5TV.hD_22 rfl

theorem colorable_22 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_22.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_22.colorable_of_occ_entry HDA5TV.hD_22 rfl htri h IH

/-- Entry 23, `tw_d8_w6_0_362_fx_0` (ring 13, 12 interior vertices). -/
def dEntry_23 : ClaimGlue.DEntry := HA5D_23.dEntryOf HDA5TV.hD_23 rfl

theorem colorable_23 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5D_23.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_23.colorable_of_occ_entry HDA5TV.hD_23 rfl htri h IH

/-- Entry 24, `tw_d8_w6_0_363_fx_0` (ring 13, 12 interior vertices). -/
def dEntry_24 : ClaimGlue.DEntry := HA5D_24.dEntryOf HDA5TV.hD_24 rfl

theorem colorable_24 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : HA5D_24.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_24.colorable_of_occ_entry HDA5TV.hD_24 rfl htri h IH

/-- Entry 25, `tw_d8_w6_0_88_fx_0` (ring 13, 11 interior vertices). -/
def dEntry_25 : ClaimGlue.DEntry := HA5D_25.dEntryOf HDA5TV.hD_25 rfl

theorem colorable_25 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_25.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_25.colorable_of_occ_entry HDA5TV.hD_25 rfl htri h IH

/-- Entry 26, `tw_d8_w6_0_93_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_26 : ClaimGlue.DEntry := HA5D_26.dEntryOf HDA5TV.hD_26 rfl

theorem colorable_26 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_26.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_26.colorable_of_occ_entry HDA5TV.hD_26 rfl htri h IH

/-- Entry 27, `tw_d8_w7_p1_129_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_27 : ClaimGlue.DEntry := HA5D_27.dEntryOf HDA5TV.hD_27 rfl

theorem colorable_27 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_27.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_27.colorable_of_occ_entry HDA5TV.hD_27 rfl htri h IH

/-- Entry 28, `tw_d8_w7_p1_145_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_28 : ClaimGlue.DEntry := HA5D_28.dEntryOf HDA5TV.hD_28 rfl

theorem colorable_28 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_28.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_28.colorable_of_occ_entry HDA5TV.hD_28 rfl htri h IH

/-- Entry 29, `tw_d8_w7_p1_175_fx_0` (ring 13, 10 interior vertices). -/
def dEntry_29 : ClaimGlue.DEntry := HA5D_29.dEntryOf HDA5TV.hD_29 rfl

theorem colorable_29 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : HA5D_29.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_29.colorable_of_occ_entry HDA5TV.hD_29 rfl htri h IH

/-- Entry 30, `tw_d8_w7_p1_176_fx_0` (ring 13, 11 interior vertices). -/
def dEntry_30 : ClaimGlue.DEntry := HA5D_30.dEntryOf HDA5TV.hD_30 rfl

theorem colorable_30 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_30.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_30.colorable_of_occ_entry HDA5TV.hD_30 rfl htri h IH

/-- Entry 31, `tw_d8_w7_p1_294_fx_0` (ring 13, 11 interior vertices). -/
def dEntry_31 : ClaimGlue.DEntry := HA5D_31.dEntryOf HDA5TV.hD_31 rfl

theorem colorable_31 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_31.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_31.colorable_of_occ_entry HDA5TV.hD_31 rfl htri h IH

/-- Entry 32, `tw_d9_w6_0_67_fx_0` (ring 11, 8 interior vertices). -/
def dEntry_32 : ClaimGlue.DEntry := HA5D_32.dEntryOf HDA5TV.hD_32 rfl

theorem colorable_32 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 11 → Fin n}
    {int : Fin 8 → Fin n} (h : HA5D_32.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_32.colorable_of_occ_entry HDA5TV.hD_32 rfl htri h IH

/-- Entry 33, `tw_d9_w6_0_68_fx_0` (ring 12, 9 interior vertices). -/
def dEntry_33 : ClaimGlue.DEntry := HA5D_33.dEntryOf HDA5TV.hD_33 rfl

theorem colorable_33 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HA5D_33.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_33.colorable_of_occ_entry HDA5TV.hD_33 rfl htri h IH

/-- Entry 34, `tw_d7_w7_m1_1133_fx_0` (ring 15, 11 interior vertices). -/
def dEntry_34 : ClaimGlue.DEntry := HA5D_34.dEntryOf HDA5TV.hD_34 rfl

theorem colorable_34 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 11 → Fin n} (h : HA5D_34.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HA5D_34.colorable_of_occ_entry HDA5TV.hD_34 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9, dEntry_10, dEntry_11, dEntry_12, dEntry_13, dEntry_14, dEntry_15, dEntry_16, dEntry_17, dEntry_18, dEntry_19, dEntry_20, dEntry_21, dEntry_22, dEntry_23, dEntry_24, dEntry_25, dEntry_26, dEntry_27, dEntry_28, dEntry_29, dEntry_30, dEntry_31, dEntry_32, dEntry_33, dEntry_34]

end HDA5TOcc

#print axioms HDA5TOcc.dEntry_0
#print axioms HDA5TOcc.colorable_0
#print axioms HDA5TOcc.dEntry_1
#print axioms HDA5TOcc.colorable_1
#print axioms HDA5TOcc.dEntry_2
#print axioms HDA5TOcc.colorable_2
#print axioms HDA5TOcc.dEntry_3
#print axioms HDA5TOcc.colorable_3
#print axioms HDA5TOcc.dEntry_4
#print axioms HDA5TOcc.colorable_4
#print axioms HDA5TOcc.dEntry_5
#print axioms HDA5TOcc.colorable_5
#print axioms HDA5TOcc.dEntry_6
#print axioms HDA5TOcc.colorable_6
#print axioms HDA5TOcc.dEntry_7
#print axioms HDA5TOcc.colorable_7
#print axioms HDA5TOcc.dEntry_8
#print axioms HDA5TOcc.colorable_8
#print axioms HDA5TOcc.dEntry_9
#print axioms HDA5TOcc.colorable_9
#print axioms HDA5TOcc.dEntry_10
#print axioms HDA5TOcc.colorable_10
#print axioms HDA5TOcc.dEntry_11
#print axioms HDA5TOcc.colorable_11
#print axioms HDA5TOcc.dEntry_12
#print axioms HDA5TOcc.colorable_12
#print axioms HDA5TOcc.dEntry_13
#print axioms HDA5TOcc.colorable_13
#print axioms HDA5TOcc.dEntry_14
#print axioms HDA5TOcc.colorable_14
#print axioms HDA5TOcc.dEntry_15
#print axioms HDA5TOcc.colorable_15
#print axioms HDA5TOcc.dEntry_16
#print axioms HDA5TOcc.colorable_16
#print axioms HDA5TOcc.dEntry_17
#print axioms HDA5TOcc.colorable_17
#print axioms HDA5TOcc.dEntry_18
#print axioms HDA5TOcc.colorable_18
#print axioms HDA5TOcc.dEntry_19
#print axioms HDA5TOcc.colorable_19
#print axioms HDA5TOcc.dEntry_20
#print axioms HDA5TOcc.colorable_20
#print axioms HDA5TOcc.dEntry_21
#print axioms HDA5TOcc.colorable_21
#print axioms HDA5TOcc.dEntry_22
#print axioms HDA5TOcc.colorable_22
#print axioms HDA5TOcc.dEntry_23
#print axioms HDA5TOcc.colorable_23
#print axioms HDA5TOcc.dEntry_24
#print axioms HDA5TOcc.colorable_24
#print axioms HDA5TOcc.dEntry_25
#print axioms HDA5TOcc.colorable_25
#print axioms HDA5TOcc.dEntry_26
#print axioms HDA5TOcc.colorable_26
#print axioms HDA5TOcc.dEntry_27
#print axioms HDA5TOcc.colorable_27
#print axioms HDA5TOcc.dEntry_28
#print axioms HDA5TOcc.colorable_28
#print axioms HDA5TOcc.dEntry_29
#print axioms HDA5TOcc.colorable_29
#print axioms HDA5TOcc.dEntry_30
#print axioms HDA5TOcc.colorable_30
#print axioms HDA5TOcc.dEntry_31
#print axioms HDA5TOcc.colorable_31
#print axioms HDA5TOcc.dEntry_32
#print axioms HDA5TOcc.colorable_32
#print axioms HDA5TOcc.dEntry_33
#print axioms HDA5TOcc.colorable_33
#print axioms HDA5TOcc.dEntry_34
#print axioms HDA5TOcc.colorable_34
