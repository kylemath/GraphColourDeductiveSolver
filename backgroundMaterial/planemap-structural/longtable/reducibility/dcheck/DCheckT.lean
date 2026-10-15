import DCheck
/-!
# DCheckT: the checker with its matching table as a parameter (Job 23, exploratory)

`runT mt` is the body of `DCheck.run` (copied verbatim) with `matchTable` replaced by the argument `mt`.
`matchTableN N` is `matchTable` with `Array.range N`: `DCheck`, `DCheck16`, `DCheck18` use N = 8, 9, 10.
-/
namespace DCheck

/-- The matching table for `p < N` (`p` = half the number of transitions). -/
def matchTableN (N : Nat) : Array (Array (Array Nat)) :=
  (Array.range N).map fun p =>
    ((ncm (2 * p) (List.range (2 * p))).map (arcRegions (2 * p))).toArray

theorem matchTable_eq : matchTable = matchTableN 8 := rfl

/-- The D-reducibility closure with matching table `mt`. -/
def runT (mt : Array (Array (Array Nat))) (cf : Conf) : Result := Id.run do
  let r := cf.r
  let ks := ringColourings r
  let N := ks.size
  let mut index : Std.HashMap Nat Nat := {}
  for i in [0:N] do
    index := index.insert ks[i]! i
  let mut good : Array Bool := ks.map (extendsQ cf)
  let ext := (good.filter id).size
  let mut reached := ext
  -- progress[3*i + (θ-1)] = first unsatisfied matching; `dead` if θ has no transitions
  let dead := 1000000
  let mut prog : Array Nat := Array.replicate (3 * N) 0
  let mut depth := 0
  for _ in [0:N + 1] do
    let mut new : Array Nat := #[]
    for i in [0:N] do
      if good[i]! then continue
      let k := ks[i]!
      let mut done := false
      for th in [1:4] do
        if done then break
        let pi := prog[3 * i + th - 1]!
        if pi == dead then continue
        -- transitions
        let mut T : Array Nat := #[]
        for v in [0:r] do
          let x := col k v ^^^ col k ((v + 1) % r)
          if x != 0 && x != th then T := T.push v
        let n := T.size
        if n == 0 then
          prog := prog.set! (3 * i + th - 1) dead
          continue
        -- arc of each ring vertex
        let arcOf : Array Nat := (Array.range r).map fun v =>
          ((T.filter (· < v)).size + n - 1) % n
        let mats := mt[n / 2]!
        let mut ptr := pi
        let mut stuck := false
        while ptr < mats.size && !stuck do
          let lab := mats[ptr]!
          -- XOR mask of each region
          let mut rm : Array Nat := Array.replicate (n / 2 + 1) 0
          for v in [0:r] do
            let g := lab[arcOf[v]!]!
            rm := rm.set! g (rm[g]! ||| (th <<< (2 * v)))
          let mut sat := false
          for s in [1:(1 <<< (n / 2))] do
            let mut k2 := k
            for b in [0:n / 2] do
              if (s >>> b) % 2 == 1 then k2 := k2 ^^^ rm[b + 1]!
            match index[canon r k2]? with
            | some j =>
              if good[j]! then
                sat := true
                break
            | none => pure ()
          if sat then ptr := ptr + 1 else stuck := true
        prog := prog.set! (3 * i + th - 1) ptr
        if ptr == mats.size then done := true
      if done then new := new.push i
    if new.isEmpty then break
    for i in new do good := good.set! i true
    reached := reached + new.size
    depth := depth + 1
  return { classes := N, ext := ext, reached := reached, depth := depth }

/-- The parametrised checker. -/
def dReducibleT (mt : Array (Array (Array Nat))) (cf : Conf) : Bool :=
  let res := runT mt cf
  res.reached == res.classes

theorem run_eq_runT (cf : Conf) : run cf = runT matchTable cf := rfl

theorem dReducible_eq_T (cf : Conf) : dReducible cf = dReducibleT (matchTableN 8) cf := rfl

end DCheck
