import DCheckRingKempe
import DCheckRingMeet

/-! Job 25 step 4 (bridge): the ring codes realised by proper colourings of a map with a ring face
of length `r ≤ 5` give a Kempe-closed class predicate (`closedB`); a realised colouring with a
property of its ring colours puts its class in the predicate with the same property. -/

namespace SimpleGraph.SphericalMap
open VacancySlide DCheck DCheck.R2 DCheck.Meet

variable {n : ℕ} {G : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} {h : Fin n}

/-- Ring codes of proper colourings of `G` off `h`. -/
def Realised (G : SphericalMap n) (h : Fin n) (r : ℕ) (ρ : ℕ → Fin n) (k : ℕ) : Prop :=
  ∃ c : Fin n → Fin 4, ProperOff G.graph h c ∧ k = code (ringSeq ρ c) r

theorem canon_col (c : Fin n → Fin 4) :
    ∃ g : Fin 4 → Fin 4, Function.Injective g ∧
      canon r (code (ringSeq ρ c) r) = code (fun t => (g (c (ρ t))).val) r := by
  obtain ⟨g, hg, heq⟩ := canon_rename r (ringSeq ρ c) (ringSeq_lt ρ c)
  refine ⟨g, hg, ?_⟩
  rw [heq]
  apply code_congr
  intro t _
  simp only [ringSeq]
  congr 3
  exact Nat.mod_eq_of_lt (c (ρ t)).isLt

theorem realised_canon {k : ℕ} (hk : Realised G h r ρ k) : Realised G h r ρ (canon r k) := by
  obtain ⟨c1, hc1, rfl⟩ := hk
  obtain ⟨g, hg, heq⟩ := canon_col (r := r) (ρ := ρ) c1
  exact ⟨fun v => g (c1 v), fun u v huv hu hv e => hc1 huv hu hv (hg e), heq⟩

theorem realised_prop (R : RingNC G r ρ) (hh : ∀ t, ρ t ≠ h) {k : ℕ} (hk : Realised G h r ρ k) :
    (∀ i, i < r → col k i ≠ col k ((i + 1) % r)) ∧ k < 4 ^ r := by
  obtain ⟨c1, hc1, rfl⟩ := hk
  refine ⟨fun i hi => ?_, code_lt _ (ringSeq_lt ρ c1) _⟩
  rw [col_code _ (ringSeq_lt ρ c1) _ _ hi, col_code _ (ringSeq_lt ρ c1) _ _ (Nat.mod_lt _ (by omega))]
  simp only [ringSeq]
  intro e
  have hw : ρ ((i + 1) % r) = ρ (i + 1) := by
    by_cases hi1 : i + 1 < r
    · rw [Nat.mod_eq_of_lt hi1]
    · rw [show i + 1 = r by omega, Nat.mod_self, show r = 0 + r by omega, R.per 0]
  rw [hw] at e
  exact hc1 (R.adj i) (hh i) (hh (i + 1)) (Fin.ext e)

open Classical in
/-- The class predicate of the realised codes. -/
noncomputable def gR (G : SphericalMap n) (h : Fin n) (r : ℕ) (ρ : ℕ → Fin n) (K : ℕ) : Fin K → Bool :=
  fun i => decide (Realised G h r ρ (ringColourings r)[i.val]!)

theorem mem_of_realised (R : RingNC G r ρ) (hh : ∀ t, ρ t ≠ h) {K : ℕ}
    (hK : (ringColourings r).size = K) (hr2 : 2 ≤ r) {k : ℕ} (hk : Realised G h r ρ k) :
    ∃ i : Fin K, gR G h r ρ K i = true ∧ (ringColourings r)[i.val]! = canon r k := by
  classical
  have hp := realised_prop R hh hk
  have hm := canon_mem r k hr2 hp.1 hp.2
  obtain ⟨i, hi, e⟩ := Array.mem_iff_getElem.1 hm
  refine ⟨⟨i, hK ▸ hi⟩, ?_, ?_⟩
  · unfold gR; rw [decide_eq_true_iff]
    show Realised G h r ρ (ringColourings r)[i]!
    rw [getElem!_pos _ i hi, e]; exact realised_canon hk
  · show (ringColourings r)[i]! = _
    rw [getElem!_pos _ i hi, e]

