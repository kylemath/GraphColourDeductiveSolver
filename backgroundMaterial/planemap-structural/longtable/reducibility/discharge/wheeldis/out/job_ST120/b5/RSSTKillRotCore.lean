import RSSTD9Core

/-!
# ST-120 B5: rotation-respecting containment (`checkEmbRot`) and the checkers that use it

Studio, 11 Nov (partial-mirror gap). `checkEmb` checks degrees, injectivity and induced adjacency only; a placement
that flips one block of `K` across a small interior cut passes it but is no occurrence. `checkEmbRot` adds:
**one common chirality** `ε ∈ {+1, −1}` such that at every interior vertex `x` the cyclic neighbour list of `x` in
`K` (`rot x`: interior neighbour `j` as `j`, a ring neighbour as `1000`) maps onto the window rotation of the host
`e x` (`hostRot`, B4 M1 / spec §2):
* `u`: `w_0, …, w_{d−1}`;
* `w_i`: `u, w_{i−1}, s_{i−1}, p_i.1, …, p_i.k, s_i, w_{i+1}`;
* `s_i`: `R2next, w_{i+1}, w_i, R2prev`, then `deg − 4` ring-3 slots (unknown);
* `p_i.(k+1)`: `R2next, w_i, R2prev`, then `deg − 3` ring-3 slots;
read with an offset `o` and direction `ε`; every interior neighbour must land on its image (a ring neighbour of `K`
may land anywhere, also on a ring-3 slot). The host's rotation length must equal `deg x`.
`KillsRot KLR W` uses it; `KillsRot.toKills`, `KillsRot.mono`. The checkers `checkDegPR`, `checkDegRotPR`,
`checkDegHiR` are `checkDegP`, `checkDegRotP`, `checkDegHi` with the kill requirement `reqOfR` (= `reqOf` after the
rotation test; the rotation test reads only `d`, the link word and `K`).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-- A configuration with its interior rotations. -/
abbrev ConfR := Conf × List (List Nat)

def ringTag : Nat := 1000

/-- Window rotation at a vertex code (`none` = ring-3 slot); `deg` = the letter the host must have. -/
def hostRot (d : Nat) (link : List Nat) (v deg : Nat) : List (Option Nat) :=
  let np := fun i => npriv (link.getD i 9)
  let w := fun i => 1 + i % d
  let s := fun i => 1 + d + i % d
  let p := fun i k => 1 + 2 * d + 3 * i + k
  match vkind d v with
  | .u => (List.range d).map fun j => some (w j)
  | .w i => [some 0, some (w (i + d - 1)), some (s (i + d - 1))] ++ ((List.range (np i)).map fun k => some (p i k)) ++
      [some (s i), some (w (i + 1))]
  | .s i =>
    let nx := if 1 ≤ np ((i + 1) % d) then p ((i + 1) % d) 0 else s (i + 1)
    let pv := if 1 ≤ np i then p i (np i - 1) else s (i + d - 1)
    [some nx, some (w (i + 1)), some (w i), some pv] ++ List.replicate (deg - 4) none
  | .p i k =>
    let nx := if k + 1 < np i then p i (k + 1) else s i
    let pv := if 1 ≤ k then p i (k - 1) else s (i + d - 1)
    [some nx, some (w i), some pv] ++ List.replicate (deg - 3) none
  | .bad => []

/-- One interior vertex: `K`'s rotation `kr` (images by `e`) sits in the host rotation `hr` at some offset, direction
`ε` (`true` = same, `false` = reversed). -/
def vertexOK (hr : List (Option Nat)) (kr : List Nat) (e : List Nat) (ε : Bool) : Bool :=
  let n := hr.length
  kr.length == n &&
  (List.range n).any fun o => (List.range n).all fun k =>
    let y := kr.getD k ringTag
    y == ringTag || hr.getD (if ε then (o + k) % n else (o + (n - k)) % n) none == some (e.getD y 0)

/-- The rotation test, under one chirality for all interior vertices. -/
def rotOK (Kr : ConfR) (d : Nat) (link : List Nat) (e : List Nat) : Bool :=
  [true, false].any fun ε => (List.range Kr.1.size).all fun x =>
    vertexOK (hostRot d link (e.getD x 0) (Kr.1.degOf x)) (Kr.2.getD x []) e ε

