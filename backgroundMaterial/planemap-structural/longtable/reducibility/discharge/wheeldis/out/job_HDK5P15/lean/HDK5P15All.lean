import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P15V00
open HDK5P15 DCheck18
namespace HDK5P15V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p15Confs.get (k.cast hdk5p15Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P15V
#print axioms HDK5P15V.hD_all
