/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterJordanDual
public import Mathlib.Combinatorics.SimpleGraph.Acyclic

/-!
# Lemma Fix: `σ` is a fixed point iff the `{A, B}`-graph is a forest

Formalises §1 of `NightF012.md` (roles at `k ≤ 2`, the local `{A, B}`-path, and Lemma Fix).
Frame as in `QuarterSigmaExit`: link `(α, μ, α, A, B)` at `x j, …, x (j+4)`, and
`σ = sigSwap P c j` swaps `K_σ`, the `{α, μ}`-component of `x (j+1)`.

## Main results (sorry-free, no new axioms)

* `SigmaFixed P c j`: `K_σ` contains every vertex of `T − h` coloured `α` or `μ` (the note's
  "fixed point": `K_σ` is the whole `{α, μ}`-subgraph). `sigmaFixed_iff_sigSwap`: equivalently
  `σ` acts on `T − h` as the global transposition `α ↔ μ`, i.e. `σ(r) = r` up to colour names.
* `sigmaFixed_iff_acyclic` (**Lemma Fix**, general form): on a connected triangulated sphere,
  at any repeat state at `j`, `SigmaFixed P c j` iff the `{A, B}`-graph of `T − h`
  (`A = c (x (j+3))`, `B = c (x (j+4))`) is acyclic.
  - `acyclic_of_sigmaFixed` (a cycle kills the fixed point): no connectivity needed. At a cycle
    vertex `z` off the link, the two rotation neighbours `y₁, y₃` of the next cycle vertex `y₂`
    are `α/μ`-coloured (triangles `z y₁ y₂`, `z y₂ y₃`), and the Jordan lemma
    `alternating_walks_intersect` at `z` separates them by the cycle, so they lie in different
    `{α, μ}`-components.
  - `not_acyclic_of_not_sigmaFixed` (the duality direction): if an `α/μ` vertex `u` is outside
    `K_σ`, the face boundary of the `{α, μ}`-component `S` of `u` (the boundary-parity graph of
    `kempe_hex`) misses `h` and the link, consists of `{A, B}`-edges, has even degrees, and is
    nonempty (connectivity: faces at `u` meet `S`, faces at `h` do not). An even graph with an
    edge is not acyclic.
* `LowBall P w m j k` (`k ∈ {0, 1, 2}`): the 2-ball with `p = x (j+k)` of degree six, outer
  neighbours `y = w (j+k+4)`, `m`, `z = w (j+k)`, ring edges `w (t-1) w t` for `t ≠ k`.
* `low_roles` (**§1.1**): at `R3` with `k ≤ 2`, `{c p, c m} = {α, μ}`, `{c y, c z} = {A, B}`,
  and `p, m ∈ K_σ`.
* `low_path_k0/k1/k2` (**§1.2**): the explicit 6-vertex `{A, B}`-path from `y` to `z`:
  - `k = 0`: `w₄ x₄ x₃ w₂ w₁ w₀`;
  - `k = 1`: `w₀ w₄ x₄ x₃ w₂ w₁`;
  - `k = 2`: `w₁ w₀ w₄ x₄ x₃ w₂`.
* `lemmaFix` (**§1.3**): at `R3@k`, `k ≤ 2`, `σ` is a fixed point iff the
  `{c y, c z}`-graph of `T − h` is acyclic.

The hypothesis `M.graph.Connected` is needed only for the duality direction (a disconnected
`SphericalMap` could carry an extra `{α, μ}`-component with no `{A, B}`-cycle); it is not part
of `SphericalMap`. The planar helpers (`TriMeets`, `bdGraph`, `bdGraph_even`, `odd_iff_bd`) are
private in `QuarterJordanDual` and are copied verbatim below.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Private copies of the boundary-parity helpers of `QuarterJordanDual` -/

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

/-! ### Generic tools -/

section generic
variable {n : ℕ} {M : SphericalMap n}

