import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDW13V00
import HDW13V01
import HDW13V02
import HDW13V03
import HDW13V04
import HDW13V05
import HDW13V06
import HDW13V07
import HDW13V08
import HDW13V09
import HDW13V10
import HDW13V11
import HDW13V12
import HDW13V13
import HDW13V14
import HDW13V15
import HDW13V16
import HDW13V17
import HDW13V18
import HDW13V19
import HDW13V20
import HDW13V21
import HDW13V22
import HDW13V23
import HDW13V24
import HDW13V25
import HDW13V26
open HDW13 DCheck18
namespace HDW13V
theorem hD_all (k : Fin 27) : DCheck18.dReducible (hdw13Confs.get (k.cast hdw13Confs_length.symm)) = true := by
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
end HDW13V
#print axioms HDW13V.hD_all
