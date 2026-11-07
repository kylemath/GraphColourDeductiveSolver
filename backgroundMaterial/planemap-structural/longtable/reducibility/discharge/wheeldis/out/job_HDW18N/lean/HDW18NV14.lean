import HDW18N
open HDW18N DCheck18
namespace HDW18NV
theorem hD_14 : DCheck18.dReducible (hdw18nConfs.get ⟨14, by rw [hdw18nConfs_length]; decide⟩) = true := by native_decide
end HDW18NV
#print axioms HDW18NV.hD_14
