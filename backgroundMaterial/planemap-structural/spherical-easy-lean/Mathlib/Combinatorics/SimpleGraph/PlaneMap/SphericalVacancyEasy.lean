module
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FourColorExtension
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyEasyNeighbour
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobility
@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyEasyNeighbour
variable {n : ℕ} {M : SphericalMap n}

private lemma pair_reach_induce {h u v : Fin n} {c : Fin n → Fin 4} {a b : Fin 4}
    (hu : Active h c a b u) (hv : Active h c a b v)
    (reach : (pairGraph M.graph h c a b).Reachable u v) :
    (M.graph.induce {z | Active h c a b z}).Reachable ⟨u,hu⟩ ⟨v,hv⟩ := by
  obtain ⟨p⟩ := reach
  induction p with
  | nil => exact Reachable.rfl
  | @cons u w v edge p ih =>
    obtain ⟨q⟩ := ih edge.2.2 hv
    exact ⟨.cons (v := ⟨w,edge.2.2⟩) (by exact edge.1) q⟩

/-- Actual original-hole fill by zero or one whole Kempe component swap.
The spherical separation hypothesis is supplied by the existing native carrier. -/
theorem vacancy_easy_degree_four (h : Fin n) (degree : M.graph.degree h ≤ 4) :
    EasyAt (C := Fin 4) M.graph h := by
  classical
  intro c proper
  by_cases small : ((M.graph.neighborFinset h).image c).card ≤ 3
  · left
    have fewer : ((M.graph.neighborFinset h).image c).card <
        (Finset.univ : Finset (Fin 4)).card := by simpa using (show _ < 4 by omega)
    obtain ⟨a,_,ha⟩ := Finset.exists_mem_notMem_of_card_lt_card fewer
    refine ⟨a,?_⟩
    intro v adj eq
    exact ha (Finset.mem_image.mpr ⟨v,(by simpa [mem_neighborFinset] using adj),eq⟩)
  · have imageBound : ((M.graph.neighborFinset h).image c).card ≤ M.graph.degree h :=
      Finset.card_image_le
    have four : M.graph.degree h = 4 := by omega
    have equalCard : ((M.graph.neighborFinset h).image c).card =
        (M.graph.neighborFinset h).card := by rw [card_neighborFinset_eq_degree]; omega
    have injective := Finset.injOn_of_card_image_eq equalCard
    obtain ⟨e,rotation⟩ := degree_four_neighbour_rotation h four
    let v : Fin 4 → Fin n := fun i => (e i).val
    have adj (i : Fin 4) : M.Adj h (v i) := (e i).property
    have colors : Function.Injective (fun i => c (v i)) := by
      intro i j equal
      apply e.injective
      apply Subtype.ext
      exact injective (by simp)
        (by simp) equal
    have next (i : Fin 4) : M.rotation.next ⟨(h,v i),adj i⟩ =
        ⟨(h,v (i+1)),adj (i+1)⟩ := rotation i
    have unique (i : Fin 4) : UniqueAt M.graph h (v i) c := by
      intro z hz equal
      obtain ⟨j,hj⟩ := e.surjective ⟨z,hz⟩
      have vz : v j = z := congrArg Subtype.val hj
      have ji : j = i := colors (by simpa [vz] using equal)
      exact vz.symm.trans (congrArg v ji)
    have opposite : (pairGraph M.graph h c (c (v 0)) (c (v 2))).Reachable (v 0) (v 2) →
        ¬ (pairGraph M.graph h c (c (v 1)) (c (v 3))).Reachable (v 1) (v 3) := by
      intro r02 r13
      exact four_colour_hopposite c h v adj next colors
        (pair_reach_induce ⟨(adj 0).ne.symm,Or.inl rfl⟩
          ⟨(adj 2).ne.symm,Or.inr rfl⟩ r02)
        (pair_reach_induce ⟨(adj 1).ne.symm,Or.inl rfl⟩
          ⟨(adj 3).ne.symm,Or.inr rfl⟩ r13)
    have fill (i j : Fin 4) (ne : i ≠ j)
        (separate : ¬ (pairGraph M.graph h c (c (v i)) (c (v j))).Reachable (v i) (v j)) :
        ∃ d, KempeStep M.graph h c d ∧ Target M.graph h d := by
      obtain ⟨d,step,_,target⟩ := one_swap_target M.graph proper (adj i) (unique i)
        (colors.ne ne) (fun z hz equal => by
          have zi : z = v j := unique j hz equal
          simpa [zi] using separate)
      exact ⟨d,step,target⟩
    right
    by_cases r02 : (pairGraph M.graph h c (c (v 0)) (c (v 2))).Reachable (v 0) (v 2)
    · exact fill 1 3 (by decide) (opposite r02)
    · exact fill 0 2 (by decide) r02

