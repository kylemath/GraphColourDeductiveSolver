import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK3BV00
open HDK3B DCheck18
namespace HDK3BV
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk3bConfs.get (k.cast hdk3bConfs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK3BV
#print axioms HDK3BV.hD_all
