import K3LV00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K3LV
theorem hC_all (k : Fin 1) : cReducible18 (k3lEntries.get (k.cast k3lEntries_length.symm)).cf
    (k3lEntries.get (k.cast k3lEntries_length.symm)).eqR (k3lEntries.get (k.cast k3lEntries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K3LV
#print axioms K3LV.hC_all
