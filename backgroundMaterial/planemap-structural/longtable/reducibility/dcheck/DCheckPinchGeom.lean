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


theorem arcA_succ_of_lt (P : PinchWalk G r m ρ) {s : ℕ} (hs : s < m) : arcA m ρ (s + 1) = ρ (s + 1) := by
  rcases Nat.lt_or_ge (s + 1) m with h | h
  · exact arcA_lt h
  · have : s + 1 = m := by omega
    rw [this, P.pin]; simp [arcA]

theorem arcA_pred (P : PinchWalk G r m ρ) {s : ℕ} (hs0 : 0 < s) (hs : s < m) :
    arcA m ρ (s + m - 1) = ρ (s - 1) := by
  have hm := P.three
  simp only [arcA]
  rw [show s + m - 1 = (s - 1) + m by omega, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega)]

/-- The walk dart at an arc position is a cycle edge of the arc: indicator `1`. -/
theorem PinchWalk.cycInd_D (P : PinchWalk G r m ρ) {s : ℕ} (hs : s < m) :
    cycInd G m (arcA m ρ) (edgeOfDart (P.D s)) = 1 := by
  have h := cycInd_cycle' P.cycA s
  have e : edgeOfDart (P.D s) = edgeOfDart ⟨(arcA m ρ s, arcA m ρ (s + 1)), P.cycA.adj s⟩ := by
    apply Subtype.ext
    change s(ρ s, ρ (s + 1)) = s(arcA m ρ s, arcA m ρ (s + 1))
    rw [arcA_lt hs, arcA_succ_of_lt P hs]
  rw [e, h]

