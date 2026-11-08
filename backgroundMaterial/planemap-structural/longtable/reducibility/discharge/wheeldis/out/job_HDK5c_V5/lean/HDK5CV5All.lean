import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5CV5V00
open HDK5CV5 DCheck18
namespace HDK5CV5V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5cv5Confs.get (k.cast hdk5cv5Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5CV5V
#print axioms HDK5CV5V.hD_all
