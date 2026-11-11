import RSSTD9Sound
import RSSTKill768

/-!
# ST-127 (2): degrees 9..14, 79 parts, kill list K768

For each `d`, `checkDegHi` (RSSTD9Core) builds the verified `c⁺` table, runs the link-word search (prune
`60 − 10d + Σ c⁺ ≤ 0`, rotation-least words), and replays `cert/cert<d>_p79_k768.txt` on the survivors
(exported by `py/export_cert.py d … --links-file cert/links<d>_lean.txt`; u is a host with letter `d`).
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert9s : String := include_str "cert/cert9_p79_k768.txt"
def cert9 : List LinkCert := parseCert cert9s
theorem deg9_check : checkDegHi rsstParts79 k768 9 cert9 = true := by native_decide
theorem B5_deg9_rot : ∀ W : UWin, RealShape W → W.d = 9 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W := checkDegHi_sound rsstParts79 k768 9 cert9 deg9_check
#print axioms B5_deg9_rot

def cert10s : String := include_str "cert/cert10_p79_k768.txt"
def cert10 : List LinkCert := parseCert cert10s
theorem deg10_check : checkDegHi rsstParts79 k768 10 cert10 = true := by native_decide
theorem B5_deg10_rot : ∀ W : UWin, RealShape W → W.d = 10 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W := checkDegHi_sound rsstParts79 k768 10 cert10 deg10_check
#print axioms B5_deg10_rot

def cert11s : String := include_str "cert/cert11_p79_k768.txt"
def cert11 : List LinkCert := parseCert cert11s
theorem deg11_check : checkDegHi rsstParts79 k768 11 cert11 = true := by native_decide
theorem B5_deg11_rot : ∀ W : UWin, RealShape W → W.d = 11 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W := checkDegHi_sound rsstParts79 k768 11 cert11 deg11_check
#print axioms B5_deg11_rot

def cert12s : String := include_str "cert/cert12_p79_k768.txt"
def cert12 : List LinkCert := parseCert cert12s
theorem deg12_check : checkDegHi rsstParts79 k768 12 cert12 = true := by native_decide
theorem B5_deg12_rot : ∀ W : UWin, RealShape W → W.d = 12 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W := checkDegHi_sound rsstParts79 k768 12 cert12 deg12_check
#print axioms B5_deg12_rot

def cert13s : String := include_str "cert/cert13_p79_k768.txt"
def cert13 : List LinkCert := parseCert cert13s
theorem deg13_check : checkDegHi rsstParts79 k768 13 cert13 = true := by native_decide
theorem B5_deg13_rot : ∀ W : UWin, RealShape W → W.d = 13 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W := checkDegHi_sound rsstParts79 k768 13 cert13 deg13_check
#print axioms B5_deg13_rot

def cert14s : String := include_str "cert/cert14_p79_k768.txt"
def cert14 : List LinkCert := parseCert cert14s
theorem deg14_check : checkDegHi rsstParts79 k768 14 cert14 = true := by native_decide
theorem B5_deg14_rot : ∀ W : UWin, RealShape W → W.d = 14 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W := checkDegHi_sound rsstParts79 k768 14 cert14 deg14_check
#print axioms B5_deg14_rot

end SimpleGraph.SphericalMap.RSSTSeed
