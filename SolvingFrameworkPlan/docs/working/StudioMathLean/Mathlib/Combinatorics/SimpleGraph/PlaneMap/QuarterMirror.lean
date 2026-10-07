/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterGammaPeriod

/-!
# The mirror orientation reverses `π` on doubly locked states

The PlaneMap library has no mirror construction, so the minimal one is built here.

* `RotationSystem.mirror`: reverse every vertex's cyclic order (`next ↦ next⁻¹`);
  `RotationSystem.mirror_mirror`. (No `SphericalMap.mirror` is built: that would need the
  face-filling property of the reversed system, and nothing below uses it.)
* `Pent.mirror`: the link read in the opposite cyclic order, `x' i = x (-i)`; same graph, same
  hole. `Pent.oriented_mirror`: if the link follows the rotation at `h`
  (`R.next (h → x i) = (h → x (i+1))`), the mirrored link follows the mirrored rotation.
  The moves `π`, `π⁻¹` depend only on the graph and the link labelling, so changing the
  embedding to its mirror acts on `π` exactly through `P ↦ P.mirror`.

Index transport: the repeat index `k` of `P` becomes `mj k = -(k+2)` of `P.mirror`; `μ` and
`α` stay, `A ↔ B` swap. Hence

* `repeat_mirror_iff`, `lock1_mirror_iff` (`Lock1` of the mirror is `Lock2`),
  `lock2_mirror_iff`, `doublyLocked_mirror_iff`, `dlState_mirror_iff`.
* `rot3_mirror`: `R₊₃` of the mirror is `R₊₂` (`rot2`); `rot2_mirror` conversely.
* `piMove_mirror`: on an unfilled state with `Lock1`, `π_mirror = π⁻¹` **exactly** (no
  relabelling of states; only the link index changes, `k ↦ mj k`). `piInv_mirror`: with
  `Lock2`, `π⁻¹_mirror = π`. On `DL` states both hold (`mirror_dl`). (Without `Lock1` they
  differ in general: `φ_B⁻¹` of the mirror swaps the `{μ, A}`-component of `x (k+3)`, `φ_A⁻¹`
  that of `x (k+1)`; these are different components when `Lock1` fails.)
* `gammaOrbit_mirror` (sphere): an all-`DL` `π`-cycle of length `L > 0` is an all-`DL`
  `π_mirror`-cycle with the same state set, traversed backwards:
  `π_mirror^[t] s = π^[L - t] s`.
* `Hole6.mirror`: the `(5,5,5,5,6)` hole data transports (`w' t = w (-(t+1))`, `q ↦ -q`).
* `gseq_mirror`: on the all-`DL` orbit of `gamma_period_ten`, the `n`-th state has mirror
  `(type, k) = mrel (gseq n) = (type, 2 - k)`: the **type is kept** and `k ↦ 2 - k`
  (it is not `R1 ↔ R3`: at `R3k1` the pair fact `c (w q) = A` makes the mirror type `R3`).
  `gstep_mrel`: `gstep ∘ mrel ∘ gstep = mrel`, so the mirror sequence is the `gstep` table run
  backwards; `gseq_mirror_reversed`: along the mirror orbit, state `t` has mirror
  `(type, k) = mrel (gseq (L - t))`.

Sorry-free, no new axioms.
-/

@[expose] public section

namespace SimpleGraph

/-- The mirror rotation system: every vertex's cyclic order reversed. -/
def RotationSystem.mirror {V : Type*} {G : SimpleGraph V} (R : RotationSystem G) :
    RotationSystem G where
  next := R.next.symm
  next_fst d := by
    have e := R.next_fst (R.next.symm d)
    rw [Equiv.apply_symm_apply] at e
    exact e.symm
  cyclic d e hde := by
    obtain ⟨k, hk⟩ := R.cyclic e d hde.symm
    exact ⟨k, by rw [← hk]; exact Function.LeftInverse.iterate R.next.symm_apply_apply k e⟩

theorem RotationSystem.mirror_mirror {V : Type*} {G : SimpleGraph V} (R : RotationSystem G) :
    R.mirror.mirror = R := by
  cases R; rfl

namespace QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### The mirrored link -/

section mirror
variable {V : Type*} {G : SimpleGraph V} {h : V}

private lemma mneg1 (i : Fin 5) : -(i + 1) + 1 = -i := by revert i; decide

