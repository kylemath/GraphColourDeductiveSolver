/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterWindow
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterW2Frame

/-!
# `σ`-fixed points at every position of the period as acyclic colour-pair subgraphs

Setting of `gamma_period_ten` (all-`DL` `π`-orbit from an `R3k4` state at a `Hole6 P w m q`,
positions `N % 10 = 0 … 9` of types `R3k4, R1k1, R3k3, R1k0, R3k2, R1k4, R3k1, R1k3, R3k0,
R1k2`). Night log entry `NightSigmaImage`: on `Γ` periods the spacing rules A₃₄′ and W2 become
statements about the positions at which `σ` is a fixed point.

Colours are named in the **position-4 frame** of period `b` (state `10 b + 4`, `R3k2`) as in
`QuarterW2Frame`: `frame4 = ![c₄ p, c₄ m, c₄ y, c₄ z]`, letters `0, 1, 2, 3` (the note's
`1 = p, 2 = m, 3 = y, 4 = z`).

## Main results (sorry-free, no new axioms)

* `frame_pos`: at position `10 b + i` (any `i : ℕ`, own repeat index `j'`) the frame
  `![α, μ, A, B]` is `frm (s (10b+4)) j₄ ∘ sig^[(i + 2) % 3]` (from `frm_iter`, forwards or
  backwards to position 4, with `sig^[3] = id`).
* `fixed_at_pos` (Lemma Fix at any position): `SigmaFixed` at `10 b + i` iff the two-colour
  subgraph of `T − h` in the pair complementary to that position's repeat pair `{α, μ}` is
  acyclic; the pair is `(F (sig^[e] 2), F (sig^[e] 3))`, `e = (i + 2) % 3`, `F` the position-4
  frame.
* `frm_pos4`: the position-4 frame is `![c₄ p, c₄ m, c₄ y, c₄ z]`.
* `fixed_pos_iff n` (`n : Fin 10`): the named statement. Repeat pair `{α, μ}` = `repTab n`
  and complementary pair = `pairTab n` in letters (`0 = p, 1 = m, 2 = y, 3 = z`):
  position `0 … 9` have `{α, μ}` = `13, 12, 14, 13, 12, 14, 13, 12, 14, 13` and pair
  `24, 34, 23, 24, 34, 23, 24, 34, 23, 24` (note's names; Studio Job AY's table of σ pairs).
* `fixed_pos1_iff` (`R1k1`): fixed iff the `{c₄ y, c₄ z}`-subgraph is acyclic.
  `fixed_pos11_iff`: at `10 b + 11` (position 1 of the next period) fixed iff the
  `{c₄ m, c₄ y}`-subgraph is acyclic.
* `fixed_pos1_period_shift`: in the frame `F₁` of position `10 b + 1`, the complementary pair at
  `10 b + 11` is `σ` of the pair at `10 b + 1`: `(F₁ (σ 2), F₁ (σ 3))` versus `(F₁ 2, F₁ 3)`
  (the frame rotation of `period_colour_rotation`, via `frm_iter` with `sig^[10] = sig`).
* `fixedPoint_spacing_conj`: "`σ` fixed at `10b+1` and at `10b+11`" ⇔ "the pair-`P` subgraph is
  acyclic at `10b+1` and the pair-`σP` subgraph is acyclic at `10b+11`". This is only the
  fixed-point reformulation; its link to A₃₄′ (k = 3/4 failure ⇔ fixed at `R1k1`) is data
  (550/552 degree-6 periods, Studio Job AY), **not** an equivalence.
