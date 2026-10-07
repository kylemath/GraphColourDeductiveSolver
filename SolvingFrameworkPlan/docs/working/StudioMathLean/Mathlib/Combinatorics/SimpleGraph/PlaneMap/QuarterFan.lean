/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterW2Frame

/-!
# The fan lemma and W2′

Formalises `NightW2.md` §8.1–§8.2. Frame at a repeat state at `j`: `α = c (x j)`,
`μ = c (x (j+1))`, `A = c (x (j+3))`, `B = c (x (j+4))`, and `K_σ` the `{α, μ}`-component of
`x (j+1)` in `T − h`. `Escape P c j u`: some `{α, μ}`-neighbour of `u` lies outside `K_σ`.

## Main results (sorry-free, no new axioms)

* `escape_of_onCycle` (fan lemma `⇒`): if `u` is off the link and lies on an `{A, B}`-cycle of
  `T − h`, then `Escape u` (the argument of `acyclic_of_sigmaFixed`, run at `u`).
* `onCycle_of_escape` (fan lemma `⇐`): if `u` is coloured `A` or `B`, has a neighbour in `K_σ`,
  and `Escape u`, then `u` lies on an `{A, B}`-cycle: the face boundary of the
  `{α, μ}`-component of the escaping neighbour is an even subgraph of the `{A, B}`-graph with
  an edge at `u`, and in an even graph every edge lies on a cycle. No connectivity needed.
* `fan_iff`: both together.
* `yz_cycle_iff_escape` (**W2′ at one state**): for `y, z` off the link, coloured `A/B`, with a
  common neighbour in `K_σ`: "`y` or `z` lies on an `{A, B}`-cycle" `⇔` "`y` or `z` escapes".
* `not_sigmaFixed_of_escape`: an escape is literally `¬ SigmaFixed`.
* Orbit form (setting of `QuarterW2Frame`, positions 4, 6, 8 of a period, `k = m`):
  `w2'_iff` (cycle form `⇔` escape form, over the three states), and
  `not_all_fixed_of_w2'`: W2′ ⇒ `¬ (F₄ ∧ F₆ ∧ F₈)`. W2′ itself is not proved.

The planar helpers (`TriMeets`, `bdGraph`, `bdGraph_even`, `odd_iff_bd`, …) are private in
`QuarterSigmaFix` and are copied verbatim below.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Private copies of the boundary-parity helpers of `QuarterSigmaFix` -/

section copied
variable {n : ℕ} {M : SphericalMap n}

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

end copied

section generic
variable {n : ℕ} {M : SphericalMap n}

/-- The third vertex of the (triangular) face of `d` is adjacent to `d.fst`. -/
private lemma face_third_adj (htri : M.Triangulated) (d : M.Dart) :
    M.Adj (M.rotation.faceNext d).snd d.fst := by
  have e1 := M.rotation.face_next_fst (M.rotation.faceNext d)
  have e2 := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
  rw [tri3 htri d] at e2
  have := (M.rotation.faceNext (M.rotation.faceNext d)).adj
  rw [e1, ← e2] at this
  exact this

/-- Every vertex of a two-colour walk from an active vertex is active. -/
private lemma pair_support_active {h : Fin n} {c : Fin n → Fin 4} {a b : Fin 4} {s t : Fin n}
    (p : (pairGraph M.graph h c a b).Walk s t) (hs : Active h c a b s) :
    ∀ z ∈ p.support, Active h c a b z := by
  induction p with
  | nil => intro z hz; rw [Walk.support_nil, List.mem_singleton] at hz; exact hz ▸ hs
  | cons e p ih =>
    intro z hz
    rw [Walk.support_cons, List.mem_cons] at hz
    rcases hz with rfl | hz
    · exact hs
    · exact ih e.2.2 z hz

