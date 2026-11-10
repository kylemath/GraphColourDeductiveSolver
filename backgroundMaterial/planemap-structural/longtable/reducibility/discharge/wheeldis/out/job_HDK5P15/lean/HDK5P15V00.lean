import HDK5P15
open HDK5P15 DCheck18
namespace HDK5P15V
theorem hD_0 : DCheck18.dReducible (hdk5p15Confs.get ⟨0, by rw [hdk5p15Confs_length]; decide⟩) = true := by native_decide
end HDK5P15V
#print axioms HDK5P15V.hD_0
