import K5BL2V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5BL2V
theorem hC_all (k : Fin 1) : cReducible18 (k5bl2Entries.get (k.cast k5bl2Entries_length.symm)).cf
    (k5bl2Entries.get (k.cast k5bl2Entries_length.symm)).eqR (k5bl2Entries.get (k.cast k5bl2Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5BL2V
#print axioms K5BL2V.hC_all
