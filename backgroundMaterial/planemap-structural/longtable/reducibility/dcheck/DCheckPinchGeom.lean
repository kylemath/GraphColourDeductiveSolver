import DCheckPinch
import SideCycle

/-! Job 26 route B2, step (ii′) (exploratory): the geometry of a pinched face walk.

A face walk `ρ` of `G` (period `r`, `faceNext` steps along it) visits the vertex `u` exactly at positions `0` and
`m`. Its A-arc `ρ 0 … ρ (m-1)` closes up at `u` into a cycle `C_A` of `G` (chords allowed). With a face potential
`c` of `C_A`, side A is `C_A` plus the far side (potential `c f + 1`, `f` the walk's face), and side B is the rest
plus `u`. Then:
- the arc's interior vertices have no near darts besides the face corner (consecutive jumps), so every edge
  of `G` lies in a side (`hcut`);
- at `u` the rotation runs from the A-arc dart into ρ(m-1) through near darts only, up to the dart into ρ 1, and back
  through far darts only;
- so the two kept maps (`subgraph_tracked`) have the two arcs as ring faces.
Their `RingTNC`, plus `RingTNC.of_pinch`, give `RingTNC G r ρ h`, hence `KempeMatching` for the realised codes
of a pinched ring. -/

namespace SimpleGraph.SphericalMap
open RotationSystem VacancyCliqueLift VacancyIcosahedral VacancySlide DCheck DCheck.R2

variable {n : ℕ}

/-- A cycle of `T` of length `r ≥ 3` (chords allowed). -/
structure Cyc (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) : Prop where
  three : 3 ≤ r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, T.Adj (ρ t) (ρ (t + 1))
  inj : ∀ s t, s < r → t < r → ρ s = ρ t → s = t

variable {T : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n}

theorem Cyc.per_mod (C : Cyc T r ρ) (t : ℕ) : ρ (t % r) = ρ t := by
  conv_rhs => rw [← Nat.mod_add_div t r]
  induction t / r with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, C.per, ih]

theorem Cyc.onCyc (C : Cyc T r ρ) (t : ℕ) : OnCyc r ρ (ρ t) :=
  ⟨t % r, Nat.mod_lt _ (by have := C.three; omega), C.per_mod t⟩

theorem Cyc.mod_eq_of (C : Cyc T r ρ) {s t : ℕ} (h : ρ s = ρ t) : s % r = t % r := by
  have hpos : 0 < r := by have := C.three; omega
  exact C.inj _ _ (Nat.mod_lt _ hpos) (Nat.mod_lt _ hpos) (by rw [C.per_mod, C.per_mod]; exact h)

theorem cycInd_even' (C : Cyc T r ρ) : IsEven T (cycInd T r ρ) := by
  classical
  intro x
  change ∑ e : T.graph.edgeSet, (if x ∈ e.val then cycInd T r ρ e else 0) = 0
  have split : ∀ e : T.graph.edgeSet, (if x ∈ e.val then cycInd T r ρ e else 0) =
      ∑ t ∈ Finset.range r,
        (if x ∈ e.val then (if e.val = s(ρ t, ρ (t + 1)) then (1 : ZMod 2) else 0) else 0) := by
    intro e; unfold cycInd; split_ifs <;> simp
  rw [Finset.sum_congr rfl (fun e _ => split e), Finset.sum_comm]
  have h1 : ∀ t ∈ Finset.range r, (∑ e : T.graph.edgeSet,
      (if x ∈ e.val then (if e.val = s(ρ t, ρ (t + 1)) then (1 : ZMod 2) else 0) else 0)) =
      (if x = ρ t then 1 else 0) + (if x = ρ (t + 1) then 1 else 0) := by
    intro t _
    rw [incidence_single T (C.adj t)]
    have hne := (C.adj t).ne
    by_cases a : x = ρ t
    · subst a; simp [hne]
    · by_cases b : x = ρ (t + 1)
      · subst b; simp [a]
      · simp [a, b]
  rw [Finset.sum_congr rfl h1, Finset.sum_add_distrib]
  have shift : ∑ t ∈ Finset.range r, (if x = ρ (t + 1) then (1 : ZMod 2) else 0) =
      ∑ t ∈ Finset.range r, (if x = ρ t then (1 : ZMod 2) else 0) := by
    have hr : 0 < r := by have := C.three; omega
    obtain ⟨r', rfl⟩ : ∃ r', r = r' + 1 := ⟨r - 1, by omega⟩
    rw [Finset.sum_range_succ, Finset.sum_range_succ' (fun t => if x = ρ t then (1 : ZMod 2) else 0)]
    rw [show r' + 1 = 0 + (r' + 1) by omega, C.per 0]
  rw [shift]
  generalize (∑ t ∈ Finset.range r, if x = ρ t then (1 : ZMod 2) else 0) = a
  exact (show ∀ a : ZMod 2, a + a = 0 by decide) a

