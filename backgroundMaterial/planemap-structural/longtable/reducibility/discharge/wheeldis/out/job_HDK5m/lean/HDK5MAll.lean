import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5MV00
open HDK5M DCheck18
namespace HDK5MV
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5mConfs.get (k.cast hdk5mConfs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5MV
#print axioms HDK5MV.hD_all
