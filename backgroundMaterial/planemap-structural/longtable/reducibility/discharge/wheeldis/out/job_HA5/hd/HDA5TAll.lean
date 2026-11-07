import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDA5TV00
import HDA5TV01
import HDA5TV02
import HDA5TV03
import HDA5TV04
import HDA5TV05
import HDA5TV06
import HDA5TV07
import HDA5TV08
import HDA5TV09
import HDA5TV10
import HDA5TV11
import HDA5TV12
import HDA5TV13
import HDA5TV14
import HDA5TV15
import HDA5TV16
import HDA5TV17
import HDA5TV18
import HDA5TV19
import HDA5TV20
import HDA5TV21
import HDA5TV22
import HDA5TV23
import HDA5TV24
import HDA5TV25
import HDA5TV26
import HDA5TV27
import HDA5TV28
import HDA5TV29
import HDA5TV30
import HDA5TV31
import HDA5TV32
import HDA5TV33
import HDA5TV34
open HDA5T DCheck18
namespace HDA5TV
theorem hD_all (k : Fin 35) : DCheck18.dReducible (hda5tConfs.get (k.cast hda5tConfs_length.symm)) = true := by
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
end HDA5TV
#print axioms HDA5TV.hD_all
