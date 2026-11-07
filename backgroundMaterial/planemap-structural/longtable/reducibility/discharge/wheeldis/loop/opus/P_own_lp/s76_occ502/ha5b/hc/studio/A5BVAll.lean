import A5BV00
import A5BV01
import A5BV02
import A5BV03
import A5BV04
import A5BV05
import A5BV06
import A5BV07
import A5BV08
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace A5BV
theorem hC_all (k : Fin 9) : cReducible18 (a5bEntries.get (k.cast a5bEntries_length.symm)).cf
    (a5bEntries.get (k.cast a5bEntries_length.symm)).eqR (a5bEntries.get (k.cast a5bEntries_length.symm)).eqI = true := by
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
end A5BV
#print axioms A5BV.hC_all
