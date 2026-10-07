/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterZsplit

/-!
# The step-8 component `K₈` and the hole (Studio Job AV)

Setting of `QuarterWindow`/`QuarterZsplit`: an all-`DL` `π`-orbit `s n = π^[n] s` from an
`R3k4` state at a `(5,5,5,5,6)` hole `Hole6 P w m q`, names `p = x q`, `x⁺ = x (q+1)`,
`x₂ = x (q+2)`, `x₃ = x (q+3)`, `x⁻ = x (q+4)`, `z = w q`, `w⁺ = w (q+1)`, `w₂ = w (q+2)`,
`w₃ = w (q+3)`, `y = w (q+4)`, `m`.

At position `8` (`n % 10 = 8`, type `R3k0`) the repeat index is `j = q` (bookkeeping), and the
`π`-step is the `R₊₃` swap of the component `K₈` of `x (j+2) = x₂` in the two-colour graph of
`{c (x j), c (x (j+3))} = {c p, c x₃} = {α, A}` (`pair_own`: `p` and `y` carry this pair).
In the state's own frame the hole colours are `x (q+t) = (α, μ, α, A, B)`,
`w (q+t) = (B, A, B, μ, A)`, `m = μ`.

## Main results (sorry-free, no new axioms)

1. `K8_contains_x2_x3_wplus`: `x₂, x₃, w⁺ ∈ K₈`, along the ring edges `x₂ x₃` (link) and
   `x₂ w⁺` (`w⁺ ~ x (q+1), x (q+2)`), all three coloured in the pair.
2. `K8_avoids_pmyz`: `p, m, y, z ∉ K₈` and the step fixes their colours (`step8_far`).
3. `K8_meets_hole_exactly`: a hole vertex lies in `K₈` iff it is `x₂`, `x₃` or `w⁺`
   (`x⁺, x⁻, z, w₂, w₃, m` are coloured outside the pair; `p, y` are separated, `step8_far`).