/-- A cycle at `z` splits into two edges `z y`, `z v` and a walk `v → y` avoiding `z`. -/
private lemma cycle_split {V : Type*} {G : SimpleGraph V} {z : V} (D : G.Walk z z)
    (hD : D.IsCycle) :
    ∃ (y v : V) (_ : G.Adj z y) (_ : G.Adj z v) (r : G.Walk v y), v ≠ y ∧ z ∉ r.support := by
  cases D with
  | nil => exact absurd hD Walk.not_isCycle_nil
  | cons e q =>
    rename_i y
    rw [Walk.cons_isCycle_iff] at hD
    obtain ⟨hq, hnot⟩ := hD
    have hq' := hq.reverse
    have hedges : s(z, y) ∉ q.reverse.edges := by
      rwa [Walk.edges_reverse, List.mem_reverse]
    generalize q.reverse = r at hq' hedges
    cases r with
    | nil => exact (e.ne rfl).elim
    | cons e' r' =>
      rename_i v
      rw [Walk.cons_isPath_iff] at hq'
      refine ⟨y, v, e, e', r', ?_, hq'.2⟩
      rintro rfl
      exact hedges (by simp)

open Classical in
/-- In an even graph every edge lies on a cycle (it is not a bridge). -/
private lemma cycle_of_even {G : SimpleGraph (Fin n)} (hev : ∀ x, Even (G.degree x))
    {u v : Fin n} (huv : G.Adj u v) : ∃ C : G.Walk u u, C.IsCycle := by
  have hm : Odd ((compKeep (offV G u) v).degree v) := by
    rw [odd_iff_bd _ hev]
    exact ⟨Reachable.refl _, huv.ne.symm, huv.symm⟩
  obtain ⟨w, hwv, hw⟩ := exists_ne_odd_degree_of_exists_odd_degree (h := hm)
  rw [odd_iff_bd _ hev] at hw
  obtain ⟨hr, hwu, hadj⟩ := hw
  have e1 : (G.deleteEdges {s(u, v)}).Adj u w := by
    rw [deleteEdges_adj]
    refine ⟨hadj.symm, ?_⟩
    rw [Set.mem_singleton_iff, Sym2.eq_iff]
    rintro (⟨-, e⟩ | ⟨e, -⟩)
    · exact hwv e
    · exact huv.ne e
  have hle : offV G u ≤ G.deleteEdges {s(u, v)} := by
    intro a b ⟨e, ha, hb⟩
    rw [deleteEdges_adj]
    refine ⟨e, ?_⟩
    rw [Set.mem_singleton_iff, Sym2.eq_iff]
    rintro (⟨e', -⟩ | ⟨-, e'⟩)
    · exact ha e'
    · exact hb e'
  have reach : (G.deleteEdges {s(u, v)}).Reachable u v := e1.reachable.trans (hr.mono hle).symm
  obtain ⟨u', p, hp, he⟩ := adj_and_reachable_delete_edges_iff_exists_cycle.1 ⟨huv, reach⟩
  have hu : u ∈ p.support := p.fst_mem_support_of_mem_edges he
  exact ⟨p.rotate u hu, hp.rotate hu⟩

end generic

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- `u` lies on a cycle of `G`. -/
def OnCycle {V : Type*} (G : SimpleGraph V) (u : V) : Prop := ∃ C : G.Walk u u, C.IsCycle

variable (P : Pent M.graph h) in
/-- **Escape at `u`**: some `{α, μ}`-neighbour of `u` lies outside `K_σ`, the
`{α, μ}`-component of `x (j+1)`. -/
def Escape (c : Fin n → Fin 4) (j : Fin 5) (u : Fin n) : Prop :=
  ∃ v, M.graph.Adj u v ∧ Active h c (c (P.x j)) (c (P.x (j + 1))) v ∧
    ¬ (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) v

variable {P : Pent M.graph h} {c : Fin n → Fin 4} {j : Fin 5}

/-- An escape is a vertex of colour `α/μ` outside `K_σ`: not a fixed point. -/
theorem not_sigmaFixed_of_escape {u : Fin n} (he : Escape P c j u) : ¬ SigmaFixed P c j := by
  rintro hf
  obtain ⟨v, -, hv, hn⟩ := he
  exact hn (hf v hv)

