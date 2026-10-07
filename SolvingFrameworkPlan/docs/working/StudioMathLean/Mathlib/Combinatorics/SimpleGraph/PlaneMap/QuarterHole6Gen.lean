/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterHole6Clean

/-!
# Weak F6 at `(5,5,5,5,d)` holes for every `d ≥ 6`

Generalises `QuarterHole6Clean.pureClean_of_hole6` from the `(5,5,5,5,6)` link to a link with
four consecutive degree-five vertices and the fifth vertex `p = x q` of **any** degree
`d = ms.length + 5 ≥ 6`, with outer path `y = w (q+4), m₁, …, m_{d-5}, z = w q`.

## Where "degree exactly six" was used

An audit of the `(5,5,5,5,6)` chain shows that the inserted vertex `m` (and the exact
neighbourhood of `x (j+4)`) enters only in:

* `m_col_k4` / `m_col_k3` (Lemma D, `m = α`) and the exit criteria `lock2_after_sigma_k4`,
  `lock1_after_sigma_k3` ("the only `K_B − x₀`-neighbour of `p` is `m`");
* the `m`-carriers of `pair_own` (`R1k1 (m,y)`, `R3k3 (m,p)`, `R1k4 (y,m)`, `R3k1 (m,z)`,
  `R1k2 (p,m)`) and the **first** component of `pair_R3k4_of_pred`.

None of these is used by `pureClean_of_hole6`:

* `sigma_exit_not_DL_k4` uses only `TripleBallP` at `j` and the degree-five neighbourhood of
  `x (j+3)` (Lock 1 of `σ c` dies at `x (j+3)`); `K4Ball.nbr4`, `m`, and the ring edges at `m`
  are never touched.
* `tk_step` (`r1_step`, `r1_ring`, `r3_step`) and `untyped_dd` use the degree-five
  neighbourhoods of the four vertices `x t`, `t ≠ q`, the ring edges `w t ~ w (t+1)` with
  `t + 1 ≠ q`, and the two edges `x q ~ w q`, `x q ~ w (q+4)`; never `m` or `nbrq`.
* `r3k4_R3At` needs only `c (w q) = A` at the `R3k4` state, which is the **second** component of
  `pair_R3k4_of_pred`; its proof uses only `r1_ring` and the `μ`-neighbour of `x (j+3)`.

So no step needs `d = 6` and there is no residual hypothesis.

## Main results (sorry-free, no new axioms)

* `Hole4 P w q`: the minimal hypothesis (four degree-five link vertices `x t`, `t ≠ q`, the ring
  edges not ending at `w q` from the left, `x q ~ w q`, `x q ~ w (q+4)`, `w` off `N[h]`).
  `Hole6.toHole4`, `Hole6Gen.toHole4`.
* `Hole6Gen P w ms q`: the `(5,5,5,5,d)` hole, `d = ms.length + 5 ≥ 6` (`ms ≠ []`), with the
  exact neighbourhood of `x q` and the outer path `w (q+4) :: ms ++ [w q]`. `Hole6.toHole6Gen`
  (`ms = [m]`).
* `K4BallGen P w ms j` and `sigma_exit_not_DL_k4_gen`: at an `R3` state at `k = 4` the `σ`-image
  is never doubly locked, for every `d ≥ 6` (via `sigma_exit_not_DL_k4_core`, which needs no
  hypothesis on `x (j+4)` beyond `TripleBallP`).
* `untyped_dd4`, `typed_in_orbit4`, `tk_step4`, `pair_R3k4_z4`, `r3k4_R3At4`: the orbit facts.
* `gammaImages_of_hole4`, `pureClean_of_hole4`, **`pureClean_of_hole6gen`**: every Kempe class
  at such a hole has a filled state.

## What this does NOT give

* Not the quarter floor; not the `pair_own` carrier table or `gamma_period_ten` for `d ≥ 7`
  (the `m`-carriers need a single inserted vertex; only the `(type, k)` transition table
  `tk_step4` is generalised, which is all the weak F6 argument uses).
* Not `(5,5,5,6,6)` or holes with fewer than four consecutive degree-five link vertices.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

private lemma gstep_to_R1k2' : ∀ t : GType, ∀ k : Fin 5, ∃ d, d < 10 ∧
    gstep^[d] (t, k) = (.R1, 2) := by
  intro t; cases t <;> decide

