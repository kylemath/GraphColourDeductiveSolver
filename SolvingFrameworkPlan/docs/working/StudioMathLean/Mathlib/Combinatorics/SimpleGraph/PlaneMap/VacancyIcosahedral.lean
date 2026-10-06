module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityTriangulated
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron
public import Mathlib.Data.Fintype.Basic
public import Mathlib.Tactic.IntervalCases

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


/-! ## Deriving the icosahedral two-ball from triangulation and degree hypotheses -/

/-- `Nx u v w`: in the rotation at `u`, the neighbour after `v` is `w`. -/
def Nx (u v w : Fin n) : Prop :=
  ∃ huv : M.Adj u v, (M.rotation.next ⟨(u,v),huv⟩).snd = w

/-- Every triangle through `h` is a face: adjacent neighbours of `h` are consecutive in the
rotation at `h`. On a triangulation this says that no separating triangle passes through `h`. -/
def NoSeparatingTriangleAt (h : Fin n) : Prop :=
  ∀ u v (hu : M.Adj h u) (hv : M.Adj h v), M.Adj u v →
    M.rotation.next ⟨(h,u),hu⟩ = ⟨(h,v),hv⟩ ∨ M.rotation.next ⟨(h,v),hv⟩ = ⟨(h,u),hu⟩

variable {M}

lemma nx_dart {u v w : Fin n} (hx : Nx M u v w) :
    ∃ (huv : M.Adj u v) (huw : M.Adj u w),
      M.rotation.next ⟨(u,v),huv⟩ = ⟨(u,w),huw⟩ := by
  obtain ⟨huv, hs⟩ := hx
  have hf : (M.rotation.next ⟨(u,v),huv⟩).fst = u := M.rotation.next_fst _
  have huw : M.Adj u w := by
    have := (M.rotation.next ⟨(u,v),huv⟩).adj
    rwa [show (M.rotation.next ⟨(u,v),huv⟩).toProd.1 = u from hf,
      show (M.rotation.next ⟨(u,v),huv⟩).toProd.2 = w from hs] at this
  exact ⟨huv, huw, (by apply Dart.ext; exact Prod.ext hf hs)⟩

lemma nx_of_dart {u v w : Fin n} {huv : M.Adj u v} {huw : M.Adj u w}
    (e : M.rotation.next ⟨(u,v),huv⟩ = ⟨(u,w),huw⟩) : Nx M u v w :=
  ⟨huv, by rw [e]⟩

lemma nx_adj_left {u v w : Fin n} (hx : Nx M u v w) : M.Adj u v := hx.1

lemma nx_adj_right {u v w : Fin n} (hx : Nx M u v w) : M.Adj u w :=
  (nx_dart hx).2.1

/-- The triangle law: going round a triangular face. -/
lemma nx_tri (htri : M.Triangulated) {u v y : Fin n} (hx : Nx M v u y) :
    Nx M y v u ∧ Nx M u y v := by
  obtain ⟨hvu, hvy, h1⟩ := nx_dart hx
  have h3 := M.rotation.face_next_iterate_length (⟨(u,v),hvu.symm⟩ : M.Dart)
  rw [show M.rotation.faceLength (M.rotation.faceOf _) = 3 from htri _] at h3
  simp only [Function.iterate_succ_apply', Function.iterate_zero_apply,
    RotationSystem.face_next_apply] at h3
  change M.rotation.next (M.rotation.next (M.rotation.next ⟨(v,u),hvu⟩).symm).symm = _ at h3
  rw [h1] at h3
  change M.rotation.next (M.rotation.next ⟨(y,v),hvy.symm⟩).symm = _ at h3
  set d2 := M.rotation.next ⟨(y,v),hvy.symm⟩ with hd2
  have hf : d2.fst = y := M.rotation.next_fst _
  have hs : d2.snd = u := by
    have := congrArg (fun d : M.Dart => d.fst) h3
    simp only [RotationSystem.next_fst] at this
    exact this
  have hyu : M.Adj y u := by
    have := d2.adj
    rwa [show d2.toProd.1 = y from hf, show d2.toProd.2 = u from hs] at this
  have hd : d2 = ⟨(y,u),hyu⟩ := (by apply Dart.ext; exact Prod.ext hf hs)
  refine ⟨nx_of_dart hd, ?_⟩
  rw [hd] at h3
  exact nx_of_dart h3

/-- At a vertex of degree five the rotation is a single five-cycle of darts. -/
lemma orbit5 {v : Fin n} (hv : M.graph.degree v = 5) (d : M.Dart) (hd : d.fst = v) :
    (⇑M.rotation.next)^[5] d = d ∧
    (∀ i j : ℕ, i < 5 → j < 5 →
      (⇑M.rotation.next)^[i] d = (⇑M.rotation.next)^[j] d → i = j) ∧
    (∀ e : M.Dart, e.fst = v → ∃ k, k < 5 ∧ (⇑M.rotation.next)^[k] d = e) := by
  classical
  subst hd
  let R := M.rotation
  let σ := R.neighborRotation d.fst
  let w : M.graph.neighborSet d.fst := ⟨d.snd, d.adj⟩
  have hdw : M.graph.dartOfNeighborSet d.fst w = d := rfl
  have hsemi : Function.Semiconj (M.graph.dartOfNeighborSet d.fst) σ R.next :=
    R.neighbor_rotation_dart d.fst
  have hit : ∀ k, (⇑R.next)^[k] d = M.graph.dartOfNeighborSet d.fst (σ^[k] w) := fun k => by
    have := hsemi.iterate_right k w
    rw [hdw] at this
    exact this.symm
  have hp : Function.minimalPeriod σ w = 5 := by
    rw [R.neighbor_period_eq_degree, hv]
  refine ⟨?_, ?_, ?_⟩
  · rw [hit, ← hp, Function.iterate_minimalPeriod, hdw]
  · intro i j hi hj hij
    rw [hit, hit] at hij
    exact Function.iterate_injOn_Iio_minimalPeriod (by rw [hp]; exact hi) (by rw [hp]; exact hj)
      (M.graph.dartOfNeighborSet_injective _ hij)
  · intro e he
    obtain ⟨k, hk⟩ := R.neighbor_rotation_cyclic d.fst w ⟨e.snd, by rw [← he]; exact e.adj⟩
    refine ⟨k % 5, Nat.mod_lt _ (by norm_num), ?_⟩
    rw [hit, ← hp, Function.iterate_mod_minimalPeriod_eq, hk]
    exact (by apply Dart.ext; exact Prod.ext he.symm rfl)