/-- **Fan lemma, `⇒`.** If `u` is off the link and lies on an `{A, B}`-cycle of `T − h`, then
some `{α, μ}`-neighbour of `u` lies outside `K_σ`: the two rotation neighbours at `u` of the
next cycle vertex are `α/μ`-coloured and separated by the cycle (Jordan). -/
theorem escape_of_onCycle (htri : M.Triangulated) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) {u : Fin n} (hu : ∀ i, u ≠ P.x i)
    (hC : OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) u) :
    Escape P c j u := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have dis : ∀ {x}, Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) x →
      Active h c (c (P.x j)) (c (P.x (j + 1))) x → False := by
    rintro x ⟨-, e | e⟩ ⟨-, f | f⟩
    · exact h3 (e.symm.trans f)
    · exact h13 (f.symm.trans e)
    · exact h4 (e.symm.trans f)
    · exact h14 (f.symm.trans e)
  obtain ⟨C, hCc⟩ := hC
  obtain ⟨y2, v0, e, e0, r, hv0, hzr⟩ := cycle_split C hCc
  have az := e.2.1
  have ay := e.2.2
  have hzy : c u ≠ c y2 := hc e.1 az.1 ay.1
  have hzh : ¬ M.Adj u h := by
    intro hh
    obtain ⟨i, rfl⟩ := P.only _ hh.symm
    exact hu i rfl
  set Dd : M.Dart := ⟨(u, y2), e.1⟩ with hDd
  set d1 := M.rotation.next.symm Dd with hd1
  set d3 := M.rotation.next Dd with hd3
  have n1 : M.rotation.next d1 = Dd := Equiv.apply_symm_apply _ _
  have g1 : d1.fst = u := by
    have := M.rotation.next_fst d1; rw [n1] at this; exact this.symm
  have g3 : d3.fst = u := M.rotation.next_fst Dd
  have a1 : M.Adj u d1.snd := g1 ▸ d1.adj
  have a3 : M.Adj u d3.snd := g3 ▸ d3.adj
  have E1 : (⟨(u, d1.snd), a1⟩ : M.Dart) = d1 := Dart.ext _ _ (Prod.ext g1.symm rfl)
  have E3 : (⟨(u, d3.snd), a3⟩ : M.Dart) = d3 := Dart.ext _ _ (Prod.ext g3.symm rfl)
  have r12 : M.rotation.next ⟨(u, d1.snd), a1⟩ = Dd := by rw [E1]; exact n1
  have r23 : M.rotation.next Dd = ⟨(u, d3.snd), a3⟩ := E3.symm
  have t1 : M.Adj y2 d1.snd := by
    have := face_third_adj htri d1.symm
    rw [show M.rotation.faceNext d1.symm = Dd by
      rw [RotationSystem.face_next_apply, Dart.symm_symm]; exact n1] at this
    exact this
  have t3 : M.Adj d3.snd y2 := by
    have := face_third_adj htri Dd.symm
    rw [show M.rotation.faceNext Dd.symm = d3 by
      rw [RotationSystem.face_next_apply, Dart.symm_symm]] at this
    exact this
  have hy1h : d1.snd ≠ h := fun e' => hzh (e' ▸ a1)
  have hy3h : d3.snd ≠ h := fun e' => hzh (e' ▸ a3)
  have act1 : Active h c (c (P.x j)) (c (P.x (j + 1))) d1.snd := by
    obtain ⟨n1', n2'⟩ := f4_third h34 az.2 ay.2 hzy (hc a1.symm hy1h az.1) (hc t1.symm hy1h ay.1)
    exact ⟨hy1h, f4_rest h34 h3 h13.symm h4 h14.symm h1.symm n1' n2'⟩
  have act3 : Active h c (c (P.x j)) (c (P.x (j + 1))) d3.snd := by
    obtain ⟨n1', n2'⟩ := f4_third h34 az.2 ay.2 hzy (hc a3.symm hy3h az.1) (hc t3 hy3h ay.1)
    exact ⟨hy3h, f4_rest h34 h3 h13.symm h4 h14.symm h1.symm n1' n2'⟩
  by_contra hno
  have in1 : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1))
      d1.snd := by
    by_contra hn; exact hno ⟨_, a1, act1, hn⟩
  have in3 : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1))
      d3.snd := by
    by_contra hn; exact hno ⟨_, a3, act3, hn⟩
  obtain ⟨q⟩ := in1.symm.trans in3
  have hle1 : pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1))) ≤ M.graph := fun _ _ e => e.1
  have hle2 : pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) ≤ M.graph :=
    fun _ _ e => e.1
  have hqz : u ∉ (q.mapLe hle1).support := by
    rw [Walk.support_mapLe_eq_support]
    exact fun hz => dis az (pair_support_active q act1 u hz)
  have hrz : u ∉ (r.mapLe hle2).support := by
    rw [Walk.support_mapLe_eq_support]; exact hzr
  obtain ⟨x, hx1, hx2⟩ := alternating_walks_intersect e0.1 a1 e.1 a3 hv0 r12 r23
    (r.mapLe hle2) hrz (q.mapLe hle1) hqz
  rw [Walk.support_mapLe_eq_support] at hx1 hx2
  exact dis (pair_support_active r e0.2.2 x hx1) (pair_support_active q act1 x hx2)

