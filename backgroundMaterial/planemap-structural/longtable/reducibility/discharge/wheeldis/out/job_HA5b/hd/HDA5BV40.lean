import HDA5B
open HDA5B DCheck18
namespace HDA5BV
theorem hD_40 : DCheck18.dReducible (hda5bConfs.get ⟨40, by rw [hda5bConfs_length]; decide⟩) = true := by native_decide
end HDA5BV
#print axioms HDA5BV.hD_40
