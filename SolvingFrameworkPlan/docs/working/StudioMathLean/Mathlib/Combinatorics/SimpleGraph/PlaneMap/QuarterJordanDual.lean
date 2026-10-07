/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaK34
public import Mathlib.Data.Fin.VecNotation

/-!
# The Jordan duality (D) at `k = 3, 4`

Formalises the Kempe/Jordan duality (D) of `NightC1Gamma.md` §2 in the two configurations
where `QuarterSigmaK34` needs it, and derives the notes' final exit criteria. Frame as in
`QuarterSigmaK34`: link `(α, μ, α, A, B)` at `x j, …, x (j+4)`, ring `(w₀..w₄) = (B, A, B, μ, A)`,
`m = α` (Lemma D).

## Main results (sorry-free, no new axioms)

* `duality_k4` (`K4Ball`, triangulated):
  `w₀ ⇝ m` in the `{α, B}`-graph with `x j` deleted  ↔  `¬ (w₄ ∈ K_{μ,A}(x (j+1)))`.
* `duality_k3` (`K3Ball`, triangulated):
  `w₁ ⇝ m` in the `{α, A}`-graph with `x (j+2)` deleted  ↔  `¬ (w₂ ∈ K_{μ,B}(x (j+1)))`.
* `sigma_exit_criterion_k4'`: `σ c` lockless ↔ `w₄ ∈ K_{μ,A}(x (j+1))` (the note's form).
  `sigma_exit_criterion_k3'`: `σ c` lockless ↔ `w₂ ∈ K_{μ,B}(x (j+1))`.
* `sigma_exit_f_ge_two_k3'`: at `k = 3` a lockless `σ`-exit has `f ≥ 2`, unconditionally
  (`sigma_exit_f_ge_two_k3` with its hypothesis discharged by (D)).

## Method

"Not both" (`not_both_k4`, `not_both_k3`, no triangulation needed) is Kempe separation at the
degree-five link vertex `x j` (resp. `x (j+2)`): its neighbours `h, x (j+1), w₀, w₄, x (j+4)`
(resp. `h, x (j+1), w₁, w₂, x (j+3)`) form a 5-cycle, so the vertex is itself a `Pent` centre
(`pent5`), and `lock_separates` applies to the closed `{α, B}`-walk `x j, x (j+4), m, …, w₀`
against the `{μ, A}`-walk `x (j+1), …, w₄`.

"At least one" (`hex_core`) is the boundary-parity argument of `kempe_hex`, with `S` the
`{μ, A}`- (resp. `{μ, B}`-) component of `x (j+1)`. Lock 1 (resp. Lock 2) of the `R3` state puts
`x (j+3)` (resp. `x (j+4)`) in `S`, so the only boundary edges at `h` go to `x j` and `x (j+4)`
(resp. `x (j+2)` and `x (j+3)`); when `w₄ ∉ S` (resp. `w₂ ∉ S`) the only other boundary edge at
the degree-five vertex goes to `w₀` (resp. `w₁`). The handshake lemma then joins `w₀` to
`x (j+4)` (resp. `w₁` to `x (j+3)`) through boundary edges avoiding `h` and the deleted vertex,
and every such edge is `{α, B}` (resp. `{α, A}`). The planar helpers of `QuarterRotationPlanar`
are private there and are copied verbatim below.

## Not formalised: `f ≥ 2` at `k = 4` (`FGeTwoK4Statement`)

It is **not** proved here, and the hand proof of `NightF6.md` §2 has a gap. With
`t = π (σ c) = φ_B⁻¹ (σ c)` (link `μ, α, μ, A, α`), `f ≥ 2` is `x j ⇝ x (j+2)` in the
`{μ, B}`-graph of `t`, equivalently (Hex at the hole in `t`) `x (j+1)` reaches neither
`x (j+3)` nor `x (j+4)` in the `{α, A}`-graph of `t`. The note's closed walk
`h, x j, w₄, R, w₁, x (j+2)` is a `{μ, A}`-walk (it does exist in `t`: `R` is off-link and the
swaps touch only `{α, μ}` on the triple and `{α, B}` on `K_φ`). It shares the colour `A` with
the `{α, A}`-graph, so it separates nothing there. It only shows `x (j+1) ↛ x (j+3), x (j+4)` in
the `{α, B}`-graph of `t`, which is not the needed statement. What the argument does give: an
`{α, A}`-path of `t` from `x (j+1)` to `w₄` must pass through a `B`-vertex of `K_φ`. Otherwise it
would be an `{α, A}`-path of `c` joining `x j` to `x (j+2)`, against Lock 2. Closing the gap
needs the Lock 2 path of `c` rerouted off `K_φ`. That is a radius-unbounded Kempe statement and
is open here.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Private copies of the planar helpers of `QuarterRotationPlanar`

`rotation_nbrs`, `lock_separates` and the boundary-parity machinery of `kempe_hex` are private
in `QuarterRotationPlanar`; they are reproduced verbatim here (`NoFrozen` cannot be imported
alongside `QuarterRotation`). Both are stated for an arbitrary `Pent M.graph h`, so below they
are also applied with the centre a degree-five link vertex instead of the hole. -/

section copied
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} (P : Pent M.graph h)

section fin
private lemma fin5_a (j : Fin 5) : j + 2 + 1 = j + 3 ∧ j + 2 + 2 = j + 4 ∧ j + 3 + 1 = j + 4 ∧
    j + 3 + 2 = j ∧ j + 1 + 1 = j + 2 := by
  revert j; decide
end fin

private lemma Pent.ne (P : Pent M.graph h) {a b : Fin 5} (hab : a ≠ b) : P.x a ≠ P.x b :=
  fun e => hab (P.inj e)

private lemma Pent.h_ne (P : Pent M.graph h) (i : Fin 5) : h ≠ P.x i := (P.adj_h i).ne

/-- Walks inside three consecutive pentagon vertices. -/
private lemma Pent.walk3 (P : Pent M.graph h) (a : Fin 5) (u v : Fin n)
    (hu : u = P.x a ∨ u = P.x (a + 1) ∨ u = P.x (a + 2))
    (hv : v = P.x a ∨ v = P.x (a + 1) ∨ v = P.x (a + 2)) :
    ∃ q : M.graph.Walk u v,
      ∀ z ∈ q.support, z = P.x a ∨ z = P.x (a + 1) ∨ z = P.x (a + 2) := by
  have e1 : M.Adj (P.x a) (P.x (a + 1)) := P.adj_cyc a
  have e2 : M.Adj (P.x (a + 1)) (P.x (a + 2)) := by
    have := P.adj_cyc (a + 1); rwa [add_assoc] at this
  rcases hu with rfl | rfl | rfl <;> rcases hv with rfl | rfl | rfl
  · exact ⟨.nil, by simp⟩
  · exact ⟨e1.toWalk, by simp⟩
  · exact ⟨.cons e1 e2.toWalk, by simp⟩
  · exact ⟨e1.symm.toWalk, by simp⟩
  · exact ⟨.nil, by simp⟩
  · exact ⟨e2.toWalk, by simp⟩
  · exact ⟨.cons e2.symm e1.symm.toWalk, by simp⟩
  · exact ⟨e2.symm.toWalk, by simp⟩
  · exact ⟨.nil, by simp⟩

private lemma Pent.mem3 (P : Pent M.graph h) (a k : Fin 5) (u : Fin n) (hu : u = P.x k)
    (hk : k = a ∨ k = a + 1 ∨ k = a + 2) :
    u = P.x a ∨ u = P.x (a + 1) ∨ u = P.x (a + 2) := by
  subst hu; rcases hk with rfl | rfl | rfl <;> simp

