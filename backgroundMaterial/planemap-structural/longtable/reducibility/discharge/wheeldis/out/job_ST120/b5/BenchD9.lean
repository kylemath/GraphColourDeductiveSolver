import RSSTD9Core
import RSSTRulesN2
namespace SimpleGraph.SphericalMap.RSSTSeed
def dumpSurv : IO Unit := do
  let tab := cTab rsstParts79
  IO.println s!"tabOK {tabOK rsstParts79 tab}"
  for d in [9, 10, 11, 12, 13, 14] do
    let S := linkSurv tab d
    IO.FS.writeFile s!"cert/links{d}_lean.txt" ("\n".intercalate (S.map fun l => String.join (l.map toString)) ++ "\n")
    IO.println s!"d{d} {S.length}"
#eval dumpSurv
end SimpleGraph.SphericalMap.RSSTSeed