/-- A chosen singleton neighbour of degree at most four yields at most two
actual Kempe swaps at the original hole; the auxiliary hole is eliminated. -/
theorem vacancy_singleton_easy {h u : Fin n} {c : Fin n → Fin 4}
    (proper : ProperOff M.graph h c) (adj : M.Adj h u)
    (unique : UniqueAt M.graph h u c) (degree : M.graph.degree u ≤ 4) :
    PureFill M.graph h c 2 := by
  classical
  exact singleton_easy M.graph proper adj unique (vacancy_easy_degree_four u degree)

/-- Every intermediate hole of the actual replacement stays at the original
vertex, including when the easy neighbour belongs to the protected set. -/
theorem vacancy_singleton_easy_protected {h u : Fin n} {c : Fin n → Fin 4}
    (Z : Set (Fin n)) (proper : ProperOff M.graph h c) (outside : h ∉ Z)
    (adj : M.Adj h u) (unique : UniqueAt M.graph h u c)
    (degree : M.graph.degree u ≤ 4) :
    ∃ k, k ≤ 2 ∧ ∃ d, PurePath M.graph h k c d ∧
      VacancyCliqueLift.ProtectedPath M.graph Set.univ Z k (h,c) (h,d) ∧
      ProperOff M.graph h d ∧ Target M.graph h d := by
  classical
  exact pure_fill_protected M.graph proper outside
    (vacancy_singleton_easy proper adj unique degree)

/-- An actual optional Kempe prefix exposing a slide to an easy neighbour
has an original-hole replacement by at most three actual swaps. -/
theorem vacancy_approach_easy {h u : Fin n} {c : Fin n → Fin 4}
    (proper : ProperOff M.graph h c) (approach : VacancyMobility.Approach M.graph h c u)
    (degree : M.graph.degree u ≤ 4) : PureFill M.graph h c 3 := by
  classical
  obtain ⟨d,first,_,adj,unique⟩ := approach
  rcases first with equal | step
  · subst d
    exact pureFill_mono M.graph (vacancy_singleton_easy proper adj unique degree) (by decide)
  · exact prepend_kempe M.graph step
      (vacancy_singleton_easy (kempe_proper M.graph proper step) adj unique degree)

/-- Native geometric integration of mobility and M3 in the normalized gap
case. Word rotation and colour-renaming transport are not premises hidden here. -/
theorem vacancy_gap_easy {h u : Fin n} {c : Fin n → Fin 4}
    (L : VacancyMobility.FiveLink M.graph h) (proper : ProperOff M.graph h c)
    (pattern : VacancyMobility.Pattern M.graph L c)
    (rotation : ∀ i : Fin 5,
      M.rotation.next ⟨(h,L.port i),VacancyMobility.port_adj M.graph L i⟩ =
        ⟨(h,L.port (i+1)),VacancyMobility.port_adj M.graph L (i+1)⟩)
    (adj : M.Adj h u) (degree : M.graph.degree u ≤ 4) :
    PureFill M.graph h c 3 := by
  classical
  rcases vacancy_mobility_normalized M L proper pattern rotation with fill | access
  · exact pureFill_mono M.graph fill (by decide)
  · exact vacancy_approach_easy proper (access u adj) degree

end SimpleGraph.SphericalMap
