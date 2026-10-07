/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterRotation
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalFiveColor
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalCompletion

/-!
# Definedness of the rotations from planarity

On a spherical map, the definedness hypotheses `Rot3Def` / `Rot2Def` of `QuarterRotation`
follow from the locks by the Jordan separation of `NoFrozen` (reproduced privately below,
since `NoFrozen` and `QuarterRotation` clash on `pairGraph_comm` and cannot be co-imported):

* `rot3Def_of_lock2`: `Lock2 j → Rot3Def j` (from `not_reach_alpha_A_of_lock2`).
* `rot2Def_of_lock1`: `Lock1 j → Rot2Def j` (from `not_reach_alpha_B_of_lock1`).
* `rot3_bijOn_planar`: hence `R₊₃` is a bijection from
  `{proper, repeat at j, lock 2 at j}` onto `{proper, repeat at j+3, lock 1 at j+3}`.
  This needs only the two directions above (sorry-free).

## The converse (hand dichotomy L2), and why it needs triangulation

`Rot3Def j → Lock2 j` is **false** for general spherical maps: in the wheel `W₅`
(hub `h`, rim `x 0 … x 4`, rim colours `(α, μ, α, A, B)` from `j`) `x j` is isolated in the
`{α, A}`-graph of `G - h`, so `Rot3Def` holds, while `x (j+1)` and `x (j+4)` are not adjacent and
are the only `{μ, B}` vertices, so `Lock2` fails. The pentagonal face of `W₅` is the obstruction.

For triangulated maps the converse is the Hex lemma for the disc `G - h` (boundary the link,
split into the arcs `{x j}`, `{x (j+1)}`, `{x (j+2), x (j+3)}`, `{x (j+4)}`, vertices typed by
colour class `{α, A}` vs `{μ, B}`). The library has no Hex lemma; it is stated here as
`kempe_hex` with `sorry`, and `lock2_of_rot3Def` is derived from it.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

variable {n : ℕ} {M : SphericalMap n} {h : Fin n} (P : Pent M.graph h)

/-! ### Jordan separation at the hole

Private copy of `NoFrozen` (lines 41–295): `NoFrozen` and `QuarterRotation` cannot be imported
together because both declare `SimpleGraph.QuarterFloor.pairGraph_comm`. -/


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

/-- Shared core: a lock walk `p` (colours `{μ, X}`) from `v0` to `m` and a reachability in
colours `{α, Y}` between `x j` and `x (j+2)` cannot coexist when the four colours
`μ, X, α, Y` are such that `{μ, X} ∩ {α, Y} = ∅`. -/
private lemma no_cross (c : Fin n → Fin 4) (j : Fin 5) {μ X α Y : Fin 4}
    (hdis : ∀ z, (z = μ ∨ z = X) → (z = α ∨ z = Y) → False)
    {v0 : Fin n} (h0 : M.Adj h v0) (hne : v0 ≠ P.x (j + 1))
    (hlock : (pairGraph M.graph h c μ X).Reachable (P.x (j + 1)) v0)
    (hreach : (pairGraph M.graph h c α Y).Reachable (P.x j) (P.x (j + 2))) : False := by
  obtain ⟨p⟩ := hlock.symm
  obtain ⟨q⟩ := hreach
  have hpa := support_active p
  have hqa := support_active q
  have hp : ∀ z ∈ (p.mapLe (pairGraph_le c μ X)).support, Active h c μ X z := by
    intro z hz
    rw [Walk.support_mapLe_eq_support] at hz
    rcases hpa z hz with hz' | ⟨rfl, rfl⟩
    · exact hz'
    · exact absurd rfl hne
  have hq : ∀ z ∈ (q.mapLe (pairGraph_le c α Y)).support, Active h c α Y z := by
    intro z hz
    rw [Walk.support_mapLe_eq_support] at hz
    rcases hqa z hz with hz' | ⟨rfl, e⟩
    · exact hz'
    · exact absurd e (P.ne (by simp))
  obtain ⟨z, hzp, hzq⟩ := lock_separates P j h0 hne _ (fun hh => (hp h hh).1 rfl) _
    (fun hh => (hq h hh).1 rfl)
  exact hdis _ (hp z hzp).2 (hq z hzq).2

/-- Lock 2 separates: `x j` and `x (j+2)` are in different `{α, A}`-components. -/
private theorem not_reach_alpha_A_of_lock2 (c : Fin n → Fin 4) (j : Fin 5) (hr : RepeatAt P c j)
    (hl : Lock2 P c j) :
    ¬ (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x j) (P.x (j + 2)) := by
  obtain ⟨-, h1, h2, h3, h4, h5, h6⟩ := hr
  intro hreach
  refine no_cross P c j ?_ (P.adj_h (j + 4)) (P.ne (by simp)) hl hreach
  rintro z (rfl | rfl) (e | e)
  · exact h1 e
  · exact h4 e
  · exact h3 e
  · exact h6 e.symm

