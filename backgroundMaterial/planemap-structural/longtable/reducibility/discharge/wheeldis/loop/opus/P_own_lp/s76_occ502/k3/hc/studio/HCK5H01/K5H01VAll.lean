import K5H01V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5H01V
theorem hC_all (k : Fin 1) : cReducible18 (k5h01Entries.get (k.cast k5h01Entries_length.symm)).cf
    (k5h01Entries.get (k.cast k5h01Entries_length.symm)).eqR (k5h01Entries.get (k.cast k5h01Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5H01V
#print axioms K5H01V.hC_all
