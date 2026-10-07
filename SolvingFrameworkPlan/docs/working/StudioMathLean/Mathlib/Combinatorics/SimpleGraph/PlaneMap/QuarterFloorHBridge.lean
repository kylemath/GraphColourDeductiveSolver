/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFloorH
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyIcosahedral

/-!
# Theorem F5 from triangulation and degree-five link vertices

Discharges the hypothesis `IcoBallP` of `quarterFloor_of_icoBall` on a spherical triangulation
whose hole `h` is pentagonal (`Pent`) with all five link vertices of degree five.

The library's `icoBall_of_triangulated` also assumes `NoSeparatingTriangleAt h`; it is used
only to exclude `w t = x (t+3)`. Here that hypothesis is dropped: if some `w t = x (t+3)`,
the rotation at the degree-five vertex `x (t+3)` forces `w (t+2) = x t`, `w (t+3) = x (t+1)`,
so the coincidence propagates to every `t`, and then the link is a 5-clique of `G - h`, which
has no proper 4-colouring; the quarter floor holds vacuously.

## Main results (sorry-free)

* `icoBall_or_linkClique`: on a triangulation with degree-five link vertices listed in
  rotation order, either an `IcoBall` exists or the link is a clique.
* `quarterFloor_of_fiveLink` (**Theorem F5, unconditional form**).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral SphericalMap

variable {n : ℕ} {M : SphericalMap n}

