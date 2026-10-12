module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FrameAppears
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFloor

/-!
# Scope of the hole theorems: `555` and `565` link runs are configuration appearances

Track C, 7 Oct 2026 (`TrackD/PartialResultsPaper.md` §6.4). Let `h` be a degree-five vertex of a
triangulation with no separating triangle, with pentagonal link `P` (`x 0, …, x 4`).

* `tips_not_adj`: two link vertices `x j`, `x (j+2)` are not adjacent. (All three triangles
  `h x j x (j+1)`, `h x (j+1) x (j+2)`, `h x j x (j+2)` would be facial, so the rotation at `h`
  would contain a 3-cycle, contradicting degree five. Minimum degree five is not used.)
* `appears_diamond_of_run`: if `x j, x (j+1), x (j+2)` have degree five, then
  `![h, x j, x (j+1), x (j+2)]` is an `Appears ![5,5,5,5]` (centres `h`, `x (j+1)`).
* `appears_c2122_of_run`: if `x j, x (j+2)` have degree five and `x (j+1)` degree six, then
  `![x (j+1), x j, h, x (j+2)]` is an `Appears ![6,5,5,5]` (degree-six centre `x (j+1)`).
* Under `LinkTipsClean P j` (every common neighbour of `x j` and `x (j+2)` is `h` or `x (j+1)`)
  these give an `Occ` (`occ_diamond_of_run`, `occ_c2122_of_run`), so a `DiamondFree`
  (resp. `Conf2122Free`) map has no such run with clean tips (`no_555_run`, `no_565_run`).

## Main results (sorry-free, no new axioms)

`tips_not_adj`, `appears_diamond_of_run`, `appears_c2122_of_run`, `occ_diamond_of_run`,
`occ_c2122_of_run`, `no_555_run`, `no_565_run`.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap.FrameScope
open VacancyIcosahedral QuarterFloor

variable {n : ℕ} {T : SphericalMap n}

/-- On a triangulation, `Nx u · w` is injective. -/
theorem nx_inj (htri : T.Triangulated) {u a b w : Fin n} (ha : Nx T u a w) (hb : Nx T u b w) :
    a = b :=
  nx_func (nx_tri htri ha).1 (nx_tri htri hb).1

/-- With `NoSep`, a triangle through `h` is consecutive in the rotation at `h`. -/
theorem facial_at (htri : T.Triangulated) (hns : NoSep T) {h a b : Fin n}
    (hha : T.Adj h a) (hab : T.Adj a b) (hbh : T.Adj b h) : Nx T h a b ∨ Nx T h b a := by
  rcases hns h a b hha hab hbh with e | e
  · exact Or.inr (nx_tri htri e).2
  · exact Or.inl e

/-- At a degree-five vertex `h` of a `NoSep` triangulation, if `h a m b` is a path of
neighbours (`a ~ m ~ b`), then `a` and `b` are not adjacent. -/
theorem tips_not_adj (htri : T.Triangulated) (hns : NoSep T) {h a m b : Fin n}
    (hdeg : T.graph.degree h = 5) (hha : T.Adj h a) (hhm : T.Adj h m) (hhb : T.Adj h b)
    (ham : T.Adj a m) (hmb : T.Adj m b) (nab : a ≠ b) (nam : a ≠ m) (nmb : m ≠ b) :
    ¬ T.Adj a b := by
  intro hab
  rcases facial_at htri hns hha ham hhm.symm with A | A <;>
  rcases facial_at htri hns hhm hmb hhb.symm with B | B <;>
  rcases facial_at htri hns hha hab hhb.symm with C | C <;>
  first
  | exact nmb (nx_func A C)
  | exact (chain5 hdeg A B C A).2.1.2.2.1 rfl
  | exact nab (nx_inj htri A B)
  | exact nab (nx_func A B)
  | exact (chain5 hdeg B A C B).2.1.2.2.1 rfl
  | exact nam (nx_func B C).symm

theorem fin5_ne : ∀ j : Fin 5, j ≠ j + 1 ∧ j ≠ j + 2 ∧ j + 1 ≠ j + 2 := by decide

theorem fin5_add : ∀ j : Fin 5, j + 1 + 1 = j + 2 := by decide

