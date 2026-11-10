import RSSTView

/-!
# ST-120 B2: cross-check driver (evaluation only, no theorems)

`#eval` (interpreted, no `native_decide`) of the B2 semantics on the windows in `cases.txt` (written by
`crosscheck.py gen`). For each case it writes one line to `lean_out.txt`:

`id lo hi nOpen dis5 dis9 fit fit …` with `fit = tag@hub>target:S` (sure) or `:O` (OPEN), `nOpen` the number of OPEN
fits, and `dis5` / `dis9` the number of fit attempts where the Bool `Part.fitsAt` on the view with ring 3 filled by 5 /
by 9 disagrees with the three-valued result being `sure`.

It also writes `lean_parts.txt`: the 71 parts in the format of `in/inputs/parts71.txt`, and runs a planted locality
control (a part with a non-`*` hat on subpart 0 must fail `Part.isLocal`).

Case line format: `id;d;link;apex;p_0,p_1,…,p_{d-1}` with letters as digits and `p_i` the private letters of `w_i`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

def digits (s : String) : List Nat := s.toList.map fun c => c.toNat - '0'.toNat

def parseCase (line : String) : Option (String × UWin) :=
  match line.splitOn ";" with
  | [id, d, link, apex, priv] =>
    some (id, { d := d.toNat!, link := digits link, apex := digits apex,
                priv := (priv.splitOn ",").map digits })
  | _ => none

def triTag : Tri → String
  | .sure => "S"
  | .open_ => "O"
  | .no => "N"

def firedStr (f : UWin.Fired) : String :=
  let hub := match f.hub with | none => "u" | some i => s!"w{i}"
  let tgt := if f.into then "u" else s!"w{f.recv}"
  s!"{f.tag}@{hub}>{tgt}:{triTag f.res}"

def fmtR (r : Rng) : String :=
  if r.isFull then "*" else if r.lo == r.hi then s!"={r.lo}" else if r.hi == 9 then s!">={r.lo}"
  else if r.lo == 5 then s!"<={r.hi}" else s!"in{r.lo}..{r.hi}"

def partLine (p : Part) : String :=
  let subs := p.subs.map fun s => s!"{fmtR s.spoke}[{fmtR s.hat}|{",".intercalate (s.fans.map fmtR)}]"
  s!"{p.tag}\t{p.subs.length}\t{"  ".intercalate subs}"

def runCheck : IO Unit := do
  let txt ← IO.FS.readFile "cases.txt"
  let mut out : Array String := #[]
  let mut n := 0
  for line in txt.splitOn "\n" do
    if line.isEmpty then continue
    match parseCase line with
    | none => throw (IO.userError s!"bad case line {line}")
    | some (id, W) =>
      let fs := W.fired
      let (lo, hi) := W.loHi
      let nOpen := (fs.filter (·.res == .open_)).length
      out := out.push (s!"{id} {lo} {hi} {nOpen} {W.boolDisagree 5} {W.boolDisagree 9} " ++
        " ".intercalate (fs.map firedStr))
      n := n + 1
  IO.FS.writeFile "lean_out.txt" ("\n".intercalate out.toList ++ "\n")
  IO.FS.writeFile "lean_parts.txt" ("\n".intercalate (rsstParts.map partLine) ++ "\n")
  -- planted locality control: drule1 with hat `5` on subpart 0 (read across a ring-2 edge from a hub w_i)
  let bad : Part := match rsstParts.head? with
    | some p => { p with subs := p.subs.set 0 { spoke := ⟨5, 9⟩, hat := ⟨5, 5⟩, fans := [] } }
    | none => p0
  IO.println s!"cases {n}; parts {rsstParts.length}; local(all) {rsstParts.all Part.isLocal}; planted control local {bad.isLocal}"
where p0 : Part := { tag := "", base := "", isMirror := false, hub := 0, subs := [], target := 2, amount := 1 }

#eval runCheck

end SimpleGraph.SphericalMap.RSSTSeed

#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts_length
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts_count_by_hub
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts_wellShaped
#print axioms SimpleGraph.SphericalMap.RSSTSeed.rsstParts_local
#print axioms SimpleGraph.SphericalMap.RSSTSeed.slotPosU_not_ring3
