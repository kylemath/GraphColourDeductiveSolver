/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPi
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterEvenCut

/-!
# The Tait (5-pole) form of the hole machinery (`NightG66IPR.md` §1)

Let `T` be a triangulation, `h` a degree-5 vertex with link `x 0, …, x 4` (a `Pent`), `F = T*`
the dual cubic graph and `P` the pentagon of `F` dual to `h`. Removing `P` leaves the
**5-pole** `F − P`: a cubic graph with five dangling legs (spokes) `s 0, …, s 4`. The spoke
`s i` is the dual of the **link edge** `x i x (i+1)` (equivalently, the edge of the pentagon
face `P` that separates the faces `x i` and `x (i+1)`, cut at `P`); the dual edges of the five
edges `h x i` are the sides of `P` and disappear with it. With the `F₂²` encoding `enc` of
`QuarterEvenCut`, the Tait colour of the dual of `uv` is `tait c u v = enc (c u) + enc (c v)`,
and properness of `c` is exactly properness of this 3-edge-colouring of `F − P`.

Formal content (no planarity used anywhere in this file):

1. `spoke P c i := enc (c (x i)) + enc (c (x (i+1)))`, the leg colour of `s i`.
   `spoke_ne_zero` (properness: each leg colour is in `F₂² ∖ {0}`), `spoke_sum` (the five leg
   colours sum to `0`, telescoping), `spoke_count_odd` (parity lemma: every nonzero colour
   occurs an odd number of times, so every leg word is `3 + 1 + 1`).
2. `filled_iff_spokes`: `Target G h c` (the link misses a colour, i.e. uses at most three)
   iff some leg colour occurs on three cyclically consecutive legs `s i, s (i+1), s (i+2)`.
   (Matches the note: "filled ⇔ the triple leg colour sits on three consecutive legs"; by
   `spoke_count_odd` the triple is the whole colour class.)
