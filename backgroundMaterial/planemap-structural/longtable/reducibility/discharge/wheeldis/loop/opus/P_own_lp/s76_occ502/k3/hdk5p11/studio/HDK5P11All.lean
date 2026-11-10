import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5P11V00
open HDK5P11 DCheck18
namespace HDK5P11V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5p11Confs.get (k.cast hdk5p11Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5P11V
#print axioms HDK5P11V.hD_all
