import CHW13
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace HW13V
theorem hC_2 : cReducible18 (w13Entries.get ⟨2, by rw [w13Entries_length]; decide⟩).cf (w13Entries.get ⟨2, by rw [w13Entries_length]; decide⟩).eqR (w13Entries.get ⟨2, by rw [w13Entries_length]; decide⟩).eqI = true := by native_decide
end HW13V
#print axioms HW13V.hC_2
