import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HD13V00
import HD13V01
import HD13V02
import HD13V03
import HD13V04
import HD13V05
import HD13V06
import HD13V07
import HD13V08
import HD13V09
open HD13 DCheck18
namespace HD13V
theorem hD_all (k : Fin 10) : DCheck18.dReducible (hd13Confs.get (k.cast hd13Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
  · exact hD_3
  · exact hD_4
  · exact hD_5
  · exact hD_6
  · exact hD_7
  · exact hD_8
  · exact hD_9
end HD13V
#print axioms HD13V.hD_all
