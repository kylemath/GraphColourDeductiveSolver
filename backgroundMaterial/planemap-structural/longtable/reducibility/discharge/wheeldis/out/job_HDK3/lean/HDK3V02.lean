import HDK3
open HDK3 DCheck18
namespace HDK3V
theorem hD_2 : DCheck18.dReducible (hdk3Confs.get ⟨2, by rw [hdk3Confs_length]; decide⟩) = true := by native_decide
end HDK3V
#print axioms HDK3V.hD_2
