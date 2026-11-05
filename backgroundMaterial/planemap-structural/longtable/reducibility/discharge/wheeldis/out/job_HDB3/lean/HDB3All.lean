import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDB3V00
import HDB3V01
import HDB3V02
import HDB3V03
open HDB3 DCheck18
namespace HDB3V
theorem hD_all (k : Fin 4) : DCheck18.dReducible (hdb3Confs.get (k.cast hdb3Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
  · exact hD_3
end HDB3V
#print axioms HDB3V.hD_all