open Classical in
/-- An even graph with an edge is not acyclic: the edge `u v` is not a bridge, since in the
graph with the edges at `u` removed the component of `v` has a second odd vertex, a neighbour
`w ≠ v` of `u`. -/
private lemma not_isAcyclic_of_even {G : SimpleGraph (Fin n)} (hev : ∀ x, Even (G.degree x))
    {u v : Fin n} (huv : G.Adj u v) : ¬ G.IsAcyclic := by
  intro hA
  have hm : Odd ((compKeep (offV G u) v).degree v) := by
    rw [odd_iff_bd _ hev]
    exact ⟨Reachable.refl _, huv.ne.symm, huv.symm⟩
  obtain ⟨w, hwv, hw⟩ := exists_ne_odd_degree_of_exists_odd_degree (h := hm)
  rw [odd_iff_bd _ hev] at hw
  obtain ⟨hr, hwu, hadj⟩ := hw
  have hB := isAcyclic_iff_forall_adj_isBridge.1 hA huv
  apply hB
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
  exact e1.reachable.trans (hr.mono hle).symm

/-- The third vertex of the (triangular) face of `d` is adjacent to `d.fst`. -/
private lemma face_third_adj (htri : M.Triangulated) (d : M.Dart) :
    M.Adj (M.rotation.faceNext d).snd d.fst := by
  have e1 := M.rotation.face_next_fst (M.rotation.faceNext d)
  have e2 := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
  rw [tri3 htri d] at e2
  have := (M.rotation.faceNext (M.rotation.faceNext d)).adj
  rw [e1, ← e2] at this
  exact this

