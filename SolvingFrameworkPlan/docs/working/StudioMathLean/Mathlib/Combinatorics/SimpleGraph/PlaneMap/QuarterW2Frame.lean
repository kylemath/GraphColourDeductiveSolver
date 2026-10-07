/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPeriodJ
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaFix

/-!
# The W2 frame: colours and fixed-point conditions at positions 4–8 of a period

Formalises `NightW2.md` §1 (bookkeeping, proved by hand). Setting of `gamma_period_ten`: an
all-`DL` `π`-orbit `s N = π^[N] s` from an `R3k4` state at a `Hole6 P w m q`, with
`p = x q`, `y = w (q+4)`, `z = w q`. Position `N` with `N % 10 = 4` is `R3k2`, with repeat index
`j` (`q = j + 2`); positions `N+1 … N+4` are `R1k4, R3k1, R1k3, R3k0` with repeat indices
`j+3, j+1, j+4, j+2`. The four colours are named by their values at position 4:
`1 = c₄ p`, `2 = c₄ m`, `3 = c₄ y`, `4 = c₄ z`.

## Main results (sorry-free, no new axioms)

* `chain_local`: the whole bookkeeping for four `R₊₃` steps from an `R3k2` state, with no orbit
  hypothesis (only `Rot3Def` at each step).
* `steps_pos4_to_7`: the steps `K₄ … K₇` are the Kempe swaps of
  `{1,3}` (component of `p`, `∋ y`), `{1,2}` (component of `y`, `∋ m`),
  `{1,4}` (component of `z`, `∋ m`), `{1,3}` (component of `p`, `∋ z`).
* `colours_pos4_to_8`: `(p, m, y, z)` is `(3,2,1,4), (3,1,2,4), (3,4,2,1), (1,4,2,3)` at
  positions `5, 6, 7, 8`.
* `repeat_pos4_to_8`, `links_pos4_to_8`: repeat indices and link colours
  (`1 2 1 3 4`, `1 2 3 1 4`, `2 1 3 1 4`, `2 1 3 4 1`, `2 3 1 4 1` at `x j … x (j+4)`).
* `alpha_const_pos4_8`: at every one of positions `4 … 8`, `α = c (x j')` (own repeat index
  `j'`) is colour `1`.
* `fixed_pos4_iff`, `fixed_pos6_iff`, `fixed_pos8_iff` (Lemma Fix with the roles named):
  `F₄ ⇔ {3,4}` acyclic at position 4, `F₆ ⇔ {2,4}` acyclic at position 6,
  `F₈ ⇔ {2,3}` acyclic at position 8.
* `fixed_not_lockless`: a fixed point is not a lockless exit. `W2Period` (some `k ≤ 2` exit of
  the period is lockless); `w2_not_all_acyclic`: `W2 ⇒ ¬ (F₄ ∧ F₆ ∧ F₈)` in the named pair
  graphs; `not_all_fixed_iff`: `¬ (F₄ ∧ F₆ ∧ F₈) ⇔ ¬ (all three named pair graphs acyclic)`.
  The converse of `W2 ⇒ ¬(F₄ ∧ F₆ ∧ F₈)` is **not** definitional (single-lock exits) and is
  not claimed. W2 itself is not proved.
* `p_x4_connected_R1k4` (Studio Job AK): at position 5 (`R1k4`), `p` and `x (j+4)` are joined in
  the `{3,4}`-graph; this is Lock 2 of that state.
* The fan lemma and W2′ are in `QuarterFan`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}

/-- `R₊₃` on a vertex of its component, with the colours and seed named. -/
lemma rot3_in' {c : Fin n → Fin 4} {j : Fin 5} {v s : Fin n} {a b : Fin 4}
    (ha : c (P.x j) = a) (hb : c (P.x (j + 3)) = b) (hs : P.x (j + 2) = s)
    (hv : (pairGraph M.graph h c a b).Reachable s v) :
    rot3 P c j v = Equiv.swap a b (c v) := by
  subst ha hb hs
  unfold rot3
  exact swap_in (S := {u | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
    (P.x (j + 2)) u}) hv

/-- `R₊₃` off its pair, with the colours named. -/
lemma rot3_keep' {c : Fin n → Fin 4} {j : Fin 5} {v : Fin n} {a b : Fin 4}
    (ha : c (P.x j) = a) (hb : c (P.x (j + 3)) = b) (h1 : c v ≠ a) (h2 : c v ≠ b) :
    rot3 P c j v = c v := by
  subst ha hb
  exact rot3_keep h1 h2

