module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltAllRoots
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFill

/-!
# Belt holes with equal pole colours (one Kempe swap)

`belt-joined.md` §3.  Let the hole be a belt vertex and `c a = c b`.  Then no coloured belt
vertex has the pole colour `A`.  Either the hole is already filled, or one actual whole-component
Kempe swap fills it:

* hole `u i`: the `(A,B)`-component of `b` is exactly `{b} ∪ {v j | c (v j) = B}`;
* hole `v i`: the `(A,B)`-component of `a` is exactly `{a} ∪ {u j | c (u j) = B}`.

The swap component is proved to be a `VacancyShortFill.Whole` (the full connected component of the
two-colour graph), and `KempeStep` is the actual move.  No hypothesis about `n mod 3` is used.
-/

@[expose] public section
namespace SimpleGraph.TwoPoleBeltEqual
open VacancySlide TwoPoleBelt TwoPoleBelt.Vertex

variable {n : ℕ}

/-- Finite pigeonhole on the middle of a four-vertex path: with the three non-`A` colours all
present on the path `p - q - r - s`, one of the two middle vertices is uniquely coloured. -/
lemma middle_unique : ∀ A p q r s : Colour, p ≠ A → q ≠ A → r ≠ A → s ≠ A →
    p ≠ q → q ≠ r → r ≠ s →
    (∀ x : Colour, x = A ∨ x = p ∨ x = q ∨ x = r ∨ x = s) →
    (q ≠ p ∧ q ≠ r ∧ q ≠ s) ∨ (r ≠ p ∧ r ≠ q ∧ r ≠ s) := by
  decide

/-! ## Hole `u i`: swap the star of `b` -/

/-- The star of `b`: `b` and its neighbours of colour `B`. -/
def Sv (c : Vertex n → Colour) (B : Colour) : Set (Vertex n) :=
  {x | x = b ∨ ∃ j, x = v j ∧ c (v j) = B}

lemma whole_u (hn : 5 ≤ n) (i : ZMod n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) (u i) c) (heq : c a = c b) (B : Colour) :
    VacancyShortFill.Whole (graph n) (u i) c (c a) B (Sv c B) := by
  have noA_u : ∀ k, u k ≠ u i → c (u k) ≠ c a := fun k hk e =>
    hc (show (graph n).Adj a (u k) by simp [graph, TwoPoleBelt.edge]) (by simp) hk e.symm
  have noA_v : ∀ k, c (v k) ≠ c a := fun k e =>
    hc (show (graph n).Adj b (v k) by simp [graph, TwoPoleBelt.edge]) (by simp) (by simp)
      (heq.symm.trans e.symm)
  refine ⟨b, ⟨by simp, Or.inl heq.symm⟩, fun x => ?_⟩
  constructor
  · intro hx
    simp only [Sv, Set.mem_setOf_eq] at hx
    rcases hx with rfl | ⟨j, rfl, hj⟩
    · exact SimpleGraph.Reachable.rfl
    · exact SimpleGraph.Adj.reachable
        ⟨by simp [graph, TwoPoleBelt.edge], ⟨by simp, Or.inl heq.symm⟩, ⟨by simp, Or.inr hj⟩⟩
  · intro hr
    refine VacancyShortFill.reachable_invariant (H := VacancyShortFill.pairGraph (graph n) (u i) c (c a) B)
      (P := fun x => x ∈ Sv c B) ?_ (s := b) (Or.inl rfl) hr
    intro y z e hy
    obtain ⟨e, ⟨hyh, hyc⟩, ⟨hzh, hzc⟩⟩ := e
    simp only [Sv, Set.mem_setOf_eq] at hy ⊢
    cases z with
    | a =>
      exfalso
      rcases hy with rfl | ⟨j, rfl, _⟩ <;> simp [graph, TwoPoleBelt.edge] at e
    | b => exact Or.inl rfl
    | v k =>
      refine Or.inr ⟨k, rfl, ?_⟩
      rcases hzc with h | h
      · exact absurd h (noA_v k)
      · exact h
    | u k =>
      exfalso
      have hB : c (u k) = B := by
        rcases hzc with h | h
        · exact absurd h (noA_u k hzh)
        · exact h
      rcases hy with rfl | ⟨j, rfl, hj⟩
      · simp [graph, TwoPoleBelt.edge] at e
      · exact hc e hyh hzh (hj.trans hB.symm)

