import DCheck18
open DCheck18

/-! Studio Job 8/9 (exploratory): run the DCheck closure on configurations read from a file.
Input lines: `name r m ra_0;ra_1;...;ra_{m-1} ia_0;...;ia_{m-1}` where ra_i / ia_i are comma-separated ring /
interior neighbour lists of interior vertex i (empty list = `-`).  Output per line: name, r, m, classes, ext,
reached, D-reducible, depth, ms.  Rings up to 19 (DCheck18: matchTable p <= 9). -/

def parseList (s : String) : Array Nat :=
  if s == "-" then #[] else (s.splitOn ",").toArray.map (·.toNat!)

def parseConf (line : String) : Option Conf :=
  match line.splitOn " " with
  | [name, r, m, ra, ia] =>
    some { name := name, r := r.toNat!, m := m.toNat!,
           ringAdj := (ra.splitOn ";").toArray.map parseList,
           intAdj := (ia.splitOn ";").toArray.map parseList }
  | _ => none

def main (args : List String) : IO Unit := do
  let path := args.getD 0 "configs.txt"
  let lines ← IO.FS.lines path
  for line in lines do
    match parseConf line with
    | none => pure ()
    | some cf =>
      if cf.r > 19 then
        IO.println s!"{cf.name} r={cf.r} m={cf.m} SKIP ring>19"
        continue
      let t0 ← IO.monoMsNow
      let res := run cf
      let t1 ← IO.monoMsNow
      IO.println s!"{cf.name} r={cf.r} m={cf.m} classes={res.classes} ext={res.ext} reached={res.reached} D={res.reached == res.classes} depth={res.depth} {t1 - t0}ms"
      (← IO.getStdout).flush
