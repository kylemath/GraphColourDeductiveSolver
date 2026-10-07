/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLockJ

/-!
# `z` is in the `Lock2` witness two states after a break (Studio Job AE, probe)

Setting of `QuarterLockJ`: an all-`DL` orbit at a `Hole6`, `p = x q`, `y = w (q+4)`,
`z = w q`. Write the period-`b` state at position `9` (`R1k2`) with repeat index `j`, so
`q = j + 2`; a break there is `z ∉ K_{μ,B}(x (j+1))` (`J_iff_lock2_R1k2`).

## Names at positions `0` and `1` of period `b + 1` (`tk_step`, `pair_own`)

* Position `0` (`R3k4`), repeat index `j' = j + 3 = q + 1`: `x (j'+1) = x (q+2)`; the `Lock2`
  pair is `{μ', B'} = {c (x (q+2)), c p}` (`x (j'+4) = p`); the `Lock2` witness is the
  `{μ', B'}`-chain from `x (q+2)` to `p`, and it contains `y` (`TypeR3`: `c y = μ'`, `y ~ p`).
  The swap `0 → 1` is `{α', A'}`, carried by `(m, z)` (`c m = α'`, `c z = A'`), so `z` has
  colour `A' ∉ {μ', B'}` and is **not** on the position-`0` witness.
* Position `1` (`R1k1`), repeat index `j'' = j + 1 = q + 4`: `x (j''+1) = p` itself; the `Lock2`
  pair is `{c p, c (x (q+3))}`; the witness is the chain from `p` to `x (q+3)`, and
  `z = w (j''+1)` is the `B''`-neighbour of `p` (`r1_ring`, `k = 1`: `c (w (j''+1)) = B''`).

So `z ∈ K_{μ'',B''}(x (j''+1))` at position `1` is **local**: `z` is adjacent to
`x (j''+1) = p` and has colour `B''`. It uses only that positions `1` and `2` are `DL` (through
`r1_w1_k1`); it holds in every period, whether or not `J` broke at position `9`.

## Main results (sorry-free, no new axioms)

* `lock2_R1k1_z`: state form at `R1k1`.
* `restore_pos0`: position `0` (`n % 10 = 0`, `n > 0`): `x (j+4) = p`, `y` on the `Lock2`
  witness, `c z = A ∉ {μ, B}`.
* `z_in_lock2_R1k1`: position `1` (`n % 10 = 1`): `x (j+1) = p`, `c z = B`, `z ∈ K_{μ,B}(p)`.
* `z_in_lock2_after_break`: the AE statement, a break at `k` (`k % 10 = 9`) gives
  `z ∈ Lock2`-component at `k + 2` (the break hypothesis is not used).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

/-- **`R1k1`, state form.** At an `R1` `DD` state with `q = j + 1`: `x (j+1) = p`,
`z = w q` has colour `B = c (x (j+4))`, and `z` lies in the `Lock2` component of `x (j+1)`. -/
theorem lock2_R1k1_z (H : Hole6 P w m q) (hq : q = j + 1) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) :
    P.x (j + 1) = P.x q ∧ c (w q) = c (P.x (j + 4)) ∧ Lock2 P c j ∧
    (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 1)) (w q) := by
  obtain ⟨w1, -⟩ := r1_ring H hq hc hD hT
  subst hq
  refine ⟨rfl, w1, hD.1.2.2, ?_⟩
  exact pgR (H.adj_w (j + 1)) (P.x_ne_h _) (H.offh _) (Or.inl rfl) (Or.inr w1)

