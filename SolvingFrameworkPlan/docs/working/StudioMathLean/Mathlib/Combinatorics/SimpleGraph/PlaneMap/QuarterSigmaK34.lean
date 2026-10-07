/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaExit

/-!
# `σ`-exits at a `(5,5,5,5,6)` hole with the degree-6 vertex at `k = 3` or `k = 4`

Formalises the local [proved] facts of `NightC1Gamma.md` §2 (`k = 3`, `k = 4`) and
`NightF6.md` §2 about the `σ`-exit `σ = sigSwap` at an `R3` state `c` with repeat index `j`
(link `α, μ, α, A, B` at `x j, …, x (j+4)`, ring `(w₀..w₄) = (B, A, B, μ, A)`).

* `K4Ball`: `x j, x (j+1), x (j+2)` as in `TripleBallP`, `x (j+3)` of degree five with its ring,
  and `p = x (j+4)` of degree six with outer neighbours `x (j+3), w₃, m, w₄, x j` (a path).
  `K3Ball`: the mirror, `p = x (j+3)` of degree six (outer path `x (j+2), w₂, m, w₃, x (j+4)`)
  and `x (j+4)` of degree five.
* `m_col_k4`, `m_col_k3`: the extra neighbour `m` has colour `α` (Lemma D, from properness).

## Main results (sorry-free, no planarity)

1. `sigma_exit_not_DL_k4`, `sigma_exit_not_DL_k3`: the `σ`-image is never doubly locked; at
   `k = 4` its Lock 1 dies at `x (j+3)` (`sigma_exit_noLock1_k4`), at `k = 3` its Lock 2 dies at
   `x (j+4)` (`sigma_exit_noLock2_k3`).
2. `sigma_exit_criterion_k4`: `σ c` is lockless iff `w₀ = w j` does **not** reach `m` in the
   `{α, B}`-graph of `c` with `x j` deleted (`K_B − x₀`); otherwise it has exactly Lock 2
   (`lock2_after_sigma_k4`). `sigma_exit_criterion_k3`: `σ c` is lockless iff `w₁ = w (j+1)`
   does not reach `m` in the `{α, A}`-graph of `c` with `x (j+2)` deleted (`K_F − x₂`).
   Both are stated in `c` (before the swap). The note's final forms
   (`k = 4`: `w₄ ∈ K_{μ,A}(x₁)`; `k = 3`: `w₂ ∈ K_{μ,B}(x₁)`) follow from these by the
   Kempe/Jordan duality (D) of `NightC1Gamma.md` §2, which is **not** formalised here.
3. `sigma_exit_f_ge_two_k3`: at `k = 3`, if `w₂ ∈ K_{μ,B}(x₁)` in `c` (the note's criterion,
   equivalent to `σ c` lockless by (D)), then `π (σ c)` and `π (π (σ c))` are both filled, i.e.
   the excursion entered at `σ c` has `f ≥ 2`. This uses no Jordan argument: Lock 2 dies, so
   `π (σ c) = φ_B⁻¹`, whose component is `{x (j+4)}`, and the `{μ,B}`-path persists.
   `sigma_exit_filled_k4`: at `k = 4` a lockless image steps to a filled state (`f ≥ 1`).

## Not formalised

* `FGeTwoK4Statement` (a `Prop`, not asserted): `f ≥ 2` at `k = 4`. The note's proof uses a
  closed `{μ,A}`-walk separating `x₁` from `x₃, x₄` in `t₁ = π (σ c)` and then (D) again.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- If every `H`-neighbour of `t` is `u`, a vertex `s ≠ t` reaching `t` reaches `u`. -/
lemma reach_of_only {V : Type*} {H : SimpleGraph V} {s t u : V} (hst : s ≠ t)
    (only : ∀ v, H.Adj t v → v = u) (r : H.Reachable s t) : H.Reachable s u := by
  obtain ⟨p⟩ := r.symm
  cases p with
  | nil => exact (hst rfl).elim
  | cons e q =>
    rw [only _ e] at q
    exact q.reachable.symm

