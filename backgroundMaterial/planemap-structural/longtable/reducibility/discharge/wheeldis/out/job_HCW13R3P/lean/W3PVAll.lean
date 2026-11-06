import W3PV00
import W3PV01
import W3PV02
import W3PV03
import W3PV04
import W3PV05
import W3PV06
import W3PV07
import W3PV08
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace W3PV
theorem hC_all (k : Fin 9) : cReducible18 (w3pEntries.get (k.cast w3pEntries_length.symm)).cf
    (w3pEntries.get (k.cast w3pEntries_length.symm)).eqR (w3pEntries.get (k.cast w3pEntries_length.symm)).eqI = true := by
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
end W3PV
#print axioms W3PV.hC_all