set_option maxHeartbeats 2000000 in
/-- **Bookkeeping of positions 4 → 8** (`NightW2.md` §1), local form. From an `R3` state `c4`
at `j` with `q = j + 2` (`R3k2`), with `α μ A B` its link colours, four `R₊₃` steps at
`j, j+3, j+1, j+4` give the table of §1 (`p = x (j+2)`, `y = w (j+1)`, `z = w (j+2)`). -/
theorem chain_local {c4 c5 c6 c7 c8 : Fin n → Fin 4} {j : Fin 5} {α μ A B : Fin 4}
    (H : Hole6 P w m q) (hq : q = j + 2) (hc : ProperOff M.graph h c4)
    (hr : RepeatAt P c4 j) (hT : TypeR3 P w c4 j)
    (hα : c4 (P.x j) = α) (hμ : c4 (P.x (j + 1)) = μ) (hA : c4 (P.x (j + 3)) = A)
    (hB : c4 (P.x (j + 4)) = B)
    (e5 : c5 = rot3 P c4 j) (e6 : c6 = rot3 P c5 (j + 3)) (e7 : c7 = rot3 P c6 (j + 1))
    (e8 : c8 = rot3 P c7 (j + 4))
    (K4 : Rot3Def P c4 j) (K5 : Rot3Def P c5 (j + 3)) (K6 : Rot3Def P c6 (j + 1))
    (K7 : Rot3Def P c7 (j + 4)) :
    (α ≠ μ ∧ α ≠ A ∧ α ≠ B ∧ μ ≠ A ∧ μ ≠ B ∧ A ≠ B) ∧
    (c4 (P.x (j + 2)) = α ∧ c4 m = μ ∧ c4 (w (j + 1)) = A ∧ c4 (w (j + 2)) = B) ∧
    (c5 (P.x (j + 2)) = A ∧ c5 m = μ ∧ c5 (w (j + 1)) = α ∧ c5 (w (j + 2)) = B) ∧
    (c6 (P.x (j + 2)) = A ∧ c6 m = α ∧ c6 (w (j + 1)) = μ ∧ c6 (w (j + 2)) = B) ∧
    (c7 (P.x (j + 2)) = A ∧ c7 m = B ∧ c7 (w (j + 1)) = μ ∧ c7 (w (j + 2)) = α) ∧
    (c8 (P.x (j + 2)) = α ∧ c8 m = B ∧ c8 (w (j + 1)) = μ ∧ c8 (w (j + 2)) = A) ∧
    (c5 (P.x j) = α ∧ c5 (P.x (j + 1)) = μ ∧ c5 (P.x (j + 3)) = α ∧ c5 (P.x (j + 4)) = B) ∧
    (c6 (P.x j) = μ ∧ c6 (P.x (j + 1)) = α ∧ c6 (P.x (j + 3)) = α ∧ c6 (P.x (j + 4)) = B) ∧
    (c7 (P.x j) = μ ∧ c7 (P.x (j + 1)) = α ∧ c7 (P.x (j + 3)) = B ∧ c7 (P.x (j + 4)) = α) ∧
    (c8 (P.x j) = μ ∧ c8 (P.x (j + 1)) = A ∧ c8 (P.x (j + 3)) = B ∧ c8 (P.x (j + 4)) = α) ∧
    (pairGraph M.graph h c4 α A).Reachable (P.x (j + 2)) (w (j + 1)) ∧
    ((pairGraph M.graph h c5 α μ).Reachable (P.x j) (w (j + 1)) ∧
      (pairGraph M.graph h c5 α μ).Reachable (w (j + 1)) m) ∧
    ((pairGraph M.graph h c6 α B).Reachable (P.x (j + 3)) (w (j + 2)) ∧
      (pairGraph M.graph h c6 α B).Reachable (w (j + 2)) m) ∧
    ((pairGraph M.graph h c7 α A).Reachable (P.x (j + 1)) (P.x (j + 2)) ∧
      (pairGraph M.graph h c7 α A).Reachable (P.x (j + 2)) (w (j + 2))) ∧
    (ProperOff M.graph h c5 ∧ ProperOff M.graph h c6 ∧ ProperOff M.graph h c7 ∧
      ProperOff M.graph h c8) ∧
    (RepeatAt P c5 (j + 3) ∧ RepeatAt P c6 (j + 1) ∧ RepeatAt P c7 (j + 4) ∧
      RepeatAt P c8 (j + 2)) := by
  subst hq
  have hr0 := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr0
  simp only [hα, hμ, hA, hB] at h02 h1 h3 h4 h13 h14 h34
  have dist : α ≠ μ ∧ α ≠ A ∧ α ≠ B ∧ μ ≠ A ∧ μ ≠ B ∧ A ≠ B :=
    ⟨h1.symm, h3.symm, h4.symm, h13, h14, h34⟩
  -- position 4
  obtain ⟨t0, t3⟩ := hT
  rw [hB] at t0
  rw [hμ] at t3
  have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
  have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  have am := hc H.adj_m (P.x_ne_h _) H.offmh
  have ay := hc H.ringy (H.offh _) H.offmh
  have az := hc H.ringz H.offmh (H.offh _)
  simp only [add_assoc, Fin.reduceAdd] at ay
  rw [← h02] at d1' d2 am
  rw [hμ] at d1
  rw [hA] at d2'
  have cp4 : c4 (P.x (j + 2)) = α := h02.symm
  have cy4 : c4 (w (j + 1)) = A := by
    clear * - h1 h3 h4 h13 h14 h34 r01 t0 d1 d1'; omega
  have cz4 : c4 (w (j + 2)) = B := by
    clear * - h1 h3 h4 h13 h14 h34 r23 t3 d2 d2'; omega
  have cm4 : c4 m = μ := by
    rw [cy4] at ay; rw [cz4] at az
    clear * - h1 h3 h4 h13 h14 h34 am ay az; omega
  -- adjacencies
  have xp1 : M.graph.Adj (P.x (j + 2)) (w (j + 1)) := by
    have e := H.adj_w' (j + 1); simp only [add_assoc, Fin.reduceAdd] at e; exact e
  have x1y : M.graph.Adj (P.x (j + 1)) (w (j + 1)) := H.adj_w (j + 1)
  have x01 : M.graph.Adj (P.x j) (P.x (j + 1)) := P.adj_cyc j
  have x12 : M.graph.Adj (P.x (j + 1)) (P.x (j + 2)) := by
    have e := P.adj_cyc (j + 1); simp only [add_assoc, Fin.reduceAdd] at e; exact e
  have x3z : M.graph.Adj (P.x (j + 3)) (w (j + 2)) := by
    have e := H.adj_w' (j + 2); simp only [add_assoc, Fin.reduceAdd] at e; exact e
  have pz : M.graph.Adj (P.x (j + 2)) (w (j + 2)) := H.adj_w (j + 2)
  have ym : M.graph.Adj (w (j + 1)) m := by
    have e := H.ringy; simp only [add_assoc, Fin.reduceAdd] at e; exact e
  have zm : M.graph.Adj (w (j + 2)) m := H.ringz.symm
  have xh := P.x_ne_h
  have wh := H.offh
  have mh := H.offmh
  -- step K₄ (position 4 → 5)
  obtain ⟨-, pr5, rp5, -⟩ := rot3_spec hc hr K4
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values hr K4
  rw [← e5] at pr5 rp5 v0 v1 v2 v3 v4
  rw [hα] at v0 v3; rw [hμ] at v1; rw [hA] at v2; rw [hB] at v4
  have R4 : (pairGraph M.graph h c4 α A).Reachable (P.x (j + 2)) (w (j + 1)) :=
    pgR xp1 (xh _) (wh _) (Or.inl cp4) (Or.inr cy4)
  have cy5 : c5 (w (j + 1)) = α := by
    rw [e5, rot3_in' hα hA rfl R4, cy4, Equiv.swap_apply_right]
  have cm5 : c5 m = μ := by
    rw [e5, rot3_keep' hα hA (by rw [cm4]; exact h1) (by rw [cm4]; exact h13), cm4]
  have cz5 : c5 (w (j + 2)) = B := by
    rw [e5, rot3_keep' hα hA (by rw [cz4]; exact h4) (by rw [cz4]; exact h34.symm), cz4]
  -- step K₅ (position 5 → 6), at `j + 3`
  obtain ⟨-, pr6, rp6, -⟩ := rot3_spec pr5 rp5 K5
  obtain ⟨u0, u1, u2, u3, u4⟩ := rot3_values rp5 K5
  rw [← e6] at pr6 rp6 u0 u1 u2 u3 u4
  simp only [add_assoc, Fin.reduceAdd, add_zero] at rp6 u0 u1 u2 u3 u4
  rw [v3] at u0 u3; rw [v4] at u1; rw [v1] at u2; rw [v2] at u4
  have ka5 : c5 (P.x (j + 3)) = α := v3
  have kb5 : c5 (P.x (j + 3 + 3)) = μ := by simp only [add_assoc, Fin.reduceAdd]; exact v1
  have ks5 : P.x (j + 3 + 2) = P.x j := by simp only [add_assoc, Fin.reduceAdd, add_zero]
  have R5a : (pairGraph M.graph h c5 α μ).Reachable (P.x j) (w (j + 1)) :=
    (pgR x01 (xh _) (xh _) (Or.inl v0) (Or.inr v1)).trans
      (pgR x1y (xh _) (wh _) (Or.inr v1) (Or.inl cy5))
  have R5b : (pairGraph M.graph h c5 α μ).Reachable (w (j + 1)) m :=
    pgR ym (wh _) mh (Or.inl cy5) (Or.inr cm5)
  have cy6 : c6 (w (j + 1)) = μ := by
    rw [e6, rot3_in' ka5 kb5 ks5 R5a, cy5, Equiv.swap_apply_left]
  have cm6 : c6 m = α := by
    rw [e6, rot3_in' ka5 kb5 ks5 (R5a.trans R5b), cm5, Equiv.swap_apply_right]
  have cp6 : c6 (P.x (j + 2)) = A := u4
  have cz6 : c6 (w (j + 2)) = B := by
    rw [e6, rot3_keep' ka5 kb5 (by rw [cz5]; exact h4) (by rw [cz5]; exact h14.symm), cz5]
  -- step K₆ (position 6 → 7), at `j + 1`
  obtain ⟨-, pr7, rp7, -⟩ := rot3_spec pr6 rp6 K6
  obtain ⟨g0, g1, g2, g3, g4⟩ := rot3_values rp6 K6
  rw [← e7] at pr7 rp7 g0 g1 g2 g3 g4
  simp only [add_assoc, Fin.reduceAdd, add_zero] at rp7 g0 g1 g2 g3 g4
  rw [u3] at g0 g3; rw [u4] at g1; rw [u1] at g2; rw [u2] at g4
  have ka6 : c6 (P.x (j + 1)) = α := u3
  have kb6 : c6 (P.x (j + 1 + 3)) = B := by simp only [add_assoc, Fin.reduceAdd]; exact u1
  have ks6 : P.x (j + 1 + 2) = P.x (j + 3) := by simp only [add_assoc, Fin.reduceAdd]
  have R6a : (pairGraph M.graph h c6 α B).Reachable (P.x (j + 3)) (w (j + 2)) :=
    pgR x3z (xh _) (wh _) (Or.inl u0) (Or.inr cz6)
  have R6b : (pairGraph M.graph h c6 α B).Reachable (w (j + 2)) m :=
    pgR zm (wh _) mh (Or.inr cz6) (Or.inl cm6)
  have cz7 : c7 (w (j + 2)) = α := by
    rw [e7, rot3_in' ka6 kb6 ks6 R6a, cz6, Equiv.swap_apply_right]
  have cm7 : c7 m = B := by
    rw [e7, rot3_in' ka6 kb6 ks6 (R6a.trans R6b), cm6, Equiv.swap_apply_left]
  have cp7 : c7 (P.x (j + 2)) = A := g1
  have cy7 : c7 (w (j + 1)) = μ := by
    rw [e7, rot3_keep' ka6 kb6 (by rw [cy6]; exact h1) (by rw [cy6]; exact h14), cy6]
  -- step K₇ (position 7 → 8), at `j + 4`
  obtain ⟨-, pr8, rp8, -⟩ := rot3_spec pr7 rp7 K7
  obtain ⟨f0, f1, f2, f3, f4⟩ := rot3_values rp7 K7
  rw [← e8] at pr8 rp8 f0 f1 f2 f3 f4
  simp only [add_assoc, Fin.reduceAdd, add_zero] at rp8 f0 f1 f2 f3 f4
  rw [g3] at f0 f3; rw [g4] at f1; rw [g1] at f2; rw [g2] at f4
  have ka7 : c7 (P.x (j + 4)) = α := g3
  have kb7 : c7 (P.x (j + 4 + 3)) = A := by simp only [add_assoc, Fin.reduceAdd]; exact g1
  have ks7 : P.x (j + 4 + 2) = P.x (j + 1) := by simp only [add_assoc, Fin.reduceAdd]
  have R7a : (pairGraph M.graph h c7 α A).Reachable (P.x (j + 1)) (P.x (j + 2)) :=
    pgR x12 (xh _) (xh _) (Or.inl g0) (Or.inr cp7)
  have R7b : (pairGraph M.graph h c7 α A).Reachable (P.x (j + 2)) (w (j + 2)) :=
    pgR pz (xh _) (wh _) (Or.inr cp7) (Or.inl cz7)
  have cz8 : c8 (w (j + 2)) = A := by
    rw [e8, rot3_in' ka7 kb7 ks7 (R7a.trans R7b), cz7, Equiv.swap_apply_left]
  have cm8 : c8 m = B := by
    rw [e8, rot3_keep' ka7 kb7 (by rw [cm7]; exact h4) (by rw [cm7]; exact h34.symm), cm7]
  have cy8 : c8 (w (j + 1)) = μ := by
    rw [e8, rot3_keep' ka7 kb7 (by rw [cy7]; exact h1) (by rw [cy7]; exact h13), cy7]
  exact ⟨dist, ⟨cp4, cm4, cy4, cz4⟩, ⟨v2, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨f3, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u2, u3, u0, u1⟩,
    ⟨g4, g0, g2, g3⟩, ⟨f1, f2, f4, f0⟩, R4, ⟨R5a, R5b⟩, ⟨R6a, R6b⟩, ⟨R7a, R7b⟩,
    ⟨pr5, pr6, pr7, pr8⟩, ⟨rp5, rp6, rp7, rp8⟩⟩

/-! ### A fixed point is not a lockless exit -/

/-- At a doubly locked state, if `σ` is a fixed point then `σ c` is `c` up to the colour names
(`sigmaFixed_iff_sigSwap`), so it is doubly locked at the same `j`: the exit is not lockless. -/
theorem fixed_not_lockless {c : Fin n → Fin 4} {j : Fin 5} (hd : DoublyLocked P c j)
    (hf : SigmaFixed P c j) : ¬ NoLock P (sigSwap P c j) := by
  rintro ⟨j', hr', l1, -⟩
  have key := (sigmaFixed_iff_sigSwap hd.1).1 hf
  set τ := Equiv.swap (c (P.x j)) (c (P.x (j + 1))) with hτ
  have kx : ∀ i, sigSwap P c j (P.x i) = τ (c (P.x i)) := fun i => key _ (P.x_ne_h i)
  have act : ∀ a b u, Active h (sigSwap P c j) (τ a) (τ b) u ↔ Active h c a b u := by
    intro a b u
    unfold Active
    constructor
    · rintro ⟨hu, e⟩
      rw [key u hu] at e
      exact ⟨hu, e.imp (fun e => τ.injective e) (fun e => τ.injective e)⟩
    · rintro ⟨hu, e⟩
      rw [key u hu]
      exact ⟨hu, e.imp (congrArg τ) (congrArg τ)⟩
  have pg : ∀ a b, pairGraph M.graph h (sigSwap P c j) (τ a) (τ b) =
      pairGraph M.graph h c a b := by
    intro a b
    ext u v
    show M.graph.Adj u v ∧ _ ∧ _ ↔ M.graph.Adj u v ∧ _ ∧ _
    rw [act, act]
  have hr : RepeatAt P c j' := by
    unfold RepeatAt at hr' ⊢
    simp only [kx, Equiv.apply_eq_iff_eq, ne_eq] at hr'
    simpa only [ne_eq] using hr'
  have e := rep_unique hd.1 hr
  subst e
  apply l1
  unfold Lock1
  rw [kx, kx, pg]
  exact hd.2.1

/-! ### The orbit setting -/

section orbit
variable {s : Fin n → Fin 4} {j₀ : Fin 5}

/-- One `DD` step on an all-`DL` orbit: `π = R₊₃` at `j`, defined, image doubly locked at
`j + 3`. -/
lemma orbit_rot3 (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (N : ℕ) {j : Fin 5} (hd : DoublyLocked P ((piMove P)^[N] s) j) :
    (piMove P)^[N + 1] s = rot3 P ((piMove P)^[N] s) j ∧ Rot3Def P ((piMove P)^[N] s) j ∧
      DoublyLocked P ((piMove P)^[N + 1] s) (j + 3) := by
  have hD := orbit_dd hc hall N j hd
  have hπ : piMove P ((piMove P)^[N] s) = rot3 P ((piMove P)^[N] s) j := by
    rw [piMove_rep hd.1, ite_eq_left hd.2.2]
  rw [Function.iterate_succ_apply']
  exact ⟨hπ, rot3Def_of_lock2 P hd.1 hd.2.2, hD.2⟩

/-- The setting of positions `4 … 8`: at `N % 10 = 4` the state is `R3k2` with `q = j + 2`, and
the next four steps are `R₊₃` at `j, j+3, j+1, j+4`. -/
theorem w2_setup (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    q = j + 2 ∧ TypeR3 P w ((piMove P)^[N] s) j ∧ ProperOff M.graph h ((piMove P)^[N] s) ∧
    (piMove P)^[N + 1] s = rot3 P ((piMove P)^[N] s) j ∧
    (piMove P)^[N + 2] s = rot3 P ((piMove P)^[N + 1] s) (j + 3) ∧
    (piMove P)^[N + 3] s = rot3 P ((piMove P)^[N + 2] s) (j + 1) ∧
    (piMove P)^[N + 4] s = rot3 P ((piMove P)^[N + 3] s) (j + 4) ∧
    Rot3Def P ((piMove P)^[N] s) j ∧ Rot3Def P ((piMove P)^[N + 1] s) (j + 3) ∧
    Rot3Def P ((piMove P)^[N + 2] s) (j + 1) ∧ Rot3Def P ((piMove P)^[N + 3] s) (j + 4) ∧
    DoublyLocked P ((piMove P)^[N] s) j := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq N = (.R3, 2) := by rw [gseq_mod, hN]; decide
  obtain ⟨j', hd, hq', hT'⟩ := tk N
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  have ej := rep_unique hd.1 hj
  subst ej
  have o1 := orbit_rot3 hc hall N hd
  have o2 := orbit_rot3 hc hall (N + 1) o1.2.2
  have i1 : j + 3 + 3 = j + 1 := by simp only [add_assoc, Fin.reduceAdd]
  rw [i1] at o2
  have o3 := orbit_rot3 hc hall (N + 1 + 1) o2.2.2
  have i2 : j + 1 + 3 = j + 4 := by simp only [add_assoc, Fin.reduceAdd]
  rw [i2] at o3
  have o4 := orbit_rot3 hc hall (N + 1 + 1 + 1) o3.2.2
  exact ⟨hq', hT', iter_proper hc N, o1.1, o2.1, o3.1, o4.1, o1.2.1, o2.2.1, o3.2.1, o4.2.1, hd⟩

/-- The four steps `K₄ … K₇` (`NightW2.md` §1, last column), with colours named at position 4
(`1 = c₄ p`, `2 = c₄ m`, `3 = c₄ y`, `4 = c₄ z`): `K₄` swaps the `{1,3}`-component of `p`
(`∋ y`), `K₅` the `{1,2}`-component of `y` (`∋ m`), `K₆` the `{1,4}`-component of `z`
(`∋ m`), `K₇` the `{1,3}`-component of `p` (`∋ z`). -/
theorem steps_pos4_to_7 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    (piMove P)^[N + 1] s = swap ((piMove P)^[N] s) (((piMove P)^[N] s) (P.x q))
      (((piMove P)^[N] s) (w (q + 4)))
      {v | (pairGraph M.graph h ((piMove P)^[N] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) (w (q + 4)))).Reachable (P.x q) v} ∧
    (pairGraph M.graph h ((piMove P)^[N] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) (w (q + 4)))).Reachable (P.x q) (w (q + 4)) ∧
    (piMove P)^[N + 2] s = swap ((piMove P)^[N + 1] s) (((piMove P)^[N] s) (P.x q))
      (((piMove P)^[N] s) m)
      {v | (pairGraph M.graph h ((piMove P)^[N + 1] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) m)).Reachable (w (q + 4)) v} ∧
    (pairGraph M.graph h ((piMove P)^[N + 1] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) m)).Reachable (w (q + 4)) m ∧
    (piMove P)^[N + 3] s = swap ((piMove P)^[N + 2] s) (((piMove P)^[N] s) (P.x q))
      (((piMove P)^[N] s) (w q))
      {v | (pairGraph M.graph h ((piMove P)^[N + 2] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) (w q))).Reachable (w q) v} ∧
    (pairGraph M.graph h ((piMove P)^[N + 2] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) (w q))).Reachable (w q) m ∧
    (piMove P)^[N + 4] s = swap ((piMove P)^[N + 3] s) (((piMove P)^[N] s) (P.x q))
      (((piMove P)^[N] s) (w (q + 4)))
      {v | (pairGraph M.graph h ((piMove P)^[N + 3] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) (w (q + 4)))).Reachable (P.x q) v} ∧
    (pairGraph M.graph h ((piMove P)^[N + 3] s) (((piMove P)^[N] s) (P.x q))
        (((piMove P)^[N] s) (w (q + 4)))).Reachable (P.x q) (w q) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, -⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, -, -, ⟨g1, -, -, -⟩, -, ⟨-, v1, v3, -⟩, ⟨-, u3, -, u1⟩, ⟨-, -, -, g3⟩,
    -, R4, ⟨R5a, R5b⟩, ⟨R6a, R6b⟩, ⟨R7a, R7b⟩, -, -⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  simp only [add_assoc, Fin.reduceAdd]
  simp only [cp4, cm4, cy4, cz4]
  refine ⟨?_, R4, ?_, R5b, ?_, R6b, ?_, R7b⟩
  · rw [e5]; rfl
  · rw [e6]; unfold rot3
    simp only [add_assoc, Fin.reduceAdd, add_zero, v1, v3]
    congr 1; ext v; exact ⟨fun r => R5a.symm.trans r, fun r => R5a.trans r⟩
  · rw [e7]; unfold rot3
    simp only [add_assoc, Fin.reduceAdd, u1, u3]
    congr 1; ext v; exact ⟨fun r => R6a.symm.trans r, fun r => R6a.trans r⟩
  · rw [e8]; unfold rot3
    simp only [add_assoc, Fin.reduceAdd, g3, g1]
    congr 1; ext v; exact ⟨fun r => R7a.symm.trans r, fun r => R7a.trans r⟩

/-- **Colours of `p, m, y, z` at positions 5–8** (`NightW2.md` §1 table), named at position 4
(`1 = c₄ p`, `2 = c₄ m`, `3 = c₄ y`, `4 = c₄ z`): `(3,2,1,4)`, `(3,1,2,4)`, `(3,4,2,1)`,
`(1,4,2,3)`. -/
theorem colours_pos4_to_8 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    ((piMove P)^[N + 1] s) (P.x q) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 1] s) m = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 1] s) (w (q + 4)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 1] s) (w q) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 2] s) (P.x q) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 2] s) m = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 2] s) (w (q + 4)) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 2] s) (w q) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 3] s) (P.x q) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 3] s) m = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 3] s) (w (q + 4)) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 3] s) (w q) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 4] s) (P.x q) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 4] s) m = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 4] s) (w (q + 4)) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 4] s) (w q) = ((piMove P)^[N] s) (w (q + 4)) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  simp only [add_assoc, Fin.reduceAdd]
  simp only [cp4, cm4, cy4, cz4, cp5, cm5, cy5, cz5, cp6, cm6, cy6, cz6, cp7, cm7, cy7, cz7, cp8,
    cm8, cy8, cz8, and_self]

