/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLemmaP

/-!
# U34: a failing `σ`-exit starts a short unfilled run

Formalises "U34" of the Night log (Studio Job BA): at a doubly locked `R3` state `r` with
repeat index `j` in the `k = 4` ball (`K4Ball`) whose `σ`-exit fails, the image `s = σ r` is
`Lock2`-only, starts its unfilled run, the run has length `u ∈ {3, 4}`, and when `u = 4` the
following filled run has `f = 1`. At `k = 3` (`K3Ball`) a failing image is `Lock1`-only, is the
last state of its run, and the run after it has the forward pattern `(1, 1)`: `π s` filled and
`π² s` unfilled.

## The colour walk (`k = 4`; link `(α, μ, α, A, B)` and ring `(B, A, B, μ, A)` in `r`, `m = α`)

* `s = σ r` (swap of the triple `x j, x (j+1), x (j+2)`): link `(μ, α, μ, A, B)`,
  `w₂ = B`, `w₃ = μ` (unchanged off the triple).
* `t₁ = π s = R₊₃` (swap the `{μ, A}`-component of `x (j+2)`; it contains `x (j+3)` and `w₃`):
  link `(μ, α, A, μ, B)`, repeat index `j + 3`, `w₂ = B`, `w₃ = A`. Its Lock 2 is the
  `{B, A}`-walk `x (j+4), w₃, w₂, x (j+2)` (`K4Ball.nbr4`, `ring23`, the triple ball): so
  `π t₁` is unfilled, `u ≥ 3`.
* `t₂ = π t₁ = R₊₃` (swap the `{μ, α}`-component of `x j`): link `(α, μ, A, μ, B)`, repeat
  index `j + 1`, `w₂ = B`, `w₃ = A`. If `Lock2 t₂` fails, `π t₂` is filled: `u = 3`.
* Otherwise `t₃ = π t₂ = R₊₃` (swap the `{μ, B}`-component of `x (j+3)`; it contains `w₂`):
  link `(α, μ, A, B, μ)`, repeat index `j + 4`, `w₂ = μ`, `w₃ = A`. Now `x (j+3)` (colour `B`,
  degree five) has neighbours `x (j+2) = A`, `x (j+4) = μ`, `w₂ = μ`, `w₃ = A`: it is isolated in
  the `{α, B}`-graph, so `Lock2 t₃` dies and `π t₃ = φ_B⁻¹` is filled: `u = 4`.
* `t₄ = π t₃ = φ_B⁻¹` recolours only `x (j+3)` (to `α`): link `(α, μ, A, α, μ)`, a filled state
  with singleton at `j + 2` and `{Y, Z} = {μ, B}`. Its `{μ, B}`-graph is contained in that of
  `t₃` (`pairGraph_le_of_one`), where `x (j+4) ↛ x (j+1)` because `t₃` has Lock 1 at `j + 4`
  (`rot2Def_of_lock1`, Jordan at the hole). So `t₄` is `M3`-short, `π t₄` is unfilled: `f = 1`.

At `k = 3`: Lock 2 of `s` dies at `x (j+4)` (`sigma_exit_noLock2_k3`), which is isolated in the
`{α, B}`-graph of `s`; `t = π s = φ_B⁻¹` recolours only `x (j+4)` (to `α`), link
`(μ, α, μ, A, α)`, singleton at `j + 3`, `{Y, Z} = {μ, B}`; and `x j ↛ x (j+2)` in the
`{μ, B}`-graph of `s` by Lock 1 of `s` (`rot2Def_of_lock1`). So `t` is `M3`-short.

## Main results (sorry-free, no new axioms, no hypotheses beyond the local ball)

* `u34_lock2_only`, `u34_run_start` (1): a failing `k = 4` image is `Lock2`-only, `π⁻¹ s` is
  filled and `π s` unfilled (Lemma P).
* `u34_core`, `u34_run_length` (2): `π s`, `π² s` unfilled, and `π³ s` filled or
  (`π³ s` unfilled, `π⁴ s` filled): `∃ u ∈ {3, 4}`, `π^k s` unfilled for `k < u`, `π^u s` filled.
* `u34_f_one` (3): if `π³ s` is unfilled (`u = 4`), then `π⁴ s` is filled and `π⁵ s` unfilled.
  `u34_excursion`: `s` starts an `Excursion P s u f` with `u ∈ {3, 4}` and `u = 4 → f = 1`.
* `u3_lock1_only`, `u3_run_end` (4): a failing `k = 3` image is `Lock1`-only, `π⁻¹ s` is
  unfilled, `π s` filled and `π² s` unfilled.

* `u34_mass_bound`: the excursion has mass `u − 3f`, equal to `1` when `u = 4`.
* `u34_f_one_of_three`, `u34_mass` (**conditional**): `f = 1` when `u = 3`, hence mass `∈ {0, 1}`,
  under the named hypothesis `hw`: `w₃` is not in the `{A, α}`-component of `x j` in `π² s`
  (the component that `π (π² s) = φ_B⁻¹` swaps). Under `hw`, `x (j+3)` is isolated in the
  `{μ, α}`-graph of `π³ s`. Without it, `w₃` turns `α` and that component runs through `m`, whose
  colour in `π² s` is not determined locally, so `f = 1` at `u = 3` is a non-local Kempe claim.
* `u3_mass`: at `k = 3`, in any excursion `(e, u, f)` containing the image `s = π^k e`:
  `k = u − 1`, `u ≥ 2`, `f = 1`, mass `u − 3`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- Changing a colouring at one vertex `p` only, to a colour outside `{a, b}`, can only shrink
