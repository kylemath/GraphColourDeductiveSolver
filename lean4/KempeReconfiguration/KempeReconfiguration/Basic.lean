/-
  Basic.lean — Kempe chain definitions and fundamental properties.

  Agent 1210, Manager M4, Sub-subagent S1: Foundations Builder

  Defines:
  - Bichromatic subgraph B_{a,b}(G,c)
  - Kempe chain as connected component of bichromatic subgraph
  - Kempe swap operation
  - Proof that Kempe swap preserves proper colouring

  Target: 0 sorry
-/

import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Combinatorics.SimpleGraph.Connectivity
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fin.Basic

namespace KempeReconfiguration

variable {V : Type*} [Fintype V] [DecidableEq V]
variable {k : ℕ}

/-- A proper k-colouring assigns each vertex a colour in Fin k such that
    adjacent vertices get different colours. -/
def IsProperColouring (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) : Prop :=
  ∀ u v : V, G.Adj u v → c u ≠ c v

/-- The bichromatic subgraph B_{a,b}(G,c): the subgraph of G induced by
    vertices coloured a or b. Two such vertices are adjacent in B_{a,b}
    iff they are adjacent in G. -/
def bichromaticAdj (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u v : V) : Prop :=
  G.Adj u v ∧ (c u = a ∨ c u = b) ∧ (c v = a ∨ c v = b)

/-- The bichromatic subgraph as a SimpleGraph on the vertices coloured a or b. -/
def bichromaticSubgraph (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) : SimpleGraph V where
  Adj u v := bichromaticAdj G c a b u v
  symm u v h := ⟨G.symm h.1, h.2.2, h.2.1⟩
  loopless v h := G.loopless v h.1

/-- A Kempe chain is a set of vertices forming a connected component
    of the bichromatic subgraph B_{a,b}(G,c). We represent it as
    the connected component containing a given vertex. -/
def inSameKempeChain (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u v : V) : Prop :=
  (bichromaticSubgraph G c a b).Reachable u v

/-- Kempe swap: exchange colours a ↔ b on all vertices in a set S. -/
def kempeSwap (c : V → Fin k) (S : Set V) [DecidablePred (· ∈ S)]
    (a b : Fin k) : V → Fin k :=
  fun v =>
    if v ∈ S then
      if c v = a then b
      else if c v = b then a
      else c v
    else c v

/-- Key property: Kempe swap only modifies colours within {a, b}. -/
theorem kempeSwap_colour_cases (c : V → Fin k) (S : Set V)
    [DecidablePred (· ∈ S)] (a b : Fin k) (v : V) :
    kempeSwap c S a b v = a ∨ kempeSwap c S a b v = b ∨
    kempeSwap c S a b v = c v := by
  simp only [kempeSwap]
  split
  · split
    · left; rfl
    · split
      · right; left; rfl
      · right; right; rfl
  · right; right; rfl

/-- If a colour is not in {a, b}, Kempe swap doesn't change it. -/
theorem kempeSwap_preserves_other (c : V → Fin k) (S : Set V)
    [DecidablePred (· ∈ S)] (a b : Fin k) (v : V)
    (hva : c v ≠ a) (hvb : c v ≠ b) :
    kempeSwap c S a b v = c v := by
  simp only [kempeSwap]
  split
  · split
    · exact absurd (by assumption) hva
    · split
      · exact absurd (by assumption) hvb
      · rfl
  · rfl

/-- Vertices outside the swap set keep their colour. -/
theorem kempeSwap_outside (c : V → Fin k) (S : Set V)
    [DecidablePred (· ∈ S)] (a b : Fin k) (v : V)
    (hv : v ∉ S) :
    kempeSwap c S a b v = c v := by
  simp only [kempeSwap, if_neg hv]

/-- Kempe swap on a Kempe chain preserves proper colouring.

    The key insight: within the chain, adjacent vertices have opposite
    colours (one a, one b), so swapping preserves this opposition.
    Across the chain boundary, the exterior vertex keeps its original
    colour and the boundary vertex switches, but they were in {a,b}
    and the exterior vertex is NOT in {a,b} (by definition of bichromatic
    subgraph), so they remain properly coloured. -/
theorem kempeSwap_preserves_proper
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (hab : a ≠ b)
    (S : Set V) [DecidablePred (· ∈ S)]
    (hS_ab : ∀ v ∈ S, c v = a ∨ c v = b)
    (hS_closed : ∀ u v : V, G.Adj u v → u ∈ S → (c v = a ∨ c v = b) → v ∈ S)
    (hproper : IsProperColouring G c) :
    IsProperColouring G (kempeSwap c S a b) := by
  intro u v huv
  simp only [kempeSwap]
  by_cases hu : u ∈ S <;> by_cases hv : v ∈ S
  · -- Both in S: they had opposite colours in {a,b}, swap preserves this
    have hcu := hS_ab u hu
    have hcv := hS_ab v hv
    have hne := hproper u v huv
    rcases hcu with rfl | rfl <;> rcases hcv with rfl | rfl
    · exact absurd rfl hne
    · simp [hab]
    · simp [Ne.symm hab]
    · exact absurd rfl hne
  · -- u in S, v not: v's colour is not in {a,b} (since S is closed)
    have hcv_not : ¬(c v = a ∨ c v = b) := fun h => hv (hS_closed u v huv hu h)
    push_neg at hcv_not
    simp [if_neg hv]
    have hcu := hS_ab u hu
    rcases hcu with rfl | rfl
    · split
      · exact hcv_not.2
      · exact absurd rfl (by omega)
    · split
      · exact absurd rfl (by omega)
      · split
        · exact hcv_not.1
        · exact hproper u v huv
  · -- u not in S, v in S: symmetric to previous case
    have hcu_not : ¬(c u = a ∨ c u = b) :=
      fun h => hu (hS_closed v u (G.symm huv) hv h)
    push_neg at hcu_not
    simp [if_neg hu]
    have hcv := hS_ab v hv
    rcases hcv with rfl | rfl
    · split
      · Ne.symm hcu_not.2
      · exact absurd rfl (by omega)
    · split
      · exact absurd rfl (by omega)
      · split
        · Ne.symm hcu_not.1
        · Ne.symm (hproper u v huv)
  · -- Neither in S: both keep original colours
    simp [if_neg hu, if_neg hv]
    exact hproper u v huv

end KempeReconfiguration
