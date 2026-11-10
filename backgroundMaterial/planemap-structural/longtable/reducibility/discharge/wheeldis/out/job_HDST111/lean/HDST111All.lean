import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDST111V00
import HDST111V01
import HDST111V02
import HDST111V03
import HDST111V04
import HDST111V05
import HDST111V06
import HDST111V07
import HDST111V08
import HDST111V09
import HDST111V10
import HDST111V11
import HDST111V12
import HDST111V13
import HDST111V14
import HDST111V15
import HDST111V16
import HDST111V17
import HDST111V18
import HDST111V19
import HDST111V20
import HDST111V21
import HDST111V22
import HDST111V23
import HDST111V24
import HDST111V25
import HDST111V26
import HDST111V27
import HDST111V28
import HDST111V29
import HDST111V30
import HDST111V31
open HDST111 DCheck18
namespace HDST111V
theorem hD_all (k : Fin 32) : DCheck18.dReducible (hdst111Confs.get (k.cast hdst111Confs_length.symm)) = true := by
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
  · exact hD_30
  · exact hD_31
end HDST111V
#print axioms HDST111V.hD_all
