module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStar
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyCliqueLift

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
    ∃ z, (z ≠ p ∧ z ≠ q ∧ z ≠ r) ∧ (∃ y, T.Adj z y) ∧ OnSide T c b z := by
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
      ∃ z, (z ≠ p ∧ z ≠ q ∧ z ≠ r) ∧ (∃ y, T.Adj z y) ∧
        OnSide T c (c (T.faceOf ⟨(u,v),huv⟩)) z := by
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
    refine ⟨z, hz, ⟨u, hzu'⟩, ?_⟩
    have := onSide_of_dart T hc hz ⟨(z,u),hzu'⟩ rfl
    rwa [hface] at this
  have two : ∀ a : ZMod 2, a = b ∨ a + 1 = b := by
    intro a; revert a b; decide
  rcases two (c (T.faceOf d0)) with e | e
  · obtain ⟨z, hz, hy, hs⟩ := third p q hpq (Or.inl ⟨rfl, rfl⟩)
    exact ⟨z, hz, hy, e ▸ hs⟩
  · obtain ⟨z, hz, hy, hs⟩ := third q p hpq.symm (Or.inr ⟨rfl, rfl⟩)
    refine ⟨z, hz, hy, ?_⟩
    have : c (T.faceOf ⟨(q,p),hpq.symm⟩) = b := by
      have hj : c (T.faceOf d0.symm) = 1 + c (T.faceOf d0) := by
        have := zmod2_swap _ _ _ hjump.symm; exact this
      change c (T.faceOf d0.symm) = b
      rw [hj, ← e]; ring
    rwa [this] at hs

end Sides

/-! ## D3. The kept side as a spherical map -/

section Kept
open RotationSystem VacancyCliqueLift

/-- The triangle's vertices together with every vertex whose darts all see potential `b`. -/
def keep (T : SphericalMap n) (c : T.Face → ZMod 2) (b : ZMod 2) (p q r : Fin n) :
    Set (Fin n) := {x | x = p ∨ x = q ∨ x = r ∨ OnSide T c b x}

theorem runTo_first {M : SphericalMap n} {H : SimpleGraph (Fin n)} {d e : M.Dart}
    (h : RunTo M H d e) (hn : H.Adj (M.rotation.next d).fst (M.rotation.next d).snd) :
    e = M.rotation.next d := by
  obtain ⟨k, hk, hke, hj⟩ := h
  rcases Nat.lt_or_ge 1 k with h1 | h1
  · exact absurd (by simpa using hn) (hj 1 (by norm_num) h1)
  · obtain rfl : k = 1 := by omega
    simpa using hke.symm

variable {T : SphericalMap n} {p q r : Fin n} {c : T.Face → ZMod 2} {b : ZMod 2}

theorem keep_of_face (hc : TriPotential T p q r c) (d : T.Dart) (hd : c (T.faceOf d) = b) :
    d.fst ∈ keep T c b p q r := by
  by_cases hx : d.fst ≠ p ∧ d.fst ≠ q ∧ d.fst ≠ r
  · have := onSide_of_dart T hc hx d rfl
    rw [hd] at this
    exact Or.inr (Or.inr (Or.inr this))
  · simp only [not_and_or, not_not] at hx
    rcases hx with h | h | h
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
    · exact Or.inr (Or.inr (Or.inl h))

theorem faceNext_face (d : T.Dart) : T.faceOf (T.rotation.faceNext d) = T.faceOf d :=
  T.rotation.face_of_face_next d

/-- The second end of a dart lies on its face. -/
theorem snd_keep_of_face (hc : TriPotential T p q r c) (d : T.Dart) (hd : c (T.faceOf d) = b) :
    d.snd ∈ keep T c b p q r := by
  have := keep_of_face (b := b) hc (T.rotation.faceNext d) (by rw [faceNext_face]; exact hd)
  rwa [RotationSystem.face_next_fst] at this

theorem offF_not_keep {z : Fin n} (hz : z ≠ p ∧ z ≠ q ∧ z ≠ r)
    (e : T.Dart) (he : e.fst = z) (hb : c (T.faceOf e) ≠ b) : z ∉ keep T c b p q r := by
  rintro (h | h | h | h)
  · exact hz.1 h
  · exact hz.2.1 h
  · exact hz.2.2 h
  · exact hb (h e he)

theorem inF_keep {x : Fin n} (hx : x = p ∨ x = q ∨ x = r) : x ∈ keep T c b p q r := by
  rcases hx with h | h | h
  · exact Or.inl h
  · exact Or.inr (Or.inl h)
  · exact Or.inr (Or.inr (Or.inl h))


theorem liftDart_injective {M : SphericalMap n} {G : SimpleGraph (Fin n)} (hle : G ≤ M.graph) :
    Function.Injective (liftDart (M := M) hle) := by
  intro a b h
  apply Dart.ext
  exact congrArg (fun d : M.Dart => d.toProd) h

