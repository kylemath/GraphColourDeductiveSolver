import K3IV00
import K3IV01
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3IV
theorem hC_all (k : Fin 2) : cReducible18 (k3iEntries.get (k.cast k3iEntries_length.symm)).cf
    (k3iEntries.get (k.cast k3iEntries_length.symm)).eqR (k3iEntries.get (k.cast k3iEntries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
end K3IV
#print axioms K3IV.hC_all
