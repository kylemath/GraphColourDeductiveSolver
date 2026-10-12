module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameF3

/-!
# From an appearance to an occurrence: shared definitions

The Birkhoff diamond and RSST 2.122 both have interior `K₄ − e`: centres `0` and `2`, tips `1`
and `3`. `Appears γ T int` is the RSST notion "appears", for a triangulation:
* the interior is injective;
* it induces `K₄ − e`;
* it has the free-completion degrees `γ`.
Faces are not assumed: with `NoSep`, every triangle is facial.

`TipsClean T int`: every common neighbour of the two tips is a centre. If it fails, a vertex
`x` outside the interior is adjacent to both tips. Then `x – int 1 – int 0 – int 3` is a 4-cycle
with vertices of the rotation at `int 0` on both sides, so it is a separating 4-cycle (F2).
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancyIcosahedral

variable {n : ℕ}

/-- The RSST notion "appears", for an interior `K₄ − e` with degrees `γ`. -/
structure Appears (γ : Fin 4 → ℕ) (T : SphericalMap n) (int : Fin 4 → Fin n) : Prop where
  int_inj : Function.Injective int
  a01 : T.Adj (int 0) (int 1)
  a02 : T.Adj (int 0) (int 2)
  a03 : T.Adj (int 0) (int 3)
  a12 : T.Adj (int 1) (int 2)
  a23 : T.Adj (int 2) (int 3)
  n13 : ¬ T.Adj (int 1) (int 3)
  deg : ∀ a, T.graph.degree (int a) = γ a

/-- Every common neighbour of the tips is a centre. -/
def TipsClean (T : SphericalMap n) (int : Fin 4 → Fin n) : Prop :=
  ∀ x, T.Adj (int 1) x → T.Adj (int 3) x → x = int 0 ∨ x = int 2

variable {M : SphericalMap n}

theorem nx_func {u v w w' : Fin n} (h : Nx M u v w) (h' : Nx M u v w') : w = w' := by
  obtain ⟨h1, e1⟩ := h
  obtain ⟨h2, e2⟩ := h'
  exact e1.symm.trans e2

/-- At a vertex of degree `d` the rotation is a single `d`-cycle of darts. -/
theorem orbitN {v : Fin n} {d : ℕ} (hv : M.graph.degree v = d) (D : M.Dart) (hd : D.fst = v) :
    (⇑M.rotation.next)^[d] D = D ∧
    (∀ i j : ℕ, i < d → j < d →
      (⇑M.rotation.next)^[i] D = (⇑M.rotation.next)^[j] D → i = j) := by
  classical
  subst hd
  let R := M.rotation
  let σ := R.neighborRotation D.fst
  let w : M.graph.neighborSet D.fst := ⟨D.snd, D.adj⟩
  have hdw : M.graph.dartOfNeighborSet D.fst w = D := rfl
  have hsemi : Function.Semiconj (M.graph.dartOfNeighborSet D.fst) σ R.next :=
    R.neighbor_rotation_dart D.fst
  have hit : ∀ k, (⇑R.next)^[k] D = M.graph.dartOfNeighborSet D.fst (σ^[k] w) := fun k => by
    have := hsemi.iterate_right k w
    rw [hdw] at this
    exact this.symm
  have hp : Function.minimalPeriod σ w = d := by
    rw [R.neighbor_period_eq_degree, hv]
  refine ⟨?_, ?_⟩
  · rw [hit, ← hp, Function.iterate_minimalPeriod, hdw]
  · intro i j hi hj hij
    rw [hit, hit] at hij
    exact Function.iterate_injOn_Iio_minimalPeriod (by rw [hp]; exact hi) (by rw [hp]; exact hj)
      (M.graph.dartOfNeighborSet_injective _ hij)

/-- A rotation chain of five steps at a degree-six vertex closes up, with distinct entries. -/
theorem chain6 {v a0 a1 a2 a3 a4 a5 : Fin n} (hv : M.graph.degree v = 6)
    (h01 : Nx M v a0 a1) (h12 : Nx M v a1 a2) (h23 : Nx M v a2 a3) (h34 : Nx M v a3 a4)
    (h45 : Nx M v a4 a5) :
    Nx M v a5 a0 ∧
      (a0 ≠ a1 ∧ a0 ≠ a2 ∧ a0 ≠ a3 ∧ a0 ≠ a4 ∧ a0 ≠ a5 ∧ a1 ≠ a2 ∧ a1 ≠ a3 ∧ a1 ≠ a4 ∧
        a1 ≠ a5 ∧ a2 ≠ a3 ∧ a2 ≠ a4 ∧ a2 ≠ a5 ∧ a3 ≠ a4 ∧ a3 ≠ a5 ∧ a4 ≠ a5) := by
  obtain ⟨g0, g1, e01⟩ := nx_dart h01
  obtain ⟨_, g2, e12⟩ := nx_dart h12
  obtain ⟨_, g3, e23⟩ := nx_dart h23
  obtain ⟨_, g4, e34⟩ := nx_dart h34
  obtain ⟨_, g5, e45⟩ := nx_dart h45
  let D : M.Dart := ⟨(v,a0),g0⟩
  obtain ⟨p6, inj⟩ := orbitN hv D rfl
  have i0 : (⇑M.rotation.next)^[0] D = ⟨(v,a0),g0⟩ := rfl
  have i1 : (⇑M.rotation.next)^[1] D = ⟨(v,a1),g1⟩ := e01
  have i2 : (⇑M.rotation.next)^[2] D = ⟨(v,a2),g2⟩ := by
    rw [Function.iterate_succ_apply', i1]; exact e12
  have i3 : (⇑M.rotation.next)^[3] D = ⟨(v,a3),g3⟩ := by
    rw [Function.iterate_succ_apply', i2]; exact e23
  have i4 : (⇑M.rotation.next)^[4] D = ⟨(v,a4),g4⟩ := by
    rw [Function.iterate_succ_apply', i3]; exact e34
  have i5 : (⇑M.rotation.next)^[5] D = ⟨(v,a5),g5⟩ := by
    rw [Function.iterate_succ_apply', i4]; exact e45
  have close : M.rotation.next ⟨(v,a5),g5⟩ = ⟨(v,a0),g0⟩ := by
    rw [← i5, ← Function.iterate_succ_apply' (⇑M.rotation.next) 5]; exact p6
  have ne : ∀ i j : ℕ, i < 6 → j < 6 → i ≠ j → ∀ x y : Fin n, ∀ (hx : M.Adj v x) (hy : M.Adj v y),
      (⇑M.rotation.next)^[i] D = ⟨(v,x),hx⟩ → (⇑M.rotation.next)^[j] D = ⟨(v,y),hy⟩ → x ≠ y := by
    intro i j hi hj hij x y hx hy ex ey e
    subst e
    exact hij (inj i j hi hj (ex.trans ey.symm))
  refine ⟨nx_of_dart close, ?_⟩
  exact ⟨ne 0 1 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i0 i1,
    ne 0 2 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i0 i2,
    ne 0 3 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i0 i3,
    ne 0 4 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i0 i4,
    ne 0 5 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i0 i5,
    ne 1 2 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i1 i2,
    ne 1 3 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i1 i3,
    ne 1 4 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i1 i4,
    ne 1 5 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i1 i5,
    ne 2 3 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i2 i3,
    ne 2 4 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i2 i4,
    ne 2 5 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i2 i5,
    ne 3 4 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i3 i4,
    ne 3 5 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i3 i5,
    ne 4 5 (by norm_num) (by norm_num) (by norm_num) _ _ _ _ i4 i5⟩

end SimpleGraph.SphericalMap
