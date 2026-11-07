import A5CV00
import A5CV01
import A5CV02
import A5CV03
import A5CV04
import A5CV05
import A5CV06
import A5CV07
import A5CV08
import A5CV09
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace A5CV
theorem hC_all (k : Fin 10) : cReducible18 (a5cEntries.get (k.cast a5cEntries_length.symm)).cf
    (a5cEntries.get (k.cast a5cEntries_length.symm)).eqR (a5cEntries.get (k.cast a5cEntries_length.symm)).eqI = true := by
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
end A5CV
#print axioms A5CV.hC_all