/-- The two rotation neighbours of the dart `h → x (j+1)` are `x j` and `x (j+2)`. This is
forced by planarity: a pentagon edge from `x (j+1)` and a walk along the other three pentagon
vertices would otherwise be alternating at `h`. -/
private theorem rotation_nbrs (j : Fin 5) :
    ∃ (y1 y3 : Fin n) (h1 : M.Adj h y1) (h3 : M.Adj h y3),
      M.rotation.next ⟨(h, y1), h1⟩ = ⟨(h, P.x (j + 1)), P.adj_h _⟩ ∧
      M.rotation.next ⟨(h, P.x (j + 1)), P.adj_h _⟩ = ⟨(h, y3), h3⟩ ∧
      ((y1 = P.x j ∧ y3 = P.x (j + 2)) ∨ (y1 = P.x (j + 2) ∧ y3 = P.x j)) := by
  obtain ⟨f1, f2, f3, f4, f5⟩ := fin5_a j
  set D : M.Dart := ⟨(h, P.x (j + 1)), P.adj_h _⟩ with hD
  set d1 := M.rotation.next.symm D with hd1
  set d3 := M.rotation.next D with hd3
  have n1 : M.rotation.next d1 = D := Equiv.apply_symm_apply _ _
  have g1 : d1.fst = h := by
    have := M.rotation.next_fst d1; rw [n1] at this; exact this.symm
  have g3 : d3.fst = h := M.rotation.next_fst D
  have a1 : M.Adj h d1.snd := g1 ▸ d1.adj
  have a3 : M.Adj h d3.snd := g3 ▸ d3.adj
  have E1 : (⟨(h, d1.snd), a1⟩ : M.Dart) = d1 := Dart.ext _ _ (Prod.ext g1.symm rfl)
  have E3 : (⟨(h, d3.snd), a3⟩ : M.Dart) = d3 := Dart.ext _ _ (Prod.ext g3.symm rfl)
  -- the rotation at `h` is not trivial
  have nfix : M.rotation.next D ≠ D := by
    intro hfix
    obtain ⟨k, hk⟩ := M.rotation.cyclic D ⟨(h, P.x (j + 2)), P.adj_h _⟩ rfl
    rw [Function.iterate_fixed hfix] at hk
    exact P.ne (by simp) (congrArg (fun d : M.Dart => d.snd) hk)
  have s1 : d1.snd ≠ P.x (j + 1) := by
    intro e; apply nfix
    have : d1 = D := Dart.ext _ _ (Prod.ext g1 e)
    calc M.rotation.next D = M.rotation.next d1 := by rw [this]
      _ = D := n1
  have s3 : d3.snd ≠ P.x (j + 1) := by
    intro e; apply nfix
    exact Dart.ext _ _ (Prod.ext g3 e)
  obtain ⟨k1, hk1⟩ := P.only _ a1
  obtain ⟨k3, hk3⟩ := P.only _ a3
  have r12 : M.rotation.next ⟨(h, d1.snd), a1⟩ = D := by rw [E1]; exact n1
  have r23 : M.rotation.next D = ⟨(h, d3.snd), a3⟩ := E3.symm
  -- generic use of the separation lemma: an edge `v0 – x (j+1)` and a walk `q` disjoint from it
  have sep : ∀ (v0 : Fin n) (h0 : M.Adj h v0), v0 ≠ P.x (j + 1) → M.Adj v0 (P.x (j + 1)) →
      ∀ q : M.graph.Walk d1.snd d3.snd, h ∉ q.support →
        (∀ z ∈ q.support, z ≠ v0 ∧ z ≠ P.x (j + 1)) → False := by
    intro v0 h0 hne e q hq hqz
    obtain ⟨z, hzp, hzq⟩ := alternating_walks_intersect h0 a1 (P.adj_h (j + 1)) a3 hne r12 r23
      e.toWalk (by simp [h0.ne, (P.adj_h (j + 1)).ne]) q hq
    simp only [Adj.toWalk, Walk.support_cons, Walk.support_nil, List.mem_cons,
      List.not_mem_nil, or_false] at hzp
    rcases hzp with rfl | rfl
    · exact (hqz _ hzq).1 rfl
    · exact (hqz _ hzq).2 rfl
  have hqh : ∀ (a : Fin 5) {u v : Fin n} (q : M.graph.Walk u v),
      (∀ z ∈ q.support, z = P.x a ∨ z = P.x (a + 1) ∨ z = P.x (a + 2)) → h ∉ q.support := by
    intro a u v q hq hm
    rcases hq h hm with e | e | e <;> exact P.h_ne _ e
  -- Claim A: one of the rotation neighbours is `x j`
  have cA : d1.snd = P.x j ∨ d3.snd = P.x j := by
    by_contra hc
    push Not at hc
    have mem : ∀ k, d1.snd = P.x k ∨ d3.snd = P.x k → (k ≠ j ∧ k ≠ j + 1) := by
      intro k hk
      refine ⟨?_, ?_⟩ <;> rintro rfl
      · rcases hk with e | e
        · exact hc.1 e
        · exact hc.2 e
      · rcases hk with e | e
        · exact s1 e
        · exact s3 e
    have loc : ∀ k, k ≠ j ∧ k ≠ j + 1 → k = j + 2 ∨ k = j + 2 + 1 ∨ k = j + 2 + 2 := by
      intro k ⟨h1, h2⟩
      rw [f1, f2]
      rcases fin5_cases j k with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl h1
      · exact absurd rfl h2
      · exact Or.inl rfl
      · exact Or.inr (Or.inl rfl)
      · exact Or.inr (Or.inr rfl)
    obtain ⟨q, hq⟩ := P.walk3 (j + 2) _ _ (P.mem3 _ _ _ hk1 (loc _ (mem _ (Or.inl hk1))))
      (P.mem3 _ _ _ hk3 (loc _ (mem _ (Or.inr hk3))))
    refine sep (P.x j) (P.adj_h j) (P.ne (by simp)) (P.adj_cyc j) _ (hqh _ _ hq) ?_
    intro z hz
    rw [f1, f2] at hq
    rcases hq z hz with rfl | rfl | rfl <;> exact ⟨P.ne (by simp), P.ne (by simp)⟩
  -- Claim B: one of the rotation neighbours is `x (j+2)`
  have cB : d1.snd = P.x (j + 2) ∨ d3.snd = P.x (j + 2) := by
    by_contra hc
    push Not at hc
    have mem : ∀ k, d1.snd = P.x k ∨ d3.snd = P.x k → (k ≠ j + 2 ∧ k ≠ j + 1) := by
      intro k hk
      refine ⟨?_, ?_⟩ <;> rintro rfl
      · rcases hk with e | e
        · exact hc.1 e
        · exact hc.2 e
      · rcases hk with e | e
        · exact s1 e
        · exact s3 e
    have loc : ∀ k, k ≠ j + 2 ∧ k ≠ j + 1 → k = j + 3 ∨ k = j + 3 + 1 ∨ k = j + 3 + 2 := by
      intro k ⟨h1, h2⟩
      rw [f3, f4]
      rcases fin5_cases j k with rfl | rfl | rfl | rfl | rfl
      · exact Or.inr (Or.inr rfl)
      · exact absurd rfl h2
      · exact absurd rfl h1
      · exact Or.inl rfl
      · exact Or.inr (Or.inl rfl)
    obtain ⟨q, hq⟩ := P.walk3 (j + 3) _ _ (P.mem3 _ _ _ hk1 (loc _ (mem _ (Or.inl hk1))))
      (P.mem3 _ _ _ hk3 (loc _ (mem _ (Or.inr hk3))))
    have e : M.Adj (P.x (j + 2)) (P.x (j + 1)) := by
      have := P.adj_cyc (j + 1); rw [f5] at this; exact this.symm
    refine sep (P.x (j + 2)) (P.adj_h _) (P.ne (by simp)) e _ (hqh _ _ hq) ?_
    intro z hz
    rw [f3, f4] at hq
    rcases hq z hz with rfl | rfl | rfl <;> exact ⟨P.ne (by simp), P.ne (by simp)⟩
  refine ⟨d1.snd, d3.snd, a1, a3, r12, r23, ?_⟩
  have hj2 : P.x j ≠ P.x (j + 2) := P.ne (by simp)
  rcases cA with e1 | e1 <;> rcases cB with e2 | e2
  · exact absurd (e1.symm.trans e2) hj2
  · exact Or.inl ⟨e1, e2⟩
  · exact Or.inr ⟨e2, e1⟩
  · exact absurd (e1.symm.trans e2) hj2

