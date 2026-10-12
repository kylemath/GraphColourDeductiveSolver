module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameWit22Map
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarSanity

/-!
# The frame class is non-empty: an order-22 witness

Track C, 7 Oct 2026. `FrameWit22.sphericalMap` is the triangulation at line 642 (0-based 641) of
`backgroundMaterial/planemap-structural/studiointel/gentri/tri22.txt` (4-connected
minimum-degree-five triangulations), the smallest of the six configuration-free graphs of the
orders 12–24 census (`NightConfigurationLead.md`). It has twelve vertices of degree five and ten of
degree six. As a genuine `SphericalMap` (`Fills` by the linear certificate in `FrameWit22Map`):

* it is connected and triangulated, has minimum degree five and no separating triangle;
* `diamondFree`, `conf2122Free`: no `Occ` of the Birkhoff diamond or of RSST 2.122, in either
  orientation. Every `Occ` gives an edge `int 0 ~ int 2` with two distinct common neighbours
  `int 1`, `int 3`, with the configuration's degrees; a kernel `decide` shows that no such
  quadruple exists in this map.
* `frameClass_nonempty`: the hypotheses of `RStarFrame` are satisfiable.

## Main results (sorry-free, no new axioms, no `native_decide`)

`connected`, `noSep`, `min_degree`, `diamondFree`, `conf2122Free`, `frameClass`,
`frameClass_nonempty`.
-/

@[expose] public section
namespace SimpleGraph.FrameWit22
open SphericalMap VacancyIcosahedral

theorem nx_t {u v w : Fin 22} (h : graph.Adj u v) (e : nextTable u v = w) :
    sphericalMap.Nx u v w := ⟨h, e⟩

theorem connected : sphericalMap.graph.Connected := by
  have r : ∀ v, True → graph.Reachable 0 v :=
    reachable_of_parent (G := graph) 0
      ![0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 8, 9, 11, 11, 14]
      ![0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4] (fun _ => True)
      (fun v _ hv => ⟨trivial, (by decide : ∀ v : Fin 22, v ≠ 0 →
        ![0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4]
          (![0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 8, 9, 11, 11, 14] v) <
        ![0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4] v ∧
        graph.Adj (![0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 7, 8, 9, 11, 11, 14] v) v)
        v hv⟩)
  exact Connected.mk (fun u v => (r u trivial).symm.trans (r v trivial))

theorem noSep : NoSep sphericalMap := by
  have h : ∀ x y : Fin 22, graph.Adj x y → ∀ z, graph.Adj y z → graph.Adj z x →
      nextTable y x = z ∨ nextTable x y = z := by decide
  intro x y z hxy hyz hzx
  rcases h x y hxy z hyz hzx with e | e
  · exact Or.inl (nx_t hxy.symm e)
  · exact Or.inr (nx_t hxy e)

theorem min_degree (x : Fin 22) : 5 ≤ sphericalMap.graph.degree x := by
  rw [sphericalMap_degree]; revert x; decide

/-- No edge `q ~ r` with `deg q = d`, `deg r = 5` has two distinct common neighbours of degree
five (`d = 5`: the diamond shape; `d = 6`: the 2.122 shape). -/
theorem no_shape (d : ℕ) (hd : d = 5 ∨ d = 6) : ∀ q : Fin 22, degTable q = d →
    ∀ r : Fin 22, degTable r = 5 → graph.Adj q r →
    ∀ p : Fin 22, degTable p = 5 → graph.Adj q p → graph.Adj r p →
    ∀ s : Fin 22, degTable s = 5 → graph.Adj q s → graph.Adj r s → p = s := by
  rcases hd with rfl | rfl
  · decide
  · decide

