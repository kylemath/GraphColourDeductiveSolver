/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterEuler

/-!
# The per-step change of the six pair-graphs under one Kempe swap (`NightSixEvent.md` §1–§2)

Let `c` be a proper 4-colouring of `T − h`, `a ≠ b`, `K` one whole `{a, b}`-component, and
`c' = swap c a b K`; write `τ = Equiv.swap a b`. For a colour pair `{p, q}` write `E, V, C, r`
for the edge, vertex, component counts and cycle rank of the `{p, q}`-subgraph of `T − h`
(`QuarterEuler`), and `Δ` for "value at `c'` minus value at `c`" (`dE`, `dV`, `dC`, `dR`).

## Main results (sorry-free, no new axioms)

1. `swap_pair_graph_invariant`: the `{a, b}`- and the `{x, y}`-subgraphs (`{x, y} = {a, b}ᶜ`)
   are unchanged, hence so are their `E, V, C, r` (`swap_pairRank_ab`, `swap_pairRank_other`).
2. `swap_pairEdges` (exact formula, every pair): `E'(p,q) + e_K(p,q) = E(p,q) + e_K(τp,τq)`,
   where `e_K(p,q)` (`cutEdges`) counts the edges of `T − h` coloured `{p, q}` (at `c`) with
   exactly one end in `K` (`edge_map_swap`: a cut edge has its `K`-end recoloured, every other
   edge keeps its colour pair). For the mixed pairs: `swap_mixed_edges`
   `ΔE(a,x) = e_K(b,x) − e_K(a,x)`, and `swap_mixed_edges_sum`: `ΔE(a,x) + ΔE(b,x) = 0`
   (edges leaving `K` towards `x` move between the two mixed pairs containing `x`).
3. `swap_pairVerts` (every pair), `swap_mixed_verts`: `ΔV(a,x) = |K_b| − |K_a|`,
   `ΔV(b,x) = |K_a| − |K_b|`.
4. `delta_rank_sum`: `Δ Σ r = Δ Σ C` (the totals of `E` and `V` are invariant);
   `delta_rank_sum_mixed`: `Δ Σ r = ΔC(a,x) + ΔC(a,y) + ΔC(b,x) + ΔC(b,y)`;
   `delta_rank_pairing`: `Δr(a,x) + Δr(b,x) = ΔC(a,x) + ΔC(b,x)` (same for `y`).
   **This is all the sums give**: the mixed `ΔC`s are otherwise unconstrained by (2)–(3).
   `delta_C_relation`: *with* the two step dualities `Δr(a,x) = ΔC(b,y)`, `Δr(a,y) = ΔC(b,x)`
   (named hypotheses; `NightW2Euler`/`NightSixEvent` §2.1, not formalised here) and the edge
   lemma `ΔE(a,y) − ΔE(a,x) = 1`, one gets `ΔC(b,x) = ΔC(a,y) + 1 + ΔC(b,y) − ΔC(a,x)`
   (`v = y + 1 + u − x` for `(a, b, x, y) = (α, A, μ, B)`).
5. `delta_E_face_count` (the edge lemma, §2.2): at a `RepeatAt j` state, for the `{α, A}`-swap
   (`α = c x_j`, `A = c x_{j+3}`, `μ = c x_{j+1}`, `B = c x_{j+4}`) of a component `K ∋ x_{j+2}`
   with `x_j ∉ K`, `ΔE(α,B) − ΔE(α,μ) = 1`. The triangle-by-triangle cancellation
   (`tri_zero`) and the link-edge evaluation are proved; the face structure of `T − h` enters
   only through the named hypothesis `TriangleCover` (a finite family of triangles of `T − h`
   covering each edge twice, the five link edges once), the faces of the triangulation
   not containing `h`.
6. `delta_rank_odd`: under the dualities and the edge lemma, `Δ Σ r = 2(ΔC(a,y) + ΔC(b,y)) + 1`
   is odd; `delta_rank_odd_step` combines it with (5).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap Finset

/-- Four distinct colours cover `Fin 4`. -/
lemma fin4_cover : ∀ a b x y z : Fin 4, a ≠ b → a ≠ x → a ≠ y → b ≠ x → b ≠ y → x ≠ y →
    z = a ∨ z = b ∨ z = x ∨ z = y := by decide

section step
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4} {a b : Fin 4}
  {K : Set (Fin n)}

open Classical

/-! ### Changes as integers -/