/-- **Jordan separation at the hole.** A walk from a neighbour `v0 ≠ x (j+1)` of `h` to
`x (j+1)` and a walk from `x j` to `x (j+2)`, both avoiding `h`, meet. -/
private theorem lock_separates (j : Fin 5) {v0 : Fin n} (h0 : M.Adj h v0) (hne : v0 ≠ P.x (j + 1))
    (p : M.graph.Walk v0 (P.x (j + 1))) (hp : h ∉ p.support)
    (q : M.graph.Walk (P.x j) (P.x (j + 2))) (hq : h ∉ q.support) :
    ∃ z, z ∈ p.support ∧ z ∈ q.support := by
  obtain ⟨y1, y3, a1, a3, r12, r23, hy⟩ := rotation_nbrs P j
  rcases hy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact alternating_walks_intersect h0 a1 (P.adj_h _) a3 hne r12 r23 p hp q hq
  · obtain ⟨z, h1, h2⟩ :=
      alternating_walks_intersect h0 a1 (P.adj_h _) a3 hne r12 r23 p hp q.reverse
        (by rwa [Walk.support_reverse, List.mem_reverse])
    exact ⟨z, h1, by rwa [Walk.support_reverse, List.mem_reverse] at h2⟩

section pair
variable {G : SimpleGraph (Fin n)}

/-- Every vertex of a walk in a two-colour graph is active, or the walk is a trivial
loop at its start. -/
private lemma support_active {c : Fin n → Fin 4} {a b : Fin 4} {u v : Fin n}
    (p : (pairGraph G h c a b).Walk u v) :
    ∀ z ∈ p.support, Active h c a b z ∨ (z = u ∧ z = v) := by
  induction p with
  | nil => intro z hz; simp at hz; exact Or.inr ⟨hz, hz⟩
  | cons e p ih =>
    intro z hz
    rw [Walk.support_cons, List.mem_cons] at hz
    rcases hz with rfl | hz
    · exact Or.inl e.2.1
    · rcases ih z hz with hz' | ⟨rfl, -⟩
      · exact Or.inl hz'
      · exact Or.inl e.2.2

private lemma pairGraph_le (c : Fin n → Fin 4) (a b : Fin 4) : pairGraph G h c a b ≤ G :=
  fun _ _ e => e.1


end pair

section hex

/-- The face of a dart (a triangle, on a triangulated map) meets `S`. -/
private def TriMeets (M : SphericalMap n) (S : Fin n → Prop) (d : M.Dart) : Prop :=
  S d.fst ∨ S d.snd ∨ S (M.rotation.faceNext d).snd