private lemma q_two_three' : ∀ j q : Fin 5, (q = j + 2 ∨ q = j + 3) →
    (q = j + 3 + 1 ∨ q = j + 3 + 2 ∨ q = j + 3 + 3) → False := by decide

private lemma q_k4' : ∀ j : Fin 5, j + 2 = j + 3 + 4 := by decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-! ### The hypotheses -/

/-- Four consecutive degree-five link vertices: every `x t`, `t ≠ q`, has neighbours
`h, x (t-1), x (t+1), w (t-1), w t`; the ring edges `w t ~ w (t+1)` with `t + 1 ≠ q`; the edges
`x q ~ w q`, `x q ~ w (q+4)`; `w` off the link and off `h`. Nothing about the degree of
`x q`. -/
structure Hole4 (P : Pent M.graph h) (w : Fin 5 → Fin n) (q : Fin 5) : Prop where
  nbr : ∀ t, t ≠ q → ∀ u, M.graph.Adj (P.x t) u ↔
    u = h ∨ u = P.x (t + 4) ∨ u = P.x (t + 1) ∨ u = w (t + 4) ∨ u = w t
  adjq : M.graph.Adj (P.x q) (w q)
  adjq4 : M.graph.Adj (P.x q) (w (q + 4))
  ring : ∀ t, t + 1 ≠ q → M.graph.Adj (w t) (w (t + 1))
  off : ∀ t i, w t ≠ P.x i
  offh : ∀ t, w t ≠ h

/-- A `(5,5,5,5,d)` hole, `d = ms.length + 5 ≥ 6`: `x q` has neighbours
`h, x (q+4), x (q+1), w (q+4), ms, w q`, with outer path `w (q+4), m₁, …, m_{d-5}, w q`; every
other link vertex has degree five. -/
structure Hole6Gen (P : Pent M.graph h) (w : Fin 5 → Fin n) (ms : List (Fin n)) (q : Fin 5) :
    Prop where
  ne : ms ≠ []
  nbr : ∀ t, t ≠ q → ∀ u, M.graph.Adj (P.x t) u ↔
    u = h ∨ u = P.x (t + 4) ∨ u = P.x (t + 1) ∨ u = w (t + 4) ∨ u = w t
  nbrq : ∀ u, M.graph.Adj (P.x q) u ↔
    u = h ∨ u = P.x (q + 4) ∨ u = P.x (q + 1) ∨ u = w (q + 4) ∨ u ∈ ms ∨ u = w q
  ring : ∀ t, t + 1 ≠ q → M.graph.Adj (w t) (w (t + 1))
  path : List.IsChain M.graph.Adj (w (q + 4) :: (ms ++ [w q]))
  off : ∀ t i, w t ≠ P.x i
  offm : ∀ v ∈ ms, ∀ i, v ≠ P.x i
  offh : ∀ t, w t ≠ h
  offmh : ∀ v ∈ ms, v ≠ h

/-- The `k = 4` ball at any degree `d = ms.length + 5 ≥ 6` of `p = x (j+4)`: the triple ball at
`j`, `x (j+3)` of degree five, `p` with neighbours `h, x (j+3), x j, w₃, ms, w₄` (outer path
`x (j+3), w₃, m₁, …, m_{d-5}, w₄, x j`). -/
structure K4BallGen (P : Pent M.graph h) (w : Fin 5 → Fin n) (ms : List (Fin n)) (j : Fin 5) :
    Prop where
  tri : TripleBallP P w j
  nbr3 : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
    u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3)
  nbr4 : ∀ u, M.graph.Adj (P.x (j + 4)) u ↔
    u = h ∨ u = P.x (j + 3) ∨ u = P.x j ∨ u = w (j + 3) ∨ u ∈ ms ∨ u = w (j + 4)
  ring23 : M.graph.Adj (w (j + 2)) (w (j + 3))
  path : List.IsChain M.graph.Adj (w (j + 3) :: (ms ++ [w (j + 4)]))
  ne : ms ≠ []
  off3 : ∀ i, w (j + 3) ≠ P.x i
  offm : ∀ v ∈ ms, ∀ i, v ≠ P.x i
  offh : w (j + 3) ≠ h ∧ ∀ v ∈ ms, v ≠ h

variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {ms : List (Fin n)} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

