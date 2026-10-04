/-
  F4_KempeChains.lean — navigator node `f4` (first half: swap validity).

  Agent 1720, M-Foundation, group L2.

  Kempe chains and Kempe swaps stated on Mathlib's `SimpleGraph.Coloring`.
  Same mathematics as `lean4/KempeReconfiguration/KempeReconfiguration/Basic.lean`
  (`bichromaticSubgraph`, `kempeSwap`, `kempeSwap_preserves_proper`), but phrased
  so that a swap returns a `G.Coloring (Fin k)` and can feed F5 directly.

  Main results (target: 0 sorry):
  * `swapOn_proper`        : swapping a ↔ b on a set closed under a/b-coloured
                             neighbours preserves properness
  * `kempeChain_closed`    : a Kempe chain is such a set
  * `kempeSwapColoring`    : the swapped proper colouring
  * `kempeSwapColoring_self` : the swap recolours the base vertex from a to b

  Not here: the degree ≤ 4 extension half of `f4` (needs vertex deletion / induced
  subgraph plumbing; planned together with F5).
-/

import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Logic.Equiv.Basic

namespace FourColor.Foundation

open SimpleGraph

variable {V : Type*} {k : ℕ}

/-- The a/b-bichromatic subgraph `B_{a,b}(G,c)`: edges of `G` both of whose ends
    have colour `a` or `b`. -/
def kempeGraph (G : SimpleGraph V) (c : V → Fin k) (a b : Fin k) : SimpleGraph V where
  Adj u w := G.Adj u w ∧ (c u = a ∨ c u = b) ∧ (c w = a ∨ c w = b)
  symm _ _ h := ⟨G.symm h.1, h.2.2, h.2.1⟩
  loopless u h := G.loopless u h.1

/-- The a/b-Kempe chain at `v`: vertices coloured `a` or `b` reachable from `v`
    in `B_{a,b}(G,c)`. Empty when `c v ∉ {a, b}`. -/
def kempeChain (G : SimpleGraph V) (c : V → Fin k) (a b : Fin k) (v : V) : Set V :=
  {w | (c w = a ∨ c w = b) ∧ (kempeGraph G c a b).Reachable v w}

/-- Recolour by the transposition `a ↔ b` on `S`, identity elsewhere. -/
def swapOn (c : V → Fin k) (S : Set V) [DecidablePred (· ∈ S)] (a b : Fin k) : V → Fin k :=
  fun v => if v ∈ S then Equiv.swap a b (c v) else c v

/-- A Kempe chain is closed under `G`-neighbours coloured `a` or `b`. -/
theorem kempeChain_closed {G : SimpleGraph V} {c : V → Fin k} {a b : Fin k} {v u w : V}
    (hu : u ∈ kempeChain G c a b v) (huw : G.Adj u w) (hw : c w = a ∨ c w = b) :
    w ∈ kempeChain G c a b v :=
  ⟨hw, hu.2.trans (SimpleGraph.Adj.reachable (show (kempeGraph G c a b).Adj u w from ⟨huw, hu.1, hw⟩))⟩

/-- **Swap validity.** If `c` is proper and `S` contains every `a`/`b`-coloured
    neighbour of each of its vertices, then swapping `a ↔ b` on `S` is proper. -/
theorem swapOn_proper (G : SimpleGraph V) (c : V → Fin k) (a b : Fin k)
    (S : Set V) [DecidablePred (· ∈ S)]
    (hS : ∀ u w, G.Adj u w → u ∈ S → (c w = a ∨ c w = b) → w ∈ S)
    (hc : ∀ u w, G.Adj u w → c u ≠ c w) :
    ∀ u w, G.Adj u w → swapOn c S a b u ≠ swapOn c S a b w := by
  have key : ∀ u w, G.Adj u w → u ∈ S → w ∉ S → Equiv.swap a b (c u) ≠ c w := by
    intro u w huw hu hw heq
    have hfix : Equiv.swap a b (c w) = c w :=
      Equiv.swap_apply_of_ne_of_ne
        (fun h => hw (hS u w huw hu (Or.inl h)))
        (fun h => hw (hS u w huw hu (Or.inr h)))
    apply hc u w huw
    apply (Equiv.swap a b).injective
    rw [heq, hfix]
  intro u w huw
  unfold swapOn
  by_cases hu : u ∈ S <;> by_cases hw : w ∈ S
  · rw [if_pos hu, if_pos hw]
    exact fun h => hc u w huw ((Equiv.swap a b).injective h)
  · rw [if_pos hu, if_neg hw]
    exact key u w huw hu hw
  · rw [if_neg hu, if_pos hw]
    exact fun h => key w u (G.symm huw) hw hu h.symm
  · rw [if_neg hu, if_neg hw]
    exact hc u w huw

/-- Swap on a closed set, packaged as a Mathlib colouring. -/
def swapColoring {G : SimpleGraph V} (C : G.Coloring (Fin k)) (S : Set V)
    [DecidablePred (· ∈ S)] (a b : Fin k)
    (hS : ∀ u w, G.Adj u w → u ∈ S → (C w = a ∨ C w = b) → w ∈ S) :
    G.Coloring (Fin k) :=
  Coloring.mk (swapOn C S a b)
    (fun {u w} huw => swapOn_proper G C a b S hS (fun _ _ h => C.valid h) u w huw)

open Classical in
/-- **Kempe swap.** Swap `a ↔ b` on the a/b-Kempe chain at `v`. -/
noncomputable def kempeSwapColoring {G : SimpleGraph V} (C : G.Coloring (Fin k))
    (a b : Fin k) (v : V) : G.Coloring (Fin k) :=
  swapColoring C (kempeChain G C a b v) a b
    (fun _ _ huw hu hw => kempeChain_closed hu huw hw)

open Classical in
/-- The Kempe swap at `v` recolours `v` from `a` to `b`. -/
theorem kempeSwapColoring_self {G : SimpleGraph V} (C : G.Coloring (Fin k))
    (a b : Fin k) (v : V) (hv : C v = a) :
    kempeSwapColoring C a b v v = b := by
  have hmem : v ∈ kempeChain G C a b v := ⟨Or.inl hv, SimpleGraph.Reachable.refl v⟩
  show swapOn C (kempeChain G C a b v) a b v = b
  unfold swapOn
  rw [if_pos hmem, hv, Equiv.swap_apply_left]

open Classical in
/-- Vertices outside the chain keep their colour. -/
theorem kempeSwapColoring_of_not_mem {G : SimpleGraph V} (C : G.Coloring (Fin k))
    (a b : Fin k) (v w : V) (hw : w ∉ kempeChain G C a b v) :
    kempeSwapColoring C a b v w = C w := by
  show swapOn C (kempeChain G C a b v) a b w = C w
  unfold swapOn
  rw [if_neg hw]

end FourColor.Foundation