private lemma f4_last {α μ A B x : Fin 4} (h1 : μ ≠ α) (h3 : A ≠ α) (h4 : B ≠ α) (h13 : μ ≠ A)
    (h14 : μ ≠ B) (h34 : A ≠ B) (a : x ≠ μ) (b : x ≠ A) (d : x ≠ B) : x = α := by
  revert α μ A B x; decide

private lemma fneK (j : Fin 5) : j + 4 ≠ j ∧ j + 3 ≠ j + 2 ∧ j + 1 ≠ j + 4 ∧ j + 2 ≠ j + 4 ∧
    j + 3 ≠ j + 4 := by
  revert j; decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- The `k = 4` ball: the triple ball at `j`, `x (j+3)` of degree five, and `p = x (j+4)` of
degree six with neighbours `h, x (j+3), x j, w₃, m, w₄` (outer path `x (j+3), w₃, m, w₄, x j`). -/
structure K4Ball (P : Pent M.graph h) (w : Fin 5 → Fin n) (m : Fin n) (j : Fin 5) : Prop where
  tri : TripleBallP P w j
  nbr3 : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
    u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3)
  nbr4 : ∀ u, M.graph.Adj (P.x (j + 4)) u ↔
    u = h ∨ u = P.x (j + 3) ∨ u = P.x j ∨ u = w (j + 3) ∨ u = m ∨ u = w (j + 4)
  ring23 : M.graph.Adj (w (j + 2)) (w (j + 3))
  ring3m : M.graph.Adj (w (j + 3)) m
  ringm4 : M.graph.Adj m (w (j + 4))
  off3 : ∀ i, w (j + 3) ≠ P.x i
  offm : ∀ i, m ≠ P.x i
  offh : w (j + 3) ≠ h ∧ m ≠ h

/-- The `k = 3` ball (mirror): the triple ball at `j`, `p = x (j+3)` of degree six with
neighbours `h, x (j+2), x (j+4), w₂, m, w₃`, and `x (j+4)` of degree five. -/
structure K3Ball (P : Pent M.graph h) (w : Fin 5 → Fin n) (m : Fin n) (j : Fin 5) : Prop where
  tri : TripleBallP P w j
  nbr3 : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
    u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = m ∨ u = w (j + 3)
  nbr4 : ∀ u, M.graph.Adj (P.x (j + 4)) u ↔
    u = h ∨ u = P.x (j + 3) ∨ u = P.x j ∨ u = w (j + 3) ∨ u = w (j + 4)
  ring2m : M.graph.Adj (w (j + 2)) m
  ringm3 : M.graph.Adj m (w (j + 3))
  ring34 : M.graph.Adj (w (j + 3)) (w (j + 4))
  off3 : ∀ i, w (j + 3) ≠ P.x i
  offm : ∀ i, m ≠ P.x i
  offh : w (j + 3) ≠ h ∧ m ≠ h

variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {c : Fin n → Fin 4} {j : Fin 5}

lemma R3At.outer (hR : R3At P w c j) : OuterBABA P w c j :=
  ⟨hR.2.1, hR.2.2.1, hR.2.2.2.1, hR.2.2.2.2.2⟩

/-! ### Lemma D: `m = α` -/

/-- At `k = 4`, `m` (adjacent to `x (j+4) = B`, `w₃ = μ`, `w₄ = A`) has colour `α`. -/
theorem m_col_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    c m = c (P.x j) := by
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, -, e3, e4⟩ := hR
  obtain ⟨o3, om⟩ := K.offh
  have a4 : M.graph.Adj (P.x (j + 4)) m := (K.nbr4 m).2 (by simp)
  refine f4_last h1 h3 h4 h13 h14 h34 ?_ ?_ ?_
  · rw [← e3]; exact (hc K.ring3m o3 om).symm
  · rw [← e4]; exact hc K.ringm4 om (K.tri.offh.1)
  · exact (hc a4 (P.x_ne_h _) om).symm