theorem Hole6Gen.toHole4 (H : Hole6Gen P w ms q) : Hole4 P w q :=
  ⟨H.nbr, (H.nbrq _).2 (by simp), (H.nbrq _).2 (by simp), H.ring, H.off, H.offh⟩

theorem Hole6.toHole4 (H : Hole6 P w m q) : Hole4 P w q :=
  ⟨H.nbr, H.adj_w q, H.adj_w4 q, H.ring, H.off, H.offh⟩

/-- The `(5,5,5,5,6)` hole is the case `ms = [m]`. -/
theorem Hole6.toHole6Gen (H : Hole6 P w m q) : Hole6Gen P w [m] q :=
  ⟨by simp, H.nbr, fun u => by simpa using H.nbrq u, H.ring,
    .cons_cons H.ringy (.cons_cons H.ringz (.singleton _)), H.off,
    fun v hv => by rw [List.mem_singleton.1 hv]; exact H.offm,
    H.offh, fun v hv => by rw [List.mem_singleton.1 hv]; exact H.offmh⟩

namespace Hole4

lemma adj_w (H : Hole4 P w q) (t : Fin 5) : M.graph.Adj (P.x t) (w t) := by
  by_cases ht : t = q
  · subst ht; exact H.adjq
  · exact (H.nbr t ht _).2 (by simp)

lemma adj_w4 (H : Hole4 P w q) (t : Fin 5) : M.graph.Adj (P.x t) (w (t + 4)) := by
  by_cases ht : t = q
  · subst ht; exact H.adjq4
  · exact (H.nbr t ht _).2 (by simp)

lemma adj_w' (H : Hole4 P w q) (t : Fin 5) : M.graph.Adj (P.x (t + 1)) (w t) := by
  have e := H.adj_w4 (t + 1)
  rwa [add_assoc, show (1 : Fin 5) + 4 = 0 from rfl, add_zero] at e

lemma dom (H : Hole4 P w q) (hc : ProperOff M.graph h c) (t : Fin 5) :
    c (w t) ≠ c (P.x t) ∧ c (w t) ≠ c (P.x (t + 1)) :=
  ⟨(hc (H.adj_w t) (P.x_ne_h _) (H.offh t)).symm,
    (hc (H.adj_w' t) (P.x_ne_h _) (H.offh t)).symm⟩

lemma domAt (H : Hole4 P w q) (hc : ProperOff M.graph h c) {a b : Fin 5} (hab : a + 1 = b) :
    c (w (j + a)) ≠ c (P.x (j + a)) ∧ c (w (j + a)) ≠ c (P.x (j + b)) := by
  have d := H.dom hc (j + a)
  rwa [add_assoc, hab] at d

lemma ring0 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hq : j + 1 ≠ q) :
    c (w j) ≠ c (w (j + 1)) :=
  hc (H.ring j hq) (H.offh _) (H.offh _)

lemma ringAt (H : Hole4 P w q) (hc : ProperOff M.graph h c) {a b : Fin 5} (hab : a + 1 = b)
    (hq : j + b ≠ q) : c (w (j + a)) ≠ c (w (j + b)) := by
  have e := H.ring (j + a) (by rwa [add_assoc, hab])
  rw [add_assoc, hab] at e
  exact hc e (H.offh _) (H.offh _)

lemma ring4 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hq : j ≠ q) :
    c (w (j + 4)) ≠ c (w j) := by
  have e := H.ring (j + 4) (by rwa [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero])
  rw [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero] at e
  exact hc e (H.offh _) (H.offh _)

/-- At `q = j + 4`: the triple ball at `j`. -/
theorem triple (H : Hole4 P w q) (hq : q = j + 4) : TripleBallP P w j := by
  subst hq
  have n0 := H.nbr j (fin5_ne0 (by decide))
  have n1 := H.nbr (j + 1) (fin5_ne (by decide))
  have n2 := H.nbr (j + 2) (fin5_ne (by decide))
  have g40 := H.ring (j + 4) (by rw [add_assoc]; exact fin5_ne (by decide))
  have g01 := H.ring j (fin5_ne (by decide))
  have g12 := H.ring (j + 1) (by rw [add_assoc]; exact fin5_ne (by decide))
  have a3 := H.adj_w4 (j + 3)
  simp only [add_assoc, Fin.reduceAdd, add_zero] at n1 n2 g40 g12 a3
  exact ⟨n0, n1, n2, g40, g01, g12, H.adj_w (j + 4), a3,
    fun i => ⟨H.off _ i, H.off _ i, H.off _ i, H.off _ i⟩,
    ⟨H.offh _, H.offh _, H.offh _, H.offh _⟩⟩

