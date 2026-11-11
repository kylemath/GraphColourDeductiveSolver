import RSSTCheckCore

/-!
# ST-120 B5 M2: cross-check of the symbolic instances (evaluation only, no theorems)

For every link word listed in `cert/inst_py_all.txt` (written by `py/export_cert.py --dump-inst`, which re-runs
RSST-1SHOT's `rcore.fit` with every test kept), compute the checker's own `instIn` / `instOut` (B2's views on the
tagged word, `symFit`), drop `no`, and write `cert/inst_lean_all.txt` in the same format: `LINK in I I … out I I …`,
each `I` = `code:lo-hi&…` (sorted) with `+O` if OPEN, the instances sorted as strings.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

def condStr (cr : Nat × Rng) : String := s!"{cr.1}:{cr.2.lo}-{cr.2.hi}"

def condLt (a b : Nat × Rng) : Bool :=
  a.1 < b.1 || (a.1 == b.1 && (a.2.lo < b.2.lo || (a.2.lo == b.2.lo && a.2.hi < b.2.hi)))

def instStr : SRes → String
  | .no => "NO"
  | .c cs o => "&".intercalate ((cs.mergeSort condLt).map condStr) ++ (if o then "+O" else "")

def instsStr (l : List SRes) : String :=
  " ".intercalate ((l.map instStr).mergeSort fun a b => decide (a ≤ b))

def runInstCheck : IO Unit := do
  let txt ← IO.FS.readFile "cert/inst_py_all.txt"
  let mut out : Array String := #[]
  for line in txt.splitOn "\n" do
    match line.splitOn " " with
    | w :: _ =>
      if w.isEmpty then continue
      let link := w.toList.map fun c => c.toNat - '0'.toNat
      let X := tagW link.length link
      let ins := (instIn rsstParts X).filter (· != .no)
      let outs := (instOut rsstParts X).filter (· != .no)
      out := out.push s!"{w} in {instsStr ins} out {instsStr outs}"
    | [] => continue
  IO.FS.writeFile "cert/inst_lean_all.txt" ("\n".intercalate out.toList ++ "\n")
  IO.println s!"links {out.size}"

#eval runInstCheck

end SimpleGraph.SphericalMap.RSSTSeed
