import HDK5P08
open HDK5P08 DCheck18
namespace HDK5P08V
theorem hD_0 : DCheck18.dReducible (hdk5p08Confs.get ⟨0, by rw [hdk5p08Confs_length]; decide⟩) = true := by native_decide
end HDK5P08V
#print axioms HDK5P08V.hD_0