/-- With no boundary edges, `TriMeets` is constant on darts at reachable vertices. -/
private lemma triMeets_const (htri : M.Triangulated) {S : Fin n → Prop}
    (hno : ∀ a b, ¬ (bdGraph M S).Adj a b) :
    ∀ {a b : Fin n} (_ : M.graph.Walk a b) (d d' : M.Dart), d.fst = a → d'.fst = b →
      (TriMeets M S d ↔ TriMeets M S d') := by
  have hsym : ∀ d : M.Dart, TriMeets M S d ↔ TriMeets M S d.symm := by
    rintro ⟨⟨a, b⟩, e⟩
    by_contra hb
    exact hno a b ⟨e, hb⟩
  have hnext : ∀ d : M.Dart, TriMeets M S (M.rotation.next d) ↔ TriMeets M S d :=
    fun d => (triMeets_symm htri S d).symm.trans (hsym d).symm
  have hit : ∀ (k : ℕ) (d : M.Dart), TriMeets M S ((M.rotation.next : M.Dart → M.Dart)^[k] d) ↔
      TriMeets M S d := by
    intro k
    induction k with
    | zero => intro d; rfl
    | succ k ih =>
      intro d
      rw [Function.iterate_succ_apply']
      exact (hnext _).trans (ih d)
  have hvert : ∀ d d' : M.Dart, d.fst = d'.fst → (TriMeets M S d ↔ TriMeets M S d') := by
    intro d d' hdd
    obtain ⟨k, hk⟩ := M.rotation.cyclic d d' hdd
    rw [← hk]
    exact (hit k d).symm
  intro a b p
  induction p with
  | nil => intro d d' h1 h2; exact hvert d d' (h1.trans h2.symm)
  | @cons a x b e p ih =>
    intro d d' h1 h2
    have e0 : TriMeets M S d ↔ TriMeets M S ⟨(a, x), e⟩ := hvert _ _ h1
    exact e0.trans ((hsym _).trans (ih _ d' rfl h2))

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

private lemma exists_mem_ne_ne {l : List (Fin n)} (hl : l.Nodup) (h3 : 3 ≤ l.length)
    (a b : Fin n) : ∃ z ∈ l, z ≠ a ∧ z ≠ b := by
  by_contra hcon
  push Not at hcon
  have hsub : l.toFinset ⊆ {a, b} := fun z hz => by
    rw [List.mem_toFinset] at hz
    by_cases ha : z = a
    · simp [ha]
    · simp [hcon z hz ha]
  have h1 := Finset.card_le_card hsub
  rw [List.toFinset_card_of_nodup hl] at h1
  have h2 : ({a, b} : Finset (Fin n)).card ≤ 2 := Finset.card_le_two
  omega

end generic

lemma f4_third {A B a b x : Fin 4} (hAB : A ≠ B) (ha : a = A ∨ a = B) (hb : b = A ∨ b = B)
    (hab : a ≠ b) (hxa : x ≠ a) (hxb : x ≠ b) : x ≠ A ∧ x ≠ B := by
  revert A B a b x; decide


private lemma fin5_ne (j : Fin 5) : j + 4 ≠ j + 2 ∧ j + 4 ≠ j + 1 ∧ j + 4 ≠ j ∧ j + 2 ≠ j + 1 ∧
    j + 2 ≠ j ∧ j + 1 ≠ j ∧ j + 4 ≠ j + 3 := by
  revert j; decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

variable (P : Pent M.graph h) in
/-- **`σ` is a fixed point** (`NightF012.md`, Frame): `K_σ`, the `{α, μ}`-component of
`x (j+1)` with `α = c (x j)`, `μ = c (x (j+1))`, contains every vertex of `T − h` coloured `α`
or `μ`, i.e. it is the whole `{α, μ}`-subgraph. -/
def SigmaFixed (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  ∀ v, Active h c (c (P.x j)) (c (P.x (j + 1))) v →
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) v

variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {c : Fin n → Fin 4} {j : Fin 5}

/-- `SigmaFixed` says exactly that `σ` acts on `T − h` as the global colour transposition
`α ↔ μ`, so `σ(r) = r` as a state up to the names of the colours. -/
theorem sigmaFixed_iff_sigSwap (hr : RepeatAt P c j) :
    SigmaFixed P c j ↔
      ∀ v, v ≠ h → sigSwap P c j v = Equiv.swap (c (P.x j)) (c (P.x (j + 1))) (c v) := by
  have h1 := hr.2.1
  unfold sigSwap kswap SigmaFixed
  constructor
  · intro hf v _
    by_cases hv : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) v
    · exact swap_in hv
    · rw [swap_out (S := {x | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) x}) hv]
      have n1 : c v ≠ c (P.x j) := fun e => hv (hf v ⟨fun e' => ?_, Or.inl e⟩)
      · have n2 : c v ≠ c (P.x (j + 1)) := fun e => hv (hf v ⟨fun e' => ?_, Or.inr e⟩)
        · exact (Equiv.swap_apply_of_ne_of_ne n1 n2).symm
        · rename_i hvh; exact hvh e'
      · rename_i hvh; exact hvh e'
  · intro H v hv
    by_contra hn
    have := H v hv.1
    rw [swap_out (S := {x | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) x}) hn] at this
    rcases hv.2 with e | e
    · rw [e, Equiv.swap_apply_left] at this
      exact h1 this.symm
    · rw [e, Equiv.swap_apply_right] at this
      exact h1 this

/-- **Lemma Fix, `⇒`** (a cycle kills the fixed point). If `K_σ` is the whole
`{α, μ}`-subgraph, the `{A, B}`-graph of `T − h` has no cycle. A cycle has a vertex `z` off the
link; with `y₂` its successor on the cycle, the rotation neighbours `y₁, y₃` of `y₂` at `z` are
`α/μ`-coloured, and an `{α, μ}`-walk `y₁ → y₃` would cross the cycle at `z`
(`alternating_walks_intersect`). -/
theorem acyclic_of_sigmaFixed (htri : M.Triangulated) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hf : SigmaFixed P c j) :
    (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))).IsAcyclic := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have dis : ∀ {x}, Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) x →
      Active h c (c (P.x j)) (c (P.x (j + 1))) x → False := by
    rintro x ⟨-, e | e⟩ ⟨-, f | f⟩
    · exact h3 (e.symm.trans f)
    · exact h13 (f.symm.trans e)
    · exact h4 (e.symm.trans f)
    · exact h14 (f.symm.trans e)
  intro z0 C hC
  obtain ⟨z, hzt, hz3, hz4⟩ := exists_mem_ne_ne hC.support_nodup
    (by rw [List.length_tail, Walk.length_support]; have := hC.three_le_length; omega)
    (P.x (j + 3)) (P.x (j + 4))
  have hzs : z ∈ C.support := List.mem_of_mem_tail hzt
  obtain ⟨y2, v0, e, e0, r, hv0, hzr⟩ := cycle_split (C.rotate z hzs) (hC.rotate hzs)
  have az := e.2.1
  have ay := e.2.2
  have hzy : c z ≠ c y2 := hc e.1 az.1 ay.1
  have hzh : ¬ M.Adj z h := by
    intro hzh'
    obtain ⟨i, rfl⟩ := P.only _ hzh'.symm
    rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
    · rcases az.2 with f | f
      · exact h3 f.symm
      · exact h4 f.symm
    · rcases az.2 with f | f
      · exact h13 f
      · exact h14 f
    · rcases az.2 with f | f
      · exact h3 (h02.trans f).symm
      · exact h4 (h02.trans f).symm
    · exact hz3 rfl
    · exact hz4 rfl
  -- the rotation neighbours of `y₂` at `z`
  set Dd : M.Dart := ⟨(z, y2), e.1⟩ with hDd
  set d1 := M.rotation.next.symm Dd with hd1
  set d3 := M.rotation.next Dd with hd3
  have n1 : M.rotation.next d1 = Dd := Equiv.apply_symm_apply _ _
  have g1 : d1.fst = z := by
    have := M.rotation.next_fst d1; rw [n1] at this; exact this.symm
  have g3 : d3.fst = z := M.rotation.next_fst Dd
  have a1 : M.Adj z d1.snd := g1 ▸ d1.adj
  have a3 : M.Adj z d3.snd := g3 ▸ d3.adj
  have E1 : (⟨(z, d1.snd), a1⟩ : M.Dart) = d1 := Dart.ext _ _ (Prod.ext g1.symm rfl)
  have E3 : (⟨(z, d3.snd), a3⟩ : M.Dart) = d3 := Dart.ext _ _ (Prod.ext g3.symm rfl)
  have r12 : M.rotation.next ⟨(z, d1.snd), a1⟩ = Dd := by rw [E1]; exact n1
  have r23 : M.rotation.next Dd = ⟨(z, d3.snd), a3⟩ := E3.symm
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
  obtain ⟨q⟩ := (hf _ act1).symm.trans (hf _ act3)
  have hle1 : pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1))) ≤ M.graph := fun _ _ e => e.1
  have hle2 : pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) ≤ M.graph :=
    fun _ _ e => e.1
  have hqz : z ∉ (q.mapLe hle1).support := by
    rw [Walk.support_mapLe_eq_support]
    exact fun hz => dis az (pair_support_active q act1 z hz)
  have hrz : z ∉ (r.mapLe hle2).support := by
    rw [Walk.support_mapLe_eq_support]; exact hzr
  obtain ⟨x, hx1, hx2⟩ := alternating_walks_intersect e0.1 a1 e.1 a3 hv0 r12 r23
    (r.mapLe hle2) hrz (q.mapLe hle1) hqz
  rw [Walk.support_mapLe_eq_support] at hx1 hx2
  exact dis (pair_support_active r e0.2.2 x hx1) (pair_support_active q act1 x hx2)

