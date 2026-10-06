module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarCore

/-!
# The minimal-counterexample frame

`four_color_of_smaller_gate`: the library's support-size induction, with the gate allowed to
use the four-colourability of *every* spherical map of smaller support (not only `T - r`).

F1. `colorable_of_separating_triangle`: a triangulation with a separating triangle is
four-colourable when both kept sides are (glue along the triangle after a colour permutation).

F4 + F1. `four_color_of_RStar_noSepTri`: if every connected spherical triangulation of minimum
degree five **with no separating triangle** has a pure-clean vertex of degree five, every spherical
map is four-colourable. No protected face is needed.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral VacancyCliqueLift

/-- **Assembly with a strong gate.** If every connected triangulation of minimum degree five is
four-colourable as soon as every spherical map of smaller support is, then every spherical map
is four-colourable. -/
theorem four_color_of_smaller_gate
    (hgate : ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
      (∀ x, 5 ≤ T.graph.degree x) →
      (∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
        N.graph.Colorable 4) → T.graph.Colorable 4)
    {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4 := by
  classical
  suffices H : ∀ k, ∀ (n : ℕ) (M : SphericalMap n), Nat.card M.graph.support = k →
      M.graph.Colorable 4 from H _ n M rfl
  intro k
  induction k using Nat.strong_induction_on with
  | h k ih =>
    intro n M hk
    by_cases hd : Nonempty M.Dart
    · obtain ⟨d⟩ := hd
      by_cases hlow : ∃ x ∈ M.graph.support, M.graph.degree x ≤ 4
      · obtain ⟨x, hx, hdeg⟩ := hlow
        have hxpos := (M.graph.degree_pos_iff_mem_support x).mpr hx
        obtain ⟨N, hN, _⟩ := M.isolate_closed x hxpos
        have hlt : Nat.card N.graph.support < k := by
          rw [hN, ← hk]
          exact M.isolate_support_card_lt x hx
        obtain ⟨c⟩ := ih _ hlt n N rfl
        apply M.four_color_extension x hdeg
        exact ⟨SimpleGraph.Coloring.mk (fun z => c z.val) (fun {u v} huv =>
          c.valid (by rw [hN]; exact ⟨huv, u.property, v.property⟩))⟩
      · have hmin : ∀ x ∈ M.graph.support, 5 ≤ M.graph.degree x := by
          intro x hx
          by_contra h
          exact hlow ⟨x, hx, by omega⟩
        let s := Nat.card M.graph.support
        let i := M.supportEquivFin
        let S := M.supportTransport i
        have hs : 0 < s := by
          exact Nat.card_pos_iff.mpr ⟨⟨⟨d.fst, d.adj.mem_support_left⟩⟩, inferInstance⟩
        have hS : ∀ x, 5 ≤ S.graph.degree x := M.support_min_degree i 5 hmin
        obtain ⟨T, hST, hconn, htri, hT⟩ := S.exists_triangulated_completion_min_five hs hS
        have hsupport : T.graph.support = Set.univ := by
          ext x
          simp only [Set.mem_univ, iff_true]
          exact (T.graph.degree_pos_iff_mem_support x).mp (by have := hT x; omega)
        have hcard : Nat.card T.graph.support = s := by
          rw [hsupport]
          simp
        have hcT : T.graph.Colorable 4 := hgate s T hs hconn htri hT
          (fun m' N hN => ih _ (by rw [← hk]; exact hN.trans_eq hcard) m' N rfl)
        obtain ⟨cS⟩ := hcT.mono_left hST
        exact ⟨M.extendSupportColoring i (0 : Fin 4) cS⟩
    · exact ⟨SimpleGraph.Coloring.mk (fun _ => (0 : Fin 4)) (fun {u v} huv =>
        (hd ⟨⟨(u, v), huv⟩⟩).elim)⟩


theorem natCard_support_eq {n : ℕ} (T : SphericalMap n) :
    Nat.card T.graph.support = supportSize T := by
  classical
  rw [Nat.card_eq_card_toFinset]
  unfold supportSize
  congr 1
  ext x
  simp [SimpleGraph.degree_pos_iff_mem_support]

set_option synthInstance.maxHeartbeats 400000 in
/-- Three distinct colours can be sent to any three distinct colours. -/
theorem exists_perm_three : ∀ a1 a2 a3 b1 b2 b3 : Fin 4, a1 ≠ a2 → a2 ≠ a3 → a3 ≠ a1 →
    b1 ≠ b2 → b2 ≠ b3 → b3 ≠ b1 →
    ∃ σ : Equiv.Perm (Fin 4), σ b1 = a1 ∧ σ b2 = a2 ∧ σ b3 = a3 := by
  decide +kernel

section Glue
variable {n : ℕ} {T : SphericalMap n} {p q r : Fin n} {c : T.Face → ZMod 2}

/-- A vertex with an edge that is not kept on side `0` is kept on side `1`. -/
theorem keep_one_of_not_keep_zero (hc : TriPotential T p q r c) {x y : Fin n} (hxy : T.Adj x y)
    (hx : x ∉ keep T c 0 p q r) : x ∈ keep T c 1 p q r := by
  have hoff : x ≠ p ∧ x ≠ q ∧ x ≠ r :=
    ⟨fun h => hx (inF_keep (Or.inl h)), fun h => hx (inF_keep (Or.inr (Or.inl h))),
      fun h => hx (inF_keep (Or.inr (Or.inr h)))⟩
  let d : T.Dart := ⟨(x, y), hxy⟩
  have hs := onSide_of_dart T hc hoff d rfl
  have two : ∀ a : ZMod 2, a = 0 ∨ a = 1 := by decide
  rcases two (c (T.faceOf d)) with h | h
  · rw [h] at hs; exact absurd (Or.inr (Or.inr (Or.inr hs))) hx
  · rw [h] at hs; exact Or.inr (Or.inr (Or.inr hs))

/-- The kept side loses a non-isolated vertex. -/
theorem kept_supportSize_lt (htri : T.Triangulated) (hpq : T.Adj p q) (hqr : T.Adj q r)
    (hrp : T.Adj r p) (hnf : ¬ Facial T p q r) (hc : TriPotential T p q r c) (b : ZMod 2)
    {N : SphericalMap n} (hN : N.graph = sideGraph T.graph (keep T c b p q r))
    (hle : N.graph ≤ T.graph) : supportSize N < supportSize T := by
  classical
  obtain ⟨z0, hz0, ⟨y0, hy0⟩, hon0⟩ := exists_onSide T htri hpq hqr hrp hnf hc (b + 1)
  have hz0k : z0 ∉ keep T c b p q r := by
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

/-- **F1.** A triangulation with a separating triangle is four-colourable when every spherical
map of smaller support is. -/
theorem colorable_of_separating_triangle (htri : T.Triangulated) (hpq : T.Adj p q)
    (hqr : T.Adj q r) (hrp : T.Adj r p) (hnf : ¬ Facial T p q r)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  obtain ⟨c, hc⟩ := exists_triPotential T hpq hqr hrp
  set K0 := keep T c 0 p q r
  set K1 := keep T c 1 p q r
  obtain ⟨N0, hN0, hle0, -⟩ := subgraph_tracked T (sideGraph T.graph K0) (fun _ _ e => e.1)
  obtain ⟨N1, hN1, hle1, -⟩ := subgraph_tracked T (sideGraph T.graph K1) (fun _ _ e => e.1)
  have lt0 := kept_supportSize_lt htri hpq hqr hrp hnf hc 0 hN0 hle0
  have lt1 := kept_supportSize_lt htri hpq hqr hrp hnf hc 1 hN1 hle1
  obtain ⟨cA⟩ := IH n N0 (by rw [natCard_support_eq, natCard_support_eq]; exact lt0)
  obtain ⟨cB⟩ := IH n N1 (by rw [natCard_support_eq, natCard_support_eq]; exact lt1)
  have inF0 : ∀ w, (w = p ∨ w = q ∨ w = r) → w ∈ K0 := fun w h => inF_keep h
  have inF1 : ∀ w, (w = p ∨ w = q ∨ w = r) → w ∈ K1 := fun w h => inF_keep h
  have adj0 : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∈ K0 → N0.graph.Adj u v :=
    fun h hu hv => by rw [hN0]; exact ⟨h, hu, hv⟩
  have adj1 : ∀ {u v}, T.Adj u v → u ∈ K1 → v ∈ K1 → N1.graph.Adj u v :=
    fun h hu hv => by rw [hN1]; exact ⟨h, hu, hv⟩
  have hp' : p = p ∨ p = q ∨ p = r := Or.inl rfl
  have hq' : q = p ∨ q = q ∨ q = r := Or.inr (Or.inl rfl)
  have hr' : r = p ∨ r = q ∨ r = r := Or.inr (Or.inr rfl)
  obtain ⟨σ, sp, sq, sr⟩ := exists_perm_three (cA p) (cA q) (cA r) (cB p) (cB q) (cB r)
    (cA.valid (adj0 hpq (inF0 _ hp') (inF0 _ hq')))
    (cA.valid (adj0 hqr (inF0 _ hq') (inF0 _ hr')))
    (cA.valid (adj0 hrp (inF0 _ hr') (inF0 _ hp')))
    (cB.valid (adj1 hpq (inF1 _ hp') (inF1 _ hq')))
    (cB.valid (adj1 hqr (inF1 _ hq') (inF1 _ hr')))
    (cB.valid (adj1 hrp (inF1 _ hr') (inF1 _ hp')))
  have agree : ∀ w, (w = p ∨ w = q ∨ w = r) → σ (cB w) = cA w := by
    rintro w (rfl | rfl | rfl)
    exacts [sp, sq, sr]
  have bd := keep_boundary (b := 0) hc
  -- mixed edge: the kept end lies on the triangle
  have mixed : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∉ K0 → cA u ≠ σ (cB v) := by
    intro u v huv hu hv
    have huF : u = p ∨ u = q ∨ u = r := bd.2 u v hu hv huv
    have hv1 := keep_one_of_not_keep_zero hc huv.symm hv
    rw [← agree u huF]
    exact σ.injective.ne (cB.valid (adj1 huv (inF1 u huF) hv1))
  refine ⟨SimpleGraph.Coloring.mk (fun v => if v ∈ K0 then cA v else σ (cB v)) ?_⟩
  intro u v huv
  by_cases hu : u ∈ K0 <;> by_cases hv : v ∈ K0
  · simp only [hu, hv, ↓reduceIte]; exact cA.valid (adj0 huv hu hv)
  · simp only [hu, hv, ↓reduceIte]; exact mixed huv hu hv
  · simp only [hu, hv, ↓reduceIte]; exact (mixed huv.symm hv hu).symm
  · simp only [hu, hv, ↓reduceIte]
    exact σ.injective.ne (cB.valid (adj1 huv (keep_one_of_not_keep_zero hc huv hu)
      (keep_one_of_not_keep_zero hc huv.symm hv)))

end Glue

/-- R\* asked only for minimum-degree-five triangulations with no separating triangle, with the
clean vertex anywhere. -/
def RStarNoSepTri : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) → NoSep T → ∃ v, T.graph.degree v = 5 ∧ PureClean T v

