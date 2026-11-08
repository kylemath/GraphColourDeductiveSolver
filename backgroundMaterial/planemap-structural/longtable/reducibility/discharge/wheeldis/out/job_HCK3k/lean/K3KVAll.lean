import K3KV00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3KV
theorem hC_all (k : Fin 1) : cReducible18 (k3kEntries.get (k.cast k3kEntries_length.symm)).cf
    (k3kEntries.get (k.cast k3kEntries_length.symm)).eqR (k3kEntries.get (k.cast k3kEntries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K3KV
#print axioms K3KV.hC_all
