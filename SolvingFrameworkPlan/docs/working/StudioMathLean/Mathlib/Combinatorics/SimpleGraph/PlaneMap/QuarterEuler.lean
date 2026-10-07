/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.EulerSharp
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.NoFrozen
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RotationBoundary
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalCompletion
public import Mathlib.Combinatorics.SimpleGraph.Metric

/-!
# The six-pair Euler identity for the cycle ranks of the Kempe pair-graphs

Formalises `NightW2.md` §11.4. Let `T` be a connected triangulated spherical map on `n`
vertices, `h` a degree-5 vertex (a `Pent`), and `c` a proper 4-colouring of `T − h`. For each
of the six colour pairs `a < b` let `E_ab`, `V_ab`, `C_ab` be the edge, vertex and component
counts of the `{a, b}`-subgraph of `T − h`, and `r_ab = E_ab − V_ab + C_ab` its cycle rank.

## Main results (sorry-free, no new axioms)

* `SphericalMap.euler_lower`: on a connected spherical map, `n + F ≤ E + 2` (the reverse of
  `edge_card_bound_sharp`; the face potential of a kernel element is constant by rotation
  cyclicity and connectivity, and the incidence map hits every even vertex function).
* `SphericalMap.edges_add_six`: a connected triangulated spherical map has `E + 6 = 3n`.
* `card_le_edges_add_comps`: for any finite graph and vertex set `S`,
  `|S| ≤ E + #(components meeting S)` (parent-edge injection along a shortest path to a root).
* `sum_edges_pairs`: `Σ_{pairs} E_ab = E(T − h)` (each edge has a unique colour pair).
* `sum_vertices_pairs`: `Σ_{pairs} V_ab + 3 = 3n` (each vertex of `T − h` is in three pairs).
* `edges_minus_h`: `E(T − h) = 3(n − 1) − 8`.
* `pairRank_nonneg`: `0 ≤ r_ab`.
* **`six_pair_rank_identity`**: `Σ_{pairs} r_ab = Σ_{pairs} C_ab − 8`.
* `comps_sum_ge_eight_of_DL`: at a doubly locked state `ΣC ≥ 8` (`{α, A}` and `{α, B}` have
  at least two components each by `not_reach_alpha_A_of_lock2` / `not_reach_alpha_B_of_lock1`,
  and every pair-graph is nonempty), so the total rank `ΣC − 8` is the excess over the
  extremal state.
-/

@[expose] public section

namespace SimpleGraph

/-! ### Rank of a finite graph -/

section forest
variable {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]

omit [Fintype V] [DecidableEq V] [DecidableRel G.Adj] in
lemma exists_parent {v r : V} (hne : v ≠ r) (hr : G.Reachable v r) :
    ∃ w, G.Adj v w ∧ G.dist w r < G.dist v r := by
  obtain ⟨p, hp⟩ := hr.exists_walk_length_eq_dist
  cases p with
  | nil => exact absurd rfl hne
  | cons hadj q =>
    refine ⟨_, hadj, ?_⟩
    have := G.dist_le q
    rw [Walk.length_cons] at hp
    omega