/-- **Lemma Fix, `⇐`** (the duality direction). If some `α/μ` vertex `u` is outside `K_σ`, the
face boundary of the `{α, μ}`-component of `u` is a nonempty even subgraph of the
`{A, B}`-graph of `T − h`, hence that graph has a cycle. -/
theorem not_acyclic_of_not_sigmaFixed (htri : M.Triangulated) (hconn : M.graph.Connected)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) (hn : ¬ SigmaFixed P c j) :
    ¬ (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))).IsAcyclic := by
  obtain ⟨rj, rj2⟩ := triple_reach (P := P) hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  simp only [SigmaFixed, not_forall] at hn
  obtain ⟨u, hu, hnu⟩ := hn
  set S : Fin n → Prop := fun v =>
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable u v with hS
  have actS : ∀ {v}, S v → Active h c (c (P.x j)) (c (P.x (j + 1))) v := by
    intro v hv
    by_cases e : u = v
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
  have hSh : ¬ S h := fun hs => (actS hs).1 rfl
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
  have hedge : ∃ a b, (bdGraph M S).Adj a b := by
    by_contra hno
    push Not at hno
    obtain ⟨p⟩ := hconn.preconnected u h
    cases p with
    | nil => exact hu.1 rfl
    | cons e p =>
      have key := triMeets_const htri hno (Walk.cons e p) ⟨(u, _), e⟩
        ⟨(h, P.x j), P.adj_h j⟩ rfl rfl
      have hT : TriMeets M S ⟨(u, _), e⟩ := Or.inl (Reachable.refl u)
      rcases key.1 hT with hh | hx | ht
      · exact hSh hh
      · exact linkS j hx
      · exact nbh ht (face_third_adj htri _)
  obtain ⟨a, b, hab⟩ := hedge
  exact fun hA => not_isAcyclic_of_even (bdGraph_even htri S) hab (hA.anti hle)

