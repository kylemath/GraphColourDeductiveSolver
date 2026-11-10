import HDK5P14
open HDK5P14 DCheck18
namespace HDK5P14V
theorem hD_0 : DCheck18.dReducible (hdk5p14Confs.get ⟨0, by rw [hdk5p14Confs_length]; decide⟩) = true := by native_decide
end HDK5P14V
#print axioms HDK5P14V.hD_0
