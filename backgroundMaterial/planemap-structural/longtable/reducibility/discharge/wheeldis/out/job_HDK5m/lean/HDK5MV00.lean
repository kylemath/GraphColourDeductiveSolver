import HDK5M
open HDK5M DCheck18
namespace HDK5MV
theorem hD_0 : DCheck18.dReducible (hdk5mConfs.get ⟨0, by rw [hdk5mConfs_length]; decide⟩) = true := by native_decide
end HDK5MV
#print axioms HDK5MV.hD_0