private lemma tri3 (htri : M.Triangulated) (d : M.Dart) :
    M.rotation.faceNext (M.rotation.faceNext (M.rotation.faceNext d)) = d := by
  have := M.rotation.face_next_iterate_length d
  rw [htri d] at this
  simpa only [Function.iterate_succ_apply', Function.iterate_zero_apply] using this

private lemma triMeets_faceNext (htri : M.Triangulated) (S : Fin n → Prop) (d : M.Dart) :
    TriMeets M S (M.rotation.faceNext d) ↔ TriMeets M S d := by
  have h1 : (M.rotation.faceNext d).fst = d.snd := M.rotation.face_next_fst d
  have h2 : (M.rotation.faceNext (M.rotation.faceNext d)).snd = d.fst := by
    have := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
    rw [tri3 htri d] at this
    exact this.symm
  unfold TriMeets
  rw [h1, h2]
  tauto

private lemma triMeets_symm (htri : M.Triangulated) (S : Fin n → Prop) (d : M.Dart) :
    TriMeets M S d.symm ↔ TriMeets M S (M.rotation.next d) := by
  rw [← triMeets_faceNext htri S d.symm, RotationSystem.face_next_apply, Dart.symm_symm]

/-- The third vertex of a triangle meeting `S` at neither end of the dart. -/
private lemma triMeets_apex (htri : M.Triangulated) {S : Fin n → Prop} {d : M.Dart}
    (hd : TriMeets M S d) (h1 : ¬ S d.fst) (h2 : ¬ S d.snd) :
    ∃ w, S w ∧ M.Adj d.fst w ∧ M.Adj d.snd w := by
  set e := M.rotation.faceNext d
  have he : e.fst = d.snd := M.rotation.face_next_fst d
  have e2 : (M.rotation.faceNext e).fst = e.snd := M.rotation.face_next_fst e
  have e3 : (M.rotation.faceNext e).snd = d.fst := by
    have := M.rotation.face_next_fst (M.rotation.faceNext e)
    rw [tri3 htri d] at this
    exact this.symm
  refine ⟨e.snd, ?_, ?_, ?_⟩
  · rcases hd with h | h | h
    · exact absurd h h1
    · exact absurd h h2
    · exact h
  · have := (M.rotation.faceNext e).adj
    rw [e2, e3] at this
    exact this.symm
  · have := e.adj
    rwa [he] at this

/-- Edges separating a face meeting `S` from one missing it. -/
private def bdGraph (M : SphericalMap n) (S : Fin n → Prop) : SimpleGraph (Fin n) where
  Adj u v := ∃ huv : M.Adj u v,
    ¬ (TriMeets M S ⟨(u, v), huv⟩ ↔ TriMeets M S ⟨(v, u), huv.symm⟩)
  symm := ⟨fun _ _ ⟨e, hb⟩ => ⟨e.symm, fun hh => hb hh.symm⟩⟩
  loopless := ⟨fun _ ⟨e, _⟩ => e.ne rfl⟩

private lemma bdGraph_out (htri : M.Triangulated) {S : Fin n → Prop} {u v : Fin n}
    (huv : (bdGraph M S).Adj u v) :
    ¬ S u ∧ ∃ w, S w ∧ M.Adj u w := by
  obtain ⟨e, hb⟩ := huv
  by_cases ht : TriMeets M S ⟨(u, v), e⟩
  · have hf : ¬ TriMeets M S ⟨(v, u), e.symm⟩ := fun hf => hb ⟨fun _ => hf, fun _ => ht⟩
    have hu : ¬ S u := fun hs => hf (Or.inr (Or.inl hs))
    have hv : ¬ S v := fun hs => hf (Or.inl hs)
    obtain ⟨w, hw, h1, -⟩ := triMeets_apex htri ht hu hv
    exact ⟨hu, w, hw, h1⟩
  · have ht' : TriMeets M S ⟨(v, u), e.symm⟩ := by
      by_contra hf; exact hb ⟨fun h => absurd h ht, fun h => absurd h hf⟩
    have hu : ¬ S u := fun hs => ht (Or.inl hs)
    have hv : ¬ S v := fun hs => ht (Or.inr (Or.inl hs))
    obtain ⟨w, hw, -, h2⟩ := triMeets_apex htri ht' hv hu
    exact ⟨hu, w, hw, h2⟩

private lemma zmod2_ite_xor (p q : Prop) [Decidable p] [Decidable q] :
    (if ¬ (p ↔ q) then (1 : ZMod 2) else 0) = (if p then 1 else 0) + (if q then 1 else 0) := by
  by_cases hp : p <;> by_cases hq : q <;> simp [hp, hq]; decide

open Classical in
/-- Every vertex has even degree in the boundary graph. -/
private lemma bdGraph_even (htri : M.Triangulated) (S : Fin n → Prop) (x : Fin n) :
    Even ((bdGraph M S).degree x) := by
  classical
  have hcard : Fintype.card {d : M.Dart // d.fst = x ∧
      ¬ (TriMeets M S d ↔ TriMeets M S d.symm)} = (bdGraph M S).degree x := by
    rw [← card_neighborSet_eq_degree]
    refine Fintype.card_of_bijective (f := fun d => ⟨d.1.snd, by
      obtain ⟨⟨⟨u, v⟩, huv⟩, hu, hb⟩ := d
      subst hu
      exact ⟨huv, hb⟩⟩) ⟨?_, ?_⟩
    · rintro ⟨d1, h1, h1'⟩ ⟨d2, h2, h2'⟩ he
      apply Subtype.ext
      apply Dart.ext
      exact Prod.ext (h1.trans h2.symm) (congrArg Subtype.val he)
    · rintro ⟨w, huv, hb⟩
      exact ⟨⟨⟨(x, w), huv⟩, rfl, hb⟩, rfl⟩
  rw [← hcard, ← ZMod.natCast_eq_zero_iff_even, Fintype.card_subtype,
    Finset.natCast_card_filter]
  have hsplit : ∀ d : M.Dart,
      (if d.fst = x ∧ ¬ (TriMeets M S d ↔ TriMeets M S d.symm) then (1 : ZMod 2) else 0) =
        (if d.fst = x ∧ TriMeets M S d then 1 else 0) +
          (if (M.rotation.next d).fst = x ∧ TriMeets M S (M.rotation.next d) then 1 else 0) := by
    intro d
    rw [M.rotation.next_fst, ← triMeets_symm htri]
    by_cases hx : d.fst = x
    · simp only [hx, true_and]
      exact zmod2_ite_xor _ _
    · simp [hx]
  rw [Finset.sum_congr rfl (fun d _ => hsplit d), Finset.sum_add_distrib,
    Equiv.sum_comp M.rotation.next
      (fun d => if d.fst = x ∧ TriMeets M S d then (1 : ZMod 2) else 0)]
  exact CharTwo.add_self_eq_zero _


/-- `G` with all edges at `h` removed. -/
private def offV (G : SimpleGraph (Fin n)) (h : Fin n) : SimpleGraph (Fin n) where
  Adj u v := G.Adj u v ∧ u ≠ h ∧ v ≠ h
  symm := ⟨fun _ _ ⟨e, a, b⟩ => ⟨e.symm, b, a⟩⟩
  loopless := ⟨fun _ ⟨e, _⟩ => e.ne rfl⟩

/-- `G` restricted to the component of `m`. -/
private def compKeep (G : SimpleGraph (Fin n)) (m : Fin n) : SimpleGraph (Fin n) where
  Adj u v := G.Adj u v ∧ G.Reachable m u
  symm := ⟨fun _ _ ⟨e, r⟩ => ⟨e.symm, r.trans e.reachable⟩⟩
  loopless := ⟨fun _ ⟨e, _⟩ => e.ne rfl⟩

open Classical in
/-- Handshake bookkeeping: in an even graph with the edges at `h` removed, the odd vertices
of the component of `m` are the reachable neighbours of `h`. -/
private lemma odd_iff_bd (G : SimpleGraph (Fin n)) (hev : ∀ x, Even (G.degree x))
    (h m w : Fin n) :
    Odd ((compKeep (offV G h) m).degree w) ↔ (offV G h).Reachable m w ∧ w ≠ h ∧ G.Adj w h := by
  have key : (compKeep (offV G h) m).degree w =
      if (offV G h).Reachable m w ∧ w ≠ h then ((G.neighborFinset w).erase h).card else 0 := by
    rw [← card_neighborFinset_eq_degree]
    split_ifs with hw
    · congr 1
      ext v
      rw [mem_neighborFinset, Finset.mem_erase, mem_neighborFinset]
      simp only [compKeep, offV]
      exact ⟨fun ⟨⟨e, _, hv⟩, _⟩ => ⟨hv, e⟩, fun ⟨hv, e⟩ => ⟨⟨e, hw.2, hv⟩, hw.1⟩⟩
    · rw [Finset.card_eq_zero]
      ext v
      rw [mem_neighborFinset]
      simp only [compKeep, offV, Finset.notMem_empty, iff_false]
      exact fun ⟨⟨_, hwh, _⟩, hr⟩ => hw ⟨hr, hwh⟩
  rw [key]
  split_ifs with hw
  · by_cases ha : G.Adj w h
    · rw [Finset.card_erase_of_mem (mem_neighborFinset _ _ _ |>.2 ha),
        card_neighborFinset_eq_degree]
      refine ⟨fun _ => ⟨hw.1, hw.2, ha⟩, fun _ => Nat.Even.sub_odd ?_ (hev w) odd_one⟩
      rw [← card_neighborFinset_eq_degree]
      exact Finset.card_pos.2 ⟨h, (mem_neighborFinset _ _ _).2 ha⟩
    · rw [Finset.erase_eq_of_notMem (fun hm => ha ((mem_neighborFinset _ _ _).1 hm)),
        card_neighborFinset_eq_degree]
      exact ⟨fun ho => absurd (hev w) (Nat.not_even_iff_odd.2 ho), fun ⟨_, _, e⟩ => absurd e ha⟩
  · exact ⟨fun ho => absurd ho (by decide), fun ⟨a, b, _⟩ => absurd ⟨a, b⟩ hw⟩

open Classical in
/-- Boundary edges at the hole: the edge `x (k+1) – h` separates the two faces
`h x k x (k+1)` and `h x (k+1) x (k+2)`. -/
private lemma bd_link (htri : M.Triangulated) {S : Fin n → Prop} (hSh : ¬ S h) (k : Fin 5) :
    (bdGraph M S).Adj (P.x (k + 1)) h ↔
      ¬ ((S (P.x (k + 1)) ∨ S (P.x k)) ↔ (S (P.x (k + 1)) ∨ S (P.x (k + 2)))) := by
  obtain ⟨y1, y3, a1, a3, r12, r23, hy⟩ := rotation_nbrs P k
  have hyh : M.Adj (P.x (k + 1)) h := (P.adj_h (k + 1)).symm
  have t1 : TriMeets M S ⟨(P.x (k + 1), h), hyh⟩ ↔ S (P.x (k + 1)) ∨ S y3 := by
    have hf : M.rotation.faceNext ⟨(P.x (k + 1), h), hyh⟩ = ⟨(h, y3), a3⟩ := r23
    show S (P.x (k + 1)) ∨ S h ∨ S (M.rotation.faceNext ⟨(P.x (k + 1), h), hyh⟩).snd ↔ _
    rw [hf]
    tauto
  have t2 : TriMeets M S ⟨(h, P.x (k + 1)), hyh.symm⟩ ↔ S (P.x (k + 1)) ∨ S y1 := by
    set e := M.rotation.faceNext ⟨(h, P.x (k + 1)), hyh.symm⟩
    have hn : M.rotation.next (M.rotation.faceNext e).symm = ⟨(h, P.x (k + 1)), hyh.symm⟩ := by
      rw [← RotationSystem.face_next_apply]
      exact tri3 htri _
    have hs : (M.rotation.faceNext e).symm = ⟨(h, y1), a1⟩ :=
      M.rotation.next.injective (hn.trans r12.symm)
    have hsnd : e.snd = y1 :=
      (M.rotation.face_next_fst e).symm.trans (congrArg (fun d : M.Dart => d.snd) hs)
    show S h ∨ S (P.x (k + 1)) ∨ S e.snd ↔ _
    rw [hsnd]
    tauto
  constructor
  · rintro ⟨e, hb⟩
    have hb' : ¬ (TriMeets M S ⟨(P.x (k + 1), h), hyh⟩ ↔
        TriMeets M S ⟨(h, P.x (k + 1)), hyh.symm⟩) := hb
    rw [t1, t2] at hb'
    rcases hy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> tauto
  · intro hc
    refine ⟨hyh, ?_⟩
    change ¬ (TriMeets M S ⟨(P.x (k + 1), h), hyh⟩ ↔
        TriMeets M S ⟨(h, P.x (k + 1)), hyh.symm⟩)
    rw [t1, t2]
    rcases hy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> tauto

