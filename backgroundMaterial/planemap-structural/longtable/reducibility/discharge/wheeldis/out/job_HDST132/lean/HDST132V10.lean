import HDST132
open HDST132 DCheck18
namespace HDST132V
theorem hD_10 : DCheck18.dReducible (hdst132Confs.get ⟨10, by rw [hdst132Confs_length]; decide⟩) = true := by native_decide
end HDST132V
#print axioms HDST132V.hD_10
