import HDR5
open HDR5 DCheck18
namespace HDR5V
theorem hD_1 : DCheck18.dReducible (hdr5Confs.get ⟨1, by rw [hdr5Confs_length]; decide⟩) = true := by native_decide
end HDR5V
#print axioms HDR5V.hD_1
