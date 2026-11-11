import RSSTRulesN2

/-! ST-120 B5: dump `rsstParts79` (B2 `RSSTRulesN2`) as `cert/parts79.txt` in parts71.txt format (for the exporter). -/

namespace SimpleGraph.SphericalMap.RSSTSeed

def fmtR5 (r : Rng) : String :=
  if r.isFull then "*" else if r.lo == r.hi then s!"={r.lo}" else if r.hi == 9 then s!">={r.lo}"
  else if r.lo == 5 then s!"<={r.hi}" else s!"in{r.lo}..{r.hi}"

def partLine5 (p : Part) : String :=
  let subs := p.subs.map fun s => s!"{fmtR5 s.spoke}[{fmtR5 s.hat}|{",".intercalate (s.fans.map fmtR5)}]"
  s!"{p.tag}\t{p.subs.length}\t{"  ".intercalate subs}"

#eval IO.FS.writeFile "cert/parts79.txt" ("\n".intercalate (rsstParts79.map partLine5) ++ "\n")

end SimpleGraph.SphericalMap.RSSTSeed
