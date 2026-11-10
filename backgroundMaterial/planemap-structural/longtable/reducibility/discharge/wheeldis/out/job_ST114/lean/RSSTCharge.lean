import ClaimGlue
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.EulerSharp

/-!
# ST-114 B1: charge and Euler skeleton (statements only)

Studio, 10 Nov. Initial charge `10 (6 − deg v)`. By Euler (`twice_edges_add_twelve_le`, EulerSharp: `2E + 12 ≤ 6n`) and the
handshake lemma, the total charge is at least 120. A discharging transfer `τ` conserves the total, so some vertex ends
positive. Proofs are `sorry` pending the review. No existing module is edited.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap

variable {n : ℕ}

/-- RSST's initial charge, `10 (6 − deg v)`. -/
noncomputable def charge0 (T : SphericalMap n) (v : Fin n) : ℤ :=
  10 * (6 - (T.graph.degree v : ℤ))

/-- Every face of a triangulation with a dart has length 3. -/
theorem faceLength_all {T : SphericalMap n} (htri : T.Triangulated) (d0 : T.Dart) :
    ∀ f : T.Face, T.rotation.faceLength f = 3 := by
  intro f
  rcases f with q | ⟨_, he⟩
  · induction q using Quotient.inductionOn with
    | h a => exact htri a
  · exact (he.false d0).elim

/-- Euler for a triangulation with at least one dart: the total initial charge is at least 120. -/
theorem sum_charge0_ge {T : SphericalMap n} (htri : T.Triangulated) (d0 : T.Dart) :
    120 ≤ ∑ v, charge0 T v := by
  classical
  have hE := T.twice_edges_add_twelve_le d0 (faceLength_all htri d0)
  have hH := T.graph.sum_degrees_eq_twice_card_edges
  have hsum : ∑ v, charge0 T v = 60 * (n : ℤ) - 10 * ((∑ v, T.graph.degree v : ℕ) : ℤ) := by
    have hv : ∀ v, charge0 T v = 60 - 10 * (T.graph.degree v : ℤ) := by intro v; simp only [charge0]; ring
    rw [Finset.sum_congr rfl (fun v _ => hv v), Finset.sum_sub_distrib, ← Finset.mul_sum, Nat.cast_sum]
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    ring
  rw [hsum, hH]
  push_cast
  have : ((2 * T.graph.edgeFinset.card + 12 : ℕ) : ℤ) ≤ ((6 * n : ℕ) : ℤ) := by exact_mod_cast hE
  push_cast at this
  linarith

/-- A discharging step: `τ v w` is the charge `v` sends to `w`. -/
noncomputable def final (T : SphericalMap n) (τ : Fin n → Fin n → ℤ) (v : Fin n) : ℤ :=
  charge0 T v - ∑ w, τ v w + ∑ w, τ w v

/-- Discharging conserves the total charge. -/
theorem sum_final_eq (T : SphericalMap n) (τ : Fin n → Fin n → ℤ) :
    ∑ v, final T τ v = ∑ v, charge0 T v := by
  have hc : ∑ v, ∑ w, τ w v = ∑ v, ∑ w, τ v w := Finset.sum_comm
  simp only [final, Finset.sum_add_distrib, Finset.sum_sub_distrib]
  linarith

/-- Some vertex ends with positive charge. The fixed-point check (B5) shows that every vertex with positive final charge
sees a K633 configuration in its window (via B3 / B4 / B6). -/
theorem exists_pos_final {T : SphericalMap n} (htri : T.Triangulated) (d0 : T.Dart) (τ : Fin n → Fin n → ℤ) :
    ∃ v, 0 < final T τ v := by
  by_contra h
  have h' : ∀ v, final T τ v ≤ 0 := fun v => not_lt.mp (fun hv => h ⟨v, hv⟩)
  have h1 : ∑ v, final T τ v ≤ 0 := Finset.sum_nonpos (fun v _ => h' v)
  have h2 := sum_charge0_ge htri d0
  rw [sum_final_eq] at h1
  linarith

#print axioms sum_charge0_ge
#print axioms sum_final_eq
#print axioms exists_pos_final

end SimpleGraph.SphericalMap.RSSTSeed
