import Mathlib.Tactic.FinCases
import Mathlib.Data.Fintype.Fin
import HDK5CV2V00
open HDK5CV2 DCheck18
namespace HDK5CV2V
theorem hD_all (k : Fin 1) : DCheck18.dReducible (hdk5cv2Confs.get (k.cast hdk5cv2Confs_length.symm)) = true := by
  fin_cases k
  · exact hD_0
end HDK5CV2V
#print axioms HDK5CV2V.hD_all
