import RSSTDeg7R783
import RSSTDeg8R783
import RSSTDegHiR783
import RSSTDeg15

/-!
# ST-132: B5 assembled, rotation-aware — 79 parts (71 + N2), kill list K783, `KillsRot` (one common chirality)

d5, d6: the K768 rotation-aware certificates (`cert/cert{5,6}_p79_k768R.txt`; indices < 768 are the same entries in
k783R) replayed against k783R; d7, d8 (`checkDegRotPR`); d9..14 (`checkDegHiR`); d ≥ 15 (`B5_ge15_79`, no kills).
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap

def cert5R783s : String := include_str "cert/cert5_p79_k768R.txt"
def cert6R783s : String := include_str "cert/cert6_p79_k768R.txt"
theorem deg5R783_check : checkDegPR rsstParts79 k783R 5 (parseCert cert5R783s) = true := by native_decide
theorem deg6R783_check : checkDegPR rsstParts79 k783R 6 (parseCert cert6R783s) = true := by native_decide

theorem B5R_79 : ∀ W : UWin, RealShape W → isRotMin W.link = true → 0 < (loHiP rsstParts79 W).2 →
    KillsRot k783R W := by
  intro W hW hrot hpos
  have h5 := hW.1
  by_cases h15 : 15 ≤ W.d
  · exfalso
    have := hiP_le_60_sub_4d slotAll_79 hW (by omega)
    push_cast at this; omega
  interval_cases hd : W.d
  · exact checkDegPR_sound rsstParts79 k783R 5 _ deg5R783_check W hW hd hpos
  · exact checkDegPR_sound rsstParts79 k783R 6 _ deg6R783_check W hW hd hpos
  · exact B5R_deg7 W hW hd hrot hpos
  · exact B5R_deg8 W hW hd hrot hpos
  · exact B5R_deg9 W hW hd hrot hpos
  · exact B5R_deg10 W hW hd hrot hpos
  · exact B5R_deg11 W hW hd hrot hpos
  · exact B5R_deg12 W hW hd hrot hpos
  · exact B5R_deg13 W hW hd hrot hpos
  · exact B5R_deg14 W hW hd hrot hpos

/-- **The RSST seed, rotation-aware**: every `Internally6` triangulation has a vertex `u` and a link listing `w` whose
window word has a rotation-respecting (one chirality) embedding of a K783 configuration. -/
theorem seedR_79 {n : ℕ} {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ KillsRot k783R (wordOf T u w) :=
  seed_of_B5_79 hT (KillsRot k783R) B5R_79

/-- The K783 rotation data is well formed. -/
theorem k783R_wf : k783R.all rotWF = true := by native_decide

#print axioms B5R_79
#print axioms seedR_79
#print axioms k783R_wf

end SimpleGraph.SphericalMap.RSSTSeed