/-- Lock 1 separates: `x j` and `x (j+2)` are in different `{α, B}`-components. -/
private theorem not_reach_alpha_B_of_lock1 (c : Fin n → Fin 4) (j : Fin 5) (hr : RepeatAt P c j)
    (hl : Lock1 P c j) :
    ¬ (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) (P.x (j + 2)) := by
  obtain ⟨-, h1, h2, h3, h4, h5, h6⟩ := hr
  intro hreach
  refine no_cross P c j ?_ (P.adj_h (j + 3)) (P.ne (by simp)) hl hreach
  rintro z (rfl | rfl) (e | e)
  · exact h1 e
  · exact h5 e
  · exact h2 e
  · exact h6 e

/-- **Item 1.** Lock 2 makes `R₊₃` defined. -/
theorem rot3Def_of_lock2 {c : Fin n → Fin 4} {j : Fin 5} (hr : RepeatAt P c j)
    (hl : Lock2 P c j) : Rot3Def P c j :=
  fun hreach => not_reach_alpha_A_of_lock2 P c j hr hl hreach.symm

/-- **Item 2.** Lock 1 makes `R₊₂` defined. -/
theorem rot2Def_of_lock1 {c : Fin n → Fin 4} {j : Fin 5} (hr : RepeatAt P c j)
    (hl : Lock1 P c j) : Rot2Def P c j :=
  not_reach_alpha_B_of_lock1 P c j hr hl

/-- On a sphere, `Dom3` is just `{proper, repeat, lock 2}`. -/
lemma dom3_eq (j : Fin 5) :
    Dom3 P j = {c | ProperOff M.graph h c ∧ RepeatAt P c j ∧ Lock2 P c j} := by
  ext c
  exact ⟨fun ⟨a, b, l, _⟩ => ⟨a, b, l⟩, fun ⟨a, b, l⟩ => ⟨a, b, l, rot3Def_of_lock2 P b l⟩⟩

/-- On a sphere, `Dom2` is just `{proper, repeat, lock 1}`. -/
lemma dom2_eq (j : Fin 5) :
    Dom2 P j = {c | ProperOff M.graph h c ∧ RepeatAt P c j ∧ Lock1 P c j} := by
  ext c
  exact ⟨fun ⟨a, b, l, _⟩ => ⟨a, b, l⟩, fun ⟨a, b, l⟩ => ⟨a, b, l, rot2Def_of_lock1 P b l⟩⟩

/-- **Item 4.** On a sphere, `R₊₃` is a bijection from `{proper, repeat at j, lock 2 at j}`
onto `{proper, repeat at j+3, lock 1 at j+3}`, with inverse `R₊₂`. -/
theorem rot3_bijOn_planar (j : Fin 5) :
    Set.BijOn (fun c => rot3 P c j)
      {c | ProperOff M.graph h c ∧ RepeatAt P c j ∧ Lock2 P c j}
      {c | ProperOff M.graph h c ∧ RepeatAt P c (j + 3) ∧ Lock1 P c (j + 3)} := by
  rw [← dom3_eq, ← dom2_eq]
  exact rot3_bijOn P j

/-- **Missing library lemma (Hex lemma at a pentagonal hole).** In a triangulated spherical
map, at a repeat state `(α, μ, α, A, B)` at `j`, either `x j` reaches `x (j+3)` in the
`{α, A}`-graph of `G - h`, or `x (j+1)` reaches `x (j+4)` in the `{μ, B}`-graph.
False without `Triangulated` (wheel `W₅`, see the module docstring). -/
theorem kempe_hex (htri : M.Triangulated) (c : Fin n → Fin 4) (j : Fin 5)
    (hr : RepeatAt P c j) :
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x j) (P.x (j + 3)) ∨
      Lock2 P c j := by
  sorry

/-- **Item 3** (triangulated maps, modulo `kempe_hex`). If `R₊₃` is defined then lock 2
holds. -/
theorem lock2_of_rot3Def (htri : M.Triangulated) {c : Fin n → Fin 4} {j : Fin 5}
    (hr : RepeatAt P c j) (hK : Rot3Def P c j) : Lock2 P c j := by
  rcases kempe_hex P htri c j hr with hx | hl
  · exact absurd ((rot3_reach hr).trans hx.symm) hK
  · exact hl

/-- The dichotomy L2 on triangulated maps (modulo `kempe_hex`). -/
theorem rot3Def_iff_lock2 (htri : M.Triangulated) {c : Fin n → Fin 4} {j : Fin 5}
    (hr : RepeatAt P c j) : Rot3Def P c j ↔ Lock2 P c j :=
  ⟨lock2_of_rot3Def P htri hr, rot3Def_of_lock2 P hr⟩

end SimpleGraph.QuarterFloor
