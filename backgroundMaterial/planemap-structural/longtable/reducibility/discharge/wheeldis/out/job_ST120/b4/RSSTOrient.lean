import RSSTWindow

/-!
# ST-120 B4 M1: orientation coherence of the window

Studio, 10 Nov. Extends B3 (`window_induced`) with the arc order of every rotation in the 2-ball of `u`
(B3_STATEMENT §9 note 1). No existing module is edited.

## Convention (fixed here, used by M2/M3)

* "ccw" of the spec (§2) is `T.rotation.next`. A link listing `w` (`IsLink`) follows `T.rotation.next` at `u`:
  `rot(u) = w_0, w_1, …, w_{d-1}`.
* Then, reading `rot(w_i)` with `T.rotation.next` from `u` (`rotNbr T (w i) u k`, `D = deg w_i`):
  `k = 0 ↦ u`, `1 ↦ w_{i-1}`, `2 ↦ s_{i-1}`, `3..D-3 ↦ p_i.1..p_i.(D-5)`, `D-2 ↦ s_i`, `D-1 ↦ w_{i+1}`.
  This is exactly B2's / the spec's `rot(w_i) = u, w_{i-1}, s_{i-1}, p_i.1, …, s_i, w_{i+1}`, in the same direction for
  every `i` (field `at1`, `at2`, `atL2`, `atL1`).
* Every vertex `x = rotNbr T (w i) u k` (`1 ≤ k ≤ D-2`, i.e. `w_{i-1}`, a seg vertex) has the matching contiguous arc
  `next(k+1), w_i, next(k-1)` in its own rotation (field `arc`): `rot(x)` runs `…, y_{k+1}, w_i, y_{k-1}, …`.
* `apexV T w i = s_i` is defined as the vertex after `w_i` in `rot(w_{i+1})`; `rot(s_i)` contains `w_{i+1}, w_i`
  consecutively (field `apexRot`).
* **Mirror windows.** Nothing here is proved for the reversed chirality: a listing of `rot(u)` in the `next⁻¹`
  direction is not an `IsLink` of `T`. The mirror statement is this same theorem applied to the mirrored map
  (`rotation.next` replaced by its inverse), with the link reversed. The 71 parts are closed under reflection (spec §3.2),
  so the soundness proof (M3) never needs it: `τ_RSST` is defined on `T`'s own rotation and every fit, mirror parts
  included, is evaluated in that one direction.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap RotationSystem

variable {n : ℕ} {T : SphericalMap n}

/-! ## `rotNbr` basics -/

theorem iter_fst (e : T.Dart) (k : ℕ) : ((⇑T.rotation.next)^[k] e).fst = e.fst := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply', T.rotation.next_fst, ih]

theorem rotNbr_eq {v a : Fin n} (h : T.Adj v a) (k : ℕ) :
    rotNbr T v a k = ((⇑T.rotation.next)^[k] ⟨(v, a), h⟩).snd := by
  unfold rotNbr; rw [dite_cond_eq_true (eq_true h)]

theorem rotNbr_adj {v a : Fin n} (h : T.Adj v a) (k : ℕ) : T.Adj v (rotNbr T v a k) := by
  rw [rotNbr_eq h]
  have := ((⇑T.rotation.next)^[k] (⟨(v, a), h⟩ : T.Dart)).adj
  have hf := iter_fst (T := T) ⟨(v, a), h⟩ k
  rw [show ((⇑T.rotation.next)^[k] (⟨(v, a), h⟩ : T.Dart)).toProd.1 = v from hf] at this
  exact this

theorem rotNbr_dart {v a : Fin n} (h : T.Adj v a) (k : ℕ) :
    (⇑T.rotation.next)^[k] ⟨(v, a), h⟩ = ⟨(v, rotNbr T v a k), rotNbr_adj h k⟩ := by
  apply Dart.ext; exact Prod.ext (iter_fst _ k) (rotNbr_eq h k).symm

theorem rotNbr_zero {v a : Fin n} (h : T.Adj v a) : rotNbr T v a 0 = a := by
  rw [rotNbr_eq h]; rfl

theorem rotNbr_add {v a : Fin n} (h : T.Adj v a) (j k : ℕ) :
    rotNbr T v (rotNbr T v a j) k = rotNbr T v a (j + k) := by
  rw [rotNbr_eq h (j + k), Nat.add_comm, Function.iterate_add_apply, rotNbr_dart h j]
  exact rotNbr_eq (rotNbr_adj h j) k

