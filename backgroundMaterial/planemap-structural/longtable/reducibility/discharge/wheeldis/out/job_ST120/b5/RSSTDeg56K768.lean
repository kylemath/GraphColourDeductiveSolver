import RSSTDeg5
import RSSTDeg6
import RSSTRulesN2
import RSSTKill768

/-!
# ST-127: degrees 5 and 6 on the final kill list K768 (582 + 2.126 + 185 substitutes), 79 parts

`k768` (RSSTKill768, from `st127/k767_kc.txt`) begins with the same 583 entries as `k583`, so the K583 certificates
(`cert/cert{5,6}_k583.txt`, indices < 583) replay unchanged.
-/

set_option profiler true

namespace SimpleGraph.SphericalMap.RSSTSeed

theorem deg5_check79_768 : checkDegP rsstParts79 k768 5 cert5 = true := by native_decide
theorem deg6_check79_768 : checkDegP rsstParts79 k768 6 cert6 = true := by native_decide

#print axioms deg5_check79_768
#print axioms deg6_check79_768

end SimpleGraph.SphericalMap.RSSTSeed