/-- `ΔE(p,q)` from `c` to `c'`. -/
noncomputable def dE (M : SphericalMap n) (h : Fin n) (c c' : Fin n → Fin 4) (p q : Fin 4) : ℤ :=
  (pairEdges M h c' p q : ℤ) - pairEdges M h c p q

/-- `ΔV(p,q)` from `c` to `c'`. -/
noncomputable def dV (h : Fin n) (c c' : Fin n → Fin 4) (p q : Fin 4) : ℤ :=
  (pairVerts h c' p q : ℤ) - pairVerts h c p q

/-- `ΔC(p,q)` from `c` to `c'`. -/
noncomputable def dC (M : SphericalMap n) (h : Fin n) (c c' : Fin n → Fin 4) (p q : Fin 4) : ℤ :=
  (pairComps M h c' p q : ℤ) - pairComps M h c p q

/-- `Δr(p,q)` from `c` to `c'`. -/
noncomputable def dR (M : SphericalMap n) (h : Fin n) (c c' : Fin n → Fin 4) (p q : Fin 4) : ℤ :=
  pairRank M h c' p q - pairRank M h c p q

lemma dR_eq (c c' : Fin n → Fin 4) (p q : Fin 4) :
    dR M h c c' p q = dE M h c c' p q - dV h c c' p q + dC M h c c' p q := by
  unfold dR dE dV dC pairRank; ring

/-! ### (1) The `{a,b}`- and `{x,y}`-subgraphs are unchanged -/

/-- An `{a, b}`-swap leaves an `{x, y}`-subgraph unchanged when `{x, y}` avoids `a, b` (as
`QuarterRotation.pairGraph_swap_other`, which cannot be imported next to `QuarterEuler`). -/
lemma stepGraph_swap_other (c : Fin n → Fin 4) (K : Set (Fin n)) {x y : Fin 4}
    (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairGraph M.graph h (swap c a b K) x y = pairGraph M.graph h c x y := by
  have key : ∀ v, Active h (swap c a b K) x y v ↔ Active h c x y v := by
    intro v
    unfold Active
    by_cases hv : v ∈ K
    · rw [swap_in hv, Equiv.swap_apply_eq_iff, Equiv.swap_apply_eq_iff,
        Equiv.swap_apply_of_ne_of_ne hxa hxb, Equiv.swap_apply_of_ne_of_ne hya hyb]
    · rw [swap_out hv]
  ext u v
  exact and_congr Iff.rfl (and_congr (key u) (key v))

/-- **(1)** The `{a, b}`-subgraph and the complementary `{x, y}`-subgraph of `T − h` are
unchanged by the swap. -/
theorem swap_pair_graph_invariant (c : Fin n → Fin 4) (K : Set (Fin n)) {x y : Fin 4}
    (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairGraph M.graph h (swap c a b K) a b = pairGraph M.graph h c a b ∧
    pairGraph M.graph h (swap c a b K) x y = pairGraph M.graph h c x y :=
  ⟨pairGraph_swap c a b K, stepGraph_swap_other c K hxa hxb hya hyb⟩

lemma swap_val_eq (v : Fin n) (p : Fin 4) :
    swap c a b K v = p ↔ if v ∈ K then c v = Equiv.swap a b p else c v = p := by
  by_cases hv : v ∈ K
  · simp only [hv, ite_true]; exact swap_eq_iff hv p
  · simp only [hv, ite_false]; rw [swap_out hv]

lemma pairComps_of_graph_eq {c' : Fin n → Fin 4} {p q : Fin 4}
    (hG : pairGraph M.graph h c' p q = pairGraph M.graph h c p q)
    (hA : ∀ v, (c' v = p ∨ c' v = q) ↔ (c v = p ∨ c v = q)) :
    pairComps M h c' p q = pairComps M h c p q := by
  unfold pairComps
  rw [hG]
  simp only [hA]

lemma active_or_ab (v : Fin n) :
    (swap c a b K v = a ∨ swap c a b K v = b) ↔ (c v = a ∨ c v = b) := by
  by_cases hv : v ∈ K
  · rw [swap_in hv, Equiv.swap_apply_eq_iff, Equiv.swap_apply_eq_iff, Equiv.swap_apply_left,
      Equiv.swap_apply_right, or_comm]
  · rw [swap_out hv]

lemma active_or_other {x y : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b)
    (v : Fin n) :
    (swap c a b K v = x ∨ swap c a b K v = y) ↔ (c v = x ∨ c v = y) := by
  by_cases hv : v ∈ K
  · rw [swap_in hv, Equiv.swap_apply_eq_iff, Equiv.swap_apply_eq_iff,
      Equiv.swap_apply_of_ne_of_ne hxa hxb, Equiv.swap_apply_of_ne_of_ne hya hyb]
  · rw [swap_out hv]

theorem swap_pairComps_ab :
    pairComps M h (swap c a b K) a b = pairComps M h c a b :=
  pairComps_of_graph_eq (pairGraph_swap c a b K) active_or_ab

theorem swap_pairComps_other {x y : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a)
    (hyb : y ≠ b) : pairComps M h (swap c a b K) x y = pairComps M h c x y :=
  pairComps_of_graph_eq (stepGraph_swap_other c K hxa hxb hya hyb)
    (active_or_other hxa hxb hya hyb)

/-! ### (2) Edges -/

/-- `u v` is cut by `K`: exactly one end in `K` (as `QuarterEvenCut.Cut`). -/
def StepCut (K : Set (Fin n)) (u v : Fin n) : Prop := ¬ (u ∈ K ↔ v ∈ K)

/-- An edge `e` is cut by `K`: exactly one end in `K`. -/
def ECut (K : Set (Fin n)) : Sym2 (Fin n) → Prop :=
  Sym2.lift ⟨fun u v => StepCut K u v, fun _ _ => propext (not_congr Iff.comm)⟩

lemma eCut_mk (u v : Fin n) : ECut K s(u, v) ↔ StepCut K u v := Iff.rfl

variable (M h c K) in
/-- `e_K(p,q)`: the edges of `T − h` coloured `{p, q}` (at `c`) with exactly one end in `K`. -/
noncomputable def cutEdges (p q : Fin 4) : ℕ :=
  ((offEdges M h).filter fun e => ECut K e ∧ e.map c = s(p, q)).card

lemma cutEdges_comm (p q : Fin 4) : cutEdges M h c K p q = cutEdges M h c K q p := by
  unfold cutEdges; rw [Sym2.eq_swap]

lemma mem_offEdges {u v : Fin n} :
    s(u, v) ∈ offEdges M h ↔ M.graph.Adj u v ∧ u ≠ h ∧ v ≠ h := by
  simp only [offEdges, Finset.mem_filter, mem_edgeFinset, mem_edgeSet, Sym2.mem_iff, not_or]
  constructor
  · rintro ⟨e, h1, h2⟩; exact ⟨e, Ne.symm h1, Ne.symm h2⟩
  · rintro ⟨e, h1, h2⟩; exact ⟨e, Ne.symm h1, Ne.symm h2⟩

/-- On an edge of `T − h`, the swap recolours the colour pair by `τ` iff the edge is cut. -/
lemma edge_map_swap (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K) {u v : Fin n}
    (he : M.graph.Adj u v) (hu : u ≠ h) (hv : v ≠ h) :
    s(u, v).map (swap c a b K) =
      if ECut K s(u, v) then (s(u, v).map c).map (Equiv.swap a b) else s(u, v).map c := by
  simp only [Sym2.map_mk, eCut_mk, StepCut]
  have out : ∀ {z w : Fin n}, z ∈ K → w ∉ K → M.graph.Adj z w → w ≠ h →
      Equiv.swap a b (c w) = c w := by
    intro z w hz hw e hwh
    apply Equiv.swap_apply_of_ne_of_ne
    · intro hca; exact hw (whole_closed M.graph hK hz e ⟨hwh, Or.inl hca⟩)
    · intro hcb; exact hw (whole_closed M.graph hK hz e ⟨hwh, Or.inr hcb⟩)
  by_cases hu' : u ∈ K <;> by_cases hv' : v ∈ K
  · simp only [hu', hv', not_true_eq_false, ite_false]
    rw [swap_in hu', swap_in hv']
    have ne := hc he hu hv
    rcases (whole_active M.graph hK hu').2 with h1 | h1 <;>
      rcases (whole_active M.graph hK hv').2 with h2 | h2 <;> rw [h1, h2] at ne ⊢
    · exact absurd rfl ne
    · rw [Equiv.swap_apply_left, Equiv.swap_apply_right, Sym2.eq_swap]
    · rw [Equiv.swap_apply_left, Equiv.swap_apply_right, Sym2.eq_swap]
    · exact absurd rfl ne
  · simp only [hu', hv', iff_false, not_true_eq_false, not_false_eq_true, ite_true]
    rw [swap_in hu', swap_out hv', out hu' hv' he hv]
  · simp only [hu', hv', false_iff, not_true_eq_false, not_false_eq_true, ite_true]
    rw [swap_out hu', swap_in hv', out hv' hu' he.symm hu]
  · simp only [hu', hv', iff_self, not_true_eq_false, ite_false]
    rw [swap_out hu', swap_out hv']

lemma map_swap_eq_iff (z : Sym2 (Fin 4)) (p q : Fin 4) :
    z.map (Equiv.swap a b) = s(p, q) ↔ z = s(Equiv.swap a b p, Equiv.swap a b q) := by
  constructor
  · intro e
    have := congrArg (Sym2.map (Equiv.swap a b)) e
    simpa [Sym2.map_map, Function.comp_def, Equiv.swap_apply_self] using this
  · rintro rfl
    simp [Equiv.swap_apply_self]

/-- **(2) Exact edge formula**, every pair: `E'(p,q) + e_K(p,q) = E(p,q) + e_K(τp,τq)`. -/
theorem swap_pairEdges (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    (p q : Fin 4) :
    pairEdges M h (swap c a b K) p q + cutEdges M h c K p q =
      pairEdges M h c p q + cutEdges M h c K (Equiv.swap a b p) (Equiv.swap a b q) := by
  unfold pairEdges cutEdges
  simp only [Finset.card_filter]
  rw [← sum_add_distrib, ← sum_add_distrib]
  refine sum_congr rfl fun e he => ?_
  induction e using Sym2.ind with
  | h u v =>
  obtain ⟨hadj, hu, hv⟩ := mem_offEdges.mp he
  rw [edge_map_swap hc hK hadj hu hv]
  by_cases hcut : ECut K s(u, v)
  · simp only [hcut, ite_true, true_and]
    simp only [map_swap_eq_iff]; exact add_comm _ _
  · simp [hcut]

/-- **(2) Mixed pairs.** For `x ∉ {a, b}`: `ΔE(a,x) = e_K(b,x) − e_K(a,x)` and
`ΔE(b,x) = e_K(a,x) − e_K(b,x)`. -/
theorem swap_mixed_edges (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K) {x : Fin 4}
    (hxa : x ≠ a) (hxb : x ≠ b) :
    dE M h c (swap c a b K) a x = (cutEdges M h c K b x : ℤ) - cutEdges M h c K a x ∧
    dE M h c (swap c a b K) b x = (cutEdges M h c K a x : ℤ) - cutEdges M h c K b x := by
  have e1 := swap_pairEdges hc hK a x
  have e2 := swap_pairEdges hc hK b x
  rw [Equiv.swap_apply_left, Equiv.swap_apply_of_ne_of_ne hxa hxb] at e1
  rw [Equiv.swap_apply_right, Equiv.swap_apply_of_ne_of_ne hxa hxb] at e2
  unfold dE
  constructor <;> omega

/-- **(2)** The cut edges towards `x` move between the two mixed pairs containing `x`:
`ΔE(a,x) + ΔE(b,x) = 0`. -/
theorem swap_mixed_edges_sum (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    {x : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) :
    dE M h c (swap c a b K) a x + dE M h c (swap c a b K) b x = 0 := by
  obtain ⟨e1, e2⟩ := swap_mixed_edges hc hK hxa hxb
  rw [e1, e2]; ring

theorem swap_pairEdges_ab (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K) :
    pairEdges M h (swap c a b K) a b = pairEdges M h c a b := by
  have e := swap_pairEdges hc hK a b
  rw [Equiv.swap_apply_left, Equiv.swap_apply_right, cutEdges_comm b a] at e
  omega

theorem swap_pairEdges_other (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    {x y : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairEdges M h (swap c a b K) x y = pairEdges M h c x y := by
  have e := swap_pairEdges hc hK x y
  rw [Equiv.swap_apply_of_ne_of_ne hxa hxb, Equiv.swap_apply_of_ne_of_ne hya hyb] at e
  omega

/-! ### (3) Vertices -/

variable (c K) in
/-- The vertices of `K` coloured `p` or `q` (at `c`). -/
noncomputable def kVerts (p q : Fin 4) : ℕ :=
  (Finset.univ.filter fun v => v ∈ K ∧ (c v = p ∨ c v = q)).card

variable (c K) in
/-- `|K_p|`: the vertices of `K` coloured `p`. -/
noncomputable def kCount (p : Fin 4) : ℕ :=
  (Finset.univ.filter fun v => v ∈ K ∧ c v = p).card

/-- **(3) Exact vertex formula**, every pair: `V'(p,q) + |K ∩ {p,q}| = V(p,q) + |K ∩ {τp,τq}|`. -/
theorem swap_pairVerts (hK : Whole M.graph h c a b K) (p q : Fin 4) :
    pairVerts h (swap c a b K) p q + kVerts c K p q =
      pairVerts h c p q + kVerts c K (Equiv.swap a b p) (Equiv.swap a b q) := by
  unfold pairVerts kVerts
  simp only [Finset.card_filter]
  rw [← sum_add_distrib, ← sum_add_distrib]
  refine sum_congr rfl fun v _ => ?_
  by_cases hv : v ∈ K
  · have hvh : v ≠ h := (whole_active M.graph hK hv).1
    simp only [hv, hvh, ne_eq, not_false_eq_true, true_and, swap_eq_iff hv]
    exact add_comm _ _
  · simp [hv, swap_out hv]

lemma kVerts_mixed (hK : Whole M.graph h c a b K) {x : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b)
    (p : Fin 4) : kVerts c K p x = kCount c K p := by
  unfold kVerts kCount
  congr 1
  refine Finset.filter_congr fun v _ => ?_
  constructor
  · rintro ⟨hv, h1 | h1⟩
    · exact ⟨hv, h1⟩
    · exfalso
      rcases (whole_active M.graph hK hv).2 with h2 | h2 <;> rw [h1] at h2
      · exact hxa h2
      · exact hxb h2
  · rintro ⟨hv, h1⟩; exact ⟨hv, Or.inl h1⟩

/-- **(3) Mixed pairs.** `ΔV(a,x) = |K_b| − |K_a|` and `ΔV(b,x) = |K_a| − |K_b|`. -/
theorem swap_mixed_verts (hK : Whole M.graph h c a b K) {x : Fin 4} (hxa : x ≠ a)
    (hxb : x ≠ b) :
    dV h c (swap c a b K) a x = (kCount c K b : ℤ) - kCount c K a ∧
    dV h c (swap c a b K) b x = (kCount c K a : ℤ) - kCount c K b := by
  have e1 := swap_pairVerts hK a x
  have e2 := swap_pairVerts hK b x
  rw [Equiv.swap_apply_left, Equiv.swap_apply_of_ne_of_ne hxa hxb] at e1
  rw [Equiv.swap_apply_right, Equiv.swap_apply_of_ne_of_ne hxa hxb] at e2
  rw [kVerts_mixed hK hxa hxb a, kVerts_mixed hK hxa hxb b] at e1 e2
  unfold dV
  constructor <;> omega

theorem swap_pairVerts_ab (hK : Whole M.graph h c a b K) :
    pairVerts h (swap c a b K) a b = pairVerts h c a b := by
  have e := swap_pairVerts hK a b
  rw [Equiv.swap_apply_left, Equiv.swap_apply_right] at e
  have : kVerts c K b a = kVerts c K a b := by
    unfold kVerts; congr 1; exact Finset.filter_congr fun v _ => by rw [or_comm]
  omega

theorem swap_pairVerts_other (hK : Whole M.graph h c a b K) {x y : Fin 4} (hxa : x ≠ a)
    (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairVerts h (swap c a b K) x y = pairVerts h c x y := by
  have e := swap_pairVerts hK x y
  rw [Equiv.swap_apply_of_ne_of_ne hxa hxb, Equiv.swap_apply_of_ne_of_ne hya hyb] at e
  omega

/-- **(1)** The rank of the `{a, b}`-graph is unchanged. -/
theorem swap_pairRank_ab (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K) :
    pairRank M h (swap c a b K) a b = pairRank M h c a b := by
  unfold pairRank
  rw [swap_pairEdges_ab hc hK, swap_pairVerts_ab hK, swap_pairComps_ab]

/-- **(1)** The rank of the complementary `{x, y}`-graph is unchanged. -/
theorem swap_pairRank_other (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    {x y : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairRank M h (swap c a b K) x y = pairRank M h c x y := by
  unfold pairRank
  rw [swap_pairEdges_other hc hK hxa hxb hya hyb, swap_pairVerts_other hK hxa hxb hya hyb,
    swap_pairComps_other hxa hxb hya hyb]

/-! ### (4) Sums -/

/-- **(4)** `Δ Σ r = Δ Σ C`: the totals `Σ E` and `Σ V` are invariant. -/
theorem delta_rank_sum (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K) :
    ∑ p ∈ pairs, pairRank M h (swap c a b K) p.1 p.2 - ∑ p ∈ pairs, pairRank M h c p.1 p.2 =
      ∑ p ∈ pairs, (pairComps M h (swap c a b K) p.1 p.2 : ℤ) -
        ∑ p ∈ pairs, (pairComps M h c p.1 p.2 : ℤ) := by
  have hc' := properOff_swap M.graph hc hK
  have hE := sum_edges_pairs M h c hc
  have hE' := sum_edges_pairs M h _ hc'
  have hV := sum_vertices_pairs h c
  have hV' := sum_vertices_pairs h (swap c a b K)
  unfold pairRank
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  have hE2 : ∑ p ∈ pairs, (pairEdges M h (swap c a b K) p.1 p.2 : ℤ) =
      ∑ p ∈ pairs, (pairEdges M h c p.1 p.2 : ℤ) := by exact_mod_cast hE'.trans hE.symm
  have hV2 : ∑ p ∈ pairs, (pairVerts h (swap c a b K) p.1 p.2 : ℤ) =
      ∑ p ∈ pairs, (pairVerts h c p.1 p.2 : ℤ) := by
    have : ∑ p ∈ pairs, pairVerts h (swap c a b K) p.1 p.2 = ∑ p ∈ pairs, pairVerts h c p.1 p.2 :=
      by omega
    exact_mod_cast this
  rw [hE2, hV2]; ring

/-- A symmetric function summed over the six sorted pairs, listed from any enumeration
`a, b, x, y` of the four colours. -/
lemma sum_pairs_eq (f : Fin 4 → Fin 4 → ℤ) (hf : ∀ p q, f p q = f q p) {a b x y : Fin 4}
    (hab : a ≠ b) (hax : a ≠ x) (hay : a ≠ y) (hbx : b ≠ x) (hby : b ≠ y) (hxy : x ≠ y) :
    ∑ p ∈ pairs, f p.1 p.2 = f a b + f a x + f a y + f b x + f b y + f x y := by
  rw [show pairs = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)} from by decide]
  rw [sum_insert (by decide), sum_insert (by decide), sum_insert (by decide),
    sum_insert (by decide), sum_insert (by decide), sum_singleton]
  have s01 := hf 0 1; have s02 := hf 0 2; have s03 := hf 0 3
  have s12 := hf 1 2; have s13 := hf 1 3; have s23 := hf 2 3
  fin_cases a <;> fin_cases b <;> fin_cases x <;> fin_cases y <;>
    first
    | (exfalso; revert hab hax hay hbx hby hxy; decide)
    | (try simp only [Fin.zero_eta, Fin.isValue, Fin.mk_one, Fin.reduceFinMk] at *); linarith

/-- **(4)** `Δ Σ r` is the sum of the four mixed `ΔC`s (the `{a,b}` and `{x,y}` terms vanish). -/
theorem delta_rank_sum_mixed (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    {x y : Fin 4} (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b)
    (hxy : x ≠ y) :
    ∑ p ∈ pairs, pairRank M h (swap c a b K) p.1 p.2 - ∑ p ∈ pairs, pairRank M h c p.1 p.2 =
      dC M h c (swap c a b K) a x + dC M h c (swap c a b K) a y +
        dC M h c (swap c a b K) b x + dC M h c (swap c a b K) b y := by
  rw [delta_rank_sum hc hK, ← Finset.sum_sub_distrib]
  have hsym : ∀ p q, dC M h c (swap c a b K) p q = dC M h c (swap c a b K) q p := by
    intro p q; unfold dC; rw [pairComps_comm, pairComps_comm (c := c)]
  rw [show (∑ p ∈ pairs, ((pairComps M h (swap c a b K) p.1 p.2 : ℤ) -
      pairComps M h c p.1 p.2)) = ∑ p ∈ pairs, dC M h c (swap c a b K) p.1 p.2 from rfl,
    sum_pairs_eq _ hsym hab hxa.symm hya.symm hxb.symm hyb.symm hxy]
  have h1 : dC M h c (swap c a b K) a b = 0 := by unfold dC; rw [swap_pairComps_ab]; ring
  have h2 : dC M h c (swap c a b K) x y = 0 := by
    unfold dC; rw [swap_pairComps_other hxa hxb hya hyb]; ring
  rw [h1, h2]; ring

/-- **(4)** For each colour `x ∉ {a,b}`: `Δr(a,x) + Δr(b,x) = ΔC(a,x) + ΔC(b,x)`. -/
theorem delta_rank_pairing (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    {x : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) :
    dR M h c (swap c a b K) a x + dR M h c (swap c a b K) b x =
      dC M h c (swap c a b K) a x + dC M h c (swap c a b K) b x := by
  rw [dR_eq, dR_eq]
  have e := swap_mixed_edges_sum hc hK hxa hxb
  obtain ⟨v1, v2⟩ := swap_mixed_verts hK hxa hxb
  rw [v1, v2]; linarith

/-- **(4) The NightSixEvent relation** `v = y + 1 + u − x`, from the two step dualities
`Δr(a,x) = ΔC(b,y)`, `Δr(a,y) = ΔC(b,x)` (named hypotheses) and the edge lemma. -/
theorem delta_C_relation (hK : Whole M.graph h c a b K) {x y : Fin 4} (hxa : x ≠ a)
    (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b)
    (hdual1 : dR M h c (swap c a b K) a x = dC M h c (swap c a b K) b y)
    (hdual2 : dR M h c (swap c a b K) a y = dC M h c (swap c a b K) b x)
    (hedge : dE M h c (swap c a b K) a y - dE M h c (swap c a b K) a x = 1) :
    dC M h c (swap c a b K) b x =
      dC M h c (swap c a b K) a y + 1 + dC M h c (swap c a b K) b y -
        dC M h c (swap c a b K) a x := by
  rw [dR_eq] at hdual1 hdual2
  have v1 := (swap_mixed_verts hK hxa hxb).1
  have v2 := (swap_mixed_verts hK hya hyb).1
  linarith

/-- **(6)** Under the dualities and the edge lemma, `Δ Σ r = 2(ΔC(a,y) + ΔC(b,y)) + 1`; in
particular it is odd. -/
theorem delta_rank_odd (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K)
    {x y : Fin 4} (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b)
    (hxy : x ≠ y)
    (hdual1 : dR M h c (swap c a b K) a x = dC M h c (swap c a b K) b y)
    (hdual2 : dR M h c (swap c a b K) a y = dC M h c (swap c a b K) b x)
    (hedge : dE M h c (swap c a b K) a y - dE M h c (swap c a b K) a x = 1) :
    ∑ p ∈ pairs, pairRank M h (swap c a b K) p.1 p.2 - ∑ p ∈ pairs, pairRank M h c p.1 p.2 =
      2 * (dC M h c (swap c a b K) a y + dC M h c (swap c a b K) b y) + 1 ∧
    Odd (∑ p ∈ pairs, pairRank M h (swap c a b K) p.1 p.2 -
      ∑ p ∈ pairs, pairRank M h c p.1 p.2) := by
  have e := delta_rank_sum_mixed hc hK hab hxa hxb hya hyb hxy
  have r := delta_C_relation hK hxa hxb hya hyb hdual1 hdual2 hedge
  have key : ∑ p ∈ pairs, pairRank M h (swap c a b K) p.1 p.2 -
      ∑ p ∈ pairs, pairRank M h c p.1 p.2 =
      2 * (dC M h c (swap c a b K) a y + dC M h c (swap c a b K) b y) + 1 := by
    rw [e, r]; ring
  exact ⟨key, ⟨_, key⟩⟩

end step

/-! ### (5) The edge lemma by a face count -/

section face
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4} {a b : Fin 4}
  {K : Set (Fin n)}

open Classical

/-- The five link edges `x_i x_{i+1}` of a pentagonal hole. -/
noncomputable def linkEdges (P : Pent M.graph h) : Finset (Sym2 (Fin n)) :=
  Finset.univ.image fun i : Fin 5 => s(P.x i, P.x (i + 1))

/-- **Named hypothesis (face structure).** `T` is a family of triangles of `T − h` (each
`t : Fin 3 → Fin n` with sides `t k t (k+1)`) covering every edge of `T − h` exactly twice,
except the five link edges, covered once. For a triangulated spherical map this is the family
of faces not containing `h` (each edge lies in two faces; the five faces at `h` are
`h x_i x_{i+1}`); this file does not derive it from the rotation system. -/
def TriangleCover (P : Pent M.graph h) (T : Finset (Fin 3 → Fin n)) : Prop :=
  (∀ t ∈ T, ∀ k : Fin 3, s(t k, t (k + 1)) ∈ offEdges M h) ∧
  ∀ e ∈ offEdges M h,
    ∑ t ∈ T, ((Finset.univ : Finset (Fin 3)).filter fun k => s(t k, t (k + 1)) = e).card =
      if e ∈ linkEdges P then 1 else 2

/-- The weight `[A B] − [α B] − [A μ] + [α μ]` of a colour pair, with `(α, A, μ, B) =
(a, b, x, y)`. -/
def wt (a b x y : Fin 4) (z : Sym2 (Fin 4)) : ℤ :=
  (if z = s(b, y) then 1 else 0) - (if z = s(a, y) then 1 else 0) -
    (if z = s(b, x) then 1 else 0) + (if z = s(a, x) then 1 else 0)

variable (c K) in
/-- The weight of an edge: `wt` of its colour pair if it is cut by `K`, else `0`. -/
noncomputable def phi (a b x y : Fin 4) (e : Sym2 (Fin n)) : ℤ :=
  if ECut K e then wt a b x y (e.map c) else 0

lemma sum_phi (a b x y : Fin 4) :
    ∑ e ∈ offEdges M h, phi c K a b x y e =
      (cutEdges M h c K b y : ℤ) - cutEdges M h c K a y - cutEdges M h c K b x +
        cutEdges M h c K a x := by
  unfold cutEdges
  simp only [Finset.card_filter]
  push_cast
  rw [← sum_sub_distrib, ← sum_sub_distrib, ← sum_add_distrib]
  refine sum_congr rfl fun e _ => ?_
  unfold phi wt
  by_cases hcut : ECut K e <;> simp [hcut]

/-- **The face count.** `Σ_e w(e) φ(e) = Σ_{t} Σ_k φ(side_k t)` with `w = 1` on link edges and
`2` elsewhere. -/
lemma face_sum (P : Pent M.graph h) {T : Finset (Fin 3 → Fin n)} (hT : TriangleCover P T)
    (f : Sym2 (Fin n) → ℤ) :
    ∑ e ∈ offEdges M h, (if e ∈ linkEdges P then (1 : ℤ) else 2) * f e =
      ∑ t ∈ T, ∑ k : Fin 3, f s(t k, t (k + 1)) := by
  calc ∑ e ∈ offEdges M h, (if e ∈ linkEdges P then (1 : ℤ) else 2) * f e
      = ∑ e ∈ offEdges M h, ∑ t ∈ T, ∑ k : Fin 3,
          (if s(t k, t (k + 1)) = e then f e else 0) := by
        refine sum_congr rfl fun e he => ?_
        have h2 := hT.2 e he
        have h3 : (if e ∈ linkEdges P then (1 : ℤ) else 2) =
            ((if e ∈ linkEdges P then 1 else 2 : ℕ) : ℤ) := by split_ifs <;> rfl
        rw [h3, ← h2]
        push_cast
        rw [sum_mul]
        refine sum_congr rfl fun t _ => ?_
        rw [Finset.card_filter]
        push_cast
        rw [sum_mul]
        refine sum_congr rfl fun k _ => ?_
        split_ifs <;> simp
    _ = ∑ t ∈ T, ∑ k : Fin 3, ∑ e ∈ offEdges M h,
          (if s(t k, t (k + 1)) = e then f e else 0) := by
        rw [sum_comm]
        refine sum_congr rfl fun t _ => ?_
        rw [sum_comm]
    _ = ∑ t ∈ T, ∑ k : Fin 3, f s(t k, t (k + 1)) := by
        refine sum_congr rfl fun t ht => sum_congr rfl fun k _ => ?_
        rw [sum_ite_eq]; simp [hT.1 t ht k]

lemma wt_one {a b x y p q r : Fin 4} (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a)
    (hyb : y ≠ b) (hxy : x ≠ y) (hp : p = a ∨ p = b) (hq : q = x ∨ q = y) (hr : r = x ∨ r = y)
    (hqr : q ≠ r) : wt a b x y s(p, q) + wt a b x y s(r, p) = 0 := by
  rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> rcases hr with rfl | rfl <;>
    first
    | exact absurd rfl hqr
    | simp [wt, hab, hab.symm, hxa, hxa.symm, hxb, hxb.symm, hya, hya.symm, hyb,
        hyb.symm, hxy, hxy.symm]

lemma wt_two {a b x y p q r : Fin 4} (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a)
    (hyb : y ≠ b) (hxy : x ≠ y) (hp : p = a ∨ p = b) (hq : q = a ∨ q = b) (hpq : p ≠ q)
    (hr : r = x ∨ r = y) : wt a b x y s(q, r) + wt a b x y s(r, p) = 0 := by
  rcases hp with rfl | rfl <;> rcases hq with rfl | rfl <;> rcases hr with rfl | rfl <;>
    first
    | exact absurd rfl hpq
    | simp [wt, hab, hab.symm, hxa, hxa.symm, hxb, hxb.symm, hya, hya.symm, hyb,
        hyb.symm, hxy, hxy.symm]

lemma phi_nocut {a b x y : Fin 4} {u v : Fin n} (hu : u ∈ K ↔ v ∈ K) :
    phi c K a b x y s(u, v) = 0 := by
  unfold phi
  have hn : ¬ ECut K s(u, v) := by rw [eCut_mk, StepCut, not_not]; exact hu
  simp [hn]

lemma phi_cut {a b x y : Fin 4} {u v : Fin n} (hu : ¬ (u ∈ K ↔ v ∈ K)) :
    phi c K a b x y s(u, v) = wt a b x y s(c u, c v) := by
  unfold phi
  have hn : ECut K s(u, v) := by rw [eCut_mk]; exact hu
  simp [hn]

/-- **Per-triangle cancellation.** Every triangle of `T − h` has total weight `0`. -/
lemma tri_zero (hc : ProperOff M.graph h c) (hK : Whole M.graph h c a b K) {x y : Fin 4}
    (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) (hxy : x ≠ y)
    {u v w : Fin n} (huv : M.graph.Adj u v) (hvw : M.graph.Adj v w) (hwu : M.graph.Adj w u)
    (hu : u ≠ h) (hv : v ≠ h) (hw : w ≠ h) :
    phi c K a b x y s(u, v) + phi c K a b x y s(v, w) + phi c K a b x y s(w, u) = 0 := by
  have cov := fin4_cover a b x y
  have inK : ∀ {z : Fin n}, z ∈ K → c z = a ∨ c z = b := fun hz => (whole_active _ hK hz).2
  have outK : ∀ {z z' : Fin n}, z ∈ K → z' ∉ K → M.graph.Adj z z' → z' ≠ h →
      c z' = x ∨ c z' = y := by
    intro z z' hz hz' e hz'h
    have h1 : c z' ≠ a := fun e' => hz' (whole_closed M.graph hK hz e ⟨hz'h, Or.inl e'⟩)
    have h2 : c z' ≠ b := fun e' => hz' (whole_closed M.graph hK hz e ⟨hz'h, Or.inr e'⟩)
    rcases cov (c z') hab hxa.symm hya.symm hxb.symm hyb.symm hxy with e | e | e | e
    · exact absurd e h1
    · exact absurd e h2
    · exact Or.inl e
    · exact Or.inr e
  -- one vertex in `K`
  have one : ∀ {u v w : Fin n}, M.graph.Adj u v → M.graph.Adj v w → M.graph.Adj w u →
      u ≠ h → v ≠ h → w ≠ h → u ∈ K → v ∉ K → w ∉ K →
      phi c K a b x y s(u, v) + phi c K a b x y s(v, w) + phi c K a b x y s(w, u) = 0 := by
    intro u v w huv hvw hwu hu hv hw ku kv kw
    rw [phi_cut (by tauto), phi_nocut (by tauto), phi_cut (by tauto), add_zero]
    exact wt_one hab hxa hxb hya hyb hxy (inK ku) (outK ku kv huv hv) (outK ku kw hwu.symm hw)
      (hc hvw hv hw)
  -- two vertices in `K`
  have two : ∀ {u v w : Fin n}, M.graph.Adj u v → M.graph.Adj v w → M.graph.Adj w u →
      u ≠ h → v ≠ h → w ≠ h → u ∈ K → v ∈ K → w ∉ K →
      phi c K a b x y s(u, v) + phi c K a b x y s(v, w) + phi c K a b x y s(w, u) = 0 := by
    intro u v w huv hvw hwu hu hv hw ku kv kw
    rw [phi_nocut (by tauto), phi_cut (by tauto), phi_cut (by tauto), zero_add]
    exact wt_two hab hxa hxb hya hyb hxy (inK ku) (inK kv) (hc huv hu hv)
      (outK kv kw hvw hw)
  by_cases ku : u ∈ K <;> by_cases kv : v ∈ K <;> by_cases kw : w ∈ K
  · rw [phi_nocut (by tauto), phi_nocut (by tauto), phi_nocut (by tauto)]; simp
  · exact two huv hvw hwu hu hv hw ku kv kw
  · have := two hwu huv hvw hw hu hv kw ku kv; linarith
  · exact one huv hvw hwu hu hv hw ku kv kw
  · have := two hvw hwu huv hv hw hu kv kw ku; linarith
  · have := one hvw hwu huv hv hw hu kv kw ku; linarith
  · have := one hwu huv hvw hw hu hv kw ku kv; linarith
  · rw [phi_nocut (by tauto), phi_nocut (by tauto), phi_nocut (by tauto)]; simp

lemma link_inj (P : Pent M.graph h) :
    Set.InjOn (fun i : Fin 5 => s(P.x i, P.x (i + 1))) (Finset.univ : Finset (Fin 5)) := by
  intro i _ j _ e
  rcases Sym2.eq_iff.mp e with ⟨h1, -⟩ | ⟨h1, h2⟩
  · exact P.inj h1
  · have e1 := P.inj h1; have e2 := P.inj h2
    subst e1
    exact absurd e2 ((by decide : ∀ k : Fin 5, k + 1 + 1 ≠ k) j)

lemma linkEdges_sub (P : Pent M.graph h) : linkEdges P ⊆ offEdges M h := by
  intro e he
  simp only [linkEdges, Finset.mem_image, Finset.mem_univ, true_and] at he
  obtain ⟨i, rfl⟩ := he
  exact mem_offEdges.mpr ⟨P.adj_cyc i, (P.adj_h i).ne', (P.adj_h (i + 1)).ne'⟩

/-- **(5) The edge lemma** (`NightSixEvent` §2.2). At a `RepeatAt j` state, swap `{α, A}` with
`α = c x_j`, `A = c x_{j+3}` on a component `K ∋ x_{j+2}` with `x_j ∉ K` (`pair_own` and `Lock2`);
write `μ = c x_{j+1}`, `B = c x_{j+4}`. Given the face structure `TriangleCover`,
`ΔE(α,B) − ΔE(α,μ) = 1`. -/
theorem delta_E_face_count (hc : ProperOff M.graph h c) (P : Pent M.graph h) {j : Fin 5}
    (hr : RepeatAt P c j)
    (hK : Whole M.graph h c (c (P.x j)) (c (P.x (j + 3))) K)
    (h2 : P.x (j + 2) ∈ K) (h0 : P.x j ∉ K)
    {T : Finset (Fin 3 → Fin n)} (hT : TriangleCover P T) :
    dE M h c (swap c (c (P.x j)) (c (P.x (j + 3))) K) (c (P.x j)) (c (P.x (j + 4))) -
      dE M h c (swap c (c (P.x j)) (c (P.x (j + 3))) K) (c (P.x j)) (c (P.x (j + 1))) = 1 := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  set α := c (P.x j) with hα
  set A := c (P.x (j + 3)) with hA
  set μ := c (P.x (j + 1)) with hμ
  set B := c (P.x (j + 4)) with hB
  have hab : α ≠ A := Ne.symm h3
  have hxa : μ ≠ α := h1
  have hxb : μ ≠ A := h13
  have hya : B ≠ α := h4
  have hyb : B ≠ A := Ne.symm h34
  have hxy : μ ≠ B := h14
  -- the change as the weighted cut count
  obtain ⟨eB, -⟩ := swap_mixed_edges hc hK hya hyb
  obtain ⟨eμ, -⟩ := swap_mixed_edges hc hK hxa hxb
  rw [eB, eμ]
  have hsum := sum_phi (M := M) (h := h) (c := c) (K := K) α A μ B
  -- triangles cancel
  have hzero : ∑ e ∈ offEdges M h, (if e ∈ linkEdges P then (1 : ℤ) else 2) *
      phi c K α A μ B e = 0 := by
    rw [face_sum P hT]
    refine sum_eq_zero fun t ht => ?_
    have s0 := mem_offEdges.mp (hT.1 t ht 0)
    have s1 := mem_offEdges.mp (hT.1 t ht 1)
    have s2 := mem_offEdges.mp (hT.1 t ht 2)
    simp only [Fin.isValue, Fin.reduceAdd] at s0 s1 s2
    rw [Fin.sum_univ_three]
    simp only [Fin.isValue, Fin.reduceAdd]
    exact tri_zero hc hK hab hxa hxb hya hyb hxy s0.1 s1.1 s2.1 s0.2.1 s1.2.1 s2.2.1
  -- split the weights
  have hsplit : ∑ e ∈ offEdges M h, (if e ∈ linkEdges P then (1 : ℤ) else 2) *
      phi c K α A μ B e =
      2 * ∑ e ∈ offEdges M h, phi c K α A μ B e - ∑ e ∈ linkEdges P, phi c K α A μ B e := by
    have : ∀ e ∈ offEdges M h, (if e ∈ linkEdges P then (1 : ℤ) else 2) * phi c K α A μ B e =
        2 * phi c K α A μ B e - (if e ∈ linkEdges P then phi c K α A μ B e else 0) := by
      intro e _; split_ifs <;> ring
    rw [sum_congr rfl this, sum_sub_distrib, ← mul_sum, sum_ite_mem,
      Finset.inter_eq_right.mpr (linkEdges_sub P)]
  -- the link edges
  have hlink : ∑ e ∈ linkEdges P, phi c K α A μ B e = 2 := by
    unfold linkEdges
    rw [sum_image (link_inj P)]
    rw [← Equiv.sum_comp (Equiv.addLeft j)]
    simp only [Equiv.coe_addLeft, Fin.sum_univ_five, add_zero, add_assoc, Fin.isValue,
      Fin.reduceAdd]
    have hA3 : P.x (j + 3) ∈ K :=
      whole_closed M.graph hK h2 (by simpa [add_assoc] using P.adj_cyc (j + 2))
        ⟨(P.adj_h _).ne', Or.inr rfl⟩
    have h1K : P.x (j + 1) ∉ K := by
      intro hm; rcases (whole_active M.graph hK hm).2 with e | e
      · exact hxa e
      · exact hxb e
    have h4K : P.x (j + 4) ∉ K := by
      intro hm; rcases (whole_active M.graph hK hm).2 with e | e
      · exact hya e
      · exact hyb e
    rw [phi_nocut (by tauto), phi_cut (by tauto), phi_nocut (by tauto), phi_cut (by tauto),
      phi_nocut (by tauto)]
    simp only [← hμ, ← hA, ← hB, ← h02]
    simp [wt, hab, hab.symm, hxa, hxa.symm, hxb, hxb.symm, hya, hya.symm, hyb,
      hyb.symm, hxy, hxy.symm]
  linarith

/-- **(5) + (6)** At a `RepeatAt j` step as in `delta_E_face_count`, given the face structure
and the two step dualities (named hypotheses), `Δ Σ r` is odd. -/
theorem delta_rank_odd_step (hc : ProperOff M.graph h c) (P : Pent M.graph h) {j : Fin 5}
    (hr : RepeatAt P c j)
    (hK : Whole M.graph h c (c (P.x j)) (c (P.x (j + 3))) K)
    (h2 : P.x (j + 2) ∈ K) (h0 : P.x j ∉ K)
    {T : Finset (Fin 3 → Fin n)} (hT : TriangleCover P T)
    (hdual1 : dR M h c (swap c (c (P.x j)) (c (P.x (j + 3))) K) (c (P.x j)) (c (P.x (j + 1))) =
      dC M h c (swap c (c (P.x j)) (c (P.x (j + 3))) K) (c (P.x (j + 3))) (c (P.x (j + 4))))
    (hdual2 : dR M h c (swap c (c (P.x j)) (c (P.x (j + 3))) K) (c (P.x j)) (c (P.x (j + 4))) =
      dC M h c (swap c (c (P.x j)) (c (P.x (j + 3))) K) (c (P.x (j + 3))) (c (P.x (j + 1)))) :
    Odd (∑ p ∈ pairs, pairRank M h (swap c (c (P.x j)) (c (P.x (j + 3))) K) p.1 p.2 -
      ∑ p ∈ pairs, pairRank M h c p.1 p.2) := by
  have hedge := delta_E_face_count hc P hr hK h2 h0 hT
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  exact (delta_rank_odd hc hK (Ne.symm h3) h1 h13 h4 (Ne.symm h34) h14 hdual1 hdual2 hedge).2

end face

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.swap_pair_graph_invariant
#print axioms SimpleGraph.QuarterFloor.swap_pairRank_ab
#print axioms SimpleGraph.QuarterFloor.swap_pairRank_other
#print axioms SimpleGraph.QuarterFloor.swap_pairEdges
#print axioms SimpleGraph.QuarterFloor.swap_mixed_edges_sum
#print axioms SimpleGraph.QuarterFloor.swap_mixed_verts
#print axioms SimpleGraph.QuarterFloor.delta_rank_sum
#print axioms SimpleGraph.QuarterFloor.delta_rank_sum_mixed
#print axioms SimpleGraph.QuarterFloor.delta_rank_pairing
#print axioms SimpleGraph.QuarterFloor.delta_C_relation
#print axioms SimpleGraph.QuarterFloor.delta_rank_odd
#print axioms SimpleGraph.QuarterFloor.delta_E_face_count
#print axioms SimpleGraph.QuarterFloor.delta_rank_odd_step
