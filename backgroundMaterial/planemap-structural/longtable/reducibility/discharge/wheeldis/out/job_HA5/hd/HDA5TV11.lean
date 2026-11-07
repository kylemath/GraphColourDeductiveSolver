import HDA5T
open HDA5T DCheck18
namespace HDA5TV
theorem hD_11 : DCheck18.dReducible (hda5tConfs.get ⟨11, by rw [hda5tConfs_length]; decide⟩) = true := by native_decide
end HDA5TV
#print axioms HDA5TV.hD_11
