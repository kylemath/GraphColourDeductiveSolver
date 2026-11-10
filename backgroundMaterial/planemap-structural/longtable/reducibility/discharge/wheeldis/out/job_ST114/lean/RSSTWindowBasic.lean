import ClaimGlue

/-!
# ST-114 B3, generic tools (Studio, 10 Nov)

Map-level lemmas used by the induced-window theorem (`RSSTWindow.lean`). Nothing here mentions a link.
- L0 `facial_nx`: a facial triangle `a b c` has `b, c` consecutive in `rot(a)`, in one orientation.
- `face_nx`: the face of a rotation corner.
- `nx_unique`, `nx_inj_left`: the rotation is a function and a permutation.
- L1 `rot_iter_mod`: a dart orbit at `v` has length `deg v`.
- L5 `sides_of_edge`, `onSide_adjC'`: off-cycle vertices on the two faces of a cycle edge get opposite sides, and adjacent
  off-cycle vertices share a side (for the `Cyc` of `DCheckPinchGeom`, chords allowed).
- `cyc5`, `cyc5_cyc`, `onCyc5_sub`: five-vertex cycles, as `SepAll.cyc4`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap RotationSystem

variable {n : ℕ} {T : SphericalMap n}

/-- The face of a rotation corner: if `c` follows `b` at `a`, the darts `b → a` and `a → c` bound one face. -/
theorem face_nx {a b c : Fin n} (h : Nx T a b c) (hba : T.Adj b a) (hac : T.Adj a c) :
    T.faceOf ⟨(b, a), hba⟩ = T.faceOf ⟨(a, c), hac⟩ := by
  obtain ⟨hab, hac', e⟩ := nx_dart h
  have := T.rotation.face_of_face_next (⟨(b, a), hba⟩ : T.Dart)
  rw [RotationSystem.face_next_apply] at this
  exact this.symm.trans (congrArg T.rotation.faceOf e)

/-- L0. A facial triangle `a b c` has `b` and `c` consecutive in the rotation at `a`. -/
theorem facial_nx (htri : T.Triangulated) {a b c : Fin n} (hf : Facial T a b c) :
    Nx T a b c ∨ Nx T a c b := by
  rcases hf with h | h
  · exact Or.inr (nx_tri htri h).2
  · exact Or.inl h

