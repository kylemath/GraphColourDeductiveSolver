/-
  FiveColor.lean — Heawood five-colour lemmas that do not need a plane map.

  A proper `Fin 5` colouring of `G` off a vertex `x` extends across `x` as soon
  as the neighbours of `x` use at most four colours (in particular if
  `deg(x) ≤ 4`). A Kempe swap of a connected component of the `(a,b)`-subgraph
  stays proper.

  The degree-5 opposite-pair case of the Five Colour Theorem is not claimed:
  it needs combinatorial Jordan (`cycle_two_sides`), a degree-`≤ 5` vertex,
  and the cyclic order of the link.

  This file is not the Four Colour Theorem. Target: no sorry, admit, or axiom.
-/

/- upstream PlaneMap: cycle_two_sides + exists_degree_le_five + neighbour_rotation -/

import KempeReconfiguration.Degree4Extend
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fin.Basic

namespace KempeReconfiguration

variable {V : Type*} [Fintype V] [DecidableEq V]
variable {k : ℕ}

noncomputable section

open SimpleGraph
set_option linter.unusedSectionVars false

/-- A subset of `Fin 5` of size at most 4 omits a colour. This is the
pigeonhole fact used when at most four colours appear on a finite set. -/
theorem exists_missing_colour {s : Finset (Fin 5)} (hs : s.card ≤ 4) :
    ∃ α : Fin 5, α ∉ s := by
  by_contra h
  have hall : ∀ col : Fin 5, col ∈ s := by
    intro col
    by_contra hnin
    exact h ⟨col, hnin⟩
  have hsub : (Finset.univ : Finset (Fin 5)) ⊆ s := fun col _ => hall col
  have hle : 5 ≤ s.card := by
    have hcard := Finset.card_le_card hsub
    simpa [Finset.card_univ, Fintype.card_fin] using hcard
  exact Nat.not_le_of_lt (Nat.lt_succ_of_le hs) hle

/-- At most four colours on the image of a finite set leaves a free colour. -/
theorem exists_missing_colour_on {α : Type*} [DecidableEq α]
    (f : α → Fin 5) (s : Finset α) (hs : (s.image f).card ≤ 4) :
    ∃ col : Fin 5, ∀ a ∈ s, f a ≠ col := by
  obtain ⟨col, hcol⟩ := exists_missing_colour hs
  refine ⟨col, fun a ha hf => ?_⟩
  exact hcol (Finset.mem_image.mpr ⟨a, ha, hf⟩)

/-- Colours appearing on `N(x)` under `c`. This Finset is `c '' neighborSet x`. -/
def neighbourColourFinset (G : SimpleGraph V) [DecidableRel G.Adj]
    (x : V) (c : V → Fin 5) : Finset (Fin 5) :=
  (G.neighborFinset x).image c

lemma coe_neighbourColourFinset
    (G : SimpleGraph V) [DecidableRel G.Adj] (x : V) (c : V → Fin 5) :
    (neighbourColourFinset G x c : Set (Fin 5)) = c '' G.neighborSet x := by
  ext col
  simp [neighbourColourFinset, Finset.mem_image, mem_neighborFinset, Set.mem_image,
    mem_neighborSet]

lemma neighbourColourFinset_card_le_degree
    (G : SimpleGraph V) [DecidableRel G.Adj] (x : V) (c : V → Fin 5) :
    (neighbourColourFinset G x c).card ≤ G.degree x :=
  Finset.card_image_le

lemma neighbourColourFinset_card_le_of_degree_le_four
    (G : SimpleGraph V) [DecidableRel G.Adj] (x : V) (c : V → Fin 5)
    (hdeg : G.degree x ≤ 4) :
    (neighbourColourFinset G x c).card ≤ 4 :=
  Nat.le_trans (neighbourColourFinset_card_le_degree G x c) hdeg

/-- Properness of `c` on `G - x` as an induced subgraph is properness of every
edge that misses `x`. -/
theorem isProperColouring_induce_iff
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (x : V) (c : V → Fin 5) :
    IsProperColouring (G.induce {v | v ≠ x}) (fun y : {v : V // v ≠ x} => c y.val) ↔
      ∀ u v : V, G.Adj u v → u ≠ x → v ≠ x → c u ≠ c v := by
  constructor
  · intro h u v huv hu hv
    exact h ⟨u, hu⟩ ⟨v, hv⟩ huv
  · intro h u v huv
    exact h u.val v.val huv u.property v.property

/-- The connected component of `u` in the `(a,b)`-subgraph. -/
abbrev kempeComponent (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u : V) : Set V :=
  ((bichromaticSubgraph G c a b).connectedComponentMk u).supp

instance kempeComponent_decidablePred
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u : V) :
    DecidablePred (fun v => v ∈ kempeComponent G c a b u) :=
  fun _ => Classical.propDecidable _

lemma kempeComponent_eq_kempeChain
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u : V) :
    kempeComponent G c a b u = kempeChain G c a b u := by
  ext v
  simp only [kempeComponent, ConnectedComponent.mem_supp_iff, ConnectedComponent.eq,
    kempeChain, Set.mem_setOf_eq]
  exact ⟨Reachable.symm, Reachable.symm⟩

