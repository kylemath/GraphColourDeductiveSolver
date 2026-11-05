import HDK7
open HDK7 DCheck18
namespace HDK7V
theorem hD_6 : DCheck18.dReducible (hdk7Confs.get ⟨6, by rw [hdk7Confs_length]; decide⟩) = true := by native_decide
end HDK7V
#print axioms HDK7V.hD_6
