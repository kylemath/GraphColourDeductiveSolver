import HDK5CV4
open HDK5CV4 DCheck18
namespace HDK5CV4V
theorem hD_0 : DCheck18.dReducible (hdk5cv4Confs.get ⟨0, by rw [hdk5cv4Confs_length]; decide⟩) = true := by native_decide
end HDK5CV4V
#print axioms HDK5CV4V.hD_0
