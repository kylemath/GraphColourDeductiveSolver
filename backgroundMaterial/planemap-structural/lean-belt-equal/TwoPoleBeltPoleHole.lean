module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltEqualPoles
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleNoSingleton

/-!
# The belt theorem at every belt hole, and at the pole `a`

* `belt_complete`: every belt hole, every proper colouring (equal or unequal poles), reaches a
  filled hole by a mixed path of at most `2 n` moves (at most one Kempe swap for equal poles,
  at most `2 n` slides for unequal poles).
* `pole_a_singleton`: pole hole `a` with a singleton ring colour: one slide, then `belt_complete`
  (the poles may now be equal).
* `pole_a_complete`: pole hole `a`, every colouring: Theorem P (Kempe swaps) to a fill or a
  singleton, then a slide and `belt_complete`.  At most `6 n` moves in all.
* `pole_b_singleton`: the same slide step at the pole `b`.
-/

@[expose] public section
namespace SimpleGraph.TwoPoleBeltPoleHole
open VacancySlide TwoPoleBelt TwoPoleBelt.Vertex TwoPoleBeltWalk

variable {n : ℕ}

lemma mixedPath_append {k l : ℕ} {s t w : State n}
    (p : VacancyShortFill.MixedPath (graph n) k s t)
    (q : VacancyShortFill.MixedPath (graph n) l t w) :
    VacancyShortFill.MixedPath (graph n) (k + l) s w := by
  induction p with
  | nil => simpa using q
  | @cons m _ _ _ step rest ih =>
    have := VacancyShortFill.MixedPath.cons step (ih q)
    have e : m + l + 1 = m + 1 + l := by omega
    rwa [e] at this

lemma mixed_of_slidePath {k : ℕ} {s t : State n}
    (p : VacancyPotential.Path SlideStep k s t) :
    VacancyShortFill.MixedPath (graph n) k s t := by
  induction p with
  | nil s => exact .nil s
  | @cons s t _ m step _ ih =>
    obtain ⟨x, adj, uniq, rfl⟩ := step
    obtain ⟨h, c⟩ := s
    exact .cons (.slide adj uniq) ih

/-- **The belt theorem at a belt hole**, for every proper colouring of the deletion. -/
theorem belt_complete (hn : 5 ≤ n) (h : Vertex n) (hb : IsBelt h) (c : Vertex n → Colour)
    (hc : ProperOff (graph n) h c) :
    ∃ k, k ≤ 2 * n ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (h, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2 := by
  by_cases hab : c a = c b
  · have key : Filled (h, c) ∨ ∃ d, VacancyShortFill.KempeStep (graph n) h c d ∧
        ProperOff (graph n) h d ∧ Target h d := by
      cases h with
      | a => exact (hb.1 rfl).elim
      | b => exact (hb.2 rfl).elim
      | u i => exact TwoPoleBeltEqual.equal_u hn i hc hab
      | v i => exact TwoPoleBeltEqual.equal_v hn i hc hab
    rcases key with hf | ⟨d, hk, hd, hf⟩
    · exact ⟨0, by omega, (h, c), .nil _, hf, hc⟩
    · exact ⟨1, by omega, (h, d), .cons (.kempe hk) (.nil _), hf, hd⟩
  · obtain ⟨k, t, p, hk, hf, hp, -, -, -⟩ := belt_unequal_at hn h hb c hc hab
    exact ⟨k, hk, t, mixed_of_slidePath p, hf, hp⟩

/-- Pole hole `a`, ring singleton at `u i`: one slide, then the belt theorem (equal or
unequal poles). -/
theorem pole_a_singleton (hn : 5 ≤ n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) a c) (i : ZMod n) (hU : UniqueAt (graph n) a (u i) c) :
    ∃ k, k ≤ 2 * n + 1 ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (a, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2 := by
  have hc' := properOff_slide (graph n) hc hU
  obtain ⟨k, hk, t, p, hf, hp⟩ := belt_complete hn (u i) (isBelt_u i) _ hc'
  exact ⟨1 + k, by omega, t,
    mixedPath_append (.cons (.slide (nbr_a i) hU) (.nil _)) p, hf, hp⟩

/-- Pole hole `b`, ring singleton at `v i`: one slide, then the belt theorem. -/
theorem pole_b_singleton (hn : 5 ≤ n) {c : Vertex n → Colour}
    (hc : ProperOff (graph n) b c) (i : ZMod n) (hU : UniqueAt (graph n) b (v i) c) :
    ∃ k, k ≤ 2 * n + 1 ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (b, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2 := by
  have hc' := properOff_slide (graph n) hc hU
  obtain ⟨k, hk, t, p, hf, hp⟩ := belt_complete hn (v i) (isBelt_v i) _ hc'
  exact ⟨1 + k, by omega, t,
    mixedPath_append (.cons (.slide (nbr_b i) hU) (.nil _)) p, hf, hp⟩

/-- **The belt theorem at the pole `a`**, every proper colouring of `G_n - a`:
at most `6 n` moves (Kempe swaps and slides) reach a filled hole. -/
theorem pole_a_complete (hn : 5 ≤ n) [NeZero n] (c : Vertex n → Colour)
    (hc : ProperOff (graph n) a c) :
    ∃ k, k ≤ 6 * n ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (a, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2 := by
  obtain ⟨k, hk, d, hd, x, hx⟩ := TheoremPPole.theoremP hn c hc
  have hcard : (TheoremPPole.jset c).card ≤ n := by
    calc _ ≤ (Finset.univ : Finset (ZMod n)).card := Finset.card_le_univ _
      _ = n := by simp
  have hpd := hd.proper _ hc
  have pm := VacancyShortFill.purePath_mixed (graph n) hd
  by_cases hex : ∃ i, d (u i) = x
  · obtain ⟨i, hi⟩ := hex
    have hU : UniqueAt (graph n) a (u i) d := by
      intro y hy hyc
      obtain ⟨j, rfl⟩ := TheoremPPole.adj_a_iff.mp hy
      exact congrArg u (hx j i (hyc.trans hi) hi)
    obtain ⟨m, hm, t, p, hf, hp⟩ := pole_a_singleton hn hpd i hU
    exact ⟨k + m, by omega, t, mixedPath_append pm p, hf, hp⟩
  · push Not at hex
    have hf : Filled (a, d) := ⟨x, fun v hv => by
      obtain ⟨i, rfl⟩ := TheoremPPole.adj_a_iff.mp hv
      exact hex i⟩
    exact ⟨k, by omega, (a, d), pm, hf, hpd⟩

end SimpleGraph.TwoPoleBeltPoleHole
