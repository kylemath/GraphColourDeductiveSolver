import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDOF7V00
import HDOF7V01
import HDOF7V02
import HDOF7V03
import HDOF7V04
import HDOF7V05
import HDOF7V06
import HDOF7V07
import HDOF7V08
import HDOF7V09
import HDOF7V10
import HDOF7V11
import HDOF7V12
import HDOF7V13
import HDOF7V14
import HDOF7V15
import HDOF7V16
import HDOF7V17
import HDOF7V18
import HDOF7V19
import HDOF7V20
import HDOF7V21
import HDOF7V22
import HDOF7V23
import HDOF7V24
import HDOF7V25
import HDOF7V26
import HDOF7V27
import HDOF7V28
import HDOF7V29
import HDOF7V30
import HDOF7V31
import HDOF7V32
import HDOF7V33
import HDOF7V34
import HDOF7V35
import HDOF7V36
import HDOF7V37
import HDOF7V38
import HDOF7V39
import HDOF7V40
import HDOF7V41
import HDOF7V42
import HDOF7V43
import HDOF7V44
import HDOF7V45
import HDOF7V46
import HDOF7V47
import HDOF7V48
import HDOF7V49
import HDOF7V50
import HDOF7V51
open HDOF7 DCheck18
namespace HDOF7V
theorem hD_all (k : Fin 52) : DCheck18.dReducible (hdof7Confs.get (k.cast hdof7Confs_length.symm)) = true := by
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
  · exact hD_32
  · exact hD_33
  · exact hD_34
  · exact hD_35
  · exact hD_36
  · exact hD_37
  · exact hD_38
  · exact hD_39
  · exact hD_40
  · exact hD_41
  · exact hD_42
  · exact hD_43
  · exact hD_44
  · exact hD_45
  · exact hD_46
  · exact hD_47
  · exact hD_48
  · exact hD_49
  · exact hD_50
  · exact hD_51
end HDOF7V
#print axioms HDOF7V.hD_all