/-- A rotation chain of four steps at a degree-five vertex closes up, and lists every
neighbour exactly once. -/
lemma chain5 {v a0 a1 a2 a3 a4 : Fin n} (hv : M.graph.degree v = 5)
    (h01 : Nx M v a0 a1) (h12 : Nx M v a1 a2) (h23 : Nx M v a2 a3) (h34 : Nx M v a3 a4) :
    Nx M v a4 a0 ∧
      (a0 ≠ a1 ∧ a0 ≠ a2 ∧ a0 ≠ a3 ∧ a0 ≠ a4 ∧ a1 ≠ a2 ∧ a1 ≠ a3 ∧ a1 ≠ a4 ∧
        a2 ≠ a3 ∧ a2 ≠ a4 ∧ a3 ≠ a4) ∧
      ∀ u, M.Adj v u → u = a0 ∨ u = a1 ∨ u = a2 ∨ u = a3 ∨ u = a4 := by
  obtain ⟨g0, g1, e01⟩ := nx_dart h01
  obtain ⟨_g1, g2, e12⟩ := nx_dart h12
  obtain ⟨_g2, g3, e23⟩ := nx_dart h23
  obtain ⟨_g3, g4, e34⟩ := nx_dart h34
  let D : M.Dart := ⟨(v,a0),g0⟩
  obtain ⟨p5, inj, surj⟩ := orbit5 hv D rfl
  have i1 : (⇑M.rotation.next)^[1] D = ⟨(v,a1),g1⟩ := e01
  have i2 : (⇑M.rotation.next)^[2] D = ⟨(v,a2),g2⟩ := by
    rw [Function.iterate_succ_apply', i1]; exact e12
  have i3 : (⇑M.rotation.next)^[3] D = ⟨(v,a3),g3⟩ := by
    rw [Function.iterate_succ_apply', i2]; exact e23
  have i4 : (⇑M.rotation.next)^[4] D = ⟨(v,a4),g4⟩ := by
    rw [Function.iterate_succ_apply', i3]; exact e34
  have i0 : (⇑M.rotation.next)^[0] D = ⟨(v,a0),g0⟩ := rfl
  have close : M.rotation.next ⟨(v,a4),g4⟩ = ⟨(v,a0),g0⟩ := by
    rw [← i4, ← Function.iterate_succ_apply' (⇑M.rotation.next) 4]; exact p5
  have fstI : ∀ (k : ℕ) (d : M.Dart), ((⇑M.rotation.next)^[k] d).fst = d.fst := by
    intro k
    induction k with
    | zero => intro d; rfl
    | succ k ih => intro d; rw [Function.iterate_succ_apply', M.rotation.next_fst, ih]
  have dist : ∀ i j : ℕ, i < 5 → j < 5 → i ≠ j →
      ((⇑M.rotation.next)^[i] D).snd ≠ ((⇑M.rotation.next)^[j] D).snd := by
    intro i j hi hj hij hs
    apply hij
    apply inj i j hi hj
    apply Dart.ext
    apply Prod.ext
    · rw [fstI, fstI]
    · exact hs
  refine ⟨nx_of_dart close, ?_, ?_⟩
  · have ne : ∀ i j : ℕ, i < 5 → j < 5 → i ≠ j → ∀ x y : Fin n,
        ((⇑M.rotation.next)^[i] D).snd = x → ((⇑M.rotation.next)^[j] D).snd = y → x ≠ y :=
      fun i j hi hj hij x y hx hy e => dist i j hi hj hij (by rw [hx, hy, e])
    have s0 : ((⇑M.rotation.next)^[0] D).snd = a0 := by rw [i0]
    have s1 : ((⇑M.rotation.next)^[1] D).snd = a1 := by rw [i1]
    have s2 : ((⇑M.rotation.next)^[2] D).snd = a2 := by rw [i2]
    have s3 : ((⇑M.rotation.next)^[3] D).snd = a3 := by rw [i3]
    have s4 : ((⇑M.rotation.next)^[4] D).snd = a4 := by rw [i4]
    exact ⟨ne 0 1 (by norm_num) (by norm_num) (by norm_num) _ _ s0 s1,
      ne 0 2 (by norm_num) (by norm_num) (by norm_num) _ _ s0 s2,
      ne 0 3 (by norm_num) (by norm_num) (by norm_num) _ _ s0 s3,
      ne 0 4 (by norm_num) (by norm_num) (by norm_num) _ _ s0 s4,
      ne 1 2 (by norm_num) (by norm_num) (by norm_num) _ _ s1 s2,
      ne 1 3 (by norm_num) (by norm_num) (by norm_num) _ _ s1 s3,
      ne 1 4 (by norm_num) (by norm_num) (by norm_num) _ _ s1 s4,
      ne 2 3 (by norm_num) (by norm_num) (by norm_num) _ _ s2 s3,
      ne 2 4 (by norm_num) (by norm_num) (by norm_num) _ _ s2 s4,
      ne 3 4 (by norm_num) (by norm_num) (by norm_num) _ _ s3 s4⟩
  · intro u hu
    obtain ⟨k, hk, e⟩ := surj ⟨(v,u),hu⟩ rfl
    have hs := congrArg (fun d : M.Dart => d.snd) e
    interval_cases k
    · left; rw [i0] at hs; exact hs.symm
    · right; left; rw [i1] at hs; exact hs.symm
    · right; right; left; rw [i2] at hs; exact hs.symm
    · right; right; right; left; rw [i3] at hs; exact hs.symm
    · right; right; right; right; rw [i4] at hs; exact hs.symm

variable (M)

/-- A degree-five vertex has a five-port link. -/
noncomputable def linkOfDegree {h : Fin n} (hdeg : M.graph.degree h = 5) :
    FiveLink M.graph h := by
  classical
  let e : M.graph.neighborSet h ≃ Fin 5 :=
    Fintype.equivFinOfCardEq (by rw [card_neighborSet_eq_degree, hdeg])
  exact ⟨fun i => (e.symm i).val, fun a b hab => e.symm.injective (Subtype.ext hab),
    fun v => ⟨fun hv => ⟨e ⟨v, hv⟩, by simp⟩, by rintro ⟨i, rfl⟩; exact (e.symm i).property⟩⟩

/-- **The icosahedral two-ball from triangulation data.** On a triangulation, a hole whose
link is listed in rotation order, whose five link vertices have degree five, and through
which no separating triangle passes, has an `IcoBall`. -/
theorem icoBall_of_triangulated (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    (hlink : ∀ i, M.graph.degree (L.port i) = 5) (hsep : M.NoSeparatingTriangleAt h) :
    ∃ w : Fin 5 → Fin n, IcoBall M.graph h L w := by
  classical
  have i41 : ∀ t : Fin 5, t + 4 + 1 = t := by decide
  have i14 : ∀ t : Fin 5, t + 1 + 4 = t := by decide
  have i11 : ∀ t : Fin 5, t + 1 + 1 = t + 2 := by decide
  have R : ∀ t, Nx M h (L.port t) (L.port (t+1)) := fun t => nx_of_dart (rot t)
  -- around the face (h, x_t, x_{t+1})
  have A1 : ∀ t, Nx M (L.port (t+1)) h (L.port t) := fun t => (nx_tri htri (R t)).1
  have A2 : ∀ t, Nx M (L.port t) (L.port (t+1)) h := fun t => (nx_tri htri (R t)).2
  let w : Fin 5 → Fin n := fun t =>
    (M.rotation.next ⟨(L.port (t+1), L.port t), (ring t).symm⟩).snd
  have W : ∀ t, Nx M (L.port (t+1)) (L.port t) (w t) := fun t => ⟨(ring t).symm, rfl⟩
  have B2 : ∀ t, Nx M (L.port t) (w t) (L.port (t+1)) := fun t => (nx_tri htri (W t)).2
  -- the rotation at x_t
  have A1' : ∀ t, Nx M (L.port t) h (L.port (t+4)) := fun t => by
    have := A1 (t+4); rwa [i41] at this
  have W' : ∀ t, Nx M (L.port t) (L.port (t+4)) (w (t+4)) := fun t => by
    have := W (t+4); rwa [i41] at this
  have C : ∀ t, Nx M (L.port t) (w (t+4)) (w t) ∧
      (w t ≠ L.port (t+1) ∧ w t ≠ h ∧ w t ≠ L.port (t+4) ∧ w t ≠ w (t+4) ∧
        L.port (t+1) ≠ h ∧ L.port (t+1) ≠ L.port (t+4) ∧ L.port (t+1) ≠ w (t+4) ∧
        h ≠ L.port (t+4) ∧ h ≠ w (t+4) ∧ L.port (t+4) ≠ w (t+4)) ∧
      ∀ u, M.Adj (L.port t) u → u = w t ∨ u = L.port (t+1) ∨ u = h ∨ u = L.port (t+4) ∨
        u = w (t+4) :=
    fun t => chain5 (hlink t) (B2 t) (A2 t) (A1' t) (W' t)
  have nd : ∀ t, w t ≠ L.port (t+1) ∧ w t ≠ h ∧ w t ≠ L.port (t+4) := fun t =>
    ⟨(C t).2.1.1, (C t).2.1.2.1, (C t).2.1.2.2.1⟩
  have nd2 : ∀ t, w t ≠ L.port (t+2) := by
    intro t e
    have := (C (t+1)).2.1.2.2.2.2.2.2.1
    rw [i14, i11] at this
    exact this e.symm
  have adjw : ∀ t, M.Adj (L.port t) (w t) := fun t => nx_adj_left (B2 t)
  refine ⟨w, ⟨fun t u => ⟨fun hu => ?_, fun hu => ?_⟩, fun t => ?_, fun t i => ?_,
    fun t => (nd t).2.1⟩⟩
  · rcases (C t).2.2 u hu with e | e | e | e | e
    · exact Or.inr (Or.inr (Or.inr (Or.inr e)))
    · exact Or.inr (Or.inr (Or.inl e))
    · exact Or.inl e
    · exact Or.inr (Or.inl e)
    · exact Or.inr (Or.inr (Or.inr (Or.inl e)))
  · rcases hu with rfl | rfl | rfl | rfl | rfl
    · exact (port_adj M.graph L t).symm
    · exact nx_adj_right (A1' t)
    · exact ring t
    · exact nx_adj_right (W' t)
    · exact adjw t
  · -- the ring edge w_t w_{t+1}, from the rotation at x_{t+1}
    have h1 := (C (t+1)).1
    rw [i14] at h1
    exact (nx_adj_right (nx_tri htri h1).1).symm
  · obtain ⟨j, rfl⟩ : ∃ j, i = t + j := ⟨i - t, by abel⟩
    intro e
    have hj : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 := by clear e; revert j; decide
    rcases hj with rfl | rfl | rfl | rfl | rfl
    · rw [add_zero] at e
      exact (adjw t).ne e.symm
    · exact (nd t).1 e
    · exact nd2 t e
    · -- a chord x_t x_{t+3} would give a separating triangle through h
      have hc : M.Adj (L.port t) (L.port (t+3)) := e ▸ adjw t
      have n13 : ∀ s : Fin 5, s + 1 ≠ s + 3 := by decide
      have n31 : ∀ s : Fin 5, s + 3 + 1 ≠ s := by decide
      rcases hsep _ _ (port_adj M.graph L t) (port_adj M.graph L (t+3)) hc with r | r
      · rw [rot t] at r
        exact n13 t (L.injective
          (show L.port (t+1) = L.port (t+3) from congrArg (fun d : M.Dart => d.snd) r))
      · rw [rot (t+3)] at r
        exact n31 t (L.injective
          (show L.port (t+3+1) = L.port t from congrArg (fun d : M.Dart => d.snd) r))
    · exact (nd t).2.2 e

/-- **Theorem H on a triangulation.** Let `M` be a spherical triangulation and `h` a vertex of
degree five whose five neighbours all have degree five, with no separating triangle through
`h`. Then every proper four-colouring of `M - h` reaches a filled hole by at most three
whole-component Kempe swaps. -/
theorem theorem_H (htri : M.Triangulated) {h : Fin n} (hdeg : M.graph.degree h = 5)
    (hlink : ∀ u, M.Adj h u → M.graph.degree u = 5) (hsep : M.NoSeparatingTriangleAt h)
    {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) : PureFill M.graph h c 3 := by
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri (M.linkOfDegree hdeg)
  obtain ⟨w, B⟩ := M.icoBall_of_triangulated htri L ring rot
    (fun i => hlink _ (port_adj M.graph L i)) hsep
  exact M.ico_fill L B rot hc

end SimpleGraph.SphericalMap

/-! ## Non-vacuity: the hypotheses hold on the icosahedron -/

namespace SimpleGraph.Icosahedron
open VacancySlide VacancyShortFill SphericalMap

theorem sphericalMap_triangulated : sphericalMap.Triangulated :=
  fun _ => sphericalMap_triangular _

theorem noSeparatingTriangle_zero : sphericalMap.NoSeparatingTriangleAt 0 := by
  have h : ∀ u v : Fin 12, graph.Adj 0 u → graph.Adj 0 v → graph.Adj u v →
      nextTable 0 u = v ∨ nextTable 0 v = u := by decide
  intro u v hu hv huv
  rcases h u v hu hv huv with e | e
  · left; apply Dart.ext; exact Prod.ext rfl e
  · right; apply Dart.ext; exact Prod.ext rfl e

/-- A colouring of the icosahedron minus vertex `0` whose link uses all four colours. -/
def sampleColouring : Fin 12 → Fin 4 := ![0, 0, 1, 0, 1, 2, 3, 1, 2, 3, 2, 3]

theorem sampleColouring_proper : ProperOff sphericalMap.graph 0 sampleColouring := by
  have h : ∀ u v : Fin 12, graph.Adj u v → u ≠ 0 → v ≠ 0 →
      sampleColouring u ≠ sampleColouring v := by decide
  exact fun u v e hu hv => h u v e hu hv

theorem sampleColouring_unfilled : ¬ Target sphericalMap.graph 0 sampleColouring := by
  rintro ⟨x, hx⟩
  have h : ∀ x : Fin 4, ∃ v, graph.Adj 0 v ∧ sampleColouring v = x := by decide
  obtain ⟨v, hv, e⟩ := h x
  exact hx hv e

/-- **Non-vacuity of Theorem H.** All hypotheses of `theorem_H` hold at vertex `0` of the
icosahedron, for a colouring that is not already filled. -/
theorem theorem_H_icosahedron : PureFill sphericalMap.graph 0 sampleColouring 3 :=
  sphericalMap.theorem_H sphericalMap_triangulated (sphericalMap_degree 0)
    (fun u _ => sphericalMap_degree u) noSeparatingTriangle_zero sampleColouring_proper

end SimpleGraph.Icosahedron

/-! ## Theorem HP: four link vertices of degree five, one free -/

namespace SimpleGraph.VacancyIcosahedral

set_option synthInstance.maxHeartbeats 400000 in
set_option synthInstance.maxSize 4096 in
/-- The doubly locked ring words at a hole with one free port `k`: `R1`, `R3`, or a word
killed by B-starvation (`k ≠ 0`) or F-starvation (`k ≠ 2`). -/
lemma hp_cases : ∀ (k : Fin 5) (a0 a1 a2 a3 a4 : Fin 4),
    a0 ≠ 0 → a0 ≠ 1 → a1 ≠ 1 → a1 ≠ 0 → a2 ≠ 0 → a2 ≠ 2 → a3 ≠ 2 → a3 ≠ 3 →
    a4 ≠ 3 → a4 ≠ 0 →
    (k ≠ 0 → a4 ≠ a0) → (k ≠ 1 → a0 ≠ a1) → (k ≠ 2 → a1 ≠ a2) → (k ≠ 3 → a2 ≠ a3) →
    (k ≠ 4 → a3 ≠ a4) →
    (k ≠ 1 → a0 = 2 ∨ a1 = 2) → (k ≠ 1 → a0 = 3 ∨ a1 = 3) → (k ≠ 3 → a2 = 1 ∨ a3 = 1) →
    (k ≠ 4 → a3 = 1 ∨ a4 = 1) →
    (a0 = 2 ∧ a1 = 3 ∧ a2 = 1 ∧ a3 = 0 ∧ a4 = 1) ∨
    (a0 = 3 ∧ a1 = 2 ∧ a2 = 3 ∧ a3 = 1 ∧ a4 = 2) ∨
    (k ≠ 0 ∧ a0 = 3 ∧ a4 = 1) ∨ (k ≠ 2 ∧ a1 = 2 ∧ a2 = 1) := by
  decide +kernel

/-- Colour renaming after an F move (`0,3,1,2 ↦ 0,1,2,3`). -/
def renF : Fin 4 ≃ Fin 4 := ⟨![0, 2, 3, 1], ![0, 3, 1, 2], by decide, by decide⟩
/-- Colour renaming after a B move (`0,2,3,1 ↦ 0,1,2,3`). -/
def renB : Fin 4 ≃ Fin 4 := ⟨![0, 3, 1, 2], ![0, 2, 3, 1], by decide, by decide⟩
/-- The ring word `R1 = (g,d,b,a,b)`. -/
def wR1 : Fin 5 → Fin 4 := ![2, 3, 1, 0, 1]
/-- The ring word `R3 = (d,g,d,b,g)`. -/
def wR3 : Fin 5 → Fin 4 := ![3, 2, 3, 1, 2]

end SimpleGraph.VacancyIcosahedral

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral
variable {n : Nat} (M : SphericalMap n)

/-- The two-ball of a hole whose link vertices other than `L.port k` have degree five. -/
structure HPBall (h : Fin n) (L : FiveLink M.graph h) (w : Fin 5 → Fin n) (k : Fin 5) :
    Prop where
  nbr : ∀ t, t ≠ k → ∀ u, M.Adj (L.port t) u ↔
    u = h ∨ u = L.port (t+4) ∨ u = L.port (t+1) ∨ u = w (t+4) ∨ u = w t
  adjl : ∀ t, M.Adj (L.port t) (w t)
  adjr : ∀ t, M.Adj (L.port (t+1)) (w t)
  ringP : ∀ t, M.Adj (L.port t) (L.port (t+1))
  ring : ∀ t, t ≠ k → M.Adj (w (t+4)) (w t)
  off : ∀ t i, w t ≠ L.port i
  offh : ∀ t, w t ≠ h
  rot : ∀ i : Fin 5, M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
    ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩

variable {M}

theorem HPBall.shift {h : Fin n} {L : FiveLink M.graph h} {w : Fin 5 → Fin n} {k : Fin 5}
    (B : HPBall M h L w k) (s : Fin 5) :
    HPBall M h (FiveLink.shift M L s) (fun t => w (t+s)) (k - s) := by
  have c4 : ∀ t : Fin 5, t + 4 + s = t + s + 4 := fun t => add_right_comm _ _ _
  have c1 : ∀ t : Fin 5, t + 1 + s = t + s + 1 := fun t => add_right_comm _ _ _
  have hk : ∀ t : Fin 5, t ≠ k - s → t + s ≠ k := fun t ht e => ht (by rw [← e]; abel)
  refine ⟨fun t ht u => ?_, fun t => B.adjl (t+s), fun t => ?_, fun t => ?_, fun t ht => ?_,
    fun t i => B.off _ _, fun t => B.offh _, fun i => ?_⟩
  · change M.Adj (L.port (t + s)) u ↔ u = h ∨ u = L.port (t + 4 + s) ∨
      u = L.port (t + 1 + s) ∨ u = w (t + 4 + s) ∨ u = w (t + s)
    rw [c4, c1]; exact B.nbr (t+s) (hk t ht) u
  · change M.Adj (L.port (t + 1 + s)) (w (t + s)); rw [c1]; exact B.adjr _
  · change M.Adj (L.port (t + s)) (L.port (t + 1 + s)); rw [c1]; exact B.ringP _
  · change M.Adj (w (t + 4 + s)) (w (t + s)); rw [c4]; exact B.ring _ (hk t ht)
  · have key : ∀ j j' : Fin 5, j' = j + 1 →
        M.rotation.next ⟨(h, L.port j), port_adj M.graph L j⟩ =
          ⟨(h, L.port j'), port_adj M.graph L j'⟩ := by
      rintro j j' rfl; exact B.rot j
    exact key (i + s) (i + 1 + s) (by abel)

section Moves
variable {h : Fin n} {L : FiveLink M.graph h} {w : Fin 5 → Fin n} {k : Fin 5}
  {c : Fin n → Fin 4}

/-- F on `R1`: the image, read in the frame shifted by three, has ring word `R3`. -/
theorem moveF_R1 (B : HPBall M h L w k) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR1 t)
    (lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)) :
    ∃ d, KempeStep M.graph h c d ∧ ProperOff M.graph h d ∧
      Pattern M.graph (FiveLink.shift M L 3) (fun v => renF (d v)) ∧
      ∀ t, renF (d (w (t+3))) = wR3 t := by
  classical
  have sep := vacancy_alternation M L pat B.rot
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  have e0 : c (w 0) = 2 := by simpa [wR1] using ring 0
  have e1 : c (w 1) = 3 := by simpa [wR1] using ring 1
  have e2 : c (w 2) = 1 := by simpa [wR1] using ring 2
  have e3 : c (w 3) = 0 := by simpa [wR1] using ring 3
  have e4 : c (w 4) = 1 := by simpa [wR1] using ring 4
  obtain ⟨K, hK, hKm⟩ : ∃ K : Set (Fin n), Whole M.graph h c 0 2 K ∧
      ∀ v, v ∈ K ↔ (pairGraph M.graph h c 0 2).Reachable (L.port 2) v :=
    ⟨_, whole_component M.graph h c 0 2 (L.port 2) ⟨pn 2, Or.inl c2⟩, fun _ => Iff.rfl⟩
  have x2K : L.port 2 ∈ K := (hKm _).mpr Reachable.rfl
  have x0K : L.port 0 ∉ K := fun hin => (sep.right lock2).1 ((hKm _).mp hin).symm
  have x3K : L.port 3 ∈ K :=
    whole_closed M.graph hK x2K (by simpa using B.ringP 2) ⟨pn 3, Or.inr c3⟩
  have w0K : w 0 ∉ K := fun hin =>
    x0K (whole_closed M.graph hK hin (B.adjl 0).symm ⟨pn 0, Or.inl c0⟩)
  have w3K : w 3 ∈ K := whole_closed M.graph hK x3K (B.adjl 3) ⟨B.offh 3, Or.inl e3⟩
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
  refine ⟨d, ⟨0, 2, K, by decide, hK, rfl⟩, properOff_swap M.graph hc hK, fun i => ?_,
    fun t => ?_⟩
  · change renF (d (L.port (i + 3))) = gapWord i
    fin_cases i <;> simp [d0, d1, d2, d3, d4, renF, gapWord]
  · fin_cases t <;> simp [dw0, dw1, dw2, dw3, dw4, renF, wR3]

/-- F on `R3`: the image, read in the frame shifted by three, has ring word `R1`. -/
theorem moveF_R3 (B : HPBall M h L w k) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR3 t)
    (lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)) :
    ∃ d, KempeStep M.graph h c d ∧ ProperOff M.graph h d ∧
      Pattern M.graph (FiveLink.shift M L 3) (fun v => renF (d v)) ∧
      ∀ t, renF (d (w (t+3))) = wR1 t := by
  classical
  have sep := vacancy_alternation M L pat B.rot
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  have e0 : c (w 0) = 3 := by simpa [wR3] using ring 0
  have e1 : c (w 1) = 2 := by simpa [wR3] using ring 1
  have e2 : c (w 2) = 3 := by simpa [wR3] using ring 2
  have e3 : c (w 3) = 1 := by simpa [wR3] using ring 3
  have e4 : c (w 4) = 2 := by simpa [wR3] using ring 4
  obtain ⟨K, hK, hKm⟩ : ∃ K : Set (Fin n), Whole M.graph h c 0 2 K ∧
      ∀ v, v ∈ K ↔ (pairGraph M.graph h c 0 2).Reachable (L.port 2) v :=
    ⟨_, whole_component M.graph h c 0 2 (L.port 2) ⟨pn 2, Or.inl c2⟩, fun _ => Iff.rfl⟩
  have x2K : L.port 2 ∈ K := (hKm _).mpr Reachable.rfl
  have x0K : L.port 0 ∉ K := fun hin => (sep.right lock2).1 ((hKm _).mp hin).symm
  have x3K : L.port 3 ∈ K :=
    whole_closed M.graph hK x2K (by simpa using B.ringP 2) ⟨pn 3, Or.inr c3⟩
  have w1K : w 1 ∈ K :=
    whole_closed M.graph hK x2K (by simpa using B.adjr 1) ⟨B.offh 1, Or.inr e1⟩
  have w4K : w 4 ∉ K := fun hin =>
    x0K (whole_closed M.graph hK hin (by simpa using (B.adjr 4).symm) ⟨pn 0, Or.inl c0⟩)
  set d := swap c 0 2 K with hd
  have d0 : d (L.port 0) = 0 := by rw [hd, swap_out x0K, c0]
  have d1 : d (L.port 1) = 1 := by
    rw [hd, swap_other (by rw [c1]; decide) (by rw [c1]; decide), c1]
  have d2 : d (L.port 2) = 2 := by rw [hd, swap_in x2K, c2]; decide
  have d3 : d (L.port 3) = 0 := by rw [hd, swap_in x3K, c3]; decide
  have d4 : d (L.port 4) = 3 := by
    rw [hd, swap_other (by rw [c4]; decide) (by rw [c4]; decide), c4]
  have dw0 : d (w 0) = 3 := by
    rw [hd, swap_other (by rw [e0]; decide) (by rw [e0]; decide), e0]
  have dw1 : d (w 1) = 0 := by rw [hd, swap_in w1K, e1]; decide
  have dw2 : d (w 2) = 3 := by
    rw [hd, swap_other (by rw [e2]; decide) (by rw [e2]; decide), e2]
  have dw3 : d (w 3) = 1 := by
    rw [hd, swap_other (by rw [e3]; decide) (by rw [e3]; decide), e3]
  have dw4 : d (w 4) = 2 := by rw [hd, swap_out w4K, e4]
  refine ⟨d, ⟨0, 2, K, by decide, hK, rfl⟩, properOff_swap M.graph hc hK, fun i => ?_,
    fun t => ?_⟩
  · change renF (d (L.port (i + 3))) = gapWord i
    fin_cases i <;> simp [d0, d1, d2, d3, d4, renF, gapWord]
  · fin_cases t <;> simp [dw0, dw1, dw2, dw3, dw4, renF, wR1]

/-- B on `R1`: the image, read in the frame shifted by two, has ring word `R3`. -/
theorem moveB_R1 (B : HPBall M h L w k) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR1 t)
    (lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)) :
    ∃ d, KempeStep M.graph h c d ∧ ProperOff M.graph h d ∧
      Pattern M.graph (FiveLink.shift M L 2) (fun v => renB (d v)) ∧
      ∀ t, renB (d (w (t+2))) = wR3 t := by
  classical
  have sep := vacancy_alternation M L pat B.rot
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  have e0 : c (w 0) = 2 := by simpa [wR1] using ring 0
  have e1 : c (w 1) = 3 := by simpa [wR1] using ring 1
  have e2 : c (w 2) = 1 := by simpa [wR1] using ring 2
  have e3 : c (w 3) = 0 := by simpa [wR1] using ring 3
  have e4 : c (w 4) = 1 := by simpa [wR1] using ring 4
  obtain ⟨K, hK, hKm⟩ : ∃ K : Set (Fin n), Whole M.graph h c 0 3 K ∧
      ∀ v, v ∈ K ↔ (pairGraph M.graph h c 0 3).Reachable (L.port 0) v :=
    ⟨_, whole_component M.graph h c 0 3 (L.port 0) ⟨pn 0, Or.inl c0⟩, fun _ => Iff.rfl⟩
  have x0K : L.port 0 ∈ K := (hKm _).mpr Reachable.rfl
  have x2K : L.port 2 ∉ K := fun hin => (sep.left lock1).1 ((hKm _).mp hin).symm
  have x4K : L.port 4 ∈ K :=
    whole_closed M.graph hK x0K (by simpa using (B.ringP 4).symm) ⟨pn 4, Or.inr c4⟩
  have w3K : w 3 ∈ K :=
    whole_closed M.graph hK x4K (by simpa using B.adjr 3) ⟨B.offh 3, Or.inl e3⟩
  have w1K : w 1 ∉ K := fun hin =>
    x2K (whole_closed M.graph hK hin (by simpa using (B.adjr 1).symm) ⟨pn 2, Or.inl c2⟩)
  set d := swap c 0 3 K with hd
  have d0 : d (L.port 0) = 3 := by rw [hd, swap_in x0K, c0]; decide
  have d1 : d (L.port 1) = 1 := by
    rw [hd, swap_other (by rw [c1]; decide) (by rw [c1]; decide), c1]
  have d2 : d (L.port 2) = 0 := by rw [hd, swap_out x2K, c2]
  have d3 : d (L.port 3) = 2 := by
    rw [hd, swap_other (by rw [c3]; decide) (by rw [c3]; decide), c3]
  have d4 : d (L.port 4) = 0 := by rw [hd, swap_in x4K, c4]; decide
  have dw0 : d (w 0) = 2 := by
    rw [hd, swap_other (by rw [e0]; decide) (by rw [e0]; decide), e0]
  have dw1 : d (w 1) = 3 := by rw [hd, swap_out w1K, e1]
  have dw2 : d (w 2) = 1 := by
    rw [hd, swap_other (by rw [e2]; decide) (by rw [e2]; decide), e2]
  have dw3 : d (w 3) = 3 := by rw [hd, swap_in w3K, e3]; decide
  have dw4 : d (w 4) = 1 := by
    rw [hd, swap_other (by rw [e4]; decide) (by rw [e4]; decide), e4]
  refine ⟨d, ⟨0, 3, K, by decide, hK, rfl⟩, properOff_swap M.graph hc hK, fun i => ?_,
    fun t => ?_⟩
  · change renB (d (L.port (i + 2))) = gapWord i
    fin_cases i <;> simp [d0, d1, d2, d3, d4, renB, gapWord]
  · fin_cases t <;> simp [dw0, dw1, dw2, dw3, dw4, renB, wR3]

/-- B on `R3`: the image, read in the frame shifted by two, has ring word `R1`. -/
theorem moveB_R3 (B : HPBall M h L w k) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR3 t)
    (lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)) :
    ∃ d, KempeStep M.graph h c d ∧ ProperOff M.graph h d ∧
      Pattern M.graph (FiveLink.shift M L 2) (fun v => renB (d v)) ∧
      ∀ t, renB (d (w (t+2))) = wR1 t := by
  classical
  have sep := vacancy_alternation M L pat B.rot
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  have e0 : c (w 0) = 3 := by simpa [wR3] using ring 0
  have e1 : c (w 1) = 2 := by simpa [wR3] using ring 1
  have e2 : c (w 2) = 3 := by simpa [wR3] using ring 2
  have e3 : c (w 3) = 1 := by simpa [wR3] using ring 3
  have e4 : c (w 4) = 2 := by simpa [wR3] using ring 4
  obtain ⟨K, hK, hKm⟩ : ∃ K : Set (Fin n), Whole M.graph h c 0 3 K ∧
      ∀ v, v ∈ K ↔ (pairGraph M.graph h c 0 3).Reachable (L.port 0) v :=
    ⟨_, whole_component M.graph h c 0 3 (L.port 0) ⟨pn 0, Or.inl c0⟩, fun _ => Iff.rfl⟩
  have x0K : L.port 0 ∈ K := (hKm _).mpr Reachable.rfl
  have x2K : L.port 2 ∉ K := fun hin => (sep.left lock1).1 ((hKm _).mp hin).symm
  have x4K : L.port 4 ∈ K :=
    whole_closed M.graph hK x0K (by simpa using (B.ringP 4).symm) ⟨pn 4, Or.inr c4⟩
  have w0K : w 0 ∈ K := whole_closed M.graph hK x0K (B.adjl 0) ⟨B.offh 0, Or.inr e0⟩
  have w2K : w 2 ∉ K := fun hin =>
    x2K (whole_closed M.graph hK hin (B.adjl 2).symm ⟨pn 2, Or.inl c2⟩)
  set d := swap c 0 3 K with hd
  have d0 : d (L.port 0) = 3 := by rw [hd, swap_in x0K, c0]; decide
  have d1 : d (L.port 1) = 1 := by
    rw [hd, swap_other (by rw [c1]; decide) (by rw [c1]; decide), c1]
  have d2 : d (L.port 2) = 0 := by rw [hd, swap_out x2K, c2]
  have d3 : d (L.port 3) = 2 := by
    rw [hd, swap_other (by rw [c3]; decide) (by rw [c3]; decide), c3]
  have d4 : d (L.port 4) = 0 := by rw [hd, swap_in x4K, c4]; decide
  have dw0 : d (w 0) = 0 := by rw [hd, swap_in w0K, e0]; decide
  have dw1 : d (w 1) = 2 := by
    rw [hd, swap_other (by rw [e1]; decide) (by rw [e1]; decide), e1]
  have dw2 : d (w 2) = 3 := by rw [hd, swap_out w2K, e2]
  have dw3 : d (w 3) = 1 := by
    rw [hd, swap_other (by rw [e3]; decide) (by rw [e3]; decide), e3]
  have dw4 : d (w 4) = 2 := by
    rw [hd, swap_other (by rw [e4]; decide) (by rw [e4]; decide), e4]
  refine ⟨d, ⟨0, 3, K, by decide, hK, rfl⟩, properOff_swap M.graph hc hK, fun i => ?_,
    fun t => ?_⟩
  · change renB (d (L.port (i + 2))) = gapWord i
    fin_cases i <;> simp [d0, d1, d2, d3, d4, renB, gapWord]
  · fin_cases t <;> simp [dw0, dw1, dw2, dw3, dw4, renB, wR1]

end Moves

section Chains
variable {h : Fin n} {L : FiveLink M.graph h} {w : Fin 5 → Fin n} {k : Fin 5}
  {c : Fin n → Fin 4}

lemma after_move {d : Fin n → Fin 4} {σ : Fin 4 ≃ Fin 4} {b : Nat}
    (step : KempeStep M.graph h c d) (f : PureFill M.graph h (fun v => σ (d v)) b) :
    PureFill M.graph h c (b+1) := by
  have f' := pureFill_rename M.graph σ.symm f
  simp only [Equiv.symm_apply_apply] at f'
  exact prepend M.graph step f'

/-- B-starvation: if `x_0` has degree five and outer colours `3, 1`, then B, then a fill. -/
theorem killB (B : HPBall M h L w k) (hk : k ≠ 0) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (e0 : c (w 0) = 3) (e4 : c (w 4) = 1)
    (lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)) :
    PureFill M.graph h c 2 := by
  classical
  have sep := vacancy_alternation M L pat B.rot
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have pne : ∀ i j, i ≠ j → L.port i ≠ L.port j := fun i j hij e => hij (L.injective e)
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  obtain ⟨K, hK, hKm⟩ : ∃ K : Set (Fin n), Whole M.graph h c 0 3 K ∧
      ∀ v, v ∈ K ↔ (pairGraph M.graph h c 0 3).Reachable (L.port 0) v :=
    ⟨_, whole_component M.graph h c 0 3 (L.port 0) ⟨pn 0, Or.inl c0⟩, fun _ => Iff.rfl⟩
  have x0K : L.port 0 ∈ K := (hKm _).mpr Reachable.rfl
  have x2K : L.port 2 ∉ K := fun hin => (sep.left lock1).1 ((hKm _).mp hin).symm
  have x4K : L.port 4 ∈ K :=
    whole_closed M.graph hK x0K (by simpa using (B.ringP 4).symm) ⟨pn 4, Or.inr c4⟩
  have w0K : w 0 ∈ K := whole_closed M.graph hK x0K (B.adjl 0) ⟨B.offh 0, Or.inr e0⟩
  set d := swap c 0 3 K with hd
  have d0 : d (L.port 0) = 3 := by rw [hd, swap_in x0K, c0]; decide
  have d1 : d (L.port 1) = 1 := by
    rw [hd, swap_other (by rw [c1]; decide) (by rw [c1]; decide), c1]
  have d2 : d (L.port 2) = 0 := by rw [hd, swap_out x2K, c2]
  have d3 : d (L.port 3) = 2 := by
    rw [hd, swap_other (by rw [c3]; decide) (by rw [c3]; decide), c3]
  have d4 : d (L.port 4) = 0 := by rw [hd, swap_in x4K, c4]; decide
  have dw0 : d (w 0) = 0 := by rw [hd, swap_in w0K, e0]; decide
  have dw4 : d (w 4) = 1 := by
    rw [hd, swap_other (by rw [e4]; decide) (by rw [e4]; decide), e4]
  have step : KempeStep M.graph h c d := ⟨0, 3, K, by decide, hK, rfl⟩
  have hd' : ProperOff M.graph h d := properOff_swap M.graph hc hK
  have fill : PureFill M.graph h d 1 := by
    apply fill_of_isolated M.graph hd' (port_adj M.graph L 3) (t := L.port 0) (rho := 3)
    · intro y ey eq
      obtain ⟨i, rfl⟩ := (L.neighbours y).mp ey
      fin_cases i <;> simp [d0, d1, d2, d3, d4] at eq ⊢
    · rw [d3]; decide
    · exact pne 3 0 (by decide)
    · intro v ev eq
      obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
      fin_cases i <;> simp [d0, d1, d2, d3, d4] at eq ⊢
    · intro z hz
      have hb := hz.2.2.2
      rw [d3] at hb
      rcases (B.nbr 0 (Ne.symm hk) z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl hz.2.2.1
      · simp [d4] at hb
      · simp [d1] at hb
      · simp [dw4] at hb
      · simp [dw0] at hb
  exact prepend M.graph step fill

/-- F-starvation: if `x_2` has degree five and outer colours `2, 1`, then F, then a fill. -/
theorem killF (B : HPBall M h L w k) (hk : k ≠ 2) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (e1 : c (w 1) = 2) (e2 : c (w 2) = 1)
    (lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)) :
    PureFill M.graph h c 2 := by
  classical
  have sep := vacancy_alternation M L pat B.rot
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have pne : ∀ i j, i ≠ j → L.port i ≠ L.port j := fun i j hij e => hij (L.injective e)
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  obtain ⟨K, hK, hKm⟩ : ∃ K : Set (Fin n), Whole M.graph h c 0 2 K ∧
      ∀ v, v ∈ K ↔ (pairGraph M.graph h c 0 2).Reachable (L.port 2) v :=
    ⟨_, whole_component M.graph h c 0 2 (L.port 2) ⟨pn 2, Or.inl c2⟩, fun _ => Iff.rfl⟩
  have x2K : L.port 2 ∈ K := (hKm _).mpr Reachable.rfl
  have x0K : L.port 0 ∉ K := fun hin => (sep.right lock2).1 ((hKm _).mp hin).symm
  have x3K : L.port 3 ∈ K :=
    whole_closed M.graph hK x2K (by simpa using B.ringP 2) ⟨pn 3, Or.inr c3⟩
  have w1K : w 1 ∈ K :=
    whole_closed M.graph hK x2K (by simpa using B.adjr 1) ⟨B.offh 1, Or.inr e1⟩
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
  have step : KempeStep M.graph h c d := ⟨0, 2, K, by decide, hK, rfl⟩
  have hd' : ProperOff M.graph h d := properOff_swap M.graph hc hK
  have fill : PureFill M.graph h d 1 := by
    apply fill_of_isolated M.graph hd' (port_adj M.graph L 4) (t := L.port 2) (rho := 2)
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
      rcases (B.nbr 2 (Ne.symm hk) z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl hz.2.2.1
      · simp [d1] at hb
      · simp [d3] at hb
      · simp [dw1] at hb
      · simp [dw2] at hb
  exact prepend M.graph step fill

/-- `R3` with the free port a singleton (`k = 3, 4`): the three-vertex AB swap, then a fill. -/
theorem chainR3_34 (B : HPBall M h L w k) (hk : k = 3 ∨ k = 4) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR3 t) : PureFill M.graph h c 2 := by
  classical
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have pne : ∀ i j, i ≠ j → L.port i ≠ L.port j := fun i j hij e => hij (L.injective e)
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  have e0 : c (w 0) = 3 := by simpa [wR3] using ring 0
  have e1 : c (w 1) = 2 := by simpa [wR3] using ring 1
  have e2 : c (w 2) = 3 := by simpa [wR3] using ring 2
  have e3 : c (w 3) = 1 := by simpa [wR3] using ring 3
  have e4 : c (w 4) = 2 := by simpa [wR3] using ring 4
  have k0 : (0 : Fin 5) ≠ k := by rcases hk with rfl | rfl <;> decide
  have k1 : (1 : Fin 5) ≠ k := by rcases hk with rfl | rfl <;> decide
  have k2 : (2 : Fin 5) ≠ k := by rcases hk with rfl | rfl <;> decide
  obtain ⟨J, hJ, hJm⟩ : ∃ J : Set (Fin n), Whole M.graph h c 0 1 J ∧
      ∀ v, v ∈ J ↔ (pairGraph M.graph h c 0 1).Reachable (L.port 1) v :=
    ⟨_, whole_component M.graph h c 0 1 (L.port 1) ⟨pn 1, Or.inr c1⟩, fun _ => Iff.rfl⟩
  have Jsub : ∀ v, v ∈ J → v = L.port 0 ∨ v = L.port 1 ∨ v = L.port 2 := by
    intro v hv
    refine reachable_invariant (H := pairGraph M.graph h c 0 1)
      (P := fun v => v = L.port 0 ∨ v = L.port 1 ∨ v = L.port 2) ?_
      (Or.inr (Or.inl rfl)) ((hJm v).mp hv)
    intro a b e ha
    have hb := e.2.2.2
    rcases ha with rfl | rfl | rfl
    · rcases (B.nbr 0 k0 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl e.2.2.1
      · simp [c4] at hb
      · simp
      · simp [e4] at hb
      · simp [e0] at hb
    · rcases (B.nbr 1 k1 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl e.2.2.1
      · simp
      · simp
      · simp [e0] at hb
      · simp [e1] at hb
    · rcases (B.nbr 2 k2 b).mp e.1 with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl e.2.2.1
      · simp
      · simp [c3] at hb
      · simp [e1] at hb
      · simp [e2] at hb
  have x1J : L.port 1 ∈ J := (hJm _).mpr Reachable.rfl
  have x0J : L.port 0 ∈ J :=
    whole_closed M.graph hJ x1J (by simpa using (B.ringP 0).symm) ⟨pn 0, Or.inl c0⟩
  have x2J : L.port 2 ∈ J :=
    whole_closed M.graph hJ x1J (by simpa using B.ringP 1) ⟨pn 2, Or.inl c2⟩
  have x3J : L.port 3 ∉ J := fun hin => by
    rcases Jsub _ hin with e | e | e <;> exact pne _ _ (by decide) e
  have x4J : L.port 4 ∉ J := fun hin => by
    rcases Jsub _ hin with e | e | e <;> exact pne _ _ (by decide) e
  have wJ : ∀ t, w t ∉ J := fun t hin => by
    rcases Jsub _ hin with e | e | e <;> exact B.off t _ e
  set f := swap c 0 1 J with hf
  have f0 : f (L.port 0) = 1 := by rw [hf, swap_in x0J, c0]; decide
  have f1 : f (L.port 1) = 0 := by rw [hf, swap_in x1J, c1]; decide
  have f2 : f (L.port 2) = 1 := by rw [hf, swap_in x2J, c2]; decide
  have f3 : f (L.port 3) = 2 := by rw [hf, swap_out x3J, c3]
  have f4 : f (L.port 4) = 3 := by rw [hf, swap_out x4J, c4]
  have fw2 : f (w 2) = 3 := by rw [hf, swap_out (wJ 2), e2]
  have fw3 : f (w 3) = 1 := by rw [hf, swap_out (wJ 3), e3]
  have fw4 : f (w 4) = 2 := by rw [hf, swap_out (wJ 4), e4]
  have step : KempeStep M.graph h c f := ⟨0, 1, J, by decide, hJ, rfl⟩
  have hf' : ProperOff M.graph h f := properOff_swap M.graph hc hJ
  have uniq : UniqueAt M.graph h (L.port 1) f := by
    intro y ey eq
    obtain ⟨i, rfl⟩ := (L.neighbours y).mp ey
    fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
  rcases hk with rfl | rfl
  · -- k = 3: isolate x_4 in the {0,3} pair graph
    have fill : PureFill M.graph h f 1 := by
      apply fill_of_isolated M.graph hf' (port_adj M.graph L 1) (t := L.port 4) (rho := 3) uniq
      · rw [f1]; decide
      · exact pne 1 4 (by decide)
      · intro v ev eq
        obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
        fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
      · intro z hz
        have hb := hz.2.2.2
        rw [f1] at hb
        rcases (B.nbr 4 (by decide) z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hz.2.2.1
        · simp [f3] at hb
        · simp [f0] at hb
        · simp [fw3] at hb
        · simp [fw4] at hb
    exact prepend M.graph step fill
  · -- k = 4: isolate x_3 in the {0,2} pair graph
    have fill : PureFill M.graph h f 1 := by
      apply fill_of_isolated M.graph hf' (port_adj M.graph L 1) (t := L.port 3) (rho := 2) uniq
      · rw [f1]; decide
      · exact pne 1 3 (by decide)
      · intro v ev eq
        obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
        fin_cases i <;> simp [f0, f1, f2, f3, f4] at eq ⊢
      · intro z hz
        have hb := hz.2.2.2
        rw [f1] at hb
        rcases (B.nbr 3 (by decide) z).mp hz.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hz.2.2.1
        · simp [f2] at hb
        · simp [f4] at hb
        · simp [fw2] at hb
        · simp [fw3] at hb
    exact prepend M.graph step fill

theorem chainR1_012 (B : HPBall M h L w k) (hk : k = 0 ∨ k = 1 ∨ k = 2)
    (hc : ProperOff M.graph h c) (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR1 t) :
    PureFill M.graph h c 3 := by
  by_cases lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_right_missing M.graph L hc pat lock2)
  by_cases lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_left_missing M.graph L hc pat lock1)
  rcases hk with rfl | rfl | rfl
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveB_R1 B hc pat ring lock1
    exact after_move step (chainR3_34 (B.shift 2) (by decide) (properOff_rename _ renB hd)
      pat' ring')
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveF_R1 B hc pat ring lock2
    exact after_move step (chainR3_34 (B.shift 3) (by decide) (properOff_rename _ renF hd)
      pat' ring')
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveF_R1 B hc pat ring lock2
    exact after_move step (chainR3_34 (B.shift 3) (by decide) (properOff_rename _ renF hd)
      pat' ring')

theorem chainR3_02 (B : HPBall M h L w k) (hk : k = 0 ∨ k = 2)
    (hc : ProperOff M.graph h c) (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR3 t) :
    PureFill M.graph h c 4 := by
  by_cases lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_right_missing M.graph L hc pat lock2)
  by_cases lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_left_missing M.graph L hc pat lock1)
  rcases hk with rfl | rfl
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveF_R3 B hc pat ring lock2
    exact after_move step (chainR1_012 (B.shift 3) (by decide) (properOff_rename _ renF hd)
      pat' ring')
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveB_R3 B hc pat ring lock1
    exact after_move step (chainR1_012 (B.shift 2) (by decide) (properOff_rename _ renB hd)
      pat' ring')