lemma swap_v_ne [DecidableEq Colour] {c : Vertex n → Colour} {B : Colour} (hBA : B ≠ c a) (j : ZMod n) :
    VacancyShortFill.swap c (c a) B (Sv c B) (v j) ≠ B := by
  by_cases h : c (v j) = B
  · have hm : v j ∈ Sv c B := Or.inr ⟨j, rfl, h⟩
    rw [VacancyShortFill.swap_in hm, h, Equiv.swap_apply_right]
    exact hBA.symm
  · have hm : v j ∉ Sv c B := by simp [Sv, h]
    rw [VacancyShortFill.swap_out hm]
    exact h

/-- The one-swap escape at `u i`, given a colour `B` absent from the two `u`-neighbours. -/
theorem equal_u_swap (hn : 5 ≤ n) (i : ZMod n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) (u i) c) (heq : c a = c b) (B : Colour) (hBA : B ≠ c a)
    (hp : c (u (i+1)) ≠ B) (hs : c (u (i-1)) ≠ B) :
    ∃ d, VacancyShortFill.KempeStep (graph n) (u i) c d ∧ ProperOff (graph n) (u i) d ∧
      Target (u i) d := by
  classical
  have hw := whole_u hn i hc heq B
  refine ⟨VacancyShortFill.swap c (c a) B (Sv c B),
    ⟨c a, B, Sv c B, hBA.symm, hw, rfl⟩, VacancyShortFill.properOff_swap _ hc hw, B, ?_⟩
  intro y hy hyB
  rcases (adj_u hn i y).mp hy with rfl | rfl | rfl | rfl | rfl
  · rw [VacancyShortFill.swap_out (by simp [Sv])] at hyB
    exact hBA hyB.symm
  · rw [VacancyShortFill.swap_out (by simp [Sv])] at hyB
    exact hp hyB
  · exact swap_v_ne hBA i hyB
  · exact swap_v_ne hBA (i-1) hyB
  · rw [VacancyShortFill.swap_out (by simp [Sv])] at hyB
    exact hs hyB

/-- **Equal poles, hole `u i`**: already filled, or one Kempe swap fills it. -/
theorem equal_u (hn : 5 ≤ n) (i : ZMod n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) (u i) c) (heq : c a = c b) :
    Target (u i) c ∨ ∃ d, VacancyShortFill.KempeStep (graph n) (u i) c d ∧
      ProperOff (graph n) (u i) d ∧ Target (u i) d := by
  by_cases hT : Target (u i) c
  · exact Or.inl hT
  right
  have noA_u : ∀ k, u k ≠ u i → c (u k) ≠ c a := fun k hk e =>
    hc (show (graph n).Adj a (u k) by simp [graph, TwoPoleBelt.edge]) (by simp) hk e.symm
  have noA_v : ∀ k, c (v k) ≠ c a := fun k e =>
    hc (show (graph n).Adj b (v k) by simp [graph, TwoPoleBelt.edge]) (by simp) (by simp)
      (heq.symm.trans e.symm)
  have hall : ∀ x : Colour, ∃ w, (graph n).Adj (u i) w ∧ c w = x := by
    intro x
    by_contra hno
    push Not at hno
    exact hT ⟨x, fun w hw => hno w hw⟩
  have hfull : ∀ x : Colour, x = c a ∨ x = c (u (i+1)) ∨ x = c (v i) ∨ x = c (v (i-1)) ∨
      x = c (u (i-1)) := by
    intro x
    obtain ⟨w, hw, rfl⟩ := hall x
    rcases (adj_u hn i w).mp hw with rfl | rfl | rfl | rfl | rfl <;> simp
  have hp1 : u (i+1) ≠ u i := by simpa using plus_ne hn i
  have hm1 : u (i-1) ≠ u i := by simpa using minus_ne hn i
  have e12 : (graph n).Adj (u (i+1)) (v i) :=
    ((adj_v hn i _).mpr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))).symm
  have e23 : (graph n).Adj (v i) (v (i-1)) := (adj_v hn i _).mpr (Or.inr (Or.inl rfl))
  have e34 : (graph n).Adj (v (i-1)) (u (i-1)) :=
    ((adj_u hn (i-1) _).mpr (Or.inr (Or.inr (Or.inl rfl)))).symm
  rcases middle_unique (c a) (c (u (i+1))) (c (v i)) (c (v (i-1))) (c (u (i-1)))
      (noA_u _ hp1) (noA_v _) (noA_v _) (noA_u _ hm1)
      (hc e12 hp1 (by simp)) (hc e23 (by simp) (by simp)) (hc e34 (by simp) hm1) hfull with
    ⟨h1, h2, h3⟩ | ⟨h1, h2, h3⟩
  · exact equal_u_swap hn i hc heq (c (v i)) (noA_v i) (fun e => h1 e.symm) (fun e => h3 e.symm)
  · exact equal_u_swap hn i hc heq (c (v (i-1))) (noA_v _) (fun e => h1 e.symm) (fun e => h3 e.symm)

