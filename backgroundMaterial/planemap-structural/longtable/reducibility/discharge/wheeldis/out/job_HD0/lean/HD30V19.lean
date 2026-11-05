import HD30
open HD30 DCheck18
namespace HD30V
theorem hD_19 : DCheck18.dReducible (hd30Confs.get ⟨19, by rw [hd30Confs_length]; decide⟩) = true := by native_decide
end HD30V
#print axioms HD30V.hD_19
