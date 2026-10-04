/-
  ChainEquality.lean — reachability in an (a,b)-Kempe chain after deleting
  a vertex whose colour lies outside {a, b}.

  `colour5_isolated_in_bichromatic_14` only shows that paper colour 5 is
  isolated in B_{a,b}. `bichromatic_adj_delete_irrelevant` is `rfl` and does
  not mention vertex deletion. Neither one identifies walks in G with walks
  in the induced subgraph on V \ {v}.

  Target: 0 sorry
-/

import KempeReconfiguration.ChainLifting
import Mathlib.Combinatorics.SimpleGraph.Subgraph

namespace KempeReconfiguration

variable {V : Type*}

/-- A chain in the image of an embedding comes from a chain in the domain. -/
lemma exists_preimage_reflTransGen_map
    {α β : Type*} {r : α → α → Prop} (f : α ↪ β) {a : α} {b : β}
    (h : Relation.ReflTransGen (Relation.Map r f f) (f a) b) :
    ∃ b' : α, f b' = b ∧ Relation.ReflTransGen r a b' := by
  induction h with
  | refl =>
    exact ⟨a, rfl, Relation.ReflTransGen.refl⟩
  | tail _ hstep ih =>
    obtain ⟨c', hc', hrel⟩ := ih
    obtain ⟨x, y, hxy, hx, hy⟩ := hstep
    have hxeq : x = c' := f.injective (hx.trans hc'.symm)
    subst hxeq
    exact ⟨y, hy, hrel.tail hxy⟩

/-- Reflexive-transitive closure commutes with pushing a relation along an embedding. -/
lemma reflTransGen_map_embedding_iff
    {α β : Type*} {r : α → α → Prop} (f : α ↪ β) {a b : α} :
    Relation.ReflTransGen (Relation.Map r f f) (f a) (f b) ↔
      Relation.ReflTransGen r a b := by
  constructor
  · intro h
    obtain ⟨b', hb', hrel⟩ := exists_preimage_reflTransGen_map f h
    obtain rfl := f.injective hb'
    exact hrel
  · intro h
    exact Relation.ReflTransGen.lift (⇑f)
      (fun x y hxy => ⟨x, y, hxy, rfl, rfl⟩) h

/-- Vertices of an induced graph are reachable in the spanning graph on `V`
if and only if they are reachable in the induced graph. -/
lemma reachable_spanningCoe_iff {s : Set V} (G : SimpleGraph s) {a b : s} :
    G.spanningCoe.Reachable (a : V) (b : V) ↔ G.Reachable a b := by
  rw [SimpleGraph.reachable_iff_reflTransGen, SimpleGraph.reachable_iff_reflTransGen]
  exact reflTransGen_map_embedding_iff (Function.Embedding.subtype s)

/-- If `v` is isolated, `G` is the spanning graph of its induced subgraph on `V \ {v}`. -/
lemma eq_induce_spanningCoe_of_isolated {G : SimpleGraph V} {v : V}
    (hiso : ∀ u, ¬ G.Adj v u) :
    G = (G.induce (({v} : Set V)ᶜ)).spanningCoe := by
  ext x y
  constructor
  · intro hxy
    have hx : x ≠ v := by
      intro hxv
      exact hiso y (hxv ▸ hxy)
    have hy : y ≠ v := by
      intro hyv
      exact hiso x (hyv ▸ hxy.symm)
    exact ⟨⟨x, Set.mem_compl_singleton_iff.mpr hx⟩,
      ⟨y, Set.mem_compl_singleton_iff.mpr hy⟩, hxy, rfl, rfl⟩
  · intro hxy
    obtain ⟨x', y', h, rfl, rfl⟩ := hxy
    exact h

/-- An isolated vertex is not reachable from a different vertex. -/
lemma ne_of_reachable_isolated {G : SimpleGraph V} {v x y : V}
    (hiso : ∀ u, ¬ G.Adj v u) (hx : x ≠ v) (h : G.Reachable x y) : y ≠ v := by
  rw [SimpleGraph.reachable_iff_reflTransGen] at h
  induction h with
  | refl => exact hx
  | tail _ hstep ih =>
    intro hy
    exact hiso _ (hy ▸ hstep.symm)

