import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDST123V00
open HDST123 DCheck18
namespace HDST123V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdst123Confs.get (k.cast hdst123Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDST123V
#print axioms HDST123V.hD_all
