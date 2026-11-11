import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDST132V00
import HDST132V01
import HDST132V02
import HDST132V03
import HDST132V04
import HDST132V05
import HDST132V06
import HDST132V07
import HDST132V08
import HDST132V09
import HDST132V10
import HDST132V11
import HDST132V12
open HDST132 DCheck18
namespace HDST132V
theorem hD_all (k : Fin 13) : DCheck18.dReducible (hdst132Confs.get (k.cast hdst132Confs_length.symm)) = true := by
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
end HDST132V
#print axioms HDST132V.hD_all