private lemma fin5_b (j : Fin 5) : j + 4 + 1 = j ∧ j + 4 + 2 = j + 1 ∧ j + 1 + 1 = j + 2 ∧
    j + 1 + 2 = j + 3 ∧ j + 2 + 1 = j + 3 ∧ j + 2 + 2 = j + 4 := by
  revert j; decide

private lemma fin4_rest (a m A B u : Fin 4) (h1 : m ≠ a) (h2 : A ≠ a) (h3 : B ≠ a) (h4 : m ≠ A)
    (h5 : m ≠ B) (h6 : A ≠ B) (hu1 : u ≠ a) (hu2 : u ≠ A) : u = m ∨ u = B := by
  revert a m A B u; decide

end hex

end copied

/-! ### Generic tools -/

section generic
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

private lemma support_pred {H : SimpleGraph (Fin n)} {Q : Fin n → Prop}
    (hQ : ∀ u v, H.Adj u v → Q v) :
    ∀ {s t : Fin n} (p : H.Walk s t), Q s → ∀ z ∈ p.support, Q z
  | _, _, .nil, hs, z, hz => by
      rw [Walk.support_nil, List.mem_singleton] at hz
      exact hz ▸ hs
  | _, _, .cons e p, hs, z, hz => by
      rw [Walk.support_cons, List.mem_cons] at hz
      rcases hz with rfl | hz
      · exact hs
      · exact support_pred hQ p (hQ _ _ e) z hz

/-- A reachability in a subgraph of `M.graph` whose edges end in `Q` gives a walk of
`M.graph` inside `Q`. -/
private lemma walk_of_reach {H : SimpleGraph (Fin n)} (hle : H ≤ M.graph) {Q : Fin n → Prop}
    (hQ : ∀ u v, H.Adj u v → Q v) {s t : Fin n} (hs : Q s) (r : H.Reachable s t) :
    ∃ p : M.graph.Walk s t, ∀ z ∈ p.support, Q z := by
  obtain ⟨p⟩ := r
  refine ⟨p.mapLe hle, fun z hz => ?_⟩
  rw [Walk.support_mapLe_eq_support] at hz
  exact support_pred hQ p hs z hz

