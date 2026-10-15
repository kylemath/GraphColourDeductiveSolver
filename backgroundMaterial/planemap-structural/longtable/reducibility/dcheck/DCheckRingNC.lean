import DCheckR2D

/-! Job 25: the ring data that the Kempe closure actually uses (`RingNC`: periodic, cyclically
adjacent, and the two non-crossing facts for Kempe chains joining alternating ring positions).
A ring face gives it in either orientation, so the two sides of a separating cycle can be compared
on one ring labelling. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill

variable {n : ℕ}

/-- Ring data used by the Kempe closure. -/
structure RingNC (G : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) : Prop where
  pos : 0 < r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, G.Adj (ρ t) (ρ (t + 1))
  nc : ∀ {h : Fin n} {c : Fin n → Fin 4} {a b a' b' : Fin 4},
    (∀ x : Fin 4, (x = a ∨ x = b) → (x = a' ∨ x = b') → False) →
    ∀ {i j k l : ℕ}, i < j → j < k → k < l → l < r →
    (pairGraph G.graph h c a b).Reachable (ρ i) (ρ k) →
    (pairGraph G.graph h c a' b').Reachable (ρ j) (ρ l) → False
  ncs : ∀ {h : Fin n} {c : Fin n → Fin 4} {a b : Fin 4} {i j k l : ℕ},
    i < j → j < k → k < l → l < r →
    (pairGraph G.graph h c a b).Reachable (ρ i) (ρ k) →
    (pairGraph G.graph h c a b).Reachable (ρ j) (ρ l) →
    ¬ (pairGraph G.graph h c a b).Reachable (ρ i) (ρ j) → False

variable {G : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n}

theorem RingFace.toNC (R : RingFace G r ρ) : RingNC G r ρ :=
  ⟨R.pos, R.per, R.adj, fun hd _ _ _ _ h1 h2 h3 h4 =>
    chains_noncrossing R hd h1 h2 h3 h4, fun h1 h2 h3 h4 p q hne =>
    chains_noncrossing_same R h1 h2 h3 h4 p q hne⟩

/-- The reversed ring: `revR r ρ t = ρ ((r - 1) t)`, i.e. `ρ (-t)` up to the period. -/
def revR (r : ℕ) (ρ : ℕ → Fin n) : ℕ → Fin n := fun t => ρ ((r - 1) * t)

theorem per_mul (hper : ∀ t, ρ (t + r) = ρ t) (x : ℕ) : ∀ k, ρ (x + r * k) = ρ x := by
  intro k
  induction k with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, hper, ih]

/-- Reversed position of `p`: `0 ↦ 0`, `p ↦ r - p`. -/
def rpos (r p : ℕ) : ℕ := if p = 0 then 0 else r - p

