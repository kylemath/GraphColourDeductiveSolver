/-!
# Birkhoff diamond: D-reducibility closure computed in the kernel

A direct Lean transcription of `dred.py` (the vertex-colour form of RSST's consistent-matching
closure).  `closureOK` computes: the 31 canonical proper colourings of the 6-ring, the 16 that
extend to the diamond interior, and the iterated Kempe closure; it returns `true` iff every class
is reached.  `diamond_D_reducible_check` proves `closureOK = true` by `decide +kernel`, i.e. by
kernel evaluation only.

What this does NOT prove: that the closure is *sound* (that a colouring reached by the closure
really gives a 4-colouring of any triangulation containing the diamond).  That is the Kempe-chain /
Jordan-curve meta-theorem, which in this repo lives (in a different, per-step form) in
StudioMathLean `RingChains`/`RingReduce` + `DiamondCert`.  Here we only certify the finite search.
All recursion is structural (fuel), so the kernel can evaluate it.
-/
namespace BirkhoffDiamondC

def r : Nat := 6
def ringAdj : List (List Nat) := [[0, 1], [1, 2, 3], [3, 4], [0, 4, 5]]
def intAdj : List (List Nat) := [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]

/-- base-4 digits, length `n`. -/
def digits : Nat → Nat → List Nat
  | 0, _ => []
  | n + 1, x => x % 4 :: digits n (x / 4)

/-- canonical renaming: colours renumbered in order of first appearance. -/
def canonAux : List Nat → List Nat → List Nat
  | [], _ => []
  | x :: xs, seen =>
    match seen.idxOf? x with
    | some i => i :: canonAux xs seen
    | none => seen.length :: canonAux xs (seen ++ [x])
def canon (k : List Nat) : List Nat := canonAux k []

def ringProper (k : List Nat) : Bool :=
  (List.range r).all fun i => k.getD i 0 != k.getD ((i + 1) % r) 0

def ringColourings : List (List Nat) :=
  ((List.range (4 ^ r)).map (digits r)).filter fun k => ringProper k && canon k == k

def extends? (k : List Nat) : Bool :=
  (List.range 256).any fun n =>
    let c := digits 4 n
    (List.range 4).all fun a =>
      ((ringAdj.getD a []).all fun t => c.getD a 9 != k.getD t 8) &&
      ((intAdj.getD a []).all fun b => c.getD a 9 != c.getD b 7)

/-- non-crossing perfect matchings of a cyclically ordered list (fuel = length). -/
def ncm : Nat → List Nat → List (List (Nat × Nat))
  | _, [] => [[]]
  | 0, _ => []
  | f + 1, a :: rest =>
    (List.range rest.length).flatMap fun j =>
      if j % 2 == 0 then
        let inner := rest.take j
        let outer := rest.drop (j + 1)
        (ncm f inner).flatMap fun m1 => (ncm f outer).map fun m2 => (a, rest.getD j 0) :: m1 ++ m2
      else []

/-- relabel: every arc label equal to `y` becomes `x`. -/
def merge (lab : List Nat) (x y : Nat) : List Nat := lab.map fun l => if l == y then x else l

/-- region label of each ring vertex, given transitions `T` (sorted) and a matching. -/
def regionLabels (T : List Nat) (M : List (Nat × Nat)) : List Nat :=
  let n := T.length
  let idx := fun t => T.idxOf t
  -- arc j = vertices T[j]+1 .. T[j+1]; label arcs 0..n-1
  let lab0 := List.range n
  let lab := M.foldl (fun lab (st : Nat × Nat) =>
      let i := min (idx st.1) (idx st.2)
      let j := max (idx st.1) (idx st.2)
      let lab := merge lab (lab.getD ((i + n - 1) % n) 0) (lab.getD j 0)
      merge lab (lab.getD i 0) (lab.getD ((j + n - 1) % n) 0)) lab0
  -- arc of vertex v: number of transitions t with t < v, minus 1, cyclically
  (List.range r).map fun v =>
    let c := (T.filter fun t => t < v).length
    lab.getD ((c + n - 1) % n) 0

def stepOK (good : List (List Nat)) (k : List Nat) : Bool :=
  [1, 2, 3].any fun th =>
    let T := (List.range r).filter fun i =>
      let x := Nat.xor (k.getD i 0) (k.getD ((i + 1) % r) 0)
      x != 0 && x != th
    (ncm T.length T).all fun M =>
      if T.isEmpty then false else
      let lab := regionLabels T M
      (List.range (2 ^ T.length)).any fun mask =>
        mask != 0 &&
        let k2 := (List.range r).map fun v =>
          if (mask >>> lab.getD v 0) % 2 == 1 then Nat.xor (k.getD v 0) th else k.getD v 0
        good.contains (canon k2)

def closure : Nat → List (List Nat) → List (List Nat)
  | 0, good => good
  | f + 1, good =>
    let new := ringColourings.filter fun k => !good.contains k && stepOK good k
    if new.isEmpty then good else closure f (good ++ new)

def base : List (List Nat) := ringColourings.filter extends?

def closureOK : Bool :=
  ringColourings.length == 31 && base.length == 16 &&
  (closure 40 base).length == ringColourings.length

theorem diamond_ring_count : ringColourings.length = 31 := by decide +kernel
theorem diamond_base_count : base.length = 16 := by decide +kernel
theorem diamond_D_reducible_check : closureOK = true := by decide +kernel

end BirkhoffDiamondC

#print axioms BirkhoffDiamondC.diamond_D_reducible_check
