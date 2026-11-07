import HDK3C
open HDK3C DCheck18
namespace HDK3CV
theorem hD_0 : DCheck18.dReducible (hdk3cConfs.get ⟨0, by rw [hdk3cConfs_length]; decide⟩) = true := by native_decide
end HDK3CV
#print axioms HDK3CV.hD_0
