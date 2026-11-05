import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDR5V00
import HDR5V01
import HDR5V02
import HDR5V03
import HDR5V04
open HDR5 DCheck18
namespace HDR5V
theorem hD_all (k : Fin 5) : DCheck18.dReducible (hdr5Confs.get (k.cast hdr5Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
  · exact hD_1
  · exact hD_2
  · exact hD_3
  · exact hD_4
end HDR5V
#print axioms HDR5V.hD_all
