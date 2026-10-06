module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameF3

/-!
# Sanity checks: the formal R\* predicate on concrete maps

These evaluate the formal definitions on concrete maps, to rule out a vacuous or mismatched
definition.

* **Icosahedron.** It lies in the class of `RStarNoSepTri` (connected, triangulated, minimum
  degree five, no separating triangle), and every vertex is pure-clean, so R\* holds there.
  Both orientations of the Birkhoff diamond occur in it (`DiamondM.Occ`, `DiamondP.Occ` hold for
  explicit labellings), so the occurrence predicate is not vacuous and the icosahedron lies outside
  the class of `RStarFrame`. RSST 2.122 does not occur (it needs a vertex of degree six).
* **Certificate tools** for `RadiusFive`: a whole Kempe component certified by closure and a
  parent tree (`whole_of_cert`), and a swap computed pointwise (`swap_eq`).
-/

@[expose] public section

namespace SimpleGraph

/-- Reachability from a root along a parent function with decreasing rank. -/
theorem reachable_of_parent {V : Type*} {G : SimpleGraph V} (s : V) (par : V → V) (rk : V → ℕ)
    (P : V → Prop) (h : ∀ v, P v → v ≠ s → P (par v) ∧ rk (par v) < rk v ∧ G.Adj (par v) v) :
    ∀ v, P v → G.Reachable s v := by
  intro v
  induction hv : rk v using Nat.strong_induction_on generalizing v with
  | _ k ih =>
    intro hP
    by_cases e : v = s
    · subst e; rfl
    · obtain ⟨hp, hr, ha⟩ := h v hP e
      exact (ih _ (hv ▸ hr) _ rfl hp).trans ha.reachable

namespace VacancyShortFill
variable {V : Type*} [DecidableEq V] {G : SimpleGraph V}

/-- A whole two-colour component, certified by closure under the pair graph and a parent tree. -/
theorem whole_of_cert {h : V} {c : V → Fin 4} {a b : Fin 4} (s : V) (S : Finset V)
    (hs : s ≠ h ∧ (c s = a ∨ c s = b)) (hsS : s ∈ S)
    (closed : ∀ u v, G.Adj u v → u ≠ h ∧ (c u = a ∨ c u = b) → v ≠ h ∧ (c v = a ∨ c v = b) →
      u ∈ S → v ∈ S)
    (par : V → V) (rk : V → ℕ)
    (tree : ∀ v, v ∈ S → v ≠ s → par v ∈ S ∧ rk (par v) < rk v ∧ G.Adj (par v) v ∧
      (par v ≠ h ∧ (c (par v) = a ∨ c (par v) = b)) ∧ (v ≠ h ∧ (c v = a ∨ c v = b))) :
    Whole G h c a b ↑S := by
  refine ⟨s, hs, fun v => ⟨fun hv => ?_, fun hr => ?_⟩⟩
  · refine reachable_of_parent (G := pairGraph G h c a b) s par rk (· ∈ S)
      (fun w hw hne => ?_) v hv
    obtain ⟨h1, h2, h3, h4, h5⟩ := tree w hw hne
    exact ⟨h1, h2, h3, h4, h5⟩
  · exact reachable_invariant (H := pairGraph G h c a b) (P := (· ∈ S))
      (fun u w ⟨e, au, aw⟩ hu => closed u w e au aw hu) hsS hr

/-- A swap computed pointwise. -/
theorem swap_eq (c d : V → Fin 4) (a b : Fin 4) (S : Finset V)
    (hd : ∀ v, d v = if v ∈ S then Equiv.swap a b (c v) else c v) : d = swap c a b ↑S := by
  funext v
  rw [hd v]
  unfold swap
  by_cases hv : v ∈ S <;> simp [hv]

end VacancyShortFill

namespace Icosahedron
open VacancySlide VacancyShortFill VacancyIcosahedral SphericalMap

theorem nx_ico {u v w : Fin 12} (h : graph.Adj u v) (e : nextTable u v = w) :
    sphericalMap.Nx u v w := ⟨h, e⟩

theorem connected : sphericalMap.graph.Connected := by
  have r : ∀ v, True → graph.Reachable 0 v :=
    reachable_of_parent (G := graph) 0 ![0, 0, 1, 2, 5, 0, 1, 0, 0, 8, 7, 0]
      ![0, 1, 2, 3, 2, 1, 2, 1, 1, 2, 2, 1] (fun _ => True)
      (fun v _ hv => ⟨trivial, (by decide : ∀ v : Fin 12, v ≠ 0 →
        ![0, 1, 2, 3, 2, 1, 2, 1, 1, 2, 2, 1] (![0, 0, 1, 2, 5, 0, 1, 0, 0, 8, 7, 0] v) <
          ![0, 1, 2, 3, 2, 1, 2, 1, 1, 2, 2, 1] v ∧
        graph.Adj (![0, 0, 1, 2, 5, 0, 1, 0, 0, 8, 7, 0] v) v) v hv⟩)
  exact Connected.mk (fun u v => (r u trivial).symm.trans (r v trivial))

theorem noSep : NoSep sphericalMap := by
  have h : ∀ x y : Fin 12, graph.Adj x y → ∀ z, graph.Adj y z → graph.Adj z x →
      nextTable y x = z ∨ nextTable x y = z := by decide
  intro x y z hxy hyz hzx
  rcases h x y hxy z hyz hzx with e | e
  · exact Or.inl (nx_ico hxy.symm e)
  · exact Or.inr (nx_ico hxy e)

