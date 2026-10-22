import CC3V00
import CC3V01
import CC3V02
import CC3V03
import CC3V04
import CC3V05
import CC3V06
import CC3V07
import CC3V08
import CC3V09
import CC3V10
import CC3V11
import CC3V12
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace CC3V
theorem hC_all (k : Fin 13) : cReducible18 (cc3Entries.get (k.cast cc3Entries_length.symm)).cf
    (cc3Entries.get (k.cast cc3Entries_length.symm)).eqR (cc3Entries.get (k.cast cc3Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
  · exact hC_3
  · exact hC_4
  · exact hC_5
  · exact hC_6
  · exact hC_7
  · exact hC_8
  · exact hC_9
  · exact hC_10
  · exact hC_11
  · exact hC_12
def ccF (k : Fin 13) : CEntryF :=
  (cc3Entries.get (k.cast cc3Entries_length.symm)).toCEntryF
    (List.all_eq_true.1 cc3Entries_ok _ (List.get_mem _ _)) (hC_all k)
end CC3V
#print axioms CC3V.hC_all
#print axioms CC3V.ccF
