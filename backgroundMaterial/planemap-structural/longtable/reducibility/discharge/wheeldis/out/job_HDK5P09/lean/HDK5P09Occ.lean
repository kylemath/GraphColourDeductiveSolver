import HDK5P09All
import COccHK5P09D_00

/-! # HDK5P09Occ (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK5P09V.hD_i` on `HDK5P09.hdk5p09Confs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK5P09.hdk5p09Confs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK5P09Occ

variable {n : ℕ}

/-- Entry 0, `b9_u555557557_.....676.` (ring 15, 13 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK5P09D_00.dEntryOf HDK5P09V.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 15 → Fin n}
    {int : Fin 13 → Fin n} (h : HK5P09D_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK5P09D_00.colorable_of_occ_entry HDK5P09V.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK5P09Occ

#print axioms HDK5P09Occ.dEntry_0
#print axioms HDK5P09Occ.colorable_0
