/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterNonDLImage
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPeriodJ

/-!
# Every Kempe class at a `(5,5,5,5,6)` hole has a filled state (weak F6)

Assembles the night's library into the weak, R\*-type form of F6: at a pentagonal hole `h`
satisfying `Hole6 P w m q` (`QuarterGammaPeriod`), every Kempe class of proper colourings of
`M - h` contains a filled state, i.e. `PureClean M h`.

## The argument

A class with no filled state is all-`DL` (`allDL_of_targetless`, Lemma C1). Take any `π`-orbit
in it; it is an all-`DL` orbit. Some state among the first two has a type `R1`/`R3`
(`untyped_dd`: an untyped `DD` state at `k ∈ {0, 4}` does not exist, at `k = 1` its image is
`R3`, at `k ∈ {2, 3}` its image is untyped at `k ∈ {4, 0}`). From a typed state `tk_step`
walks the ten `(type, k)` values, so the orbit reaches an `R1k2` state `r`; then `π r` is an
`R3k4` state whose pair fact (`pair_R3k4_of_pred`) completes the `R3` ring (`r3k4_R3At`),
`Hole6.k4Ball` gives the `K4Ball`, and `sigma_exit_not_DL_k4` says `σ (π r)` is not `DL`.
This is `GammaImages P`, and `QuarterNonDLImage` turns it into `PureClean M h`.

## Main results (sorry-free, no new axioms)

* `untyped_dd`, `typed_in_orbit`: every all-`DL` orbit at a `Hole6` has a typed state.
* `gammaImages_of_hole6`: `Hole6 P w m q → GammaImages P`.
* `every_class_filled_of_hole6`, `pureClean_of_hole6`: every class at a `Hole6` hole has a
  filled state; `PureClean M h`.
* `gammaImages_of_icoBall`, `pureClean_of_icoBall`: the same at an icosahedral `(5,5,5,5,5)`
  hole (`IcoBallP`), from `dd_r3` and `sigSwap_spec` (weaker than F5, which already gives the
  quarter floor there).
* `rStarNoSepTri_of_hole6`: the conditional bridge to `RStarNoSepTri`.

## What this does NOT give

* Not the quarter floor (`QuarterFloorConj`) at a `(5,5,5,5,6)` hole: only "at least one
  filled state per class", not "at least a quarter filled".
* Not R\* for all triangulations: the hypothesis `Hole6 P w m q` is local (exact neighbour lists
  of the five link vertices: four of degree five, `x q` of degree six with outer path
  `w (q-1), m, w q`, ring edges, `w`, `m` off the link and off `h`). Not every minimum-degree-five
  triangulation has a degree-five vertex with such a link, so `rStarNoSepTri_of_hole6` is
  conditional. The derivation of `Hole6` from degrees on a triangulation (as
  `quarterFloor_of_fiveLink` does for `IcoBallP`) is not done here.
* Not `(5,5,5,6,6)` or `(5,5,5,5,7)`: `K4Ball` needs `x j, …, x (j+3)` of degree five and
  `x (j+4)` of degree exactly six (neighbours `h, x (j+3), x j, w (j+3), m, w (j+4)`); `K3Ball`
  needs `x j, x (j+1), x (j+2), x (j+4)` of degree five and `x (j+3)` of degree exactly six.
  Both thus need the `(5,5,5,5,6)` link; `Hole6` and `tk_step` also assume it.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

private lemma gstep_to_R1k2 : ∀ t : GType, ∀ k : Fin 5, ∃ d, d < 10 ∧ gstep^[d] (t, k) = (.R1, 2) := by
  intro t; cases t <;> decide

private lemma q_two_three : ∀ j q : Fin 5, (q = j + 2 ∨ q = j + 3) →
    (q = j + 3 + 1 ∨ q = j + 3 + 2 ∨ q = j + 3 + 3) → False := by decide

private lemma q_k4 : ∀ j : Fin 5, j + 2 = j + 3 + 4 := by decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