/-- **Fan lemma, `⇐`.** If `u` is coloured `A` or `B`, has a neighbour `k ∈ K_σ`, and some
`{α, μ}`-neighbour `v₀` of `u` lies outside `K_σ`, then `u` lies on an `{A, B}`-cycle. The face
boundary of the `{α, μ}`-component `S` of `v₀` is an even subgraph of the `{A, B}`-graph; the
faces at `u` through `v₀` meet `S` and the faces through `k` do not, so `u` has an edge in it. -/
theorem onCycle_of_escape (htri : M.Triangulated) (hr : RepeatAt P c j) {u k : Fin n}
    (huA : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) u) (hk : M.graph.Adj u k)
    (hkA : Active h c (c (P.x j)) (c (P.x (j + 1))) k)
    (hkK : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) k)
    (he : Escape P c j u) :
    OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) u := by
  obtain ⟨rj, rj2⟩ := triple_reach (P := P) hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨v0, hv0, hu, hnu⟩ := he
  set S : Fin n → Prop := fun v =>
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable v0 v with hS
  have actS : ∀ {v}, S v → Active h c (c (P.x j)) (c (P.x (j + 1))) v := by
    intro v hv
    by_cases e : v0 = v
    · exact e ▸ hu
    · exact reach_active hv e
  have linkS : ∀ i, ¬ S (P.x i) := by
    intro i hs
    rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
    · exact hnu (rj.trans hs.symm)
    · exact hnu hs.symm
    · exact hnu (rj2.trans hs.symm)
    · rcases (actS hs).2 with e | e
      · exact h3 e
      · exact h13 e.symm
    · rcases (actS hs).2 with e | e
      · exact h4 e
      · exact h14 e.symm
  have nbh : ∀ {v}, S v → ¬ M.Adj v h := by
    intro v hs e
    obtain ⟨i, rfl⟩ := P.only _ e.symm
    exact linkS i hs
  have col : ∀ {a b : Fin n}, (bdGraph M S).Adj a b →
      Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) a := by
    intro a b hb
    obtain ⟨haS, x, hx, e⟩ := bdGraph_out htri hb
    have hah : a ≠ h := by rintro rfl; exact nbh hx e.symm
    have n1 : c a ≠ c (P.x j) := fun hca =>
      haS (hx.trans (Adj.reachable ⟨e.symm, actS hx, hah, Or.inl hca⟩))
    have n2 : c a ≠ c (P.x (j + 1)) := fun hca =>
      haS (hx.trans (Adj.reachable ⟨e.symm, actS hx, hah, Or.inr hca⟩))
    exact ⟨hah, f4_rest h1.symm h3.symm h4.symm h13 h14 h34 n1 n2⟩
  have hle : bdGraph M S ≤ pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) :=
    fun a b hb => ⟨hb.fst, col hb, col hb.symm⟩
  have uS : ¬ S u := by
    intro hs
    have a := actS hs
    rcases huA.2 with e | e <;> rcases a.2 with f | f
    · exact h3 (e.symm.trans f)
    · exact h13 (f.symm.trans e)
    · exact h4 (e.symm.trans f)
    · exact h14 (f.symm.trans e)
  have kS : ¬ S k := fun hs => hnu (hkK.trans hs.symm)
  -- an edge of the boundary graph at `u`
  have hedge : ∃ v, (bdGraph M S).Adj u v := by
    by_contra hno
    push Not at hno
    have hsym : ∀ d : M.Dart, d.fst = u → (TriMeets M S d ↔ TriMeets M S d.symm) := by
      rintro ⟨⟨a, b⟩, e⟩ ha
      simp only at ha
      subst ha
      by_contra hb
      exact hno b ⟨e, hb⟩
    have hit : ∀ (t : ℕ) (d : M.Dart), d.fst = u →
        (TriMeets M S ((M.rotation.next : M.Dart → M.Dart)^[t] d) ↔ TriMeets M S d) := by
      intro t
      induction t with
      | zero => intro d _; rfl
      | succ t ih =>
        intro d hd
        rw [Function.iterate_succ_apply']
        have hf : ((M.rotation.next : M.Dart → M.Dart)^[t] d).fst = u := by
          clear ih
          induction t with
          | zero => exact hd
          | succ t ih' => rw [Function.iterate_succ_apply', M.rotation.next_fst]; exact ih'
        exact ((triMeets_symm htri S _).symm.trans (hsym _ hf).symm).trans (ih d hd)
    have d0 : TriMeets M S ⟨(u, v0), hv0⟩ := Or.inr (Or.inl (Reachable.refl v0))
    have dk : ¬ TriMeets M S ⟨(u, k), hk⟩ := by
      rintro (hs | hs | hs)
      · exact uS hs
      · exact kS hs
      · set t := (M.rotation.faceNext (⟨(u, k), hk⟩ : M.Dart)).snd
        have hkt : M.Adj k t := by
          have := (M.rotation.faceNext (⟨(u, k), hk⟩ : M.Dart)).adj
          rwa [M.rotation.face_next_fst] at this
        exact kS (hs.trans (Adj.reachable ⟨hkt.symm, actS hs, hkA⟩))
    obtain ⟨t, ht⟩ := M.rotation.cyclic (⟨(u, v0), hv0⟩ : M.Dart) ⟨(u, k), hk⟩ rfl
    have := hit t ⟨(u, v0), hv0⟩ rfl
    rw [ht] at this
    exact dk (this.2 d0)
  obtain ⟨v, huv⟩ := hedge
  obtain ⟨C, hC⟩ := cycle_of_even (bdGraph_even htri S) huv
  exact ⟨C.mapLe hle, hC.mapLe hle⟩

