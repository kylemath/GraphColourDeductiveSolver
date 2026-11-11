import HDRS403
open HDRS403 DCheck18
namespace HDRS403V
theorem hD_180 : DCheck18.dReducible (hdrs403Confs.get ⟨180, by rw [hdrs403Confs_length]; decide⟩) = true := by native_decide
end HDRS403V
#print axioms HDRS403V.hD_180
