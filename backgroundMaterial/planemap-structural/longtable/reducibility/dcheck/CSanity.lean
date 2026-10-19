import CGlue
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron

/-!
# CSanity: the icosahedron is `Internally6`, so `Unavoidable` is not vacuous (Long Table, 19 Oct 2026)

`CGlue.Unavoidable R` quantifies over internally 6-connected triangulations (`Internally6`). If the
class were empty, every registry would be "unavoidable" and `four_color_of_unavoidableC` would say
nothing. Here the icosahedron is shown to be `Internally6`, so the empty registry is not unavoidable
(`CGlue.not_unavoidable_nil`).

The one non-trivial field is `NoShortSepCycle`. The potential of a cycle is constant along edges off
the cycle (`side_step`), so the two sides of a cycle with vertex set `S` lie in different components
of the icosahedron minus `S`. A finite check (`ico_check`, `native_decide` over the 1,586 vertex sets
of size at most 5) shows that removing at most 4 vertices leaves the rest connected, and removing 5
leaves all but at most one vertex connected. That rules out `BothSides` (r ≤ 4) and `BothSides2`
(r = 5).
-/

namespace SimpleGraph.SphericalMap
open RotationSystem VacancyIcosahedral

variable {n : ℕ} {T : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} {c : T.Face → ZMod 2}

