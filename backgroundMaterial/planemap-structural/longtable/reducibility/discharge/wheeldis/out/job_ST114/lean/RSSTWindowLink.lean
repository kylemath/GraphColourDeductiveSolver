import RSSTWindowDefs
import RSSTWindowBasic

/-!
# ST-114 B3, link lemmas (Studio, 10 Nov)

For a link listing `w` of `u` (`IsLink`): the darts at `u` are the iterates of `u → w 0` (L1), so the link is injective
mod `d`; it has no chord (L2); each link edge has exactly one apex (L4). Index arithmetic mod `d` is reduced to `ite`
via `succ_mod_eq`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap RotationSystem

variable {n : ℕ} {T : SphericalMap n} {u : Fin n} {d : ℕ} {w : ℕ → Fin n}

theorem succ_mod_eq {a d : ℕ} (ha : a < d) : (a + 1) % d = if a + 1 = d then 0 else a + 1 := by
  split_ifs with h
  · rw [h, Nat.mod_self]
  · exact Nat.mod_eq_of_lt (by omega)

theorem succ_mod_mod (a d : ℕ) : (a + 1) % d = (a % d + 1) % d := by
  conv_rhs => rw [Nat.add_mod, Nat.mod_mod, ← Nat.add_mod]

/-- Two link indices are close: equal or cyclically adjacent mod `d`. -/
def Close (d a b : ℕ) : Prop := b % d = a % d ∨ b % d = (a + 1) % d ∨ a % d = (b + 1) % d

theorem Close.symm {a b : ℕ} (h : Close d a b) : Close d b a := by
  rcases h with h | h | h
  · exact Or.inl h.symm
  · exact Or.inr (Or.inr h)
  · exact Or.inr (Or.inl h)

theorem Close.shift {a b : ℕ} (h : Close d a b) (m : ℕ) : Close d (m + a) (m + b) := by
  rcases h with h | h | h
  · exact Or.inl (Nat.ModEq.add_left m h)
  · exact Or.inr (Or.inl (Nat.ModEq.add_left m h))
  · exact Or.inr (Or.inr (Nat.ModEq.add_left m h))

namespace IsLink

theorem nx_of_adj (hL : IsLink T u d w) {i : ℕ} (h : T.Adj u (w i)) : Nx T u (w i) (w (i + 1)) := by
  have := hL.step i
  unfold rotNbr at this
  rw [dif_pos h] at this
  exact ⟨h, by simpa using this⟩

theorem adj (hL : IsLink T u d w) : ∀ i, T.Adj u (w i) := by
  intro i
  induction i with
  | zero => exact hL.adj0
  | succ i ih => exact nx_adj_right (hL.nx_of_adj ih)

theorem nx (hL : IsLink T u d w) (i : ℕ) : Nx T u (w i) (w (i + 1)) := hL.nx_of_adj (hL.adj i)

theorem ne (hL : IsLink T u d w) (i : ℕ) : w i ≠ u := (hL.adj i).ne.symm

theorem dart_iter (hL : IsLink T u d w) (i : ℕ) :
    (⇑T.rotation.next)^[i] ⟨(u, w 0), hL.adj 0⟩ = ⟨(u, w i), hL.adj i⟩ := by
  induction i with
  | zero => rfl
  | succ i ih =>
    rw [Function.iterate_succ_apply', ih]
    obtain ⟨_, _, e⟩ := nx_dart (hL.nx i)
    exact e

theorem d5 (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) : 5 ≤ d := hL.deg ▸ hT.minDeg u

theorem per_mod (hL : IsLink T u d w) (t : ℕ) : w (t % d) = w t := by
  conv_rhs => rw [← Nat.mod_add_div t d]
  induction t / d with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, hL.per, ih]

/-- L1. The link is injective below `d`. -/
theorem inj (hL : IsLink T u d w) {i j : ℕ} (hi : i < d) (hj : j < d) (h : w i = w j) : i = j := by
  have e : (⇑T.rotation.next)^[i] ⟨(u, w 0), hL.adj 0⟩ = (⇑T.rotation.next)^[j] ⟨(u, w 0), hL.adj 0⟩ := by
    rw [hL.dart_iter i, hL.dart_iter j]
    apply Dart.ext; exact Prod.ext rfl h
  have := rot_iter_mod _ rfl e
  simp only [hL.deg] at this
  rwa [Nat.mod_eq_of_lt hi, Nat.mod_eq_of_lt hj] at this

theorem eq_iff (hL : IsLink T u d w) (hd : 0 < d) (i j : ℕ) : w i = w j ↔ i % d = j % d := by
  constructor
  · intro h
    exact hL.inj (Nat.mod_lt _ hd) (Nat.mod_lt _ hd) (by rw [hL.per_mod, hL.per_mod]; exact h)
  · intro h
    rw [← hL.per_mod i, ← hL.per_mod j, h]

theorem ww (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) (i : ℕ) : T.Adj (w i) (w (i + 1)) :=
  nx_adj_left (nx_tri hT.triangulated (hL.nx i)).2

/-- L2. The link has no chord. -/
theorem chordless (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) (i j : ℕ) (h : T.Adj (w i) (w j)) :
    j % d = (i + 1) % d ∨ i % d = (j + 1) % d := by
  have hd : 0 < d := by have := hL.d5 hT; omega
  have hf := hT.noSep u (w i) (w j) (hL.adj i) h (hL.adj j).symm
  rcases facial_nx hT.triangulated hf with h1 | h1
  · left
    exact ((hL.eq_iff hd _ _).1 (nx_unique (hL.nx i) h1)).symm
  · right
    exact ((hL.eq_iff hd _ _).1 (nx_unique (hL.nx j) h1)).symm