/-- **Repeat indices** at positions 4–8: `j, j+3, j+1, j+4, j+2` (`q = j + 2`). -/
theorem repeat_pos4_to_8 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    q = j + 2 ∧ RepeatAt P ((piMove P)^[N + 1] s) (j + 3) ∧ RepeatAt P ((piMove P)^[N + 2] s) (j + 1) ∧
    RepeatAt P ((piMove P)^[N + 3] s) (j + 4) ∧ RepeatAt P ((piMove P)^[N + 4] s) (j + 2) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  exact ⟨rfl, rp5, rp6, rp7, rp8⟩

/-- **Link colours** at positions 4–8 on `x j, …, x (j+4)`, named at position 4:
`1 2 1 3 4`, `1 2 3 1 4`, `2 1 3 1 4`, `2 1 3 4 1`, `2 3 1 4 1`. -/
theorem links_pos4_to_8 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    ((piMove P)^[N] s) (P.x j) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N] s) (P.x (j + 1)) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N] s) (P.x (j + 2)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N] s) (P.x (j + 3)) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N] s) (P.x (j + 4)) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 1] s) (P.x j) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 1] s) (P.x (j + 1)) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 1] s) (P.x (j + 2)) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 1] s) (P.x (j + 3)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 1] s) (P.x (j + 4)) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 2] s) (P.x j) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 2] s) (P.x (j + 1)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 2] s) (P.x (j + 2)) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 2] s) (P.x (j + 3)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 2] s) (P.x (j + 4)) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 3] s) (P.x j) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 3] s) (P.x (j + 1)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 3] s) (P.x (j + 2)) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 3] s) (P.x (j + 3)) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 3] s) (P.x (j + 4)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 4] s) (P.x j) = ((piMove P)^[N] s) m ∧
    ((piMove P)^[N + 4] s) (P.x (j + 1)) = ((piMove P)^[N] s) (w (q + 4)) ∧
    ((piMove P)^[N + 4] s) (P.x (j + 2)) = ((piMove P)^[N] s) (P.x q) ∧
    ((piMove P)^[N + 4] s) (P.x (j + 3)) = ((piMove P)^[N] s) (w q) ∧
    ((piMove P)^[N + 4] s) (P.x (j + 4)) = ((piMove P)^[N] s) (P.x q) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  simp only [add_assoc, Fin.reduceAdd]
  simp only [cp4, cm4, cy4, cz4, cp5, cp6, cp7, cp8, v0, v1, v3, v4, u0, u1, u3, u4, g0, g1, g3,
    g4, f0, f1, f3, f4, and_self]

