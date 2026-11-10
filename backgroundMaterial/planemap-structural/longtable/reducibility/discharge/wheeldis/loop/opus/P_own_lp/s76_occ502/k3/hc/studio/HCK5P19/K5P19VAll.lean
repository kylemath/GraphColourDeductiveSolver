import K5P19V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5P19V
theorem hC_all (k : Fin 1) : cReducible18 (k5p19Entries.get (k.cast k5p19Entries_length.symm)).cf
    (k5p19Entries.get (k.cast k5p19Entries_length.symm)).eqR (k5p19Entries.get (k.cast k5p19Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5P19V
#print axioms K5P19V.hC_all
