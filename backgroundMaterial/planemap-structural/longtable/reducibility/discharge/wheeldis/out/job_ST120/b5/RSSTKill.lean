import RSSTView

/-!
# ST-120 B5 M1: containment of an RSST configuration in a window word (spec §7, errata §14)

Studio, 10 Nov. Core Lean only (imports B2's `RSSTView`). Spec: `out/job_RSST1SHOT/in_spec_v2_a7915274.md` §7 with the
W6r errata: **u is a host at every degree** (letter = its exact degree `d`).

## Window vertices (codes relative to `d`)

| code | vertex |
|---|---|
| `0` | `u` |
| `1 + i` (`i < d`) | `w_i` |
| `1 + d + i` (`i < d`) | `s_i` |
| `1 + 2d + 3i + k` (`i < d`, `k < 3`) | the private `p_i.(k+1)` (it exists iff `k < npriv L_i`) |

## Hosts (spec §7)

`u` (letter `d`, always), and every `w_i`, `s_i`, private whose letter is exact (`≤ 8`). Never a host: a 9+ vertex, ring
3, and the drawn middle `p_i.2` of a 9+ link vertex (whatever letter the word stores there; B4's `RealShape` does not pin
it, `wordOf` writes 9).

## Window edges (spec §2 faces; the host graph is the induced subgraph on the hosts)

`u–w_i`; `w_i–w_{i+1}`; `w_i–x` for every `x` in `seg_i = [s_{i-1}, p_i.1, …, p_i.k, s_i]`; consecutive entries of
`seg_i` (so `s_{i-1}–s_i` when `L_i = 5`). This is RSST-1SHOT's `window_hostgraph` (rcore.py 3d133146) with the middle
of a 9+ seg kept as a non-host.

## Containment

`checkEmb K W e`: `e` lists the images of `K`'s interior vertices `0..m-1`; it is injective, every image is a host whose
letter equals the vertex degree, and adjacency is preserved both ways (induced). The spec's face condition (every
interior face onto a triangle) is implied: an interior face is a triangle of interior edges, and their images are
adjacent. `Kills KL W := ∃ K ∈ KL, ∃ e, checkEmb K W e`. The kill list is a parameter.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-- An RSST configuration's interior: `deg x` (degree in the configuration's triangulation, ring included) and the
interior adjacency lists (0-based interior indices). -/
structure Conf where
  name : String
  deg : List Nat
  adj : List (List Nat)
deriving Repr

def Conf.size (K : Conf) : Nat := K.deg.length
def Conf.degOf (K : Conf) (x : Nat) : Nat := K.deg.getD x 0
def Conf.adjB (K : Conf) (x y : Nat) : Bool := (K.adj.getD x []).contains y

/-! ## Window vertices -/

inductive VK
  | u
  | w (i : Nat)
  | s (i : Nat)
  | p (i k : Nat)
  | bad
deriving DecidableEq, Repr

/-- Decode a vertex code (table above). -/
def vkind (d v : Nat) : VK :=
  if v = 0 then .u
  else if v ≤ d then .w (v - 1)
  else if v ≤ 2 * d then .s (v - d - 1)
  else if v - 2 * d - 1 < 3 * d then .p ((v - 2 * d - 1) / 3) ((v - 2 * d - 1) % 3)
  else .bad

def le8 (x : Nat) : Option Nat := if x ≤ 8 then some x else none

/-- The private `p_i.(k+1)` exists as a host candidate: `k < npriv L_i`, and it is not the middle of a 9+ link vertex. -/
def privOk (L k : Nat) : Bool := decide (k < npriv L) && !(decide (9 ≤ L) && k == 1)

/-- Host letter of a window vertex (`none` = not a host). -/
def hostLetter (W : UWin) (v : Nat) : Option Nat :=
  match vkind W.d v with
  | .u => some W.d
  | .w i => le8 (W.linkL i)
  | .s i => le8 (W.apexL i)
  | .p i k => if privOk (W.linkL i) k then le8 ((W.priv.getD i []).getD k 9) else none
  | .bad => none