theorem third_corner {p q r u v : Fin n} (hpq : p ≠ q) (hqr : q ≠ r) (hrp : r ≠ p)
    (hu : u = p ∨ u = q ∨ u = r) (hv : v = p ∨ v = q ∨ v = r) (huv : u ≠ v) :
    ∃ w, (w = p ∨ w = q ∨ w = r) ∧ w ≠ u ∧ w ≠ v ∧
      ∀ z, (z = p ∨ z = q ∨ z = r) → z = u ∨ z = v ∨ z = w := by
  rcases hu with rfl | rfl | rfl <;> rcases hv with rfl | rfl | rfl
  all_goals first
    | exact absurd rfl huv
    | exact ⟨r, by simp, by tauto, by tauto, by tauto⟩
    | exact ⟨q, by simp, by tauto, by tauto, by tauto⟩
    | exact ⟨p, by simp, by tauto, by tauto, by tauto⟩

theorem adj_corners {T : SphericalMap n} {p q r x y : Fin n} (hpq : T.Adj p q) (hqr : T.Adj q r)
    (hrp : T.Adj r p) (hx : x = p ∨ x = q ∨ x = r) (hy : y = p ∨ y = q ∨ y = r) (hxy : x ≠ y) :
    T.Adj x y := by
  rcases hx with rfl | rfl | rfl <;> rcases hy with rfl | rfl | rfl
  all_goals first
    | exact absurd rfl hxy
    | assumption
    | exact SimpleGraph.Adj.symm (by assumption)

section Map
variable (hc : TriPotential T p q r c) {N : SphericalMap n}
  (hN : N.graph = sideGraph T.graph (keep T c b p q r)) (hle : N.graph ≤ T.graph)
  (spec : ∀ d : N.Dart, RunTo T (sideGraph T.graph (keep T c b p q r)) (liftDart hle d)
    (liftDart hle (N.rotation.next d)))
include hc hN spec

/-- **LA.** On a kept face the new face successor is the old one. -/
theorem lift_faceNext_keptFace (d : N.Dart) (hd : c (T.faceOf (liftDart hle d)) = b) :
    liftDart hle (N.rotation.faceNext d) = T.rotation.faceNext (liftDart hle d) := by
  rw [RotationSystem.face_next_apply, RotationSystem.face_next_apply]
  have r := spec d.symm
  apply runTo_first r
  have h1 := snd_keep_of_face hc (liftDart hle d) hd
  have hf : c (T.faceOf (T.rotation.faceNext (liftDart hle d))) = b := by
    rw [faceNext_face]; exact hd
  have h2 := snd_keep_of_face hc _ hf
  rw [RotationSystem.face_next_apply] at h2 hf
  refine ⟨(T.rotation.next (liftDart hle d.symm)).adj, ?_, h2⟩
  rw [T.rotation.next_fst]
  exact h1

/-- On a kept face the potential is unchanged by the new face successor. -/
theorem keptFace_faceNext (d : N.Dart) (hd : c (T.faceOf (liftDart hle d)) = b) :
    c (T.faceOf (liftDart hle (N.rotation.faceNext d))) = b := by
  rw [lift_faceNext_keptFace hc hN hle spec d hd, faceNext_face]; exact hd

