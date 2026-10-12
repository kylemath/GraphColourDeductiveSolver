/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalCompletion
public import Mathlib.LinearAlgebra.Matrix.Rank
public import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
public import Mathlib.Algebra.Field.ZMod

/-!
# Tutte's identity for a two-sided vertex split, from `Fills` (no topology)

Split the vertices of a map by a predicate `τ`. The *side edges* `S_τ` are the edges with both
ends in `τ`. Over `ZMod 2`:

* `chainSpace G τ`: functions vanishing off `τ` and constant along side edges. Its dimension is
  the number of `τ`-chains, i.e. the components of the side graph that meet `τ`
  (`finrank_chainSpace`).
* `finrank_chainSpace_insert` (merge lemma): adding a vertex `h` whose only `τ`-neighbours are
  `a` and `b` lowers the chain count by `[a, b in different chains]`.
* `graph_side`: `dim Z(S_τ) + |V| = |S_τ| + dim constSpace`. This is the rank of the incidence
  matrix computed through its transpose (`Matrix.rank_transpose`).
* `face_side` (the only use of `Fills`): the boundary map from face functions constant across
  the non-side edges onto `Z(S_τ)` is onto. Its kernel is the face functions constant across
  every edge, of dimension `γ` (`gammaM`).
* `finrank_faceSpace`: on a triangulation without isolated vertices, if every face has a corner
  off `τ`, those face functions correspond to the chain functions of the other side. Faces
  around a vertex are linked through its edges.

Together these give **`tutte_sides`**: `|S_τ| + #(τ-chains) + γ = #τ + #(¬τ-chains)`. On a
connected sphere (`γ = 1`) this is Tutte's identity `p(XY) − p(ZW) = |X| + |Y| − e(XY) − 1`. With
τ ≡ true the same lemmas give **`euler_tri`**: `|E| + 6γ = 3n`.

No Jordan curve theorem, region, or dual graph is used. The planar input is exactly `Fills`
(every even edge set is a sum of face boundaries).
-/

@[expose] public section
namespace SimpleGraph.TutteSides
open Finset

section graph
variable {V : Type*} (G : SimpleGraph V)

/-- The side graph of `τ`: the edges of `G` with both ends in `τ` (all vertices kept). -/
def sideGraph (τ : V → Prop) : SimpleGraph V where
  Adj u v := G.Adj u v ∧ τ u ∧ τ v
  symm := ⟨fun _ _ e => ⟨e.1.symm, e.2.2, e.2.1⟩⟩
  loopless := ⟨fun _ e => e.1.ne rfl⟩