the `{a, b}`-graph. -/
lemma pairGraph_le_of_one {V : Type*} {G : SimpleGraph V} {h p : V} {c d : V → Fin 4}
    {a b : Fin 4} (hd : ∀ v, v ≠ p → d v = c v) (ha : d p ≠ a) (hb : d p ≠ b) :
    pairGraph G h d a b ≤ pairGraph G h c a b := by
  have act : ∀ v, Active h d a b v → Active h c a b v := by
    rintro v ⟨hv, hcol⟩
    by_cases e : v = p
    · subst e
      rcases hcol with f | f
      · exact absurd f ha
      · exact absurd f hb
    · exact ⟨hv, by rw [← hd v e]; exact hcol⟩
  rintro u v ⟨e, au, av⟩
  exact ⟨e, act u au, act v av⟩

private lemma fneU (j : Fin 5) : j ≠ j + 3 ∧ j + 2 ≠ j + 3 ∧ j + 4 ≠ j + 3 ∧ j ≠ j + 4 ∧
    j + 3 ≠ j + 4 := by
  revert j; decide

private lemma fne13 (j : Fin 5) : j + 1 ≠ j + 3 := by
  revert j; decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h}
  {w : Fin 5 → Fin n} {m : Fin n} {r : Fin n → Fin 4} {j : Fin 5}

lemma rot3_eq_kswap (c : Fin n → Fin 4) (i : Fin 5) :
    rot3 P c i = kswap M.graph h c (c (P.x i)) (c (P.x (i + 3))) (P.x (i + 2)) := rfl

lemma rot3_keep' {c : Fin n → Fin 4} {i : Fin 5} {v : Fin n} (h1 : c v ≠ c (P.x i))
    (h2 : c v ≠ c (P.x (i + 3))) : rot3 P c i v = c v :=
  swap_other h1 h2

/-! ### Building an excursion from a run -/

