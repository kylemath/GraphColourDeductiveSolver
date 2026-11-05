import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK7V00
import HDK7V01
import HDK7V02
import HDK7V03
import HDK7V04
import HDK7V05
import HDK7V06
open HDK7 DCheck18
namespace HDK7V
theorem hD_all (k : Fin 7) : DCheck18.dReducible (hdk7Confs.get (k.cast hdk7Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
  · exact hD_3
  · exact hD_4
  · exact hD_5
  · exact hD_6
end HDK7V
#print axioms HDK7V.hD_all
