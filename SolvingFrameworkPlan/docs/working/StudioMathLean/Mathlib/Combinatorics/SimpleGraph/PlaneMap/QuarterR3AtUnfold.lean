/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPeriodJ

/-!
# `R3At` unfolded, and what it adds to the Studio's type `R3` at `k = 4`

For data pipelines (`NightK4Hypotheses.md`). Link at `j, …, j+4` is `(α, μ, α, A, B)` with
`α = c (x j)`, `μ = c (x (j+1))`, `A = c (x (j+3))`, `B = c (x (j+4))`.

* `r3At_iff`: `R3At` as an explicit conjunction (definitional).
* `typeR3_k4_ring`: at a `Hole6` with `q = j + 4`, a doubly locked state of Studio type `R3`
  (`w₀ = B`, `w₃ = μ`) has `w₁ = A`, `w₂ = B`, and `w₄ ∈ {A, μ}`.
* `r3At_k4_iff`: in that situation `R3At ↔ w₄ = A`. So the only condition of `R3At` beyond
  the Studio typing (and `DL`) at `k = 4` is `c (w (j+4)) = c (x (j+3))`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

/-- `R3At` unfolded: the repeat pattern, both locks, and the ring `(B, A, B, μ, A)`. -/
theorem r3At_iff : R3At P w c j ↔
    ((c (P.x j) = c (P.x (j + 2)) ∧
      c (P.x (j + 1)) ≠ c (P.x j) ∧ c (P.x (j + 3)) ≠ c (P.x j) ∧ c (P.x (j + 4)) ≠ c (P.x j) ∧
      c (P.x (j + 1)) ≠ c (P.x (j + 3)) ∧ c (P.x (j + 1)) ≠ c (P.x (j + 4)) ∧
      c (P.x (j + 3)) ≠ c (P.x (j + 4))) ∧
     (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable
        (P.x (j + 1)) (P.x (j + 3)) ∧
     (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
        (P.x (j + 1)) (P.x (j + 4))) ∧
    c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
    c (w (j + 2)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x (j + 1)) ∧
    c (w (j + 4)) = c (P.x (j + 3)) :=
  Iff.rfl

/-- At `k = 4` (`q = j + 4`), a doubly locked state of Studio type `R3` has `w₁ = A`, `w₂ = B`,
and `w₄ ∈ {A, μ}` (both occur locally). -/
theorem typeR3_k4_ring (H : Hole6 P w m q) (hq : q = j + 4) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) (hT : TypeR3 P w c j) :
    c (w (j + 1)) = c (P.x (j + 3)) ∧ c (w (j + 2)) = c (P.x (j + 4)) ∧
      (c (w (j + 4)) = c (P.x (j + 3)) ∨ c (w (j + 4)) = c (P.x (j + 1))) := by
  subst hq
  obtain ⟨t0, t3⟩ := hT
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
  have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
  have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hd.1
  refine ⟨?_, ?_, ?_⟩
  · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r01 t0; omega
  · clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
  · clear * - h1 h3 h4 h13 h14 h34 d4 d4'; omega

/-- **`R3At` at `k = 4` is Studio type `R3` plus `w₄ = A`.** -/
theorem r3At_k4_iff (H : Hole6 P w m q) (hq : q = j + 4) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) (hT : TypeR3 P w c j) :
    R3At P w c j ↔ c (w (j + 4)) = c (P.x (j + 3)) := by
  refine ⟨fun hR => hR.2.2.2.2.2, fun hz => r3k4_R3At H hq hc hd hT ?_⟩
  rw [hq]; exact hz

end sphere
end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.r3At_iff
#print axioms SimpleGraph.QuarterFloor.typeR3_k4_ring
#print axioms SimpleGraph.QuarterFloor.r3At_k4_iff