private lemma walk_avoid {G1 H : SimpleGraph (Fin n)} {z : Fin n}
    (hH : ∀ u v, G1.Adj u v → u ≠ z → v ≠ z → H.Adj u v) :
    ∀ {a b : Fin n} (q : G1.Walk a b), z ∉ q.support → H.Reachable a b
  | _, _, .nil, _ => Reachable.refl _
  | _, _, .cons e q, hz => by
      rw [Walk.support_cons, List.mem_cons, not_or] at hz
      refine (hH _ _ e (Ne.symm hz.1) fun h' => hz.2 ?_).reachable.trans (walk_avoid hH q hz.2)
      rw [← h']
      exact q.start_mem_support

/-- A path out of `z` whose only first step is `y` gives a walk from `y` avoiding `z`. -/
private lemma path_tail {G1 H : SimpleGraph (Fin n)} {z y t : Fin n}
    (hy : ∀ v, G1.Adj z v → v = y)
    (hH : ∀ u v, G1.Adj u v → u ≠ z → v ≠ z → H.Adj u v) (hzt : z ≠ t)
    (q : G1.Walk z t) (hq : q.IsPath) : H.Reachable y t := by
  cases q with
  | nil => exact absurd rfl hzt
  | cons e q =>
    obtain rfl := hy _ e
    exact walk_avoid hH q ((Walk.cons_isPath_iff _ _).1 hq).2

/-- A degree-five vertex `z` whose neighbours `a, b, d, e, f` form a 5-cycle in this order is a
pentagonal "hole" (`Pent`) in its own right. -/
private lemma pent5 {z a b d e f : Fin n}
    (hn : ∀ u, M.graph.Adj z u ↔ u = a ∨ u = b ∨ u = d ∨ u = e ∨ u = f)
    (ab : M.graph.Adj a b) (bd : M.graph.Adj b d) (de : M.graph.Adj d e)
    (ef : M.graph.Adj e f) (fa : M.graph.Adj f a)
    (hab : a ≠ b) (had : a ≠ d) (hae : a ≠ e) (haf : a ≠ f) (hbd : b ≠ d) (hbe : b ≠ e)
    (hbf : b ≠ f) (hde : d ≠ e) (hdf : d ≠ f) (hef : e ≠ f) :
    ∃ Q : Pent M.graph z, Q.x = ![a, b, d, e, f] := by
  refine ⟨⟨![a, b, d, e, f], fun i => ?_, fun i => ?_, fun i k hik => ?_, fun v hv => ?_⟩, rfl⟩
  · fin_cases i <;> simp [hn]
  · fin_cases i <;> simpa
  · fin_cases i <;> fin_cases k <;> simp at hik ⊢ <;>
      first | exact absurd hik ‹_› | exact absurd hik.symm ‹_›
  · rcases (hn v).1 hv with rfl | rfl | rfl | rfl | rfl
    exacts [⟨0, rfl⟩, ⟨1, rfl⟩, ⟨2, rfl⟩, ⟨3, rfl⟩, ⟨4, rfl⟩]

/-- **Jordan separation at a degree-five vertex** `z` with cyclic neighbours
`h, s, y₂, y₃, y₄`: a walk `y₄ → y₂` inside `X` and a walk `s → y₃` inside `Y`, both
avoiding `z`, cannot exist when `X` and `Y` are disjoint. -/
private lemma sep_core {z s y2 y3 y4 : Fin n} (Q : Pent M.graph z)
    (hQ : Q.x = ![h, s, y2, y3, y4]) {X Y : Fin n → Prop} (hXY : ∀ v, X v → Y v → False)
    (p : M.graph.Walk y4 y2) (hp : ∀ v ∈ p.support, X v) (hpz : ¬ X z)
    (q : M.graph.Walk s y3) (hq : ∀ v ∈ q.support, Y v) (hqz : ¬ Y z) : False := by
  have e1 : Q.x 1 = s := by rw [hQ]; rfl
  have e2 : Q.x (1 + 1) = y2 := by rw [hQ]; rfl
  have e3 : Q.x (1 + 2) = y3 := by rw [hQ]; rfl
  have e4 : Q.x 4 = y4 := by rw [hQ]; rfl
  have a4 : M.Adj z y4 := e4 ▸ Q.adj_h 4
  have hne : y4 ≠ Q.x (1 + 1) := fun e => absurd (Q.inj (e4.trans e)) (by decide)
  obtain ⟨v, hv1, hv2⟩ := lock_separates Q 1 a4 hne (p.copy rfl e2.symm)
    (by rw [Walk.support_copy]; exact fun hz => hpz (hp z hz)) (q.copy e1.symm e3.symm)
    (by rw [Walk.support_copy]; exact fun hz => hqz (hq z hz))
  rw [Walk.support_copy] at hv1 hv2
  exact hXY v (hp v hv1) (hq v hv2)

/-- The boundary edges at the two "far" spokes of a degree-five vertex `z` with cyclic
neighbours `a, b, d, e, f`. -/
private lemma bd_pent (htri : M.Triangulated) {S : Fin n → Prop} {z a b d e f : Fin n}
    (Q : Pent M.graph z) (hQ : Q.x = ![a, b, d, e, f]) (hSz : ¬ S z) :
    ((bdGraph M S).Adj e z ↔ ¬ ((S e ∨ S d) ↔ (S e ∨ S f))) ∧
      ((bdGraph M S).Adj f z ↔ ¬ ((S f ∨ S e) ↔ (S f ∨ S a))) := by
  have b2 := bd_link Q htri hSz 2
  have b3 := bd_link Q htri hSz 3
  rw [hQ] at b2 b3
  exact ⟨b2, b3⟩

open Classical in
/-- **Hex at the hole, rerouted.** Let `S` be any vertex set missing `h`. If, among the link
vertices, exactly `z` and `t` carry boundary edges to `h`, and `y` is the only boundary
neighbour of `z` other than `h`, then `y` reaches `t` through boundary edges avoiding `h` and
`z` (handshake lemma in the boundary graph, which has even degrees on a triangulation). -/
private lemma hex_core (htri : M.Triangulated) (P : Pent M.graph h) {S : Fin n → Prop}
    {z t y : Fin n} (hzh : z ≠ h) (hzt : z ≠ t) (hz : (bdGraph M S).Adj z h)
    (honly : ∀ i, (bdGraph M S).Adj (P.x i) h → P.x i = z ∨ P.x i = t)
    (hy : ∀ v, (bdGraph M S).Adj z v → v ≠ h → v = y)
    {H : SimpleGraph (Fin n)}
    (hH : ∀ u v, (bdGraph M S).Adj u v → u ≠ h → v ≠ h → u ≠ z → v ≠ z → H.Adj u v) :
    H.Reachable y t := by
  have hev := bdGraph_even htri S
  have hm : Odd ((compKeep (offV (bdGraph M S) h) z).degree z) := by
    rw [odd_iff_bd _ hev]
    exact ⟨Reachable.refl _, hzh, hz⟩
  obtain ⟨w, hwz, hw⟩ := exists_ne_odd_degree_of_exists_odd_degree (h := hm)
  rw [odd_iff_bd _ hev] at hw
  obtain ⟨hreach, -, hadj⟩ := hw
  obtain ⟨i, rfl⟩ := P.only w hadj.fst.symm
  rw [(honly i hadj).resolve_left hwz] at hreach
  obtain ⟨p⟩ := hreach
  exact path_tail (G1 := offV (bdGraph M S) h) (fun v e => hy v e.1 e.2.2)
    (fun u v e hu hv => hH u v e.1 e.2.1 e.2.2 hu hv) hzt p.bypass p.bypass_isPath

end generic

/-! ### The duality (D) at `k = 4` and `k = 3` -/

private lemma iff_ff {p q r s : Prop} (hp : ¬ p) (hq : ¬ q) (hr : ¬ r) (hs : ¬ s) :
    (p ∨ q) ↔ (r ∨ s) :=
  ⟨fun hh => hh.elim (absurd · hp) (absurd · hq), fun hh => hh.elim (absurd · hr) (absurd · hs)⟩

private lemma iff_of_both {p q r s : Prop} (a : p ∨ q) (b : r ∨ s) : (p ∨ q) ↔ (r ∨ s) :=
  ⟨fun _ => b, fun _ => a⟩

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {c : Fin n → Fin 4} {j : Fin 5}

/-- The Kempe set of `x (j+1)` in the pair `{a, b}` lies in the active vertices. -/
private lemma comp_active {a b : Fin 4} (ha : c (P.x (j + 1)) = a ∨ c (P.x (j + 1)) = b)
    {v : Fin n} (hv : (pairGraph M.graph h c a b).Reachable (P.x (j + 1)) v) :
    Active h c a b v := by
  by_cases e : P.x (j + 1) = v
  · exact e ▸ ⟨P.x_ne_h _, ha⟩
  · exact reach_active hv e

/-- A vertex outside the `{a, b}`-component of `x (j+1)` but next to it, and not `h`, has a
colour outside `{a, b}`. -/
private lemma comp_nbr {a b : Fin 4} (ha : c (P.x (j + 1)) = a ∨ c (P.x (j + 1)) = b)
    {u : Fin n} (hu : u ≠ h)
    (hnS : ¬ (pairGraph M.graph h c a b).Reachable (P.x (j + 1)) u)
    (hw : ∃ v, (pairGraph M.graph h c a b).Reachable (P.x (j + 1)) v ∧ M.Adj u v) :
    c u ≠ a ∧ c u ≠ b := by
  obtain ⟨v, hv, e⟩ := hw
  exact ⟨fun hc => hnS (hv.trans (Adj.reachable ⟨e.symm, comp_active ha hv, hu, Or.inl hc⟩)),
    fun hc => hnS (hv.trans (Adj.reachable ⟨e.symm, comp_active ha hv, hu, Or.inr hc⟩))⟩

/-- **(D) at `k = 4`, "not both" (Kempe separation, no triangulation needed).** The
`{α, B}`-walk `x (j+4), m, …, w₀` (with `x j` deleted) and the `{μ, A}`-walk `x (j+1), …, w₄`
are separated at `x j`, whose rotation is `h, x (j+1), w₀, w₄, x (j+4)`. -/
theorem not_both_k4 (K : K4Ball P w m j) (hc : ProperOff M.graph h c) (hR : R3At P w c j)
    (hB : (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)).Reachable (w j) m)
    (hA : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 1))
      (w (j + 4))) : False := by
  have T := K.tri
  have cm := m_col_k4 K hc hR
  obtain ⟨⟨⟨-, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -⟩ := hR
  obtain ⟨o4, o0, -, -⟩ := T.offh
  obtain ⟨-, -, a10, -, -, -⟩ := T.adjs
  obtain ⟨Q, hQ⟩ := pent5 (z := P.x j) (a := h) (b := P.x (j + 1)) (d := w j) (e := w (j + 4))
    (f := P.x (j + 4)) (fun u => (T.nbr0 u).trans (by tauto)) (P.adj_h _) a10 T.ring40.symm
    T.adj4.symm (P.adj_h _).symm (P.x_ne_h _).symm o0.symm o4.symm (P.x_ne_h _).symm
    (T.off _).2.1.symm (T.off _).1.symm (fun e => absurd (P.inj e) (by simp))
    T.ring40.ne.symm (T.off _).2.1 (T.off _).1
  -- the `{α, B}`-walk `x (j+4) → w₀`
  obtain ⟨r, hr⟩ := walk_of_reach (M := M)
    (H := pairDel M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)) (fun u v e => e.1.1)
    (Q := fun v => v ≠ P.x j ∧ Active h c (c (P.x j)) (c (P.x (j + 4))) v)
    (fun u v e => ⟨e.2.2, e.1.2.2⟩) ⟨K.offm j, K.offh.2, Or.inl cm⟩ hB.symm
  have a4m : M.Adj (P.x (j + 4)) m := (K.nbr4 m).2 (by simp)
  -- the `{μ, A}`-walk `x (j+1) → w₄`
  obtain ⟨q, hq⟩ := walk_of_reach (M := M)
    (H := pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))) (fun u v e => e.1)
    (Q := Active h c (c (P.x (j + 1))) (c (P.x (j + 3)))) (fun u v e => e.2.2)
    ⟨P.x_ne_h _, Or.inl rfl⟩ hA
  refine sep_core Q hQ (X := fun v => v ≠ P.x j ∧ Active h c (c (P.x j)) (c (P.x (j + 4))) v)
    (Y := Active h c (c (P.x (j + 1))) (c (P.x (j + 3)))) ?_ (.cons a4m r) ?_ (fun H => H.1 rfl)
    q hq ?_
  · rintro v ⟨-, -, e | e⟩ ⟨-, f | f⟩
    · exact h1 (f.symm.trans e)
    · exact h3 (f.symm.trans e)
    · exact h14 (f.symm.trans e)
    · exact h34 (f.symm.trans e)
  · intro v hv
    rw [Walk.support_cons, List.mem_cons] at hv
    rcases hv with rfl | hv
    · exact ⟨fun e => absurd (P.inj e) (by simp), P.x_ne_h _, Or.inr rfl⟩
    · exact hr v hv
  · rintro ⟨-, e | e⟩
    · exact h1 e.symm
    · exact h3 e.symm

