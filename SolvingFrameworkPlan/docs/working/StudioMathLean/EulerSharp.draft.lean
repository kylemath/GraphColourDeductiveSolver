module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalDegree
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.EulerCounting

/-!
# The sharp Euler bound for algebraic spherical maps

`SphericalMap.edge_card_bound` gives `E + 1 ≤ V + F`. Summing the mod-two
incidence over all vertices gives zero, because every edge has two ends. So the
incidence map misses a hyperplane, and the bound improves by one:
`E + 2 ≤ n + F`. No connectivity is needed. For a triangulation (all faces of
length three) this is `E ≤ 3n - 6`, which is the Euler input of the counting
lemma `StudioMath.good_card_ge_twelve`.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap

open scoped BigOperators
open Module

variable {n : ℕ} (M : SphericalMap n)

/-- Mod-two incidence into functions on all vertices. Its kernel is exactly
the set of even edge combinations. -/
noncomputable def incidenceAll : (M.graph.edgeSet → ZMod 2) →ₗ[ZMod 2]
    (Fin n → ZMod 2) where
  toFun φ x := edgeIncidence M.graph φ x
  map_add' φ ψ := by
    classical
    ext x
    simp only [Pi.add_apply]
    unfold edgeIncidence
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro e _
    split_ifs <;> simp
  map_smul' a φ := by
    classical
    ext x
    simp only [Pi.smul_apply, RingHom.id_apply]
    unfold edgeIncidence
    rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro e _
    split_ifs <;> simp

/-- The sum of all coordinates. -/
noncomputable def coordSum : (Fin n → ZMod 2) →ₗ[ZMod 2] ZMod 2 where
  toFun f := ∑ x, f x
  map_add' f g := by simp [Finset.sum_add_distrib]
  map_smul' a f := by simp [Finset.mul_sum]

/-- Every edge has exactly two ends. -/
theorem card_ends (e : M.graph.edgeSet) :
    (Finset.univ.filter fun x : Fin n => x ∈ e.val).card = 2 := by
  classical
  obtain ⟨d, rfl⟩ := RotationSystem.edge_of_dart_surjective e
  have hne : d.fst ≠ d.snd := d.adj.ne
  have : (Finset.univ.filter fun x : Fin n => x ∈ (RotationSystem.edgeOfDart d).val) =
      {d.fst, d.snd} := by
    ext x
    simp [mem_edgeOfDart_iff]
  rw [this, Finset.card_pair hne]

theorem coordSum_incidenceAll (φ : M.graph.edgeSet → ZMod 2) :
    coordSum (incidenceAll M φ) = 0 := by
  classical
  change ∑ x, edgeIncidence M.graph φ x = 0
  unfold edgeIncidence
  rw [Finset.sum_comm]
  have h : ∀ e : M.graph.edgeSet,
      (∑ x : Fin n, if x ∈ e.val then φ e else 0) = 0 := by
    intro e
    rw [← Finset.sum_filter, Finset.sum_const, card_ends M e]
    simp only [nsmul_eq_mul, Nat.cast_ofNat]
    rw [show (2 : ZMod 2) = 0 from rfl, zero_mul]
  exact Finset.sum_eq_zero (fun e _ => h e)

/-- The sharp Euler bound: `E + 2 ≤ n + F` for every algebraic spherical map
with at least one edge. -/
theorem edge_card_bound_sharp (d : M.Dart) :
    Fintype.card M.graph.edgeSet + 2 ≤ n + Fintype.card M.Face := by
  classical
  let I := incidenceAll M
  let B := boundaryLinear M
  have hker : LinearMap.ker I ≤ LinearMap.range B := by
    intro φ hφ
    have hφ' : IsEven M φ := fun x => congrFun (LinearMap.mem_ker.mp hφ) x
    obtain ⟨c, hc⟩ := even_is_face_sum M φ hφ'
    exact ⟨c, funext (fun e => (hc e).symm)⟩
  have hle := Submodule.finrank_mono hker
  have hi := I.finrank_range_add_finrank_ker
  have hb := B.finrank_range_add_finrank_ker
  -- the range of `I` lies in the kernel of the coordinate sum
  have hrange : LinearMap.range I ≤ LinearMap.ker (coordSum (n := n)) := by
    rintro _ ⟨φ, rfl⟩
    exact LinearMap.mem_ker.mpr (coordSum_incidenceAll M φ)
  have hσ := (coordSum (n := n)).finrank_range_add_finrank_ker
  have hσpos : 1 ≤ finrank (ZMod 2) (LinearMap.range (coordSum (n := n))) := by
    apply Submodule.one_le_finrank_iff.mpr
    intro hh
    have hmem : coordSum (Pi.single d.fst (1 : ZMod 2)) ∈
        LinearMap.range (coordSum (n := n)) := LinearMap.mem_range_self _ _
    rw [hh, Submodule.mem_bot] at hmem
    change ∑ x, Pi.single d.fst (1 : ZMod 2) x = 0 at hmem
    simp at hmem
  have hrle := Submodule.finrank_mono hrange
  have hnonzero : LinearMap.ker B ≠ ⊥ := by
    intro hh
    have hconst : (fun _ : M.Face => (1 : ZMod 2)) ∈ LinearMap.ker B := by
      apply LinearMap.mem_ker.mpr
      ext e
      change (1 : ZMod 2) + 1 = 0
      exact ZMod.natCast_self 2
    rw [hh] at hconst
    have hc : (fun _ : M.Face => (1 : ZMod 2)) = 0 := by simpa using hconst
    exact one_ne_zero (congrFun hc (M.faceOf d))
  have hpos : 1 ≤ finrank (ZMod 2) (LinearMap.ker B) :=
    Submodule.one_le_finrank_iff.mpr hnonzero
  simp only [Module.finrank_fintype_fun_eq_card, Fintype.card_fin] at hi hb hσ
  omega

/-- A spherical triangulation has `2E + 12 ≤ 6n`, that is, `E ≤ 3n - 6`. -/
theorem twice_edges_add_twelve_le (d : M.Dart)
    (htri : ∀ f : M.Face, M.rotation.faceLength f = 3) :
    2 * M.graph.edgeFinset.card + 12 ≤ 6 * n := by
  classical
  have hs := M.rotation.sum_face_lengths_eq_twice_card_edges
  simp only [htri, Finset.sum_const, Finset.card_univ, smul_eq_mul] at hs
  have he := edge_card_bound_sharp M d
  rw [← edgeFinset_card] at he
  omega

/-- **Euler lemma.** In a spherical triangulation of minimum degree five, at
least twelve vertices have degree five and at most one neighbour of degree at
least twelve. -/
theorem twelve_light_fives (d : M.Dart)
    (htri : ∀ f : M.Face, M.rotation.faceLength f = 3)
    (hmin : ∀ v, 5 ≤ M.graph.degree v) :
    12 ≤ (StudioMath.goodSet M.graph).card :=
  StudioMath.good_card_ge_twelve M.graph hmin
    (by simpa using twice_edges_add_twelve_le M d htri)

end SimpleGraph.SphericalMap
