import K5P22V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P22V
theorem hC_all (k : Fin 1) : cReducible18 (k5p22Entries.get (k.cast k5p22Entries_length.symm)).cf
    (k5p22Entries.get (k.cast k5p22Entries_length.symm)).eqR (k5p22Entries.get (k.cast k5p22Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P22V
#print axioms K5P22V.hC_all
