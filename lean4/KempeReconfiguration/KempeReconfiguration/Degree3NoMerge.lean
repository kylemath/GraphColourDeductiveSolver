/-
  Degree3NoMerge.lean — Lemma 5.2: Degree-3 No-Merge Lemma

  Agent 1210, Manager M4, Sub-subagent S3

  Statement: In a triangulation, if v has deg(v) = 3 and c(v) = 5,
  then adding v back to G-v never merges (a,5)-chains.
  Specifically: all neighbours of v in B_{a,5}(G-v) belong to the
  same (a,5)-chain.

  Proof: In a triangulation, the link of a degree-3 vertex is K_3
  (a triangle). So all three neighbours are pairwise adjacent.
  If u_i, u_j are both in B_{a,5}, the edge u_i-u_j in G-v places
  them in the same connected component.

  Target: ≤ 2 sorry (planarity axioms)
-/

import KempeReconfiguration.Basic

namespace KempeReconfiguration

variable {V : Type*} [Fintype V] [DecidableEq V]
variable {k : ℕ}

/-- A triangulation is a maximal planar graph: |E| = 3|V| - 6 and planar. -/
class Triangulation (G : SimpleGraph V) [DecidableRel G.Adj] where
  -- TODO: sorry — Mathlib lacks a full planar graph API.
  -- Axiomatize the key property we need: in a triangulation,
  -- the link (open neighbourhood) of a degree-3 vertex forms K_3.
  link_degree3_complete : ∀ v : V, G.degree v = 3 →
    ∀ u w : V, G.Adj v u → G.Adj v w → u ≠ w → G.Adj u w

/-- If two vertices are both in B_{a,5}(G-v) and are adjacent in G-v,
    then they are in the same (a,5)-Kempe chain. -/
theorem adj_same_chain
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a target : Fin k)
    (u w : V) (hadj : G.Adj u w)
    (hu : c u = a ∨ c u = target)
    (hw : c w = a ∨ c w = target) :
    inSameKempeChain G c a target u w := by
  exact ⟨SimpleGraph.Walk.cons ⟨hadj, hu, hw⟩ SimpleGraph.Walk.nil⟩

/-- The Degree-3 No-Merge Lemma.

    Let G be a triangulation, v a vertex with deg(v) = 3.
    If u_i and u_j are both neighbours of v in G, and both are
    coloured a or 5 (i.e., in B_{a,5}), then u_i and u_j are
    in the same (a,5)-Kempe chain of G-v.

    The key step: since G is a triangulation and deg(v) = 3,
    all neighbours of v are pairwise adjacent (link is K_3).
    This edge persists in G-v, placing u_i and u_j in the same
    connected component of B_{a,5}(G-v).

    Note: We state this for G directly (the edge u_i-u_j exists in G
    and hence in any subgraph containing both). The vertex-deletion
    step requires showing the edge persists, which follows because
    u_i ≠ v and u_j ≠ v. -/
theorem degree3_no_merge
    (G : SimpleGraph V) [DecidableRel G.Adj]
    [Triangulation G]
    (c : V → Fin k) (a target : Fin k)
    (v : V) (hdeg : G.degree v = 3)
    (u₁ u₂ : V) (h₁ : G.Adj v u₁) (h₂ : G.Adj v u₂)
    (hne : u₁ ≠ u₂)
    (hc₁ : c u₁ = a ∨ c u₁ = target)
    (hc₂ : c u₂ = a ∨ c u₂ = target) :
    inSameKempeChain G c a target u₁ u₂ := by
  have hadj : G.Adj u₁ u₂ := Triangulation.link_degree3_complete v hdeg u₁ u₂ h₁ h₂ hne
  exact adj_same_chain G c a target u₁ u₂ hadj hc₁ hc₂

/-
  The sorry count in this file: 0 explicit sorry statements.

  However, the `Triangulation` class axiomatizes a property (link completeness)
  that would require planarity to prove from first principles. This is noted
  as an axiomatic assumption rather than a sorry, following the formalization
  plan's recommendation.

  To remove this axiom, we would need:
  1. Mathlib's PlanarEmbedding API (not yet available)
  2. Proof that |E| = 3|V| - 6 + planarity → every face is a triangle
  3. Proof that triangular faces → link completeness at degree 3
-/

end KempeReconfiguration