/-- The link read in the opposite cyclic order: `x' i = x (-i)`. -/
def Pent.mirror (P : Pent G h) : Pent G h where
  x i := P.x (-i)
  adj_h _ := P.adj_h _
  adj_cyc i := by
    have e := P.adj_cyc (-(i + 1))
    rw [mneg1] at e
    exact e.symm
  inj _ _ e := neg_injective (P.inj e)
  only v hv := by
    obtain ⟨i, rfl⟩ := P.only v hv
    exact ⟨-i, show P.x i = P.x (- -i) by rw [neg_neg]⟩

lemma Pent.mirror_x (P : Pent G h) (i : Fin 5) : P.mirror.x i = P.x (-i) := rfl

theorem Pent.mirror_mirror (P : Pent G h) : P.mirror.mirror = P := by
  cases P
  simp only [Pent.mirror, neg_neg]

/-- The link follows the rotation at `h`: the rotation successor of `h → x i` is
`h → x (i+1)`. -/
def Pent.Oriented (R : RotationSystem G) (P : Pent G h) : Prop :=
  ∀ i, R.next ⟨(h, P.x i), P.adj_h i⟩ = ⟨(h, P.x (i + 1)), P.adj_h (i + 1)⟩

/-- The mirrored link follows the mirrored rotation. -/
theorem Pent.oriented_mirror {R : RotationSystem G} {P : Pent G h} (hO : P.Oriented R) :
    P.mirror.Oriented R.mirror := by
  intro i
  show R.next.symm ⟨(h, P.x (-i)), P.adj_h _⟩ = ⟨(h, P.x (-(i + 1))), P.adj_h _⟩
  rw [Equiv.symm_apply_eq, hO]
  apply Dart.ext
  show (h, P.x (-i)) = (h, P.x (-(i + 1) + 1))
  rw [mneg1]

/-- The repeat index of the mirror: `k ↦ -(k+2)`. -/
def mj (k : Fin 5) : Fin 5 := -(k + 2)

lemma mj_mj (k : Fin 5) : mj (mj k) = k := by revert k; decide

private lemma i0 (k : Fin 5) : -(mj k) = k + 2 := by revert k; decide
private lemma i1 (k : Fin 5) : -(mj k + 1) = k + 1 := by revert k; decide
private lemma i2 (k : Fin 5) : -(mj k + 2) = k := by revert k; decide
private lemma i3 (k : Fin 5) : -(mj k + 3) = k + 4 := by revert k; decide
private lemma i4 (k : Fin 5) : -(mj k + 4) = k + 3 := by revert k; decide

variable (P : Pent G h)

lemma mx0 (k : Fin 5) : P.mirror.x (mj k) = P.x (k + 2) := congrArg P.x (i0 k)
lemma mx1 (k : Fin 5) : P.mirror.x (mj k + 1) = P.x (k + 1) := congrArg P.x (i1 k)
lemma mx2 (k : Fin 5) : P.mirror.x (mj k + 2) = P.x k := congrArg P.x (i2 k)
lemma mx3 (k : Fin 5) : P.mirror.x (mj k + 3) = P.x (k + 4) := congrArg P.x (i3 k)
lemma mx4 (k : Fin 5) : P.mirror.x (mj k + 4) = P.x (k + 3) := congrArg P.x (i4 k)

variable (c : V → Fin 4) (k : Fin 5)

/-- Repeat index `k` of `P` is repeat index `mj k` of the mirror. -/
theorem repeat_mirror_iff : RepeatAt P.mirror c (mj k) ↔ RepeatAt P c k := by
  unfold RepeatAt
  rw [mx0, mx1, mx2, mx3, mx4]
  constructor
  · rintro ⟨e, h1, h2, h3, h4, h5, h6⟩
    exact ⟨e.symm, by rw [← e]; exact h1, by rw [← e]; exact h3, by rw [← e]; exact h2,
      h5, h4, h6.symm⟩
  · rintro ⟨e, h1, h2, h3, h4, h5, h6⟩
    exact ⟨e.symm, by rw [← e]; exact h1, by rw [← e]; exact h3, by rw [← e]; exact h2,
      h5, h4, h6.symm⟩

/-- Lock 1 of the mirror is lock 2 (same `{μ, B}` graph and ends). -/
theorem lock1_mirror_iff : Lock1 P.mirror c (mj k) ↔ Lock2 P c k := by
  unfold Lock1 Lock2
  rw [mx1, mx3]