/-- Functions vanishing off `τ` and constant along the edges of `G` inside `τ`
(one free value per `τ`-chain). -/
def chainSpace (τ : V → Prop) : Submodule (ZMod 2) (V → ZMod 2) where
  carrier := {g | (∀ v, ¬ τ v → g v = 0) ∧ ∀ u v, G.Adj u v → τ u → τ v → g u = g v}
  add_mem' := by
    rintro g g' ⟨h1, h2⟩ ⟨h1', h2'⟩
    refine ⟨fun v hv => ?_, fun u v e hu hv => ?_⟩
    · simp [h1 v hv, h1' v hv]
    · simp [h2 u v e hu hv, h2' u v e hu hv]
  zero_mem' := ⟨fun _ _ => rfl, fun _ _ _ _ _ => rfl⟩
  smul_mem' := by
    rintro r g ⟨h1, h2⟩
    refine ⟨fun v hv => ?_, fun u v e hu hv => ?_⟩
    · simp [h1 v hv]
    · simp [h2 u v e hu hv]

/-- Functions constant along the edges of `G` inside `τ` (all vertices free off `τ`). -/
def constSpace (τ : V → Prop) : Submodule (ZMod 2) (V → ZMod 2) where
  carrier := {g | ∀ u v, G.Adj u v → τ u → τ v → g u = g v}
  add_mem' := by
    intro g g' h h' u v e hu hv
    simp [h u v e hu hv, h' u v e hu hv]
  zero_mem' := fun _ _ _ _ _ => rfl
  smul_mem' := by
    intro r g h u v e hu hv
    simp [h u v e hu hv]

variable {G}

lemma mem_chainSpace {τ : V → Prop} {g : V → ZMod 2} :
    g ∈ chainSpace G τ ↔ (∀ v, ¬ τ v → g v = 0) ∧ ∀ u v, G.Adj u v → τ u → τ v → g u = g v :=
  Iff.rfl

lemma mem_constSpace {τ : V → Prop} {g : V → ZMod 2} :
    g ∈ constSpace G τ ↔ ∀ u v, G.Adj u v → τ u → τ v → g u = g v :=
  Iff.rfl

lemma chainSpace_congr {τ τ' : V → Prop} (h : ∀ v, τ v ↔ τ' v) :
    chainSpace G τ = chainSpace G τ' := by
  ext g
  simp only [mem_chainSpace, h]

/-- A function constant along the edges of `H` is constant on `H`-components. -/
lemma const_of_reachable {H : SimpleGraph V} {g : V → ZMod 2}
    (hg : ∀ u v, H.Adj u v → g u = g v) {u v : V} (huv : H.Reachable u v) : g u = g v := by
  obtain ⟨p⟩ := huv
  induction p with
  | nil => rfl
  | cons e _ ih => exact (hg _ _ e).trans ih

lemma side_const {τ : V → Prop} {g : V → ZMod 2} (hg : g ∈ chainSpace G τ) {u v : V}
    (huv : (sideGraph G τ).Reachable u v) : g u = g v :=
  const_of_reachable (H := sideGraph G τ) (fun a b e => hg.2 a b e.1 e.2.1 e.2.2) huv

variable [Fintype V]

open Classical in
/-- **Chain count.** The dimension of `chainSpace G τ` is the number of components of the side
graph that meet `τ`. -/
theorem finrank_chainSpace (τ : V → Prop) [DecidablePred τ] :
    Module.finrank (ZMod 2) (chainSpace G τ) =
      #((univ.filter τ).image (sideGraph G τ).connectedComponentMk) := by
  classical
  set Q := (univ.filter τ).image (sideGraph G τ).connectedComponentMk with hQ
  have rep : ∀ q : Q, ∃ v, τ v ∧ (sideGraph G τ).connectedComponentMk v = q := by
    intro q
    obtain ⟨v, hv, e⟩ := Finset.mem_image.mp q.2
    exact ⟨v, (Finset.mem_filter.mp hv).2, e⟩
  let r : Q → V := fun q => Classical.choose (rep q)
  have hr : ∀ q, τ (r q) ∧ (sideGraph G τ).connectedComponentMk (r q) = q :=
    fun q => Classical.choose_spec (rep q)
  have memQ : ∀ v, τ v → (sideGraph G τ).connectedComponentMk v ∈ Q := fun v hv =>
    Finset.mem_image_of_mem _ (Finset.mem_filter.mpr ⟨Finset.mem_univ _, hv⟩)
  let toF : chainSpace G τ →ₗ[ZMod 2] (Q → ZMod 2) :=
    { toFun := fun g q => (g : V → ZMod 2) (r q)
      map_add' := fun _ _ => rfl
      map_smul' := fun _ _ => rfl }
  let ofF : (Q → ZMod 2) → chainSpace G τ := fun b =>
    ⟨fun v => if hv : τ v then b ⟨_, memQ v hv⟩ else 0, by
      refine ⟨fun v hv => by simp [hv], fun u v e hu hv => ?_⟩
      simp only [hu, hv, dite_true]
      congr 2
      exact ConnectedComponent.connectedComponentMk_eq_of_adj ⟨e, hu, hv⟩⟩
  let E : chainSpace G τ ≃ₗ[ZMod 2] (Q → ZMod 2) :=
    { toF with
      invFun := ofF
      left_inv := by
        intro g
        apply Subtype.ext
        funext v
        show (if hv : τ v then (g : V → ZMod 2) (r ⟨_, memQ v hv⟩) else 0) = (g : V → ZMod 2) v
        by_cases hv : τ v
        · simp only [hv, dite_true]
          apply side_const g.2
          exact ConnectedComponent.exact (hr ⟨_, memQ v hv⟩).2
        · simp only [hv, dite_false]
          exact (g.2.1 v hv).symm
      right_inv := by
        intro b
        funext q
        show (if hv : τ (r q) then b ⟨_, memQ (r q) hv⟩ else 0) = b q
        simp only [(hr q).1, dite_true]
        congr 1
        exact Subtype.ext (hr q).2 }
  rw [E.finrank_eq, Module.finrank_fintype_fun_eq_card, Fintype.card_coe]

open Classical in
/-- Vertices off `τ` are free in `constSpace`: its dimension exceeds that of `chainSpace` by the
number of vertices off `τ`. -/
theorem finrank_constSpace (τ : V → Prop) [DecidablePred τ] :
    Module.finrank (ZMod 2) (constSpace G τ) =
      Module.finrank (ZMod 2) (chainSpace G τ) + #(univ.filter (fun v => ¬ τ v)) := by
  classical
  -- `D` = functions vanishing on `τ`
  set D := chainSpace (⊥ : SimpleGraph V) (fun v => ¬ τ v) with hD
  have hDr : Module.finrank (ZMod 2) D = #(univ.filter (fun v => ¬ τ v)) := by
    rw [hD, finrank_chainSpace]
    apply Finset.card_image_of_injective
    intro u v huv
    have hr := ConnectedComponent.exact huv
    exact reachable_bot.mp
      (hr.mono (show sideGraph (⊥ : SimpleGraph V) (fun v => ¬ τ v) ≤ ⊥ from fun a b e => e.1))
  have hsup : chainSpace G τ ⊔ D = constSpace G τ := by
    apply le_antisymm
    · refine sup_le (fun g hg => fun u v e hu hv => hg.2 u v e hu hv) ?_
      intro g hg u v _ hu hv
      rw [hg.1 u (not_not.mpr hu), hg.1 v (not_not.mpr hv)]
    · intro g hg
      refine Submodule.mem_sup.mpr ⟨fun v => if τ v then g v else 0, ?_,
        fun v => if τ v then 0 else g v, ?_, ?_⟩
      · refine ⟨fun v hv => by simp [hv], fun u v e hu hv => ?_⟩
        simp [hu, hv, hg u v e hu hv]
      · exact ⟨fun v hv => by simp [not_not.mp hv], fun u v e => e.elim⟩
      · funext v
        by_cases hv : τ v <;> simp [hv]
  have hinf : chainSpace G τ ⊓ D = ⊥ := by
    rw [eq_bot_iff]
    intro g hg
    rw [Submodule.mem_bot]
    funext v
    by_cases hv : τ v
    · exact hg.2.1 v (not_not.mpr hv)
    · exact hg.1.1 v hv
  have := Submodule.finrank_sup_add_finrank_inf_eq (K := ZMod 2) (chainSpace G τ) D
  rw [hsup, hinf, finrank_bot, add_zero, hDr] at this
  exact this

/-- `x + y = 0` in `ZMod 2` iff `x = y`. -/
lemma zmod2_add_eq_zero : ∀ x y : ZMod 2, x + y = 0 ↔ x = y := by decide

lemma zmod2_add_self : ∀ x : ZMod 2, x + x = 0 := by decide

open Classical in
/-- **Merging at a new vertex.** Adding a vertex `h` (off `τ`) whose only `τ`-neighbours are
`a` and `b` lowers the chain count by one unless `a` and `b` are already in one chain. -/
theorem finrank_chainSpace_insert (τ : V → Prop) {h a b : V} (hh : ¬ τ h) (ha : τ a)
    (hb : τ b) (hha : G.Adj h a) (hhb : G.Adj h b)
    (honly : ∀ v, G.Adj h v → τ v → v = a ∨ v = b) :
    Module.finrank (ZMod 2) (chainSpace G (fun v => v = h ∨ τ v)) +
        (if (sideGraph G τ).Reachable a b then 0 else 1) =
      Module.finrank (ZMod 2) (chainSpace G τ) := by
  set τ' : V → Prop := fun v => v = h ∨ τ v with hτ'
  let ℓ : chainSpace G τ →ₗ[ZMod 2] ZMod 2 :=
    { toFun := fun g => (g : V → ZMod 2) a + (g : V → ZMod 2) b
      map_add' := fun g g' => add_add_add_comm _ _ _ _
      map_smul' := fun r g => (mul_add r _ _).symm }
  let ρf : chainSpace G τ' → chainSpace G τ := fun g =>
    ⟨fun v => if v = h then 0 else (g : V → ZMod 2) v, by
      refine ⟨fun v hv => ?_, fun u v e hu hv => ?_⟩
      · by_cases hvh : v = h
        · simp [hvh]
        · simp only [hvh, ↓reduceIte]
          exact g.2.1 v (by simp [hτ', hvh, hv])
      · have hu' : u ≠ h := fun e' => hh (e' ▸ hu)
        have hv' : v ≠ h := fun e' => hh (e' ▸ hv)
        simp only [hu', hv', ↓reduceIte]
        exact g.2.2 u v e (Or.inr hu) (Or.inr hv)⟩
  let ρ : chainSpace G τ' →ₗ[ZMod 2] chainSpace G τ :=
    { toFun := ρf
      map_add' := fun g g' => by
        apply Subtype.ext; funext v
        simp only [ρf, Submodule.coe_add, Pi.add_apply]
        split_ifs <;> simp
      map_smul' := fun r g => by
        apply Subtype.ext; funext v
        simp only [ρf, Submodule.coe_smul, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
        split_ifs <;> simp }
  have hga : ∀ g : chainSpace G τ', (g : V → ZMod 2) h = (g : V → ZMod 2) a :=
    fun g => g.2.2 h a hha (Or.inl rfl) (Or.inr ha)
  have hgb : ∀ g : chainSpace G τ', (g : V → ZMod 2) h = (g : V → ZMod 2) b :=
    fun g => g.2.2 h b hhb (Or.inl rfl) (Or.inr hb)
  have hah : a ≠ h := fun e => hh (e ▸ ha)
  have hbh : b ≠ h := fun e => hh (e ▸ hb)
  have hinj : Function.Injective ρ := by
    rw [← LinearMap.ker_eq_bot, eq_bot_iff]
    intro g hg
    rw [LinearMap.mem_ker] at hg
    rw [Submodule.mem_bot]
    have hv : ∀ v, v ≠ h → (g : V → ZMod 2) v = 0 := fun v hv => by
      have := congrArg (fun x : chainSpace G τ => (x : V → ZMod 2) v) hg
      simpa [ρ, ρf, hv] using this
    apply Subtype.ext
    funext v
    by_cases hvh : v = h
    · subst hvh
      rw [hga g, hv a hah]
      rfl
    · exact hv v hvh
  have hrange : LinearMap.range ρ = LinearMap.ker ℓ := by
    apply le_antisymm
    · rintro _ ⟨g, rfl⟩
      rw [LinearMap.mem_ker]
      show (if a = h then 0 else (g : V → ZMod 2) a) + (if b = h then 0 else (g : V → ZMod 2) b) = 0
      simp only [hah, hbh, ↓reduceIte]
      rw [← hga g, ← hgb g]
      exact zmod2_add_self _
    · intro g hg
      rw [LinearMap.mem_ker] at hg
      have hab : (g : V → ZMod 2) a = (g : V → ZMod 2) b := (zmod2_add_eq_zero _ _).mp hg
      refine ⟨⟨fun v => if v = h then (g : V → ZMod 2) a else (g : V → ZMod 2) v, ?_⟩, ?_⟩
      · refine ⟨fun v hv => ?_, fun u v e hu hv => ?_⟩
        · have hvh : v ≠ h := fun e => hv (Or.inl e)
          simp only [hvh, ↓reduceIte]
          exact g.2.1 v (fun t => hv (Or.inr t))
        · by_cases hu' : u = h
          · subst hu'
            have hv' : v ≠ u := fun e' => G.loopless.irrefl _ (e' ▸ e)
            have hvt : τ v := hv.resolve_left hv'
            simp only [hv', ↓reduceIte]
            rcases honly v e hvt with rfl | rfl
            · rfl
            · exact hab
          · by_cases hv' : v = h
            · subst hv'
              have hut : τ u := hu.resolve_left hu'
              simp only [hu', ↓reduceIte]
              rcases honly u e.symm hut with rfl | rfl
              · rfl
              · exact hab.symm
            · simp only [hu', hv', ↓reduceIte]
              exact g.2.2 u v e (hu.resolve_left hu') (hv.resolve_left hv')
      · apply Subtype.ext
        funext v
        show (if v = h then 0 else (if v = h then (g : V → ZMod 2) a else (g : V → ZMod 2) v)) =
          (g : V → ZMod 2) v
        by_cases hvh : v = h
        · subst hvh
          simp only [↓reduceIte]
          exact (g.2.1 v hh).symm
        · simp [hvh]
  have e1 : Module.finrank (ZMod 2) (chainSpace G τ') = Module.finrank (ZMod 2) (LinearMap.ker ℓ) := by
    rw [← hrange, LinearMap.finrank_range_of_inj hinj]
  have e2 := LinearMap.finrank_range_add_finrank_ker ℓ
  have e3 : Module.finrank (ZMod 2) (LinearMap.range ℓ) =
      (if (sideGraph G τ).Reachable a b then 0 else 1) := by
    by_cases hr : (sideGraph G τ).Reachable a b
    · simp only [hr, ↓reduceIte]
      rw [Submodule.finrank_eq_zero, eq_bot_iff]
      rintro _ ⟨g, rfl⟩
      rw [Submodule.mem_bot]
      show (g : V → ZMod 2) a + (g : V → ZMod 2) b = 0
      rw [side_const g.2 hr]
      exact zmod2_add_self _
    · simp only [hr, ↓reduceIte]
      let g0 : chainSpace G τ :=
        ⟨fun v => if τ v ∧ (sideGraph G τ).Reachable a v then 1 else 0, by
          refine ⟨fun v hv => by simp [hv], fun u v e hu hv => ?_⟩
          have : (sideGraph G τ).Reachable a u ↔ (sideGraph G τ).Reachable a v :=
            ⟨fun r => r.trans (Adj.reachable ⟨e, hu, hv⟩),
              fun r => r.trans (Adj.reachable ⟨e.symm, hv, hu⟩)⟩
          simp only [hu, hv, true_and, this]⟩
      have hl : ℓ g0 = 1 := by
        show (if τ a ∧ (sideGraph G τ).Reachable a a then (1 : ZMod 2) else 0) +
          (if τ b ∧ (sideGraph G τ).Reachable a b then 1 else 0) = 1
        simp [ha, hr]
      have hle : Module.finrank (ZMod 2) (LinearMap.range ℓ) ≤ 1 := by
        have := Submodule.finrank_le (LinearMap.range ℓ)
        rwa [Module.finrank_self] at this
      have hne : LinearMap.range ℓ ≠ ⊥ := by
        intro hb0
        have : (1 : ZMod 2) ∈ LinearMap.range ℓ := ⟨g0, hl⟩
        rw [hb0, Submodule.mem_bot] at this
        exact one_ne_zero this
      have hpos : 0 < Module.finrank (ZMod 2) (LinearMap.range ℓ) :=
        Nat.pos_of_ne_zero (fun h0 => hne (Submodule.finrank_eq_zero.mp h0))
      omega
  omega

/-! ### The graph side: cycle space of the side edges -/

variable (G) [DecidableEq V] [DecidableRel G.Adj]

/-- The edges of `G` with both ends in `τ`. -/
def SE (τ : V → Prop) := {e : G.edgeSet // ∀ x ∈ (e : Sym2 V), τ x}

noncomputable instance (τ : V → Prop) : Fintype (SE G τ) := by
  unfold SE; classical exact inferInstance

/-- The mod-two incidence matrix of the side edges. -/
def incMat (τ : V → Prop) : Matrix V (SE G τ) (ZMod 2) :=
  fun x e => if x ∈ ((e.1 : G.edgeSet) : Sym2 V) then 1 else 0

lemma sum_mem_pair (g : V → ZMod 2) {u v : V} (huv : u ≠ v) :
    ∑ x, (if x ∈ s(u, v) then (1 : ZMod 2) else 0) * g x = g u + g v := by
  have : ∀ x, (if x ∈ s(u, v) then (1 : ZMod 2) else 0) * g x =
      if x ∈ ({u, v} : Finset V) then g x else 0 := by
    intro x
    simp only [Sym2.mem_iff, Finset.mem_insert, Finset.mem_singleton]
    split_ifs <;> simp
  rw [Finset.sum_congr rfl (fun x _ => this x), Finset.sum_ite_mem, Finset.univ_inter,
    Finset.sum_pair huv]

omit [DecidableRel G.Adj] in
lemma ker_incMat_transpose (τ : V → Prop) :
    LinearMap.ker (incMat G τ).transpose.mulVecLin = constSpace G τ := by
  ext g
  rw [LinearMap.mem_ker, mem_constSpace]
  constructor
  · intro hg u v e hu hv
    have he : s(u, v) ∈ G.edgeSet := e
    let ee : SE G τ := ⟨⟨s(u, v), he⟩, fun x hx => by
      rcases Sym2.mem_iff.mp hx with rfl | rfl
      · exact hu
      · exact hv⟩
    have := congrFun hg ee
    simp only [Matrix.mulVecLin_apply, Matrix.mulVec, dotProduct, Matrix.transpose_apply,
      incMat, Pi.zero_apply] at this
    rw [sum_mem_pair g e.ne] at this
    exact (zmod2_add_eq_zero _ _).mp this
  · intro hg
    funext ee
    simp only [Matrix.mulVecLin_apply, Matrix.mulVec, dotProduct, Matrix.transpose_apply,
      incMat, Pi.zero_apply]
    obtain ⟨⟨e, he⟩, hτ⟩ := ee
    induction e using Sym2.ind with
    | h u v =>
      have hadj : G.Adj u v := he
      simp only
      rw [sum_mem_pair g hadj.ne]
      rw [hg u v hadj (hτ u (Sym2.mem_mk_left u v)) (hτ v (Sym2.mem_mk_right u v))]
      exact zmod2_add_self _

open Classical in
/-- Each side edge has two darts. -/
lemma card_darts_side (τ : V → Prop) :
    #(univ.filter (fun d : G.Dart => τ d.fst ∧ τ d.snd)) = 2 * Fintype.card (SE G τ) := by
  rw [Finset.card_filter]
  rw [← Finset.sum_fiberwise Finset.univ (fun d : G.Dart => RotationSystem.edgeOfDart d)
    (fun d => if τ d.fst ∧ τ d.snd then 1 else 0)]
  have hfib : ∀ e : G.edgeSet, ∑ d ∈ Finset.univ.filter
      (fun d : G.Dart => RotationSystem.edgeOfDart d = e), (if τ d.fst ∧ τ d.snd then 1 else 0) =
      if ∀ x ∈ (e : Sym2 V), τ x then 2 else 0 := by
    intro e
    obtain ⟨d0, hd0⟩ := RotationSystem.edge_of_dart_surjective e
    have hf : Finset.univ.filter (fun d : G.Dart => RotationSystem.edgeOfDart d = e) =
        {d0, d0.symm} := by
      ext d
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert,
        Finset.mem_singleton]
      rw [← hd0, RotationSystem.edge_of_dart_eq_iff]
    rw [hf, Finset.sum_pair (RotationSystem.dart_ne_symm d0)]
    have hmem : (∀ x ∈ (e : Sym2 V), τ x) ↔ τ d0.fst ∧ τ d0.snd := by
      rw [← hd0]
      show (∀ x ∈ d0.edge, τ x) ↔ _
      simp only [Dart.edge, Sym2.mem_iff, forall_eq_or_imp, forall_eq]
    rw [show d0.symm.fst = d0.snd from rfl, show d0.symm.snd = d0.fst from rfl]
    by_cases h1 : τ d0.fst ∧ τ d0.snd
    · have h2 : τ d0.snd ∧ τ d0.fst := ⟨h1.2, h1.1⟩
      rw [ite_eq_left h1, ite_eq_left h2, ite_eq_left (hmem.mpr h1)]
    · have h2 : ¬ (τ d0.snd ∧ τ d0.fst) := fun h => h1 ⟨h.2, h.1⟩
      simp [h1, h2, hmem, -not_and]
  rw [Finset.sum_congr rfl (fun e _ => hfib e), ← Finset.sum_filter, Finset.sum_const,
    smul_eq_mul, mul_comm]
  congr 1
  rw [← Fintype.card_subtype]
  exact Fintype.card_congr (Equiv.refl _)

/-- **Graph side.** `dim Z(S_τ) + |V| = |S_τ| + dim constSpace`, where `Z(S_τ)` is the kernel of
the incidence matrix (even edge sets of side edges). -/
theorem graph_side (τ : V → Prop) :
    Module.finrank (ZMod 2) (LinearMap.ker (incMat G τ).mulVecLin) + Fintype.card V =
      Fintype.card (SE G τ) + Module.finrank (ZMod 2) (constSpace G τ) := by
  have h1 := LinearMap.finrank_range_add_finrank_ker (incMat G τ).mulVecLin
  have h2 := LinearMap.finrank_range_add_finrank_ker (incMat G τ).transpose.mulVecLin
  have hr := Matrix.rank_transpose (incMat G τ)
  unfold Matrix.rank at hr
  rw [ker_incMat_transpose, hr, Module.finrank_fintype_fun_eq_card] at h2
  rw [Module.finrank_fintype_fun_eq_card] at h1
  omega

end graph

/-! ### Darts and edges -/

section darts
variable {V : Type*} [Fintype V] [DecidableEq V] {G : SimpleGraph V} [DecidableRel G.Adj]

/-- A sum over the edges at `x` is a sum over the darts leaving `x`. -/
lemma sum_edges_at {R : Type*} [AddCommMonoid R] (F : G.edgeSet → R) (x : V) :
    ∑ e : G.edgeSet, (if x ∈ (e : Sym2 V) then F e else 0) =
      ∑ d : G.Dart, (if d.fst = x then F (RotationSystem.edgeOfDart d) else 0) := by
  classical
  rw [← Finset.sum_fiberwise Finset.univ (fun d : G.Dart => RotationSystem.edgeOfDart d)
    (fun d => if d.fst = x then F (RotationSystem.edgeOfDart d) else 0)]
  refine Finset.sum_congr rfl fun e _ => ?_
  obtain ⟨d0, hd0⟩ := RotationSystem.edge_of_dart_surjective e
  have hfib : Finset.univ.filter (fun d : G.Dart => RotationSystem.edgeOfDart d = e) =
      {d0, d0.symm} := by
    ext d
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_insert,
      Finset.mem_singleton]
    rw [← hd0, RotationSystem.edge_of_dart_eq_iff]
  rw [hfib, Finset.sum_pair (RotationSystem.dart_ne_symm d0)]
  simp only [RotationSystem.edge_of_dart_symm, hd0]
  rw [show d0.symm.fst = d0.snd from rfl]
  have hmem : x ∈ (e : Sym2 V) ↔ x = d0.fst ∨ x = d0.snd := by
    rw [← hd0]
    show x ∈ d0.edge ↔ _
    rw [Dart.edge, Sym2.mem_iff]
  have hne := d0.adj.ne
  by_cases h1 : d0.fst = x
  · have h2 : ¬ d0.snd = x := fun h => hne (h1.trans h.symm)
    simp [h1, h2, hmem]
  · by_cases h2 : d0.snd = x
    · simp [h1, h2, hmem]
    · have : ¬ (x ∈ (e : Sym2 V)) := by
        rw [hmem]
        rintro (h | h)
        · exact h1 h.symm
        · exact h2 h.symm
      simp [h1, h2, this]

end darts

/-! ### The face side (`Fills`) -/

section faces
variable {n : ℕ} (M : SphericalMap n)

/-- Face functions constant across every edge that is not a side edge of `τ`. -/
def faceSpace (τ : Fin n → Prop) : Submodule (ZMod 2) (M.Face → ZMod 2) where
  carrier := {a | ∀ d : M.Dart, ¬ (τ d.fst ∧ τ d.snd) → a (M.faceOf d) = a (M.faceOf d.symm)}
  add_mem' := by
    intro a a' ha ha' d hd
    simp [ha d hd, ha' d hd]
  zero_mem' := fun _ _ => rfl
  smul_mem' := by
    intro r a ha d hd
    simp [ha d hd]

/-- `γ`: the dimension of the face functions constant across every edge (one per component). -/
noncomputable def gammaM : ℕ := Module.finrank (ZMod 2) (faceSpace M (fun _ => False))

/-- The boundary of a face function, on the side edges. -/
noncomputable def bdry (τ : Fin n → Prop) : (M.Face → ZMod 2) →ₗ[ZMod 2] (SE M.graph τ → ZMod 2) where
  toFun a e := SphericalMap.faceSum M a e.1
  map_add' a a' := by
    funext e
    simp only [SphericalMap.faceSum, Pi.add_apply]
    abel_nf
  map_smul' r a := by
    funext e
    simp only [SphericalMap.faceSum, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    exact (mul_add r _ _).symm

variable {M}

lemma faceSum_eq_zero_of_mem {τ : Fin n → Prop} {a : M.Face → ZMod 2} (ha : a ∈ faceSpace M τ)
    (e : M.graph.edgeSet) (he : ¬ ∀ x ∈ (e : Sym2 (Fin n)), τ x) :
    SphericalMap.faceSum M a e = 0 := by
  obtain ⟨d, rfl⟩ := RotationSystem.edge_of_dart_surjective e
  rw [SphericalMap.cycle_faceSum_edgeOfDart]
  have : ¬ (τ d.fst ∧ τ d.snd) := by
    rintro ⟨h1, h2⟩
    apply he
    intro x hx
    have hx' : x ∈ d.edge := hx
    rcases Sym2.mem_iff.mp hx' with rfl | rfl
    · exact h1
    · exact h2
  rw [ha d this]
  exact zmod2_add_self _

/-- Face boundaries are even. -/
lemma faceSum_even (a : M.Face → ZMod 2) (x : Fin n) :
    ∑ e : M.graph.edgeSet, (if x ∈ (e : Sym2 (Fin n)) then SphericalMap.faceSum M a e else 0) = 0 := by
  classical
  rw [sum_edges_at]
  simp only [SphericalMap.cycle_faceSum_edgeOfDart]
  have hnext : ∀ d : M.Dart, M.faceOf d.symm = M.faceOf (M.rotation.next d) := by
    intro d
    have : M.rotation.next d = M.rotation.faceNext d.symm := by
      rw [RotationSystem.face_next_apply, Dart.symm_symm]
    rw [this, SphericalMap.faceOf, RotationSystem.face_of_face_next]
  have hperm : ∑ d : M.Dart, (if d.fst = x then a (M.faceOf (M.rotation.next d)) else 0) =
      ∑ d : M.Dart, (if d.fst = x then a (M.faceOf d) else 0) := by
    rw [← Equiv.sum_comp M.rotation.next (fun d => if d.fst = x then a (M.faceOf d) else 0)]
    refine Finset.sum_congr rfl fun d _ => ?_
    rw [M.rotation.next_fst]
  have : ∀ d : M.Dart, (if d.fst = x then a (M.faceOf d) + a (M.faceOf d.symm) else 0) =
      (if d.fst = x then a (M.faceOf d) else 0) +
        (if d.fst = x then a (M.faceOf (M.rotation.next d)) else 0) := by
    intro d
    rw [hnext d]
    split_ifs <;> simp
  rw [Finset.sum_congr rfl (fun d _ => this d), Finset.sum_add_distrib, hperm]
  exact zmod2_add_self _

/-- **Face side.** By `Fills`, the boundary map from `faceSpace τ` onto the even side-edge sets
is onto, with kernel the face functions constant across every edge. -/
theorem face_side (τ : Fin n → Prop) :
    Module.finrank (ZMod 2) (LinearMap.ker (incMat M.graph τ).mulVecLin) + gammaM M =
      Module.finrank (ZMod 2) (faceSpace M τ) := by
  classical
  set K := LinearMap.ker (incMat M.graph τ).mulVecLin with hK
  -- the sum over side edges of a function vanishing off the side edges
  have hsub : ∀ (F : M.graph.edgeSet → ZMod 2),
      (∀ e : M.graph.edgeSet, (¬ ∀ x ∈ (e : Sym2 (Fin n)), τ x) → F e = 0) →
      ∀ x, ∑ e : SE M.graph τ, (if x ∈ ((e.1 : M.graph.edgeSet) : Sym2 (Fin n)) then F e.1 else 0) =
        ∑ e : M.graph.edgeSet, (if x ∈ (e : Sym2 (Fin n)) then F e else 0) := by
    intro F hF x
    rw [← Fintype.sum_subtype_add_sum_subtype (fun e : M.graph.edgeSet => ∀ x ∈ (e : Sym2 (Fin n)), τ x)]
    have : ∑ e : {e : M.graph.edgeSet // ¬ ∀ x ∈ (e : Sym2 (Fin n)), τ x},
        (if x ∈ ((e.1 : M.graph.edgeSet) : Sym2 (Fin n)) then F e.1 else 0) = 0 :=
      Finset.sum_eq_zero fun e _ => by simp [hF e.1 e.2]
    rw [this, add_zero]
    exact Fintype.sum_equiv (ι := SE M.graph τ)
      (κ := {e : M.graph.edgeSet // ∀ x ∈ (e : Sym2 (Fin n)), τ x}) (Equiv.refl _) _ _
      (fun _ => rfl)
  have hmulVec : ∀ (ψ : SE M.graph τ → ZMod 2) x, (incMat M.graph τ).mulVecLin ψ x =
      ∑ e : SE M.graph τ, (if x ∈ ((e.1 : M.graph.edgeSet) : Sym2 (Fin n)) then ψ e else 0) := by
    intro ψ x
    simp only [Matrix.mulVecLin_apply, Matrix.mulVec, dotProduct, incMat]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp
  have hin : ∀ a ∈ faceSpace M τ, bdry M τ a ∈ K := by
    intro a ha
    rw [hK, LinearMap.mem_ker]
    funext x
    rw [hmulVec]
    have := hsub (fun e => SphericalMap.faceSum M a e) (fun e he => faceSum_eq_zero_of_mem ha e he) x
    simp only [bdry, LinearMap.coe_mk, AddHom.coe_mk]
    rw [this]
    exact faceSum_even a x
  let D : faceSpace M τ →ₗ[ZMod 2] K :=
    LinearMap.codRestrict K ((bdry M τ).comp (faceSpace M τ).subtype) (fun a => hin a.1 a.2)
  have hsurj : Function.Surjective D := by
    rintro ⟨ψ, hψ⟩
    rw [hK, LinearMap.mem_ker] at hψ
    let φ : M.graph.edgeSet → ZMod 2 := fun e =>
      if h : ∀ x ∈ (e : Sym2 (Fin n)), τ x then ψ ⟨e, h⟩ else 0
    have hφe : ∀ e : SE M.graph τ, φ e.1 = ψ e := by
      intro e
      simp only [φ]
      split_ifs with hh
      · rfl
      · exact absurd e.2 hh
    have heven : ∀ x, edgeIncidence M.graph φ x = 0 := by
      intro x
      have h1 := congrFun hψ x
      rw [hmulVec] at h1
      have h2 := hsub φ (fun e he => by simp [φ, he]) x
      unfold edgeIncidence
      rw [← h2]
      refine Eq.trans ?_ h1
      refine Finset.sum_congr rfl fun e _ => ?_
      rw [hφe]
    obtain ⟨c, hc⟩ := M.fills φ heven
    have hcS : c ∈ faceSpace M τ := by
      intro d hd
      have := hc d
      have h0 : φ (RotationSystem.edgeOfDart d) = 0 := by
        have : ¬ ∀ x ∈ ((RotationSystem.edgeOfDart d : M.graph.edgeSet) : Sym2 (Fin n)), τ x := by
          intro hall
          exact hd ⟨hall _ (Sym2.mem_mk_left _ _), hall _ (Sym2.mem_mk_right _ _)⟩
        simp [φ, this]
      rw [h0] at this
      exact (zmod2_add_eq_zero _ _).mp this.symm
    refine ⟨⟨c, hcS⟩, ?_⟩
    apply Subtype.ext
    funext e
    show SphericalMap.faceSum M c e.1 = ψ e
    have := hc (SphericalMap.edgeDart M.graph e.1)
    rw [SphericalMap.edgeDart_spec] at this
    unfold SphericalMap.faceSum
    rw [← this]
    exact hφe e
  have hker : LinearMap.ker D = (faceSpace M (fun _ => False)).comap (faceSpace M τ).subtype := by
    ext ⟨a, ha⟩
    simp only [LinearMap.mem_ker, Submodule.mem_comap, Submodule.subtype_apply]
    constructor
    · intro h0 d _
      by_cases hd : τ d.fst ∧ τ d.snd
      · have he : ∀ x ∈ ((RotationSystem.edgeOfDart d : M.graph.edgeSet) : Sym2 (Fin n)), τ x := by
          intro x hx
          have hx' : x ∈ d.edge := hx
          rcases Sym2.mem_iff.mp hx' with rfl | rfl
          · exact hd.1
          · exact hd.2
        have := congrArg (fun z : K => (z : SE M.graph τ → ZMod 2) ⟨_, he⟩) h0
        simp only [D, LinearMap.codRestrict_apply, LinearMap.comp_apply, Submodule.subtype_apply,
          bdry, LinearMap.coe_mk, AddHom.coe_mk, Submodule.coe_zero] at this
        rw [SphericalMap.cycle_faceSum_edgeOfDart] at this
        exact (zmod2_add_eq_zero _ _).mp this
      · exact ha d hd
    · intro h0
      apply Subtype.ext
      funext e
      simp only [D, LinearMap.codRestrict_apply, LinearMap.comp_apply, Submodule.subtype_apply,
        bdry, LinearMap.coe_mk, AddHom.coe_mk, Submodule.coe_zero, Pi.zero_apply]
      exact faceSum_eq_zero_of_mem (τ := fun _ => False) h0 e.1 (fun h => by
        obtain ⟨d, hd⟩ := RotationSystem.edge_of_dart_surjective e.1
        have := h d.fst (by rw [← hd]; exact Sym2.mem_mk_left _ _)
        exact this)
  have hle : faceSpace M (fun _ => False) ≤ faceSpace M τ := fun a ha d _ => ha d (fun h => h.1)
  have e1 := LinearMap.finrank_range_add_finrank_ker D
  rw [LinearMap.range_eq_top.mpr hsurj, finrank_top, hker,
    (Submodule.comapSubtypeEquivOfLe hle).finrank_eq] at e1
  unfold gammaM
  exact e1

/-! ### Faces and chains -/

lemma tri3 (htri : M.Triangulated) (d : M.Dart) :
    M.rotation.faceNext (M.rotation.faceNext (M.rotation.faceNext d)) = d := by
  have := M.rotation.face_next_iterate_length d
  rw [htri d] at this
  simpa only [Function.iterate_succ_apply', Function.iterate_zero_apply] using this

/-- Faces around a vertex off `τ` carry one value of a function in `faceSpace τ`. -/
lemma faceSpace_rot {τ : Fin n → Prop} {a : M.Face → ZMod 2} (ha : a ∈ faceSpace M τ)
    {d e : M.Dart} (hx : ¬ τ d.fst) (hde : d.fst = e.fst) :
    a (M.faceOf d) = a (M.faceOf e) := by
  have step : ∀ d' : M.Dart, ¬ τ d'.fst →
      a (M.faceOf (M.rotation.next d')) = a (M.faceOf d') := by
    intro d' hd'
    have : M.rotation.next d' = M.rotation.faceNext d'.symm := by
      rw [RotationSystem.face_next_apply, Dart.symm_symm]
    rw [this, SphericalMap.faceOf, RotationSystem.face_of_face_next]
    exact (ha d' (fun h => hd' h.1)).symm
  have itf : ∀ j : ℕ, ((M.rotation.next : M.Dart → M.Dart)^[j] d).fst = d.fst := by
    intro j
    induction j with
    | zero => rfl
    | succ j ihj => rw [Function.iterate_succ_apply', M.rotation.next_fst, ihj]
  obtain ⟨k, hk⟩ := M.rotation.cyclic d e hde
  subst hk
  clear hde
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', step _ (by rw [itf k]; exact hx), ih]

variable (htri : M.Triangulated)
include htri

/-- The three corners of the face of `d`. -/
def corner (d : M.Dart) (w : Fin n) : Prop :=
  w = d.fst ∨ w = d.snd ∨ w = (M.rotation.faceNext d).snd

omit htri in
lemma corner_adj (htri : M.Triangulated) (d : M.Dart) {u w : Fin n} (hu : corner d u)
    (hw : corner d w) : u = w ∨ M.graph.Adj u w := by
  have h3 := tri3 htri d
  have a1 : M.graph.Adj d.fst d.snd := d.adj
  have a2 : M.graph.Adj d.snd (M.rotation.faceNext d).snd := by
    have := (M.rotation.faceNext d).adj
    rwa [M.rotation.face_next_fst] at this
  have a3 : M.graph.Adj (M.rotation.faceNext d).snd d.fst := by
    have := (M.rotation.faceNext (M.rotation.faceNext d)).adj
    rw [M.rotation.face_next_fst] at this
    have e : (M.rotation.faceNext (M.rotation.faceNext d)).snd = d.fst := by
      have := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
      rw [h3] at this
      exact this.symm
    rwa [e] at this
  rcases hu with rfl | rfl | rfl <;> rcases hw with rfl | rfl | rfl <;>
    first | exact Or.inl rfl | exact Or.inr a1 | exact Or.inr a1.symm | exact Or.inr a2 |
      exact Or.inr a2.symm | exact Or.inr a3 | exact Or.inr a3.symm

omit htri in
lemma corner_next (htri : M.Triangulated) (d : M.Dart) {w : Fin n}
    (hw : corner (M.rotation.faceNext d) w) : corner d w := by
  have h3 := tri3 htri d
  have e : (M.rotation.faceNext (M.rotation.faceNext d)).snd = d.fst := by
    have := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
    rw [h3] at this
    exact this.symm
  unfold corner at hw ⊢
  rw [M.rotation.face_next_fst, e] at hw
  tauto

open Classical in
/-- The value of a chain function on the face of `d`: at its first corner off `τ`. -/
noncomputable def faceVal (τ : Fin n → Prop) (g : Fin n → ZMod 2) (d : M.Dart) : ZMod 2 :=
  if ¬ τ d.fst then g d.fst else if ¬ τ d.snd then g d.snd else g (M.rotation.faceNext d).snd

omit htri in
lemma faceVal_eq (htri : M.Triangulated) {τ : Fin n → Prop}
    (hface : ∀ d : M.Dart, ¬ τ d.fst ∨ ¬ τ d.snd ∨ ¬ τ (M.rotation.faceNext d).snd)
    {g : Fin n → ZMod 2} (hg : g ∈ chainSpace M.graph (fun v => ¬ τ v)) (d : M.Dart)
    {w : Fin n} (hw : corner d w) (hwt : ¬ τ w) : faceVal τ g d = g w := by
  have same : ∀ u, corner d u → ¬ τ u → g u = g w := by
    intro u hu hut
    rcases corner_adj htri d hu hw with rfl | e
    · rfl
    · exact hg.2 u w e hut hwt
  unfold faceVal
  by_cases h1 : τ d.fst
  · by_cases h2 : τ d.snd
    · rw [ite_eq_right (not_not.mpr h1), ite_eq_right (not_not.mpr h2)]
      exact same _ (Or.inr (Or.inr rfl))
        (((hface d).resolve_left (not_not.mpr h1)).resolve_left (not_not.mpr h2))
    · rw [ite_eq_right (not_not.mpr h1), ite_eq_left h2]
      exact same _ (Or.inr (Or.inl rfl)) h2
  · rw [ite_eq_left h1]
    exact same _ (Or.inl rfl) h1

omit htri in
lemma faceVal_corner {τ : Fin n → Prop}
    (hface : ∀ d : M.Dart, ¬ τ d.fst ∨ ¬ τ d.snd ∨ ¬ τ (M.rotation.faceNext d).snd)
    (d : M.Dart) : ∃ w, corner d w ∧ ¬ τ w := by
  rcases hface d with h | h | h
  · exact ⟨_, Or.inl rfl, h⟩
  · exact ⟨_, Or.inr (Or.inl rfl), h⟩
  · exact ⟨_, Or.inr (Or.inr rfl), h⟩

omit htri in
lemma faceVal_next (htri : M.Triangulated) {τ : Fin n → Prop}
    (hface : ∀ d : M.Dart, ¬ τ d.fst ∨ ¬ τ d.snd ∨ ¬ τ (M.rotation.faceNext d).snd)
    {g : Fin n → ZMod 2} (hg : g ∈ chainSpace M.graph (fun v => ¬ τ v)) (d : M.Dart) :
    faceVal τ g d = faceVal τ g (M.rotation.faceNext d) := by
  obtain ⟨w, hw, hwt⟩ := faceVal_corner hface (M.rotation.faceNext d)
  rw [faceVal_eq htri hface hg _ hw hwt, faceVal_eq htri hface hg _ (corner_next htri d hw) hwt]

omit htri in
lemma faceVal_add {τ : Fin n → Prop} (g g' : Fin n → ZMod 2) (d : M.Dart) :
    faceVal τ (g + g') d = faceVal τ g d + faceVal τ g' d := by
  unfold faceVal
  split_ifs <;> rfl

omit htri in
lemma faceVal_smul {τ : Fin n → Prop} (r : ZMod 2) (g : Fin n → ZMod 2) (d : M.Dart) :
    faceVal τ (r • g) d = r * faceVal τ g d := by
  unfold faceVal
  split_ifs <;> rfl

omit htri in
/-- **Faces ↔ chains.** If every face has a corner off `τ`, the face functions constant across
the non-side edges correspond to the chain functions of the complementary side. -/
theorem finrank_faceSpace (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w)
    (d0 : M.Dart) {τ : Fin n → Prop}
    (hface : ∀ d : M.Dart, ¬ τ d.fst ∨ ¬ τ d.snd ∨ ¬ τ (M.rotation.faceNext d).snd) :
    Module.finrank (ZMod 2) (faceSpace M τ) =
      Module.finrank (ZMod 2) (chainSpace M.graph (fun v => ¬ τ v)) := by
  classical
  let dv : Fin n → M.Dart := fun v => ⟨(v, Classical.choose (hiso v)), Classical.choose_spec (hiso v)⟩
  let Θf : (M.Face → ZMod 2) → Fin n → ZMod 2 := fun a v => if ¬ τ v then a (M.faceOf (dv v)) else 0
  have hΘ : ∀ a ∈ faceSpace M τ, Θf a ∈ chainSpace M.graph (fun v => ¬ τ v) := by
    intro a ha
    refine ⟨fun v hv => by simp [Θf, hv], fun u v e hu hv => ?_⟩
    simp only [Θf, hu, hv, not_false_eq_true, ↓reduceIte]
    let duv : M.Dart := ⟨(u, v), e⟩
    rw [faceSpace_rot ha (d := dv u) (e := duv) hu rfl, ha duv (fun h => hu h.1),
      faceSpace_rot ha (d := duv.symm) (e := dv v) hv rfl]
  have hresp : ∀ g ∈ chainSpace M.graph (fun v => ¬ τ v), ∀ d e : M.Dart,
      M.rotation.FaceRelation d e → faceVal τ g d = faceVal τ g e := by
    intro g hg d e hde
    induction hde with
    | refl => rfl
    | step d => exact faceVal_next htri hface hg d
    | symm _ ih => exact ih.symm
    | trans _ _ ih1 ih2 => exact ih1.trans ih2
  let Ψf : chainSpace M.graph (fun v => ¬ τ v) → M.Face → ZMod 2 := fun g =>
    Sum.elim (Quotient.lift (faceVal τ (g : Fin n → ZMod 2)) (hresp g g.2)) (fun _ => 0)
  have hΨ : ∀ g d, Ψf g (M.faceOf d) = faceVal τ (g : Fin n → ZMod 2) d := fun _ _ => rfl
  have hΨS : ∀ g, Ψf g ∈ faceSpace M τ := by
    intro g d hd
    rw [hΨ, hΨ]
    have hw : ∃ w, corner d w ∧ corner d.symm w ∧ ¬ τ w := by
      by_cases h1 : τ d.fst
      · exact ⟨d.snd, Or.inr (Or.inl rfl), Or.inl rfl, fun h2 => hd ⟨h1, h2⟩⟩
      · exact ⟨d.fst, Or.inl rfl, Or.inr (Or.inl rfl), h1⟩
    obtain ⟨w, h1, h2, h3⟩ := hw
    rw [faceVal_eq htri hface g.2 _ h1 h3, faceVal_eq htri hface g.2 _ h2 h3]
  have hface_eq : ∀ (a : M.Face → ZMod 2), a ∈ faceSpace M τ → ∀ d : M.Dart, ∀ w, corner d w →
      ¬ τ w → a (M.faceOf (dv w)) = a (M.faceOf d) := by
    intro a ha d w hw hwt
    rcases hw with rfl | rfl | rfl
    · exact faceSpace_rot ha hwt rfl
    · rw [faceSpace_rot ha (e := M.rotation.faceNext d) hwt (M.rotation.face_next_fst d).symm]
      exact congrArg a (RotationSystem.face_of_face_next _ d)
    · have e1 : (M.rotation.faceNext (M.rotation.faceNext d)).fst = (M.rotation.faceNext d).snd :=
        M.rotation.face_next_fst _
      rw [faceSpace_rot ha (e := M.rotation.faceNext (M.rotation.faceNext d)) hwt e1.symm]
      exact congrArg a ((RotationSystem.face_of_face_next _ _).trans
        (RotationSystem.face_of_face_next _ d))
  let E : faceSpace M τ ≃ₗ[ZMod 2] chainSpace M.graph (fun v => ¬ τ v) :=
    { toFun := fun a => ⟨Θf a, hΘ a a.2⟩
      map_add' := fun a a' => by
        apply Subtype.ext
        funext v
        simp only [Θf, Submodule.coe_add, Pi.add_apply]
        split_ifs <;> simp
      map_smul' := fun r a => by
        apply Subtype.ext
        funext v
        simp only [Θf, Submodule.coe_smul, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
        split_ifs <;> simp
      invFun := fun g => ⟨Ψf g, hΨS g⟩
      left_inv := by
        intro a
        apply Subtype.ext
        funext f
        rcases f with q | ⟨_, hE⟩
        · induction q using Quotient.inductionOn with
          | h d =>
            show faceVal τ (Θf a) d = (a : M.Face → ZMod 2) (M.faceOf d)
            obtain ⟨w, hw, hwt⟩ := faceVal_corner hface d
            rw [faceVal_eq htri hface (hΘ a a.2) d hw hwt]
            simp only [Θf, hwt, not_false_eq_true, ↓reduceIte]
            exact hface_eq a a.2 d w hw hwt
        · exact (hE.false d0).elim
      right_inv := by
        intro g
        apply Subtype.ext
        funext v
        show Θf (Ψf g) v = (g : Fin n → ZMod 2) v
        by_cases hv : τ v
        · simp only [Θf, hv, not_true_eq_false, ↓reduceIte]
          exact (g.2.1 v (not_not.mpr hv)).symm
        · simp only [Θf, hv, not_false_eq_true, ↓reduceIte]
          rw [hΨ]
          exact faceVal_eq htri hface g.2 (dv v) (Or.inl rfl) hv }
  exact E.finrank_eq

end faces

/-! ### Tutte's identity and Euler's formula -/

section assembled
variable {n : ℕ} {M : SphericalMap n}

/-- **Tutte's identity, sides form.** On a triangulated spherical map without isolated vertices,
for a vertex predicate `τ` such that every face has a corner off `τ`:
`|S_τ| + (#τ-chains) + γ = #τ + (#(¬τ)-chains)`. On a connected map (`γ = 1`) this is Tutte's
`p(XY) − p(ZW) = |X| + |Y| − e(XY) − 1`. -/
theorem tutte_sides (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w) (d0 : M.Dart)
    (τ : Fin n → Prop) [DecidablePred τ]
    (hface : ∀ d : M.Dart, ¬ τ d.fst ∨ ¬ τ d.snd ∨ ¬ τ (M.rotation.faceNext d).snd) :
    Fintype.card (SE M.graph τ) + Module.finrank (ZMod 2) (chainSpace M.graph τ) + gammaM M =
      #(univ.filter τ) + Module.finrank (ZMod 2) (chainSpace M.graph (fun v => ¬ τ v)) := by
  classical
  have g1 := graph_side M.graph τ
  have g2 := finrank_constSpace (G := M.graph) τ
  have f1 := face_side (M := M) τ
  have f2 := finrank_faceSpace htri hiso d0 hface
  have hc := Finset.card_filter_add_card_filter_not (s := (univ : Finset (Fin n))) τ
  rw [Finset.card_univ] at hc
  omega

/-- **Euler's formula** for a triangulated spherical map without isolated vertices:
`|E| + 6γ = 3n` (so `|E| = 3n − 6` when connected). -/
theorem euler_tri (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w) (d0 : M.Dart) :
    Fintype.card M.graph.edgeSet + 6 * gammaM M = 3 * n := by
  classical
  have g1 := graph_side M.graph (fun _ => True)
  have g2 := finrank_constSpace (G := M.graph) (fun _ => True)
  have f1 := face_side (M := M) (fun _ => True)
  have f2 := finrank_faceSpace htri hiso d0 (τ := fun _ => False) (fun _ => Or.inl not_false)
  have hcong : chainSpace M.graph (fun _ : Fin n => ¬ False) = chainSpace M.graph (fun _ => True) :=
    chainSpace_congr (fun _ => by simp)
  rw [hcong] at f2
  have hgam : gammaM M = Module.finrank (ZMod 2) (chainSpace M.graph (fun _ => True)) := f2
  have htop : faceSpace M (fun _ => True) = ⊤ := by
    rw [eq_top_iff]
    intro a _ d hd
    exact absurd ⟨trivial, trivial⟩ hd
  rw [htop, finrank_top, Module.finrank_fintype_fun_eq_card] at f1
  have hSE : Fintype.card (SE M.graph (fun _ => True)) = Fintype.card M.graph.edgeSet :=
    Fintype.card_congr (Equiv.subtypeUnivEquiv (fun e x _ => trivial))
  have hfaces : 3 * Fintype.card M.Face = Fintype.card M.Dart := by
    rw [← M.rotation.sum_face_lengths_eq_card_darts]
    have : ∀ f : M.Face, M.rotation.faceLength f = 3 := by
      intro f
      rcases f with q | ⟨_, hE⟩
      · induction q using Quotient.inductionOn with
        | h d => exact htri d
      · exact (hE.false d0).elim
    rw [Finset.sum_congr rfl (fun f _ => this f), Finset.sum_const, Finset.card_univ, smul_eq_mul,
      mul_comm]
  have hdart := SimpleGraph.card_dart_eq_twice_card_edges (G := M.graph)
  rw [SimpleGraph.edgeFinset_card] at hdart
  rw [Fintype.card_fin] at g1
  simp only [not_true_eq_false, Finset.filter_false, Finset.card_empty, add_zero] at g2
  have hdd : Fintype.card M.Dart = Fintype.card M.graph.Dart := Fintype.card_congr (Equiv.refl _)
  omega

end assembled

end SimpleGraph.TutteSides

#print axioms SimpleGraph.TutteSides.finrank_chainSpace
#print axioms SimpleGraph.TutteSides.finrank_chainSpace_insert
#print axioms SimpleGraph.TutteSides.graph_side
#print axioms SimpleGraph.TutteSides.face_side
#print axioms SimpleGraph.TutteSides.finrank_faceSpace
#print axioms SimpleGraph.TutteSides.tutte_sides
#print axioms SimpleGraph.TutteSides.euler_tri
