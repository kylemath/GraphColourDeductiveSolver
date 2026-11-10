import HDK5P13
open HDK5P13 DCheck18
namespace HDK5P13V
theorem hD_0 : DCheck18.dReducible (hdk5p13Confs.get ⟨0, by rw [hdk5p13Confs_length]; decide⟩) = true := by native_decide
end HDK5P13V
#print axioms HDK5P13V.hD_0
