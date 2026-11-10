import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P06V00
open HDK5P06 DCheck18
namespace HDK5P06V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p06Confs.get (k.cast hdk5p06Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P06V
#print axioms HDK5P06V.hD_all