/-- **(D) at `k = 4`.** On a triangulated sphere, `w₀` reaches `m` in the `{α, B}`-graph with
`x j` deleted iff `w₄` is **not** in the `{μ, A}`-component of `x (j+1)`. "Not both" is
`not_both_k4`; "at least one" is the boundary-parity (Hex) argument of `kempe_hex`, run with
`S` the `{μ, A}`-component of `x (j+1)` and rerouted at the degree-five vertex `x j`: the only
boundary edges at `h` go to `x j` and `x (j+4)` (`x (j+3) ∈ S` by Lock 1), and the only other
boundary edge at `x j` goes to `w₀` (`w₄ ∉ S`). -/
theorem duality_k4 (htri : M.Triangulated) (K : K4Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)).Reachable (w j) m ↔
      ¬ (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 1))
        (w (j + 4)) := by
  refine ⟨fun hB hA => not_both_k4 K hc hR hB hA, fun hn => ?_⟩
  refine (lock2_after_sigma_k4 K hc hR).1 ((lock2_after_sigma_iff K.tri hc hR.1.1 hR.outer).2 ?_)
  have T := K.tri
  have hL1 := hR.1.2.1
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -, -⟩, e0, -, -, -, e4⟩ := hR
  obtain ⟨o4, o0, -, -⟩ := T.offh
  obtain ⟨-, -, a10, -, -, -⟩ := T.adjs
  obtain ⟨g1, g2, g3, g4, g5, g6⟩ := fin5_b j
  set S : Fin n → Prop :=
    fun v => (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 1)) v
    with hS
  have act : ∀ {v}, S v → Active h c (c (P.x (j + 1))) (c (P.x (j + 3))) v :=
    comp_active (Or.inl rfl)
  have notS : ∀ {v}, (c v = c (P.x j) ∨ c v = c (P.x (j + 4))) → ¬ S v := by
    rintro v (e | e) hv
    · rcases (act hv).2 with f | f
      · exact h1 (f.symm.trans e)
      · exact h3 (f.symm.trans e)
    · rcases (act hv).2 with f | f
      · exact h14 (f.symm.trans e)
      · exact h34 (f.symm.trans e)
  have hSh : ¬ S h := fun hv => (act hv).1 rfl
  have S1 : S (P.x (j + 1)) := Reachable.refl _
  have S3 : S (P.x (j + 3)) := hL1
  have nS0 : ¬ S (P.x j) := notS (Or.inl rfl)
  have nS2 : ¬ S (P.x (j + 2)) := notS (Or.inl h02.symm)
  have nS4 : ¬ S (P.x (j + 4)) := notS (Or.inr rfl)
  have nSw0 : ¬ S (w j) := notS (Or.inr e0)
  have nSw4 : ¬ S (w (j + 4)) := hn
  obtain ⟨Q, hQ⟩ := pent5 (z := P.x j) (a := h) (b := P.x (j + 1)) (d := w j) (e := w (j + 4))
    (f := P.x (j + 4)) (fun u => (T.nbr0 u).trans (by tauto)) (P.adj_h _) a10 T.ring40.symm
    T.adj4.symm (P.adj_h _).symm (P.x_ne_h _).symm o0.symm o4.symm (P.x_ne_h _).symm
    (T.off _).2.1.symm (T.off _).1.symm (fun e => absurd (P.inj e) (by simp))
    T.ring40.ne.symm (T.off _).2.1 (T.off _).1
  obtain ⟨bw4, bx4⟩ := bd_pent htri Q hQ nS0
  refine hex_core htri P (S := S) (z := P.x j) (t := P.x (j + 4)) (y := w j) (P.x_ne_h _)
    (fun e => absurd (P.inj e) (by simp)) ?_ ?_ ?_ ?_
  · have b := bd_link P htri hSh (j + 4)
    rw [g1, g2] at b
    exact b.2 fun hh => (hh.2 (Or.inr S1)).elim nS0 nS4
  · intro i hb
    rcases fin5_cases j i with e | e | e | e | e <;> rw [e] at hb ⊢
    · exact Or.inl rfl
    · exact absurd (iff_of_both (Or.inl S1) (Or.inl S1)) ((bd_link P htri hSh j).1 hb)
    · have b := bd_link P htri hSh (j + 1)
      rw [g3, g4] at b
      exact absurd (iff_of_both (Or.inr S1) (Or.inr S3)) (b.1 hb)
    · have b := bd_link P htri hSh (j + 2)
      rw [g5, g6] at b
      exact absurd (iff_of_both (Or.inl S3) (Or.inl S3)) (b.1 hb)
    · exact Or.inr rfl
  · intro v hb hvh
    rcases (T.nbr0 v).1 hb.fst with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hvh
    · exact absurd (iff_ff nS4 nSw4 nS4 hSh) (bx4.1 hb.symm)
    · exact absurd S1 (bdGraph_out htri hb.symm).1
    · exact absurd (iff_ff nSw4 nSw0 nSw4 nS4) (bw4.1 hb.symm)
    · rfl
  · intro u v hb hu hv hu0 hv0
    have col : ∀ {x y : Fin n}, (bdGraph M S).Adj x y → x ≠ h →
        c x = c (P.x j) ∨ c x = c (P.x (j + 4)) := by
      intro x y hb hx
      obtain ⟨hxS, hw⟩ := bdGraph_out htri hb
      obtain ⟨n1, n3⟩ := comp_nbr (Or.inl rfl) hx hxS hw
      exact f4_rest h13 h1 h14 h3 h34 (Ne.symm h4) n1 n3
    exact ⟨⟨hb.fst, ⟨hu, col hb hu⟩, ⟨hv, col hb.symm hv⟩⟩, hu0, hv0⟩

/-- **(D) at `k = 3`, "not both".** Mirror of `not_both_k4` at `x (j+2)`, whose rotation is
`h, x (j+1), w₁, w₂, x (j+3)`. -/
theorem not_both_k3 (K : K3Ball P w m j) (hc : ProperOff M.graph h c) (hR : R3At P w c j)
    (hA : (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))).Reachable
      (w (j + 1)) m)
    (hB : (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1))
      (w (j + 2))) : False := by
  have T := K.tri
  have cm := m_col_k3 K hc hR
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -⟩ := hR
  obtain ⟨-, -, o1, o2⟩ := T.offh
  obtain ⟨-, -, -, a11, -, -⟩ := T.adjs
  obtain ⟨Q, hQ⟩ := pent5 (z := P.x (j + 2)) (a := h) (b := P.x (j + 1)) (d := w (j + 1))
    (e := w (j + 2)) (f := P.x (j + 3)) (fun u => (T.nbr2 u).trans (by tauto)) (P.adj_h _) a11
    T.ring12 T.adj3.symm (P.adj_h _).symm (P.x_ne_h _).symm o1.symm o2.symm (P.x_ne_h _).symm
    (T.off _).2.2.1.symm (T.off _).2.2.2.symm (fun e => absurd (P.inj e) (by simp))
    T.ring12.ne (T.off _).2.2.1 (T.off _).2.2.2
  obtain ⟨r, hr⟩ := walk_of_reach (M := M)
    (H := pairDel M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))) (fun u v e => e.1.1)
    (Q := fun v => v ≠ P.x (j + 2) ∧ Active h c (c (P.x j)) (c (P.x (j + 3))) v)
    (fun u v e => ⟨e.2.2, e.1.2.2⟩) ⟨K.offm _, K.offh.2, Or.inl cm⟩ hA.symm
  have a3m : M.Adj (P.x (j + 3)) m := (K.nbr3 m).2 (by simp)
  obtain ⟨q, hq⟩ := walk_of_reach (M := M)
    (H := pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))) (fun u v e => e.1)
    (Q := Active h c (c (P.x (j + 1))) (c (P.x (j + 4)))) (fun u v e => e.2.2)
    ⟨P.x_ne_h _, Or.inl rfl⟩ hB
  refine sep_core Q hQ
    (X := fun v => v ≠ P.x (j + 2) ∧ Active h c (c (P.x j)) (c (P.x (j + 3))) v)
    (Y := Active h c (c (P.x (j + 1))) (c (P.x (j + 4)))) ?_ (.cons a3m r) ?_ (fun H => H.1 rfl)
    q hq ?_
  · rintro v ⟨-, -, e | e⟩ ⟨-, f | f⟩
    · exact h1 (f.symm.trans e)
    · exact h4 (f.symm.trans e)
    · exact h13 (f.symm.trans e)
    · exact h34 (e.symm.trans f)
  · intro v hv
    rw [Walk.support_cons, List.mem_cons] at hv
    rcases hv with rfl | hv
    · exact ⟨fun e => absurd (P.inj e) (by simp), P.x_ne_h _, Or.inr rfl⟩
    · exact hr v hv
  · rintro ⟨-, e | e⟩
    · exact h1 (e.symm.trans h02.symm)
    · exact h4 (e.symm.trans h02.symm)