theorem rotNbr_nx {v a : Fin n} (h : T.Adj v a) (k : ℕ) : Nx T v (rotNbr T v a k) (rotNbr T v a (k + 1)) := by
  refine ⟨rotNbr_adj h k, ?_⟩
  rw [rotNbr_eq h (k + 1), Function.iterate_succ_apply', rotNbr_dart h k]

theorem rotNbr_one_of_nx {v a b : Fin n} (h : Nx T v a b) : rotNbr T v a 1 = b := by
  have := rotNbr_nx (T := T) (nx_adj_left h) 0
  rw [rotNbr_zero (nx_adj_left h)] at this
  exact nx_unique this h

/-- The darts at `v` have period `deg v` under the rotation. -/
theorem iter_deg (e : T.Dart) : (⇑T.rotation.next)^[T.graph.degree e.fst] e = e := by
  classical
  let σ := T.rotation.neighborRotation e.fst
  let a : T.graph.neighborSet e.fst := ⟨e.snd, e.adj⟩
  have hdw : T.graph.dartOfNeighborSet e.fst a = e := rfl
  have hsemi : Function.Semiconj (T.graph.dartOfNeighborSet e.fst) σ T.rotation.next :=
    T.rotation.neighbor_rotation_dart e.fst
  have hp : Function.minimalPeriod σ a = T.graph.degree e.fst := T.rotation.neighbor_period_eq_degree _ a
  have := hsemi.iterate_right (T.graph.degree e.fst) a
  rw [hdw] at this
  rw [← this, ← hp, Function.iterate_minimalPeriod]
  exact hdw

theorem rotNbr_per {v a : Fin n} (h : T.Adj v a) (k : ℕ) :
    rotNbr T v a (k + T.graph.degree v) = rotNbr T v a k := by
  rw [rotNbr_eq h, rotNbr_eq h, Function.iterate_add_apply]
  rw [show (⇑T.rotation.next)^[T.graph.degree v] (⟨(v, a), h⟩ : T.Dart) = ⟨(v, a), h⟩ from
    iter_deg (T := T) ⟨(v, a), h⟩]

/-- `k ↦ rotNbr T v a k` is a link listing of `v`. -/
theorem rotNbr_isLink {v a : Fin n} (h : T.Adj v a) : IsLink T v (T.graph.degree v) (rotNbr T v a) where
  deg := rfl
  per k := rotNbr_per h k
  adj0 := by rw [rotNbr_zero h]; exact h
  step k := rotNbr_add h k 1

/-! ## Neighbour sums along a link -/

theorem link_image {u : Fin n} {d : ℕ} {w : ℕ → Fin n} (hL : IsLink T u d w) :
    T.graph.neighborFinset u = (Finset.range d).image w := by
  classical
  symm
  apply Finset.eq_of_subset_of_card_le
  · intro x hx
    obtain ⟨i, -, rfl⟩ := Finset.mem_image.1 hx
    exact (mem_neighborFinset _ _ _).2 (hL.adj i)
  · rw [card_neighborFinset_eq_degree, hL.deg, Finset.card_image_of_injOn, Finset.card_range]
    intro i hi j hj e
    exact hL.inj (Finset.mem_range.1 hi) (Finset.mem_range.1 hj) e

theorem sum_nbr_link {u : Fin n} {d : ℕ} {w : ℕ → Fin n} (hL : IsLink T u d w) {M : Type*} [AddCommMonoid M]
    (f : Fin n → M) : ∑ y ∈ T.graph.neighborFinset u, f y = ∑ a ∈ Finset.range d, f (w a) := by
  classical
  rw [link_image hL, Finset.sum_image]
  intro i hi j hj e
  exact hL.inj (Finset.mem_range.1 hi) (Finset.mem_range.1 hj) e

/-! ## M1: orientation coherence -/

/-- The apex `s_i`: the vertex after `w_i` in the rotation at `w_{i+1}` (B3 L4). -/
noncomputable def apexV (T : SphericalMap n) (w : ℕ → Fin n) (i : ℕ) : Fin n := rotNbr T (w (i + 1)) (w i) 1

/-- **M1 conclusion.** The rotation at every link vertex `w_i`, read from `u` with `T.rotation.next`, is
`u, w_{i-1}, s_{i-1}, (privates), s_i, w_{i+1}` (indices `0, 1, 2, …, D-2, D-1`, `D = deg w_i`); it has period `D` and
is injective below `D`; every vertex of that rotation other than `u` and `w_{i+1}` has the arc
`next, w_i, previous` in its own rotation; and `rot(s_i)` has `w_{i+1}` then `w_i`. Indices `i - 1` are written as
`i` with hub `w (i+1)` to avoid subtraction. -/
structure WindowOriented (T : SphericalMap n) (u : Fin n) (w : ℕ → Fin n) : Prop where
  at0 : ∀ i, rotNbr T (w i) u 0 = u
  /-- `rot(w_{i+1})[1] = w_i` -/
  at1 : ∀ i, rotNbr T (w (i + 1)) u 1 = w i
  /-- `rot(w_{i+1})[2] = s_i` -/
  at2 : ∀ i, rotNbr T (w (i + 1)) u 2 = apexV T w i
  /-- `rot(w_i)[D-2] = s_i` -/
  atL2 : ∀ i, rotNbr T (w i) u (T.graph.degree (w i) - 2) = apexV T w i
  /-- `rot(w_i)[D-1] = w_{i+1}` -/
  atL1 : ∀ i, rotNbr T (w i) u (T.graph.degree (w i) - 1) = w (i + 1)
  per : ∀ i k, rotNbr T (w i) u (k + T.graph.degree (w i)) = rotNbr T (w i) u k
  inj : ∀ i k k', k < T.graph.degree (w i) → k' < T.graph.degree (w i) →
    rotNbr T (w i) u k = rotNbr T (w i) u k' → k = k'
  /-- consecutive in `rot(w_i)` -/
  nx : ∀ i k, Nx T (w i) (rotNbr T (w i) u k) (rotNbr T (w i) u (k + 1))
  /-- the matching arc in `rot(x)` for `x = rot(w_i)[k+1]`: after `rot(w_i)[k+2]` comes `w_i`, then `rot(w_i)[k]` -/
  arc : ∀ i k, Nx T (rotNbr T (w i) u (k + 1)) (rotNbr T (w i) u (k + 2)) (w i) ∧
    Nx T (rotNbr T (w i) u (k + 1)) (w i) (rotNbr T (w i) u k)
  /-- `rot(s_i)`: `w_{i+1}` then `w_i` -/
  apexRot : ∀ i, Nx T (apexV T w i) (w (i + 1)) (w i)
  /-- `s_i` is the B3 apex: not `u`, adjacent to `w_i` and `w_{i+1}` -/
  apex : ∀ i, IsApex T u w i (apexV T w i)

/-- **M1, orientation coherence** (extends B3 `window_induced`). -/
theorem window_oriented (hT : ClaimGlue.Internally6 T) {u : Fin n} {d : ℕ} {w : ℕ → Fin n}
    (hL : IsLink T u d w) : WindowOriented T u w := by
  have htri := hT.triangulated
  have hwu : ∀ i, T.Adj (w i) u := fun i => (hL.adj i).symm
  -- the apex as a rotation successor
  have hap : ∀ i, Nx T (w (i + 1)) (w i) (apexV T w i) := by
    intro i
    obtain ⟨s, -, hs, -⟩ := hL.apex hT i
    unfold apexV; rw [rotNbr_one_of_nx hs]; exact hs
  have rot1 : ∀ i, rotNbr T (w (i + 1)) u 1 = w i := fun i =>
    rotNbr_one_of_nx (nx_tri htri (hL.nx i)).1
  have hD : ∀ i, 5 ≤ T.graph.degree (w i) := fun i => hT.minDeg _
  -- a vertex is the predecessor of `b` iff it is at index `D-1` before it
  have pred : ∀ i (a b : Fin n) (k : ℕ), 1 ≤ k → Nx T (w i) a b → rotNbr T (w i) u k = b →
      rotNbr T (w i) u (k - 1) = a := by
    intro i a b k hk hab hb
    have h1 := rotNbr_nx (hwu i) (k - 1)
    rw [show k - 1 + 1 = k by omega, hb] at h1
    exact nx_inj_left h1 hab
  have atL1 : ∀ i, rotNbr T (w i) u (T.graph.degree (w i) - 1) = w (i + 1) := by
    intro i
    have e := rotNbr_per (hwu i) 0
    rw [Nat.zero_add, rotNbr_zero (hwu i)] at e
    exact pred i _ _ (T.graph.degree (w i)) (by have := hD i; omega) (nx_tri htri (hL.nx i)).2 e
  refine ⟨fun i => rotNbr_zero (hwu i), rot1, ?_, ?_, atL1, fun i k => rotNbr_per (hwu i) k, ?_,
    fun i k => rotNbr_nx (hwu i) k, ?_, ?_, ?_⟩
  · intro i
    have := rotNbr_add (hwu (i + 1)) 1 1
    rw [rot1, rotNbr_one_of_nx (hap i)] at this
    exact this.symm
  · intro i
    have h2 := (nx_tri htri (hap i)).2
    have := pred i _ _ (T.graph.degree (w i) - 1) (by have := hD i; omega) h2 (atL1 i)
    rwa [show T.graph.degree (w i) - 1 - 1 = T.graph.degree (w i) - 2 by omega] at this
  · intro i k k' hk hk' e
    exact (rotNbr_isLink (hwu i)).inj hk hk' e
  · intro i k
    have a1 := nx_tri htri (rotNbr_nx (hwu i) (k + 1))
    have a0 := nx_tri htri (rotNbr_nx (hwu i) k)
    exact ⟨a1.2, a0.1⟩
  · intro i; exact (nx_tri htri (hap i)).1
  · intro i
    obtain ⟨s, hsu, hs1, -, hsi, hsi1⟩ := hL.apex hT i
    have : apexV T w i = s := nx_unique (hap i) hs1
    rw [this]; exact ⟨hsu, hsi, hsi1⟩

#print axioms window_oriented

end SimpleGraph.SphericalMap.RSSTSeed
