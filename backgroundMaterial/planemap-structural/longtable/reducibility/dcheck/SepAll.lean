import Sep5

/-! Job 25 follow-ups: (i) separating triangles in the same framework (side maps + gluing by a
colour permutation; no Kempe chains), (ii) cycles with chords reduce to shorter separating cycles
(the edge indicators add, so potentials add), and (iii) the combined statement: a minimal
counterexample has no separating cycle of length `≤ 5` except a 5-cycle around a single vertex. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyCliqueLift VacancyIcosahedral RotationSystem PlaneMapConstruction
  DCheck DCheck.R2 DCheck.Meet

variable {n : ℕ} {T : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} {c : T.Face → ZMod 2}

/-- A cycle (chords allowed). -/
structure SepCyc (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) : Prop where
  three : 3 ≤ r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, T.Adj (ρ t) (ρ (t + 1))
  inj : ∀ s t, s < r → t < r → ρ s = ρ t → s = t

/-- A triangle is induced. -/
theorem SepCyc.icycle3 (C : SepCyc T 3 ρ) : ICycle T 3 ρ := by
  refine ⟨C.three, C.per, C.adj, C.inj, fun s t hs ht h => ?_⟩
  have hne : s ≠ t := fun e => by subst e; exact h.ne rfl
  rcases (show s = 0 ∨ s = 1 ∨ s = 2 by omega) with rfl | rfl | rfl <;>
    rcases (show t = 0 ∨ t = 1 ∨ t = 2 by omega) with rfl | rfl | rfl <;> simp_all

