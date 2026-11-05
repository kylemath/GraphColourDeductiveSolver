import HDB3
open HDB3 DCheck18
namespace HDB3V
theorem hD_3 : DCheck18.dReducible (hdb3Confs.get ⟨3, by rw [hdb3Confs_length]; decide⟩) = true := by native_decide
end HDB3V
#print axioms HDB3V.hD_3