* `W2_as_fixed_points`: `σ` fixed at positions 4, 6, 8 ⇔ the `{3,4}`, `{2,4}`, `{2,3}`
  subgraphs (note's names) are acyclic there (exact, Lemma Fix; reuses `QuarterW2Frame`).
* `not_fixed_R3_k34`, `not_fixed_pos0`, `not_fixed_pos2`: at an `R3` state with `k ∈ {3, 4}`
  (positions 0 and 2) the `{A, B}`-graph contains the 6-cycle
  `x (j+4), w (j+4), w j, w (j+1), w (j+2), x (j+3)` (all ring edges present since the missing
  ring edge `w (q-1) w q` is not among them), so `σ` is never a fixed point there.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Letter tables -/

/-- The repeat pair `(α, μ)` at positions `0 … 9`, letters of the position-4 frame
(`0 = p, 1 = m, 2 = y, 3 = z`). -/
def repTab : Fin 10 → Fin 4 × Fin 4 :=
  ![(0, 2), (0, 1), (0, 3), (0, 2), (0, 1), (0, 3), (0, 2), (0, 1), (0, 3), (0, 2)]

/-- The complementary pair `(A, B)` at positions `0 … 9`, letters of the position-4 frame. -/
def pairTab : Fin 10 → Fin 4 × Fin 4 :=
  ![(3, 1), (2, 3), (1, 2), (3, 1), (2, 3), (1, 2), (3, 1), (2, 3), (1, 2), (3, 1)]

theorem repTab_eq : ∀ i : Fin 10,
    repTab i = (sig^[(i.val + 2) % 3] 0, sig^[(i.val + 2) % 3] 1) := by decide

theorem pairTab_eq : ∀ i : Fin 10,
    pairTab i = (sig^[(i.val + 2) % 3] 2, sig^[(i.val + 2) % 3] 3) := by decide

/-- The repeat pair and its complement partition the four letters. -/
theorem rep_pair_partition : ∀ i : Fin 10,
    [(repTab i).1, (repTab i).2, (pairTab i).1, (pairTab i).2].Nodup := by decide

/-! ### A six-cycle kills acyclicity -/

lemma not_acyclic_of_hex {V : Type*} {G : SimpleGraph V} {a b u1 u2 u3 u4 : V}
    (eab : G.Adj a b) (e1 : G.Adj a u1) (e2 : G.Adj u1 u2) (e3 : G.Adj u2 u3) (e4 : G.Adj u3 u4)
    (e5 : G.Adj u4 b) (ha1 : a ≠ u1) (ha2 : a ≠ u2) (ha3 : a ≠ u3) (ha4 : a ≠ u4)
    (hb1 : b ≠ u1) (hb2 : b ≠ u2) (hb3 : b ≠ u3) (hb4 : b ≠ u4) : ¬ G.IsAcyclic := by
  intro hA
  have := isBridge_iff_forall_walk_mem_edges.1 (isAcyclic_iff_forall_adj_isBridge.1 hA eab)
    (.cons e1 (.cons e2 (.cons e3 (.cons e4 (.cons e5 .nil)))))
  simp [ha1, ha2, ha3, ha4, hb1, hb2, hb3, hb4] at this

lemma fin5_add_ne (j : Fin 5) {a b : Fin 5} (hab : a ≠ b) : j + a ≠ j + b :=
  fun e => hab (add_left_cancel e)

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}

variable (P w m q) in
/-- The position-4 frame `![c p, c m, c y, c z]` (`p = x q`, `y = w (q+4)`, `z = w q`). -/
def frame4 (c : Fin n → Fin 4) : Fin 4 → Fin 4 :=
  ![c (P.x q), c m, c (w (q + 4)), c (w q)]

/-! ### Positions 0 and 2 are never fixed -/

/-- **`R3` with `k ∈ {3, 4}` is never a fixed point**: the `{A, B}`-graph has the 6-cycle
`x (j+4), w (j+4), w j, w (j+1), w (j+2), x (j+3)`. -/
theorem not_fixed_R3_k34 (htri : M.Triangulated) (H : Hole6 P w m q) {c : Fin n → Fin 4}
    {j : Fin 5} (hc : ProperOff M.graph h c) (hR : R3At P w c j) (hq : q = j + 3 ∨ q = j + 4) :
    ¬ SigmaFixed P c j := by
  intro hf
  have hA := acyclic_of_sigmaFixed htri hc hR.1.1 hf
  obtain ⟨-, c0, c1, c2, -, c4⟩ := hR
  have r40 : M.graph.Adj (w (j + 4)) (w j) := by
    have := H.ring (j + 4) (by
      rw [add_assoc]; rcases hq with rfl | rfl <;> exact fin5_add_ne j (by decide))
    simpa only [add_assoc, Fin.reduceAdd, add_zero] using this
  have r01 : M.graph.Adj (w j) (w (j + 1)) :=
    H.ring j (by rcases hq with rfl | rfl <;> exact fin5_add_ne j (by decide))
  have r12 : M.graph.Adj (w (j + 1)) (w (j + 2)) := by
    have := H.ring (j + 1) (by
      rw [add_assoc]; rcases hq with rfl | rfl <;> exact fin5_add_ne j (by decide))
    simpa only [add_assoc, Fin.reduceAdd] using this
  have s4 := H.adj_w (j + 4)
  have s3 : M.graph.Adj (w (j + 2)) (P.x (j + 3)) := by
    have := (H.adj_w4 (j + 3)).symm
    simpa only [add_assoc, Fin.reduceAdd] using this
  have x34 : M.graph.Adj (P.x (j + 4)) (P.x (j + 3)) := by
    have := (P.adj_cyc (j + 3)).symm
    simpa only [add_assoc, Fin.reduceAdd] using this
  have ax3 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 3)) :=
    ⟨P.x_ne_h _, Or.inl rfl⟩
  have ax4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 4)) :=
    ⟨P.x_ne_h _, Or.inr rfl⟩
  have aw4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 4)) := ⟨H.offh _, Or.inl c4⟩
  have aw0 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w j) := ⟨H.offh _, Or.inr c0⟩
  have aw1 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 1)) := ⟨H.offh _, Or.inl c1⟩
  have aw2 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 2)) := ⟨H.offh _, Or.inr c2⟩
  have o := H.off
  exact not_acyclic_of_hex (G := pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))))
    ⟨x34, ax4, ax3⟩ ⟨s4, ax4, aw4⟩ ⟨r40, aw4, aw0⟩ ⟨r01, aw0, aw1⟩ ⟨r12, aw1, aw2⟩
    ⟨s3, aw2, ax3⟩ (o _ _).symm (o _ _).symm (o _ _).symm (o _ _).symm (o _ _).symm
    (o _ _).symm (o _ _).symm (o _ _).symm hA

