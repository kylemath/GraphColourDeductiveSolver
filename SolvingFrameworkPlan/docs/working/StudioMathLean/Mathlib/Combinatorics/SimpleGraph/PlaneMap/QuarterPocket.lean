/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterCrossing
public import Mathlib.Data.Fin.VecNotation

/-!
# The pocket lemma at `R1k2` (`NightA34.md` §2.2)

Setting of `QuarterCrossing`: a `Hole6 P w m q` with `p = x q`, `x⁺ = x (q+1)`, `z = w q`,
`w⁺ = w (q+1)`, `w₂ = w (q+2)`, `y = w (q+4)`; `G_J` the `{c y, c z}`-graph (`GJ`). The pocket
graph is the `{c p, c m}`-graph with `h, p, x⁺` deleted (`pocketGraph`).

## The frame (`PocketFrame`)

The proof uses only five facts about the state, all of which hold at position `9` (`R1k2`) of an
all-`DL` orbit (`pocketFrame_pos9`, from `J_iff_lock2_R1k2` and `pos9_xplus`):
`c y ≠ c z`; `y ~ x (q+4)` and `y ~ x (q+2)` in `G_J` (Lock 2); `x⁺` and `x (q+3)` are not
`J`-coloured.

## Main results (sorry-free, no new axioms, no planar hypothesis)

1. `pocket_of_not_J_core` / `pocket_of_not_J` (⇒, triangulated): if `J` fails, `m ⇝ w⁺` in the
   pocket graph. Boundary parity (the Hex argument of `QuarterJordanDual.duality_k4`, `hex_core`)
   with `S` the `G_J`-component of `z`, run at the degree-five vertex `x⁺` (rotation
   `h, p, z, w⁺, x (q+2)`, a `Pent` by `pent5`). `S` contains no link vertex, so `h` carries no
   boundary edge; every other boundary vertex is `{c p, c m}`-coloured; the boundary neighbours of
   `x⁺` are `p` and `w⁺` (the edge `x⁺p` is a boundary edge because `z ∈ S` sits between `p` and
   `w⁺`), and the only boundary neighbour of `p` besides `x⁺` is `m`. The handshake lemma joins
   `m` to `w⁺` by boundary edges avoiding `h, p, x⁺`. The complementary-pair curve is
   `p x⁺ w⁺ … m p`: `m` and `w⁺` are its ring ends, `p` and `x⁺` are deleted by the pair and the
   rotation at `x⁺`.
2. `not_J_of_pocket_core` / `not_J_of_pocket` (⇐): Kempe separation at `x⁺` (`sep_core`): the
   `G_J`-walk `x (q+2) ⇝ y ⇝ z` and the `{c p, c m}`-walk `p, m ⇝ w⁺` alternate at `x⁺`.
3. `pocket_iff`: `¬ J ↔ PocketPath`.
4. `separates_of_pocket`: a pocket path gives `PocketSeparates` (any walk of `T` from `z` to `y`
   or `w₂` meets `Pocket ∪ {p, x⁺}`; same separation at `x⁺`, closing the walk with
   `x (q+2), h, x (q+4), y` resp. `x (q+2), w₂`). Hence `pocketLemmaAt_pos9`
   (`PocketLemmaAt` of `QuarterCrossing` holds at `s₉` and `d₉`), and the unconditional
   corollaries `crossing_on_pocket'` and `A34_L20_of_no_two_pockets`.

The planar helpers of `QuarterJordanDual` are private there and are copied verbatim below.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

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

end hex

end copied

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

/-! ### The pocket lemma -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5} {c : Fin n → Fin 4}

variable (P w q) in
/-- The facts about the state used by the pocket lemma (all hold at `R1k2`). -/
structure PocketFrame (c : Fin n → Fin 4) : Prop where
  yz : c (w (q + 4)) ≠ c (w q)
  y4 : (GJ M h w q c).Reachable (w (q + 4)) (P.x (q + 4))
  y2 : (GJ M h w q c).Reachable (w (q + 4)) (P.x (q + 2))
  x1 : c (P.x (q + 1)) ≠ c (w (q + 4)) ∧ c (P.x (q + 1)) ≠ c (w q)
  x3 : c (P.x (q + 3)) ≠ c (w (q + 4)) ∧ c (P.x (q + 3)) ≠ c (w q)