/-- The side of a cycle propagates along an edge off the cycle. -/
theorem side_step (C : Cyc T r ρ) (hc : CycPotential T r ρ c) {x y : Fin n} (hx : ¬ OnCyc r ρ x)
    (hy : ¬ OnCyc r ρ y) (hxy : T.Adj x y) {b : ZMod 2} (h : OnSide T c b x) : OnSide T c b y := by
  intro e he
  let d : T.Dart := ⟨(x, y), hxy⟩
  have h0 := cycInd_off' C d hx
  have hp := hc d
  rw [h0] at hp
  have hd : c (T.faceOf d) = b := h d rfl
  have key : ∀ u v : ZMod 2, 0 = u + v → v = u := by decide
  have hs : c (T.faceOf d.symm) = b := (key _ _ hp).trans hd
  rw [side_constC' C hc hy e d.symm he rfl]
  exact hs

/-- A vertex with an edge is on at most one side. -/
theorem onSide_excl' {x y : Fin n} (hxy : T.Adj x y) (h0 : OnSide T c 0 x) (h1 : OnSide T c 1 x) :
    False := by
  have := (h0 ⟨(x, y), hxy⟩ rfl).symm.trans (h1 ⟨(x, y), hxy⟩ rfl)
  exact absurd this (by decide)

end SimpleGraph.SphericalMap

namespace SimpleGraph.Icosahedron

/-- The neighbour lists (checked against `graph` by `nb_adj`). -/
def nb : Fin 12 → List (Fin 12)
  | 0 => [1, 5, 7, 8, 11]
  | 1 => [0, 2, 5, 6, 8]
  | 2 => [1, 3, 6, 8, 9]
  | 3 => [2, 4, 6, 9, 10]
  | 4 => [3, 5, 6, 10, 11]
  | 5 => [0, 1, 4, 6, 11]
  | 6 => [1, 2, 3, 4, 5]
  | 7 => [0, 8, 9, 10, 11]
  | 8 => [0, 1, 2, 7, 9]
  | 9 => [2, 3, 7, 8, 10]
  | 10 => [3, 4, 7, 9, 11]
  | 11 => [0, 4, 5, 7, 10]

theorem nb_adj : ∀ u v : Fin 12, v ∈ nb u → graph.Adj u v := by decide

/-- One step of the closure inside the complement of `S`. -/
def step (S : Finset (Fin 12)) (X : List (Fin 12)) : List (Fin 12) :=
  X ++ ((X.flatMap nb).filter (fun w => decide (w ∉ S ∧ w ∉ X))).dedup

/-- Vertices reachable from `u` avoiding `S` (eleven steps suffice). -/
def comp (S : Finset (Fin 12)) (u : Fin 12) : List (Fin 12) := (step S)^[11] [u]

/-- What the finite check asks of the closure `C` from `u`. -/
def Good (S : Finset (Fin 12)) (u : Fin 12) (C : List (Fin 12)) : Prop :=
  u ∉ S ∧ (S.card ≤ 4 → ∀ v, v ∉ S → v ∈ C) ∧ ∃ e, ∀ v, v ∉ S → v ≠ e → v ∈ C

instance (S : Finset (Fin 12)) (u : Fin 12) (C : List (Fin 12)) : Decidable (Good S u C) :=
  have h1 : Decidable (u ∉ S) := inferInstance
  have h2 : Decidable (S.card ≤ 4 → ∀ v : Fin 12, v ∉ S → v ∈ C) := inferInstance
  have h3 : Decidable (∃ e : Fin 12, ∀ v : Fin 12, v ∉ S → v ≠ e → v ∈ C) := inferInstance
  @instDecidableAnd _ _ h1 (@instDecidableAnd _ _ h2 h3)

/-- The two smallest vertices off `S` (one of them is not the isolated vertex, if any). -/
def cand (S : Finset (Fin 12)) : List (Fin 12) := ((List.finRange 12).filter (· ∉ S)).take 2

/-- **The finite check.** Removing at most 4 vertices leaves the icosahedron connected; removing 5
leaves all but at most one vertex connected. -/
theorem ico_check : ∀ S : Finset (Fin 12), S.card ≤ 5 → ∃ u ∈ cand S, Good S u (comp S u) := by
  native_decide

/-- Steps that stay off `S`. -/
def Off (S : Finset (Fin 12)) (u v : Fin 12) : Prop := v ∉ S ∧ graph.Adj u v

theorem comp_sound (S : Finset (Fin 12)) (u : Fin 12) :
    ∀ k, ∀ w ∈ (step S)^[k] [u], Relation.ReflTransGen (Off S) u w := by
  intro k
  induction k with
  | zero =>
    intro w hw
    rw [Function.iterate_zero_apply, List.mem_singleton] at hw
    rw [hw]
  | succ k ih =>
    intro w hw
    rw [Function.iterate_succ_apply'] at hw
    rcases List.mem_append.1 hw with h | h
    · exact ih w h
    · obtain ⟨h1, h2⟩ := List.mem_filter.1 (List.mem_dedup.1 h)
      obtain ⟨x, hx, hxw⟩ := List.mem_flatMap.1 h1
      exact (ih x hx).tail ⟨(of_decide_eq_true h2).1, nb_adj x w hxw⟩

theorem off_not_mem {S : Finset (Fin 12)} {u w : Fin 12} (h : Relation.ReflTransGen (Off S) u w)
    (hu : u ∉ S) : w ∉ S := by
  cases h with
  | refl => exact hu
  | tail _ h => exact h.1

open SimpleGraph.SphericalMap VacancyIcosahedral in
/-- **No short separating cycle in the icosahedron.** -/
theorem noShortSep : SimpleGraph.SphericalMap.ClaimGlue.NoShortSepCycle sphericalMap := by
  classical
  intro r ρ c C hr hc hs h5
  let S : Finset (Fin 12) := (Finset.range r).image ρ
  have hOn : ∀ x, OnCyc r ρ x ↔ x ∈ S := by
    intro x
    simp only [S, Finset.mem_image, Finset.mem_range, OnCyc]
  have hcard : S.card ≤ r := Finset.card_image_le.trans (by simp)
  obtain ⟨u0, -, hu0, h4, e, h5'⟩ := ico_check S (by omega)
  -- the side is constant on everything reached from `u0`
  have hside : ∀ w, Relation.ReflTransGen (Off S) u0 w → ∀ b : ZMod 2,
      (OnSide sphericalMap c b u0 ↔ OnSide sphericalMap c b w) := by
    intro w hw b
    induction hw with
    | refl => exact Iff.rfl
    | @tail v w hv hvw ih =>
      have hvS := off_not_mem hv hu0
      have hv' : ¬ OnCyc r ρ v := fun h => hvS ((hOn v).1 h)
      have hw' : ¬ OnCyc r ρ w := fun h => hvw.1 ((hOn w).1 h)
      exact ih.trans ⟨side_step C hc hv' hw' hvw.2, side_step C hc hw' hv' hvw.2.symm⟩
  have hin : ∀ x, x ∈ comp S u0 → ∀ b : ZMod 2,
      (OnSide sphericalMap c b u0 ↔ OnSide sphericalMap c b x) :=
    fun x hx => hside x (comp_sound S u0 11 x hx)
  have hoff : ∀ x, ¬ OnCyc r ρ x → x ∉ S := fun x hx h => hx ((hOn x).2 h)
  -- two vertices off the cycle, both reached, cannot see different sides
  have hclash : ∀ x x' y', x ∈ comp S u0 → x' ∈ comp S u0 → OnSide sphericalMap c 0 x →
      OnSide sphericalMap c 1 x' → sphericalMap.Adj x' y' → False := by
    intro x x' y' hx hx' h0 h1 hxy
    have h0' := (hin x' hx' 0).1 ((hin x hx 0).2 h0)
    exact onSide_excl' hxy h0' h1
  by_cases h4c : S.card ≤ 4
  · obtain ⟨⟨x, -, hx, h0, -⟩, ⟨x', y', hx', h1, hxy'⟩⟩ := hs
    exact hclash x x' y' (h4 h4c x (hoff x hx)) (h4 h4c x' (hoff x' hx')) h0 h1 hxy'
  · have hr5 : r = 5 := by omega
    obtain ⟨x0, x0', -, -, hne0, hx0, s0, -, hx0', s0', -⟩ := h5 hr5 0
    obtain ⟨x1, x1', y1, y1', hne1, hx1, s1, hxy1, hx1', s1', hxy1'⟩ := h5 hr5 1
    have pick : ∀ x x', x ≠ x' → ¬ OnCyc r ρ x → ¬ OnCyc r ρ x' →
        (x ≠ e ∧ x ∈ comp S u0) ∨ (x' ≠ e ∧ x' ∈ comp S u0) := by
      intro x x' hne hx hx'
      by_cases hxe : x = e
      · have : x' ≠ e := fun h => hne (hxe.trans h.symm)
        exact Or.inr ⟨this, h5' x' (hoff x' hx') this⟩
      · exact Or.inl ⟨hxe, h5' x (hoff x hx) hxe⟩
    rcases pick x0 x0' hne0 hx0 hx0' with ⟨-, a⟩ | ⟨-, a⟩ <;>
      rcases pick x1 x1' hne1 hx1 hx1' with ⟨-, b⟩ | ⟨-, b⟩
    · exact hclash _ _ _ a b s0 s1 hxy1
    · exact hclash _ _ _ a b s0 s1' hxy1'
    · exact hclash _ _ _ a b s0' s1 hxy1
    · exact hclash _ _ _ a b s0' s1' hxy1'

theorem connected : sphericalMap.graph.Connected := by
  classical
  obtain ⟨u0, -, -, h4, -⟩ := ico_check ∅ (by simp)
  have key : ∀ w, Relation.ReflTransGen (Off ∅) u0 w → sphericalMap.graph.Reachable u0 w := by
    intro w h
    induction h with
    | refl => rfl
    | tail _ h ih => exact ih.trans h.2.reachable
  have hr : ∀ v, sphericalMap.graph.Reachable u0 v := fun v =>
    key v (comp_sound ∅ u0 11 v (h4 (by simp) v (by simp)))
  have : Nonempty (Fin 12) := ⟨0⟩
  exact Connected.mk (fun u v => (hr u).symm.trans (hr v))

theorem noSep : SimpleGraph.SphericalMap.NoSep sphericalMap := by
  have h : ∀ x y : Fin 12, graph.Adj x y → ∀ z, graph.Adj y z → graph.Adj z x →
      nextTable y x = z ∨ nextTable x y = z := by decide
  intro x y z hxy hyz hzx
  rcases h x y hxy z hyz hzx with e | e
  · exact Or.inl ⟨hxy.symm, e⟩
  · exact Or.inr ⟨hxy, e⟩

/-- **The icosahedron is internally 6-connected** in the sense of `Internally6`. -/
theorem internally6 : SimpleGraph.SphericalMap.ClaimGlue.Internally6 sphericalMap :=
  ⟨by norm_num, connected, fun d => sphericalMap_triangular _,
    fun x => (sphericalMap_degree x).ge, noSep, noShortSep⟩

end SimpleGraph.Icosahedron

namespace SimpleGraph.SphericalMap.CGlue

/-- **`Unavoidable` is not vacuous**: the empty registry is not unavoidable, because the icosahedron
is internally 6-connected and contains nothing. -/
theorem not_unavoidable_nil : ¬ Unavoidable ⟨[], []⟩ := by
  intro hU
  rcases hU 12 Icosahedron.sphericalMap Icosahedron.internally6 with ⟨e, he, -⟩ | ⟨e, he, -⟩ <;>
    simp at he

/-- The same for the D + single-edge registry form. -/
theorem not_unavoidable1_nil : ¬ Unavoidable1 ⟨[], []⟩ := by
  intro hU
  rcases hU 12 Icosahedron.sphericalMap Icosahedron.internally6 with ⟨e, he, -⟩ | ⟨e, he, -⟩ <;>
    simp at he

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.Icosahedron.noShortSep
#print axioms SimpleGraph.Icosahedron.internally6
#print axioms SimpleGraph.SphericalMap.CGlue.not_unavoidable_nil