/-- **Rotation-respecting containment.** -/
def checkEmbRot (Kr : ConfR) (W : UWin) (e : List Nat) : Bool := checkEmb Kr.1 W e && rotOK Kr W.d W.link e

def KillsRot (KLR : List ConfR) (W : UWin) : Prop := ∃ Kr ∈ KLR, ∃ e, checkEmbRot Kr W e = true

theorem KillsRot.toKills {KLR : List ConfR} {W : UWin} (h : KillsRot KLR W) : Kills (KLR.map Prod.fst) W := by
  obtain ⟨Kr, hK, e, he⟩ := h
  simp only [checkEmbRot, Bool.and_eq_true] at he
  exact ⟨Kr.1, List.mem_map.2 ⟨Kr, hK, rfl⟩, e, he.1⟩

theorem KillsRot.mono {KL KL' : List ConfR} (h : ∀ K ∈ KL, K ∈ KL') {W : UWin} (hk : KillsRot KL W) :
    KillsRot KL' W := by
  obtain ⟨K, hK, e, he⟩ := hk
  exact ⟨K, h K hK, e, he⟩

/-- The rotation data agrees with the configuration (length = degree, interior entries = the interior neighbours, each
once) and is coherently oriented (if `y, z` follow each other in `rot x` and are interior, then `z, x` in `rot y`). -/
def rotWF (Kr : ConfR) : Bool :=
  Kr.2.length == Kr.1.size &&
  (List.range Kr.1.size).all fun x =>
    let r := Kr.2.getD x []
    let n := r.length
    n == Kr.1.degOf x &&
    (r.filter (· != ringTag)).length == (Kr.1.adj.getD x []).length &&
    (Kr.1.adj.getD x []).all (fun y => r.contains y) &&
    (List.range n).all fun k =>
      let y := r.getD k ringTag
      let z := r.getD ((k + 1) % n) ringTag
      y == ringTag || z == ringTag ||
        (let ry := Kr.2.getD y []
         (List.range ry.length).any fun t => ry.getD t ringTag == z && ry.getD ((t + 1) % ry.length) ringTag == x)

/-- Kill requirement of a rotation-respecting embedding. -/
def reqOfR (Kr : ConfR) (d : Nat) (link : List Nat) (e : List Nat) : Option (List (Nat × Nat)) :=
  if rotOK Kr d link e then reqOf Kr.1 d link e else none

/-! ## The checkers with rotation-respecting kills -/

def checkLinkPR (parts : List Part) (KLR : List ConfR) (d : Nat) (link : List Nat) (c : LinkCert) : Bool :=
  let X := tagW d link
  let ins := (instIn parts X).filter (· != .no)
  let outs := (instOut parts X).filter (· != .no)
  let reqs := c.embs.filterMap fun ke => match KLR[ke.1]? with
    | some K => reqOfR K d link ke.2
    | none => none
  c.order.all isCode && dfs (10 * (6 - (d : Int))) (c.order.map fun v => (v, classesOf v (ins ++ outs))) ins outs reqs

def checkLinksPR (parts : List Part) (KLR : List ConfR) (d : Nat) : List (List Nat) → List LinkCert → Bool
  | [], _ => true
  | l :: ls, [] => checkLinkPR parts KLR d l .empty && checkLinksPR parts KLR d ls []
  | l :: ls, c :: cs => checkLinkPR parts KLR d l c && checkLinksPR parts KLR d ls cs

def checkDegPR (parts : List Part) (KLR : List ConfR) (d : Nat) (cert : List LinkCert) : Bool :=
  parts.all Part.fanExact && Nat.ble 5 d && Nat.ble d 30 && checkLinksPR parts KLR d (allWords d) cert

def checkDegRotPR (parts : List Part) (KLR : List ConfR) (d : Nat) (cert : List LinkCert) : Bool :=
  parts.all Part.fanExact && Nat.ble 5 d && Nat.ble d 30 &&
    checkLinksPR parts KLR d ((allWords d).filter isRotMin) cert

def checkDegHiR (parts : List Part) (KLR : List ConfR) (d : Nat) (cert : List LinkCert) : Bool :=
  let tab := cTab parts
  parts.all Part.fanExact && parts.all Part.wellShaped && slotAll parts && Nat.ble 9 d && Nat.ble d 30 &&
    tabOK parts tab && checkLinksPR parts KLR d (linkSurv tab d) cert

end SimpleGraph.SphericalMap.RSSTSeed
