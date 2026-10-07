/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterHole6Gen

/-!
# The all-six hole `(6,6,6,6,6)` and its `DD`-step table

Gap G66 of `NightWeakForm.md`: at a degree-five vertex `h` whose five link vertices all have
degree six, none of the `σ`-exit lemmas and none of the period lemmas of `QuarterGammaPeriod` /
`QuarterHole6Gen` apply. This module sets up the hole and derives what survives.

## Conventions

* `Hole66 P w m`: every link vertex `x t` has degree six, with neighbours
  `h, x (t-1), x (t+1), w (t-1), m t, w t`, the outer ones in rotation order `w (t-1), m t, w t`.
  `w t` is the third vertex of the face `x t x (t+1)`, `m t` is the inserted vertex of `x t`.
  The second ring is the ten-cycle `… w (t-1) ~ m t ~ w t ~ m (t+1) …` (`ringy`, `ringz` of
  `Hole6`, for every `t`). The 2-ball is `x, w, m`.
* Types at repeat index `j` (link `α, μ, α, A, B`), as in `QuarterGammaPeriod`:
  `R1`: `w j = A`; `R3`: `w j = B ∧ w (j+3) = μ`; and here also
  `R2` (`TypeR2`): `w j = B ∧ w (j+3) = α`. At an all-six hole these are exhaustive and
  exclusive (`type66_trichotomy`, `type66_exclusive`), because `w j ∈ {A, B}` and
  `w (j+3) ∈ {α, μ}` by properness alone.

## Main results (sorry-free, no new axioms)

1. `ring66_dom`, `ring66_of_dl`: the colour facts forced by a `DL` state at `j`:
   `w j, w (j+1) ∈ {A, B}`, `w (j+2) ∈ {μ, B}`, `w (j+3) ∈ {α, μ}`, `w (j+4) ∈ {μ, A}`;
   on the triangle `w j, m (j+1), w (j+1)` at `x (j+1)` exactly one of
   `(A, B, A)`, `(B, A, B)`, `(w j ≠ w (j+1), m (j+1) = α)` (both lock ends at `x (j+1)`);
   a `μ` on `{w (j+2), m (j+3), w (j+3)}` (Lock 1 end at `x (j+3)`) and on
   `{w (j+3), m (j+4), w (j+4)}` (Lock 2 end at `x (j+4)`).
   `dd_ends66`: on a `DD` step additionally `B` on `{w (j+1), m (j+2), w (j+2)}` and
   `w (j+3) = α ∨ w (j+4) = A ∨ (π c) (m (j+4)) = A` (the lock ends of `π c`).
2. `image_type66`: the type of `π c` at `j + 3` is read off `c` at `w (j+3)`, `w (j+1)`:
   `w (j+3) = μ ⇒ R1`; `w (j+3) = α, w (j+1) = B ⇒ R3`; `w (j+3) = α, w (j+1) = A ⇒ R2`.
   **The new repeat index is `j + 3`** for every pattern (`rot3_move`, no hole hypothesis);
   in `Hole6` language `k = q - j ↦ k + 2`. (It is `j + 3`, not `j + 2`.)
3. `dd_step66`: on a `DD` step, `(type) ↦ type'` with `succ66 type type'`:
   `R3 → {R1}`, `R2 → {R2, R3}`, `R1 → {R1, R2, R3}`. With the `m`-colours
   (`dd_step66_R1`): from `R1`, `→ R1` iff `w (j+3) = μ`; `→ R3` iff `w (j+3) = α` and then
   `w (j+1) = B, m (j+1) = α`; `→ R2` iff `w (j+3) = α` and then `w (j+1) = A, m (j+1) = B`.
   **The type is not determined** at an all-six hole: the successor sets above are the exact
   sets allowed by the local facts used here. (Hand check, not formal: each of the five
   transitions `R1→R1, R1→R2, R1→R3, R2→R2, R2→R3` has a proper colouring of the 2-ball
   satisfying every lock-end condition of `c` and `π c` listed in 1.; e.g. `R1→R2` with
   `(w₀..w₄) = (A, A, B, α, μ)`, `(m₀..m₄) = (B, B, μ, μ, A)`.)
4. `untyped_dd66` (the `R2` analogue of `untyped_dd4`): an `R2` `DL` state goes to `R3` with
   `w (j+1) = B, m (j+1) = A`, or to `R2` with `w (j+1) = A, m (j+1) = α`. There is no
   positional restriction (all link vertices look alike).
