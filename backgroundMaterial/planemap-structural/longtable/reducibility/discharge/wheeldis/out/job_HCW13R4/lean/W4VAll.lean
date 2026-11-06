import W4V00
import W4V01
import W4V02
import W4V03
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace W4V
theorem hC_all (k : Fin 4) : cReducible18 (w4Entries.get (k.cast w4Entries_length.symm)).cf
    (w4Entries.get (k.cast w4Entries_length.symm)).eqR (w4Entries.get (k.cast w4Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
  · exact hC_3
end W4V
#print axioms W4V.hC_all
