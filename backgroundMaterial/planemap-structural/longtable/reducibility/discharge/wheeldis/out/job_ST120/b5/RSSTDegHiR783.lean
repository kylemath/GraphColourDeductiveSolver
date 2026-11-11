import RSSTKillRotSound
import RSSTKillRot783

/-!
# ST-132: degrees 9..14, rotation-aware kills, K783, 79 parts (`checkDegHiR`: verified c⁺ table, link-word search,
replay of `st132/cert<d>_census.txt` on the survivors)
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert9R783s : String := include_str "st132/cert9_census.txt"
theorem deg9R783_check : checkDegHiR rsstParts79 k783R 9 (parseCert cert9R783s) = true := by native_decide
theorem B5R_deg9 : ∀ W : UWin, RealShape W → W.d = 9 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W := checkDegHiR_sound rsstParts79 k783R 9 _ deg9R783_check
#print axioms B5R_deg9

def cert10R783s : String := include_str "st132/cert10_census.txt"
theorem deg10R783_check : checkDegHiR rsstParts79 k783R 10 (parseCert cert10R783s) = true := by native_decide
theorem B5R_deg10 : ∀ W : UWin, RealShape W → W.d = 10 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W := checkDegHiR_sound rsstParts79 k783R 10 _ deg10R783_check
#print axioms B5R_deg10

def cert11R783s : String := include_str "st132/cert11_census.txt"
theorem deg11R783_check : checkDegHiR rsstParts79 k783R 11 (parseCert cert11R783s) = true := by native_decide
theorem B5R_deg11 : ∀ W : UWin, RealShape W → W.d = 11 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W := checkDegHiR_sound rsstParts79 k783R 11 _ deg11R783_check
#print axioms B5R_deg11

def cert12R783s : String := include_str "st132/cert12_census.txt"
theorem deg12R783_check : checkDegHiR rsstParts79 k783R 12 (parseCert cert12R783s) = true := by native_decide
theorem B5R_deg12 : ∀ W : UWin, RealShape W → W.d = 12 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W := checkDegHiR_sound rsstParts79 k783R 12 _ deg12R783_check
#print axioms B5R_deg12

def cert13R783s : String := include_str "st132/cert13_census.txt"
theorem deg13R783_check : checkDegHiR rsstParts79 k783R 13 (parseCert cert13R783s) = true := by native_decide
theorem B5R_deg13 : ∀ W : UWin, RealShape W → W.d = 13 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W := checkDegHiR_sound rsstParts79 k783R 13 _ deg13R783_check
#print axioms B5R_deg13

def cert14R783s : String := include_str "st132/cert14_census.txt"
theorem deg14R783_check : checkDegHiR rsstParts79 k783R 14 (parseCert cert14R783s) = true := by native_decide
theorem B5R_deg14 : ∀ W : UWin, RealShape W → W.d = 14 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → KillsRot k783R W := checkDegHiR_sound rsstParts79 k783R 14 _ deg14R783_check
#print axioms B5R_deg14

end SimpleGraph.SphericalMap.RSSTSeed
