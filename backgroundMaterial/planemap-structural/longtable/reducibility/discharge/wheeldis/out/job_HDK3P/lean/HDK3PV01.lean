import HDK3P
open HDK3P DCheck18
namespace HDK3PV
theorem hD_1 : DCheck18.dReducible (hdk3pConfs.get ⟨1, by rw [hdk3pConfs_length]; decide⟩) = true := by native_decide
end HDK3PV
#print axioms HDK3PV.hD_1
