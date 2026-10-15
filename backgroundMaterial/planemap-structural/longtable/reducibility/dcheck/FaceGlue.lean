import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalMap
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.Algebra.Field.ZMod

/-! Job 26 route B, piece (i): the potential gluing lemma. On a map with `Fills` (every even edge
combination is a sum of face boundaries), an edge labelling whose sum around every face is zero is a
vertex cut: it is orthogonal to every even combination, hence (by linear duality, `ker B` against
`range Bᵀ` for the incidence map `B`) of the form `p u + p v`. Coordinate-wise over `(ZMod 2)²` a
nowhere-zero labelling with zero face sums gives a proper 4-colouring. No connectivity is needed. -/

noncomputable section
namespace SimpleGraph
open RotationSystem Classical

variable {n : ℕ} {G : SimpleGraph (Fin n)}

/-- A sum over darts, grouped by edges. -/
theorem sum_darts_eq_sum_edges (F : G.Dart → ZMod 2) :
    ∑ d, F d = ∑ e : G.edgeSet,
      (F (SphericalMap.edgeDart G e) + F (SphericalMap.edgeDart G e).symm) := by
  classical
  rw [← Fintype.sum_equiv (edgeFiberEquiv (G := G)) (fun p => F p.2.val) F (fun _ => rfl),
    Fintype.sum_sigma]
  apply Finset.sum_congr rfl
  intro e _
  have hd := SphericalMap.edgeDart_spec G e
  rw [← Fintype.sum_equiv (edgeFiberBoolEquiv e _ hd).symm (fun b => F
      ((edgeFiberBoolEquiv e _ hd).symm b).val) (fun x => F x.val) (fun _ => rfl)]
  rw [Fintype.sum_bool]
  simp [edgeFiberBoolEquiv, add_comm]

