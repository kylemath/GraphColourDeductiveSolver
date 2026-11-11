import RSSTKillRotSound
import RSSTKillRot783
import RSSTRot

/-!
# ST-132: degree 8, rotation-aware kills, K783 (K768 + 15 rotation-respecting substitutes), 79 parts

`st132/cert8_census.txt` (the K783 rotation-aware census run, 0 failing leaves) replayed by `checkDegRotPR`.
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert8R783s : String := include_str "st132/cert8_census.txt"

theorem deg8R783_check : checkDegRotPR rsstParts79 k783R 8 (parseCert cert8R783s) = true := by native_decide

theorem B5R_deg8 : ∀ W : UWin, RealShape W → W.d = 8 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W :=
  checkDegRotPR_sound rsstParts79 k783R 8 _ deg8R783_check

#print axioms B5R_deg8

end SimpleGraph.SphericalMap.RSSTSeed
