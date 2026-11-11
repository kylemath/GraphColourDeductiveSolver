import RSSTKillRot768
namespace SimpleGraph.SphericalMap.RSSTSeed
#eval (k768R.length, k768R.all rotWF)
-- demo: link 5567757, rsst213 (index 192 in k768) mirror-only placement
#eval (k768R.findIdx? fun K => K.1.name == "rsst213_184o3686406")
#eval match k768R[192]? with
  | some K => (K.1.name, rotOK K 7 [5,5,6,7,7,5,7] [0,1,2,3,6,5,8,9,12,28], embShape K.1 7 [5,5,6,7,7,5,7] [0,1,2,3,6,5,8,9,12,28])
  | none => ("", false, false)
end SimpleGraph.SphericalMap.RSSTSeed