/-- At `k = 3`, `m` (adjacent to `x (j+3) = A`, `w₂ = B`, `w₃ = μ`) has colour `α`. -/
theorem m_col_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    c m = c (P.x j) := by
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, e2, e3, -⟩ := hR
  obtain ⟨o3, om⟩ := K.offh
  have a3 : M.graph.Adj (P.x (j + 3)) m := (K.nbr3 m).2 (by simp)
  refine f4_last h1 h3 h4 h13 h14 h34 ?_ ?_ ?_
  · rw [← e3]; exact hc K.ringm3 om o3
  · exact (hc a3 (P.x_ne_h _) om).symm
  · rw [← e2]; exact (hc K.ring2m (K.tri.offh.2.2.2) om).symm

/-! ### 1. The `σ`-image is never doubly locked -/

/-- At `k = 4`, Lock 1 of `σ c` dies at the degree-five vertex `x (j+3)`. -/
theorem sigma_exit_noLock1_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : ¬ Lock1 P (sigSwap P c j) j := by
  have hr := hR.1.1
  rw [lock1_after_sigma_iff K.tri hc hr hR.outer]
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, e2, e3, -⟩ := hR
  refine not_reach_of_isolated ((K.tri.off _).2.2.1) fun v e => ?_
  obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
  rcases (K.nbr3 v).1 ea with rfl | rfl | rfl | rfl | rfl
  · exact hv.1 rfl
  · exact vp rfl
  · rcases hv.2 with f | f
    · exact h4 f
    · exact h34 f.symm
  · have hv2 := hv.2
    rw [e2] at hv2
    rcases hv2 with f | f
    · exact h4 f
    · exact h34 f.symm
  · have hv2 := hv.2
    rw [e3] at hv2
    rcases hv2 with f | f
    · exact h1 f
    · exact h13 f

/-- At `k = 3`, Lock 2 of `σ c` dies at the degree-five vertex `x (j+4)`. -/
theorem sigma_exit_noLock2_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : ¬ Lock2 P (sigSwap P c j) j := by
  have hr := hR.1.1
  rw [lock2_after_sigma_iff K.tri hc hr hR.outer]
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, -, e3, e4⟩ := hR
  refine not_reach_of_isolated ((K.tri.off _).2.1) fun v e => ?_
  obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
  rcases (K.nbr4 v).1 ea with rfl | rfl | rfl | rfl | rfl
  · exact hv.1 rfl
  · rcases hv.2 with f | f
    · exact h3 f
    · exact h34 f
  · exact vp rfl
  · have hv2 := hv.2
    rw [e3] at hv2
    rcases hv2 with f | f
    · exact h1 f
    · exact h14 f
  · have hv2 := hv.2
    rw [e4] at hv2
    rcases hv2 with f | f
    · exact h3 f
    · exact h34 f

