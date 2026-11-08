import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5CV4V00
open HDK5CV4 DCheck18
namespace HDK5CV4V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5cv4Confs.get (k.cast hdk5cv4Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5CV4V
#print axioms HDK5CV4V.hD_all