theorem chainR1_34 (B : HPBall M h L w k) (hk : k = 3 ∨ k = 4)
    (hc : ProperOff M.graph h c) (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR1 t) :
    PureFill M.graph h c 5 := by
  by_cases lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_right_missing M.graph L hc pat lock2)
  by_cases lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_left_missing M.graph L hc pat lock1)
  rcases hk with rfl | rfl
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveF_R1 B hc pat ring lock2
    exact after_move step (chainR3_02 (B.shift 3) (by decide) (properOff_rename _ renF hd)
      pat' ring')
  · obtain ⟨d, step, hd, pat', ring'⟩ := moveB_R1 B hc pat ring lock1
    exact after_move step (chainR3_02 (B.shift 2) (by decide) (properOff_rename _ renB hd)
      pat' ring')

theorem chainR3_1 (B : HPBall M h L w k) (hk : k = 1)
    (hc : ProperOff M.graph h c) (pat : Pattern M.graph L c) (ring : ∀ t, c (w t) = wR3 t) :
    PureFill M.graph h c 6 := by
  by_cases lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_right_missing M.graph L hc pat lock2)
  subst hk
  obtain ⟨d, step, hd, pat', ring'⟩ := moveF_R3 B hc pat ring lock2
  exact after_move step (chainR1_34 (B.shift 3) (by decide) (properOff_rename _ renF hd)
    pat' ring')

