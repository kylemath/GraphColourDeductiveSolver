import HDK5P11
open HDK5P11 DCheck18
namespace HDK5P11V
theorem hD_0 : DCheck18.dReducible (hdk5p11Confs.get ⟨0, by rw [hdk5p11Confs_length]; decide⟩) = true := by native_decide
end HDK5P11V
#print axioms HDK5P11V.hD_0
