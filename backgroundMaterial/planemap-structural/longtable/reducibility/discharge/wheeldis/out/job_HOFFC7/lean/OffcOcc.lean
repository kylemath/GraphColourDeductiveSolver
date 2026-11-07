import COccBridge
import DCheckMirror

/-!
# OffcOcc (Opus, s76_occ502/offc7, HOFFC7, 7 Nov 2026): window → occurrence for off-centre kills

STATEMENT ONLY. This file has NOT been compiled: there is no Lean toolchain where it was written. Every claim is a
`def … : Prop`, so the file contains no `sorry`. The Studio is asked to prove `OffcRotOcc`.

## Why the existing glue cannot express this

The glue generated so far (gen_occ_kc.py: `<K>.lean`, `COcc<K>.lean`, `<MOD>Occ.lean`) takes a rotation occurrence
`<K>.Occ T ring int` as a hypothesis. `Occ` lists an injective interior, its degrees, and `T`'s rotation at every
interior vertex (the `Nx` facts, ring vertices included). It never mentions `u`, a row, LINK/SWORD or a window, so it is
centre-free. Once `Occ` is in hand, it applies at an off-centre `phi` exactly as it does at `u`.

What the glue does not contain is the step from a row to `Occ`: COORDINATOR-STATE's Job 26 (iii)(b), "Nx facts from an
appearing 2-ball", which is still open on main. That step is missing for u-centred windows too, so the current glue does
not prove occurrence for u-centred windows either. A generator cannot supply the step one key at a time:
* the ring vertices of `K` (`ring` in `Occ`) are in general privates and ring-3 vertices, which the 1.5-ball does not
  name, so they have to be extracted from `T`'s rotation;
* the interior `Nx` facts have to come from the window's faces;
* the interior non-adjacencies have to come from §1's internal-6-connectivity reading.
Each of these is a generic lemma about `T`. The only key- and line-specific content is decidable. It is `OffcOK` (per
line) and `RingLinked` (per key), which `native_decide` would check.

## The statement

* `Window T d c w s` is the row's 1.5-ball in `T` (OFFC_SPEC §1), as `Nx` facts in `T`'s orientation:
  - `Nx T c (w i) (w (i+1))`, the link of `c`;
  - `Nx T (w (i+1)) (w i) (s i)`, so `s i` is the apex of `w i w (i+1)` across from `c`.
  It also carries injectivity on the known vertices and §1's adjacency rule among them (`s (i-1) – s i` iff
  `deg (w i) = 5`). Those two fields are §1's internal-6-connectivity argument (Job 26 step 3a). They are hypotheses
  here, not proved.
* `Matches T c w s pat`: every lettered slot of the line has that degree in `T` (`N` means ≥ 6).
* `OffcOK d rot φ pat ε` is decidable:
  - `φ` is injective;
  - `u` takes only a vertex of degree `d`, and every other image carries its exact letter;
  - `φ` is induced on §1's adjacency, with the `s (i-1) s i` pairs read from the letter of `w i` (5, or N/6/7/8);
  - every two consecutive interior slots of `rot a` span a window face with the single orientation `ε`;
  - the interior slots of each `rot a` form one nonempty cyclic block.
  This replaces OFFC_SPEC §R's conditions 1-5 and its proof on the line itself.
* `RingLinked r rot fan` is decidable and per key: every ring position occurs, and its occurrences are chained by
  faces that both rotations see.
* `OffcRotOcc` concludes `∃ ρ, RotOcc (bif ε then T else T.mirror) ρ (vert ∘ φ) rot`.
  - Per key, `occ_of_rotOcc` (template at the end, the converse of `rotOcc_of_occ`) turns this into `<K>.Occ`.
  - The existing `colorable_of_occ_entry` / `colorable_of_mirror_occ_entry` (D, with `hD`) or
    `colorable_of_occ_centry` / `colorable_of_mirror_occ_centry` (C, with a `CEntryF`) then colour `T`.
  - So a minimal counterexample has no row window that matches the line, and the row is inadmissible.

## Proof plan (for the Studio)

(a) Window faces.
  - `link` and `apex` give the faces `c w_i w_{i+1}` and `w_{i+1} w_i s_i` at all three corners (`nx_tri`).
  - At a five `w_i`, `orbitN` closes the four steps `s_i → w_{i+1} → c → w_{i-1} → s_{i-1}` with `s_{i-1} → s_i`.
  - Hence `face five x y z → Nx T (vert x) (vert y) (vert z)`, and `nx_mirror` gives the `ε = false` case.

(b) Positions in the rotation.
  - Pick an interior slot `q` of `rot a` and let `nb a k` be the `((q - k) mod L)`-th `next` of the dart
    `(ι a, ι (rot a)[q])`.
  - Then `Nx (ι a) (nb a (k+1)) (nb a k)` for every `k` (`orbitN` at degree `L`).
  - (4) and (5) give `nb a k = ι (rot a)[k]` on the interior block.

