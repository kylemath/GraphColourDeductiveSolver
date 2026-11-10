import RSSTRules

/-!
# ST-120 B2: the local view a fit reads, fit semantics, and the locality lemma

Spec: `out/job_RSST1SHOT/in_spec_v2_a7915274.md` §2 (window), §3.3-3.5 (fits), §4 (charge), §6 (9+).

## Two levels

1. **Hub view** (`HubView`, B4-facing). For a hub `h` with rotation `S = S[0..n-1]`, spoke `x = S[t]` contributes a
   `SpokeView`: the letter of `x`, the letter of its *hat* `opp(x, S[t-1])` (the vertex after `S[t-1]` in `rot x`, read
   from `h`), and the letters of its *fans*: the vertices of `rot x` strictly between the hat and `opp(S[t+1], x)` (spec
   §3.3: in `rot x` the order is `h, S[t-1], hat, fans…, hat of S[t+1], S[t+1]`). `Part.fitsAt p v a : Bool` is the
   spec's fit at anchor `a`; it moves `p.amount` units from `h` to `S[(a + p.target) % n]`. All letters are known here,
   which is the situation in a real triangulation (letter = `min deg 9`).

2. **u-window** (`UWin`, the spec's 2-ball of `u`, used for the cross-check). The positions every test reads are
   explicit data (`WPos`, the `*Pos` functions below), relative to the hub. Ring-3 positions have no letter, so a test
   there is three-valued (`Tri`: fail / OPEN / true, spec §3.4). `UWin.fired` lists the fits that move `u`'s charge
   (spec §3.5) and `UWin.loHi` the charge interval (spec §4).

The locality lemma `rsstParts_local` (by `decide`) says that, at a hub `w_i` fitted with target `u` (anchor `n-2`),
no part constrains a ring-3 position, every constrained position that could be the middle of a 9+ link vertex is a fan
of an exact 6..8 spoke (so it is never a 9+ middle), and the hub letter is in `5..8`. For hub `u` every position is in
the window by construction (`uSpokePos` etc. have no ring-3 case).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-! ## Hub views and fits (all letters known) -/

/-- What a fit test reads at one spoke of a hub (letters `5..9`, `9` = 9+). -/
structure SpokeView where
  spoke : Nat
  hat : Nat
  fans : List Nat
deriving DecidableEq, Repr

/-- The spokes of a hub in rotation order; the hub degree is the length. -/
abbrev HubView := List SpokeView

/-- Subpart test at one spoke (spec §3.3 items 1-3). A fan list that is all `*` is not read. -/
def Sub.fits (s : Sub) (v : SpokeView) : Bool :=
  (s.spoke.isFull || s.spoke.test v.spoke) && (s.hat.isFull || s.hat.test v.hat) &&
  (s.fans.all Rng.isFull ||
    (s.fans.length == v.fans.length && (s.fans.zip v.fans).all fun rx => rx.1.isFull || rx.1.test rx.2))

/-- `p` fits the hub view `v` at anchor `a`: `deg hub = n` exactly and subpart `j` fits spoke `(a + j) % n`. -/
def Part.fitsAt (p : Part) (v : HubView) (a : Nat) : Bool :=
  v.length == p.subs.length &&
  (List.range p.subs.length).all fun j =>
    match p.subs[j]?, v[(a + j) % v.length]? with
    | some s, some x => s.fits x
    | _, _ => false

/-- `fits p v` at anchor 0 (the view already starts at the anchor). -/
def fits (p : Part) (v : HubView) : Bool := p.fitsAt v 0

/-- Index of the spoke that receives `p.amount` units when `p` fits at anchor `a` on a hub of degree `n`. -/
def Part.receiver (p : Part) (n a : Nat) : Nat := (a + p.target) % n

/-- Signed charge that one fit moves into the hub's spoke `t` (hub loses the same amount). -/
def Part.moved (p : Part) (v : HubView) (a : Nat) : Int := if p.fitsAt v a then (p.amount : Int) else 0

/-! ## Three-valued tests (some positions unknown) -/

/-- Result of a test or fit when some positions are ring 3: `no` = fails, `open_` = OPEN (passes every decided test),
`sure` = holds. -/
inductive Tri | no | open_ | sure
deriving DecidableEq, Repr

def Tri.and : Tri → Tri → Tri
  | .no, _ => .no
  | _, .no => .no
  | .open_, _ => .open_
  | _, .open_ => .open_
  | .sure, .sure => .sure

def Tri.ofBool (b : Bool) : Tri := if b then .sure else .no

/-- Range test on a possibly unknown letter (spec §3.4): `*` is always true; unknown + non-`*` is OPEN. -/
def Rng.test3 (r : Rng) : Option Nat → Tri
  | none => if r.isFull then .sure else .open_
  | some x => Tri.ofBool (r.isFull || r.test x)

/-- A spoke view whose hat and fans may be unknown (ring 3). Spokes are always window vertices. -/
structure PSpokeView where
  spoke : Nat
  hat : Option Nat
  fans : List (Option Nat)
deriving Repr

def Sub.fit3 (s : Sub) (v : PSpokeView) : Tri :=
  (Tri.ofBool (s.spoke.isFull || s.spoke.test v.spoke)).and <| (s.hat.test3 v.hat).and <|
    if s.fans.all Rng.isFull then .sure
    else if s.fans.length != v.fans.length then .no
    else (s.fans.zip v.fans).foldl (fun acc rx => acc.and (rx.1.test3 rx.2)) .sure

def Part.fit3At (p : Part) (v : List PSpokeView) (a : Nat) : Tri :=
  if v.length != p.subs.length then .no else
  (List.range p.subs.length).foldl (fun acc j =>
    acc.and <| match p.subs[j]?, v[(a + j) % v.length]? with
      | some s, some x => s.fit3 x
      | _, _ => .no) .sure

/-- Replace every unknown letter by `c` (used to check that the Bool and three-valued semantics agree). -/
def PSpokeView.fill (c : Nat) (v : PSpokeView) : SpokeView :=
  ⟨v.spoke, v.hat.getD c, v.fans.map (·.getD c)⟩

/-! ## Window positions (spec §2), relative to a base link index `b` -/

/-- Number of privates of a link letter; a 9+ is drawn as an 8 (spec §2, §6). -/
def npriv (L : Nat) : Nat := if L ≤ 5 then 0 else if 9 ≤ L then 3 else L - 5

/-- A window position relative to a base link index `b`:
* `u`; `w δ` = `w_{b+δ}`;
* `seg δ k` = `seg_{b+δ}[k]`, where `seg_m = [s_{m-1}, p_m.1, …, p_m.k, s_m]` (so `seg δ 0 = s_{b+δ-1}`);
* `segR δ k` = `seg_{b+δ}[len-1-k]` (counted from the `s_{b+δ}` end);
* `ring3`: outside the 2-ball. -/
inductive WPos
  | u
  | w (δ : Int)
  | seg (δ : Int) (k : Nat)
  | segR (δ : Int) (k : Nat)
  | ring3
deriving DecidableEq, Repr

/-- A position that is the middle `p.2` of a link vertex `w_{b+δ}` if that vertex is 9+ (its drawn seg then has 5
entries and the middle is index 2 from either end). With `hubOwn = true` the seg `δ = 0` is exempt: it belongs to the
hub `w_b` itself, whose letter is `≤ 8`. -/
def WPos.middleRisk (hubOwn : Bool) : WPos → Bool
  | .seg δ 2 => !(hubOwn && δ == 0)
  | .segR δ 2 => !(hubOwn && δ == 0)
  | _ => false

def WPos.isRing3 : WPos → Bool
  | .ring3 => true
  | _ => false

/-! ### Hub `w_i`, rotation `rot(w_i) = u, w_{i-1}, s_{i-1}, p_i.1..p_i.k, s_i, w_{i+1}` (`n = L_i` entries) -/

/-- Spoke at rotation index `t`. -/
def wSpokePos (n t : Nat) : WPos :=
  if t = 0 then .u else if t = 1 then .w (-1) else if t + 1 = n then .w 1 else .seg 0 (t - 2)

/-- Hat of the spoke at rotation index `t` (the vertex across the edge `S[t-1]–S[t]` from the hub). -/
def wHatPos (n t : Nat) : WPos :=
  if t = 0 then .w 2              -- across w_{i+1}–u
  else if t = 1 then .w (-2)      -- across u–w_{i-1}
  else if t = 2 then .segR (-1) 1 -- across w_{i-1}–s_{i-1}: p_{i-1}.last, or s_{i-2} if L_{i-1} = 5
  else if t + 1 = n then .seg 1 1 -- across s_i–w_{i+1}: p_{i+1}.1, or s_{i+1} if L_{i+1} = 5
  else .ring3                     -- across a ring-2 edge

/-- Fan `k` of the spoke at rotation index `t`. -/
def wFanPos (n t k : Nat) : WPos :=
  if t = 0 then .w (3 + k)            -- fans of u: w_{i+3}, …, w_{i-3}
  else if t = 1 then .seg (-1) k      -- fans of w_{i-1}: s_{i-2}, p_{i-1}.1, …
  else if t + 1 = n then .seg 1 (k + 2) -- fans of w_{i+1}: p_{i+1}.2, …, s_{i+1}
  else .ring3                         -- fans of s_i, s_{i-1} and the privates

/-! ### Hub `u`, rotation `rot(u) = w_0..w_{d-1}` (base 0) -/

def uSpokePos (t : Nat) : WPos := .w t
/-- Hat of `w_t` from `u`: `opp(w_t, w_{t-1}) = s_{t-1}`. -/
def uHatPos (t : Nat) : WPos := .seg t 0
/-- Fans of `w_t` from `u`: its privates `p_t.1..p_t.k`. -/
def uFanPos (t k : Nat) : WPos := .seg t (k + 1)

/-! ## The u-window -/

/-- The 2-ball of `u` with every window letter filled (spec §2): `link[i]` = letter of `w_i`, `apex[i]` = letter of
`s_i`, `priv[i]` = letters of `p_i.1..p_i.(npriv link[i])` (for a 9+ link vertex: y, middle, x). Letters `5..9`. -/
structure UWin where
  d : Nat
  link : List Nat
  apex : List Nat
  priv : List (List Nat)
deriving Repr

namespace UWin

def idx (W : UWin) (b : Nat) (δ : Int) : Nat := ((b + δ) % (W.d : Int)).toNat

def linkL (W : UWin) (m : Nat) : Nat := W.link.getD m 9
def apexL (W : UWin) (m : Nat) : Nat := W.apex.getD m 9

/-- `seg_m` as letters. -/
def segL (W : UWin) (m : Nat) : List Nat :=
  [W.apexL ((m + W.d - 1) % W.d)] ++ (W.priv.getD m []).take (npriv (W.linkL m)) ++ [W.apexL m]

/-- Letter at a position relative to base `b`; `none` for ring 3 (and for an out-of-range seg index). -/
def letter (W : UWin) (b : Nat) : WPos → Option Nat
  | .u => some (min W.d 9)
  | .w δ => some (W.linkL (W.idx b δ))
  | .seg δ k => (W.segL (W.idx b δ))[k]?
  | .segR δ k => let s := W.segL (W.idx b δ); if k < s.length then s[s.length - 1 - k]? else none
  | .ring3 => none

/-- Number of fans of a spoke vertex: `deg − 5` (u has degree d; 9+ drawn as 8). -/
def fanCount (W : UWin) (spokePos : WPos) (letter : Nat) : Nat :=
  match spokePos with
  | .u => W.d - 5
  | _ => npriv letter

/-- The view of hub `w_i` (rotation starting at u). -/
def viewW (W : UWin) (i : Nat) : List PSpokeView :=
  let n := W.linkL i
  (List.range n).map fun t =>
    let sp := (W.letter i (wSpokePos n t)).getD 0
    { spoke := sp, hat := W.letter i (wHatPos n t),
      fans := (List.range (W.fanCount (wSpokePos n t) sp)).map fun k => W.letter i (wFanPos n t k) }

/-- The view of hub `u`. -/
def viewU (W : UWin) : List PSpokeView :=
  (List.range W.d).map fun t =>
    let sp := (W.letter 0 (uSpokePos t)).getD 0
    { spoke := sp, hat := W.letter 0 (uHatPos t),
      fans := (List.range (npriv sp)).map fun k => W.letter 0 (uFanPos t k) }

/-- A fit that moves u's charge: part tag, hub (`none` = u, `some i` = w_i), receiving link index (for hub u),
`into` = target is u, and its three-valued result (never `no`). -/
structure Fired where
  tag : String
  hub : Option Nat
  recv : Nat
  into : Bool
  res : Tri
deriving Repr

/-- All fits that move u's charge (spec §3.5): hub `u` (d ∈ 5..8, every anchor), and hub `w_i` (letter 5..8, the anchor
`n-2` whose third spoke is u). -/
def fired (W : UWin) (parts : List Part := rsstParts) : List Fired :=
  let fromU :=
    if 5 ≤ W.d ∧ W.d ≤ 8 then
      (parts.filter (·.hub == W.d)).flatMap fun p =>
        (List.range W.d).filterMap fun a =>
          let r := p.fit3At W.viewU a
          if r == .no then none else some ⟨p.tag, none, p.receiver W.d a, false, r⟩
    else []
  let intoU := (List.range W.d).flatMap fun i =>
    let n := W.linkL i
    if n ≤ 8 then
      (parts.filter (·.hub == n)).filterMap fun p =>
        let r := p.fit3At (W.viewW i) (n - 2)
        if r == .no then none else some ⟨p.tag, some i, 0, true, r⟩
    else []
  fromU ++ intoU