/-- **Theorem HP, normalised.** With the link word `0,1,0,2,3` and one free port, every proper
colouring fills within six pure Kempe swaps. -/
theorem hp_fill_normalized (B : HPBall M h L w k) (hc : ProperOff M.graph h c)
    (pat : Pattern M.graph L c) : PureFill M.graph h c 6 := by
  classical
  have pn : ∀ i, L.port i ≠ h := fun i => (port_adj M.graph L i).ne.symm
  have pne : ∀ i j, i ≠ j → L.port i ≠ L.port j := fun i j hij e => hij (L.injective e)
  have c0 : c (L.port 0) = 0 := by simpa [gapWord] using pat 0
  have c1 : c (L.port 1) = 1 := by simpa [gapWord] using pat 1
  have c2 : c (L.port 2) = 0 := by simpa [gapWord] using pat 2
  have c3 : c (L.port 3) = 2 := by simpa [gapWord] using pat 3
  have c4 : c (L.port 4) = 3 := by simpa [gapWord] using pat 4
  by_cases lock2 : (pairGraph M.graph h c 1 3).Reachable (L.port 1) (L.port 4)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_right_missing M.graph L hc pat lock2)
  by_cases lock1 : (pairGraph M.graph h c 1 2).Reachable (L.port 1) (L.port 3)
  swap
  · exact fill_mono M.graph (by norm_num) (one_fill_of_left_missing M.graph L hc pat lock1)
  have E1 : k ≠ 1 → c (w 0) = 2 ∨ c (w 1) = 2 := fun hk => by
    obtain ⟨u, hu⟩ := first_step M.graph lock1 (pne 1 3 (by decide))
    have hcu := step_colour M.graph hc hu c1
    rcases (B.nbr 1 (Ne.symm hk) u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c0] at hcu
    · simp [c2] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have E2 : k ≠ 1 → c (w 0) = 3 ∨ c (w 1) = 3 := fun hk => by
    obtain ⟨u, hu⟩ := first_step M.graph lock2 (pne 1 4 (by decide))
    have hcu := step_colour M.graph hc hu c1
    rcases (B.nbr 1 (Ne.symm hk) u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c0] at hcu
    · simp [c2] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have E3 : k ≠ 3 → c (w 2) = 1 ∨ c (w 3) = 1 := fun hk => by
    obtain ⟨u, hu⟩ := first_step M.graph lock1.symm (pne 3 1 (by decide))
    have hcu := step_colour' M.graph hc hu c3
    rcases (B.nbr 3 (Ne.symm hk) u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c2] at hcu
    · simp [c4] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have E4 : k ≠ 4 → c (w 3) = 1 ∨ c (w 4) = 1 := fun hk => by
    obtain ⟨u, hu⟩ := first_step M.graph lock2.symm (pne 4 1 (by decide))
    have hcu := step_colour' M.graph hc hu c4
    rcases (B.nbr 4 (Ne.symm hk) u).mp hu.1 with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hu.2.2.1
    · simp [c3] at hcu
    · simp [c0] at hcu
    · left; simpa using hcu
    · right; exact hcu
  have pwl : ∀ t, c (w t) ≠ c (L.port t) := fun t => (hc (B.adjl t) (pn t) (B.offh t)).symm
  have pwr : ∀ t, c (w t) ≠ c (L.port (t+1)) := fun t => (hc (B.adjr t) (pn _) (B.offh t)).symm
  have hw : ∀ t, t ≠ k → c (w (t+4)) ≠ c (w t) := fun t ht =>
    hc (B.ring t ht) (B.offh _) (B.offh _)
  rcases hp_cases k (c (w 0)) (c (w 1)) (c (w 2)) (c (w 3)) (c (w 4))
      (by simpa [c0] using pwl 0) (by simpa [c1] using pwr 0)
      (by simpa [c1] using pwl 1) (by simpa [c2] using pwr 1)
      (by simpa [c2] using pwl 2) (by simpa [c3] using pwr 2)
      (by simpa [c3] using pwl 3) (by simpa [c4] using pwr 3)
      (by simpa [c4] using pwl 4) (by simpa [c0] using pwr 4)
      (fun hk => by simpa using hw 0 (Ne.symm hk)) (fun hk => by simpa using hw 1 (Ne.symm hk))
      (fun hk => by simpa using hw 2 (Ne.symm hk)) (fun hk => by simpa using hw 3 (Ne.symm hk))
      (fun hk => by simpa using hw 4 (Ne.symm hk))
      E1 E2 E3 E4 with
    ⟨e0, e1, e2, e3, e4⟩ | ⟨e0, e1, e2, e3, e4⟩ | ⟨hk, e0, e4⟩ | ⟨hk, e1, e2⟩
  · have ring : ∀ t, c (w t) = wR1 t := fun t => by
      fin_cases t <;> simp [wR1, e0, e1, e2, e3, e4]
    have hk : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 :=
      (show ∀ j : Fin 5, j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 by decide) k
    rcases hk with rfl | rfl | rfl | rfl | rfl
    · exact fill_mono M.graph (by norm_num) (chainR1_012 B (by decide) hc pat ring)
    · exact fill_mono M.graph (by norm_num) (chainR1_012 B (by decide) hc pat ring)
    · exact fill_mono M.graph (by norm_num) (chainR1_012 B (by decide) hc pat ring)
    · exact fill_mono M.graph (by norm_num) (chainR1_34 B (by decide) hc pat ring)
    · exact fill_mono M.graph (by norm_num) (chainR1_34 B (by decide) hc pat ring)
  · have ring : ∀ t, c (w t) = wR3 t := fun t => by
      fin_cases t <;> simp [wR3, e0, e1, e2, e3, e4]
    have hk : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 :=
      (show ∀ j : Fin 5, j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 by decide) k
    rcases hk with rfl | rfl | rfl | rfl | rfl
    · exact fill_mono M.graph (by norm_num) (chainR3_02 B (by decide) hc pat ring)
    · exact chainR3_1 B rfl hc pat ring
    · exact fill_mono M.graph (by norm_num) (chainR3_02 B (by decide) hc pat ring)
    · exact fill_mono M.graph (by norm_num) (chainR3_34 B (by decide) hc pat ring)
    · exact fill_mono M.graph (by norm_num) (chainR3_34 B (by decide) hc pat ring)
  · exact fill_mono M.graph (by norm_num) (killB B hk hc pat e0 e4 lock1)
  · exact fill_mono M.graph (by norm_num) (killF B hk hc pat e1 e2 lock2)

