import HDOF7
open HDOF7 DCheck18
namespace HDOF7V
theorem hD_13 : DCheck18.dReducible (hdof7Confs.get ⟨13, by rw [hdof7Confs_length]; decide⟩) = true := by native_decide
end HDOF7V
#print axioms HDOF7V.hD_13
