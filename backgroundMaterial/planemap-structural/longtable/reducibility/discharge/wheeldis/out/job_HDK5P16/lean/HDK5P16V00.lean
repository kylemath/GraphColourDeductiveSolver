import HDK5P16
open HDK5P16 DCheck18
namespace HDK5P16V
theorem hD_0 : DCheck18.dReducible (hdk5p16Confs.get ⟨0, by rw [hdk5p16Confs_length]; decide⟩) = true := by native_decide
end HDK5P16V
#print axioms HDK5P16V.hD_0