end Chains
end SimpleGraph.SphericalMap

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral
variable {n : Nat} (M : SphericalMap n)

/-- Theorem HP over the two-ball data, for every proper colouring. -/
theorem hp_fill {h : Fin n} {L : FiveLink M.graph h} {w : Fin 5 → Fin n} {k : Fin 5}
    (B : HPBall M h L w k) {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) :
    PureFill M.graph h c 6 := by
  classical
  by_cases surj : ∀ x : Fin 4, ∃ i, c (L.port i) = x
  · obtain ⟨k0, inj, hk⟩ := ring_normalize (fun i => c (L.port i))
      (fun i => hc (B.ringP i) (port_adj M.graph L i).ne.symm (port_adj M.graph L _).ne.symm)
      surj
    let σ : Fin 4 ≃ Fin 4 := Equiv.ofBijective _ (Finite.injective_iff_bijective.mp inj)
    have pat : Pattern M.graph (FiveLink.shift M L k0) (fun v => σ (c v)) := fun i => hk i
    have fill := hp_fill_normalized (B.shift k0) (properOff_rename _ σ hc) pat
    have := pureFill_rename M.graph σ.symm fill
    simpa using this
  · push Not at surj
    obtain ⟨x, hx⟩ := surj
    refine ⟨0, by decide, c, PurePath.nil _, x, ?_⟩
    intro v ev
    obtain ⟨i, rfl⟩ := (L.neighbours v).mp ev
    exact hx i

