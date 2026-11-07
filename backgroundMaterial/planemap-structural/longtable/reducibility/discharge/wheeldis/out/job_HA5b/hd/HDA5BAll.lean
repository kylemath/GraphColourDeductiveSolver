import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDA5BV00
import HDA5BV01
import HDA5BV02
import HDA5BV03
import HDA5BV04
import HDA5BV05
import HDA5BV06
import HDA5BV07
import HDA5BV08
import HDA5BV09
import HDA5BV10
import HDA5BV11
import HDA5BV12
import HDA5BV13
import HDA5BV14
import HDA5BV15
import HDA5BV16
import HDA5BV17
import HDA5BV18
import HDA5BV19
import HDA5BV20
import HDA5BV21
import HDA5BV22
import HDA5BV23
import HDA5BV24
import HDA5BV25
import HDA5BV26
import HDA5BV27
import HDA5BV28
import HDA5BV29
import HDA5BV30
import HDA5BV31
import HDA5BV32
import HDA5BV33
import HDA5BV34
import HDA5BV35
import HDA5BV36
import HDA5BV37
import HDA5BV38
import HDA5BV39
import HDA5BV40
import HDA5BV41
import HDA5BV42
import HDA5BV43
import HDA5BV44
open HDA5B DCheck18
namespace HDA5BV
theorem hD_all (k : Fin 45) : DCheck18.dReducible (hda5bConfs.get (k.cast hda5bConfs_length.symm)) = true := by
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
end HDA5BV
#print axioms HDA5BV.hD_all
