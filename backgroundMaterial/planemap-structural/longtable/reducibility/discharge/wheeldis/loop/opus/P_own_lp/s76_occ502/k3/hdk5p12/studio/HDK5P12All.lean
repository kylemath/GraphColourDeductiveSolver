import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P12V00
open HDK5P12 DCheck18
namespace HDK5P12V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p12Confs.get (k.cast hdk5p12Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P12V
#print axioms HDK5P12V.hD_all
