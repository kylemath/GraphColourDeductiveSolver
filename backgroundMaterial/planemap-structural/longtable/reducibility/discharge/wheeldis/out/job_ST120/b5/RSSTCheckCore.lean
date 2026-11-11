import RSSTKill

/-!
# ST-120 B5 M2: the certificate checker (computational part, core Lean only)

Studio, 10 Nov. Route (c) of `SEED_PLAN.md` §B5: a checker that replays an exported certificate. Its soundness is
`RSSTCheckSound.lean`. The checker does no search for kills: every kill it uses is a configuration index plus an
embedding from the certificate, verified by `checkEmb`'s symbolic form `reqOf`.

## Grouping (spec §8.1/§8.3, made symbolic)

For a degree `d` the checker runs over **every** link word `link ∈ {5..9}^d` (`allWords d`, no symmetry reduction).
For one link word it builds the *tagged word* `tagW d link`: the apex `s_j` carries the code `100 + j` and the private
`p_i.(k+1)` the code `200 + 3i + k` in place of a letter. B2's own window functions (`UWin.letter`, the hub views) run
on the tagged word; a test that reads a code becomes a *condition* `code ∈ range`, a test on a link letter or on `u` is
decided, and a ring-3 test is OPEN. So each (part, hub, anchor) attempt that moves `u`'s charge becomes an `SRes`: `no`,
or a conjunction of conditions plus an OPEN flag (spec §3.4's "alternative"). These are the spec's `instances`; the
relevant privates/apexes are their condition codes.

## The search the certificate replays

A DFS over the variables in the certificate's order. A node fixes a *class* of letters for each variable so far (the
classes of a variable: the letters whose truth pattern on its conditions equals 9's, together with 9 — spec §13 A.3.2
dominance — and every other letter alone). At a node:
* the instances are simplified by the classes fixed so far (a condition that holds on the whole class is dropped, one
  that fails on the whole class kills the instance);
