import HDRS403
open HDRS403 DCheck18
namespace HDRS403V
theorem hD_30 : DCheck18.dReducible (hdrs403Confs.get ⟨30, by rw [hdrs403Confs_length]; decide⟩) = true := by native_decide
end HDRS403V
#print axioms HDRS403V.hD_30
