import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDW18NV00
import HDW18NV01
import HDW18NV02
import HDW18NV03
import HDW18NV04
import HDW18NV05
import HDW18NV06
import HDW18NV07
import HDW18NV08
import HDW18NV09
import HDW18NV10
import HDW18NV11
import HDW18NV12
import HDW18NV13
import HDW18NV14
open HDW18N DCheck18
namespace HDW18NV
theorem hD_all (k : Fin 15) : DCheck18.dReducible (hdw18nConfs.get (k.cast hdw18nConfs_length.symm)) = true := by
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
end HDW18NV
#print axioms HDW18NV.hD_all
