import HDOF7
open HDOF7 DCheck18
namespace HDOF7V
theorem hD_56 : DCheck18.dReducible (hdof7Confs.get ⟨56, by rw [hdof7Confs_length]; decide⟩) = true := by native_decide
end HDOF7V
#print axioms HDOF7V.hD_56