/-- **(1), `k = 4`.** A `σ`-exit at `k = 4` is never doubly locked. -/
theorem sigma_exit_not_DL_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : ¬ DLState P (sigSwap P c j) := by
  obtain ⟨-, -, r', -⟩ := sigSwap_basic hc hR.1.1
  rw [dl_rep r']
  exact fun H => sigma_exit_noLock1_k4 K hc hR H.1

/-- **(1), `k = 3`.** A `σ`-exit at `k = 3` is never doubly locked. -/
theorem sigma_exit_not_DL_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : ¬ DLState P (sigSwap P c j) := by
  obtain ⟨-, -, r', -⟩ := sigSwap_basic hc hR.1.1
  rw [dl_rep r']
  exact fun H => sigma_exit_noLock2_k3 K hc hR H.2

/-! ### 2. The exit criteria (in `c`, before the swap) -/

/-- At `k = 4`: `σ c` has Lock 2 iff `w₀` reaches `m` in `K_B − x₀` (the `{α, B}`-graph of `c`
with `x j` deleted). The only `K_B − x₀`-neighbour of `p = x (j+4)` is `m`. -/
theorem lock2_after_sigma_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    Lock2 P (sigSwap P c j) j ↔
      (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)).Reachable (w j) m := by
  have cm := m_col_k4 K hc hR
  rw [lock2_after_sigma_iff K.tri hc hR.1.1 hR.outer]
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, -, e3, e4⟩ := hR
  obtain ⟨f40, -, -, -, -⟩ := fneK j
  constructor
  · refine reach_of_only ((K.tri.off _).2.1) fun v e => ?_
    obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
    rcases (K.nbr4 v).1 ea with rfl | rfl | rfl | rfl | rfl | rfl
    · exact (hv.1 rfl).elim
    · rcases hv.2 with f | f
      · exact (h3 f).elim
      · exact (h34 f).elim
    · exact (vp rfl).elim
    · have hv2 := hv.2
      rw [e3] at hv2
      rcases hv2 with f | f
      · exact (h1 f).elim
      · exact (h14 f).elim
    · rfl
    · have hv2 := hv.2
      rw [e4] at hv2
      rcases hv2 with f | f
      · exact (h3 f).elim
      · exact (h34 f).elim
  · intro r
    exact r.trans (Adj.reachable ⟨⟨((K.nbr4 m).2 (by simp)).symm, ⟨K.offh.2, Or.inl cm⟩,
      ⟨P.x_ne_h _, Or.inr rfl⟩⟩, K.offm j, fun e => f40 (P.inj e)⟩)

/-- **(2), `k = 4`.** `σ c` is lockless iff `w₀` does not reach `m` in `K_B − x₀`; otherwise it
has exactly Lock 2 (Lock 1 always dies). By the duality (D) of `NightC1Gamma.md` §2 (not
formalised) the right side is the note's `w₄ ∈ K_{μ,A}(x₁)`. -/
theorem sigma_exit_criterion_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    NoLock P (sigSwap P c j) ↔
      ¬ (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)).Reachable (w j) m := by
  obtain ⟨-, -, r', -⟩ := sigSwap_basic hc hR.1.1
  rw [noLock_rep r', lock2_after_sigma_k4 K hc hR]
  exact ⟨fun H => H.2, fun H => ⟨sigma_exit_noLock1_k4 K hc hR, H⟩⟩

/-- At `k = 3`: `σ c` has Lock 1 iff `w₁` reaches `m` in `K_F − x₂` (the `{α, A}`-graph of `c`
with `x (j+2)` deleted). The only `K_F − x₂`-neighbour of `p = x (j+3)` is `m`. -/
theorem lock1_after_sigma_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    Lock1 P (sigSwap P c j) j ↔
      (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))).Reachable
        (w (j + 1)) m := by
  have cm := m_col_k3 K hc hR
  rw [lock1_after_sigma_iff K.tri hc hR.1.1 hR.outer]
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, e2, e3, -⟩ := hR
  obtain ⟨-, f32, -, -, -⟩ := fneK j
  constructor
  · refine reach_of_only ((K.tri.off _).2.2.1) fun v e => ?_
    obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
    rcases (K.nbr3 v).1 ea with rfl | rfl | rfl | rfl | rfl | rfl
    · exact (hv.1 rfl).elim
    · exact (vp rfl).elim
    · rcases hv.2 with f | f
      · exact (h4 f).elim
      · exact (h34 f.symm).elim
    · have hv2 := hv.2
      rw [e2] at hv2
      rcases hv2 with f | f
      · exact (h4 f).elim
      · exact (h34 f.symm).elim
    · rfl
    · have hv2 := hv.2
      rw [e3] at hv2
      rcases hv2 with f | f
      · exact (h1 f).elim
      · exact (h13 f).elim
  · intro r
    exact r.trans (Adj.reachable ⟨⟨((K.nbr3 m).2 (by simp)).symm, ⟨K.offh.2, Or.inl cm⟩,
      ⟨P.x_ne_h _, Or.inr rfl⟩⟩, K.offm _, fun e => f32 (P.inj e)⟩)