/-- At `q = j + 4`: `x (j+3)` has degree five. -/
theorem nbr3 (H : Hole4 P w q) (hq : q = j + 4) : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
    u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3) := by
  subst hq
  have n3 := H.nbr (j + 3) (fin5_ne (by decide))
  simp only [add_assoc, Fin.reduceAdd] at n3
  exact n3

end Hole4

/-- At `q = j + 4` the `Hole6Gen` hypothesis gives the `K4BallGen`. -/
theorem Hole6Gen.k4BallGen (H : Hole6Gen P w ms q) (hq : q = j + 4) : K4BallGen P w ms j := by
  have T := H.toHole4.triple hq
  have n3 := H.toHole4.nbr3 hq
  subst hq
  have n4 := H.nbrq
  have g23 := H.ring (j + 2) (by rw [add_assoc]; exact fin5_ne (by decide))
  have pa := H.path
  simp only [add_assoc, Fin.reduceAdd, add_zero] at n4 g23 pa
  exact ⟨T, n3, n4, g23, pa, H.ne, H.off _, H.offm, ⟨H.offh _, H.offmh⟩⟩

/-! ### 1. The `σ`-image at `k = 4` is never doubly locked, at every degree -/

/-- Lock 1 of `σ c` at an `R3` state dies at `x (j+3)`, using only the triple ball at `j` and
the degree-five neighbourhood of `x (j+3)`: no hypothesis on `x (j+4)`. -/
theorem sigma_exit_noLock1_core (T : TripleBallP P w j)
    (nbr3 : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
      u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3))
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) : ¬ Lock1 P (sigSwap P c j) j := by
  have hr := hR.1.1
  rw [lock1_after_sigma_iff T hc hr hR.outer]
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, e2, e3, -⟩ := hR
  refine not_reach_of_isolated ((T.off _).2.2.1) fun v e => ?_
  obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
  rcases (nbr3 v).1 ea with rfl | rfl | rfl | rfl | rfl
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

theorem sigma_exit_not_DL_k4_core (T : TripleBallP P w j)
    (nbr3 : ∀ u, M.graph.Adj (P.x (j + 3)) u ↔
      u = h ∨ u = P.x (j + 2) ∨ u = P.x (j + 4) ∨ u = w (j + 2) ∨ u = w (j + 3))
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) : ¬ DLState P (sigSwap P c j) := by
  obtain ⟨-, -, r', -⟩ := sigSwap_basic hc hR.1.1
  rw [dl_rep r']
  exact fun H => sigma_exit_noLock1_core T nbr3 hc hR H.1

/-- **(1), `k = 4`, any degree `d ≥ 6`.** A `σ`-exit at `k = 4` is never doubly locked. -/
theorem sigma_exit_not_DL_k4_gen (K : K4BallGen P w ms j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : ¬ DLState P (sigSwap P c j) :=
  sigma_exit_not_DL_k4_core K.tri K.nbr3 hc hR

/-! ### 2. The orbit facts under `Hole4` -/

lemma r1_w1_ring4 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hT : TypeR1 P w c j) (hq : j + 1 ≠ q) : c (w (j + 1)) = c (P.x (j + 4)) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have r := H.ring0 hc hq
  obtain ⟨d1, d2⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  unfold TypeR1 at hT
  omega

lemma r1_w3_chain4 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hw1 : c (w (j + 1)) = c (P.x (j + 4))) (hq2 : j + 2 ≠ q) (hq3 : j + 3 ≠ q) :
    c (w (j + 3)) = c (P.x j) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl hq2
  have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl hq3
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  omega

