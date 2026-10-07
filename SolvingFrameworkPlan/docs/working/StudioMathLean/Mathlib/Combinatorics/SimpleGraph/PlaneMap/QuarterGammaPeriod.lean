/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaGroups

/-!
# The universal period of a `Γ`-cycle at a `(5,5,5,5,6)` hole

Formalises the local part of Lemma 2 of `NightFloorHP2.md` and of Studio Job O
(`NightLog-2026-10-06.md`): along an all-`DL` `π`-orbit at a hole whose link has exactly one
vertex of degree six, the sequence of `(type, k)` is
`R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2` with exact period ten, and the colour pair
swapped by each step (`π = R₊₃` swaps `{α, A} = {c (x j), c (x (j+3))}`) is carried by two of
the four hole vertices `p, m, y, z`, in the pattern of Job O.

## Conventions

* `Hole6 P w m q`: the link vertex `p = x q` has degree six, with outer path
  `x (q-1), y = w (q-1), m, z = w q, x (q+1)`; every other link vertex `x t` has degree five,
  with neighbours `h, x (t-1), x (t+1), w (t-1), w t`. The ring is `w t ~ w (t+1)` except that
  `w (q-1) ~ m ~ w q` replaces the edge `w (q-1) ~ w q`. (So `w t` is the common outer
  neighbour of `x t` and `x (t+1)`, as `widx` in the Studio's `picyc.cpp`.) This is the
  `(5,5,5,5,6)` hypothesis: exactly one link vertex of degree six. `K4Ball`/`K3Ball` of
  `QuarterSigmaK34` are the cases `q = j + 4`, `q = j + 3`.
* Types follow the Studio (`frame` in `picyc.cpp`): at repeat index `j` (link
  `α, μ, α, A, B`), `R1` is `c (w j) = A` (`TypeR1`), `R3` is `c (w j) = B ∧ c (w (j+3)) = μ`
  (`TypeR3`). The position is `k` with `q = j + k`.

## Main results (sorry-free, no new axioms)

1. `r3_step`: if `c` is `DL` of type `R3` at `j`, then `π c` is of type `R1` at `j + 3`
   (no hole hypothesis). `r1_step`: if `c` is `DL` of type `R1` at `j`, `π c` is `DL`, and the
   hole is `(5,5,5,5,6)`, then `π c` is of type `R3` at `j + 3`. Hence `tk_step`: on a `DD` step
   `(type, k) ↦ (flip type, k + 2)` (i.e. `k ↦ k − 3`). No `R2` state can follow an `R3`
   state.
2. `pair_own`: at a `DD` state of type `t` at position `k`, `(t, k) ≠ (R3, 4)`, the pair
   `{α, A}` is carried by the two vertices `gammaPairVerts t k` (first gets `α`, second `A`):
   `R1k1 (m,y)`, `R3k3 (m,p)`, `R1k0 (p,z)`, `R3k2 (p,y)`, `R1k4 (y,m)`, `R3k1 (m,z)`,
   `R1k3 (z,p)`, `R3k0 (p,y)`, `R1k2 (p,m)`. These use only properness, the two locks of the
   state, and the locks of its image (lock ends).
   `pair_R3k4_of_pred`: at `R3k4` the pair `(m,z)` is **not** determined by the state alone
   (locally `z` may have colour `μ`); it follows when the state is the `π`-image of a `DD`
   state of type `R1` at `k = 2`.
3. `gamma_period_ten`: from a `DL` state of type `R3` at `k = 4` on an all-`DL` forward orbit,
   the `n`-th state has `(type, k) = gseq n` (`gseq_table`: the ten-term table above), the
   pair facts hold at every `n ≥ 1`, `gseq` has exact period `10`, and every `(type, k)`
   occurs exactly once in every window of ten. `hasTK_unique`: `(type, k)` of a state is
   unique, so this is the observed `(type, k)`.

## Hypotheses

Nothing non-local is assumed beyond the all-`DL` orbit itself. The only fact not derived
is the pair at the *initial* `R3k4` state `n = 0` (it needs the predecessor; see 2.); with a
cycle hypothesis `π^[L] s = s`, `L > 0`, it follows (`gamma_pair_zero`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

lemma fin5_ne {j a b : Fin 5} (hab : a ≠ b) : j + a ≠ j + b := fun e => hab (add_left_cancel e)

lemma fin5_five (k : Fin 5) : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 := by
  revert k; decide

lemma fin5_ne0 {j a : Fin 5} (ha : a ≠ 0) : j ≠ j + a :=
  fun e => ha (add_left_cancel (e.symm.trans (add_zero j).symm))

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- A `(5,5,5,5,6)` hole: `x q` has degree six (extra outer neighbour `m` between `w (q+4)`
and `w q`), every other link vertex has degree five. -/
structure Hole6 (P : Pent M.graph h) (w : Fin 5 → Fin n) (m : Fin n) (q : Fin 5) : Prop where
  nbr : ∀ t, t ≠ q → ∀ u, M.graph.Adj (P.x t) u ↔
    u = h ∨ u = P.x (t + 4) ∨ u = P.x (t + 1) ∨ u = w (t + 4) ∨ u = w t
  nbrq : ∀ u, M.graph.Adj (P.x q) u ↔
    u = h ∨ u = P.x (q + 4) ∨ u = P.x (q + 1) ∨ u = w (q + 4) ∨ u = m ∨ u = w q
  ring : ∀ t, t + 1 ≠ q → M.graph.Adj (w t) (w (t + 1))
  ringy : M.graph.Adj (w (q + 4)) m
  ringz : M.graph.Adj m (w q)
  off : ∀ t i, w t ≠ P.x i
  offm : ∀ i, m ≠ P.x i
  offh : ∀ t, w t ≠ h
  offmh : m ≠ h

variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

namespace Hole6

lemma adj_w (H : Hole6 P w m q) (t : Fin 5) : M.graph.Adj (P.x t) (w t) := by
  by_cases ht : t = q
  · subst ht; exact (H.nbrq _).2 (by simp)
  · exact (H.nbr t ht _).2 (by simp)

lemma adj_w4 (H : Hole6 P w m q) (t : Fin 5) : M.graph.Adj (P.x t) (w (t + 4)) := by
  by_cases ht : t = q
  · subst ht; exact (H.nbrq _).2 (by simp)
  · exact (H.nbr t ht _).2 (by simp)

lemma adj_w' (H : Hole6 P w m q) (t : Fin 5) : M.graph.Adj (P.x (t + 1)) (w t) := by
  have e := H.adj_w4 (t + 1)
  rwa [add_assoc, show (1 : Fin 5) + 4 = 0 from rfl, add_zero] at e

lemma adj_m (H : Hole6 P w m q) : M.graph.Adj (P.x q) m := (H.nbrq _).2 (by simp)

lemma dom (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (t : Fin 5) :
    c (w t) ≠ c (P.x t) ∧ c (w t) ≠ c (P.x (t + 1)) :=
  ⟨(hc (H.adj_w t) (P.x_ne_h _) (H.offh t)).symm,
    (hc (H.adj_w' t) (P.x_ne_h _) (H.offh t)).symm⟩

lemma domAt (H : Hole6 P w m q) (hc : ProperOff M.graph h c) {a b : Fin 5} (hab : a + 1 = b) :
    c (w (j + a)) ≠ c (P.x (j + a)) ∧ c (w (j + a)) ≠ c (P.x (j + b)) := by
  have d := H.dom hc (j + a)
  rwa [add_assoc, hab] at d

lemma dom4 (H : Hole6 P w m q) (hc : ProperOff M.graph h c) :
    c (w (j + 4)) ≠ c (P.x (j + 4)) ∧ c (w (j + 4)) ≠ c (P.x j) := by
  have d := H.dom hc (j + 4)
  rwa [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero] at d

lemma ring0 (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hq : j + 1 ≠ q) :
    c (w j) ≠ c (w (j + 1)) :=
  hc (H.ring j hq) (H.offh _) (H.offh _)

lemma ringAt (H : Hole6 P w m q) (hc : ProperOff M.graph h c) {a b : Fin 5} (hab : a + 1 = b)
    (hq : j + b ≠ q) : c (w (j + a)) ≠ c (w (j + b)) := by
  have e := H.ring (j + a) (by rwa [add_assoc, hab])
  rw [add_assoc, hab] at e
  exact hc e (H.offh _) (H.offh _)

lemma ring4 (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hq : j ≠ q) :
    c (w (j + 4)) ≠ c (w j) := by
  have e := H.ring (j + 4) (by rwa [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero])
  rw [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero] at e
  exact hc e (H.offh _) (H.offh _)

end Hole6

/-! ### Types -/

/-- The two state types occurring on `Γ`-cycles. -/
inductive GType
  | R1
  | R3
  deriving DecidableEq

/-- `R1 ↔ R3`. -/
def GType.flip : GType → GType
  | .R1 => .R3
  | .R3 => .R1

variable (P w) in
/-- Type `R1` at `j` (Studio convention): `c (w j) = A`. -/
def TypeR1 (c : Fin n → Fin 4) (j : Fin 5) : Prop := c (w j) = c (P.x (j + 3))

variable (P w) in
/-- Type `R3` at `j` (Studio convention): `c (w j) = B` and `c (w (j+3)) = μ`. -/
def TypeR3 (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  c (w j) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x (j + 1))

variable (P w) in
/-- The type predicate. -/
def TypeOf : GType → (Fin n → Fin 4) → Fin 5 → Prop
  | .R1 => TypeR1 P w
  | .R3 => TypeR3 P w

variable (P w) in
/-- `c` is doubly locked at some `j`, of type `t`, with the degree-six vertex at `k`
(`q = j + k`). -/
def HasTK (q : Fin 5) (c : Fin n → Fin 4) (t : GType) (k : Fin 5) : Prop :=
  ∃ j, DoublyLocked P c j ∧ q = j + k ∧ TypeOf P w t c j

/-- `(type, k)` of a state is unique. -/
theorem hasTK_unique {t t' : GType} {k k' : Fin 5} (H1 : HasTK P w q c t k)
    (H2 : HasTK P w q c t' k') : t = t' ∧ k = k' := by
  obtain ⟨j, hd, hq, hT⟩ := H1
  obtain ⟨j', hd', hq', hT'⟩ := H2
  have e := rep_unique hd.1 hd'.1
  subst e
  have hr := hd.1
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  refine ⟨?_, add_left_cancel (hq.symm.trans hq')⟩
  cases t <;> cases t' <;> simp only [TypeOf, TypeR1, TypeR3] at hT hT' <;> first
    | rfl
    | (exfalso; omega)

/-! ### The image under `π = R₊₃` -/

section rot

lemma rot3_keep {v : Fin n} (h1 : c v ≠ c (P.x j)) (h2 : c v ≠ c (P.x (j + 3))) :
    rot3 P c j v = c v :=
  swap_other h1 h2

lemma rot3_K2 {v : Fin n} (hr : RepeatAt P c j) (e : M.graph.Adj (P.x (j + 2)) v) (hv : v ≠ h)
    (hcv : c v = c (P.x j) ∨ c v = c (P.x (j + 3))) :
    rot3 P c j v = Equiv.swap (c (P.x j)) (c (P.x (j + 3))) (c v) :=
  swap_in (show v ∈ {u | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
    (P.x (j + 2)) u} from Adj.reachable ⟨e, ⟨P.x_ne_h _, Or.inl hr.1.symm⟩, ⟨hv, hcv⟩⟩)

lemma rot3_K3 {v : Fin n} (hr : RepeatAt P c j) (e : M.graph.Adj (P.x (j + 3)) v) (hv : v ≠ h)
    (hcv : c v = c (P.x j) ∨ c v = c (P.x (j + 3))) :
    rot3 P c j v = Equiv.swap (c (P.x j)) (c (P.x (j + 3))) (c v) :=
  swap_in (show v ∈ {u | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
    (P.x (j + 2)) u} from
      (rot3_reach hr).trans (Adj.reachable ⟨e, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨hv, hcv⟩⟩))

lemma rot3_K0 {v : Fin n} (hK : Rot3Def P c j) (e : M.graph.Adj (P.x j) v) (hv : v ≠ h) :
    rot3 P c j v = c v := by
  by_cases hcv : c v = c (P.x j) ∨ c v = c (P.x (j + 3))
  · refine swap_out (fun hin => hK ?_)
    exact (show (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable
      (P.x (j + 2)) v from hin).trans
        (Adj.reachable ⟨e.symm, ⟨hv, hcv⟩, ⟨P.x_ne_h _, Or.inl rfl⟩⟩)
  · exact swap_other (fun e => hcv (Or.inl e)) (fun e => hcv (Or.inr e))

/-- The local facts of a `DD` step at `j`: `π c = R₊₃ c`, the lock ends of `c` at `x (j+3)`,
and the two lock ends of `π c` (at `x (j+2)`: a `B`-neighbour; at `x (j+4)`: an
`A`-neighbour, colours after the swap). -/
theorem dd_ends (hc : ProperOff M.graph h c) (hD : DDstate P c j) :
    piMove P c = rot3 P c j ∧ RepeatAt P c j ∧ Rot3Def P c j ∧
    (∃ u, M.graph.Adj (P.x (j + 3)) u ∧ u ≠ h ∧ c u = c (P.x (j + 1))) ∧
    (∃ u, M.graph.Adj (P.x (j + 2)) u ∧ u ≠ h ∧ rot3 P c j u = c (P.x (j + 4))) ∧
    (∃ u, M.graph.Adj (P.x (j + 4)) u ∧ u ≠ h ∧ rot3 P c j u = c (P.x (j + 3))) := by
  obtain ⟨⟨hr, l1, l2⟩, hd'⟩ := hD
  have hK := rot3Def_of_lock2 P hr l2
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hr, ite_eq_left l2]
  obtain ⟨-, hp', -, -, -⟩ := rot3_move hc hr l2
  obtain ⟨-, -, v2, -, v4⟩ := rot3_values hr hK
  rw [hπ] at hd'
  obtain ⟨-, -, L⟩ := hd'
  unfold Lock2 at L
  simp only [add_assoc, Fin.reduceAdd] at L
  refine ⟨hπ, hr, hK, lock_end hc l1 (fun e => fin5_ne (by decide) (P.inj e)) rfl, ?_, ?_⟩
  · obtain ⟨u, a, b, d⟩ := lock_end hp' L (fun e => fin5_ne (by decide) (P.inj e)) rfl
    exact ⟨u, a, b, d.trans v4⟩
  · rw [pairGraph_comm_gen] at L
    obtain ⟨u, a, b, d⟩ := lock_end hp' L.symm (fun e => fin5_ne (by decide) (P.inj e)) rfl
    exact ⟨u, a, b, d.trans v2⟩

end rot

/-! ### 1. The transition table -/

/-- **`R3 → R1`.** No hole hypothesis and no lock of the image is needed. -/
theorem r3_step (hd : DoublyLocked P c j) (hT : TypeR3 P w c j) :
    TypeR1 P w (piMove P c) (j + 3) := by
  obtain ⟨hr, -, l2⟩ := hd
  have hK := rot3Def_of_lock2 P hr l2
  rw [piMove_rep hr, ite_eq_left l2]
  obtain ⟨-, v1, -, -, -⟩ := rot3_values hr hK
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  unfold TypeR1
  simp only [add_assoc, Fin.reduceAdd]
  rw [v1, rot3_keep (by rw [hT.2]; exact h1) (by rw [hT.2]; exact h13), hT.2]

/-- `R1`, `x (j+1)` of degree five: `w (j+1) = B` from the ring edge `w j ~ w (j+1)`. -/
lemma r1_w1_ring (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hT : TypeR1 P w c j) (hq : j + 1 ≠ q) : c (w (j + 1)) = c (P.x (j + 4)) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have r := H.ring0 hc hq
  obtain ⟨d1, d2⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  unfold TypeR1 at hT
  omega

/-- `R1` with `w (j+1) = B`, `x (j+2), x (j+3)` of degree five: `w (j+3) = α` along the ring. -/
lemma r1_w3_chain (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hw1 : c (w (j + 1)) = c (P.x (j + 4))) (hq2 : j + 2 ≠ q) (hq3 : j + 3 ≠ q) :
    c (w (j + 3)) = c (P.x j) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl hq2
  have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl hq3
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  omega

/-- `R1`, `x j, x (j+4)` of degree five, image `DL`: `w (j+3) = α`, from the `A`-neighbour of
`x (j+4)` required by Lock 2 of `π c`. -/
lemma r1_w3_I3 (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (hT : TypeR1 P w c j) (hq4 : j + 4 ≠ q) (hq0 : j ≠ q) : c (w (j + 3)) = c (P.x j) := by
  obtain ⟨-, hr, hK, -, -, ⟨u, hu, huh, hcu⟩⟩ := dd_ends hc hD
  obtain ⟨v0, -, -, v3, -⟩ := rot3_values hr hK
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  unfold TypeR1 at hT
  by_contra hne
  have n4 := (H.nbr (j + 4) hq4 u).1 hu
  simp only [add_assoc, Fin.reduceAdd, add_zero] at n4
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  rcases n4 with rfl | rfl | rfl | rfl | rfl
  · exact huh rfl
  · rw [v3] at hcu; exact h3 hcu.symm
  · rw [v0] at hcu; exact h3 hcu.symm
  · rw [rot3_keep hne d3] at hcu; exact d3 hcu
  · rw [rot3_K0 hK (H.adj_w4 j) (H.offh _)] at hcu
    exact H.ring4 hc hq0 (hcu.trans hT.symm)

/-- `R1` at `k = 1` (`x (j+1)` of degree six), image `DL`: `w (j+1) = B`. If `w (j+1) = A`, the
`B`-neighbour of `x (j+2)` in `π c` is `w (j+2)`, the `μ`-neighbour of `x (j+3)` in `c` is then
`w (j+3)`, contradicting `r1_w3_I3`. -/
lemma r1_w1_k1 (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (hD : DDstate P c j)
    (hT : TypeR1 P w c j) (hq2 : j + 2 ≠ q) (hq3 : j + 3 ≠ q) (hq4 : j + 4 ≠ q)
    (hq0 : j ≠ q) : c (w (j + 1)) = c (P.x (j + 4)) := by
  have w3 := r1_w3_I3 H hc hD hT hq4 hq0
  obtain ⟨-, hr, hK, ⟨u', hu', hu'h, hcu'⟩, ⟨u, hu, huh, hcu⟩, -⟩ := dd_ends hc hD
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  by_contra hne
  have hA : c (w (j + 1)) = c (P.x (j + 3)) := by omega
  -- the `B`-neighbour of `x (j+2)` in `π c` is `w (j+2)`
  have w2 : c (w (j + 2)) = c (P.x (j + 4)) := by
    have n2 := (H.nbr (j + 2) hq2 u).1 hu
    simp only [add_assoc, Fin.reduceAdd] at n2
    rcases n2 with rfl | rfl | rfl | rfl | rfl
    · exact (huh rfl).elim
    · rw [v1] at hcu; exact (h14 hcu).elim
    · rw [v3] at hcu; exact (h4 hcu.symm).elim
    · have e := H.adj_w' (j + 1)
      simp only [add_assoc, Fin.reduceAdd] at e
      rw [rot3_K2 hr' e (H.offh _) (Or.inr hA), hA, Equiv.swap_apply_right] at hcu
      exact (h4 hcu.symm).elim
    · rwa [rot3_keep (by omega) d2'] at hcu
  -- the `μ`-neighbour of `x (j+3)` in `c` is `w (j+3)`
  have n3 := (H.nbr (j + 3) hq3 u').1 hu'
  simp only [add_assoc, Fin.reduceAdd] at n3
  rcases n3 with rfl | rfl | rfl | rfl | rfl
  · exact hu'h rfl
  · exact h1 (hcu'.symm.trans h02.symm)
  · exact h14 hcu'.symm
  · exact h14 (hcu'.symm.trans w2)
  · exact h1 (hcu'.symm.trans w3)

/-- The ring of an `R1` `DD` state at any `k`: `w (j+1) = B`, `w (j+3) = α`. -/
theorem r1_ring {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) :
    c (w (j + 1)) = c (P.x (j + 4)) ∧ c (w (j + 3)) = c (P.x j) := by
  subst hq
  have hr := hD.1.1
  obtain rfl | rfl | rfl | rfl | rfl := fin5_five k
  · have w1 := r1_w1_ring H hc hr hT (fin5_ne (by decide))
    exact ⟨w1, r1_w3_chain H hc hr w1 (fin5_ne (by decide)) (fin5_ne (by decide))⟩
  · exact ⟨r1_w1_k1 H hc hD hT (fin5_ne (by decide)) (fin5_ne (by decide))
      (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide)),
      r1_w3_I3 H hc hD hT (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide))⟩
  · exact ⟨r1_w1_ring H hc hr hT (fin5_ne (by decide)),
      r1_w3_I3 H hc hD hT (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide))⟩
  · exact ⟨r1_w1_ring H hc hr hT (fin5_ne (by decide)),
      r1_w3_I3 H hc hD hT (fin5_ne (by decide)) (fin5_ne0 (a := _) (by decide))⟩
  · have w1 := r1_w1_ring H hc hr hT (fin5_ne (by decide))
    exact ⟨w1, r1_w3_chain H hc hr w1 (fin5_ne (by decide)) (fin5_ne (by decide))⟩

/-- **`R1 → R3`** at a `(5,5,5,5,6)` hole, for every position `k`, when `π c` is `DL`. -/
theorem r1_step {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) : TypeR3 P w (piMove P c) (j + 3) := by
  obtain ⟨w1, w3⟩ := r1_ring H hq hc hD hT
  obtain ⟨hπ, hr, hK, -, -, -⟩ := dd_ends hc hD
  obtain ⟨-, -, v2, -, v4⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  unfold TypeR3
  simp only [add_assoc, Fin.reduceAdd, hπ]
  refine ⟨?_, ?_⟩
  · rw [v2, rot3_K3 hr' (H.adj_w (j + 3)) (H.offh _) (Or.inl w3), w3, Equiv.swap_apply_left]
  · rw [v4, rot3_keep (by rw [w1]; exact h4) (by rw [w1]; exact h34.symm), w1]

/-- **(1) The transition table.** On a `DD` step, `(type, k) ↦ (flip type, k + 2)`. -/
theorem tk_step {t : GType} {k : Fin 5} (H : Hole6 P w m q) (hc : ProperOff M.graph h c)
    (hs : HasTK P w q c t k) (hd' : DLState P (piMove P c)) :
    HasTK P w q (piMove P c) t.flip (k + 2) := by
  obtain ⟨j, hd, hq, hT⟩ := hs
  obtain ⟨-, -, r', -, -⟩ := rot3_move hc hd.1 hd.2.2
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hd.1, ite_eq_left hd.2.2]
  rw [← hπ] at r'
  have hd2 : DoublyLocked P (piMove P c) (j + 3) := ⟨r', (dl_rep r').1 hd'⟩
  refine ⟨j + 3, hd2, ?_, ?_⟩
  · rw [hq]
    have e : ∀ a b : Fin 5, a + b = a + 3 + (b + 2) := by decide
    exact e j k
  · cases t
    · exact r1_step H hq hc ⟨hd, hd2⟩ hT
    · exact r3_step hd hT

/-! ### 2. The swapped pair -/

variable (P) in
/-- The swapped pair `{α, A} = {c (x j), c (x (j+3))}` of the `R₊₃` step at `j` is carried by
`u` (colour `α`) and `v` (colour `A`). -/
def PairFact (c : Fin n → Fin 4) (j : Fin 5) (u v : Fin n) : Prop :=
  c u = c (P.x j) ∧ c v = c (P.x (j + 3))

variable (P w m) in
/-- The carriers of the swapped pair by `(type, k)`, with `p = x q`, `y = w (q+4)`,
`z = w q` (Studio Job O). -/
def gammaPairVerts (q : Fin 5) (t : GType) (k : Fin 5) : Fin n × Fin n :=
  match t, k.val with
  | .R3, 4 => (m, w q)
  | .R1, 1 => (m, w (q + 4))
  | .R3, 3 => (m, P.x q)
  | .R1, 0 => (P.x q, w q)
  | .R3, 2 => (P.x q, w (q + 4))
  | .R1, 4 => (w (q + 4), m)
  | .R3, 1 => (m, w q)
  | .R1, 3 => (w q, P.x q)
  | .R3, 0 => (P.x q, w (q + 4))
  | .R1, 2 => (P.x q, m)
  | _, _ => (m, m)

section pv
variable (q : Fin 5)
lemma pv_R1_0 : gammaPairVerts P w m q .R1 0 = (P.x q, w q) := rfl
lemma pv_R1_1 : gammaPairVerts P w m q .R1 1 = (m, w (q + 4)) := rfl
lemma pv_R1_2 : gammaPairVerts P w m q .R1 2 = (P.x q, m) := rfl
lemma pv_R1_3 : gammaPairVerts P w m q .R1 3 = (w q, P.x q) := rfl
lemma pv_R1_4 : gammaPairVerts P w m q .R1 4 = (w (q + 4), m) := rfl
lemma pv_R3_0 : gammaPairVerts P w m q .R3 0 = (P.x q, w (q + 4)) := rfl
lemma pv_R3_1 : gammaPairVerts P w m q .R3 1 = (m, w q) := rfl
lemma pv_R3_2 : gammaPairVerts P w m q .R3 2 = (P.x q, w (q + 4)) := rfl
lemma pv_R3_3 : gammaPairVerts P w m q .R3 3 = (m, P.x q) := rfl
lemma pv_R3_4 : gammaPairVerts P w m q .R3 4 = (m, w q) := rfl
end pv

set_option maxHeartbeats 1000000 in
/-- The pair at every `DD` state other than `R3k4`. -/
theorem pair_own {t : GType} {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k)
    (hc : ProperOff M.graph h c) (hD : DDstate P c j) (hT : TypeOf P w t c j)
    (hne : ¬ (t = .R3 ∧ k = 4)) :
    PairFact P c j (gammaPairVerts P w m q t k).1 (gammaPairVerts P w m q t k).2 := by
  subst hq
  obtain ⟨-, hr, hK, ⟨u', hu', hu'h, hcu'⟩, ⟨u, hu, huh, hcu⟩, -⟩ := dd_ends hc hD
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have d0 := H.dom hc j
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  have d4 := H.dom4 hc (j := j)
  have am := hc H.adj_m (P.x_ne_h _) H.offmh
  have ay := hc H.ringy (H.offh _) H.offmh
  have az := hc H.ringz H.offmh (H.offh _)
  cases t <;> obtain rfl | rfl | rfl | rfl | rfl := fin5_five k
  all_goals simp only [add_assoc, Fin.reduceAdd, add_zero] at H am ay az
  all_goals simp only [pv_R1_0, pv_R1_1, pv_R1_2, pv_R1_3, pv_R1_4, pv_R3_0, pv_R3_1, pv_R3_2,
    pv_R3_3, pv_R3_4, PairFact, add_assoc, Fin.reduceAdd, add_zero]
  · -- R1k0: (p, z)
    exact ⟨trivial, hT⟩
  · -- R1k1: (m, y)
    obtain ⟨w1, -⟩ := r1_ring H (k := 1) rfl hc hD hT
    unfold TypeOf TypeR1 at hT
    exact ⟨by clear * - h1 h3 h4 h13 h14 h34 am ay az w1 hT; omega, hT⟩
  · -- R1k2: (p, m); `w (j+2) = μ` is the `μ`-neighbour of `x (j+3)`
    obtain ⟨w1, w3⟩ := r1_ring H (k := 2) rfl hc hD hT
    have n3 := (H.nbr (j + 3) (fin5_ne (by decide)) u').1 hu'
    simp only [add_assoc, Fin.reduceAdd] at n3
    have w2 : c (w (j + 2)) = c (P.x (j + 1)) := by
      rcases n3 with rfl | rfl | rfl | rfl | rfl
      · exact (hu'h rfl).elim
      · exact (h1 (hcu'.symm.trans h02.symm)).elim
      · exact (h14 hcu'.symm).elim
      · exact hcu'
      · exact (h1 (hcu'.symm.trans w3)).elim
    exact ⟨h02.symm, by clear * - h1 h3 h4 h13 h14 h34 am ay az w1 w2 h02; omega⟩
  · -- R1k3: (z, p)
    obtain ⟨-, w3⟩ := r1_ring H (k := 3) rfl hc hD hT
    exact ⟨w3, trivial⟩
  · -- R1k4: (y, m)
    obtain ⟨-, w3⟩ := r1_ring H (k := 4) rfl hc hD hT
    unfold TypeOf TypeR1 at hT
    have r40 := H.ring4 hc (j := j) (fin5_ne0 (a := 4) (by decide))
    have w4 : c (w (j + 4)) = c (P.x (j + 1)) := by
      clear * - h1 h3 h4 h13 h14 h34 d4 r40 hT; omega
    exact ⟨w3, by clear * - h1 h3 h4 h13 h14 h34 w4 w3 am ay az; omega⟩
  · -- R3k0: (p, y)
    obtain ⟨t0, t3⟩ := hT
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl
      (fun e => fin5_ne0 (a := 4) (by decide) e.symm)
    exact ⟨trivial, by clear * - h1 h3 h4 h13 h14 h34 d4 r34 t3; omega⟩
  · -- R3k1: (m, z)
    obtain ⟨t0, t3⟩ := hT
    have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have w2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      clear * - h1 h3 h4 h13 h14 h34 d2 d2' r23 t3 h02; omega
    have w1 : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 d1 d1' r12 w2 h02; omega
    exact ⟨by clear * - h1 h3 h4 h13 h14 h34 am ay az t0 w1; omega, w1⟩
  · -- R3k2: (p, y)
    obtain ⟨t0, t3⟩ := hT
    have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
    exact ⟨h02.symm, by clear * - h1 h3 h4 h13 h14 h34 d1 d1' r01 t0 h02; omega⟩
  · -- R3k3: (m, p); `w (j+2) = B` is the `B`-neighbour of `x (j+2)` in `π c`
    obtain ⟨t0, t3⟩ := hT
    have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
    have hA : c (w (j + 1)) = c (P.x (j + 3)) := by
      clear * - h1 h3 h4 h13 h14 h34 d1 d1' r01 t0 h02; omega
    have n2 := (H.nbr (j + 2) (fin5_ne (by decide)) u).1 hu
    simp only [add_assoc, Fin.reduceAdd] at n2
    have w2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      rcases n2 with rfl | rfl | rfl | rfl | rfl
      · exact (huh rfl).elim
      · rw [v1] at hcu; exact (h14 hcu).elim
      · rw [v3] at hcu; exact (h4 hcu.symm).elim
      · have e := H.adj_w' (j + 1)
        simp only [add_assoc, Fin.reduceAdd] at e
        rw [rot3_K2 hr' e (H.offh _) (Or.inr hA), hA, Equiv.swap_apply_right] at hcu
        exact (h4 hcu.symm).elim
      · rwa [rot3_keep (by rw [h02]; exact d2) d2'] at hcu
    exact ⟨by clear * - h1 h3 h4 h13 h14 h34 am ay az t3 w2; omega, trivial⟩
  · exact (hne ⟨rfl, rfl⟩).elim

/-- **`R3k4` from its predecessor.** If `r` is a `DD` state of type `R1` at `k = 2`, then at
`π r` (type `R3`, `k = 4`, repeat index `j + 3`) the pair is carried by `(m, z)`. -/
theorem pair_R3k4_of_pred {r : Fin n → Fin 4} (H : Hole6 P w m q) (hq : q = j + 2)
    (hc : ProperOff M.graph h r) (hD : DDstate P r j) (hT : TypeR1 P w r j) :
    PairFact P (piMove P r) (j + 3) m (w q) := by
  have own := pair_own (t := .R1) (k := 2) H hq hc hD hT (by simp)
  rw [pv_R1_2] at own
  unfold PairFact at own
  subst hq
  obtain ⟨hπ, hr, hK, ⟨u', hu', hu'h, hcu'⟩, -, -⟩ := dd_ends hc hD
  obtain ⟨w1, w3⟩ := r1_ring H (k := 2) rfl hc hD hT
  obtain ⟨-, v1, -, v3, -⟩ := rot3_values hr hK
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have n3 := (H.nbr (j + 3) (fin5_ne (by decide)) u').1 hu'
  simp only [add_assoc, Fin.reduceAdd] at n3
  have w2 : r (w (j + 2)) = r (P.x (j + 1)) := by
    rcases n3 with rfl | rfl | rfl | rfl | rfl
    · exact (hu'h rfl).elim
    · exact (h1 (hcu'.symm.trans h02.symm)).elim
    · exact (h14 hcu'.symm).elim
    · exact hcu'
    · exact (h1 (hcu'.symm.trans w3)).elim
  unfold PairFact
  simp only [add_assoc, Fin.reduceAdd, hπ]
  refine ⟨?_, ?_⟩
  · rw [v3, rot3_K2 hr' H.adj_m H.offmh (Or.inr own.2), own.2, Equiv.swap_apply_right]
  · rw [v1, rot3_keep (by rw [w2]; exact h1) (by rw [w2]; exact h13), w2]

/-! ### 3. The period -/

/-- One step of the table. -/
def gstep (x : GType × Fin 5) : GType × Fin 5 := (x.1.flip, x.2 + 2)

/-- The `(type, k)` sequence from `R3k4`. -/
def gseq (n : ℕ) : GType × Fin 5 := gstep^[n] (.R3, 4)

lemma gseq_succ (n : ℕ) : gseq (n + 1) = gstep (gseq n) := by
  unfold gseq; rw [Function.iterate_succ_apply']

lemma gseq_add (n d : ℕ) : gseq (n + d) = gstep^[d] (gseq n) := by
  unfold gseq; rw [add_comm, Function.iterate_add_apply]

/-- The table `R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2`. -/
theorem gseq_table : (List.range 10).map gseq =
    [(.R3, 4), (.R1, 1), (.R3, 3), (.R1, 0), (.R3, 2), (.R1, 4), (.R3, 1), (.R1, 3), (.R3, 0),
      (.R1, 2)] := by
  decide

private lemma gstep_ten : ∀ t : GType, ∀ k : Fin 5, gstep^[10] (t, k) = (t, k) := by
  intro t; cases t <;> decide

private lemma gstep_exact : ∀ t : GType, ∀ k : Fin 5, ∀ d, d < 10 → 0 < d →
    gstep^[d] (t, k) ≠ (t, k) := by
  intro t; cases t <;> decide

private lemma gstep_onto : ∀ t t' : GType, ∀ k k' : Fin 5, ∃ d, d < 10 ∧
    gstep^[d] (t, k) = (t', k') := by
  intro t t'; cases t <;> cases t' <;> decide

private lemma gstep_pre : ∀ x : GType × Fin 5, gstep x = (.R3, 4) → x = (.R1, 2) := by
  rintro ⟨t, k⟩; cases t <;> revert k <;> decide

theorem gseq_period (n : ℕ) : gseq (n + 10) = gseq n := by
  rw [gseq_add]; exact gstep_ten _ _

theorem gseq_exact (n d : ℕ) (hd0 : 0 < d) (hd : d < 10) : gseq (n + d) ≠ gseq n := by
  rw [gseq_add]; exact gstep_exact _ _ d hd hd0

theorem gseq_once (n : ℕ) (x : GType × Fin 5) : ∃! d, d < 10 ∧ gseq (n + d) = x := by
  obtain ⟨d, hd, e⟩ := gstep_onto (gseq n).1 x.1 (gseq n).2 x.2
  refine ⟨d, ⟨hd, by rw [gseq_add]; exact e⟩, ?_⟩
  rintro d' ⟨hd', e'⟩
  have e2 : gseq (n + d) = x := by rw [gseq_add]; exact e
  by_contra hne
  rcases Nat.lt_or_gt_of_ne hne with l | l
  · have := gseq_exact (n + d') (d - d') (by omega) (by omega)
    rw [show n + d' + (d - d') = n + d by omega, e2, e'] at this
    exact this rfl
  · have := gseq_exact (n + d) (d' - d) (by omega) (by omega)
    rw [show n + d + (d' - d) = n + d' by omega, e2, e'] at this
    exact this rfl

lemma iter_proper {s : Fin n → Fin 4} (hc : ProperOff M.graph h s) :
    ∀ n, ProperOff M.graph h ((piMove P)^[n] s)
  | 0 => hc
  | n + 1 => by
    rw [Function.iterate_succ_apply']
    exact piMove_properOff (iter_proper hc n)

/-- **The universal period** (`NightFloorHP2.md` Lemma 2, Studio Job O). At a `(5,5,5,5,6)`
hole, start from a `DL` state of type `R3` at `k = 4` whose forward `π`-orbit is all `DL`.
Then the `n`-th state has `(type, k) = gseq n` (`gseq_table`), the swapped pair of every state
`n ≥ 1` is carried by `gammaPairVerts (gseq n)`, and `gseq` has exact period `10` with each
`(type, k)` once per period. -/
theorem gamma_period_ten {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) :
    (∀ n, HasTK P w q ((piMove P)^[n] s) (gseq n).1 (gseq n).2) ∧
    (∀ n, 0 < n → ∀ j, RepeatAt P ((piMove P)^[n] s) j →
      PairFact P ((piMove P)^[n] s) j (gammaPairVerts P w m q (gseq n).1 (gseq n).2).1
        (gammaPairVerts P w m q (gseq n).1 (gseq n).2).2) ∧
    (∀ n, gseq (n + 10) = gseq n) ∧
    (∀ n d, 0 < d → d < 10 → gseq (n + d) ≠ gseq n) ∧
    (∀ n x, ∃! d, d < 10 ∧ gseq (n + d) = x) := by
  have tk : ∀ n, HasTK P w q ((piMove P)^[n] s) (gseq n).1 (gseq n).2 := by
    intro n
    induction n with
    | zero => exact ⟨j₀, ⟨hr, (dl_rep hr).1 (hall 0)⟩, hq, hT⟩
    | succ n ih =>
      have e := tk_step H (iter_proper hc n) ih
        (by rw [← Function.iterate_succ_apply' (piMove P)]; exact hall (n + 1))
      rw [Function.iterate_succ_apply', gseq_succ]
      exact e
  have dd : ∀ n j, DoublyLocked P ((piMove P)^[n] s) j →
      DDstate P ((piMove P)^[n] s) j := by
    intro n j hd
    obtain ⟨-, -, r', -, -⟩ := rot3_move (iter_proper hc n) hd.1 hd.2.2
    have hπ : piMove P ((piMove P)^[n] s) = rot3 P ((piMove P)^[n] s) j := by
      rw [piMove_rep hd.1, ite_eq_left hd.2.2]
    rw [← hπ] at r'
    have hn := hall (n + 1)
    rw [Function.iterate_succ_apply'] at hn
    exact ⟨hd, r', (dl_rep r').1 hn⟩
  refine ⟨tk, ?_, gseq_period, gseq_exact, gseq_once⟩
  intro n hn j hrj
  by_cases h34 : (gseq n).1 = .R3 ∧ (gseq n).2 = 4
  · obtain ⟨n', rfl⟩ : ∃ n', n = n' + 1 := ⟨n - 1, by omega⟩
    obtain ⟨j', hd', hq', hT'⟩ := tk n'
    have hg : gseq n' = (.R1, 2) := by
      rw [gseq_succ] at h34
      exact gstep_pre _ (Prod.ext h34.1 h34.2)
    rw [hg] at hq' hT'
    have P0 := pair_R3k4_of_pred H hq' (iter_proper hc n') (dd n' j' hd') hT'
    have hr2 : RepeatAt P ((piMove P)^[n' + 1] s) (j' + 3) := by
      rw [Function.iterate_succ_apply']
      have := dd n' j' hd'
      exact this.2.1
    have ej := rep_unique hr2 hrj
    rw [ej, h34.1, h34.2, pv_R3_4, Function.iterate_succ_apply']
    exact P0
  · obtain ⟨j', hd', hq', hT'⟩ := tk n
    have ej := rep_unique hd'.1 hrj
    subst ej
    exact pair_own H hq' (iter_proper hc n) (dd n j hd') hT' h34

/-- On a `π`-cycle (`π^[L] s = s`, `L > 0`) the pair holds at `n = 0` too. -/
theorem gamma_pair_zero {s : Fin n → Fin 4} {j₀ : Fin 5} (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {L : ℕ} (hL : 0 < L) (hcyc : (piMove P)^[L] s = s) :
    PairFact P s j₀ m (w q) := by
  obtain ⟨tk, pr, -⟩ := gamma_period_ten H hc hall hr hq hT
  have e := pr L hL j₀ (by rw [hcyc]; exact hr)
  have u := hasTK_unique (tk L) (by rw [hcyc]; exact tk 0)
  have g : gseq L = (.R3, 4) := Prod.ext u.1 u.2
  rw [hcyc, g, pv_R3_4] at e
  exact e

end sphere

end SimpleGraph.QuarterFloor

