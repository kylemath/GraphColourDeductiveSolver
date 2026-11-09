import HDK5P06
open HDK5P06 DCheck18
namespace HDK5P06V
theorem hD_0 : DCheck18.dReducible (hdk5p06Confs.get ⟨0, by rw [hdk5p06Confs_length]; decide⟩) = true := by native_decide
end HDK5P06V
#print axioms HDK5P06V.hD_0