5. `allDL_orbit_visits_all_j66`: on an all-`DL` orbit the repeat index runs `j₀ + 3N`, so every
   index occurs among the first five states (pattern-independent). `allDL_orbit_walk66`: at an
   all-six hole the orbit's types form a walk of `succ66`.

## Which `Hole6` facts fail at `Hole66`

* The ring edges `w t ~ w (t+1)` do not exist (each is replaced by `w t ~ m (t+1) ~ w (t+1)`).
  So `r1_w1_ring` (`w (j+1) = B` from `w j ~ w (j+1)`), `r1_w3_chain`, and the last case of
  `r1_w3_I3` (`ring4`) fail; with them `r1_ring`, `r1_step` and the `R1 → R3` row of `tk_step`.
* No link vertex has degree five. `r1_w3_I3` (the `A`-end of `π c` at `x (j+4)`) and
  `r1_w1_k1`/`untyped_dd`'s `core` (the `B`-end at `x (j+2)`, the `μ`-end at `x (j+3)`) case
  on a five-element neighbourhood; at `Hole66` the extra neighbour `m t` can carry the
  lock-end colour, which is exactly the third disjunct in each lock-end fact of 1.
* `R2` is not excluded, so `untyped_dd`/`untyped_dd4` and `typed_in_orbit4` have no
  analogue; the `(type, k)` sequence is not a function of the start and `gamma_period_ten`
  fails (the position `k` is meaningless: there is no distinguished `q`).
* `pair_own`: the carriers `m, y, z, p` of the swapped pair use one inserted vertex and the
  edges `y ~ m ~ z`; here there are five `m t` and the carrier table is not determined
  (only `m (j+1)` is pinned, by 1.).
* `TripleBallP`, `K4Ball`, `K4BallGen` and every `σ`-exit lemma need degree-five link
  vertices; all are vacuous at `Hole66` (as `NightWeakForm.md` §2 notes for X4/X3).
* What holds verbatim: `r3_step` (`R3 → R1`, no hole hypothesis), the index shift `j ↦ j + 3`,
  `dd_ends` (hole-free), and the domain facts `dom`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- The all-six hole: every link vertex `x t` has neighbours `h, x (t-1), x (t+1), w (t-1),
m t, w t` (outer ones in rotation order), with second-ring edges `w (t-1) ~ m t ~ w t`. -/
structure Hole66 (P : Pent M.graph h) (w m : Fin 5 → Fin n) : Prop where
  nbr : ∀ t u, M.graph.Adj (P.x t) u ↔
    u = h ∨ u = P.x (t + 4) ∨ u = P.x (t + 1) ∨ u = w (t + 4) ∨ u = m t ∨ u = w t
  ringy : ∀ t, M.graph.Adj (w (t + 4)) (m t)
  ringz : ∀ t, M.graph.Adj (m t) (w t)
  off : ∀ t i, w t ≠ P.x i
  offm : ∀ t i, m t ≠ P.x i
  offh : ∀ t, w t ≠ h
  offmh : ∀ t, m t ≠ h

variable {P : Pent M.graph h} {w m : Fin 5 → Fin n} {c : Fin n → Fin 4} {j : Fin 5}

namespace Hole66

lemma adj_w (H : Hole66 P w m) (t : Fin 5) : M.graph.Adj (P.x t) (w t) := (H.nbr t _).2 (by simp)

lemma adj_w4 (H : Hole66 P w m) (t : Fin 5) : M.graph.Adj (P.x t) (w (t + 4)) :=
  (H.nbr t _).2 (by simp)

lemma adj_m (H : Hole66 P w m) (t : Fin 5) : M.graph.Adj (P.x t) (m t) := (H.nbr t _).2 (by simp)

lemma adj_w' (H : Hole66 P w m) (t : Fin 5) : M.graph.Adj (P.x (t + 1)) (w t) := by
  have e := H.adj_w4 (t + 1)
  rwa [add_assoc, show (1 : Fin 5) + 4 = 0 from rfl, add_zero] at e

