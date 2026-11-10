import RSSTRulesN2
import RSSTCheck

/-!
# ST-120 B2 follow-up: cross-check driver for the 79 parts (evaluation only, no theorems)

Like `RSSTCheck.lean`, with `rsstParts79`: reads `cases_n2.txt` (written by `crosscheck_n2.py gen`), writes
`lean_out_n2.txt` (same line format) and `lean_parts_n2.txt` (the 8 N2 parts in the parts71.txt format).
`RSSTCheck` is imported only for `parseCase`, `firedStr`, `partLine` (an import does not re-run its `#eval`).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

def loHiWith (W : UWin) (parts : List Part) : Int × Int :=
  (W.fired parts).foldl (fun (lh : Int × Int) f =>
    let s : Int := if f.res == .sure then 1 else 0
    if f.into then (lh.1 + s, lh.2 + 1) else (lh.1 - 1, lh.2 - s)) (10 * (6 - (W.d : Int)), 10 * (6 - (W.d : Int)))

def boolDisagreeWith (W : UWin) (parts : List Part) (c : Nat) : Nat :=
  let du :=
    if 5 ≤ W.d ∧ W.d ≤ 8 then
      (parts.filter (·.hub == W.d)).foldl (fun acc p =>
        acc + ((List.range W.d).filter fun a =>
          (p.fitsAt (W.viewU.map (·.fill c)) a) != (p.fit3At W.viewU a == .sure)).length) 0
    else 0
  let dw := (List.range W.d).foldl (fun acc i =>
    let n := W.linkL i
    if n ≤ 8 then
      acc + ((parts.filter (·.hub == n)).filter fun p =>
        (p.fitsAt ((W.viewW i).map (·.fill c)) (n - 2)) != (p.fit3At (W.viewW i) (n - 2) == .sure)).length
    else acc) 0
  du + dw

def runCheckN2 : IO Unit := do
  let txt ← IO.FS.readFile "cases_n2.txt"
  let mut out : Array String := #[]
  let mut n := 0
  for line in txt.splitOn "\n" do
    if line.isEmpty then continue
    match parseCase line with
    | none => throw (IO.userError s!"bad case line {line}")
    | some (id, W) =>
      let fs := W.fired rsstParts79
      let (lo, hi) := loHiWith W rsstParts79
      let nOpen := (fs.filter (·.res == .open_)).length
      out := out.push (s!"{id} {lo} {hi} {nOpen} {boolDisagreeWith W rsstParts79 5} {boolDisagreeWith W rsstParts79 9} " ++
        " ".intercalate (fs.map firedStr))
      n := n + 1
  IO.FS.writeFile "lean_out_n2.txt" ("\n".intercalate out.toList ++ "\n")
  IO.FS.writeFile "lean_parts_n2.txt" ("\n".intercalate (rsstPartsN2.map partLine) ++ "\n")
  IO.println s!"cases {n}; parts {rsstParts79.length}; local(79) {rsstParts79.all Part.isLocal}; wellShaped(79) {rsstParts79.all Part.wellShaped}"

#eval runCheckN2

end SimpleGraph.SphericalMap.RSSTSeed

#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstPartsN2_length
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts79_length
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts79_count_by_hub
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts79_wellShaped
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts79_local