/-- **Fan lemma** (`NightW2.md` §8.1). For `u` off the link, coloured `A/B`, with a neighbour in
`K_σ`: `u` lies on an `{A, B}`-cycle of `T − h` iff some `{α, μ}`-neighbour of `u` lies outside
`K_σ`. -/
theorem fan_iff (htri : M.Triangulated) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    {u k : Fin n} (hu : ∀ i, u ≠ P.x i)
    (huA : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) u) (hk : M.graph.Adj u k)
    (hkA : Active h c (c (P.x j)) (c (P.x (j + 1))) k)
    (hkK : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) k) :
    OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) u ↔ Escape P c j u :=
  ⟨escape_of_onCycle htri hc hr hu, onCycle_of_escape htri hr huA hk hkA hkK⟩

/-- **W2′ at one state.** For `y, z` off the link, coloured `A/B`, with a common neighbour `k`
in `K_σ` (at `R3@k ≤ 2`: `k = m`): `y` or `z` lies on an `{A, B}`-cycle iff `y` or `z` has an
`{α, μ}`-neighbour outside `K_σ`. -/
theorem yz_cycle_iff_escape (htri : M.Triangulated) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) {y z k : Fin n} (hy : ∀ i, y ≠ P.x i) (hz : ∀ i, z ≠ P.x i)
    (hyA : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) y)
    (hzA : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) z)
    (hyk : M.graph.Adj y k) (hzk : M.graph.Adj z k)
    (hkA : Active h c (c (P.x j)) (c (P.x (j + 1))) k)
    (hkK : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) k) :
    (OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) y ∨
      OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) z) ↔
    (Escape P c j y ∨ Escape P c j z) := by
  rw [fan_iff htri hc hr hy hyA hyk hkA hkK, fan_iff htri hc hr hz hzA hzk hkA hkK]

