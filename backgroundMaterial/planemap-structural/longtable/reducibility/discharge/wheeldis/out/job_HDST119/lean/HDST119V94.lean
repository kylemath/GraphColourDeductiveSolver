import HDST119
open HDST119 DCheck18
namespace HDST119V
theorem hD_94 : DCheck18.dReducible (hdst119Confs.get ⟨94, by rw [hdst119Confs_length]; decide⟩) = true := by native_decide
end HDST119V
#print axioms HDST119V.hD_94