/-- The incidence map of edge combinations. -/
noncomputable def incidenceLin (G : SimpleGraph (Fin n)) :
    (G.edgeSet → ZMod 2) →ₗ[ZMod 2] (Fin n → ZMod 2) where
  toFun φ x := edgeIncidence G φ x
  map_add' φ ψ := by
    funext x
    unfold edgeIncidence
    simp only [Pi.add_apply, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro e _
    split_ifs <;> simp
  map_smul' a φ := by
    funext x
    unfold edgeIncidence
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro e _
    split_ifs <;> simp

/-- Pairing with a labelling. -/
noncomputable def pairLin (ψ : G.edgeSet → ZMod 2) : Module.Dual (ZMod 2) (G.edgeSet → ZMod 2) where
  toFun φ := ∑ e, φ e * ψ e
  map_add' φ χ := by simp [add_mul, Finset.sum_add_distrib]
  map_smul' a φ := by simp [Finset.mul_sum, mul_assoc]

theorem incidenceLin_single (d : G.Dart) :
    incidenceLin G (Pi.single (edgeOfDart d) 1) = Pi.single d.fst 1 + Pi.single d.snd 1 := by
  classical
  funext x
  change edgeIncidence G _ x = _
  unfold edgeIncidence
  rw [Finset.sum_eq_single (edgeOfDart d)]
  · have hne : d.fst ≠ d.snd := d.adj.ne
    have hmem : x ∈ (edgeOfDart d).val ↔ x = d.fst ∨ x = d.snd := by
      change x ∈ s(d.fst, d.snd) ↔ _
      exact Sym2.mem_iff
    by_cases h1 : x = d.fst
    · subst h1
      simp [hmem, Pi.single_apply, Ne.symm hne]
    · by_cases h2 : x = d.snd
      · subst h2
        simp [hmem, Pi.single_apply, hne]
      · simp [hmem, Pi.single_apply, h1, h2]
  · intro e _ he
    split_ifs <;> simp [Pi.single_apply, he]
  · simp

/-- **Gluing lemma (mod 2).** A labelling with zero sum around every face is a vertex cut. -/
theorem cut_of_face_sums (R : RotationSystem G) (hR : R.Fills) (ψ : G.edgeSet → ZMod 2)
    (hψ : ∀ f : R.Face, ∑ d ∈ Finset.univ.filter (fun d => R.faceOf d = f),
      ψ (edgeOfDart d) = 0) :
    ∃ p : Fin n → ZMod 2, ∀ d : G.Dart, ψ (edgeOfDart d) = p d.fst + p d.snd := by
  classical
  have hmem : pairLin ψ ∈ (LinearMap.ker (incidenceLin G)).dualAnnihilator := by
    rw [Submodule.mem_dualAnnihilator]
    intro φ hφ
    have heven : ∀ x, edgeIncidence G φ x = 0 := fun x => congrFun (LinearMap.mem_ker.1 hφ) x
    obtain ⟨c, hc⟩ := hR φ heven
    change ∑ e, φ e * ψ e = 0
    have h1 : ∑ e, φ e * ψ e = ∑ d, c (R.faceOf d) * ψ (edgeOfDart d) := by
      rw [sum_darts_eq_sum_edges]
      apply Finset.sum_congr rfl
      intro e _
      have hd := SphericalMap.edgeDart_spec G e
      have := hc (SphericalMap.edgeDart G e)
      rw [hd] at this
      rw [this, edge_of_dart_symm, hd, add_mul]
    rw [h1, ← Finset.sum_fiberwise Finset.univ R.faceOf]
    apply Finset.sum_eq_zero
    intro f _
    rw [Finset.sum_congr rfl (g := fun d => c f * ψ (edgeOfDart d))
      (fun d hd => by rw [(Finset.mem_filter.1 hd).2]), ← Finset.mul_sum, hψ f, mul_zero]
  haveI : Fact (Nat.Prime 2) := ⟨Nat.prime_two⟩
  have hr := LinearMap.range_dualMap_eq_dualAnnihilator_ker (K := ZMod 2) (incidenceLin G)
  have hmem' : pairLin ψ ∈ LinearMap.range (incidenceLin G).dualMap := by
    rw [hr]; convert hmem
  obtain ⟨g, hg⟩ := hmem'
  refine ⟨fun x => g (Pi.single x 1), fun d => ?_⟩
  have h2 : pairLin ψ (Pi.single (edgeOfDart d) 1) = ψ (edgeOfDart d) := by
    change ∑ e, (Pi.single (edgeOfDart d) (1 : ZMod 2) : G.edgeSet → ZMod 2) e * ψ e = _
    rw [Finset.sum_eq_single (edgeOfDart d)] <;> simp_all [Pi.single_apply]
  rw [← h2, ← hg, LinearMap.dualMap_apply, incidenceLin_single, map_add]

/-- **Gluing lemma, colour version.** A nowhere-zero `(ZMod 2)²` labelling with zero sum around every
face is the difference labelling of a proper 4-colouring. -/
theorem colouring_of_face_sums (R : RotationSystem G) (hR : R.Fills)
    (τ : G.edgeSet → ZMod 2 × ZMod 2) (hτ : ∀ e, τ e ≠ 0)
    (hface : ∀ f : R.Face, ∑ d ∈ Finset.univ.filter (fun d => R.faceOf d = f),
      τ (edgeOfDart d) = 0) :
    ∃ κ : Fin n → ZMod 2 × ZMod 2, (∀ d : G.Dart, τ (edgeOfDart d) = κ d.fst + κ d.snd) ∧
      ∀ u v, G.Adj u v → κ u ≠ κ v := by
  classical
  obtain ⟨p, hp⟩ := cut_of_face_sums R hR (fun e => (τ e).1) (fun f => by
    have := congrArg Prod.fst (hface f); simpa [Prod.fst_sum] using this)
  obtain ⟨q, hq⟩ := cut_of_face_sums R hR (fun e => (τ e).2) (fun f => by
    have := congrArg Prod.snd (hface f); simpa [Prod.snd_sum] using this)
  have hκ : ∀ d : G.Dart, τ (edgeOfDart d) = (p d.fst, q d.fst) + (p d.snd, q d.snd) :=
    fun d => Prod.ext (hp d) (hq d)
  refine ⟨fun x => (p x, q x), hκ, fun u v h huv => ?_⟩
  apply hτ (edgeOfDart ⟨(u, v), h⟩)
  rw [hκ]
  change (p u, q u) + (p v, q v) = 0
  have huv' : (p u, q u) = (p v, q v) := huv
  rw [huv']
  exact Prod.ext (by simp [CharTwo.add_self_eq_zero]) (by simp [CharTwo.add_self_eq_zero])

end SimpleGraph
end

#print axioms SimpleGraph.colouring_of_face_sums