private lemma fq (q : Fin 5) : q + 1 + 4 = q ∧ q + 1 + 1 = q + 2 := by revert q; decide

private lemma gj_act {a v : Fin n} (ha : Active h c (c (w (q + 4))) (c (w q)) a)
    (r : (GJ M h w q c).Reachable a v) : Active h c (c (w (q + 4))) (c (w q)) v := by
  by_cases e : a = v
  · exact e ▸ ha
  · exact reach_active r e

/-- The six colour facts at the hole. -/
private lemma cols (H : Hole6 P w m q) (hc : ProperOff M.graph h c) (F : PocketFrame P w q c) :
    c (w (q + 4)) ≠ c (w q) ∧ c (w (q + 4)) ≠ c (P.x q) ∧ c (w (q + 4)) ≠ c m ∧
    c (w q) ≠ c (P.x q) ∧ c (w q) ≠ c m ∧ c (P.x q) ≠ c m := by
  have py : M.graph.Adj (P.x q) (w (q + 4)) := (H.nbrq _).2 (by simp)
  have pz : M.graph.Adj (P.x q) (w q) := (H.nbrq _).2 (by simp)
  exact ⟨F.yz, (hc py (P.x_ne_h _) (H.offh _)).symm, hc H.ringy (H.offh _) H.offmh,
    (hc pz (P.x_ne_h _) (H.offh _)).symm, (hc H.ringz H.offmh (H.offh _)).symm,
    hc H.adj_m (P.x_ne_h _) H.offmh⟩

/-- `x (q+4)` and `x (q+2)` are `J`-coloured. -/
private lemma x24_act (H : Hole6 P w m q) (F : PocketFrame P w q c) :
    Active h c (c (w (q + 4))) (c (w q)) (P.x (q + 4)) ∧
      Active h c (c (w (q + 4))) (c (w q)) (P.x (q + 2)) :=
  ⟨gj_act ⟨H.offh _, Or.inl rfl⟩ F.y4, gj_act ⟨H.offh _, Or.inl rfl⟩ F.y2⟩

/-- Pocket vertices are off `h` and `x⁺`. -/
lemma pocket_ne (H : Hole6 P w m q) {v : Fin n} (hv : v ∈ Pocket P m q c) :
    v ≠ h ∧ v ≠ P.x (q + 1) := by
  obtain ⟨W⟩ := (show (pocketGraph P m q c).Reachable m v from hv).symm
  cases W with
  | nil => exact ⟨H.offmh, H.offm _⟩
  | cons e _ => exact ⟨e.1.2.1.1, e.2.2.1⟩

/-- `x⁺` is a degree-five vertex with rotation `h, p, z, w⁺, x (q+2)`. -/
private lemma pent_xplus (H : Hole6 P w m q) :
    ∃ Q : Pent M.graph (P.x (q + 1)), Q.x = ![h, P.x q, w q, w (q + 1), P.x (q + 2)] := by
  obtain ⟨f1, f2⟩ := fq q
  have hq1 : q + 1 ≠ q := fun e => absurd (add_left_cancel (e.trans (add_zero q).symm))
    (by decide)
  have hn := H.nbr (q + 1) hq1
  rw [f1, f2] at hn
  have ef : M.graph.Adj (w (q + 1)) (P.x (q + 2)) := by
    have := H.adj_w' (q + 1); rw [f2] at this; exact this.symm
  have zw : M.graph.Adj (w q) (w (q + 1)) := H.ring q hq1
  exact pent5 (fun u => (hn u).trans (by tauto)) (P.adj_h _) (H.adj_w q) zw ef (P.adj_h _).symm
    (P.x_ne_h _).symm (H.offh _).symm (H.offh _).symm (P.x_ne_h _).symm (H.off _ _).symm
    (H.off _ _).symm (fun e => absurd (P.inj e) (by simp)) zw.ne (H.off _ _) (H.off _ _)

