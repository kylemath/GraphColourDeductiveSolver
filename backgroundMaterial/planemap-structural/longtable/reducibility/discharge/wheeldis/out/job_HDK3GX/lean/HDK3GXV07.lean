import HDK3GX
open HDK3GX DCheck18
namespace HDK3GXV
theorem hD_7 : DCheck18.dReducible (hdk3gxConfs.get ⟨7, by rw [hdk3gxConfs_length]; decide⟩) = true := by native_decide
end HDK3GXV
#print axioms HDK3GXV.hD_7
