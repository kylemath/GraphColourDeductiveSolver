import HDW13
open HDW13 DCheck18
namespace HDW13V
theorem hD_15 : DCheck18.dReducible (hdw13Confs.get ⟨15, by rw [hdw13Confs_length]; decide⟩) = true := by native_decide
end HDW13V
#print axioms HDW13V.hD_15
