import K5P07V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P07V
theorem hC_all (k : Fin 1) : cReducible18 (k5p07Entries.get (k.cast k5p07Entries_length.symm)).cf
    (k5p07Entries.get (k.cast k5p07Entries_length.symm)).eqR (k5p07Entries.get (k.cast k5p07Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P07V
#print axioms K5P07V.hC_all
