/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLockParity
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterTait
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TutteSides

/-!
# The primal dictionary for A5v (bridge to the Quarter modules)

Long Table draft, 13 Oct 2026, written after the scope note `axioms/scope/SCOPE-A5v.md`
(commit `359c937c`): in primal form A5v is `¬inA`, i.e. `x j ∉ K_{αA}(x (j+2))`, and its
Tait/matching form follows by a local argument at the triangles (Lemma F).

Setting: `M : SphericalMap n` is the triangulation `T`, `h` a degree-5 hole with link
`P : Pent M.graph h`, `c` a colouring proper off `h`, and the state is unfilled with repeat
frame `j`: link colours `(α, μ, α, A, B)` at `x j, …, x (j+4)`. The Tait dual `G` of `T − h` has
the triangles of `T − h` as cubic vertices and the pentagon as `v`. Its edges are the edges of
`T − h`; the spoke `s i` is the link edge `x i x (i+1)`. Everything below is stated in primal
coordinates. **The dual graph itself is not constructed** (the library has none), so the
matching-form objects appear as primal edge predicates:

* `tM` (the colour-2 matching `Mt`): edges of `T − h` of Tait colour `γ₂ = α + A = μ + B`,
  i.e. inside the `{α, A}` or the `{μ, B}` class (`tM_iff`, from `tait_cross_iff`);
* `K = K_{αA}(x (j+2))`, `K' = K_{αA}(x j)`, `L = K_{μB}(x (j+1))` (Kempe chains, `pairGraph`);
* `tX` = edges between `K` and `L`, `tY` = edges between `K'` and `L` (the loops `X`, `Y`).

## Results (no `sorry`)

* `mSpoke`, `not_tM_spoke`: `v`'s matching edge is the spoke `x (j+2) x (j+3)`; the other
  four spokes are not in `tM`.
* `xSpokes`, `ySpokes` (at a `Lock2` state): the spokes `x (j+1) x (j+2)` and `x (j+3) x (j+4)`
  are `X`-edges; `x (j+4) x j` and `x j x (j+1)` are `Y`-edges. This is the pairing of the
  matching-form figure-eight: `X` through `f (k±1)`, `Y` through `f (k±2)`.
* `notInA` (**¬inA from `Lock2`**): the existing formal Kempe duality D2
  (`not_reach_alpha_A_of_lock2`, `NoFrozen.lean`, sphere) gives `x j ∉ K`.
* `tX_tY_disjoint`: given `¬inA`, no edge is both an `X`- and a `Y`-edge.
* `q_edge_cover` (the figure-eight dictionary): if `K, K', L` are the only chains of the
  `{α, A} | {μ, B}` partition (`ThreeChains`, the primal form of "`E − Mt` is a connected
  figure-eight"), every edge of `T − h` outside `tM` is an `X`- or a `Y`-edge.
* `triangle_step` (**Lemma F, local step**): at every triangle of `T − h` with an `X`-edge,
  the other two edges are one `X`-edge and one `tM`-edge (same for `Y`). So the dual walk
  along `E − Mt` that starts on an `X`-edge stays on `X`-edges: the dual loop `X` is contained
  in `E(K, L)`.
* `a5v_primal` (**A5v, primal form**): at a doubly locked state with `ThreeChains`, both
  non-matching edges of the far triangle of `v`'s matching spoke are `X`-edges and not
  `Y`-edges. `y_far_iff_inA`: such an edge is a `Y`-edge iff `inA` holds, so in primal
  coordinates A5v is exactly `¬inA`.

## The remaining gap to the matching form

To instantiate `A5vJordan` (or a future T1-v proof) on real states one needs the Tait dual as
a `RotationSystem` on `Fin N` and the identification of `Hole5`, `Mt`, `Fig8` with the primal
objects above. Given that, `a5v_of_facePot` needs only a face potential of `X`, and the
indicator of `K` (a set of primal vertices = dual faces) is one: `∂ 1_K = δ(K) = E(K, L)`
under `ThreeChains`. No dual `Fills`, Euler or Jordan input is needed for that step; the
planar input is `¬inA`, i.e. D2.
-/

@[expose] public section
namespace SimpleGraph.A5vBridge
open QuarterFloor VacancySlide VacancyShortFill

variable {n : ℕ} {M : SphericalMap n} {h : Fin n} (P : Pent M.graph h) (c : Fin n → Fin 4)
  (j : Fin 5)

/-! ### The dictionary -/

/-- The chain `K = K_{αA}(x (j+2))`. -/
def InK (u : Fin n) : Prop :=
  (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) u

/-- The chain `K' = K_{αA}(x j)`. -/
def InK' (u : Fin n) : Prop :=
  (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x j) u

/-- The chain `L = K_{μB}(x (j+1))`. -/
def InL (u : Fin n) : Prop :=
  (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1)) u