/-- **LB.** At a corner `v` of the triangle, starting from a triangle dart whose face lies on the
far side, the new successor skips the far side and lands on the third corner `w`. -/
theorem lift_next_farFace (d : N.Dart) {u v w : Fin n}
    (hdu : (liftDart hle d).fst = u) (hdv : (liftDart hle d).snd = v)
    (hu : u = p ∨ u = q ∨ u = r) (hv : v = p ∨ v = q ∨ v = r) (hw : w = p ∨ w = q ∨ w = r)
    (hwu : w ≠ u) (hvwAdj : T.Adj v w)
    (hcov : ∀ z, (z = p ∨ z = q ∨ z = r) → z = u ∨ z = v ∨ z = w)
    (hd : c (T.faceOf (liftDart hle d)) ≠ b) :
    (liftDart hle (N.rotation.next d.symm)).snd = w ∧
      c (T.faceOf (liftDart hle (N.rotation.next d.symm))) ≠ b := by
  classical
  set H := sideGraph T.graph (keep T c b p q r) with hH
  set y0 := liftDart hle d.symm with hy0
  have hy0fst : y0.fst = v := hdv
  have hy0snd : y0.snd = u := hdu
  obtain ⟨k, hk, hke, hj⟩ := spec d.symm
  set Y : ℕ → T.Dart := fun j => (⇑T.rotation.next)^[j] y0 with hY
  have Yfst : ∀ j, (Y j).fst = v := fun j => (iterate_next_fst T j y0).trans hy0fst
  have hvK : v ∈ keep T c b p q r := inF_keep hv
  -- the potential stays on the far side along the run
  have C : ∀ j, 1 ≤ j → j ≤ k → c (T.faceOf (Y j)) ≠ b := by
    intro j
    induction j with
    | zero => intro h; omega
    | succ j ih =>
      intro _ hjk
      rcases Nat.eq_zero_or_pos j with rfl | hj0
      · change c (T.faceOf (T.rotation.next y0)) ≠ b
        rw [faceOf_next]; exact hd
      · have hnot := hj j hj0 (by omega)
        have hsnd : (Y j).snd ∉ keep T c b p q r := fun hs =>
          hnot ⟨(Y j).adj, by rw [Yfst]; exact hvK, hs⟩
        have hoff : (Y j).snd ≠ p ∧ (Y j).snd ≠ q ∧ (Y j).snd ≠ r := by
          refine ⟨fun e => hsnd (inF_keep (Or.inl e)), fun e => hsnd (inF_keep (Or.inr (Or.inl e))),
            fun e => hsnd (inF_keep (Or.inr (Or.inr e)))⟩
        have h0 : triInd T p q r (edgeOfDart (Y j)) = 0 := by
          rw [← edge_of_dart_symm]; exact triInd_off T _ hoff
        have := zmod2_swap _ _ _ (hc (Y j))
        rw [h0, zero_add] at this
        rw [show Y (j + 1) = T.rotation.next (Y j) from Function.iterate_succ_apply' _ _ _,
          faceOf_next, this]
        exact ih (by omega) (by omega)
  have Ck := C k hk le_rfl
  have hYk : Y k = liftDart hle (N.rotation.next d.symm) := hke
  refine ⟨?_, hYk ▸ Ck⟩
  -- the end of the run is a kept dart
  have hadj : H.Adj (Y k).fst (Y k).snd := by
    rw [hYk]
    exact hN.le (N.rotation.next d.symm).adj
  have hzK := hadj.2.2
  set z := (Y k).snd with hz
  have hzF : z = p ∨ z = q ∨ z = r := by
    by_contra hoff
    simp only [not_or] at hoff
    have hoff' : z ≠ p ∧ z ≠ q ∧ z ≠ r := hoff
    have hon : OnSide T c b z := by
      rcases hzK with h | h | h | h
      · exact absurd h hoff'.1
      · exact absurd h hoff'.2.1
      · exact absurd h hoff'.2.2
      · exact h
    have := hon (T.rotation.faceNext (Y k)) (RotationSystem.face_next_fst _ _)
    rw [faceNext_face] at this
    exact Ck this
  rcases hcov z hzF with hzu | hzv | hzw
  · -- back at `u`: then the run passed `v → w`, a kept dart
    exfalso
    have hback : Y k = y0 := by
      apply Dart.ext; apply Prod.ext
      · rw [Yfst, hy0fst]
      · rw [← hz, hzu, hy0snd]
    have hper : Function.IsPeriodicPt (⇑T.rotation.next) k y0 := hback
    let dw : T.Dart := ⟨(v, w), hvwAdj⟩
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
    exact ⟨hvwAdj, hvK, inF_keep hw⟩
  · exfalso
    have := (Y k).adj
    rw [Yfst] at this
    exact this.ne (hzv.symm.trans hz)
  · rw [← hYk]; exact hzw

/-- Darts of the kept map on a far face join two corners. -/
theorem far_ends (d : N.Dart) (hd : c (T.faceOf (liftDart hle d)) ≠ b) :
    ((liftDart hle d).fst = p ∨ (liftDart hle d).fst = q ∨ (liftDart hle d).fst = r) ∧
    ((liftDart hle d).snd = p ∨ (liftDart hle d).snd = q ∨ (liftDart hle d).snd = r) := by
  have hadj := hN.le d.adj
  have corner : ∀ (x : Fin n), x ∈ keep T c b p q r → (e : T.Dart) → e.fst = x →
      c (T.faceOf e) ≠ b → (x = p ∨ x = q ∨ x = r) := by
    intro x hx e he hb
    rcases hx with h | h | h | h
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
    · exact Or.inr (Or.inr h)
    · exact absurd (h e he) hb
  refine ⟨corner _ hadj.2.1 (liftDart hle d) rfl hd, ?_⟩
  exact corner _ hadj.2.2 (T.rotation.faceNext (liftDart hle d)) (RotationSystem.face_next_fst _ _)
    (by rw [faceNext_face]; exact hd)

variable (htri : T.Triangulated) (hpq : T.Adj p q) (hqr : T.Adj q r) (hrp : T.Adj r p)
include htri hpq hqr hrp

theorem T_faceNext_three (D : T.Dart) : (⇑T.rotation.faceNext)^[3] D = D := by
  have h := T.rotation.face_next_iterate_length D
  rwa [show T.rotation.faceLength (T.rotation.faceOf D) = 3 from htri D] at h

