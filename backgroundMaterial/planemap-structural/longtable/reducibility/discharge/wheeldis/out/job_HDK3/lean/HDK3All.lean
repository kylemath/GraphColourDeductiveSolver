import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK3V00
import HDK3V01
import HDK3V02
import HDK3V03
import HDK3V04
import HDK3V05
open HDK3 DCheck18
namespace HDK3V
theorem hD_all (k : Fin 6) : DCheck18.dReducible (hdk3Confs.get (k.cast hdk3Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
  · exact hD_3
  · exact hD_4
  · exact hD_5
end HDK3V
#print axioms HDK3V.hD_all
