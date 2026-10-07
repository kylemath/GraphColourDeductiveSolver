/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterHole6Clean
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFloorHBridge
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarCore

/-!
# `Hole6` from vertex degrees; `PureClean` at every `(5,5,5,5,6)` vertex

Discharges the local hypothesis `Hole6 P w m q` of `pureClean_of_hole6` (`QuarterHole6Clean`)
on a spherical triangulation from degree hypotheses alone, as `QuarterFloorHBridge` does for
`IcoBallP` (Theorem F5).

## Construction

List the link `x 0, …, x 4` of the degree-five vertex `h` in rotation order. The face on the
far side of the edge `x t x (t+1)` has third vertex `w t` (the rotation successor of `x t` at
`x (t+1)`). At a degree-five `x t` the rotation is `w t, x (t+1), h, x (t-1), w (t-1)`
(`chain5`); at the degree-six `x q` it is `w q, x (q+1), h, x (q-1), w (q-1), m`, and `m` is
the rotation successor of `w (q-1)` at `x q` (`hole6Bridge_chain6`). Faces give the ring
`w t ~ w (t+1)` (`t + 1 ≠ q`) and `w (q-1) ~ m ~ w q`.

All the off-link conditions follow from the rotations except `w t ≠ x (t+3)` and
`m ≠ x (q+2), x (q+3)`. No separating-triangle hypothesis is used: if `w s = x (s+3)` for some
`s` (or `m` is `x (q+2)` or `x (q+3)`, which forces `w (q+2) = x q`), the coincidence
propagates around the link (at degree-five `x (s+3)`: to `s+2` and `s+3`; at the degree-six
`x q`: from `s = q+2` to `q+4` or `q`), so it holds at every `s`, and then the link is a
5-clique of `G - h`, which has no proper four-colouring; `PureClean` holds vacuously.

## Main results (sorry-free, no new axioms)

* `hole6_or_linkClique`: on a triangulation, with the link in rotation order, `x q` of degree
  six and the others of degree five, either `Hole6 P w m q` for some `w`, `m`, or the link is a
  clique.
* `hole6_of_degrees`: the same, with the clique excluded by hypothesis, gives `Hole6 P w m q`.
* **`pureClean_of_degrees`**: `P : Pent M.graph h` in any order, one link vertex of degree six
  and the other four of degree five: `PureClean M h`.
* `pureClean_of_fiveLink`: the `(5,5,5,5,5)` case, from F5's bridge (`icoBall_or_linkClique`)
  and `pureClean_of_icoBall`.
* `pureClean_of_linkDegrees`: at a degree-five vertex `h` with a neighbour `p` of degree five or
  six and all other neighbours of degree five, `PureClean M h`.
* `cleanOff_of_degrees`: the `RStarCore`-side form: such a vertex off the protected face gives
  `CleanOff T p q r`. `rStarCore_of_linkDegrees`: R\* in the core **conditionally** on every
  core triangulation having such a vertex off the face.

## Scope

F5's bridge plus this bridge give `PureClean` at every degree-five vertex whose link degrees are
`(5,5,5,5,5)` or `(5,5,5,5,6)` (in some rotation), and nothing else yet from degrees alone: not
at `(5,5,5,6,6)` or any link with two vertices of degree at least six, and not the quarter
floor at `(5,5,5,5,6)`. (`QuarterHole6Gen` proves `PureClean` from the local hypotheses
`Hole4`/`Hole6Gen` for `(5,5,5,5,d)`, `d ≥ 6`; the degree-to-`Hole4` bridge for `d ≥ 7` is not
done here.) Not every minimum-degree-five triangulation has such a vertex, so
`rStarCore_of_linkDegrees` is conditional and is not R\*.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral SphericalMap

variable {n : ℕ} {M : SphericalMap n}