variable {h : Fin n} (P : Pent T.graph h)

/-- Every common neighbour of the link vertices `x j` and `x (j+2)` is `h` or `x (j+1)`. -/
def LinkTipsClean (j : Fin 5) : Prop :=
  ∀ y, T.Adj (P.x j) y → T.Adj (P.x (j + 2)) y → y = h ∨ y = P.x (j + 1)

theorem link_adj_succ (j : Fin 5) : T.Adj (P.x (j + 1)) (P.x (j + 2)) := by
  have := P.adj_cyc (j + 1)
  rwa [fin5_add] at this

theorem link_tips_not_adj (htri : T.Triangulated) (hns : NoSep T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) : ¬ T.Adj (P.x j) (P.x (j + 2)) := by
  obtain ⟨e1, e2, e3⟩ := fin5_ne j
  exact tips_not_adj htri hns hdeg (P.adj_h j) (P.adj_h (j + 1)) (P.adj_h (j + 2))
    (P.adj_cyc j) (link_adj_succ P j) (fun e => e2 (P.inj e)) (fun e => e1 (P.inj e))
    (fun e => e3 (P.inj e))

/-- A `555` link run at a degree-five vertex is an appearance of the Birkhoff diamond. -/
theorem appears_diamond_of_run (htri : T.Triangulated) (hns : NoSep T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) (d0 : T.graph.degree (P.x j) = 5)
    (d1 : T.graph.degree (P.x (j + 1)) = 5) (d2 : T.graph.degree (P.x (j + 2)) = 5) :
    Appears ![5, 5, 5, 5] T ![h, P.x j, P.x (j + 1), P.x (j + 2)] := by
  obtain ⟨e1, e2, e3⟩ := fin5_ne j
  have n01 : h ≠ P.x j := (P.adj_h j).ne
  have n02 : h ≠ P.x (j + 1) := (P.adj_h (j + 1)).ne
  have n03 : h ≠ P.x (j + 2) := (P.adj_h (j + 2)).ne
  have n12 : P.x j ≠ P.x (j + 1) := fun e => e1 (P.inj e)
  have n13 : P.x j ≠ P.x (j + 2) := fun e => e2 (P.inj e)
  have n23 : P.x (j + 1) ≠ P.x (j + 2) := fun e => e3 (P.inj e)
  refine ⟨?_, P.adj_h j, P.adj_h (j + 1), P.adj_h (j + 2), P.adj_cyc j, link_adj_succ P j,
    link_tips_not_adj P htri hns hdeg j, ?_⟩
  · intro s t hst
    fin_cases s <;> fin_cases t <;>
      first | rfl | exact absurd hst ‹_› | exact absurd hst.symm ‹_›
  · intro a
    fin_cases a
    exacts [hdeg, d0, d1, d2]

/-- A `565` link run at a degree-five vertex is an appearance of RSST 2.122. -/
theorem appears_c2122_of_run (htri : T.Triangulated) (hns : NoSep T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) (d0 : T.graph.degree (P.x j) = 5)
    (d1 : T.graph.degree (P.x (j + 1)) = 6) (d2 : T.graph.degree (P.x (j + 2)) = 5) :
    Appears ![6, 5, 5, 5] T ![P.x (j + 1), P.x j, h, P.x (j + 2)] := by
  obtain ⟨e1, e2, e3⟩ := fin5_ne j
  have n01 : P.x (j + 1) ≠ P.x j := fun e => e1 (P.inj e).symm
  have n02 : P.x (j + 1) ≠ h := (P.adj_h (j + 1)).ne.symm
  have n03 : P.x (j + 1) ≠ P.x (j + 2) := fun e => e3 (P.inj e)
  have n12 : P.x j ≠ h := (P.adj_h j).ne.symm
  have n13 : P.x j ≠ P.x (j + 2) := fun e => e2 (P.inj e)
  have n23 : h ≠ P.x (j + 2) := (P.adj_h (j + 2)).ne
  refine ⟨?_, (P.adj_cyc j).symm, (P.adj_h (j + 1)).symm, link_adj_succ P j, (P.adj_h j).symm,
    P.adj_h (j + 2), link_tips_not_adj P htri hns hdeg j, ?_⟩
  · intro s t hst
    fin_cases s <;> fin_cases t <;>
      first | rfl | exact absurd hst ‹_› | exact absurd hst.symm ‹_›
  · intro a
    fin_cases a
    exacts [d1, d0, hdeg, d2]

