/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterGammaPeriod
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterJordanDual

/-!
# The period lemma for the `y – z` join `J` at a `(5,5,5,5,6)` hole

Formalises `NightLemmaS.md` §0 (Lemmas P1, P2, Corollary P3). Setting and notation as in
`QuarterGammaPeriod`: `Hole6 P w m q`, `p = x q` of degree six, `y = w (q+4)`, `z = w q` the two
ring vertices flanking `m`. `JoinYZ G h w q c` (the note's `J`) is
"`y ∼ z` in the `{c y, c z}`-graph of `c` with the hole `h` deleted".

## Main results (sorry-free, no new axioms)

1. **P1** `join_R3`, `join_R1`, `forced_join`: `J` holds at every `R3` state with
   `k ∈ {0, 1, 2}` (only `RepeatAt` and the type are needed) and every `R1` `DD` state with
   `k ∈ {3, 4}`, by an explicit six-vertex two-coloured path around the hole avoiding `m`. This is
   the only place where the single degree-six position enters: the path uses the four ring
   edges `w t ~ w (t+1)` that `Hole6` keeps.
2. **P2** `pm_step_join`: if the swapped pair of a `DD` step is carried by `{p, m}` (in either
   order), the step does not change `J`: `y, z` are adjacent to `p` and `m`, so their colours lie
   outside the swapped pair, and an `{a, b}`-swap fixes every `{x, y}`-graph with `{x, y}`
   disjoint from `{a, b}` (`pairGraph_swap_other`). By `pair_own` this applies at `R3k3`
   (pair `(m, p)`) and `R1k2` (pair `(p, m)`), i.e. at period steps `2` and `9`.
3. **P3** `period_J` (over the all-`DL` orbit setting of `gamma_period_ten`, `s n = π^[n] s`):
   * `J (s n)` for `n % 10 ∈ {4, …, 8}` (`R3k2 R1k4 R3k1 R1k3 R3k0`), so any break is undone
     by the `R3k2` state;
   * `J (s (n+1)) ↔ J (s n)` for `n % 10 ∈ {2, 9}`;
   * hence `J` can change only at steps `n % 10 ∈ {0, 1, 3, 8}`.
4. `k4_lockless_iff_join`: at an `R3` state at `k = 4` (triangulated), the `σ`-exit is lockless
   iff `J` holds there (from `sigma_exit_criterion_k4'`, not reproved: the `{μ, A}`-component
   of `x (j+1)` contains `y = w (j+3)` by Lock 1).
5. **Main theorem** `k4_exit_period`: on an all-`DL` orbit from an `R3k4` state at a `Hole6`,
   at the `(b+1)`-st `R3k4` state `s (10 b + 10)` (repeat index `j`, `q = j + 4`):
   `J (s (10 b + 8))` holds and the `σ`-exit is lockless iff `J (s (10 b + 9))`, i.e. iff the
   `R₊₃` swap at the preceding `R3k0` state (step 8) did not break `J`.
   `k4_failure_iff_break`: the exit is not lockless iff step 8 broke `J`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- The `y – z` join `J`: `y = w (q+4)` and `z = w q` are joined in the `{c y, c z}`-graph of
`c` with `h` deleted. -/
def JoinYZ {V : Type*} (G : SimpleGraph V) (h : V) (w : Fin 5 → V) (q : Fin 5)
    (c : V → Fin 4) : Prop :=
  (pairGraph G h c (c (w (q + 4))) (c (w q))).Reachable (w (q + 4)) (w q)

/-- The `(type, k)` at which P1 forces `J`: `R3` with `k ≤ 2`, `R1` with `k ≥ 3`. -/
def isForced : GType × Fin 5 → Bool
  | (.R3, k) => decide (k.val ≤ 2)
  | (.R1, k) => decide (3 ≤ k.val)

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

/-- An edge of the two-colour graph. -/
lemma pgR {a b : Fin 4} {u v : Fin n} (e : M.graph.Adj u v) (hu : u ≠ h) (hv : v ≠ h)
    (cu : c u = a ∨ c u = b) (cv : c v = a ∨ c v = b) :
    (pairGraph M.graph h c a b).Reachable u v :=
  Adj.reachable ⟨e, ⟨hu, cu⟩, ⟨hv, cv⟩⟩

/-- A ring edge kept by `Hole6`. -/
lemma Hole6.ringR {k : Fin 5} (H : Hole6 P w m (j + k)) (a : Fin 5) (hk : a + 1 ≠ k) :
    M.graph.Adj (w (j + a)) (w (j + a + 1)) :=
  H.ring (j + a) (by rw [add_assoc]; exact fin5_ne hk)

/-! ### P1: five forced joins -/

/-- **P1, `R3`.** At an `R3` state with `k ∈ {0, 1, 2}` (ring `(B, A, B, μ, A)`), `J` holds:
`k = 0`: `w₄ x₄ x₃ w₂ w₁ w₀`; `k = 1`: `w₀ w₄ x₄ x₃ w₂ w₁`; `k = 2`: `w₁ w₀ w₄ x₄ x₃ w₂`. -/
theorem join_R3 {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hT : TypeR3 P w c j) (hk : k = 0 ∨ k = 1 ∨ k = 2) :
    JoinYZ M.graph h w q c := by
  subst hq
  obtain ⟨t0, t3⟩ := hT
  obtain ⟨d0, d0'⟩ := H.dom hc j
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have e44 := (H.adj_w (j + 4)).symm
  have e43 := (P.adj_cyc (j + 3)).symm
  have e32 := H.adj_w4 (j + 3)
  simp only [add_assoc, Fin.reduceAdd] at e43 e32
  have o0 := H.offh j
  have o1 := H.offh (j + 1)
  have o2 := H.offh (j + 2)
  have o4 := H.offh (j + 4)
  have x3 := P.x_ne_h (j + 3)
  have x4 := P.x_ne_h (j + 4)
  unfold JoinYZ
  obtain rfl | rfl | rfl := hk
  · -- k = 0: y = w₄ (A), z = w₀ (B)
    simp only [add_zero]
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl (fin5_ne (by decide))
    have f4 : c (w (j + 4)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 t3; omega
    have f2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
    have f1 : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r12 f2; omega
    have e21 := (H.ringR 1 (by decide)).symm
    have e10 := (H.ringR 0 (by decide)).symm
    simp only [add_assoc, Fin.reduceAdd, add_zero] at e21 e10
    exact (pgR e44 o4 x4 (Or.inl rfl) (by rw [t0]; exact Or.inr rfl)).trans
      ((pgR e43 x4 x3 (by rw [t0]; exact Or.inr rfl) (by rw [f4]; exact Or.inl rfl)).trans
      ((pgR e32 x3 o2 (by rw [f4]; exact Or.inl rfl) (by rw [f2, t0]; exact Or.inr rfl)).trans
      ((pgR e21 o2 o1 (by rw [f2, t0]; exact Or.inr rfl) (by rw [f1, f4]; exact Or.inl rfl)).trans
      (pgR e10 o1 o0 (by rw [f1, f4]; exact Or.inl rfl) (Or.inr rfl)))))
  · -- k = 1: y = w₀ (B), z = w₁ (A)
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl (fin5_ne (by decide))
    have f4 : c (w (j + 4)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 t3; omega
    have f2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
    have f1 : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r12 f2; omega
    have e04 := (H.ringR 4 (by decide)).symm
    have e21 := (H.ringR 1 (by decide)).symm
    simp only [add_assoc, Fin.reduceAdd, add_zero] at e04 e21
    exact (pgR e04 o0 o4 (Or.inl rfl) (by rw [f4, f1]; exact Or.inr rfl)).trans
      ((pgR e44 o4 x4 (by rw [f4, f1]; exact Or.inr rfl) (by rw [t0]; exact Or.inl rfl)).trans
      ((pgR e43 x4 x3 (by rw [t0]; exact Or.inl rfl) (by rw [f1]; exact Or.inr rfl)).trans
      ((pgR e32 x3 o2 (by rw [f1]; exact Or.inr rfl) (by rw [f2, t0]; exact Or.inl rfl)).trans
      (pgR e21 o2 o1 (by rw [f2, t0]; exact Or.inl rfl) (Or.inr rfl)))))
  · -- k = 2: y = w₁ (A), z = w₂ (B)
    simp only [add_assoc, Fin.reduceAdd]
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
    have f4 : c (w (j + 4)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 t3; omega
    have f2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
    have f1 : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r01 t0; omega
    have e10 := (H.ringR 0 (by decide)).symm
    have e04 := (H.ringR 4 (by decide)).symm
    simp only [add_assoc, Fin.reduceAdd, add_zero] at e10 e04
    exact (pgR e10 o1 o0 (Or.inl rfl) (by rw [t0, f2]; exact Or.inr rfl)).trans
      ((pgR e04 o0 o4 (by rw [t0, f2]; exact Or.inr rfl) (by rw [f4, f1]; exact Or.inl rfl)).trans
      ((pgR e44 o4 x4 (by rw [f4, f1]; exact Or.inl rfl) (by rw [f2]; exact Or.inr rfl)).trans
      ((pgR e43 x4 x3 (by rw [f2]; exact Or.inr rfl) (by rw [f1]; exact Or.inl rfl)).trans
      (pgR e32 x3 o2 (by rw [f1]; exact Or.inl rfl) (Or.inr rfl)))))

/-- **P1, `R1`.** At an `R1` `DD` state with `k ∈ {3, 4}` (ring `(A, B, μ, α, μ)`), `J` holds:
`k = 3`: `w₂ x₂ x₁ x₀ w₄ w₃`; `k = 4`: `w₃ w₂ x₂ x₁ x₀ w₄`. -/
theorem join_R1 {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) (hk : k = 3 ∨ k = 4) :
    JoinYZ M.graph h w q c := by
  subst hq
  obtain ⟨w1, w3⟩ := r1_ring H rfl hc hD hT
  unfold TypeR1 at hT
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hD.1.1
  have e22 := (H.adj_w (j + 2)).symm
  have e21 := (P.adj_cyc (j + 1)).symm
  have e10 := (P.adj_cyc j).symm
  have e04 := H.adj_w4 j
  simp only [add_assoc, Fin.reduceAdd] at e21
  have o2 := H.offh (j + 2)
  have o3 := H.offh (j + 3)
  have o4 := H.offh (j + 4)
  have x0 := P.x_ne_h j
  have x1 := P.x_ne_h (j + 1)
  have x2 := P.x_ne_h (j + 2)
  have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl (fin5_ne (by obtain rfl | rfl := hk <;> decide))
  have r40 := H.ring4 hc (j := j) (fin5_ne0 (by obtain rfl | rfl := hk <;> decide))
  have f2 : c (w (j + 2)) = c (P.x (j + 1)) := by
    clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r12 w1; omega
  have f4 : c (w (j + 4)) = c (P.x (j + 1)) := by
    clear * - h1 h3 h4 h13 h14 h34 d4 d4' r40 hT; omega
  unfold JoinYZ
  obtain rfl | rfl := hk
  · -- k = 3: y = w₂ (μ), z = w₃ (α)
    simp only [add_assoc, Fin.reduceAdd]
    have e43 := (H.ringR 3 (by decide)).symm
    simp only [add_assoc, Fin.reduceAdd] at e43
    exact (pgR e22 o2 x2 (Or.inl rfl) (by rw [w3, ← h02]; exact Or.inr rfl)).trans
      ((pgR e21 x2 x1 (by rw [w3, ← h02]; exact Or.inr rfl) (by rw [f2]; exact Or.inl rfl)).trans
      ((pgR e10 x1 x0 (by rw [f2]; exact Or.inl rfl) (by rw [w3]; exact Or.inr rfl)).trans
      ((pgR e04 x0 o4 (by rw [w3]; exact Or.inr rfl) (by rw [f4, f2]; exact Or.inl rfl)).trans
      (pgR e43 o4 o3 (by rw [f4, f2]; exact Or.inl rfl) (Or.inr rfl)))))
  · -- k = 4: y = w₃ (α), z = w₄ (μ)
    simp only [add_assoc, Fin.reduceAdd]
    have e32 := (H.ringR 2 (by decide)).symm
    simp only [add_assoc, Fin.reduceAdd] at e32
    exact (pgR e32 o3 o2 (Or.inl rfl) (by rw [f2, f4]; exact Or.inr rfl)).trans
      ((pgR e22 o2 x2 (by rw [f2, f4]; exact Or.inr rfl) (by rw [w3, ← h02]; exact Or.inl rfl)).trans
      ((pgR e21 x2 x1 (by rw [w3, ← h02]; exact Or.inl rfl) (by rw [f4]; exact Or.inr rfl)).trans
      ((pgR e10 x1 x0 (by rw [f4]; exact Or.inr rfl) (by rw [w3]; exact Or.inl rfl)).trans
      (pgR e04 x0 o4 (by rw [w3]; exact Or.inl rfl) (Or.inr rfl)))))

/-- **P1** in `(type, k)` form: at a doubly locked state of a forced `(type, k)` whose
doubly locked index is a `DD` state, `J` holds. -/
theorem forced_join {t : GType} {k : Fin 5} (H : Hole6 P w m q) (hc : ProperOff M.graph h c)
    (hs : HasTK P w q c t k) (hD : ∀ j, DoublyLocked P c j → DDstate P c j)
    (hf : isForced (t, k) = true) : JoinYZ M.graph h w q c := by
  obtain ⟨j, hd, hq, hT⟩ := hs
  cases t <;> obtain rfl | rfl | rfl | rfl | rfl := fin5_five k
  all_goals first | exact absurd hf (by decide) | skip
  · exact join_R1 H hq hc (hD j hd) hT (Or.inl rfl)
  · exact join_R1 H hq hc (hD j hd) hT (Or.inr rfl)
  · exact join_R3 H hq hc hd.1 hT (Or.inl rfl)
  · exact join_R3 H hq hc hd.1 hT (Or.inr (Or.inl rfl))
  · exact join_R3 H hq hc hd.1 hT (Or.inr (Or.inr rfl))

/-! ### P2: the `{p, m}` swaps do not change `J` -/

/-- **P2.** A `DD` step whose swapped pair is carried by `{p, m}` does not change `J`. -/
theorem pm_step_join (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (hpm : PairFact P c j m (P.x q) ∨ PairFact P c j (P.x q) m) :
    (JoinYZ M.graph h w q (piMove P c) ↔ JoinYZ M.graph h w q c) := by
  obtain ⟨hπ, -⟩ := dd_ends hc hD
  have yp := hc (H.adj_w4 q) (P.x_ne_h _) (H.offh _)
  have ym := hc H.ringy (H.offh _) H.offmh
  have zp := hc (H.adj_w q) (P.x_ne_h _) (H.offh _)
  have zm := hc H.ringz H.offmh (H.offh _)
  have ya : c (w (q + 4)) ≠ c (P.x j) ∧ c (w (q + 4)) ≠ c (P.x (j + 3)) := by
    unfold PairFact at hpm
    rcases hpm with ⟨a, b⟩ | ⟨a, b⟩ <;> refine ⟨?_, ?_⟩ <;> omega
  have za : c (w q) ≠ c (P.x j) ∧ c (w q) ≠ c (P.x (j + 3)) := by
    unfold PairFact at hpm
    rcases hpm with ⟨a, b⟩ | ⟨a, b⟩ <;> refine ⟨?_, ?_⟩ <;> omega
  unfold JoinYZ
  rw [hπ, rot3_keep ya.1 ya.2, rot3_keep za.1 za.2]
  unfold rot3
  rw [pairGraph_swap_other _ _ _ _ ya.1 ya.2 za.1 za.2]

/-! ### `k = 4`: lockless `σ`-exit ⇔ `J` -/

/-- At `q = j + 4` the `Hole6` hypothesis gives the `K4Ball`. -/
theorem Hole6.k4Ball (H : Hole6 P w m q) (hq : q = j + 4) : K4Ball P w m j := by
  subst hq
  have n0 := H.nbr j (fin5_ne0 (by decide))
  have n1 := H.nbr (j + 1) (fin5_ne (by decide))
  have n2 := H.nbr (j + 2) (fin5_ne (by decide))
  have n3 := H.nbr (j + 3) (fin5_ne (by decide))
  have n4 := H.nbrq
  have g40 := H.ring (j + 4) (by rw [add_assoc]; exact fin5_ne (by decide))
  have g01 := H.ring j (fin5_ne (by decide))
  have g12 := H.ring (j + 1) (by rw [add_assoc]; exact fin5_ne (by decide))
  have g23 := H.ring (j + 2) (by rw [add_assoc]; exact fin5_ne (by decide))
  have gy := H.ringy
  have a3 := H.adj_w4 (j + 3)
  simp only [add_assoc, Fin.reduceAdd, add_zero] at n1 n2 n3 n4 g40 g12 g23 gy a3
  exact ⟨⟨n0, n1, n2, g40, g01, g12, H.adj_w (j + 4), a3,
    fun i => ⟨H.off _ i, H.off _ i, H.off _ i, H.off _ i⟩,
    ⟨H.offh _, H.offh _, H.offh _, H.offh _⟩⟩, n3, n4, g23, gy, H.ringz, H.off _, H.offm,
    ⟨H.offh _, H.offmh⟩⟩

/-- At an `R3k4` state with `z = A` (the pair fact `(m, z)` of `pair_R3k4_of_pred`), the ring
is the full `R3` ring `(B, A, B, μ, A)`. -/
theorem r3k4_R3At (H : Hole6 P w m q) (hq : q = j + 4) (hc : ProperOff M.graph h c)
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

/-- **`k = 4`: lockless ⇔ `J`.** At an `R3` state at `k = 4` of a triangulated map, the
`σ`-exit is lockless iff `y = w (j+3)` and `z = w (j+4)` are `{μ, A}`-joined. This is
`sigma_exit_criterion_k4'` (`z ∈ K_{μ,A}(x (j+1))`) together with `y ∈ K_{μ,A}(x (j+1))`
(Lock 1 and the edge `x (j+3) ~ y`). -/
theorem k4_lockless_iff_join (htri : M.Triangulated) (H : Hole6 P w m q) (hq : q = j + 4)
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    NoLock P (sigSwap P c j) ↔ JoinYZ M.graph h w q c := by
  rw [sigma_exit_criterion_k4' htri (H.k4Ball hq) hc hR]
  subst hq
  unfold JoinYZ
  simp only [add_assoc, Fin.reduceAdd]
  obtain ⟨⟨-, l1, -⟩, -, -, -, e3, e4⟩ := hR
  rw [e3, e4]
  have ey : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
      (P.x (j + 1)) (w (j + 3)) :=
    l1.trans (pgR (H.adj_w (j + 3)) (P.x_ne_h _) (H.offh _) (Or.inr rfl) (Or.inl e3))
  exact ⟨fun r => ey.symm.trans r, fun r => ey.trans r⟩

/-! ### P3 on an all-`DL` orbit -/

lemma gseq_mod (n : ℕ) : gseq n = gseq (n % 10) := by
  conv_lhs => rw [← Nat.mod_add_div n 10]
  generalize n / 10 = d
  induction d with
  | zero => simp
  | succ d ih =>
    rw [show n % 10 + 10 * (d + 1) = n % 10 + 10 * d + 10 by ring, gseq_period, ih]

lemma orbit_dd {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (n : ℕ) (j : Fin 5)
    (hd : DoublyLocked P ((piMove P)^[n] s) j) : DDstate P ((piMove P)^[n] s) j := by
  obtain ⟨-, -, r', -, -⟩ := rot3_move (iter_proper hc n) hd.1 hd.2.2
  have hπ : piMove P ((piMove P)^[n] s) = rot3 P ((piMove P)^[n] s) j := by
    rw [piMove_rep hd.1, ite_eq_left hd.2.2]
  rw [← hπ] at r'
  have hn := hall (n + 1)
  rw [Function.iterate_succ_apply'] at hn
  exact ⟨hd, r', (dl_rep r').1 hn⟩

/-- **The period lemma for `J`** (`NightLemmaS.md` §0, P1–P3), in the setting of
`gamma_period_ten`: `J` holds at positions `4 … 8` of the period, is unchanged by the steps at
positions `2` and `9`, and so can change only at the steps at positions `0, 1, 3, 8`. -/
theorem period_J {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) :
    (∀ n, 4 ≤ n % 10 → n % 10 ≤ 8 → JoinYZ M.graph h w q ((piMove P)^[n] s)) ∧
    (∀ n, (n % 10 = 2 ∨ n % 10 = 9) →
      (JoinYZ M.graph h w q ((piMove P)^[n + 1] s) ↔ JoinYZ M.graph h w q ((piMove P)^[n] s))) ∧
    (∀ n, n % 10 ≠ 0 → n % 10 ≠ 1 → n % 10 ≠ 3 → n % 10 ≠ 8 →
      (JoinYZ M.graph h w q ((piMove P)^[n + 1] s) ↔ JoinYZ M.graph h w q ((piMove P)^[n] s))) := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have P1 : ∀ n, 4 ≤ n % 10 → n % 10 ≤ 8 → JoinYZ M.graph h w q ((piMove P)^[n] s) := by
    intro n a b
    have hf : isForced (gseq n) = true := by
      rw [gseq_mod]
      rcases (show n % 10 = 4 ∨ n % 10 = 5 ∨ n % 10 = 6 ∨ n % 10 = 7 ∨ n % 10 = 8 by omega)
        with e | e | e | e | e <;> rw [e] <;> decide
    exact forced_join H (iter_proper hc n) (tk n) (orbit_dd hc hall n) hf
  have P2 : ∀ n, (n % 10 = 2 ∨ n % 10 = 9) →
      (JoinYZ M.graph h w q ((piMove P)^[n + 1] s) ↔
        JoinYZ M.graph h w q ((piMove P)^[n] s)) := by
    intro n hn
    obtain ⟨j, hd, hq', hT'⟩ := tk n
    rw [Function.iterate_succ_apply']
    rcases hn with e | e
    · have g : gseq n = (.R3, 3) := by rw [gseq_mod, e]; decide
      rw [g] at hq' hT'
      dsimp only at hq' hT'
      have own := pair_own (m := m) (t := .R3) (k := 3) H hq' (iter_proper hc n)
        (orbit_dd hc hall n j hd) hT' (by decide)
      rw [pv_R3_3] at own
      exact pm_step_join H (iter_proper hc n) (orbit_dd hc hall n j hd) (Or.inl own)
    · have g : gseq n = (.R1, 2) := by rw [gseq_mod, e]; decide
      rw [g] at hq' hT'
      dsimp only at hq' hT'
      have own := pair_own (m := m) (t := .R1) (k := 2) H hq' (iter_proper hc n)
        (orbit_dd hc hall n j hd) hT' (by decide)
      rw [pv_R1_2] at own
      exact pm_step_join H (iter_proper hc n) (orbit_dd hc hall n j hd) (Or.inr own)
  refine ⟨P1, P2, fun n a b c' d => ?_⟩
  by_cases e : n % 10 = 2 ∨ n % 10 = 9
  · exact P2 n e
  · exact iff_of_true (P1 (n + 1) (by omega) (by omega)) (P1 n (by omega) (by omega))

/-- **Main theorem** (`NightLemmaS.md` §0, Corollary P3). On an all-`DL` orbit from an `R3k4`
state at a `(5,5,5,5,6)` hole of a triangulated map, at the `(b+1)`-st `R3k4` state
`s (10 b + 10)` (doubly locked at `j`, `q = j + 4`): `J` holds at the preceding `R3k0` state
`s (10 b + 8)`, and the `σ`-exit is lockless iff `J` still holds after the step-8 swap, at
`s (10 b + 9)`. -/
theorem k4_exit_period (htri : M.Triangulated) {s : Fin n → Fin 4} {j₀ : Fin 5}
    (H : Hole6 P w m q) (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (b : ℕ) :
    ∃ j, DoublyLocked P ((piMove P)^[10 * b + 10] s) j ∧ q = j + 4 ∧
      JoinYZ M.graph h w q ((piMove P)^[10 * b + 8] s) ∧
      (NoLock P (sigSwap P ((piMove P)^[10 * b + 10] s) j) ↔
        JoinYZ M.graph h w q ((piMove P)^[10 * b + 9] s)) := by
  obtain ⟨tk, pr, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  obtain ⟨P1, P2, -⟩ := period_J (m := m) H hc hall hr hq hT
  have g : gseq (10 * b + 10) = (.R3, 4) := by
    rw [gseq_mod, show (10 * b + 10) % 10 = 0 by omega]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk (10 * b + 10)
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  have pz := pr (10 * b + 10) (by omega) j hd.1
  rw [g] at pz
  dsimp only at pz
  rw [pv_R3_4] at pz
  have hR := r3k4_R3At H hq' (iter_proper hc _) hd hT' pz.2
  have e9 := P2 (10 * b + 9) (Or.inr (by omega))
  refine ⟨j, hd, hq', P1 _ (by omega) (by omega), ?_⟩
  rw [k4_lockless_iff_join htri H hq' (iter_proper hc _) hR, ← e9]

/-- **A `k = 4` failure is a break at step 8.** In the setting of `k4_exit_period`, the `σ`-exit
at `s (10 b + 10)` is not lockless iff the step-8 swap (from `s (10 b + 8)` to `s (10 b + 9)`)
breaks `J`. -/
theorem k4_failure_iff_break (htri : M.Triangulated) {s : Fin n → Fin 4} {j₀ : Fin 5}
    (H : Hole6 P w m q) (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (b : ℕ) :
    ∃ j, DoublyLocked P ((piMove P)^[10 * b + 10] s) j ∧ q = j + 4 ∧
      (¬ NoLock P (sigSwap P ((piMove P)^[10 * b + 10] s) j) ↔
        (JoinYZ M.graph h w q ((piMove P)^[10 * b + 8] s) ∧
          ¬ JoinYZ M.graph h w q ((piMove P)^[10 * b + 9] s))) := by
  obtain ⟨j, hd, hq', j8, e⟩ := k4_exit_period htri H hc hall hr hq hT b
  exact ⟨j, hd, hq', by rw [e]; exact ⟨fun x => ⟨j8, x⟩, fun x => x.2⟩⟩

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.period_J
#print axioms SimpleGraph.QuarterFloor.k4_exit_period
#print axioms SimpleGraph.QuarterFloor.k4_failure_iff_break