/-- **Pocket lemma ⇒ (core).** If `J` fails, `m ⇝ w⁺` in the pocket graph. -/
theorem pocket_of_not_J_core (htri : M.Triangulated) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h c) (F : PocketFrame P w q c) (hJ : ¬ JoinYZ M.graph h w q c) :
    PocketPath P w m q c := by
  obtain ⟨cyz, cyp, cym, czp, czm, cpm⟩ := cols H hc F
  obtain ⟨a4, a2⟩ := x24_act H F
  obtain ⟨Q, hQ⟩ := pent_xplus H
  set S : Fin n → Prop := fun v => (GJ M h w q c).Reachable (w q) v with hS
  have Sact : ∀ {v}, S v → Active h c (c (w (q + 4))) (c (w q)) v :=
    gj_act ⟨H.offh _, Or.inr rfl⟩
  have Sz : S (w q) := Reachable.refl _
  have nSy : ∀ {v}, (GJ M h w q c).Reachable (w (q + 4)) v → ¬ S v :=
    fun r hv => hJ (r.trans hv.symm)
  have nScol : ∀ {v}, c v ≠ c (w (q + 4)) → c v ≠ c (w q) → ¬ S v := by
    intro v h1 h2 hv
    rcases (Sact hv).2 with e | e
    · exact h1 e
    · exact h2 e
  have nSx : ∀ i, ¬ S (P.x i) := by
    intro i
    rcases fin5_cases q i with rfl | rfl | rfl | rfl | rfl
    · exact nScol cyp.symm czp.symm
    · exact nScol F.x1.1 F.x1.2
    · exact nSy F.y2
    · exact nScol F.x3.1 F.x3.2
    · exact nSy F.y4
  have hh : ∀ v, ¬ (bdGraph M S).Adj h v := by
    intro v e
    obtain ⟨-, u, hu, a⟩ := bdGraph_out htri e
    obtain ⟨i, rfl⟩ := P.only _ a
    exact nSx i hu
  have bdc : ∀ {u v}, (bdGraph M S).Adj u v →
      u ≠ h ∧ ¬ S u ∧ (c u = c (P.x q) ∨ c u = c m) := by
    intro u v e
    obtain ⟨hu, t, ht, a⟩ := bdGraph_out htri e
    have uh : u ≠ h := fun e' => hh v (e' ▸ e)
    have n1 : c u ≠ c (w (q + 4)) := fun hcu =>
      hu (ht.trans (Adj.reachable ⟨a.symm, Sact ht, ⟨uh, Or.inl hcu⟩⟩))
    have n2 : c u ≠ c (w q) := fun hcu =>
      hu (ht.trans (Adj.reachable ⟨a.symm, Sact ht, ⟨uh, Or.inr hcu⟩⟩))
    exact ⟨uh, hu, f4_rest cyz cyp cym czp czm cpm n1 n2⟩
  have notpm : ∀ {v}, Active h c (c (w (q + 4))) (c (w q)) v →
      ¬ (c v = c (P.x q) ∨ c v = c m) := by
    rintro v ⟨-, e | e⟩ (f | f)
    · exact cyp (e.symm.trans f)
    · exact cym (e.symm.trans f)
    · exact czp (e.symm.trans f)
    · exact czm (e.symm.trans f)
  have hzb : (bdGraph M S).Adj (P.x q) (P.x (q + 1)) := by
    have b : (bdGraph M S).Adj (P.x q) (P.x (q + 1)) ↔
        ¬ ((S (P.x q) ∨ S h) ↔ (S (P.x q) ∨ S (w q))) := by
      have := bd_link Q htri (nSx (q + 1)) 0
      rw [hQ] at this
      exact this
    refine b.2 fun hh' => ?_
    rcases hh'.2 (Or.inr Sz) with e | e
    · exact nSx q e
    · exact (Sact e).1 rfl
  obtain ⟨f1, f2⟩ := fq q
  have hq1 : q + 1 ≠ q := fun e => absurd (add_left_cancel (e.trans (add_zero q).symm))
    (by decide)
  have hn := H.nbr (q + 1) hq1
  rw [f1, f2] at hn
  have honly' : ∀ u, M.graph.Adj (P.x (q + 1)) u → (bdGraph M S).Adj u (P.x (q + 1)) →
      u = P.x q ∨ u = w (q + 1) := by
    intro u a e
    rcases (hn u).1 a with rfl | rfl | rfl | rfl | rfl
    · exact ((bdc e).1 rfl).elim
    · exact Or.inl rfl
    · exact (notpm a2 (bdc e).2.2).elim
    · exact ((bdc e).2.1 Sz).elim
    · exact Or.inr rfl
  refine hex_core htri Q (S := S) (z := P.x q) (t := w (q + 1)) (y := m)
    (fun e => absurd (P.inj e) (by simp)) (H.off _ _).symm hzb
    (fun i e => honly' _ (Q.adj_h i) e) ?_ ?_
  · intro v e hv
    rcases (H.nbrq v).1 e.fst with rfl | rfl | rfl | rfl | rfl | rfl
    · exact ((bdc e.symm).1 rfl).elim
    · exact (notpm a4 (bdc e.symm).2.2).elim
    · exact (hv rfl).elim
    · exact (notpm ⟨H.offh _, Or.inl rfl⟩ (bdc e.symm).2.2).elim
    · rfl
    · exact ((bdc e.symm).2.1 Sz).elim
  · intro u v e hu hv hu0 hv0
    exact ⟨⟨e.fst, ⟨(bdc e).1, (bdc e).2.2⟩, ⟨(bdc e.symm).1, (bdc e.symm).2.2⟩⟩,
      hu0, hu, hv0, hv⟩

/-- **Pocket lemma ⇐ (core).** A pocket path forces `J` to fail. -/
theorem not_J_of_pocket_core (H : Hole6 P w m q) (hc : ProperOff M.graph h c)
    (F : PocketFrame P w q c) (hP : PocketPath P w m q c) : ¬ JoinYZ M.graph h w q c := by
  intro hJ
  obtain ⟨cyz, cyp, cym, czp, czm, cpm⟩ := cols H hc F
  obtain ⟨-, a2⟩ := x24_act H F
  obtain ⟨Q, hQ⟩ := pent_xplus H
  obtain ⟨r, hr⟩ := walk_of_reach (M := M) (H := GJ M h w q c) (fun _ _ e => e.1)
    (Q := Active h c (c (w (q + 4))) (c (w q))) (fun _ _ e => e.2.2) a2
    (F.y2.symm.trans (show (GJ M h w q c).Reachable (w (q + 4)) (w q) from hJ))
  obtain ⟨t, ht⟩ := walk_of_reach (M := M) (H := pocketGraph P m q c) (fun _ _ e => e.1.1)
    (Q := fun v => v ≠ P.x (q + 1) ∧ (c v = c (P.x q) ∨ c v = c m))
    (fun _ _ e => ⟨e.2.2.2.2, e.1.2.2.2⟩) ⟨H.offm _, Or.inr rfl⟩ hP
  refine sep_core Q hQ (X := Active h c (c (w (q + 4))) (c (w q)))
    (Y := fun v => v ≠ P.x (q + 1) ∧ (c v = c (P.x q) ∨ c v = c m)) ?_ r hr
    (fun ha => ha.2.elim F.x1.1 F.x1.2) (.cons H.adj_m t) ?_ (fun hy => hy.1 rfl)
  · rintro v ⟨-, e | e⟩ ⟨-, f | f⟩
    · exact cyp (e.symm.trans f)
    · exact cym (e.symm.trans f)
    · exact czp (e.symm.trans f)
    · exact czm (e.symm.trans f)
  · intro v hv
    rw [Walk.support_cons, List.mem_cons] at hv
    rcases hv with rfl | hv
    · exact ⟨fun e => absurd (P.inj e) (by simp), Or.inl rfl⟩
    · exact ht v hv

/-- **Pocket lemma (core).** `J` fails iff `m ⇝ w⁺` in the pocket graph. -/
theorem pocket_iff_core (htri : M.Triangulated) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h c) (F : PocketFrame P w q c) :
    ¬ JoinYZ M.graph h w q c ↔ PocketPath P w m q c :=
  ⟨pocket_of_not_J_core htri H hc F, not_J_of_pocket_core H hc F⟩