/-- **Lemma Fix** (general form, any repeat state at `j`): on a connected triangulated sphere,
`σ` is a fixed point iff the `{A, B}`-graph of `T − h` is acyclic. -/
theorem sigmaFixed_iff_acyclic (htri : M.Triangulated) (hconn : M.graph.Connected)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    SigmaFixed P c j ↔
      (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))).IsAcyclic :=
  ⟨acyclic_of_sigmaFixed htri hc hr, fun hA => by
    by_contra hn
    exact not_acyclic_of_not_sigmaFixed htri hconn hc hr hn hA⟩

/-! ### The roles at `k ≤ 2` (`NightF012.md` §1.1–§1.2) -/

variable (P w) in
/-- The `k ≤ 2` ball at the frame `j`, with `w (j+t)` the outer vertex `wₜ` of the frame
(`(w₀..w₄) = (B, A, B, μ, A)` at `R3`). The degree-six link vertex is `p = x (j+k)`, with
rotation `h, x (j+k-1), y, m, z, x (j+k+1)`, where `y = w (j+k-1)` and `z = w (j+k)`; every
other link vertex has degree five. The faces around the link give the spokes `x t – w t` and
`x (t+1) – w t` for every `t`, and the ring edges `w (t-1) – w t` for `t ≠ k` (at `t = k` the
ring passes through `m` instead: `y – m – z`). -/
structure LowBall (m : Fin n) (j k : Fin 5) : Prop where
  hk : k = 0 ∨ k = 1 ∨ k = 2
  nbrp : ∀ u, M.graph.Adj (P.x (j + k)) u ↔ u = h ∨ u = P.x (j + k + 4) ∨ u = w (j + k + 4) ∨
    u = m ∨ u = w (j + k) ∨ u = P.x (j + k + 1)
  spoke : ∀ t, M.graph.Adj (P.x (j + t)) (w (j + t)) ∧ M.graph.Adj (P.x (j + t + 1)) (w (j + t))
  ring : ∀ t, t ≠ k → M.graph.Adj (w (j + t + 4)) (w (j + t))
  ringm : M.graph.Adj (w (j + k + 4)) m ∧ M.graph.Adj m (w (j + k))
  winj : Function.Injective w
  off : ∀ t i, w t ≠ P.x i
  offh : ∀ t, w t ≠ h
  mh : m ≠ h

