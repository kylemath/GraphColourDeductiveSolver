import DCheckRingNC

/-! Job 25 step 1 (Studio, exploratory): the two sides of an induced `r`-cycle in a spherical map,
generalising `SideTriangle` (F1) from triangles. The cycle is `ρ : ℕ → Fin n`, `r`-periodic,
injective below `r`, cyclically adjacent, and induced (no chords). Its edge indicator is even,
so it has a face potential `c`; the kept map of side `b` (delete every vertex off the cycle whose
darts see potential `≠ b`) has the cycle as a face (`RingFace`), in the orientation whose darts
see the far side. -/

namespace SimpleGraph.SphericalMap
open RotationSystem VacancyCliqueLift VacancyIcosahedral

variable {n : ℕ}

/-- An induced cycle of `T` of length `r ≥ 3`. -/
structure ICycle (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) : Prop where
  three : 3 ≤ r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, T.Adj (ρ t) (ρ (t + 1))
  inj : ∀ s t, s < r → t < r → ρ s = ρ t → s = t
  ind : ∀ s t, s < r → t < r → T.Adj (ρ s) (ρ t) → t = (s + 1) % r ∨ s = (t + 1) % r

/-- On the cycle. -/
def OnCyc (r : ℕ) (ρ : ℕ → Fin n) (x : Fin n) : Prop := ∃ t, t < r ∧ ρ t = x

/-- The cycle's edge indicator: the sum of the single-edge indicators of its `r` edges. -/
noncomputable def cycInd (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) : T.graph.edgeSet → ZMod 2 := by
  classical
  exact fun e => ∑ t ∈ Finset.range r, if e.val = s(ρ t, ρ (t + 1)) then 1 else 0

variable {T : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n}

theorem ICycle.per_mod (C : ICycle T r ρ) (t : ℕ) : ρ (t % r) = ρ t := by
  conv_rhs => rw [← Nat.mod_add_div t r]
  induction t / r with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, C.per, ih]

theorem ICycle.onCyc (C : ICycle T r ρ) (t : ℕ) : OnCyc r ρ (ρ t) :=
  ⟨t % r, Nat.mod_lt _ (by have := C.three; omega), C.per_mod t⟩

theorem cycInd_even (C : ICycle T r ρ) : IsEven T (cycInd T r ρ) := by
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

/-- A face potential of the cycle. -/
def CycPotential (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (c : T.Face → ZMod 2) : Prop :=
  ∀ d : T.Dart, cycInd T r ρ (edgeOfDart d) = c (T.faceOf d) + c (T.faceOf d.symm)

theorem exists_cycPotential (C : ICycle T r ρ) : ∃ c, CycPotential T r ρ c :=
  T.fills _ (cycInd_even C)

/-- Darts from a vertex off the cycle carry indicator `0`. -/
theorem cycInd_off (C : ICycle T r ρ) (d : T.Dart) (hx : ¬ OnCyc r ρ d.fst) : cycInd T r ρ (edgeOfDart d) = 0 := by
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

theorem side_constC (C : ICycle T r ρ) {c : T.Face → ZMod 2} (hc : CycPotential T r ρ c)
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
    have h0 := cycInd_off C y (by rw [hy]; exact hx)
    have := zmod2_swap _ _ _ (hc y)
    rw [h0, zero_add] at this
    rw [this, ih]

theorem onSide_of_dartC (C : ICycle T r ρ) {c : T.Face → ZMod 2} (hc : CycPotential T r ρ c)
    {x : Fin n} (hx : ¬ OnCyc r ρ x) (d : T.Dart) (hd : d.fst = x) :
    OnSide T c (c (T.faceOf d)) x :=
  fun e he => (side_constC C hc hx d e hd he).symm

/-- The kept vertex set of side `b`: the cycle, and the vertices off it seeing potential `b`. -/
def keepC (T : SphericalMap n) (c : T.Face → ZMod 2) (b : ZMod 2) (r : ℕ) (ρ : ℕ → Fin n) :
    Set (Fin n) := {x | OnCyc r ρ x ∨ OnSide T c b x}

variable {c : T.Face → ZMod 2} {b : ZMod 2}

theorem keep_of_faceC (C : ICycle T r ρ) (hc : CycPotential T r ρ c) (d : T.Dart)
    (hd : c (T.faceOf d) = b) : d.fst ∈ keepC T c b r ρ := by
  by_cases hx : OnCyc r ρ d.fst
  · exact Or.inl hx
  · have := onSide_of_dartC C hc hx d rfl
    rw [hd] at this
    exact Or.inr this

theorem snd_keep_of_faceC (C : ICycle T r ρ) (hc : CycPotential T r ρ c) (d : T.Dart)
    (hd : c (T.faceOf d) = b) : d.snd ∈ keepC T c b r ρ := by
  have := keep_of_faceC (b := b) C hc (T.rotation.faceNext d) (by rw [faceNext_face]; exact hd)
  rwa [RotationSystem.face_next_fst] at this

theorem ICycle.per_mul (C : ICycle T r ρ) (x : ℕ) : ∀ k, ρ (x + r * k) = ρ x := by
  intro k
  induction k with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, C.per, ih]

