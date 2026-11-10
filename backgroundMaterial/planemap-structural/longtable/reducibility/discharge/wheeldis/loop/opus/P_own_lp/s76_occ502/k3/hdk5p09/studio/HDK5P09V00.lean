import HDK5P09
open HDK5P09 DCheck18
namespace HDK5P09V
theorem hD_0 : DCheck18.dReducible (hdk5p09Confs.get ⟨0, by rw [hdk5p09Confs_length]; decide⟩) = true := by native_decide
end HDK5P09V
#print axioms HDK5P09V.hD_0