theorem mem_true (R : RingNC G r ρ) (hh : ∀ t, ρ t ≠ h) {K : ℕ}
    (hK : (ringColourings r).size = K) (hr2 : 2 ≤ r) {k : ℕ} (hk : Realised G h r ρ k) :
    mem r K (gR G h r ρ K) (canon r k) = true := by
  obtain ⟨i, hi, e⟩ := mem_of_realised R hh hK hr2 hk
  unfold mem
  rw [List.any_eq_true]
  exact ⟨i, List.mem_finRange _, by simp [e, hi]⟩

/-- **The realised class predicate is Kempe-closed** (rings `2 ≤ r ≤ 5`). -/
theorem closedB_realised (R : RingNC G r ρ) (hh : ∀ t, ρ t ≠ h) {K : ℕ}
    (hK : (ringColourings r).size = K) (hr2 : 2 ≤ r) (hr5 : r ≤ 5) :
    closedB r K (gR G h r ρ K) = true := by
  classical
  let cf : Conf := { name := "", r := r, m := 0, ringAdj := #[], intAdj := #[] }
  have hKM := R.kempeMatching hh cf 3 (by decide) rfl (by omega)
  unfold closedB
  rw [List.all_eq_true]
  intro i _
  simp only [Bool.or_eq_true, Bool.not_eq_true']
  by_cases hg : gR G h r ρ K i = true
  · right
    have hk : Realised G h r ρ (ringColourings r)[i.val]! := by
      unfold gR at hg; exact of_decide_eq_true hg
    rw [List.all_eq_true]
    intro th hth
    have hth' : 1 ≤ th ∧ th ≤ 3 := by
      simp only [List.mem_cons, List.mem_singleton, List.not_mem_nil, or_false] at hth
      omega
    simp only [Bool.or_eq_true, beq_iff_eq]
    by_cases hT : (transitions r (ringColourings r)[i.val]! th).size = 0
    · left; exact hT
    · right
      obtain ⟨lab, hlab, hall⟩ := hKM _ th hk hth'.1 hth'.2 hT
      rw [Array.any_eq_true]
      obtain ⟨j, hj, e⟩ := Array.mem_iff_getElem.1 hlab
      refine ⟨j, hj, ?_⟩
      rw [e, List.all_eq_true]
      intro s _
      exact mem_true R hh hK hr2 (hall s)
  · left; simpa using hg

/-- A realised colouring whose renamed ring colours satisfy `Q` puts a class with `Q` into `gR`. -/
theorem has_realised (R : RingNC G r ρ) (hh : ∀ t, ρ t ≠ h) {K : ℕ}
    (hK : (ringColourings r).size = K) (hr2 : 2 ≤ r) (Q : ℕ → Bool)
    {c : Fin n → Fin 4} (hc : ProperOff G.graph h c)
    (hQ : ∀ g : Fin 4 → Fin 4, Function.Injective g → Q (code (fun t => (g (c (ρ t))).val) r) = true) :
    has r K (gR G h r ρ K) Q = true := by
  obtain ⟨i, hi, e⟩ := mem_of_realised R hh hK hr2 (k := code (ringSeq ρ c) r) ⟨c, hc, rfl⟩
  obtain ⟨g, hg, heq⟩ := canon_col (r := r) (ρ := ρ) c
  unfold has
  rw [List.any_eq_true]
  refine ⟨i, List.mem_finRange _, ?_⟩
  rw [hi, e, heq, hQ g hg]; rfl

theorem col_renamed (g : Fin 4 → Fin 4) (c : Fin n → Fin 4) {t : ℕ} (ht : t < r) :
    col (code (fun t => (g (c (ρ t))).val) r) t = (g (c (ρ t))).val :=
  col_code _ (fun t => (g (c (ρ t))).isLt) r t ht

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.closedB_realised
#print axioms SimpleGraph.SphericalMap.has_realised
