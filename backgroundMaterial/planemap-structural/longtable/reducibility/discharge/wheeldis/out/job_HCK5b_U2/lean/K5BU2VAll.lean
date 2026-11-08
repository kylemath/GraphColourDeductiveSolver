import K5BU2V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5BU2V
theorem hC_all (k : Fin 1) : cReducible18 (k5bu2Entries.get (k.cast k5bu2Entries_length.symm)).cf
    (k5bu2Entries.get (k.cast k5bu2Entries_length.symm)).eqR (k5bu2Entries.get (k.cast k5bu2Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5BU2V
#print axioms K5BU2V.hC_all