/-! ### W2′ on the period (positions 4, 6, 8) -/

variable {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5} {s : Fin n → Fin 4} {j₀ : Fin 5}

variable (P w) in
/-- At a state with repeat index `j`: `y` or `z` lies on an `{A, B}`-cycle. -/
def CycleYZ (q : Fin 5) (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) (w (q + 4)) ∨
    OnCycle (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))) (w q)

variable (P w) in
/-- At a state with repeat index `j`: `y` or `z` escapes `K_σ`. -/
def EscapeYZ (q : Fin 5) (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  Escape P c j (w (q + 4)) ∨ Escape P c j (w q)


/-- **W2′, cycle form ⇔ escape form** (`NightW2.md` §8.2), over positions 4, 6, 8 of a period
(`N % 10 = 4`, repeat indices `j, j+1, j+2`). -/
theorem w2'_iff (htri : M.Triangulated) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀)
    {N : ℕ} (hN : N % 10 = 4) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j) :
    (CycleYZ P w q ((piMove P)^[N] s) j ∨ CycleYZ P w q ((piMove P)^[N + 2] s) (j + 1) ∨
      CycleYZ P w q ((piMove P)^[N + 4] s) (j + 2)) ↔
    (EscapeYZ P w q ((piMove P)^[N] s) j ∨ EscapeYZ P w q ((piMove P)^[N + 2] s) (j + 1) ∨
      EscapeYZ P w q ((piMove P)^[N + 4] s) (j + 2)) := by
  obtain ⟨hq2, hT2, hc4, e5, e6, e7, e8, K4, K5, K6, K7, hd4⟩ :=
    w2_setup H hc hall hr hq hT hN hj
  obtain ⟨-, ⟨cp4, cm4, cy4, cz4⟩, -, ⟨cp6, cm6, cy6, cz6⟩,
    -, ⟨cp8, cm8, cy8, cz8⟩, -, ⟨u0, u1, u3, u4⟩,
    -, ⟨f0, f1, f3, f4⟩, -, -, -, -, ⟨pr5, pr6, pr7, pr8⟩,
    ⟨rp5, rp6, rp7, rp8⟩⟩ :=
    chain_local H hq2 hc4 hj hT2 rfl rfl rfl rfl e5 e6 e7 e8 K4 K5 K6 K7
  subst hq2
  have pm := H.adj_m
  have ym : M.graph.Adj (w (j + 2 + 4)) m := H.ringy
  have zm : M.graph.Adj (w (j + 2)) m := H.ringz.symm
  have hy : ∀ i, w (j + 2 + 4) ≠ P.x i := fun i => H.off _ i
  have hz : ∀ i, w (j + 2) ≠ P.x i := fun i => H.off _ i
  have wh := H.offh
  have mh := H.offmh
  simp only [add_assoc, Fin.reduceAdd] at ym hy cy4
  unfold CycleYZ EscapeYZ
  simp only [add_assoc, Fin.reduceAdd, add_zero]
  have pm6 : M.graph.Adj (P.x (j + 1 + 1)) m := by simp only [add_assoc, Fin.reduceAdd]; exact pm
  -- position 4
  have i4 := yz_cycle_iff_escape (P := P) htri hc4 hj hy hz ⟨wh _, Or.inl cy4⟩
    ⟨wh _, Or.inr cz4⟩ ym zm ⟨mh, Or.inr cm4⟩
    ((triple_reach hj).2.trans (pgR pm (P.x_ne_h _) mh (Or.inl cp4) (Or.inr cm4)))
  -- position 6 (repeat index `j + 1`)
  have i6 := yz_cycle_iff_escape (P := P) (j := j + 1) htri pr6 rp6 hy hz
    ⟨wh _, Or.inr (by simp only [add_assoc, Fin.reduceAdd, add_zero]; rw [cy6, u0])⟩
    ⟨wh _, Or.inl (by simp only [add_assoc, Fin.reduceAdd]; rw [cz6, u4])⟩ ym zm
    ⟨mh, Or.inl (by rw [cm6, u1])⟩
    (pgR pm6 (P.x_ne_h _) mh (Or.inr rfl)
      (Or.inl (by rw [cm6, u1])))
  -- position 8 (repeat index `j + 2`)
  have i8 := yz_cycle_iff_escape (P := P) (j := j + 2) htri pr8 rp8 hy hz
    ⟨wh _, Or.inl (by simp only [add_assoc, Fin.reduceAdd, add_zero]; rw [cy8, f0])⟩
    ⟨wh _, Or.inr (by simp only [add_assoc, Fin.reduceAdd]; rw [cz8, f1])⟩ ym zm
    ⟨mh, Or.inr (by simp only [add_assoc, Fin.reduceAdd]; rw [cm8, f3])⟩
    ((triple_reach rp8).1.trans (pgR pm (P.x_ne_h _) mh (Or.inl rfl)
      (Or.inr (by simp only [add_assoc, Fin.reduceAdd]; rw [cm8, f3]))))
  simp only [add_assoc, Fin.reduceAdd, add_zero] at i4 i6 i8
  rw [i4, i6, i8]

