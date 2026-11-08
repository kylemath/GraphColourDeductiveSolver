import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5DB1V00
open HDK5DB1 DCheck18
namespace HDK5DB1V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5db1Confs.get (k.cast hdk5db1Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5DB1V
#print axioms HDK5DB1V.hD_all