* `ub = 10(6-d) + #(into-u instances left) - #(out-of-u instances left with no condition and not OPEN)`; `ub ≤ 0` closes
  the node (this is the spec's hi⁺ / DFS bound);
* a kill requirement (from a certificate embedding: the letters it needs on codes) that the fixed singleton classes
  meet closes the node (monotone kills, spec §7);
* otherwise the node branches on the next variable's classes (they must cover 5..9: checked); with no variable left
  the check fails.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-! ## Tagged words -/

def apexCode (j : Nat) : Nat := 100 + j
def privCode (i k : Nat) : Nat := 200 + 3 * i + k
def isCode (x : Nat) : Bool := Nat.ble 100 x

/-- The tagged word of a link word: codes in place of the apex and private letters. -/
def tagW (d : Nat) (link : List Nat) : UWin where
  d := d
  link := link
  apex := (List.range d).map apexCode
  priv := (List.range d).map fun i => (List.range (npriv (link.getD i 9))).map (privCode i)

/-- The valuation of the codes read off a real word (letters `< 100` are fixed). -/
def sigmaW (W : UWin) (c : Nat) : Nat :=
  if c < 100 then c
  else if c < 200 then W.apex.getD (c - 100) 9
  else (W.priv.getD ((c - 200) / 3) []).getD ((c - 200) % 3) 9

/-! ## Symbolic fit results -/

/-- `no`, or a conjunction of conditions `code ∈ range` with an OPEN flag. -/
inductive SRes
  | no
  | c (cs : List (Nat × Rng)) (op : Bool)
deriving DecidableEq, Repr

namespace SRes

def sure : SRes := .c [] false
def opn : SRes := .c [] true
def ofBool (b : Bool) : SRes := if b then sure else no

def and : SRes → SRes → SRes
  | .no, _ => .no
  | .c _ _, .no => .no
  | .c a o, .c b p => .c (a ++ b) (o || p)

/-- Value under a valuation of the codes. -/
def eval (σ : Nat → Nat) : SRes → Tri
  | .no => .no
  | .c cs o => if cs.all (fun vr => vr.2.test (σ vr.1)) then (if o then .open_ else .sure) else .no

end SRes

def symTest (r : Rng) (o : Option Nat) : SRes :=
  if r.isFull then .sure else
  match o with
  | none => .opn
  | some x => if isCode x then .c [(x, r)] false else .ofBool (r.test x)

/-- A spoke of a tagged view: spoke letter (maybe a code), hat, the fan list for a given fan count, the fan count as a
function of the spoke letter. -/
structure TSpoke where
  sp : Nat
  hat : Option Nat
  fansOf : Nat → List (Option Nat)
  fc : Nat → Nat

/-- B2's `Sub.fit3`, symbolically. On a code spoke with a constrained fan the spoke range is an exact letter `L`
(`Part.wellShaped`), so the fan list is read for `L`. -/
def symSub (s : Sub) (x : TSpoke) : SRes :=
  let spokeP : SRes :=
    if s.spoke.isFull then .sure else if isCode x.sp then .c [(x.sp, s.spoke)] false else .ofBool (s.spoke.test x.sp)
  let fanP : SRes :=
    if s.fans.all Rng.isFull then .sure
    else
      let fl := x.fansOf (x.fc (if isCode x.sp then s.spoke.lo else x.sp))
      if s.fans.length != fl.length then .no
      else (s.fans.zip fl).foldl (fun acc rx => acc.and (symTest rx.1 rx.2)) .sure
  spokeP.and ((symTest s.hat x.hat).and fanP)

/-- B2's `Part.fit3At`, symbolically. -/
def symFit (p : Part) (tv : List TSpoke) (a : Nat) : SRes :=
  if tv.length != p.subs.length then .no else
  (List.range p.subs.length).foldl (fun acc j =>
    acc.and <| match p.subs[j]?, tv[(a + j) % tv.length]? with
      | some s, some x => symSub s x
      | _, _ => .no) .sure

/-- B2's `UWin.viewW`, tagged. -/
def tviewW (X : UWin) (i : Nat) : List TSpoke :=
  let n := X.linkL i
  (List.range n).map fun t =>
    { sp := (X.letter i (wSpokePos n t)).getD 0, hat := X.letter i (wHatPos n t),
      fansOf := fun m => (List.range m).map fun k => X.letter i (wFanPos n t k),
      fc := X.fanCount (wSpokePos n t) }

/-- B2's `UWin.viewU`, tagged. -/
def tviewU (X : UWin) : List TSpoke :=
  (List.range X.d).map fun t =>
    { sp := (X.letter 0 (uSpokePos t)).getD 0, hat := X.letter 0 (uHatPos t),
      fansOf := fun m => (List.range m).map fun k => X.letter 0 (uFanPos t k),
      fc := npriv }

/-- Every attempt into `u` (hub `w_i` with letter `≤ 8`, anchor `n-2`), as in B2's `UWin.fired`. -/
def instIn (parts : List Part) (X : UWin) : List SRes :=
  (List.range X.d).flatMap fun i =>
    if X.linkL i ≤ 8 then
      parts.flatMap fun p => if p.hub = X.linkL i then [symFit p (tviewW X i) (X.linkL i - 2)] else []
    else []

/-- Every attempt out of `u` (hub `u`, `d ∈ 5..8`, every anchor). -/
def instOut (parts : List Part) (X : UWin) : List SRes :=
  if 5 ≤ X.d ∧ X.d ≤ 8 then
    parts.flatMap fun p => if p.hub = X.d then (List.range X.d).map fun a => symFit p (tviewU X) a else []
  else []

/-! ## Kill requirements from an embedding -/

inductive HS
  | fixed (x : Nat)
  | var (c : Nat)
  | none

/-- The host status of a window vertex in the tagged word: a fixed letter (`u`, an exact `w`), a code (apex, private),
or not a host. -/
def hostSym (d : Nat) (link : List Nat) (v : Nat) : HS :=
  match vkind d v with
  | .u => .fixed d
  | .w i => match le8 (link.getD i 9) with
    | some x => .fixed x
    | none => .none
  | .s i => .var (apexCode i)
  | .p i k => if privOk (link.getD i 9) k then .var (privCode i k) else .none
  | .bad => .none

def reqStep (K : Conf) (d : Nat) (link : List Nat) (e : List Nat) (x : Nat) :
    Option (List (Nat × Nat)) → Option (List (Nat × Nat))
  | none => none
  | some R => match hostSym d link (e.getD x 0) with
    | .fixed y => if y == K.degOf x then some R else none
    | .var c => if K.degOf x ≤ 8 then some ((c, K.degOf x) :: R) else none
    | .none => none

/-- The letters an embedding needs on codes (`none` if it can never be valid for this link word). -/
def reqOf (K : Conf) (d : Nat) (link : List Nat) (e : List Nat) : Option (List (Nat × Nat)) :=
  if embShape K d link e then (List.range K.size).foldr (reqStep K d link e) (some []) else none

/-! ## The DFS -/

/-- Simplify one instance by "code `v` has a letter in `S`". -/
def simp1 (v : Nat) (S : List Nat) : SRes → Option SRes
  | .no => none
  | .c cs o =>
    if cs.any (fun cr => cr.1 == v && S.all (fun l => !cr.2.test l)) then none
    else some (.c (cs.filter (fun cr => !(cr.1 == v && S.all (fun l => cr.2.test l)))) o)

/-- Simplify a kill requirement. -/
def simpR1 (v : Nat) (S : List Nat) (R : List (Nat × Nat)) : Option (List (Nat × Nat)) :=
  if R.any (fun cl => cl.1 == v && S != [cl.2]) then none else some (R.filter (fun cl => cl.1 != v))

def certain : SRes → Bool
  | .c [] false => true
  | _ => false

def coverOK (cls : List (List Nat)) : Bool := [5, 6, 7, 8, 9].all fun l => cls.any fun S => S.contains l

/-- The DFS. `vs`: variables with their classes; `ins`/`outs`: the live instances into / out of `u`; `reqs`: the live
kill requirements. -/
def dfs (base : Int) : List (Nat × List (List Nat)) → List SRes → List SRes → List (List (Nat × Nat)) → Bool
  | vs, ins, outs, reqs =>
    if base + (ins.length : Int) - ((outs.filter certain).length : Int) ≤ 0 then true
    else if reqs.any List.isEmpty then true
    else match vs with
      | [] => false
      | (v, cls) :: rest =>
        coverOK cls && cls.all fun S =>
          dfs base rest (ins.filterMap (simp1 v S)) (outs.filterMap (simp1 v S)) (reqs.filterMap (simpR1 v S))

/-- The ranges tested on code `v`. -/
def testsOf (v : Nat) (l : List SRes) : List Rng :=
  l.flatMap fun x => match x with
    | .c cs _ => cs.filterMap fun cr => if cr.1 == v then some cr.2 else none
    | .no => []

/-- Classes of a variable: 9 with every letter of the same truth pattern, and every other letter alone. -/
def classesOf (v : Nat) (l : List SRes) : List (List Nat) :=
  let ts := testsOf v l
  let pat := fun (x : Nat) => ts.map fun r => r.test x
  ([5, 6, 7, 8, 9].filter fun x => pat x == pat 9) :: (([5, 6, 7, 8].filter fun x => pat x != pat 9).map fun x => [x])

/-! ## Certificates -/

/-- Per link word: the variable order and the embeddings `(index into the kill list, images)`. -/
structure LinkCert where
  order : List Nat
  embs : List (Nat × List Nat)
deriving Repr, Inhabited

def LinkCert.empty : LinkCert := ⟨[], []⟩

/-- What the symbolic evaluator needs of a part (spec §3.2: a constrained fan sits on an exact spoke). -/
def Part.fanExact (p : Part) : Bool := p.subs.all fun s => s.fans.all Rng.isFull || s.spoke.lo == s.spoke.hi

/-- One link word, for a part list `parts` and a kill list `KL`. -/
def checkLinkP (parts : List Part) (KL : List Conf) (d : Nat) (link : List Nat) (c : LinkCert) : Bool :=
  let X := tagW d link
  let ins := (instIn parts X).filter (· != .no)
  let outs := (instOut parts X).filter (· != .no)
  let reqs := c.embs.filterMap fun ke => match KL[ke.1]? with
    | some K => reqOf K d link ke.2
    | none => none
  c.order.all isCode && dfs (10 * (6 - (d : Int))) (c.order.map fun v => (v, classesOf v (ins ++ outs))) ins outs reqs

/-- All words of length `n` over `5..9` (first letter slowest, as Python's `itertools.product`). -/
def allWords : Nat → List (List Nat)
  | 0 => [[]]
  | n + 1 => [5, 6, 7, 8, 9].flatMap fun a => (allWords n).map (a :: ·)

def checkLinksP (parts : List Part) (KL : List Conf) (d : Nat) : List (List Nat) → List LinkCert → Bool
  | [], _ => true
  | l :: ls, [] => checkLinkP parts KL d l .empty && checkLinksP parts KL d ls []
  | l :: ls, c :: cs => checkLinkP parts KL d l c && checkLinksP parts KL d ls cs

/-- **The per-degree check**: every link word of length `d`, with the certificate entries in `allWords d` order. -/
def checkDegP (parts : List Part) (KL : List Conf) (d : Nat) (cert : List LinkCert) : Bool :=
  parts.all Part.fanExact && Nat.ble 5 d && Nat.ble d 30 && checkLinksP parts KL d (allWords d) cert

/-- The check for the 71 RSST parts (B2's `rsstParts`, the part list of `UWin.loHi`). -/
def checkDeg (KL : List Conf) (d : Nat) (cert : List LinkCert) : Bool := checkDegP rsstParts KL d cert

/-! ## Certificate text format

One line per link word in `allWords d` order: `ORDER|EMBS`, `ORDER` = comma-separated codes, `EMBS` = `;`-separated
`k:v,v,…` (configuration index into the kill list, images of its interior vertices `0..m-1`). An empty line (or a line
`|`) is the empty certificate. Lines starting with `#` are skipped. The checker's soundness does not depend on the
parser. -/

def parseNats (s : String) : List Nat :=
  if s.isEmpty then [] else (s.splitOn ",").map String.toNat!

def parseEmb (s : String) : Option (Nat × List Nat) :=
  match s.splitOn ":" with
  | [k, e] => some (k.toNat!, parseNats e)
  | _ => none

def parseLine (s : String) : LinkCert :=
  match s.splitOn "|" with
  | [o, e] => ⟨parseNats o, if e.isEmpty then [] else (e.splitOn ";").filterMap parseEmb⟩
  | _ => .empty

def parseCert (s : String) : List LinkCert :=
  ((s.splitOn "\n").filter fun l => !l.startsWith "#").map parseLine

end SimpleGraph.SphericalMap.RSSTSeed
