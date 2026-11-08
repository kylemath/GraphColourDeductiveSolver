import K5P02V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P02V
theorem hC_all (k : Fin 1) : cReducible18 (k5p02Entries.get (k.cast k5p02Entries_length.symm)).cf
    (k5p02Entries.get (k.cast k5p02Entries_length.symm)).eqR (k5p02Entries.get (k.cast k5p02Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P02V
#print axioms K5P02V.hC_all