(c) The ring vertices.
  - Let `ρ t := nb a k` for the first `a ∈ fan t` and its slot `k` with `(rot a)[k] = inr t`, and `ρ t := ρ (t % r)`
    for `t ≥ r`.
  - `RingLinked` and `nx_tri` (plus injectivity of `next`) give the same vertex for every occurrence.

(d) `disj`.
  - If `nb a k = ι b`, then `Window.adj`, `Matches` and (3) put `inl b` in `rot a` at another position.
  - That contradicts `orbitN`'s injectivity at degree `L`.

(e) The other fields. `ιinj` comes from `Window.inj` and (1); `deg` comes from `Matches`, `deg_c` and (2).

Data: `d7_lines.tsv` holds the 68 d = 7 lines. For the 55 kills whose kc line is in the tree it gives `phi` in kc order
(`φ`) and `ε`. `fans_d7.tsv` holds each key's `fan`. scripts/offc_model.py is a Python model of `OffcOK` and passes on
all 250 lines. scripts/kcmap.py and scripts/fans.py check `OffcOK` and `RingLinked` on gen_occ_kc's own `rot` for those
55 keys.
-/

namespace SimpleGraph.SphericalMap.Offc
open VacancyIcosahedral

/-! ## The degree-`d` window (OFFC_SPEC §1) -/

/-- A known slot of the degree-`d` window: the centre `u`, a link vertex `w i`, an apex `s i`. -/
inductive Slot (d : ℕ) where
  | u : Slot d
  | w : Fin d → Slot d
  | s : Fin d → Slot d
  deriving DecidableEq

/-- The vertex of `T` at a slot. -/
def Slot.vert {n d : ℕ} (c : Fin n) (w s : Fin d → Fin n) : Slot d → Fin n
  | .u => c
  | .w i => w i
  | .s i => s i

/-- §1's adjacency among known slots. `five i`: `w i` has degree 5. -/
def wAdj {d : ℕ} [NeZero d] (five : Fin d → Bool) : Slot d → Slot d → Bool
  | .u, .w _ => true
  | .w _, .u => true
  | .w i, .w j => decide (j = i + 1) || decide (i = j + 1)
  | .w i, .s j => decide (j = i) || decide (j + 1 = i)
  | .s j, .w i => decide (j = i) || decide (j + 1 = i)
  | .s i, .s j => (decide (j = i + 1) && five j) || (decide (i = j + 1) && five i)
  | _, _ => false

/-- `(x, y, z)` is, in this cyclic order, one of §1's faces in `Window`'s orientation: `u w_i w_{i+1}`,
`w_{i+1} w_i s_i`, or (when `five i`) `w_i s_{i-1} s_i`. -/
def face0 {d : ℕ} [NeZero d] (five : Fin d → Bool) : Slot d → Slot d → Slot d → Bool
  | .u, .w i, .w j => decide (j = i + 1)
  | .w j, .w i, .s k => decide (j = i + 1) && decide (k = i)
  | .w i, .s k, .s l => decide (k + 1 = i) && decide (l = i) && five i
  | _, _, _ => false

/-- `face0` up to cyclic rotation of the triple. -/
def face {d : ℕ} [NeZero d] (five : Fin d → Bool) (x y z : Slot d) : Bool :=
  face0 five x y z || face0 five y z x || face0 five z x y

/-- **The row's 1.5-ball in `T`** at a centre `c` of degree `d` (OFFC_SPEC §1). `w` is the link of `c` in rotation
order, and `s i` is the apex of `w i w (i+1)` across from `c`. `inj` and `adj` are §1's reading of a minimal
counterexample: the known vertices are distinct, and two of them are adjacent exactly as in the window, with the pair
`s (i-1) s i` adjacent iff `w i` has degree 5. They come from internal 6-connectivity (Job 26 step 3a) and are not
proved here. -/
structure Window {n : ℕ} (T : SphericalMap n) (d : ℕ) [NeZero d] (c : Fin n) (w s : Fin d → Fin n) : Prop where
  inj : Function.Injective (Slot.vert c w s)
  deg_c : T.graph.degree c = d
  link : ∀ i, Nx T c (w i) (w (i + 1))
  apex : ∀ i, Nx T (w (i + 1)) (w i) (s i)
  adj : ∀ x y : Slot d, x ≠ y →
    (T.Adj (Slot.vert c w s x) (Slot.vert c w s y) ↔
      wAdj (fun i => decide (T.graph.degree (w i) = 5)) x y = true)

/-! ## A line's letters (OFFC_SPEC §3, §F) -/

/-- A slot letter of an rpatN line: an exact degree (5..8), `N` (degree ≥ 6, LINK only), or free (`.`). -/
inductive Letter where
  | exact : ℕ → Letter
  | big : Letter
  | free : Letter
  deriving DecidableEq