/-- Swapping a connected component of the `(a,b)`-subgraph preserves a proper
colouring. The set is `ConnectedComponent.supp` of `connectedComponentMk`
in `bichromaticSubgraph`; this is the chain used by
`kempeSwap_chain_proper`. -/
theorem kempeSwap_component_preserves
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (hab : a ≠ b) (u : V)
    (hu : c u = a)
    (hproper : IsProperColouring G c) :
    IsProperColouring G (kempeSwap c (kempeComponent G c a b u) a b) := by
  have hS : kempeComponent G c a b u = kempeChain G c a b u :=
    kempeComponent_eq_kempeChain G c a b u
  refine kempeSwap_preserves_proper G c a b hab (kempeComponent G c a b u) ?_ ?_ hproper
  · intro v hv
    have hv' : v ∈ kempeChain G c a b u := by
      simpa [hS] using hv
    exact kempeChain_colours G c a b u v (Or.inl hu) hv'
  · intro w v hwv hw hvcol
    have hw' : w ∈ kempeChain G c a b u := by
      simpa [hS] using hw
    have hv' := kempeChain_closed G c a b u w v (Or.inl hu) hwv hw' hvcol
    simpa [hS] using hv'

/-- If `c` is a proper `Fin 5` colouring of the induced subgraph `G - x`, and
either `deg(x) ≤ 4` or at most four colours appear on `N(x)`, then `c`
extends to a proper 5-colouring of `G` that agrees with `c` off `x`. -/
theorem five_color_degree_at_most_four
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (x : V) (c : V → Fin 5)
    (hproper : IsProperColouring (G.induce {v | v ≠ x})
      (fun y : {v : V // v ≠ x} => c y.val))
    (hbound : G.degree x ≤ 4 ∨ ((G.neighborFinset x).image c).card ≤ 4) :
    ∃ c' : V → Fin 5, IsProperColouring G c' ∧ ∀ v : V, v ≠ x → c' v = c v := by
  have hused : ((G.neighborFinset x).image c).card ≤ 4 := by
    cases hbound with
    | inl hdeg =>
        simpa [neighbourColourFinset] using
          neighbourColourFinset_card_le_of_degree_le_four G x c hdeg
    | inr hcard =>
        exact hcard
  obtain ⟨α, hα⟩ := exists_missing_colour hused
  refine ⟨fun v => if v = x then α else c v, ?_, ?_⟩
  · intro u v huv
    by_cases hu : u = x
    · have hvx : v ≠ x := hu ▸ (G.ne_of_adj huv).symm
      have hmem : v ∈ G.neighborFinset x := by
        rw [mem_neighborFinset, ← hu]
        exact huv
      have hnc : c v ≠ α := by
        intro hcv
        exact hα (Finset.mem_image.mpr ⟨v, hmem, hcv⟩)
      simp [hu, hvx]
      exact Ne.symm hnc
    · by_cases hv : v = x
      · have hmem : u ∈ G.neighborFinset x := by
          rw [mem_neighborFinset, ← hv]
          exact G.symm huv
        have hnc : c u ≠ α := by
          intro hcu
          exact hα (Finset.mem_image.mpr ⟨u, hmem, hcu⟩)
        simp [hu, hv]
        exact hnc
      · simp [hu, hv]
        exact (isProperColouring_induce_iff G x c).mp hproper u v huv hu hv
  · intro v hv
    simp [hv]

/-- Same extension, stated from a colouring of the deleted-vertex type. -/
theorem five_color_degree_at_most_four_subtype
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (x : V) (c : {v : V // v ≠ x} → Fin 5)
    (hproper : IsProperColouring (G.induce {v | v ≠ x}) c)
    (hbound : G.degree x ≤ 4 ∨
      ((G.neighborFinset x).image fun y =>
        if h : y = x then (0 : Fin 5) else c ⟨y, h⟩).card ≤ 4) :
    ∃ c' : V → Fin 5, IsProperColouring G c' ∧
      ∀ v : V, (hv : v ≠ x) → c' v = c ⟨v, hv⟩ := by
  let cV : V → Fin 5 := fun y => if h : y = x then 0 else c ⟨y, h⟩
  have hproperV :
      IsProperColouring (G.induce {v | v ≠ x})
        (fun y : {v : V // v ≠ x} => cV y.val) := by
    intro u v huv
    have hu : u.val ≠ x := u.property
    have hv : v.val ≠ x := v.property
    have : cV u.val = c u := dif_neg hu
    have : cV v.val = c v := dif_neg hv
    simpa [cV, hu, hv] using hproper u v huv
  have hboundV : G.degree x ≤ 4 ∨ ((G.neighborFinset x).image cV).card ≤ 4 := by
    simpa [cV] using hbound
  obtain ⟨c', hc', hag⟩ := five_color_degree_at_most_four G x cV hproperV hboundV
  refine ⟨c', hc', fun v hv => ?_⟩
  have := hag v hv
  simp [cV, hv] at this
  exact this

/-- Graphs on at most five vertices are 5-colourable: inject the vertices
into `Fin 5`. Planarity is not used. -/
theorem five_colorable_of_card_le_five
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (hV : Fintype.card V ≤ 5) :
    ∃ c : V → Fin 5, IsProperColouring G c := by
  let e := Fintype.equivFin V
  refine ⟨fun v => Fin.castLE hV (e v), fun u v huv => ?_⟩
  exact (Fin.castLE_injective hV).ne (e.injective.ne (G.ne_of_adj huv))

/-
  The Five Colour Theorem for planar graphs is not stated here.

  Heawood's degree-5 step needs a vertex of degree at most 5, the cyclic
  order of its link, and the fact that a cycle cuts the remaining graph
  into two sides. Those lemmas live in the PlaneMap development, which
  targets Lean 4.35 and is not in this Mathlib v4.15.0 pin.
-/

/- upstream PlaneMap: cycle_two_sides + exists_degree_le_five + neighbour_rotation -/

end

end KempeReconfiguration
