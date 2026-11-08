import HDK3CAll
import COccHK3CD_00

/-! # HDK3COcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK3CV.hD_i` on `HDK3C.hdk3cConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK3C.hdk3cConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK3COcc

variable {n : ℕ}

/-- Entry 0, `b8_u...56556_...5.66.` (ring 12, 9 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK3CD_00.dEntryOf HDK3CV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 12 → Fin n}
    {int : Fin 9 → Fin n} (h : HK3CD_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3CD_00.colorable_of_occ_entry HDK3CV.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK3COcc

#print axioms HDK3COcc.dEntry_0
#print axioms HDK3COcc.colorable_0