/-- Charge interval of u (spec §4), RSST units: base `10(6-d)`. -/
def loHi (W : UWin) : Int × Int :=
  (W.fired).foldl (fun (lh : Int × Int) f =>
    let s : Int := if f.res == .sure then 1 else 0
    if f.into then (lh.1 + s, lh.2 + 1) else (lh.1 - 1, lh.2 - s)) (10 * (6 - (W.d : Int)), 10 * (6 - (W.d : Int)))

/-- Count of (part, hub, anchor) attempts where the Bool semantics on the view with unknowns filled by `c` disagrees
with the three-valued result being `sure` (0 everywhere is what locality predicts). -/
def boolDisagree (W : UWin) (c : Nat) : Nat :=
  let du :=
    if 5 ≤ W.d ∧ W.d ≤ 8 then
      (rsstParts.filter (·.hub == W.d)).foldl (fun acc p =>
        acc + ((List.range W.d).filter fun a =>
          (p.fitsAt (W.viewU.map (·.fill c)) a) != (p.fit3At W.viewU a == .sure)).length) 0
    else 0
  let dw := (List.range W.d).foldl (fun acc i =>
    let n := W.linkL i
    if n ≤ 8 then
      acc + ((rsstParts.filter (·.hub == n)).filter fun p =>
        (p.fitsAt ((W.viewW i).map (·.fill c)) (n - 2)) != (p.fit3At (W.viewW i) (n - 2) == .sure)).length
    else acc) 0
  du + dw

