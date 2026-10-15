import DCheckRef
import DCheckT
/-! Job 23: `DCheckRef` with the matching table as a parameter (`thLoopT`, `iLoopT`, `runRefT`);
the table-free pieces are reused from `DCheck.Ref`. -/
namespace DCheck
namespace Ref

def thLoopT (mt : Array (Array (Array Nat))) (r i k : Nat) (index : Std.HashMap Nat Nat) (good : Array Bool) (prog : Array Nat) :
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
    let mats := mt[n / 2]!
    let ptr := ptrLoop r n k th index good arcOf mats pi
    prog := prog.set! (3 * i + th - 1) ptr
    if ptr == mats.size then done := true
  return (prog, done)

def iLoopT (mt : Array (Array (Array Nat))) (r : Nat) (ks : Array Nat) (index : Std.HashMap Nat Nat) (good : Array Bool)
    (prog : Array Nat) : Array Nat × Array Nat := Id.run do
  let mut prog := prog
  let mut new : Array Nat := #[]
  for i in [0:ks.size] do
    if good[i]! then continue
    let k := ks[i]!
    let (prog', done) := thLoopT mt r i k index good prog
    prog := prog'
    if done then new := new.push i
  return (prog, new)

def runRefT (mt : Array (Array (Array Nat))) (cf : Conf) : Result := Id.run do
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
    let (prog', new) := iLoopT mt r ks index good prog
    prog := prog'
    if new.isEmpty then break
    good := setLoop new good
    reached := reached + new.size
    depth := depth + 1
  return { classes := N, ext := ext, reached := reached, depth := depth }

end Ref

theorem runT_eq_runRefT (mt : Array (Array (Array Nat))) (cf : Conf) : runT mt cf = Ref.runRefT mt cf := by
  rfl

end DCheck
