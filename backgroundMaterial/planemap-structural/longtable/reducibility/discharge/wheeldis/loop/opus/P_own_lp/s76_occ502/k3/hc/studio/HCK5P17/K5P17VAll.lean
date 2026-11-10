import K5P17V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P17V
theorem hC_all (k : Fin 1) : cReducible18 (k5p17Entries.get (k.cast k5p17Entries_length.symm)).cf
    (k5p17Entries.get (k.cast k5p17Entries_length.symm)).eqR (k5p17Entries.get (k.cast k5p17Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P17V
#print axioms K5P17V.hC_all