/-- **(D) at `k = 3`.** On a triangulated sphere, `w₁` reaches `m` in the `{α, A}`-graph with
`x (j+2)` deleted iff `w₂` is **not** in the `{μ, B}`-component of `x (j+1)`. The Hex half uses
`S` the `{μ, B}`-component of `x (j+1)` (containing `x (j+4)` by Lock 2): the boundary edges at
`h` go to `x (j+2)` and `x (j+3)`, and the only other one at `x (j+2)` goes to `w₁`. -/
theorem duality_k3 (htri : M.Triangulated) (K : K3Ball P w m j) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))).Reachable (w (j + 1)) m ↔
      ¬ (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1))
        (w (j + 2)) := by
  refine ⟨fun hA hB => not_both_k3 K hc hR hA hB, fun hn => ?_⟩
  refine (lock1_after_sigma_k3 K hc hR).1 ((lock1_after_sigma_iff K.tri hc hR.1.1 hR.outer).2 ?_)
  have T := K.tri
  have hL2 := hR.1.2.2
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -, -⟩, -, e1, -, -, -⟩ := hR
  obtain ⟨-, -, o1, o2⟩ := T.offh
  obtain ⟨-, -, -, a11, -, -⟩ := T.adjs
  obtain ⟨g1, g2, g3, g4, -, -⟩ := fin5_b j
  obtain ⟨-, -, f3, f4, -⟩ := fin5_a j
  set S : Fin n → Prop :=
    fun v => (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1)) v
    with hS
  have act : ∀ {v}, S v → Active h c (c (P.x (j + 1))) (c (P.x (j + 4))) v :=
    comp_active (Or.inl rfl)
  have notS : ∀ {v}, (c v = c (P.x j) ∨ c v = c (P.x (j + 3))) → ¬ S v := by
    rintro v (e | e) hv
    · rcases (act hv).2 with f | f
      · exact h1 (f.symm.trans e)
      · exact h4 (f.symm.trans e)
    · rcases (act hv).2 with f | f
      · exact h13 (f.symm.trans e)
      · exact h34 (e.symm.trans f)
  have hSh : ¬ S h := fun hv => (act hv).1 rfl
  have S1 : S (P.x (j + 1)) := Reachable.refl _
  have S4 : S (P.x (j + 4)) := hL2
  have nS0 : ¬ S (P.x j) := notS (Or.inl rfl)
  have nS2 : ¬ S (P.x (j + 2)) := notS (Or.inl h02.symm)
  have nS3 : ¬ S (P.x (j + 3)) := notS (Or.inr rfl)
  have nSw1 : ¬ S (w (j + 1)) := notS (Or.inr e1)
  have nSw2 : ¬ S (w (j + 2)) := hn
  obtain ⟨Q, hQ⟩ := pent5 (z := P.x (j + 2)) (a := h) (b := P.x (j + 1)) (d := w (j + 1))
    (e := w (j + 2)) (f := P.x (j + 3)) (fun u => (T.nbr2 u).trans (by tauto)) (P.adj_h _) a11
    T.ring12 T.adj3.symm (P.adj_h _).symm (P.x_ne_h _).symm o1.symm o2.symm (P.x_ne_h _).symm
    (T.off _).2.2.1.symm (T.off _).2.2.2.symm (fun e => absurd (P.inj e) (by simp))
    T.ring12.ne (T.off _).2.2.1 (T.off _).2.2.2
  obtain ⟨bw2, bx3⟩ := bd_pent htri Q hQ nS2
  refine hex_core htri P (S := S) (z := P.x (j + 2)) (t := P.x (j + 3)) (y := w (j + 1))
    (P.x_ne_h _) (fun e => absurd (P.inj e) (by simp)) ?_ ?_ ?_ ?_
  · have b := bd_link P htri hSh (j + 1)
    rw [g3, g4] at b
    exact b.2 fun hh => (hh.1 (Or.inr S1)).elim nS2 nS3
  · intro i hb
    rcases fin5_cases j i with e | e | e | e | e <;> rw [e] at hb ⊢
    · have b := bd_link P htri hSh (j + 4)
      rw [g1, g2] at b
      exact absurd (iff_of_both (Or.inr S4) (Or.inr S1)) (b.1 hb)
    · exact absurd (iff_of_both (Or.inl S1) (Or.inl S1)) ((bd_link P htri hSh j).1 hb)
    · exact Or.inl rfl
    · exact Or.inr rfl
    · have b := bd_link P htri hSh (j + 3)
      rw [f3, f4] at b
      exact absurd (iff_of_both (Or.inl S4) (Or.inl S4)) (b.1 hb)
  · intro v hb hvh
    rcases (T.nbr2 v).1 hb.fst with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hvh
    · exact absurd S1 (bdGraph_out htri hb.symm).1
    · exact absurd (iff_ff nS3 nSw2 nS3 hSh) (bx3.1 hb.symm)
    · rfl
    · exact absurd (iff_ff nSw2 nSw1 nSw2 nS3) (bw2.1 hb.symm)
  · intro u v hb hu hv hu0 hv0
    have col : ∀ {x y : Fin n}, (bdGraph M S).Adj x y → x ≠ h →
        c x = c (P.x j) ∨ c x = c (P.x (j + 3)) := by
      intro x y hb hx
      obtain ⟨hxS, hw⟩ := bdGraph_out htri hb
      obtain ⟨n1, n4⟩ := comp_nbr (Or.inl rfl) hx hxS hw
      exact f4_rest h14 h1 h13 h4 (Ne.symm h34) (Ne.symm h3) n1 n4
    exact ⟨⟨hb.fst, ⟨hu, col hb hu⟩, ⟨hv, col hb.symm hv⟩⟩, hu0, hv0⟩

/-! ### The exit criteria in the notes' form -/

/-- **`k = 4`, the note's criterion.** `σ c` is lockless iff `w₄` lies in the `{μ, A}`-component
of `x (j+1)` (the Lock 1 component). -/
theorem sigma_exit_criterion_k4' (htri : M.Triangulated) (K : K4Ball P w m j)
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    NoLock P (sigSwap P c j) ↔
      (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))).Reachable (P.x (j + 1))
        (w (j + 4)) := by
  rw [sigma_exit_criterion_k4 K hc hR, duality_k4 htri K hc hR, not_not]

/-- **`k = 3`, the note's criterion.** `σ c` is lockless iff `w₂` lies in the `{μ, B}`-component
of `x (j+1)` (the Lock 2 component). -/
theorem sigma_exit_criterion_k3' (htri : M.Triangulated) (K : K3Ball P w m j)
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    NoLock P (sigSwap P c j) ↔
      (pairGraph M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable (P.x (j + 1))
        (w (j + 2)) := by
  rw [sigma_exit_criterion_k3 K hc hR, duality_k3 htri K hc hR, not_not]

/-- **`f ≥ 2` at `k = 3`, unconditionally.** A lockless `σ`-image at a `k = 3` `R3` state steps to
two filled states (`sigma_exit_f_ge_two_k3` with its hypothesis discharged by (D)). -/
theorem sigma_exit_f_ge_two_k3' (htri : M.Triangulated) (K : K3Ball P w m j)
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) (hN : NoLock P (sigSwap P c j)) :
    Target M.graph h (piMove P (sigSwap P c j)) ∧
      Target M.graph h (piMove P (piMove P (sigSwap P c j))) :=
  sigma_exit_f_ge_two_k3 K hc hR ((sigma_exit_criterion_k3' htri K hc hR).1 hN)

end sphere

end SimpleGraph.QuarterFloor