/-- **The two-ball of Theorem HP from triangulation data.** On a triangulation, a hole whose
link is listed in rotation order, whose link vertices other than `L.port k` have degree five,
and through which no separating triangle passes, has an `HPBall` with free port `k`. -/
theorem hpBall_of_triangulated (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    (k : Fin 5) (hlink : ∀ i, i ≠ k → M.graph.degree (L.port i) = 5)
    (hsep : M.NoSeparatingTriangleAt h) :
    ∃ w : Fin 5 → Fin n, HPBall M h L w k := by
  classical
  have i41 : ∀ t : Fin 5, t + 4 + 1 = t := by decide
  have i14 : ∀ t : Fin 5, t + 1 + 4 = t := by decide
  have R : ∀ t, Nx M h (L.port t) (L.port (t+1)) := fun t => nx_of_dart (rot t)
  have A1 : ∀ t, Nx M (L.port (t+1)) h (L.port t) := fun t => (nx_tri htri (R t)).1
  have A2 : ∀ t, Nx M (L.port t) (L.port (t+1)) h := fun t => (nx_tri htri (R t)).2
  let w : Fin 5 → Fin n := fun t =>
    (M.rotation.next ⟨(L.port (t+1), L.port t), (ring t).symm⟩).snd
  have W : ∀ t, Nx M (L.port (t+1)) (L.port t) (w t) := fun t => ⟨(ring t).symm, rfl⟩
  have B2 : ∀ t, Nx M (L.port t) (w t) (L.port (t+1)) := fun t => (nx_tri htri (W t)).2
  have A1' : ∀ t, Nx M (L.port t) h (L.port (t+4)) := fun t => by
    have := A1 (t+4); rwa [i41] at this
  have W' : ∀ t, Nx M (L.port t) (L.port (t+4)) (w (t+4)) := fun t => by
    have := W (t+4); rwa [i41] at this
  have C := fun t (ht : t ≠ k) => chain5 (hlink t ht) (B2 t) (A2 t) (A1' t) (W' t)
  have adjw : ∀ t, M.Adj (L.port t) (w t) := fun t => nx_adj_left (B2 t)
  have adjw' : ∀ t, M.Adj (L.port (t+1)) (w t) := fun t => nx_adj_right (W t)
  -- a chord of the link at `h` joins rotation-consecutive ports only
  have chord : ∀ i j, M.Adj (L.port i) (L.port j) → j = i + 1 ∨ i = j + 1 := by
    intro i j e
    rcases hsep _ _ (port_adj M.graph L i) (port_adj M.graph L j) e with r | r
    · rw [rot i] at r
      exact Or.inl (L.injective
        (show L.port (i+1) = L.port j from congrArg (fun d : M.Dart => d.snd) r)).symm
    · rw [rot j] at r
      exact Or.inr (L.injective
        (show L.port (j+1) = L.port i from congrArg (fun d : M.Dart => d.snd) r)).symm
  refine ⟨w, ⟨fun t ht u => ⟨fun hu => ?_, fun hu => ?_⟩, adjw, adjw', ring,
    fun t ht => ?_, fun t i => ?_, fun t => ?_, rot⟩⟩
  · rcases (C t ht).2.2 u hu with e | e | e | e | e
    · exact Or.inr (Or.inr (Or.inr (Or.inr e)))
    · exact Or.inr (Or.inr (Or.inl e))
    · exact Or.inl e
    · exact Or.inr (Or.inl e)
    · exact Or.inr (Or.inr (Or.inr (Or.inl e)))
  · rcases hu with rfl | rfl | rfl | rfl | rfl
    · exact (port_adj M.graph L t).symm
    · exact nx_adj_right (A1' t)
    · exact ring t
    · exact nx_adj_right (W' t)
    · exact adjw t
  · exact (nx_adj_right (nx_tri htri (C t ht).1).1).symm
  · obtain ⟨j, rfl⟩ : ∃ j, i = t + j := ⟨i - t, by abel⟩
    intro e
    have hj : j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 :=
      (show ∀ j : Fin 5, j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 by decide) j
    rcases hj with rfl | rfl | rfl | rfl | rfl
    · rw [add_zero] at e
      exact (adjw t).ne e.symm
    · exact (adjw' t).ne e.symm
    · exact (show ∀ s : Fin 5, ¬ (s + 2 = s + 1 ∨ s = s + 2 + 1) by decide) t
        (chord t (t+2) (e ▸ adjw t))
    · exact (show ∀ s : Fin 5, ¬ (s + 3 = s + 1 ∨ s = s + 3 + 1) by decide) t
        (chord t (t+3) (e ▸ adjw t))
    · exact (show ∀ s : Fin 5, ¬ (s + 4 = s + 1 + 1 ∨ s + 1 = s + 4 + 1) by decide) t
        (chord (t+1) (t+4) (e ▸ adjw' t))
  · by_cases ht : t = k
    · have ht1 : t + 1 ≠ k := fun e =>
        (show ∀ s : Fin 5, s + 1 ≠ s by decide) t (e.trans ht.symm)
      have := (C (t+1) ht1).2.1.2.2.2.2.2.2.2.2.1
      rw [i14] at this
      exact fun e => this e.symm
    · exact (C t ht).2.1.2.1

/-- **Theorem HP on a triangulation.** Let `M` be a spherical triangulation and `h` a vertex of
degree five such that all its neighbours except possibly one, `p`, have degree five, with no
separating triangle through `h`. Then every proper four-colouring of `M - h` reaches a filled
hole by at most six whole-component Kempe swaps. Nothing is assumed about `p`. -/
theorem theorem_HP (htri : M.Triangulated) {h p : Fin n} (hdeg : M.graph.degree h = 5)
    (hp : M.Adj h p) (hlink : ∀ u, M.Adj h u → u ≠ p → M.graph.degree u = 5)
    (hsep : M.NoSeparatingTriangleAt h) {c : Fin n → Fin 4} (hc : ProperOff M.graph h c) :
    PureFill M.graph h c 6 := by
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri (M.linkOfDegree hdeg)
  obtain ⟨k, rfl⟩ := (L.neighbours p).mp hp
  obtain ⟨w, B⟩ := M.hpBall_of_triangulated htri L ring rot k
    (fun i hi => hlink _ (port_adj M.graph L i) (fun e => hi (L.injective e))) hsep
  exact M.hp_fill B hc

end SimpleGraph.SphericalMap

namespace SimpleGraph.Icosahedron
open VacancySlide VacancyShortFill SphericalMap

/-- **Non-vacuity of Theorem HP**, with free neighbour `p = 1` (which happens to have degree
five on the icosahedron). -/
theorem theorem_HP_icosahedron : PureFill sphericalMap.graph 0 sampleColouring 6 :=
  sphericalMap.theorem_HP sphericalMap_triangulated (p := 1) (sphericalMap_degree 0)
    (show graph.Adj 0 1 by decide) (fun u _ _ => sphericalMap_degree u)
    noSeparatingTriangle_zero sampleColouring_proper

end SimpleGraph.Icosahedron