/-- At a vertex of degree six the rotation is a single six-cycle of darts. -/
private lemma hole6Bridge_orbit6 {v : Fin n} (hv : M.graph.degree v = 6) (d : M.Dart)
    (hd : d.fst = v) :
    (⇑M.rotation.next)^[6] d = d ∧
    (∀ i j : ℕ, i < 6 → j < 6 →
      (⇑M.rotation.next)^[i] d = (⇑M.rotation.next)^[j] d → i = j) ∧
    (∀ e : M.Dart, e.fst = v → ∃ k, k < 6 ∧ (⇑M.rotation.next)^[k] d = e) := by
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
  have hp : Function.minimalPeriod σ w = 6 := by
    rw [R.neighbor_period_eq_degree, hv]
  refine ⟨?_, ?_, ?_⟩
  · rw [hit, ← hp, Function.iterate_minimalPeriod, hdw]
  · intro i j hi hj hij
    rw [hit, hit] at hij
    exact Function.iterate_injOn_Iio_minimalPeriod (by rw [hp]; exact hi) (by rw [hp]; exact hj)
      (M.graph.dartOfNeighborSet_injective _ hij)
  · intro e he
    obtain ⟨k, hk⟩ := R.neighbor_rotation_cyclic d.fst w ⟨e.snd, by rw [← he]; exact e.adj⟩
    refine ⟨k % 6, Nat.mod_lt _ (by norm_num), ?_⟩
    rw [hit, ← hp, Function.iterate_mod_minimalPeriod_eq, hk]
    exact (by apply Dart.ext; exact Prod.ext he.symm rfl)