theorem ICycle.mod_eq_of (C : ICycle T r ρ) {s t : ℕ} (h : ρ s = ρ t) : s % r = t % r := by
  have hpos : 0 < r := by have := C.three; omega
  exact C.inj _ _ (Nat.mod_lt _ hpos) (Nat.mod_lt _ hpos) (by rw [C.per_mod, C.per_mod]; exact h)

/-- The indicator is `1` on a cycle edge. -/
theorem cycInd_cycle (C : ICycle T r ρ) (t : ℕ) :
    cycInd T r ρ (edgeOfDart ⟨(ρ t, ρ (t + 1)), C.adj t⟩) = 1 := by
  classical
  have hpos : 0 < r := by have := C.three; omega
  have h3 := C.three
  unfold cycInd
  rw [Finset.sum_eq_single (t % r)]
  · rw [if_pos]
    change s(ρ t, ρ (t + 1)) = s(ρ (t % r), ρ (t % r + 1))
    have : ρ (t % r + 1) = ρ (t + 1) := by
      have e : t + 1 = (t % r + 1) + r * (t / r) := by have := Nat.mod_add_div t r; omega
      rw [e, C.per_mul]
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
      -- t ≡ u + 1 and t + 1 ≡ u, so 2 ≡ 0
      have : (u + 2) % r = u % r := by
        rw [show u + 2 = (u + 1) + 1 by omega, Nat.add_mod (u + 1), ← m1, ← Nat.add_mod, ← m2]
      have h0 := Nat.sub_mod_eq_zero_of_mod_eq this
      rw [show u + 2 - u = 2 by omega, Nat.mod_eq_of_lt (by omega : 2 < r)] at h0
      omega
  · intro h; exact absurd (Finset.mem_range.2 (Nat.mod_lt _ hpos)) h

section Map
variable (C : ICycle T r ρ) (hc : CycPotential T r ρ c) {N : SphericalMap n}
  (hN : N.graph = sideGraph T.graph (keepC T c b r ρ)) (hle : N.graph ≤ T.graph)
  (spec : ∀ d : N.Dart, RunTo T (sideGraph T.graph (keepC T c b r ρ)) (liftDart hle d)
    (liftDart hle (N.rotation.next d)))
include C hc hN spec

