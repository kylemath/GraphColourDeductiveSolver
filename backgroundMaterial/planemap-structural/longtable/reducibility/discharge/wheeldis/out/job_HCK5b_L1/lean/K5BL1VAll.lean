import K5BL1V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5BL1V
theorem hC_all (k : Fin 1) : cReducible18 (k5bl1Entries.get (k.cast k5bl1Entries_length.symm)).cf
    (k5bl1Entries.get (k.cast k5bl1Entries_length.symm)).eqR (k5bl1Entries.get (k.cast k5bl1Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5BL1V
#print axioms K5BL1V.hC_all
