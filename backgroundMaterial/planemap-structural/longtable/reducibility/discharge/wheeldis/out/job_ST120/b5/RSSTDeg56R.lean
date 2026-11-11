import RSSTKillRotSound
import RSSTKillRot768
import RSSTRulesN2

/-!
# ST-120 B5 (rotation-aware): degrees 5 and 6, 79 parts, K768 with rotations (`KillsRot`)

`cert/cert{5,6}_p79_k768R.txt` (exported by `py/export_cert.py d … --rot`: only rotation-respecting placements)
replayed by `checkDegPR` (kills through `reqOfR` = `rotOK` then `reqOf`).
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert5Rs : String := include_str "cert/cert5_p79_k768R.txt"
def cert6Rs : String := include_str "cert/cert6_p79_k768R.txt"

theorem deg5R_check : checkDegPR rsstParts79 k768R 5 (parseCert cert5Rs) = true := by native_decide
theorem deg6R_check : checkDegPR rsstParts79 k768R 6 (parseCert cert6Rs) = true := by native_decide

theorem B5R_deg56 : ∀ W : UWin, RealShape W → (W.d = 5 ∨ W.d = 6) → 0 < (loHiP rsstParts79 W).2 → KillsRot k768R W := by
  intro W hW hd hpos
  rcases hd with hd | hd
  · exact checkDegPR_sound rsstParts79 k768R 5 _ deg5R_check W hW hd hpos
  · exact checkDegPR_sound rsstParts79 k768R 6 _ deg6R_check W hW hd hpos

/-- The rotation data of K768 is well formed (lengths = degrees, interior entries = interior neighbours, coherent
orientation across interior faces). -/
theorem k768R_wf : k768R.all rotWF = true := by native_decide

#print axioms B5R_deg56
#print axioms k768R_wf

end SimpleGraph.SphericalMap.RSSTSeed
