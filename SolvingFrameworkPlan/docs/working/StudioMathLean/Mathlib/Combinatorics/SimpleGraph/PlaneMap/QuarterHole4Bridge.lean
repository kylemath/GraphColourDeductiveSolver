/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterHole6Bridge
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterHole6Gen

/-!
# `Hole4` from vertex degrees; `PureClean` at every `(5,5,5,5,d)` vertex

Discharges the local hypothesis `Hole4 P w q` of `pureClean_of_hole4` (`QuarterHole6Gen`) on a
spherical triangulation from degree hypotheses, as `QuarterHole6Bridge` does for `Hole6`.

**Scope.** Four consecutive degree-five link vertices at a degree-five vertex `h` contain three
consecutive ones, which with `h` form a Birkhoff diamond (NightWeakForm.md §1, table §5). The
diamond is reducible and already excluded from a minimal counterexample by the library
(`DiamondMCert`/`DiamondPCert`, `FrameF3`). So everything here is inside Birkhoff-diamond
territory and does **not** bear on a minimal counterexample.

## Construction

As in `QuarterHole6Bridge`: the link `x 0, …, x 4` in rotation order, `w t` the third vertex of
the face beyond `x t x (t+1)`. Hole4 needs, for `t ≠ q`, the degree-five neighbourhood of `x t`
(`chain5`), the ring edges `w t ~ w (t+1)` with `t + 1 ≠ q` (faces at the degree-five
`x (t+1)`), `x q ~ w q`, `x q ~ w (q+4)` (faces), `w t ≠ h`, and `w t ≠ x i`.

Where the Hole6 bridge used the exact rotation at the degree-six `x q`, here only
`4 ≤ deg (x q)` is used: `w q ≠ x (q+4)` and `w (q+4) ≠ x (q+1)` because otherwise the rotation
at `x q` would have period dividing three (`hole4Bridge_nx3_ne`).

The remaining condition `w t ≠ x (t+3)` propagates as in the Hole6 bridge, from `s` with
`s + 3 ≠ q` to `s + 2` and `s + 3` (at the degree-five `x (s+3)`), and from any such `s` to
every `s`; then the link is a clique. The one coincidence that does **not** propagate when
`deg (x q) ≥ 7` is `w (q+2) = x q` alone (the face `x (q+2) x (q+3) x q`): then `x q` is
adjacent to `x (q+2)` and `x (q+3)`, `h x q x (q+2)` is a separating triangle, the link is not a
clique, and `Hole4` fails (`off`). This chord case is genuinely possible on a triangulation, so
the degree dichotomy is a **trichotomy** (`hole4_or_linkClique_or_chord`). It is excluded by
`NoSeparatingTriangleAt h` (`not_adj_skip`), and in `RStarCore` by `NoSep`.

## Main results (sorry-free, no new axioms)

* `hole4_or_linkClique_or_chord`: `x t` of degree five for `t ≠ q`, `4 ≤ deg (x q)`: `Hole4`, or
  the link is a clique, or `x q ~ x (q+2)` and `x q ~ x (q+3)`.
* `hole4_of_degrees`: with `NoSeparatingTriangleAt h`, `Hole4 P w q` (clique and chord both
  contain the chord `x q x (q+2)`, which a separating-triangle-free `h` excludes).
* **`pureClean_of_four_consecutive_fives`**: `P` in any order, four link vertices of degree five
  and `5 ≤ deg (x q)`, and either `NoSeparatingTriangleAt h` or `deg (x q) ≤ 6`: `PureClean M h`.
  The clique case is excluded exactly as in the Hole6 bridge: a clique link has no proper
  four-colouring off `h` (`no_properOff_of_linkClique`), so `PureClean` is vacuous. Degrees 5
  and 6 of `x q` go through the F5 and Hole6 bridges (no separating-triangle hypothesis).
* `pureClean_of_linkDegrees'`: vertex form, link degrees `(5,5,5,5,5)`, `(5,5,5,5,6)`, and
  `(5,5,5,5,d)` for every `d ≥ 7` given `NoSeparatingTriangleAt h`.
* `cleanOff_of_four_consecutive_fives`: the `RStarCore`-side form, using `NoSep T`.

## Not done

