import K5P18V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P18V
theorem hC_all (k : Fin 1) : cReducible18 (k5p18Entries.get (k.cast k5p18Entries_length.symm)).cf
    (k5p18Entries.get (k.cast k5p18Entries_length.symm)).eqR (k5p18Entries.get (k.cast k5p18Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P18V
#print axioms K5P18V.hC_all
