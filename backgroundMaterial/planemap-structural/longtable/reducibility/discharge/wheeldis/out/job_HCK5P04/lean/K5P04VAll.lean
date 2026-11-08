import K5P04V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P04V
theorem hC_all (k : Fin 1) : cReducible18 (k5p04Entries.get (k.cast k5p04Entries_length.symm)).cf
    (k5p04Entries.get (k.cast k5p04Entries_length.symm)).eqR (k5p04Entries.get (k.cast k5p04Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P04V
#print axioms K5P04V.hC_all
