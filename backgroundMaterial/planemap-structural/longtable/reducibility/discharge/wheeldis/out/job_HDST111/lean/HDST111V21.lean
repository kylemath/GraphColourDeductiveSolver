import HDST111
open HDST111 DCheck18
namespace HDST111V
theorem hD_21 : DCheck18.dReducible (hdst111Confs.get ⟨21, by rw [hdst111Confs_length]; decide⟩) = true := by native_decide
end HDST111V
#print axioms HDST111V.hD_21
