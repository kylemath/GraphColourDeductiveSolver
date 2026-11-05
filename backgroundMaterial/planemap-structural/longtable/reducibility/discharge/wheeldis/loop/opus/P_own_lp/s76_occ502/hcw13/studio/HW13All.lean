import HW13V00
import HW13V01
import HW13V02
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace HW13V
theorem hC_all (k : Fin 3) : cReducible18 (w13Entries.get (k.cast w13Entries_length.symm)).cf
    (w13Entries.get (k.cast w13Entries_length.symm)).eqR (w13Entries.get (k.cast w13Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
end HW13V
#print axioms HW13V.hC_all