/-- **Far run at a cycle vertex.** From a cycle dart `ρ t → ρ (t+1)` whose face is on the far side,
the kept map's successor at `ρ (t+1)` skips the far side and lands on `ρ (t+2)`, again with a
far face. -/
theorem lift_next_farFaceC (d : N.Dart) (t : ℕ) (hdu : (liftDart hle d).fst = ρ t)
    (hdv : (liftDart hle d).snd = ρ (t + 1)) (hd : c (T.faceOf (liftDart hle d)) ≠ b) :
    (liftDart hle (N.rotation.next d.symm)).snd = ρ (t + 2) ∧
      c (T.faceOf (liftDart hle (N.rotation.next d.symm))) ≠ b := by
  classical
  have hr3 := C.three
  set u := ρ t; set v := ρ (t + 1); set w := ρ (t + 2)
  set H := sideGraph T.graph (keepC T c b r ρ) with hH
  set y0 := liftDart hle d.symm with hy0
  have hy0fst : y0.fst = v := hdv
  have hy0snd : y0.snd = u := hdu
  obtain ⟨k, hk, hke, hj⟩ := spec d.symm
  set Y : ℕ → T.Dart := fun j => (⇑T.rotation.next)^[j] y0 with hY
  have Yfst : ∀ j, (Y j).fst = v := fun j => (iterate_next_fst T j y0).trans hy0fst
  have hvK : v ∈ keepC T c b r ρ := Or.inl (C.onCyc _)
  have C' : ∀ j, 1 ≤ j → j ≤ k → c (T.faceOf (Y j)) ≠ b := by
    intro j
    induction j with
    | zero => intro h; omega
    | succ j ih =>
      intro _ hjk
      rcases Nat.eq_zero_or_pos j with rfl | hj0
      · change c (T.faceOf (T.rotation.next y0)) ≠ b
        rw [faceOf_next]; exact hd
      · have hnot := hj j hj0 (by omega)
        have hsnd : (Y j).snd ∉ keepC T c b r ρ := fun hs =>
          hnot ⟨(Y j).adj, by rw [Yfst]; exact hvK, hs⟩
        have hoff : ¬ OnCyc r ρ (Y j).snd := fun h => hsnd (Or.inl h)
        have h0 : cycInd T r ρ (edgeOfDart (Y j)) = 0 := by
          rw [← edge_of_dart_symm]; exact cycInd_off C _ hoff
        have := zmod2_swap _ _ _ (hc (Y j))
        rw [h0, zero_add] at this
        rw [show Y (j + 1) = T.rotation.next (Y j) from Function.iterate_succ_apply' _ _ _,
          faceOf_next, this]
        exact ih (by omega) (by omega)
  have Ck := C' k hk le_rfl
  have hYk : Y k = liftDart hle (N.rotation.next d.symm) := hke
  refine ⟨?_, hYk ▸ Ck⟩
  have hadj : H.Adj (Y k).fst (Y k).snd := by
    rw [hYk]; exact hN.le (N.rotation.next d.symm).adj
  have hzK := hadj.2.2
  set z := (Y k).snd with hz
  have hzC : OnCyc r ρ z := by
    rcases hzK with h | h
    · exact h
    · exfalso
      have := h (T.rotation.faceNext (Y k)) (RotationSystem.face_next_fst _ _)
      rw [faceNext_face] at this
      exact Ck this
  obtain ⟨s, hs, hsz⟩ := hzC
  have hvz : T.Adj v z := by have := (Y k).adj; rwa [Yfst] at this
  -- indices modulo r
  have ht1 : (t + 1) % r < r := Nat.mod_lt _ (by omega)
  have hvm : v = ρ ((t + 1) % r) := (C.per_mod _).symm
  rw [hvm, ← hsz] at hvz
  rcases C.ind _ _ ht1 hs hvz with h1 | h1
  · -- z = ρ (t+2)
    rw [← hYk]
    change z = w
    have e : ((t + 1) % r + 1) % r = (t + 2) % r := by
      rw [show t + 2 = (t + 1) + 1 by omega, Nat.add_mod (t + 1) 1, Nat.mod_eq_of_lt (show 1 < r by omega)]
    rw [← hsz, h1, e, C.per_mod]
  · -- z = ρ t = u: excluded by the kept dart v → w
    exfalso
    have hzu : z = u := by
      rw [← hsz]
      have e1 : ρ ((s + 1) % r) = ρ (s + 1) := C.per_mod _
      have : ρ (t + 1) = ρ (s + 1) := by rw [← C.per_mod (t + 1), h1, e1]
      -- t ≡ s (mod r)
      have hts : t % r = s := by
        have a := C.inj ((t + 1) % r) ((s + 1) % r) ht1 (Nat.mod_lt _ (by omega))
          (by rw [C.per_mod, C.per_mod]; exact this)
        have : (t + 1) % r = (s + 1) % r := a
        rw [Nat.add_mod t, Nat.add_mod s, Nat.mod_eq_of_lt hs] at this
        by_cases hr1 : s + 1 < r
        · rw [Nat.mod_eq_of_lt (by omega : 1 < r)] at this
          rw [Nat.mod_eq_of_lt (show s + 1 < r by omega)] at this
          have htr := Nat.mod_lt t (show 0 < r by omega)
          by_cases ht' : t % r + 1 < r
          · rw [Nat.mod_eq_of_lt ht'] at this; omega
          · rw [show t % r + 1 = r by omega, Nat.mod_self] at this; omega
        · have hsr : s = r - 1 := by omega
          rw [Nat.mod_eq_of_lt (by omega : 1 < r), show s + 1 = r by omega, Nat.mod_self] at this
          have htr := Nat.mod_lt t (show 0 < r by omega)
          by_cases ht' : t % r + 1 < r
          · rw [Nat.mod_eq_of_lt ht'] at this; omega
          · omega
      rw [← hts, C.per_mod]
    have hback : Y k = y0 := by
      apply Dart.ext; apply Prod.ext
      · rw [Yfst, hy0fst]
      · rw [← hz, hzu, hy0snd]
    have hper : Function.IsPeriodicPt (⇑T.rotation.next) k y0 := hback
    have hvw : T.Adj v w := by
      have := C.adj (t + 1); simpa [v, w, show t + 1 + 1 = t + 2 by omega] using this
    let dw : T.Dart := ⟨(v, w), hvw⟩
    have hwu : w ≠ u := by
      intro e
      have e' : ρ ((t + 2) % r) = ρ (t % r) := by rw [C.per_mod, C.per_mod]; exact e
      have hm := C.inj _ _ (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) e'
      have h0 := Nat.sub_mod_eq_zero_of_mod_eq hm
      rw [show t + 2 - t = 2 by omega, Nat.mod_eq_of_lt (by omega : 2 < r)] at h0
      omega
    obtain ⟨m, hm⟩ := T.rotation.cyclic y0 dw hy0fst
    have hpos := hper.minimalPeriod_pos hk
    have hdvd := hper.minimalPeriod_dvd
    have hle' := Nat.le_of_dvd hk hdvd
    have hmod : (⇑T.rotation.next)^[m % Function.minimalPeriod (⇑T.rotation.next) y0] y0 = dw := by
      rw [Function.iterate_mod_minimalPeriod_eq]; exact hm
    have hm0 : m % Function.minimalPeriod (⇑T.rotation.next) y0 ≠ 0 := by
      intro h0
      rw [h0] at hmod
      have := congrArg (fun e : T.Dart => e.snd) hmod
      simp only [Function.iterate_zero, id] at this
      exact hwu (this.symm.trans hy0snd)
    apply hj _ (Nat.pos_of_ne_zero hm0) (lt_of_lt_of_le (Nat.mod_lt _ hpos) hle')
    rw [hmod]
    exact ⟨hvw, hvK, Or.inl (C.onCyc _)⟩

/-- Reversed far run: from `ρ (t+2) → ρ (t+1)` with a far face, the kept successor lands on `ρ t`. -/
theorem lift_next_farFaceC_rev (d : N.Dart) (t : ℕ) (hdu : (liftDart hle d).fst = ρ (t + 2))
    (hdv : (liftDart hle d).snd = ρ (t + 1)) (hd : c (T.faceOf (liftDart hle d)) ≠ b) :
    (liftDart hle (N.rotation.next d.symm)).snd = ρ t ∧
      c (T.faceOf (liftDart hle (N.rotation.next d.symm))) ≠ b := by
  classical
  have hr3 := C.three
  set u := ρ (t + 2); set v := ρ (t + 1); set w := ρ t
  set H := sideGraph T.graph (keepC T c b r ρ) with hH
  set y0 := liftDart hle d.symm with hy0
  have hy0fst : y0.fst = v := hdv
  have hy0snd : y0.snd = u := hdu
  obtain ⟨k, hk, hke, hj⟩ := spec d.symm
  set Y : ℕ → T.Dart := fun j => (⇑T.rotation.next)^[j] y0 with hY
  have Yfst : ∀ j, (Y j).fst = v := fun j => (iterate_next_fst T j y0).trans hy0fst
  have hvK : v ∈ keepC T c b r ρ := Or.inl (C.onCyc _)
  have C' : ∀ j, 1 ≤ j → j ≤ k → c (T.faceOf (Y j)) ≠ b := by
    intro j
    induction j with
    | zero => intro h; omega
    | succ j ih =>
      intro _ hjk
      rcases Nat.eq_zero_or_pos j with rfl | hj0
      · change c (T.faceOf (T.rotation.next y0)) ≠ b
        rw [faceOf_next]; exact hd
      · have hnot := hj j hj0 (by omega)
        have hsnd : (Y j).snd ∉ keepC T c b r ρ := fun hs =>
          hnot ⟨(Y j).adj, by rw [Yfst]; exact hvK, hs⟩
        have hoff : ¬ OnCyc r ρ (Y j).snd := fun h => hsnd (Or.inl h)
        have h0 : cycInd T r ρ (edgeOfDart (Y j)) = 0 := by
          rw [← edge_of_dart_symm]; exact cycInd_off C _ hoff
        have := zmod2_swap _ _ _ (hc (Y j))
        rw [h0, zero_add] at this
        rw [show Y (j + 1) = T.rotation.next (Y j) from Function.iterate_succ_apply' _ _ _,
          faceOf_next, this]
        exact ih (by omega) (by omega)
  have Ck := C' k hk le_rfl
  have hYk : Y k = liftDart hle (N.rotation.next d.symm) := hke
  refine ⟨?_, hYk ▸ Ck⟩
  have hadj : H.Adj (Y k).fst (Y k).snd := by
    rw [hYk]; exact hN.le (N.rotation.next d.symm).adj
  have hzK := hadj.2.2
  set z := (Y k).snd with hz
  have hzC : OnCyc r ρ z := by
    rcases hzK with h | h
    · exact h
    · exfalso
      have := h (T.rotation.faceNext (Y k)) (RotationSystem.face_next_fst _ _)
      rw [faceNext_face] at this
      exact Ck this
  obtain ⟨s, hs, hsz⟩ := hzC
  have hvz : T.Adj v z := by have := (Y k).adj; rwa [Yfst] at this
  -- indices modulo r
  have ht1 : (t + 1) % r < r := Nat.mod_lt _ (by omega)
  have hvm : v = ρ ((t + 1) % r) := (C.per_mod _).symm
  rw [hvm, ← hsz] at hvz
  rcases C.ind _ _ ht1 hs hvz with h1 | h1
  · -- z = ρ (t+2) = u: excluded by the kept dart v → w
    exfalso
    have hzu : z = u := by
      have e : ((t + 1) % r + 1) % r = (t + 2) % r := by
        rw [show t + 2 = (t + 1) + 1 by omega, Nat.add_mod (t + 1) 1, Nat.mod_eq_of_lt (show 1 < r by omega)]
      rw [← hsz, h1, e, C.per_mod]
    have hback : Y k = y0 := by
      apply Dart.ext; apply Prod.ext
      · rw [Yfst, hy0fst]
      · rw [← hz, hzu, hy0snd]
    have hper : Function.IsPeriodicPt (⇑T.rotation.next) k y0 := hback
    have hvw : T.Adj v w := (C.adj t).symm
    let dw : T.Dart := ⟨(v, w), hvw⟩
    have hwu : w ≠ u := by
      intro e
      have e' : ρ ((t + 2) % r) = ρ (t % r) := by rw [C.per_mod, C.per_mod]; exact e.symm
      have hm := C.inj _ _ (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) e'
      have h0 := Nat.sub_mod_eq_zero_of_mod_eq hm
      rw [show t + 2 - t = 2 by omega, Nat.mod_eq_of_lt (by omega : 2 < r)] at h0
      omega
    obtain ⟨m, hm⟩ := T.rotation.cyclic y0 dw hy0fst
    have hpos := hper.minimalPeriod_pos hk
    have hdvd := hper.minimalPeriod_dvd
    have hle' := Nat.le_of_dvd hk hdvd
    have hmod : (⇑T.rotation.next)^[m % Function.minimalPeriod (⇑T.rotation.next) y0] y0 = dw := by
      rw [Function.iterate_mod_minimalPeriod_eq]; exact hm
    have hm0 : m % Function.minimalPeriod (⇑T.rotation.next) y0 ≠ 0 := by
      intro h0
      rw [h0] at hmod
      have := congrArg (fun e : T.Dart => e.snd) hmod
      simp only [Function.iterate_zero, id] at this
      exact hwu (this.symm.trans hy0snd)
    apply hj _ (Nat.pos_of_ne_zero hm0) (lt_of_lt_of_le (Nat.mod_lt _ hpos) hle')
    rw [hmod]
    exact ⟨hvw, hvK, Or.inl (C.onCyc _)⟩
  · -- z = ρ t = w
    rw [← hYk]
    change z = w
    rw [← hsz]
    have e1 : ρ ((s + 1) % r) = ρ (s + 1) := C.per_mod _
    have : ρ (t + 1) = ρ (s + 1) := by rw [← C.per_mod (t + 1), h1, e1]
    -- t ≡ s (mod r)
    have hts : t % r = s := by
      have a := C.inj ((t + 1) % r) ((s + 1) % r) ht1 (Nat.mod_lt _ (by omega))
        (by rw [C.per_mod, C.per_mod]; exact this)
      have : (t + 1) % r = (s + 1) % r := a
      rw [Nat.add_mod t, Nat.add_mod s, Nat.mod_eq_of_lt hs] at this
      by_cases hr1 : s + 1 < r
      · rw [Nat.mod_eq_of_lt (by omega : 1 < r)] at this
        rw [Nat.mod_eq_of_lt (show s + 1 < r by omega)] at this
        have htr := Nat.mod_lt t (show 0 < r by omega)
        by_cases ht' : t % r + 1 < r
        · rw [Nat.mod_eq_of_lt ht'] at this; omega
        · rw [show t % r + 1 = r by omega, Nat.mod_self] at this; omega
      · have hsr : s = r - 1 := by omega
        rw [Nat.mod_eq_of_lt (by omega : 1 < r), show s + 1 = r by omega, Nat.mod_self] at this
        have htr := Nat.mod_lt t (show 0 < r by omega)
        by_cases ht' : t % r + 1 < r
        · rw [Nat.mod_eq_of_lt ht'] at this; omega
        · omega
    rw [← hts, C.per_mod]

/-- **The cycle is a face of the kept map**, in the orientation whose darts see the far side. -/
theorem kept_ringFace (hfar : ∀ h : T.Adj (ρ 0) (ρ 1), c (T.faceOf ⟨(ρ 0, ρ 1), h⟩) ≠ b) :
    RingFace N r ρ := by
  classical
  have hNadj : ∀ t, N.Adj (ρ t) (ρ (t + 1)) := fun t => by
    show N.graph.Adj _ _
    rw [hN]; exact ⟨C.adj t, Or.inl (C.onCyc _), Or.inl (C.onCyc _)⟩
  let D : ℕ → N.Dart := fun t => ⟨(ρ t, ρ (t + 1)), hNadj t⟩
  have far : ∀ t, c (T.faceOf (liftDart hle (D t))) ≠ b ∧
      N.rotation.faceNext (D t) = D (t + 1) := by
    intro t
    induction t with
    | zero =>
      refine ⟨hfar _, ?_⟩
      obtain ⟨h1, -⟩ := lift_next_farFaceC C hc hN hle spec (D 0) 0 rfl rfl (hfar _)
      apply liftDart_injective hle
      rw [RotationSystem.face_next_apply]
      apply Dart.ext; apply Prod.ext
      · change (N.rotation.next (D 0).symm).fst = ρ (0 + 1)
        rw [N.rotation.next_fst]; rfl
      · exact h1
    | succ t ih =>
      obtain ⟨hf, hs⟩ := ih
      obtain ⟨-, f2⟩ := lift_next_farFaceC C hc hN hle spec (D t) t rfl rfl hf
      have hf' : c (T.faceOf (liftDart hle (D (t + 1)))) ≠ b := by
        rw [← hs, RotationSystem.face_next_apply]; exact f2
      refine ⟨hf', ?_⟩
      obtain ⟨h1, -⟩ := lift_next_farFaceC C hc hN hle spec (D (t + 1)) (t + 1) rfl rfl hf'
      apply liftDart_injective hle
      rw [RotationSystem.face_next_apply]
      apply Dart.ext; apply Prod.ext
      · change (N.rotation.next (D (t + 1)).symm).fst = ρ (t + 1 + 1)
        rw [N.rotation.next_fst]; rfl
      · rw [h1]; rfl
  exact ⟨by have := C.three; omega, C.per, hNadj, fun t => (far t).2, C.inj⟩

/-- **The near side.** If the dart `ρ 0 → ρ 1` sees side `b`, the kept map of side `b` has the
reversed cycle `revR r ρ` (`t ↦ ρ ((r-1) t)`) as a face. -/
theorem kept_ringFace_rev (hnear : ∀ h : T.Adj (ρ 0) (ρ 1), c (T.faceOf ⟨(ρ 0, ρ 1), h⟩) = b) :
    RingFace N r (revR r ρ) := by
  classical
  have h3 := C.three
  obtain ⟨q, rfl⟩ : ∃ q, r = q + 2 := ⟨r - 2, by omega⟩
  have hq1 : q + 2 - 1 = q + 1 := by omega
  -- positions: ρ' s = ρ ((q+1) s)
  have rv : ∀ s, revR (q + 2) ρ s = ρ ((q + 1) * s) := fun s => by unfold revR; rw [hq1]
  -- the three ρ-positions of a reversed step
  have p2 : ∀ s, ρ ((q + 1) * s + q + 2) = ρ ((q + 1) * s) := fun s => by
    rw [show (q + 1) * s + q + 2 = (q + 1) * s + (q + 2) by omega, C.per]
  have p1 : ∀ s, (q + 1) * s + q + 1 = (q + 1) * (s + 1) := fun s => by ring
  have p0 : ∀ s, ρ ((q + 1) * (s + 2)) = ρ ((q + 1) * s + q) := fun s => by
    rw [show (q + 1) * (s + 2) = ((q + 1) * s + q) + (q + 2) by ring, C.per]
  have hTadj : ∀ s, T.Adj (revR (q + 2) ρ s) (revR (q + 2) ρ (s + 1)) := fun s => by
    rw [rv, rv]
    have a := C.adj ((q + 1) * s + q + 1)
    rw [show (q + 1) * s + q + 1 + 1 = (q + 1) * s + q + 2 by omega, p2, p1] at a
    exact a.symm
  have hNadj : ∀ s, N.Adj (revR (q + 2) ρ s) (revR (q + 2) ρ (s + 1)) := fun s => by
    show N.graph.Adj _ _
    rw [hN]
    refine ⟨hTadj s, Or.inl ?_, Or.inl ?_⟩ <;> rw [rv] <;> exact C.onCyc _
  let D : ℕ → N.Dart := fun s => ⟨(revR (q + 2) ρ s, revR (q + 2) ρ (s + 1)), hNadj s⟩
  have Dper : ∀ s, D (s + (q + 2)) = D s := fun s => by
    apply Dart.ext; apply Prod.ext
    · change revR (q + 2) ρ (s + (q + 2)) = revR (q + 2) ρ s
      unfold revR; rw [show (q + 2 - 1) * (s + (q + 2)) = (q + 2 - 1) * s + (q + 2) * (q + 1) by
        rw [hq1]; ring, C.per_mul]
    · change revR (q + 2) ρ (s + (q + 2) + 1) = revR (q + 2) ρ (s + 1)
      unfold revR; rw [show (q + 2 - 1) * (s + (q + 2) + 1) = (q + 2 - 1) * (s + 1) + (q + 2) * (q + 1) by
        rw [hq1]; ring, C.per_mul]
  -- one reversed step
  have step : ∀ s, c (T.faceOf (liftDart hle (D s))) ≠ b →
      c (T.faceOf (liftDart hle (D (s + 1)))) ≠ b ∧ N.rotation.faceNext (D s) = D (s + 1) := by
    intro s hf
    have hu : (liftDart hle (D s)).fst = ρ ((q + 1) * s + q + 2) := by
      change revR (q + 2) ρ s = _; rw [rv, p2]
    have hv : (liftDart hle (D s)).snd = ρ ((q + 1) * s + q + 1) := by
      change revR (q + 2) ρ (s + 1) = _; rw [rv, p1]
    obtain ⟨e1, f1⟩ := lift_next_farFaceC_rev C hc hN hle spec (D s) ((q + 1) * s + q) hu hv hf
    have hnext : N.rotation.faceNext (D s) = D (s + 1) := by
      apply liftDart_injective hle
      rw [RotationSystem.face_next_apply]
      apply Dart.ext; apply Prod.ext
      · change (N.rotation.next (D s).symm).fst = revR (q + 2) ρ (s + 1)
        rw [N.rotation.next_fst]; rfl
      · change _ = revR (q + 2) ρ (s + 1 + 1)
        rw [e1, rv, show s + 1 + 1 = s + 2 by omega, p0]
    refine ⟨?_, hnext⟩
    rw [← hnext, RotationSystem.face_next_apply]; exact f1
  -- the base: D (q+1) = ρ 1 → ρ 0 sees the far side
  have base : c (T.faceOf (liftDart hle (D (q + 1)))) ≠ b := by
    have e1 : revR (q + 2) ρ (q + 1) = ρ 1 := by
      rw [rv, show (q + 1) * (q + 1) = 1 + (q + 2) * q by ring, C.per_mul]
    have e0 : revR (q + 2) ρ (q + 1 + 1) = ρ 0 := by
      rw [rv, show (q + 1) * (q + 1 + 1) = 0 + (q + 2) * (q + 1) by ring, C.per_mul]
    have hd : liftDart hle (D (q + 1)) = (⟨(ρ 0, ρ 1), C.adj 0⟩ : T.Dart).symm := by
      apply Dart.ext; apply Prod.ext
      · exact e1
      · exact e0
    rw [hd]
    have hj := hc ⟨(ρ 0, ρ 1), C.adj 0⟩
    rw [cycInd_cycle C 0, hnear] at hj
    intro h
    rw [h] at hj
    exact (show ∀ x : ZMod 2, 1 ≠ x + x by decide) b hj
  have all : ∀ m, c (T.faceOf (liftDart hle (D (q + 1 + m)))) ≠ b ∧
      N.rotation.faceNext (D (q + 1 + m)) = D (q + 1 + m + 1) := by
    intro m
    induction m with
    | zero => exact ⟨base, (step _ base).2⟩
    | succ m ih =>
      have f : c (T.faceOf (liftDart hle (D (q + 1 + (m + 1))))) ≠ b := (step _ ih.1).1
      exact ⟨f, (step _ f).2⟩
  refine ⟨by omega, fun t => ?_, hNadj, fun s => ?_, fun s t hs ht e => ?_⟩
  · unfold revR
    rw [show (q + 2 - 1) * (t + (q + 2)) = (q + 2 - 1) * t + (q + 2) * (q + 1) by rw [hq1]; ring,
      C.per_mul]
  · have := (all (s + 1)).2
    rw [show q + 1 + (s + 1) = s + (q + 2) by omega, Dper,
      show s + (q + 2) + 1 = (s + 1) + (q + 2) by omega, Dper] at this
    exact this
  · -- injectivity of the reversed positions below the period
    rw [rv, rv] at e
    have m := C.mod_eq_of e
    have val : ∀ x, x < q + 2 → (q + 1) * x % (q + 2) = if x = 0 then 0 else q + 2 - x := by
      intro x hx
      rcases Nat.eq_zero_or_pos x with h0 | h0
      · subst h0; simp
      · obtain ⟨x', rfl⟩ : ∃ x', x = x' + 1 := ⟨x - 1, by omega⟩
        rw [if_neg (by omega)]
        have : (q + 1) * (x' + 1) = (q + 1 - x') + (q + 2) * x' := by
          have hx' : x' ≤ q := by omega
          obtain ⟨d, rfl⟩ : ∃ d, q = x' + d := ⟨q - x', by omega⟩
          rw [show x' + d + 1 - x' = d + 1 by omega]; ring
        rw [this, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (by omega)]
        omega
    rw [val s hs, val t ht] at m
    split_ifs at m <;> omega

end Map

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.kept_ringFace
#print axioms SimpleGraph.SphericalMap.kept_ringFace_rev
