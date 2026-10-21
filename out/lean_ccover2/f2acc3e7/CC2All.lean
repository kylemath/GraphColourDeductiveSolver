import CC2V00
import CC2V01
import CC2V02
import CC2V03
import CC2V04
import CC2V05
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace CC2V
theorem hC_all (k : Fin 6) : cReducible18 (cc2Entries.get (k.cast cc2Entries_length.symm)).cf
    (cc2Entries.get (k.cast cc2Entries_length.symm)).eqR (cc2Entries.get (k.cast cc2Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
  · exact hC_3
  · exact hC_4
  · exact hC_5
def ccF (k : Fin 6) : CEntryF :=
  (cc2Entries.get (k.cast cc2Entries_length.symm)).toCEntryF
    (List.all_eq_true.1 cc2Entries_ok _ (List.get_mem _ _)) (hC_all k)
end CC2V
#print axioms CC2V.hC_all
#print axioms CC2V.ccF