/-- **F1 + F4.** If every connected spherical triangulation of minimum degree five with no
separating triangle has a pure-clean vertex of degree five, every spherical map is
four-colourable. -/
theorem four_color_of_RStar_noSepTri (hR : RStarNoSepTri) {n : ℕ} (M : SphericalMap n) :
    M.graph.Colorable 4 := by
  refine four_color_of_smaller_gate (fun m T hm hconn htri hdeg IH => ?_) M
  classical
  by_cases hns : NoSep T
  · obtain ⟨v, hv5, hpc⟩ := hR m T hm hconn htri hdeg hns
    apply extend_of_pureClean T v hpc
    have hvs : v ∈ T.graph.support := (T.graph.degree_pos_iff_mem_support v).mp (by omega)
    obtain ⟨N, hN, _⟩ := T.isolate_closed v (by omega)
    obtain ⟨cN⟩ := IH m N (by rw [hN]; exact T.isolate_support_card_lt v hvs)
    exact ⟨SimpleGraph.Coloring.mk (fun z => cN z.val) (fun {u w} huw =>
      cN.valid (by rw [hN]; exact ⟨huw, u.property, w.property⟩))⟩
  · simp only [NoSep, not_forall] at hns
    obtain ⟨x, y, z, hxy, hyz, hzx, hnf⟩ := hns
    exact colorable_of_separating_triangle htri hxy hyz hzx hnf IH

