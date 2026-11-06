import CW2B
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace W2BV
theorem hC_5 : cReducible18 (w2bEntries.get ⟨5, by rw [w2bEntries_length]; decide⟩).cf (w2bEntries.get ⟨5, by rw [w2bEntries_length]; decide⟩).eqR (w2bEntries.get ⟨5, by rw [w2bEntries_length]; decide⟩).eqI = true := by native_decide
end W2BV
#print axioms W2BV.hC_5