theorem revR_rpos (hr : 2 ≤ r) (hper : ∀ t, ρ (t + r) = ρ t) (p : ℕ) (hp : p < r) :
    revR r ρ (rpos r p) = ρ p := by
  unfold revR rpos
  obtain ⟨q, rfl⟩ : ∃ q, r = q + 2 := ⟨r - 2, by omega⟩
  split_ifs with h0
  · subst h0; simp
  · obtain ⟨p', rfl⟩ : ∃ p', p = p' + 1 := ⟨p - 1, by omega⟩
    obtain ⟨u, hu⟩ : ∃ u, q + 2 - (p' + 1) = u + 1 := ⟨q - p', by omega⟩
    have hq : q + 2 - 1 = q + 1 := by omega
    rw [hq, hu]
    have : (q + 1) * (u + 1) = (p' + 1) + (q + 2) * u := by
      have hpu : p' + u + 1 = q + 2 - 1 := by omega
      nlinarith [hpu]
    rw [this, per_mul hper]

/-- A ring face of the reversed ring gives the ring data of `ρ` (rings `r ≥ 2`). -/
theorem RingFace.revNC (R : RingFace G r (revR r ρ)) (hr : 2 ≤ r) (hper : ∀ t, ρ (t + r) = ρ t) :
    RingNC G r ρ := by
  have hpos : 0 < r := by omega
  refine ⟨hpos, hper, fun t => ?_, ?_, ?_⟩
  · -- `revR s ~ revR (s+1)` at `s = (r-1) t + (r-1)` gives `ρ (t+1) ~ ρ t`
    obtain ⟨q, rfl⟩ : ∃ q, r = q + 2 := ⟨r - 2, by omega⟩
    have a := R.adj ((q + 1) * t + (q + 1))
    unfold revR at a
    rw [show q + 2 - 1 = q + 1 by omega] at a
    have e1 : (q + 1) * ((q + 1) * t + (q + 1)) = (t + 1) + (q + 2) * (q * (t + 1)) := by ring
    have e2 : (q + 1) * ((q + 1) * t + (q + 1) + 1) = t + (q + 2) * (q * (t + 1) + 1) := by ring
    rw [e1, e2, per_mul hper, per_mul hper] at a
    exact a.symm
  · intro h c a b a' b' hd i j k l hij hjk hkl hlr h1 h2
    have hP := fun x hx => revR_rpos (ρ := ρ) hr hper x hx
    have rp : ∀ x, 0 < x → rpos r x = r - x := fun x hx => by unfold rpos; rw [if_neg (by omega)]
    rcases Nat.eq_zero_or_pos i with hi | hi
    · subst hi
      have q1 : (pairGraph G.graph h c a b).Reachable (revR r ρ 0) (revR r ρ (r - k)) := by
        have e0 : revR r ρ 0 = ρ 0 := hP 0 hpos
        have e3 := hP k (by omega); rw [rp k (by omega)] at e3
        rw [e0, e3]; exact h1
      have q2 : (pairGraph G.graph h c a' b').Reachable (revR r ρ (r - l)) (revR r ρ (r - j)) := by
        have e1 := hP l hlr; have e2 := hP j (by omega)
        rw [rp l (by omega)] at e1; rw [rp j (by omega)] at e2
        rw [e1, e2]; exact h2.symm
      exact chains_noncrossing R hd (by omega : 0 < r - l) (by omega : r - l < r - k)
        (by omega : r - k < r - j) (by omega : r - j < r) q1 q2
    · have e1 := hP l hlr; have e2 := hP j (by omega)
      have e3 := hP k (by omega); have e4 := hP i (by omega)
      rw [rp l (by omega)] at e1; rw [rp j (by omega)] at e2
      rw [rp k (by omega)] at e3; rw [rp i hi] at e4
      have q1 : (pairGraph G.graph h c a' b').Reachable (revR r ρ (r - l)) (revR r ρ (r - j)) := by
        rw [e1, e2]; exact h2.symm
      have q2 : (pairGraph G.graph h c a b).Reachable (revR r ρ (r - k)) (revR r ρ (r - i)) := by
        rw [e3, e4]; exact h1.symm
      exact chains_noncrossing R (fun x u v => hd x v u) (by omega : r - l < r - k)
        (by omega : r - k < r - j) (by omega : r - j < r - i) (by omega : r - i < r) q1 q2
  · intro h c a b i j k l hij hjk hkl hlr h1 h2 hne
    have hP := fun x hx => revR_rpos (ρ := ρ) hr hper x hx
    have rp : ∀ x, 0 < x → rpos r x = r - x := fun x hx => by unfold rpos; rw [if_neg (by omega)]
    rcases Nat.eq_zero_or_pos i with hi | hi
    · subst hi
      have e0 : revR r ρ 0 = ρ 0 := hP 0 hpos
      have e1 := hP l hlr; have e2 := hP j (by omega); have e3 := hP k (by omega)
      rw [rp l (by omega)] at e1; rw [rp j (by omega)] at e2; rw [rp k (by omega)] at e3
      apply chains_noncrossing_same R (by omega : 0 < r - l) (by omega : r - l < r - k)
        (by omega : r - k < r - j) (by omega : r - j < r)
      · rw [e0, e3]; exact h1
      · rw [e1, e2]; exact h2.symm
      · rw [e0, e1]; exact fun hr' => hne (hr'.trans h2.symm)
    · have e1 := hP l hlr; have e2 := hP j (by omega)
      have e3 := hP k (by omega); have e4 := hP i (by omega)
      rw [rp l (by omega)] at e1; rw [rp j (by omega)] at e2
      rw [rp k (by omega)] at e3; rw [rp i hi] at e4
      apply chains_noncrossing_same R (by omega : r - l < r - k) (by omega : r - k < r - j)
        (by omega : r - j < r - i) (by omega : r - i < r)
      · rw [e1, e2]; exact h2.symm
      · rw [e3, e4]; exact h1.symm
      · rw [e1, e3]; exact fun hr' => hne ((h1.trans hr'.symm).trans h2.symm)

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.RingFace.revNC