`PureClean` in the chord case with `deg (x q) ≥ 7` and a separating triangle through `h`; it
would need a Kempe-chain confinement (Jordan) argument not available here.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral SphericalMap

variable {n : ℕ} {M : SphericalMap n}

/-- A rotation orbit at `v` that returns after `k` steps has `deg v ∣ k`. -/
private lemma hole4Bridge_period_dvd {v : Fin n} (d : M.Dart) (hd : d.fst = v) (k : ℕ)
    (hk : (⇑M.rotation.next)^[k] d = d) : M.graph.degree v ∣ k := by
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
  have hp : Function.minimalPeriod σ w = M.graph.degree d.fst := R.neighbor_period_eq_degree _ _
  rw [← hp]
  apply Function.IsPeriodicPt.minimalPeriod_dvd
  have e : M.graph.dartOfNeighborSet d.fst (σ^[k] w) = M.graph.dartOfNeighborSet d.fst w := by
    rw [← hit, hk, hdw]
  exact M.graph.dartOfNeighborSet_injective _ e

/-- At a vertex of degree at least four, three rotation steps never return. -/
lemma hole4Bridge_nx3_ne {v a b c d : Fin n} (hv : 4 ≤ M.graph.degree v)
    (h1 : Nx M v a b) (h2 : Nx M v b c) (h3 : Nx M v c d) : d ≠ a := by
  rintro rfl
  obtain ⟨g0, g1, e1⟩ := nx_dart h1
  obtain ⟨_g1, g2, e2⟩ := nx_dart h2
  obtain ⟨_g2, g3, e3⟩ := nx_dart h3
  let D : M.Dart := ⟨(v,d),g0⟩
  have i1 : (⇑M.rotation.next)^[1] D = ⟨(v,b),g1⟩ := e1
  have i2 : (⇑M.rotation.next)^[2] D = ⟨(v,c),g2⟩ := by
    rw [Function.iterate_succ_apply', i1]; exact e2
  have i3 : (⇑M.rotation.next)^[3] D = D := by
    rw [Function.iterate_succ_apply', i2]; exact e3
  have := Nat.le_of_dvd (by norm_num) (hole4Bridge_period_dvd (v := v) D rfl 3 i3)
  omega

/-- Propagation of `w s = x (s+3)` from `s` with `s + 3 ≠ q`: any such `s` gives every `s`. -/
private lemma hole4Bridge_closure : ∀ (q : Fin 5) (b : Fin 5 → Bool),
    (∀ s, s + 3 ≠ q → b s = true → b (s + 2) = true ∧ b (s + 3) = true) →
    ∀ s, s + 3 ≠ q → b s = true → ∀ t, b t = true := by
  decide

/-- With `NoSeparatingTriangleAt h` and the link in rotation order, `x i` and `x (i+2)` are not
adjacent. -/
theorem not_adj_skip {h : Fin n} (P : Pent M.graph h)
    (rot : ∀ i : Fin 5, M.rotation.next ⟨(h, P.x i), P.adj_h i⟩ =
      ⟨(h, P.x (i + 1)), P.adj_h (i + 1)⟩)
    (hns : M.NoSeparatingTriangleAt h) (i : Fin 5) : ¬ M.Adj (P.x i) (P.x (i + 2)) := by
  intro ha
  rcases hns _ _ (P.adj_h i) (P.adj_h (i + 2)) ha with e | e
  · rw [rot i] at e
    have := P.inj (congrArg (fun d : M.Dart => d.snd) e)
    exact absurd this (by
      have : ∀ t : Fin 5, t + 1 ≠ t + 2 := by decide
      exact this i)
  · rw [rot (i + 2)] at e
    have := P.inj (congrArg (fun d : M.Dart => d.snd) e)
    exact absurd this (by
      have : ∀ t : Fin 5, t + 2 + 1 ≠ t := by decide
      exact this i)

/-- **The `(5,5,5,5,d)` degree trichotomy.** On a triangulation, with the link of `h` in rotation
order, `x t` of degree five for `t ≠ q` and `x q` of degree at least four: `Hole4 P w q` for some
outer ring `w`, or the link is a clique, or `x q` is adjacent to `x (q+2)` and `x (q+3)`. No
separating-triangle hypothesis. -/
theorem hole4_or_linkClique_or_chord (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (rot : ∀ i : Fin 5, M.rotation.next ⟨(h, P.x i), P.adj_h i⟩ =
      ⟨(h, P.x (i + 1)), P.adj_h (i + 1)⟩)
    (q : Fin 5) (hq4 : 4 ≤ M.graph.degree (P.x q))
    (h5 : ∀ i, i ≠ q → M.graph.degree (P.x i) = 5) :
    (∃ w : Fin 5 → Fin n, Hole4 P w q) ∨
      (∀ i j, i ≠ j → M.graph.Adj (P.x i) (P.x j)) ∨
      (M.graph.Adj (P.x q) (P.x (q + 2)) ∧ M.graph.Adj (P.x q) (P.x (q + 3))) := by
  classical
  have i41 : ∀ t : Fin 5, t + 4 + 1 = t := by decide
  have i14 : ∀ t : Fin 5, t + 1 + 4 = t := by decide
  have i11 : ∀ t : Fin 5, t + 1 + 1 = t + 2 := by decide
  have ring := P.adj_cyc
  have R : ∀ t, Nx M h (P.x t) (P.x (t+1)) := fun t => nx_of_dart (rot t)
  have A1 : ∀ t, Nx M (P.x (t+1)) h (P.x t) := fun t => (nx_tri htri (R t)).1
  have A2 : ∀ t, Nx M (P.x t) (P.x (t+1)) h := fun t => (nx_tri htri (R t)).2
  have Wex : ∀ t, ∃ y, Nx M (P.x (t+1)) (P.x t) y := fun t => ⟨_, (ring t).symm, rfl⟩
  choose w W using Wex
  have B2 : ∀ t, Nx M (P.x t) (w t) (P.x (t+1)) := fun t => (nx_tri htri (W t)).2
  have A1' : ∀ t, Nx M (P.x t) h (P.x (t+4)) := fun t => by
    have := A1 (t+4); rwa [i41] at this
  have W' : ∀ t, Nx M (P.x t) (P.x (t+4)) (w (t+4)) := fun t => by
    have := W (t+4); rwa [i41] at this
  have C := fun t (ht : t ≠ q) => chain5 (h5 t ht) (B2 t) (A2 t) (A1' t) (W' t)
  have q1 : q + 1 ≠ q := by
    have : ∀ t : Fin 5, t + 1 ≠ t := by decide
    exact this q
  have c03 : w q ≠ P.x (q+4) := (hole4Bridge_nx3_ne hq4 (B2 q) (A2 q) (A1' q)).symm
  have c14 : P.x (q+1) ≠ w (q+4) := (hole4Bridge_nx3_ne hq4 (A2 q) (A1' q) (W' q)).symm
  have hne : ∀ i j, i ≠ j → P.x i ≠ P.x j := fun i j hij e => hij (P.inj e)
  have adjw : ∀ t, M.Adj (P.x t) (w t) := fun t => nx_adj_left (B2 t)
  have adjw1 : ∀ t, M.Adj (P.x (t+1)) (w t) := fun t => nx_adj_right (W t)
  have Dh : ∀ t, w t ≠ h := fun t => by
    by_cases ht : t = q
    · subst ht
      have := (C (t+1) q1).2.1.2.2.2.2.2.2.2.2.1
      rw [i14] at this
      exact fun e => this e.symm
    · exact (C t ht).2.1.2.1
  have D4 : ∀ t, w t ≠ P.x (t+4) := fun t => by
    by_cases ht : t = q
    · subst ht; exact c03
    · exact (C t ht).2.1.2.2.1
  have D2 : ∀ t, w t ≠ P.x (t+2) := fun t => by
    by_cases hs : t + 1 = q
    · have := c14
      rw [← hs, i11, i14] at this
      exact fun e => this e.symm
    · have := (C (t+1) hs).2.1.2.2.2.2.2.2.1
      rw [i14, i11] at this
      exact fun e => this e.symm
  -- at a degree-five `x (s+3)` the coincidence `w s = x (s+3)` propagates
  have step : ∀ s, s + 3 ≠ q → w s = P.x (s+3) →
      w (s+2) = P.x (s+2+3) ∧ w (s+3) = P.x (s+3+3) := by
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
    intro s hq hs
    have e5 := e5' s
    have e6 := e6' s
    have e34 := e34' s
    have e31 := e31' s
    have e24 := e24' s
    have e32 := e32' s
    rw [e5, e6]
    have a0 : M.Adj (P.x (s+3)) (P.x s) := hs ▸ (adjw s).symm
    have a1 : M.Adj (P.x (s+3)) (P.x (s+1)) := hs ▸ (adjw1 s).symm
    have c0 := (C (s+3) hq).2.2 _ a0
    have c1 := (C (s+3) hq).2.2 _ a1
    rw [e34, e31] at c0 c1
    have nh0 : P.x s ≠ h := P.x_ne_h s
    have nh1 : P.x (s+1) ≠ h := P.x_ne_h (s+1)
    have x1 : P.x (s+1) = w (s+3) := by
      rcases c1 with e | e | e | e | e
      · exact e
      · exact absurd e (hne _ _ (n14' s))
      · exact absurd e nh1
      · exact absurd e (hne _ _ (n12' s))
      · exfalso; have := D4 (s+2); rw [e24] at this; exact this e.symm
    have x0 : P.x s = w (s+2) := by
      rcases c0 with e | e | e | e | e
      · exfalso; have := D2 (s+3); rw [e32] at this; exact this e.symm
      · exact absurd e (hne _ _ (n04' s))
      · exact absurd e nh0
      · exact absurd e (hne _ _ (n02' s))
      · exact e
    exact ⟨x0.symm, x1.symm⟩
  by_cases hsep : ∀ t, w t ≠ P.x (t+3)
  · left
    refine ⟨w, ⟨fun t ht u => ⟨fun hu => ?_, fun hu => ?_⟩, adjw q, nx_adj_right (W' q),
      fun t ht => ?_, fun t i => ?_, Dh⟩⟩
    · rcases (C t ht).2.2 u hu with e | e | e | e | e
      · exact Or.inr (Or.inr (Or.inr (Or.inr e)))
      · exact Or.inr (Or.inr (Or.inl e))
      · exact Or.inl e
      · exact Or.inr (Or.inl e)
      · exact Or.inr (Or.inr (Or.inr (Or.inl e)))
    · rcases hu with rfl | rfl | rfl | rfl | rfl
      · exact (P.adj_h t).symm
      · exact nx_adj_right (A1' t)
      · exact ring t
      · exact nx_adj_right (W' t)
      · exact adjw t
    · have h1 := (C (t+1) ht).1
      rw [i14] at h1
      exact (nx_adj_right (nx_tri htri h1).1).symm
    · obtain ⟨j, rfl⟩ : ∃ j, i = t + j := ⟨i - t, by abel⟩
      intro e
      rcases fin5_five j with rfl | rfl | rfl | rfl | rfl
      · rw [add_zero] at e
        exact (adjw t).ne e.symm
      · exact (adjw1 t).ne e.symm
      · exact D2 t e
      · exact hsep t e
      · exact D4 t e
  · right
    push Not at hsep
    obtain ⟨t₀, ht₀⟩ := hsep
    by_cases hq : t₀ + 3 = q
    · -- the chord case: `w (q+2) = x q`
      right
      have ht : t₀ = q + 2 := by
        rw [← hq]
        have : ∀ s : Fin 5, s = s + 3 + 2 := by decide
        exact this t₀
      subst ht
      rw [hq] at ht₀
      have a2 := (adjw (q+2)).symm
      have a3 := (adjw1 (q+2)).symm
      rw [ht₀] at a2 a3
      have f3 : q + 2 + 1 = q + 3 := by
        have : ∀ t : Fin 5, t + 2 + 1 = t + 3 := by decide
        exact this q
      rw [f3] at a3
      exact ⟨a2, a3⟩
    left
    have all : ∀ s, w s = P.x (s+3) := by
      let b : Fin 5 → Bool := fun s => decide (w s = P.x (s+3))
      have hb : ∀ s, b s = true ↔ w s = P.x (s+3) := fun s => decide_eq_true_iff
      have cl := hole4Bridge_closure q b
        (fun s hq hs => by
          rw [hb] at hs
          have := step s hq hs
          exact ⟨(hb _).2 this.1, (hb _).2 this.2⟩)
      intro s
      exact (hb s).1 (cl t₀ hq ((hb t₀).2 ht₀) s)
    have q2 : ∀ i : Fin 5, i + 4 + 3 = i + 2 := by decide
    intro i j hij
    obtain ⟨k, rfl⟩ : ∃ k, j = i + k := ⟨j - i, by abel⟩
    rcases fin5_five k with rfl | rfl | rfl | rfl | rfl
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

/-- **`Hole4` from vertex degrees.** On a triangulation, with the link of `h` in rotation order,
`x t` of degree five for `t ≠ q`, `x q` of degree at least four, and no separating triangle
through `h`: `Hole4 P w q` for some outer ring `w`. -/
theorem hole4_of_degrees (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (rot : ∀ i : Fin 5, M.rotation.next ⟨(h, P.x i), P.adj_h i⟩ =
      ⟨(h, P.x (i + 1)), P.adj_h (i + 1)⟩)
    (q : Fin 5) (hq4 : 4 ≤ M.graph.degree (P.x q))
    (h5 : ∀ i, i ≠ q → M.graph.degree (P.x i) = 5) (hns : M.NoSeparatingTriangleAt h) :
    ∃ w : Fin 5 → Fin n, Hole4 P w q := by
  rcases hole4_or_linkClique_or_chord htri P rot q hq4 h5 with H | hcl | hch
  · exact H
  · exact absurd (hcl q (q + 2) (by
      have : ∀ t : Fin 5, t ≠ t + 2 := by decide
      exact this q))
      (not_adj_skip P rot hns q)
  · exact absurd hch.1 (not_adj_skip P rot hns q)

/-- On a triangulation, a link in rotation order with four degree-five vertices and the fifth of
degree at least five gives `PureClean`, when `h` has no separating triangle or the fifth degree
is at most six. -/
theorem pureClean_of_rotLink4 (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    (k : Fin 5) (hk : 5 ≤ M.graph.degree (L.port k))
    (h5 : ∀ i, i ≠ k → M.graph.degree (L.port i) = 5)
    (hns : M.NoSeparatingTriangleAt h ∨ M.graph.degree (L.port k) ≤ 6) : PureClean M h := by
  by_cases e5 : M.graph.degree (L.port k) = 5
  · refine pureClean_of_rotLink5 htri L ring rot (fun i => ?_)
    by_cases hi : i = k
    · rw [hi]; exact e5
    · exact h5 i hi
  by_cases e6 : M.graph.degree (L.port k) = 6
  · exact pureClean_of_rotLink6 htri L ring rot k e6 h5
  have hns' : M.NoSeparatingTriangleAt h := hns.resolve_right (by omega)
  let P' : Pent M.graph h :=
    ⟨L.port, port_adj M.graph L, ring, L.injective, fun v hv => (L.neighbours v).mp hv⟩
  obtain ⟨w, H⟩ := hole4_of_degrees (P := P') htri rot k (by change 4 ≤ M.graph.degree (L.port k); omega) h5 hns'
  exact pureClean_of_hole4 H

/-- **`PureClean` at every degree-five vertex with four consecutive degree-five neighbours.**
On a spherical triangulation, if the pentagonal hole `h` (link `P`, in any order; any four of
five link vertices are cyclically consecutive) has four link vertices of degree five and the
fifth `P.x q` of degree at least five, then every proper four-colouring of `M - h` reaches a
filled hole by pure Kempe swaps, provided `h` lies on no separating triangle or
`deg (P.x q) ≤ 6`. The clique case is vacuous (`no_properOff_of_linkClique`). Inside
Birkhoff-diamond territory: no bearing on a minimal counterexample. -/
theorem pureClean_of_four_consecutive_fives (htri : M.Triangulated) {h : Fin n}
    (P : Pent M.graph h) (q : Fin 5) (hq : 5 ≤ M.graph.degree (P.x q))
    (h5 : ∀ i, i ≠ q → M.graph.degree (P.x i) = 5)
    (hns : M.NoSeparatingTriangleAt h ∨ M.graph.degree (P.x q) ≤ 6) : PureClean M h := by
  classical
  let L0 : FiveLink M.graph h :=
    ⟨P.x, P.inj, fun v => ⟨P.only v, by rintro ⟨i, rfl⟩; exact P.adj_h i⟩⟩
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri L0
  obtain ⟨k, hk⟩ := (L.neighbours (P.x q)).mp (P.adj_h q)
  refine pureClean_of_rotLink4 htri L ring rot k (hk ▸ hq) (fun i hi => ?_) (hk ▸ hns)
  obtain ⟨j, e⟩ := P.only _ (port_adj M.graph L i)
  rw [e]
  refine h5 j (fun hj => hi (L.injective ?_))
  rw [e, hj, hk]

/-- **`PureClean` from link degrees, `(5,5,5,5,d)`.** At a degree-five vertex `h` with a
neighbour `p` of degree `d ≥ 5` and every other neighbour of degree five: `PureClean M h`, for
`d ∈ {5, 6}` unconditionally and for every `d ≥ 7` when `h` lies on no separating triangle. -/
theorem pureClean_of_linkDegrees' (htri : M.Triangulated) {h p : Fin n}
    (hdeg : M.graph.degree h = 5) (hp : M.Adj h p) (hp5 : 5 ≤ M.graph.degree p)
    (hlink : ∀ u, M.Adj h u → u ≠ p → M.graph.degree u = 5)
    (hns : M.NoSeparatingTriangleAt h ∨ M.graph.degree p ≤ 6) : PureClean M h := by
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri (M.linkOfDegree hdeg)
  obtain ⟨k, rfl⟩ := (L.neighbours p).mp hp
  exact pureClean_of_rotLink4 htri L ring rot k hp5
    (fun i hi => hlink _ (port_adj M.graph L i) (fun e => hi (L.injective e))) hns

/-- `NoSep` on a triangulation gives `NoSeparatingTriangleAt` at every vertex. -/
theorem noSeparatingTriangleAt_of_noSep {T : SphericalMap n} (htri : T.Triangulated)
    (hns : NoSep T) (v : Fin n) : T.NoSeparatingTriangleAt v := by
  intro u u' hu hu' huu'
  rcases hns v u u' hu huu' hu'.symm with f | f
  · -- `Nx T u v u'`: round the face, `Nx T v u' u`
    right
    obtain ⟨_, _, e⟩ := nx_dart (nx_tri htri f).2
    exact e
  · left
    obtain ⟨_, _, e⟩ := nx_dart f
    exact e

/-- **`CleanOff` from four consecutive degree-five neighbours** (`RStarCore` side). A
triangulation with no separating triangle and a degree-five vertex `v` off the protected face
`p q r` whose link degrees are `(5,5,5,5,d)`, `d ≥ 5`, satisfies `CleanOff T p q r`. Inside
Birkhoff-diamond territory: no bearing on a minimal counterexample. -/
theorem cleanOff_of_four_consecutive_fives {T : SphericalMap n} (htri : T.Triangulated)
    (hsep : NoSep T) {p q r v u : Fin n}
    (hvp : v ≠ p) (hvq : v ≠ q) (hvr : v ≠ r) (hdeg : T.graph.degree v = 5)
    (hu : T.Adj v u) (hu5 : 5 ≤ T.graph.degree u)
    (hlink : ∀ u', T.Adj v u' → u' ≠ u → T.graph.degree u' = 5) : CleanOff T p q r :=
  ⟨v, hvp, hvq, hvr, hdeg, pureClean_of_linkDegrees' htri hdeg hu hu5 hlink
    (Or.inl (noSeparatingTriangleAt_of_noSep htri hsep v))⟩

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.hole4_or_linkClique_or_chord
#print axioms SimpleGraph.QuarterFloor.hole4_of_degrees
#print axioms SimpleGraph.QuarterFloor.pureClean_of_four_consecutive_fives
#print axioms SimpleGraph.QuarterFloor.pureClean_of_linkDegrees'
#print axioms SimpleGraph.QuarterFloor.noSeparatingTriangleAt_of_noSep
#print axioms SimpleGraph.QuarterFloor.cleanOff_of_four_consecutive_fives
