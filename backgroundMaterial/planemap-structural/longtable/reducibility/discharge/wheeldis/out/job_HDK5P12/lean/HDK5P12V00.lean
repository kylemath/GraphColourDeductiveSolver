import HDK5P12
open HDK5P12 DCheck18
namespace HDK5P12V
theorem hD_0 : DCheck18.dReducible (hdk5p12Confs.get ⟨0, by rw [hdk5p12Confs_length]; decide⟩) = true := by native_decide
end HDK5P12V
#print axioms HDK5P12V.hD_0
