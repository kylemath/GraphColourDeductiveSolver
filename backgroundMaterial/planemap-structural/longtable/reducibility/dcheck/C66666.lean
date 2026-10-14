import DCheck
/-! Studio Job 16 (exploratory): the D-closure reached set of the 66666 wheel, and the C-reduction candidate
X = {R0-I1, I2-I3, I3-I4, I4-I5} (Long Table discharge/c66666/).
`runGood` is the body of `DCheck.run` copied verbatim, returning the ring colourings and the final `good` array
instead of the counts; `runGood_agrees` ties it back to `run`.  Theorems by native_decide (one auxiliary axiom each). -/
namespace DCheck

/-- The body of `run`, verbatim, returning (ring colourings, good). -/
def runGood (cf : Conf) : Array Nat × Array Bool := Id.run do
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
        let mats := matchTable[n / 2]!
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
  return (ks, good)

/-- The 66666 wheel (hole 0, neighbours 1..5 of degree 6), as in wheels.py / configs_wheels.txt. -/
def w66666 : Conf := { name := "66666", r := 10, m := 6, ringAdj := #[#[], #[9, 0, 1], #[1, 2, 3], #[3, 4, 5], #[5, 6, 7], #[7, 8, 9]], intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 5], #[0, 3, 1], #[0, 4, 2], #[0, 5, 3], #[0, 1, 4]] }

/-- number of colours used by ring colouring k -/
def numCol (r k : Nat) : Nat := ((List.range r).map (col k)).eraseDups.length

/-- Extension after contraction: interior vertex a gets colour x; a contracted ring-interior edge (t, a) forces
x = col k t, other ring edges force x != col k t; a contracted interior edge (a, b), b < a, forces x = colour of b,
other interior edges force difference. -/
def extCAux (cf : Conf) (eqR : List (Nat × Nat)) (eqI : List (Nat × Nat)) (k : Nat) : Nat → Array Nat → Bool
  | 0, _ => true
  | f + 1, cols =>
    let a := cols.size
    [0, 1, 2, 3].any fun x =>
      (cf.ringAdj[a]!).all (fun t => if eqR.contains (t, a) then col k t == x else col k t != x) &&
      (cf.intAdj[a]!).all (fun b => b >= a || (if eqI.contains (b, a) || eqI.contains (a, b) then cols[b]! == x else cols[b]! != x)) &&
      extCAux cf eqR eqI k f (cols.push x)

/-- X = {R0-I1, I2-I3, I3-I4, I4-I5} -/
def extX (k : Nat) : Bool := extCAux w66666 [(0, 1)] [(2, 3), (3, 4), (4, 5)] k w66666.m #[]

theorem w66666_run : run w66666 = { classes := 2461, ext := 530, reached := 1241, depth := 15 } := by native_decide

theorem runGood_agrees : ((runGood w66666).2.filter id).size = 1241 ∧ (runGood w66666).1.size = 2461 := by native_decide

/-- (a) every ring colouring of the 10-ring that uses at most 3 colours is in the D-closure of the 66666 wheel. -/
theorem three_colour_reached :
    (let p := runGood w66666; (List.range p.1.size).all fun i => !(decide (numCol 10 p.1[i]! ≤ 3)) || p.2[i]!) = true := by
  native_decide

/-- the ring colourings that extend after contracting X are exactly those with at most 3 colours (171 classes) -/
theorem extX_iff_three :
    (let p := runGood w66666; (List.range p.1.size).all fun i => extX p.1[i]! == decide (numCol 10 p.1[i]! ≤ 3)) = true ∧
    ((runGood w66666).1.filter fun k => extX k).size = 171 := by
  native_decide

/-- the computational half of C-reducibility: every ring colouring extending after contraction is reached -/
theorem extX_reached :
    (let p := runGood w66666; (List.range p.1.size).all fun i => !(extX p.1[i]!) || p.2[i]!) = true := by
  native_decide

end DCheck

#print axioms DCheck.w66666_run
#print axioms DCheck.runGood_agrees
#print axioms DCheck.three_colour_reached
#print axioms DCheck.extX_iff_three
#print axioms DCheck.extX_reached
