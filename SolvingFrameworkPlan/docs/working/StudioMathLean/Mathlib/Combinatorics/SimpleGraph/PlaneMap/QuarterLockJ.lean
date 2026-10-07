/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPeriodJ

/-!
# The lock-membership form of `J` (`NightLemmaS.md` §5.1, Lemma 5.1)

Setting and notation as in `QuarterPeriodJ`: `Hole6 P w m q`, `p = x q`, `y = w (q+4)`,
`z = w q`, `JoinYZ G h w q c` (the note's `J`). The state at position `n % 10` of an all-`DL`
orbit (`gamma_period_ten`) is doubly locked at some `j`; `Lock1` is the `{μ, A}`-component
`K_{μ,A}(x (j+1))` and `Lock2` the `{μ, B}`-component `K_{μ,B}(x (j+1))`, with
`μ = c (x (j+1))`, `A = c (x (j+3))`, `B = c (x (j+4))`.

## Main results (sorry-free, no new axioms)

* `J_iff_lock2_R1k2` (position `9`, `R1k2`, `q = j + 2`): `y = w (j+1)` has colour `B` and
  `z = w (j+2)` has colour `μ`, so the pair of `J` is the `Lock2` pair (as graphs:
  `pairGraph c (c y) (c z) = pairGraph c μ B`); the `Lock2` component of `x (j+1)` contains
  `y` and `x (j+4)`; and `J ⇔ z ∈ K_{μ,B}(x (j+1))`.
* `J_iff_lock1_R3k4` (position `0`, `R3k4`, `q = j + 4`, `n > 0`): `y = w (j+3)` (`μ`) and
  `x (j+3)` lie in the `Lock1` component `K_{μ,A}(x (j+1))`, and
  `J ⇔ w₄ = z = w (j+4) ∈ K_{μ,A}(x (j+1))` (the component **of `x (j+1)`**).
* `J_iff_lock2_R3k3` (position `2`, `R3k3`, `q = j + 3`): `z = w (j+3)` (`μ`) and `x (j+4)`
  lie in the `Lock2` component `K_{μ,B}(x (j+1))`, and
  `J ⇔ w₂ = y = w (j+2) ∈ K_{μ,B}(x (j+1))`.
* `step8_fixes_lock2_graph` (position `8`, `R3k0`, `q = j`): the swapped pair is
  `{α, A} = {c p, c y}` (`pair_own`), while `c m = μ` and `c z = B`, so the `Lock2` pair
  `{μ, B} = {c m, c z}` is disjoint from it, and the step-8 swap leaves the `Lock2` two-colour
  graph `pairGraph c μ B` of the `R3k0` state unchanged.

The state-level forms are `lock2_R1k2`, `lock1_R3k4`, `lock2_R3k3`, `step_R3k0_lock2`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

/-! ### State-level forms -/

/-- **`R1k2`.** At an `R1` `DD` state at `k = 2`: `y = w (j+1)` is `B`, `z = w (j+2)` is `μ`,
the pair of `J` is the `Lock2` pair, the `Lock2` component of `x (j+1)` contains `y` and
`x (j+4)`, and `J ⇔ z ∈ K_{μ,B}(x (j+1))`. -/
theorem lock2_R1k2 (H : Hole6 P w m q) (hq : q = j + 2) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) :
    c (w (j + 1)) = c (P.x (j + 4)) ∧ c (w (j + 2)) = c (P.x (j + 1)) ∧
    pairGraph M.graph h c (c (w (q + 4))) (c (w q)) =
      pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) ∧
    (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 1)) (w (j + 1)) ∧
    Lock2 P c j ∧
    (JoinYZ M.graph h w q c ↔
      (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
        (P.x (j + 1)) (w (j + 2))) := by
  subst hq
  obtain ⟨w1, w3⟩ := r1_ring H rfl hc hD hT
  obtain ⟨-, hr, -, ⟨u', hu', hu'h, hcu'⟩, -, -⟩ := dd_ends hc hD
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have n3 := (H.nbr (j + 3) (fin5_ne (by decide)) u').1 hu'
  simp only [add_assoc, Fin.reduceAdd] at n3
  have w2 : c (w (j + 2)) = c (P.x (j + 1)) := by
    rcases n3 with rfl | rfl | rfl | rfl | rfl
    · exact (hu'h rfl).elim
    · exact (h1 (hcu'.symm.trans h02.symm)).elim
    · exact (h14 hcu'.symm).elim
    · exact hcu'
    · exact (h1 (hcu'.symm.trans w3)).elim
  have l2 : Lock2 P c j := hD.1.2.2
  have ey : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 1)) (w (j + 1)) :=
    pgR (H.adj_w (j + 1)) (P.x_ne_h _) (H.offh _) (Or.inl rfl) (Or.inr w1)
  have hg : pairGraph M.graph h c (c (w (j + 2 + 4))) (c (w (j + 2))) =
      pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) := by
    simp only [add_assoc, Fin.reduceAdd]
    rw [w1, w2, pairGraph_comm]
  refine ⟨w1, w2, hg, ey, l2, ?_⟩
  unfold JoinYZ
  rw [hg]
  simp only [add_assoc, Fin.reduceAdd]
  exact ⟨fun r => ey.trans r, fun r => ey.symm.trans r⟩

/-- **`R3k4`.** At an `R3` state at `k = 4` (full ring): `y = w (j+3)` is `μ`, `z = w (j+4)`
is `A`, so the pair of `J` is the `Lock1` pair; the `Lock1` component of `x (j+1)` contains `y`
and `x (j+3)`, and `J ⇔ w₄ ∈ K_{μ,A}(x (j+1))`. -/
theorem lock1_R3k4 (H : Hole6 P w m q) (hq : q = j + 4) (hR : R3At P w c j) :
    c (w (j + 3)) = c (P.x (j + 1)) ∧ c (w (j + 4)) = c (P.x (j + 3)) ∧
    (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
      (P.x (j + 1)) (w (j + 3)) ∧
    Lock1 P c j ∧
    (JoinYZ M.graph h w q c ↔
      (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
        (P.x (j + 1)) (w (j + 4))) := by
  subst hq
  obtain ⟨⟨-, l1, -⟩, -, -, -, e3, e4⟩ := hR
  have ey : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
      (P.x (j + 1)) (w (j + 3)) :=
    l1.trans (pgR (H.adj_w (j + 3)) (P.x_ne_h _) (H.offh _) (Or.inr rfl) (Or.inl e3))
  refine ⟨e3, e4, ey, l1, ?_⟩
  unfold JoinYZ
  simp only [add_assoc, Fin.reduceAdd]
  rw [e3, e4]
  exact ⟨fun r => ey.trans r, fun r => ey.symm.trans r⟩

/-- **`R3k3`.** At an `R3` state at `k = 3` (full ring): `y = w (j+2)` is `B`, `z = w (j+3)`
is `μ`, so the pair of `J` is the `Lock2` pair; the `Lock2` component of `x (j+1)` contains `z`
and `x (j+4)`, and `J ⇔ w₂ ∈ K_{μ,B}(x (j+1))`. -/
theorem lock2_R3k3 (H : Hole6 P w m q) (hq : q = j + 3) (hR : R3At P w c j) :
    c (w (j + 2)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x (j + 1)) ∧
    (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 1)) (w (j + 3)) ∧
    Lock2 P c j ∧
    (JoinYZ M.graph h w q c ↔
      (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
        (P.x (j + 1)) (w (j + 2))) := by
  subst hq
  obtain ⟨⟨-, -, l2⟩, -, -, e2, e3, -⟩ := hR
  have a := H.adj_w4 (j + 4)
  simp only [add_assoc, Fin.reduceAdd] at a
  have ez : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 1)) (w (j + 3)) :=
    l2.trans (pgR a (P.x_ne_h _) (H.offh _) (Or.inr rfl) (Or.inl e3))
  refine ⟨e2, e3, ez, l2, ?_⟩
  unfold JoinYZ
  simp only [add_assoc, Fin.reduceAdd]
  rw [e2, e3, pairGraph_comm c (c (P.x (j + 4))) (c (P.x (j + 1)))]
  exact ⟨fun r => ez.trans r.symm, fun r => r.symm.trans ez⟩

/-- **`R3k0`, the step-8 swap.** At an `R3` `DD` state at `k = 0` (`q = j`): the swapped pair
`{α, A}` is carried by `(p, y)` (`pair_own`), `m` has colour `μ` and `z` colour `B`, so the
`Lock2` pair `{μ, B} = {c m, c z}` is disjoint from `{c p, c y}`, and `π c` has the same
`Lock2` two-colour graph as `c`. -/
theorem step_R3k0_lock2 (H : Hole6 P w m q) (hq : q = j + 0) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR3 P w c j) :
    PairFact P c j (P.x q) (w (q + 4)) ∧
    c m = c (P.x (j + 1)) ∧ c (w q) = c (P.x (j + 4)) ∧
    (c (P.x q) ≠ c m ∧ c (P.x q) ≠ c (w q) ∧ c (w (q + 4)) ≠ c m ∧ c (w (q + 4)) ≠ c (w q)) ∧
    pairGraph M.graph h (piMove P c) (c (P.x (j + 1))) (c (P.x (j + 4))) =
      pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) ∧
    pairGraph M.graph h (piMove P c) (c m) (c (w q)) = pairGraph M.graph h c (c m) (c (w q)) := by
  have own := pair_own (t := .R3) (k := 0) H hq hc hD hT (by decide)
  rw [pv_R3_0] at own
  subst hq
  simp only [add_zero] at own ⊢
  obtain ⟨op, oy⟩ := own
  obtain ⟨hπ, hr, -, -, -, -⟩ := dd_ends hc hD
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have am := hc (H.adj_m) (P.x_ne_h _) H.offmh
  have ay := hc H.ringy (H.offh _) H.offmh
  have az := hc H.ringz H.offmh (H.offh _)
  simp only [add_zero] at am ay az
  have t0 := hT.1
  have cm : c m = c (P.x (j + 1)) := by
    clear * - h1 h3 h4 h13 h14 h34 am ay az t0 oy; omega
  have hg : pairGraph M.graph h (piMove P c) (c (P.x (j + 1))) (c (P.x (j + 4))) =
      pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) := by
    rw [hπ]
    unfold rot3
    exact pairGraph_swap_other _ _ _ _ h1 h13 h4 h34.symm
  refine ⟨⟨op, oy⟩, cm, t0, ⟨?_, ?_, ?_, ?_⟩, hg, ?_⟩
  · exact am
  · rw [t0]; exact h4.symm
  · exact ay
  · rw [oy, t0]; exact h34
  · rw [cm, t0]; exact hg

/-! ### On the all-`DL` orbit (the setting of `gamma_period_ten`) -/

/-- **Lemma 5.1, position 9 (`R1k2`).** On an all-`DL` orbit from an `R3k4` state at a
`Hole6`, at every `n` with `n % 10 = 9` the state is doubly locked at some `j` with
`q = j + 2`; the pair of `J` is the `Lock2` pair; the `Lock2` component of `x (j+1)` contains
`y = w (j+1)` and `x (j+4)`; and `J ⇔ z = w (j+2)` lies in that component. -/
theorem J_iff_lock2_R1k2 {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 9) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j + 2 ∧
      ((piMove P)^[k] s) (w (j + 1)) = ((piMove P)^[k] s) (P.x (j + 4)) ∧
      ((piMove P)^[k] s) (w (j + 2)) = ((piMove P)^[k] s) (P.x (j + 1)) ∧
      pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (w (q + 4)))
          (((piMove P)^[k] s) (w q)) =
        pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4))) ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w (j + 1)) ∧
      Lock2 P ((piMove P)^[k] s) j ∧
      (JoinYZ M.graph h w q ((piMove P)^[k] s) ↔
        (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w (j + 2))) := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R1, 2) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  exact ⟨j, hd, hq', lock2_R1k2 H hq' (iter_proper hc k) (orbit_dd hc hall k j hd) hT'⟩

