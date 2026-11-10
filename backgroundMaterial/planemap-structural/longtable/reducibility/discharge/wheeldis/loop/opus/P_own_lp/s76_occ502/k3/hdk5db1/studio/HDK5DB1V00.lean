import HDK5DB1
open HDK5DB1 DCheck18
namespace HDK5DB1V
theorem hD_0 : DCheck18.dReducible (hdk5db1Confs.get ⟨0, by rw [hdk5db1Confs_length]; decide⟩) = true := by native_decide
end HDK5DB1V
#print axioms HDK5DB1V.hD_0
