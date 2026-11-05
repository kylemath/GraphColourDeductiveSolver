import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HD30V00
import HD30V01
import HD30V02
import HD30V03
import HD30V04
import HD30V05
import HD30V06
import HD30V07
import HD30V08
import HD30V09
import HD30V10
import HD30V11
import HD30V12
import HD30V13
import HD30V14
import HD30V15
import HD30V16
import HD30V17
import HD30V18
import HD30V19
import HD30V20
import HD30V21
import HD30V22
import HD30V23
import HD30V24
import HD30V25
import HD30V26
import HD30V27
import HD30V28
import HD30V29
open HD30 DCheck18
namespace HD30V
theorem hD_all (k : Fin 30) : DCheck18.dReducible (hd30Confs.get (k.cast hd30Confs_length.symm)) = true := by
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
  · exact hD_10
  · exact hD_11
  · exact hD_12
  · exact hD_13
  · exact hD_14
  · exact hD_15
  · exact hD_16
  · exact hD_17
  · exact hD_18
  · exact hD_19
  · exact hD_20
  · exact hD_21
  · exact hD_22
  · exact hD_23
  · exact hD_24
  · exact hD_25
  · exact hD_26
  · exact hD_27
  · exact hD_28
  · exact hD_29
end HD30V
#print axioms HD30V.hD_all