/-- A run of `u ≥ 1` unfilled states after a filled one, followed by a filled state, is the
start of an excursion (`π`-orbits are periodic). -/
theorem excursion_of_run {s : Fin n → Fin 4} {u : ℕ} (hs : ProperOff M.graph h s) (hu : 0 < u)
    (hprev : Target M.graph h (piInv P s))
    (hunf : ∀ k, k < u → ¬ Target M.graph h ((piMove P)^[k] s))
    (hfil : Target M.graph h ((piMove P)^[u] s)) : ∃ f, Excursion P s u f := by
  classical
  obtain ⟨m, hm, hper⟩ := iterate_period (P := P) hs
  have hex : ∃ k, ¬ Target M.graph h ((piMove P)^[u + (k + 1)] s) := by
    refine ⟨m * (u + 1) - u - 1, ?_⟩
    have e : u + (m * (u + 1) - u - 1 + 1) = m * (u + 1) := by
      have : u + 1 ≤ m * (u + 1) := Nat.le_mul_of_pos_left (u + 1) hm
      omega
    rw [e, Function.iterate_mul, Function.iterate_fixed hper]
    exact hunf 0 hu
  refine ⟨Nat.find hex + 1, hs, hu, Nat.succ_pos _, hprev, hunf, fun k hk hk' => ?_,
    Nat.find_spec hex⟩
  rcases Nat.eq_or_lt_of_le hk with rfl | hlt
  · exact hfil
  · obtain ⟨k', rfl⟩ : ∃ k', k = u + (k' + 1) := ⟨k - u - 1, by omega⟩
    exact not_not.1 (Nat.find_min hex (by omega))

/-! ### `k = 4` -/

/-- **(1a)** At `k = 4` a failing `σ`-image is `Lock2`-only. -/
theorem u34_lock2_only (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    ¬ Lock1 P (sigSwap P r j) j ∧ Lock2 P (sigSwap P r j) j := by
  have n1 := sigma_exit_noLock1_k4 K hc hR
  obtain ⟨-, -, rs, -⟩ := sigSwap_basic hc hR.1.1
  exact ⟨n1, Classical.byContradiction fun n2 => hF ((noLock_rep rs).2 ⟨n1, n2⟩)⟩

/-- **(1) `u34_run_start`.** A failing `k = 4` image starts its unfilled run: `π⁻¹ s` is filled
and `π s` is unfilled (Lemma P). -/
theorem u34_run_start (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    Target M.graph h (piInv P (sigSwap P r j)) ∧
      ¬ Target M.graph h (piMove P (sigSwap P r j)) := by
  obtain ⟨-, ps, rs, -⟩ := sigSwap_basic hc hR.1.1
  exact (lemmaP ps rs).2.1.1 (u34_lock2_only K hc hR hF)

/-- **The `k = 4` colour walk.** From a `Lock2` image `s = σ r`: `π s`, `π² s` are unfilled, and
either `π³ s` is filled, or `π³ s` is unfilled, `π⁴ s` filled and `π⁵ s` unfilled. -/
theorem u34_core (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hL2 : Lock2 P (sigSwap P r j) j) :
    ¬ Target M.graph h (piMove P (sigSwap P r j)) ∧
    ¬ Target M.graph h (piMove P (piMove P (sigSwap P r j))) ∧
    (Target M.graph h (piMove P (piMove P (piMove P (sigSwap P r j)))) ∨
      (¬ Target M.graph h (piMove P (piMove P (piMove P (sigSwap P r j)))) ∧
        Target M.graph h (piMove P (piMove P (piMove P (piMove P (sigSwap P r j))))) ∧
        ¬ Target M.graph h
          (piMove P (piMove P (piMove P (piMove P (piMove P (sigSwap P r j)))))))) := by
  have T := K.tri
  obtain ⟨-, -, ps, rs, sout⟩ := sigma_exit T hc hR.1.1 hR.outer
  obtain ⟨-, -, -, s0, s1, s2, s3, s4⟩ := sigSwap_basic hc hR.1.1
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, e2, e3, -⟩ := hR
  obtain ⟨f03, f23, f43, -, -⟩ := fneU j
  obtain ⟨-, -, -, o2⟩ := T.offh
  generalize hsd : sigSwap P r j = s at *
  have sw2 : s (w (j + 2)) = r (P.x (j + 4)) :=
    (sout _ ((T.off _).2.2.2) ((T.off _).2.2.2) ((T.off _).2.2.2)).trans e2
  have sw3 : s (w (j + 3)) = r (P.x (j + 1)) :=
    (sout _ (K.off3 _) (K.off3 _) (K.off3 _)).trans e3
  -- Step 1: `t₁ = R₊₃ s` at `j`.
  have hK1 := rot3Def_of_lock2 P rs hL2
  obtain ⟨u0, u1, u2, u3, u4⟩ := rot3_values rs hK1
  rw [s0] at u0 u3
  rw [s1] at u1
  rw [s3] at u2
  rw [s4] at u4
  obtain ⟨-, p1, r1, -, -⟩ := rot3_move ps rs hL2
  have E1 : piMove P s = rot3 P s j := by rw [piMove_rep rs, ite_eq_left hL2]
  have u5 : rot3 P s j (w (j + 3)) = r (P.x (j + 3)) := by
    have reach1 : (pairGraph M.graph h s (s (P.x j)) (s (P.x (j + 3)))).Reachable
        (P.x (j + 2)) (w (j + 3)) :=
      (rot3_reach rs).trans (Adj.reachable ⟨(K.nbr3 _).2 (by simp), ⟨P.x_ne_h _, Or.inr rfl⟩,
        ⟨K.offh.1, Or.inl (by rw [sw3, s0])⟩⟩)
    rw [rot3_eq_kswap, kswap_mem reach1 (by rw [sw3, s0]), s3]
  have u6 : rot3 P s j (w (j + 2)) = r (P.x (j + 4)) := by
    rw [rot3_keep' (by rw [sw2, s0]; exact h14.symm) (by rw [sw2, s3]; exact h34.symm), sw2]
  generalize ht1 : rot3 P s j = t1 at *
  have L2t1 : Lock2 P t1 (j + 3) := by
    unfold Lock2
    simp only [add_assoc, Fin.reduceAdd]
    have aw3 : Active h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2))) (w (j + 3)) :=
      ⟨K.offh.1, Or.inr (u5.trans u2.symm)⟩
    have aw2 : Active h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2))) (w (j + 2)) :=
      ⟨o2, Or.inl (u6.trans u4.symm)⟩
    have a1 : (pairGraph M.graph h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2)))).Adj
        (P.x (j + 4)) (w (j + 3)) := ⟨(K.nbr4 _).2 (by simp), ⟨P.x_ne_h _, Or.inl rfl⟩, aw3⟩
    have a2 : (pairGraph M.graph h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2)))).Adj
        (w (j + 3)) (w (j + 2)) := ⟨K.ring23.symm, aw3, aw2⟩
    have a3 : (pairGraph M.graph h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2)))).Adj
        (w (j + 2)) (P.x (j + 2)) := ⟨T.adjs.2.2.2.2.2.symm, aw2, ⟨P.x_ne_h _, Or.inr rfl⟩⟩
    exact a1.reachable.trans (a2.reachable.trans a3.reachable)
  -- Step 2: `t₂ = R₊₃ t₁` at `j + 3`.
  have hK2 := rot3Def_of_lock2 P r1 L2t1
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values r1 hK2
  simp only [add_assoc, Fin.reduceAdd, add_zero] at v1 v2 v3 v4
  rw [u3] at v0
  rw [u4] at v1
  rw [u1] at v2
  rw [u3] at v3
  rw [u2] at v4
  obtain ⟨-, p2, r2, -, -⟩ := rot3_move p1 r1 L2t1
  simp only [add_assoc, Fin.reduceAdd] at r2
  have E2 : piMove P t1 = rot3 P t1 (j + 3) := by rw [piMove_rep r1, ite_eq_left L2t1]
  have v5 : rot3 P t1 (j + 3) (w (j + 3)) = r (P.x (j + 3)) := by
    rw [rot3_keep' (by rw [u5, u3]; exact h13.symm)
      (by simp only [add_assoc, Fin.reduceAdd]; rw [u5, u1]; exact h3), u5]
  have v6 : rot3 P t1 (j + 3) (w (j + 2)) = r (P.x (j + 4)) := by
    rw [rot3_keep' (by rw [u6, u3]; exact h14.symm)
      (by simp only [add_assoc, Fin.reduceAdd]; rw [u6, u1]; exact h4), u6]
  generalize ht2 : rot3 P t1 (j + 3) = t2 at *
  refine ⟨by rw [E1]; exact rep_not_target r1, by rw [E1, E2]; exact rep_not_target r2, ?_⟩
  by_cases L2t2 : Lock2 P t2 (j + 1)
  swap
  · left
    rw [E1, E2]
    exact Classical.byContradiction fun hn => L2t2 ((unfilled_succ_iff_lock2 p2 r2).1 hn)
  right
  -- Step 3: `t₃ = R₊₃ t₂` at `j + 1`.
  have hK3 := rot3Def_of_lock2 P r2 L2t2
  obtain ⟨y0, y1, y2, y3, y4⟩ := rot3_values r2 hK3
  simp only [add_assoc, Fin.reduceAdd, add_zero] at y1 y2 y3 y4
  rw [v3] at y0
  rw [v4] at y1
  rw [v1] at y2
  rw [v3] at y3
  rw [v2] at y4
  obtain ⟨-, p3, r3, l3, -⟩ := rot3_move p2 r2 L2t2
  simp only [add_assoc, Fin.reduceAdd] at r3 l3
  have E3 : piMove P t2 = rot3 P t2 (j + 1) := by rw [piMove_rep r2, ite_eq_left L2t2]
  have y5 : rot3 P t2 (j + 1) (w (j + 2)) = r (P.x (j + 1)) := by
    rw [rot3_eq_kswap]
    simp only [add_assoc, Fin.reduceAdd]
    rw [kswap_mem' (Adj.reachable ⟨T.adj3, ⟨P.x_ne_h _, Or.inl (by rw [v0, v3])⟩,
      ⟨o2, Or.inr (by rw [v6, v1])⟩⟩) (by rw [v6, v1]), v3]
  have y6 : rot3 P t2 (j + 1) (w (j + 3)) = r (P.x (j + 3)) := by
    rw [rot3_keep' (by rw [v5, v3]; exact h13.symm)
      (by simp only [add_assoc, Fin.reduceAdd]; rw [v5, v1]; exact h34), v5]
  generalize ht3 : rot3 P t2 (j + 1) = t3 at *
  -- `x (j+3)` is isolated in the `{α, B}`-graph of `t₃`.
  have iso : ∀ v, ¬ (pairGraph M.graph h t3 (t3 (P.x j)) (t3 (P.x (j + 3)))).Adj
      (P.x (j + 3)) v := by
    rintro v ⟨ea, -, av⟩
    have hv := av.2
    rw [y4, y2] at hv
    rcases (K.nbr3 v).1 ea with rfl | rfl | rfl | rfl | rfl
    · exact av.1 rfl
    · rw [y1] at hv
      rcases hv with f | f
      · exact h3 f
      · exact h34 f
    · rw [y3] at hv
      rcases hv with f | f
      · exact h1 f
      · exact h14 f
    · rw [y5] at hv
      rcases hv with f | f
      · exact h1 f
      · exact h14 f
    · rw [y6] at hv
      rcases hv with f | f
      · exact h3 f
      · exact h34 f
  have nL2t3 : ¬ Lock2 P t3 (j + 4) := by
    unfold Lock2
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    exact not_reach_of_isolated (fun e => f03 (P.inj e)) iso
  have E4 : piMove P t3 = phiBinv P t3 (j + 4) := by rw [piMove_rep r3, ite_eq_right nL2t3]
  obtain ⟨-, p4, st4, -, -⟩ := phiBinv_spec p3 r3 nL2t3
  simp only [add_assoc, Fin.reduceAdd] at st4
  -- Step 4: `t₄ = φ_B⁻¹ t₃` recolours only `x (j+3)`.
  have hphi : phiBinv P t3 (j + 4) =
      kswap M.graph h t3 (t3 (P.x j)) (t3 (P.x (j + 3))) (P.x (j + 3)) := by
    unfold phiBinv
    simp only [add_assoc, Fin.reduceAdd, add_zero]
  have z_off : ∀ v, v ≠ P.x (j + 3) → phiBinv P t3 (j + 4) v = t3 v := fun v hv => by
    rw [hphi]
    exact kswap_out fun R => not_reach_of_isolated hv iso R.symm
  have z3 : phiBinv P t3 (j + 4) (P.x (j + 3)) = r (P.x j) := by
    rw [hphi, kswap_mem' (Reachable.refl _) rfl, y4]
  have M3 : M3Short P (phiBinv P t3 (j + 4)) (j + 2) := by
    unfold M3Short zcol
    simp only [add_assoc, Fin.reduceAdd]
    rw [z_off (P.x (j + 4)) (fun e => f43 (P.inj e)), z_off (P.x (j + 2)) (fun e => f23 (P.inj e)),
      z3, y3, y1, fourth_eq h3 h13.symm h1.symm h34.symm h4 h14.symm]
    intro R
    have R' := R.mono (pairGraph_le_of_one (p := P.x (j + 3)) z_off
      (by rw [z3]; exact h1.symm) (by rw [z3]; exact h4.symm))
    have hd := rot2Def_of_lock1 P r3 l3
    unfold Rot2Def at hd
    simp only [add_assoc, Fin.reduceAdd] at hd
    rw [y3, y2] at hd
    exact hd R'
  refine ⟨by rw [E1, E2, E3]; exact rep_not_target r3, by rw [E1, E2, E3, E4]; exact st4.1, ?_⟩
  rw [E1, E2, E3, E4]
  exact fun ht => (filled_succ_iff_m3long p4 st4).1 ht M3

