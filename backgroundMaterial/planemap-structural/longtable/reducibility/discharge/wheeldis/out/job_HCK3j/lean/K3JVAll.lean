import K3JV00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3JV
theorem hC_all (k : Fin 1) : cReducible18 (k3jEntries.get (k.cast k3jEntries_length.symm)).cf
    (k3jEntries.get (k.cast k3jEntries_length.symm)).eqR (k3jEntries.get (k.cast k3jEntries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K3JV
#print axioms K3JV.hC_all