/-! ## Hole `v i`: swap the star of `a` -/

/-- The star of `a`: `a` and its neighbours of colour `B`. -/
def Su (c : Vertex n → Colour) (B : Colour) : Set (Vertex n) :=
  {x | x = a ∨ ∃ j, x = u j ∧ c (u j) = B}

lemma whole_v (hn : 5 ≤ n) (i : ZMod n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) (v i) c) (heq : c a = c b) (B : Colour) :
    VacancyShortFill.Whole (graph n) (v i) c (c a) B (Su c B) := by
  have noA_v : ∀ k, v k ≠ v i → c (v k) ≠ c a := fun k hk e =>
    hc (show (graph n).Adj b (v k) by simp [graph, TwoPoleBelt.edge]) (by simp) hk
      (heq.symm.trans e.symm)
  have noA_u : ∀ k, c (u k) ≠ c a := fun k e =>
    hc (show (graph n).Adj a (u k) by simp [graph, TwoPoleBelt.edge]) (by simp) (by simp) e.symm
  refine ⟨a, ⟨by simp, Or.inl rfl⟩, fun x => ?_⟩
  constructor
  · intro hx
    simp only [Su, Set.mem_setOf_eq] at hx
    rcases hx with rfl | ⟨j, rfl, hj⟩
    · exact SimpleGraph.Reachable.rfl
    · exact SimpleGraph.Adj.reachable
        ⟨by simp [graph, TwoPoleBelt.edge], ⟨by simp, Or.inl rfl⟩, ⟨by simp, Or.inr hj⟩⟩
  · intro hr
    refine VacancyShortFill.reachable_invariant (H := VacancyShortFill.pairGraph (graph n) (v i) c (c a) B)
      (P := fun x => x ∈ Su c B) ?_ (s := a) (Or.inl rfl) hr
    intro y z e hy
    obtain ⟨e, ⟨hyh, hyc⟩, ⟨hzh, hzc⟩⟩ := e
    simp only [Su, Set.mem_setOf_eq] at hy ⊢
    cases z with
    | a => exact Or.inl rfl
    | b =>
      exfalso
      rcases hy with rfl | ⟨j, rfl, _⟩ <;> simp [graph, TwoPoleBelt.edge] at e
    | u k =>
      refine Or.inr ⟨k, rfl, ?_⟩
      rcases hzc with h | h
      · exact absurd h (noA_u k)
      · exact h
    | v k =>
      exfalso
      have hB : c (v k) = B := by
        rcases hzc with h | h
        · exact absurd h (noA_v k hzh)
        · exact h
      rcases hy with rfl | ⟨j, rfl, hj⟩
      · simp [graph, TwoPoleBelt.edge] at e
      · exact hc e hyh hzh (hj.trans hB.symm)

lemma swap_u_ne [DecidableEq Colour] {c : Vertex n → Colour} {B : Colour} (hBA : B ≠ c a) (j : ZMod n) :
    VacancyShortFill.swap c (c a) B (Su c B) (u j) ≠ B := by
  by_cases h : c (u j) = B
  · have hm : u j ∈ Su c B := Or.inr ⟨j, rfl, h⟩
    rw [VacancyShortFill.swap_in hm, h, Equiv.swap_apply_right]
    exact hBA.symm
  · have hm : u j ∉ Su c B := by simp [Su, h]
    rw [VacancyShortFill.swap_out hm]
    exact h