lemma dom (H : Hole66 P w m) (hc : ProperOff M.graph h c) (t : Fin 5) :
    c (w t) ≠ c (P.x t) ∧ c (w t) ≠ c (P.x (t + 1)) :=
  ⟨(hc (H.adj_w t) (P.x_ne_h _) (H.offh t)).symm,
    (hc (H.adj_w' t) (P.x_ne_h _) (H.offh t)).symm⟩

lemma domAt (H : Hole66 P w m) (hc : ProperOff M.graph h c) {a b : Fin 5} (hab : a + 1 = b) :
    c (w (j + a)) ≠ c (P.x (j + a)) ∧ c (w (j + a)) ≠ c (P.x (j + b)) := by
  have d := H.dom hc (j + a)
  rwa [add_assoc, hab] at d

lemma dom4 (H : Hole66 P w m) (hc : ProperOff M.graph h c) :
    c (w (j + 4)) ≠ c (P.x (j + 4)) ∧ c (w (j + 4)) ≠ c (P.x j) := by
  have d := H.dom hc (j + 4)
  rwa [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero] at d

/-- `m t` sees `x t`, `w (t-1)`, `w t`. -/
lemma mdom (H : Hole66 P w m) (hc : ProperOff M.graph h c) (t : Fin 5) :
    c (m t) ≠ c (P.x t) ∧ c (m t) ≠ c (w (t + 4)) ∧ c (m t) ≠ c (w t) :=
  ⟨(hc (H.adj_m t) (P.x_ne_h _) (H.offmh t)).symm,
    (hc (H.ringy t) (H.offh _) (H.offmh t)).symm, hc (H.ringz t) (H.offmh t) (H.offh _)⟩

/-- A non-`h` neighbour of `x t` of colour `a`. -/
lemma nbr_col (H : Hole66 P w m) {t : Fin 5} {u : Fin n} {a : Fin 4}
    (hu : M.graph.Adj (P.x t) u) (huh : u ≠ h) (hcu : c u = a) :
    c (P.x (t + 4)) = a ∨ c (P.x (t + 1)) = a ∨ c (w (t + 4)) = a ∨ c (m t) = a ∨
      c (w t) = a := by
  rcases (H.nbr t u).1 hu with rfl | rfl | rfl | rfl | rfl | rfl
  · exact (huh rfl).elim
  · exact Or.inl hcu
  · exact Or.inr (Or.inl hcu)
  · exact Or.inr (Or.inr (Or.inl hcu))
  · exact Or.inr (Or.inr (Or.inr (Or.inl hcu)))
  · exact Or.inr (Or.inr (Or.inr (Or.inr hcu)))

end Hole66

/-! ### Types -/

variable (P w) in
/-- Type `R2` at `j`: `c (w j) = B` and `c (w (j+3)) = α` (the type excluded at `Hole6`). -/
def TypeR2 (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  c (w j) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x j)

/-- The three state types at an all-six hole. -/
inductive GType3
  | R1
  | R2
  | R3
  deriving DecidableEq

variable (P w) in
/-- The type predicate, three types. -/
def TypeOf66 : GType3 → (Fin n → Fin 4) → Fin 5 → Prop
  | .R1 => TypeR1 P w
  | .R2 => TypeR2 P w
  | .R3 => TypeR3 P w

/-- The allowed type successions on a `DD` step: `R3 → R1`, `R2 → R2, R3`, `R1 → any`. -/
def succ66 : GType3 → GType3 → Bool
  | .R3, .R1 => true
  | .R3, _ => false
  | .R2, .R1 => false
  | .R2, _ => true
  | .R1, _ => true

/-! ### 1. The ring of a `DL` state -/

/-- The domain facts on `w`: properness and the repeat pattern only. -/
theorem ring66_dom (H : Hole66 P w m) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    (c (w j) = c (P.x (j + 3)) ∨ c (w j) = c (P.x (j + 4))) ∧
    (c (w (j + 1)) = c (P.x (j + 3)) ∨ c (w (j + 1)) = c (P.x (j + 4))) ∧
    (c (w (j + 2)) = c (P.x (j + 1)) ∨ c (w (j + 2)) = c (P.x (j + 4))) ∧
    (c (w (j + 3)) = c (P.x j) ∨ c (w (j + 3)) = c (P.x (j + 1))) ∧
    (c (w (j + 4)) = c (P.x (j + 1)) ∨ c (w (j + 4)) = c (P.x (j + 3))) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨d0, d0'⟩ := H.dom hc j
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · clear * - h1 h3 h4 h13 h14 h34 d0 d0'; omega
  · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1'; omega
  · clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2'; omega
  · clear * - h1 h3 h4 h13 h14 h34 d3 d3'; omega
  · clear * - h1 h3 h4 h13 h14 h34 d4 d4'; omega

/-- The types are exhaustive at an all-six hole. -/
theorem type66_trichotomy (H : Hole66 P w m) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) : TypeR1 P w c j ∨ TypeR2 P w c j ∨ TypeR3 P w c j := by
  obtain ⟨a0, -, -, a3, -⟩ := ring66_dom H hc hr
  unfold TypeR1 TypeR2 TypeR3
  rcases a0 with a0 | a0
  · exact Or.inl a0
  · rcases a3 with a3 | a3
    · exact Or.inr (Or.inl ⟨a0, a3⟩)
    · exact Or.inr (Or.inr ⟨a0, a3⟩)

/-- The types are exclusive. -/
theorem type66_exclusive (hr : RepeatAt P c j) :
    ¬ (TypeR1 P w c j ∧ TypeR2 P w c j) ∧ ¬ (TypeR1 P w c j ∧ TypeR3 P w c j) ∧
      ¬ (TypeR2 P w c j ∧ TypeR3 P w c j) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  unfold TypeR1 TypeR2 TypeR3
  refine ⟨fun ⟨e1, e2, _⟩ => h34 (e1.symm.trans e2), fun ⟨e1, e2, _⟩ => h34 (e1.symm.trans e2),
    fun ⟨⟨_, e1⟩, ⟨_, e2⟩⟩ => h1 (e2.symm.trans e1)⟩

/-- Every state has exactly one of the three types. -/
theorem typeOf66_unique (H : Hole66 P w m) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    ∃! t : GType3, TypeOf66 P w t c j := by
  obtain ⟨e12, e13, e23⟩ := type66_exclusive (w := w) hr
  rcases type66_trichotomy H hc hr with t | t | t
  · refine ⟨.R1, t, fun t' ht' => ?_⟩
    cases t' <;> simp only [TypeOf66] at ht'
    · rfl
    · exact (e12 ⟨t, ht'⟩).elim
    · exact (e13 ⟨t, ht'⟩).elim
  · refine ⟨.R2, t, fun t' ht' => ?_⟩
    cases t' <;> simp only [TypeOf66] at ht'
    · exact (e12 ⟨ht', t⟩).elim
    · rfl
    · exact (e23 ⟨t, ht'⟩).elim
  · refine ⟨.R3, t, fun t' ht' => ?_⟩
    cases t' <;> simp only [TypeOf66] at ht'
    · exact (e13 ⟨ht', t⟩).elim
    · exact (e23 ⟨ht', t⟩).elim
    · rfl

/-- The four lock ends of a `DL` state at `j`, as colour facts on the 2-ball. -/
theorem lock_ends66 (H : Hole66 P w m) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) :
    (c (w j) = c (P.x (j + 3)) ∨ c (m (j + 1)) = c (P.x (j + 3)) ∨
      c (w (j + 1)) = c (P.x (j + 3))) ∧
    (c (w j) = c (P.x (j + 4)) ∨ c (m (j + 1)) = c (P.x (j + 4)) ∨
      c (w (j + 1)) = c (P.x (j + 4))) ∧
    (c (w (j + 2)) = c (P.x (j + 1)) ∨ c (m (j + 3)) = c (P.x (j + 1)) ∨
      c (w (j + 3)) = c (P.x (j + 1))) ∧
    (c (w (j + 3)) = c (P.x (j + 1)) ∨ c (m (j + 4)) = c (P.x (j + 1)) ∨
      c (w (j + 4)) = c (P.x (j + 1))) := by
  obtain ⟨hr, l1, l2⟩ := hd
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have ne13 : P.x (j + 1) ≠ P.x (j + 3) := fun e => fin5_ne (by decide) (P.inj e)
  have ne14 : P.x (j + 1) ≠ P.x (j + 4) := fun e => fin5_ne (by decide) (P.inj e)
  -- the `μ`-ends at `x (j+3)` and `x (j+4)`
  obtain ⟨u3, a3, n3, e3⟩ := lock_end hc l1 ne13 rfl
  obtain ⟨u4, a4, n4, e4⟩ := lock_end hc l2 ne14 rfl
  -- the `A`- and `B`-ends at `x (j+1)`
  have l1' := l1
  have l2' := l2
  unfold Lock1 at l1'
  unfold Lock2 at l2'
  rw [pairGraph_comm_gen] at l1' l2'
  obtain ⟨uA, aA, nA, eA⟩ := lock_end hc l1'.symm (Ne.symm ne13) rfl
  obtain ⟨uB, aB, nB, eB⟩ := lock_end hc l2'.symm (Ne.symm ne14) rfl
  have cA := H.nbr_col aA nA eA
  have cB := H.nbr_col aB nB eB
  have c3 := H.nbr_col a3 n3 e3
  have c4 := H.nbr_col a4 n4 e4
  simp only [add_assoc, Fin.reduceAdd, add_zero] at cA cB c3 c4
  refine ⟨?_, ?_, ?_, ?_⟩
  · clear * - cA h02 h3; omega
  · clear * - cB h02 h4; omega
  · clear * - c3 h02 h1 h14; omega
  · clear * - c4 h13 h1; omega

/-- **`ring66_of_dl`.** The colour facts on `w` and `m` forced by a `DL` state at `j` of an
all-six hole (link `α, μ, α, A, B`). -/
theorem ring66_of_dl (H : Hole66 P w m) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) :
    -- domains
    (c (w j) = c (P.x (j + 3)) ∨ c (w j) = c (P.x (j + 4))) ∧
    (c (w (j + 1)) = c (P.x (j + 3)) ∨ c (w (j + 1)) = c (P.x (j + 4))) ∧
    (c (w (j + 2)) = c (P.x (j + 1)) ∨ c (w (j + 2)) = c (P.x (j + 4))) ∧
    (c (w (j + 3)) = c (P.x j) ∨ c (w (j + 3)) = c (P.x (j + 1))) ∧
    (c (w (j + 4)) = c (P.x (j + 1)) ∨ c (w (j + 4)) = c (P.x (j + 3))) ∧
    -- the triangle `w j, m (j+1), w (j+1)` at `x (j+1)`
    ((c (w j) = c (P.x (j + 3)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
        c (m (j + 1)) = c (P.x (j + 4))) ∨
      (c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 4)) ∧
        c (m (j + 1)) = c (P.x (j + 3))) ∨
      (c (w j) ≠ c (w (j + 1)) ∧ c (m (j + 1)) = c (P.x j))) ∧
    -- `μ` at `x (j+3)` and at `x (j+4)`
    (c (w (j + 2)) = c (P.x (j + 1)) ∨ c (m (j + 3)) = c (P.x (j + 1)) ∨
      c (w (j + 3)) = c (P.x (j + 1))) ∧
    (c (w (j + 3)) = c (P.x (j + 1)) ∨ c (m (j + 4)) = c (P.x (j + 1)) ∨
      c (w (j + 4)) = c (P.x (j + 1))) := by
  obtain ⟨a0, a1, a2, a3, a4⟩ := ring66_dom H hc hd.1
  obtain ⟨eA, eB, e3, e4⟩ := lock_ends66 H hc hd
  have md := H.mdom hc (j + 1)
  simp only [add_assoc, Fin.reduceAdd, add_zero] at md
  obtain ⟨m0, m1, m2⟩ := md
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hd.1
  refine ⟨a0, a1, a2, a3, a4, ?_, e3, e4⟩
  rcases a0 with x0 | x0 <;> rcases a1 with x1 | x1
  · exact Or.inl ⟨x0, x1, by clear * - eB x0 x1 h34; omega⟩
  · refine Or.inr (Or.inr ⟨by rw [x0, x1]; exact h34, ?_⟩)
    exact fin4_fourth _ _ _ _ _ h13 h14 h34 m0 (by rw [x0] at m1; exact m1)
      (by rw [x1] at m2; exact m2) h1.symm h3.symm h4.symm
  · refine Or.inr (Or.inr ⟨by rw [x0, x1]; exact h34.symm, ?_⟩)
    exact fin4_fourth _ _ _ _ _ h13 h14 h34 m0 (by rw [x1] at m2; exact m2)
      (by rw [x0] at m1; exact m1) h1.symm h3.symm h4.symm
  · exact Or.inr (Or.inl ⟨x0, x1, by clear * - eA x0 x1 h34; omega⟩)

/-! ### 2. The image type -/

/-- **The image type.** At a `DL` state at `j`, `π c = R₊₃ c` has repeat index `j + 3` and its
type there is read off `c (w (j+3))` and `c (w (j+1))`. -/
theorem image_type66 (H : Hole66 P w m) (hd : DoublyLocked P c j) :
    (c (w (j + 3)) = c (P.x (j + 1)) → TypeR1 P w (piMove P c) (j + 3)) ∧
    (c (w (j + 3)) = c (P.x j) → c (w (j + 1)) = c (P.x (j + 4)) →
      TypeR3 P w (piMove P c) (j + 3)) ∧
    (c (w (j + 3)) = c (P.x j) → c (w (j + 1)) = c (P.x (j + 3)) →
      TypeR2 P w (piMove P c) (j + 3)) := by
  obtain ⟨hr, -, l2⟩ := hd
  have hK := rot3Def_of_lock2 P hr l2
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hr, ite_eq_left l2]
  obtain ⟨-, v1, v2, v3, v4⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have e1 := H.adj_w' (j + 1)
  simp only [add_assoc, Fin.reduceAdd] at e1
  refine ⟨fun w3 => ?_, fun w3 w1 => ?_, fun w3 w1 => ?_⟩
  · unfold TypeR1
    simp only [add_assoc, Fin.reduceAdd, hπ]
    rw [v1, rot3_keep (by rw [w3]; exact h1) (by rw [w3]; exact h13), w3]
  · unfold TypeR3
    simp only [add_assoc, Fin.reduceAdd, hπ]
    refine ⟨?_, ?_⟩
    · rw [v2, rot3_K3 hr' (H.adj_w (j + 3)) (H.offh _) (Or.inl w3), w3, Equiv.swap_apply_left]
    · rw [v4, rot3_keep (by rw [w1]; exact h4) (by rw [w1]; exact h34.symm), w1]
  · unfold TypeR2
    simp only [add_assoc, Fin.reduceAdd, hπ]
    refine ⟨?_, ?_⟩
    · rw [v2, rot3_K3 hr' (H.adj_w (j + 3)) (H.offh _) (Or.inl w3), w3, Equiv.swap_apply_left]
    · rw [v3, rot3_K2 hr' e1 (H.offh _) (Or.inr w1), w1, Equiv.swap_apply_right]

/-! ### 3. The `DD`-step table -/

/-- A value of `R₊₃ c` outside the swapped pair is the old value. -/
lemma rot3_eq_other {v : Fin n} {b : Fin 4} (hb1 : b ≠ c (P.x j)) (hb2 : b ≠ c (P.x (j + 3)))
    (e : rot3 P c j v = b) : c v = b := by
  classical
  unfold rot3 at e
  by_cases hv : v ∈ {u | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
      (P.x (j + 2)) u}
  · rw [swap_in hv, Equiv.swap_apply_def] at e
    split_ifs at e
    · exact absurd e.symm hb2
    · exact absurd e.symm hb1
    · exact e
  · rwa [swap_out hv] at e

/-- The two lock ends of `π c` on a `DD` step, as colour facts on `c`: a `B` next to `x (j+2)`
and an (image) `A` next to `x (j+4)`. -/
theorem dd_ends66 (H : Hole66 P w m) (hc : ProperOff M.graph h c) (hD : DDstate P c j) :
    (c (w (j + 1)) = c (P.x (j + 4)) ∨ c (m (j + 2)) = c (P.x (j + 4)) ∨
      c (w (j + 2)) = c (P.x (j + 4))) ∧
    (c (w (j + 3)) = c (P.x j) ∨ c (w (j + 4)) = c (P.x (j + 3)) ∨
      piMove P c (m (j + 4)) = c (P.x (j + 3))) := by
  obtain ⟨hπ, hr, hK, -, ⟨u, hu, huh, hcu⟩, ⟨u', hu', hu'h, hcu'⟩⟩ := dd_ends hc hD
  obtain ⟨v0, -, -, v3, -⟩ := rot3_values hr hK
  obtain ⟨a0, a1, a2, a3, a4⟩ := ring66_dom H hc hr
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  refine ⟨?_, ?_⟩
  · have cu := rot3_eq_other (j := j) h4 h34.symm hcu
    have c2 := H.nbr_col hu huh cu
    simp only [add_assoc, Fin.reduceAdd] at c2
    clear * - c2 h14 h34
    omega
  · rw [hπ]
    have n4 := (H.nbr (j + 4) u').1 hu'
    simp only [add_assoc, Fin.reduceAdd, add_zero] at n4
    rcases n4 with rfl | rfl | rfl | rfl | rfl | rfl
    · exact (hu'h rfl).elim
    · rw [v3] at hcu'; exact (h3 hcu'.symm).elim
    · rw [v0] at hcu'; exact (h3 hcu'.symm).elim
    · left
      by_contra hne
      have hμ : c (w (j + 3)) = c (P.x (j + 1)) := by clear * - hne a3; omega
      rw [rot3_keep (by rw [hμ]; exact h1) (by rw [hμ]; exact h13), hμ] at hcu'
      exact h13 hcu'
    · exact Or.inr (Or.inr hcu')
    · right; left
      rwa [rot3_K0 hK (H.adj_w4 j) (H.offh _)] at hcu'

/-- **`R1` row.** From an `R1` `DL` state: `→ R1` when `w (j+3) = μ`; otherwise `w (j+3) = α`
and either `w (j+1) = B, m (j+1) = α` and `→ R3`, or `w (j+1) = A, m (j+1) = B` and `→ R2`. -/
theorem dd_step66_R1 (H : Hole66 P w m) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) (hT : TypeR1 P w c j) :
    (c (w (j + 3)) = c (P.x (j + 1)) ∧ TypeR1 P w (piMove P c) (j + 3)) ∨
    (c (w (j + 3)) = c (P.x j) ∧ c (w (j + 1)) = c (P.x (j + 4)) ∧ c (m (j + 1)) = c (P.x j) ∧
      TypeR3 P w (piMove P c) (j + 3)) ∨
    (c (w (j + 3)) = c (P.x j) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
      c (m (j + 1)) = c (P.x (j + 4)) ∧ TypeR2 P w (piMove P c) (j + 3)) := by
  obtain ⟨i1, i3, i2⟩ := image_type66 H hd
  obtain ⟨a0, a1, a2, a3, a4, tri, -, -⟩ := ring66_of_dl H hc hd
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hd.1
  unfold TypeR1 at hT
  rcases a3 with w3 | w3
  · rcases a1 with w1 | w1
    · exact Or.inr (Or.inr ⟨w3, w1, by clear * - tri hT w1 h34; omega, i2 w3 w1⟩)
    · exact Or.inr (Or.inl ⟨w3, w1, by clear * - tri hT w1 h34; omega, i3 w3 w1⟩)
  · exact Or.inl ⟨w3, i1 w3⟩

/-- **`R3` row** (`r3_step`, hole-free): `R3 → R1`. -/
theorem dd_step66_R3 (hd : DoublyLocked P c j) (hT : TypeR3 P w c j) :
    TypeR1 P w (piMove P c) (j + 3) := r3_step hd hT

/-- **(4) `untyped_dd66`, the `R2` row.** An `R2` `DL` state goes to `R3` with
`w (j+1) = B, m (j+1) = A`, or to `R2` with `w (j+1) = A, m (j+1) = α`. -/
theorem untyped_dd66 (H : Hole66 P w m) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) (hT : TypeR2 P w c j) :
    (c (w (j + 1)) = c (P.x (j + 4)) ∧ c (m (j + 1)) = c (P.x (j + 3)) ∧
      TypeR3 P w (piMove P c) (j + 3)) ∨
    (c (w (j + 1)) = c (P.x (j + 3)) ∧ c (m (j + 1)) = c (P.x j) ∧
      TypeR2 P w (piMove P c) (j + 3)) := by
  obtain ⟨-, i3, i2⟩ := image_type66 H hd
  obtain ⟨a0, a1, a2, a3, a4, tri, -, -⟩ := ring66_of_dl H hc hd
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hd.1
  obtain ⟨t0, t3⟩ := hT
  rcases a1 with w1 | w1
  · exact Or.inr ⟨w1, by clear * - tri t0 w1 h34; omega, i2 t3 w1⟩
  · exact Or.inl ⟨w1, by clear * - tri t0 w1 h34; omega, i3 t3 w1⟩

/-- **(3) `dd_step66`.** On a `DD` step at an all-six hole the new repeat index is `j + 3` and
the type moves along `succ66`: `R3 → R1`, `R2 → R2 | R3`, `R1 → R1 | R2 | R3`. -/
theorem dd_step66 {t : GType3} (H : Hole66 P w m) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) (hT : TypeOf66 P w t c j) (hd' : DLState P (piMove P c)) :
    ∃ t', succ66 t t' = true ∧ DoublyLocked P (piMove P c) (j + 3) ∧
      TypeOf66 P w t' (piMove P c) (j + 3) := by
  obtain ⟨-, -, r', -, -⟩ := rot3_move hc hd.1 hd.2.2
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hd.1, ite_eq_left hd.2.2]
  rw [← hπ] at r'
  have hd2 : DoublyLocked P (piMove P c) (j + 3) := ⟨r', (dl_rep r').1 hd'⟩
  cases t
  · rcases dd_step66_R1 H hc hd hT with ⟨-, e⟩ | ⟨-, -, -, e⟩ | ⟨-, -, -, e⟩
    · exact ⟨.R1, rfl, hd2, e⟩
    · exact ⟨.R3, rfl, hd2, e⟩
    · exact ⟨.R2, rfl, hd2, e⟩
  · rcases untyped_dd66 H hc hd hT with ⟨-, -, e⟩ | ⟨-, -, e⟩
    · exact ⟨.R3, rfl, hd2, e⟩
    · exact ⟨.R2, rfl, hd2, e⟩
  · exact ⟨.R1, rfl, hd2, dd_step66_R3 hd hT⟩

/-! ### 5. Orbits -/

lemma allDL_next {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ k, DLState P ((piMove P)^[k] s)) {N : ℕ} {i : Fin 5}
    (hd : DoublyLocked P ((piMove P)^[N] s) i) :
    DoublyLocked P ((piMove P)^[N + 1] s) (i + 3) := by
  have e := (allDL_orbit_dd hc hall N i hd).2
  rwa [← Function.iterate_succ_apply' (piMove P)] at e

/-- **(5)** On an all-`DL` orbit the repeat index of the `N`-th state is `j₀ + 3N`, so every
index `i` is the repeat index of one of the first five states (any link pattern). -/
theorem allDL_orbit_visits_all_j66 {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ k, DLState P ((piMove P)^[k] s)) (i : Fin 5) :
    ∃ N, N < 5 ∧ DoublyLocked P ((piMove P)^[N] s) i := by
  obtain ⟨j₀, d0⟩ := hall 0
  have d1 := allDL_next hc hall d0
  have d2 := allDL_next hc hall d1
  have d3 := allDL_next hc hall d2
  have d4 := allDL_next hc hall d3
  have e : ∀ a b : Fin 5, b = a ∨ b = a + 3 ∨ b = a + 3 + 3 ∨ b = a + 3 + 3 + 3 ∨
      b = a + 3 + 3 + 3 + 3 := by decide
  rcases e j₀ i with rfl | rfl | rfl | rfl | rfl
  · exact ⟨0, by omega, d0⟩
  · exact ⟨1, by omega, d1⟩
  · exact ⟨2, by omega, d2⟩
  · exact ⟨3, by omega, d3⟩
  · exact ⟨4, by omega, d4⟩

/-- At an all-six hole the types along an all-`DL` orbit form a walk of `succ66`. -/
theorem allDL_orbit_walk66 (H : Hole66 P w m) {s : Fin n → Fin 4}
    (hc : ProperOff M.graph h s) (hall : ∀ k, DLState P ((piMove P)^[k] s)) (N : ℕ) :
    ∃ j t t', DoublyLocked P ((piMove P)^[N] s) j ∧ TypeOf66 P w t ((piMove P)^[N] s) j ∧
      DoublyLocked P ((piMove P)^[N + 1] s) (j + 3) ∧
      TypeOf66 P w t' ((piMove P)^[N + 1] s) (j + 3) ∧ succ66 t t' = true := by
  obtain ⟨j, hd⟩ := hall N
  obtain ⟨t, ht, -⟩ := typeOf66_unique H (iter_proper hc N) hd.1
  have hN1 := hall (N + 1)
  rw [Function.iterate_succ_apply'] at hN1 ⊢
  obtain ⟨t', st, hd2, ht'⟩ := dd_step66 H (iter_proper hc N) hd ht hN1
  exact ⟨j, t, t', hd, ht, hd2, ht', st⟩

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.ring66_of_dl
#print axioms SimpleGraph.QuarterFloor.typeOf66_unique
#print axioms SimpleGraph.QuarterFloor.image_type66
#print axioms SimpleGraph.QuarterFloor.dd_ends66
#print axioms SimpleGraph.QuarterFloor.dd_step66
#print axioms SimpleGraph.QuarterFloor.untyped_dd66
#print axioms SimpleGraph.QuarterFloor.allDL_orbit_visits_all_j66
#print axioms SimpleGraph.QuarterFloor.allDL_orbit_walk66
