import HDK3BAll
import COccHK3BD_00

/-! # HDK3BOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `HDK3BV.hD_i` on `HDK3B.hdk3bConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `HDK3B.hdk3bConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace HDK3BOcc

variable {n : ℕ}

/-- Entry 0, `b8_u.5665675_.....55.` (ring 14, 10 interior vertices). -/
def dEntry_0 : ClaimGlue.DEntry := HK3BD_00.dEntryOf HDK3BV.hD_0 rfl

theorem colorable_0 {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 14 → Fin n}
    {int : Fin 10 → Fin n} (h : HK3BD_00.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  HK3BD_00.colorable_of_occ_entry HDK3BV.hD_0 rfl htri h IH

/-- The batch as a list of D registry entries. -/
def dEntries : List ClaimGlue.DEntry := [dEntry_0]

end HDK3BOcc

#print axioms HDK3BOcc.dEntry_0
#print axioms HDK3BOcc.colorable_0
