import K5P05V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P05V
theorem hC_all (k : Fin 1) : cReducible18 (k5p05Entries.get (k.cast k5p05Entries_length.symm)).cf
    (k5p05Entries.get (k.cast k5p05Entries_length.symm)).eqR (k5p05Entries.get (k.cast k5p05Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P05V
#print axioms K5P05V.hC_all
