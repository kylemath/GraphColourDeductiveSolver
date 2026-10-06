module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityGeneral
public import Mathlib.Data.Fintype.Basic

/-!
# Theorem H: an icosahedral hole fills within three pure Kempe swaps

Let the hole `h` have five link vertices `x_t`, each of degree five, so that the
neighbours of `x_t` are exactly `h`, `x_{t-1}`, `x_{t+1}`, `w_{t-1}` and `w_t`,
where `w_t` is the outer common neighbour of `x_t` and `x_{t+1}` and the `w_t`
form a cycle. Then every proper four-colouring of the deletion reaches a filled
hole by at most three whole-component Kempe swaps.

Proof (Math, `MathRadiusGeometry.md`, Theorem H; reviewed in
`StudioMathReviewHPandH.md`). Normalise to the link word `0,1,0,2,3`. If a lock
fails, one swap fills. If both locks hold, the two lock paths force the outer
ring to one of three words, and each has an explicit short sequence:

* `R2`: swap the `{0,2}` component of `x_2`; then `x_2` is isolated in the
  `{3,2}` pair graph and one more swap fills;
* `R3`: swap the three-vertex `{0,1}` component `{x_0,x_1,x_2}`; then `x_3` is
  isolated in the `{0,2}` pair graph and one more swap fills;
* `R1`: swap the `{0,2}` component of `x_2` (it misses `x_0` by the Jordan
  separation), then the three-vertex `{0,3}` component `{x_3,x_4,x_0}`; then `x_1`
  is isolated in the `{0,1}` pair graph and one more swap fills.

The only geometric input is the library's `Alternation` (discharged on spherical
maps by `vacancy_alternation`); it is used for `R1` and `R2`.
-/

@[expose] public section
namespace SimpleGraph.VacancyIcosahedral
open VacancySlide VacancyShortFill VacancyMobility

variable {V : Type*} [DecidableEq V] (G : SimpleGraph V)

/-- The local data of an icosahedral two-ball around the hole. -/
structure IcoBall (h : V) (L : FiveLink G h) (w : Fin 5 → V) : Prop where
  nbr : ∀ t u, G.Adj (L.port t) u ↔
    u = h ∨ u = L.port (t+4) ∨ u = L.port (t+1) ∨ u = w (t+4) ∨ u = w t
  ring : ∀ t, G.Adj (w t) (w (t+1))
  off : ∀ t i, w t ≠ L.port i
  offh : ∀ t, w t ≠ h

set_option synthInstance.maxHeartbeats 400000 in
set_option synthInstance.maxSize 2048 in
/-- The three outer-ring words compatible with both locks. -/
lemma ring_cases : ∀ a0 a1 a2 a3 a4 : Fin 4,
    a0 ≠ 0 → a0 ≠ 1 → a1 ≠ 1 → a1 ≠ 0 → a2 ≠ 0 → a2 ≠ 2 → a3 ≠ 2 → a3 ≠ 3 →
    a4 ≠ 3 → a4 ≠ 0 → a0 ≠ a1 → a1 ≠ a2 → a2 ≠ a3 → a3 ≠ a4 → a4 ≠ a0 →
    (a0 = 2 ∨ a1 = 2) → (a0 = 3 ∨ a1 = 3) → (a2 = 1 ∨ a3 = 1) → (a3 = 1 ∨ a4 = 1) →
    (a0 = 2 ∧ a1 = 3 ∧ a2 = 1 ∧ a3 = 0 ∧ a4 = 1) ∨
    (a0 = 3 ∧ a1 = 2 ∧ a2 = 1 ∧ a3 = 0 ∧ a4 = 1) ∨
    (a0 = 3 ∧ a1 = 2 ∧ a2 = 3 ∧ a3 = 1 ∧ a4 = 2) := by
  decide +kernel

