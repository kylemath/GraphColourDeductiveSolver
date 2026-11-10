import K5P21V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P21V
theorem hC_all (k : Fin 1) : cReducible18 (k5p21Entries.get (k.cast k5p21Entries_length.symm)).cf
    (k5p21Entries.get (k.cast k5p21Entries_length.symm)).eqR (k5p21Entries.get (k.cast k5p21Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P21V
#print axioms K5P21V.hC_all
