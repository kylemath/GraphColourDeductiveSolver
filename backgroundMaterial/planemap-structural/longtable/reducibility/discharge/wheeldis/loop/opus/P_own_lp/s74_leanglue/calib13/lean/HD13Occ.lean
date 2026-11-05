import HD13All
import COccH13_00
import COccH13_01
import COccH13_02
import COccH13_03
import COccH13_04
import COccH13_05
import COccH13_06
import COccH13_07
import COccH13_08
import COccH13_09

/-! # HD13Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HD13V.hD_i` on `HD13.hd13Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HD13.hd13Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HD13Occ

variable {n : ℕ}

/-- Entry 0, `rsst105_482o611` (ring 13, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := H13_00.dEntryOf HD13V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : H13_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_00.colorable_of_occ_entry HD13V.hD_0 rfl htri h IH

/-- Entry 1, `rsst219_2o226173962` (ring 13, 9 interior vertices). -/
def dEntry_1 : ClaimGlue.DEntry := H13_01.dEntryOf HD13V.hD_1 rfl

theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : H13_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_01.colorable_of_occ_entry HD13V.hD_1 rfl htri h IH

/-- Entry 2, `rsst275_1322o1028` (ring 13, 9 interior vertices). -/
def dEntry_2 : ClaimGlue.DEntry := H13_02.dEntryOf HD13V.hD_2 rfl

theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : H13_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_02.colorable_of_occ_entry HD13V.hD_2 rfl htri h IH

/-- Entry 3, `rsst383_7322o611` (ring 13, 9 interior vertices). -/
def dEntry_3 : ClaimGlue.DEntry := H13_03.dEntryOf HD13V.hD_3 rfl

theorem colorable_3 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : H13_03.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_03.colorable_of_occ_entry HD13V.hD_3 rfl htri h IH

/-- Entry 4, `nl0245_r13` (ring 13, 10 interior vertices). -/
def dEntry_4 : ClaimGlue.DEntry := H13_04.dEntryOf HD13V.hD_4 rfl

theorem colorable_4 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : H13_04.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_04.colorable_of_occ_entry HD13V.hD_4 rfl htri h IH

/-- Entry 5, `nl0417_r13` (ring 13, 10 interior vertices). -/
def dEntry_5 : ClaimGlue.DEntry := H13_05.dEntryOf HD13V.hD_5 rfl

theorem colorable_5 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 10 → Fin n} (h : H13_05.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_05.colorable_of_occ_entry HD13V.hD_5 rfl htri h IH

/-- Entry 6, `nl0250_r13` (ring 13, 11 interior vertices). -/
def dEntry_6 : ClaimGlue.DEntry := H13_06.dEntryOf HD13V.hD_6 rfl

theorem colorable_6 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : H13_06.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_06.colorable_of_occ_entry HD13V.hD_6 rfl htri h IH

/-- Entry 7, `nl0567_r13` (ring 13, 11 interior vertices). -/
def dEntry_7 : ClaimGlue.DEntry := H13_07.dEntryOf HD13V.hD_7 rfl

theorem colorable_7 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 11 → Fin n} (h : H13_07.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_07.colorable_of_occ_entry HD13V.hD_7 rfl htri h IH

/-- Entry 8, `nl2179_r13` (ring 13, 12 interior vertices). -/
def dEntry_8 : ClaimGlue.DEntry := H13_08.dEntryOf HD13V.hD_8 rfl

theorem colorable_8 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : H13_08.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_08.colorable_of_occ_entry HD13V.hD_8 rfl htri h IH

/-- Entry 9, `nl2180_r13` (ring 13, 12 interior vertices). -/
def dEntry_9 : ClaimGlue.DEntry := H13_09.dEntryOf HD13V.hD_9 rfl

theorem colorable_9 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 12 → Fin n} (h : H13_09.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  H13_09.colorable_of_occ_entry HD13V.hD_9 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0, dEntry_1, dEntry_2, dEntry_3, dEntry_4, dEntry_5, dEntry_6, dEntry_7, dEntry_8, dEntry_9]

end HD13Occ

#print axioms HD13Occ.dEntry_0
#print axioms HD13Occ.colorable_0
#print axioms HD13Occ.dEntry_1
#print axioms HD13Occ.colorable_1
#print axioms HD13Occ.dEntry_2
#print axioms HD13Occ.colorable_2
#print axioms HD13Occ.dEntry_3
#print axioms HD13Occ.colorable_3
#print axioms HD13Occ.dEntry_4
#print axioms HD13Occ.colorable_4
#print axioms HD13Occ.dEntry_5
#print axioms HD13Occ.colorable_5
#print axioms HD13Occ.dEntry_6
#print axioms HD13Occ.colorable_6
#print axioms HD13Occ.dEntry_7
#print axioms HD13Occ.colorable_7
#print axioms HD13Occ.dEntry_8
#print axioms HD13Occ.colorable_8
#print axioms HD13Occ.dEntry_9
#print axioms HD13Occ.colorable_9
