import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P13V00
open HDK5P13 DCheck18
namespace HDK5P13V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p13Confs.get (k.cast hdk5p13Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P13V
#print axioms HDK5P13V.hD_all
