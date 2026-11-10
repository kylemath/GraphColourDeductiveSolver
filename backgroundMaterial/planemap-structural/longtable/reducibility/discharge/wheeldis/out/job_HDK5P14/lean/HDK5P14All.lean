import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P14V00
open HDK5P14 DCheck18
namespace HDK5P14V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p14Confs.get (k.cast hdk5p14Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P14V
#print axioms HDK5P14V.hD_all