/-- **(2) `u34_run_length`.** The unfilled run starting at a failing `k = 4` image has length
`u ∈ {3, 4}`: `π^k s` is unfilled for `k < u` and `π^u s` is filled. -/
theorem u34_run_length (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    ∃ u, (u = 3 ∨ u = 4) ∧
      (∀ k, k < u → ¬ Target M.graph h ((piMove P)^[k] (sigSwap P r j))) ∧
      Target M.graph h ((piMove P)^[u] (sigSwap P r j)) := by
  obtain ⟨-, -, rs, -⟩ := sigSwap_basic hc hR.1.1
  obtain ⟨a1, a2, a3⟩ := u34_core K hc hR (u34_lock2_only K hc hR hF).2
  rcases a3 with b | ⟨b1, b2, -⟩
  · refine ⟨3, Or.inl rfl, fun k hk => ?_, b⟩
    rcases k with _ | _ | _ | k
    · exact rep_not_target rs
    · exact a1
    · exact a2
    · exact absurd hk (by omega)
  · refine ⟨4, Or.inr rfl, fun k hk => ?_, b2⟩
    rcases k with _ | _ | _ | _ | k
    · exact rep_not_target rs
    · exact a1
    · exact a2
    · exact b1
    · exact absurd hk (by omega)

/-- **(3) `u34_f_one`.** If the run has length `u = 4` (`π³ s` unfilled), the filled run after
it has `f = 1`: `π⁴ s` is filled (an `M3`-short state, move `φ_A`) and `π⁵ s` is unfilled. -/
theorem u34_f_one (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j))
    (hu4 : ¬ Target M.graph h ((piMove P)^[3] (sigSwap P r j))) :
    Target M.graph h ((piMove P)^[4] (sigSwap P r j)) ∧
      ¬ Target M.graph h ((piMove P)^[5] (sigSwap P r j)) := by
  obtain ⟨-, -, a3⟩ := u34_core K hc hR (u34_lock2_only K hc hR hF).2
  rcases a3 with b | ⟨-, b2, b3⟩
  · exact absurd b hu4
  · exact ⟨b2, b3⟩