/-- The chord condition for indices below `d`, in `ite` form. -/
theorem chordless_lt (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) {i j : ℕ} (hi : i < d) (hj : j < d)
    (h : T.Adj (w i) (w j)) :
    j = (if i + 1 = d then 0 else i + 1) ∨ i = (if j + 1 = d then 0 else j + 1) := by
  have := hL.chordless hT i j h
  rwa [Nat.mod_eq_of_lt hi, Nat.mod_eq_of_lt hj, succ_mod_eq hi, succ_mod_eq hj] at this

/-- The shifted listing `t ↦ w (a + t)` is a link listing. -/
theorem shift (hL : IsLink T u d w) (a : ℕ) : IsLink T u d (fun t => w (a + t)) where
  deg := hL.deg
  per t := by show w (a + (t + d)) = w (a + t); rw [← Nat.add_assoc, hL.per]
  adj0 := hL.adj a
  step t := hL.step (a + t)

/-- L4 (existence). The apex `s_i`: the vertex after `w_i` in the rotation at `w_{i+1}`. It is not `u`. -/
theorem apex (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) (i : ℕ) :
    ∃ s, s ≠ u ∧ Nx T (w (i + 1)) (w i) s ∧ Nx T s (w (i + 1)) (w i) ∧ T.Adj (w i) s ∧
      T.Adj (w (i + 1)) s := by
  have htri := hT.triangulated
  have h2 := (nx_tri htri (hL.nx i)).1
  have hw : T.Adj (w (i + 1)) (w i) := nx_adj_right h2
  have hs : Nx T (w (i + 1)) (w i) (T.rotation.next ⟨(w (i + 1), w i), hw⟩).snd := ⟨hw, rfl⟩
  set s := (T.rotation.next ⟨(w (i + 1), w i), hw⟩).snd
  have t := nx_tri htri hs
  refine ⟨s, ?_, hs, t.1, nx_adj_left t.2, nx_adj_right hs⟩
  intro hsu
  rw [hsu] at hs
  obtain ⟨_, _, E1⟩ := nx_dart hs
  obtain ⟨_, _, E2⟩ := nx_dart h2
  have e : (⇑T.rotation.next)^[2] (⟨(w (i + 1), w i), hw⟩ : T.Dart) =
      (⇑T.rotation.next)^[0] ⟨(w (i + 1), w i), hw⟩ := by
    simp only [Function.iterate_succ_apply', Function.iterate_zero_apply]
    rw [E1, E2]
  have := rot_iter_mod (v := w (i + 1)) _ rfl e
  have h5 := hT.minDeg (w (i + 1))
  rw [Nat.zero_mod, Nat.mod_eq_of_lt (by omega)] at this
  omega

/-- L4 (uniqueness). Any apex of `w_i w_{i+1}` is the rotation successor of `w_i` at `w_{i+1}`. -/
theorem apex_eq (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) {i : ℕ} {s y : Fin n}
    (hs : Nx T (w (i + 1)) (w i) s) (hy : IsApex T u w i y) : y = s := by
  obtain ⟨hyu, hiy, hi1y⟩ := hy
  have h2 := (nx_tri hT.triangulated (hL.nx i)).1
  have hw : T.Adj (w (i + 1)) (w i) := nx_adj_right h2
  have hf := hT.noSep (w (i + 1)) (w i) y hw hiy hi1y.symm
  rcases facial_nx hT.triangulated hf with h1 | h1
  · exact nx_unique h1 hs
  · exact absurd (nx_inj_left h1 h2) hyu

/-- The apex is no link vertex (review point (a)). -/
theorem apex_off_link (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) {i : ℕ} {x : Fin n}
    (hx : IsApex T u w i x) (k : ℕ) : w k ≠ x := by
  intro hk
  obtain ⟨-, h1, h2⟩ := hx
  rw [← hk] at h1 h2
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  have c1 := hL.chordless hT i k h1
  have c2 := hL.chordless hT (i + 1) k h2
  rw [succ_mod_mod (i + 1)] at c2
  have hJ : (i + 1) % d = (i % d + 1) % d := succ_mod_mod i d
  rw [succ_mod_mod i] at c1
  rw [succ_mod_mod k] at c1 c2
  have hi := Nat.mod_lt i hd
  have hk' := Nat.mod_lt k hd
  have hj := Nat.mod_lt (i + 1) hd
  generalize (i + 1) % d = J at *
  generalize i % d = I at *
  generalize k % d = K at *
  rw [succ_mod_eq hi] at c1 hJ
  rw [succ_mod_eq hk'] at c1 c2
  rw [succ_mod_eq hj] at c2
  split_ifs at c1 c2 hJ <;> omega

/-- The two faces of the link edge `u w_0`: `w_{d-1}` sees one, `w_1` the other. -/
theorem faces_u0 (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) (h1 : T.Adj (w (d - 1)) u)
    (h2 : T.Adj u (w 0)) (h3 : T.Adj (w 1) (w 0)) (h4 : T.Adj (w 0) u) :
    T.faceOf ⟨(w (d - 1), u), h1⟩ = T.faceOf ⟨(u, w 0), h2⟩ ∧
      T.faceOf ⟨(w 1, w 0), h3⟩ = T.faceOf ⟨(w 0, u), h4⟩ := by
  have d5 := hL.d5 hT
  have hN := hL.nx (d - 1)
  rw [show d - 1 + 1 = 0 + d by omega, hL.per] at hN
  refine ⟨face_nx hN h1 h2, ?_⟩
  have A := face_nx (hL.nx 0) h4 (hL.adj 1)
  have B := face_nx (nx_tri hT.triangulated (hL.nx 0)).1 (hL.adj 1) h3
  exact (A.trans B).symm

end IsLink

end SimpleGraph.SphericalMap.RSSTSeed
