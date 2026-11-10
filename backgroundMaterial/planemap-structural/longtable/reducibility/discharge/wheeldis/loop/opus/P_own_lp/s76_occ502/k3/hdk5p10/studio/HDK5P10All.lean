import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P10V00
open HDK5P10 DCheck18
namespace HDK5P10V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p10Confs.get (k.cast hdk5p10Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P10V
#print axioms HDK5P10V.hD_all