4. `consecutive_K8_share_hole`: at positions `10 b + 8` and `10 b + 18` the components `K₈`
   meet the hole in the same three absolute vertices `x₂, x₃, w⁺` (the names are
   period-independent: `j = q` at every position `8`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- A vertex reachable from a pair-coloured vertex in a two-colour graph is pair-coloured. -/
lemma reach_col' {V C : Type*} {G : SimpleGraph V} {h s v : V} {c : V → C} {a b : C}
    (r : (pairGraph G h c a b).Reachable s v) (hs : c s = a ∨ c s = b) :
    c v = a ∨ c v = b := by
  by_cases e : s = v
  · subst e; exact hs
  · exact reach_col r e

section sphere
variable {N : ℕ} {M : SphericalMap N} {h : Fin N}
variable {P : Pent M.graph h} {w : Fin 5 → Fin N} {m : Fin N} {q : Fin 5}

section orbit
variable {s : Fin N → Fin 4} {j₀ : Fin 5}

/-- **Position-8 colours.** At `n % 10 = 8` (`R3k0`, `j = q`): `x₂, x₃, w⁺` are joined to `x₂`
in the `{c p, c x₃}`-graph, and `x⁺, x⁻, z, w₂, w₃, m` are coloured outside that pair. -/
lemma pos8_setup (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 8) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j ∧
      (((piMove P)^[k] s) (P.x (j + 2)) = ((piMove P)^[k] s) (P.x j) ∨
        ((piMove P)^[k] s) (P.x (j + 2)) = ((piMove P)^[k] s) (P.x (j + 3))) ∧
      (∀ v, (v = P.x (q + 2) ∨ v = P.x (q + 3) ∨ v = w (q + 1)) →
        (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v) ∧
      (∀ v, (v = P.x (q + 1) ∨ v = P.x (q + 4) ∨ v = w q ∨ v = w (q + 2) ∨ v = w (q + 3) ∨
          v = m) →
        ¬ (((piMove P)^[k] s) v = ((piMove P)^[k] s) (P.x j) ∨
          ((piMove P)^[k] s) v = ((piMove P)^[k] s) (P.x (j + 3)))) := by
  have hk0 : 0 < k := by omega
  obtain ⟨j, hd, hq', inj, ox, ow, om⟩ := pos_cols H hc hall hr hq hT k hk0
    (g := (.R3, 0)) (by rw [gseq_mod, hk]; decide)
  dsimp only at hq'
  rw [add_zero] at hq'
  subst hq'
  refine ⟨q, hd, rfl, ?_⟩
  clear hall hc hr hT
  generalize (piMove P)^[k] s = c at *
  have inP : ∀ v a, c v = frm P c q a → (a = 0 ∨ a = 2) →
      (c v = c (P.x q) ∨ c v = c (P.x (q + 3))) := by
    rintro v a e (rfl | rfl)
    · exact Or.inl e
    · exact Or.inr e
  have outP : ∀ v a, c v = frm P c q a → a ≠ 0 → a ≠ 2 →
      ¬ (c v = c (P.x q) ∨ c v = c (P.x (q + 3))) := by
    rintro v a e h0 h2 (e' | e')
    · exact h0 (inj (show frm P c q a = frm P c q 0 from e.symm.trans e'))
    · exact h2 (inj (show frm P c q a = frm P c q 2 from e.symm.trans e'))
  have c2 := inP _ _ (ox 2) (by decide)
  have c3 := inP _ _ (ox 3) (by decide)
  have cw := inP _ _ (ow 1) (by decide)
  have e23 := P.adj_cyc (q + 2)
  have e2w := H.adj_w' (q + 1)
  simp only [add_assoc, Fin.reduceAdd] at e23 e2w
  refine ⟨c2, fun v hv => ?_, fun v hv => ?_⟩
  · rcases hv with rfl | rfl | rfl
    · rfl
    · exact pgR e23 (P.x_ne_h _) (P.x_ne_h _) c2 c3
    · exact pgR e2w (P.x_ne_h _) (H.offh _) c2 cw
  · rcases hv with rfl | rfl | rfl | rfl | rfl | rfl
    · exact outP _ _ (ox 1) (by decide) (by decide)
    · exact outP _ _ (ox 4) (by decide) (by decide)
    · have e := ow 0
      rw [add_zero] at e
      exact outP _ _ e (by decide) (by decide)
    · exact outP _ _ (ow 2) (by decide) (by decide)
    · exact outP _ _ (ow 3) (by decide) (by decide)
    · exact outP _ _ om (by decide) (by decide)

/-- **(1) `K₈ ∋ x₂, x₃, w⁺`.** At position `8` (`R3k0`, repeat index `j = q`), the step-8
swapped component `K₈ = K_{c p, c x₃}(x (j+2))`, the `R₊₃` component of `x_{j+2} = x₂`,
contains `x₂ = x (q+2)`, `x₃ = x (q+3)` and `w⁺ = w (q+1)`. -/
theorem K8_contains_x2_x3_wplus (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 8) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x (q + 2)) ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x (q + 3)) ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) (w (q + 1)) := by
  obtain ⟨j, hd, hqj, -, IN, -⟩ := pos8_setup H hc hall hr hq hT k hk
  exact ⟨j, hd, hqj, IN _ (Or.inl rfl), IN _ (Or.inr (Or.inl rfl)), IN _ (Or.inr (Or.inr rfl))⟩

/-- **(2) `K₈` avoids `p, m, y, z`** and the step fixes their colours: `step8_far`. -/
theorem K8_avoids_pmyz (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 8) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j ∧
      (∀ v, (v = P.x q ∨ v = m ∨ v = w (q + 4) ∨ v = w q) →
        ¬ (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
            (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v ∧
        ((piMove P)^[k + 1] s) v = ((piMove P)^[k] s) v) :=
  step8_far H hc hall hr hq hT k hk

/-- **(3) `K₈` meets the hole exactly in `{x₂, x₃, w⁺}`.** At position `8`, a hole vertex
(`x t`, `w t` or `m`) lies in the step-8 swapped component iff it is `x (q+2)`, `x (q+3)` or
`w (q+1)`. -/
theorem K8_meets_hole_exactly (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 8) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j ∧ ∀ v, HoleV P w m v →
      ((pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
          (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v ↔
        (v = P.x (q + 2) ∨ v = P.x (q + 3) ∨ v = w (q + 1))) := by
  obtain ⟨j, hd, hqj, src, IN, OUT⟩ := pos8_setup H hc hall hr hq hT k hk
  subst hqj
  obtain ⟨j', -, hqj', far⟩ := step8_far H hc hall hr hq hT k hk
  subst hqj'
  refine ⟨q, hd, rfl, fun v hv => ⟨fun r => ?_, IN v⟩⟩
  have col := reach_col' r src
  rcases hv with ⟨t, rfl⟩ | ⟨t, rfl⟩ | rfl
  · obtain ⟨t, rfl⟩ : ∃ t', t = q + t' := ⟨t - q, by abel⟩
    rcases fin5_five t with rfl | rfl | rfl | rfl | rfl
    · rw [add_zero] at r; exact ((far _ (Or.inl rfl)).1 r).elim
    · exact (OUT _ (Or.inl rfl) col).elim
    · exact Or.inl rfl
    · exact Or.inr (Or.inl rfl)
    · exact (OUT _ (Or.inr (Or.inl rfl)) col).elim
  · obtain ⟨t, rfl⟩ : ∃ t', t = q + t' := ⟨t - q, by abel⟩
    rcases fin5_five t with rfl | rfl | rfl | rfl | rfl
    · rw [add_zero] at r; exact ((far _ (Or.inr (Or.inr (Or.inr rfl)))).1 r).elim
    · exact Or.inr (Or.inr rfl)
    · exact (OUT _ (Or.inr (Or.inr (Or.inr (Or.inl rfl)))) col).elim
    · exact (OUT _ (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))) col).elim
    · exact ((far _ (Or.inr (Or.inr (Or.inl rfl)))).1 r).elim
  · exact ((far _ (Or.inr (Or.inl rfl))).1 r).elim

/-- **(4) Consecutive `K₈`'s share the hole vertices `x₂, x₃, w⁺`.** At positions `10 b + 8`
and `10 b + 18` the repeat index is `q` both times, and both step-8 components meet the hole in
exactly the same absolute vertices `x (q+2)`, `x (q+3)`, `w (q+1)`. -/
theorem consecutive_K8_share_hole (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (b : ℕ) :
    ∀ i ∈ ({0, 10} : Finset ℕ), ∀ v, HoleV P w m v →
      ((pairGraph M.graph h ((piMove P)^[10 * b + 8 + i] s)
          (((piMove P)^[10 * b + 8 + i] s) (P.x q))
          (((piMove P)^[10 * b + 8 + i] s) (P.x (q + 3)))).Reachable (P.x (q + 2)) v ↔
        (v = P.x (q + 2) ∨ v = P.x (q + 3) ∨ v = w (q + 1))) := by
  intro i hi v hv
  have hk : (10 * b + 8 + i) % 10 = 8 := by
    simp only [Finset.mem_insert, Finset.mem_singleton] at hi
    rcases hi with rfl | rfl <;> omega
  obtain ⟨j, -, hqj, E⟩ := K8_meets_hole_exactly H hc hall hr hq hT _ hk
  subst hqj
  exact E v hv

end orbit

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.K8_contains_x2_x3_wplus
#print axioms SimpleGraph.QuarterFloor.K8_avoids_pmyz
#print axioms SimpleGraph.QuarterFloor.K8_meets_hole_exactly
#print axioms SimpleGraph.QuarterFloor.consecutive_K8_share_hole