/-- **W2′ ⇒ not all three fixed** (`NightW2.md` §8.2): no Lemma Fix and no duality needed. -/
theorem not_all_fixed_of_w2' {N : ℕ} {j : Fin 5}
    (hW : EscapeYZ P w q ((piMove P)^[N] s) j ∨ EscapeYZ P w q ((piMove P)^[N + 2] s) (j + 1) ∨
      EscapeYZ P w q ((piMove P)^[N + 4] s) (j + 2)) :
    ¬ (SigmaFixed P ((piMove P)^[N] s) j ∧ SigmaFixed P ((piMove P)^[N + 2] s) (j + 1) ∧
      SigmaFixed P ((piMove P)^[N + 4] s) (j + 2)) := by
  rintro ⟨f4, f6, f8⟩
  rcases hW with (e | e) | (e | e) | (e | e)
  · exact not_sigmaFixed_of_escape e f4
  · exact not_sigmaFixed_of_escape e f4
  · exact not_sigmaFixed_of_escape e f6
  · exact not_sigmaFixed_of_escape e f6
  · exact not_sigmaFixed_of_escape e f8
  · exact not_sigmaFixed_of_escape e f8

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.escape_of_onCycle
#print axioms SimpleGraph.QuarterFloor.onCycle_of_escape
#print axioms SimpleGraph.QuarterFloor.fan_iff
#print axioms SimpleGraph.QuarterFloor.yz_cycle_iff_escape
#print axioms SimpleGraph.QuarterFloor.not_sigmaFixed_of_escape
#print axioms SimpleGraph.QuarterFloor.w2'_iff
#print axioms SimpleGraph.QuarterFloor.not_all_fixed_of_w2'