3. `repeat_spokes`: at `RepeatAt P c j` with link `(α, μ, α, A, B)` the leg word at
   `s j, …, s (j+4)` is `(α+μ, μ+α, α+A, A+B, B+α)`; `repeat_spokes_gamma`: this is
   `(γ₁, γ₁, γ₂, γ₁, γ₃)` with `γ₁ = α+μ = A+B`, `γ₂ = α+A = μ+B`, `γ₃ = α+B = μ+A`, and
   `γ₁, γ₂, γ₃` are the three distinct nonzero elements (the note's §1.2 word).
4. Locks in Tait language. `taitGraph G h c γ` is the subgraph of `G − h` of edges whose dual
   edge has Tait colour `γ`. `pair_reach_iff_tait`: for a proper `c`, the `{p, q}`-Kempe chain
   of an active vertex is its component in `taitGraph (enc p + enc q)`. Hence
   `lock1_iff_tait`: Lock1 at `j` ⇔ `x (j+1)` and `x (j+3)` are joined by edges of Tait colour
   `γ₃ = spoke (j+4)` (the colour of the isolated leg `s (j+4)`); `lock2_iff_tait`: Lock2 ⇔
   they (`x (j+1)`, `x (j+4)`) are joined by edges of colour `γ₂ = spoke (j+2)`.
   `tait_cross_iff`: an edge `uv` of `G − h` lies inside the `{p,q} | {r,s}` pair classes iff
   its Tait colour is `p + q`; otherwise (colour in the complement `{δ, ε}`) it crosses
   from a `{p,q}`-vertex to an `{r,s}`-vertex. So the `{μ, A}`-chains are cut out by the
   `{γ₁, γ₂}`-curves of `F − P`, whose leg ends are exactly the four legs
   `s j, s (j+1), s (j+2), s (j+3)` (`repeat_spokes_gamma`), and the `{μ, B}`-chains by the
   `{γ₁, γ₃}`-curves with leg ends `s j, s (j+1), s (j+3), s (j+4)`.

**Missing bridge (not formalised; needs the face structure of the dual and a Jordan argument).**
For a proper unfilled `c` at `j` on a spherical triangulation:
`Lock1 P c j ⇔` the `{γ₁, γ₂}`-bicoloured leg-to-leg paths of `F − P` pair the legs as
`(s j, s (j+3)) (s (j+1), s (j+2))` (rather than `(s j, s (j+1)) (s (j+2), s (j+3))`), and
`Lock2 P c j ⇔` the `{γ₁, γ₃}`-paths pair `(s j, s (j+4)) (s (j+1), s (j+3))`. So
`DoublyLocked` ⇔ both Kempe path systems take the wrong non-crossing pairing (Kempe's 1879
pentagon case in edge form); the `{γ₂, γ₃}`-path always joins `s (j+2)` to `s (j+4)`.
The library has no dual cubic graph or edge-colour paths, so `lock1_iff_tait`/`lock2_iff_tait`
(Kempe chain = component of a single Tait colour class of `G − h`) are the formal half;
the other half is the planar statement that such a component is a band between the two
bicoloured curves.

**Engine check (recorded, not formal).** `tait_pairing` (NightG66IPR scratchpad script, walking
the bicoloured paths of the dual) agrees with `radius.classify` on every unfilled state at every
hole of the 37 IPR duals with 32–43 vertices (C60–C82), and at A₃, the icosahedron and GC(2,0):
**0 mismatches**.

**Kempe classes (remark, not a theorem).** Vertex-Kempe classes of `T − h` (mod `S₄`) are the
edge-Kempe classes of `F − P` (mod `S₃`), a switch being allowed on a bicoloured cycle or a
leg-to-leg bicoloured path (NightG66IPR §1.4, hand proof). The library has no edge-Kempe
switches on a dual graph, so this is not stated formally; its local ingredient is
`QuarterEvenCut.swap_edge_colour` (a vertex swap changes the Tait colour exactly on the cut
edges, by `enc a + enc b`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill

/-! ### Word-level facts (five link colours) -/

/-- The leg word of a cyclic link word `a`. -/
def legWord (a : Fin 5 → Fin 4) (i : Fin 5) : F22 := enc (a i) + enc (a (i + 1))

/-- A cyclic link word is proper when consecutive letters differ. -/
def LinkProper (a : Fin 5 → Fin 4) : Prop := ∀ i, a i ≠ a (i + 1)

instance (a : Fin 5 → Fin 4) : Decidable (LinkProper a) :=
  by unfold LinkProper; infer_instance

/-- Three cyclically consecutive equal legs. -/
def TripleConsec (e : Fin 5 → F22) : Prop := ∃ i, e i = e (i + 1) ∧ e (i + 1) = e (i + 2)

instance (e : Fin 5 → F22) : Decidable (TripleConsec e) :=
  by unfold TripleConsec; infer_instance

lemma word_eta (a : Fin 5 → Fin 4) : a = ![a 0, a 1, a 2, a 3, a 4] := by
  funext i; fin_cases i <;> rfl

lemma word_forall {Q : (Fin 5 → Fin 4) → Prop}
    (H : ∀ a0 a1 a2 a3 a4 : Fin 4, Q ![a0, a1, a2, a3, a4]) (a : Fin 5 → Fin 4) : Q a := by
  rw [word_eta a]; exact H _ _ _ _ _

theorem legWord_filled_table : ∀ a0 a1 a2 a3 a4 : Fin 4,
    LinkProper ![a0, a1, a2, a3, a4] →
      ((∃ x, ∀ i, ![a0, a1, a2, a3, a4] i ≠ x) ↔
        TripleConsec (legWord ![a0, a1, a2, a3, a4])) := by
  decide +kernel

theorem legWord_count_table : ∀ a0 a1 a2 a3 a4 : Fin 4,
    LinkProper ![a0, a1, a2, a3, a4] → ∀ γ : F22, γ ≠ 0 →
      (Finset.univ.filter (fun i => legWord ![a0, a1, a2, a3, a4] i = γ)).card % 2 = 1 := by
  decide +kernel

/-- Word level: a proper link word misses a colour iff its leg word has three consecutive
equal legs. -/
theorem legWord_filled_iff (a : Fin 5 → Fin 4) (ha : LinkProper a) :
    (∃ x, ∀ i, a i ≠ x) ↔ TripleConsec (legWord a) :=
  word_forall (Q := fun a => LinkProper a →
    ((∃ x, ∀ i, a i ≠ x) ↔ TripleConsec (legWord a))) legWord_filled_table a ha

/-- Word level parity lemma. -/
theorem legWord_count_odd (a : Fin 5 → Fin 4) (ha : LinkProper a) (γ : F22) (hγ : γ ≠ 0) :
    (Finset.univ.filter (fun i => legWord a i = γ)).card % 2 = 1 :=
  word_forall (Q := fun a => LinkProper a → ∀ γ : F22, γ ≠ 0 →
    (Finset.univ.filter (fun i => legWord a i = γ)).card % 2 = 1) legWord_count_table a ha γ hγ

/-- Four distinct colours have `enc`-sum `0`. -/
lemma enc_four : ∀ a b c d : Fin 4, a ≠ b → a ≠ c → a ≠ d → b ≠ c → b ≠ d → c ≠ d →
    enc a + enc b = enc c + enc d := by decide

lemma enc_three_ne : ∀ a b c d : Fin 4, a ≠ b → a ≠ c → a ≠ d → b ≠ c → b ≠ d → c ≠ d →
    enc a + enc b ≠ enc a + enc c ∧ enc a + enc b ≠ enc a + enc d ∧
      enc a + enc c ≠ enc a + enc d := by decide

/-! ### The spoke colours of a hole -/

variable {V : Type*} {G : SimpleGraph V} {h : V} (P : Pent G h)

/-- The link word of `c` at the hole. -/
def linkWord (c : V → Fin 4) : Fin 5 → Fin 4 := fun i => c (P.x i)

/-- The colour of the spoke `s i` (the dual of the link edge `x i x (i+1)`): the Tait colour
`enc (c (x i)) + enc (c (x (i+1)))`. -/
def spokeColour (c : V → Fin 4) (i : Fin 5) : F22 := tait c (P.x i) (P.x (i + 1))

variable {P} {c : V → Fin 4}

lemma spokeColour_eq_legWord : spokeColour P c = legWord (linkWord P c) := rfl

lemma linkProper (hc : ProperOff G h c) : LinkProper (linkWord P c) :=
  fun i => link_ne hc i (i + 1) rfl

/-- Each spoke colour is nonzero (properness of the link edge). -/
theorem spoke_ne_zero (hc : ProperOff G h c) (i : Fin 5) : spokeColour P c i ≠ 0 :=
  enc_add_ne_zero (link_ne hc i (i + 1) rfl)

/-- The five spoke colours sum to `0` (telescoping). -/
theorem spoke_sum (c : V → Fin 4) : ∑ i, spokeColour P c i = 0 := by
  simp only [spokeColour, tait]
  rw [Finset.sum_add_distrib, show ∑ i, enc (c (P.x (i + 1))) = ∑ i, enc (c (P.x i)) from
    Fintype.sum_equiv (Equiv.addRight 1) _ _ (fun _ => rfl), F22_add_self]

/-- Parity lemma (the 5-edge cut around the pentagon): every nonzero colour occurs on an odd
number of spokes, so the leg word is `3 + 1 + 1`. -/
theorem spoke_count_odd (hc : ProperOff G h c) (γ : F22) (hγ : γ ≠ 0) :
    (Finset.univ.filter (fun i => spokeColour P c i = γ)).card % 2 = 1 :=
  legWord_count_odd _ (linkProper hc) γ hγ

lemma target_iff_link : Target G h c ↔ ∃ x, ∀ i, c (P.x i) ≠ x := by
  constructor
  · rintro ⟨x, hx⟩; exact ⟨x, fun i => hx (P.adj_h i)⟩
  · rintro ⟨x, hx⟩; exact target_of_vals x hx

/-- **Filled ⇔ three consecutive equal spokes.** A proper `c` is filled (its link misses a
colour) iff some spoke colour sits on three cyclically consecutive spokes. -/
theorem filled_iff_spokes (hc : ProperOff G h c) :
    Target G h c ↔ ∃ i, spokeColour P c i = spokeColour P c (i + 1) ∧
      spokeColour P c (i + 1) = spokeColour P c (i + 2) := by
  rw [target_iff_link]
  exact legWord_filled_iff (linkWord P c) (linkProper hc)

lemma fin5_add (j : Fin 5) : j + 1 + 1 = j + 2 ∧ j + 2 + 1 = j + 3 ∧ j + 3 + 1 = j + 4 ∧
    j + 4 + 1 = j := by
  revert j; decide

/-- **The leg word at a repeat state** `(α, μ, α, A, B)` at `x j, …, x (j+4)`:
`(α+μ, μ+α, α+A, A+B, B+α)`. -/
theorem repeat_spokes {j : Fin 5} (hr : RepeatAt P c j) :
    spokeColour P c j = enc (c (P.x j)) + enc (c (P.x (j + 1))) ∧
    spokeColour P c (j + 1) = enc (c (P.x (j + 1))) + enc (c (P.x j)) ∧
    spokeColour P c (j + 2) = enc (c (P.x j)) + enc (c (P.x (j + 3))) ∧
    spokeColour P c (j + 3) = enc (c (P.x (j + 3))) + enc (c (P.x (j + 4))) ∧
    spokeColour P c (j + 4) = enc (c (P.x (j + 4))) + enc (c (P.x j)) := by
  obtain ⟨e1, e2, e3, e4⟩ := fin5_add j
  obtain ⟨h0, -⟩ := hr
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp only [spokeColour, tait, e1, e2, e3, e4, h0]

/-- The leg word at a repeat state is `(γ₁, γ₁, γ₂, γ₁, γ₃)` with `γ₁ = α+μ = A+B`,
`γ₂ = α+A = μ+B`, `γ₃ = α+B = μ+A`, three distinct colours. -/
theorem repeat_spokes_gamma {j : Fin 5} (hr : RepeatAt P c j) :
    let α := c (P.x j); let μ := c (P.x (j + 1)); let A := c (P.x (j + 3))
    let B := c (P.x (j + 4))
    spokeColour P c j = enc α + enc μ ∧ spokeColour P c (j + 1) = enc α + enc μ ∧
    spokeColour P c (j + 2) = enc α + enc A ∧ spokeColour P c (j + 3) = enc α + enc μ ∧
    spokeColour P c (j + 4) = enc α + enc B ∧
    enc α + enc μ = enc A + enc B ∧ enc α + enc A = enc μ + enc B ∧
    enc α + enc B = enc μ + enc A ∧
    enc α + enc μ ≠ enc α + enc A ∧ enc α + enc μ ≠ enc α + enc B ∧
    enc α + enc A ≠ enc α + enc B := by
  intro α μ A B
  obtain ⟨s0, s1, s2, s3, s4⟩ := repeat_spokes hr
  obtain ⟨-, h1, h2, h3, h4, h5, h6⟩ := hr
  have g1 := enc_four α μ A B (Ne.symm h1) (Ne.symm h2) (Ne.symm h3) h4 h5 h6
  have g2 := enc_four α A μ B (Ne.symm h2) (Ne.symm h1) (Ne.symm h3) (Ne.symm h4) h6 h5
  have g3 := enc_four α B μ A (Ne.symm h3) (Ne.symm h1) (Ne.symm h2) (Ne.symm h5)
    (Ne.symm h6) h4
  have dd := enc_three_ne α μ A B (Ne.symm h1) (Ne.symm h2) (Ne.symm h3) h4 h5 h6
  refine ⟨s0, s1.trans (add_comm _ _), s2, s3.trans g1.symm, s4.trans (add_comm _ _),
    g1, g2, g3, dd⟩

/-! ### Kempe chains as single-colour components of the Tait colouring -/

variable (G h) in
/-- The edges of `G − h` whose dual edge has Tait colour `γ`. -/
def taitGraph (c : V → Fin 4) (γ : F22) : SimpleGraph V where
  Adj u v := G.Adj u v ∧ u ≠ h ∧ v ≠ h ∧ tait c u v = γ
  symm := ⟨fun u v e => ⟨e.1.symm, e.2.2.1, e.2.1, by
    rw [← e.2.2.2]; exact add_comm _ _⟩⟩
  loopless := ⟨fun _ e => e.1.ne rfl⟩

/-- Pair classes and Tait colours: for distinct `a ≠ b` and `p ≠ q`, the edge `ab` stays inside
the `{p,q} | {r,s}` partition iff its Tait colour is `p + q`; otherwise its Tait colour is in
the complement and it crosses from `{p,q}` to `{r,s}`. -/
theorem tait_cross_iff : ∀ a b p q : Fin 4, a ≠ b → p ≠ q →
    (((a = p ∨ a = q) ↔ (b = p ∨ b = q)) ↔ enc a + enc b = enc p + enc q) := by decide

lemma enc_step : ∀ a b p q : Fin 4, p ≠ q → (a = p ∨ a = q) →
    enc a + enc b = enc p + enc q → (b = p ∨ b = q) ∧ a ≠ b := by decide

lemma enc_pair : ∀ a b p q : Fin 4, a ≠ b → (a = p ∨ a = q) → (b = p ∨ b = q) →
    enc a + enc b = enc p + enc q := by decide

/-- **Kempe chains are Tait components.** For proper `c`, the `{p,q}`-Kempe chain of an
active vertex `s` is its component in the subgraph of `G − h` of Tait colour `p + q`. -/
theorem pair_reach_iff_tait (hc : ProperOff G h c) {p q : Fin 4} (hpq : p ≠ q) {s v : V}
    (hs : Active h c p q s) :
    (pairGraph G h c p q).Reachable s v ↔ (taitGraph G h c (enc p + enc q)).Reachable s v := by
  constructor
  · rintro ⟨w⟩
    refine ⟨w.map (Hom.ofLE ?_)⟩
    intro x y hxy
    obtain ⟨e, ⟨hx, cx⟩, ⟨hy, cy⟩⟩ := hxy
    exact ⟨e, hx, hy, enc_pair _ _ _ _ (hc e hx hy) cx cy⟩
  · rintro ⟨w⟩
    suffices H : ∀ {x y : V} (w : (taitGraph G h c (enc p + enc q)).Walk x y),
        Active h c p q x → (pairGraph G h c p q).Reachable x y from H w hs
    intro x y w
    induction w with
    | nil => intro _; exact Reachable.refl _
    | cons e w ih =>
      intro hx
      obtain ⟨e, -, hy, et⟩ := e
      obtain ⟨cy, -⟩ := enc_step _ _ _ _ hpq hx.2 et
      have ep : (pairGraph G h c p q).Adj _ _ := ⟨e, hx, hy, cy⟩
      exact ep.reachable.trans (ih ⟨hy, cy⟩)

/-- **Lock1 in Tait form**: at a proper repeat state at `j`, Lock1 holds iff `x (j+1)` and
`x (j+3)` are joined in `G − h` by edges of Tait colour `γ₃ = spoke (j+4)`, the colour of the
isolated leg. (The cutting curves are the `{γ₁, γ₂}`-curves, with leg ends `s j … s (j+3)`.) -/
theorem lock1_iff_tait (hc : ProperOff G h c) {j : Fin 5} (hr : RepeatAt P c j) :
    Lock1 P c j ↔
      (taitGraph G h c (spokeColour P c (j + 4))).Reachable (P.x (j + 1)) (P.x (j + 3)) := by
  obtain ⟨-, -, -, -, s4, -, -, g3, -⟩ := repeat_spokes_gamma hr
  rw [s4, g3]
  exact pair_reach_iff_tait hc hr.2.2.2.2.1 ⟨P.x_ne_h _, Or.inl rfl⟩

/-- **Lock2 in Tait form**: at a proper repeat state at `j`, Lock2 holds iff `x (j+1)` and
`x (j+4)` are joined in `G − h` by edges of Tait colour `γ₂ = spoke (j+2)`. (The cutting curves
are the `{γ₁, γ₃}`-curves, with leg ends `s j, s (j+1), s (j+3), s (j+4)`.) -/
theorem lock2_iff_tait (hc : ProperOff G h c) {j : Fin 5} (hr : RepeatAt P c j) :
    Lock2 P c j ↔
      (taitGraph G h c (spokeColour P c (j + 2))).Reachable (P.x (j + 1)) (P.x (j + 4)) := by
  obtain ⟨-, -, s2, -, -, -, g2, -, -⟩ := repeat_spokes_gamma hr
  rw [s2, g2]
  exact pair_reach_iff_tait hc hr.2.2.2.2.2.1 ⟨P.x_ne_h _, Or.inl rfl⟩

/-- At a repeat state no three consecutive spokes agree (cross-check of `filled_iff_spokes`
with `rep_not_target`). -/
theorem repeat_not_triple (hc : ProperOff G h c) {j : Fin 5} (hr : RepeatAt P c j) :
    ¬ ∃ i, spokeColour P c i = spokeColour P c (i + 1) ∧
      spokeColour P c (i + 1) = spokeColour P c (i + 2) :=
  fun H => rep_not_target hr ((filled_iff_spokes hc).2 H)

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.spoke_sum
#print axioms SimpleGraph.QuarterFloor.spoke_count_odd
#print axioms SimpleGraph.QuarterFloor.filled_iff_spokes
#print axioms SimpleGraph.QuarterFloor.repeat_spokes_gamma
#print axioms SimpleGraph.QuarterFloor.lock1_iff_tait
#print axioms SimpleGraph.QuarterFloor.lock2_iff_tait
#print axioms SimpleGraph.QuarterFloor.repeat_not_triple
