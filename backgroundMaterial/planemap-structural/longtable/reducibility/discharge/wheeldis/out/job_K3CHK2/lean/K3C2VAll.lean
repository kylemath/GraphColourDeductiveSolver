import K3C2V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3C2V
theorem hC_all (k : Fin 1) : cReducible18 (k3c2Entries.get (k.cast k3c2Entries_length.symm)).cf
    (k3c2Entries.get (k.cast k3c2Entries_length.symm)).eqR (k3c2Entries.get (k.cast k3c2Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K3C2V
#print axioms K3C2V.hC_all