theorem nx_unique {a b c c' : Fin n} (h : Nx T a b c) (h' : Nx T a b c') : c = c' := by
  obtain ⟨h1, e1⟩ := h
  obtain ⟨h2, e2⟩ := h'
  rw [← e1, ← e2]

theorem nx_inj_left {a b b' c : Fin n} (h : Nx T a b c) (h' : Nx T a b' c) : b = b' := by
  obtain ⟨h1, h2, e1⟩ := nx_dart h
  obtain ⟨h1', h2', e2⟩ := nx_dart h'
  have := T.rotation.next.injective (e1.trans e2.symm)
  exact congrArg (fun d : T.Dart => d.snd) this

/-- L1. Two iterates of the rotation on a dart at `v` agree only modulo `deg v`. -/
theorem rot_iter_mod {v : Fin n} (e : T.Dart) (he : e.fst = v) {i j : ℕ}
    (h : (⇑T.rotation.next)^[i] e = (⇑T.rotation.next)^[j] e) :
    i % T.graph.degree v = j % T.graph.degree v := by
  classical
  let a : T.graph.neighborSet v := ⟨e.snd, by rw [← he]; exact e.adj⟩
  have ha : T.graph.dartOfNeighborSet v a = e := by
    apply Dart.ext; exact Prod.ext he.symm rfl
  have hsc : Function.Semiconj (T.graph.dartOfNeighborSet v) (T.rotation.neighborRotation v)
      T.rotation.next := T.rotation.neighbor_rotation_dart v
  have h' : (⇑(T.rotation.neighborRotation v))^[i] a = (⇑(T.rotation.neighborRotation v))^[j] a := by
    apply T.graph.dartOfNeighborSet_injective v
    rw [hsc.iterate_right i a, hsc.iterate_right j a, ha]
    exact h
  have hp := T.rotation.neighbor_period_eq_degree v a
  have hpos : 0 < Function.minimalPeriod (⇑(T.rotation.neighborRotation v)) a :=
    Function.minimalPeriod_pos_of_mem_periodicPts
      ((T.rotation.neighborRotation v).injective.mem_periodicPts a)
  rw [← Function.iterate_mod_minimalPeriod_eq (n := i),
    ← Function.iterate_mod_minimalPeriod_eq (n := j)] at h'
  have := Function.iterate_injOn_Iio_minimalPeriod (Nat.mod_lt i hpos) (Nat.mod_lt j hpos) h'
  rw [hp] at this
  exact this

/-- At a vertex of degree at least four there is a neighbour avoiding three given vertices. -/
theorem exists_nbr_avoid {v : Fin n} (hv : 4 ≤ T.graph.degree v) (a b c : Fin n) :
    ∃ z, T.Adj v z ∧ z ≠ a ∧ z ≠ b ∧ z ≠ c := by
  classical
  have hcard : ({a, b, c} : Finset (Fin n)).card < (T.graph.neighborFinset v).card := by
    rw [card_neighborFinset_eq_degree]
    have := Finset.card_le_three (a := a) (b := b) (c := c)
    omega
  obtain ⟨z, hz, hz'⟩ := Finset.exists_mem_notMem_of_card_lt_card hcard
  rw [mem_neighborFinset] at hz
  simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at hz'
  exact ⟨z, hz, hz'.1, hz'.2.1, hz'.2.2⟩

/-! ## Sides of a cycle (chords allowed) -/

variable {r : ℕ} {ρ : ℕ → Fin n} {c : T.Face → ZMod 2}

/-- Adjacent off-cycle vertices lie on one side. -/
theorem onSide_adjC' (C : Cyc T r ρ) (hc : CycPotential T r ρ c) {x y : Fin n}
    (hx : ¬ OnCyc r ρ x) (hy : ¬ OnCyc r ρ y) (hxy : T.Adj x y) {b : ZMod 2} (h : OnSide T c b x) :
    OnSide T c b y := by
  let d : T.Dart := ⟨(x, y), hxy⟩
  have h0 := cycInd_off' C d hx
  have := zmod2_swap _ _ _ (hc d)
  rw [h0, zero_add, h d rfl] at this
  have hs := onSide_of_dartC' C hc hy d.symm rfl
  rwa [this] at hs

/-- L5. Off-cycle vertices touching the two faces of the cycle edge `ρ 0 ρ 1` lie on opposite sides. -/
theorem sides_of_edge (C : Cyc T r ρ) (hc : CycPotential T r ρ c) {p q : Fin n} (dp dq : T.Dart)
    (hp : dp.fst = p) (hq : dq.fst = q) (hpo : ¬ OnCyc r ρ p) (hqo : ¬ OnCyc r ρ q)
    (h01 : T.Adj (ρ 0) (ρ 1)) (h10 : T.Adj (ρ 1) (ρ 0))
    (fp : T.faceOf dp = T.faceOf ⟨(ρ 0, ρ 1), h01⟩) (fq : T.faceOf dq = T.faceOf ⟨(ρ 1, ρ 0), h10⟩) :
    ∃ b, OnSide T c b p ∧ OnSide T c (b + 1) q := by
  have h1 := cycInd_cycle' C 0
  have h2 := hc ⟨(ρ 0, ρ (0 + 1)), C.adj 0⟩
  rw [h1] at h2
  have sp := onSide_of_dartC' C hc hpo dp hp
  have sq := onSide_of_dartC' C hc hqo dq hq
  refine ⟨c (T.faceOf dp), sp, ?_⟩
  have e : c (T.faceOf dq) = c (T.faceOf dp) + 1 := by
    rw [fp, fq]
    have := zmod2_swap _ _ _ h2
    exact this.trans (add_comm _ _)
  rwa [e] at sq

theorem zmod2_cases (b : ZMod 2) : b = 0 ∨ b = 1 := by generalize b = x; revert x; decide

/-- `BothSides` from two off-cycle vertices on opposite sides. -/
theorem bothSides_of {p q y y' : Fin n} {b : ZMod 2} (hpo : ¬ OnCyc r ρ p) (hqo : ¬ OnCyc r ρ q)
    (sp : OnSide T c b p) (sq : OnSide T c (b + 1) q) (hp : T.Adj p y) (hq : T.Adj q y') :
    BothSides T r ρ c := by
  rcases zmod2_cases b with rfl | rfl
  · exact ⟨⟨p, y, hpo, sp, hp⟩, ⟨q, y', hqo, by simpa using sq, hq⟩⟩
  · exact ⟨⟨q, y', hqo, by simpa [show (1 + 1 : ZMod 2) = 0 by decide] using sq, hq⟩,
      ⟨p, y, hpo, sp, hp⟩⟩

/-! ## Five-vertex cycles -/

/-- A cycle given by five vertices. -/
def cyc5 (a b d e f : Fin n) : ℕ → Fin n := fun t => ![a, b, d, e, f] ⟨t % 5, Nat.mod_lt _ (by decide)⟩

theorem cyc5_cyc {a b d e f : Fin n} (hab : T.Adj a b) (hbd : T.Adj b d) (hde : T.Adj d e)
    (hef : T.Adj e f) (hfa : T.Adj f a)
    (hne : ∀ x y : Fin 5, x ≠ y → ![a, b, d, e, f] x ≠ ![a, b, d, e, f] y) :
    Cyc T 5 (cyc5 a b d e f) := by
  refine ⟨by omega, fun t => ?_, fun t => ?_, fun s t hs ht h => ?_⟩
  · unfold cyc5; congr 2; simp [Nat.add_mod_right]
  · unfold cyc5
    rcases (show t % 5 = 0 ∨ t % 5 = 1 ∨ t % 5 = 2 ∨ t % 5 = 3 ∨ t % 5 = 4 by omega) with
      h | h | h | h | h
    · have h' : (t + 1) % 5 = 1 := by omega
      simp only [h, h']; exact hab
    · have h' : (t + 1) % 5 = 2 := by omega
      simp only [h, h']; exact hbd
    · have h' : (t + 1) % 5 = 3 := by omega
      simp only [h, h']; exact hde
    · have h' : (t + 1) % 5 = 4 := by omega
      simp only [h, h']; exact hef
    · have h' : (t + 1) % 5 = 0 := by omega
      simp only [h, h']; exact hfa
  · unfold cyc5 at h
    by_contra hst
    exact hne ⟨s % 5, Nat.mod_lt _ (by omega)⟩ ⟨t % 5, Nat.mod_lt _ (by omega)⟩
      (fun h' => hst (by
        have := congrArg Fin.val h'; simp only at this
        rwa [Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at this)) h

theorem onCyc5_sub {a b d e f : Fin n} {x : Fin n} (h : OnCyc 5 (cyc5 a b d e f) x) :
    x = a ∨ x = b ∨ x = d ∨ x = e ∨ x = f := by
  obtain ⟨t, ht, rfl⟩ := h
  unfold cyc5
  rcases (show t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 by omega) with rfl | rfl | rfl | rfl | rfl <;> simp

theorem ne_vec4 {a b d e : Fin n} (h01 : a ≠ b) (h02 : a ≠ d) (h03 : a ≠ e) (h12 : b ≠ d) (h13 : b ≠ e)
    (h23 : d ≠ e) : ∀ x y : Fin 4, x ≠ y → ![a, b, d, e] x ≠ ![a, b, d, e] y := by
  intro x y hxy
  fin_cases x <;> fin_cases y <;> simp at hxy ⊢ <;>
    first | assumption | exact Ne.symm ‹_›

theorem ne_vec5 {a b d e f : Fin n} (h01 : a ≠ b) (h02 : a ≠ d) (h03 : a ≠ e) (h04 : a ≠ f)
    (h12 : b ≠ d) (h13 : b ≠ e) (h14 : b ≠ f) (h23 : d ≠ e) (h24 : d ≠ f) (h34 : e ≠ f) :
    ∀ x y : Fin 5, x ≠ y → ![a, b, d, e, f] x ≠ ![a, b, d, e, f] y := by
  intro x y hxy
  fin_cases x <;> fin_cases y <;> simp at hxy ⊢ <;>
    first | assumption | exact Ne.symm ‹_›

/-- A `SepAll.cyc4` cycle as a `Cyc`. -/
theorem cyc4_cyc' {a b d f : Fin n} (hab : T.Adj a b) (hbd : T.Adj b d) (hdf : T.Adj d f)
    (hfa : T.Adj f a) (hne : ∀ x y : Fin 4, x ≠ y → ![a, b, d, f] x ≠ ![a, b, d, f] y) :
    Cyc T 4 (cyc4 a b d f) :=
  let C := cyc4_cyc hab hbd hdf hfa hne
  ⟨C.three, C.per, C.adj, C.inj⟩

example (a b d f : Fin n) : cyc4 a b d f 0 = a ∧ cyc4 a b d f 1 = b := ⟨rfl, rfl⟩
example (a b d e f : Fin n) : cyc5 a b d e f 0 = a ∧ cyc5 a b d e f 1 = b := ⟨rfl, rfl⟩

end SimpleGraph.SphericalMap.RSSTSeed