/-- A rotation chain of five steps at a degree-six vertex closes up, and lists every neighbour
exactly once. -/
lemma hole6Bridge_chain6 {v a0 a1 a2 a3 a4 a5 : Fin n} (hv : M.graph.degree v = 6)
    (h01 : Nx M v a0 a1) (h12 : Nx M v a1 a2) (h23 : Nx M v a2 a3) (h34 : Nx M v a3 a4)
    (h45 : Nx M v a4 a5) :
    Nx M v a5 a0 ∧
      (∀ i j : Fin 6, i ≠ j → ![a0, a1, a2, a3, a4, a5] i ≠ ![a0, a1, a2, a3, a4, a5] j) ∧
      ∀ u, M.Adj v u → u = a0 ∨ u = a1 ∨ u = a2 ∨ u = a3 ∨ u = a4 ∨ u = a5 := by
  obtain ⟨g0, g1, e01⟩ := nx_dart h01
  obtain ⟨_g1, g2, e12⟩ := nx_dart h12
  obtain ⟨_g2, g3, e23⟩ := nx_dart h23
  obtain ⟨_g3, g4, e34⟩ := nx_dart h34
  obtain ⟨_g4, g5, e45⟩ := nx_dart h45
  let D : M.Dart := ⟨(v,a0),g0⟩
  obtain ⟨p6, inj, surj⟩ := hole6Bridge_orbit6 hv D rfl
  have i1 : (⇑M.rotation.next)^[1] D = ⟨(v,a1),g1⟩ := e01
  have i2 : (⇑M.rotation.next)^[2] D = ⟨(v,a2),g2⟩ := by
    rw [Function.iterate_succ_apply', i1]; exact e12
  have i3 : (⇑M.rotation.next)^[3] D = ⟨(v,a3),g3⟩ := by
    rw [Function.iterate_succ_apply', i2]; exact e23
  have i4 : (⇑M.rotation.next)^[4] D = ⟨(v,a4),g4⟩ := by
    rw [Function.iterate_succ_apply', i3]; exact e34
  have i5 : (⇑M.rotation.next)^[5] D = ⟨(v,a5),g5⟩ := by
    rw [Function.iterate_succ_apply', i4]; exact e45
  have i0 : (⇑M.rotation.next)^[0] D = ⟨(v,a0),g0⟩ := rfl
  have close : M.rotation.next ⟨(v,a5),g5⟩ = ⟨(v,a0),g0⟩ := by
    rw [← i5, ← Function.iterate_succ_apply' (⇑M.rotation.next) 5]; exact p6
  have fstI : ∀ (k : ℕ) (d : M.Dart), ((⇑M.rotation.next)^[k] d).fst = d.fst := by
    intro k
    induction k with
    | zero => intro d; rfl
    | succ k ih => intro d; rw [Function.iterate_succ_apply', M.rotation.next_fst, ih]
  have s : ∀ i : Fin 6,
      ((⇑M.rotation.next)^[i.val] D).snd = ![a0, a1, a2, a3, a4, a5] i := by
    intro i
    fin_cases i
    · exact congrArg (fun d : M.Dart => d.snd) i0
    · exact congrArg (fun d : M.Dart => d.snd) i1
    · exact congrArg (fun d : M.Dart => d.snd) i2
    · exact congrArg (fun d : M.Dart => d.snd) i3
    · exact congrArg (fun d : M.Dart => d.snd) i4
    · exact congrArg (fun d : M.Dart => d.snd) i5
  refine ⟨nx_of_dart close, ?_, ?_⟩
  · intro i j hij hs
    apply hij
    rw [← s, ← s] at hs
    apply Fin.ext
    apply inj i.val j.val i.isLt j.isLt
    apply Dart.ext
    apply Prod.ext
    · rw [fstI, fstI]
    · exact hs
  · intro u hu
    obtain ⟨k, hk, e⟩ := surj ⟨(v,u),hu⟩ rfl
    have hs := congrArg (fun d : M.Dart => d.snd) e
    interval_cases k
    · left; rw [i0] at hs; exact hs.symm
    · right; left; rw [i1] at hs; exact hs.symm
    · right; right; left; rw [i2] at hs; exact hs.symm
    · right; right; right; left; rw [i3] at hs; exact hs.symm
    · right; right; right; right; left; rw [i4] at hs; exact hs.symm
    · right; right; right; right; right; rw [i5] at hs; exact hs.symm

/-- Propagation of `w s = x (s+3)` around the link: from `s ≠ q + 2` to `s + 2`, `s + 3`; from
`q + 2` to `q + 4` or `q`. Any one coincidence then gives all five. -/
private lemma hole6Bridge_closure : ∀ (q : Fin 5) (b : Fin 5 → Bool),
    (∀ s, s + 3 ≠ q → b s = true → b (s + 2) = true ∧ b (s + 3) = true) →
    (b (q + 2) = true → b (q + 4) = true ∨ b q = true) →
    ∀ s t, b s = true → b t = true := by
  decide

private lemma hole6Bridge_ne : ∀ (t a : Fin 5), a ≠ 0 → t ≠ t + a := by decide

/-- A link that is a clique of `G - h` admits no proper four-colouring off `h`. -/
theorem no_properOff_of_linkClique {h : Fin n} (P : Pent M.graph h)
    (hcl : ∀ i j, i ≠ j → M.graph.Adj (P.x i) (P.x j)) {c : Fin n → Fin 4}
    (hc : ProperOff M.graph h c) : False := by
  have inj : Function.Injective (fun i => c (P.x i)) := by
    intro i j e
    by_contra hij
    exact hc (hcl i j hij) (P.x_ne_h i) (P.x_ne_h j) e
  have := Fintype.card_le_of_injective _ inj
  simp at this

/-- **The `(5,5,5,5,6)` two-ball dichotomy.** On a triangulation, with the link of `h` in
rotation order, `x q` of degree six and the other link vertices of degree five, either
`Hole6 P w m q` holds for some outer ring `w` and inserted vertex `m`, or the five link
vertices are pairwise adjacent. No separating-triangle hypothesis. -/
theorem hole6_or_linkClique (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (rot : ∀ i : Fin 5, M.rotation.next ⟨(h, P.x i), P.adj_h i⟩ =
      ⟨(h, P.x (i + 1)), P.adj_h (i + 1)⟩)
    (q : Fin 5) (h6 : M.graph.degree (P.x q) = 6)
    (h5 : ∀ i, i ≠ q → M.graph.degree (P.x i) = 5) :
    (∃ (w : Fin 5 → Fin n) (m : Fin n), Hole6 P w m q) ∨
      ∀ i j, i ≠ j → M.graph.Adj (P.x i) (P.x j) := by
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
  obtain ⟨m, Hm⟩ : ∃ m, Nx M (P.x q) (w (q+4)) m := ⟨_, nx_adj_right (W' q), rfl⟩
  have C6 := hole6Bridge_chain6 h6 (B2 q) (A2 q) (A1' q) (W' q) Hm
  have c02 : w q ≠ h := C6.2.1 0 2 (by decide)
  have c03 : w q ≠ P.x (q+4) := C6.2.1 0 3 (by decide)
  have c14 : P.x (q+1) ≠ w (q+4) := C6.2.1 1 4 (by decide)
  have c52 : m ≠ h := C6.2.1 5 2 (by decide)
  have c51 : m ≠ P.x (q+1) := C6.2.1 5 1 (by decide)
  have c53 : m ≠ P.x (q+4) := C6.2.1 5 3 (by decide)
  have hne : ∀ i j, i ≠ j → P.x i ≠ P.x j := fun i j hij e => hij (P.inj e)
  have adjw : ∀ t, M.Adj (P.x t) (w t) := fun t => nx_adj_left (B2 t)
  have adjw1 : ∀ t, M.Adj (P.x (t+1)) (w t) := fun t => nx_adj_right (W t)
  have adjm : M.Adj (P.x q) m := nx_adj_right Hm
  have Dh : ∀ t, w t ≠ h := fun t => by
    by_cases ht : t = q
    · subst ht; exact c02
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
  -- (i) at a degree-five `x (s+3)` the coincidence `w s = x (s+3)` propagates
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
  -- (ii) at the degree-six `x q`: from `q + 2` to `q + 4` or `q`
  have stepq : w (q+2) = P.x (q+2+3) → w (q+4) = P.x (q+4+3) ∨ w q = P.x (q+3) := by
    intro hb
    have f1 : q + 2 + 3 = q := by
      have : ∀ t : Fin 5, t + 2 + 3 = t := by decide
      exact this q
    have f2 : q + 4 + 3 = q + 2 := by
      have : ∀ t : Fin 5, t + 4 + 3 = t + 2 := by decide
      exact this q
    have f3 : q + 2 + 1 = q + 3 := by
      have : ∀ t : Fin 5, t + 2 + 1 = t + 3 := by decide
      exact this q
    have f4 : q + 4 + 4 = q + 3 := by
      have : ∀ t : Fin 5, t + 4 + 4 = t + 3 := by decide
      exact this q
    rw [f1] at hb
    rw [f2]
    have a2 : M.Adj (P.x q) (P.x (q+2)) := hb ▸ (adjw (q+2)).symm
    have a3 : M.Adj (P.x q) (P.x (q+3)) := by
      have := (adjw1 (q+2)).symm; rw [hb, f3] at this; exact this
    have d43 := D4 (q+4)
    rw [f4] at d43
    have nb : ∀ a : Fin 5, a ≠ 0 → a ≠ 1 → a ≠ 4 →
        P.x (q+a) = w (q+4) ∨ P.x (q+a) = m ∨ P.x (q+a) = w q := by
      intro a a0 a1 a4
      have : M.Adj (P.x q) (P.x (q+a)) := by
        have ha : a = 2 ∨ a = 3 := by revert a; decide
        rcases ha with rfl | rfl
        · exact a2
        · exact a3
      rcases C6.2.2 _ this with e | e | e | e | e | e
      · exact Or.inr (Or.inr e)
      · exact absurd e (hne _ _ (fun e' => a1 (add_left_cancel e')))
      · exact absurd e (P.x_ne_h _)
      · exact absurd e (hne _ _ (fun e' => a4 (add_left_cancel e')))
      · exact Or.inl e
      · exact Or.inr (Or.inl e)
    rcases nb 2 (by decide) (by decide) (by decide) with e2 | e2 | e2
    · exact Or.inl e2.symm
    · rcases nb 3 (by decide) (by decide) (by decide) with e3 | e3 | e3
      · exact absurd e3.symm d43
      · exact absurd (e2.trans e3.symm) (hne _ _ (fun e' => by
          have := add_left_cancel e'; exact absurd this (by decide)))
      · exact Or.inr e3.symm
    · exact absurd e2.symm (D2 q)
  -- (iii) `m = x (q+2)` or `m = x (q+3)` forces `w (q+2) = x q`
  have mq : ∀ a : Fin 5, (a = 2 ∨ a = 3) → m = P.x (q+a) → w (q+2) = P.x (q+2+3) := by
    have f1 : q + 2 + 3 = q := by
      have : ∀ t : Fin 5, t + 2 + 3 = t := by decide
      exact this q
    rw [f1]
    have hq2 : q + 2 ≠ q := fun e => hole6Bridge_ne q 2 (by decide) e.symm
    have hq3 : q + 3 ≠ q := fun e => hole6Bridge_ne q 3 (by decide) e.symm
    rintro a (rfl | rfl) e
    · have a0 : M.Adj (P.x (q+2)) (P.x q) := (e ▸ adjm).symm
      rcases (C (q+2) hq2).2.2 _ a0 with e' | e' | e' | e' | e'
      · exact e'.symm
      · exact absurd e' (hne _ _ (by
          have : ∀ t : Fin 5, t ≠ t + 2 + 1 := by decide
          exact this q))
      · exact absurd e' (P.x_ne_h _)
      · exact absurd e' (hne _ _ (by
          have : ∀ t : Fin 5, t ≠ t + 2 + 4 := by decide
          exact this q))
      · exfalso
        have := D4 (q+1)
        rw [show q + 2 + 4 = q + 1 from (by
          have : ∀ t : Fin 5, t + 2 + 4 = t + 1 := by decide
          exact this q), show q + 1 + 4 = q from i14 q] at *
        exact this e'.symm
    · have a0 : M.Adj (P.x (q+3)) (P.x q) := (e ▸ adjm).symm
      rcases (C (q+3) hq3).2.2 _ a0 with e' | e' | e' | e' | e'
      · exfalso
        have := D2 (q+3)
        rw [show q + 3 + 2 = q from (by
          have : ∀ t : Fin 5, t + 3 + 2 = t := by decide
          exact this q)] at this
        exact this e'.symm
      · exact absurd e' (hne _ _ (by
          have : ∀ t : Fin 5, t ≠ t + 3 + 1 := by decide
          exact this q))
      · exact absurd e' (P.x_ne_h _)
      · exact absurd e' (hne _ _ (by
          have : ∀ t : Fin 5, t ≠ t + 3 + 4 := by decide
          exact this q))
      · rw [show q + 3 + 4 = q + 2 from (by
          have : ∀ t : Fin 5, t + 3 + 4 = t + 2 := by decide
          exact this q)] at e'
        exact e'.symm
  by_cases hsep : ∀ t, w t ≠ P.x (t+3)
  · left
    refine ⟨w, m, ⟨fun t ht u => ⟨fun hu => ?_, fun hu => ?_⟩, fun u => ⟨fun hu => ?_, fun hu => ?_⟩,
      fun t ht => ?_, ?_, ?_, fun t i => ?_, fun i => ?_, Dh, c52⟩⟩
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
    · rcases C6.2.2 u hu with e | e | e | e | e | e
      · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr e))))
      · exact Or.inr (Or.inr (Or.inl e))
      · exact Or.inl e
      · exact Or.inr (Or.inl e)
      · exact Or.inr (Or.inr (Or.inr (Or.inl e)))
      · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl e))))
    · rcases hu with rfl | rfl | rfl | rfl | rfl | rfl
      · exact (P.adj_h q).symm
      · exact nx_adj_right (A1' q)
      · exact ring q
      · exact nx_adj_right (W' q)
      · exact adjm
      · exact adjw q
    · have h1 := (C (t+1) ht).1
      rw [i14] at h1
      exact (nx_adj_right (nx_tri htri h1).1).symm
    · exact nx_adj_left (nx_tri htri Hm).2
    · exact nx_adj_left (nx_tri htri C6.1).2
    · obtain ⟨j, rfl⟩ : ∃ j, i = t + j := ⟨i - t, by abel⟩
      intro e
      rcases fin5_five j with rfl | rfl | rfl | rfl | rfl
      · rw [add_zero] at e
        exact (adjw t).ne e.symm
      · exact (adjw1 t).ne e.symm
      · exact D2 t e
      · exact hsep t e
      · exact D4 t e
    · obtain ⟨j, rfl⟩ : ∃ j, i = q + j := ⟨i - q, by abel⟩
      intro e
      rcases fin5_five j with rfl | rfl | rfl | rfl | rfl
      · rw [add_zero] at e
        exact adjm.ne e.symm
      · exact c51 e
      · exact hsep _ (mq 2 (Or.inl rfl) e)
      · exact hsep _ (mq 3 (Or.inr rfl) e)
      · exact c53 e
  · right
    push Not at hsep
    obtain ⟨t₀, ht₀⟩ := hsep
    have all : ∀ s, w s = P.x (s+3) := by
      let b : Fin 5 → Bool := fun s => decide (w s = P.x (s+3))
      have hb : ∀ s, b s = true ↔ w s = P.x (s+3) := fun s => decide_eq_true_iff
      have cl := hole6Bridge_closure q b
        (fun s hq hs => by
          rw [hb] at hs
          have := step s hq hs
          exact ⟨(hb _).2 this.1, (hb _).2 this.2⟩)
        (fun hs => by
          rw [hb] at hs
          rcases stepq hs with e | e
          · exact Or.inl ((hb _).2 e)
          · exact Or.inr ((hb _).2 e))
      intro s
      exact (hb s).1 (cl t₀ s ((hb t₀).2 ht₀))
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

/-- **`Hole6` from vertex degrees.** On a triangulation, with the link of `h` listed in
rotation order, `x q` of degree six and the other four link vertices of degree five, and the
link not a clique (automatic when `M - h` has a proper four-colouring; on a genuinely planar
map it is never a clique), there are an outer ring `w` and an inserted vertex `m` with
`Hole6 P w m q`. -/
theorem hole6_of_degrees (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (rot : ∀ i : Fin 5, M.rotation.next ⟨(h, P.x i), P.adj_h i⟩ =
      ⟨(h, P.x (i + 1)), P.adj_h (i + 1)⟩)
    (q : Fin 5) (h6 : M.graph.degree (P.x q) = 6)
    (h5 : ∀ i, i ≠ q → M.graph.degree (P.x i) = 5)
    (hncl : ¬ ∀ i j, i ≠ j → M.graph.Adj (P.x i) (P.x j)) :
    ∃ (w : Fin 5 → Fin n) (m : Fin n), Hole6 P w m q :=
  (hole6_or_linkClique htri P rot q h6 h5).resolve_right hncl

/-- On a triangulation, a link listed in rotation order with degrees `(5,5,5,5,6)` gives
`PureClean`. -/
theorem pureClean_of_rotLink6 (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    (k : Fin 5) (h6 : M.graph.degree (L.port k) = 6)
    (h5 : ∀ i, i ≠ k → M.graph.degree (L.port i) = 5) : PureClean M h := by
  let P' : Pent M.graph h :=
    ⟨L.port, port_adj M.graph L, ring, L.injective, fun v hv => (L.neighbours v).mp hv⟩
  rcases hole6_or_linkClique (P := P') htri rot k h6 h5 with ⟨w, m, H⟩ | hcl
  · exact pureClean_of_hole6 H
  · exact fun c hc => (no_properOff_of_linkClique P' hcl hc).elim

/-- On a triangulation, a link listed in rotation order with degrees `(5,5,5,5,5)` gives
`PureClean` (F5's bridge `icoBall_or_linkClique` with `pureClean_of_icoBall`). -/
theorem pureClean_of_rotLink5 (htri : M.Triangulated) {h : Fin n} (L : FiveLink M.graph h)
    (ring : ∀ i : Fin 5, M.graph.Adj (L.port i) (L.port (i+1)))
    (rot : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),port_adj M.graph L (i+1)⟩)
    (h5 : ∀ i, M.graph.degree (L.port i) = 5) : PureClean M h := by
  let P' : Pent M.graph h :=
    ⟨L.port, port_adj M.graph L, ring, L.injective, fun v hv => (L.neighbours v).mp hv⟩
  rcases icoBall_or_linkClique htri L ring rot h5 with ⟨w, B⟩ | hcl
  · exact pureClean_of_icoBall (P := P') (w := w) ⟨B.nbr, B.ring, B.off, B.offh⟩
  · exact fun c hc => (no_properOff_of_linkClique P' hcl hc).elim

/-- **`PureClean` at a `(5,5,5,5,6)` hole, from degrees.** On a spherical triangulation, if the
pentagonal hole `h` (link `P`, in any order) has one link vertex `P.x q` of degree six and the
other four of degree five, then every proper four-colouring of `M - h` reaches a filled hole
by pure Kempe swaps. No separating-triangle hypothesis. -/
theorem pureClean_of_degrees (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (q : Fin 5) (h6 : M.graph.degree (P.x q) = 6)
    (h5 : ∀ i, i ≠ q → M.graph.degree (P.x i) = 5) : PureClean M h := by
  classical
  let L0 : FiveLink M.graph h :=
    ⟨P.x, P.inj, fun v => ⟨P.only v, by rintro ⟨i, rfl⟩; exact P.adj_h i⟩⟩
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri L0
  obtain ⟨k, hk⟩ := (L.neighbours (P.x q)).mp (P.adj_h q)
  refine pureClean_of_rotLink6 htri L ring rot k (hk ▸ h6) (fun i hi => ?_)
  obtain ⟨j, e⟩ := P.only _ (port_adj M.graph L i)
  rw [e]
  refine h5 j (fun hj => hi (L.injective ?_))
  rw [e, hj, hk]

/-- The `(5,5,5,5,5)` case from degrees, any order (F5's bridge). -/
theorem pureClean_of_fiveLink (htri : M.Triangulated) {h : Fin n} (P : Pent M.graph h)
    (hdeg : ∀ i, M.graph.degree (P.x i) = 5) : PureClean M h := by
  classical
  let L0 : FiveLink M.graph h :=
    ⟨P.x, P.inj, fun v => ⟨P.only v, by rintro ⟨i, rfl⟩; exact P.adj_h i⟩⟩
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri L0
  refine pureClean_of_rotLink5 htri L ring rot (fun i => ?_)
  obtain ⟨j, e⟩ := P.only _ (port_adj M.graph L i)
  rw [e]; exact hdeg j

/-- **`PureClean` from link degrees.** At a degree-five vertex `h` of a spherical triangulation
with a neighbour `p` of degree five or six and every other neighbour of degree five (link
degrees `(5,5,5,5,5)` or `(5,5,5,5,6)`), `PureClean M h`. -/
theorem pureClean_of_linkDegrees (htri : M.Triangulated) {h p : Fin n}
    (hdeg : M.graph.degree h = 5) (hp : M.Adj h p)
    (hp56 : M.graph.degree p = 5 ∨ M.graph.degree p = 6)
    (hlink : ∀ u, M.Adj h u → u ≠ p → M.graph.degree u = 5) : PureClean M h := by
  obtain ⟨L, ring, rot⟩ := M.exists_rotation_link htri (M.linkOfDegree hdeg)
  obtain ⟨k, rfl⟩ := (L.neighbours p).mp hp
  have h5 : ∀ i, i ≠ k → M.graph.degree (L.port i) = 5 := fun i hi =>
    hlink _ (port_adj M.graph L i) (fun e => hi (L.injective e))
  rcases hp56 with e | e
  · refine pureClean_of_rotLink5 htri L ring rot (fun i => ?_)
    by_cases hi : i = k
    · rw [hi]; exact e
    · exact h5 i hi
  · exact pureClean_of_rotLink6 htri L ring rot k e h5

/-- **`CleanOff` from link degrees** (`RStarCore` side). A triangulation with a degree-five
vertex `v` off the protected face `p q r` whose link degrees are `(5,5,5,5,5)` or `(5,5,5,5,6)`
satisfies `CleanOff T p q r`. -/
theorem cleanOff_of_degrees {T : SphericalMap n} (htri : T.Triangulated) {p q r v u : Fin n}
    (hvp : v ≠ p) (hvq : v ≠ q) (hvr : v ≠ r) (hdeg : T.graph.degree v = 5)
    (hu : T.Adj v u) (hu56 : T.graph.degree u = 5 ∨ T.graph.degree u = 6)
    (hlink : ∀ u', T.Adj v u' → u' ≠ u → T.graph.degree u' = 5) : CleanOff T p q r :=
  ⟨v, hvp, hvq, hvr, hdeg, pureClean_of_linkDegrees htri hdeg hu hu56 hlink⟩

/-- `RStarCore`, **conditionally**: if every core triangulation (as in `RStarCore`) has a
degree-five vertex off the protected face with link degrees `(5,5,5,5,5)` or `(5,5,5,5,6)`.
Not every triangulation has one, so this is not R\*. -/
theorem rStarCore_of_linkDegrees
    (H : ∀ (m : ℕ) (T : SphericalMap m) (p q r : Fin m), T.graph.Connected → T.Triangulated →
      T.Adj p q → T.Adj q r → T.Adj r p → Facial T p q r → NoSep T →
      (∀ x, x ≠ p → x ≠ q → x ≠ r → 5 ≤ T.graph.degree x) →
      ∃ v u, v ≠ p ∧ v ≠ q ∧ v ≠ r ∧ T.graph.degree v = 5 ∧ T.Adj v u ∧
        (T.graph.degree u = 5 ∨ T.graph.degree u = 6) ∧
        ∀ u', T.Adj v u' → u' ≠ u → T.graph.degree u' = 5) :
    RStarCore := by
  intro m T p q r hconn htri hpq hqr hrp hf hns hdeg
  obtain ⟨v, u, hvp, hvq, hvr, hv, hu, hu56, hl⟩ := H m T p q r hconn htri hpq hqr hrp hf hns hdeg
  exact cleanOff_of_degrees htri hvp hvq hvr hv hu hu56 hl

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.hole6_or_linkClique
#print axioms SimpleGraph.QuarterFloor.hole6_of_degrees
#print axioms SimpleGraph.QuarterFloor.pureClean_of_degrees
#print axioms SimpleGraph.QuarterFloor.pureClean_of_fiveLink
#print axioms SimpleGraph.QuarterFloor.pureClean_of_linkDegrees
#print axioms SimpleGraph.QuarterFloor.cleanOff_of_degrees
#print axioms SimpleGraph.QuarterFloor.rStarCore_of_linkDegrees