/-- Lock 2 of the mirror is lock 1. -/
theorem lock2_mirror_iff : Lock2 P.mirror c (mj k) ↔ Lock1 P c k := by
  unfold Lock1 Lock2
  rw [mx1, mx4]

theorem doublyLocked_mirror_iff : DoublyLocked P.mirror c (mj k) ↔ DoublyLocked P c k := by
  unfold DoublyLocked
  rw [repeat_mirror_iff, lock1_mirror_iff, lock2_mirror_iff, and_comm (a := Lock2 P c k)]

variable {P c k}

/-- `R₊₃` of the mirror at `mj k` is `R₊₂` at `k`. -/
theorem rot3_mirror (hr : RepeatAt P c k) : rot3 P.mirror c (mj k) = rot2 P c k := by
  unfold rot3 rot2
  rw [mx0, mx2, mx3, ← hr.1]

/-- `R₊₂` of the mirror at `mj k` is `R₊₃` at `k`. -/
theorem rot2_mirror (hr : RepeatAt P c k) : rot2 P.mirror c (mj k) = rot3 P c k := by
  unfold rot3 rot2
  rw [mx0, mx4, ← hr.1]

/-- **The mirror's `π` is `π⁻¹`** on unfilled states with lock 1 (in particular on `DL`
states): both are the rotation `R₊₂` of `P`. -/
theorem piMove_mirror (hr : RepeatAt P c k) (hl : Lock1 P c k) :
    piMove P.mirror c = piInv P c := by
  rw [piMove_rep ((repeat_mirror_iff P c k).2 hr), ite_eq_left ((lock2_mirror_iff P c k).2 hl),
    rot3_mirror hr, piInv_rep hr, ite_eq_left hl]

/-- The mirror's `π⁻¹` is `π` on unfilled states with lock 2. -/
theorem piInv_mirror (hr : RepeatAt P c k) (hl : Lock2 P c k) :
    piInv P.mirror c = piMove P c := by
  rw [piInv_rep ((repeat_mirror_iff P c k).2 hr), ite_eq_left ((lock1_mirror_iff P c k).2 hl),
    rot2_mirror hr, piMove_rep hr, ite_eq_left hl]

/-- On a doubly locked state, the mirror exchanges `π` and `π⁻¹`. -/
theorem mirror_dl (hd : DoublyLocked P c k) :
    piMove P.mirror c = piInv P c ∧ piInv P.mirror c = piMove P c :=
  ⟨piMove_mirror hd.1 hd.2.1, piInv_mirror hd.1 hd.2.2⟩

end mirror

/-! ### On the sphere: orbits -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h}
  {c s : Fin n → Fin 4} {k : Fin 5}

theorem dlState_mirror_iff : DLState P.mirror c ↔ DLState P c := by
  constructor
  · rintro ⟨j, hd⟩
    exact ⟨mj j, (doublyLocked_mirror_iff P c (mj j)).1 (by rwa [mj_mj])⟩
  · rintro ⟨k, hd⟩
    exact ⟨mj k, (doublyLocked_mirror_iff P c k).2 hd⟩

/-- After a forward `R₊₃` step of `P`, the mirror's `π` steps back. -/
theorem piMove_mirror_piMove (hc : ProperOff M.graph h c) (hr : RepeatAt P c k)
    (hl : Lock2 P c k) : piMove P.mirror (piMove P c) = c := by
  obtain ⟨-, -, r', l', -⟩ := rot3_move hc hr hl
  have hπ : piMove P c = rot3 P c k := by rw [piMove_rep hr, ite_eq_left hl]
  rw [← hπ] at r' l'
  rw [piMove_mirror r' l', piInv_piMove hc]