/-- **U34 as an excursion.** A failing `k = 4` image starts an excursion `(s, u, f)` with
`u ∈ {3, 4}`, and `f = 1` when `u = 4`. -/
theorem u34_excursion (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    ∃ u f, (u = 3 ∨ u = 4) ∧ Excursion P (sigSwap P r j) u f ∧ (u = 4 → f = 1) := by
  obtain ⟨-, ps, rs, -⟩ := sigSwap_basic hc hR.1.1
  have hprev := (u34_run_start K hc hR hF).1
  obtain ⟨a1, a2, a3⟩ := u34_core K hc hR (u34_lock2_only K hc hR hF).2
  rcases a3 with b | ⟨b1, b2, b3⟩
  · obtain ⟨f, E⟩ := excursion_of_run (P := P) (u := 3) ps (by omega) hprev
      (fun k hk => by
        rcases k with _ | _ | _ | k
        · exact rep_not_target rs
        · exact a1
        · exact a2
        · exact absurd hk (by omega)) b
    exact ⟨3, f, Or.inl rfl, E, by omega⟩
  · refine ⟨4, 1, Or.inr rfl, ⟨ps, by omega, by omega, hprev, fun k hk => ?_,
      fun k hk hk' => ?_, b3⟩, fun _ => rfl⟩
    · rcases k with _ | _ | _ | _ | k
      · exact rep_not_target rs
      · exact a1
      · exact a2
      · exact b1
      · exact absurd hk (by omega)
    · obtain rfl : k = 4 := by omega
      exact b2

/-! ### `k = 3` -/

/-- **(4a)** At `k = 3` a failing `σ`-image is `Lock1`-only. -/
theorem u3_lock1_only (K : K3Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    Lock1 P (sigSwap P r j) j ∧ ¬ Lock2 P (sigSwap P r j) j := by
  have n2 := sigma_exit_noLock2_k3 K hc hR
  obtain ⟨-, -, rs, -⟩ := sigSwap_basic hc hR.1.1
  exact ⟨Classical.byContradiction fun n1 => hF ((noLock_rep rs).2 ⟨n1, n2⟩), n2⟩

/-- **(4) `u3_run_end`.** At `k = 3` a failing `σ`-image `s` is the last state of its unfilled
run (`π⁻¹ s` unfilled, `π s` filled), and the filled run after it has length one: `π² s` is
unfilled (forward pattern `(1, 1)`). -/
theorem u3_run_end (K : K3Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    ¬ Target M.graph h (piInv P (sigSwap P r j)) ∧
      Target M.graph h (piMove P (sigSwap P r j)) ∧
      ¬ Target M.graph h (piMove P (piMove P (sigSwap P r j))) := by
  have T := K.tri
  obtain ⟨hL1, nL2⟩ := u3_lock1_only K hc hR hF
  obtain ⟨-, -, ps, rs, sout⟩ := sigma_exit T hc hR.1.1 hR.outer
  obtain ⟨-, -, -, s0, s1, s2, s3, s4⟩ := sigSwap_basic hc hR.1.1
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, -, e3, e4⟩ := hR
  obtain ⟨-, -, -, f04, f34⟩ := fneU j
  generalize hsd : sigSwap P r j = s at *
  obtain ⟨hprev, hnext⟩ := (lemmaP ps rs).2.2.1.1 ⟨hL1, nL2⟩
  refine ⟨hprev, hnext, ?_⟩
  have E : piMove P s = phiBinv P s j := by rw [piMove_rep rs, ite_eq_right nL2]
  obtain ⟨-, pt, st, -, -⟩ := phiBinv_spec ps rs nL2
  have sw : ∀ {u}, (∀ i, u ≠ P.x i) → s u = r u := fun hu => sout _ (hu _) (hu _) (hu _)
  -- `x (j+4)` is isolated in the `{α, B}`-graph of `s`.
  have iso : ∀ u, ¬ (pairGraph M.graph h s (s (P.x (j + 1))) (s (P.x (j + 4)))).Adj
      (P.x (j + 4)) u := by
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
  have z_off : ∀ v, v ≠ P.x (j + 4) → phiBinv P s j v = s v := fun v hv =>
    kswap_out fun R => not_reach_of_isolated hv iso R.symm
  have z4 : phiBinv P s j (P.x (j + 4)) = r (P.x j) := by
    rw [show phiBinv P s j (P.x (j + 4)) = s (P.x (j + 1)) from
      kswap_mem' (Reachable.refl _) rfl, s1]
  have M3 : M3Short P (phiBinv P s j) (j + 3) := by
    unfold M3Short zcol
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    rw [z_off (P.x j) (fun e => f04 (P.inj e)), z_off (P.x (j + 3)) (fun e => f34 (P.inj e)),
      z4, s0, s3, fourth_eq h3 h13.symm h1.symm h34.symm h4 h14.symm]
    intro R
    have R' := R.mono (pairGraph_le_of_one (p := P.x (j + 4)) z_off
      (by rw [z4]; exact h1.symm) (by rw [z4]; exact h4.symm))
    have hd := rot2Def_of_lock1 P rs hL1
    unfold Rot2Def at hd
    rw [s0, s4] at hd
    exact hd R'
  rw [E]
  exact fun ht => (filled_succ_iff_m3long pt st).1 ht M3

/-! ### The `u = 3` branch: `f = 1` under a named non-local hypothesis -/

/-- The state `t₂ = π² s` of the `k = 4` colour walk: repeat index `j + 1`, `Lock1`, link
`(α, μ, A, μ, B)`, `w₂ = B`, `w₃ = A` (colours named in `r`). -/
theorem u34_two (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hL2 : Lock2 P (sigSwap P r j) j) :
    ProperOff M.graph h (piMove P (piMove P (sigSwap P r j))) ∧
    RepeatAt P (piMove P (piMove P (sigSwap P r j))) (j + 1) ∧
    Lock1 P (piMove P (piMove P (sigSwap P r j))) (j + 1) ∧
    piMove P (piMove P (sigSwap P r j)) (P.x j) = r (P.x j) ∧
    piMove P (piMove P (sigSwap P r j)) (P.x (j + 1)) = r (P.x (j + 1)) ∧
    piMove P (piMove P (sigSwap P r j)) (P.x (j + 2)) = r (P.x (j + 3)) ∧
    piMove P (piMove P (sigSwap P r j)) (P.x (j + 3)) = r (P.x (j + 1)) ∧
    piMove P (piMove P (sigSwap P r j)) (P.x (j + 4)) = r (P.x (j + 4)) ∧
    piMove P (piMove P (sigSwap P r j)) (w (j + 2)) = r (P.x (j + 4)) ∧
    piMove P (piMove P (sigSwap P r j)) (w (j + 3)) = r (P.x (j + 3)) := by
  have T := K.tri
  obtain ⟨-, -, ps, rs, sout⟩ := sigma_exit T hc hR.1.1 hR.outer
  obtain ⟨-, -, -, s0, s1, s2, s3, s4⟩ := sigSwap_basic hc hR.1.1
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, -, e2, e3, -⟩ := hR
  obtain ⟨f03, f23, f43, -, -⟩ := fneU j
  obtain ⟨-, -, -, o2⟩ := T.offh
  generalize hsd : sigSwap P r j = s at *
  have sw2 : s (w (j + 2)) = r (P.x (j + 4)) :=
    (sout _ ((T.off _).2.2.2) ((T.off _).2.2.2) ((T.off _).2.2.2)).trans e2
  have sw3 : s (w (j + 3)) = r (P.x (j + 1)) :=
    (sout _ (K.off3 _) (K.off3 _) (K.off3 _)).trans e3
  -- Step 1: `t₁ = R₊₃ s` at `j`.
  have hK1 := rot3Def_of_lock2 P rs hL2
  obtain ⟨u0, u1, u2, u3, u4⟩ := rot3_values rs hK1
  rw [s0] at u0 u3
  rw [s1] at u1
  rw [s3] at u2
  rw [s4] at u4
  obtain ⟨-, p1, r1, -, -⟩ := rot3_move ps rs hL2
  have E1 : piMove P s = rot3 P s j := by rw [piMove_rep rs, ite_eq_left hL2]
  have u5 : rot3 P s j (w (j + 3)) = r (P.x (j + 3)) := by
    have reach1 : (pairGraph M.graph h s (s (P.x j)) (s (P.x (j + 3)))).Reachable
        (P.x (j + 2)) (w (j + 3)) :=
      (rot3_reach rs).trans (Adj.reachable ⟨(K.nbr3 _).2 (by simp), ⟨P.x_ne_h _, Or.inr rfl⟩,
        ⟨K.offh.1, Or.inl (by rw [sw3, s0])⟩⟩)
    rw [rot3_eq_kswap, kswap_mem reach1 (by rw [sw3, s0]), s3]
  have u6 : rot3 P s j (w (j + 2)) = r (P.x (j + 4)) := by
    rw [rot3_keep' (by rw [sw2, s0]; exact h14.symm) (by rw [sw2, s3]; exact h34.symm), sw2]
  generalize ht1 : rot3 P s j = t1 at *
  have L2t1 : Lock2 P t1 (j + 3) := by
    unfold Lock2
    simp only [add_assoc, Fin.reduceAdd]
    have aw3 : Active h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2))) (w (j + 3)) :=
      ⟨K.offh.1, Or.inr (u5.trans u2.symm)⟩
    have aw2 : Active h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2))) (w (j + 2)) :=
      ⟨o2, Or.inl (u6.trans u4.symm)⟩
    have a1 : (pairGraph M.graph h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2)))).Adj
        (P.x (j + 4)) (w (j + 3)) := ⟨(K.nbr4 _).2 (by simp), ⟨P.x_ne_h _, Or.inl rfl⟩, aw3⟩
    have a2 : (pairGraph M.graph h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2)))).Adj
        (w (j + 3)) (w (j + 2)) := ⟨K.ring23.symm, aw3, aw2⟩
    have a3 : (pairGraph M.graph h t1 (t1 (P.x (j + 4))) (t1 (P.x (j + 2)))).Adj
        (w (j + 2)) (P.x (j + 2)) := ⟨T.adjs.2.2.2.2.2.symm, aw2, ⟨P.x_ne_h _, Or.inr rfl⟩⟩
    exact a1.reachable.trans (a2.reachable.trans a3.reachable)
  -- Step 2: `t₂ = R₊₃ t₁` at `j + 3`.
  have hK2 := rot3Def_of_lock2 P r1 L2t1
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values r1 hK2
  simp only [add_assoc, Fin.reduceAdd, add_zero] at v1 v2 v3 v4
  rw [u3] at v0
  rw [u4] at v1
  rw [u1] at v2
  rw [u3] at v3
  rw [u2] at v4
  obtain ⟨-, p2, r2, l2, -⟩ := rot3_move p1 r1 L2t1
  simp only [add_assoc, Fin.reduceAdd] at r2 l2
  have E2 : piMove P t1 = rot3 P t1 (j + 3) := by rw [piMove_rep r1, ite_eq_left L2t1]
  have v5 : rot3 P t1 (j + 3) (w (j + 3)) = r (P.x (j + 3)) := by
    rw [rot3_keep' (by rw [u5, u3]; exact h13.symm)
      (by simp only [add_assoc, Fin.reduceAdd]; rw [u5, u1]; exact h3), u5]
  have v6 : rot3 P t1 (j + 3) (w (j + 2)) = r (P.x (j + 4)) := by
    rw [rot3_keep' (by rw [u6, u3]; exact h14.symm)
      (by simp only [add_assoc, Fin.reduceAdd]; rw [u6, u1]; exact h4), u6]
  rw [E1, E2]
  exact ⟨p2, r2, l2, v2, v3, v4, v0, v1, v6, v5⟩

