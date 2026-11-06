import W2AV00
import W2AV01
import W2AV02
import W2AV03
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace W2AV
theorem hC_all (k : Fin 4) : cReducible18 (w2aEntries.get (k.cast w2aEntries_length.symm)).cf
    (w2aEntries.get (k.cast w2aEntries_length.symm)).eqR (w2aEntries.get (k.cast w2aEntries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
  · exact hC_3
end W2AV
#print axioms W2AV.hC_all
