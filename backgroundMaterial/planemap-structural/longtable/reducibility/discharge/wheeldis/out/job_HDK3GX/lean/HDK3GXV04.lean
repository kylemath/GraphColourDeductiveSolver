import HDK3GX
open HDK3GX DCheck18
namespace HDK3GXV
theorem hD_4 : DCheck18.dReducible (hdk3gxConfs.get ⟨4, by rw [hdk3gxConfs_length]; decide⟩) = true := by native_decide
end HDK3GXV
#print axioms HDK3GXV.hD_4