section orbit
variable {s : Fin n → Fin 4} {j₀ : Fin 5}

/-- The `R3At` facts at an `R3` position of the orbit. -/
lemma orbit_R3At (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) {N : ℕ} (hN : 0 < N) {k : Fin 5} (g : gseq N = (.R3, k))
    {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    R3At P w ((piMove P)^[N] s) j ∧ q = j + k := by
  obtain ⟨j', hd, hq', tab⟩ := orbit_tab H hc hall hr hq hT N hN
  rw [g] at hq' tab
  have e := rep_unique hd.1 hj
  subst e
  exact ⟨(tab_R3 hd hq' tab).1, hq'⟩

/-- **Position 0 (`R3k4`) is never a fixed point.** -/
theorem not_fixed_pos0 (htri : M.Triangulated) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN0 : 0 < N) (hN : N % 10 = 0) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[N] s) j) : ¬ SigmaFixed P ((piMove P)^[N] s) j := by
  have g : gseq N = (.R3, 4) := by rw [gseq_mod, hN]; decide
  obtain ⟨hR, hq'⟩ := orbit_R3At H hc hall hr hq hT hN0 g hj
  exact not_fixed_R3_k34 htri H (iter_proper hc N) hR (Or.inr hq')

/-- **Position 2 (`R3k3`) is never a fixed point.** -/
theorem not_fixed_pos2 (htri : M.Triangulated) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 2) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[N] s) j) : ¬ SigmaFixed P ((piMove P)^[N] s) j := by
  have g : gseq N = (.R3, 3) := by rw [gseq_mod, hN]; decide
  obtain ⟨hR, hq'⟩ := orbit_R3At H hc hall hr hq hT (by omega) g hj
  exact not_fixed_R3_k34 htri H (iter_proper hc N) hR (Or.inl hq')

/-! ### The frame at every position, in the position-4 frame -/

/-- **The frame at position `10 b + i`** is the position-4 frame composed with
`sig^[(i + 2) % 3]`. -/
theorem frame_pos (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (b i : ℕ) {j₄ j' : Fin 5} (h4 : RepeatAt P ((piMove P)^[10 * b + 4] s) j₄)
    (hj' : RepeatAt P ((piMove P)^[10 * b + i] s) j') (a : Fin 4) :
    frm P ((piMove P)^[10 * b + i] s) j' a =
      frm P ((piMove P)^[10 * b + 4] s) j₄ (sig^[(i + 2) % 3] a) := by
  rcases le_or_gt 4 i with hi | hi
  · obtain ⟨d, rfl⟩ : ∃ d, i = 4 + d := ⟨i - 4, by omega⟩
    have fi := frm_iter hc hall (10 * b + 4) h4 d j'
      (by rwa [show 10 * b + 4 + d = 10 * b + (4 + d) by omega])
    rw [show 10 * b + (4 + d) = 10 * b + 4 + d by omega, fi a, sig_iter_mod d,
      show (4 + d + 2) % 3 = d % 3 by omega]
  · have fi := frm_iter hc hall (10 * b + i) hj' (4 - i) j₄
      (by rwa [show 10 * b + i + (4 - i) = 10 * b + 4 by omega])
    rw [show 10 * b + 4 = 10 * b + i + (4 - i) by omega, fi, ← Function.iterate_add_apply,
      sig_iter_mod, show (4 - i + (i + 2) % 3) % 3 = 0 by omega]
    rfl

/-- **Lemma Fix at every position**: `σ` is fixed at `10 b + i` iff the subgraph of the pair
complementary to that position's repeat pair `{α, μ}` is acyclic; the pair, in the position-4
frame `F`, is `(F (sig^[e] 2), F (sig^[e] 3))` with `e = (i + 2) % 3`. -/
theorem fixed_at_pos (htri : M.Triangulated) (hconn : M.graph.Connected)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (b i : ℕ) {j₄ j' : Fin 5} (h4 : RepeatAt P ((piMove P)^[10 * b + 4] s) j₄)
    (hj' : RepeatAt P ((piMove P)^[10 * b + i] s) j') :
    SigmaFixed P ((piMove P)^[10 * b + i] s) j' ↔
      (pairGraph M.graph h ((piMove P)^[10 * b + i] s)
        (frm P ((piMove P)^[10 * b + 4] s) j₄ (sig^[(i + 2) % 3] 2))
        (frm P ((piMove P)^[10 * b + 4] s) j₄ (sig^[(i + 2) % 3] 3))).IsAcyclic := by
  rw [sigmaFixed_iff_acyclic htri hconn (iter_proper hc _) hj', ← frame_pos hc hall b i h4 hj',
    ← frame_pos hc hall b i h4 hj']
  rfl

/-- The position-4 frame is `![c₄ p, c₄ m, c₄ y, c₄ z]`. -/
theorem frm_pos4 (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    frm P ((piMove P)^[N] s) j = frame4 P w m q ((piMove P)^[N] s) := by
  obtain ⟨l0, l1, -, l3, l4, -⟩ := links_pos4_to_8 H hc hall hr hq hT hN hj
  funext a
  fin_cases a
  exacts [l0, l1, l3, l4]

/-- **`fixed_pos_iff n`** (every position `n = 0 … 9` of period `b`, R1 and R3 alike), in the
position-4 frame `F = frame4 (s (10b+4))` (`0 = p, 1 = m, 2 = y, 3 = z`): the repeat pair is
`α = F (repTab n).1`, `μ = F (repTab n).2`, and `σ` is fixed iff the subgraph of the
complementary pair `(F (pairTab n).1, F (pairTab n).2)` is acyclic. -/
theorem fixed_pos_iff (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    (n : Fin 10) (b : ℕ) {j₄ j' : Fin 5} (h4 : RepeatAt P ((piMove P)^[10 * b + 4] s) j₄)
    (hj' : RepeatAt P ((piMove P)^[10 * b + n] s) j') :
    ((piMove P)^[10 * b + n] s) (P.x j') =
        frame4 P w m q ((piMove P)^[10 * b + 4] s) (repTab n).1 ∧
      ((piMove P)^[10 * b + n] s) (P.x (j' + 1)) =
        frame4 P w m q ((piMove P)^[10 * b + 4] s) (repTab n).2 ∧
      (SigmaFixed P ((piMove P)^[10 * b + n] s) j' ↔
        (pairGraph M.graph h ((piMove P)^[10 * b + n] s)
          (frame4 P w m q ((piMove P)^[10 * b + 4] s) (pairTab n).1)
          (frame4 P w m q ((piMove P)^[10 * b + 4] s) (pairTab n).2)).IsAcyclic) := by
  have f4 := frm_pos4 H hc hall hr hq hT (N := 10 * b + 4) (by omega) h4
  have fp := frame_pos hc hall b n h4 hj'
  rw [f4] at fp
  rw [repTab_eq, pairTab_eq, fixed_at_pos htri hconn hc hall b n h4 hj', f4]
  exact ⟨fp 0, fp 1, Iff.rfl⟩

/-- **`fixed_pos1_iff`** (`R1k1`, position `10 b + 1`): `σ` is fixed iff the
`{c₄ y, c₄ z}`-subgraph (note's `{3, 4}`) is acyclic. -/
theorem fixed_pos1_iff (htri : M.Triangulated) (hconn : M.graph.Connected) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    (b : ℕ) {j₄ j₁ : Fin 5} (h4 : RepeatAt P ((piMove P)^[10 * b + 4] s) j₄)
    (h1 : RepeatAt P ((piMove P)^[10 * b + 1] s) j₁) :
    SigmaFixed P ((piMove P)^[10 * b + 1] s) j₁ ↔
      (pairGraph M.graph h ((piMove P)^[10 * b + 1] s)
        (((piMove P)^[10 * b + 4] s) (w (q + 4))) (((piMove P)^[10 * b + 4] s) (w q))).IsAcyclic := by
  rw [fixed_at_pos htri hconn hc hall b 1 h4 h1,
    frm_pos4 H hc hall hr hq hT (N := 10 * b + 4) (by omega) h4]
  rfl

/-- **`fixed_pos11_iff`** (position `10 b + 11`, `R1k1` of the next period): `σ` is fixed iff
the `{c₄ m, c₄ y}`-subgraph (note's `{2, 3}`) is acyclic. -/
theorem fixed_pos11_iff (htri : M.Triangulated) (hconn : M.graph.Connected)
    (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    (b : ℕ) {j₄ j₁₁ : Fin 5} (h4 : RepeatAt P ((piMove P)^[10 * b + 4] s) j₄)
    (h11 : RepeatAt P ((piMove P)^[10 * b + 11] s) j₁₁) :
    SigmaFixed P ((piMove P)^[10 * b + 11] s) j₁₁ ↔
      (pairGraph M.graph h ((piMove P)^[10 * b + 11] s)
        (((piMove P)^[10 * b + 4] s) m) (((piMove P)^[10 * b + 4] s) (w (q + 4)))).IsAcyclic := by
  rw [fixed_at_pos htri hconn hc hall b 11 h4 h11,
    frm_pos4 H hc hall hr hq hT (N := 10 * b + 4) (by omega) h4]
  rfl

/-- **The period shift of the position-1 pair.** In the frame `F₁ = frm (s (10b+1)) j₁`, the
complementary pair at position `10 b + 1` is `(F₁ 2, F₁ 3)` (definitionally,
`c (x (j₁+3)), c (x (j₁+4))`), and at `10 b + 11` it is `σ` of it, `(F₁ (σ 2), F₁ (σ 3))`;
correspondingly `σ` is fixed at `10 b + 11` iff the `σ`-pair subgraph is acyclic. -/
theorem fixed_pos1_period_shift (htri : M.Triangulated) (hconn : M.graph.Connected)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (b : ℕ) {j₁ j₁₁ : Fin 5} (h1 : RepeatAt P ((piMove P)^[10 * b + 1] s) j₁)
    (h11 : RepeatAt P ((piMove P)^[10 * b + 11] s) j₁₁) :
    ((piMove P)^[10 * b + 11] s) (P.x (j₁₁ + 3)) = frm P ((piMove P)^[10 * b + 1] s) j₁ (sig 2) ∧
      ((piMove P)^[10 * b + 11] s) (P.x (j₁₁ + 4)) =
        frm P ((piMove P)^[10 * b + 1] s) j₁ (sig 3) ∧
      (SigmaFixed P ((piMove P)^[10 * b + 11] s) j₁₁ ↔
        (pairGraph M.graph h ((piMove P)^[10 * b + 11] s)
          (frm P ((piMove P)^[10 * b + 1] s) j₁ (sig 2))
          (frm P ((piMove P)^[10 * b + 1] s) j₁ (sig 3))).IsAcyclic) := by
  have fi := frm_iter hc hall (10 * b + 1) h1 10 j₁₁
    (by rwa [show 10 * b + 1 + 10 = 10 * b + 11 by omega])
  have e10 : sig^[10] = sig := by rw [sig_iter_mod]; rfl
  rw [show 10 * b + 1 + 10 = 10 * b + 11 by omega, e10] at fi
  refine ⟨fi 2, fi 3, ?_⟩
  rw [sigmaFixed_iff_acyclic htri hconn (iter_proper hc _) h11, ← fi 2, ← fi 3]
  rfl

/-- **The fixed-point reformulation at `R1k1` in two consecutive periods**
(`fixedPoint_spacing_conj`): "`σ` fixed at `10b+1` and at `10b+11`" ⇔ "the pair-`P` subgraph is
acyclic at `10b+1` and the pair-`σP` subgraph is acyclic at `10b+11`", `P = (F₁ 2, F₁ 3)`.

This is exact (Lemma Fix), but it is **only the fixed-point reformulation**: the link between
A₃₄′ and fixed points ("a `k = 3/4` failure occurs in a period ⇔ `σ` is fixed at `R1k1`") holds
in 550/552 degree-6 periods (Studio Job AY; fails at p26 #87942 h22), so this statement is
**not** equivalent to A₃₄′ and nothing here proves or assumes A₃₄′. -/
theorem fixedPoint_spacing_conj (htri : M.Triangulated) (hconn : M.graph.Connected)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (b : ℕ) {j₁ j₁₁ : Fin 5} (h1 : RepeatAt P ((piMove P)^[10 * b + 1] s) j₁)
    (h11 : RepeatAt P ((piMove P)^[10 * b + 11] s) j₁₁) :
    (SigmaFixed P ((piMove P)^[10 * b + 1] s) j₁ ∧
        SigmaFixed P ((piMove P)^[10 * b + 11] s) j₁₁) ↔
      ((pairGraph M.graph h ((piMove P)^[10 * b + 1] s)
          (frm P ((piMove P)^[10 * b + 1] s) j₁ 2)
          (frm P ((piMove P)^[10 * b + 1] s) j₁ 3)).IsAcyclic ∧
        (pairGraph M.graph h ((piMove P)^[10 * b + 11] s)
          (frm P ((piMove P)^[10 * b + 1] s) j₁ (sig 2))
          (frm P ((piMove P)^[10 * b + 1] s) j₁ (sig 3))).IsAcyclic) := by
  rw [sigmaFixed_iff_acyclic htri hconn (iter_proper hc _) h1,
    (fixed_pos1_period_shift htri hconn hc hall b h1 h11).2.2]
  rfl

/-- **W2 positions as fixed points** (exact, Lemma Fix; `QuarterW2Frame`): `σ` is fixed at all
of positions 4, 6, 8 (`R3k2, R3k1, R3k0`, repeat indices `j, j+1, j+2`) iff the
`{c₄ y, c₄ z}`, `{c₄ m, c₄ z}`, `{c₄ m, c₄ y}` subgraphs (note's `{3,4}, {2,4}, {2,3}`) are
acyclic there. W2 is "not fixed at all three". -/
theorem W2_as_fixed_points (htri : M.Triangulated) (hconn : M.graph.Connected)
    (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    (SigmaFixed P ((piMove P)^[N] s) j ∧ SigmaFixed P ((piMove P)^[N + 2] s) (j + 1) ∧
        SigmaFixed P ((piMove P)^[N + 4] s) (j + 2)) ↔
      ((pairGraph M.graph h ((piMove P)^[N] s) (((piMove P)^[N] s) (w (q + 4)))
          (((piMove P)^[N] s) (w q))).IsAcyclic ∧
        (pairGraph M.graph h ((piMove P)^[N + 2] s) (((piMove P)^[N] s) m)
          (((piMove P)^[N] s) (w q))).IsAcyclic ∧
        (pairGraph M.graph h ((piMove P)^[N + 4] s) (((piMove P)^[N] s) m)
          (((piMove P)^[N] s) (w (q + 4)))).IsAcyclic) := by
  rw [fixed_pos4_iff htri hconn H hc hall hr hq hT hN hj,
    fixed_pos6_iff htri hconn H hc hall hr hq hT hN hj,
    fixed_pos8_iff htri hconn H hc hall hr hq hT hN hj]

end orbit

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.repTab_eq
#print axioms SimpleGraph.QuarterFloor.pairTab_eq
#print axioms SimpleGraph.QuarterFloor.rep_pair_partition
#print axioms SimpleGraph.QuarterFloor.not_fixed_R3_k34
#print axioms SimpleGraph.QuarterFloor.not_fixed_pos0
#print axioms SimpleGraph.QuarterFloor.not_fixed_pos2
#print axioms SimpleGraph.QuarterFloor.frame_pos
#print axioms SimpleGraph.QuarterFloor.fixed_at_pos
#print axioms SimpleGraph.QuarterFloor.frm_pos4
#print axioms SimpleGraph.QuarterFloor.fixed_pos_iff
#print axioms SimpleGraph.QuarterFloor.fixed_pos1_iff
#print axioms SimpleGraph.QuarterFloor.fixed_pos11_iff
#print axioms SimpleGraph.QuarterFloor.fixed_pos1_period_shift
#print axioms SimpleGraph.QuarterFloor.fixedPoint_spacing_conj
#print axioms SimpleGraph.QuarterFloor.W2_as_fixed_points