omit [DecidableEq V] in
lemma prepend {h : V} {c d : V → Fin 4} {b : Nat} (step : KempeStep G h c d)
    (fill : PureFill G h d b) : PureFill G h c (b+1) := by
  obtain ⟨n, hn, e, path, target⟩ := fill
  exact ⟨n+1, Nat.add_le_add_right hn 1, e, .cons step path, target⟩

omit [DecidableEq V] in
lemma fill_mono {h : V} {c : V → Fin 4} {a b : Nat} (hab : a ≤ b)
    (f : PureFill G h c a) : PureFill G h c b := by
  obtain ⟨n, hn, rest⟩ := f
  exact ⟨n, hn.trans hab, rest⟩

omit [DecidableEq V] in
lemma first_step {h s t : V} {c : V → Fin 4} {a b : Fin 4}
    (r : (pairGraph G h c a b).Reachable s t) (hst : s ≠ t) :
    ∃ u, (pairGraph G h c a b).Adj s u := by
  obtain ⟨p⟩ := r
  cases p with
  | nil => exact (hst rfl).elim
  | cons e _ => exact ⟨_, e⟩

omit [DecidableEq V] in
lemma step_colour {h s u : V} {c : V → Fin 4} {a b : Fin 4} (hc : ProperOff G h c)
    (e : (pairGraph G h c a b).Adj s u) (hs : c s = a) : c u = b := by
  rcases e.2.2.2 with hu | hu
  · exact absurd (hs.trans hu.symm) (hc e.1 e.2.1.1 e.2.2.1)
  · exact hu

omit [DecidableEq V] in
lemma step_colour' {h s u : V} {c : V → Fin 4} {a b : Fin 4} (hc : ProperOff G h c)
    (e : (pairGraph G h c a b).Adj s u) (hs : c s = b) : c u = a := by
  rcases e.2.2.2 with hu | hu
  · exact hu
  · exact absurd (hs.trans hu.symm) (hc e.1 e.2.1.1 e.2.2.1)

omit [DecidableEq V] in
/-- One swap fills when the only port of colour `rho` is isolated in the pair
graph of `rho` and the colour of a unique port `u`. -/
lemma fill_of_isolated {h u t : V} {c : V → Fin 4} {rho : Fin 4}
    (hc : ProperOff G h c) (hu : G.Adj h u) (uniq : UniqueAt G h u c)
    (hne : c u ≠ rho) (hut : u ≠ t)
    (only : ∀ v, G.Adj h v → c v = rho → v = t)
    (iso : ∀ z, ¬ (pairGraph G h c (c u) rho).Adj t z) :
    PureFill G h c 1 := by
  apply pureFill_one G
  apply one_swap_target G hc hu uniq hne
  intro v ev hv r
  have hvt := only v ev hv
  subst hvt
  obtain ⟨z, hz⟩ := first_step G r.symm (Ne.symm hut)
  exact iso z hz

