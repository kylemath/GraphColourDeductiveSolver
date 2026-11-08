import HDK5BL3
open HDK5BL3 DCheck18
namespace HDK5BL3V
theorem hD_0 : DCheck18.dReducible (hdk5bl3Confs.get ⟨0, by rw [hdk5bl3Confs_length]; decide⟩) = true := by native_decide
end HDK5BL3V
#print axioms HDK5BL3V.hD_0
