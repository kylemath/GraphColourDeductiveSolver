import HDK5CV2
open HDK5CV2 DCheck18
namespace HDK5CV2V
theorem hD_0 : DCheck18.dReducible (hdk5cv2Confs.get ⟨0, by rw [hdk5cv2Confs_length]; decide⟩) = true := by native_decide
end HDK5CV2V
#print axioms HDK5CV2V.hD_0
