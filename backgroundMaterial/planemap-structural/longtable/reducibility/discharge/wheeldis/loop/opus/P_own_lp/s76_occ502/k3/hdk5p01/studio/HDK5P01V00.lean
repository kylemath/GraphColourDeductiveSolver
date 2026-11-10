import HDK5P01
open HDK5P01 DCheck18
namespace HDK5P01V
theorem hD_0 : DCheck18.dReducible (hdk5p01Confs.get ⟨0, by rw [hdk5p01Confs_length]; decide⟩) = true := by native_decide
end HDK5P01V
#print axioms HDK5P01V.hD_0