end UWin

/-! ## Locality (B3 §9 note 2), decidable over the 71 parts -/

/-- A test slot of a part, indexed by subpart `j` (relative to the anchor). -/
inductive Slot
  | spoke (j : Nat)
  | hat (j : Nat)
  | fan (j k : Nat)
deriving DecidableEq, Repr

/-- The slots whose range is not `*`: the positions the part constrains. -/
def Part.constrained (p : Part) : List Slot :=
  (List.range p.subs.length).flatMap fun j =>
    match p.subs[j]? with
    | none => []
    | some s =>
      (if s.spoke.isFull then [] else [Slot.spoke j]) ++ (if s.hat.isFull then [] else [Slot.hat j]) ++
      (if s.fans.all Rng.isFull then []
       else ((List.range s.fans.length).filter fun k => !(s.fans.getD k ⟨5, 9⟩).isFull).map (Slot.fan j))

/-- Window position read by a slot when the part is fitted at a hub `w_i` with target u (anchor `n-2`, so subpart `j`
reads rotation index `(n-2+j) % n`). -/
def Part.slotPosW (p : Part) : Slot → WPos
  | .spoke j => wSpokePos p.hub ((p.hub - 2 + j) % p.hub)
  | .hat j => wHatPos p.hub ((p.hub - 2 + j) % p.hub)
  | .fan j k => wFanPos p.hub ((p.hub - 2 + j) % p.hub) k

