import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P08V00
open HDK5P08 DCheck18
namespace HDK5P08V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p08Confs.get (k.cast hdk5p08Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P08V
#print axioms HDK5P08V.hD_all