/-- **Roles at `k ≤ 2`** (§1.1). At `R3@k`, `k ≤ 2`: `p = x (j+k)` and `m` carry `α` and `μ`
(in some order), `y = w (j+k-1)` and `z = w (j+k)` carry `A` and `B` (in some order), and
`p, m ∈ K_σ`. Explicitly: `k = 0`: `(p, m, y, z) = (α, μ, A, B)`; `k = 1`: `(μ, α, B, A)`;
`k = 2`: `(α, μ, A, B)`. -/
theorem low_roles (L : LowBall P w m j k) (hc : ProperOff M.graph h c) (hR : R3At P w c j) :
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) (P.x (j + k)) ∧
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) m ∧
    ((c (P.x (j + k)) = c (P.x j) ∧ c m = c (P.x (j + 1))) ∨
      (c (P.x (j + k)) = c (P.x (j + 1)) ∧ c m = c (P.x j))) ∧
    ((c (w (j + k + 4)) = c (P.x (j + 3)) ∧ c (w (j + k)) = c (P.x (j + 4))) ∨
      (c (w (j + k + 4)) = c (P.x (j + 4)) ∧ c (w (j + k)) = c (P.x (j + 3)))) := by
  have hr := hR.1.1
  obtain ⟨rj, rj2⟩ := triple_reach (P := P) hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨-, c0, c1, c2, -, c4⟩ := hR
  have pm : M.Adj (P.x (j + k)) m := (L.nbrp m).2 (by simp)
  obtain ⟨ym, mz⟩ := L.ringm
  have offh := L.offh
  have mh := L.mh
  have reachm : ∀ {i : Fin 5}, (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable
      (P.x (j + 1)) (P.x i) → (c (P.x i) = c (P.x j) ∨ c (P.x i) = c (P.x (j + 1))) →
      M.Adj (P.x i) m → (c m = c (P.x j) ∨ c m = c (P.x (j + 1))) →
      (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) m :=
    fun r a e b => r.trans (Adj.reachable ⟨e, ⟨P.x_ne_h _, a⟩, ⟨mh, b⟩⟩)
  rcases L.hk with rfl | rfl | rfl <;>
    simp only [add_zero, add_assoc, Fin.reduceAdd] at pm ym mz ⊢
  · -- k = 0: p = x j (α), y = w₄ (A), z = w₀ (B), m = μ
    have cm : c m = c (P.x (j + 1)) := by
      rcases f4_rest h34 h3 h13.symm h4 h14.symm h1.symm
        (by rw [← c4]; exact hc ym.symm mh (offh _))
        (by rw [← c0]; exact hc mz mh (offh _)) with e | e
      · exact absurd e (hc pm.symm mh (P.x_ne_h _))
      · exact e
    exact ⟨rj, reachm rj (Or.inl rfl) pm (Or.inr cm), Or.inl ⟨trivial, cm⟩,
      Or.inl ⟨c4, c0⟩⟩
  · -- k = 1: p = x (j+1) (μ), y = w₀ (B), z = w₁ (A), m = α
    have cm : c m = c (P.x j) := by
      rcases f4_rest h34 h3 h13.symm h4 h14.symm h1.symm
        (by rw [← c1]; exact hc mz mh (offh _))
        (by rw [← c0]; exact hc ym.symm mh (offh _)) with e | e
      · exact e
      · exact absurd e (hc pm.symm mh (P.x_ne_h _))
    exact ⟨Reachable.refl _, reachm (Reachable.refl _) (Or.inr rfl) pm (Or.inl cm),
      Or.inr ⟨trivial, cm⟩, Or.inr ⟨c0, c1⟩⟩
  · -- k = 2: p = x (j+2) (α), y = w₁ (A), z = w₂ (B), m = μ
    have cm : c m = c (P.x (j + 1)) := by
      rcases f4_rest h34 h3 h13.symm h4 h14.symm h1.symm
        (by rw [← c1]; exact hc ym.symm mh (offh _))
        (by rw [← c2]; exact hc mz mh (offh _)) with e | e
      · exact absurd (e.trans h02) (hc pm.symm mh (P.x_ne_h _))
      · exact e
    exact ⟨rj2, reachm rj2 (Or.inl h02.symm) pm (Or.inr cm), Or.inl ⟨h02.symm, cm⟩,
      Or.inl ⟨c1, c2⟩⟩

/-- The six vertices `w₄, x₄, x₃, w₂, w₁, w₀` of the `{A, B}`-hexagon are distinct. -/
lemma LowBall.hex_nodup (L : LowBall P w m j k) :
    [w (j + 4), P.x (j + 4), P.x (j + 3), w (j + 2), w (j + 1), w j].Nodup := by
  obtain ⟨f1, f2, f3, f4, f5, f6, f7⟩ := fin5_ne j
  have hw : ∀ {a b : Fin 5}, a ≠ b → w a ≠ w b := fun hab e => hab (L.winj e)
  have hx : P.x (j + 4) ≠ P.x (j + 3) := fun e => f7 (P.inj e)
  have o := L.off
  simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false,
    not_or, List.nodup_nil, and_true]
  exact ⟨⟨o _ _, o _ _, hw f1, hw f2, hw f3⟩, ⟨hx, (o _ _).symm, (o _ _).symm, (o _ _).symm⟩,
    ⟨(o _ _).symm, (o _ _).symm, (o _ _).symm⟩, ⟨hw f4, hw f5⟩, ⟨hw f6, not_false⟩⟩

