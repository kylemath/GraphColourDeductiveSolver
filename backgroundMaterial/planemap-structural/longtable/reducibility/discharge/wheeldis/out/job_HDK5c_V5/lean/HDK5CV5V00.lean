import HDK5CV5
open HDK5CV5 DCheck18
namespace HDK5CV5V
theorem hD_0 : DCheck18.dReducible (hdk5cv5Confs.get ⟨0, by rw [hdk5cv5Confs_length]; decide⟩) = true := by native_decide
end HDK5CV5V
#print axioms HDK5CV5V.hD_0
