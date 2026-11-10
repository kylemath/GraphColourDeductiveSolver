import HDK5P10
open HDK5P10 DCheck18
namespace HDK5P10V
theorem hD_0 : DCheck18.dReducible (hdk5p10Confs.get ⟨0, by rw [hdk5p10Confs_length]; decide⟩) = true := by native_decide
end HDK5P10V
#print axioms HDK5P10V.hD_0