/-- The local `{A, B}`-path at `k = 0` (§1.2): `y = w₄, x₄, x₃, w₂, w₁, w₀ = z`. -/
theorem low_path_k0 (L : LowBall P w m j 0) (hR : R3At P w c j) :
    ∃ q : (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))).Walk (w (j + 4)) (w j),
      q.IsPath ∧ q.support = [w (j + 4), P.x (j + 4), P.x (j + 3), w (j + 2), w (j + 1), w j] := by
  obtain ⟨-, c0, c1, c2, -, c4⟩ := hR
  have aw4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 4)) := ⟨L.offh _, Or.inl c4⟩
  have aw2 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 2)) := ⟨L.offh _, Or.inr c2⟩
  have aw1 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 1)) := ⟨L.offh _, Or.inl c1⟩
  have aw0 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w j) := ⟨L.offh _, Or.inr c0⟩
  have ax3 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 3)) :=
    ⟨P.x_ne_h _, Or.inl rfl⟩
  have ax4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 4)) :=
    ⟨P.x_ne_h _, Or.inr rfl⟩
  have e44 := (L.spoke 4).1
  have e43 := P.adj_cyc (j + 3)
  have e32 := (L.spoke 2).2
  have e21 := L.ring 2 (by decide)
  have e10 := L.ring 1 (by decide)
  simp only [add_zero, add_assoc, Fin.reduceAdd] at e43 e32 e21 e10
  refine ⟨.cons ⟨e44.symm, aw4, ax4⟩ (.cons ⟨e43.symm, ax4, ax3⟩ (.cons ⟨e32, ax3, aw2⟩
    (.cons ⟨e21.symm, aw2, aw1⟩ (.cons ⟨e10.symm, aw1, aw0⟩ .nil)))), ?_, rfl⟩
  rw [Walk.isPath_def]
  exact L.hex_nodup

/-- The local `{A, B}`-path at `k = 1` (§1.2): `y = w₀, w₄, x₄, x₃, w₂, w₁ = z`. -/
theorem low_path_k1 (L : LowBall P w m j 1) (hR : R3At P w c j) :
    ∃ q : (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))).Walk (w j) (w (j + 1)),
      q.IsPath ∧ q.support = [w j, w (j + 4), P.x (j + 4), P.x (j + 3), w (j + 2), w (j + 1)] := by
  obtain ⟨-, c0, c1, c2, -, c4⟩ := hR
  have aw4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 4)) := ⟨L.offh _, Or.inl c4⟩
  have aw2 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 2)) := ⟨L.offh _, Or.inr c2⟩
  have aw1 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 1)) := ⟨L.offh _, Or.inl c1⟩
  have aw0 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w j) := ⟨L.offh _, Or.inr c0⟩
  have ax3 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 3)) :=
    ⟨P.x_ne_h _, Or.inl rfl⟩
  have ax4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 4)) :=
    ⟨P.x_ne_h _, Or.inr rfl⟩
  have e44 := (L.spoke 4).1
  have e43 := P.adj_cyc (j + 3)
  have e32 := (L.spoke 2).2
  have e21 := L.ring 2 (by decide)
  have e04 := L.ring 0 (by decide)
  simp only [add_zero, add_assoc, Fin.reduceAdd] at e43 e32 e21 e04
  refine ⟨.cons ⟨e04.symm, aw0, aw4⟩ (.cons ⟨e44.symm, aw4, ax4⟩ (.cons ⟨e43.symm, ax4, ax3⟩
    (.cons ⟨e32, ax3, aw2⟩ (.cons ⟨e21.symm, aw2, aw1⟩ .nil)))), ?_, rfl⟩
  rw [Walk.isPath_def]
  exact ((List.rotate_perm _ 5).nodup_iff).2 L.hex_nodup

