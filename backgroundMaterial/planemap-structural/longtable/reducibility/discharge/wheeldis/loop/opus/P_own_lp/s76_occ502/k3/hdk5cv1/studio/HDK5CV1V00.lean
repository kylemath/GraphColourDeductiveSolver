import HDK5CV1
open HDK5CV1 DCheck18
namespace HDK5CV1V
theorem hD_0 : DCheck18.dReducible (hdk5cv1Confs.get ⟨0, by rw [hdk5cv1Confs_length]; decide⟩) = true := by native_decide
end HDK5CV1V
#print axioms HDK5CV1V.hD_0