def Letter.ofChar : Char → Letter
  | '5' => .exact 5
  | '6' => .exact 6
  | '7' => .exact 7
  | '8' => .exact 8
  | 'N' => .big
  | _ => .free

/-- Is the letter a five? `none` for a free slot. -/
def Letter.five : Letter → Option Bool
  | .exact k => some (k == 5)
  | .big => some false
  | .free => none

/-- The line's letters on slots, from its LINK and SWORD fields (written in phi's own orientation, §F). -/
def patOf {d : ℕ} (link sword : String) : Slot d → Letter
  | .u => .free
  | .w i => Letter.ofChar (link.toList.getD i.val '.')
  | .s i => Letter.ofChar (sword.toList.getD i.val '.')

/-- The row at `(c, w, s)` carries the line's letters: each lettered slot other than `u` has that degree in `T`. -/
def Matches {n d : ℕ} (T : SphericalMap n) (c : Fin n) (w s : Fin d → Fin n) (pat : Slot d → Letter) : Prop :=
  ∀ x, x ≠ Slot.u → match pat x with
    | .exact k => T.graph.degree (Slot.vert c w s x) = k
    | .big => 6 ≤ T.graph.degree (Slot.vert c w s x)
    | .free => True

/-- §1's adjacency as the line fixes it. The pair `s (i-1) s i` is read from the letter of `w i`; it is `none` when
that letter is free. -/
def pAdj {d : ℕ} [NeZero d] (pat : Slot d → Letter) : Slot d → Slot d → Option Bool
  | .s i, .s j =>
    if j = i + 1 then (pat (.w j)).five else if i = j + 1 then (pat (.w i)).five else some false
  | x, y => some (wAdj (fun _ => false) x y)

/-! ## The decidable checks -/

/-- **Per line** (`native_decide`). `rot` is the key's rotation in `RotOcc`'s convention (the `rot` of `COcc<K>.lean`:
`Nx T (ι a) (rot a)[k+1] (rot a)[k]`). `φ a` is the window slot of interior vertex `a` (the line's `phi` in the key's
kc order, column `phi_kc` of d7_lines.tsv). `pat = patOf LINK SWORD`. `ε = false` means the occurrence is in
`T.mirror`. -/
def OffcOK {m : ℕ} (d : ℕ) [NeZero d] (rot : Fin m → List (Fin m ⊕ ℕ)) (φ : Fin m → Slot d)
    (pat : Slot d → Letter) (ε : Bool) : Bool :=
  let five : Fin d → Bool := fun i => (pat (.w i)).five == some true
  let slotAt : Fin m → ℕ → Fin m ⊕ ℕ := fun a k => (rot a).getD (k % (rot a).length) (.inr 0)
  let V := List.finRange m
  -- (1) φ is injective
  V.all (fun a => V.all (fun b => a == b || φ a != φ b)) &&
  -- (2) `u` only for a vertex of degree `d`; every other image carries its exact letter
  V.all (fun a => match φ a with
    | .u => (rot a).length == d
    | x => pat x == Letter.exact (rot a).length) &&
  -- (3) induced on §1's adjacency
  V.all (fun a => V.all (fun b => a == b ||
    pAdj pat (φ a) (φ b) == some ((rot a).contains (.inl b)))) &&
  -- (4) two consecutive interior slots `(k+1, k)` of `rot a` span a window face, all with orientation `ε`
  V.all (fun a => (List.range (rot a).length).all (fun k =>
    match slotAt a (k + 1), slotAt a k with
    | .inl b, .inl c => if ε then face five (φ a) (φ b) (φ c) else face five (φ a) (φ c) (φ b)
    | _, _ => true)) &&
  -- (5) the interior slots of `rot a` form one nonempty cyclic block
  V.all (fun a => (rot a).any Sum.isLeft &&
    decide (((List.range (rot a).length).filter
      (fun k => (slotAt a k).isLeft && (slotAt a (k + 1)).isRight)).length ≤ 1))

/-- Both rotations see the face `a b t` (ring position `t`), from either side. -/
def seesFace {m : ℕ} (rot : Fin m → List (Fin m ⊕ ℕ)) (a b : Fin m) (t : ℕ) : Bool :=
  let sl : Fin m → ℕ → Fin m ⊕ ℕ := fun x k => (rot x).getD (k % (rot x).length) (.inr 0)
  (List.range (rot a).length).any (fun k =>
    (sl a (k + 1) == (Sum.inl b : Fin m ⊕ ℕ) && sl a k == (Sum.inr t : Fin m ⊕ ℕ) &&
      (List.range (rot b).length).any (fun j =>
        sl b j == (Sum.inl a : Fin m ⊕ ℕ) && sl b (j + 1) == (Sum.inr t : Fin m ⊕ ℕ))) ||
    (sl a (k + 1) == (Sum.inr t : Fin m ⊕ ℕ) && sl a k == (Sum.inl b : Fin m ⊕ ℕ) &&
      (List.range (rot b).length).any (fun j =>
        sl b j == (Sum.inr t : Fin m ⊕ ℕ) && sl b (j + 1) == (Sum.inl a : Fin m ⊕ ℕ))))