/-- The local `{A, B}`-path at `k = 2` (§1.2): `y = w₁, w₀, w₄, x₄, x₃, w₂ = z`. -/
theorem low_path_k2 (L : LowBall P w m j 2) (hR : R3At P w c j) :
    ∃ q : (pairGraph M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4)))).Walk (w (j + 1)) (w (j + 2)),
      q.IsPath ∧ q.support = [w (j + 1), w j, w (j + 4), P.x (j + 4), P.x (j + 3), w (j + 2)] := by
  obtain ⟨-, c0, c1, c2, -, c4⟩ := hR
  have aw4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 4)) := ⟨L.offh _, Or.inl c4⟩
  have aw2 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 2)) := ⟨L.offh _, Or.inr c2⟩
  have aw1 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w (j + 1)) := ⟨L.offh _, Or.inl c1⟩
  have aw0 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (w j) := ⟨L.offh _, Or.inr c0⟩
  have ax3 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 3)) :=
    ⟨P.x_ne_h _, Or.inl rfl⟩
  have ax4 : Active h c (c (P.x (j + 3))) (c (P.x (j + 4))) (P.x (j + 4)) :=
    ⟨P.x_ne_h _, Or.inr rfl⟩
  have e44 := (L.spoke 4).1
  have e43 := P.adj_cyc (j + 3)
  have e32 := (L.spoke 2).2
  have e10 := L.ring 1 (by decide)
  have e04 := L.ring 0 (by decide)
  simp only [add_zero, add_assoc, Fin.reduceAdd] at e43 e32 e10 e04
  refine ⟨.cons ⟨e10.symm, aw1, aw0⟩ (.cons ⟨e04.symm, aw0, aw4⟩ (.cons ⟨e44.symm, aw4, ax4⟩
    (.cons ⟨e43.symm, ax4, ax3⟩ (.cons ⟨e32, ax3, aw2⟩ .nil)))), ?_, rfl⟩
  rw [Walk.isPath_def]
  exact ((List.rotate_perm _ 4).nodup_iff).2 L.hex_nodup

/-- **Lemma Fix** (§1.3, `NightF012.md`). At `R3@k` with `k ≤ 2`, on a connected triangulated
sphere: `σ` is a fixed point (`K_σ` is the whole `{α, μ}`-subgraph of `T − h`) iff the
`{c y, c z}`-graph of `T − h` is acyclic, where `y = w (j+k-1)`, `z = w (j+k)`. These two are
always joined by the 6-vertex path of `low_path_k0/k1/k2`; a fixed point means that path is
the only `y`–`z` route and there is no `{A, B}`-cycle anywhere. -/
theorem lemmaFix (htri : M.Triangulated) (hconn : M.graph.Connected)
    (hc : ProperOff M.graph h c) (hR : R3At P w c j) (L : LowBall P w m j k) :
    SigmaFixed P c j ↔
      (pairGraph M.graph h c (c (w (j + k + 4))) (c (w (j + k)))).IsAcyclic := by
  rw [sigmaFixed_iff_acyclic htri hconn hc hR.1.1]
  rcases (low_roles L hc hR).2.2.2 with ⟨e1, e2⟩ | ⟨e1, e2⟩
  · rw [e1, e2]
  · rw [e1, e2, pairGraph_comm_gen]

end sphere

end SimpleGraph.QuarterFloor
