/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TutteSides

/-!
# Axiom A5v ("Jordan at v") on the sphere, from `Fills`

Long Table draft (13 Oct 2026), outside the accepted build. Source of the axiom:
`longtable/axioms/README.md` (Runs 1–2).

## Setting (TrackU's matching form)

`M` is a `SphericalMap` (a rotation system in which every even edge set is a sum of face
boundaries, `Fills`). In the intended use `M` is the Tait dual of a sphere triangulation with
a hole: cubic except one vertex `v` of degree 5 whose darts `f 0, …, f 4` are in rotation
order (`Hole5`). A *state* is a perfect matching `Mt` (`IsPerfectMatching`). At frame `k`
(`f k ∈ Mt`) the state is a *figure-eight* (`Fig8`) when `E − Mt` is connected and its two
loops at `v` are `X` through `f (k−1), f (k+1)` and `Y` through `f (k+2), f (k−2)`.
The interiors of the loops are the two components of `qGraph` (`E − Mt` with `v` deleted).

**A5v** (`A5vAt`): the far end of `f k` lies on `X`.

## Results

* `jordan_at_vertex_of_facePot` (the planar core; any rotation system, no matchings): let
  `X = ∂a` for a face function `a` (`FacePot`), and let `d`, `next d`, `next (next d)` be three
  consecutive darts at a vertex with `X`-values `0, 1, 0`. Then the far ends of `d` and of
  `next (next d)` are not joined by a path through vertices that meet no edge of `X`. Proof:
  `a` changes by `X` when the rotation crosses an edge, is constant around an `X`-free vertex
  and across a non-`X` edge. `jordan_at_vertex`: the same for every even `X` on a
  `SphericalMap` (`Fills` gives `a`).
* `xEdges_even`: at a figure-eight state with all vertices but `v` cubic, the edge set of the
  loop `X` is even.
* `a5v_of_facePot` (**A5v from a bounding `X`**; any rotation system, no degree hypothesis):
  if the loop `X` bounds a face set, the far end of `f k` lies on `X`.
* `a5v` (**A5v on the sphere**): on every `SphericalMap`, at every figure-eight state of a
  degree-5 vertex with all other vertices of degree 3, the far end of `f k` lies on `X`.
  No parity clause is needed.