/-- **The pocket curve separates.** Given a pocket path, every walk of `T` from `z` to `y` or to
`w₂` meets `Pocket ∪ {p, x⁺}`. The walk, closed by `x (q+2), h, x (q+4), y` (resp. `x (q+2), w₂`),
and the curve walk `p, m ⇝ w⁺` alternate at `x⁺` (`sep_core`). -/
theorem separates_of_pocket (H : Hole6 P w m q) (hc : ProperOff M.graph h c)
    (F : PocketFrame P w q c) (hP : PocketPath P w m q c) : PocketSeparates P w m q c := by
  obtain ⟨cyz, cyp, cym, czp, czm, cpm⟩ := cols H hc F
  obtain ⟨a4, a2⟩ := x24_act H F
  obtain ⟨Q, hQ⟩ := pent_xplus H
  have nC : ∀ {v}, Active h c (c (w (q + 4))) (c (w q)) v → v ≠ P.x q → v ≠ P.x (q + 1) →
      ¬ OnCurve P m q c v := by
    rintro v ha h0 h1 (hv | e | e)
    · rcases ha.2 with e | e <;> rcases pocket_col hv with f | f
      · exact cyp (e.symm.trans f)
      · exact cym (e.symm.trans f)
      · exact czp (e.symm.trans f)
      · exact czm (e.symm.trans f)
    · exact h0 e
    · exact h1 e
  have nCh : ¬ OnCurve P m q c h := by
    rintro (hv | e | e)
    · exact (pocket_ne H hv).1 rfl
    · exact P.x_ne_h _ e.symm
    · exact P.x_ne_h _ e.symm
  have nC2 : ¬ OnCurve P m q c (P.x (q + 2)) :=
    nC a2 (fun e => absurd (P.inj e) (by simp)) (fun e => absurd (P.inj e) (by simp))
  have nC4 : ¬ OnCurve P m q c (P.x (q + 4)) :=
    nC a4 (fun e => absurd (P.inj e) (by simp)) (fun e => absurd (P.inj e) (by simp))
  intro t ht W
  by_contra hno
  push Not at hno
  obtain ⟨W2⟩ := (show (pocketGraph P m q c).Reachable m (w (q + 1)) from hP)
  have hB : ∀ v ∈ (Walk.cons H.adj_m (W2.mapLe (fun _ _ e => e.1.1 : pocketGraph P m q c ≤
      M.graph))).support, OnCurve P m q c v ∧ v ≠ P.x (q + 1) := by
    intro v hv
    rw [Walk.support_cons, List.mem_cons, Walk.support_mapLe_eq_support] at hv
    rcases hv with rfl | hv
    · exact ⟨Or.inr (Or.inl rfl), fun e => absurd (P.inj e) (by simp)⟩
    · have hp : v ∈ Pocket P m q c := ⟨W2.takeUntil v hv⟩
      exact ⟨Or.inl hp, (pocket_ne H hp).2⟩
  rcases ht with rfl | rfl
  · refine sep_core Q hQ (X := fun v => ¬ OnCurve P m q c v)
      (Y := fun v => OnCurve P m q c v ∧ v ≠ P.x (q + 1)) (fun v a b => a b.1)
      (Walk.cons (P.adj_h (q + 2)).symm (Walk.cons (P.adj_h (q + 4))
        (Walk.cons (H.adj_w (q + 4)) W.reverse))) ?_ (fun hx => hx (Or.inr (Or.inr rfl))) _ hB
      (fun hy => hy.2 rfl)
    intro v hv
    simp only [Walk.support_cons, Walk.support_reverse, List.mem_cons, List.mem_reverse] at hv
    rcases hv with rfl | rfl | rfl | hv
    · exact nC2
    · exact nCh
    · exact nC4
    · exact hno v hv
  · refine sep_core Q hQ (X := fun v => ¬ OnCurve P m q c v)
      (Y := fun v => OnCurve P m q c v ∧ v ≠ P.x (q + 1)) (fun v a b => a b.1)
      (Walk.cons (H.adj_w (q + 2)) W.reverse) ?_ (fun hx => hx (Or.inr (Or.inr rfl))) _ hB
      (fun hy => hy.2 rfl)
    intro v hv
    simp only [Walk.support_cons, Walk.support_reverse, List.mem_cons, List.mem_reverse] at hv
    rcases hv with rfl | hv
    · exact nC2
    · exact hno v hv

