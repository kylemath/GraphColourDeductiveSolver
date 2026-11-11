import RSSTCheckCore
import RSSTConfs
set_option profiler true
namespace SimpleGraph.SphericalMap.RSSTSeed
def benchS (d : Nat) : IO Unit := do
  let ls := ((← IO.FS.readFile s!"cert/sample{d}_links.txt").splitOn "\n").filter (· ≠ "")
  let cs := parseCert (← IO.FS.readFile s!"cert/sample{d}.txt")
  let mut ok := 0
  let t0 ← IO.monoMsNow
  for (l, c) in ls.zip cs do
    let link := l.toList.map fun ch => ch.toNat - '0'.toNat
    if checkLink k633 d link c then ok := ok + 1
  let t1 ← IO.monoMsNow
  IO.println s!"d{d}: links {ls.length} ok {ok} ms {t1 - t0}"
#eval benchS 7
#eval benchS 8
end SimpleGraph.SphericalMap.RSSTSeed
