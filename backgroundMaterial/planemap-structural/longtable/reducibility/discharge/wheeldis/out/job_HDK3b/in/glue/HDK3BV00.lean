import HDK3B
open HDK3B DCheck18
namespace HDK3BV
theorem hD_0 : DCheck18.dReducible (hdk3bConfs.get ⟨0, by rw [hdk3bConfs_length]; decide⟩) = true := by native_decide
end HDK3BV
#print axioms HDK3BV.hD_0
