import CKQ5
open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck
namespace Q5V
theorem hC_0 : cReducible18 (q5Entries.get ⟨0, by rw [q5Entries_length]; decide⟩).cf (q5Entries.get ⟨0, by rw [q5Entries_length]; decide⟩).eqR (q5Entries.get ⟨0, by rw [q5Entries_length]; decide⟩).eqI = true := by native_decide
theorem hC_1 : cReducible18 (q5Entries.get ⟨1, by rw [q5Entries_length]; decide⟩).cf (q5Entries.get ⟨1, by rw [q5Entries_length]; decide⟩).eqR (q5Entries.get ⟨1, by rw [q5Entries_length]; decide⟩).eqI = true := by native_decide
theorem hC_2 : cReducible18 (q5Entries.get ⟨2, by rw [q5Entries_length]; decide⟩).cf (q5Entries.get ⟨2, by rw [q5Entries_length]; decide⟩).eqR (q5Entries.get ⟨2, by rw [q5Entries_length]; decide⟩).eqI = true := by native_decide
theorem hC_3 : cReducible18 (q5Entries.get ⟨3, by rw [q5Entries_length]; decide⟩).cf (q5Entries.get ⟨3, by rw [q5Entries_length]; decide⟩).eqR (q5Entries.get ⟨3, by rw [q5Entries_length]; decide⟩).eqI = true := by native_decide
theorem hC_4 : cReducible18 (q5Entries.get ⟨4, by rw [q5Entries_length]; decide⟩).cf (q5Entries.get ⟨4, by rw [q5Entries_length]; decide⟩).eqR (q5Entries.get ⟨4, by rw [q5Entries_length]; decide⟩).eqI = true := by native_decide
theorem hC_all (k : Fin 5) : cReducible18 (q5Entries.get (k.cast q5Entries_length.symm)).cf
    (q5Entries.get (k.cast q5Entries_length.symm)).eqR (q5Entries.get (k.cast q5Entries_length.symm)).eqI = true := by
  fin_cases k
  · exact hC_0
  · exact hC_1
  · exact hC_2
  · exact hC_3
  · exact hC_4
end Q5V
#print axioms Q5V.hC_all
