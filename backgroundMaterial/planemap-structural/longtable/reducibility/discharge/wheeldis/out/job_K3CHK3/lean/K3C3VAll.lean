import K3C3V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3C3V
theorem hC_all (k : Fin 1) : cReducible18 (k3c3Entries.get (k.cast k3c3Entries_length.symm)).cf
    (k3c3Entries.get (k.cast k3c3Entries_length.symm)).eqR (k3c3Entries.get (k.cast k3c3Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K3C3V
#print axioms K3C3V.hC_all
