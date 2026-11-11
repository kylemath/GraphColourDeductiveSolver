import RSSTCheckSound
import RSSTKillSet583

/-!
# ST-120 B5 M3: degree 6, end to end

`cert/cert6_k583.txt` (exported by `py/export_cert.py 6 … --model 583`: the 582 proved configurations + 2.126,
128.1324802 not used) replayed by `checkDeg` under `native_decide`, then `checkDeg_sound`. By `Kills.mono` the
result holds for any final kill list containing these 583. Control: with the empty certificate the check is `false`.
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert6s : String := include_str "cert/cert6_k583.txt"
def cert6 : List LinkCert := parseCert cert6s

theorem deg6_check : checkDeg k583 6 cert6 = true := by native_decide

/-- **B5 at degree 6** (kill list: 582 proved + 2.126). -/
theorem B5_deg6 : ∀ W : UWin, RealShape W → W.d = 6 → 0 < W.loHi.2 → Kills k583 W :=
  checkDeg_sound k583 6 cert6 deg6_check

/-- Planted control: without the certificate's kills the degree-6 check fails. -/
theorem deg6_needs_kills : checkDeg k583 6 [] = false := by native_decide

#print axioms deg6_check
#print axioms B5_deg6
#print axioms deg6_needs_kills

end SimpleGraph.SphericalMap.RSSTSeed
