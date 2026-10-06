module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame

/-!
# Jordan separation at a vertex, for arbitrary rotation positions

`rotation_arc_separation`: let `x` be a vertex, `p` a walk between two neighbours `a` and `b`
of `x` that avoids `x`, and `u`, `w` neighbours of `x` lying strictly inside the two different
rotation arcs cut out by `a` and `b`. Then every walk from `u` to `w` that avoids `x` meets `p`.

This generalises the library's `alternating_walks_intersect` (which needs the three later
neighbours to be rotation-consecutive). It is the geometric input for the non-crossing of Kempe
chains on a ring (D-reducibility) and on a separating four-cycle.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap

variable {n : ℕ} {M : SphericalMap n}

private theorem zmod2_add_self (a : ZMod 2) : a + a = 0 := by
  rw [← two_mul, show (2 : ZMod 2) = 0 from ZMod.natCast_self 2, zero_mul]

/-- **Arc separation at a vertex.** -/
theorem rotation_arc_separation {x a b u w : Fin n} (hxa : M.Adj x a)
    {β μ ω : ℕ} (hμ : 0 < μ) (hμβ : μ < β) (hβω : β < ω)
    (hω : ω < Function.minimalPeriod (⇑M.rotation.next) (⟨(x, a), hxa⟩ : M.Dart))
    (hb : ((⇑M.rotation.next)^[β] ⟨(x, a), hxa⟩).snd = b)
    (hu : ((⇑M.rotation.next)^[μ] ⟨(x, a), hxa⟩).snd = u)
    (hw : ((⇑M.rotation.next)^[ω] ⟨(x, a), hxa⟩).snd = w)
    (p : M.graph.Walk a b) (hp : x ∉ p.support)
    (q : M.graph.Walk u w) (hq : x ∉ q.support)
    (hdis : ∀ z ∈ q.support, z ∉ p.support) : False := by
  classical
  set D0 : M.Dart := ⟨(x, a), hxa⟩
  set D : ℕ → M.Dart := fun j => (⇑M.rotation.next)^[j] D0 with hD
  have Dfst : ∀ j, (D j).fst = x := fun j => iterate_next_fst M j D0
  set P := Function.minimalPeriod (⇑M.rotation.next) D0
  have hPpos : 0 < P := by omega
  -- distinct positions below the period give distinct heads
  have head_ne : ∀ i j, i < P → j < P → i ≠ j → (D i).snd ≠ (D j).snd := by
    intro i j hi hj hij hs
    apply hij
    apply Function.iterate_injOn_Iio_minimalPeriod hi hj
    apply Dart.ext; apply Prod.ext
    · exact (Dfst i).trans (Dfst j).symm
    · exact hs
  have hbx : M.Adj b x := by
    have := (D β).adj; rw [Dfst, hb] at this; exact this.symm
  let loop : M.graph.Walk x x := .cons hxa (p.append hbx.toWalk)
  obtain ⟨c, hc⟩ := walkEdgeCoeff_is_face_sum loop
  -- edge coefficients of the loop at `x`
  have coef : ∀ j, j < P → walkEdgeCoeff loop (RotationSystem.edgeOfDart (D j)) =
      (if j = 0 then 1 else 0) + (if j = β then 1 else 0) := by
    intro j hj
    have hp0 : walkEdgeCoeff p (RotationSystem.edgeOfDart (D j)) = 0 :=
      walkEdgeCoeff_zero_of_not_mem_support p x hp _
        ((mem_edgeOfDart_iff (D j) x).2 (Or.inl (Dfst j)))
    simp only [loop, walkEdgeCoeff_cons, walkEdgeCoeff_append, hp0]
    have e1 : (RotationSystem.edgeOfDart (⟨(x, a), hxa⟩ : M.Dart) = RotationSystem.edgeOfDart (D j))
        ↔ j = 0 := by
      constructor
      · intro h
        rcases (RotationSystem.edge_of_dart_eq_iff _ _).1 h with h | h
        · by_contra hj0
          exact head_ne 0 j hPpos hj (Ne.symm hj0) (by
            have := congrArg (fun d : M.Dart => d.snd) h; exact this)
        · exfalso
          have := congrArg (fun d : M.Dart => d.fst) h
          change x = (D j).snd at this
          have h2 := (D j).adj
          rw [Dfst, ← this] at h2
          exact h2.ne rfl
      · rintro rfl; rfl
    have e2 : RotationSystem.edgeOfDart (⟨(b, x), hbx⟩ : M.Dart) =
        RotationSystem.edgeOfDart (D j) ↔ j = β := by
      constructor
      · intro h
        by_contra hjb
        rcases (RotationSystem.edge_of_dart_eq_iff _ _).1 h with h | h
        · have := congrArg (fun d : M.Dart => d.fst) h
          change b = (D j).fst at this
          have h2 := (D β).adj
          rw [Dfst, hb, this, Dfst] at h2
          exact h2.ne rfl
        · have := congrArg (fun d : M.Dart => d.fst) h
          change b = (D j).snd at this
          exact head_ne β j (by omega) hj (Ne.symm hjb) (hb.trans this)
      · intro h
        rw [h]
        apply (RotationSystem.edge_of_dart_eq_iff _ _).2
        right
        apply Dart.ext; apply Prod.ext
        · exact hb.symm
        · exact (Dfst β).symm
    simp only [Adj.toWalk, walkEdgeCoeff_cons, walkEdgeCoeff_nil, add_zero, zero_add]
    by_cases hj0 : j = 0 <;> by_cases hjb : j = β
    · exfalso; omega
    · rw [if_pos (e1.2 hj0), if_neg (fun h => hjb (e2.1 h)), if_pos hj0, if_neg hjb]
    · rw [if_neg (fun h => hj0 (e1.1 h)), if_pos (e2.2 hjb), if_neg hj0, if_pos hjb]
    · rw [if_neg (fun h => hj0 (e1.1 h)), if_neg (fun h => hjb (e2.1 h)), if_neg hj0, if_neg hjb]
  -- face values around `x`
  have step : ∀ j, j < P → c (M.faceOf (D (j + 1))) =
      c (M.faceOf (D j)) + walkEdgeCoeff loop (RotationSystem.edgeOfDart (D j)) := by
    intro j _
    have h1 : M.faceOf (D (j + 1)) = M.faceOf (D j).symm := by
      change M.faceOf ((⇑M.rotation.next)^[j + 1] D0) = _
      rw [Function.iterate_succ_apply']
      exact faceOf_next M (D j)
    rw [h1, hc, cycle_faceSum_edgeOfDart]
    rw [← add_assoc, zmod2_add_self, zero_add]
  have c0 : ∀ j, j < P → j ≠ 0 → j ≠ β →
      walkEdgeCoeff loop (RotationSystem.edgeOfDart (D j)) = 0 := by
    intro j hj h0 hb'; rw [coef j hj]; simp [h0, hb']
  have one_add : ∀ a : ZMod 2, a + 1 + 1 = a := by decide
  have val1 : ∀ j, 1 ≤ j → j ≤ β → c (M.faceOf (D j)) = c (M.faceOf (D 0)) + 1 := by
    intro j h1 hjb
    induction j with
    | zero => omega
    | succ j ih =>
      rw [step j (by omega)]
      rcases Nat.eq_zero_or_pos j with rfl | hj0
      · rw [coef 0 hPpos]; simp [show (0 : ℕ) ≠ β by omega]
      · rw [c0 j (by omega) (by omega) (by omega), add_zero, ih (by omega) (by omega)]
  have val2 : ∀ j, β < j → j ≤ ω → c (M.faceOf (D j)) = c (M.faceOf (D 0)) := by
    intro j h1 hjω
    induction j with
    | zero => omega
    | succ j ih =>
      rw [step j (by omega)]
      by_cases hjb : j = β
      · subst hjb
        rw [coef j (by omega), val1 j (by omega) le_rfl]
        simp [show j ≠ 0 by omega, one_add]
      · rw [c0 j (by omega) (by omega) hjb, add_zero, ih (by omega) (by omega)]
  have vμ := val1 μ hμ hμβ.le
  have vω := val2 ω hβω le_rfl
  -- along `q` the face value is constant
  have hloop : ∀ z ∈ q.support, z ∉ loop.support := by
    intro z hz hzl
    simp only [loop, Walk.support_cons, List.mem_cons, Walk.mem_support_append_iff,
      Adj.toWalk, Walk.support_nil, List.not_mem_nil, or_false] at hzl
    rcases hzl with rfl | hzp | rfl | rfl
    · exact hq hz
    · exact hdis z hz hzp
    · exact hdis _ hz (Walk.end_mem_support p)
    · exact hq hz
  have hu' : (D μ).symm.fst = u := hu
  have hw' : (D ω).symm.fst = w := hw
  have const := face_coeff_eq_along_disjoint_walk loop c hc q hloop (D μ).symm (D ω).symm hu' hw'
  have flip : ∀ j, j < P → j ≠ 0 → j ≠ β →
      c (M.faceOf (D j).symm) = c (M.faceOf (D j)) := by
    intro j hj h0 hb'
    have h := hc (RotationSystem.edgeOfDart (D j))
    rw [c0 j hj h0 hb', cycle_faceSum_edgeOfDart] at h
    exact (show ∀ a b : ZMod 2, 0 = a + b → b = a by decide) _ _ h
  rw [flip μ (by omega) (by omega) (by omega), flip ω hω (by omega) (by omega), vμ, vω] at const
  exact (show ∀ a : ZMod 2, a + 1 ≠ a by decide) _ const


/-! ## Jordan separation across a face -/

section FaceJordan
variable (M : SphericalMap n) (b0 : M.Dart)

/-- The boundary darts of the face of `b0`, in face order. -/
def bd (t : ℕ) : M.Dart := (⇑M.rotation.faceNext)^[t] b0

/-- The boundary vertices of the face of `b0`. -/
def rv (t : ℕ) : Fin n := (bd M b0 t).fst

theorem bd_succ (t : ℕ) : bd M b0 (t + 1) = M.rotation.faceNext (bd M b0 t) :=
  Function.iterate_succ_apply' _ _ _

theorem rv_succ (t : ℕ) : rv M b0 (t + 1) = (bd M b0 t).snd := by
  unfold rv; rw [bd_succ, RotationSystem.face_next_fst]

theorem face_bd (t : ℕ) : M.faceOf (bd M b0 t) = M.faceOf b0 :=
  M.rotation.face_of_iterate b0 t

theorem rv_adj (t : ℕ) : M.Adj (rv M b0 t) (rv M b0 (t + 1)) := by
  rw [rv_succ]; exact (bd M b0 t).adj

/-- The walk along the boundary from position `a` through `mm` steps. -/
def arcW (a : ℕ) : (mm : ℕ) → M.graph.Walk (rv M b0 a) (rv M b0 (a + mm))
  | 0 => Walk.nil
  | mm + 1 => (arcW a mm).concat (rv_adj M b0 (a + mm))

theorem walkEdgeCoeff_concat {u v w : Fin n} (p : M.graph.Walk u v) (h : M.Adj v w)
    (e : M.graph.edgeSet) :
    walkEdgeCoeff (p.concat h) e = walkEdgeCoeff p e +
      (if RotationSystem.edgeOfDart (⟨(v, w), h⟩ : M.Dart) = e then 1 else 0) := by
  rw [Walk.concat_eq_append, walkEdgeCoeff_append, walkEdgeCoeff_cons, walkEdgeCoeff_nil,
    add_zero]

theorem walkEdgeCoeff_reverse {u v : Fin n} (p : M.graph.Walk u v) (e : M.graph.edgeSet) :
    walkEdgeCoeff p.reverse e = walkEdgeCoeff p e := by
  classical
  simp [walkEdgeCoeff, Walk.edges_reverse, List.count_reverse]

end FaceJordan

/-- **Jordan separation across a face.** Let the face of `b0` have period `K` and distinct
boundary vertices `rv 0, …, rv (K-1)`. Disjoint walks joining the alternating boundary pairs
`rv i, rv (i+m)` and `rv j, rv l` (with `i < j < i+m < l < K`) cannot exist. -/
theorem face_alternating_walks_meet (M : SphericalMap n) (b0 : M.Dart) {K i m j l : ℕ}
    (hK : K = Function.minimalPeriod (⇑M.rotation.faceNext) b0)
    (hsimple : ∀ s t, s < K → t < K → rv M b0 s = rv M b0 t → s = t)
    (hij : i < j) (hjm : j < i + m) (hml : i + m < l) (hlK : l < K)
    (p : M.graph.Walk (rv M b0 i) (rv M b0 (i + m)))
    (q : M.graph.Walk (rv M b0 j) (rv M b0 l))
    (hdis : ∀ z ∈ q.support, z ∉ p.support) : False := by
  classical
  revert p q hdis
  set f := M.faceOf b0 with hf
  set B := bd M b0
  set R := rv M b0
  intro p q hdis
  have rsuccB : ∀ t, R (t + 1) = (B t).snd := fun t => rv_succ M b0 t
  have faceB : ∀ t, M.faceOf (B t) = f := fun t => face_bd M b0 t
  have bsucc : ∀ t, B (t + 1) = M.rotation.faceNext (B t) := fun t => bd_succ M b0 t
  have hKpos : 0 < K := by omega
  have per0 : (⇑M.rotation.faceNext)^[K] b0 = b0 := by rw [hK]; exact Function.iterate_minimalPeriod
  have bmod : ∀ t, B t = B (t % K) := by
    intro t
    change (⇑M.rotation.faceNext)^[t] b0 = (⇑M.rotation.faceNext)^[t % K] b0
    rw [hK, Function.iterate_mod_minimalPeriod_eq]
  have rmod : ∀ t, R t = R (t % K) := fun t => by
    change (B t).fst = (B (t % K)).fst; rw [bmod t]
  have rinj : ∀ s t, s < K → t < K → (R s = R t ↔ s = t) :=
    fun s t hs ht => ⟨hsimple s t hs ht, fun h => h ▸ rfl⟩
  have binj : ∀ s t, s < K → t < K → B s = B t → s = t := fun s t hs ht h =>
    hsimple s t hs ht (by change (B s).fst = (B t).fst; rw [h])
  -- the next position, reduced
  have rsucc : ∀ t, t < K → R (t + 1) = R ((t + 1) % K) := fun t _ => rmod (t + 1)
  -- a boundary dart is never the reverse of a boundary dart
  have no_double : ∀ s t, s < K → t < K → (B s).symm ≠ B t := by
    intro s t hs ht h
    have h1 : R t = R (s + 1) := by
      change (B t).fst = _; rw [← h, rsuccB]; rfl
    have h2 : R (t + 1) = R s := by
      rw [rsuccB]; change (B t).snd = (B s).fst; rw [← h]; rfl
    rw [rmod (s + 1)] at h1
    rw [rmod (t + 1)] at h2
    have e1 := (rinj _ _ ht (Nat.mod_lt _ hKpos)).1 h1
    have e2 := (rinj _ _ (Nat.mod_lt _ hKpos) hs).1 h2
    rcases Nat.lt_or_ge (s + 1) K with hs1 | hs1
    · rw [Nat.mod_eq_of_lt hs1] at e1
      subst e1
      rcases Nat.lt_or_ge (s + 1 + 1) K with hs2 | hs2
      · rw [Nat.mod_eq_of_lt hs2] at e2; omega
      · have : s + 1 + 1 = K := by omega
        rw [this, Nat.mod_self] at e2; omega
    · have : s + 1 = K := by omega
      rw [this, Nat.mod_self] at e1
      subst e1
      rw [Nat.mod_eq_of_lt (by omega : 0 + 1 < K)] at e2
      omega
  -- faces equal to `f` are boundary darts
  have face_char : ∀ d : M.Dart, M.faceOf d = f → ∃ t, t < K ∧ B t = d := by
    intro d hd
    have hr : M.rotation.FaceRelation b0 d :=
      ((M.rotation.face_of_eq_iff _ _).1 hd.symm)
    obtain ⟨k, hk⟩ := (M.rotation.face_relation_iff_iterate _ _).1 hr
    refine ⟨k % K, Nat.mod_lt _ hKpos, ?_⟩
    rw [← bmod]; exact hk
  -- boundary edges are distinct
  have edge_inj : ∀ s t, s < K → t < K →
      RotationSystem.edgeOfDart (B s) = RotationSystem.edgeOfDart (B t) → s = t := by
    intro s t hs ht h
    rcases (RotationSystem.edge_of_dart_eq_iff _ _).1 h with h | h
    · exact binj s t hs ht h
    · exact (no_double t s ht hs h.symm).elim
  -- the arc and the loop
  have arc_coef : ∀ mm, i + mm ≤ K → ∀ t, t < K →
      walkEdgeCoeff (arcW M b0 i mm) (RotationSystem.edgeOfDart (B t)) =
        if i ≤ t ∧ t < i + mm then 1 else 0 := by
    intro mm
    induction mm with
    | zero =>
      intro _ t _
      simp only [arcW, walkEdgeCoeff_nil]
      rw [if_neg (by omega)]
    | succ mm ih =>
      intro hmm t ht
      simp only [arcW]
      rw [walkEdgeCoeff_concat, ih (by omega) t ht]
      have hedge : ∀ h' : M.Adj (rv M b0 (i + mm)) (rv M b0 (i + (mm + 1))),
          RotationSystem.edgeOfDart (⟨(rv M b0 (i + mm), rv M b0 (i + (mm + 1))), h'⟩ : M.Dart) =
            RotationSystem.edgeOfDart (B (i + mm)) := fun h' => by
        congr 1; apply Dart.ext; apply Prod.ext
        · rfl
        · exact rsuccB (i + mm)
      rw [hedge]
      by_cases hti : t = i + mm
      · subst hti
        rw [if_pos rfl]
        have : ¬ (i ≤ i + mm ∧ i + mm < i + mm) := by omega
        rw [if_neg this, if_pos (by omega)]; rfl
      · have hne : RotationSystem.edgeOfDart (B (i + mm)) ≠ RotationSystem.edgeOfDart (B t) :=
          fun h => hti (edge_inj _ _ (by omega) ht h).symm
        rw [if_neg hne, add_zero]
        by_cases h1 : i ≤ t ∧ t < i + mm
        · rw [if_pos h1, if_pos (by omega)]
        · rw [if_neg h1, if_neg (by omega)]
  have arc_off : ∀ e : M.graph.edgeSet, (∀ t, t < K → RotationSystem.edgeOfDart (B t) ≠ e) →
      ∀ mm, walkEdgeCoeff (arcW M b0 i mm) e = 0 := by
    intro e he mm
    induction mm with
    | zero => simp [arcW]
    | succ mm ih =>
      simp only [arcW]
      rw [walkEdgeCoeff_concat, ih]
      have hedge : ∀ h' : M.Adj (rv M b0 (i + mm)) (rv M b0 (i + (mm + 1))),
          RotationSystem.edgeOfDart (⟨(rv M b0 (i + mm), rv M b0 (i + (mm + 1))), h'⟩ : M.Dart) =
            RotationSystem.edgeOfDart (B ((i + mm) % K)) := fun h' => by
        rw [← bmod]; congr 1; apply Dart.ext; apply Prod.ext
        · rfl
        · exact rsuccB (i + mm)
      rw [hedge, if_neg (he _ (Nat.mod_lt _ hKpos)), add_zero]
  let loop : M.graph.Walk (R i) (R i) := p.append (arcW M b0 i m).reverse
  obtain ⟨c, hc⟩ := walkEdgeCoeff_is_face_sum loop
  -- the arc indicator and the virtual value of a dart
  let inArc : M.Dart → Prop := fun d => ∃ t, t < K ∧ B t = d ∧ i ≤ t ∧ t < i + m
  let val : M.Dart → ZMod 2 := fun d =>
    if M.faceOf d = f then (if inArc d then 1 else 0) + c f else c (M.faceOf d)
  have inArc_B : ∀ t, t < K → (inArc (B t) ↔ i ≤ t ∧ t < i + m) := by
    intro t ht
    constructor
    · rintro ⟨s, hs, hst, h1, h2⟩
      have := binj s t hs ht hst; subst this; exact ⟨h1, h2⟩
    · intro h; exact ⟨t, ht, rfl, h⟩
  have val_B : ∀ t, t < K → val (B t) = (if i ≤ t ∧ t < i + m then 1 else 0) + c f := by
    intro t ht
    simp only [val, faceB t, ↓reduceIte]
    by_cases h : i ≤ t ∧ t < i + m
    · rw [if_pos ((inArc_B t ht).2 h), if_pos h]
    · rw [if_neg (fun h' => h ((inArc_B t ht).1 h')), if_neg h]
  -- the loop coefficient on an edge at a vertex off `p`
  have coefL : ∀ d : M.Dart, d.fst ∉ p.support →
      walkEdgeCoeff loop (RotationSystem.edgeOfDart d) =
        walkEdgeCoeff (arcW M b0 i m) (RotationSystem.edgeOfDart d) := by
    intro d hd
    simp only [loop, walkEdgeCoeff_append, walkEdgeCoeff_reverse]
    rw [walkEdgeCoeff_zero_of_not_mem_support p d.fst hd _
      ((mem_edgeOfDart_iff d _).2 (Or.inl rfl)), zero_add]
  have jump : ∀ d : M.Dart, d.fst ∉ p.support →
      c (M.faceOf d.symm) = c (M.faceOf d) +
        walkEdgeCoeff (arcW M b0 i m) (RotationSystem.edgeOfDart d) := by
    intro d hd
    have h := hc (RotationSystem.edgeOfDart d)
    rw [coefL d hd, cycle_faceSum_edgeOfDart] at h
    rw [h, ← add_assoc, zmod2_add_self, zero_add]
  -- edges that are not boundary edges carry no arc coefficient
  have off_edge : ∀ d : M.Dart, M.faceOf d ≠ f → M.faceOf d.symm ≠ f →
      walkEdgeCoeff (arcW M b0 i m) (RotationSystem.edgeOfDart d) = 0 := by
    intro d h1 h2
    apply arc_off _ _ m
    intro t ht he
    rcases (RotationSystem.edge_of_dart_eq_iff _ _).1 he with h | h
    · exact h1 (h ▸ faceB t)
    · exact h2 (h ▸ faceB t)
  have arc_le : i + m ≤ K := by omega
  have valF : ∀ d, M.faceOf d = f → val d = (if inArc d then 1 else 0) + c f :=
    fun d h => if_pos h
  have valN : ∀ d, M.faceOf d ≠ f → val d = c (M.faceOf d) := fun d h => if_neg h
  have ind : ∀ t, t < K → (if inArc (B t) then (1 : ZMod 2) else 0) =
      if i ≤ t ∧ t < i + m then 1 else 0 := by
    intro t ht
    by_cases h : i ≤ t ∧ t < i + m
    · rw [if_pos ((inArc_B t ht).2 h), if_pos h]
    · rw [if_neg (fun h' => h ((inArc_B t ht).1 h')), if_neg h]
  have z1 : ∀ a b : ZMod 2, b + a = a + b := fun a b => add_comm b a
  have z2 : ∀ a b : ZMod 2, a + (b + a) = b := by decide
  -- invariance across an edge
  have ES : ∀ d : M.Dart, d.fst ∉ p.support → val d.symm = val d := by
    intro d hd
    by_cases h1 : M.faceOf d = f
    · obtain ⟨t, ht, rfl⟩ := face_char d h1
      have h2 : M.faceOf (B t).symm ≠ f := by
        intro h2
        obtain ⟨s, hs, hsd⟩ := face_char _ h2
        exact no_double t s ht hs hsd.symm
      rw [valN _ h2, valF _ h1, ind t ht, jump _ hd, faceB, arc_coef m arc_le t ht, z1]
    · by_cases h2 : M.faceOf d.symm = f
      · obtain ⟨t, ht, hdt⟩ := face_char _ h2
        have hd' : d = (B t).symm := by rw [hdt, Dart.symm_symm]
        rw [valF _ h2, valN _ h1, ← hdt, ind t ht]
        have hj := jump _ hd
        rw [← hdt, faceB, hd', RotationSystem.edge_of_dart_symm, arc_coef m arc_le t ht] at hj
        rw [hd', hj, z2]
      · rw [valN _ h1, valN _ h2, jump _ hd, off_edge d h1 h2, add_zero]
  -- invariance under a rotation step at a vertex off `p`
  have VS : ∀ d : M.Dart, d.fst ∉ p.support → val (M.rotation.next d) = val d := by
    intro d hd
    have hface : M.faceOf (M.rotation.next d) = M.faceOf d.symm := faceOf_next M d
    by_cases h2 : M.faceOf d.symm = f
    · obtain ⟨s, hs, hsd⟩ := face_char _ h2
      have hd' : d = (B s).symm := by rw [hsd, Dart.symm_symm]
      have hnext : M.rotation.next d = B ((s + 1) % K) := by
        rw [← bmod, bsucc, hd', RotationSystem.face_next_apply]
      have h1 : M.faceOf d ≠ f := by
        intro h1
        obtain ⟨t, ht, hdt⟩ := face_char _ h1
        exact no_double s t hs ht (hd' ▸ hdt).symm
      have hj := jump _ hd
      rw [← hsd, faceB, hd', RotationSystem.edge_of_dart_symm, arc_coef m arc_le s hs] at hj
      rw [hnext, valF _ (faceB _), ind _ (Nat.mod_lt _ hKpos), valN _ h1, hd', hj]
      have hfst : d.fst = R (s + 1) := by rw [hd']; exact (rsuccB s).symm
      have ends : (s + 1) % K ≠ i ∧ (s + 1) % K ≠ i + m := by
        constructor
        · intro h; apply hd; rw [hfst, rmod (s + 1), h]; exact Walk.start_mem_support p
        · intro h; apply hd; rw [hfst, rmod (s + 1), h]; exact Walk.end_mem_support p
      have same : (i ≤ (s + 1) % K ∧ (s + 1) % K < i + m) ↔ (i ≤ s ∧ s < i + m) := by
        rcases Nat.lt_or_ge (s + 1) K with h | h
        · rw [Nat.mod_eq_of_lt h] at ends ⊢; omega
        · have : s + 1 = K := by omega
          rw [this, Nat.mod_self] at ends ⊢; omega
      by_cases hin : i ≤ s ∧ s < i + m
      · rw [if_pos (same.2 hin), if_pos hin, z2]
      · rw [if_neg (fun h => hin (same.1 h)), if_neg hin, z2]
    · by_cases h1 : M.faceOf d = f
      · obtain ⟨t, ht, hdt⟩ := face_char _ h1
        rw [valN _ (hface ▸ h2), hface, valF _ h1, ← hdt, ind t ht]
        have hj := jump _ (hdt ▸ hd)
        rw [faceB, arc_coef m arc_le t ht] at hj
        rw [hj, z1]
      · rw [valN _ (hface ▸ h2), hface, valN _ h1, jump _ hd, off_edge d h1 h2, add_zero]
  -- all darts at a vertex off `p` have the same value
  have at_vertex : ∀ (y : Fin n), y ∉ p.support → ∀ d e : M.Dart, d.fst = y → e.fst = y →
      val d = val e := by
    intro y hy d e hd he
    obtain ⟨k, hk⟩ := M.rotation.cyclic d e (hd.trans he.symm)
    rw [← hk]
    clear hk
    induction k with
    | zero => rfl
    | succ k ih =>
      rw [Function.iterate_succ_apply', VS _ (by rw [iterate_next_fst, hd]; exact hy), ih]
  -- along `q`
  have along : ∀ {y z : Fin n} (W : M.graph.Walk y z), (∀ v ∈ W.support, v ∉ p.support) →
      ∀ d e : M.Dart, d.fst = y → e.fst = z → val d = val e := by
    intro y z W
    induction W with
    | nil => intro hW d e hd he; exact at_vertex _ (hW _ (Walk.start_mem_support _)) d e hd he
    | @cons y y' z h W ih =>
      intro hW d e hd he
      have hy := hW y (Walk.start_mem_support _)
      have hW' : ∀ v ∈ W.support, v ∉ p.support := fun v hv =>
        hW v (by simp only [Walk.support_cons, List.mem_cons]; exact Or.inr hv)
      let a : M.Dart := ⟨(y, y'), h⟩
      rw [at_vertex y hy d a hd rfl, ← ES a hy]
      exact ih hW' a.symm e rfl he
  have hj := along q hdis (B j) (B l) rfl rfl
  rw [val_B j (by omega), val_B l hlK, if_pos ⟨hij.le, hjm⟩, if_neg (by omega)] at hj
  exact (show ∀ a : ZMod 2, 1 + a ≠ 0 + a by decide) _ hj

end SimpleGraph.SphericalMap