/-- **(2), `k = 3`.** `σ c` is lockless iff `w₁` does not reach `m` in `K_F − x₂`; otherwise it
has exactly Lock 1 (Lock 2 always dies). By (D) (not formalised) the right side is the note's
`w₂ ∈ K_{μ,B}(x₁)`. -/
theorem sigma_exit_criterion_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    NoLock P (sigSwap P c j) ↔
      ¬ (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))).Reachable
        (w (j + 1)) m := by
  obtain ⟨-, -, r', -⟩ := sigSwap_basic hc hR.1.1
  rw [noLock_rep r', lock1_after_sigma_k3 K hc hR]
  exact ⟨fun H => H.1, fun H => ⟨H, sigma_exit_noLock2_k3 K hc hR⟩⟩

/-! ### 3. The excursion after the exit -/

/-- At `k = 4` a lockless `σ`-image steps to a filled state (`φ_B⁻¹`), i.e. `f ≥ 1`. -/
theorem sigma_exit_filled_k4 (hc : ProperOff M.graph h c) (hR : R3At P w c j)
    (hN : NoLock P (sigSwap P c j)) : Target M.graph h (piMove P (sigSwap P c j)) := by
  obtain ⟨-, ps, r', -⟩ := sigSwap_basic hc hR.1.1
  have hl := ((noLock_rep r').1 hN).2
  rw [piMove_rep r', ite_eq_right hl]
  exact (phiBinv_spec ps r' hl).2.2.1.1

/-- **(3), `k = 3`.** If `w₂` lies in the `{μ, B}`-component of `x₁` in `c` (the note's
criterion; by (D) equivalent to `σ c` lockless), then `π (σ c)` and `π (π (σ c))` are filled:
the excursion entered at `σ c` has `f ≥ 2`. -/
theorem sigma_exit_f_ge_two_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j)
    (hK : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 1)) (w (j + 2))) :
    Target M.graph h (piMove P (sigSwap P c j)) ∧
      Target M.graph h (piMove P (piMove P (sigSwap P c j))) := by
  have T := K.tri
  have noL2 := sigma_exit_noLock2_k3 K hc hR
  obtain ⟨Kt, -, -, -, sout⟩ := sigma_exit T hc hR.1.1 hR.outer
  obtain ⟨-, ps, rs, s0, s1, s2, s3, s4⟩ := sigSwap_basic hc hR.1.1
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -, -⟩, e0, e1, e2, e3, e4⟩ := hR
  obtain ⟨-, -, f14, f24, f34⟩ := fneK j
  obtain ⟨-, a00, a10, -, -, a22⟩ := T.adjs
  obtain ⟨o4, o0, o1, o2⟩ := T.offh
  have sw : ∀ {u}, (∀ i, u ≠ P.x i) → sigSwap P c j u = c u :=
    fun hu => sout _ (hu _) (hu _) (hu _)
  -- `π (σ c) = φ_B⁻¹ (σ c)`, a filled state `t`.
  rw [piMove_rep rs, ite_eq_right noL2]
  obtain ⟨-, pt, st, -, -⟩ := phiBinv_spec ps rs noL2
  refine ⟨st.1, ?_⟩
  -- The `{α, B}`-component of `x (j+4)` in `σ c` is `{x (j+4)}`.
  have iso : ∀ u, ¬ (pairGraph M.graph h (sigSwap P c j) (sigSwap P c j (P.x (j + 1)))
      (sigSwap P c j (P.x (j + 4)))).Adj (P.x (j + 4)) u := by
    rintro u ⟨ea, -, au⟩
    have au2 := au.2
    rw [s1, s4] at au2
    rcases (K.nbr4 u).1 ea with rfl | rfl | rfl | rfl | rfl
    · exact au.1 rfl
    · rw [s3] at au2
      rcases au2 with f | f
      · exact h3 f
      · exact h34 f
    · rw [s0] at au2
      rcases au2 with f | f
      · exact h1 f
      · exact h14 f
    · rw [sw K.off3, e3] at au2
      rcases au2 with f | f
      · exact h1 f
      · exact h14 f
    · rw [sw fun i => (T.off i).1, e4] at au2
      rcases au2 with f | f
      · exact h3 f
      · exact h34 f
  have tout : ∀ {v}, v ≠ P.x (j + 4) →
      phiBinv P (sigSwap P c j) j v = sigSwap P c j v :=
    fun hv => kswap_out fun r => not_reach_of_isolated hv iso r.symm
  have toff : ∀ {v}, v ≠ P.x j → v ≠ P.x (j + 1) → v ≠ P.x (j + 2) → v ≠ P.x (j + 4) →
      phiBinv P (sigSwap P c j) j v = c v :=
    fun a b d e => (tout e).trans (sout _ a b d)
  have tv0 : phiBinv P (sigSwap P c j) j (P.x j) = c (P.x (j + 1)) :=
    (tout fun e => (fneK j).1 (P.inj e).symm).trans s0
  have tv1 : phiBinv P (sigSwap P c j) j (P.x (j + 1)) = c (P.x j) :=
    (tout fun e => f14 (P.inj e)).trans s1
  have tv2 : phiBinv P (sigSwap P c j) j (P.x (j + 2)) = c (P.x (j + 1)) :=
    (tout fun e => f24 (P.inj e)).trans s2
  have tv3 : phiBinv P (sigSwap P c j) j (P.x (j + 3)) = c (P.x (j + 3)) :=
    (tout fun e => f34 (P.inj e)).trans s3
  have tv4 : phiBinv P (sigSwap P c j) j (P.x (j + 4)) = c (P.x j) :=
    (kswap_mem' (Reachable.refl _) rfl).trans s1
  -- `M3` is long at `t`: `x j` reaches `x (j+2)` in the `{μ, B}`-graph of `t`.
  have R : (pairGraph M.graph h (phiBinv P (sigSwap P c j) j) (c (P.x (j + 1)))
      (c (P.x (j + 4)))).Reachable (P.x j) (P.x (j + 2)) := by
    set t := phiBinv P (sigSwap P c j) j with ht
    have key := reachable_invariant (H := pairGraph M.graph h c (c (P.x (j + 1)))
      (c (P.x (j + 4))))
      (P := fun u => u = P.x (j + 1) ∨
        (pairGraph M.graph h t (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x j) u ∨
        (u = P.x (j + 4) ∧ (pairGraph M.graph h t (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
          (P.x j) (w (j + 3)))) ?_ (Or.inl rfl) hK
    · rcases key with e | e | ⟨e, -⟩
      · exact absurd e ((T.off _).2.2.2)
      · exact e.trans (Adj.reachable ⟨a22.symm,
          ⟨o2, Or.inr (by rw [toff ((T.off _).2.2.2) ((T.off _).2.2.2) ((T.off _).2.2.2)
            ((T.off _).2.2.2), e2])⟩, ⟨P.x_ne_h _, Or.inl tv2⟩⟩)
      · exact absurd e ((T.off _).2.2.2)
    · intro u v e hu
      obtain ⟨ea, au, av⟩ := e
      have notA : ∀ {x}, c x = c (P.x j) →
          ¬ (c x = c (P.x (j + 1)) ∨ c x = c (P.x (j + 4))) := by
        rintro x hx (f | f)
        · exact h1 (f.symm.trans hx)
        · exact h4 (f.symm.trans hx)
      have notAA : ∀ {x}, c x = c (P.x (j + 3)) →
          ¬ (c x = c (P.x (j + 1)) ∨ c x = c (P.x (j + 4))) := by
        rintro x hx (f | f)
        · exact h13 (f.symm.trans hx)
        · exact h34 (hx.symm.trans f)
      rcases hu with rfl | hu | ⟨rfl, hw⟩
      · rcases (T.nbr1 v).1 ea with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl av.1
        · exact absurd av.2 (notA rfl)
        · exact absurd av.2 (notA h02.symm)
        · exact Or.inr (Or.inl (Adj.reachable ⟨a00, ⟨P.x_ne_h _, Or.inl tv0⟩,
            ⟨o0, Or.inr (by rw [toff ((T.off _).2.1) ((T.off _).2.1) ((T.off _).2.1)
              ((T.off _).2.1), e0])⟩⟩))
        · exact absurd av.2 (notAA e1)
      · have u0 : u ≠ P.x j := by
          rintro rfl
          exact notA rfl au.2
        have u2 : u ≠ P.x (j + 2) := by
          rintro rfl
          exact notA h02.symm au.2
        have tu := reach_active hu u0.symm
        have u1 : u ≠ P.x (j + 1) := by
          rintro rfl
          have tu2 := tu.2
          rw [tv1] at tu2
          rcases tu2 with f | f
          · exact h1 f.symm
          · exact h4 f.symm
        have u4 : u ≠ P.x (j + 4) := by
          rintro rfl
          have tu2 := tu.2
          rw [tv4] at tu2
          rcases tu2 with f | f
          · exact h1 f.symm
          · exact h4 f.symm
        by_cases v4 : v = P.x (j + 4)
        · subst v4
          rcases (K.nbr4 u).1 ea.symm with rfl | rfl | rfl | rfl | rfl
          · exact absurd rfl au.1
          · exact absurd au.2 (notAA rfl)
          · exact absurd rfl u0
          · exact Or.inr (Or.inr ⟨rfl, hu⟩)
          · exact absurd au.2 (notAA e4)
        by_cases v1 : v = P.x (j + 1)
        · exact Or.inl v1
        have v0 : v ≠ P.x j := by
          rintro rfl
          exact notA rfl av.2
        have v2 : v ≠ P.x (j + 2) := by
          rintro rfl
          exact notA h02.symm av.2
        exact Or.inr (Or.inl (hu.trans (Adj.reachable ⟨ea, tu,
          ⟨av.1, by rw [toff v0 v1 v2 v4]; exact av.2⟩⟩)))
      · rcases (K.nbr4 v).1 ea with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl av.1
        · exact absurd av.2 (notAA rfl)
        · exact absurd av.2 (notA rfl)
        · exact Or.inr (Or.inl hw)
        · exact absurd av.2 (notAA e4)
  have hm : ¬ M3Short P (phiBinv P (sigSwap P c j) j) (j + 3) := by
    have hz : zcol P (phiBinv P (sigSwap P c j) j) (j + 3) = c (P.x (j + 4)) := by
      unfold zcol
      simp only [add_assoc, Fin.reduceAdd, add_zero]
      rw [tv3, tv4, tv0]
      exact fourth_eq h3 (Ne.symm h13) (Ne.symm h1) (Ne.symm h34) h4 (Ne.symm h14)
    unfold M3Short
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    rw [tv0]
    exact fun H => H R
  rw [piMove_single pt st, ite_eq_right hm]
  exact (tau_spec pt st hm).2.2.1.1

/-- **Not asserted.** `f ≥ 2` at `k = 4` (`NightF6.md` §2): a lockless `σ`-image at a `k = 4`
`R3` state steps to two filled states. The note's proof uses a closed `{μ,A}`-walk separating
`x₁` from `x₃, x₄` in `π (σ c)` and the duality (D) twice; neither is formalised. -/
def FGeTwoK4Statement : Prop :=
  ∀ {n : ℕ} {M : SphericalMap n} {h : Fin n} (P : Pent M.graph h) (w : Fin 5 → Fin n)
    (m : Fin n) (c : Fin n → Fin 4) (j : Fin 5), M.Triangulated → K4Ball P w m j →
    ProperOff M.graph h c → R3At P w c j → NoLock P (sigSwap P c j) →
    Target M.graph h (piMove P (sigSwap P c j)) ∧
      Target M.graph h (piMove P (piMove P (sigSwap P c j)))

end sphere

end SimpleGraph.QuarterFloor