/-- **`u34_f_one_of_three`** (conditional). If the run has length `u = 3` (`π³ s` filled), the
filled run after it has `f = 1` (`π⁴ s` unfilled), **provided** `w₃` is not in the
`{A, α}`-component of `x j` in `t₂ = π² s` (hypothesis `hw`; `A = r (x (j+3))`, `α = r (x j)`).
That component is what `π t₂ = φ_B⁻¹` swaps. Under `hw` the vertex `x (j+3)` (colour `μ`) has
neighbours `x (j+2) = A`, `x (j+4) = B`, `w₂ = B`, `w₃ = A` in `π³ s`, so it is isolated in the
`{μ, α}`-graph and `π³ s` is `M3`-short. Without `hw`, `w₃` turns `α` and the
`{μ, α}`-component of `x (j+3)` leaves the ball (through `m`, whose colour in `t₂` is not
determined locally), so `M3Short` is then a non-local Kempe statement. -/
theorem u34_f_one_of_three (K : K4Ball P w m j) (hc : ProperOff M.graph h r)
    (hR : R3At P w r j) (hF : ¬ NoLock P (sigSwap P r j))
    (hw : ¬ (pairGraph M.graph h (piMove P (piMove P (sigSwap P r j))) (r (P.x (j + 3)))
      (r (P.x j))).Reachable (P.x j) (w (j + 3)))
    (hu3 : Target M.graph h ((piMove P)^[3] (sigSwap P r j))) :
    ¬ Target M.graph h ((piMove P)^[4] (sigSwap P r j)) := by
  have hL2 := (u34_lock2_only K hc hR hF).2
  obtain ⟨p2, r2, -, v0, v1, v2, v3, v4, v5, v6⟩ := u34_two K hc hR hL2
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -⟩ := hR
  have f13 : P.x (j + 1) ≠ P.x (j + 3) := fun e => fne13 j (P.inj e)
  show ¬ Target M.graph h (piMove P (piMove P (piMove P (piMove P (sigSwap P r j)))))
  change Target M.graph h (piMove P (piMove P (piMove P (sigSwap P r j)))) at hu3
  generalize ht2 : piMove P (piMove P (sigSwap P r j)) = t2 at *
  have nL2 : ¬ Lock2 P t2 (j + 1) := fun l => (unfilled_succ_iff_lock2 p2 r2).2 l hu3
  have E : piMove P t2 = phiBinv P t2 (j + 1) := by rw [piMove_rep r2, ite_eq_right nL2]
  obtain ⟨-, pt, st, -, -⟩ := phiBinv_spec p2 r2 nL2
  simp only [add_assoc, Fin.reduceAdd] at st
  have hphi : phiBinv P t2 (j + 1) = kswap M.graph h t2 (r (P.x (j + 3))) (r (P.x j)) (P.x j) := by
    unfold phiBinv
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    rw [v2, v0]
  have nL2' : ¬ (pairGraph M.graph h t2 (r (P.x (j + 3))) (r (P.x j))).Reachable (P.x j)
      (P.x (j + 2)) := by
    intro R
    apply nL2
    unfold Lock2
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    rw [v2, v0]
    exact R.symm
  have z1 : phiBinv P t2 (j + 1) (P.x (j + 1)) = r (P.x (j + 1)) := by
    rw [hphi, kswap_other (by rw [v1]; exact h13) (by rw [v1]; exact h1), v1]
  have z2 : phiBinv P t2 (j + 1) (P.x (j + 2)) = r (P.x (j + 3)) := by
    rw [hphi, kswap_out nL2', v2]
  have z4 : phiBinv P t2 (j + 1) (P.x (j + 4)) = r (P.x (j + 4)) := by
    rw [hphi, kswap_other (by rw [v4]; exact h34.symm) (by rw [v4]; exact h4), v4]
  have z0 : phiBinv P t2 (j + 1) (P.x j) = r (P.x (j + 3)) := by
    rw [hphi, kswap_mem' (Reachable.refl _) v0]
  have zw2 : phiBinv P t2 (j + 1) (w (j + 2)) = r (P.x (j + 4)) := by
    rw [hphi, kswap_other (by rw [v5]; exact h34.symm) (by rw [v5]; exact h4), v5]
  have zw3 : phiBinv P t2 (j + 1) (w (j + 3)) = r (P.x (j + 3)) := by
    rw [hphi, kswap_out hw, v6]
  have M3 : M3Short P (phiBinv P t2 (j + 1)) (j + 4) := by
    unfold M3Short zcol
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    rw [z1, z4, z0, fourth_eq h34.symm h14.symm h13.symm h4.symm h3.symm h1.symm]
    refine not_reach_of_isolated f13 fun v e => ?_
    obtain ⟨ea, -, av⟩ := e
    have hv := av.2
    rcases (K.nbr3 v).1 ea with rfl | rfl | rfl | rfl | rfl
    · exact av.1 rfl
    · rw [z2] at hv
      rcases hv with f | f
      · exact h13 f.symm
      · exact h3 f
    · rw [z4] at hv
      rcases hv with f | f
      · exact h14 f.symm
      · exact h4 f
    · rw [zw2] at hv
      rcases hv with f | f
      · exact h14 f.symm
      · exact h4 f
    · rw [zw3] at hv
      rcases hv with f | f
      · exact h13 f.symm
      · exact h3 f
  rw [E]
  exact fun ht => (filled_succ_iff_m3long pt st).1 ht M3

/-- **Excursion mass, unconditional.** A failing `k = 4` image starts an excursion `(s, u, f)`
with `u ∈ {3, 4}`, mass `u − 3f`; when `u = 4` the mass is `1`. -/
theorem u34_mass_bound (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) :
    ∃ u f, (u = 3 ∨ u = 4) ∧ Excursion P (sigSwap P r j) u f ∧
      excMass P (sigSwap P r j) u f = (u : ℤ) - 3 * f ∧
      (u = 4 → excMass P (sigSwap P r j) u f = 1) := by
  obtain ⟨u, f, hu, E, h4⟩ := u34_excursion K hc hR hF
  refine ⟨u, f, hu, E, excursion_mass E, fun e => ?_⟩
  rw [excursion_mass E, h4 e, e]
  norm_num

/-- **`u34_mass`** (conditional on `hw`, as in `u34_f_one_of_three`): the excursion started by
a failing `k = 4` image has `f = 1` and mass `0` (`(u, f) = (3, 1)`) or `1` (`(4, 1)`). -/
theorem u34_mass (K : K4Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j))
    (hw : ¬ (pairGraph M.graph h (piMove P (piMove P (sigSwap P r j))) (r (P.x (j + 3)))
      (r (P.x j))).Reachable (P.x j) (w (j + 3))) :
    ∃ u f, Excursion P (sigSwap P r j) u f ∧ f = 1 ∧
      (excMass P (sigSwap P r j) u f = 0 ∨ excMass P (sigSwap P r j) u f = 1) := by
  obtain ⟨u, f, hu, E, h4⟩ := u34_excursion K hc hR hF
  have hf : f = 1 := by
    rcases hu with rfl | rfl
    · by_contra hf
      have f2 : 2 ≤ f := by have := E.f_pos; omega
      exact u34_f_one_of_three K hc hR hF hw (E.fil 3 le_rfl (by omega))
        (E.fil 4 (by omega) (by omega))
    · exact h4 rfl
  refine ⟨u, f, E, hf, ?_⟩
  rw [excursion_mass E, hf]
  rcases hu with rfl | rfl
  · left; norm_num
  · right; norm_num

/-! ### `k = 3`: the excursion containing the image -/

/-- **`u3_mass`.** At `k = 3` a failing image `s` lies in an excursion `(e, u, f)` as its last
unfilled state: `s = π^(u−1) e`, `u ≥ 2`, the filled run after it has `f = 1`, and the mass is
`u − 3` (so at least `−1`). -/
theorem u3_mass (K : K3Ball P w m j) (hc : ProperOff M.graph h r) (hR : R3At P w r j)
    (hF : ¬ NoLock P (sigSwap P r j)) {e : Fin n → Fin 4} {u f k : ℕ}
    (E : Excursion P e u f) (hk : k < u + f) (hke : (piMove P)^[k] e = sigSwap P r j) :
    k + 1 = u ∧ 2 ≤ u ∧ f = 1 ∧ excMass P e u f = (u : ℤ) - 3 := by
  obtain ⟨-, -, rs, -⟩ := sigSwap_basic hc hR.1.1
  obtain ⟨hprev, hnext, hnn⟩ := u3_run_end K hc hR hF
  have hp := iter_properOff (P := P) E.proper
  have ku : k < u := by
    by_contra hl
    exact rep_not_target rs (hke ▸ E.fil k (by omega) hk)
  have k1 : k + 1 = u := by
    by_contra hl
    apply E.unf (k + 1) (by omega)
    rw [Function.iterate_succ_apply', hke]
    exact hnext
  have u2 : 2 ≤ u := by
    rcases k with _ | k
    · exfalso
      apply hprev
      rw [← hke]
      exact E.prev
    · omega
  have f1 : f = 1 := by
    by_contra hf
    have f2 : 2 ≤ f := by have := E.f_pos; omega
    apply hnn
    rw [← hke, ← Function.iterate_succ_apply' (piMove P), ← Function.iterate_succ_apply' (piMove P)]
    exact E.fil _ (by omega) (by omega)
  refine ⟨k1, u2, f1, ?_⟩
  rw [excursion_mass E, f1]
  norm_num

end sphere

end SimpleGraph.QuarterFloor

/-! ### Axiom check -/
#print axioms SimpleGraph.QuarterFloor.u34_run_start
#print axioms SimpleGraph.QuarterFloor.u34_core
#print axioms SimpleGraph.QuarterFloor.u34_run_length
#print axioms SimpleGraph.QuarterFloor.u34_f_one
#print axioms SimpleGraph.QuarterFloor.u34_excursion
#print axioms SimpleGraph.QuarterFloor.u3_run_end
#print axioms SimpleGraph.QuarterFloor.u34_f_one_of_three
#print axioms SimpleGraph.QuarterFloor.u34_mass_bound
#print axioms SimpleGraph.QuarterFloor.u34_mass
#print axioms SimpleGraph.QuarterFloor.u3_mass
