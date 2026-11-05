import HDCtrl
open HDCtrl DCheck18
namespace HDCtrlV
theorem hD_0 : DCheck18.dReducible (hdcConfs.get ⟨0, by rw [hdcConfs_length]; decide⟩) = true := by native_decide
end HDCtrlV
#print axioms HDCtrlV.hD_0
