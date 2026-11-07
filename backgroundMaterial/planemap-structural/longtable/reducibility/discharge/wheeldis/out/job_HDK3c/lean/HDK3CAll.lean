import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK3CV00
open HDK3C DCheck18
namespace HDK3CV
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk3cConfs.get (k.cast hdk3cConfs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK3CV
#print axioms HDK3CV.hD_all
