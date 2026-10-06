module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalDegree
public import Mathlib.Combinatorics.Enumerative.DoubleCounting
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron

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

section Counting
open Finset

namespace StudioMath

variable {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]

/-- vertices of degree at least 12 -/
def highSet : Finset V := univ.filter fun v => 12 ≤ G.degree v

/-- degree-5 vertices with at most one neighbour of degree ≥ 12 -/
def goodSet : Finset V :=
  univ.filter fun v => G.degree v = 5 ∧ ((highSet G).filter (G.Adj v)).card ≤ 1

theorem good_card_ge_twelve (hmin : ∀ v, 5 ≤ G.degree v)
    (hE : 2 * G.edgeFinset.card + 12 ≤ 6 * Fintype.card V) :
    12 ≤ (goodSet G).card := by
  classical
  set H := highSet G with hH
  set A : Finset V := univ.filter fun v => G.degree v = 5 with hA
  set B : Finset V := A.filter fun v => 2 ≤ (H.filter (G.Adj v)).card with hB
  have hgood : goodSet G = A.filter fun v => ¬ 2 ≤ (H.filter (G.Adj v)).card := by
    ext v; simp [goodSet, hA, ← hH]
  have hsplit : (goodSet G).card + B.card = A.card := by
    rw [hgood, hB, add_comm]; exact Finset.card_filter_add_card_filter_not _
  -- Claim 1
  have hB_le_A : B ⊆ A := Finset.filter_subset _ _
  have hdc := Finset.sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow (s := B) (t := H) G.Adj
  have h1 : 2 * B.card ≤ ∑ h ∈ H, G.degree h := by
    calc 2 * B.card = ∑ _b ∈ B, 2 := by simp [mul_comm]
      _ ≤ ∑ b ∈ B, (H.bipartiteAbove G.Adj b).card := by
          apply Finset.sum_le_sum
          intro b hb
          have := (Finset.mem_filter.mp hb).2
          simpa [Finset.bipartiteAbove] using this
      _ = ∑ h ∈ H, (B.bipartiteBelow G.Adj h).card := hdc
      _ ≤ ∑ h ∈ H, G.degree h := by
          apply Finset.sum_le_sum
          intro h _
          rw [← G.card_neighborFinset_eq_degree]
          apply Finset.card_le_card
          intro b hb
          have := (Finset.mem_filter.mp hb).2
          simpa [SimpleGraph.mem_neighborFinset, G.adj_comm] using this
  have h2 : ∑ h ∈ H, G.degree h ≤ 2 * ∑ h ∈ H, ((G.degree h : ℤ) - 6).toNat := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro h hh
    have : 12 ≤ G.degree h := (Finset.mem_filter.mp hh).2
    omega
  -- Claim 2
  have hdeg : ∑ v, G.degree v = 2 * G.edgeFinset.card := G.sum_degrees_eq_twice_card_edges
  have hpt : ∀ v, ((G.degree v : ℤ) - 6) ≥
      -(if G.degree v = 5 then (1:ℤ) else 0) + (if v ∈ H then (G.degree v : ℤ) - 6 else 0) := by
    intro v
    have := hmin v
    by_cases h5 : G.degree v = 5
    · have : v ∉ H := by simp [hH, highSet]; omega
      simp [h5, this]
    · by_cases hv : v ∈ H
      · simp [h5, hv]
      · simp [h5, hv]; omega
  have hsum := Finset.sum_le_sum (s := univ) (fun v _ => hpt v)
  rw [Finset.sum_add_distrib, Finset.sum_neg_distrib] at hsum
  have e1 : ∑ v, (if G.degree v = 5 then (1:ℤ) else 0) = (A.card : ℤ) := by
    simp [hA, Finset.sum_boole]
  have e2 : ∑ v, (if v ∈ H then (G.degree v : ℤ) - 6 else 0) =
      ∑ h ∈ H, ((G.degree h : ℤ) - 6) := by
    rw [← Finset.sum_filter]; congr 1; ext v; simp
  have e3 : ∑ v, ((G.degree v : ℤ) - 6) = 2 * (G.edgeFinset.card : ℤ) - 6 * (Fintype.card V : ℤ) := by
    rw [Finset.sum_sub_distrib]
    have : ((∑ v, G.degree v : ℕ) : ℤ) = ∑ v, (G.degree v : ℤ) := by push_cast; rfl
    rw [← this, hdeg]; simp [mul_comm]
  have e4 : ∑ h ∈ H, ((G.degree h : ℤ) - 6) = ((∑ h ∈ H, ((G.degree h : ℤ) - 6).toNat : ℕ) : ℤ) := by
    push_cast
    apply Finset.sum_congr rfl
    intro h hh
    have : 12 ≤ G.degree h := (Finset.mem_filter.mp hh).2
    omega
  rw [e1, e2, e3, e4] at hsum
  have hE' : 2 * (G.edgeFinset.card : ℤ) + 12 ≤ 6 * (Fintype.card V : ℤ) := by exact_mod_cast hE
  have hs : (∑ h ∈ H, G.degree h : ℤ) ≤ 2 * (∑ h ∈ H, ((G.degree h : ℤ) - 6).toNat : ℕ) := by
    exact_mod_cast h2
  have h1' : (2 * B.card : ℤ) ≤ (∑ h ∈ H, G.degree h : ℕ) := by exact_mod_cast h1
  have hsplit' : ((goodSet G).card : ℤ) + B.card = A.card := by exact_mod_cast hsplit
  push_cast at h1' hs
  omega

end StudioMath

end Counting

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
    simp [mem_edgeOfDart_iff, eq_comm]
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
  have hF : Fintype.card M.Face = Fintype.card M.rotation.Face := rfl
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

/-- **Non-vacuity of the Euler lemma.** Its hypotheses hold on the icosahedron. -/
theorem SimpleGraph.Icosahedron.twelve_light_fives_icosahedron :
    12 ≤ (StudioMath.goodSet SimpleGraph.Icosahedron.sphericalMap.graph).card :=
  SimpleGraph.Icosahedron.sphericalMap.twelve_light_fives
    ⟨(0, 1), (show SimpleGraph.Icosahedron.graph.Adj 0 1 by decide)⟩
    (fun f => SimpleGraph.Icosahedron.sphericalMap_triangular f)
    (fun v => (SimpleGraph.Icosahedron.sphericalMap_degree v).ge)

theorem auditPlanted : (1:ℕ) = 2 := sorry

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