/-- An untyped `DD` state at a `Hole6` hole (neither `TypeR1` nor `TypeR3`, i.e. `w j = B` and
`w (j+3) = α`): the degree-six vertex is at `k = 1` and the image is `R3`, or at `k ∈ {2, 3}`.
(At `k ∈ {0, 4}`, Lock 2 of the image has no `B`-end at `x (j+2)`.) -/
theorem untyped_dd (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (n1 : ¬ TypeR1 P w c j) (n3 : ¬ TypeR3 P w c j) :
    (q = j + 1 ∧ TypeR3 P w (piMove P c) (j + 3)) ∨ q = j + 2 ∨ q = j + 3 := by
  obtain ⟨hπ, hr, hK, ⟨u', hu', hu'h, hcu'⟩, ⟨u, hu, huh, hcu⟩, -⟩ := dd_ends hc hD
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨d0, d0'⟩ := H.dom hc j
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  have a0 : c (w j) = c (P.x (j + 4)) := by
    unfold TypeR1 at n1
    clear * - h1 h3 h4 h13 h14 h34 h02 d0 d0' n1; omega
  have a3 : c (w (j + 3)) = c (P.x j) := by
    have n3' : c (w (j + 3)) ≠ c (P.x (j + 1)) := fun e => n3 ⟨a0, e⟩
    clear * - h1 h3 h4 h13 h14 h34 h02 d3 d3' n3'; omega
  -- outside `k ∈ {2, 3}`: the Lock 1 end gives `w (j+2) = μ`, the image's Lock 2 end `w (j+1) = B`
  have core : j + 3 ≠ q → j + 2 ≠ q → c (w (j + 1)) = c (P.x (j + 4)) := by
    intro hq3 hq2
    have w2 : c (w (j + 2)) = c (P.x (j + 1)) := by
      have n3' := (H.nbr (j + 3) hq3 u').1 hu'
      simp only [add_assoc, Fin.reduceAdd] at n3'
      rcases n3' with rfl | rfl | rfl | rfl | rfl
      · exact (hu'h rfl).elim
      · exact (h1 (hcu'.symm.trans h02.symm)).elim
      · exact (h14 hcu'.symm).elim
      · exact hcu'
      · exact (h1 (hcu'.symm.trans a3)).elim
    by_contra hne
    have hA : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' hne; omega
    have n2 := (H.nbr (j + 2) hq2 u).1 hu
    simp only [add_assoc, Fin.reduceAdd] at n2
    rcases n2 with rfl | rfl | rfl | rfl | rfl
    · exact huh rfl
    · rw [v1] at hcu; exact h14 hcu
    · rw [v3] at hcu; exact h4 hcu.symm
    · have e := H.adj_w' (j + 1)
      simp only [add_assoc, Fin.reduceAdd] at e
      rw [rot3_K2 hr' e (H.offh _) (Or.inr hA), hA, Equiv.swap_apply_right] at hcu
      exact h4 hcu.symm
    · rw [rot3_keep (by rw [w2]; exact h1) (by rw [w2]; exact h13), w2] at hcu
      exact h14 hcu
  have hq : q = j + (q - j) := (add_sub_cancel j q).symm
  rcases fin5_five (q - j) with hk | hk | hk | hk | hk <;> rw [hk] at hq <;> subst hq
  · exact absurd (a0.trans (core (fin5_ne (by decide)) (fin5_ne (by decide))).symm)
      (H.ring0 hc (fin5_ne (by decide)))
  · refine Or.inl ⟨rfl, ?_⟩
    have w1 := core (fin5_ne (by decide)) (fin5_ne (by decide))
    obtain ⟨-, -, v2, -, v4⟩ := rot3_values hr' hK
    unfold TypeR3
    simp only [add_assoc, Fin.reduceAdd, hπ]
    refine ⟨?_, ?_⟩
    · rw [v2, rot3_K3 hr' (H.adj_w (j + 3)) (H.offh _) (Or.inl a3), a3, Equiv.swap_apply_left]
    · rw [v4, rot3_keep (by rw [w1]; exact h4) (by rw [w1]; exact h34.symm), w1]
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)
  · exact absurd (a0.trans (core (fin5_ne (by decide)) (fin5_ne (by decide))).symm)
      (H.ring0 hc (fin5_ne (by decide)))

/-- On an all-`DL` forward orbit every doubly locked state is a `DD` state. -/
lemma allDL_orbit_dd {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ k, DLState P ((piMove P)^[k] s)) (N : ℕ) (j : Fin 5)
    (hd : DoublyLocked P ((piMove P)^[N] s) j) : DDstate P ((piMove P)^[N] s) j := by
  obtain ⟨-, -, r', -, -⟩ := rot3_move (iter_proper hc N) hd.1 hd.2.2
  have hπ : piMove P ((piMove P)^[N] s) = rot3 P ((piMove P)^[N] s) j := by
    rw [piMove_rep hd.1, ite_eq_left hd.2.2]
  rw [← hπ] at r'
  have h1 := hall (N + 1)
  rw [Function.iterate_succ_apply'] at h1
  exact ⟨hd, r', (dl_rep r').1 h1⟩

lemma hasTK_of_dl (hd : DoublyLocked P c j) (t : GType) (hT : TypeOf P w t c j) :
    HasTK P w q c t (q - j) :=
  ⟨j, hd, (add_sub_cancel j q).symm, hT⟩

/-- Every all-`DL` orbit at a `Hole6` hole has a typed state (`R1` or `R3`), among its first two
states. -/
theorem typed_in_orbit (H : Hole6 P w m q) {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ k, DLState P ((piMove P)^[k] s)) :
    ∃ N t k, HasTK P w q ((piMove P)^[N] s) t k := by
  obtain ⟨j, hd⟩ := hall 0
  have D0 := allDL_orbit_dd hc hall 0 j hd
  by_cases t1 : TypeR1 P w s j
  · exact ⟨0, .R1, _, hasTK_of_dl hd .R1 t1⟩
  by_cases t3 : TypeR3 P w s j
  · exact ⟨0, .R3, _, hasTK_of_dl hd .R3 t3⟩
  have D1 : DDstate P ((piMove P)^[1] s) (j + 3) := allDL_orbit_dd hc hall 1 _ D0.2
  rcases untyped_dd H hc D0 t1 t3 with ⟨-, hT⟩ | h23
  · exact ⟨1, .R3, _, hasTK_of_dl D0.2 .R3 hT⟩
  by_cases t1' : TypeR1 P w ((piMove P)^[1] s) (j + 3)
  · exact ⟨1, .R1, _, hasTK_of_dl D0.2 .R1 t1'⟩
  by_cases t3' : TypeR3 P w ((piMove P)^[1] s) (j + 3)
  · exact ⟨1, .R3, _, hasTK_of_dl D0.2 .R3 t3'⟩
  exfalso
  refine q_two_three j q h23 ?_
  rcases untyped_dd H (iter_proper hc 1) D1 t1' t3' with ⟨e, -⟩ | e | e
  · exact Or.inl e
  · exact Or.inr (Or.inl e)
  · exact Or.inr (Or.inr e)

/-- **Every `Γ`-cycle at a `(5,5,5,5,6)` hole has a non-`DL` `σ`-image.** -/
theorem gammaImages_of_hole6 (H : Hole6 P w m q) : GammaImages P := by
  intro s hc hall
  obtain ⟨N, t, k, h0⟩ := typed_in_orbit H hc hall
  have it : ∀ d, HasTK P w q ((piMove P)^[N + d] s) (gstep^[d] (t, k)).1
      (gstep^[d] (t, k)).2 := by
    intro d
    induction d with
    | zero => exact h0
    | succ d ih =>
      have e := tk_step H (iter_proper hc (N + d)) ih
        (by rw [← Function.iterate_succ_apply' (piMove P)]; exact hall (N + d + 1))
      rw [← add_assoc, Function.iterate_succ_apply', Function.iterate_succ_apply']
      exact e
  obtain ⟨d, -, hd2⟩ := gstep_to_R1k2 t k
  have hr := it d
  rw [hd2] at hr
  obtain ⟨j, hdl, hq, hT1⟩ := hr
  set r := (piMove P)^[N + d] s with hrdef
  have hcr : ProperOff M.graph h r := iter_proper hc _
  have hD : DDstate P r j := allDL_orbit_dd hc hall _ j hdl
  have pair := pair_R3k4_of_pred H hq hcr hD hT1
  have hT3 := r1_step H hq hcr hD hT1
  have hq' : q = j + 3 + 4 := hq.trans (q_k4 j)
  have hR := r3k4_R3At H hq' (piMove_properOff hcr) hD.2 hT3 pair.2
  refine ⟨N + d + 1, j + 3, ?_, ?_⟩ <;> rw [Function.iterate_succ_apply', ← hrdef]
  · exact hD.2
  · exact sigma_exit_not_DL_k4 (H.k4Ball hq') (piMove_properOff hcr) hR

/-- **Weak F6.** At a `(5,5,5,5,6)` hole every Kempe class contains a filled state. -/
theorem every_class_filled_of_hole6 (H : Hole6 P w m q) {c₀ : Fin n → Fin 4}
    (hc₀ : ProperOff M.graph h c₀) : ∃ d ∈ kclass M h c₀, Target M.graph h d :=
  filled_in_class_of_images (gammaImages_of_hole6 H) hc₀

/-- **Weak F6, `PureClean` form.** A `(5,5,5,5,6)` hole is pure-clean. -/
theorem pureClean_of_hole6 (H : Hole6 P w m q) : PureClean M h :=
  pureClean_of_images (gammaImages_of_hole6 H)

/-- At an icosahedral `(5,5,5,5,5)` hole every `Γ`-cycle has a non-`DL` `σ`-image: a `DD` step
has an `R3` endpoint (`dd_r3`), whose `σ`-image has neither lock (`sigSwap_spec`). -/
theorem gammaImages_of_icoBall (B : IcoBallP P w) : GammaImages P := by
  intro s hc hall
  obtain ⟨j, hd⟩ := hall 0
  have D0 := allDL_orbit_dd hc hall 0 j hd
  have h1 := hall 1
  rw [Function.iterate_one] at h1
  have key : ∀ (N : ℕ) (j : Fin 5), R3At P w ((piMove P)^[N] s) j →
      ∃ (k : ℕ) (j : Fin 5), DoublyLocked P ((piMove P)^[k] s) j ∧
        ¬ DLState P (sigSwap P ((piMove P)^[k] s) j) := by
    intro N j hR
    obtain ⟨-, -, r', n1, -⟩ := sigSwap_spec B (iter_proper hc N) hR
    exact ⟨N, j, hR.1, fun H => n1 ((dl_rep r').1 H).1⟩
  rcases dd_r3 B hc hd h1 with hR | hR
  · exact key 0 j hR
  · exact key 1 (j + 3) hR

/-- At an icosahedral hole every class has a filled state (`PureClean`). -/
theorem pureClean_of_icoBall (B : IcoBallP P w) : PureClean M h :=
  pureClean_of_images (gammaImages_of_icoBall B)

end sphere

/-- `RStarNoSepTri`, **conditionally**: if every minimum-degree-five triangulation with no
separating triangle has a degree-five vertex with a `(5,5,5,5,6)` link (`Hole6`). Not every
triangulation has one, so this is not R\*. -/
theorem rStarNoSepTri_of_hole6
    (H : ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) → NoSep T →
      ∃ v, T.graph.degree v = 5 ∧ ∃ (P : Pent T.graph v) (w : Fin 5 → Fin m) (p : Fin m)
        (q : Fin 5), Hole6 P w p q) :
    RStarNoSepTri :=
  rStarNoSepTri_of_images fun m T hm hconn htri hdeg hns => by
    obtain ⟨v, hv, P, w, p, q, H6⟩ := H m T hm hconn htri hdeg hns
    exact ⟨v, hv, P, gammaImages_of_hole6 H6⟩

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.gammaImages_of_hole6
#print axioms SimpleGraph.QuarterFloor.every_class_filled_of_hole6
#print axioms SimpleGraph.QuarterFloor.pureClean_of_hole6
#print axioms SimpleGraph.QuarterFloor.pureClean_of_icoBall
#print axioms SimpleGraph.QuarterFloor.rStarNoSepTri_of_hole6
