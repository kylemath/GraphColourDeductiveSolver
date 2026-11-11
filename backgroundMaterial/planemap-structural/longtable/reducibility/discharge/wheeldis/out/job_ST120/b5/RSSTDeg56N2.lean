import RSSTDeg5
import RSSTDeg6
import RSSTRulesN2

/-!
# ST-120 B5 M3 with the 79 parts (71 + N2, B2 `RSSTRulesN2`)

At d = 5, 6 no N2 part fits at a hub `u` (N2 hubs are 7s) or into `u` (N2's third spoke is exactly 9+), so the
exporter run with the 79 parts (`--parts cert/parts79.txt`) wrote byte-identical certificates; they are replayed here
by `checkDegP rsstParts79` (B4's `loHiP rsstParts79`). Kill list: 582 proved + 2.126.
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

theorem deg5_check79 : checkDegP rsstParts79 k583 5 cert5 = true := by native_decide
theorem deg6_check79 : checkDegP rsstParts79 k583 6 cert6 = true := by native_decide

/-- **B5 at degrees 5 and 6, 79 parts.** -/
theorem B5_deg56_79 : ∀ W : UWin, RealShape W → (W.d = 5 ∨ W.d = 6) → 0 < (loHiP rsstParts79 W).2 → Kills k583 W := by
  intro W hW hd hpos
  rcases hd with hd | hd
  · exact checkDegP_sound rsstParts79 k583 5 cert5 deg5_check79 W hW hd hpos
  · exact checkDegP_sound rsstParts79 k583 6 cert6 deg6_check79 W hW hd hpos

#print axioms B5_deg56_79

end SimpleGraph.SphericalMap.RSSTSeed