/-- **Lemma 5.1, position 0 (`R3k4`).** At every `n > 0` with `n % 10 = 0` the state is
doubly locked at `j` with `q = j + 4`, `y = w (j+3)` and `x (j+3)` lie in the `Lock1` component
`K_{μ,A}(x (j+1))` of `x (j+1)`, and `J ⇔ w₄ = z = w (j+4)` lies in that component. -/
theorem J_iff_lock1_R3k4 {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk0 : 0 < k)
    (hk : k % 10 = 0) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j + 4 ∧
      ((piMove P)^[k] s) (w (j + 3)) = ((piMove P)^[k] s) (P.x (j + 1)) ∧
      ((piMove P)^[k] s) (w (j + 4)) = ((piMove P)^[k] s) (P.x (j + 3)) ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 1)) (w (j + 3)) ∧
      Lock1 P ((piMove P)^[k] s) j ∧
      (JoinYZ M.graph h w q ((piMove P)^[k] s) ↔
        (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 1)) (w (j + 4))) := by
  obtain ⟨tk, pr, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R3, 4) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  have pz := pr k hk0 j hd.1
  rw [g] at pz
  dsimp only at pz
  rw [pv_R3_4] at pz
  have hR := r3k4_R3At H hq' (iter_proper hc _) hd hT' pz.2
  exact ⟨j, hd, hq', lock1_R3k4 H hq' hR⟩