/-- **K1.** At an arc vertex `ρ s` (`0 < s < m`), every dart other than the walk dart sees the far potential. -/
theorem PinchWalk.k1 (P : PinchWalk G r m ρ) {c : G.Face → ZMod 2} (hc : CycPotential G m (arcA m ρ) c)
    {s : ℕ} (hs0 : 0 < s) (hsm : s < m) (d : G.Dart) (hd : d.fst = ρ s) (hne : d ≠ P.D s) :
    c (G.faceOf d) = c (G.faceOf (P.D 0)) + 1 := by
  classical
  set b := P.D s with hb
  set a := (P.D (s - 1)).symm with ha
  have hab : G.rotation.next a = b := by
    have := P.next_D (s - 1); rw [show s - 1 + 1 = s by omega] at this; exact this
  have hafst : a.fst = ρ s := by
    change ρ (s - 1 + 1) = ρ s; rw [show s - 1 + 1 = s by omega]
  have hasnd : a.snd = ρ (s - 1) := rfl
  obtain ⟨k, hk, hmin⟩ := first_arrival b d (by rw [hd]; rfl)
  have hk1 : 1 ≤ k := by
    rcases Nat.eq_zero_or_pos k with h | h
    · subst h; exact absurd hk.symm hne
    · exact h
  -- no intermediate dart is `a` or `b`
  have hmid : ∀ j, 1 ≤ j → j < k →
      cycInd G m (arcA m ρ) (edgeOfDart ((⇑G.rotation.next)^[j] b)) = 0 := by
    intro j hj1 hjk
    set x := (⇑G.rotation.next)^[j] b with hx
    have hxb : x ≠ b := by
      intro e
      apply hmin (k - j) (by omega)
      have h' : (⇑G.rotation.next)^[k] b = (⇑G.rotation.next)^[k - j] ((⇑G.rotation.next)^[j] b) := by
        rw [← Function.iterate_add_apply, Nat.sub_add_cancel (by omega)]
      rw [← hx, e] at h'
      exact h'.symm.trans hk
    have hxa : x ≠ a := by
      intro e
      apply hmin (k - (j + 1)) (by omega)
      have h' : (⇑G.rotation.next)^[k] b =
          (⇑G.rotation.next)^[k - (j + 1)] ((⇑G.rotation.next)^[j + 1] b) := by
        rw [← Function.iterate_add_apply, Nat.sub_add_cancel (by omega)]
      rw [Function.iterate_succ_apply', ← hx, e, hab] at h'
      exact h'.symm.trans hk
    have hxfst : x.fst = arcA m ρ s := by
      rw [arcA_lt hsm, hx, iterate_next_fst]; rfl
    apply cycInd_dart_off P.cycA x hxfst
    · rw [arcA_succ_of_lt P hsm]
      intro e; apply hxb; apply Dart.ext; apply Prod.ext
      · rw [hxfst, arcA_lt hsm]; rfl
      · exact e
    · rw [arcA_pred P hs0 hsm]
      intro e; apply hxa; apply Dart.ext; apply Prod.ext
      · rw [hxfst, arcA_lt hsm, hafst]
      · rw [e, hasnd]
  have h1 : c (G.faceOf (G.rotation.next b)) = c (G.faceOf (P.D 0)) + 1 := by
    rw [next_jump hc, P.cycInd_D hsm, hb, P.face_D]
  have := iterate_const hc (G.rotation.next b) (k - 1) (fun j hj => by
    rw [← Function.iterate_succ_apply]; exact hmid (j + 1) (by omega) (by omega))
  rw [← Function.iterate_succ_apply, show (k - 1).succ = k by omega, hk, h1] at this
  exact this


section sides
variable (P : PinchWalk G r m ρ) {c : G.Face → ZMod 2} (hc : CycPotential G m (arcA m ρ) c)

/-- Side A: the arc cycle and its far side. -/
def PinchWalk.SA (c : G.Face → ZMod 2) : Fin n → Prop :=
  fun x => OnCyc m (arcA m ρ) x ∨ OnSide G c (c (G.faceOf (P.D 0)) + 1) x

/-- Side B: everything else, and `u`. -/
def PinchWalk.SB (c : G.Face → ZMod 2) : Fin n → Prop := fun x => ¬ P.SA c x ∨ x = ρ 0

omit P in
theorem onCyc_arcA_iff {x : Fin n} : OnCyc m (arcA m ρ) x ↔ ∃ t, t < m ∧ ρ t = x := by
  constructor
  · rintro ⟨t, ht, e⟩; exact ⟨t, ht, by rw [← e, arcA_lt ht]⟩
  · rintro ⟨t, ht, e⟩; exact ⟨t, ht, by rw [arcA_lt ht, e]⟩

theorem PinchWalk.sa_ring {t : ℕ} (ht : t < m) : P.SA c (ρ t) := Or.inl (onCyc_arcA_iff.2 ⟨t, ht, rfl⟩)

theorem onSide_excl {b : ZMod 2} {x : Fin n} (h : OnSide G c b x) (d : G.Dart) (hd : d.fst = x)
    (hne : c (G.faceOf d) ≠ b) : False := hne (h d hd)

include P hc in
/-- Across an edge leaving the cycle, the two faces have equal potential. -/
theorem faces_eq_off {x y : Fin n} (hy : ¬ OnCyc m (arcA m ρ) y) (e : G.Adj x y) :
    c (G.faceOf (⟨(x, y), e⟩ : G.Dart).symm) = c (G.faceOf ⟨(x, y), e⟩) := by
  have h0 := cycInd_off' P.cycA (⟨(x, y), e⟩ : G.Dart).symm hy
  have h1 := hc (⟨(x, y), e⟩ : G.Dart).symm
  rw [h0, Dart.symm_symm] at h1
  exact (show ∀ a b : ZMod 2, 0 = a + b → a = b by decide) _ _ h1

include hc in
/-- **K2.** Neighbours of an arc vertex `ρ s` (`0 < s < m`) lie on side A. -/
theorem PinchWalk.k2 {s : ℕ} (hs0 : 0 < s) (hsm : s < m) {y : Fin n} (e : G.Adj (ρ s) y) : P.SA c y := by
  by_cases hy : OnCyc m (arcA m ρ) y
  · exact Or.inl hy
  · right
    let d : G.Dart := ⟨(ρ s, y), e⟩
    have hne : d ≠ P.D s := by
      intro h; apply hy
      have : y = ρ (s + 1) := congrArg (fun z : G.Dart => z.snd) h
      rw [this, ← arcA_succ_of_lt P hsm]; exact P.cycA.onCyc _
    have hk := P.k1 hc hs0 hsm d rfl hne
    have := onSide_of_dartC' P.cycA hc hy d.symm rfl
    rwa [faces_eq_off P hc hy e, hk] at this

include hc in
/-- Off the cycle, side A propagates along edges. -/
theorem PinchWalk.sa_off_edge {x y : Fin n} (hx : ¬ OnCyc m (arcA m ρ) x) (hxs : P.SA c x) (e : G.Adj x y) :
    P.SA c y := by
  rcases hxs with h | h
  · exact absurd h hx
  · by_cases hy : OnCyc m (arcA m ρ) y
    · exact Or.inl hy
    · right
      have := onSide_of_dartC' P.cycA hc hy (⟨(x, y), e⟩ : G.Dart).symm rfl
      rwa [faces_eq_off P hc hy e, h ⟨(x, y), e⟩ rfl] at this

include hc in
theorem PinchWalk.sa_edge {x y : Fin n} (hxs : P.SA c x) (hxu : x ≠ ρ 0) (e : G.Adj x y) : P.SA c y := by
  by_cases hx : OnCyc m (arcA m ρ) x
  · obtain ⟨t, ht, rfl⟩ := onCyc_arcA_iff.1 hx
    rcases Nat.eq_zero_or_pos t with h0 | h0
    · subst h0; exact absurd rfl hxu
    · exact P.k2 hc h0 ht e
  · exact P.sa_off_edge hc hx hxs e

include hc in
/-- **K3.** The B-arc vertices are on the near side, so not on side A. -/
theorem PinchWalk.not_sa_B {t : ℕ} (hmt : m < t) (htr : t < r) : ¬ P.SA c (ρ t) := by
  rintro (h | h)
  · obtain ⟨s, hs, e⟩ := onCyc_arcA_iff.1 h
    rcases P.inj s t (by have := P.threeB; omega) htr e with h | ⟨-, h⟩ | ⟨-, h⟩ <;> omega
  · apply onSide_excl h (P.D t) rfl
    rw [P.face_D]
    generalize c (G.faceOf (P.D 0)) = a; revert a; decide

include hc in
theorem PinchWalk.hcut (x y : Fin n) (e : G.Adj x y) :
    (P.SA c x ∧ P.SA c y) ∨ (P.SB c x ∧ P.SB c y) := by
  by_cases hxu : x = ρ 0
  · by_cases hy : P.SA c y
    · exact Or.inl ⟨hxu ▸ P.sa_ring (by have := P.three; omega), hy⟩
    · exact Or.inr ⟨Or.inr hxu, Or.inl hy⟩
  · by_cases hx : P.SA c x
    · exact Or.inl ⟨hx, P.sa_edge hc hx hxu e⟩
    · by_cases hyu : y = ρ 0
      · exact Or.inr ⟨Or.inl hx, Or.inr hyu⟩
      · exact Or.inr ⟨Or.inl hx, Or.inl (fun hy => hx (P.sa_edge hc hy hyu e.symm))⟩


end sides

/-- The end of a run is the first `H`-dart along the rotation. -/
theorem runTo_eq_first {M : SphericalMap n} {H : SimpleGraph (Fin n)} {d e e' : M.Dart}
    (h : RunTo M H d e) (heH : H.Adj e.fst e.snd) {K : ℕ} (hK : 0 < K) (hKe : (⇑M.rotation.next)^[K] d = e')
    (hmid : ∀ j, 0 < j → j < K → ¬ H.Adj ((⇑M.rotation.next)^[j] d).fst ((⇑M.rotation.next)^[j] d).snd)
    (he' : H.Adj e'.fst e'.snd) : e = e' := by
  obtain ⟨k, hk, hke, hj⟩ := h
  rcases Nat.lt_trichotomy k K with h1 | h1 | h1
  · exact absurd (hke ▸ heH) (hmid k hk h1)
  · subst h1; exact hke.symm.trans hKe
  · exact absurd (hKe ▸ he') (hj K hK h1)

/-- The dart into `ρ (m-1)` at `u`. -/
def PinchWalk.bU (P : PinchWalk G r m ρ) : G.Dart := (P.D (m - 1)).symm

theorem PinchWalk.bU_fst (P : PinchWalk G r m ρ) : P.bU.fst = ρ 0 := by
  have := P.three
  change ρ (m - 1 + 1) = ρ 0; rw [show m - 1 + 1 = m by omega, P.pin]

theorem PinchWalk.bU_snd (P : PinchWalk G r m ρ) : P.bU.snd = ρ (m - 1) := rfl

theorem PinchWalk.next_bU (P : PinchWalk G r m ρ) : G.rotation.next P.bU = P.D m := by
  have := P.next_D (m - 1); rw [show m - 1 + 1 = m by have := P.three; omega] at this; exact this

theorem PinchWalk.ne_zero_ring (P : PinchWalk G r m ρ) {t : ℕ} (ht0 : 0 < t) (htr : t < r) (htm : t ≠ m) :
    ρ t ≠ ρ 0 := by
  intro e
  rcases P.inj t 0 htr (by omega) e with h | ⟨h, -⟩ | ⟨h, -⟩ <;> omega

/-- Darts at `u` other than the two arc darts carry indicator `0`. -/
theorem PinchWalk.cycInd_u_off (P : PinchWalk G r m ρ) (x : G.Dart) (hx : x.fst = ρ 0)
    (ha : x ≠ P.D 0) (hb : x ≠ P.bU) : cycInd G m (arcA m ρ) (edgeOfDart x) = 0 := by
  have hm := P.three
  apply cycInd_dart_off P.cycA x (s := 0) (by rw [hx, arcA_lt (by omega)])
  · rw [arcA_lt (show 0 + 1 < m by omega)]
    intro e; apply ha; apply Dart.ext; apply Prod.ext
    · exact hx
    · exact e
  · rw [show 0 + m - 1 = m - 1 by omega, arcA_lt (show m - 1 < m by omega)]
    intro e; apply hb; apply Dart.ext; apply Prod.ext
    · rw [hx, P.bU_fst]
    · rw [e, P.bU_snd]

/-- Iterates avoiding a target: the general minimality step. -/
theorem iter_ne_start {M : SphericalMap n} {d e : M.Dart} {k : ℕ}
    (hk : (⇑M.rotation.next)^[k] d = e) (hmin : ∀ j, j < k → (⇑M.rotation.next)^[j] d ≠ e)
    {i : ℕ} (hi1 : 1 ≤ i) (hik : i < k) : (⇑M.rotation.next)^[i] d ≠ d := by
  intro h
  apply hmin (k - i) (by omega)
  have h' : (⇑M.rotation.next)^[k] d = (⇑M.rotation.next)^[k - i] ((⇑M.rotation.next)^[i] d) := by
    rw [← Function.iterate_add_apply, Nat.sub_add_cancel (by omega)]
  rw [h] at h'; exact h'.symm.trans hk

section k4
variable (P : PinchWalk G r m ρ) {c : G.Face → ZMod 2} (hc : CycPotential G m (arcA m ρ) c)
include hc

/-- From `bU`, the rotation sees the near potential up to its first arrival at `D 0`. -/
theorem PinchWalk.walk_from_bU {ka : ℕ} (hka : (⇑G.rotation.next)^[ka] P.bU = P.D 0)
    (hmin : ∀ j, j < ka → (⇑G.rotation.next)^[j] P.bU ≠ P.D 0) :
    ∀ j, 1 ≤ j → j ≤ ka → c (G.faceOf ((⇑G.rotation.next)^[j] P.bU)) = c (G.faceOf (P.D 0)) := by
  intro j hj1 hjk
  have h1 : c (G.faceOf (G.rotation.next P.bU)) = c (G.faceOf (P.D 0)) := by rw [P.next_bU, P.face_D]
  have := iterate_const hc (G.rotation.next P.bU) (j - 1) (fun i hi => by
    rw [← Function.iterate_succ_apply]
    apply P.cycInd_u_off
    · rw [iterate_next_fst, P.bU_fst]
    · exact hmin (i + 1) (by omega)
    · exact iter_ne_start hka hmin (by omega) (by omega))
  rw [← Function.iterate_succ_apply, show (j - 1).succ = j by omega, h1] at this
  exact this

/-- From `D 0`, the rotation sees the far potential up to its first arrival at `bU`. -/
theorem PinchWalk.walk_from_a {kb : ℕ} (hkb : (⇑G.rotation.next)^[kb] (P.D 0) = P.bU)
    (hmin : ∀ j, j < kb → (⇑G.rotation.next)^[j] (P.D 0) ≠ P.bU) :
    ∀ j, 1 ≤ j → j ≤ kb → c (G.faceOf ((⇑G.rotation.next)^[j] (P.D 0))) = c (G.faceOf (P.D 0)) + 1 := by
  intro j hj1 hjk
  have hm := P.three
  have h1 : c (G.faceOf (G.rotation.next (P.D 0))) = c (G.faceOf (P.D 0)) + 1 := by
    rw [next_jump hc, P.cycInd_D (by omega)]
  have := iterate_const hc (G.rotation.next (P.D 0)) (j - 1) (fun i hi => by
    rw [← Function.iterate_succ_apply]
    apply P.cycInd_u_off
    · rw [iterate_next_fst]; rfl
    · exact iter_ne_start hkb hmin (by omega) (by omega)
    · exact hmin (i + 1) (by omega))
  rw [← Function.iterate_succ_apply, show (j - 1).succ = j by omega, h1] at this
  exact this


/-- A dart at `u` whose reverse sees the near potential, other than `bU`, does not reach side A. -/
theorem PinchWalk.notSA_of_near (x : G.Dart) (hx : x.fst = ρ 0) (hxb : x ≠ P.bU)
    (h1 : c (G.faceOf x.symm) = c (G.faceOf (P.D 0))) : ¬ P.SA c x.snd := by
  have hm := P.three; have hr := P.threeB
  rintro (hcyc | hside)
  · obtain ⟨t, ht, e⟩ := onCyc_arcA_iff.1 hcyc
    rcases Nat.eq_zero_or_pos t with h0 | h0
    · subst h0; exact x.adj.ne (hx.trans e)
    · by_cases hxs : x.symm = P.D t
      · apply hxb
        have hf : x.fst = ρ (t + 1) := congrArg (fun z : G.Dart => z.snd) hxs
        have htm : t + 1 = m := by
          by_contra hne; exact P.ne_zero_ring (by omega) (by omega) hne (hf.symm.trans hx)
        apply Dart.ext; apply Prod.ext
        · rw [hx, P.bU_fst]
        · rw [P.bU_snd, ← e, show t = m - 1 by omega]
      · have := P.k1 hc h0 ht x.symm (show x.symm.fst = ρ t from e.symm) hxs
        rw [this] at h1
        generalize c (G.faceOf (P.D 0)) = a at h1; revert a h1; decide
  · apply onSide_excl hside x.symm rfl
    rw [h1]; generalize c (G.faceOf (P.D 0)) = a; revert a; decide

/-- A dart whose reverse sees the far potential reaches side A. -/
theorem PinchWalk.sa_of_far (x : G.Dart) (h1 : c (G.faceOf x.symm) = c (G.faceOf (P.D 0)) + 1) :
    P.SA c x.snd := by
  by_cases hy : OnCyc m (arcA m ρ) x.snd
  · exact Or.inl hy
  · right; have := onSide_of_dartC' P.cycA hc hy x.symm rfl; rwa [h1] at this

end k4

/-- The side graphs. -/
def sideG (G : SphericalMap n) (S : Fin n → Prop) : SimpleGraph (Fin n) where
  Adj x y := G.Adj x y ∧ S x ∧ S y
  symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.2, h.2.1⟩⟩
  loopless := ⟨fun _ h => h.1.ne rfl⟩

theorem sideG_le (G : SphericalMap n) (S : Fin n → Prop) : sideG G S ≤ G.graph := fun _ _ h => h.1

theorem arcA_mod (t : ℕ) : arcA m ρ t = ρ (t % m) := rfl

section ringA
variable (P : PinchWalk G r m ρ) {c : G.Face → ZMod 2} (hc : CycPotential G m (arcA m ρ) c)
  {N : SphericalMap n} (hN : N.graph = sideG G (P.SA c)) (hle : N.graph ≤ G.graph)
  (spec : ∀ d : N.Dart, RunTo G (sideG G (P.SA c)) (liftDart hle d) (liftDart hle (N.rotation.next d)))
include hc hN spec

/-- **Side A's map has the A-arc as a ring face.** -/
theorem PinchWalk.ringFaceA : RingFace N m (arcA m ρ) := by
  classical
  have hm := P.three; have hr := P.threeB
  have hNadj : ∀ t, N.Adj (arcA m ρ t) (arcA m ρ (t + 1)) := fun t => by
    show N.graph.Adj _ _
    rw [hN]
    exact ⟨P.cycA.adj t, Or.inl (P.cycA.onCyc t), Or.inl (P.cycA.onCyc (t + 1))⟩
  let DN : ℕ → N.Dart := fun t => ⟨(arcA m ρ t, arcA m ρ (t + 1)), hNadj t⟩
  have hHA : ∀ x y, (sideG G (P.SA c)).Adj x y ↔ G.Adj x y ∧ P.SA c x ∧ P.SA c y := fun _ _ => Iff.rfl
  have Dsa : ∀ t, t ≤ m → P.SA c (ρ t) := fun t ht => by
    rcases Nat.lt_or_ge t m with h | h
    · exact P.sa_ring h
    · rw [show t = m by omega, P.pin]; exact P.sa_ring (by omega)
  refine ⟨by omega, fun t => by simp [arcA], hNadj, fun t => ?_, fun s t hs ht e => P.cycA.inj s t hs ht e⟩
  change N.rotation.faceNext (DN t) = DN (t + 1)
  rw [face_next_apply]
  apply liftDart_injective hle
  set y := (DN t).symm
  have hrun := spec y
  have heH : (sideG G (P.SA c)).Adj (liftDart hle (N.rotation.next y)).fst
      (liftDart hle (N.rotation.next y)).snd := by
    exact (show N.graph ≤ sideG G (P.SA c) from hN.le) (N.rotation.next y).adj
  set s := (t + 1) % m with hs
  have hsm : s < m := Nat.mod_lt _ (by omega)
  have ht1 : arcA m ρ (t + 1) = ρ s := rfl
  by_cases hs0 : s = 0
  · -- the pinch vertex: the run from `bU` ends at `D 0`
    have htm : t % m = m - 1 := by
      have h1 := Nat.mod_lt t (show 0 < m by omega)
      rcases Nat.lt_or_ge (t % m + 1) m with h | h
      · exfalso
        have : s = t % m + 1 := by rw [hs, Nat.add_mod, Nat.mod_eq_of_lt (show 1 < m by omega), Nat.mod_eq_of_lt h]
        omega
      · omega
    have hy : liftDart hle y = P.bU := by
      apply Dart.ext; apply Prod.ext
      · change arcA m ρ (t + 1) = _; rw [ht1, hs0, P.bU_fst]
      · change arcA m ρ t = _; rw [arcA_mod, htm, P.bU_snd]
    have ht2 : (t + 2) % m = 1 := by
      rw [show t + 2 = (t + 1) + 1 by omega, Nat.add_mod (t + 1), ← hs, hs0, zero_add,
        Nat.mod_eq_of_lt (show 1 < m by omega), Nat.mod_eq_of_lt (show 1 < m by omega)]
    have hD : liftDart hle (DN (t + 1)) = P.D 0 := by
      apply Dart.ext; apply Prod.ext
      · change arcA m ρ (t + 1) = ρ 0; rw [ht1, hs0]
      · change arcA m ρ (t + 1 + 1) = ρ (0 + 1); rw [arcA_mod, show t + 1 + 1 = t + 2 by omega, ht2]
    rw [hD]
    rw [hy] at hrun
    obtain ⟨ka, hka, hmin⟩ := first_arrival P.bU (P.D 0) (by rw [P.bU_fst]; rfl)
    have hka0 : 0 < ka := by
      rcases Nat.eq_zero_or_pos ka with h | h
      · exfalso; subst h
        have : ρ (m - 1) = ρ 1 := (congrArg (fun z : G.Dart => z.snd) hka : _)
        rcases P.inj (m - 1) 1 (by omega) (by omega) this with h | ⟨h, -⟩ | ⟨h, -⟩ <;> omega
      · exact h
    refine runTo_eq_first hrun heH hka0 hka (fun j hj0 hjk => ?_) ?_
    · rintro ⟨-, -, hsnd⟩
      set x := (⇑G.rotation.next)^[j] P.bU
      have hxf : x.fst = ρ 0 := by rw [iterate_next_fst, P.bU_fst]
      have hxb : x ≠ P.bU := iter_ne_start hka hmin hj0 hjk
      have hnear : c (G.faceOf x.symm) = c (G.faceOf (P.D 0)) := by
        rw [← faceOf_next, show G.rotation.next x = (⇑G.rotation.next)^[j + 1] P.bU from
          (Function.iterate_succ_apply' _ _ _).symm]
        exact P.walk_from_bU hc hka hmin (j + 1) (by omega) (by omega)
      exact P.notSA_of_near hc x hxf hxb hnear hsnd
    · exact ⟨P.adj 0, P.sa_ring (by omega), P.sa_ring (by omega)⟩
  · -- an arc vertex: nothing is skipped
    have htm : t % m + 1 = s := by
      have h1 := Nat.mod_lt t (show 0 < m by omega)
      rcases Nat.lt_or_ge (t % m + 1) m with h | h
      · rw [hs, Nat.add_mod, Nat.mod_eq_of_lt (show 1 < m by omega), Nat.mod_eq_of_lt h]
      · exfalso; apply hs0
        rw [hs, Nat.add_mod, show t % m = m - 1 by omega, Nat.mod_eq_of_lt (show 1 < m by omega),
          show m - 1 + 1 = m by omega, Nat.mod_self]
    have hy : liftDart hle y = (P.D (s - 1)).symm := by
      apply Dart.ext; apply Prod.ext
      · change arcA m ρ (t + 1) = ρ (s - 1 + 1); rw [ht1, show s - 1 + 1 = s by omega]
      · change arcA m ρ t = ρ (s - 1); rw [arcA_mod, show s - 1 = t % m by omega]
    have hnx : G.rotation.next (liftDart hle y) = P.D s := by
      rw [hy]; have := P.next_D (s - 1); rwa [show s - 1 + 1 = s by omega] at this
    have hD : liftDart hle (DN (t + 1)) = P.D s := by
      apply Dart.ext; apply Prod.ext
      · change arcA m ρ (t + 1) = ρ s; exact ht1
      · change arcA m ρ (t + 1 + 1) = ρ (s + 1)
        rw [show t + 1 + 1 = (t + 1) + 1 by rfl, arcA_mod, Nat.add_mod (t + 1), ← hs,
          Nat.mod_eq_of_lt (show 1 < m by omega)]
        rcases Nat.lt_or_ge (s + 1) m with h | h
        · rw [Nat.mod_eq_of_lt h]
        · rw [show s + 1 = m by omega, Nat.mod_self, P.pin]
    rw [hD, runTo_first hrun (by rw [hnx]; exact ⟨P.adj s, Dsa s (by omega), Dsa (s + 1) (by omega)⟩), hnx]

end ringA

/-- The B-arc walk. -/
def arcB (r m : ℕ) (ρ : ℕ → Fin n) : ℕ → Fin n := fun t => ρ (m + t % (r - m))

theorem PinchWalk.ring_r (P : PinchWalk G r m ρ) : ρ r = ρ 0 := by
  have := P.per 0; rwa [zero_add] at this

section ringB
variable (P : PinchWalk G r m ρ) {c : G.Face → ZMod 2} (hc : CycPotential G m (arcA m ρ) c)
  {N : SphericalMap n} (hN : N.graph = sideG G (P.SB c)) (hle : N.graph ≤ G.graph)
  (spec : ∀ d : N.Dart, RunTo G (sideG G (P.SB c)) (liftDart hle d) (liftDart hle (N.rotation.next d)))
include hc

theorem PinchWalk.sb_ring {t : ℕ} (h1 : m ≤ t) (h2 : t ≤ r) : P.SB c (ρ t) := by
  rcases Nat.eq_or_lt_of_le h1 with h | h
  · subst h; exact Or.inr P.pin
  · rcases Nat.eq_or_lt_of_le h2 with h' | h'
    · subst h'; exact Or.inr P.ring_r
    · exact Or.inl (P.not_sa_B hc h h')

include hN spec

/-- **Side B's map has the B-arc as a ring face.** -/
theorem PinchWalk.ringFaceB : RingFace N (r - m) (arcB r m ρ) := by
  classical
  have hm := P.three; have hr := P.threeB
  have hrB3 : 3 ≤ (r - m) := by omega
  have hmod : ∀ t, t % (r - m) < (r - m) := fun t => Nat.mod_lt _ (by omega)
  have hGadj : ∀ t, G.Adj (arcB r m ρ t) (arcB r m ρ (t + 1)) := fun t => by
    simp only [arcB]
    rcases Nat.lt_or_ge (t % (r - m) + 1) (r - m) with h | h
    · rw [show (t + 1) % (r - m) = t % (r - m) + 1 by rw [Nat.add_mod, Nat.mod_eq_of_lt (show 1 < (r - m) by omega)]; exact Nat.mod_eq_of_lt h]
      exact P.adj _
    · have h1 : t % (r - m) = (r - m) - 1 := by have := hmod t; omega
      have h2 : (t + 1) % (r - m) = 0 := by
        rw [Nat.add_mod, h1, Nat.mod_eq_of_lt (show 1 < (r - m) by omega), show (r - m) - 1 + 1 = (r - m) by omega, Nat.mod_self]
      rw [h1, h2, Nat.add_zero, P.pin, ← P.ring_r]
      have := P.adj (m + ((r - m) - 1)); rwa [show m + ((r - m) - 1) + 1 = r by omega] at this
  have Bsb : ∀ t, P.SB c (arcB r m ρ t) := fun t => P.sb_ring hc (by omega) (by have := hmod t; omega)
  have hNadj : ∀ t, N.Adj (arcB r m ρ t) (arcB r m ρ (t + 1)) := fun t => by
    show N.graph.Adj _ _
    rw [hN]; exact ⟨hGadj t, Bsb t, Bsb (t + 1)⟩
  let DN : ℕ → N.Dart := fun t => ⟨(arcB r m ρ t, arcB r m ρ (t + 1)), hNadj t⟩
  refine ⟨by omega, fun t => by simp [arcB], hNadj, fun t => ?_, fun s t hs ht e => ?_⟩
  rotate_left
  · simp only [arcB, Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at e
    rcases P.inj (m + s) (m + t) (by omega) (by omega) e with h | ⟨h, -⟩ | ⟨-, h⟩ <;> omega
  change N.rotation.faceNext (DN t) = DN (t + 1)
  rw [face_next_apply]
  apply liftDart_injective hle
  set y := (DN t).symm
  have hrun := spec y
  have heH : (sideG G (P.SB c)).Adj (liftDart hle (N.rotation.next y)).fst
      (liftDart hle (N.rotation.next y)).snd :=
    (show N.graph ≤ sideG G (P.SB c) from hN.le) (N.rotation.next y).adj
  set s := (t + 1) % (r - m) with hs
  have hsB : s < (r - m) := hmod _
  have ht1 : arcB r m ρ (t + 1) = ρ (m + s) := rfl
  by_cases hs0 : s = 0
  · -- the pinch vertex: the run from the dart into ρ (r-1) ends at `D m`
    have htm : t % (r - m) = (r - m) - 1 := by
      have h1 := hmod t
      rcases Nat.lt_or_ge (t % (r - m) + 1) (r - m) with h | h
      · exfalso
        have : s = t % (r - m) + 1 := by rw [hs, Nat.add_mod, Nat.mod_eq_of_lt (show 1 < (r - m) by omega), Nat.mod_eq_of_lt h]
        omega
      · omega
    have hy : liftDart hle y = (P.D (r - 1)).symm := by
      apply Dart.ext; apply Prod.ext
      · change arcB r m ρ (t + 1) = ρ (r - 1 + 1); rw [ht1, hs0, Nat.add_zero, show r - 1 + 1 = r by omega, P.pin, P.ring_r]
      · change ρ (m + t % (r - m)) = ρ (r - 1); rw [htm, show m + ((r - m) - 1) = r - 1 by omega]
    have hnx : G.rotation.next (liftDart hle y) = P.D 0 := by
      rw [hy]; have := P.next_D (r - 1); rw [show r - 1 + 1 = r by omega] at this; rw [this]
      apply Dart.ext; apply Prod.ext
      · exact P.ring_r
      · change ρ (r + 1) = ρ (0 + 1); rw [show r + 1 = 1 + r by omega, P.per]
    have ht2 : (t + 2) % (r - m) = 1 := by
      rw [show t + 2 = (t + 1) + 1 by omega, Nat.add_mod (t + 1), ← hs, hs0, zero_add,
        Nat.mod_eq_of_lt (show 1 < (r - m) by omega), Nat.mod_eq_of_lt (show 1 < (r - m) by omega)]
    have hD : liftDart hle (DN (t + 1)) = P.D m := by
      apply Dart.ext; apply Prod.ext
      · change ρ (m + s) = ρ m; rw [hs0, Nat.add_zero]
      · change ρ (m + (t + 1 + 1) % (r - m)) = ρ (m + 1); rw [show t + 1 + 1 = t + 2 by omega, ht2]
    rw [hD]; rw [hy] at hrun
    obtain ⟨kb, hkb, hmin⟩ := first_arrival (P.D 0) P.bU (by rw [P.bU_fst]; rfl)
    have hiter : ∀ i, (⇑G.rotation.next)^[i + 1] (P.D (r - 1)).symm = (⇑G.rotation.next)^[i] (P.D 0) := by
      intro i; rw [Function.iterate_succ_apply, ← hy, hnx]
    refine runTo_eq_first hrun heH (K := kb + 2) (by omega) ?_ (fun j hj0 hjk => ?_) ?_
    · rw [show kb + 2 = (kb + 1) + 1 by omega, hiter, Function.iterate_succ_apply', hkb, P.next_bU]
    · rintro ⟨-, -, hsnd⟩
      obtain ⟨i, rfl⟩ : ∃ i, j = i + 1 := ⟨j - 1, by omega⟩
      rw [hiter] at hsnd
      set x := (⇑G.rotation.next)^[i] (P.D 0)
      have hxf : x.fst = ρ 0 := by rw [iterate_next_fst]; rfl
      have hsa : P.SA c x.snd ∧ x.snd ≠ ρ 0 := by
        refine ⟨?_, fun e => x.adj.ne (hxf.trans e.symm)⟩
        rcases Nat.eq_zero_or_pos i with h0 | h0
        · subst h0; exact P.sa_ring (show 0 + 1 < m by omega)
        · rcases Nat.eq_or_lt_of_le (show i ≤ kb by omega) with he | hlt
          · subst he; rw [show x = P.bU from hkb, P.bU_snd]; exact P.sa_ring (by omega)
          · apply P.sa_of_far hc x
            rw [← faceOf_next, show G.rotation.next x = (⇑G.rotation.next)^[i + 1] (P.D 0) from
              (Function.iterate_succ_apply' _ _ _).symm]
            exact P.walk_from_a hc hkb hmin (i + 1) (by omega) (by omega)
      rcases hsnd with h | h
      · exact h hsa.1
      · exact hsa.2 h
    · exact ⟨P.adj m, P.sb_ring hc le_rfl (by omega), P.sb_ring hc (by omega) (by omega)⟩
  · -- a B-arc vertex: nothing is skipped
    have htm : t % (r - m) + 1 = s := by
      have h1 := hmod t
      rcases Nat.lt_or_ge (t % (r - m) + 1) (r - m) with h | h
      · rw [hs, Nat.add_mod, Nat.mod_eq_of_lt (show 1 < (r - m) by omega), Nat.mod_eq_of_lt h]
      · exfalso; apply hs0
        rw [hs, Nat.add_mod, show t % (r - m) = (r - m) - 1 by omega, Nat.mod_eq_of_lt (show 1 < (r - m) by omega),
          show (r - m) - 1 + 1 = (r - m) by omega, Nat.mod_self]
    have hy : liftDart hle y = (P.D (m + s - 1)).symm := by
      apply Dart.ext; apply Prod.ext
      · change ρ (m + s) = ρ (m + s - 1 + 1); rw [show m + s - 1 + 1 = m + s by omega]
      · change ρ (m + t % (r - m)) = ρ (m + s - 1); rw [show m + s - 1 = m + t % (r - m) by omega]
    have hnx : G.rotation.next (liftDart hle y) = P.D (m + s) := by
      rw [hy]; have := P.next_D (m + s - 1); rwa [show m + s - 1 + 1 = m + s by omega] at this
    have hD : liftDart hle (DN (t + 1)) = P.D (m + s) := by
      apply Dart.ext; apply Prod.ext
      · exact ht1
      · change ρ (m + (t + 1 + 1) % (r - m)) = ρ (m + s + 1)
        rw [Nat.add_mod (t + 1), ← hs, Nat.mod_eq_of_lt (show 1 < (r - m) by omega)]
        rcases Nat.lt_or_ge (s + 1) (r - m) with h | h
        · rw [Nat.mod_eq_of_lt h, Nat.add_assoc]
        · rw [show s + 1 = (r - m) by omega, Nat.mod_self, Nat.add_zero, show m + s + 1 = r by omega, P.pin, P.ring_r]
    rw [hD, runTo_first hrun (by rw [hnx]; exact ⟨P.adj _, P.sb_ring hc (by omega) (by omega),
      P.sb_ring hc (by omega) (by omega)⟩), hnx]

end ringB

/-- **(ii′) assembled: a pinched face walk is θ-non-crossing.** -/
theorem PinchWalk.ringTNC (P : PinchWalk G r m ρ) (h : Fin n) (hoff : ∀ t, ρ t ≠ h) : RingTNC G r ρ h := by
  classical
  have hm := P.three; have hr := P.threeB
  obtain ⟨c, hc⟩ := exists_cycPotential' P.cycA
  obtain ⟨GA, hGA, hleA, specA⟩ := subgraph_tracked G (sideG G (P.SA c)) (sideG_le _ _)
  obtain ⟨GB, hGB, hleB, specB⟩ := subgraph_tracked G (sideG G (P.SB c)) (sideG_le _ _)
  have RA := (P.ringFaceA hc hGA hleA specA).toNC.toTNC (h := h) (fun t => hoff _)
  have RB := (P.ringFaceB hc hGB hleB specB).toNC.toTNC (h := h) (fun t => hoff _)
  have TA : TNC GA m ρ h := by
    intro c' hc' θ hθ i j k l hij hjk hkl hlm h1 h2
    have := RA.tnc hc' hθ hij hjk hkl hlm
      (by rwa [arcA_lt (show i < m by omega), arcA_lt (show k < m by omega)])
      (by rwa [arcA_lt (show j < m by omega), arcA_lt hlm])
    rwa [arcA_lt (show i < m by omega), arcA_lt (show j < m by omega)] at this
  have hB : ∀ t, t < r - m → arcB r m ρ t = ρ (m + t) := fun t ht => by simp [arcB, Nat.mod_eq_of_lt ht]
  have TB : TNC GB (r - m) (fun t => ρ (m + t)) h := by
    intro c' hc' θ hθ i j k l hij hjk hkl hlm h1 h2
    have := RB.tnc hc' hθ hij hjk hkl hlm
      (by rwa [hB i (by omega), hB k (by omega)]) (by rwa [hB j (by omega), hB l hlm])
    rwa [hB i (by omega), hB j (by omega)] at this
  refine ⟨by omega, P.per, P.adj, hoff, ?_⟩
  intro c' hc' θ hθ
  exact TNC.pinch (G := G) (GA := GA) (GB := GB) (SA := P.SA c) (SB := P.SB c) (u := ρ 0)
    (fun x hx hb => by rcases hb with hb | hb; exact absurd hx hb; exact hb)
    (P.hcut hc)
    (fun x y e hx hy => by show GA.graph.Adj x y; rw [hGA]; exact ⟨e, hx, hy⟩)
    (fun x y e hx hy => by show GB.graph.Adj x y; rw [hGB]; exact ⟨e, hx, hy⟩)
    (fun x y e => hleA e) (fun x y e => hleB e)
    (by omega) rfl P.pin (fun t ht => P.sa_ring ht) (fun t h1 h2 => P.sb_ring hc h1 (by omega)) TA TB hc' hθ

/-- **`KempeMatching` for a pinched ring** (the codes realised by colourings of `G` off the hole). -/
theorem PinchWalk.kempeMatching (P : PinchWalk G r m ρ) (h : Fin n) (hoff : ∀ t, ρ t ≠ h) (cf : Conf)
    (N : ℕ) (hN : N ≤ 10) (hr : cf.r = r) (hrN : r < 2 * N) :
    KempeMatchingT (matchTableN N) cf (fun k => ∃ c : Fin n → Fin 4, ProperOff G.graph h c ∧
      k = code (ringSeq ρ c) r) :=
  (P.ringTNC h hoff).kempeMatching cf N hN hr hrN

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.PinchWalk.ringTNC
#print axioms SimpleGraph.SphericalMap.PinchWalk.kempeMatching