/-- **Position `0` (`R3k4`).** At `n > 0`, `n % 10 = 0`: repeat index `j` with `q = j + 4`,
so `x (j+4) = p`; `y = w (j+3)` has colour `μ` and lies on the `Lock2` witness (the chain from
`x (j+1)` to `p`); `z` has colour `A`, outside the `Lock2` pair `{μ, B}`. -/
theorem restore_pos0 {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk0 : 0 < k)
    (hk : k % 10 = 0) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j + 4 ∧ P.x (j + 4) = P.x q ∧
      PairFact P ((piMove P)^[k] s) j m (w q) ∧
      ((piMove P)^[k] s) (w (q + 4)) = ((piMove P)^[k] s) (P.x (j + 1)) ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w (q + 4)) ∧
      ((piMove P)^[k] s) (w q) ≠ ((piMove P)^[k] s) (P.x (j + 1)) ∧
      ((piMove P)^[k] s) (w q) ≠ ((piMove P)^[k] s) (P.x (j + 4)) := by
  obtain ⟨tk, pr, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R3, 4) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  have pz := pr k hk0 j hd.1
  rw [g] at pz
  dsimp only at pz
  rw [pv_R3_4] at pz
  set c := (piMove P)^[k] s
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hd.1
  have l2 : Lock2 P c j := hd.2.2
  subst hq'
  have ey : c (w (j + 4 + 4)) = c (P.x (j + 1)) := by
    simp only [add_assoc, Fin.reduceAdd]; exact hT'.2
  refine ⟨j, hd, rfl, rfl, pz, ey, ?_, ?_, ?_⟩
  · have a := H.adj_w4 (j + 4)
    exact l2.trans (pgR a (P.x_ne_h _) (H.offh _) (Or.inr rfl) (Or.inl ey))
  · rw [pz.2]; exact h13.symm
  · rw [pz.2]; exact h34

/-- **Position `1` (`R1k1`).** At every `n % 10 = 1` the state is doubly locked at `j` with
`q = j + 1`, so `x (j+1) = p`; `z = w q` has colour `B`, and `z` lies in the `Lock2` component
`K_{μ,B}(x (j+1))` (it is the `B`-neighbour of `p`). Purely local: no hypothesis on `J`. -/
theorem z_in_lock2_R1k1 {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 1) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j + 1 ∧ P.x (j + 1) = P.x q ∧
      ((piMove P)^[k] s) (w q) = ((piMove P)^[k] s) (P.x (j + 4)) ∧
      Lock2 P ((piMove P)^[k] s) j ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x (j + 1)))
          (((piMove P)^[k] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w q) := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R1, 1) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  exact ⟨j, hd, hq', lock2_R1k1_z H hq' (iter_proper hc k) (orbit_dd hc hall k j hd) hT'⟩

/-- **Studio Job AE (i), the probe.** If `J` fails at position `9` of a period (`k % 10 = 9`),
then two states later (position `1` of the next period) `z` lies in the `Lock2` component of
`x (j+1) = p`. The break hypothesis is not used: the conclusion holds at every position `1`. -/
theorem z_in_lock2_after_break {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 9)
    (_hbreak : ¬ JoinYZ M.graph h w q ((piMove P)^[k] s)) :
    ∃ j, DoublyLocked P ((piMove P)^[k + 2] s) j ∧ q = j + 1 ∧ P.x (j + 1) = P.x q ∧
      ((piMove P)^[k + 2] s) (w q) = ((piMove P)^[k + 2] s) (P.x (j + 4)) ∧
      Lock2 P ((piMove P)^[k + 2] s) j ∧
      (pairGraph M.graph h ((piMove P)^[k + 2] s) (((piMove P)^[k + 2] s) (P.x (j + 1)))
          (((piMove P)^[k + 2] s) (P.x (j + 4)))).Reachable (P.x (j + 1)) (w q) :=
  z_in_lock2_R1k1 H hc hall hr hq hT (k + 2) (by omega)

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.lock2_R1k1_z
#print axioms SimpleGraph.QuarterFloor.restore_pos0
#print axioms SimpleGraph.QuarterFloor.z_in_lock2_R1k1
#print axioms SimpleGraph.QuarterFloor.z_in_lock2_after_break