/-- Window position read by a slot when the part is fitted at hub u with anchor `a` (relative to `w_a`: `δ = j`). -/
def Part.slotPosU : Slot → WPos
  | .spoke j => uSpokePos j
  | .hat j => uHatPos j
  | .fan j k => uFanPos j k

/-- The slot is a fan of a subpart whose spoke range is an exact `L ∈ 6..8` with `L − 5` fans: the spoke test then
forces the spoke vertex to have letter `L ≤ 8`, so its own seg (which the fan reads) has no 9+ middle. -/
def Part.fanOnExact (p : Part) : Slot → Bool
  | .fan j _ => match p.subs[j]? with
    | some s => s.spoke.exact68 && s.fans.length == s.spoke.lo - 5
    | none => false
  | _ => false

/-- The decidable locality property of one part (B3 §9 note 2):
1. hub letter in `5..8` and equal to the number of subparts;
2. at a hub `w_i` with target u, no constrained slot reads ring 3;
3. at a hub `w_i` and at hub u, a constrained slot that could read a 9+ middle is a fan of an exact 6..8 spoke whose
   seg it reads (fans of `w_{i±1}` read `seg (±1)`; fans of `w_t` from u read `seg t`). -/
def Part.isLocal (p : Part) : Bool :=
  Nat.ble 5 p.hub && Nat.ble p.hub 8 && p.subs.length == p.hub &&
  p.constrained.all fun s =>
    !(p.slotPosW s).isRing3 &&
    (!((p.slotPosW s).middleRisk true) || p.fanOnExact s) &&
    (!((Part.slotPosU s).middleRisk false) || p.fanOnExact s)

theorem rsstParts_local : rsstParts.all Part.isLocal = true := by decide

/-- Hub u never reads ring 3 (by construction of the hub-u positions). -/
theorem slotPosU_not_ring3 (s : Slot) : (Part.slotPosU s).isRing3 = false := by
  cases s <;> rfl

end SimpleGraph.SphericalMap.RSSTSeed