/-- **Per key** (`native_decide`; fans in fans_d7.tsv).
* Every `rot a` is duplicate-free and lists only ring positions `< r`.
* For each `t < r`, `fan t` is nonempty and is exactly the set of vertices whose rotation lists `inr t`.
* Consecutive members of `fan t` see their common face with `t`. -/
def RingLinked {m : ℕ} (r : ℕ) (rot : Fin m → List (Fin m ⊕ ℕ)) (fan : ℕ → List (Fin m)) : Bool :=
  decide (0 < r) &&
  (List.finRange m).all (fun a => decide (rot a).Nodup &&
    (rot a).all (fun x => match x with
      | .inr t => decide (t < r)
      | .inl _ => true)) &&
  (List.range r).all (fun t => !(fan t).isEmpty &&
    (List.finRange m).all (fun a => (rot a).contains (.inr t) == (fan t).contains a) &&
    ((fan t).zip (fan t).tail).all (fun p => seesFace rot p.1 p.2 t))

/-! ## The lemma to prove -/

/-- **Window → rotation occurrence (to prove).** On a triangulation, take a row window whose letters match a line,
with the line's check and the key's ring check passing. Then the key's rotation occurrence sits at `φ`: in `T` when
`ε` is true, in `T.mirror` otherwise. -/
def OffcRotOcc : Prop :=
  ∀ {n d m : ℕ} [NeZero d] (T : SphericalMap n) (c : Fin n) (w s : Fin d → Fin n)
    (r : ℕ) (rot : Fin m → List (Fin m ⊕ ℕ)) (fan : ℕ → List (Fin m)) (φ : Fin m → Slot d)
    (pat : Slot d → Letter) (ε : Bool),
    T.Triangulated → 7 ≤ d → Window T d c w s → Matches T c w s pat →
    OffcOK d rot φ pat ε = true → RingLinked r rot fan = true →
    ∃ ρ : ℕ → Fin n, RotOcc (bif ε then T else T.mirror) ρ (fun a => Slot.vert c w s (φ a)) rot

/-! ## Templates (per key and per line; generated once `OffcRotOcc` is proved and the kill has `hD`/`hC`)

Per key, in `COcc<K>.lean` next to `rotOcc_of_occ` (it is the converse; one `R.nx a k` per `Occ` field):

```
def fan (t : ℕ) : List (Fin 9) := ([[2, 1, 0, 3], [2, 7], …] : List (List (Fin 9))).getD t []
theorem fan_ok : Offc.RingLinked 11 rot fan = true := by native_decide
theorem occ_of_rotOcc {T : SphericalMap n} {ρ : ℕ → Fin n} {int : Fin 9 → Fin n}
    (R : RotOcc T ρ int rot) : Occ T (fun t => ρ t.val) int where
  int_inj := R.ιinj
  disj := fun t a => R.disj t.val a
  deg := fun a => by rw [R.deg a]; fin_cases a <;> rfl
  r0_0 := R.nx 0 0 (by decide)
  …
```

Per line. d7_lines.tsv line 4 is `7 856...5 55...55 # D f8_...55755_...56B5.`, with phi_kc
`0>w0,1>s0,2>s6,3>w6,4>u,5>w1,6>s1,7>s5,8>w2` and eps_kc `+`:

```
theorem kill_4 (hU : Offc.OffcRotOcc) {T : SphericalMap n} (htri : T.Triangulated) {c : Fin n}
    {w s : Fin 7 → Fin n} (W : Offc.Window T 7 c w s)
    (hM : Offc.Matches T c w s (Offc.patOf "856...5" "55...55"))
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨ρ, R⟩ := hU T c w s 11 K.rot K.fan
    ![.w 0, .s 0, .s 6, .w 6, .u, .w 1, .s 1, .s 5, .w 2] (Offc.patOf "856...5" "55...55") true
    htri (by norm_num) W hM (by native_decide) K.fan_ok
  exact K.colorable_of_occ_entry hD rfl htri (K.occ_of_rotOcc R) IH
```

When eps_kc is `-`, pass `false` and finish with `colorable_of_mirror_occ_entry`. For a C kill, finish with
`colorable_of_occ_centry` and the `CEntryF`. Here `K` is the kill's per-key module and `hD` its verdict. Neither
exists on main for the 66 D kills; see d7_lines.tsv column `lean`.
-/

end SimpleGraph.SphericalMap.Offc
