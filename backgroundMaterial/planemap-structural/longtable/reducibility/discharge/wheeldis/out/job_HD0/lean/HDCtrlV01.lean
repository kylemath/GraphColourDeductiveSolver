import HDCtrl
open HDCtrl DCheck18
namespace HDCtrlV
theorem hD_1 : DCheck18.dReducible (hdcConfs.get ⟨1, by rw [hdcConfs_length]; decide⟩) = true := by native_decide
end HDCtrlV
#print axioms HDCtrlV.hD_1