/-- A `555` run with clean tips is an occurrence of the diamond. -/
theorem occ_diamond_of_run (htri : T.Triangulated) (hns : NoSep T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) (d0 : T.graph.degree (P.x j) = 5)
    (d1 : T.graph.degree (P.x (j + 1)) = 5) (d2 : T.graph.degree (P.x (j + 2)) = 5)
    (htip : LinkTipsClean P j) :
    (∃ ring, DiamondM.Occ T ring ![h, P.x j, P.x (j + 1), P.x (j + 2)]) ∨
      (∃ ring, DiamondP.Occ T ring ![h, P.x j, P.x (j + 1), P.x (j + 2)]) :=
  DiamondAppears.occ_of_appears htri hns (appears_diamond_of_run P htri hns hdeg j d0 d1 d2)
    (fun y h1 h3 => htip y h1 h3)

/-- A `565` run with clean tips is an occurrence of 2.122. -/
theorem occ_c2122_of_run (htri : T.Triangulated) (hns : NoSep T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) (d0 : T.graph.degree (P.x j) = 5)
    (d1 : T.graph.degree (P.x (j + 1)) = 6) (d2 : T.graph.degree (P.x (j + 2)) = 5)
    (htip : LinkTipsClean P j) :
    (∃ ring, C2122M.Occ T ring ![P.x (j + 1), P.x j, h, P.x (j + 2)]) ∨
      (∃ ring, C2122P.Occ T ring ![P.x (j + 1), P.x j, h, P.x (j + 2)]) :=
  C2122Appears.occ_of_appears htri hns (appears_c2122_of_run P htri hns hdeg j d0 d1 d2)
    (fun y h1 h3 => (htip y h1 h3).symm)

/-- **No `555` link run with clean tips in a `DiamondFree` map** (in particular in the frame
class). -/
theorem no_555_run (htri : T.Triangulated) (hns : NoSep T) (hD : DiamondFree T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) (htip : LinkTipsClean P j) :
    ¬ (T.graph.degree (P.x j) = 5 ∧ T.graph.degree (P.x (j + 1)) = 5 ∧
      T.graph.degree (P.x (j + 2)) = 5) := by
  rintro ⟨d0, d1, d2⟩
  rcases occ_diamond_of_run P htri hns hdeg j d0 d1 d2 htip with ⟨r, o⟩ | ⟨r, o⟩
  · exact hD.1 ⟨r, _, o⟩
  · exact hD.2 ⟨r, _, o⟩

/-- **No `565` link run with clean tips in a `Conf2122Free` map.** -/
theorem no_565_run (htri : T.Triangulated) (hns : NoSep T) (hC : Conf2122Free T)
    (hdeg : T.graph.degree h = 5) (j : Fin 5) (htip : LinkTipsClean P j) :
    ¬ (T.graph.degree (P.x j) = 5 ∧ T.graph.degree (P.x (j + 1)) = 6 ∧
      T.graph.degree (P.x (j + 2)) = 5) := by
  rintro ⟨d0, d1, d2⟩
  rcases occ_c2122_of_run P htri hns hdeg j d0 d1 d2 htip with ⟨r, o⟩ | ⟨r, o⟩
  · exact hC.1 ⟨r, _, o⟩
  · exact hC.2 ⟨r, _, o⟩

end SimpleGraph.SphericalMap.FrameScope

#print axioms SimpleGraph.SphericalMap.FrameScope.tips_not_adj
#print axioms SimpleGraph.SphericalMap.FrameScope.appears_diamond_of_run
#print axioms SimpleGraph.SphericalMap.FrameScope.appears_c2122_of_run
#print axioms SimpleGraph.SphericalMap.FrameScope.occ_diamond_of_run
#print axioms SimpleGraph.SphericalMap.FrameScope.occ_c2122_of_run
#print axioms SimpleGraph.SphericalMap.FrameScope.no_555_run
#print axioms SimpleGraph.SphericalMap.FrameScope.no_565_run
