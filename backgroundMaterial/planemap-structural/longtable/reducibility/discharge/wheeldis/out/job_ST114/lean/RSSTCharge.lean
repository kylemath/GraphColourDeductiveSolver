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

/-- Euler for a triangulation with at least one dart: the total initial charge is at least 120. -/
theorem sum_charge0_ge {T : SphericalMap n} (htri : T.Triangulated) (d0 : T.Dart) :
    120 ≤ ∑ v, charge0 T v := by
  sorry

/-- A discharging step: `τ v w` is the charge `v` sends to `w`. -/
noncomputable def final (T : SphericalMap n) (τ : Fin n → Fin n → ℤ) (v : Fin n) : ℤ :=
  charge0 T v - ∑ w, τ v w + ∑ w, τ w v

/-- Discharging conserves the total charge. -/
theorem sum_final_eq (T : SphericalMap n) (τ : Fin n → Fin n → ℤ) :
    ∑ v, final T τ v = ∑ v, charge0 T v := by
  sorry

/-- Some vertex ends with positive charge. The fixed-point check (B5) shows that every vertex with positive final charge
sees a K633 configuration in its window (via B3 / B4 / B6). -/
theorem exists_pos_final {T : SphericalMap n} (htri : T.Triangulated) (d0 : T.Dart) (τ : Fin n → Fin n → ℤ) :
    ∃ v, 0 < final T τ v := by
  sorry

end SimpleGraph.SphericalMap.RSSTSeed