/-- `inA`: `x j` lies in `K` (Lemma H0's dichotomy; false at every `Lock2` state). -/
def InA : Prop := InK P c j (P.x j)

/-- The colour-2 matching `Mt` of the Tait dual, as primal edges: Tait colour `α + A`. -/
def tM (u w : Fin n) : Prop :=
  M.graph.Adj u w ∧ u ≠ h ∧ w ≠ h ∧ tait c u w = enc (c (P.x j)) + enc (c (P.x (j + 3)))

/-- The loop `X`, as primal edges: between `K` and `L`. -/
def tX (u w : Fin n) : Prop :=
  M.graph.Adj u w ∧ ((InK P c j u ∧ InL P c j w) ∨ (InL P c j u ∧ InK P c j w))

/-- The loop `Y`, as primal edges: between `K'` and `L`. -/
def tY (u w : Fin n) : Prop :=
  M.graph.Adj u w ∧ ((InK' P c j u ∧ InL P c j w) ∨ (InL P c j u ∧ InK' P c j w))

/-- The primal form of "`E − Mt` is a connected figure-eight": the `{α, A} | {μ, B}` partition
of `T − h` has exactly the three chains `K`, `K'`, `L`. -/
def ThreeChains : Prop :=
  ∀ u, u ≠ h →
    ((c u = c (P.x j) ∨ c u = c (P.x (j + 3))) → InK P c j u ∨ InK' P c j u) ∧
    ((c u = c (P.x (j + 1)) ∨ c u = c (P.x (j + 4))) → InL P c j u)

/-! ### Small lemmas -/

variable {P c j}

lemma active_of_reach {a b : Fin 4} {s u : Fin n} (hs : Active h c a b s)
    (hr : (pairGraph M.graph h c a b).Reachable s u) : Active h c a b u := by
  obtain ⟨p⟩ := hr
  have key : ∀ {x y : Fin n} (_p : (pairGraph M.graph h c a b).Walk x y),
      Active h c a b x → Active h c a b y := by
    intro x y p
    induction p with
    | nil => exact id
    | cons e _ ih => exact fun _ => ih e.2.2
  exact key p hs

/-- Distinct colours of an unfilled frame. -/
lemma col4 : ∀ a m A B x : Fin 4, m ≠ a → A ≠ a → B ≠ a → m ≠ A → m ≠ B → A ≠ B →
    ((x = a ∨ x = A) ∨ (x = m ∨ x = B)) ∧ ¬ ((x = a ∨ x = A) ∧ (x = m ∨ x = B)) := by
  decide

lemma xj2_col (hr : RepeatAt P c j) : c (P.x (j + 2)) = c (P.x j) := hr.1.symm

lemma inK_self : InK P c j (P.x (j + 2)) := Reachable.refl _

lemma inL_self : InL P c j (P.x (j + 1)) := Reachable.refl _

lemma inK'_self : InK' P c j (P.x j) := Reachable.refl _

lemma fin5_succ (j : Fin 5) : j + 2 + 1 = j + 3 ∧ j + 1 + 1 = j + 2 ∧ j + 3 + 1 = j + 4 ∧
    j + 4 + 1 = j := by
  revert j; decide

/-- `x (j+3) ∈ K`: the spoke `x (j+2) x (j+3)` is an `{α, A}`-edge. -/
lemma inK_x3 (hr : RepeatAt P c j) : InK P c j (P.x (j + 3)) := by
  have e := (fin5_succ j).1
  have hadj : M.graph.Adj (P.x (j + 2)) (P.x (j + 3)) := e ▸ P.adj_cyc (j + 2)
  exact Adj.reachable ⟨hadj, ⟨(P.adj_h _).ne', Or.inl (xj2_col hr)⟩,
    ⟨(P.adj_h _).ne', Or.inr rfl⟩⟩

/-- `x (j+4) ∈ L` at a `Lock2` state. -/
lemma inL_x4 (hl : Lock2 P c j) : InL P c j (P.x (j + 4)) := hl

/-! ### Spokes -/

/-- `v`'s matching edge is the spoke `x (j+2) x (j+3)`. -/
theorem mSpoke (hr : RepeatAt P c j) : tM P c j (P.x (j + 2)) (P.x (j + 3)) := by
  have e := (fin5_succ j).1
  refine ⟨e ▸ P.adj_cyc (j + 2), (P.adj_h _).ne', (P.adj_h _).ne', ?_⟩
  unfold tait
  rw [xj2_col hr]

/-- The other four spokes are not matching edges. -/
theorem not_tM_spoke (hr : RepeatAt P c j) :
    ¬ tM P c j (P.x j) (P.x (j + 1)) ∧ ¬ tM P c j (P.x (j + 1)) (P.x (j + 2)) ∧
    ¬ tM P c j (P.x (j + 3)) (P.x (j + 4)) ∧ ¬ tM P c j (P.x (j + 4)) (P.x j) := by
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have key : ∀ a m A B : Fin 4, m ≠ a → A ≠ a → B ≠ a → m ≠ A → m ≠ B → A ≠ B →
      enc a + enc m ≠ enc a + enc A ∧ enc m + enc a ≠ enc a + enc A ∧
      enc A + enc B ≠ enc a + enc A ∧ enc B + enc a ≠ enc a + enc A := by decide
  obtain ⟨k1, k2, k3, k4⟩ := key _ _ _ _ h1 h2 h3 h4 h5 h6
  refine ⟨fun t => k1 t.2.2.2, fun t => ?_, fun t => k3 t.2.2.2, fun t => k4 t.2.2.2⟩
  have := t.2.2.2
  unfold tait at this
  rw [← h02] at this
  exact k2 this

/-- At a `Lock2` state the spokes `x (j+1) x (j+2)` and `x (j+3) x (j+4)` are `X`-edges. -/
theorem xSpokes (hr : RepeatAt P c j) (hl : Lock2 P c j) :
    tX P c j (P.x (j + 1)) (P.x (j + 2)) ∧ tX P c j (P.x (j + 3)) (P.x (j + 4)) := by
  obtain ⟨-, e1, e3, -⟩ := fin5_succ j
  exact ⟨⟨e1 ▸ P.adj_cyc (j + 1), Or.inr ⟨inL_self, inK_self⟩⟩,
    ⟨e3 ▸ P.adj_cyc (j + 3), Or.inl ⟨inK_x3 hr, inL_x4 hl⟩⟩⟩

/-- At a `Lock2` state the spokes `x (j+4) x j` and `x j x (j+1)` are `Y`-edges. -/
theorem ySpokes (hl : Lock2 P c j) :
    tY P c j (P.x (j + 4)) (P.x j) ∧ tY P c j (P.x j) (P.x (j + 1)) := by
  obtain ⟨-, -, -, e4⟩ := fin5_succ j
  have a4 := P.adj_cyc (j + 4)
  rw [e4] at a4
  exact ⟨⟨a4, Or.inr ⟨inL_x4 hl, inK'_self⟩⟩, ⟨P.adj_cyc j, Or.inl ⟨inK'_self, inL_self⟩⟩⟩

/-! ### ¬inA (D2) and the disjointness of the loops -/

/-- **¬inA at a `Lock2` state** (the existing formal Kempe duality D2, sphere). -/
theorem notInA (hr : RepeatAt P c j) (hl : Lock2 P c j) : ¬ InA P c j :=
  fun hA => not_reach_alpha_A_of_lock2 P c j hr hl hA.symm

lemma K_K'_disjoint (hA : ¬ InA P c j) {u : Fin n} (hK : InK P c j u) (hK' : InK' P c j u) :
    False :=
  hA (hK.trans hK'.symm)

lemma K_L_disjoint (hr : RepeatAt P c j) {u : Fin n} (hK : InK P c j u) (hL : InL P c j u) :
    False := by
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have aK := active_of_reach ⟨(P.adj_h _).ne', Or.inl h02.symm⟩ hK
  have aL := active_of_reach ⟨(P.adj_h _).ne', Or.inl rfl⟩ hL
  exact ((col4 _ _ _ _ (c u) h1 h2 h3 h4 h5 h6).2) ⟨aK.2, aL.2⟩

lemma K'_L_disjoint (hr : RepeatAt P c j) {u : Fin n} (hK : InK' P c j u) (hL : InL P c j u) :
    False := by
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have aK := active_of_reach ⟨(P.adj_h _).ne', Or.inl rfl⟩ hK
  have aL := active_of_reach ⟨(P.adj_h _).ne', Or.inl rfl⟩ hL
  exact ((col4 _ _ _ _ (c u) h1 h2 h3 h4 h5 h6).2) ⟨aK.2, aL.2⟩

/-- Given `¬inA`, the loops `X` and `Y` share no edge. -/
theorem tX_tY_disjoint (hr : RepeatAt P c j) (hA : ¬ InA P c j) {u w : Fin n}
    (hX : tX P c j u w) (hY : tY P c j u w) : False := by
  rcases hX.2 with ⟨hu, hw⟩ | ⟨hu, hw⟩ <;> rcases hY.2 with ⟨hu', hw'⟩ | ⟨hu', hw'⟩
  · exact K_K'_disjoint hA hu hu'
  · exact K_L_disjoint hr hu hu'
  · exact K_L_disjoint hr hw hw'
  · exact K_K'_disjoint hA hw hw'

/-! ### The figure-eight dictionary -/

/-- `tM` is "both ends in one class" (`tait_cross_iff`). -/
theorem tM_iff (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) {u w : Fin n}
    (e : M.graph.Adj u w) (hu : u ≠ h) (hw : w ≠ h) :
    tM P c j u w ↔ ((c u = c (P.x j) ∨ c u = c (P.x (j + 3))) ↔
      (c w = c (P.x j) ∨ c w = c (P.x (j + 3)))) := by
  rw [tait_cross_iff _ _ _ _ (hc e hu hw) (Ne.symm hr.2.2.1)]
  exact ⟨fun t => t.2.2.2, fun t => ⟨e, hu, hw, t⟩⟩

/-- **The figure-eight dictionary.** Under `ThreeChains`, every edge of `T − h` outside the
matching is an `X`-edge or a `Y`-edge. -/
theorem q_edge_cover (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (h3 : ThreeChains P c j) {u w : Fin n} (e : M.graph.Adj u w) (hu : u ≠ h) (hw : w ≠ h)
    (hnot : ¬ tM P c j u w) : tX P c j u w ∨ tY P c j u w := by
  rw [tM_iff hc hr e hu hw] at hnot
  obtain ⟨-, h1, h2, h3', h4, h5, h6⟩ := hr
  have cu := col4 _ _ _ _ (c u) h1 h2 h3' h4 h5 h6
  have cw := col4 _ _ _ _ (c w) h1 h2 h3' h4 h5 h6
  rcases cu.1 with hua | hum
  · have hwm : c w = c (P.x (j + 1)) ∨ c w = c (P.x (j + 4)) :=
      (cw.1.resolve_left fun hwa => hnot ⟨fun _ => hwa, fun _ => hua⟩)
    have hL := (h3 w hw).2 hwm
    rcases (h3 u hu).1 hua with hK | hK'
    · exact Or.inl ⟨e, Or.inl ⟨hK, hL⟩⟩
    · exact Or.inr ⟨e, Or.inl ⟨hK', hL⟩⟩
  · have hwa : c w = c (P.x j) ∨ c w = c (P.x (j + 3)) :=
      cw.1.resolve_right fun hwm => hnot ⟨fun hua => absurd ⟨hua, hum⟩ cu.2,
        fun hwa => absurd ⟨hwa, hwm⟩ cw.2⟩
    have hL := (h3 u hu).2 hum
    rcases (h3 w hw).1 hwa with hK | hK'
    · exact Or.inl ⟨e, Or.inr ⟨hL, hK⟩⟩
    · exact Or.inr ⟨e, Or.inr ⟨hL, hK'⟩⟩

/-! ### Lemma F: the local step at a triangle -/

/-- The three corners of the face of `d` in a triangulation are pairwise adjacent. -/
lemma tri_adj (htri : M.Triangulated) (d : M.Dart) :
    M.graph.Adj d.snd (M.rotation.faceNext d).snd ∧
      M.graph.Adj (M.rotation.faceNext d).snd d.fst := by
  have h3 := TutteSides.tri3 htri d
  set d1 := M.rotation.faceNext d
  set d2 := M.rotation.faceNext d1
  have f1 : d1.fst = d.snd := M.rotation.face_next_fst d
  have f2 : d2.fst = d1.snd := M.rotation.face_next_fst d1
  have f3 : d2.snd = d.fst := by
    have := M.rotation.face_next_fst d2
    rw [h3] at this
    exact this.symm
  refine ⟨?_, ?_⟩
  · have := d1.adj; rwa [f1] at this
  · have := d2.adj; rwa [f2, f3] at this

/-- An `{a, b}`-chain absorbs an adjacent active vertex. -/
lemma reach_step {a b : Fin 4} {s u r : Fin n} (hu : (pairGraph M.graph h c a b).Reachable s u)
    (hs : Active h c a b s) (e : M.graph.Adj u r) (hr : Active h c a b r) :
    (pairGraph M.graph h c a b).Reachable s r :=
  hu.trans (Adj.reachable ⟨e, active_of_reach hs hu, hr⟩)

/-- **Lemma F, local step.** Let `d = (p, q)` be a dart whose edge is an `X`-edge, and `r` the
third corner of its triangle, `r ≠ h`. Then of the other two edges `q r`, `r p`, one is an
`X`-edge and the other a matching edge. (The dual cubic vertex has both `E − Mt` edges on
`X`.) -/
theorem triangle_step (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (htri : M.Triangulated) (d : M.Dart) (hX : tX P c j d.fst d.snd)
    (hrh : (M.rotation.faceNext d).snd ≠ h) :
    (tX P c j d.snd (M.rotation.faceNext d).snd ∧ tM P c j (M.rotation.faceNext d).snd d.fst) ∨
      (tM P c j d.snd (M.rotation.faceNext d).snd ∧
        tX P c j (M.rotation.faceNext d).snd d.fst) := by
  obtain ⟨eqr, erp⟩ := tri_adj htri d
  set r := (M.rotation.faceNext d).snd
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have aK0 : Active h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)) :=
    ⟨(P.adj_h _).ne', Or.inl h02.symm⟩
  have aL0 : Active h c (c (P.x (j + 1))) (c (P.x (j + 4))) (P.x (j + 1)) :=
    ⟨(P.adj_h _).ne', Or.inl rfl⟩
  have cr := col4 _ _ _ _ (c r) h1 h2 h3 h4 h5 h6
  have hrM : ∀ {u : Fin n}, M.graph.Adj u r → u ≠ h →
      ((c u = c (P.x j) ∨ c u = c (P.x (j + 3))) ↔
        (c r = c (P.x j) ∨ c r = c (P.x (j + 3)))) → tM P c j u r := by
    intro u e hu hiff
    exact (tM_iff hc ⟨h02, h1, h2, h3, h4, h5, h6⟩ e hu hrh).mpr hiff
  have hMr : ∀ {u : Fin n}, M.graph.Adj r u → u ≠ h →
      ((c r = c (P.x j) ∨ c r = c (P.x (j + 3))) ↔
        (c u = c (P.x j) ∨ c u = c (P.x (j + 3)))) → tM P c j r u := by
    intro u e hu hiff
    exact (tM_iff hc ⟨h02, h1, h2, h3, h4, h5, h6⟩ e hrh hu).mpr hiff
  rcases hX.2 with ⟨hp, hq⟩ | ⟨hp, hq⟩
  · -- `p ∈ K`, `q ∈ L`
    have ap := active_of_reach aK0 hp
    have aq := active_of_reach aL0 hq
    rcases cr.1 with hra | hrm
    · have hrK : InK P c j r := reach_step hp aK0 erp.symm ⟨hrh, hra⟩
      refine Or.inl ⟨⟨eqr, Or.inr ⟨hq, hrK⟩⟩, hMr erp ap.1 ⟨fun _ => ap.2, fun _ => hra⟩⟩
    · have hrL : InL P c j r := reach_step hq aL0 eqr ⟨hrh, hrm⟩
      refine Or.inr ⟨hrM eqr aq.1 ⟨fun hqa => absurd ⟨hqa, aq.2⟩
        (col4 _ _ _ _ _ h1 h2 h3 h4 h5 h6).2, fun hra => absurd ⟨hra, hrm⟩ cr.2⟩,
        ⟨erp, Or.inr ⟨hrL, hp⟩⟩⟩
  · -- `p ∈ L`, `q ∈ K`
    have ap := active_of_reach aL0 hp
    have aq := active_of_reach aK0 hq
    rcases cr.1 with hra | hrm
    · have hrK : InK P c j r := reach_step hq aK0 eqr ⟨hrh, hra⟩
      exact Or.inr ⟨hrM eqr aq.1 ⟨fun _ => hra, fun _ => aq.2⟩, ⟨erp, Or.inl ⟨hrK, hp⟩⟩⟩
    · have hrL : InL P c j r := reach_step hp aL0 erp.symm ⟨hrh, hrm⟩
      refine Or.inl ⟨⟨eqr, Or.inl ⟨hq, hrL⟩⟩, hMr erp ap.1 ⟨fun hra => absurd ⟨hra, hrm⟩ cr.2,
        fun hpa => absurd ⟨hpa, ap.2⟩ (col4 _ _ _ _ _ h1 h2 h3 h4 h5 h6).2⟩⟩

/-! ### A5v in primal form -/

/-- The third corner of the far triangle of the spoke `x (j+2) x (j+3)` lies in `L`. -/
lemma far_corner_L (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (h3 : ThreeChains P c j) {z : Fin n} (hz : z ≠ h)
    (e2 : M.graph.Adj (P.x (j + 2)) z) (e3 : M.graph.Adj (P.x (j + 3)) z) : InL P c j z := by
  obtain ⟨h02, h1, h2, h3', h4, h5, h6⟩ := hr
  have n2 : c (P.x (j + 2)) ≠ c z := hc e2 (P.adj_h _).ne' hz
  have n3 : c (P.x (j + 3)) ≠ c z := hc e3 (P.adj_h _).ne' hz
  have cz := col4 _ _ _ _ (c z) h1 h2 h3' h4 h5 h6
  refine (h3 z hz).2 (cz.1.resolve_left ?_)
  rintro (hza | hzA)
  · exact n2 (h02.symm.trans hza.symm)
  · exact n3 hzA.symm

/-- **A5v, primal form (Lemma F at the far triangle).** At a doubly locked state with
`ThreeChains`, let `z ≠ h` be the third corner of the far triangle of `v`'s matching spoke
`x (j+2) x (j+3)`. Then both non-matching edges `x (j+2) z` and `x (j+3) z` are `X`-edges and
neither is a `Y`-edge: the far end of `f k` lies on `X`. -/
theorem a5v_primal (hc : ProperOff M.graph h c) (hdl : DoublyLocked P c j)
    (h3 : ThreeChains P c j) {z : Fin n} (hz : z ≠ h)
    (e2 : M.graph.Adj (P.x (j + 2)) z) (e3 : M.graph.Adj (P.x (j + 3)) z) :
    (tX P c j (P.x (j + 2)) z ∧ tX P c j (P.x (j + 3)) z) ∧
      (¬ tY P c j (P.x (j + 2)) z ∧ ¬ tY P c j (P.x (j + 3)) z) := by
  obtain ⟨hr, -, hl⟩ := hdl
  have hL := far_corner_L hc hr h3 hz e2 e3
  have hA := notInA hr hl
  have x2 : tX P c j (P.x (j + 2)) z := ⟨e2, Or.inl ⟨inK_self, hL⟩⟩
  have x3 : tX P c j (P.x (j + 3)) z := ⟨e3, Or.inl ⟨inK_x3 hr, hL⟩⟩
  exact ⟨⟨x2, x3⟩, fun hY => tX_tY_disjoint hr hA x2 hY,
    fun hY => tX_tY_disjoint hr hA x3 hY⟩

/-- In primal coordinates A5v **is** `¬inA`: the edge `x (j+2) z` of the far triangle is a
`Y`-edge iff `inA` holds. -/
theorem y_far_iff_inA (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (h3 : ThreeChains P c j) {z : Fin n} (hz : z ≠ h)
    (e2 : M.graph.Adj (P.x (j + 2)) z) (e3 : M.graph.Adj (P.x (j + 3)) z) :
    tY P c j (P.x (j + 2)) z ↔ InA P c j := by
  have hL := far_corner_L hc hr h3 hz e2 e3
  constructor
  · rintro ⟨-, ⟨hK', -⟩ | ⟨hL', -⟩⟩
    · exact hK'.symm
    · exact absurd hL' (fun hL2 => K_L_disjoint hr inK_self hL2)
  · intro hA
    exact ⟨e2, Or.inl ⟨hA.symm, hL⟩⟩

end SimpleGraph.A5vBridge

#print axioms SimpleGraph.A5vBridge.mSpoke
#print axioms SimpleGraph.A5vBridge.not_tM_spoke
#print axioms SimpleGraph.A5vBridge.xSpokes
#print axioms SimpleGraph.A5vBridge.ySpokes
#print axioms SimpleGraph.A5vBridge.notInA
#print axioms SimpleGraph.A5vBridge.tX_tY_disjoint
#print axioms SimpleGraph.A5vBridge.q_edge_cover
#print axioms SimpleGraph.A5vBridge.triangle_step
#print axioms SimpleGraph.A5vBridge.a5v_primal
#print axioms SimpleGraph.A5vBridge.y_far_iff_inA
