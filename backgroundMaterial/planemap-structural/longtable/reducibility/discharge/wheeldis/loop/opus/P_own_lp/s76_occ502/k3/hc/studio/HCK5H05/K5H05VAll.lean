import K5H05V00
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace K5H05V
theorem hC_all (k : Fin 1) : cReducible18 (k5h05Entries.get (k.cast k5h05Entries_length.symm)).cf
    (k5h05Entries.get (k.cast k5h05Entries_length.symm)).eqR (k5h05Entries.get (k.cast k5h05Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
end K5H05V
#print axioms K5H05V.hC_all
