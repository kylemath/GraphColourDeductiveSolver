import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P16V00
open HDK5P16 DCheck18
namespace HDK5P16V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p16Confs.get (k.cast hdk5p16Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P16V
#print axioms HDK5P16V.hD_all
