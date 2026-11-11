import RSSTCheckSound
import RSSTKillSet583

/-!
# ST-120 B5 M3: degree 5, end to end

`cert/cert5_k583.txt` (exported by `py/export_cert.py 5 … --model 583`: the 582 proved configurations + 2.126,
128.1324802 not used) replayed by `checkDeg` under `native_decide`, then `checkDeg_sound`. By `Kills.mono` the
result holds for any final kill list containing these 583. Control: with the empty certificate the check is `false`.
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

def cert5s : String := include_str "cert/cert5_k583.txt"
def cert5 : List LinkCert := parseCert cert5s

theorem deg5_check : checkDeg k583 5 cert5 = true := by native_decide

/-- **B5 at degree 5** (kill list: 582 proved + 2.126). -/
theorem B5_deg5 : ∀ W : UWin, RealShape W → W.d = 5 → 0 < W.loHi.2 → Kills k583 W :=
  checkDeg_sound k583 5 cert5 deg5_check

/-- Planted control: without the certificate's kills the degree-5 check fails. -/
theorem deg5_needs_kills : checkDeg k583 5 [] = false := by native_decide

#print axioms deg5_check
#print axioms B5_deg5
#print axioms deg5_needs_kills

end SimpleGraph.SphericalMap.RSSTSeed