/-- **Lemma 5.1, position 2 (`R3k3`).** At every `n` with `n % 10 = 2` the state is doubly
locked at `j` with `q = j + 3`, `z = w (j+3)` and `x (j+4)` lie in the `Lock2` component
`K_{μ,B}(x (j+1))`, and `J ⇔ w₂ = y = w (j+2)` lies in that component. -/
theorem J_iff_lock2_R3k3 {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 2) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j + 3 ∧
      ((piMove P)^[k] s) (w (j + 2)) = ((piMove P)^[k] s) (P.x (j + 4)) ∧
      ((piMove P)^[k] s) (w (j + 3)) = ((piMove P)^[k] s) (P.x (j + 1)) ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w (j + 3)) ∧
      Lock2 P ((piMove P)^[k] s) j ∧
      (JoinYZ M.graph h w q ((piMove P)^[k] s) ↔
        (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w (j + 2))) := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R3, 3) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  have hR := r3k3_R3At H hq' (iter_proper hc _) (orbit_dd hc hall _ j hd) hT'
  exact ⟨j, hd, hq', lock2_R3k3 H hq' hR⟩

/-- **Lemma 5.1, the step-8 swap (`R3k0`).** At every `n` with `n % 10 = 8` the state `c` is
doubly locked at `j = q`; the swap pair `{α, A}` is carried by `(p, y)`, the `Lock2` pair
`{μ, B}` by `(m, z)`, the two pairs are disjoint, and the step `c ↦ π c` leaves the `Lock2`
two-colour graph `pairGraph c μ B` of `c` unchanged. -/
theorem step8_fixes_lock2_graph {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 8) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j ∧
      PairFact P ((piMove P)^[k] s) j (P.x q) (w (q + 4)) ∧
      ((piMove P)^[k] s) m = ((piMove P)^[k] s) (P.x (j + 1)) ∧
      ((piMove P)^[k] s) (w q) = ((piMove P)^[k] s) (P.x (j + 4)) ∧
      (((piMove P)^[k] s) (P.x q) ≠ ((piMove P)^[k] s) m ∧
        ((piMove P)^[k] s) (P.x q) ≠ ((piMove P)^[k] s) (w q) ∧
        ((piMove P)^[k] s) (w (q + 4)) ≠ ((piMove P)^[k] s) m ∧
        ((piMove P)^[k] s) (w (q + 4)) ≠ ((piMove P)^[k] s) (w q)) ∧
      pairGraph M.graph h ((piMove P)^[k + 1] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4))) =
        pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4))) ∧
      pairGraph M.graph h ((piMove P)^[k + 1] s) (((piMove P)^[k] s) m)
          (((piMove P)^[k] s) (w q)) =
        pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) m)
          (((piMove P)^[k] s) (w q)) := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R3, 0) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  have e := step_R3k0_lock2 H hq' (iter_proper hc k) (orbit_dd hc hall k j hd) hT'
  rw [Function.iterate_succ_apply']
  exact ⟨j, hd, by rw [hq', add_zero], e⟩

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.J_iff_lock2_R1k2
#print axioms SimpleGraph.QuarterFloor.J_iff_lock1_R3k4
#print axioms SimpleGraph.QuarterFloor.J_iff_lock2_R3k3
#print axioms SimpleGraph.QuarterFloor.step8_fixes_lock2_graph
