import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P09V00
open HDK5P09 DCheck18
namespace HDK5P09V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p09Confs.get (k.cast hdk5p09Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P09V
#print axioms HDK5P09V.hD_all