theorem noSeparatingTriangleAt (v : Fin 12) : sphericalMap.NoSeparatingTriangleAt v := by
  have h : ∀ v u w : Fin 12, graph.Adj v u → graph.Adj v w → graph.Adj u w →
      nextTable v u = w ∨ nextTable v w = u := by decide
  intro u w hu hw huw
  rcases h v u w hu hw huw with e | e
  · left; apply Dart.ext; exact Prod.ext rfl e
  · right; apply Dart.ext; exact Prod.ext rfl e

/-- **The icosahedron lies in the class of `RStarNoSepTri`.** -/
theorem mem_class : 0 < 12 ∧ sphericalMap.graph.Connected ∧ sphericalMap.Triangulated ∧
    (∀ x, 5 ≤ sphericalMap.graph.degree x) ∧ NoSep sphericalMap :=
  ⟨by norm_num, connected, sphericalMap_triangulated,
    fun x => (sphericalMap_degree x).ge, noSep⟩

/-- **R\* holds on the icosahedron, at every vertex.** -/
theorem pureClean (v : Fin 12) : PureClean sphericalMap v :=
  pureClean_of_theorem_H sphericalMap sphericalMap_triangulated (sphericalMap_degree v)
    (fun u _ => sphericalMap_degree u) (noSeparatingTriangleAt v)

theorem rStar_conclusion : ∃ v, sphericalMap.graph.degree v = 5 ∧ PureClean sphericalMap v :=
  ⟨0, sphericalMap_degree 0, pureClean 0⟩
/-- The Birkhoff diamond occurs in the icosahedron (`DiamondM`). -/
theorem occ_DiamondM : DiamondM.Occ sphericalMap ![11, 5, 6, 2, 9, 10] ![0, 1, 8, 7] where
  ring_inj := by decide
  int_inj := by decide
  disj := by decide
  deg := fun a => by rw [sphericalMap_degree]; revert a; decide
  r0_0 := nx_ico (by decide) rfl
  r0_1 := nx_ico (by decide) rfl
  r0_2 := nx_ico (by decide) rfl
  r0_3 := nx_ico (by decide) rfl
  r0_4 := nx_ico (by decide) rfl
  r1_0 := nx_ico (by decide) rfl
  r1_1 := nx_ico (by decide) rfl
  r1_2 := nx_ico (by decide) rfl
  r1_3 := nx_ico (by decide) rfl
  r1_4 := nx_ico (by decide) rfl
  r2_0 := nx_ico (by decide) rfl
  r2_1 := nx_ico (by decide) rfl
  r2_2 := nx_ico (by decide) rfl
  r2_3 := nx_ico (by decide) rfl
  r2_4 := nx_ico (by decide) rfl
  r3_0 := nx_ico (by decide) rfl
  r3_1 := nx_ico (by decide) rfl
  r3_2 := nx_ico (by decide) rfl
  r3_3 := nx_ico (by decide) rfl
  r3_4 := nx_ico (by decide) rfl

/-- The Birkhoff diamond occurs in the icosahedron (`DiamondP`). -/
theorem occ_DiamondP : DiamondP.Occ sphericalMap ![5, 11, 10, 9, 2, 6] ![0, 7, 8, 1] where
  ring_inj := by decide
  int_inj := by decide
  disj := by decide
  deg := fun a => by rw [sphericalMap_degree]; revert a; decide
  r0_0 := nx_ico (by decide) rfl
  r0_1 := nx_ico (by decide) rfl
  r0_2 := nx_ico (by decide) rfl
  r0_3 := nx_ico (by decide) rfl
  r0_4 := nx_ico (by decide) rfl
  r1_0 := nx_ico (by decide) rfl
  r1_1 := nx_ico (by decide) rfl
  r1_2 := nx_ico (by decide) rfl
  r1_3 := nx_ico (by decide) rfl
  r1_4 := nx_ico (by decide) rfl
  r2_0 := nx_ico (by decide) rfl
  r2_1 := nx_ico (by decide) rfl
  r2_2 := nx_ico (by decide) rfl
  r2_3 := nx_ico (by decide) rfl
  r2_4 := nx_ico (by decide) rfl
  r3_0 := nx_ico (by decide) rfl
  r3_1 := nx_ico (by decide) rfl
  r3_2 := nx_ico (by decide) rfl
  r3_3 := nx_ico (by decide) rfl
  r3_4 := nx_ico (by decide) rfl

/-- **The icosahedron is not diamond-free**, so it lies outside the class of `RStarFrame`. -/
theorem not_diamondFree : ¬ DiamondFree sphericalMap := fun h => h.1 ⟨_, _, occ_DiamondM⟩

/-- RSST 2.122 does not occur in the icosahedron: it needs a vertex of degree six. -/
theorem conf2122Free : Conf2122Free sphericalMap := by
  refine ⟨fun ⟨_, int, h⟩ => ?_, fun ⟨_, int, h⟩ => ?_⟩
  · have := h.deg 0; rw [sphericalMap_degree] at this; exact absurd this (by decide)
  · have := h.deg 0; rw [sphericalMap_degree] at this; exact absurd this (by decide)

end Icosahedron
end SimpleGraph