theorem exists_cycPotential' (C : Cyc T r ρ) : ∃ c, CycPotential T r ρ c :=
  T.fills _ (cycInd_even' C)

theorem cycInd_off' (C : Cyc T r ρ) (d : T.Dart) (hx : ¬ OnCyc r ρ d.fst) :
    cycInd T r ρ (edgeOfDart d) = 0 := by
  classical
  unfold cycInd
  apply Finset.sum_eq_zero
  intro t ht
  have hm : d.fst ∈ (edgeOfDart d).val := Sym2.mem_mk_left _ _
  rw [if_neg]
  intro h
  rw [h, Sym2.mem_iff] at hm
  rcases hm with hm | hm
  · exact hx ⟨t, Finset.mem_range.1 ht, hm.symm⟩
  · apply hx
    refine ⟨(t + 1) % r, Nat.mod_lt _ (by have := Finset.mem_range.1 ht; omega), ?_⟩
    rw [hm, C.per_mod]

theorem side_constC' (C : Cyc T r ρ) {c : T.Face → ZMod 2} (hc : CycPotential T r ρ c)
    {x : Fin n} (hx : ¬ OnCyc r ρ x) (d e : T.Dart) (hd : d.fst = x) (he : e.fst = x) :
    c (T.faceOf d) = c (T.faceOf e) := by
  obtain ⟨k, hk⟩ := T.rotation.cyclic d e (hd.trans he.symm)
  rw [← hk]
  clear hk
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', faceOf_next]
    set y := (⇑T.rotation.next)^[k] d
    have hy : y.fst = x := (iterate_next_fst T k d).trans hd
    have h0 := cycInd_off' C y (by rw [hy]; exact hx)
    have := zmod2_swap _ _ _ (hc y)
    rw [h0, zero_add] at this
    rw [this, ih]

theorem onSide_of_dartC' (C : Cyc T r ρ) {c : T.Face → ZMod 2} (hc : CycPotential T r ρ c)
    {x : Fin n} (hx : ¬ OnCyc r ρ x) (d : T.Dart) (hd : d.fst = x) :
    OnSide T c (c (T.faceOf d)) x :=
  fun e he => (side_constC' C hc hx d e hd he).symm

/-- The indicator of the cycle is `1` on a cycle edge. -/
theorem cycInd_cycle' (C : Cyc T r ρ) (t : ℕ) :
    cycInd T r ρ (edgeOfDart ⟨(ρ t, ρ (t + 1)), C.adj t⟩) = 1 := by
  classical
  have hpos : 0 < r := by have := C.three; omega
  unfold cycInd
  rw [Finset.sum_eq_single (t % r)]
  · rw [if_pos]
    change s(ρ t, ρ (t + 1)) = s(ρ (t % r), ρ (t % r + 1))
    have : ρ (t % r + 1) = ρ (t + 1) := by
      rw [← C.per_mod (t % r + 1), ← C.per_mod (t + 1), Nat.add_mod (t % r), Nat.mod_mod,
        ← Nat.add_mod]
    rw [C.per_mod, this]
  · intro u hu hne
    rw [if_neg]
    intro he
    change s(ρ t, ρ (t + 1)) = s(ρ u, ρ (u + 1)) at he
    have hu' := Finset.mem_range.1 hu
    rw [Sym2.eq_iff] at he
    rcases he with ⟨e1, -⟩ | ⟨e1, e2⟩
    · exact hne (by rw [← Nat.mod_eq_of_lt hu']; exact (C.mod_eq_of e1).symm)
    · have m1 := C.mod_eq_of e1
      have m2 := C.mod_eq_of e2
      have : (u + 2) % r = u % r := by
        rw [show u + 2 = (u + 1) + 1 by omega, Nat.add_mod (u + 1), ← m1, ← Nat.add_mod, ← m2]
      have h0 := Nat.sub_mod_eq_zero_of_mod_eq this
      rw [show u + 2 - u = 2 by omega, Nat.mod_eq_of_lt (by have := C.three; omega : 2 < r)] at h0
      omega
  · intro h; exact absurd (Finset.mem_range.2 (Nat.mod_lt _ hpos)) h


/-- At a cycle vertex `ρ s`, a dart into neither cycle neighbour carries indicator `0`. -/
theorem cycInd_dart_off (C : Cyc T r ρ) {s : ℕ} (d : T.Dart) (hd : d.fst = ρ s)
    (h1 : d.snd ≠ ρ (s + 1)) (h2 : d.snd ≠ ρ (s + r - 1)) : cycInd T r ρ (edgeOfDart d) = 0 := by
  classical
  have hpos : 0 < r := by have := C.three; omega
  unfold cycInd
  apply Finset.sum_eq_zero
  intro t ht
  rw [if_neg]
  intro he
  change s(d.fst, d.snd) = s(ρ t, ρ (t + 1)) at he
  rw [Sym2.eq_iff] at he
  rcases he with ⟨e1, e2⟩ | ⟨e1, e2⟩
  · apply h1
    have m := C.mod_eq_of (hd.symm.trans e1)
    rw [e2, ← C.per_mod (t + 1), ← C.per_mod (s + 1), Nat.add_mod t, ← m, ← Nat.add_mod]
  · apply h2
    have m := C.mod_eq_of (hd.symm.trans e1)
    have h3 : (s + (r - 1)) % r = (t + 1 + (r - 1)) % r := Nat.ModEq.add_right _ m
    rw [show t + 1 + (r - 1) = t + r by omega, Nat.add_mod_right] at h3
    rw [e2, ← C.per_mod t, ← C.per_mod (s + r - 1), show s + r - 1 = s + (r - 1) by omega, h3]

/-- One rotation step changes the potential by the indicator. -/
theorem next_jump {c : T.Face → ZMod 2} {r' : ℕ} {ρ' : ℕ → Fin n} (hc : CycPotential T r' ρ' c) (x : T.Dart) :
    c (T.faceOf (T.rotation.next x)) = c (T.faceOf x) + cycInd T r' ρ' (edgeOfDart x) := by
  rw [faceOf_next, hc x]
  generalize c (T.faceOf x) = a; generalize c (T.faceOf x.symm) = b
  revert a b; decide

/-- The potential is constant along rotation steps whose darts carry indicator `0`. -/
theorem iterate_const {c : T.Face → ZMod 2} {r' : ℕ} {ρ' : ℕ → Fin n} (hc : CycPotential T r' ρ' c)
    (d0 : T.Dart) : ∀ k, (∀ j, j < k → cycInd T r' ρ' (edgeOfDart ((⇑T.rotation.next)^[j] d0)) = 0) →
      c (T.faceOf ((⇑T.rotation.next)^[k] d0)) = c (T.faceOf d0) := by
  intro k
  induction k with
  | zero => intro _; rfl
  | succ k ih =>
    intro h
    rw [Function.iterate_succ_apply', next_jump hc, h k (by omega), add_zero, ih (fun j hj => h j (by omega))]

/-- First arrival along the rotation. -/
theorem first_arrival (d e : T.Dart) (he : d.fst = e.fst) :
    ∃ k, (⇑T.rotation.next)^[k] d = e ∧ ∀ j, j < k → (⇑T.rotation.next)^[j] d ≠ e := by
  classical
  have hex : ∃ k, (⇑T.rotation.next)^[k] d = e := T.rotation.cyclic d e he
  refine ⟨Nat.find hex, Nat.find_spec hex, fun j hj h => Nat.find_min hex hj h⟩

/-- **The pinched face walk.** `ρ` is a face walk of `G` (period `r`) that visits `ρ 0` again exactly at
position `m`. -/
structure PinchWalk (G : SphericalMap n) (r m : ℕ) (ρ : ℕ → Fin n) : Prop where
  three : 3 ≤ m
  threeB : m + 3 ≤ r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, G.Adj (ρ t) (ρ (t + 1))
  step : ∀ t, G.rotation.faceNext ⟨(ρ t, ρ (t + 1)), adj t⟩ = ⟨(ρ (t + 1), ρ (t + 2)), adj (t + 1)⟩
  pin : ρ m = ρ 0
  inj : ∀ s t, s < r → t < r → ρ s = ρ t → s = t ∨ (s = 0 ∧ t = m) ∨ (s = m ∧ t = 0)

variable {G : SphericalMap n} {m : ℕ}

/-- The walk dart at position `t`. -/
def PinchWalk.D (P : PinchWalk G r m ρ) (t : ℕ) : G.Dart := ⟨(ρ t, ρ (t + 1)), P.adj t⟩

theorem PinchWalk.face_D (P : PinchWalk G r m ρ) (t : ℕ) : G.faceOf (P.D t) = G.faceOf (P.D 0) := by
  induction t with
  | zero => rfl
  | succ t ih =>
    have := faceNext_face (T := G) (P.D t)
    rw [show G.rotation.faceNext (P.D t) = P.D (t + 1) from P.step t] at this
    rw [this, ih]

/-- `next` at the far end of a walk dart is the next walk dart. -/
theorem PinchWalk.next_D (P : PinchWalk G r m ρ) (t : ℕ) :
    G.rotation.next (P.D t).symm = P.D (t + 1) := by
  rw [← face_next_apply]; exact P.step t

/-- The A-arc, closed up at `u = ρ 0 = ρ m`. -/
def arcA (m : ℕ) (ρ : ℕ → Fin n) : ℕ → Fin n := fun t => ρ (t % m)

theorem PinchWalk.cycA (P : PinchWalk G r m ρ) : Cyc G m (arcA m ρ) := by
  have hm := P.three
  refine ⟨hm, fun t => by simp [arcA], fun t => ?_, fun s t hs ht h => ?_⟩
  · simp only [arcA]
    rcases Nat.lt_or_ge (t % m + 1) m with h | h
    · rw [show (t + 1) % m = t % m + 1 by rw [Nat.add_mod, Nat.mod_eq_of_lt (show 1 < m by omega)]; exact Nat.mod_eq_of_lt h]
      exact P.adj _
    · have h1 : t % m = m - 1 := by have := Nat.mod_lt t (show 0 < m by omega); omega
      have h2 : (t + 1) % m = 0 := by
        rw [Nat.add_mod, h1, Nat.mod_eq_of_lt (show 1 < m by omega), show m - 1 + 1 = m by omega, Nat.mod_self]
      rw [h1, h2, ← P.pin]
      have := P.adj (m - 1); rwa [show m - 1 + 1 = m by omega] at this
  · simp only [arcA, Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at h
    have := P.threeB
    rcases P.inj s t (by omega) (by omega) h with h | ⟨-, h⟩ | ⟨h, -⟩
    · exact h
    · omega
    · omega

theorem arcA_lt {t : ℕ} (ht : t < m) : arcA m ρ t = ρ t := by simp [arcA, Nat.mod_eq_of_lt ht]

end SimpleGraph.SphericalMap
