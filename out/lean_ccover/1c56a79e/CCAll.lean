import CCV00
import CCV01
import CCV02
import CCV03
import CCV04
import CCV05
import CCV06
import CCV07
import CCV08
import CCV09
import CCV10
import CCV11
import CCV12
import CCV13
import CCV14
import CCV15
import CCV16
import CCV17
import CCV18
import CCV19
import CCV20
import CCV21
import CCV22
import CCV23
import CCV24
import CCV25
import CCV26
import CCV27
import CCV28
import CCV29
import CCV30
import CCV31
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace CCV
theorem hC_all (k : Fin 32) : cReducible18 (ccEntries.get (k.cast ccEntries_length.symm)).cf
    (ccEntries.get (k.cast ccEntries_length.symm)).eqR (ccEntries.get (k.cast ccEntries_length.symm)).eqI = true := by
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
  · exact hC_13
  · exact hC_14
  · exact hC_15
  · exact hC_16
  · exact hC_17
  · exact hC_18
  · exact hC_19
  · exact hC_20
  · exact hC_21
  · exact hC_22
  · exact hC_23
  · exact hC_24
  · exact hC_25
  · exact hC_26
  · exact hC_27
  · exact hC_28
  · exact hC_29
  · exact hC_30
  · exact hC_31
def ccF (k : Fin 32) : CEntryF :=
  (ccEntries.get (k.cast ccEntries_length.symm)).toCEntryF
    (List.all_eq_true.1 ccEntries_ok _ (List.get_mem _ _)) (hC_all k)
end CCV
#print axioms CCV.hC_all
#print axioms CCV.ccF
