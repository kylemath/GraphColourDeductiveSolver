import Std.Data.HashMap
/-! DCheck16 (Studio Job 13, exploratory): an exact copy of DCheck.lean with ONE change, the matching table extended
from p <= 7 to p <= 8 (rings up to 16 have at most 16 transitions). Nothing else differs (diff against DCheck.lean). -/
/-!
# DCheck: an executable D-reducibility checker (Long Table, Run 2, exploratory)

Core Lean 4 (+ `Std` from the toolchain), no Mathlib. A Lean port of `../dred.py`, organised for
speed so that `native_decide` can run it on RSST configurations.

## Model (vertex-colour form of RSST's consistent-matching closure)
* Colours are `Z2 × Z2 = {0,1,2,3}` with XOR. A ring colouring of an `r`-ring is a code
  `k = Σ col_i · 4^i`; it is proper when `col_i ≠ col_{i+1 mod r}`. Colourings are taken up to
  renaming of colours (`canon`: colours renumbered in order of first appearance).
* `extendsQ c k`: the interior of `c` has a colouring compatible with `k` (backtracking).
* Kempe step. For `θ ∈ {1,2,3}` the colours split into the classes `{x, x⊕θ}`. A transition is a
  ring edge `(i, i+1)` with `col_i ⊕ col_{i+1} ∉ {0, θ}` (its two ends lie in different classes);
  there is an even number `2p` of them. Every non-crossing perfect matching of the transitions
  (the outside θ-edge-Kempe paths of the Tait colouring) cuts the ring into `p+1` regions (the
  ring traces of the outside vertex-Kempe chains). `k` joins level `i+1` if for some `θ`, for
  EVERY matching, some non-empty set of regions not containing region 0 can be XOR-ed with `θ` to
  give a level-`i` colouring. Level 0 = extendable colourings.
* `dReducible c` iff every proper ring colouring class is reached.

## Implementation notes
* Monotone progress pointers: for each (class, θ) the checker keeps the index of the first
  matching not yet satisfied. Since the good set only grows, a satisfied matching stays satisfied
  (closure monotonicity), so each (class, θ, matching) is decided "satisfied" at most once.
* The closure is level-synchronous (the same levels as `dred.py`), so `depth` agrees.
-/
namespace DCheck16

structure Conf where
  name : String
  r : Nat
  m : Nat
  /-- ring neighbours (positions `0..r-1`) of each interior vertex -/
  ringAdj : Array (Array Nat)
  /-- interior neighbours (`0..m-1`) of each interior vertex -/
  intAdj : Array (Array Nat)
  rsstExt : Nat := 0
  rsstContract : Nat := 0
deriving Inhabited, Repr

@[inline] def col (k i : Nat) : Nat := (k >>> (2 * i)) % 4

/-- Rename colours in order of first appearance. -/
def canon (r k : Nat) : Nat := Id.run do
  let mut mp : Array Nat := #[4, 4, 4, 4]
  let mut nxt := 0
  let mut out := 0
  for i in [0:r] do
    let c := col k i
    let d := mp[c]!
    if d == 4 then
      mp := mp.set! c nxt
      out := out ||| (nxt <<< (2 * i))
      nxt := nxt + 1
    else
      out := out ||| (d <<< (2 * i))
  return out

/-- All canonical proper colourings of the `r`-ring (`r ≥ 2`). -/
def ringColourings (r : Nat) : Array Nat := Id.run do
  -- partial colourings of positions 0..i-1 as (code, number of colours used)
  let mut cur : Array (Nat × Nat) := #[(0, 1)]
  for i in [1:r] do
    let mut nxt : Array (Nat × Nat) := #[]
    for (k, used) in cur do
      for c in [0:(min 4 (used + 1))] do
        if c != col k (i - 1) && (i + 1 != r || c != col k 0) then
          nxt := nxt.push (k ||| (c <<< (2 * i)), if c == used then used + 1 else used)
    cur := nxt
  return cur.map (·.1)

/-- Backtracking: interior vertices `a = cols.size, …` get colours avoiding ring colours of `k`
and the colours of earlier interior neighbours. Fuel = number of vertices still to colour. -/
def extAux (cf : Conf) (k : Nat) : Nat → Array Nat → Bool
  | 0, _ => true
  | f + 1, cols =>
    let a := cols.size
    let ra := cf.ringAdj[a]!
    let ia := cf.intAdj[a]!
    [0, 1, 2, 3].any fun x =>
      ra.all (fun t => col k t != x) && ia.all (fun b => b ≥ a || cols[b]! != x) &&
      extAux cf k f (cols.push x)

def extendsQ (cf : Conf) (k : Nat) : Bool := extAux cf k cf.m #[]

/-- Non-crossing perfect matchings of the points `pts` (in cyclic order); fuel = length. -/
def ncm : Nat → List Nat → List (List (Nat × Nat))
  | _, [] => [[]]
  | 0, _ => []
  | f + 1, a :: rest =>
    (List.range rest.length).flatMap fun j =>
      if j % 2 == 0 then
        (ncm f (rest.take j)).flatMap fun m1 =>
          (ncm f (rest.drop (j + 1))).map fun m2 => (a, rest[j]!) :: m1 ++ m2
      else []

/-- Region label (`0..p`, region of arc 0 is 0) of each of the `n = 2p` arcs, for a matching of
transition indices `0..n-1`. Arc `j` lies between transitions `j` and `j+1`. A chord `(i,j)`,
`i<j`, puts arcs `i-1, j` in one face and arcs `i, j-1` in one face. -/
def arcRegions (n : Nat) (M : List (Nat × Nat)) : Array Nat := Id.run do
  let mut lab : Array Nat := Array.range n
  for (s, t) in M do
    let i := min s t
    let j := max s t
    for (x, y) in [((i + n - 1) % n, j), (i, (j + n - 1) % n)] do
      let lx := lab[x]!
      let ly := lab[y]!
      lab := lab.map fun l => if l == ly then lx else l
  -- renumber in order of first appearance
  let mut mp : Array Nat := Array.replicate n n
  let mut nxt := 0
  let mut out : Array Nat := #[]
  for j in [0:n] do
    let l := lab[j]!
    if mp[l]! == n then
      mp := mp.set! l nxt
      nxt := nxt + 1
    out := out.push mp[l]!
  return out

/-- `matchTable[p]` = region labelling of the arcs for every non-crossing perfect matching of
`2p` points, `p ≤ 7` (rings up to 14 have at most 14 transitions). -/
def matchTable : Array (Array (Array Nat)) :=
  (Array.range 9).map fun p =>
    ((ncm (2 * p) (List.range (2 * p))).map (arcRegions (2 * p))).toArray

structure Result where
  classes : Nat
  ext : Nat
  reached : Nat
  depth : Nat
deriving Repr, DecidableEq

/-- The D-reducibility closure. -/
def run (cf : Conf) : Result := Id.run do
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
  return { classes := N, ext := ext, reached := reached, depth := depth }

/-- **The checker.** -/
def dReducible (cf : Conf) : Bool :=
  let res := run cf
  res.reached == res.classes

end DCheck16
