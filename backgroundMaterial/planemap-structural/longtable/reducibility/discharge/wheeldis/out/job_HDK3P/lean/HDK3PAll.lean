import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK3PV00
import HDK3PV01
open HDK3P DCheck18
namespace HDK3PV
theorem hD_all (k : Fin 2) : DCheck18.dReducible (hdk3pConfs.get (k.cast hdk3pConfs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
end HDK3PV
#print axioms HDK3PV.hD_all