/-- If `v` is isolated and `u, w ≠ v`, then `u` is reachable from `w` in `G`
if and only if it is reachable in the induced subgraph on `V \ {v}`. -/
lemma reachable_iff_induce_compl_of_isolated {G : SimpleGraph V} {v : V}
    (hiso : ∀ u, ¬ G.Adj v u) {u w : V} (hu : u ≠ v) (hw : w ≠ v) :
    G.Reachable w u ↔
      (G.induce (({v} : Set V)ᶜ)).Reachable
        ⟨w, Set.mem_compl_singleton_iff.mpr hw⟩
        ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩ := by
  let s : Set V := ({v} : Set V)ᶜ
  let hw' : w ∈ s := Set.mem_compl_singleton_iff.mpr hw
  let hu' : u ∈ s := Set.mem_compl_singleton_iff.mpr hu
  have hG : G = (G.induce s).spanningCoe := eq_induce_spanningCoe_of_isolated hiso
  constructor
  · intro h
    have hspan : (G.induce s).spanningCoe.Reachable w u := by
      rwa [← hG]
    exact (reachable_spanningCoe_iff (G.induce s) (a := ⟨w, hw'⟩) (b := ⟨u, hu'⟩)).mp hspan
  · intro h
    have hspan : (G.induce s).spanningCoe.Reachable w u :=
      (reachable_spanningCoe_iff (G.induce s) (a := ⟨w, hw'⟩) (b := ⟨u, hu'⟩)).mpr h
    rwa [hG]

variable [Fintype V] [DecidableEq V] {k : ℕ}

/-- If `c v ∉ {a, b}` and `u, w ≠ v`, then `u` is reachable from `w` in the
`(a,b)`-bichromatic subgraph of `G` if and only if the corresponding vertices
are reachable in the `(a,b)`-bichromatic subgraph of `G` induced on `V \ {v}`. -/
theorem bichromatic_reachable_iff_induce_delete
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (v : V)
    (hva : c v ≠ a) (hvb : c v ≠ b)
    {u w : V} (hu : u ≠ v) (hw : w ≠ v) :
    (bichromaticSubgraph G c a b).Reachable w u ↔
      (bichromaticSubgraph (G.induce (({v} : Set V)ᶜ)) (fun x => c x.val) a b).Reachable
        ⟨w, Set.mem_compl_singleton_iff.mpr hw⟩
        ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩ := by
  have hiso : ∀ x, ¬ (bichromaticSubgraph G c a b).Adj v x :=
    vertex_not_in_bichromatic G c a b v hva hvb
  have hreach := reachable_iff_induce_compl_of_isolated hiso hu hw
  -- `(B).induce` is definitionally the bichromatic subgraph of `G.induce`.
  simpa using hreach

/-- The same identification, written with `inSameKempeChain`. -/
theorem inSameKempeChain_iff_induce_delete
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (v : V)
    (hva : c v ≠ a) (hvb : c v ≠ b)
    {u w : V} (hu : u ≠ v) (hw : w ≠ v) :
    inSameKempeChain G c a b w u ↔
      inSameKempeChain (G.induce (({v} : Set V)ᶜ)) (fun x => c x.val) a b
        ⟨w, Set.mem_compl_singleton_iff.mpr hw⟩
        ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩ := by
  simpa [inSameKempeChain] using
    bichromatic_reachable_iff_induce_delete G c a b v hva hvb hu hw