/-- **Colour 1 is `α` at positions 4–8**: at each of these states, `α = c (x j')` for the
state's own repeat index `j'` is `c₄ p`. -/
theorem alpha_const_pos4_8 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    ∀ i, i ≤ 4 → ∀ j', RepeatAt P ((piMove P)^[N + i] s) j' →
      ((piMove P)^[N + i] s) (P.x j') = ((piMove P)^[N] s) (P.x q) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  intro i hi j' hj'
  rcases (show i = 0 ∨ i = 1 ∨ i = 2 ∨ i = 3 ∨ i = 4 by omega) with rfl | rfl | rfl | rfl | rfl
  · rw [add_zero] at hj' ⊢; rw [rep_unique hj hj', cp4]
  · rw [rep_unique rp5 hj', v3, cp4]
  · rw [rep_unique rp6 hj', u1, cp4]
  · rw [rep_unique rp7 hj', g4, cp4]
  · rw [rep_unique rp8 hj', cp8, cp4]

/-- **`F₄`** (`R3k2`, position 4): `σ` is a fixed point iff the `{3,4}`-graph is acyclic. -/
theorem fixed_pos4_iff (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    SigmaFixed P ((piMove P)^[N] s) j ↔ (pairGraph M.graph h ((piMove P)^[N] s) (((piMove P)^[N] s) (w (q + 4))) (((piMove P)^[N] s) (w q))).IsAcyclic := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  simp only [add_assoc, Fin.reduceAdd]
  rw [sigmaFixed_iff_acyclic htri hconn hc4 hj, cy4, cz4]

/-- **`F₆`** (`R3k1`, position 6, repeat index `j + 1`): fixed iff the `{2,4}`-graph is
acyclic. -/
theorem fixed_pos6_iff (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    SigmaFixed P ((piMove P)^[N + 2] s) (j + 1) ↔ (pairGraph M.graph h ((piMove P)^[N + 2] s) (((piMove P)^[N] s) m) (((piMove P)^[N] s) (w q))).IsAcyclic := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  rw [sigmaFixed_iff_acyclic htri hconn pr6 rp6]
  simp only [add_assoc, Fin.reduceAdd, add_zero, u4, u0, cm4, cz4]
  rw [pairGraph_comm_gen]

/-- **`F₈`** (`R3k0`, position 8, repeat index `j + 2`): fixed iff the `{2,3}`-graph is
acyclic. -/
theorem fixed_pos8_iff (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    SigmaFixed P ((piMove P)^[N + 4] s) (j + 2) ↔ (pairGraph M.graph h ((piMove P)^[N + 4] s) (((piMove P)^[N] s) m) (((piMove P)^[N] s) (w (q + 4)))).IsAcyclic := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  rw [sigmaFixed_iff_acyclic htri hconn pr8 rp8]
  simp only [add_assoc, Fin.reduceAdd, add_zero, f0, f1, cm4, cy4]

variable (P) in
/-- **W2 for the period** at position `N` (`N % 10 = 4`, repeat index `j`): some `k ≤ 2` exit
(`R3k2`, `R3k1`, `R3k0` at positions 4, 6, 8) is lockless. -/
def W2Period (s : Fin n → Fin 4) (N : ℕ) (j : Fin 5) : Prop :=
  NoLock P (sigSwap P ((piMove P)^[N] s) j) ∨ NoLock P (sigSwap P ((piMove P)^[N + 2] s) (j + 1)) ∨
    NoLock P (sigSwap P ((piMove P)^[N + 4] s) (j + 2))

/-- **`¬ (F₄ ∧ F₆ ∧ F₈)` in the named pair graphs** (unfolding through Lemma Fix). -/
theorem not_all_fixed_iff (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    ¬ (SigmaFixed P ((piMove P)^[N] s) j ∧ SigmaFixed P ((piMove P)^[N + 2] s) (j + 1) ∧ SigmaFixed P ((piMove P)^[N + 4] s) (j + 2)) ↔
    ¬ ((pairGraph M.graph h ((piMove P)^[N] s) (((piMove P)^[N] s) (w (q + 4))) (((piMove P)^[N] s) (w q))).IsAcyclic ∧
      (pairGraph M.graph h ((piMove P)^[N + 2] s) (((piMove P)^[N] s) m) (((piMove P)^[N] s) (w q))).IsAcyclic ∧
      (pairGraph M.graph h ((piMove P)^[N + 4] s) (((piMove P)^[N] s) m) (((piMove P)^[N] s) (w (q + 4)))).IsAcyclic) := by
  rw [fixed_pos4_iff htri hconn H hc hall hr hq hT hN hj,
    fixed_pos6_iff htri hconn H hc hall hr hq hT hN hj,
    fixed_pos8_iff htri hconn H hc hall hr hq hT hN hj]

/-- **W2 ⇒ ¬ (F₄ ∧ F₆ ∧ F₈)**: a fixed point is never a lockless exit. (The converse fails
only through single-lock exits; it is not claimed.) -/
theorem w2_not_all_acyclic (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j)
    (hW : W2Period P s N j) :
    ¬ ((pairGraph M.graph h ((piMove P)^[N] s) (((piMove P)^[N] s) (w (q + 4))) (((piMove P)^[N] s) (w q))).IsAcyclic ∧
      (pairGraph M.graph h ((piMove P)^[N + 2] s) (((piMove P)^[N] s) m) (((piMove P)^[N] s) (w q))).IsAcyclic ∧
      (pairGraph M.graph h ((piMove P)^[N + 4] s) (((piMove P)^[N] s) m) (((piMove P)^[N] s) (w (q + 4)))).IsAcyclic) := by
  rw [← not_all_fixed_iff htri hconn H hc hall hr hq hT hN hj]
  obtain ⟨-, -, rp6, -, rp8⟩ := repeat_pos4_to_8 H hc hall hr hq hT hN hj
  have dl : ∀ i (j' : Fin 5), RepeatAt P ((piMove P)^[i] s) j' →
      DoublyLocked P ((piMove P)^[i] s) j' := fun i j' r => ⟨r, (dl_rep r).1 (hall i)⟩
  rintro ⟨f4, f6, f8⟩
  rcases hW with e | e | e
  · exact fixed_not_lockless (dl _ _ hj) f4 e
  · exact fixed_not_lockless (dl _ _ rp6) f6 e
  · exact fixed_not_lockless (dl _ _ rp8) f8 e

/-- **`p` and `x (j+4)` are `{3,4}`-joined at `R1k4`** (position 5; Studio Job AK). This is
Lock 2 of the position-5 state (repeat index `j + 3`), whose `{μ, B}` pair is `{4, 3}`:
`μ = c₅ (x (j+4)) = 4` and `B = c₅ (x (j+2)) = c₅ p = 3`. -/
theorem p_x4_connected_R1k4 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    (pairGraph M.graph h ((piMove P)^[N + 1] s) (((piMove P)^[N] s) (w (q + 4))) (((piMove P)^[N] s) (w q))).Reachable (P.x q) (P.x (j + 4)) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, ⟨cp5, cm5, cy5, cz5⟩, ⟨cp6, cm6, cy6, cz6⟩,
    ⟨cp7, cm7, cy7, cz7⟩, ⟨cp8, cm8, cy8, cz8⟩, ⟨v0, v1, v3, v4⟩, ⟨u0, u1, u3, u4⟩,
    ⟨g0, g1, g3, g4⟩, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  have hd5 := (orbit_rot3 hc hall N hd4).2.2
  have l2 := hd5.2.2
  unfold Lock2 at l2
  simp only [add_assoc, Fin.reduceAdd] at l2 ⊢
  rw [v4, cp5, ← cz4, ← cy4, pairGraph_comm_gen] at l2
  exact l2.symm

end orbit

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.chain_local
#print axioms SimpleGraph.QuarterFloor.steps_pos4_to_7
#print axioms SimpleGraph.QuarterFloor.colours_pos4_to_8
#print axioms SimpleGraph.QuarterFloor.repeat_pos4_to_8
#print axioms SimpleGraph.QuarterFloor.links_pos4_to_8
#print axioms SimpleGraph.QuarterFloor.alpha_const_pos4_8
#print axioms SimpleGraph.QuarterFloor.fixed_pos4_iff
#print axioms SimpleGraph.QuarterFloor.fixed_pos6_iff
#print axioms SimpleGraph.QuarterFloor.fixed_pos8_iff
#print axioms SimpleGraph.QuarterFloor.not_all_fixed_iff
#print axioms SimpleGraph.QuarterFloor.fixed_not_lockless
#print axioms SimpleGraph.QuarterFloor.w2_not_all_acyclic
#print axioms SimpleGraph.QuarterFloor.p_x4_connected_R1k4