/-- **D3a.** The kept map is triangulated. -/
theorem kept_triangulated : N.Triangulated := by
  classical
  intro d
  have period : (⇑N.rotation.faceNext)^[3] d = d := by
    by_cases hd : c (T.faceOf (liftDart hle d)) = b
    · apply liftDart_injective hle
      have e1 := lift_faceNext_keptFace hc hN hle spec d hd
      have k1 := keptFace_faceNext hc hN hle spec d hd
      have e2 := lift_faceNext_keptFace hc hN hle spec _ k1
      have k2 := keptFace_faceNext hc hN hle spec _ k1
      have e3 := lift_faceNext_keptFace hc hN hle spec _ k2
      simp only [Function.iterate_succ_apply', Function.iterate_zero, id]
      rw [e3, e2, e1]
      have := T_faceNext_three hc hN hle spec htri hpq hqr hrp (liftDart hle d)
      simpa only [Function.iterate_succ_apply', Function.iterate_zero, id] using this
    · obtain ⟨hu, hv⟩ := far_ends hc hN hle spec d hd
      set u := (liftDart hle d).fst
      set v := (liftDart hle d).snd
      have huv : u ≠ v := (liftDart hle d).adj.ne
      obtain ⟨w, hw, hwu, hwv, hcov⟩ := third_corner hpq.ne hqr.ne hrp.ne hu hv huv
      -- first step: `u → v` to `v → w`
      obtain ⟨s1, f1⟩ := lift_next_farFace hc hN hle spec d rfl rfl hu hv hw hwu
        (adj_corners hpq hqr hrp hv hw hwv.symm) hcov hd
      set d1 := N.rotation.next d.symm
      have d1f : (liftDart hle d1).fst = v := by
        change (N.rotation.next d.symm).fst = _
        rw [N.rotation.next_fst]; rfl
      -- second step: `v → w` to `w → u`
      obtain ⟨s2, f2⟩ := lift_next_farFace hc hN hle spec d1 d1f s1 hv hw hu huv
        (adj_corners hpq hqr hrp hw hu hwu)
        (fun z hz => by
          rcases hcov z hz with h | h | h
          exacts [Or.inr (Or.inr h), Or.inl h, Or.inr (Or.inl h)])
        f1
      set d2 := N.rotation.next d1.symm
      have d2f : (liftDart hle d2).fst = w := by
        change (N.rotation.next d1.symm).fst = _
        rw [N.rotation.next_fst]; exact s1
      -- third step: `w → u` to `u → v`
      obtain ⟨s3, -⟩ := lift_next_farFace hc hN hle spec d2 d2f s2 hw hu hv hwv.symm
        (adj_corners hpq hqr hrp hu hv huv)
        (fun z hz => by
          rcases hcov z hz with h | h | h
          exacts [Or.inr (Or.inl h), Or.inr (Or.inr h), Or.inl h])
        f2
      have d3f : (liftDart hle (N.rotation.next d2.symm)).fst = u := by
        change (N.rotation.next d2.symm).fst = _
        rw [N.rotation.next_fst]; exact s2
      apply liftDart_injective hle
      simp only [Function.iterate_succ_apply', Function.iterate_zero, id,
        RotationSystem.face_next_apply]
      apply Dart.ext; apply Prod.ext
      · exact d3f
      · exact s3
  have hfix : N.rotation.faceNext d ≠ d := by
    intro he
    have h1 := congrArg (fun a : N.Dart => a.fst) he
    simp only [RotationSystem.face_next_fst] at h1
    exact d.adj.ne h1.symm
  rw [N.rotation.face_length_eq_period]
  exact Function.minimalPeriod_eq_prime (p := 3) (hp := ⟨Nat.prime_three⟩) period hfix

/-- **D3b.** The triangle is a face of the kept map. -/
theorem kept_facial : Facial N p q r := by
  classical
  have hHpq : N.graph.Adj p q := by
    rw [hN]; exact ⟨hpq, inF_keep (Or.inl rfl), inF_keep (Or.inr (Or.inl rfl))⟩
  let dpq : N.Dart := ⟨(p, q), hHpq⟩
  have hp' : p = p ∨ p = q ∨ p = r := Or.inl rfl
  have hq' : q = p ∨ q = q ∨ q = r := Or.inr (Or.inl rfl)
  have hr' : r = p ∨ r = q ∨ r = r := Or.inr (Or.inr rfl)
  have cov : ∀ z, (z = p ∨ z = q ∨ z = r) → z = p ∨ z = q ∨ z = r := fun z h => h
  by_cases hd : c (T.faceOf (liftDart hle dpq)) = b
  · -- the face of `q → p` is far
    have hjump := hc (liftDart hle dpq)
    have hqp : c (T.faceOf (liftDart hle dpq.symm)) ≠ b := by
      intro h2
      have h1 : c (T.faceOf (liftDart hle dpq)) + c (T.faceOf (liftDart hle dpq).symm) = 0 := by
        change _ + c (T.faceOf (liftDart hle dpq.symm)) = 0
        rw [hd, h2]; exact (show ∀ x : ZMod 2, x + x = 0 by decide) b
      rw [← hjump] at h1
      have n2 : s(p,q) ≠ s(q,r) := fun h => by
        rw [Sym2.eq_iff] at h; rcases h with h | h; exact hpq.ne h.1; exact hrp.ne h.1.symm
      have n3 : s(p,q) ≠ s(r,p) := fun h => by
        rw [Sym2.eq_iff] at h; rcases h with h | h; exact hrp.ne h.1.symm; exact hqr.ne h.2
      simp [triInd, edgeOfDart, liftDart, dpq, Dart.edge, n2, n3] at h1
    obtain ⟨s, -⟩ := lift_next_farFace (u := q) (v := p) (w := r) hc hN hle spec dpq.symm rfl rfl
      hq' hp' hr' hqr.ne.symm hrp.symm
      (fun z hz => by
        rcases hz with h | h | h
        exacts [Or.inr (Or.inl h), Or.inl h, Or.inr (Or.inr h)]) hqp
    exact Or.inr ⟨hHpq, s⟩
  · obtain ⟨s, -⟩ := lift_next_farFace (u := p) (v := q) (w := r) hc hN hle spec dpq rfl rfl
      hp' hq' hr' hrp.ne hqr cov hd
    exact Or.inl ⟨hHpq.symm, s⟩

end Map
end Kept

/-! ## D3c, D4. Degrees, connectivity, and lifting cleanness -/

section Lift
open RotationSystem VacancyCliqueLift VacancySlide VacancyShortFill VacancyMobility
  VacancyIcosahedral

variable {T : SphericalMap n} {p q r : Fin n} {c : T.Face → ZMod 2} {b : ZMod 2}

/-- The triangle as a vertex set. -/
def triSet (p q r : Fin n) : Set (Fin n) := {x | x = p ∨ x = q ∨ x = r}

theorem keep_nbr (hc : TriPotential T p q r c) {x y : Fin n} (hx : x ∈ keep T c b p q r)
    (hxoff : x ≠ p ∧ x ≠ q ∧ x ≠ r) (hxy : T.Adj x y) : y ∈ keep T c b p q r := by
  have hon : OnSide T c b x := by
    rcases hx with h | h | h | h
    · exact absurd h hxoff.1
    · exact absurd h hxoff.2.1
    · exact absurd h hxoff.2.2
    · exact h
  by_cases hy : y ≠ p ∧ y ≠ q ∧ y ≠ r
  · exact Or.inr (Or.inr (Or.inr (onSide_adj T hc hxoff hy hxy hon)))
  · simp only [not_and_or, not_not] at hy
    exact inF_keep hy

theorem keep_boundary (hc : TriPotential T p q r c) :
    Boundary T.graph (keep T c b p q r) (triSet p q r) := by
  refine ⟨fun x hx => inF_keep hx, fun u w hu hw huw => ?_⟩
  by_contra hoff
  have hoff' : u ≠ p ∧ u ≠ q ∧ u ≠ r := by
    have : ¬ (u = p ∨ u = q ∨ u = r) := hoff
    tauto
  exact hw (keep_nbr hc hu hoff' huw)

theorem tri_clique (hpq : T.Adj p q) (hqr : T.Adj q r) (hrp : T.Adj r p) :
    Clique T.graph (triSet p q r) :=
  fun _ _ hu hv huv => adj_corners hpq hqr hrp hu hv huv

theorem kept_neighborSet (hc : TriPotential T p q r c) {N : SphericalMap n}
    (hN : N.graph = sideGraph T.graph (keep T c b p q r)) {x : Fin n}
    (hx : x ∈ keep T c b p q r) (hxoff : x ≠ p ∧ x ≠ q ∧ x ≠ r) :
    N.graph.neighborSet x = T.graph.neighborSet x := by
  ext y
  simp only [mem_neighborSet, hN, sideGraph]
  exact ⟨fun h => h.1, fun h => ⟨h, hx, keep_nbr hc hx hxoff h⟩⟩

theorem kept_degree (hc : TriPotential T p q r c) {N : SphericalMap n}
    (hN : N.graph = sideGraph T.graph (keep T c b p q r)) {x : Fin n}
    (hx : x ∈ keep T c b p q r) (hxoff : x ≠ p ∧ x ≠ q ∧ x ≠ r) :
    N.graph.degree x = T.graph.degree x := by
  rw [← card_neighborSet_eq_degree, ← card_neighborSet_eq_degree, ← Nat.card_eq_fintype_card,
    ← Nat.card_eq_fintype_card, kept_neighborSet hc hN hx hxoff]

theorem dropped_degree {N : SphericalMap n}
    (hN : N.graph = sideGraph T.graph (keep T c b p q r)) {x : Fin n}
    (hx : x ∉ keep T c b p q r) : N.graph.degree x = 0 := by
  rw [← card_neighborSet_eq_degree, Fintype.card_eq_zero_iff]
  refine ⟨fun ⟨y, hy⟩ => ?_⟩
  have : N.graph.Adj x y := hy
  rw [hN] at this
  exact hx this.2.1

theorem kept_reach (hc : TriPotential T p q r c) (hpq : T.Adj p q) (hqr : T.Adj q r)
    (hrp : T.Adj r p) {N : SphericalMap n}
    (hN : N.graph = sideGraph T.graph (keep T c b p q r)) {a : Fin n}
    (ha : a ∈ keep T c b p q r) (hreach : T.graph.Reachable a p) : N.graph.Reachable a p := by
  obtain ⟨W⟩ := hreach
  suffices key : ∀ {a y : Fin n} (W : T.graph.Walk a y), y = p → a ∈ keep T c b p q r →
      N.graph.Reachable a p from key W rfl ha
  intro a y W
  induction W with
  | nil => intro hy _; rw [hy]
  | @cons a a' y hadj W ih =>
    intro hy ha
    by_cases hoff : a ≠ p ∧ a ≠ q ∧ a ≠ r
    · have ha' := keep_nbr hc ha hoff hadj
      have hN' : N.graph.Adj a a' := by rw [hN]; exact ⟨hadj, ha, ha'⟩
      exact hN'.reachable.trans (ih hy ha')
    · simp only [not_and_or, not_not] at hoff
      by_cases hap : a = p
      · rw [hap]
      · have hT := adj_corners hpq hqr hrp hoff (Or.inl rfl) hap
        have hN' : N.graph.Adj a p := by
          rw [hN]; exact ⟨hT, ha, inF_keep (Or.inl rfl)⟩
        exact hN'.reachable

/-- Lift a pure side path: components meeting the outside are isolated singletons there and are
skipped; the others lift through the clique interface. -/
theorem side_pure_lift {G : SimpleGraph (Fin n)} {A Fs : Set (Fin n)} (bd : Boundary G A Fs)
    (cl : Clique G Fs) {h : Fin n} {m : ℕ} {c d : Fin n → Fin 4}
    (path : PurePath (sideGraph G A) h m c d) {g : Fin n → Fin 4}
    (eq : ∀ x, x ∈ A → g x = c x) :
    ∃ m' e, PurePath G h m' g e ∧ ∀ x, x ∈ A → e x = d x := by
  classical
  induction path generalizing g with
  | nil c => exact ⟨0, g, .nil _, eq⟩
  | @cons k c c1 d step rest ih =>
    obtain ⟨a, b, S, hab, whole, rfl⟩ := step
    by_cases hS : S ⊆ A
    · obtain ⟨e1, st, agree⟩ := kempe_lift_agree G bd cl eq ⟨a, b, S, hab, whole, hS, rfl⟩
      obtain ⟨m', e, p', agree'⟩ := ih agree
      exact ⟨m' + 1, e, .cons st p', agree'⟩
    · obtain ⟨w, hwS, hwA⟩ := Set.not_subset.mp hS
      obtain ⟨s, act, mem⟩ := whole
      have iso : ∀ u, ¬ (pairGraph (sideGraph G A) h c a b).Adj w u := fun u e => hwA e.1.2.1
      have hsw : s = w := by
        by_contra hne
        obtain ⟨u, hu⟩ := first_step (sideGraph G A) ((mem w).mp hwS).symm (Ne.symm hne)
        exact iso u hu
      subst hsw
      have hout : ∀ x, x ∈ A → x ∉ S := by
        intro x hx hxS
        by_cases hxs : s = x
        · subst hxs; exact hwA hx
        · obtain ⟨u, hu⟩ := first_step (sideGraph G A) ((mem x).mp hxS) hxs
          exact iso u hu
      have eq' : ∀ x, x ∈ A → g x = swap c a b S x := fun x hx => by
        rw [swap_out (hout x hx)]; exact eq x hx
      exact ih eq'

/-- **D4.** A pure-clean vertex of the kept map, off the triangle, is pure-clean in `T`. -/
theorem pureClean_lift (hc : TriPotential T p q r c) (hpq : T.Adj p q) (hqr : T.Adj q r)
    (hrp : T.Adj r p) {N : SphericalMap n} (hN : N.graph = sideGraph T.graph (keep T c b p q r))
    {v : Fin n} (hv : v ∈ keep T c b p q r) (hvoff : v ≠ p ∧ v ≠ q ∧ v ≠ r)
    (hpc : PureClean N v) : PureClean T v := by
  classical
  intro g hg
  have hle : N.graph ≤ T.graph := by rw [hN]; exact fun _ _ e => e.1
  have hg' : ProperOff N.graph v g := fun x y e hx hy => hg (hle e) hx hy
  obtain ⟨m, k, _, d, path, tgt⟩ := hpc g hg'
  rw [hN] at path tgt
  obtain ⟨m', e, path', agree⟩ :=
    side_pure_lift (keep_boundary hc) (tri_clique hpq hqr hrp) path (fun _ _ => rfl)
  have hvF : v ∉ triSet p q r := by
    show ¬ (v = p ∨ v = q ∨ v = r)
    rintro (h | h | h)
    exacts [hvoff.1 h, hvoff.2.1 h, hvoff.2.2 h]
  exact ⟨m', m', le_rfl, e, path', target_lift T.graph (keep_boundary hc) hv hvF agree tgt⟩

end Lift

/-! ## D5. The separating-triangle induction -/

section Induction
open RotationSystem VacancyCliqueLift VacancyIcosahedral

/-- Every triangle of `T` bounds a face (`T` has no separating triangle). -/
def NoSep (T : SphericalMap n) : Prop :=
  ∀ x y z, T.Adj x y → T.Adj y z → T.Adj z x → Facial T x y z

/-- The relative class with protected face `p q r`, stated on the support: a triangulation,
connected on its non-isolated vertices, whose non-isolated vertices off the face have degree at
least five. -/
def RelClass (T : SphericalMap n) (p q r : Fin n) : Prop :=
  T.Triangulated ∧ T.Adj p q ∧ T.Adj q r ∧ T.Adj r p ∧ Facial T p q r ∧
  (∀ x, x ≠ p → x ≠ q → x ≠ r → T.graph.degree x = 0 ∨ 5 ≤ T.graph.degree x) ∧
  (∀ x y, 0 < T.graph.degree x → 0 < T.graph.degree y → T.graph.Reachable x y)

/-- A pure-clean vertex of degree five off the face `p q r`. -/
def CleanOff (T : SphericalMap n) (p q r : Fin n) : Prop :=
  ∃ v, v ≠ p ∧ v ≠ q ∧ v ≠ r ∧ T.graph.degree v = 5 ∧ PureClean T v

/-- Lemma R\* for the four-connected core, stated on the support. -/
def RStarSupport : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m) (p q r : Fin m), RelClass T p q r → NoSep T → CleanOff T p q r

/-- The three corners of a face lie on one face. -/
theorem facial_darts {T : SphericalMap n} (htri : T.Triangulated) {p q r : Fin n}
    (hf : Facial T p q r) : ∃ dφ : T.Dart, ∀ w, (w = p ∨ w = q ∨ w = r) →
      ∃ e : T.Dart, e.fst = w ∧ T.faceOf e = T.faceOf dφ := by
  rcases hf with h | h
  · -- face of `p → q`: darts `p → q`, `q → r`, `r → p`
    obtain ⟨hqp, hqr, e1⟩ := nx_dart h
    obtain ⟨hrq, hrp, e2⟩ := nx_dart (nx_tri htri h).1
    let d : T.Dart := ⟨(p, q), hqp.symm⟩
    have f1 : T.faceOf ⟨(q, r), hqr⟩ = T.faceOf d := by
      rw [← e1]; exact T.rotation.face_of_face_next d
    have f2 : T.faceOf ⟨(r, p), hrp⟩ = T.faceOf d := by
      rw [← f1, ← e2]; exact T.rotation.face_of_face_next (⟨(q, r), hqr⟩ : T.Dart)
    refine ⟨d, fun w hw => ?_⟩
    rcases hw with rfl | rfl | rfl
    · exact ⟨d, rfl, rfl⟩
    · exact ⟨_, rfl, f1⟩
    · exact ⟨_, rfl, f2⟩
  · -- face of `q → p`: darts `q → p`, `p → r`, `r → q`
    obtain ⟨hpq, hpr, e1⟩ := nx_dart h
    obtain ⟨hrp, hrq, e2⟩ := nx_dart (nx_tri htri h).1
    let d : T.Dart := ⟨(q, p), hpq.symm⟩
    have f1 : T.faceOf ⟨(p, r), hpr⟩ = T.faceOf d := by
      rw [← e1]; exact T.rotation.face_of_face_next d
    have f2 : T.faceOf ⟨(r, q), hrq⟩ = T.faceOf d := by
      rw [← f1, ← e2]; exact T.rotation.face_of_face_next (⟨(p, r), hpr⟩ : T.Dart)
    refine ⟨d, fun w hw => ?_⟩
    rcases hw with rfl | rfl | rfl
    · exact ⟨_, rfl, f1⟩
    · exact ⟨d, rfl, rfl⟩
    · exact ⟨_, rfl, f2⟩

/-- The number of non-isolated vertices. -/
noncomputable def supportSize (T : SphericalMap n) : ℕ :=
  (Finset.univ.filter fun x => 0 < T.graph.degree x).card

/-- **D5, support form.** Lemma R\* in the core gives a pure-clean vertex of degree five off the
protected face in every member of the relative class. -/
theorem cleanOff_of_RStarSupport (hR : RStarSupport) :
    ∀ (T : SphericalMap n) (p q r : Fin n), RelClass T p q r → CleanOff T p q r := by
  classical
  intro T
  generalize hk : supportSize T = k
  induction k using Nat.strong_induction_on generalizing T with
  | h k ih =>
  intro p q r hrel
  by_cases hns : NoSep T
  · exact hR n T p q r hrel hns
  obtain ⟨htri, hpq, hqr, hrp, hfac, hdeg, hconn⟩ := hrel
  simp only [NoSep, not_forall] at hns
  obtain ⟨x, y, z, hxy, hyz, hzx, hnf⟩ := hns
  obtain ⟨c, hc⟩ := exists_triPotential T hxy hyz hzx
  obtain ⟨dφ, hφ⟩ := facial_darts htri hfac
  set b : ZMod 2 := c (T.faceOf dφ) + 1 with hb
  have hbne : ∀ e : T.Dart, T.faceOf e = T.faceOf dφ → c (T.faceOf e) ≠ b := by
    intro e he h
    rw [he, hb] at h
    exact (show ∀ a : ZMod 2, a ≠ a + 1 by decide) _ h
  obtain ⟨N, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph (keep T c b x y z))
    (fun _ _ e => e.1)
  -- vertices kept off the separating triangle are off the protected face
  have off_phi : ∀ w, w ∈ keep T c b x y z → (w ≠ x ∧ w ≠ y ∧ w ≠ z) →
      w ≠ p ∧ w ≠ q ∧ w ≠ r := by
    intro w hw hoff
    have hon : OnSide T c b w := by
      rcases hw with h | h | h | h
      exacts [absurd h hoff.1, absurd h hoff.2.1, absurd h hoff.2.2, h]
    have key : ¬ (w = p ∨ w = q ∨ w = r) := by
      intro hwφ
      obtain ⟨e, he, hf⟩ := hφ w hwφ
      exact hbne e hf (hon e he)
    tauto
  have hNadj : ∀ {u v : Fin n}, T.Adj u v → u ∈ keep T c b x y z → v ∈ keep T c b x y z →
      N.graph.Adj u v := fun h hu hv => by rw [hN]; exact ⟨h, hu, hv⟩
  have hxk : x ∈ keep T c b x y z := inF_keep (Or.inl rfl)
  have hyk : y ∈ keep T c b x y z := inF_keep (Or.inr (Or.inl rfl))
  have hzk : z ∈ keep T c b x y z := inF_keep (Or.inr (Or.inr rfl))
  have hkeepdeg : ∀ w, 0 < N.graph.degree w → w ∈ keep T c b x y z := by
    intro w hw
    obtain ⟨u, hu⟩ := N.graph.degree_pos_iff_exists_adj w |>.mp hw
    rw [hN] at hu; exact hu.2.1
  have hrelN : RelClass N x y z := by
    refine ⟨kept_triangulated hc hN hle spec htri hxy hyz hzx, hNadj hxy hxk hyk,
      hNadj hyz hyk hzk, hNadj hzx hzk hxk, kept_facial hc hN hle spec htri hxy hyz hzx, ?_, ?_⟩
    · intro w h1 h2 h3
      by_cases hw : w ∈ keep T c b x y z
      · rw [kept_degree hc hN hw ⟨h1, h2, h3⟩]
        obtain ⟨n1, n2, n3⟩ := off_phi w hw ⟨h1, h2, h3⟩
        exact hdeg w n1 n2 n3
      · exact Or.inl (dropped_degree hN hw)
    · intro u v hu hv
      have hTx : 0 < T.graph.degree x := T.graph.degree_pos_iff_exists_adj x |>.mpr ⟨y, hxy⟩
      have reach : ∀ w, 0 < N.graph.degree w → N.graph.Reachable w x := by
        intro w hw
        have hwk := hkeepdeg w hw
        have hTw : 0 < T.graph.degree w :=
          lt_of_lt_of_le hw (SimpleGraph.degree_le_of_le hle)
        exact kept_reach hc hxy hyz hzx hN hwk (hconn w x hTw hTx)
      exact (reach u hu).trans (reach v hv).symm
  -- the far side loses a non-isolated vertex
  have hlt : supportSize N < k := by
    rw [← hk]
    obtain ⟨z0, hz0, ⟨y0, hy0⟩, hon0⟩ := exists_onSide T htri hxy hyz hzx hnf hc (b + 1)
    have hz0k : z0 ∉ keep T c b x y z := by
      rintro (h | h | h | h)
      · exact hz0.1 h
      · exact hz0.2.1 h
      · exact hz0.2.2 h
      · have := h ⟨(z0, y0), hy0⟩ rfl
        rw [hon0 ⟨(z0, y0), hy0⟩ rfl] at this
        exact (show ∀ a : ZMod 2, a + 1 ≠ a by decide) b this
    apply Finset.card_lt_card
    refine ⟨fun w hw => ?_, fun hsub => ?_⟩
    · simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hw ⊢
      exact lt_of_lt_of_le hw (SimpleGraph.degree_le_of_le hle)
    · have hmem : z0 ∈ Finset.univ.filter (fun x => 0 < T.graph.degree x) := by
        simp only [Finset.mem_filter, Finset.mem_univ, true_and]
        exact T.graph.degree_pos_iff_exists_adj z0 |>.mpr ⟨y0, hy0⟩
      have := hsub hmem
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at this
      rw [dropped_degree hN hz0k] at this
      exact lt_irrefl 0 this
  obtain ⟨v, hvx, hvy, hvz, hv5, hvc⟩ := ih _ hlt N rfl x y z hrelN
  have hvk := hkeepdeg v (by omega)
  have hvoff : v ≠ x ∧ v ≠ y ∧ v ≠ z := ⟨hvx, hvy, hvz⟩
  obtain ⟨n1, n2, n3⟩ := off_phi v hvk hvoff
  refine ⟨v, n1, n2, n3, ?_, pureClean_lift hc hxy hyz hzx hN hvk hvoff hvc⟩
  rw [← kept_degree hc hN hvk hvoff]; exact hv5