/-- The hand form of R\* (four-connected relative class) implies the protected-face-free form. -/
theorem rStarNoSepTri_of_core (hR : RStarCore) : RStarNoSepTri := by
  intro m T hm hconn htri hdeg hns
  let x : Fin m := ⟨0, hm⟩
  obtain ⟨y, hxy⟩ := T.graph.degree_pos_iff_exists_adj x |>.mp (by have := hdeg x; omega)
  let z := (T.rotation.next ⟨(y, x), hxy.symm⟩).snd
  have hN : Nx T y x z := ⟨hxy.symm, rfl⟩
  obtain ⟨v, -, -, -, hv5, hvc⟩ := hR m T x y z hconn htri hxy (nx_adj_right hN)
    (nx_adj_right (nx_tri htri hN).1) (Or.inl hN) hns (fun w _ _ _ => hdeg w)
  exact ⟨v, hv5, hvc⟩

end SimpleGraph.SphericalMap

#print SimpleGraph.SphericalMap.RStarNoSepTri
#check @SimpleGraph.SphericalMap.four_color_of_RStar_noSepTri
#check @SimpleGraph.SphericalMap.rStarNoSepTri_of_core
#print axioms SimpleGraph.SphericalMap.four_color_of_RStar_noSepTri
#print axioms SimpleGraph.SphericalMap.rStarNoSepTri_of_core

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"
