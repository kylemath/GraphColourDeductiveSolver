import ST119V00
import ST119V01
import ST119V02
import ST119V03
import ST119V04
import ST119V05
import ST119V06
import ST119V07
import ST119V08
import ST119V09
import ST119V10
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace ST119V
theorem hC_all (k : Fin 11) : cReducible18 (st119Entries.get (k.cast st119Entries_length.symm)).cf
    (st119Entries.get (k.cast st119Entries_length.symm)).eqR (st119Entries.get (k.cast st119Entries_length.symm)).eqI = true := by
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
end ST119V
#print axioms ST119V.hC_all
