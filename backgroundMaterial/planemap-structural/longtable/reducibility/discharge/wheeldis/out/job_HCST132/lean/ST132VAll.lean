import ST132V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace ST132V
theorem hC_all (k : Fin 1) : cReducible18 (st132Entries.get (k.cast st132Entries_length.symm)).cf
    (st132Entries.get (k.cast st132Entries_length.symm)).eqR (st132Entries.get (k.cast st132Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end ST132V
#print axioms ST132V.hC_all
