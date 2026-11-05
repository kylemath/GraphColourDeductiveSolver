import HD13
open HD13 DCheck18
namespace HD13V
theorem hD_2 : DCheck18.dReducible (hd13Confs.get ⟨2, by rw [hd13Confs_length]; decide⟩) = true := by native_decide
end HD13V
#print axioms HD13V.hD_2
