import DCheck
/-!
# DCheckRef: `DCheck.run` factored into named pieces (exploratory)

`runRef` is `DCheck.run` with each inner loop moved into its own definition, the loop bodies copied
verbatim. `run_eq_runRef` proves the two are the same function (`rfl`: definitional unfolding only).
The soundness proof (`DCheckS1.lean`) reasons about the pieces.
-/
namespace DCheck
namespace Ref

def mkIndex (ks : Array Nat) : Std.HashMap Nat Nat := Id.run do
  let mut index : Std.HashMap Nat Nat := {}
  for i in [0:ks.size] do
    index := index.insert ks[i]! i
  return index

def mkT (r k th : Nat) : Array Nat := Id.run do
  let mut T : Array Nat := #[]
  for v in [0:r] do
    let x := col k v ^^^ col k ((v + 1) % r)
    if x != 0 && x != th then T := T.push v
  return T

def mkArc (r : Nat) (T : Array Nat) : Array Nat :=
  (Array.range r).map fun v => ((T.filter (· < v)).size + T.size - 1) % T.size

def mkRm (r n th : Nat) (arcOf lab : Array Nat) : Array Nat := Id.run do
  let mut rm : Array Nat := Array.replicate (n / 2 + 1) 0
  for v in [0:r] do
    let g := lab[arcOf[v]!]!
    rm := rm.set! g (rm[g]! ||| (th <<< (2 * v)))
  return rm

def xorSel (k n s : Nat) (rm : Array Nat) : Nat := Id.run do
  let mut k2 := k
  for b in [0:n / 2] do
    if (s >>> b) % 2 == 1 then k2 := k2 ^^^ rm[b + 1]!
  return k2

def satLoop (r n k : Nat) (index : Std.HashMap Nat Nat) (good : Array Bool) (rm : Array Nat) :
    Bool := Id.run do
  let mut sat := false
  for s in [1:(1 <<< (n / 2))] do
    let k2 := xorSel k n s rm
    match index[canon r k2]? with
    | some j =>
      if good[j]! then
        sat := true
        break
    | none => pure ()
  return sat

def ptrLoop (r n k th : Nat) (index : Std.HashMap Nat Nat) (good : Array Bool)
    (arcOf : Array Nat) (mats : Array (Array Nat)) (pi : Nat) : Nat := Id.run do
  let mut ptr := pi
  let mut stuck := false
  while ptr < mats.size && !stuck do
    let lab := mats[ptr]!
    let rm := mkRm r n th arcOf lab
    let sat := satLoop r n k index good rm
    if sat then ptr := ptr + 1 else stuck := true
  return ptr

def thLoop (r i k : Nat) (index : Std.HashMap Nat Nat) (good : Array Bool) (prog : Array Nat) :
    Array Nat × Bool := Id.run do
  let dead := 1000000
  let mut prog := prog
  let mut done := false
  for th in [1:4] do
    if done then break
    let pi := prog[3 * i + th - 1]!
    if pi == dead then continue
    let T := mkT r k th
    let n := T.size
    if n == 0 then
      prog := prog.set! (3 * i + th - 1) dead
      continue
    let arcOf := (Array.range r).map fun v => ((T.filter (· < v)).size + n - 1) % n
    let mats := matchTable[n / 2]!
    let ptr := ptrLoop r n k th index good arcOf mats pi
    prog := prog.set! (3 * i + th - 1) ptr
    if ptr == mats.size then done := true
  return (prog, done)

def iLoop (r : Nat) (ks : Array Nat) (index : Std.HashMap Nat Nat) (good : Array Bool)
    (prog : Array Nat) : Array Nat × Array Nat := Id.run do
  let mut prog := prog
  let mut new : Array Nat := #[]
  for i in [0:ks.size] do
    if good[i]! then continue
    let k := ks[i]!
    let (prog', done) := thLoop r i k index good prog
    prog := prog'
    if done then new := new.push i
  return (prog, new)

def setLoop (new : Array Nat) (good : Array Bool) : Array Bool := Id.run do
  let mut good := good
  for i in new do good := good.set! i true
  return good

def runRef (cf : Conf) : Result := Id.run do
  let r := cf.r
  let ks := ringColourings r
  let N := ks.size
  let index := mkIndex ks
  let mut good : Array Bool := ks.map (extendsQ cf)
  let ext := (good.filter id).size
  let mut reached := ext
  let mut prog : Array Nat := Array.replicate (3 * N) 0
  let mut depth := 0
  for _ in [0:N + 1] do
    let (prog', new) := iLoop r ks index good prog
    prog := prog'
    if new.isEmpty then break
    good := setLoop new good
    reached := reached + new.size
    depth := depth + 1
  return { classes := N, ext := ext, reached := reached, depth := depth }

end Ref

theorem run_eq_runRef (cf : Conf) : run cf = Ref.runRef cf := by
  rfl

end DCheck
