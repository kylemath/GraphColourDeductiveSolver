import RSSTRot
import RSSTKill768

/-!
# ST-127 (b): degree 7, 79 parts (71 + N2), final kill list K768, one link word per rotation class

`cert/cert7_p79_k768_rot.txt` (exported by `py/export_cert.py 7 … --model kc:st127/k767_kc.txt --parts
cert/parts79.txt --rotmin`, 11,165 rotation-least link words) replayed by `checkDegRotP` under `native_decide`; the
rotation reduction is sound by `checkDegRotP_sound` + `seed_of_B5P_rot` (RSSTRot).
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert7s : String := include_str "cert/cert7_p79_k768_rot.txt"
def cert7 : List LinkCert := parseCert cert7s

theorem deg7_check : checkDegRotP rsstParts79 k768 7 cert7 = true := by native_decide

/-- **B5 at degree 7** (79 parts, K768, rotation-least link words). -/
theorem B5_deg7_rot : ∀ W : UWin, RealShape W → W.d = 7 → isRotMin W.link = true →
    0 < (loHiP rsstParts79 W).2 → Kills k768 W :=
  checkDegRotP_sound rsstParts79 k768 7 cert7 deg7_check

#print axioms deg7_check
#print axioms B5_deg7_rot

end SimpleGraph.SphericalMap.RSSTSeed