lemma r1_w3_I34 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (hT : TypeR1 P w c j) (hq4 : j + 4 ≠ q) (hq0 : j ≠ q) : c (w (j + 3)) = c (P.x j) := by
  obtain ⟨-, hr, hK, -, -, ⟨u, hu, huh, hcu⟩⟩ := dd_ends hc hD
  obtain ⟨v0, -, -, v3, -⟩ := rot3_values hr hK
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  unfold TypeR1 at hT
  by_contra hne
  have n4 := (H.nbr (j + 4) hq4 u).1 hu
  simp only [add_assoc, Fin.reduceAdd, add_zero] at n4
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  rcases n4 with rfl | rfl | rfl | rfl | rfl
  · exact huh rfl
  · rw [v3] at hcu; exact h3 hcu.symm
  · rw [v0] at hcu; exact h3 hcu.symm
  · rw [rot3_keep hne d3] at hcu; exact d3 hcu
  · rw [rot3_K0 hK (H.adj_w4 j) (H.offh _)] at hcu
    exact H.ring4 hc hq0 (hcu.trans hT.symm)

lemma r1_w1_k14 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (hT : TypeR1 P w c j) (hq2 : j + 2 ≠ q) (hq3 : j + 3 ≠ q) (hq4 : j + 4 ≠ q)
    (hq0 : j ≠ q) : c (w (j + 1)) = c (P.x (j + 4)) := by
  have w3 := r1_w3_I34 H hc hD hT hq4 hq0
  obtain ⟨-, hr, hK, ⟨u', hu', hu'h, hcu'⟩, ⟨u, hu, huh, hcu⟩, -⟩ := dd_ends hc hD
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  by_contra hne
  have hA : c (w (j + 1)) = c (P.x (j + 3)) := by omega
  have w2 : c (w (j + 2)) = c (P.x (j + 4)) := by
    have n2 := (H.nbr (j + 2) hq2 u).1 hu
    simp only [add_assoc, Fin.reduceAdd] at n2
    rcases n2 with rfl | rfl | rfl | rfl | rfl
    · exact (huh rfl).elim
    · rw [v1] at hcu; exact (h14 hcu).elim
    · rw [v3] at hcu; exact (h4 hcu.symm).elim
    · have e := H.adj_w' (j + 1)
      simp only [add_assoc, Fin.reduceAdd] at e
      rw [rot3_K2 hr' e (H.offh _) (Or.inr hA), hA, Equiv.swap_apply_right] at hcu
      exact (h4 hcu.symm).elim
    · rwa [rot3_keep (by omega) d2'] at hcu
  have n3 := (H.nbr (j + 3) hq3 u').1 hu'
  simp only [add_assoc, Fin.reduceAdd] at n3
  rcases n3 with rfl | rfl | rfl | rfl | rfl
  · exact hu'h rfl
  · exact h1 (hcu'.symm.trans h02.symm)
  · exact h14 hcu'.symm
  · exact h14 (hcu'.symm.trans w2)
  · exact h1 (hcu'.symm.trans w3)

/-- The ring of an `R1` `DD` state at any `k`: `w (j+1) = B`, `w (j+3) = α`. -/
theorem r1_ring4 {k : Fin 5} (H : Hole4 P w q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) :
    c (w (j + 1)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x j) := by
  subst hq
  have hr := hD.1.1
  obtain rfl | rfl | rfl | rfl | rfl := fin5_five k
  · have w1 := r1_w1_ring4 H hc hr hT (fin5_ne (by decide))
    exact ⟨w1, r1_w3_chain4 H hc hr w1 (fin5_ne (by decide)) (fin5_ne (by decide))⟩
  · exact ⟨r1_w1_k14 H hc hD hT (fin5_ne (by decide)) (fin5_ne (by decide))
      (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide)),
      r1_w3_I34 H hc hD hT (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide))⟩
  · exact ⟨r1_w1_ring4 H hc hr hT (fin5_ne (by decide)),
      r1_w3_I34 H hc hD hT (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide))⟩
  · exact ⟨r1_w1_ring4 H hc hr hT (fin5_ne (by decide)),
      r1_w3_I34 H hc hD hT (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide))⟩
  · have w1 := r1_w1_ring4 H hc hr hT (fin5_ne (by decide))
    exact ⟨w1, r1_w3_chain4 H hc hr w1 (fin5_ne (by decide)) (fin5_ne (by decide))⟩

/-- **`R1 → R3`** at a `Hole4` hole, for every position `k`, when `π c` is `DL`. -/
theorem r1_step4 {k : Fin 5} (H : Hole4 P w q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) : TypeR3 P w (piMove P c) (j + 3) := by
  obtain ⟨w1, w3⟩ := r1_ring4 H hq hc hD hT
  obtain ⟨hπ, hr, hK, -, -, -⟩ := dd_ends hc hD
  obtain ⟨-, -, v2, -, v4⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  unfold TypeR3
  simp only [add_assoc, Fin.reduceAdd, hπ]
  refine ⟨?_, ?_⟩
  · rw [v2, rot3_K3 hr' (H.adj_w (j + 3)) (H.offh _) (Or.inl w3), w3, Equiv.swap_apply_left]
  · rw [v4, rot3_keep (by rw [w1]; exact h4) (by rw [w1]; exact h34.symm), w1]

/-- **The transition table** at a `Hole4` hole: `(type, k) ↦ (flip type, k + 2)`. -/
theorem tk_step4 {t : GType} {k : Fin 5} (H : Hole4 P w q) (hc : ProperOff M.graph h c)
    (hs : HasTK P w q c t k) (hd' : DLState P (piMove P c)) :
    HasTK P w q (piMove P c) t.flip (k + 2) := by
  obtain ⟨j, hd, hq, hT⟩ := hs
  obtain ⟨-, -, r', -, -⟩ := rot3_move hc hd.1 hd.2.2
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hd.1, ite_eq_left hd.2.2]
  rw [← hπ] at r'
  have hd2 : DoublyLocked P (piMove P c) (j + 3) := ⟨r', (dl_rep r').1 hd'⟩
  refine ⟨j + 3, hd2, ?_, ?_⟩
  · rw [hq]
    have e : ∀ a b : Fin 5, a + b = a + 3 + (b + 2) := by decide
    exact e j k
  · cases t
    · exact r1_step4 H hq hc ⟨hd, hd2⟩ hT
    · exact r3_step hd hT

/-- At `π r`, `r` an `R1` `DD` state at `k = 2`: `z = w q` has colour `A` (the `z`-half of
`pair_R3k4_of_pred`, which does not involve the inserted vertices). -/
theorem pair_R3k4_z4 {r : Fin n → Fin 4} (H : Hole4 P w q) (hq : q = j + 2)
    (hc : ProperOff M.graph h r) (hD : DDstate P r j) (hT : TypeR1 P w r j) :
    piMove P r (w q) = piMove P r (P.x (j + 3 + 3)) := by
  subst hq
  obtain ⟨hπ, hr, hK, ⟨u', hu', hu'h, hcu'⟩, -, -⟩ := dd_ends hc hD
  obtain ⟨w1, w3⟩ := r1_ring4 H (k := 2) rfl hc hD hT
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have n3 := (H.nbr (j + 3) (fin5_ne (by decide)) u').1 hu'
  simp only [add_assoc, Fin.reduceAdd] at n3
  have w2 : r (w (j + 2)) = r (P.x (j + 1)) := by
    rcases n3 with rfl | rfl | rfl | rfl | rfl
    · exact (hu'h rfl).elim
    · exact (h1 (hcu'.symm.trans h02.symm)).elim
    · exact (h14 hcu'.symm).elim
    · exact hcu'
    · exact (h1 (hcu'.symm.trans w3)).elim
  simp only [add_assoc, Fin.reduceAdd, hπ]
  rw [v1, rot3_keep (by rw [w2]; exact h1) (by rw [w2]; exact h13), w2]

/-- At an `R3k4` state with `z = A`, the ring is the full `R3` ring. -/
theorem r3k4_R3At4 (H : Hole4 P w q) (hq : q = j + 4) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) (hT : TypeR3 P w c j) (hz : c (w q) = c (P.x (j + 3))) :
    R3At P w c j := by
  subst hq
  obtain ⟨t0, t3⟩ := hT
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
  have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hd.1
  refine ⟨hd, t0, ?_, ?_, t3, hz⟩
  · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r01 t0; omega
  · clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega

/-- An untyped `DD` state at a `Hole4` hole: `x q` is at `k = 1` and the image is `R3`, or at
`k ∈ {2, 3}`. -/
theorem untyped_dd4 (H : Hole4 P w q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (n1 : ¬ TypeR1 P w c j) (n3 : ¬ TypeR3 P w c j) :
    (q = j + 1 ∧ TypeR3 P w (piMove P c) (j + 3)) ∨ q = j + 2 ∨ q = j + 3 := by
  obtain ⟨hπ, hr, hK, ⟨u', hu', hu'h, hcu'⟩, ⟨u, hu, huh, hcu⟩, -⟩ := dd_ends hc hD
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨d0, d0'⟩ := H.dom hc j
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  have a0 : c (w j) = c (P.x (j + 4)) := by
    unfold TypeR1 at n1
    clear * - h1 h3 h4 h13 h14 h34 h02 d0 d0' n1; omega
  have a3 : c (w (j + 3)) = c (P.x j) := by
    have n3' : c (w (j + 3)) ≠ c (P.x (j + 1)) := fun e => n3 ⟨a0, e⟩
    clear * - h1 h3 h4 h13 h14 h34 h02 d3 d3' n3'; omega
  have core : j + 3 ≠ q → j + 2 ≠ q → c (w (j + 1)) = c (P.x (j + 4)) := by
    intro hq3 hq2
    have w2 : c (w (j + 2)) = c (P.x (j + 1)) := by
      have n3' := (H.nbr (j + 3) hq3 u').1 hu'
      simp only [add_assoc, Fin.reduceAdd] at n3'
      rcases n3' with rfl | rfl | rfl | rfl | rfl
      · exact (hu'h rfl).elim
      · exact (h1 (hcu'.symm.trans h02.symm)).elim
      · exact (h14 hcu'.symm).elim
      · exact hcu'
      · exact (h1 (hcu'.symm.trans a3)).elim
    by_contra hne
    have hA : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' hne; omega
    have n2 := (H.nbr (j + 2) hq2 u).1 hu
    simp only [add_assoc, Fin.reduceAdd] at n2
    rcases n2 with rfl | rfl | rfl | rfl | rfl
    · exact huh rfl
    · rw [v1] at hcu; exact h14 hcu
    · rw [v3] at hcu; exact h4 hcu.symm
    · have e := H.adj_w' (j + 1)
      simp only [add_assoc, Fin.reduceAdd] at e
      rw [rot3_K2 hr' e (H.offh _) (Or.inr hA), hA, Equiv.swap_apply_right] at hcu
      exact h4 hcu.symm
    · rw [rot3_keep (by rw [w2]; exact h1) (by rw [w2]; exact h13), w2] at hcu
      exact h14 hcu
  have hq : q = j + (q - j) := (add_sub_cancel j q).symm
  rcases fin5_five (q - j) with hk | hk | hk | hk | hk <;> rw [hk] at hq <;> subst hq
  · exact absurd (a0.trans (core (fin5_ne (by decide)) (fin5_ne (by decide))).symm)
      (H.ring0 hc (fin5_ne (by decide)))
  · refine Or.inl ⟨rfl, ?_⟩
    have w1 := core (fin5_ne (by decide)) (fin5_ne (by decide))
    obtain ⟨-, -, v2, -, v4⟩ := rot3_values hr' hK
    unfold TypeR3
    simp only [add_assoc, Fin.reduceAdd, hπ]
    refine ⟨?_, ?_⟩
    · rw [v2, rot3_K3 hr' (H.adj_w (j + 3)) (H.offh _) (Or.inl a3), a3, Equiv.swap_apply_left]
    · rw [v4, rot3_keep (by rw [w1]; exact h4) (by rw [w1]; exact h34.symm), w1]
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)
  · exact absurd (a0.trans (core (fin5_ne (by decide)) (fin5_ne (by decide))).symm)
      (H.ring0 hc (fin5_ne (by decide)))

/-- Every all-`DL` orbit at a `Hole4` hole has a typed state among its first two states. -/
theorem typed_in_orbit4 (H : Hole4 P w q) {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ k, DLState P ((piMove P)^[k] s)) :
    ∃ N t k, HasTK P w q ((piMove P)^[N] s) t k := by
  obtain ⟨j, hd⟩ := hall 0
  have D0 := allDL_orbit_dd hc hall 0 j hd
  by_cases t1 : TypeR1 P w s j
  · exact ⟨0, .R1, _, hasTK_of_dl hd .R1 t1⟩
  by_cases t3 : TypeR3 P w s j
  · exact ⟨0, .R3, _, hasTK_of_dl hd .R3 t3⟩
  have D1 : DDstate P ((piMove P)^[1] s) (j + 3) := allDL_orbit_dd hc hall 1 _ D0.2
  rcases untyped_dd4 H hc D0 t1 t3 with ⟨-, hT⟩ | h23
  · exact ⟨1, .R3, _, hasTK_of_dl D0.2 .R3 hT⟩
  by_cases t1' : TypeR1 P w ((piMove P)^[1] s) (j + 3)
  · exact ⟨1, .R1, _, hasTK_of_dl D0.2 .R1 t1'⟩
  by_cases t3' : TypeR3 P w ((piMove P)^[1] s) (j + 3)
  · exact ⟨1, .R3, _, hasTK_of_dl D0.2 .R3 t3'⟩
  exfalso
  refine q_two_three' j q h23 ?_
  rcases untyped_dd4 H (iter_proper hc 1) D1 t1' t3' with ⟨e, -⟩ | e | e
  · exact Or.inl e
  · exact Or.inr (Or.inl e)
  · exact Or.inr (Or.inr e)

/-! ### 3. Weak F6 -/

/-- **Every `Γ`-cycle at a hole with four consecutive degree-five link vertices has a non-`DL`
`σ`-image** (any degree of the fifth link vertex). -/
theorem gammaImages_of_hole4 (H : Hole4 P w q) : GammaImages P := by
  intro s hc hall
  obtain ⟨N, t, k, h0⟩ := typed_in_orbit4 H hc hall
  have it : ∀ d, HasTK P w q ((piMove P)^[N + d] s) (gstep^[d] (t, k)).1
      (gstep^[d] (t, k)).2 := by
    intro d
    induction d with
    | zero => exact h0
    | succ d ih =>
      have e := tk_step4 H (iter_proper hc (N + d)) ih
        (by rw [← Function.iterate_succ_apply' (piMove P)]; exact hall (N + d + 1))
      rw [← add_assoc, Function.iterate_succ_apply', Function.iterate_succ_apply']
      exact e
  obtain ⟨d, -, hd2⟩ := gstep_to_R1k2' t k
  have hr := it d
  rw [hd2] at hr
  obtain ⟨j, hdl, hq, hT1⟩ := hr
  set r := (piMove P)^[N + d] s with hrdef
  have hcr : ProperOff M.graph h r := iter_proper hc _
  have hD : DDstate P r j := allDL_orbit_dd hc hall _ j hdl
  have hz := pair_R3k4_z4 H hq hcr hD hT1
  have hT3 := r1_step4 H hq hcr hD hT1
  have hq' : q = j + 3 + 4 := hq.trans (q_k4' j)
  have hR := r3k4_R3At4 H hq' (piMove_properOff hcr) hD.2 hT3 hz
  refine ⟨N + d + 1, j + 3, ?_, ?_⟩ <;> rw [Function.iterate_succ_apply', ← hrdef]
  · exact hD.2
  · exact sigma_exit_not_DL_k4_core (H.triple hq') (H.nbr3 hq') (piMove_properOff hcr) hR

/-- Weak F6 at a `Hole4` hole. -/
theorem pureClean_of_hole4 (H : Hole4 P w q) : PureClean M h :=
  pureClean_of_images (gammaImages_of_hole4 H)

/-- **Weak F6 at `(5,5,5,5,d)`, `d ≥ 6`.** Every Kempe class contains a filled state. -/
theorem every_class_filled_of_hole6gen (H : Hole6Gen P w ms q) {c₀ : Fin n → Fin 4}
    (hc₀ : ProperOff M.graph h c₀) : ∃ d ∈ kclass M h c₀, Target M.graph h d :=
  filled_in_class_of_images (gammaImages_of_hole4 H.toHole4) hc₀

/-- **Weak F6 at `(5,5,5,5,d)`, `d ≥ 6`, `PureClean` form.** -/
theorem pureClean_of_hole6gen (H : Hole6Gen P w ms q) : PureClean M h :=
  pureClean_of_hole4 H.toHole4

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.sigma_exit_not_DL_k4_gen
#print axioms SimpleGraph.QuarterFloor.tk_step4
#print axioms SimpleGraph.QuarterFloor.typed_in_orbit4
#print axioms SimpleGraph.QuarterFloor.gammaImages_of_hole4
#print axioms SimpleGraph.QuarterFloor.pureClean_of_hole4
#print axioms SimpleGraph.QuarterFloor.every_class_filled_of_hole6gen
#print axioms SimpleGraph.QuarterFloor.pureClean_of_hole6gen
#print axioms SimpleGraph.QuarterFloor.Hole6.toHole6Gen
