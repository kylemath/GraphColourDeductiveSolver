import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5BL3V00
open HDK5BL3 DCheck18
namespace HDK5BL3V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5bl3Confs.get (k.cast hdk5bl3Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5BL3V
#print axioms HDK5BL3V.hD_all
