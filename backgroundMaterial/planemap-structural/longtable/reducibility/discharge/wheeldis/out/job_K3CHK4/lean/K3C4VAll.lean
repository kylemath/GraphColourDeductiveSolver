import K3C4V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3C4V
theorem hC_all (k : Fin 1) : cReducible18 (k3c4Entries.get (k.cast k3c4Entries_length.symm)).cf
    (k3c4Entries.get (k.cast k3c4Entries_length.symm)).eqR (k3c4Entries.get (k.cast k3c4Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K3C4V
#print axioms K3C4V.hC_all
