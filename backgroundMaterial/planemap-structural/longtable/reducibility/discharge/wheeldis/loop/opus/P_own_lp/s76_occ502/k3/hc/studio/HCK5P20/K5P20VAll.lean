import K5P20V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P20V
theorem hC_all (k : Fin 1) : cReducible18 (k5p20Entries.get (k.cast k5p20Entries_length.symm)).cf
    (k5p20Entries.get (k.cast k5p20Entries_length.symm)).eqR (k5p20Entries.get (k.cast k5p20Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P20V
#print axioms K5P20V.hC_all
