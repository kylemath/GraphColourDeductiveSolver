import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P01V00
open HDK5P01 DCheck18
namespace HDK5P01V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p01Confs.get (k.cast hdk5p01Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P01V
#print axioms HDK5P01V.hD_all