omit [DecidableEq V] in
/-- **Theorem H, normalised.** At an icosahedral hole with the link word
`0,1,0,2,3`, every proper colouring fills within three pure Kempe swaps. -/
theorem ico_fill_normalized {h : V} {L : FiveLink G h} {w : Fin 5 → V}
    (B : IcoBall G h L w) {c : V → Fin 4} (hc : ProperOff G h c)
    (pat : Pattern G L c) (sep : Alternation G L c) : PureFill G h c 3 := by
  classical
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj G L i).ne.symm
  have pne : ∀ i j, i ≠ j → L.port i ≠ L.port j := fun i j hij e => hij (L.injective e)
  have wh := B.offh
  have wp := B.off
  have adjw : ∀ t, G.Adj (L.port t) (w t) := fun t => (B.nbr t (w t)).mpr (by simp)
  have adjw' : ∀ t, G.Adj (L.port (t+1)) (w t) := by
    intro t
    have e : t + 1 + 4 = t := by rw [add_assoc]; simp
    exact (B.nbr (t+1) (w t)).mpr (Or.inr (Or.inr (Or.inr (Or.inl (by rw [e])))))
  have adjP : ∀ t, G.Adj (L.port t) (L.port (t+1)) := fun t => (B.nbr t _).mpr (by simp)
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  -- a failing lock fills in one swap
  by_cases lock2 : (pairGraph G h c 1 3).Reachable (L.port 1) (L.port 4)
  swap
  · exact fill_mono G (by norm_num) (one_fill_of_right_missing G L hc pat lock2)
  by_cases lock1 : (pairGraph G h c 1 2).Reachable (L.port 1) (L.port 3)
  swap
  · exact fill_mono G (by norm_num) (one_fill_of_left_missing G L hc pat lock1)
  -- the ends of the lock paths read the outer ring
  have E1 : c (w 0) = 2 ∨ c (w 1) = 2 := by
    obtain ⟨u, hu⟩ := first_step G lock1 (pne 1 3 (by decide))
    have hcu := step_colour G hc hu c1
    rcases (B.nbr 1 u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c0] at hcu
    · simp [c2] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have E2 : c (w 0) = 3 ∨ c (w 1) = 3 := by
    obtain ⟨u, hu⟩ := first_step G lock2 (pne 1 4 (by decide))
    have hcu := step_colour G hc hu c1
    rcases (B.nbr 1 u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c0] at hcu
    · simp [c2] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have E3 : c (w 2) = 1 ∨ c (w 3) = 1 := by
    obtain ⟨u, hu⟩ := first_step G lock1.symm (pne 3 1 (by decide))
    have hcu := step_colour' G hc hu c3
    rcases (B.nbr 3 u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c2] at hcu
    · simp [c4] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have E4 : c (w 3) = 1 ∨ c (w 4) = 1 := by
    obtain ⟨u, hu⟩ := first_step G lock2.symm (pne 4 1 (by decide))
    have hcu := step_colour' G hc hu c4
    rcases (B.nbr 4 u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c3] at hcu
    · simp [c0] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have pw : ∀ t i, G.Adj (L.port i) (w t) → c (w t) ≠ c (L.port i) :=
    fun t i e => (hc e (pn i) (wh t)).symm
  have hw : ∀ t, c (w t) ≠ c (w (t+1)) := fun t => hc (B.ring t) (wh t) (wh (t+1))
  rcases ring_cases (c (w 0)) (c (w 1)) (c (w 2)) (c (w 3)) (c (w 4))
      (by simpa [c0] using pw 0 0 (adjw 0)) (by simpa [c1] using pw 0 (0+1) (adjw' 0))
      (by simpa [c1] using pw 1 1 (adjw 1)) (by simpa [c2] using pw 1 (1+1) (adjw' 1))
      (by simpa [c2] using pw 2 2 (adjw 2)) (by simpa [c3] using pw 2 (2+1) (adjw' 2))
      (by simpa [c3] using pw 3 3 (adjw 3)) (by simpa [c4] using pw 3 (3+1) (adjw' 3))
      (by simpa [c4] using pw 4 4 (adjw 4)) (by simpa [c0] using pw 4 (4+1) (adjw' 4))
      (hw 0) (hw 1) (hw 2) (hw 3) (by simpa using hw 4) E1 E2 E3 E4 with
    ⟨e0, e1, e2, e3, e4⟩ | ⟨e0, e1, e2, e3, e4⟩ | ⟨e0, e1, e2, e3, e4⟩
  -- R1 = (2,3,1,0,1): F, then the {0,3} swap of {x_3,x_4,x_0}, then a fill
  · obtain ⟨K, hK, hKm⟩ : ∃ K : Set V, Whole G h c 0 2 K ∧
        ∀ v, v ∈ K ↔ (pairGraph G h c 0 2).Reachable (L.port 2) v :=
      ⟨_, whole_component G h c 0 2 (L.port 2) ⟨pn 2, Or.inl c2⟩, fun _ => Iff.rfl⟩
    have x2K : L.port 2 ∈ K := (hKm _).mpr Reachable.rfl
    have x0K : L.port 0 ∉ K := fun hin => (sep.right lock2).1 ((hKm _).mp hin).symm
    have x3K : L.port 3 ∈ K :=
      whole_closed G hK x2K (by simpa using adjP 2) ⟨pn 3, Or.inr c3⟩
    have w0K : w 0 ∉ K := fun hin =>
      x0K (whole_closed G hK hin (adjw 0).symm ⟨pn 0, Or.inl c0⟩)
    have w3K : w 3 ∈ K := whole_closed G hK x3K (adjw 3) ⟨wh 3, Or.inl e3⟩
    set d := swap c 0 2 K with hd
    have d0 : d (L.port 0) = 0 := by rw [hd, swap_out x0K, c0]
    have d1 : d (L.port 1) = 1 := by
      rw [hd, swap_other (by rw [c1]; decide) (by rw [c1]; decide), c1]
    have d2 : d (L.port 2) = 2 := by rw [hd, swap_in x2K, c2]; decide
    have d3 : d (L.port 3) = 0 := by rw [hd, swap_in x3K, c3]; decide
    have d4 : d (L.port 4) = 3 := by
      rw [hd, swap_other (by rw [c4]; decide) (by rw [c4]; decide), c4]
    have dw0 : d (w 0) = 2 := by rw [hd, swap_out w0K, e0]
    have dw1 : d (w 1) = 3 := by
      rw [hd, swap_other (by rw [e1]; decide) (by rw [e1]; decide), e1]
    have dw2 : d (w 2) = 1 := by
      rw [hd, swap_other (by rw [e2]; decide) (by rw [e2]; decide), e2]
    have dw3 : d (w 3) = 2 := by rw [hd, swap_in w3K, e3]; decide
    have dw4 : d (w 4) = 1 := by
      rw [hd, swap_other (by rw [e4]; decide) (by rw [e4]; decide), e4]
    have stepF : KempeStep G h c d := ⟨0, 2, K, by decide, hK, rfl⟩
    have hd' : ProperOff G h d := properOff_swap G hc hK
    -- the {0,3} component of x_4 in d is {x_3, x_4, x_0}
    obtain ⟨J, hJ, hJm⟩ : ∃ J : Set V, Whole G h d 0 3 J ∧
        ∀ v, v ∈ J ↔ (pairGraph G h d 0 3).Reachable (L.port 4) v :=
      ⟨_, whole_component G h d 0 3 (L.port 4) ⟨pn 4, Or.inr d4⟩, fun _ => Iff.rfl⟩
    have Jsub : ∀ v, v ∈ J → v = L.port 3 ∨ v = L.port 4 ∨ v = L.port 0 := by
      intro v hv
      refine reachable_invariant (H := pairGraph G h d 0 3)
        (P := fun v => v = L.port 3 ∨ v = L.port 4 ∨ v = L.port 0) ?_
        (Or.inr (Or.inl rfl)) ((hJm v).mp hv)
      intro a b e ha
      have hb := e.2.2.2
      rcases ha with rfl | rfl | rfl
      · rcases (B.nbr 3 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl e.2.2.1
        · simp [d2] at hb
        · simp
        · simp [dw2] at hb
        · simp [dw3] at hb
      · rcases (B.nbr 4 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl e.2.2.1
        · simp
        · simp
        · simp [dw3] at hb
        · simp [dw4] at hb
      · rcases (B.nbr 0 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl e.2.2.1
        · simp
        · simp [d1] at hb
        · simp [dw4] at hb
        · simp [dw0] at hb
    have x4J : L.port 4 ∈ J := (hJm _).mpr Reachable.rfl
    have x3J : L.port 3 ∈ J :=
      whole_closed G hJ x4J (by simpa using (adjP 3).symm) ⟨pn 3, Or.inl d3⟩
    have x0J : L.port 0 ∈ J :=
      whole_closed G hJ x4J (by simpa using adjP 4) ⟨pn 0, Or.inl d0⟩
    have x1J : L.port 1 ∉ J := fun hin => by
      rcases Jsub _ hin with e | e | e <;> exact pne _ _ (by decide) e
    have x2J : L.port 2 ∉ J := fun hin => by
      rcases Jsub _ hin with e | e | e <;> exact pne _ _ (by decide) e
    have wJ : ∀ t, w t ∉ J := fun t hin => by
      rcases Jsub _ hin with e | e | e <;> exact wp t _ e
    set f := swap d 0 3 J with hf
    have f0 : f (L.port 0) = 3 := by rw [hf, swap_in x0J, d0]; decide
    have f1 : f (L.port 1) = 1 := by rw [hf, swap_out x1J, d1]
    have f2 : f (L.port 2) = 2 := by rw [hf, swap_out x2J, d2]
    have f3 : f (L.port 3) = 3 := by rw [hf, swap_in x3J, d3]; decide
    have f4 : f (L.port 4) = 0 := by rw [hf, swap_in x4J, d4]; decide
    have fw0 : f (w 0) = 2 := by rw [hf, swap_out (wJ 0), dw0]
    have fw1 : f (w 1) = 3 := by rw [hf, swap_out (wJ 1), dw1]
    have stepA : KempeStep G h d f := ⟨0, 3, J, by decide, hJ, rfl⟩
    have hf' : ProperOff G h f := properOff_swap G hd' hJ
    have fill : PureFill G h f 1 := by
      apply fill_of_isolated G hf' (port_adj G L 4) (t := L.port 1) (rho := 1)
      · intro y ey eq
        obtain ⟨i, rfl⟩ := (L.neighbours y).mp ey
        fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
      · rw [f4]; decide
      · exact pne 4 1 (by decide)
      · intro v ev eq
        obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
        fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
      · intro z hz
        have hb := hz.2.2.2
        rw [f4] at hb
        rcases (B.nbr 1 z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hz.2.2.1
        · simp [f0] at hb
        · simp [f2] at hb
        · simp [fw0] at hb
        · simp [fw1] at hb
    exact prepend G stepF (prepend G stepA fill)
  -- R2 = (3,2,1,0,1): F, then a fill
  · obtain ⟨K, hK, hKm⟩ : ∃ K : Set V, Whole G h c 0 2 K ∧
        ∀ v, v ∈ K ↔ (pairGraph G h c 0 2).Reachable (L.port 2) v :=
      ⟨_, whole_component G h c 0 2 (L.port 2) ⟨pn 2, Or.inl c2⟩, fun _ => Iff.rfl⟩
    have x2K : L.port 2 ∈ K := (hKm _).mpr Reachable.rfl
    have x0K : L.port 0 ∉ K := fun hin => (sep.right lock2).1 ((hKm _).mp hin).symm
    have x3K : L.port 3 ∈ K :=
      whole_closed G hK x2K (by simpa using adjP 2) ⟨pn 3, Or.inr c3⟩
    have w1K : w 1 ∈ K := whole_closed G hK x2K (by simpa using adjw' 1) ⟨wh 1, Or.inr e1⟩
    set d := swap c 0 2 K with hd
    have d0 : d (L.port 0) = 0 := by rw [hd, swap_out x0K, c0]
    have d1 : d (L.port 1) = 1 := by
      rw [hd, swap_other (by rw [c1]; decide) (by rw [c1]; decide), c1]
    have d2 : d (L.port 2) = 2 := by rw [hd, swap_in x2K, c2]; decide
    have d3 : d (L.port 3) = 0 := by rw [hd, swap_in x3K, c3]; decide
    have d4 : d (L.port 4) = 3 := by
      rw [hd, swap_other (by rw [c4]; decide) (by rw [c4]; decide), c4]
    have dw1 : d (w 1) = 0 := by rw [hd, swap_in w1K, e1]; decide
    have dw2 : d (w 2) = 1 := by
      rw [hd, swap_other (by rw [e2]; decide) (by rw [e2]; decide), e2]
    have stepF : KempeStep G h c d := ⟨0, 2, K, by decide, hK, rfl⟩
    have hd' : ProperOff G h d := properOff_swap G hc hK
    have fill : PureFill G h d 1 := by
      apply fill_of_isolated G hd' (port_adj G L 4) (t := L.port 2) (rho := 2)
      · intro y ey eq
        obtain ⟨i, rfl⟩ := (L.neighbours y).mp ey
        fin_cases i <;> simp [d0, d1, d2, d3, d4] at eq ⊢
      · rw [d4]; decide
      · exact pne 4 2 (by decide)
      · intro v ev eq
        obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
        fin_cases i <;> simp [d0, d1, d2, d3, d4] at eq ⊢
      · intro z hz
        have hb := hz.2.2.2
        rw [d4] at hb
        rcases (B.nbr 2 z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hz.2.2.1
        · simp [d1] at hb
        · simp [d3] at hb
        · simp [dw1] at hb
        · simp [dw2] at hb
    exact fill_mono G (by norm_num) (prepend G stepF fill)
  -- R3 = (3,2,3,1,2): the {0,1} swap of {x_0,x_1,x_2}, then a fill
  · obtain ⟨J, hJ, hJm⟩ : ∃ J : Set V, Whole G h c 0 1 J ∧
        ∀ v, v ∈ J ↔ (pairGraph G h c 0 1).Reachable (L.port 1) v :=
      ⟨_, whole_component G h c 0 1 (L.port 1) ⟨pn 1, Or.inr c1⟩, fun _ => Iff.rfl⟩
    have Jsub : ∀ v, v ∈ J → v = L.port 0 ∨ v = L.port 1 ∨ v = L.port 2 := by
      intro v hv
      refine reachable_invariant (H := pairGraph G h c 0 1)
        (P := fun v => v = L.port 0 ∨ v = L.port 1 ∨ v = L.port 2) ?_
        (Or.inr (Or.inl rfl)) ((hJm v).mp hv)
      intro a b e ha
      have hb := e.2.2.2
      rcases ha with rfl | rfl | rfl
      · rcases (B.nbr 0 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl e.2.2.1
        · simp [c4] at hb
        · simp
        · simp [e4] at hb
        · simp [e0] at hb
      · rcases (B.nbr 1 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl e.2.2.1
        · simp
        · simp
        · simp [e0] at hb
        · simp [e1] at hb
      · rcases (B.nbr 2 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl e.2.2.1
        · simp
        · simp [c3] at hb
        · simp [e1] at hb
        · simp [e2] at hb
    have x1J : L.port 1 ∈ J := (hJm _).mpr Reachable.rfl
    have x0J : L.port 0 ∈ J :=
      whole_closed G hJ x1J (by simpa using (adjP 0).symm) ⟨pn 0, Or.inl c0⟩
    have x2J : L.port 2 ∈ J :=
      whole_closed G hJ x1J (by simpa using adjP 1) ⟨pn 2, Or.inl c2⟩
    have x3J : L.port 3 ∉ J := fun hin => by
      rcases Jsub _ hin with e | e | e <;> exact pne _ _ (by decide) e
    have x4J : L.port 4 ∉ J := fun hin => by
      rcases Jsub _ hin with e | e | e <;> exact pne _ _ (by decide) e
    have wJ : ∀ t, w t ∉ J := fun t hin => by
      rcases Jsub _ hin with e | e | e <;> exact wp t _ e
    set f := swap c 0 1 J with hf
    have f0 : f (L.port 0) = 1 := by rw [hf, swap_in x0J, c0]; decide
    have f1 : f (L.port 1) = 0 := by rw [hf, swap_in x1J, c1]; decide
    have f2 : f (L.port 2) = 1 := by rw [hf, swap_in x2J, c2]; decide
    have f3 : f (L.port 3) = 2 := by rw [hf, swap_out x3J, c3]
    have f4 : f (L.port 4) = 3 := by rw [hf, swap_out x4J, c4]
    have fw2 : f (w 2) = 3 := by rw [hf, swap_out (wJ 2), e2]
    have fw3 : f (w 3) = 1 := by rw [hf, swap_out (wJ 3), e3]
    have stepA : KempeStep G h c f := ⟨0, 1, J, by decide, hJ, rfl⟩
    have hf' : ProperOff G h f := properOff_swap G hc hJ
    have fill : PureFill G h f 1 := by
      apply fill_of_isolated G hf' (port_adj G L 1) (t := L.port 3) (rho := 2)
      · intro y ey eq
        obtain ⟨i, rfl⟩ := (L.neighbours y).mp ey
        fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
      · rw [f1]; decide
      · exact pne 1 3 (by decide)
      · intro v ev eq
        obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
        fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
      · intro z hz
        have hb := hz.2.2.2
        rw [f1] at hb
        rcases (B.nbr 3 z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hz.2.2.1
        · simp [f2] at hb
        · simp [f4] at hb
        · simp [fw2] at hb
        · simp [fw3] at hb
    exact fill_mono G (by norm_num) (prepend G stepA fill)

end SimpleGraph.VacancyIcosahedral

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral
variable {n : Nat} (M : SphericalMap n)

/-- **Theorem H.** On a spherical map, if the five link vertices of the hole
`h` have degree five (the icosahedral two-ball `IcoBall`) and the ports follow
the rotation at `h`, then every proper four-colouring of the deletion fills
within three pure Kempe swaps. -/
theorem ico_fill {h : Fin n} (L : FiveLink M.graph h) {w : Fin 5 → Fin n}
    (B : IcoBall M.graph h L w)
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) :
    PureFill M.graph h c 3 := by
  classical
  have ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)) :=
    fun i => (B.nbr i _).mpr (by simp)
  by_cases surj : ∀ x : Fin 4, ∃ i, c (L.port i) = x
  · obtain ⟨k, inj, hk⟩ := ring_normalize (fun i => c (L.port i))
      (fun i => hc (ring i) (port_adj M.graph L i).ne.symm (port_adj M.graph L _).ne.symm)
      surj
    let σ : Fin 4 ≃ Fin 4 := Equiv.ofBijective _ (Finite.injective_iff_bijective.mp inj)
    let L' := FiveLink.shift M L k
    have pat : Pattern M.graph L' (fun v => σ (c v)) := fun i => hk i
    have rot' : ∀ i : Fin 5,
        M.rotation.next ⟨(h, L'.port i), port_adj M.graph L' i⟩ =
          ⟨(h, L'.port (i+1)), port_adj M.graph L' (i+1)⟩ := by
      intro i
      have key : ∀ j j' : Fin 5, j' = j + 1 →
          M.rotation.next ⟨(h, L.port j), port_adj M.graph L j⟩ =
            ⟨(h, L.port j'), port_adj M.graph L j'⟩ := by
        rintro j j' rfl; exact rot j
      exact key (i + k) (i + 1 + k) (by abel)
    have B' : IcoBall M.graph h L' (fun t => w (t + k)) := by
      refine ⟨fun t u => ?_, fun t => ?_, fun t i => B.off _ _, fun t => B.offh _⟩
      · change M.graph.Adj (L.port (t + k)) u ↔ _
        rw [B.nbr (t + k) u]
        change _ ↔ u = h ∨ u = L.port (t + 4 + k) ∨ u = L.port (t + 1 + k) ∨
          u = w (t + 4 + k) ∨ u = w (t + k)
        rw [add_right_comm t 4 k, add_right_comm t 1 k]
      · show M.graph.Adj (w (t + k)) (w (t + 1 + k))
        rw [add_right_comm]; exact B.ring _
    have fill := ico_fill_normalized M.graph B' (properOff_rename _ σ hc) pat
      (vacancy_alternation M L' pat rot')
    have := pureFill_rename M.graph σ.symm fill
    simpa using this
  · push Not at surj
    obtain ⟨x, hx⟩ := surj
    refine ⟨0, by decide, c, PurePath.nil _, x, ?_⟩
    intro v ev
    obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
    exact hx i

end SimpleGraph.SphericalMap
