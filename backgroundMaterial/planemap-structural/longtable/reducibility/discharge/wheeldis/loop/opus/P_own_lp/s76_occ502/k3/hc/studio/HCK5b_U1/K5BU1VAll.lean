import K5BU1V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5BU1V
theorem hC_all (k : Fin 1) : cReducible18 (k5bu1Entries.get (k.cast k5bu1Entries_length.symm)).cf
    (k5bu1Entries.get (k.cast k5bu1Entries_length.symm)).eqR (k5bu1Entries.get (k.cast k5bu1Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5BU1V
#print axioms K5BU1V.hC_all