theorem shape_false {d : ℕ} (hd : d = 5 ∨ d = 6) {int : Fin 4 → Fin 22}
    (inj : Function.Injective int)
    (d0 : sphericalMap.graph.degree (int 0) = d) (d1 : sphericalMap.graph.degree (int 1) = 5)
    (d2 : sphericalMap.graph.degree (int 2) = 5) (d3 : sphericalMap.graph.degree (int 3) = 5)
    (a02 : graph.Adj (int 0) (int 2)) (a01 : graph.Adj (int 0) (int 1))
    (a21 : graph.Adj (int 2) (int 1)) (a03 : graph.Adj (int 0) (int 3))
    (a23 : graph.Adj (int 2) (int 3)) : False := by
  rw [sphericalMap_degree] at d0 d1 d2 d3
  exact absurd (inj (no_shape d hd _ d0 _ d2 a02 _ d1 a01 a21 _ d3 a03 a23)) (by decide)

/-- **No occurrence of the Birkhoff diamond.** -/
theorem diamondFree : DiamondFree sphericalMap := by
  refine ⟨fun ⟨_, int, o⟩ => ?_, fun ⟨_, int, o⟩ => ?_⟩
  · exact shape_false (Or.inl rfl) o.int_inj (o.deg 0) (o.deg 1) (o.deg 2) (o.deg 3)
      (nx_adj_left o.r0_1) (nx_adj_right o.r0_1) (nx_adj_left o.r2_4) (nx_adj_left o.r0_2)
      (nx_adj_right o.r2_3)
  · exact shape_false (Or.inl rfl) o.int_inj (o.deg 0) (o.deg 1) (o.deg 2) (o.deg 3)
      (nx_adj_right o.r0_1) (nx_adj_left o.r0_1) (nx_adj_right o.r2_4) (nx_adj_right o.r0_2)
      (nx_adj_left o.r2_3)

/-- **No occurrence of RSST 2.122.** -/
theorem conf2122Free : Conf2122Free sphericalMap := by
  refine ⟨fun ⟨_, int, o⟩ => ?_, fun ⟨_, int, o⟩ => ?_⟩
  · exact shape_false (Or.inr rfl) o.int_inj (o.deg 0) (o.deg 1) (o.deg 2) (o.deg 3)
      (nx_adj_left o.r0_2) (nx_adj_right o.r0_2) (nx_adj_left o.r2_4) (nx_adj_left o.r0_3)
      (nx_adj_right o.r2_3)
  · exact shape_false (Or.inr rfl) o.int_inj (o.deg 0) (o.deg 1) (o.deg 2) (o.deg 3)
      (nx_adj_right o.r0_2) (nx_adj_left o.r0_2) (nx_adj_right o.r2_4) (nx_adj_right o.r0_3)
      (nx_adj_left o.r2_3)

/-- `FrameWit22.sphericalMap` satisfies every hypothesis of `RStarFrame`. -/
theorem frameClass : 0 < 22 ∧ sphericalMap.graph.Connected ∧ sphericalMap.Triangulated ∧
    (∀ x, 5 ≤ sphericalMap.graph.degree x) ∧ NoSep sphericalMap ∧
    DiamondFree sphericalMap ∧ Conf2122Free sphericalMap :=
  ⟨by norm_num, connected, sphericalMap_triangulated, min_degree, noSep, diamondFree,
    conf2122Free⟩

/-- **The frame class is non-empty.** -/
theorem frameClass_nonempty : ∃ (m : ℕ) (T : SphericalMap m), 0 < m ∧ T.graph.Connected ∧
    T.Triangulated ∧ (∀ x, 5 ≤ T.graph.degree x) ∧ NoSep T ∧ DiamondFree T ∧ Conf2122Free T :=
  ⟨22, sphericalMap, frameClass⟩

end SimpleGraph.FrameWit22

#print axioms SimpleGraph.FrameWit22.diamondFree
#print axioms SimpleGraph.FrameWit22.conf2122Free
#print axioms SimpleGraph.FrameWit22.frameClass
#print axioms SimpleGraph.FrameWit22.frameClass_nonempty