theorem equal_v_swap (hn : 5 ≤ n) (i : ZMod n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) (v i) c) (heq : c a = c b) (B : Colour) (hBA : B ≠ c a)
    (hp : c (v (i-1)) ≠ B) (hs : c (v (i+1)) ≠ B) :
    ∃ d, VacancyShortFill.KempeStep (graph n) (v i) c d ∧ ProperOff (graph n) (v i) d ∧
      Target (v i) d := by
  classical
  have hw := whole_v hn i hc heq B
  refine ⟨VacancyShortFill.swap c (c a) B (Su c B),
    ⟨c a, B, Su c B, hBA.symm, hw, rfl⟩, VacancyShortFill.properOff_swap _ hc hw, B, ?_⟩
  intro y hy hyB
  rcases (adj_v hn i y).mp hy with rfl | rfl | rfl | rfl | rfl
  · rw [VacancyShortFill.swap_out (by simp [Su])] at hyB
    exact hBA (heq ▸ hyB.symm)
  · rw [VacancyShortFill.swap_out (by simp [Su])] at hyB
    exact hp hyB
  · exact swap_u_ne hBA i hyB
  · exact swap_u_ne hBA (i+1) hyB
  · rw [VacancyShortFill.swap_out (by simp [Su])] at hyB
    exact hs hyB

/-- **Equal poles, hole `v i`**: already filled, or one Kempe swap fills it. -/
theorem equal_v (hn : 5 ≤ n) (i : ZMod n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) (v i) c) (heq : c a = c b) :
    Target (v i) c ∨ ∃ d, VacancyShortFill.KempeStep (graph n) (v i) c d ∧
      ProperOff (graph n) (v i) d ∧ Target (v i) d := by
  by_cases hT : Target (v i) c
  · exact Or.inl hT
  right
  have noA_v : ∀ k, v k ≠ v i → c (v k) ≠ c a := fun k hk e =>
    hc (show (graph n).Adj b (v k) by simp [graph, TwoPoleBelt.edge]) (by simp) hk
      (heq.symm.trans e.symm)
  have noA_u : ∀ k, c (u k) ≠ c a := fun k e =>
    hc (show (graph n).Adj a (u k) by simp [graph, TwoPoleBelt.edge]) (by simp) (by simp) e.symm
  have hall : ∀ x : Colour, ∃ w, (graph n).Adj (v i) w ∧ c w = x := by
    intro x
    by_contra hno
    push Not at hno
    exact hT ⟨x, fun w hw => hno w hw⟩
  have hfull : ∀ x : Colour, x = c a ∨ x = c (v (i-1)) ∨ x = c (u i) ∨ x = c (u (i+1)) ∨
      x = c (v (i+1)) := by
    intro x
    obtain ⟨w, hw, rfl⟩ := hall x
    rcases (adj_v hn i w).mp hw with rfl | rfl | rfl | rfl | rfl
    · simp [heq]
    all_goals simp
  have hm1 : v (i-1) ≠ v i := by simpa using minus_ne hn i
  have hp1 : v (i+1) ≠ v i := by simpa using plus_ne hn i
  have e12 : (graph n).Adj (v (i-1)) (u i) :=
    ((adj_u hn i _).mpr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))).symm
  have e23 : (graph n).Adj (u i) (u (i+1)) := (adj_u hn i _).mpr (Or.inr (Or.inl rfl))
  have e34 : (graph n).Adj (u (i+1)) (v (i+1)) := (adj_u hn (i+1) _).mpr (Or.inr (Or.inr (Or.inl rfl)))
  rcases middle_unique (c a) (c (v (i-1))) (c (u i)) (c (u (i+1))) (c (v (i+1)))
      (noA_v _ hm1) (noA_u _) (noA_u _) (noA_v _ hp1)
      (hc e12 hm1 (by simp)) (hc e23 (by simp) (by simp)) (hc e34 (by simp) hp1) hfull with
    ⟨h1, h2, h3⟩ | ⟨h1, h2, h3⟩
  · exact equal_v_swap hn i hc heq (c (u i)) (noA_u i) (fun e => h1 e.symm) (fun e => h3 e.symm)
  · exact equal_v_swap hn i hc heq (c (u (i+1))) (noA_u _) (fun e => h1 e.symm) (fun e => h3 e.symm)

end SimpleGraph.TwoPoleBeltEqual
