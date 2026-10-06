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

end SimpleGraph.SphericalMap