/-- One direction of a window edge; `np i` = number of privates of `w_i` (letter-only data: `d` and the link word). -/
def edgeDir (d : Nat) (link : List Nat) : VK → VK → Bool
  | .u, .w _ => true
  | .w i, .w j => j == (i + 1) % d
  | .w i, .s j => j == i || j == (i + d - 1) % d
  | .w i, .p j k => j == i && decide (k < npriv (link.getD i 9))
  | .s j, .p i k =>
    let np := npriv (link.getD i 9)
    decide (k < np) && ((k == 0 && j == (i + d - 1) % d) || (k + 1 == np && j == i))
  | .p i k, .p j l => i == j && l == k + 1 && decide (l < npriv (link.getD i 9))
  | .s j, .s l => npriv (link.getD l 9) == 0 && j == (l + d - 1) % d
  | _, _ => false

/-- Window adjacency between two vertex codes (symmetric). -/
def isEdge (d : Nat) (link : List Nat) (a b : Nat) : Bool :=
  edgeDir d link (vkind d a) (vkind d b) || edgeDir d link (vkind d b) (vkind d a)

def nodupB : List Nat → Bool
  | [] => true
  | a :: l => !l.contains a && nodupB l

/-- The letter-independent part of an embedding check: length, injectivity, induced adjacency. -/
def embShape (K : Conf) (d : Nat) (link : List Nat) (e : List Nat) : Bool :=
  e.length == K.size && nodupB e &&
  (List.range K.size).all fun x => (List.range K.size).all fun y =>
    x == y || K.adjB x y == isEdge d link (e.getD x 0) (e.getD y 0)

/-- **Witness check**: `e` embeds `K`'s interior into the hosts of `W` (degrees = host letters, injective, induced). -/
def checkEmb (K : Conf) (W : UWin) (e : List Nat) : Bool :=
  embShape K W.d W.link e && (List.range K.size).all fun x => hostLetter W (e.getD x 0) == some (K.degOf x)

/-- **Kill predicate** (parametric in the kill list): some configuration of `KL` embeds into the window. -/
def Kills (KL : List Conf) (W : UWin) : Prop := ∃ K ∈ KL, ∃ e, checkEmb K W e = true

/-! ## A search (for cross-checks; only its witnesses are trusted) -/

/-- Number of vertex codes. -/
def nCodes (d : Nat) : Nat := 1 + 5 * d

/-- Interior vertices in a search order: BFS from vertex 0 (unreached vertices appended). -/
def Conf.order (K : Conf) : List Nat := Id.run do
  let mut ord : Array Nat := #[0]
  let mut seen : Array Bool := (Array.replicate K.size false).set! 0 true
  let mut qi := 0
  for _ in [0:K.size] do
    if qi < ord.size then
      let x := ord[qi]!
      qi := qi + 1
      for y in K.adj.getD x [] do
        if !seen[y]! then
          ord := ord.push y
          seen := seen.set! y true
  for y in [0:K.size] do
    if !seen[y]! then
      ord := ord.push y
      seen := seen.set! y true
  return ord.toList

/-- Backtracking search for an embedding (images indexed by interior vertex). -/
partial def findEmbAux (K : Conf) (W : UWin) (ord : List Nat) (img : Array Nat) (placed : List Nat) :
    Option (Array Nat) :=
  match ord with
  | [] => some img
  | x :: rest =>
    let cands := (List.range (nCodes W.d)).filter fun v =>
      hostLetter W v == some (K.degOf x) && !(placed.any fun y => img[y]! == v) &&
      placed.all fun y => K.adjB x y == isEdge W.d W.link v img[y]!
    cands.firstM fun v => findEmbAux K W rest (img.set! x v) (x :: placed)
where
  firstM {α : Type} (l : List Nat) (f : Nat → Option α) : Option α :=
    match l with
    | [] => none
    | v :: vs => match f v with
      | some r => some r
      | none => firstM vs f

def findEmb (K : Conf) (W : UWin) : Option (List Nat) :=
  if K.size = 0 then none else
  (findEmbAux K W K.order (Array.replicate K.size 0) []).map (·.toList)

/-- `containsK`: search, then the witness check (so `containsK = true` is backed by `checkEmb`). -/
def containsK (K : Conf) (W : UWin) : Bool :=
  match findEmb K W with
  | some e => checkEmb K W e
  | none => false

theorem containsK_sound {K : Conf} {W : UWin} (h : containsK K W = true) : ∃ e, checkEmb K W e = true := by
  unfold containsK at h
  split at h
  · exact ⟨_, h⟩
  · cases h

theorem kills_of_contains {KL : List Conf} {K : Conf} (hK : K ∈ KL) {W : UWin} (h : containsK K W = true) :
    Kills KL W :=
  ⟨K, hK, containsK_sound h⟩

end SimpleGraph.SphericalMap.RSSTSeed