/-- `|S| ≤ E + (number of components meeting S)`: the cycle rank `E − V + C` of a finite
graph is nonnegative. -/
theorem card_le_edges_add_comps [DecidableEq G.ConnectedComponent] (S : Finset V) :
    S.card ≤ G.edgeFinset.card + (S.image G.connectedComponentMk).card := by
  classical
  let root : V → V := fun v => Quot.out (G.connectedComponentMk v)
  have hmk : ∀ v, G.connectedComponentMk (root v) = G.connectedComponentMk v :=
    fun v => Quot.out_eq _
  have hroot : ∀ v, G.Reachable v (root v) := fun v =>
    ConnectedComponent.exact (hmk v).symm
  have hsame : ∀ u v, G.Reachable u v → root u = root v := fun u v huv => by
    change Quot.out (G.connectedComponentMk u) = Quot.out (G.connectedComponentMk v)
    rw [ConnectedComponent.sound huv]
  let par : V → V := fun v =>
    if hv : v ≠ root v then Classical.choose (exists_parent G hv (hroot v)) else v
  have hpar : ∀ v, v ≠ root v →
      G.Adj v (par v) ∧ G.dist (par v) (root v) < G.dist v (root v) := by
    intro v hv
    simp only [par, dif_pos hv]
    exact Classical.choose_spec (exists_parent G hv (hroot v))
  let f : V → Sym2 V ⊕ G.ConnectedComponent := fun v =>
    if v = root v then Sum.inr (G.connectedComponentMk v) else Sum.inl s(v, par v)
  have hmaps : Set.MapsTo f S (G.edgeFinset.disjSum (S.image G.connectedComponentMk)) := by
    intro v hv
    rw [Finset.mem_coe] at hv ⊢
    by_cases hr : v = root v
    · simp only [f]
      rw [if_pos hr, Finset.inr_mem_disjSum]
      exact Finset.mem_image_of_mem _ hv
    · simp only [f]
      rw [if_neg hr, Finset.inl_mem_disjSum, mem_edgeFinset, mem_edgeSet]
      exact (hpar v hr).1
  have hinj : Set.InjOn f S := by
    intro v _ w _ hfw
    simp only [f] at hfw
    by_cases hv : v = root v <;> by_cases hw : w = root w
    · rw [if_pos hv, if_pos hw, Sum.inr.injEq] at hfw
      rw [hv, hw]
      exact hsame v w (ConnectedComponent.exact hfw)
    · rw [if_pos hv, if_neg hw] at hfw; exact absurd hfw (by simp)
    · rw [if_neg hv, if_pos hw] at hfw; exact absurd hfw (by simp)
    · rw [if_neg hv, if_neg hw, Sum.inl.injEq] at hfw
      rcases Sym2.eq_iff.mp hfw with ⟨e1, -⟩ | ⟨e1, e2⟩
      · exact e1
      · exfalso
        have hv' := hpar v hv
        have hw' := hpar w hw
        have r1 : root (par v) = root v := (hsame _ _ hv'.1.reachable).symm
        have hrw : root w = root v := by rw [← e2]; exact r1
        have a1 := hv'.2
        have a2 := hw'.2
        rw [e2] at a1
        rw [← e1, hrw] at a2
        omega
  have := Finset.card_le_card_of_injOn f hmaps hinj
  rwa [Finset.card_disjSum] at this

end forest

namespace SphericalMap

open Module

variable {n : ℕ} (M : SphericalMap n)

/-! ### The Euler equality for a connected triangulation -/

/-- Face boundaries are even. -/
lemma incidenceAll_boundary (c : M.Face → ZMod 2) :
    incidenceAll M (boundaryLinear M c) = 0 := by
  have hsum : (boundaryLinear M c : M.graph.edgeSet → ZMod 2) =
      RotationSystem.faceSum M.rotation c := by
    funext e
    obtain ⟨d, rfl⟩ := RotationSystem.edge_of_dart_surjective e
    change faceSum M c _ = _
    rw [cycle_faceSum_edgeOfDart, RotationSystem.faceSum_edgeOfDart]
  funext x
  change edgeIncidence M.graph (boundaryLinear M c) x = 0
  rw [hsum]
  exact RotationSystem.faceSum_even M.rotation c x

/-- On a connected map, a face function with zero boundary is constant. -/
lemma face_const_of_boundary_zero (hconn : M.graph.Connected) (d : M.Dart)
    (c : M.Face → ZMod 2) (hc : boundaryLinear M c = 0) : ∀ f, c f = c (M.faceOf d) := by
  have hsym : ∀ e : M.Dart, c (M.faceOf e.symm) = c (M.faceOf e) := by
    intro e
    have := congrFun hc (RotationSystem.edgeOfDart e)
    change faceSum M c _ = 0 at this
    rw [cycle_faceSum_edgeOfDart] at this
    have key : ∀ a b : ZMod 2, a + b = 0 → b = a := by decide
    exact key _ _ this
  have hnext : ∀ e : M.Dart, c (M.faceOf (M.rotation.next e)) = c (M.faceOf e) := by
    intro e
    have h1 : M.rotation.next e = M.rotation.faceNext e.symm := by
      rw [RotationSystem.face_next_apply, Dart.symm_symm]
    rw [h1]
    have h2 := M.rotation.face_of_face_next e.symm
    exact (congrArg c h2 :).trans (hsym e)
  have hiter : ∀ (k : ℕ) (e : M.Dart),
      c (M.faceOf ((M.rotation.next : M.Dart → M.Dart)^[k] e)) = c (M.faceOf e) := by
    intro k
    induction k with
    | zero => intro e; rfl
    | succ k ih => intro e; rw [Function.iterate_succ_apply', hnext, ih]
  have hvert : ∀ e e' : M.Dart, e.fst = e'.fst → c (M.faceOf e) = c (M.faceOf e') := by
    intro e e' h
    obtain ⟨k, hk⟩ := M.rotation.cyclic e e' h
    rw [← hk, hiter]
  have hwalk : ∀ (u v : Fin n) (p : M.graph.Walk u v) (e e' : M.Dart),
      e.fst = u → e'.fst = v → c (M.faceOf e) = c (M.faceOf e') := by
    intro u v p
    induction p with
    | nil => intro e e' h1 h2; exact hvert e e' (h1.trans h2.symm)
    | @cons x y z hadj p ih =>
      intro e e' h1 h2
      let a : M.Dart := ⟨(x, y), hadj⟩
      calc c (M.faceOf e) = c (M.faceOf a) := hvert e a h1
        _ = c (M.faceOf a.symm) := (hsym a).symm
        _ = c (M.faceOf e') := ih a.symm e' rfl h2
  intro f
  obtain ⟨e, rfl⟩ := M.rotation.face_of_surjective d f
  obtain ⟨p⟩ := hconn.preconnected e.fst d.fst
  exact hwalk _ _ p e d rfl rfl

/-- A walk gives an edge combination with boundary at its two ends. -/
lemma exists_incidence_walk {u v : Fin n} (p : M.graph.Walk u v) :
    ∃ φ, incidenceAll M φ = Pi.single u 1 + Pi.single v 1 := by
  classical
  have key : ∀ a b c : ZMod 2, (a + b) + (b + c) = a + c := by decide
  induction p with
  | nil =>
    refine ⟨0, ?_⟩
    funext x
    rw [map_zero]
    have : ∀ a : ZMod 2, a + a = 0 := by decide
    exact (this _).symm
  | @cons x y z hadj p ih =>
    obtain ⟨φ, hφ⟩ := ih
    let e : M.graph.edgeSet := ⟨s(x, y), hadj⟩
    let ψ : M.graph.edgeSet → ZMod 2 := fun e' => if e' = e then 1 else 0
    have hψ : incidenceAll M ψ = Pi.single x 1 + Pi.single y 1 := by
      funext w
      change edgeIncidence M.graph ψ w = _
      unfold edgeIncidence
      rw [Finset.sum_eq_single e]
      · simp only [ψ, if_pos rfl, e, Sym2.mem_iff, Pi.add_apply, Pi.single_apply]
        by_cases h1 : w = x
        · subst h1; simp [hadj.ne]
        · by_cases h2 : w = y
          · subst h2; simp [h1]
          · simp [h1, h2]
      · intro b _ hb; simp [ψ, hb]
      · simp
    refine ⟨ψ + φ, ?_⟩
    rw [map_add, hψ, hφ]
    funext w
    simp only [Pi.add_apply]
    exact key _ _ _

/-- **Euler, lower bound.** On a connected spherical map with a dart, `n + F ≤ E + 2`. -/
theorem euler_lower (hconn : M.graph.Connected) (d : M.Dart) :
    n + Fintype.card M.Face ≤ Fintype.card M.graph.edgeSet + 2 := by
  classical
  let I := incidenceAll M
  let B := boundaryLinear M
  let σ := coordSum (n := n)
  let K : ZMod 2 →ₗ[ZMod 2] (M.Face → ZMod 2) := LinearMap.pi fun _ => LinearMap.id
  have hrB : LinearMap.range B ≤ LinearMap.ker I := by
    rintro _ ⟨c, rfl⟩
    exact LinearMap.mem_ker.mpr (incidenceAll_boundary M c)
  have hkB : LinearMap.ker B ≤ LinearMap.range K := by
    intro c hc
    refine ⟨c (M.faceOf d), ?_⟩
    funext f
    exact (face_const_of_boundary_zero M hconn d c (LinearMap.mem_ker.mp hc) f).symm
  have hkσ : LinearMap.ker σ ≤ LinearMap.range I := by
    intro f hf
    have hf' : ∑ x, f x = 0 := LinearMap.mem_ker.mp hf
    have hφ : ∀ x, Pi.single x 1 + Pi.single d.fst 1 ∈ LinearMap.range I := by
      intro x
      obtain ⟨p⟩ := hconn.preconnected x d.fst
      obtain ⟨φ, hφ⟩ := exists_incidence_walk M p
      exact ⟨φ, hφ⟩
    have hf2 : f = ∑ x, f x • (Pi.single x 1 + Pi.single d.fst (1 : ZMod 2)) := by
      funext y
      simp only [Finset.sum_apply, Pi.smul_apply, Pi.add_apply, smul_eq_mul, mul_add,
        Finset.sum_add_distrib, Pi.single_apply, mul_ite, mul_one, mul_zero,
        Finset.sum_ite_eq, Finset.mem_univ, if_true]
      by_cases hy : y = d.fst <;> simp [hy, hf']
    rw [hf2]
    exact Submodule.sum_mem _ fun x _ => Submodule.smul_mem _ _ (hφ x)
  have hi := I.finrank_range_add_finrank_ker
  have hb := B.finrank_range_add_finrank_ker
  have hσ := σ.finrank_range_add_finrank_ker
  have h1 := Submodule.finrank_mono hrB
  have h2 := Submodule.finrank_mono hkB
  have h3 := Submodule.finrank_mono hkσ
  have h4 : finrank (ZMod 2) (LinearMap.range K) ≤ 1 := by
    simpa using LinearMap.finrank_range_le K
  have h5 : finrank (ZMod 2) (LinearMap.range σ) ≤ 1 := by
    simpa using (LinearMap.range σ).finrank_le
  simp only [Module.finrank_fintype_fun_eq_card, Fintype.card_fin] at hi hb hσ
  omega

lemma faceLength_three (htri : M.Triangulated) (d : M.Dart) (f : M.Face) :
    M.rotation.faceLength f = 3 := by
  obtain ⟨e, rfl⟩ := M.rotation.face_of_surjective d f
  exact htri e

/-- **Euler for a connected triangulation:** `E + 6 = 3n`. -/
theorem edges_add_six (hconn : M.graph.Connected) (htri : M.Triangulated) (d : M.Dart) :
    M.graph.edgeFinset.card + 6 = 3 * n := by
  classical
  have hup := twice_edges_add_twelve_le M d (faceLength_three M htri d)
  have hlo := euler_lower M hconn d
  have hs := M.rotation.sum_face_lengths_eq_twice_card_edges
  simp only [faceLength_three M htri d, Finset.sum_const, Finset.card_univ,
    smul_eq_mul] at hs
  rw [← edgeFinset_card] at hlo
  have hF : Fintype.card M.Face = Fintype.card M.rotation.Face := rfl
  omega

end SphericalMap

/-! ### The six colour pairs -/

namespace QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- The six colour pairs `a < b`. -/
def pairs : Finset (Fin 4 × Fin 4) := Finset.univ.filter fun p => p.1 < p.2

lemma card_pairs : pairs.card = 6 := by decide

variable {n : ℕ} (M : SphericalMap n) (h : Fin n) (c : Fin n → Fin 4)

/-- The edges of `T − h`. -/
noncomputable def offEdges : Finset (Sym2 (Fin n)) := M.graph.edgeFinset.filter fun e => h ∉ e

/-- `E_ab`: the edges of `T − h` whose end colours are `{a, b}`. -/
noncomputable def pairEdges (a b : Fin 4) : ℕ :=
  ((offEdges M h).filter fun e => e.map c = s(a, b)).card

/-- `V_ab`: the vertices of `T − h` coloured `a` or `b`. -/
def pairVerts (a b : Fin 4) : ℕ :=
  (Finset.univ.filter fun v => v ≠ h ∧ (c v = a ∨ c v = b)).card

open Classical in
/-- `C_ab`: the components of the `{a, b}`-subgraph of `T − h` (with at least one vertex). -/
noncomputable def pairComps (a b : Fin 4) : ℕ :=
  ((Finset.univ.filter fun v => v ≠ h ∧ (c v = a ∨ c v = b)).image
    (pairGraph M.graph h c a b).connectedComponentMk).card

/-- `r_ab = E_ab − V_ab + C_ab`, the cycle rank of the `{a, b}`-subgraph of `T − h`. -/
noncomputable def pairRank (a b : Fin 4) : ℤ :=
  (pairEdges M h c a b : ℤ) - pairVerts h c a b + pairComps M h c a b

/-- **(1)** Each edge of `T − h` lies in exactly one pair-graph. -/
theorem sum_edges_pairs (hc : ProperOff M.graph h c) :
    ∑ p ∈ pairs, pairEdges M h c p.1 p.2 = (offEdges M h).card := by
  classical
  have hmaps : Set.MapsTo (fun e : Sym2 (Fin n) => e.map c) (offEdges M h)
      (pairs.image fun p => s(p.1, p.2)) := by
    intro e he
    induction e using Sym2.ind with
    | h u v =>
    simp only [offEdges, Finset.coe_filter, Set.mem_setOf_eq, mem_edgeFinset, mem_edgeSet,
      Sym2.mem_iff, not_or] at he
    have hne : c u ≠ c v := hc he.1 (Ne.symm he.2.1) (Ne.symm he.2.2)
    simp only [Sym2.map_mk, Finset.coe_image, Set.mem_image, Finset.mem_coe]
    rcases lt_or_gt_of_ne hne with hl | hl
    · exact ⟨(c u, c v), by simp [pairs, hl], rfl⟩
    · exact ⟨(c v, c u), by simp [pairs, hl], Sym2.eq_swap⟩
  rw [Finset.card_eq_sum_card_fiberwise hmaps, Finset.sum_image]
  · rfl
  · intro p hp q hq e
    simp only [pairs, Finset.coe_filter, Finset.mem_univ, true_and, Set.mem_setOf_eq] at hp hq
    rcases Sym2.eq_iff.mp e with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact Prod.ext h1 h2
    · exfalso; rw [h1, h2] at hp; exact absurd (hp.trans hq) (lt_irrefl _)

/-- **(2)** Each vertex of `T − h` lies in exactly three pair-graphs. -/
theorem sum_vertices_pairs : ∑ p ∈ pairs, pairVerts h c p.1 p.2 + 3 = 3 * n := by
  unfold pairVerts
  simp only [Finset.card_filter]
  rw [Finset.sum_comm]
  have hv : ∀ v : Fin n, (∑ p ∈ pairs, if v ≠ h ∧ (c v = p.1 ∨ c v = p.2) then 1 else 0) =
      if v = h then 0 else 3 := by
    intro v
    by_cases hvh : v = h
    · simp [hvh]
    · simp only [hvh, ne_eq, not_false_eq_true, true_and, if_false]
      generalize c v = x
      revert x; decide
  simp only [hv]
  rw [← Finset.add_sum_erase _ _ (Finset.mem_univ h), if_pos rfl, zero_add]
  rw [Finset.sum_congr rfl (fun v hv => if_neg (Finset.ne_of_mem_erase hv)),
    Finset.sum_const, Finset.card_erase_of_mem (Finset.mem_univ h), Finset.card_univ,
    Fintype.card_fin, smul_eq_mul]
  have : 1 ≤ n := Fin.pos_iff_nonempty.mpr ⟨h⟩
  rw [Nat.sub_mul]
  omega

variable {M h}

lemma degree_pent (P : Pent M.graph h) : M.graph.degree h = 5 := by
  classical
  rw [← card_neighborFinset_eq_degree]
  have : M.graph.neighborFinset h = Finset.univ.image P.x := by
    ext v
    simp only [mem_neighborFinset, Finset.mem_image, Finset.mem_univ, true_and]
    constructor
    · intro hv; obtain ⟨i, rfl⟩ := P.only v hv; exact ⟨i, rfl⟩
    · rintro ⟨i, rfl⟩; exact P.adj_h i
  rw [this, Finset.card_image_of_injective _ P.inj]
  rfl

lemma offEdges_add_five (P : Pent M.graph h) :
    (offEdges M h).card + 5 = M.graph.edgeFinset.card := by
  classical
  have h1 := Finset.card_filter_add_card_filter_not (s := M.graph.edgeFinset)
    (p := fun e => h ∈ e)
  have h2 : (M.graph.edgeFinset.filter fun e => h ∈ e).card = 5 := by
    rw [← degree_pent P, ← card_incidenceFinset_eq_degree, incidenceFinset_eq_filter]
  have h3 : (offEdges M h).card = (M.graph.edgeFinset.filter fun e => ¬ h ∈ e).card := by
    unfold offEdges; rfl
  omega

/-- **(3)** `E(T − h) = 3(n − 1) − 8`. -/
theorem edges_minus_h (hconn : M.graph.Connected) (htri : M.Triangulated)
    (P : Pent M.graph h) : ((offEdges M h).card : ℤ) = 3 * ((n : ℤ) - 1) - 8 := by
  have d : M.Dart := ⟨(h, P.x 0), P.adj_h 0⟩
  have h1 := edges_add_six M hconn htri d
  have h2 := offEdges_add_five P
  omega

/-- The `{a, b}`-pair graph has no more edges than `E_ab`. -/
lemma pairGraph_edges_le (hc : ProperOff M.graph h c) (a b : Fin 4)
    [DecidableRel (pairGraph M.graph h c a b).Adj] :
    (pairGraph M.graph h c a b).edgeFinset.card ≤ pairEdges M h c a b := by
  classical
  apply Finset.card_le_card
  intro e he
  induction e using Sym2.ind with
  | h u v =>
  rw [mem_edgeFinset, mem_edgeSet] at he
  obtain ⟨huv, ⟨hu, cu⟩, ⟨hv, cv⟩⟩ := he
  have hne := hc huv hu hv
  simp only [offEdges, Finset.mem_filter, mem_edgeFinset, mem_edgeSet, Sym2.mem_iff, not_or,
    Sym2.map_mk]
  refine ⟨⟨huv, Ne.symm hu, Ne.symm hv⟩, ?_⟩
  rcases cu with cu | cu <;> rcases cv with cv | cv <;> rw [cu, cv] at hne ⊢ <;>
    first | exact absurd rfl hne | rfl | exact Sym2.eq_swap

/-- The cycle rank of each pair-graph is nonnegative. -/
theorem pairRank_nonneg (hc : ProperOff M.graph h c) (a b : Fin 4) :
    0 ≤ pairRank M h c a b := by
  classical
  have h1 := card_le_edges_add_comps (pairGraph M.graph h c a b)
    (Finset.univ.filter fun v => v ≠ h ∧ (c v = a ∨ c v = b))
  have h2 := pairGraph_edges_le c hc a b
  have h3 : ((Finset.univ.filter fun v => v ≠ h ∧ (c v = a ∨ c v = b)).card : ℤ) ≤
      (pairEdges M h c a b : ℤ) +
        (((Finset.univ.filter fun v => v ≠ h ∧ (c v = a ∨ c v = b)).image
          (pairGraph M.graph h c a b).connectedComponentMk).card : ℤ) := by
    exact_mod_cast h1.trans (Nat.add_le_add_right h2 _)
  unfold pairRank pairVerts pairComps
  linarith

/-- **(4) The six-pair Euler identity.** `Σ r_ab = Σ C_ab − 8`. -/
theorem six_pair_rank_identity (hconn : M.graph.Connected) (htri : M.Triangulated)
    (P : Pent M.graph h) (hc : ProperOff M.graph h c) :
    ∑ p ∈ pairs, pairRank M h c p.1 p.2 = ∑ p ∈ pairs, (pairComps M h c p.1 p.2 : ℤ) - 8 := by
  have hE := sum_edges_pairs M h c hc
  have hV := sum_vertices_pairs h c
  have hT := edges_minus_h hconn htri P
  unfold pairRank
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  have hE' : ∑ p ∈ pairs, (pairEdges M h c p.1 p.2 : ℤ) = (offEdges M h).card := by
    exact_mod_cast hE
  have hV' : ∑ p ∈ pairs, (pairVerts h c p.1 p.2 : ℤ) + 3 = 3 * n := by
    exact_mod_cast hV
  rw [hE', hT]
  linarith

/-! ### (5) At a doubly locked state, `Σ C ≥ 8` -/

lemma pairComps_comm (a b : Fin 4) : pairComps M h c a b = pairComps M h c b a := by
  unfold pairComps
  rw [pairGraph_comm]
  simp only [or_comm]

lemma pairComps_pos {a b : Fin 4} {v : Fin n} (hv : v ≠ h) (hcv : c v = a ∨ c v = b) :
    1 ≤ pairComps M h c a b := by
  classical
  unfold pairComps
  exact Finset.card_pos.mpr ⟨_, Finset.mem_image_of_mem _
    (Finset.mem_filter.mpr ⟨Finset.mem_univ v, hv, hcv⟩)⟩

lemma pairComps_two {a b : Fin 4} {u v : Fin n} (hu : u ≠ h) (hcu : c u = a ∨ c u = b)
    (hv : v ≠ h) (hcv : c v = a ∨ c v = b)
    (hnr : ¬ (pairGraph M.graph h c a b).Reachable u v) : 2 ≤ pairComps M h c a b := by
  classical
  unfold pairComps
  exact Finset.one_lt_card.mpr ⟨_, Finset.mem_image_of_mem _
    (Finset.mem_filter.mpr ⟨Finset.mem_univ u, hu, hcu⟩), _,
    Finset.mem_image_of_mem _ (Finset.mem_filter.mpr ⟨Finset.mem_univ v, hv, hcv⟩),
    fun e => hnr (ConnectedComponent.exact e)⟩

/-- The sorted version of a pair. -/
def sortPair (a b : Fin 4) : Fin 4 × Fin 4 := if a < b then (a, b) else (b, a)

lemma sortPair_mem {a b : Fin 4} (hab : a ≠ b) : sortPair a b ∈ pairs := by
  revert a b; decide

lemma pairComps_sort (a b : Fin 4) :
    pairComps M h c (sortPair a b).1 (sortPair a b).2 = pairComps M h c a b := by
  unfold sortPair
  split_ifs
  · rfl
  · exact pairComps_comm c b a

/-- **(5)** At a doubly locked state, `Σ_{pairs} C_ab ≥ 8`: the `{α, A}`- and `{α, B}`-graphs
have at least two components each, and every pair-graph is nonempty. Hence the total cycle
rank `Σ r_ab = Σ C_ab − 8` is the excess of `Σ C` over the extremal value `8`. -/
theorem comps_sum_ge_eight_of_DL (P : Pent M.graph h) (j : Fin 5)
    (hdl : DoublyLocked P c j) : 8 ≤ ∑ p ∈ pairs, pairComps M h c p.1 p.2 := by
  classical
  obtain ⟨hr, hl1, hl2⟩ := hdl
  have nA := not_reach_alpha_A_of_lock2 P c j hr hl2
  have nB := not_reach_alpha_B_of_lock1 P c j hr hl1
  obtain ⟨h0, h1, h2, h3, h4, h5, h6⟩ := hr
  have hxh : ∀ i, P.x i ≠ h := fun i => (P.h_ne i).symm
  -- every pair-graph is nonempty
  have hall : ∀ p ∈ pairs, 1 ≤ pairComps M h c p.1 p.2 := by
    intro p _
    have key : ∀ x α μ A B : Fin 4, μ ≠ α → A ≠ α → B ≠ α → μ ≠ A → μ ≠ B → A ≠ B →
        x = α ∨ x = μ ∨ x = A ∨ x = B := by decide
    rcases key p.1 _ _ _ _ h1 h2 h3 h4 h5 h6 with e | e | e | e
    · exact pairComps_pos c (hxh j) (Or.inl e.symm)
    · exact pairComps_pos c (hxh (j + 1)) (Or.inl e.symm)
    · exact pairComps_pos c (hxh (j + 3)) (Or.inl e.symm)
    · exact pairComps_pos c (hxh (j + 4)) (Or.inl e.symm)
  have cA : 2 ≤ pairComps M h c (c (P.x j)) (c (P.x (j + 3))) :=
    pairComps_two c (hxh j) (Or.inl rfl) (hxh (j + 2)) (Or.inl h0.symm) nA
  have cB : 2 ≤ pairComps M h c (c (P.x j)) (c (P.x (j + 4))) :=
    pairComps_two c (hxh j) (Or.inl rfl) (hxh (j + 2)) (Or.inl h0.symm) nB
  set p1 := sortPair (c (P.x j)) (c (P.x (j + 3)))
  set p2 := sortPair (c (P.x j)) (c (P.x (j + 4)))
  have m1 : p1 ∈ pairs := sortPair_mem (Ne.symm h2)
  have m2 : p2 ∈ pairs := sortPair_mem (Ne.symm h3)
  have hne : p1 ≠ p2 := by
    have key : ∀ α A B : Fin 4, A ≠ α → B ≠ α → A ≠ B → sortPair α A ≠ sortPair α B := by
      decide
    exact key _ _ _ h2 h3 h6
  have m2' : p2 ∈ pairs.erase p1 := Finset.mem_erase.mpr ⟨Ne.symm hne, m2⟩
  rw [← Finset.add_sum_erase _ _ m1, ← Finset.add_sum_erase _ _ m2']
  have hrest : (((pairs.erase p1).erase p2).card) • 1 ≤
      ∑ p ∈ (pairs.erase p1).erase p2, pairComps M h c p.1 p.2 :=
    Finset.card_nsmul_le_sum _ _ _ fun p hp =>
      hall p (Finset.mem_of_mem_erase (Finset.mem_of_mem_erase hp))
  rw [Finset.card_erase_of_mem m2', Finset.card_erase_of_mem m1, card_pairs,
    smul_eq_mul] at hrest
  have e1 : pairComps M h c p1.1 p1.2 = pairComps M h c (c (P.x j)) (c (P.x (j + 3))) :=
    pairComps_sort c _ _
  have e2 : pairComps M h c p2.1 p2.2 = pairComps M h c (c (P.x j)) (c (P.x (j + 4))) :=
    pairComps_sort c _ _
  omega

end QuarterFloor

end SimpleGraph

#print axioms SimpleGraph.SphericalMap.edges_add_six
#print axioms SimpleGraph.QuarterFloor.six_pair_rank_identity
#print axioms SimpleGraph.QuarterFloor.pairRank_nonneg
#print axioms SimpleGraph.QuarterFloor.comps_sum_ge_eight_of_DL
