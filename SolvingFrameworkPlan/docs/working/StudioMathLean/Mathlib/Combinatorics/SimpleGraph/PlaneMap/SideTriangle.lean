module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStar

/-!
# Sides of a separating triangle (link D of `R* ⇒ 4CT`)

D1. `subgraph_tracked`: every spanning subgraph `H` of a spherical map `M` carries a spherical
rotation in which the successor of a dart is the first `H`-dart along the rotation of `M`.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
variable {n : ℕ}

/-- `e` is reached from `d` by `k ≥ 1` rotation steps of `M`, all intermediate darts lying
outside `H`. -/
def RunTo (M : SphericalMap n) (H : SimpleGraph (Fin n)) (d e : M.Dart) : Prop :=
  ∃ k, 0 < k ∧ (⇑M.rotation.next)^[k] d = e ∧
    ∀ j, 0 < j → j < k → ¬ H.Adj ((⇑M.rotation.next)^[j] d).fst ((⇑M.rotation.next)^[j] d).snd

theorem RunTo.mono {M : SphericalMap n} {H H' : SimpleGraph (Fin n)} (hle : H ≤ H')
    {d e : M.Dart} (r : RunTo M H' d e) : RunTo M H d e := by
  obtain ⟨k, hk, he, hj⟩ := r
  exact ⟨k, hk, he, fun j h0 h1 hadj => hj j h0 h1 (hle hadj)⟩

theorem RunTo.trans {M : SphericalMap n} {H : SimpleGraph (Fin n)} {d e f : M.Dart}
    (r1 : RunTo M H d e) (he : ¬ H.Adj e.fst e.snd) (r2 : RunTo M H e f) : RunTo M H d f := by
  obtain ⟨k, hk, hde, hj⟩ := r1
  obtain ⟨l, hl, hef, hj'⟩ := r2
  refine ⟨l + k, by omega, by rw [Function.iterate_add_apply, hde, hef], ?_⟩
  intro j h0 h1
  rcases lt_trichotomy j k with hjk | hjk | hjk
  · exact hj j h0 hjk
  · subst hjk; rw [hde]; exact he
  · have : (⇑M.rotation.next)^[j] d = (⇑M.rotation.next)^[j - k] e := by
      rw [← hde, ← Function.iterate_add_apply]; congr 1; omega
    rw [this]; exact hj' (j - k) (by omega) (by omega)

theorem erasePoint_hit {α : Type*} (σ : Equiv.Perm α) (a z : α) (hz : σ z = a) :
    σ.erasePoint a z = σ a := by
  classical
  simp only [Equiv.Perm.erasePoint, Equiv.Perm.mul_apply, hz, Equiv.swap_apply_left]

theorem erasePoint_miss {α : Type*} (σ : Equiv.Perm α) (a z : α) (hz : z ≠ a)
    (hσ : σ z ≠ a) : σ.erasePoint a z = σ z := by
  classical
  have hne : σ z ≠ σ a := σ.injective.ne hz
  simp only [Equiv.Perm.erasePoint, Equiv.Perm.mul_apply]
  exact Equiv.swap_apply_of_ne_of_ne hσ hne

/-- One erased edge: the new successor is one or two old steps on, skipping only the erased
darts. -/
theorem eraseEdge_runTo (M : SphericalMap n) (a : M.Dart) (x : (M.eraseEdge a).Dart) :
    RunTo M (RotationSystem.eraseGraph a) (RotationSystem.eraseDart a x)
      (RotationSystem.eraseDart a ((M.eraseEdge a).rotation.next x)) := by
  classical
  set σ := M.rotation.next with hσ
  set y := RotationSystem.eraseDart a x with hy
  have hya : y ≠ a ∧ y ≠ a.symm := ((RotationSystem.eraseDartEquiv a) x).property
  have hnext : RotationSystem.eraseDart a ((M.eraseEdge a).rotation.next x) =
      M.rotation.eraseNext a y := RotationSystem.eraseRotation_next _ _ _
  rw [hnext]
  have hfst : a.fst ≠ a.snd := a.adj.ne
  have hσa' : σ a.symm ≠ a := fun e => hfst (by
    have := congrArg (fun d : M.Dart => d.fst) e
    simp only [σ, M.rotation.next_fst] at this; exact this.symm)
  have hσaa' : σ a ≠ a.symm := fun e => hfst (by
    have := congrArg (fun d : M.Dart => d.fst) e
    simp only [σ, M.rotation.next_fst] at this; exact this)
  have hdist : a ≠ a.symm := RotationSystem.dart_ne_symm a
  have not_a : ¬ (RotationSystem.eraseGraph a).Adj a.fst a.snd := fun h => h.2 rfl
  have not_a' : ¬ (RotationSystem.eraseGraph a).Adj a.symm.fst a.symm.snd := fun h =>
    h.2 (Sym2.eq_swap)
  have h1a' : (σ.erasePoint a) a.symm = σ a.symm :=
    erasePoint_miss _ _ _ hdist.symm hσa'
  change RunTo M _ y (((σ.erasePoint a).erasePoint a.symm) y)
  by_cases e1 : σ y = a
  · have s1 : σ.erasePoint a y = σ a := erasePoint_hit _ _ _ e1
    have s2 : (σ.erasePoint a).erasePoint a.symm y = σ a := by
      rw [erasePoint_miss _ _ _ hya.2 (by rw [s1]; exact hσaa'), s1]
    rw [s2]
    refine ⟨2, by norm_num, by rw [Function.iterate_succ_apply', Function.iterate_one, e1], ?_⟩
    intro j h0 h1
    obtain rfl : j = 1 := by omega
    rw [Function.iterate_one, e1]; exact not_a
  · have s1 : σ.erasePoint a y = σ y := erasePoint_miss _ _ _ hya.1 e1
    by_cases e2 : σ y = a.symm
    · have s2 : (σ.erasePoint a).erasePoint a.symm y = σ a.symm := by
        rw [erasePoint_hit _ _ _ (by rw [s1]; exact e2), h1a']
      rw [s2]
      refine ⟨2, by norm_num, by rw [Function.iterate_succ_apply', Function.iterate_one, e2], ?_⟩
      intro j h0 h1
      obtain rfl : j = 1 := by omega
      rw [Function.iterate_one, e2]; exact not_a'
    · have s2 : (σ.erasePoint a).erasePoint a.symm y = σ y := by
        rw [erasePoint_miss _ _ _ hya.2 (by rw [s1]; exact e2), s1]
      rw [s2]
      exact ⟨1, by norm_num, by rw [Function.iterate_one], fun j h0 h1 => by omega⟩

/-- A dart of a spanning subgraph, viewed in the ambient map. -/
def liftDart {M : SphericalMap n} {G : SimpleGraph (Fin n)} (hle : G ≤ M.graph)
    (d : G.Dart) : M.Dart := ⟨d.toProd, hle d.adj⟩

/-- Runs of the erased map are runs of the original map. -/
theorem runTo_eraseEdge (M : SphericalMap n) (a : M.Dart) {H : SimpleGraph (Fin n)}
    (hH : H ≤ RotationSystem.eraseGraph a) (x : (M.eraseEdge a).Dart) :
    ∀ m, 0 < m →
      (∀ j, 0 < j → j < m → ¬ H.Adj ((⇑(M.eraseEdge a).rotation.next)^[j] x).fst
        ((⇑(M.eraseEdge a).rotation.next)^[j] x).snd) →
      RunTo M H (RotationSystem.eraseDart a x)
        (RotationSystem.eraseDart a ((⇑(M.eraseEdge a).rotation.next)^[m] x)) := by
  intro m
  induction m with
  | zero => intro h; omega
  | succ m ih =>
    intro _ hj
    rcases Nat.eq_zero_or_pos m with rfl | hm
    · simpa using (eraseEdge_runTo M a x).mono hH
    · have r1 := ih hm (fun j h0 h1 => hj j h0 (by omega))
      have r2 := (eraseEdge_runTo M a ((⇑(M.eraseEdge a).rotation.next)^[m] x)).mono hH
      rw [← Function.iterate_succ_apply' (⇑(M.eraseEdge a).rotation.next)] at r2
      exact r1.trans (hj m hm (by omega)) r2

/-- **D1.** Every spanning subgraph carries a spherical rotation whose successor is the first
subgraph dart along the ambient rotation. -/
theorem subgraph_tracked (M : SphericalMap n) (H : SimpleGraph (Fin n)) (hsub : H ≤ M.graph) :
    ∃ N : SphericalMap n, N.graph = H ∧ ∃ hle : N.graph ≤ M.graph,
      ∀ d : N.Dart, RunTo M H (liftDart hle d) (liftDart hle (N.rotation.next d)) := by
  classical
  generalize hk : Fintype.card M.graph.edgeSet = k
  induction k using Nat.strong_induction_on generalizing M H with
  | h k ih =>
    by_cases heq : M.graph = H
    · refine ⟨M, heq, le_rfl, fun d => ⟨1, by norm_num, by rw [Function.iterate_one]; rfl,
        fun j h0 h1 => by omega⟩⟩
    · have hex : ∃ u v, M.Adj u v ∧ ¬ H.Adj u v := by
        by_contra hh
        push Not at hh
        exact heq (le_antisymm (fun u v huv => hh u v huv) hsub)
      obtain ⟨u, v, huv, hnot⟩ := hex
      let a : M.Dart := ⟨(u, v), huv⟩
      let N' := M.eraseEdge a
      have hcount : Fintype.card N'.graph.edgeSet < k := by
        have hh := Fintype.card_congr (RotationSystem.eraseEdgeTotalEquiv a)
        simp only [Fintype.card_sum, Fintype.card_unit] at hh
        change Fintype.card N'.graph.edgeSet + 1 = Fintype.card M.graph.edgeSet at hh
        omega
      have hsub' : H ≤ N'.graph := by
        intro x y hxy
        refine ⟨hsub hxy, ?_⟩
        intro he
        have hemem : s(x, y) ∈ H.edgeSet := hxy
        rw [he] at hemem
        exact hnot hemem
      obtain ⟨N, hN, hle', spec⟩ := ih _ hcount N' H hsub' rfl
      have hle : N.graph ≤ M.graph := fun x y h => (hle' h).1
      refine ⟨N, hN, hle, fun d => ?_⟩
      obtain ⟨m, hm, hmd, hj⟩ := spec d
      have r := runTo_eraseEdge M a hsub' (liftDart hle' d) m hm hj
      rw [hmd] at r
      exact r

/-! ## D2. The two sides of a non-facial triangle -/

section Sides
open RotationSystem

/-- `p q r` bound a face (on one of the two sides of the edge `pq`). -/
def Facial (T : SphericalMap n) (p q r : Fin n) : Prop := Nx T q p r ∨ Nx T p q r

/-- The indicator of the three edges of the triangle `p q r`. -/
noncomputable def triInd (T : SphericalMap n) (p q r : Fin n) : T.graph.edgeSet → ZMod 2 := by
  classical
  exact fun e => (if e.val = s(p,q) then 1 else 0) + (if e.val = s(q,r) then 1 else 0) +
    (if e.val = s(r,p) then 1 else 0)

theorem incidence_single (T : SphericalMap n) {u v : Fin n} (huv : T.Adj u v) (x : Fin n) :
    (∑ e : T.graph.edgeSet,
      if x ∈ e.val then (if e.val = s(u,v) then (1 : ZMod 2) else 0) else 0) =
      if x = u ∨ x = v then 1 else 0 := by
  classical
  let e0 : T.graph.edgeSet := ⟨s(u,v), huv⟩
  have h : ∀ e : T.graph.edgeSet,
      (if x ∈ e.val then (if e.val = s(u,v) then (1 : ZMod 2) else 0) else 0) =
        if e = e0 then (if x = u ∨ x = v then 1 else 0) else 0 := by
    intro e
    by_cases he : e = e0
    · subst he; simp [e0, Sym2.mem_iff]
    · have : e.val ≠ s(u,v) := fun h => he (Subtype.ext h)
      simp [he, this]
  rw [Finset.sum_congr rfl (fun e _ => h e), Finset.sum_ite_eq' Finset.univ e0]
  simp

theorem triInd_even (T : SphericalMap n) {p q r : Fin n} (hpq : T.Adj p q) (hqr : T.Adj q r)
    (hrp : T.Adj r p) : IsEven T (triInd T p q r) := by
  classical
  intro x
  change ∑ e : T.graph.edgeSet, (if x ∈ e.val then triInd T p q r e else 0) = 0
  have split : ∀ e : T.graph.edgeSet, (if x ∈ e.val then triInd T p q r e else 0) =
      (if x ∈ e.val then (if e.val = s(p,q) then (1 : ZMod 2) else 0) else 0) +
      (if x ∈ e.val then (if e.val = s(q,r) then (1 : ZMod 2) else 0) else 0) +
      (if x ∈ e.val then (if e.val = s(r,p) then (1 : ZMod 2) else 0) else 0) := by
    intro e; unfold triInd; split_ifs <;> simp
  rw [Finset.sum_congr rfl (fun e _ => split e), Finset.sum_add_distrib, Finset.sum_add_distrib,
    incidence_single T hpq, incidence_single T hqr, incidence_single T hrp]
  have h1 := hpq.ne; have h2 := hqr.ne; have h3 := hrp.ne
  by_cases xp : x = p
  · subst xp; simp [h1, h3.symm]; decide
  · by_cases xq : x = q
    · subst xq; simp [xp, h2]; decide
    · by_cases xr : x = r
      · subst xr; simp [xp, xq]; decide
      · simp [xp, xq, xr]

/-- A face potential of the triangle: across every edge the potential jumps exactly on the
triangle's edges. -/
def TriPotential (T : SphericalMap n) (p q r : Fin n) (c : T.Face → ZMod 2) : Prop :=
  ∀ d : T.Dart, triInd T p q r (edgeOfDart d) = c (T.faceOf d) + c (T.faceOf d.symm)

theorem exists_triPotential (T : SphericalMap n) {p q r : Fin n} (hpq : T.Adj p q)
    (hqr : T.Adj q r) (hrp : T.Adj r p) : ∃ c, TriPotential T p q r c :=
  T.fills _ (triInd_even T hpq hqr hrp)

theorem faceOf_next (T : SphericalMap n) (d : T.Dart) :
    T.faceOf (T.rotation.next d) = T.faceOf d.symm := by
  have := T.rotation.face_of_face_next d.symm
  simp only [RotationSystem.face_next_apply, Dart.symm_symm] at this
  exact this

/-- Vertices off the triangle: the triangle indicator vanishes on their darts. -/
theorem triInd_off (T : SphericalMap n) {p q r : Fin n} (d : T.Dart)
    (hx : d.fst ≠ p ∧ d.fst ≠ q ∧ d.fst ≠ r) : triInd T p q r (edgeOfDart d) = 0 := by
  classical
  have m : d.fst ∈ (edgeOfDart d).val := Sym2.mem_mk_left _ _
  have n1 : (edgeOfDart d).val ≠ s(p,q) := fun h => by
    rw [h, Sym2.mem_iff] at m; rcases m with m | m; exact hx.1 m; exact hx.2.1 m
  have n2 : (edgeOfDart d).val ≠ s(q,r) := fun h => by
    rw [h, Sym2.mem_iff] at m; rcases m with m | m; exact hx.2.1 m; exact hx.2.2 m
  have n3 : (edgeOfDart d).val ≠ s(r,p) := fun h => by
    rw [h, Sym2.mem_iff] at m; rcases m with m | m; exact hx.2.2 m; exact hx.1 m
  simp [triInd, n1, n2, n3]

lemma zmod2_swap : ∀ a b t : ZMod 2, t = a + b → b = t + a := by decide

theorem iterate_next_fst (T : SphericalMap n) (k : ℕ) (d : T.Dart) :
    ((⇑T.rotation.next)^[k] d).fst = d.fst := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply', T.rotation.next_fst, ih]

/-- The potential is constant around a vertex off the triangle. -/
theorem side_const (T : SphericalMap n) {p q r : Fin n} {c : T.Face → ZMod 2}
    (hc : TriPotential T p q r c) {x : Fin n} (hx : x ≠ p ∧ x ≠ q ∧ x ≠ r)
    (d e : T.Dart) (hd : d.fst = x) (he : e.fst = x) :
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
    have h0 := triInd_off T y (by rw [hy]; exact hx)
    have := zmod2_swap _ _ _ (hc y)
    rw [h0, zero_add] at this
    rw [this, ih]

/-- Every dart from `x` sees the potential value `b`. -/
def OnSide (T : SphericalMap n) (c : T.Face → ZMod 2) (b : ZMod 2) (x : Fin n) : Prop :=
  ∀ d : T.Dart, d.fst = x → c (T.faceOf d) = b

theorem onSide_of_dart (T : SphericalMap n) {p q r : Fin n} {c : T.Face → ZMod 2}
    (hc : TriPotential T p q r c) {x : Fin n} (hx : x ≠ p ∧ x ≠ q ∧ x ≠ r) (d : T.Dart)
    (hd : d.fst = x) : OnSide T c (c (T.faceOf d)) x :=
  fun e he => (side_const T hc hx d e hd he).symm

/-- No edge joins the two sides off the triangle. -/
theorem onSide_adj (T : SphericalMap n) {p q r : Fin n} {c : T.Face → ZMod 2}
    (hc : TriPotential T p q r c) {x y : Fin n} (hx : x ≠ p ∧ x ≠ q ∧ x ≠ r)
    (hy : y ≠ p ∧ y ≠ q ∧ y ≠ r) (hxy : T.Adj x y) {b : ZMod 2} (h : OnSide T c b x) :
    OnSide T c b y := by
  let d : T.Dart := ⟨(x, y), hxy⟩
  have h0 := triInd_off T d hx
  have := zmod2_swap _ _ _ (hc d)
  rw [h0, zero_add, h d rfl] at this
  have hs := onSide_of_dart T hc hy d.symm rfl
  rwa [this] at hs

/-- A non-facial triangle has vertices off it on both sides. -/
theorem exists_onSide (T : SphericalMap n) (htri : T.Triangulated) {p q r : Fin n}
    (hpq : T.Adj p q) (hqr : T.Adj q r) (hrp : T.Adj r p) (hnf : ¬ Facial T p q r)
    {c : T.Face → ZMod 2} (hc : TriPotential T p q r c) (b : ZMod 2) :
    ∃ z, (z ≠ p ∧ z ≠ q ∧ z ≠ r) ∧ OnSide T c b z := by
  classical
  have h1 := hpq.ne; have h2 := hqr.ne; have h3 := hrp.ne
  let d0 : T.Dart := ⟨(p, q), hpq⟩
  have hjump : c (T.faceOf d0) + c (T.faceOf d0.symm) = 1 := by
    rw [← hc d0]
    have n2 : s(p,q) ≠ s(q,r) := fun h => by
      rw [Sym2.eq_iff] at h; rcases h with h | h; exact h1 h.1; exact h3 h.1.symm
    have n3 : s(p,q) ≠ s(r,p) := fun h => by
      rw [Sym2.eq_iff] at h; rcases h with h | h; exact h3 h.1.symm; exact h2 h.2
    simp [triInd, d0, edgeOfDart, Dart.edge, n2, n3]
  -- the face of a dart `u → v` of the triangle has its third vertex off the triangle
  have third : ∀ (u v : Fin n) (huv : T.Adj u v),
      (u = p ∧ v = q ∨ u = q ∧ v = p) →
      ∃ z, (z ≠ p ∧ z ≠ q ∧ z ≠ r) ∧ OnSide T c (c (T.faceOf ⟨(u,v),huv⟩)) z := by
    intro u v huv huv'
    let z := (T.rotation.next ⟨(v,u),huv.symm⟩).snd
    have hN : Nx T v u z := ⟨huv.symm, rfl⟩
    obtain ⟨hzv, hzu⟩ := nx_tri htri hN
    have hzr : z ≠ r := by
      intro e; apply hnf
      rcases huv' with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact Or.inl (e ▸ hN)
      · exact Or.inr (e ▸ hN)
    have hzne_v : z ≠ v := (nx_adj_right hN).ne.symm
    have hzne_u : z ≠ u := (nx_adj_right hzv).ne
    have hz : z ≠ p ∧ z ≠ q ∧ z ≠ r := by
      rcases huv' with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact ⟨hzne_u, hzne_v, hzr⟩
      · exact ⟨hzne_v, hzne_u, hzr⟩
    obtain ⟨_, hvz, e1⟩ := nx_dart hN
    obtain ⟨_, hzu', e2⟩ := nx_dart hzv
    have hface : T.faceOf ⟨(z,u),hzu'⟩ = T.faceOf ⟨(u,v),huv⟩ := by
      have f1 := T.rotation.face_of_face_next (⟨(u,v),huv⟩ : T.Dart)
      have f2 := T.rotation.face_of_face_next (⟨(v,z),hvz⟩ : T.Dart)
      simp only [RotationSystem.face_next_apply] at f1 f2
      change T.rotation.faceOf (T.rotation.next ⟨(v,u),huv.symm⟩) = _ at f1
      change T.rotation.faceOf (T.rotation.next ⟨(z,v),hvz.symm⟩) = _ at f2
      rw [e1] at f1; rw [e2] at f2
      exact f2.trans f1
    refine ⟨z, hz, ?_⟩
    have := onSide_of_dart T hc hz ⟨(z,u),hzu'⟩ rfl
    rwa [hface] at this
  have two : ∀ a : ZMod 2, a = b ∨ a + 1 = b := by
    intro a; revert a b; decide
  rcases two (c (T.faceOf d0)) with e | e
  · obtain ⟨z, hz, hs⟩ := third p q hpq (Or.inl ⟨rfl, rfl⟩)
    exact ⟨z, hz, e ▸ hs⟩
  · obtain ⟨z, hz, hs⟩ := third q p hpq.symm (Or.inr ⟨rfl, rfl⟩)
    refine ⟨z, hz, ?_⟩
    have : c (T.faceOf ⟨(q,p),hpq.symm⟩) = b := by
      have hj : c (T.faceOf d0.symm) = 1 + c (T.faceOf d0) := by
        have := zmod2_swap _ _ _ hjump.symm; exact this
      change c (T.faceOf d0.symm) = b
      rw [hj, ← e]; ring
    rwa [this] at hs

end Sides

end SimpleGraph.SphericalMap