lemma back_step {Q : Pent M.graph h} (hc : ProperOff M.graph h s)
    (hall : ∀ t, DLState Q ((piMove Q)^[t] s)) (u : ℕ) :
    piMove Q.mirror ((piMove Q)^[u + 1] s) = (piMove Q)^[u] s := by
  obtain ⟨k, hr, -, hl⟩ := hall u
  rw [Function.iterate_succ_apply']
  exact piMove_mirror_piMove (iter_proper (P := Q) hc u) hr hl

lemma orbit_back {Q : Pent M.graph h} (hc : ProperOff M.graph h s)
    (hall : ∀ t, DLState Q ((piMove Q)^[t] s)) {L : ℕ} (hcyc : (piMove Q)^[L] s = s) :
    ∀ t, t ≤ L → (piMove Q.mirror)^[t] s = (piMove Q)^[L - t] s := by
  intro t
  induction t with
  | zero => intro _; rw [Nat.sub_zero, hcyc]; rfl
  | succ t ih =>
    intro ht
    rw [Function.iterate_succ_apply', ih (by omega), show L - t = (L - (t + 1)) + 1 by omega,
      back_step hc hall]

lemma orbit_in {Q : Pent M.graph h} (hc : ProperOff M.graph h s)
    (hall : ∀ t, DLState Q ((piMove Q)^[t] s)) {L : ℕ} (hL : 0 < L)
    (hcyc : (piMove Q)^[L] s = s) :
    ∀ t, ∃ u, (piMove Q.mirror)^[t] s = (piMove Q)^[u] s := by
  intro t
  induction t with
  | zero => exact ⟨0, rfl⟩
  | succ t ih =>
    obtain ⟨u, hu⟩ := ih
    rw [Function.iterate_succ_apply', hu]
    cases u with
    | zero =>
      refine ⟨L - 1, ?_⟩
      rw [Function.iterate_zero_apply, ← back_step hc hall (L - 1), Nat.sub_add_cancel hL, hcyc]
    | succ u => exact ⟨u, back_step hc hall u⟩

/-- **The mirror reverses an all-`DL` `π`-cycle.** If the forward `π`-orbit of `s` is all
`DL` and closes after `L > 0` steps, then under the mirror orientation it is an all-`DL`
`π`-cycle with the same state set, traversed backwards. -/
theorem gammaOrbit_mirror (hc : ProperOff M.graph h s) (hall : ∀ t, DLState P ((piMove P)^[t] s))
    {L : ℕ} (hL : 0 < L) (hcyc : (piMove P)^[L] s = s) :
    (∀ t, DLState P.mirror ((piMove P.mirror)^[t] s)) ∧
    (∀ t, t ≤ L → (piMove P.mirror)^[t] s = (piMove P)^[L - t] s) ∧
    (piMove P.mirror)^[L] s = s ∧
    Set.range (fun t => (piMove P.mirror)^[t] s) = Set.range (fun t => (piMove P)^[t] s) := by
  have dl : ∀ t, DLState P.mirror ((piMove P.mirror)^[t] s) := fun t => by
    obtain ⟨u, hu⟩ := orbit_in hc hall hL hcyc t
    rw [hu, dlState_mirror_iff]
    exact hall u
  have back := orbit_back hc hall hcyc
  have cyc : (piMove P.mirror)^[L] s = s := by
    rw [back L le_rfl, Nat.sub_self]; rfl
  refine ⟨dl, back, cyc, Set.Subset.antisymm ?_ ?_⟩
  · rintro _ ⟨t, rfl⟩
    obtain ⟨u, hu⟩ := orbit_in hc hall hL hcyc t
    exact ⟨u, hu.symm⟩
  · rintro _ ⟨t, rfl⟩
    have := orbit_in (Q := P.mirror) hc dl hL cyc t
    rw [Pent.mirror_mirror] at this
    obtain ⟨u, hu⟩ := this
    exact ⟨u, hu.symm⟩

/-! ### The `(5,5,5,5,6)` hole and the `(type, k)` sequence -/

/-- The outer ring read in the mirror: `w' t = w (-(t+1))` is the common outer neighbour of
`x' t = x (-t)` and `x' (t+1) = x (-t-1)`. -/
def wMirror (w : Fin 5 → Fin n) (t : Fin 5) : Fin n := w (-(t + 1))

private lemma a1 (t : Fin 5) : -(t + 4) = -t + 1 := by revert t; decide
private lemma a2 (t : Fin 5) : -(t + 1) = -t + 4 := by revert t; decide
private lemma a3 (t : Fin 5) : -(t + 4 + 1) = -t := by revert t; decide
private lemma a4 (q : Fin 5) : -(-q + 4) = q + 1 := by revert q; decide
private lemma a5 (q : Fin 5) : -(-q + 1) = q + 4 := by revert q; decide
private lemma a6 (q : Fin 5) : -(-q + 4 + 1) = q := by revert q; decide
private lemma a7 (t : Fin 5) : -(t + 1 + 1) + 1 = -(t + 1) := by revert t; decide

variable {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}

/-- The `(5,5,5,5,6)` hole data transports to the mirror, with `q ↦ -q`. -/
theorem Hole6.mirror (H : Hole6 P w m q) : Hole6 P.mirror (wMirror w) m (-q) where
  nbr t ht u := by
    have e := H.nbr (-t) (fun e => ht (by rw [← e, neg_neg])) u
    show M.graph.Adj (P.x (-t)) u ↔ u = h ∨ u = P.x (-(t + 4)) ∨ u = P.x (-(t + 1)) ∨
      u = w (-(t + 4 + 1)) ∨ u = w (-(t + 1))
    rw [e, a1, a2, a3]
    tauto
  nbrq u := by
    have e := H.nbrq u
    show M.graph.Adj (P.x (- -q)) u ↔ u = h ∨ u = P.x (-(-q + 4)) ∨ u = P.x (-(-q + 1)) ∨
      u = w (-(-q + 4 + 1)) ∨ u = m ∨ u = w (-(-q + 1))
    rw [neg_neg, e, a4, a5, a6]
    tauto
  ring t ht := by
    have hs : -(t + 1 + 1) + 1 ≠ q := by
      rw [a7]; intro e; exact ht (by rw [← e, neg_neg])
    have e := H.ring _ hs
    rw [a7] at e
    exact e.symm
  ringy := by
    show M.graph.Adj (w (-(-q + 4 + 1))) m
    rw [a6]; exact H.ringz.symm
  ringz := by
    show M.graph.Adj m (w (-(-q + 1)))
    rw [a5]; exact H.ringy.symm
  off _ _ := H.off _ _
  offm _ := H.offm _
  offh _ := H.offh _
  offmh := H.offmh

/-- The induced relabelling of `(type, k)`: the type is kept, `k ↦ 2 - k`. -/
def mrel (x : GType × Fin 5) : GType × Fin 5 := (x.1, 2 - x.2)

/-- `mrel` conjugates `gstep` to its inverse: the mirror table is the table run backwards. -/
theorem gstep_mrel : ∀ x, gstep (mrel (gstep x)) = mrel x := by
  rintro ⟨t, k⟩; cases t <;> revert k <;> decide

lemma gseq_R3k1 (u : ℕ) : gseq (10 * u + 6) = (.R3, 1) := by
  induction u with
  | zero => decide
  | succ u ih => rw [show 10 * (u + 1) + 6 = 10 * u + 6 + 10 by ring, gseq_period, ih]

private lemma b1 (j : Fin 5) : -(j + 1) = mj j + 1 := by revert j; decide
private lemma b2 (j : Fin 5) : -(mj j + 1) = j + 1 := by revert j; decide
private lemma b3 (j : Fin 5) : -(mj j + 3 + 1) = j + 3 := by revert j; decide

/-- At an `R3k1` state with its pair fact (`c (w q) = A`), the mirror type is `R3k1`. -/
lemma mirror_type_R3k1 {j : Fin 5} (hd : DoublyLocked P c j) (hq : q = j + 1)
    (hT : TypeR3 P w c j) (hp : PairFact P c j m (w q)) :
    HasTK P.mirror (wMirror w) (-q) c .R3 1 := by
  refine ⟨mj j, (doublyLocked_mirror_iff P c j).2 hd, by rw [hq]; exact b1 j, ?_⟩
  show c (w (-(mj j + 1))) = c (P.mirror.x (mj j + 4)) ∧
    c (w (-(mj j + 3 + 1))) = c (P.mirror.x (mj j + 1))
  rw [b2, b3, mx4, mx1]
  exact ⟨by rw [← hq]; exact hp.2, hT.2⟩

/-- One mirror step back along the forward orbit: `tk_step` for the mirror. -/
lemma tk_back (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ t, DLState P ((piMove P)^[t] s)) (u : ℕ) {x : GType × Fin 5}
    (hx : HasTK P.mirror (wMirror w) (-q) ((piMove P)^[u + 1] s) x.1 x.2) :
    HasTK P.mirror (wMirror w) (-q) ((piMove P)^[u] s) (gstep x).1 (gstep x).2 := by
  have e := back_step hc hall u
  have := tk_step H.mirror (iter_proper (P := P) hc (u + 1)) hx
    (by rw [e, dlState_mirror_iff]; exact hall u)
  rw [e] at this
  exact this

/-- **The `(type, k)` sequence under the mirror.** On the all-`DL` orbit of
`gamma_period_ten`, the `n`-th state has mirror `(type, k) = mrel (gseq n)`:
the same type, position `2 - k`. -/
theorem gseq_mirror {j₀ : Fin 5} (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ u, DLState P ((piMove P)^[u] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) :
    ∀ u, HasTK P.mirror (wMirror w) (-q) ((piMove P)^[u] s) (mrel (gseq u)).1
      (mrel (gseq u)).2 := by
  obtain ⟨tk, pr, -⟩ := gamma_period_ten H hc hall hr hq hT
  have base : ∀ N, gseq N = (.R3, 1) → 0 < N →
      HasTK P.mirror (wMirror w) (-q) ((piMove P)^[N] s) (mrel (gseq N)).1
        (mrel (gseq N)).2 := by
    intro N hN hN0
    obtain ⟨j, hd, hqj, hTj⟩ := tk N
    rw [hN] at hqj hTj
    have hp := pr N hN0 j hd.1
    rw [hN] at hp
    have e : mrel ((GType.R3, (1 : Fin 5))) = (.R3, 1) := by decide
    rw [hN, e]
    exact mirror_type_R3k1 hd hqj hTj hp
  have down : ∀ N d, d ≤ N →
      HasTK P.mirror (wMirror w) (-q) ((piMove P)^[N] s) (mrel (gseq N)).1 (mrel (gseq N)).2 →
      HasTK P.mirror (wMirror w) (-q) ((piMove P)^[N - d] s) (mrel (gseq (N - d))).1
        (mrel (gseq (N - d))).2 := by
    intro N d
    induction d with
    | zero => intro _ h0; rwa [Nat.sub_zero]
    | succ d ih =>
      intro hd h0
      have h' := ih (by omega) h0
      obtain ⟨u, hu⟩ : ∃ u, N - d = u + 1 := ⟨N - d - 1, by omega⟩
      rw [hu] at h'
      have := tk_back H hc hall u h'
      rw [gseq_succ, gstep_mrel] at this
      rw [show N - (d + 1) = u by omega]
      exact this
  intro u
  have := down (10 * u + 6) (10 * u + 6 - u) (by omega) (base _ (gseq_R3k1 u) (by omega))
  rw [show 10 * u + 6 - (10 * u + 6 - u) = u by omega] at this
  exact this

/-- **Time reversal of the period.** On an all-`DL` `π`-cycle of length `L > 0` starting at
`R3k4`, the mirror orbit (`π_mirror^[t] s`, `t ≤ L`) has mirror `(type, k)` equal to
`mrel (gseq (L - t))`: the ten-term table read backwards, with `k ↦ 2 - k`. -/
theorem gseq_mirror_reversed {j₀ : Fin 5} (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ u, DLState P ((piMove P)^[u] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) {L : ℕ} (hcyc : (piMove P)^[L] s = s) :
    ∀ t, t ≤ L → HasTK P.mirror (wMirror w) (-q) ((piMove P.mirror)^[t] s)
      (mrel (gseq (L - t))).1 (mrel (gseq (L - t))).2 := by
  intro t ht
  rw [orbit_back hc hall hcyc t ht]
  exact gseq_mirror H hc hall hr hq hT (L - t)

end sphere

end QuarterFloor

end SimpleGraph

#print axioms SimpleGraph.RotationSystem.mirror_mirror
#print axioms SimpleGraph.QuarterFloor.Pent.oriented_mirror
#print axioms SimpleGraph.QuarterFloor.lock1_mirror_iff
#print axioms SimpleGraph.QuarterFloor.lock2_mirror_iff
#print axioms SimpleGraph.QuarterFloor.piMove_mirror
#print axioms SimpleGraph.QuarterFloor.piInv_mirror
#print axioms SimpleGraph.QuarterFloor.gammaOrbit_mirror
#print axioms SimpleGraph.QuarterFloor.Hole6.mirror
#print axioms SimpleGraph.QuarterFloor.gstep_mrel
#print axioms SimpleGraph.QuarterFloor.gseq_mirror
#print axioms SimpleGraph.QuarterFloor.gseq_mirror_reversed
