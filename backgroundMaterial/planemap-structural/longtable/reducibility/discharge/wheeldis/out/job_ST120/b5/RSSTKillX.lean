import RSSTConfs

/-!
# ST-120 B5 M1: cross-check driver for `containsK` (evaluation only, no theorems)

`#eval` (interpreted) over `cases_kill.txt` (written by `py/xcheck_kill.py gen`, B2's case format
`id;d;link;apex;p_0,…,p_{d-1}`). For each case and each of the 633 configurations it runs the search `findEmb` and the
witness check `checkEmb`, and writes `lean_kill.txt`: `id k k …` (configurations contained), with `!k` for a search
result that fails `checkEmb` (expected never). `py/xcheck_kill.py cmp` compares with RSST-1SHOT (rcore.py).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

def digitsK (s : String) : List Nat := s.toList.map fun c => c.toNat - '0'.toNat

def parseCaseK (line : String) : Option (String × UWin) :=
  match line.splitOn ";" with
  | [id, d, link, apex, priv] =>
    some (id, { d := d.toNat!, link := digitsK link, apex := digitsK apex, priv := (priv.splitOn ",").map digitsK })
  | _ => none

def runKillCheck : IO Unit := do
  let txt ← IO.FS.readFile "cases_kill.txt"
  let mut out : Array String := #[]
  let mut nyes := 0
  for line in txt.splitOn "\n" do
    if line.isEmpty then continue
    match parseCaseK line with
    | none => throw (IO.userError s!"bad case line {line}")
    | some (id, W) =>
      let mut s := id
      for (K, k) in k633.zipIdx do
        match findEmb K W with
        | some e =>
          if checkEmb K W e then
            s := s ++ s!" {k}"
            nyes := nyes + 1
          else s := s ++ s!" !{k}"
        | none => pure ()
      out := out.push s
  IO.FS.writeFile "lean_kill.txt" ("\n".intercalate out.toList ++ "\n")
  IO.println s!"cases {out.size}; contained pairs {nyes}"

#eval runKillCheck

end SimpleGraph.SphericalMap.RSSTSeed