/-- Lemma 5.1 for reachability: paper colour 5 is `(4 : Fin 5)`, and
`a, b ≠ 4` are the colours in `{0,1,2,3}`. -/
theorem colour5_bichromatic_reachable_iff_induce_delete
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin 5) (v : V) (hv5 : c v = 4)
    (a b : Fin 5) (ha : a ≠ 4) (hb : b ≠ 4)
    {u w : V} (hu : u ≠ v) (hw : w ≠ v) :
    (bichromaticSubgraph G c a b).Reachable w u ↔
      (bichromaticSubgraph (G.induce (({v} : Set V)ᶜ)) (fun x => c x.val) a b).Reachable
        ⟨w, Set.mem_compl_singleton_iff.mpr hw⟩
        ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩ :=
  bichromatic_reachable_iff_induce_delete G c a b v (hv5.symm ▸ ha.symm) (hv5.symm ▸ hb.symm) hu hw

/-- The set of vertices reachable from `u ≠ v` in `B_{a,b}(G,c)` is the set of
vertices other than `v` reachable from `u` in `B_{a,b}` of the induced subgraph
on `V \ {v}`. -/
theorem bichromatic_reachableSet_eq_induce_delete
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (v : V)
    (hva : c v ≠ a) (hvb : c v ≠ b)
    {u : V} (hu : u ≠ v) :
    {w | (bichromaticSubgraph G c a b).Reachable u w} =
      {w | ∃ hw : w ≠ v,
        (bichromaticSubgraph (G.induce (({v} : Set V)ᶜ)) (fun x => c x.val) a b).Reachable
          ⟨u, Set.mem_compl_singleton_iff.mpr hu⟩
          ⟨w, Set.mem_compl_singleton_iff.mpr hw⟩} := by
  ext w
  constructor
  · intro h
    have hiso : ∀ x, ¬ (bichromaticSubgraph G c a b).Adj v x :=
      vertex_not_in_bichromatic G c a b v hva hvb
    have hw : w ≠ v := ne_of_reachable_isolated hiso hu h
    exact ⟨hw, (bichromatic_reachable_iff_induce_delete G c a b v hva hvb hw hu).mp h⟩
  · rintro ⟨hw, h⟩
    exact (bichromatic_reachable_iff_induce_delete G c a b v hva hvb hw hu).mpr h

/-- Deleting an off-colour vertex from the bichromatic subgraph does not change
its adjacency relation. `Subgraph.deleteVerts` removes `v` and every edge
incident to it. -/
theorem bichromaticSubgraph_eq_deleteVerts_spanningCoe
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (v : V)
    (hva : c v ≠ a) (hvb : c v ≠ b) :
    bichromaticSubgraph G c a b =
      ((⊤ : (bichromaticSubgraph G c a b).Subgraph).deleteVerts {v}).spanningCoe := by
  have hiso : ∀ x, ¬ (bichromaticSubgraph G c a b).Adj v x :=
    vertex_not_in_bichromatic G c a b v hva hvb
  ext x y
  simp only [SimpleGraph.Subgraph.deleteVerts, SimpleGraph.Subgraph.induce_adj,
    SimpleGraph.Subgraph.spanningCoe_adj, SimpleGraph.Subgraph.top_adj,
    SimpleGraph.Subgraph.verts_top, Set.mem_diff, Set.mem_univ, Set.mem_singleton_iff,
    true_and]
  constructor
  · intro hxy
    refine ⟨?_, ?_, hxy⟩
    · intro hxv
      exact hiso y (hxv ▸ hxy)
    · intro hyv
      exact hiso x (hyv ▸ hxy.symm)
  · intro hxy
    exact hxy.2.2

/-- Same-vertex-type form of the chain equality, via `Subgraph.deleteVerts`. -/
theorem bichromatic_reachable_iff_deleteVerts
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (v : V)
    (hva : c v ≠ a) (hvb : c v ≠ b) (x y : V) :
    (bichromaticSubgraph G c a b).Reachable x y ↔
      ((⊤ : (bichromaticSubgraph G c a b).Subgraph).deleteVerts {v}).spanningCoe.Reachable x y := by
  have hEq := bichromaticSubgraph_eq_deleteVerts_spanningCoe G c a b v hva hvb
  constructor
  · exact fun h => hEq ▸ h
  · exact fun h => hEq.symm ▸ h

end KempeReconfiguration