* `a5v_iff_parity` (**the parity form**; any rotation system): if `X` has an even number of
  vertices besides `v` (TrackU's DL clause), then A5v holds iff `|Mt ∩ E(X, Y)|` is odd.
  Pure counting. `a5v_parity`: the parity form on the sphere.
* `T1v`, `NRCMSphere`, `nrcM_sphere_of_T1v`: the abstract conjecture *law + A5v ⇒ no
  R-cycle* (T1-v) as a `Prop` over all finite rotation systems, and the formal plug-in: T1-v
  implies the matching-form NRC on every `SphericalMap` (`chainLaw_of_word1212`: the law is
  automatic for the word `1212…`; `a5v` discharges the axiom).

Companion files: `A5vWitness` (all hypotheses of `a5v` and `a5v_parity` hold on an explicit
8-vertex spherical map, so neither is vacuous) and `A5vNeedsFills` (a twisted wheel: a
non-spherical rotation system where A5v fails; there `X` does not bound and `Fills` fails).

No Jordan curve theorem, region or dual-graph construction is used beyond `Fills`.
-/

@[expose] public section
namespace SimpleGraph.A5v
open Finset

variable {n : ℕ}

/-! ### Part 1. The planar core: Jordan at a vertex from a face potential -/

section jordan
variable {G : SimpleGraph (Fin n)}

variable (G) in
/-- The vertex `u` meets no edge of the edge function `X`. -/
def XFree (X : G.edgeSet → ZMod 2) (u : Fin n) : Prop :=
  ∀ d : G.Dart, d.fst = u → X (RotationSystem.edgeOfDart d) = 0

variable (G) in
/-- The edges of `G` between `X`-free vertices. -/
def freeGraph (X : G.edgeSet → ZMod 2) : SimpleGraph (Fin n) where
  Adj u w := G.Adj u w ∧ XFree G X u ∧ XFree G X w
  symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.2, h.2.1⟩⟩
  loopless := ⟨fun _ h => h.1.ne rfl⟩

/-- `a` is a face potential of `X`: `X = ∂a` (the edge `d` separates the faces of `d` and of
`d.symm`). On a `SphericalMap` every even `X` has one (`Fills`). -/
def FacePot (R : RotationSystem G) (X : G.edgeSet → ZMod 2) (a : R.Face → ZMod 2) : Prop :=
  ∀ d : G.Dart, X (RotationSystem.edgeOfDart d) = a (R.faceOf d) + a (R.faceOf d.symm)

variable {R : RotationSystem G}

lemma zmod2_eq_of_add_eq_zero {x y : ZMod 2} (h : x + y = 0) : x = y :=
  (TutteSides.zmod2_add_eq_zero x y).mp h

/-- Rotation step: from `d` to `next d` the face potential changes by the `X`-value of `d`. -/
lemma face_next_rot {X : G.edgeSet → ZMod 2} {a : R.Face → ZMod 2} (ha : FacePot R X a)
    (d : G.Dart) :
    a (R.faceOf (R.next d)) = a (R.faceOf d) + X (RotationSystem.edgeOfDart d) := by
  have e1 : R.next d = R.faceNext d.symm := by
    rw [RotationSystem.face_next_apply, Dart.symm_symm]
  have e2 : R.faceOf (R.next d) = R.faceOf d.symm := by
    rw [e1]; exact RotationSystem.face_of_face_next _ _
  rw [e2, ha d, ← add_assoc, TutteSides.zmod2_add_self, zero_add]

/-- Across an edge outside `X` the face potential does not change. -/
lemma face_symm_of_zero {X : G.edgeSet → ZMod 2} {a : R.Face → ZMod 2} (ha : FacePot R X a)
    {d : G.Dart} (h : X (RotationSystem.edgeOfDart d) = 0) :
    a (R.faceOf d.symm) = a (R.faceOf d) := by
  have := ha d
  rw [h] at this
  exact (zmod2_eq_of_add_eq_zero this.symm).symm

lemma iterate_next_fst (d : G.Dart) (j : ℕ) :
    ((R.next : G.Dart → G.Dart)^[j] d).fst = d.fst := by
  induction j with
  | zero => rfl
  | succ j ih => rw [Function.iterate_succ_apply', R.next_fst, ih]

/-- Around an `X`-free vertex the face potential is constant. -/
lemma face_const_of_free {X : G.edgeSet → ZMod 2} {a : R.Face → ZMod 2} (ha : FacePot R X a)
    {u : Fin n} (hu : XFree G X u) {d e : G.Dart} (hd : d.fst = u) (he : e.fst = u) :
    a (R.faceOf d) = a (R.faceOf e) := by
  obtain ⟨k, rfl⟩ := R.cyclic d e (hd.trans he.symm)
  clear he
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', face_next_rot ha,
      hu _ ((iterate_next_fst d k).trans hd), add_zero]
    exact ih

/-- Along a path through `X`-free vertices the face potential is constant. -/
lemma face_eq_of_walk {X : G.edgeSet → ZMod 2} {a : R.Face → ZMod 2} (ha : FacePot R X a) :
    ∀ {u w : Fin n} (_p : (freeGraph G X).Walk u w), XFree G X u →
      ∀ {d e : G.Dart}, d.fst = u → e.fst = w → a (R.faceOf d) = a (R.faceOf e) := by
  intro u w p
  induction p with
  | nil => intro hu d e hd he; exact face_const_of_free ha hu hd he
  | @cons x y z h p ih =>
    intro hu d e hd he
    let g : G.Dart := ⟨(x, y), h.1⟩
    calc a (R.faceOf d) = a (R.faceOf g) := face_const_of_free ha hu hd rfl
      _ = a (R.faceOf g.symm) := (face_symm_of_zero ha (hu g rfl)).symm
      _ = a (R.faceOf e) := ih h.2.2 rfl he

/-- **Jordan at a vertex, for a bounding `X`** (any rotation system). Let `X = ∂a` and let
`d, d₁, d₂` be consecutive darts in the rotation at a vertex, with `d, d₂ ∉ X` and `d₁ ∈ X`.
Then the far ends of `d₂` and `d` are not joined by any path through vertices that meet no
edge of `X` (provided the far end of `d₂` meets no edge of `X`). -/
theorem jordan_at_vertex_of_facePot (X : G.edgeSet → ZMod 2) {a : R.Face → ZMod 2}
    (ha : FacePot R X a) {d d₁ d₂ : G.Dart} (e₁ : R.next d = d₁) (e₂ : R.next d₁ = d₂)
    (h₀ : X (RotationSystem.edgeOfDart d) = 0) (h₁ : X (RotationSystem.edgeOfDart d₁) = 1)
    (h₂ : X (RotationSystem.edgeOfDart d₂) = 0) (hfree : XFree G X d₂.snd) :
    ¬ (freeGraph G X).Reachable d₂.snd d.snd := by
  rintro ⟨p⟩
  have r1 := face_next_rot ha d
  have r2 := face_next_rot ha d₁
  rw [e₁] at r1
  rw [e₂] at r2
  have w := face_eq_of_walk ha p hfree (d := d₂.symm) (e := d.symm) rfl rfl
  rw [face_symm_of_zero ha h₂, face_symm_of_zero ha h₀, r2, r1, h₀, h₁, add_zero] at w
  have h10 : (1 : ZMod 2) = 0 := by
    have := congrArg (fun t => t - a (R.faceOf d)) w
    simp at this
  exact absurd h10 (by decide)

/-- **Jordan at a vertex (from `Fills`).** On a spherical map every even `X` bounds, so the
conclusion of `jordan_at_vertex_of_facePot` holds for every even `X`. -/
theorem jordan_at_vertex {M : SphericalMap n} (X : M.graph.edgeSet → ZMod 2)
    (hX : ∀ x, edgeIncidence M.graph X x = 0) {d d₁ d₂ : M.Dart}
    (e₁ : M.rotation.next d = d₁) (e₂ : M.rotation.next d₁ = d₂)
    (h₀ : X (RotationSystem.edgeOfDart d) = 0) (h₁ : X (RotationSystem.edgeOfDart d₁) = 1)
    (h₂ : X (RotationSystem.edgeOfDart d₂) = 0) (hfree : XFree M.graph X d₂.snd) :
    ¬ (freeGraph M.graph X).Reachable d₂.snd d.snd := by
  obtain ⟨a, ha⟩ := M.fills X hX
  exact jordan_at_vertex_of_facePot (R := M.rotation) X ha e₁ e₂ h₀ h₁ h₂ hfree

end jordan

/-! ### Part 2. Matching-form vocabulary (any rotation system, no planarity) -/

section vocab
variable {G : SimpleGraph (Fin n)}

variable (R : RotationSystem G) in
/-- A degree-5 vertex `v` with its five darts `f 0, …, f 4` in rotation order. -/
structure Hole5 where
  v : Fin n
  f : Fin 5 → G.Dart
  fst_f : ∀ i, (f i).fst = v
  next_f : ∀ i, R.next (f i) = f (i + 1)
  inj : Function.Injective f

variable (G) in
/-- `Mt` is a perfect matching of `G`. -/
structure IsPerfectMatching (Mt : SimpleGraph (Fin n)) : Prop where
  le : Mt ≤ G
  unique : ∀ u, ∃! w, Mt.Adj u w

variable (G) in
/-- `E − Mt` with the vertex `v` deleted. At a figure-eight state its two components are the
interiors of the loops `X` and `Y`. -/
def qGraph (Mt : SimpleGraph (Fin n)) (v : Fin n) : SimpleGraph (Fin n) where
  Adj a b := G.Adj a b ∧ ¬ Mt.Adj a b ∧ a ≠ v ∧ b ≠ v
  symm := ⟨fun _ _ h => ⟨h.1.symm, fun h' => h.2.1 h'.symm, h.2.2.2, h.2.2.1⟩⟩
  loopless := ⟨fun _ h => h.1.ne rfl⟩

variable {R : RotationSystem G}

/-- The cubic-except-`v` hypothesis. -/
def CubicOff [DecidableRel G.Adj] (H : Hole5 R) : Prop := ∀ u, u ≠ H.v → G.degree u = 3

/-- `u` is an interior vertex of the loop `X` (through `f (k−1)`, `f (k+1)`). -/
def InX (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) (u : Fin n) : Prop :=
  (qGraph G Mt H.v).Reachable (H.f (k + 1)).snd u

/-- `u` is an interior vertex of the loop `Y` (through `f (k+2)`, `f (k−2)`). -/
def InY (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) (u : Fin n) : Prop :=
  (qGraph G Mt H.v).Reachable (H.f (k + 2)).snd u

/-- **The DL figure-eight at frame `k`** (TrackU's `dl`, without its parity clause):
`f k ∈ Mt`, the loop through `f (k+1)` returns through `f (k−1)`, the loop through `f (k+2)`
returns through `f (k−2) = f (k+3)`, the two loops are different, and every vertex other
than `v` lies on one of them (`E − Mt` connected). -/
structure Fig8 (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) : Prop where
  mk_adj : Mt.Adj H.v (H.f k).snd
  pairX : (qGraph G Mt H.v).Reachable (H.f (k + 1)).snd (H.f (k - 1)).snd
  pairY : (qGraph G Mt H.v).Reachable (H.f (k + 2)).snd (H.f (k + 3)).snd
  sepXY : ¬ (qGraph G Mt H.v).Reachable (H.f (k + 1)).snd (H.f (k + 2)).snd
  cover : ∀ u, u ≠ H.v → InX H Mt k u ∨ InY H Mt k u

/-- **Axiom A5v at a state**: the far end of `f k` (the `Mt`-partner of `v`) lies on `X`. -/
def A5vAt (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) : Prop :=
  InX H Mt k (H.f k).snd

open Classical in
/-- The `X`-vertices (other than `v`). -/
noncomputable def xVerts (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) : Finset (Fin n) :=
  univ.filter (fun u => u ≠ H.v ∧ InX H Mt k u)

open Classical in
/-- `|Mt ∩ E(X, Y)|`, counted at the `X`-ends: the `X`-vertices whose `Mt`-partner is a
`Y`-vertex. -/
noncomputable def crossXY (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) : ℕ :=
  #((xVerts H Mt k).filter (fun u => ∃ y, Mt.Adj u y ∧ y ≠ H.v ∧ InY H Mt k y))

/-- TrackU's DL parity clause: `X` has an even number of vertices besides `v`. -/
def XEven (H : Hole5 R) (Mt : SimpleGraph (Fin n)) (k : Fin 5) : Prop :=
  Even #(xVerts H Mt k)

end vocab

/-! ### Part 3. A5v: from a bounding `X` (any rotation system), and on the sphere -/

section a5v
variable {G : SimpleGraph (Fin n)} {R : RotationSystem G} (H : Hole5 R) {Mt : SimpleGraph (Fin n)}
  {k : Fin 5}

/-- Index arithmetic in `Fin 5`. -/
lemma fin5_facts : ∀ k : Fin 5, k + 1 ≠ k ∧ k + 2 ≠ k ∧ k + 1 + 1 = k + 2 ∧ k + 4 = k - 1 ∧
    k + 3 ≠ k ∧ k + 4 ≠ k := by decide

lemma f_snd_ne (i : Fin 5) : (H.f i).snd ≠ H.v := by
  intro h
  exact (H.f i).adj.ne ((H.fst_f i).trans h.symm)

lemma f_eq_of_snd {i j : Fin 5} (h : (H.f i).snd = (H.f j).snd) : i = j := by
  exact H.inj (Dart.ext _ _ (Prod.ext ((H.fst_f i).trans (H.fst_f j).symm) h))

lemma iterate_next_f (i : Fin 5) (m : ℕ) :
    ∃ j, ((R.next : G.Dart → G.Dart)^[m] (H.f i)) = H.f j := by
  induction m with
  | zero => exact ⟨i, rfl⟩
  | succ m ih =>
    obtain ⟨j, hj⟩ := ih
    exact ⟨j + 1, by rw [Function.iterate_succ_apply', hj, H.next_f]⟩

/-- Every dart at `v` is one of the `f i`. -/
lemma dart_at_v {d : G.Dart} (hd : d.fst = H.v) : ∃ i, H.f i = d := by
  obtain ⟨m, hm⟩ := R.cyclic (H.f 0) d ((H.fst_f 0).trans hd.symm)
  obtain ⟨j, hj⟩ := iterate_next_f H 0 m
  exact ⟨j, hj.symm.trans hm⟩

/-- Only `f k` carries the matching edge at `v`. -/
lemma not_mt_f (hF : Fig8 H Mt k) (hM : IsPerfectMatching G Mt) {i : Fin 5} (hi : i ≠ k) :
    ¬ Mt.Adj H.v (H.f i).snd := by
  intro h
  obtain ⟨w, -, hw⟩ := hM.unique H.v
  have e1 := hw _ h
  have e2 := hw _ hF.mk_adj
  exact hi (f_eq_of_snd H (e1.trans e2.symm))

variable (Mt k) in
/-- The `X`-indicator on darts: a non-matching edge with an end on `X` (off `v`). -/
noncomputable def xDart (d : G.Dart) : ZMod 2 := by
  classical
  exact if ¬ Mt.Adj d.fst d.snd ∧
      ((d.fst ≠ H.v ∧ InX H Mt k d.fst) ∨ (d.snd ≠ H.v ∧ InX H Mt k d.snd)) then 1 else 0

lemma xDart_symm (d : G.Dart) : xDart H Mt k d.symm = xDart H Mt k d := by
  have key : (¬ Mt.Adj d.symm.fst d.symm.snd ∧ ((d.symm.fst ≠ H.v ∧ InX H Mt k d.symm.fst) ∨
      (d.symm.snd ≠ H.v ∧ InX H Mt k d.symm.snd))) ↔ (¬ Mt.Adj d.fst d.snd ∧
      ((d.fst ≠ H.v ∧ InX H Mt k d.fst) ∨ (d.snd ≠ H.v ∧ InX H Mt k d.snd))) := by
    constructor
    · rintro ⟨h1, h2⟩; exact ⟨fun h => h1 h.symm, h2.symm⟩
    · rintro ⟨h1, h2⟩; exact ⟨fun h => h1 h.symm, h2.symm⟩
  unfold xDart
  split_ifs with h1 h2 h2
  · rfl
  · exact absurd (key.mp h1) h2
  · exact absurd (key.mpr h2) h1
  · rfl

variable (Mt k) in
/-- The edge set of the loop `X` (as a `ZMod 2` edge function). -/
noncomputable def xEdges : G.edgeSet → ZMod 2 :=
  fun e => xDart H Mt k (SphericalMap.edgeDart G e)

lemma xEdges_dart (d : G.Dart) :
    xEdges H Mt k (RotationSystem.edgeOfDart d) = xDart H Mt k d := by
  unfold xEdges
  rcases (RotationSystem.edge_of_dart_eq_iff _ _).mp
      (SphericalMap.edgeDart_spec G (RotationSystem.edgeOfDart d)) with h | h
  · rw [h]
  · rw [h, xDart_symm]

/-- An `X`-indicator value of `0` from the absence of `X`-ends. -/
lemma xDart_eq_zero {d : G.Dart}
    (h : Mt.Adj d.fst d.snd ∨
      ((d.fst = H.v ∨ ¬ InX H Mt k d.fst) ∧ (d.snd = H.v ∨ ¬ InX H Mt k d.snd))) :
    xDart H Mt k d = 0 := by
  unfold xDart
  split_ifs with hc
  · exfalso
    obtain ⟨h1, h2⟩ := hc
    rcases h with h | ⟨ha, hb⟩
    · exact h1 h
    · rcases h2 with ⟨h2, h3⟩ | ⟨h2, h3⟩
      · rcases ha with ha | ha
        · exact h2 ha
        · exact ha h3
      · rcases hb with hb | hb
        · exact h2 hb
        · exact hb h3
  · rfl

/-- The value `1` at a non-matching spoke into `X`. -/
lemma xDart_f_one {i : Fin 5} (hm : ¬ Mt.Adj H.v (H.f i).snd) (hx : InX H Mt k (H.f i).snd) :
    xDart H Mt k (H.f i) = 1 := by
  unfold xDart
  split_ifs with hc
  · rfl
  · exact absurd ⟨(H.fst_f i).symm ▸ hm, Or.inr ⟨f_snd_ne H i, hx⟩⟩ hc

/-- The value `0` at a spoke not into `X`. -/
lemma xDart_f_zero {i : Fin 5} (hx : ¬ InX H Mt k (H.f i).snd) : xDart H Mt k (H.f i) = 0 :=
  xDart_eq_zero H (Or.inr ⟨Or.inl (H.fst_f i), Or.inr hx⟩)

open Classical in
/-- At an `X`-vertex the `X`-indicator is the non-matching indicator. -/
lemma xDart_at_X {d : G.Dart} (hv : d.fst ≠ H.v) (hx : InX H Mt k d.fst) :
    xDart H Mt k d = if ¬ Mt.Adj d.fst d.snd then 1 else 0 := by
  unfold xDart
  by_cases hm : Mt.Adj d.fst d.snd
  · rw [ite_eq_right (fun h => h.1 hm), ite_eq_right (not_not.mpr hm)]
  · rw [ite_eq_left ⟨hm, Or.inl ⟨hv, hx⟩⟩, ite_eq_left hm]

/-- A vertex off `v` and off `X` meets no edge of `X`. -/
lemma xFree_of_not_inX {u : Fin n} (hu : u ≠ H.v) (hx : ¬ InX H Mt k u) :
    XFree G (xEdges H Mt k) u := by
  intro d hd
  rw [xEdges_dart]
  apply xDart_eq_zero
  by_cases hm : Mt.Adj d.fst d.snd
  · exact Or.inl hm
  · refine Or.inr ⟨Or.inr (hd ▸ hx), ?_⟩
    by_cases hv : d.snd = H.v
    · exact Or.inl hv
    · refine Or.inr fun hy => hx ?_
      have hq : (qGraph G Mt H.v).Adj d.snd u :=
        ⟨hd ▸ d.adj.symm, fun h => hm (hd ▸ h.symm), hv, hu⟩
      exact hy.trans hq.reachable

/-- **`X` is an even edge set.** -/
theorem xEdges_even [DecidableRel G.Adj] (hF : Fig8 H Mt k) (hM : IsPerfectMatching G Mt) (hc : CubicOff H) :
    ∀ x, edgeIncidence G (xEdges H Mt k) x = 0 := by
  classical
  intro x
  have hsum : edgeIncidence G (xEdges H Mt k) x =
      ∑ d : G.Dart, (if d.fst = x then xDart H Mt k d else 0) := by
    have h1 := TutteSides.sum_edges_at (G := G) (xEdges H Mt k) x
    simp only [xEdges_dart] at h1
    unfold edgeIncidence
    rw [← h1]
    congr
    exact Subsingleton.elim _ _
  rw [hsum]
  by_cases hxv : x = H.v
  · -- the five spokes at `v`: values `0, 1, 0, 0, 1` from `f k`
    subst hxv
    rw [← Finset.sum_filter]
    have himg : univ.filter (fun d : G.Dart => d.fst = H.v) = univ.image H.f := by
      ext d
      simp only [mem_filter, mem_univ, true_and, mem_image]
      exact ⟨fun hd => dart_at_v H hd, fun ⟨i, hi⟩ => hi ▸ H.fst_f i⟩
    rw [himg, Finset.sum_image (fun i _ j _ h => H.inj h)]
    rw [← Fintype.sum_equiv (Equiv.addLeft k) (fun i => xDart H Mt k (H.f (k + i)))
      (fun i => xDart H Mt k (H.f i)) (fun _ => rfl)]
    simp only [Fin.sum_univ_five, add_zero]
    obtain ⟨hk1, hk2, -, e4, hk3, hk4⟩ := fin5_facts k
    have hX3 : ¬ InX H Mt k (H.f (k + 3)).snd := fun h => hF.sepXY (h.trans hF.pairY.symm)
    rw [xDart_eq_zero H (Or.inl ((H.fst_f k).symm ▸ hF.mk_adj)),
      xDart_f_one H (not_mt_f H hF hM hk1) (Reachable.refl _),
      xDart_f_zero H hF.sepXY, xDart_f_zero H hX3,
      xDart_f_one H (not_mt_f H hF hM hk4) (e4 ▸ hF.pairX)]
    decide
  by_cases hxX : InX H Mt k x
  · -- an `X`-vertex: two non-matching darts
    have hpt : ∀ d : G.Dart, (if d.fst = x then xDart H Mt k d else 0) =
        if d.fst = x ∧ ¬ Mt.Adj d.fst d.snd then 1 else 0 := by
      intro d
      by_cases hd : d.fst = x
      · rw [ite_eq_left hd, xDart_at_X H (hd ▸ hxv) (hd ▸ hxX)]
        by_cases hm : Mt.Adj d.fst d.snd
        · rw [ite_eq_right (not_not.mpr hm), ite_eq_right (fun h => h.2 hm)]
        · rw [ite_eq_left hm, ite_eq_left ⟨hd, hm⟩]
      · rw [ite_eq_right hd, ite_eq_right (fun h => hd h.1)]
    rw [Finset.sum_congr rfl (fun d _ => hpt d), Finset.sum_boole]
    obtain ⟨w, hw, hwu⟩ := hM.unique x
    have hdeg : #(univ.filter (fun d : G.Dart => d.fst = x)) = 3 := by
      rw [G.dart_fst_fiber_card_eq_degree x]; exact hc x hxv
    have hone : #((univ.filter (fun d : G.Dart => d.fst = x)).filter
        (fun d => Mt.Adj d.fst d.snd)) = 1 := by
      rw [Finset.card_eq_one]
      refine ⟨⟨(x, w), hM.le hw⟩, ?_⟩
      ext d
      simp only [mem_filter, mem_univ, true_and, mem_singleton]
      constructor
      · rintro ⟨hd, hm⟩
        have : d.snd = w := hwu _ (hd ▸ hm)
        exact Dart.ext _ _ (Prod.ext hd this)
      · rintro rfl
        exact ⟨rfl, hw⟩
    have htwo := Finset.card_filter_add_card_filter_not
      (s := univ.filter (fun d : G.Dart => d.fst = x)) (fun d : G.Dart => Mt.Adj d.fst d.snd)
    rw [hone, hdeg, Finset.filter_filter] at htwo
    have h2 : #(univ.filter (fun d : G.Dart => d.fst = x ∧ ¬ Mt.Adj d.fst d.snd)) = 2 := by
      omega
    rw [h2]
    rfl
  · -- off `X`: no `X`-edges
    refine Finset.sum_eq_zero fun d _ => ?_
    by_cases hd : d.fst = x
    · rw [ite_eq_left hd, ← xEdges_dart]
      exact xFree_of_not_inX H hxv hxX d hd
    · rw [ite_eq_right hd]

/-- The `Y`-side path, transported into the `X`-free graph. -/
lemma free_reach_of_q :
    ∀ {a b : Fin n} (_q : (qGraph G Mt H.v).Walk a b), a ≠ H.v → ¬ InX H Mt k a →
      (freeGraph G (xEdges H Mt k)).Reachable a b := by
  intro a b q
  induction q with
  | nil => intro _ _; exact Reachable.refl _
  | @cons a c b h q ih =>
    intro ha hx
    have hc : ¬ InX H Mt k c := fun hc => hx (hc.trans h.symm.reachable)
    have hadj : (freeGraph G (xEdges H Mt k)).Adj a c :=
      ⟨h.1, xFree_of_not_inX H ha hx, xFree_of_not_inX H h.2.2.2 hc⟩
    exact hadj.reachable.trans (ih h.2.2.2 hc)

/-- **A5v from a bounding `X`** (any rotation system, no degree hypothesis). At a DL
figure-eight state, if the loop `X` is the boundary of a face set (`FacePot`), then the
`Mt`-partner of `v` lies on `X`. -/
theorem a5v_of_facePot (hM : IsPerfectMatching G Mt) (hF : Fig8 H Mt k) {a : R.Face → ZMod 2}
    (ha : FacePot R (xEdges H Mt k) a) : A5vAt H Mt k := by
  by_contra hw
  obtain ⟨hk1, -, e12, -⟩ := fin5_facts k
  have hk : xDart H Mt k (H.f k) = 0 := xDart_eq_zero H (Or.inl ((H.fst_f k).symm ▸ hF.mk_adj))
  have hk1x : xDart H Mt k (H.f (k + 1)) = 1 :=
    xDart_f_one H (not_mt_f H hF hM hk1) (Reachable.refl _)
  have hnotX2 : ¬ InX H Mt k (H.f (k + 2)).snd := hF.sepXY
  have hk2x : xDart H Mt k (H.f (k + 2)) = 0 :=
    xDart_eq_zero H (Or.inr ⟨Or.inl (H.fst_f _), Or.inr hnotX2⟩)
  have hY : InY H Mt k (H.f k).snd := (hF.cover _ (f_snd_ne H k)).resolve_left hw
  have J := jordan_at_vertex_of_facePot (xEdges H Mt k) ha
    (H.next_f k) ((H.next_f (k + 1)).trans (congrArg H.f e12))
    (by rw [xEdges_dart]; exact hk) (by rw [xEdges_dart]; exact hk1x)
    (by rw [xEdges_dart]; exact hk2x) (xFree_of_not_inX H (f_snd_ne H _) hnotX2)
  obtain ⟨q⟩ := hY
  exact J (free_reach_of_q H q (f_snd_ne H _) hnotX2)

end a5v

/-- **A5v on the sphere.** On every spherical map, at every DL figure-eight state of a
degree-5 vertex `v` with all other vertices cubic, the `Mt`-partner of `v` lies on `X`.
(`Fills` supplies the face potential of the even edge set `X`.) -/
theorem a5v {M : SphericalMap n} (H : Hole5 M.rotation) {Mt : SimpleGraph (Fin n)} {k : Fin 5}
    (hM : IsPerfectMatching M.graph Mt) (hc : CubicOff H) (hF : Fig8 H Mt k) :
    A5vAt H Mt k := by
  obtain ⟨a, ha⟩ := M.fills _ (xEdges_even H hF hM hc)
  exact a5v_of_facePot H hM hF ha

/-- The far end of a spoke is not `v` (any rotation system). -/
lemma f_snd_ne' {G : SimpleGraph (Fin n)} {R : RotationSystem G} (H : Hole5 R) (i : Fin 5) :
    (H.f i).snd ≠ H.v := fun h => (H.f i).adj.ne ((H.fst_f i).trans h.symm)

/-! ### Part 4. The parity form (pure counting, any rotation system) -/

section parity
variable {G : SimpleGraph (Fin n)} {R : RotationSystem G} (H : Hole5 R)
  {Mt : SimpleGraph (Fin n)} {k : Fin 5}

/-- The `Mt`-partner of a vertex. -/
noncomputable def partner (hM : IsPerfectMatching G Mt) (u : Fin n) : Fin n :=
  Classical.choose (hM.unique u).exists

lemma partner_adj (hM : IsPerfectMatching G Mt) (u : Fin n) : Mt.Adj u (partner hM u) :=
  Classical.choose_spec (hM.unique u).exists

lemma eq_partner (hM : IsPerfectMatching G Mt) {u y : Fin n} (h : Mt.Adj u y) :
    y = partner hM u :=
  (hM.unique u).unique h (partner_adj hM u)

/-- **The parity form of A5v.** At a DL figure-eight state whose loop `X` has an even number
of vertices besides `v`, the partner of `v` lies on `X` iff `|Mt ∩ E(X, Y)|` is odd.
(No planarity: the `X`-vertices are matched to `v`, to `X` in pairs, or to `Y`.) -/
theorem a5v_iff_parity (hM : IsPerfectMatching G Mt) (hF : Fig8 H Mt k) (hE : XEven H Mt k) :
    A5vAt H Mt k ↔ Odd (crossXY H Mt k) := by
  classical
  have hXY : ∀ y, InX H Mt k y → InY H Mt k y → False :=
    fun y hx hy => hF.sepXY (hx.trans hy.symm)
  set S := xVerts H Mt k with hSdef
  let p := partner hM
  let PV : Fin n → Prop := fun u => p u = H.v
  let PX : Fin n → Prop := fun u => p u ≠ H.v ∧ InX H Mt k (p u)
  let PY : Fin n → Prop := fun u => ∃ y, Mt.Adj u y ∧ y ≠ H.v ∧ InY H Mt k y
  have hPY : ∀ u, PY u ↔ p u ≠ H.v ∧ InY H Mt k (p u) := by
    intro u
    constructor
    · rintro ⟨y, hy, hyv, hyY⟩
      have e : p u = y := (eq_partner hM hy).symm
      rw [e]
      exact ⟨hyv, hyY⟩
    · intro h
      exact ⟨p u, partner_adj hM u, h⟩
  -- every `X`-vertex is in exactly one class
  have hpt : ∀ u ∈ S, (1 : ZMod 2) =
      ((if PV u then 1 else 0) + (if PX u then 1 else 0)) + (if PY u then 1 else 0) := by
    intro u _
    by_cases hv : p u = H.v
    · have h1 : ¬ PX u := fun h => h.1 hv
      have h2 : ¬ PY u := fun h => ((hPY u).mp h).1 hv
      rw [ite_eq_left (show PV u from hv), ite_eq_right h1, ite_eq_right h2]
      rfl
    · rcases hF.cover (p u) hv with hx | hy
      · have h2 : ¬ PY u := fun h => hXY _ hx ((hPY u).mp h).2
        rw [ite_eq_right (show ¬ PV u from hv), ite_eq_left (show PX u from ⟨hv, hx⟩),
          ite_eq_right h2]
        rfl
      · have h1 : ¬ PX u := fun h => hXY _ h.2 hy
        rw [ite_eq_right (show ¬ PV u from hv), ite_eq_right h1,
          ite_eq_left ((hPY u).mpr ⟨hv, hy⟩)]
        rfl
  have hsum : ((#S : ℕ) : ZMod 2) =
      ((#(S.filter PV) : ℕ) : ZMod 2) + ((#(S.filter PX) : ℕ) : ZMod 2) +
        ((#(S.filter PY) : ℕ) : ZMod 2) := by
    rw [Finset.card_eq_sum_ones, Nat.cast_sum, Nat.cast_one, Finset.sum_congr rfl hpt,
      Finset.sum_add_distrib, Finset.sum_add_distrib, Finset.sum_boole, Finset.sum_boole,
      Finset.sum_boole]
  have hS : ((#S : ℕ) : ZMod 2) = 0 := ZMod.natCast_eq_zero_iff_even.mpr hE
  -- `X`-vertices matched inside `X` come in pairs
  have hX : ((#(S.filter PX) : ℕ) : ZMod 2) = 0 := by
    rw [Finset.card_eq_sum_ones, Nat.cast_sum, Nat.cast_one]
    refine Finset.sum_involution (fun u _ => p u) (fun _ _ => rfl) ?_ ?_ ?_
    · intro u _ _ h
      have hadj := partner_adj hM u
      rw [show partner hM u = u from h] at hadj
      exact hadj.ne rfl
    · intro u hu
      obtain ⟨hu1, hu2⟩ := Finset.mem_filter.mp hu
      obtain ⟨hpv, hpx⟩ := hu2
      have hpp : p (p u) = u := (eq_partner hM (partner_adj hM u).symm).symm
      have huS := Finset.mem_filter.mp hu1
      refine Finset.mem_filter.mpr ⟨Finset.mem_filter.mpr ⟨Finset.mem_univ _, hpv, hpx⟩, ?_⟩
      show p (p u) ≠ H.v ∧ InX H Mt k (p (p u))
      rw [hpp]
      exact huS.2
    · intro u _
      exact (eq_partner hM (partner_adj hM u).symm).symm
  -- the only vertex matched to `v` is the far end of `f k`
  have hV : ((#(S.filter PV) : ℕ) : ZMod 2) = if A5vAt H Mt k then 1 else 0 := by
    have hw : ∀ u, PV u ↔ u = (H.f k).snd := by
      intro u
      constructor
      · intro h
        have h1 : Mt.Adj H.v u := by
          have := partner_adj hM u
          rw [show partner hM u = H.v from h] at this
          exact this.symm
        obtain ⟨w, -, hw⟩ := hM.unique H.v
        exact (hw _ h1).trans (hw _ hF.mk_adj).symm
      · rintro rfl
        exact (eq_partner hM hF.mk_adj.symm).symm
    have hfilt : S.filter PV = if A5vAt H Mt k then {(H.f k).snd} else ∅ := by
      ext u
      rw [Finset.mem_filter, hw u]
      split_ifs with ha
      · rw [Finset.mem_singleton]
        constructor
        · exact fun h => h.2
        · rintro rfl
          exact ⟨Finset.mem_filter.mpr ⟨Finset.mem_univ _, f_snd_ne' H k, ha⟩, rfl⟩
      · simp only [Finset.notMem_empty, iff_false, not_and]
        rintro hu rfl
        exact ha (Finset.mem_filter.mp hu).2.2
    rw [hfilt]
    split_ifs <;> rfl
  have hC : crossXY H Mt k = #(S.filter PY) := rfl
  rw [hS, hV, hX, add_zero] at hsum
  rw [hC, ← ZMod.natCast_eq_one_iff_odd]
  have key1 : ∀ x : ZMod 2, 0 = 1 + x → x = 1 := by decide
  have key0 : ∀ x : ZMod 2, 0 = 0 + x → x ≠ 1 := by decide
  by_cases ha : A5vAt H Mt k
  · rw [ite_eq_left ha] at hsum
    exact ⟨fun _ => key1 _ hsum, fun _ => ha⟩
  · rw [ite_eq_right ha] at hsum
    exact ⟨fun h => absurd h ha, fun h => absurd h (key0 _ hsum)⟩

end parity

/-- **A5v on the sphere, parity form**: `|Mt ∩ E(X, Y)|` is odd at every DL state. -/
theorem a5v_parity {M : SphericalMap n} (H : Hole5 M.rotation) {Mt : SimpleGraph (Fin n)}
    {k : Fin 5} (hM : IsPerfectMatching M.graph Mt) (hc : CubicOff H) (hF : Fig8 H Mt k)
    (hE : XEven H Mt k) : Odd (crossXY H Mt k) :=
  (a5v_iff_parity H hM hF hE).mp (a5v H hM hc hF)

/-! ### Part 5. Orbits, the R-word, and the plug-in point for T1-v -/

section orbits
variable {G : SimpleGraph (Fin n)} {R : RotationSystem G}

/-- TrackU's `k(H)`: the number of components of `A ∪ B` (all vertices kept). -/
noncomputable def kH (A B : SimpleGraph (Fin n)) : ℕ := Nat.card (A ⊔ B).ConnectedComponent

/-- **A closed orbit of DL-good states** (TrackU's dynamics, README R1/R4): period `L > 0`;
every state is a perfect matching at a DL figure-eight of frame `k t` with the parity clause;
consecutive states share no edge; and the successor contains `f (k − 2) = f (k + 3)`. -/
structure DLOrbit (H : Hole5 R) (S : ℕ → SimpleGraph (Fin n)) (k : ℕ → Fin 5) (L : ℕ) :
    Prop where
  pos : 0 < L
  periodic : ∀ t, S (t + L) = S t
  perfect : ∀ t, IsPerfectMatching G (S t)
  fig8 : ∀ t, Fig8 H (S t) (k t)
  xeven : ∀ t, XEven H (S t) (k t)
  disj : ∀ t, Disjoint (S t) (S (t + 1))
  succ : ∀ t, (S (t + 1)).Adj H.v (H.f (k t + 3)).snd

/-- The R-word `1212…`: `k(M_t ∪ M_{t+1})` alternates between `1` (Hamiltonian) and `2`. -/
def Word1212 (S : ℕ → SimpleGraph (Fin n)) : Prop :=
  ∃ p : ℕ, ∀ t, kH (S t) (S (t + 1)) = if Even (t + p) then 1 else 2

/-- The chain-parity law in matching form: consecutive words have opposite parity. -/
def ChainLaw (S : ℕ → SimpleGraph (Fin n)) : Prop :=
  ∀ t, Odd (kH (S t) (S (t + 1)) + kH (S (t + 1)) (S (t + 2)))

/-- For the word `1212…` the law holds automatically. -/
lemma chainLaw_of_word1212 {S : ℕ → SimpleGraph (Fin n)} (h : Word1212 S) : ChainLaw S := by
  obtain ⟨p, hp⟩ := h
  intro t
  rw [hp t, hp (t + 1), show t + 1 + p = t + p + 1 by omega]
  by_cases he : Even (t + p)
  · rw [ite_eq_left he, ite_eq_right (Nat.not_even_iff_odd.mpr he.add_one)]
    decide
  · rw [ite_eq_right he, ite_eq_left (Nat.not_even_iff_odd.mp he).add_one]
    decide

/-- **Conjecture T1-v** (law + A5v ⇒ no R-cycle; README Run 2, R4), over all finite rotation
systems, with no planarity: no closed DL orbit that satisfies the chain-parity law and A5v at
every state has the word `1212…`. Exhaustively true for `n ≤ 22` (SAT, not certified); open. -/
def T1v : Prop :=
  ∀ (n : ℕ) (G : SimpleGraph (Fin n)) [DecidableRel G.Adj] (R : RotationSystem G)
    (H : Hole5 R) (S : ℕ → SimpleGraph (Fin n)) (k : ℕ → Fin 5) (L : ℕ),
    CubicOff H → DLOrbit H S k L → ChainLaw S → (∀ t, A5vAt H (S t) (k t)) → ¬ Word1212 S

/-- **NRC-M on the sphere** (matching form): on every spherical map, cubic except one degree-5
vertex, no closed DL orbit has the word `1212…`. -/
def NRCMSphere : Prop :=
  ∀ (n : ℕ) (M : SphericalMap n) (H : Hole5 M.rotation) (S : ℕ → SimpleGraph (Fin n))
    (k : ℕ → Fin 5) (L : ℕ), CubicOff H → DLOrbit H S k L → ¬ Word1212 S

/-- **The plug-in theorem.** A proof of T1-v (for abstract graphs) gives NRC-M on the sphere:
the chain-parity law is automatic for the word `1212…`, and A5v holds at every state of every
spherical map (`a5v`). -/
theorem nrcM_sphere_of_T1v (h : T1v) : NRCMSphere := by
  intro n M H S k L hc hO hW
  exact h n M.graph M.rotation H S k L hc hO (chainLaw_of_word1212 hW)
    (fun t => a5v H (hO.perfect t) hc (hO.fig8 t)) hW

end orbits

end SimpleGraph.A5v

#print axioms SimpleGraph.A5v.jordan_at_vertex_of_facePot
#print axioms SimpleGraph.A5v.jordan_at_vertex
#print axioms SimpleGraph.A5v.a5v_of_facePot
#print axioms SimpleGraph.A5v.a5v
#print axioms SimpleGraph.A5v.a5v_iff_parity
#print axioms SimpleGraph.A5v.a5v_parity
#print axioms SimpleGraph.A5v.chainLaw_of_word1212
#print axioms SimpleGraph.A5v.nrcM_sphere_of_T1v