/-- **R\* in the core (support form) implies the Four Colour Theorem.** -/
theorem four_color_of_RStarSupport (hR : RStarSupport) {n : ℕ} (M : SphericalMap n) :
    M.graph.Colorable 4 := by
  refine four_color_of_global_Rstar (fun m T hm hconn htri hdeg => ?_) M
  classical
  let x : Fin m := ⟨0, hm⟩
  obtain ⟨y, hxy⟩ := T.graph.degree_pos_iff_exists_adj x |>.mp (by have := hdeg x; omega)
  let z := (T.rotation.next ⟨(y, x), hxy.symm⟩).snd
  have hN : Nx T y x z := ⟨hxy.symm, rfl⟩
  have hyz : T.Adj y z := nx_adj_right hN
  have hzx : T.Adj z x := nx_adj_right (nx_tri htri hN).1
  have hrel : RelClass T x y z :=
    ⟨htri, hxy, hyz, hzx, Or.inl hN, fun w _ _ _ => Or.inr (hdeg w),
      fun u v _ _ => hconn.preconnected u v⟩
  obtain ⟨v, -, -, -, hv5, hvc⟩ := cleanOff_of_RStarSupport hR T x y z hrel
  exact ⟨v, hv5, hvc⟩

end Induction

end SimpleGraph.SphericalMap
