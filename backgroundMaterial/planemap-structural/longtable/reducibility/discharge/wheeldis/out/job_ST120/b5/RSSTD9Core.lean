import RSSTDeg15
import RSSTRot

/-!
# ST-127 (2): d = 9..14, computational part: the window table `c⁺` and the link-word search

`slotEntryW win L t` is the slot view of a hub `w_i` (letter `L = win[2]`, anchor `L-2`) in which the four letters the
view reads off the link are known: `win = [L_{i-2}, L_{i-1}, L_i, L_{i+1}, L_{i+2}]` (spoke `t = 1` is `w_{i-1}`, spoke
`t = L-1` is `w_{i+1}`, hat `t = 0` is `w_{i+2}`, hat `t = 1` is `w_{i-2}`); every other read is a code as in
`slotEntry`. `cplusW parts win` is the least `c ≤ 6` for which the checker's `dfs` shows at most `c` possible fits into
`u` (6 if none; 6 always holds by `hub_bound`). Spec §8.4's c⁺ table.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

def slotEntryW (win : List Nat) (L t : Nat) : TSpoke :=
  { sp := if t = 0 then 9 else if t = 1 then win.getD 1 9 else if t + 1 = L then win.getD 3 9 else slotSp t,
    hat := if t = 0 then some (win.getD 4 9) else if t = 1 then some (win.getD 0 9)
      else if hatRing3 L t then none else some (slotHat t),
    fansOf := fun m => if t = 0 then [] else (List.range m).map fun k => if fanRing3 L t then none else some (slotFan t k),
    fc := if t = 0 then fun _ => 0 else npriv }

def slotViewW (win : List Nat) : List TSpoke := (List.range (win.getD 2 9)).map (slotEntryW win (win.getD 2 9))

def slotInsW (parts : List Part) (win : List Nat) : List SRes :=
  (parts.filter (·.hub == win.getD 2 9)).map fun p => symFit p (slotViewW win) (win.getD 2 9 - 2)

def slotOrderW (parts : List Part) (win : List Nat) : List Nat :=
  (((slotInsW parts win).flatMap fun x => match x with
    | .c cs _ => cs.map (·.1)
    | .no => []).eraseDups).filter isCode

def slotCheckW (parts : List Part) (win : List Nat) (c : Nat) : Bool :=
  dfs (-(c : Int)) ((slotOrderW parts win).map fun v => (v, classesOf v (slotInsW parts win)))
    ((slotInsW parts win).filter (· != .no)) [] []

/-- `c⁺` of a 5-letter link window (hub letter `win[2]`): 0 for a 9+ hub, else the least verified `c ≤ 6`. -/
def cplusW (parts : List Part) (win : List Nat) : Nat :=
  if win.getD 2 9 ≤ 8 then (([0, 1, 2, 3, 4, 5].find? fun c => slotCheckW parts win c)).getD 6 else 0

/-! ## The table, the link-word search and the per-degree check -/

/-- Base-5 index of a window over `5..9` (first letter slowest, = position in `allWords 5`). -/
def code5 (w : List Nat) : Nat := w.foldl (fun a x => 5 * a + (x - 5)) 0

/-- The `c⁺` table, in `allWords 5` order. -/
def cTab (parts : List Part) : Array Nat := (allWords 5).toArray.map (cplusW parts)

/-- Every table entry is a verified bound (`≥ 6` falls back to `hub_bound`); a 9+ hub has entry 0. -/
def tabOK (parts : List Part) (tab : Array Nat) : Bool :=
  (allWords 5).all fun w =>
    let c := tab.getD (code5 w) 6
    if w.getD 2 9 ≤ 8 then (Nat.ble 6 c || slotCheckW parts w c) else c == 0

def bnd (tab : Array Nat) (w : List Nat) : Nat := min 6 (tab.getD (code5 w) 6)

/-- Positions `i-2..i+2` (mod `d`). -/
def winIx (d i : Nat) : List Nat := [0, 1, 2, 3, 4].map fun j => (i + d + j - 2) % d

/-- The window of hub `i` in a link word. -/
def winAt (L : List Nat) (i : Nat) : List Nat := (winIx L.length i).map fun x => L.getD x 9

/-- Contribution of hub `i` given the first `P.length` letters `P` of a word of length `d`. -/
def pb (tab : Array Nat) (d : Nat) (P : List Nat) (i : Nat) : Nat :=
  if (winIx d i).all (· < P.length) then bnd tab ((winIx d i).map fun x => P.getD x 9)
  else if i < P.length ∧ P.getD i 9 = 9 then 0 else 6

def pbound (tab : Array Nat) (d : Nat) (P : List Nat) : Int :=
  60 - 10 * (d : Int) + ((List.range d).map fun i => (pb tab d P i : Int)).sum

/-- Link words of length `d` (prefix `P`, `f` letters to go) whose bound stays positive, rotation-least ones kept. -/
def search (tab : Array Nat) (d : Nat) : Nat → List Nat → List (List Nat)
  | f, P =>
    if pbound tab d P ≤ 0 then [] else
    match f with
    | 0 => if isRotMin P then [P] else []
    | f + 1 => [5, 6, 7, 8, 9].flatMap fun a => search tab d f (P ++ [a])

def linkSurv (tab : Array Nat) (d : Nat) : List (List Nat) := search tab d d []

/-- **The check for `d ≥ 9`**: `c⁺` table (verified), link-word search, the per-word replay on the survivors. -/
def checkDegHi (parts : List Part) (KL : List Conf) (d : Nat) (cert : List LinkCert) : Bool :=
  let tab := cTab parts
  parts.all Part.fanExact && parts.all Part.wellShaped && slotAll parts && Nat.ble 9 d && Nat.ble d 30 &&
    tabOK parts tab && checkLinksP parts KL d (linkSurv tab d) cert

end SimpleGraph.SphericalMap.RSSTSeed
