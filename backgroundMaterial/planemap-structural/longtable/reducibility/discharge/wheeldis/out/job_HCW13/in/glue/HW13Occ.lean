import HW13All
import COccHW3_00
import COccHW3_01
import COccHW3_02

/-! # HW13Occ (Opus, s76_occ502/hcw13, 5 Nov 2026): Studio's C verdicts `HW13V.hC_all` on `CGlue.w13Entries` (job HCW13, main
76761697), as fold-safe registry entries `CEntryF` (`XRData.toCEntryF`, the CC3All pattern), tied to the per-key occurrence
modules `COccHW3_kk` (s74_leanglue/gen_occ_kc.py, face-walk form). `colorable_k` is the per-key C reduction from a rotation
occurrence `Occ`. The `rfl` is `(cEntry k).cf = HW3_kk.cf`: `toCEntryF` keeps `cf := d.cf`, and the two Conf literals are
identical (s76_occ502/scripts/check_literals_c.py: 3 entries, 0 mismatches). -/

open SimpleGraph SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck

namespace HW13Occ

variable {n : ℕ}

/-- The fold-safe C entry `k` of `CGlue.w13Entries`, with Studio's `hC`. -/
def cEntry (k : Fin 3) : CEntryF :=
  (w13Entries.get (k.cast w13Entries_length.symm)).toCEntryF
    (List.all_eq_true.1 w13Entries_ok _ (List.get_mem _ _)) (HW13V.hC_all k)

/-- Entry 0, `b7_u5556677_.....5.` (ring 13, 9 interior vertices). -/
theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HW3_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HW3_00.colorable_of_occ_centry (cEntry 0) rfl htri h IH

/-- The same for an occurrence of the mirror image. -/
theorem colorable_mirror_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 13 → Fin n}
    {int : Fin 9 → Fin n} (h : HW3_00.Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HW3_00.colorable_of_mirror_occ_centry (cEntry 0) rfl htri h IH

/-- Entry 1, `b7_u.557755_...5...` (ring 12, 8 interior vertices). -/
theorem colorable_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : HW3_01.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HW3_01.colorable_of_occ_centry (cEntry 1) rfl htri h IH

/-- The same for an occurrence of the mirror image. -/
theorem colorable_mirror_1 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : HW3_01.Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HW3_01.colorable_of_mirror_occ_centry (cEntry 1) rfl htri h IH

/-- Entry 2, `b7_u.5775.._.555...` (ring 12, 8 interior vertices). -/
theorem colorable_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : HW3_02.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HW3_02.colorable_of_occ_centry (cEntry 2) rfl htri h IH

/-- The same for an occurrence of the mirror image. -/
theorem colorable_mirror_2 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 8 → Fin n} (h : HW3_02.Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HW3_02.colorable_of_mirror_occ_centry (cEntry 2) rfl htri h IH

/-- The batch as a list of C registry entries. -/
def cEntries : List CEntryF := [cEntry 0, cEntry 1, cEntry 2]

end HW13Occ

#print axioms HW13Occ.cEntry
#print axioms HW13Occ.colorable_0
#print axioms HW13Occ.colorable_mirror_0
#print axioms HW13Occ.colorable_1
#print axioms HW13Occ.colorable_mirror_1
#print axioms HW13Occ.colorable_2
#print axioms HW13Occ.colorable_mirror_2
