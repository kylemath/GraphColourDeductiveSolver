import DCheckData
open DCheck

/-- Usage: dcheck RMIN RMAX [LIMIT]  — run the checker on every RSST configuration with ring in range,
print name, ring, classes, ext (vs RSST), D-reducible (vs RSST contract = 0), depth, ms. -/
def main (args : List String) : IO Unit := do
  let rmin := (args.getD 0 "6").toNat!
  let rmax := (args.getD 1 "9").toNat!
  let lim := (args.getD 2 "100000").toNat!
  let mut agree := 0
  let mut total := 0
  for cf in rsst do
    if cf.r < rmin || cf.r > rmax || total ≥ lim then continue
    let t0 ← IO.monoMsNow
    let res := run cf
    let t1 ← IO.monoMsNow
    let d := res.reached == res.classes
    let ok := res.ext == cf.rsstExt && d == (cf.rsstContract == 0)
    total := total + 1
    if ok then agree := agree + 1
    IO.println s!"{cf.name} r={cf.r} m={cf.m} classes={res.classes} ext={res.ext} (RSST {cf.rsstExt}) D={d} (RSST contract {cf.rsstContract}) depth={res.depth} {t1 - t0}ms {if ok then "" else "MISMATCH"}"
    (← IO.getStdout).flush
  IO.println s!"agree {agree}/{total}"