/-- The 2-ball dichotomy: without a no-separating-triangle hypothesis, either the icosahedral
2-ball exists or the five link vertices are pairwise adjacent. -/
theorem icoBall_or_linkClique (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    (hlink : ∀ i, M.graph.degree (L.port i) = 5) :
    (∃ w : Fin 5 → Fin n, IcoBall M.graph h L w) ∨
      ∀ i j, i ≠ j → M.graph.Adj (L.port i) (L.port j) := by
  classical
  have i41 : ∀ t : Fin 5, t + 4 + 1 = t := by decide
  have i14 : ∀ t : Fin 5, t + 1 + 4 = t := by decide
  have i11 : ∀ t : Fin 5, t + 1 + 1 = t + 2 := by decide
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
  have adjw1 : ∀ t, M.Adj (L.port (t+1)) (w t) := fun t => nx_adj_right (W t)
  have hne : ∀ i j, i ≠ j → L.port i ≠ L.port j := fun i j hij e => hij (L.injective e)
  by_cases hsep : ∀ t, w t ≠ L.port (t+3)
  · left
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
    · have h1 := (C (t+1)).1
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
      · exact hsep t e
      · exact (nd t).2.2 e
  · right
    push Not at hsep
    obtain ⟨t₀, ht₀⟩ := hsep
    -- the coincidence `w s = x (s+3)` propagates to `s+2` and `s+3`
    have step : ∀ s, w s = L.port (s+3) →
        w (s+2) = L.port (s+2+3) ∧ w (s+3) = L.port (s+3+3) := by
      have e5' : ∀ s : Fin 5, s + 2 + 3 = s := by decide
      have e6' : ∀ s : Fin 5, s + 3 + 3 = s + 1 := by decide
      have e34' : ∀ s : Fin 5, s + 3 + 4 = s + 2 := by decide
      have e31' : ∀ s : Fin 5, s + 3 + 1 = s + 4 := by decide
      have e24' : ∀ s : Fin 5, s + 2 + 4 = s + 1 := by decide
      have e32' : ∀ s : Fin 5, s + 3 + 2 = s := by decide
      have n04' : ∀ s : Fin 5, s ≠ s + 4 := by decide
      have n02' : ∀ s : Fin 5, s ≠ s + 2 := by decide
      have n14' : ∀ s : Fin 5, s + 1 ≠ s + 4 := by decide
      have n12' : ∀ s : Fin 5, s + 1 ≠ s + 2 := by decide
      intro s hs
      have e5 := e5' s
      have e6 := e6' s
      have e34 := e34' s
      have e31 := e31' s
      have e24 := e24' s
      have e32 := e32' s
      rw [e5, e6]
      have a0 : M.Adj (L.port (s+3)) (L.port s) := hs ▸ (adjw s).symm
      have a1 : M.Adj (L.port (s+3)) (L.port (s+1)) := hs ▸ (adjw1 s).symm
      have c0 := (C (s+3)).2.2 _ a0
      have c1 := (C (s+3)).2.2 _ a1
      rw [e34, e31] at c0 c1
      have n04 := n04' s
      have n02 := n02' s
      have n14 := n14' s
      have n12 := n12' s
      have nh0 : L.port s ≠ h := (port_adj M.graph L s).ne.symm
      have nh1 : L.port (s+1) ≠ h := (port_adj M.graph L (s+1)).ne.symm
      have x1 : L.port (s+1) = w (s+3) := by
        rcases c1 with e | e | e | e | e
        · exact e
        · exact absurd e (hne _ _ n14)
        · exact absurd e nh1
        · exact absurd e (hne _ _ n12)
        · exfalso; have := (nd (s+2)).2.2; rw [e24] at this; exact this e.symm
      have x0 : L.port s = w (s+2) := by
        rcases c0 with e | e | e | e | e
        · exfalso; have := nd2 (s+3); rw [e32] at this; exact this e.symm
        · exact absurd e (hne _ _ n04)
        · exact absurd e nh0
        · exact absurd e (hne _ _ n02)
        · exact e
      exact ⟨x0.symm, x1.symm⟩
    have all : ∀ s, w s = L.port (s+3) := by
      have q1 : ∀ t : Fin 5, t + 3 + 3 = t + 1 := by decide
      have q4 : ∀ t : Fin 5, t + 2 + 2 = t + 4 := by decide
      have hj5 : ∀ j : Fin 5, j = 0 ∨ j = 1 ∨ j = 2 ∨ j = 3 ∨ j = 4 := by decide
      have p2 := step t₀ ht₀
      have p3 := step (t₀+2) p2.1
      have p4 := step (t₀+3) p2.2
      intro s
      obtain ⟨j, rfl⟩ : ∃ j, s = t₀ + j := ⟨s - t₀, by abel⟩
      have hj := hj5 j
      have f : ∀ a b : Fin 5, a = b → w a = L.port (a+3) → w b = L.port (b+3) := by
        rintro a b rfl e; exact e
      rcases hj with rfl | rfl | rfl | rfl | rfl
      · exact f _ _ (by abel) ht₀
      · exact f _ _ (q1 t₀) p4.2
      · exact p2.1
      · exact p2.2
      · exact f _ _ (q4 t₀) p3.1
    have q2 : ∀ i : Fin 5, i + 4 + 3 = i + 2 := by decide
    intro i j hij
    obtain ⟨k, rfl⟩ : ∃ k, j = i + k := ⟨j - i, by abel⟩
    have hk : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 := by clear hij; revert k; decide
    rcases hk with rfl | rfl | rfl | rfl | rfl
    · exact absurd (add_zero i).symm hij
    · exact ring i
    · have a := adjw1 (i+4)
      rw [all, i41, q2 i] at a
      exact a
    · have a := adjw i
      rw [all] at a
      exact a
    · have a := ring (i+4)
      rw [i41] at a
      exact a.symm

/-- **Theorem F5 on a triangulation.** On a spherical triangulation, at a pentagonal hole whose
five link vertices have degree five, every Kempe class of proper four-colourings of `M - h` is
at least a quarter filled. No separating-triangle hypothesis is needed. -/
theorem quarterFloor_of_fiveLink (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (hdeg : ∀ i, M.graph.degree (P.x i) = 5) : QuarterFloorConj (G := M.graph) (h := h) := by
  classical
  let L0 : FiveLink M.graph h :=
    ⟨P.x, P.inj, fun v => ⟨P.only v, by rintro ⟨i, rfl⟩; exact P.adj_h i⟩⟩
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri L0
  have hlink : ∀ i, M.graph.degree (L.port i) = 5 := fun i => by
    obtain ⟨j, e⟩ := P.only _ (port_adj M.graph L i)
    rw [e]; exact hdeg j
  rcases icoBall_or_linkClique htri L ring rot hlink with ⟨w, B⟩ | hcl
  · let P' : Pent M.graph h :=
      ⟨L.port, port_adj M.graph L, ring, L.injective, fun v hv => (L.neighbours v).mp hv⟩
    exact quarterFloor_of_icoBall (P := P') (w := w) ⟨B.nbr, B.ring, B.off, B.offh⟩
  · intro c₀ hc₀
    exfalso
    have inj : Function.Injective (fun i => c₀ (L.port i)) := by
      intro i j e
      by_contra hij
      exact hc₀ (hcl i j hij) (port_adj M.graph L i).ne.symm (port_adj M.graph L j).ne.symm e
    have := Fintype.card_le_of_injective _ inj
    simp at this

end SimpleGraph.QuarterFloor
