import K5JV00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5JV
theorem hC_all (k : Fin 1) : cReducible18 (k5jEntries.get (k.cast k5jEntries_length.symm)).cf
    (k5jEntries.get (k.cast k5jEntries_length.symm)).eqR (k5jEntries.get (k.cast k5jEntries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5JV
#print axioms K5JV.hC_all
