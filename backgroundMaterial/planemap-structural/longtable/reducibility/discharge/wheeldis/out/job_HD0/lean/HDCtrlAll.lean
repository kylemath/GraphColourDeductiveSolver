import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDCtrlV00
import HDCtrlV01
import HDCtrlV02
open HDCtrl DCheck18
namespace HDCtrlV
theorem hD_all (k : Fin 3) : DCheck18.dReducible (hdcConfs.get (k.cast hdcConfs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
end HDCtrlV
#print axioms HDCtrlV.hD_all
