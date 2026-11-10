import HDST123
open HDST123 DCheck18
namespace HDST123V
theorem hD_0 : DCheck18.dReducible (hdst123Confs.get ⟨0, by rw [hdst123Confs_length]; decide⟩) = true := by native_decide
end HDST123V
#print axioms HDST123V.hD_0
