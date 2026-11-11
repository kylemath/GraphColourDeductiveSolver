import RSSTKillRotSound
import RSSTKillRot783
import RSSTRot

/-!
# ST-132: degree 7, rotation-aware kills, K783 (K768 + 15 rotation-respecting substitutes), 79 parts

`st132/cert7_census.txt` (the K783 rotation-aware census run, 0 failing leaves) replayed by `checkDegRotPR`.
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert7R783s : String := include_str "st132/cert7_census.txt"

theorem deg7R783_check : checkDegRotPR rsstParts79 k783R 7 (parseCert cert7R783s) = true := by native_decide

theorem B5R_deg7 : ∀ W : UWin, RealShape W → W.d = 7 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W :=
  checkDegRotPR_sound rsstParts79 k783R 7 _ deg7R783_check

#print axioms B5R_deg7

end SimpleGraph.SphericalMap.RSSTSeed
