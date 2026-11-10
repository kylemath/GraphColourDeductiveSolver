import K5P03V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P03V
theorem hC_all (k : Fin 1) : cReducible18 (k5p03Entries.get (k.cast k5p03Entries_length.symm)).cf
    (k5p03Entries.get (k.cast k5p03Entries_length.symm)).eqR (k5p03Entries.get (k.cast k5p03Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P03V
#print axioms K5P03V.hC_all