/-- Both sides of the cycle have a non-isolated vertex off it. -/
def BothSides (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (c : T.Face → ZMod 2) : Prop :=
  (∃ x y, ¬ OnCyc r ρ x ∧ OnSide T c 0 x ∧ T.Adj x y) ∧
  (∃ x y, ¬ OnCyc r ρ x ∧ OnSide T c 1 x ∧ T.Adj x y)

/-- **Separating triangles** in the cycle framework. -/
theorem colorable_of_separating_3cycle (C : ICycle T 3 ρ) (hc : CycPotential T 3 ρ c)
    (hs : BothSides T 3 ρ c)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  obtain ⟨⟨z0, y0, hz0, hon0, hy0⟩, ⟨z1, y1, hz1, hon1, hy1⟩⟩ := hs
  have e11 : (1 + 1 : ZMod 2) = 0 := by decide
  -- side maps and their colourings
  have side : ∀ (b : ZMod 2) {z y : Fin n}, ¬ OnCyc 3 ρ z → OnSide T c (b + 1) z → T.Adj z y →
      ∃ N : SphericalMap n, N.graph = sideGraph T.graph (keepC T c b 3 ρ) ∧
        ∃ col : Fin n → Fin 4, ProperOff N.graph z col := by
    intro b z y hz hzon hzy
    obtain ⟨N, hN, hle, -⟩ := subgraph_tracked T (sideGraph T.graph (keepC T c b 3 ρ))
      (fun _ _ e => e.1)
    have hzK : z ∉ keepC T c b 3 ρ := by
      rintro (h | h)
      · exact hz h
      · exact not_onSide_flip ⟨(z, y), hzy⟩ rfl hzon h
    have hlt := supportSize_lt_of_drop hN hle hzK hzy
    obtain ⟨cN⟩ := IH n N (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
    exact ⟨N, hN, fun x => cN x, fun u v huv _ _ => cN.valid huv⟩
  obtain ⟨N0, hN0, cA, hcA⟩ := side 0 hz1 (by simpa using hon1) hy1
  obtain ⟨N1, hN1, cB0, hcB0⟩ := side 1 hz0 (by rw [e11]; exact hon0) hy0
  set K0 := keepC T c 0 3 ρ
  set K1 := keepC T c 1 3 ρ
  have inK0 : ∀ t, ρ t ∈ K0 := fun t => Or.inl (C.onCyc t)
  have inK1 : ∀ t, ρ t ∈ K1 := fun t => Or.inl (C.onCyc t)
  have hh0 := ring_ne_off C hz0
  have hh1 := ring_ne_off C hz1
  have a0 : ∀ t, N0.Adj (ρ t) (ρ (t + 1)) := fun t => by
    show N0.graph.Adj _ _; rw [hN0]; exact ⟨C.adj t, inK0 t, inK0 (t + 1)⟩
  have a1 : ∀ t, N1.Adj (ρ t) (ρ (t + 1)) := fun t => by
    show N1.graph.Adj _ _; rw [hN1]; exact ⟨C.adj t, inK1 t, inK1 (t + 1)⟩
  have p3 : ρ 3 = ρ 0 := by rw [show (3 : ℕ) = 0 + 3 by rfl, C.per]
  obtain ⟨σ, s0, s1, s2⟩ := exists_perm_three (cA (ρ 0)) (cA (ρ 1)) (cA (ρ 2))
    (cB0 (ρ 0)) (cB0 (ρ 1)) (cB0 (ρ 2))
    (hcA (a0 0) (hh1 0) (hh1 1)) (hcA (a0 1) (hh1 1) (hh1 2))
    (by have := hcA (a0 2) (hh1 2) (hh1 3); rwa [p3] at this)
    (hcB0 (a1 0) (hh0 0) (hh0 1)) (hcB0 (a1 1) (hh0 1) (hh0 2))
    (by have := hcB0 (a1 2) (hh0 2) (hh0 3); rwa [p3] at this)
  let cB : Fin n → Fin 4 := fun x => σ (cB0 x)
  have hcB : ProperOff N1.graph z0 cB := fun u v huv hu hv e => hcB0 huv hu hv (σ.injective e)
  have agree : ∀ t, cA (ρ t) = cB (ρ t) := by
    intro t
    rw [← C.per_mod t]
    have ht := Nat.mod_lt t (show 0 < 3 by omega)
    rcases (show t % 3 = 0 ∨ t % 3 = 1 ∨ t % 3 = 2 by omega) with h | h | h <;> rw [h]
    exacts [s0.symm, s1.symm, s2.symm]
  have z1K0 : z1 ∉ K0 := by
    rintro (h | h)
    · exact hz1 h
    · exact not_onSide_flip (b := 0) ⟨(z1, y1), hy1⟩ rfl (by simpa using hon1) h
  have z0K1 : z0 ∉ K1 := by
    rintro (h | h)
    · exact hz0 h
    · exact not_onSide_flip (b := 1) ⟨(z0, y0), hy0⟩ rfl (by rw [e11]; exact hon0) h
  have in1 : ∀ {u v : Fin n}, T.Adj u v → u ∉ K0 → u ∈ K1 := fun {u v} huv hu =>
    Or.inr (by simpa using (keep_other C hc hu ⟨(u, v), huv⟩ rfl).2)
  have adj0 : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∈ K0 → N0.graph.Adj u v := fun h hu hv => by
    rw [hN0]; exact ⟨h, hu, hv⟩
  have adj1 : ∀ {u v}, T.Adj u v → u ∈ K1 → v ∈ K1 → N1.graph.Adj u v := fun h hu hv => by
    rw [hN1]; exact ⟨h, hu, hv⟩
  have ne1 : ∀ {u}, u ∈ K0 → u ≠ z1 := fun hu e => z1K0 (e ▸ hu)
  have ne0 : ∀ {u}, u ∈ K1 → u ≠ z0 := fun hu e => z0K1 (e ▸ hu)
  have mixed : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∉ K0 → OnCyc 3 ρ u := by
    intro u v huv hu hv
    by_contra hoff
    have hv' := keep_other C hc hv ⟨(v, u), huv.symm⟩ rfl
    have hu0 : OnSide T c 0 u := by rcases hu with h | h; exact absurd h hoff; exact h
    have := onSide_adjC C hc hoff hv'.1 huv hu0
    exact not_onSide_flip ⟨(v, u), huv.symm⟩ rfl hv'.2 this
  have mix : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∉ K0 → cA u ≠ cB v := by
    intro u v huv hu hv
    obtain ⟨t, -, rfl⟩ := mixed huv hu hv
    rw [agree t]
    exact hcB (adj1 huv (inK1 t) (in1 huv.symm hv)) (ne0 (inK1 t)) (ne0 (in1 huv.symm hv))
  refine ⟨SimpleGraph.Coloring.mk (fun v => if v ∈ K0 then cA v else cB v) ?_⟩
  intro u v huv
  by_cases hu : u ∈ K0 <;> by_cases hv : v ∈ K0
  · simp only [hu, hv, ↓reduceIte]; exact hcA (adj0 huv hu hv) (ne1 hu) (ne1 hv)
  · simp only [hu, hv, ↓reduceIte]; exact mix huv hu hv
  · simp only [hu, hv, ↓reduceIte]; exact (mix huv.symm hv hu).symm
  · simp only [hu, hv, ↓reduceIte]
    exact hcB (adj1 huv (in1 huv hu) (in1 huv.symm hv)) (ne0 (in1 huv hu)) (ne0 (in1 huv.symm hv))

/-! ### Chords: shifting, and splitting at the chord `ρ0 ρ2` -/

theorem SepCyc.per_mod (C : SepCyc T r ρ) (t : ℕ) : ρ (t % r) = ρ t := by
  conv_rhs => rw [← Nat.mod_add_div t r]
  induction t / r with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, C.per, ih]

theorem sum_shift_range (g : ℕ → ZMod 2) (hg : ∀ t, g (t + r) = g t) :
    ∀ v, ∑ t ∈ Finset.range r, g (t + v) = ∑ t ∈ Finset.range r, g t := by
  intro v
  induction v with
  | zero => rfl
  | succ v ih =>
    rw [← ih]
    rcases Nat.eq_zero_or_pos r with h | h
    · subst h; simp
    · obtain ⟨r', rfl⟩ : ∃ r', r = r' + 1 := ⟨r - 1, by omega⟩
      rw [Finset.sum_range_succ (fun t => g (t + (v + 1))), Finset.sum_range_succ' (fun t => g (t + v))]
      simp only [show ∀ t, t + 1 + v = t + (v + 1) by intro t; omega, Nat.zero_add]
      rw [show r' + (v + 1) = v + (r' + 1) by omega, hg]

theorem SepCyc.shift (C : SepCyc T r ρ) (v : ℕ) : SepCyc T r (fun t => ρ (t + v)) := by
  refine ⟨C.three, fun t => ?_, fun t => ?_, fun s t hs ht e => ?_⟩
  · show ρ (t + r + v) = ρ (t + v); rw [show t + r + v = (t + v) + r by omega, C.per]
  · have := C.adj (t + v); rwa [show t + v + 1 = t + 1 + v by omega] at this
  · have hpos : 0 < r := by have := C.three; omega
    have e' : ρ ((s + v) % r) = ρ ((t + v) % r) := by rw [C.per_mod, C.per_mod]; exact e
    have := C.inj _ _ (Nat.mod_lt _ hpos) (Nat.mod_lt _ hpos) e'
    have h2 : s % r = t % r := Nat.ModEq.add_right_cancel' v this
    rwa [Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at h2

theorem cycInd_shift (C : SepCyc T r ρ) (v : ℕ) : cycInd T r (fun t => ρ (t + v)) = cycInd T r ρ := by
  classical
  funext e
  unfold cycInd
  have := sum_shift_range (r := r) (fun t => if e.val = s(ρ t, ρ (t + 1)) then (1 : ZMod 2) else 0)
    (fun t => by simp only [show t + r + 1 = (t + 1) + r by omega, C.per]) v
  simpa [show ∀ t, t + v + 1 = t + 1 + v by intro t; omega] using this

theorem onCyc_of_shift (C : SepCyc T r ρ) (v : ℕ) {x : Fin n} (h : OnCyc r (fun t => ρ (t + v)) x) :
    OnCyc r ρ x := by
  obtain ⟨t, -, rfl⟩ := h
  exact ⟨(t + v) % r, Nat.mod_lt _ (by have := C.three; omega), C.per_mod _⟩

theorem BothSides.shift (C : SepCyc T r ρ) (v : ℕ) (h : BothSides T r ρ c) :
    BothSides T r (fun t => ρ (t + v)) c := by
  obtain ⟨⟨x, y, hx, h0, hxy⟩, ⟨x', y', hx', h1, hxy'⟩⟩ := h
  exact ⟨⟨x, y, fun h => hx (onCyc_of_shift C v h), h0, hxy⟩,
    ⟨x', y', fun h => hx' (onCyc_of_shift C v h), h1, hxy'⟩⟩

/-- A cycle given by three vertices. -/
def cyc3 (a b d : Fin n) : ℕ → Fin n := fun t => ![a, b, d] ⟨t % 3, Nat.mod_lt _ (by decide)⟩
/-- A cycle given by four vertices. -/
def cyc4 (a b d e : Fin n) : ℕ → Fin n := fun t => ![a, b, d, e] ⟨t % 4, Nat.mod_lt _ (by decide)⟩

open Classical in
theorem cycInd3 (a b d : Fin n) (e : T.graph.edgeSet) :
    cycInd T 3 (cyc3 a b d) e = (if e.val = s(a, b) then 1 else 0) +
      (if e.val = s(b, d) then 1 else 0) + (if e.val = s(d, a) then 1 else 0) := by
  unfold cycInd cyc3
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rfl

open Classical in
theorem cycInd4 (a b d f : Fin n) (e : T.graph.edgeSet) :
    cycInd T 4 (cyc4 a b d f) e = (if e.val = s(a, b) then 1 else 0) +
      (if e.val = s(b, d) then 1 else 0) + (if e.val = s(d, f) then 1 else 0) +
      (if e.val = s(f, a) then 1 else 0) := by
  unfold cycInd cyc4
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rfl

open Classical in
theorem cycIndR4 (C : SepCyc T 4 ρ) (e : T.graph.edgeSet) :
    cycInd T 4 ρ e = (if e.val = s(ρ 0, ρ 1) then 1 else 0) + (if e.val = s(ρ 1, ρ 2) then 1 else 0) +
      (if e.val = s(ρ 2, ρ 3) then 1 else 0) + (if e.val = s(ρ 3, ρ 0) then 1 else 0) := by
  unfold cycInd
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [show ρ (3 + 1) = ρ 0 by rw [show 3 + 1 = 0 + 4 by rfl, C.per]]

open Classical in
theorem cycIndR5 (C : SepCyc T 5 ρ) (e : T.graph.edgeSet) :
    cycInd T 5 ρ e = (if e.val = s(ρ 0, ρ 1) then 1 else 0) + (if e.val = s(ρ 1, ρ 2) then 1 else 0) +
      (if e.val = s(ρ 2, ρ 3) then 1 else 0) + (if e.val = s(ρ 3, ρ 4) then 1 else 0) +
      (if e.val = s(ρ 4, ρ 0) then 1 else 0) := by
  unfold cycInd
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add]
  rw [show ρ (4 + 1) = ρ 0 by rw [show 4 + 1 = 0 + 5 by rfl, C.per]]

theorem zmod2_dbl (q : ZMod 2) : q + q = 0 := by generalize q = x; revert x; decide

theorem cyc3_icycle {a b d : Fin n} (hab : T.Adj a b) (hbd : T.Adj b d) (hda : T.Adj d a) :
    ICycle T 3 (cyc3 a b d) := by
  have hne1 := hab.ne; have hne2 := hbd.ne; have hne3 := hda.ne
  refine SepCyc.icycle3 ⟨le_rfl, fun t => ?_, fun t => ?_, fun s t hs ht e => ?_⟩
  · unfold cyc3; congr 2; simp [Nat.add_mod_right]
  · unfold cyc3
    rcases (show t % 3 = 0 ∨ t % 3 = 1 ∨ t % 3 = 2 by omega) with h | h | h
    · have h' : (t + 1) % 3 = 1 := by omega
      simp only [h, h']; exact hab
    · have h' : (t + 1) % 3 = 2 := by omega
      simp only [h, h']; exact hbd
    · have h' : (t + 1) % 3 = 0 := by omega
      simp only [h, h']; exact hda
  · unfold cyc3 at e
    simp only [Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at e
    rcases (show s = 0 ∨ s = 1 ∨ s = 2 by omega) with rfl | rfl | rfl <;>
      rcases (show t = 0 ∨ t = 1 ∨ t = 2 by omega) with rfl | rfl | rfl <;> simp_all

theorem cyc4_cyc {a b d f : Fin n} (hab : T.Adj a b) (hbd : T.Adj b d) (hdf : T.Adj d f)
    (hfa : T.Adj f a) (hne : ∀ x y : Fin 4, x ≠ y → ![a, b, d, f] x ≠ ![a, b, d, f] y) :
    SepCyc T 4 (cyc4 a b d f) := by
  refine ⟨by omega, fun t => ?_, fun t => ?_, fun s t hs ht e => ?_⟩
  · unfold cyc4; congr 2; simp [Nat.add_mod_right]
  · unfold cyc4
    rcases (show t % 4 = 0 ∨ t % 4 = 1 ∨ t % 4 = 2 ∨ t % 4 = 3 by omega) with h | h | h | h
    · have h' : (t + 1) % 4 = 1 := by omega
      simp only [h, h']; exact hab
    · have h' : (t + 1) % 4 = 2 := by omega
      simp only [h, h']; exact hbd
    · have h' : (t + 1) % 4 = 3 := by omega
      simp only [h, h']; exact hdf
    · have h' : (t + 1) % 4 = 0 := by omega
      simp only [h, h']; exact hfa
  · unfold cyc4 at e
    by_contra hst
    exact hne ⟨s % 4, Nat.mod_lt _ (by omega)⟩ ⟨t % 4, Nat.mod_lt _ (by omega)⟩
      (fun h => hst (by
        have := congrArg Fin.val h; simp only at this
        rwa [Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at this)) e

/-- Sides of a sub-cycle from sides of the cycle, through the potential sum. -/
theorem sides_split (C : SepCyc T r ρ) {rA : ℕ} {ρA : ℕ → Fin n} (CA : ICycle T rA ρA)
    {cA : T.Face → ZMod 2} (hcA : CycPotential T rA ρA cA) {rB : ℕ} {ρB : ℕ → Fin n}
    (hsubA : ∀ x, OnCyc rA ρA x → OnCyc r ρ x) (hsubB : ∀ x, OnCyc rB ρB x → OnCyc r ρ x)
    (hs : BothSides T r ρ c) :
    BothSides T rA ρA cA ∨ BothSides T rB ρB (fun f => c f + cA f) := by
  obtain ⟨⟨x0, y0, hx0, h0, hxy0⟩, ⟨x1, y1, hx1, h1, hxy1⟩⟩ := hs
  have hA0 : ¬ OnCyc rA ρA x0 := fun h => hx0 (hsubA _ h)
  have hA1 : ¬ OnCyc rA ρA x1 := fun h => hx1 (hsubA _ h)
  have hB0 : ¬ OnCyc rB ρB x0 := fun h => hx0 (hsubB _ h)
  have hB1 : ¬ OnCyc rB ρB x1 := fun h => hx1 (hsubB _ h)
  let d0 : T.Dart := ⟨(x0, y0), hxy0⟩
  let d1 : T.Dart := ⟨(x1, y1), hxy1⟩
  have sA0 := onSide_of_dartC CA hcA hA0 d0 rfl
  have sA1 := onSide_of_dartC CA hcA hA1 d1 rfl
  set a0 := cA (T.faceOf d0)
  set a1 := cA (T.faceOf d1)
  have sB : ∀ {x : Fin n} {b a : ZMod 2}, OnSide T c b x → OnSide T cA a x →
      OnSide T (fun f => c f + cA f) (b + a) x := fun hb ha d hd => by
    show c _ + cA _ = _; rw [hb d hd, ha d hd]
  by_cases hea : a0 = a1
  · right
    have s0 := sB h0 sA0
    have s1 := sB h1 sA1
    rw [← hea] at s1
    rcases (show a0 = 0 ∨ a0 = 1 by generalize a0 = x; revert x; decide) with ha | ha
    · rw [ha] at s0 s1
      exact ⟨⟨x0, y0, hB0, by simpa using s0, hxy0⟩, ⟨x1, y1, hB1, by simpa using s1, hxy1⟩⟩
    · rw [ha] at s0 s1
      exact ⟨⟨x1, y1, hB1, by simpa [show (1 + 1 : ZMod 2) = 0 by decide] using s1, hxy1⟩,
        ⟨x0, y0, hB0, by simpa using s0, hxy0⟩⟩
  · left
    rcases (show a0 = 0 ∨ a0 = 1 by generalize a0 = x; revert x; decide) with ha | ha
    · have hb : a1 = 1 := by rw [ha] at hea; generalize a1 = x at hea ⊢; revert x; decide
      rw [ha] at sA0; rw [hb] at sA1
      exact ⟨⟨x0, y0, hA0, sA0, hxy0⟩, ⟨x1, y1, hA1, sA1, hxy1⟩⟩
    · have hb : a1 = 0 := by rw [ha] at hea; generalize a1 = x at hea ⊢; revert x; decide
      rw [ha] at sA0; rw [hb] at sA1
      exact ⟨⟨x1, y1, hA1, sA1, hxy1⟩, ⟨x0, y0, hA0, sA0, hxy0⟩⟩

theorem onCyc3_sub {a b d : Fin n} {x : Fin n} (h : OnCyc 3 (cyc3 a b d) x) : x = a ∨ x = b ∨ x = d := by
  obtain ⟨t, ht, rfl⟩ := h
  unfold cyc3
  rcases (show t = 0 ∨ t = 1 ∨ t = 2 by omega) with rfl | rfl | rfl <;> simp

theorem onCyc4_sub {a b d f : Fin n} {x : Fin n} (h : OnCyc 4 (cyc4 a b d f) x) :
    x = a ∨ x = b ∨ x = d ∨ x = f := by
  obtain ⟨t, ht, rfl⟩ := h
  unfold cyc4
  rcases (show t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 by omega) with rfl | rfl | rfl | rfl <;> simp

theorem onC (C : SepCyc T r ρ) (t : ℕ) : OnCyc r ρ (ρ t) :=
  ⟨t % r, Nat.mod_lt _ (by have := C.three; omega), C.per_mod t⟩

/-- **A 4-cycle with the chord `ρ0 ρ2`** reduces to one of its two triangles. -/
theorem chord4 (C : SepCyc T 4 ρ) (hc : CycPotential T 4 ρ c) (hch : T.Adj (ρ 0) (ρ 2))
    (hs : BothSides T 4 ρ c)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  have p4 : ρ 4 = ρ 0 := by rw [show (4 : ℕ) = 0 + 4 by rfl, C.per]
  have a30 : T.Adj (ρ 3) (ρ 0) := by have := C.adj 3; rwa [p4] at this
  have CA : ICycle T 3 (cyc3 (ρ 0) (ρ 1) (ρ 2)) := cyc3_icycle (C.adj 0) (C.adj 1) hch.symm
  have CB : ICycle T 3 (cyc3 (ρ 0) (ρ 2) (ρ 3)) := cyc3_icycle hch (C.adj 2) a30
  obtain ⟨cA, hcA⟩ := exists_cycPotential CA
  have hcB : CycPotential T 3 (cyc3 (ρ 0) (ρ 2) (ρ 3)) (fun f => c f + cA f) := by
    intro d
    have h1 := hc d
    have h2 := hcA d
    rw [cycIndR4 C] at h1
    rw [cycInd3] at h2 ⊢
    rw [show s(ρ 2, ρ 0) = s(ρ 0, ρ 2) from Sym2.eq_swap] at h2
    have q1 := zmod2_dbl (if (edgeOfDart d).val = s(ρ 0, ρ 1) then (1 : ZMod 2) else 0)
    have q2 := zmod2_dbl (if (edgeOfDart d).val = s(ρ 1, ρ 2) then (1 : ZMod 2) else 0)
    show _ = c _ + cA _ + (c _ + cA _)
    linear_combination h1 + h2 - q1 - q2
  have sub : ∀ {a b d : Fin n}, (a = ρ 0 ∨ a = ρ 1 ∨ a = ρ 2 ∨ a = ρ 3) →
      (b = ρ 0 ∨ b = ρ 1 ∨ b = ρ 2 ∨ b = ρ 3) → (d = ρ 0 ∨ d = ρ 1 ∨ d = ρ 2 ∨ d = ρ 3) →
      ∀ x, OnCyc 3 (cyc3 a b d) x → OnCyc 4 ρ x := by
    intro a b d ha hb hd x hx
    rcases onCyc3_sub hx with rfl | rfl | rfl
    all_goals first
      | (rcases ha with rfl | rfl | rfl | rfl <;> exact onC C _)
      | (rcases hb with rfl | rfl | rfl | rfl <;> exact onC C _)
      | (rcases hd with rfl | rfl | rfl | rfl <;> exact onC C _)
  rcases sides_split ⟨C.three, C.per, C.adj, C.inj⟩ CA hcA
      (sub (Or.inl rfl) (Or.inr (Or.inl rfl)) (Or.inr (Or.inr (Or.inl rfl))))
      (sub (Or.inl rfl) (Or.inr (Or.inr (Or.inl rfl))) (Or.inr (Or.inr (Or.inr rfl)))) hs with h | h
  · exact colorable_of_separating_3cycle CA hcA h IH
  · exact colorable_of_separating_3cycle CB hcB h IH

theorem shift_potential (C : SepCyc T r ρ) (hc : CycPotential T r ρ c) (v : ℕ) :
    CycPotential T r (fun t => ρ (t + v)) c := by
  intro d; rw [cycInd_shift C v]; exact hc d

theorem shift_mod (C : SepCyc T r ρ) (u t : ℕ) : ρ (t + u) = ρ ((t + u) % r) := (C.per_mod _).symm

/-- **Separating 4-cycles, chords allowed.** -/
theorem colorable_of_sep4 (C : SepCyc T 4 ρ) (hc : CycPotential T 4 ρ c) (hs : BothSides T 4 ρ c)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  by_cases hind : ∀ s t, s < 4 → t < 4 → T.Adj (ρ s) (ρ t) → t = (s + 1) % 4 ∨ s = (t + 1) % 4
  · obtain ⟨⟨z0, y0, hz0, h0, hy0⟩, ⟨z1, y1, hz1, h1, hy1⟩⟩ := hs
    exact colorable_of_separating_4cycle ⟨C.three, C.per, C.adj, C.inj, hind⟩ hc hz0 h0 hy0 hz1 h1 hy1 IH
  · push_neg at hind
    obtain ⟨s, t, hs4, ht4, hadj, h1, h2⟩ := hind
    have hst : s ≠ t := fun e => by subst e; exact hadj.ne rfl
    -- the chord joins positions u and u + 2, u ∈ {0, 1}
    obtain ⟨u, hu, hch⟩ : ∃ u, u < 2 ∧ T.Adj (ρ u) (ρ (u + 2)) := by
      rcases (show s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 by omega) with rfl | rfl | rfl | rfl <;>
        rcases (show t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 by omega) with rfl | rfl | rfl | rfl <;>
        simp_all
      · exact ⟨0, by omega, hadj⟩
      · exact ⟨1, by omega, hadj⟩
      · exact ⟨0, by omega, hadj.symm⟩
      · exact ⟨1, by omega, hadj.symm⟩
    have C' := C.shift u
    refine chord4 C' (shift_potential C hc u) ?_ (hs.shift C u) IH
    simpa [Nat.add_comm] using hch

/-- **A 5-cycle with the chord `ρ0 ρ2`** reduces to the triangle `ρ0 ρ1 ρ2` or the 4-cycle
`ρ0 ρ2 ρ3 ρ4`. -/
theorem chord5 (C : SepCyc T 5 ρ) (hc : CycPotential T 5 ρ c) (hch : T.Adj (ρ 0) (ρ 2))
    (hs : BothSides T 5 ρ c)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  have p5 : ρ 5 = ρ 0 := by rw [show (5 : ℕ) = 0 + 5 by rfl, C.per]
  have a40 : T.Adj (ρ 4) (ρ 0) := by have := C.adj 4; rwa [p5] at this
  have CA : ICycle T 3 (cyc3 (ρ 0) (ρ 1) (ρ 2)) := cyc3_icycle (C.adj 0) (C.adj 1) hch.symm
  have inj : ∀ i j, i < 5 → j < 5 → i ≠ j → ρ i ≠ ρ j := fun i j hi hj h e => h (C.inj i j hi hj e)
  have CB : SepCyc T 4 (cyc4 (ρ 0) (ρ 2) (ρ 3) (ρ 4)) := by
    refine cyc4_cyc hch (C.adj 2) (C.adj 3) a40 ?_
    intro x y hxy
    fin_cases x <;> fin_cases y <;> simp at hxy ⊢ <;>
      first
      | exact inj _ _ (by omega) (by omega) (by omega)
  obtain ⟨cA, hcA⟩ := exists_cycPotential CA
  have hcB : CycPotential T 4 (cyc4 (ρ 0) (ρ 2) (ρ 3) (ρ 4)) (fun f => c f + cA f) := by
    intro d
    have h1 := hc d
    have h2 := hcA d
    rw [cycIndR5 C] at h1
    rw [cycInd3] at h2
    rw [cycInd4]
    rw [show s(ρ 2, ρ 0) = s(ρ 0, ρ 2) from Sym2.eq_swap] at h2
    have q1 := zmod2_dbl (if (edgeOfDart d).val = s(ρ 0, ρ 1) then (1 : ZMod 2) else 0)
    have q2 := zmod2_dbl (if (edgeOfDart d).val = s(ρ 1, ρ 2) then (1 : ZMod 2) else 0)
    show _ = c _ + cA _ + (c _ + cA _)
    linear_combination h1 + h2 - q1 - q2
  have sub3 : ∀ x, OnCyc 3 (cyc3 (ρ 0) (ρ 1) (ρ 2)) x → OnCyc 5 ρ x := by
    intro x hx; rcases onCyc3_sub hx with rfl | rfl | rfl <;> exact onC C _
  have sub4 : ∀ x, OnCyc 4 (cyc4 (ρ 0) (ρ 2) (ρ 3) (ρ 4)) x → OnCyc 5 ρ x := by
    intro x hx; rcases onCyc4_sub hx with rfl | rfl | rfl | rfl <;> exact onC C _
  rcases sides_split ⟨C.three, C.per, C.adj, C.inj⟩ CA hcA sub3 sub4 hs with h | h
  · exact colorable_of_separating_3cycle CA hcA h IH
  · exact colorable_of_sep4 CB hcB h IH

/-- Each side has two distinct non-isolated vertices off the cycle. -/
def BothSides2 (T : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (c : T.Face → ZMod 2) : Prop :=
  ∀ b : ZMod 2, ∃ x x' y y', x ≠ x' ∧ ¬ OnCyc r ρ x ∧ OnSide T c b x ∧ T.Adj x y ∧
    ¬ OnCyc r ρ x' ∧ OnSide T c b x' ∧ T.Adj x' y'

theorem BothSides2.both (h : BothSides2 T r ρ c) : BothSides T r ρ c := by
  obtain ⟨x, -, y, -, -, hx, h0, hxy, -⟩ := h 0
  obtain ⟨x', -, y', -, -, hx', h1, hxy', -⟩ := h 1
  exact ⟨⟨x, y, hx, h0, hxy⟩, ⟨x', y', hx', h1, hxy'⟩⟩

/-- **Separating 5-cycles with two vertices on each side, chords allowed.** -/
theorem colorable_of_sep5 (C : SepCyc T 5 ρ) (hc : CycPotential T 5 ρ c) (hs : BothSides2 T 5 ρ c)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  by_cases hind : ∀ s t, s < 5 → t < 5 → T.Adj (ρ s) (ρ t) → t = (s + 1) % 5 ∨ s = (t + 1) % 5
  · obtain ⟨z0, z0', y0, y0', h00, hz0, h0, hy0, hz0', h0', hy0'⟩ := hs 0
    obtain ⟨z1, z1', y1, y1', h11, hz1, h1, hy1, hz1', h1', hy1'⟩ := hs 1
    exact colorable_of_separating_5cycle ⟨C.three, C.per, C.adj, C.inj, hind⟩ hc
      hz0 h0 hy0 hz0' h0' hy0' h00 hz1 h1 hy1 hz1' h1' hy1' h11 IH
  · push_neg at hind
    obtain ⟨s, t, hs5, ht5, hadj, h1, h2⟩ := hind
    -- the chord joins positions u and u + 2 (mod 5)
    obtain ⟨u, hch⟩ : ∃ u, T.Adj (ρ u) (ρ (u + 2)) := by
      have hst : s ≠ t := fun e => by subst e; exact hadj.ne rfl
      rcases (show s = 0 ∨ s = 1 ∨ s = 2 ∨ s = 3 ∨ s = 4 by omega) with rfl | rfl | rfl | rfl | rfl <;>
        rcases (show t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 by omega) with rfl | rfl | rfl | rfl | rfl <;>
        simp_all
      all_goals first
        | exact ⟨_, hadj⟩
        | exact ⟨_, hadj.symm⟩
        | exact ⟨3, by rw [show 3 + 2 = 0 + 5 by rfl, C.per]; first | exact hadj | exact hadj.symm⟩
        | exact ⟨4, by rw [show 4 + 2 = 1 + 5 by rfl, C.per]; first | exact hadj | exact hadj.symm⟩
    refine chord5 (C.shift u) (shift_potential C hc u) ?_ (hs.both.shift C u) IH
    simpa [Nat.add_comm] using hch

/-- **B2 (combined).** If a cycle of length `3 ≤ r ≤ 5` of `T` has a non-isolated vertex on each side
(for `r = 5`: two on each side), then `T` is four-colourable as soon as every spherical map of
smaller support is. So a minimal counterexample has no separating 3- or 4-cycle, and no separating
5-cycle other than one around a single vertex. -/
theorem colorable_of_short_separating_cycle (C : SepCyc T r ρ) (hr : r ≤ 5) (hc : CycPotential T r ρ c)
    (hs : BothSides T r ρ c) (h5 : r = 5 → BothSides2 T r ρ c)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  have h3 := C.three
  rcases (show r = 3 ∨ r = 4 ∨ r = 5 by omega) with rfl | rfl | rfl
  · exact colorable_of_separating_3cycle C.icycle3 hc hs IH
  · exact colorable_of_sep4 C hc hs IH
  · exact colorable_of_sep5 C hc (h5 rfl) IH

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.colorable_of_short_separating_cycle

#print axioms SimpleGraph.SphericalMap.colorable_of_separating_3cycle