/-! ### Position `9` of the all-`DL` orbit -/

section setting
variable {s : Fin n → Fin 4} {j₀ : Fin 5} {ρ : Equiv.Perm (Fin 4)}
variable (htri : M.Triangulated) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
  (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
  (hT : TypeR3 P w s j₀) (hρ : (piMove P)^[20] s = recol ρ s)

private lemma fj (j : Fin 5) : j + 2 + 4 = j + 1 ∧ j + 2 + 2 = j + 4 ∧ j + 2 + 3 = j := by
  revert j; decide

include H hc hall hr hq hT in
/-- At position `9` (`R1k2`, `q = j + 2`) the frame holds: `y = w (j+1)` is `B`, `z = w (j+2)`
is `μ`; `y ~ x (j+1) ~ x (j+4)` in the `Lock2` = `J` pair; `x⁺` has letter `A` (`pos9_xplus`) and
`x (q+3) = x j` letter `α`. -/
theorem pocketFrame_pos9 : PocketFrame P w q ((piMove P)^[9] s) := by
  have px := pos9_xplus H hc hall hr hq hT
  obtain ⟨j, hd, hqj, ey, ez, hg, ry, l2, -⟩ := J_iff_lock2_R1k2 H hc hall hr hq hT 9 rfl
  obtain ⟨-, h1, -, h4, -, h14, -⟩ := hd.1
  subst hqj
  obtain ⟨e1, e2, e3⟩ := fj j
  refine ⟨?_, ?_, ?_, px, ?_⟩
  · rw [e1, ey, ez]; exact Ne.symm h14
  · show (pairGraph M.graph h _ _ _).Reachable _ _
    rw [hg, e1]; exact ry.symm
  · show (pairGraph M.graph h _ _ _).Reachable _ _
    rw [hg, e1, e2]; exact ry.symm.trans l2
  · rw [e3, e1, ey, ez]; exact ⟨Ne.symm h4, Ne.symm h1⟩

include htri H hc hall hr hq hT in
/-- **(1) Pocket lemma ⇒ at `R1k2`.** If `J` fails at `s₉`, then `m ⇝ w⁺` in the
`{c p, c m}`-graph of `s₉` with `h, p, x⁺` deleted. -/
theorem pocket_of_not_J (hJ : ¬ JoinYZ M.graph h w q ((piMove P)^[9] s)) :
    PocketPath P w m q ((piMove P)^[9] s) :=
  pocket_of_not_J_core htri H (iter_proper hc 9) (pocketFrame_pos9 H hc hall hr hq hT) hJ

include H hc hall hr hq hT in
/-- **(2) Pocket lemma ⇐ at `R1k2`.** -/
theorem not_J_of_pocket (hP : PocketPath P w m q ((piMove P)^[9] s)) :
    ¬ JoinYZ M.graph h w q ((piMove P)^[9] s) :=
  not_J_of_pocket_core H (iter_proper hc 9) (pocketFrame_pos9 H hc hall hr hq hT) hP

include htri H hc hall hr hq hT in
/-- **(3) The pocket lemma at `R1k2`.** -/
theorem pocket_iff :
    ¬ JoinYZ M.graph h w q ((piMove P)^[9] s) ↔ PocketPath P w m q ((piMove P)^[9] s) :=
  ⟨pocket_of_not_J htri H hc hall hr hq hT, not_J_of_pocket H hc hall hr hq hT⟩

include htri H hc hall hr hq hT in
/-- **(4) `PocketLemmaAt` holds at `s₉`**: a break gives a pocket path and a separating curve. -/
theorem pocketLemmaAt_pos9 : PocketLemmaAt P w m q ((piMove P)^[9] s) := fun hJ =>
  have pp := pocket_of_not_J htri H hc hall hr hq hT hJ
  ⟨pp, separates_of_pocket H (iter_proper hc 9) (pocketFrame_pos9 H hc hall hr hq hT) pp⟩

include htri H hc hall hr hq hT in
/-- `PocketLemmaAt` holds at `d₉`, `d = G s` (`d_setting`). -/
theorem pocketLemmaAt_pos9_G : PocketLemmaAt P w m q ((piMove P)^[9] (Gmap P ρ s)) := by
  obtain ⟨hcd, halld, hrd, hTd⟩ := d_setting H hc hall hr hq hT (ρ := ρ)
  exact pocketLemmaAt_pos9 htri H hcd halld hrd hq hTd

include htri H hc hall hr hq hT hρ in
/-- **Crossing on the pocket, unconditional.** If the `s`-run breaks, every `G_J(d₉)` walk from
`z` to `y` or `w₂` meets `X₉` at a non-hole vertex of the pocket of `s₉`. -/
theorem crossing_on_pocket' (hB : Break P w q s) {t : Fin n}
    (ht : t = w (q + 4) ∨ t = w (q + 2))
    (W : (GJ M h w q ((piMove P)^[9] (Gmap P ρ s))).Walk (w q) t) :
    ∃ v ∈ W.support, v ∈ X9 P ρ s ∧ v ∈ Pocket P m q ((piMove P)^[9] s) ∧
      ¬ HoleVT P w m q v :=
  crossing_on_pocket H hc hall hr hq hT hρ (pocketLemmaAt_pos9 htri H hc hall hr hq hT hB).2 ht W

include htri H hc hall hr hq hT hρ in
/-- **`A₃₄′(L = 20)` from the two-pocket obstruction, unconditional.** Refuting
`TwoPocketConj s₉ d₉` rules out two consecutive `k = 4` failures along the orbit. -/
theorem A34_L20_of_no_two_pockets
    (hobs : ¬ TwoPocketConj P w m q ((piMove P)^[9] s) ((piMove P)^[9] (Gmap P ρ s))) :
    ∀ b, ¬ (K4Fail P q ((piMove P)^[10 * b + 10] s) ∧
      K4Fail P q ((piMove P)^[10 * (b + 1) + 10] s)) :=
  no_double_break_of_crossing_obstruction htri H hc hall hr hq hT hρ
    (pocketLemmaAt_pos9 htri H hc hall hr hq hT) (pocketLemmaAt_pos9_G htri H hc hall hr hq hT)
    hobs

end setting

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.pocket_of_not_J_core
#print axioms SimpleGraph.QuarterFloor.not_J_of_pocket_core
#print axioms SimpleGraph.QuarterFloor.pocket_iff_core
#print axioms SimpleGraph.QuarterFloor.separates_of_pocket
#print axioms SimpleGraph.QuarterFloor.pocketFrame_pos9
#print axioms SimpleGraph.QuarterFloor.pocket_of_not_J
#print axioms SimpleGraph.QuarterFloor.not_J_of_pocket
#print axioms SimpleGraph.QuarterFloor.pocket_iff
#print axioms SimpleGraph.QuarterFloor.pocketLemmaAt_pos9
#print axioms SimpleGraph.QuarterFloor.pocketLemmaAt_pos9_G
#print axioms SimpleGraph.QuarterFloor.crossing_on_pocket'
#print axioms SimpleGraph.QuarterFloor.A34_L20_of_no_two_pockets
