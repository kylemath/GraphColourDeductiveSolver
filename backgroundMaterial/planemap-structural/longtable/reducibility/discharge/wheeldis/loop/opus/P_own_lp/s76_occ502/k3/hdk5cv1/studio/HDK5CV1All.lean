import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5CV1V00
open HDK5CV1 DCheck18
namespace HDK5CV1V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5cv1Confs.get (k.cast hdk5cv1Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5CV1V
#print axioms HDK5CV1V.hD_all
