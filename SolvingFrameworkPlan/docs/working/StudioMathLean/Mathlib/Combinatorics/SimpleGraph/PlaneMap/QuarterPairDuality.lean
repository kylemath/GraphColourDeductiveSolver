/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterEuler

/-!
# Exact pair dualities on a triangulated sphere and at a degree-five hole

Formalises `NightW2Euler.md` §1 ("Proved by hand"). Everything is proved outright from
Euler's formula and the rotation-system face structure; **no hypothesis is assumed**.

## Main results (sorry-free, no new axioms)

* `sphere_pair_duality` (Lemma D): for a proper 4-colouring of a connected triangulated
  sphere and complementary pairs `{a, b} ⊔ {p, q}`, `r(G_ab) = C(G_pq) − 1`, where
  `r = E − V + C` (`sRank`) and `C` counts components (`sComps`).
* `pair_dualities` (hole version): at a repeat state `α μ α A B` of a degree-five hole `h`
  of a connected triangulated sphere, in `T − h`:
  - `r(AB) = C(αμ) − 1`, `r(αμ) = C(AB) − 1`;
  - `r(μA) = C(αB) − 1 − [Lock1]`, `r(αB) = C(μA) − 1 − [¬Lock1]`;
  - `r(μB) = C(αA) − 1 − [Lock2]`, `r(αA) = C(μB) − 1 − [¬Lock2]`.
* `reach_alpha_B_of_not_lock1`, `reach_alpha_A_of_not_lock2`: the converses of `NoFrozen`'s
  `not_reach_alpha_B_of_lock1` / `not_reach_alpha_A_of_lock2` (Kempe duality at the link, by
  the boundary-parity handshake of `kempe_hex`). So `[Lock1] = [x j ↛ x (j+2) in {α, B}]`.
* `sigmaFixed_iff_C_alpha_mu_one`: `σ` fixed ⇔ `C(αμ) = 1` (no planarity);
  `sigmaFixed_iff_rank_AB_zero`: ⇔ `r(AB) = 0` (Lemma Fix in rank form).
* `six_pair_identity_from_dualities`: summing the six formulas gives `Σ r = Σ C − 8`.
* `sphere_six_pair_identity`: `Σ r = Σ C − 6` on the sphere.

## Method (no completion of the hole is built)

Over `ZMod 2`, for complementary pairs `{a, b}`, `{p, q}`:

* **Upper bound on cycles** (`finrank_ker_le`): the cycle space `ker ∂` of the `{a, b}`-graph
  has dimension at most `E − V + C` (walks to a root give `V − C` independent incidence
  vectors, and rank–nullity).
* **Lower bound on cycles** (`card_le_finrank_ker`): every triangle meets at most one
  `{p, q}`-component (its `{p, q}`-corners are adjacent). For a set `Q` of components, the
  dart function "value of the component the triangle meets" is constant on triangles, and on
  every non-`{a, b}` edge the two sides agree (one endpoint is a shared `{p, q}`-vertex, or an
  endpoint is `h` and both triangles meet only link components, which are kept out of `Q`).
  Its boundary is therefore a cycle of the `{a, b}`-graph (`inc_bd_zero`, a `next`/`symm`
  reindexing over darts), and the map is injective: a zero boundary makes the dart function
  constant (`dart_const`, connectivity), hence zero.
* Taking `Q` = all `{p, q}`-components except those through the link (hole), or except one
  (sphere), gives `C_pq − #(link components) ≤ r_ab` (`hole_lower`, `sphere_lower`). The
  link components are counted by hand: one or two, the second exactly under the lock
  (`bound_AB` … `bound_αA`, using the Kempe duality above).
* The six lower bounds add up to `Σ C − 8` (resp. `Σ C − 6`), which equals `Σ r` by
  `six_pair_rank_identity` (resp. `sphere_six_pair_identity`), so all six are equalities.

The boundary-parity helpers are private in `QuarterJordanDual` and are copied verbatim below;
`QuarterSigmaFix` cannot be imported alongside `QuarterEuler`, so `SigmaFixedE` restates its
`SigmaFixed` verbatim.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap Module

/-! ### Private copies of the boundary-parity helpers of `QuarterJordanDual` -/

section copied
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} (P : Pent M.graph h)

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

end copied

/-! ### Two-colour subgraphs off a removed vertex set, and their cycle spaces over `ZMod 2` -/

section generic
variable {n : ℕ} (M : SphericalMap n) (R : Fin n → Prop) (c : Fin n → Fin 4)

/-- A vertex outside the removed set `R` coloured `a` or `b`. -/
def KAct (a b : Fin 4) (v : Fin n) : Prop := ¬ R v ∧ (c v = a ∨ c v = b)

open Classical in
/-- The `{a, b}`-edges of `T` avoiding `R`. -/
noncomputable def kEdges (a b : Fin 4) : Finset (Sym2 (Fin n)) :=
  M.graph.edgeFinset.filter fun e => (∀ v ∈ e, ¬ R v) ∧ e.map c = s(a, b)

open Classical in
/-- The `{a, b}`-vertices off `R`. -/
noncomputable def kVertsFin (a b : Fin 4) : Finset (Fin n) := Finset.univ.filter (KAct R c a b)

/-- `v` is a corner of the triangle of the dart `d`. -/
def OnTri (d : M.Dart) (v : Fin n) : Prop :=
  v = d.fst ∨ v = d.snd ∨ v = (M.rotation.faceNext d).snd

/-- The triangle of `d` meets the component `K` of `H` in an `{a, b}`-vertex off `R`. -/
def Meets (H : SimpleGraph (Fin n)) (a b : Fin 4) (d : M.Dart) (K : H.ConnectedComponent) :
    Prop :=
  ∃ v, OnTri M d v ∧ KAct R c a b v ∧ H.connectedComponentMk v = K

open Classical in
/-- The incidence map of the `{a, b}`-edges, over `ZMod 2`. Its kernel is the cycle space. -/
noncomputable def incK (a b : Fin 4) :
    (kEdges M R c a b → ZMod 2) →ₗ[ZMod 2] (Fin n → ZMod 2) where
  toFun φ x := ∑ e : kEdges M R c a b, if x ∈ e.1 then φ e else 0
  map_add' φ ψ := by
    funext x
    simp only [Pi.add_apply, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp
  map_smul' r φ := by
    funext x
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp

open Classical in
/-- A dart function from a function on some components of `H`: a triangle gets the value of
the component it meets (each triangle meets at most one, see `faceFn_of`). -/
noncomputable def faceFn (H : SimpleGraph (Fin n)) (a b : Fin 4) (Q : Finset H.ConnectedComponent) :
    (Q → ZMod 2) →ₗ[ZMod 2] (M.Dart → ZMod 2) where
  toFun Y d := ∑ K : Q, if Meets M R c H a b d K.1 then Y K else 0
  map_add' φ ψ := by
    funext x
    simp only [Pi.add_apply, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp
  map_smul' r φ := by
    funext x
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp

open Classical in
/-- The boundary of a dart function, restricted to the `{a, b}`-edges. -/
noncomputable def bdLin (a b : Fin 4) :
    (M.Dart → ZMod 2) →ₗ[ZMod 2] (kEdges M R c a b → ZMod 2) where
  toFun X e := ∑ d : M.Dart, if d.edge = e.1 then X d else 0
  map_add' φ ψ := by
    funext x
    simp only [Pi.add_apply, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp
  map_smul' r φ := by
    funext x
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.mul_sum]
    refine Finset.sum_congr rfl fun e _ => ?_
    split_ifs <;> simp

variable {M R c}

lemma zmod2_eq_of_add {x y : ZMod 2} (hxy : x + y = 0) : x = y := by
  revert x y; decide

lemma zmod2_add3 (x y z : ZMod 2) : (x + y) + (y + z) = x + z := by
  revert x y z; decide

lemma dart_edge_eq (d : M.Dart) : d.edge = s(d.fst, d.snd) := rfl

lemma sum_edge_dart (X : M.Dart → ZMod 2) (d : M.Dart) :
    (∑ d' : M.Dart, if d'.edge = d.edge then X d' else 0) = X d + X d.symm := by
  classical
  have hne : d ≠ d.symm := (Dart.symm_ne d).symm
  have key : ∀ d' : M.Dart, (if d'.edge = d.edge then X d' else 0) =
      (if d' = d then X d' else 0) + (if d' = d.symm then X d' else 0) := by
    intro d'
    by_cases h1 : d' = d
    · subst h1; simp [hne]
    · by_cases h2 : d' = d.symm
      · subst h2; simp [h1]
      · simp [dart_edge_eq_iff, h1, h2]
  rw [Finset.sum_congr rfl fun d' _ => key d', Finset.sum_add_distrib]
  simp

/-- A dart function constant on triangles and on edges is constant (connected map). -/
lemma dart_const (hconn : M.graph.Connected) (X : M.Dart → ZMod 2)
    (hX : ∀ d, X (M.rotation.faceNext d) = X d) (hs : ∀ d, X d.symm = X d) (d d' : M.Dart) :
    X d = X d' := by
  have hnext : ∀ e : M.Dart, X (M.rotation.next e) = X e := by
    intro e
    have h1 : M.rotation.next e = M.rotation.faceNext e.symm := by
      rw [RotationSystem.face_next_apply, Dart.symm_symm]
    rw [h1, hX, hs]
  have hiter : ∀ (k : ℕ) (e : M.Dart),
      X ((M.rotation.next : M.Dart → M.Dart)^[k] e) = X e := by
    intro k
    induction k with
    | zero => intro e; rfl
    | succ k ih => intro e; rw [Function.iterate_succ_apply', hnext, ih]
  have hvert : ∀ e e' : M.Dart, e.fst = e'.fst → X e = X e' := by
    intro e e' h
    obtain ⟨k, hk⟩ := M.rotation.cyclic e e' h
    rw [← hk, hiter]
  have hwalk : ∀ (u v : Fin n) (p : M.graph.Walk u v) (e e' : M.Dart),
      e.fst = u → e'.fst = v → X e = X e' := by
    intro u v p
    induction p with
    | nil => intro e e' h1 h2; exact hvert e e' (h1.trans h2.symm)
    | @cons x y z hadj p ih =>
      intro e e' h1 h2
      let a : M.Dart := ⟨(x, y), hadj⟩
      calc X e = X a := hvert e a h1
        _ = X a.symm := (hs a).symm
        _ = X e' := ih a.symm e' rfl h2
  obtain ⟨p⟩ := hconn.preconnected d.fst d'.fst
  exact hwalk _ _ p d d' rfl rfl

lemma onTri_faceNext (htri : M.Triangulated) (d : M.Dart) (v : Fin n) :
    OnTri M (M.rotation.faceNext d) v ↔ OnTri M d v := by
  have h1 : (M.rotation.faceNext d).fst = d.snd := M.rotation.face_next_fst d
  have h2 : (M.rotation.faceNext (M.rotation.faceNext d)).snd = d.fst := by
    have := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
    rw [tri3 htri d] at this
    exact this.symm
  unfold OnTri
  rw [h1, h2]
  tauto

lemma onTri_adj (htri : M.Triangulated) {d : M.Dart} {u v : Fin n} (hu : OnTri M d u)
    (hv : OnTri M d v) : u = v ∨ M.Adj u v := by
  have a1 : M.Adj d.fst d.snd := d.adj
  have a2 : M.Adj d.snd (M.rotation.faceNext d).snd := by
    have := (M.rotation.faceNext d).adj
    rwa [M.rotation.face_next_fst] at this
  have a3 : M.Adj (M.rotation.faceNext d).snd d.fst := by
    have h2 : (M.rotation.faceNext (M.rotation.faceNext d)).snd = d.fst := by
      have := M.rotation.face_next_fst (M.rotation.faceNext (M.rotation.faceNext d))
      rw [tri3 htri d] at this
      exact this.symm
    have := (M.rotation.faceNext (M.rotation.faceNext d)).adj
    rwa [M.rotation.face_next_fst, h2] at this
  rcases hu with rfl | rfl | rfl <;> rcases hv with rfl | rfl | rfl <;>
    first | exact Or.inl rfl | exact Or.inr ‹_› | exact Or.inr (‹M.Adj _ _›).symm

section faces
variable {H : SimpleGraph (Fin n)} {a b : Fin 4}
  (hH : ∀ u v, H.Adj u v ↔ M.Adj u v ∧ KAct R c a b u ∧ KAct R c a b v)
include hH

lemma meets_iff (htri : M.Triangulated) {d : M.Dart} {w : Fin n} (hw : OnTri M d w)
    (hwa : KAct R c a b w) (K : H.ConnectedComponent) :
    Meets M R c H a b d K ↔ H.connectedComponentMk w = K := by
  constructor
  · rintro ⟨v, hv, hva, rfl⟩
    rcases onTri_adj htri hw hv with rfl | e
    · rfl
    · exact ConnectedComponent.sound ((hH _ _).2 ⟨e, hwa, hva⟩).reachable
  · intro hK
    exact ⟨w, hw, hwa, hK⟩

open Classical in
lemma faceFn_of (htri : M.Triangulated) (Q : Finset H.ConnectedComponent) (Y : Q → ZMod 2)
    {d : M.Dart} {w : Fin n} (hw : OnTri M d w) (hwa : KAct R c a b w) :
    faceFn M R c H a b Q Y d =
      if hK : H.connectedComponentMk w ∈ Q then Y ⟨_, hK⟩ else 0 := by
  classical
  change ∑ K : Q, (if Meets M R c H a b d K.1 then Y K else 0) = _
  simp only [meets_iff hH htri hw hwa]
  split_ifs with hK
  · rw [Finset.sum_eq_single ⟨_, hK⟩]
    · simp
    · intro K _ hne
      split_ifs with e
      · exact absurd (Subtype.ext e.symm) hne
      · rfl
    · simp
  · refine Finset.sum_eq_zero fun K _ => ?_
    split_ifs with e
    · exact absurd (e ▸ K.2) hK
    · rfl

omit hH in
lemma faceFn_zero (Q : Finset H.ConnectedComponent) (Y : Q → ZMod 2) {d : M.Dart}
    (hz : ∀ v, OnTri M d v → KAct R c a b v → H.connectedComponentMk v ∉ Q) :
    faceFn M R c H a b Q Y d = 0 := by
  classical
  change ∑ K : Q, (if Meets M R c H a b d K.1 then Y K else 0) = 0
  refine Finset.sum_eq_zero fun K _ => ?_
  split_ifs with hm
  · obtain ⟨v, hv, hva, e⟩ := hm
    exact absurd (e ▸ K.2) (hz v hv hva)
  · rfl

omit hH in
lemma faceFn_faceNext (htri : M.Triangulated) (Q : Finset H.ConnectedComponent)
    (Y : Q → ZMod 2) (d : M.Dart) :
    faceFn M R c H a b Q Y (M.rotation.faceNext d) = faceFn M R c H a b Q Y d := by
  classical
  change ∑ K : Q, (if Meets M R c H a b (M.rotation.faceNext d) K.1 then Y K else 0) =
    ∑ K : Q, (if Meets M R c H a b d K.1 then Y K else 0)
  refine Finset.sum_congr rfl fun K _ => if_congr ?_ rfl rfl
  simp only [Meets, onTri_faceNext htri]

end faces

end generic

section bounds
variable {n : ℕ} {M : SphericalMap n} {R : Fin n → Prop} {c : Fin n → Fin 4}

lemma mem_dart_edge (d : M.Dart) (x : Fin n) : x ∈ d.edge ↔ d.fst = x ∨ d.snd = x := by
  rw [dart_edge_eq, Sym2.mem_iff]
  constructor <;> rintro (e | e) <;> first | exact Or.inl e.symm | exact Or.inr e.symm

/-- **Boundaries are cycles.** If a dart function is constant on triangles and its boundary
vanishes off the `{a, b}`-edges, its boundary restricted to the `{a, b}`-edges has zero
incidence at every vertex. -/
theorem inc_bd_zero {a b : Fin 4} (X : M.Dart → ZMod 2)
    (hX : ∀ d, X (M.rotation.faceNext d) = X d)
    (hout : ∀ d : M.Dart, d.edge ∉ kEdges M R c a b → X d = X d.symm) :
    incK M R c a b (bdLin M R c a b X) = 0 := by
  classical
  funext x
  change ∑ e : kEdges M R c a b,
    (if x ∈ e.1 then ∑ d : M.Dart, (if d.edge = e.1 then X d else 0) else 0) = 0
  rw [Finset.sum_coe_sort (kEdges M R c a b)
    (fun e => if x ∈ e then ∑ d : M.Dart, (if d.edge = e then X d else 0) else 0)]
  have e1 : ∀ e ∈ kEdges M R c a b,
      (if x ∈ e then ∑ d : M.Dart, (if d.edge = e then X d else 0) else 0) =
        ∑ d : M.Dart, (if d.edge = e then (if x ∈ d.edge then X d else 0) else 0) := by
    intro e _
    by_cases hx : x ∈ e
    · rw [ite_eq_left hx]
      refine Finset.sum_congr rfl fun d _ => ?_
      by_cases hd : d.edge = e
      · rw [ite_eq_left hd, ite_eq_left hd, ite_eq_left (hd ▸ hx)]
      · rw [ite_eq_right hd, ite_eq_right hd]
    · rw [ite_eq_right hx]
      symm
      refine Finset.sum_eq_zero fun d _ => ?_
      by_cases hd : d.edge = e
      · rw [ite_eq_left hd, ite_eq_right (hd ▸ hx)]
      · rw [ite_eq_right hd]
  rw [Finset.sum_congr rfl e1, Finset.sum_comm]
  simp only [Finset.sum_ite_eq]
  -- now `∑ d, if d.edge ∈ kE then (if x ∈ d.edge then X d else 0) else 0`
  set kE := kEdges M R c a b
  have e2 : ∀ d : M.Dart, (if d.edge ∈ kE then (if x ∈ d.edge then X d else 0) else 0) =
      (if d.edge ∈ kE ∧ d.fst = x then X d else 0) +
        (if d.edge ∈ kE ∧ d.snd = x then X d else 0) := by
    intro d
    have hne : d.fst ≠ d.snd := d.adj.ne
    simp only [mem_dart_edge]
    by_cases hk : d.edge ∈ kE <;> by_cases h1 : d.fst = x <;> by_cases h2 : d.snd = x <;>
      simp [hk, h1, h2]
    exact (hne (h1.trans h2.symm)).elim
  rw [Finset.sum_congr rfl fun d _ => e2 d, Finset.sum_add_distrib]
  have e3 : (∑ d : M.Dart, if d.edge ∈ kE ∧ d.snd = x then X d else 0) =
      ∑ d : M.Dart, if d.edge ∈ kE ∧ d.fst = x then X d.symm else 0 := by
    rw [← Equiv.sum_comp (Function.Involutive.toPerm _ Dart.symm_involutive)]
    refine Finset.sum_congr rfl fun d _ => ?_
    simp only [Function.Involutive.coe_toPerm, Dart.edge_symm]
    rfl
  rw [e3, ← Finset.sum_add_distrib]
  have e4 : ∀ d : M.Dart, ((if d.edge ∈ kE ∧ d.fst = x then X d else 0) +
      (if d.edge ∈ kE ∧ d.fst = x then X d.symm else 0)) =
      (if d.fst = x then X d else 0) + (if d.fst = x then X (M.rotation.next d) else 0) := by
    intro d
    have hn : X (M.rotation.next d) = X d.symm := by
      rw [← hX d.symm, RotationSystem.face_next_apply, Dart.symm_symm]
    rw [hn]
    by_cases hk : d.edge ∈ kE <;> by_cases h1 : d.fst = x <;> simp [hk, h1]
    have := hout d hk
    rw [this]
    exact (CharTwo.add_self_eq_zero _).symm
  rw [Finset.sum_congr rfl fun d _ => e4 d, Finset.sum_add_distrib]
  have e5 : (∑ d : M.Dart, if d.fst = x then X (M.rotation.next d) else 0) =
      ∑ d : M.Dart, if d.fst = x then X d else 0 := by
    rw [← Equiv.sum_comp M.rotation.next (fun d => if d.fst = x then X d else 0)]
    refine Finset.sum_congr rfl fun d _ => ?_
    rw [M.rotation.next_fst]
  rw [e5]
  exact CharTwo.add_self_eq_zero _

/-- Off the `{a, b}`-edges, the two sides of an edge get equal values: one endpoint is a
`{p, q}`-vertex shared by both triangles, or an endpoint lies in `R`, in which case both
triangles meet only components excluded from `Q`. -/
theorem faceFn_symm {a b p q : Fin 4} {H : SimpleGraph (Fin n)}
    (hH : ∀ u v, H.Adj u v ↔ M.Adj u v ∧ KAct R c p q u ∧ KAct R c p q v)
    (htri : M.Triangulated) (hprop : ∀ u v, M.Adj u v → ¬ R u → ¬ R v → c u ≠ c v)
    (hcov : ∀ x : Fin 4, x ≠ p → x ≠ q → x = a ∨ x = b) (Q : Finset H.ConnectedComponent)
    (hQ : ∀ v r, M.Adj v r → R r → KAct R c p q v → H.connectedComponentMk v ∉ Q)
    (Y : Q → ZMod 2) (d : M.Dart) (hd : d.edge ∉ kEdges M R c a b) :
    faceFn M R c H p q Q Y d = faceFn M R c H p q Q Y d.symm := by
  classical
  have t1 : OnTri M d d.fst := Or.inl rfl
  have t2 : OnTri M d d.snd := Or.inr (Or.inl rfl)
  have s1 : OnTri M d.symm d.fst := Or.inr (Or.inl rfl)
  have s2 : OnTri M d.symm d.snd := Or.inl rfl
  by_cases ha : KAct R c p q d.fst
  · rw [faceFn_of hH htri Q Y t1 ha, faceFn_of hH htri Q Y s1 ha]
  by_cases hb : KAct R c p q d.snd
  · rw [faceFn_of hH htri Q Y t2 hb, faceFn_of hH htri Q Y s2 hb]
  have hR : R d.fst ∨ R d.snd := by
    by_contra hn
    rw [not_or] at hn
    apply hd
    have c1 : c d.fst = a ∨ c d.fst = b :=
      hcov _ (fun e => ha ⟨hn.1, Or.inl e⟩) (fun e => ha ⟨hn.1, Or.inr e⟩)
    have c2 : c d.snd = a ∨ c d.snd = b :=
      hcov _ (fun e => hb ⟨hn.2, Or.inl e⟩) (fun e => hb ⟨hn.2, Or.inr e⟩)
    have hne := hprop _ _ d.adj hn.1 hn.2
    simp only [kEdges, Finset.mem_filter, mem_edgeFinset]
    refine ⟨d.edge_mem, ?_, ?_⟩
    · intro v hv
      rw [dart_edge_eq, Sym2.mem_iff] at hv
      rcases hv with rfl | rfl
      exacts [hn.1, hn.2]
    · rw [dart_edge_eq, Sym2.map_mk]
      rcases c1 with e1 | e1 <;> rcases c2 with e2 | e2 <;> rw [e1, e2] at hne ⊢ <;>
        first | exact absurd rfl hne | rfl | exact Sym2.eq_swap
  have zero : ∀ e : M.Dart, OnTri M e d.fst → OnTri M e d.snd →
      faceFn M R c H p q Q Y e = 0 := by
    intro e e1 e2
    apply faceFn_zero
    intro v hv hva
    rcases hR with hr | hr
    · rcases onTri_adj htri hv e1 with rfl | adj
      · exact absurd hr hva.1
      · exact hQ v _ adj hr hva
    · rcases onTri_adj htri hv e2 with rfl | adj
      · exact absurd hr hva.1
      · exact hQ v _ adj hr hva
  rw [zero d t1 t2, zero d.symm s1 s2]

/-- **Lower bound on the cycle space.** The face functions built from `Q` give `|Q|`
independent cycles of the `{a, b}`-graph. -/
theorem card_le_finrank_ker {a b p q : Fin 4} {H : SimpleGraph (Fin n)}
    (hH : ∀ u v, H.Adj u v ↔ M.Adj u v ∧ KAct R c p q u ∧ KAct R c p q v)
    (htri : M.Triangulated) (hconn : M.graph.Connected) (hnb : ∀ v, ∃ u, M.Adj v u)
    (hprop : ∀ u v, M.Adj u v → ¬ R u → ¬ R v → c u ≠ c v)
    (hcov : ∀ x : Fin 4, x ≠ p → x ≠ q → x = a ∨ x = b) (Q : Finset H.ConnectedComponent)
    (hQsub : ∀ K ∈ Q, ∃ v, KAct R c p q v ∧ H.connectedComponentMk v = K)
    (hQ : ∀ v r, M.Adj v r → R r → KAct R c p q v → H.connectedComponentMk v ∉ Q)
    (d0 : M.Dart) (hz : ∀ v, OnTri M d0 v → KAct R c p q v → H.connectedComponentMk v ∉ Q) :
    Q.card ≤ finrank (ZMod 2) (LinearMap.ker (incK M R c a b)) := by
  classical
  let Ψ := (bdLin M R c a b).comp (faceFn M R c H p q Q)
  have hker : ∀ Y, Ψ Y ∈ LinearMap.ker (incK M R c a b) := by
    intro Y
    rw [LinearMap.mem_ker]
    exact inc_bd_zero _ (faceFn_faceNext htri Q Y)
      (fun d hd => faceFn_symm hH htri hprop hcov Q hQ Y d hd)
  let Ψ' := Ψ.codRestrict _ hker
  have hinj : Function.Injective Ψ' := by
    rw [← LinearMap.ker_eq_bot, LinearMap.ker_eq_bot']
    intro Y hY
    have hY2 : Ψ Y = 0 := congrArg Subtype.val hY
    set X := faceFn M R c H p q Q Y with hXdef
    have hs : ∀ d, X d.symm = X d := by
      intro d
      by_cases hd : d.edge ∈ kEdges M R c a b
      · have := congrFun hY2 ⟨d.edge, hd⟩
        change ∑ d' : M.Dart, (if d'.edge = d.edge then X d' else 0) = 0 at this
        rw [sum_edge_dart] at this
        exact (zmod2_eq_of_add this).symm
      · exact (faceFn_symm hH htri hprop hcov Q hQ Y d hd).symm
    have hc := dart_const hconn X (faceFn_faceNext htri Q Y) hs
    have h0 : X d0 = 0 := faceFn_zero Q Y hz
    funext K
    obtain ⟨K, hKQ⟩ := K
    obtain ⟨v, hva, hvK⟩ := hQsub K hKQ
    subst hvK
    obtain ⟨u, hu⟩ := hnb v
    have := faceFn_of hH htri Q Y (d := ⟨(v, u), hu⟩) (w := v) (Or.inl rfl) hva
    rw [dite_eq_left hKQ] at this
    rw [Pi.zero_apply, ← this, ← h0]
    exact hc _ _
  have := LinearMap.finrank_le_finrank_of_injective hinj
  rwa [Module.finrank_fintype_fun_eq_card, Fintype.card_coe] at this

open Classical in
/-- **Upper bound on the cycle space.** `dim Z₁ ≤ E − V + C` for the `{a, b}`-graph: walks to a
root give `V − C` independent incidence vectors. -/
theorem finrank_ker_le {a b : Fin 4} {H : SimpleGraph (Fin n)}
    (hH : ∀ u v, H.Adj u v ↔ M.Adj u v ∧ KAct R c a b u ∧ KAct R c a b v)
    (hprop : ∀ u v, M.Adj u v → ¬ R u → ¬ R v → c u ≠ c v) :
    (finrank (ZMod 2) (LinearMap.ker (incK M R c a b)) : ℤ) ≤
      (kEdges M R c a b).card - (kVertsFin R c a b).card +
        ((kVertsFin R c a b).image H.connectedComponentMk).card := by
  classical
  set I := incK M R c a b
  have hwalk : ∀ {u v : Fin n} (p : H.Walk u v), ∃ φ, I φ = Pi.single u 1 + Pi.single v 1 := by
    intro u v p
    induction p with
    | nil =>
      refine ⟨0, ?_⟩
      funext x
      rw [map_zero]
      have : ∀ t : ZMod 2, t + t = 0 := by decide
      exact (this _).symm
    | @cons x y z hadj p ih =>
      obtain ⟨φ, hφ⟩ := ih
      obtain ⟨hM, hx, hy⟩ := (hH x y).1 hadj
      have hmem : s(x, y) ∈ kEdges M R c a b := by
        simp only [kEdges, Finset.mem_filter, mem_edgeFinset, mem_edgeSet]
        refine ⟨hM, ?_, ?_⟩
        · intro v hv
          rw [Sym2.mem_iff] at hv
          rcases hv with rfl | rfl
          exacts [hx.1, hy.1]
        · have hne := hprop _ _ hM hx.1 hy.1
          rw [Sym2.map_mk]
          rcases hx.2 with e1 | e1 <;> rcases hy.2 with e2 | e2 <;> rw [e1, e2] at hne ⊢ <;>
            first | exact absurd rfl hne | rfl | exact Sym2.eq_swap
      let ψ : kEdges M R c a b → ZMod 2 := fun e => if e.1 = s(x, y) then 1 else 0
      have hψ : I ψ = Pi.single x 1 + Pi.single y 1 := by
        funext w
        change ∑ e : kEdges M R c a b, (if w ∈ e.1 then ψ e else 0) = _
        rw [Finset.sum_eq_single ⟨s(x, y), hmem⟩]
        · simp only [ψ, ite_true, Sym2.mem_iff, Pi.add_apply, Pi.single_apply]
          by_cases h1 : w = x
          · subst h1; simp [hM.ne]
          · by_cases h2 : w = y
            · subst h2; simp [h1]
            · simp [h1, h2]
        · intro e _ he
          have : e.1 ≠ s(x, y) := fun h' => he (Subtype.ext h')
          simp [ψ, this]
        · simp
      refine ⟨ψ + φ, ?_⟩
      rw [map_add, hψ, hφ]
      funext w
      simp only [Pi.add_apply]
      exact zmod2_add3 _ _ _
  let root : Fin n → Fin n := fun v => Quot.out (H.connectedComponentMk v)
  have hmk : ∀ v, H.connectedComponentMk (root v) = H.connectedComponentMk v :=
    fun v => Quot.out_eq _
  have hroot2 : ∀ v, root (root v) = root v := by
    intro v
    show Quot.out (H.connectedComponentMk (root v)) = _
    rw [hmk]
  set N := (kVertsFin R c a b).filter (fun v => root v ≠ v) with hN
  have hV : (kVertsFin R c a b).card ≤ N.card +
      ((kVertsFin R c a b).image H.connectedComponentMk).card := by
    have h1 : N.card + ((kVertsFin R c a b).filter (fun v => ¬ root v ≠ v)).card =
        (kVertsFin R c a b).card := by
      rw [hN]; exact Finset.card_filter_add_card_filter_not _
    have h2 : ((kVertsFin R c a b).filter (fun v => ¬ root v ≠ v)).card ≤
        ((kVertsFin R c a b).image H.connectedComponentMk).card := by
      apply Finset.card_le_card_of_injOn H.connectedComponentMk
      · intro v hv
        rw [Finset.mem_coe, Finset.mem_filter] at hv
        exact Finset.mem_coe.2 (Finset.mem_image_of_mem _ hv.1)
      · intro v hv w hw e
        rw [Finset.mem_coe, Finset.mem_filter, not_not] at hv hw
        rw [← hv.2, ← hw.2]
        show Quot.out (H.connectedComponentMk v) = Quot.out (H.connectedComponentMk w)
        rw [e]
    omega
  have hNr : N.card ≤ finrank (ZMod 2) (LinearMap.range I) := by
    have hreach : ∀ v : N, H.Reachable v.1 (root v.1) :=
      fun v => ConnectedComponent.exact (hmk v.1).symm
    choose φ hφ using fun v : N => hwalk (hreach v).some
    let ρ := LinearMap.funLeft (ZMod 2) (ZMod 2) (Subtype.val : N → Fin n)
    have hsurj : Function.Surjective (ρ ∘ₗ I) := by
      intro g
      refine ⟨∑ v : N, g v • φ v, ?_⟩
      funext w
      simp only [LinearMap.comp_apply, map_sum, map_smul, hφ]
      simp only [ρ, LinearMap.funLeft_apply, Finset.sum_apply, Pi.smul_apply, Pi.add_apply,
        Pi.single_apply, smul_eq_mul]
      have hw := (Finset.mem_filter.1 w.2).2
      rw [Finset.sum_eq_single w]
      · have : w.1 ≠ root w.1 := fun e => hw e.symm
        simp [this]
      · intro v _ hv
        have h1 : w.1 ≠ v.1 := fun e => hv (Subtype.ext e).symm
        have h2 : w.1 ≠ root v.1 := by
          intro e
          apply hw
          rw [e, hroot2]
        simp [h1, h2]
      · simp
    have htop := LinearMap.range_eq_top.2 hsurj
    have h3 : finrank (ZMod 2) (LinearMap.range (ρ ∘ₗ I)) = N.card := by
      rw [htop, finrank_top, Module.finrank_fintype_fun_eq_card, Fintype.card_coe]
    rw [← h3, LinearMap.range_comp]
    exact Submodule.finrank_map_le _ _
  have hrn := LinearMap.finrank_range_add_finrank_ker I
  rw [Module.finrank_fintype_fun_eq_card, Fintype.card_coe] at hrn
  omega

open Classical in
/-- **The generic rank bound.** `|Q| ≤ E_ab − V_ab + C_ab`. -/
theorem card_le_rank {a b p q : Fin 4} {Hab H : SimpleGraph (Fin n)}
    (hHab : ∀ u v, Hab.Adj u v ↔ M.Adj u v ∧ KAct R c a b u ∧ KAct R c a b v)
    (hH : ∀ u v, H.Adj u v ↔ M.Adj u v ∧ KAct R c p q u ∧ KAct R c p q v)
    (htri : M.Triangulated) (hconn : M.graph.Connected) (hnb : ∀ v, ∃ u, M.Adj v u)
    (hprop : ∀ u v, M.Adj u v → ¬ R u → ¬ R v → c u ≠ c v)
    (hcov : ∀ x : Fin 4, x ≠ p → x ≠ q → x = a ∨ x = b) (Q : Finset H.ConnectedComponent)
    (hQsub : ∀ K ∈ Q, ∃ v, KAct R c p q v ∧ H.connectedComponentMk v = K)
    (hQ : ∀ v r, M.Adj v r → R r → KAct R c p q v → H.connectedComponentMk v ∉ Q)
    (d0 : M.Dart) (hz : ∀ v, OnTri M d0 v → KAct R c p q v → H.connectedComponentMk v ∉ Q) :
    (Q.card : ℤ) ≤ (kEdges M R c a b).card - (kVertsFin R c a b).card +
        ((kVertsFin R c a b).image Hab.connectedComponentMk).card := by
  have h1 := card_le_finrank_ker hH htri hconn hnb hprop hcov Q hQsub hQ d0 hz
  have h2 := finrank_ker_le hHab hprop
  omega

end bounds

/-! ### The hole: Kempe duality at the link, and the bridge to `QuarterEuler` -/

section hole
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4}

lemma fin5_idx (j : Fin 5) : j + 1 + 1 = j + 2 ∧ j + 1 + 2 = j + 3 ∧ j + 2 + 1 = j + 3 ∧
    j + 2 + 2 = j + 4 ∧ j + 3 + 1 = j + 4 ∧ j + 3 + 2 = j ∧ j + 4 + 1 = j ∧ j + 4 + 2 = j + 1 := by
  revert j; decide

lemma cover4 : ∀ a b p q x : Fin 4, a ≠ b → a ≠ p → a ≠ q → b ≠ p → b ≠ q → p ≠ q →
    x ≠ p → x ≠ q → x = a ∨ x = b := by decide

lemma act_of_reach {a b : Fin 4} {s v : Fin n} (hs : Active h c a b s)
    (r : (pairGraph M.graph h c a b).Reachable s v) : Active h c a b v :=
  reachable_invariant (H := pairGraph M.graph h c a b) (fun _ _ e _ => e.2.2) hs r

open Classical in
/-- **Kempe duality at the hole.** If the `{μ, X}`-component `S` of `x (j+1)` misses
`x (j+3)` and `x (j+4)`, the boundary graph of `S` has exactly two edges at `h`, to `x j` and
`x (j+2)`; by the handshake lemma these two are joined by boundary edges avoiding `h`, and each
such edge is `{α, Y}`. -/
theorem kempe_dual (htri : M.Triangulated) (P : Pent M.graph h) (j : Fin 5) {X Y : Fin 4}
    (h02 : c (P.x (j + 2)) = c (P.x j))
    (hjμ : c (P.x j) ≠ c (P.x (j + 1))) (hjX : c (P.x j) ≠ X)
    (hcols : ∀ v, c v ≠ c (P.x (j + 1)) → c v ≠ X → c v = c (P.x j) ∨ c v = Y)
    (hn3 : ¬ (pairGraph M.graph h c (c (P.x (j + 1))) X).Reachable (P.x (j + 1)) (P.x (j + 3)))
    (hn4 : ¬ (pairGraph M.graph h c (c (P.x (j + 1))) X).Reachable (P.x (j + 1)) (P.x (j + 4))) :
    (pairGraph M.graph h c (c (P.x j)) Y).Reachable (P.x j) (P.x (j + 2)) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  set S : Fin n → Prop := fun v =>
    (pairGraph M.graph h c (c (P.x (j + 1))) X).Reachable (P.x (j + 1)) v with hS
  have hm : Active h c (c (P.x (j + 1))) X (P.x (j + 1)) := ⟨(P.adj_h _).ne', Or.inl rfl⟩
  have actS : ∀ {v}, S v → Active h c (c (P.x (j + 1))) X v := fun hv => act_of_reach hm hv
  have hSh : ¬ S h := fun hs => (actS hs).1 rfl
  have hS1 : S (P.x (j + 1)) := Reachable.refl _
  have hS0 : ¬ S (P.x j) := fun hs => by
    rcases (actS hs).2 with e | e
    · exact hjμ e
    · exact hjX e
  have hS2 : ¬ S (P.x (j + 2)) := fun hs => by
    rcases (actS hs).2 with e | e
    · exact hjμ (h02.symm.trans e)
    · exact hjX (h02.symm.trans e)
  have hS3 : ¬ S (P.x (j + 3)) := hn3
  have hS4 : ¬ S (P.x (j + 4)) := hn4
  have bj : (bdGraph M S).Adj (P.x j) h := by
    have := bd_link P htri hSh (j + 4)
    rw [i41, i42] at this
    exact this.2 (by tauto)
  have nb1 : ¬ (bdGraph M S).Adj (P.x (j + 1)) h := by
    have := bd_link P htri hSh j
    rw [this]
    tauto
  have nb3 : ¬ (bdGraph M S).Adj (P.x (j + 3)) h := by
    have := bd_link P htri hSh (j + 2)
    rw [i21, i22] at this
    rw [this]
    tauto
  have nb4 : ¬ (bdGraph M S).Adj (P.x (j + 4)) h := by
    have := bd_link P htri hSh (j + 3)
    rw [i31, i32] at this
    rw [this]
    tauto
  have colOK : ∀ {u v}, (bdGraph M S).Adj u v → u ≠ h → c u = c (P.x j) ∨ c u = Y := by
    intro u v huv hu
    obtain ⟨hnS, w, hw, e⟩ := bdGraph_out htri huv
    apply hcols
    · intro hc1
      exact hnS (hw.trans (Adj.reachable ⟨e.symm, actS hw, hu, Or.inl hc1⟩))
    · intro hc1
      exact hnS (hw.trans (Adj.reachable ⟨e.symm, actS hw, hu, Or.inr hc1⟩))
  have hle : offV (bdGraph M S) h ≤ pairGraph M.graph h c (c (P.x j)) Y := by
    rintro u v ⟨huv, hu, hv⟩
    exact ⟨huv.fst, ⟨hu, colOK huv hu⟩, ⟨hv, colOK huv.symm hv⟩⟩
  have hev := bdGraph_even htri S
  have hodd : Odd ((compKeep (offV (bdGraph M S) h) (P.x j)).degree (P.x j)) :=
    (odd_iff_bd _ hev h (P.x j) (P.x j)).2 ⟨Reachable.refl _, (P.adj_h j).ne', bj⟩
  obtain ⟨w, hwz, hw⟩ := exists_ne_odd_degree_of_exists_odd_degree (h := hodd)
  rw [odd_iff_bd _ hev] at hw
  obtain ⟨hreach, -, hadj⟩ := hw
  obtain ⟨i, rfl⟩ := P.only w hadj.fst.symm
  rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
  · exact absurd rfl hwz
  · exact absurd hadj nb1
  · exact hreach.mono hle
  · exact absurd hadj nb3
  · exact absurd hadj nb4

/-- `¬ Lock1` forces `x j ⇝ x (j+2)` in the `{α, B}`-graph (converse of
`not_reach_alpha_B_of_lock1`). -/
theorem reach_alpha_B_of_not_lock1 (htri : M.Triangulated) (P : Pent M.graph h) {j : Fin 5}
    (hr : RepeatAt P c j) (hl : ¬ Lock1 P c j) :
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x j) (P.x (j + 2)) := by
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  refine kempe_dual htri P j h02.symm (Ne.symm h1) (Ne.symm h2) ?_ hl ?_
  · intro v e1 e2
    exact cover4 _ _ _ _ _ (Ne.symm h3) (Ne.symm h1) (Ne.symm h2) (Ne.symm h5) (Ne.symm h6) h4
      e1 e2
  · intro hre
    rcases (act_of_reach ⟨(P.adj_h _).ne', Or.inl rfl⟩ hre).2 with e | e
    · exact h5 e.symm
    · exact h6 e.symm

/-- `¬ Lock2` forces `x j ⇝ x (j+2)` in the `{α, A}`-graph. -/
theorem reach_alpha_A_of_not_lock2 (htri : M.Triangulated) (P : Pent M.graph h) {j : Fin 5}
    (hr : RepeatAt P c j) (hl : ¬ Lock2 P c j) :
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x j) (P.x (j + 2)) := by
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  refine kempe_dual htri P j h02.symm (Ne.symm h1) (Ne.symm h3) ?_ ?_ hl
  · intro v e1 e2
    exact cover4 _ _ _ _ _ (Ne.symm h2) (Ne.symm h1) (Ne.symm h3) (Ne.symm h4) h6 h5 e1 e2
  · intro hre
    rcases (act_of_reach ⟨(P.adj_h _).ne', Or.inl rfl⟩ hre).2 with e | e
    · exact h4 e.symm
    · exact h6 e

variable (M h c) in
open Classical in
/-- The components of the `{p, q}`-graph of `T − h` containing a link vertex. -/
noncomputable def linkComps (p q : Fin 4) : Finset (pairGraph M.graph h c p q).ConnectedComponent :=
  (Finset.univ.filter fun v => KAct (fun v => v = h) c p q v ∧ M.Adj v h).image
    (pairGraph M.graph h c p q).connectedComponentMk

open Classical in
lemma kVerts_hole (a b : Fin 4) : kVertsFin (fun v => v = h) c a b =
    Finset.univ.filter fun v => v ≠ h ∧ (c v = a ∨ c v = b) := by
  ext v
  simp [kVertsFin, KAct]

open Classical in
lemma pairComps_eq (a b : Fin 4) : pairComps M h c a b =
    ((kVertsFin (fun v => v = h) c a b).image (pairGraph M.graph h c a b).connectedComponentMk).card := by
  rw [kVerts_hole]
  unfold pairComps
  convert rfl

open Classical in
lemma pairRank_eq (a b : Fin 4) : pairRank M h c a b =
    ((kEdges M (fun v => v = h) c a b).card : ℤ) - (kVertsFin (fun v => v = h) c a b).card +
      ((kVertsFin (fun v => v = h) c a b).image (pairGraph M.graph h c a b).connectedComponentMk).card := by
  have hE : pairEdges M h c a b = (kEdges M (fun v => v = h) c a b).card := by
    unfold pairEdges
    congr 1
    ext e
    simp only [offEdges, kEdges, Finset.mem_filter]
    constructor
    · rintro ⟨⟨he, hh⟩, hm⟩
      exact ⟨he, fun v hv e' => hh (e' ▸ hv), hm⟩
    · rintro ⟨he, hh, hm⟩
      exact ⟨⟨he, fun hm' => hh h hm' rfl⟩, hm⟩
  have hV : pairVerts h c a b = (kVertsFin (fun v => v = h) c a b).card := by
    rw [kVerts_hole]
    unfold pairVerts
    convert rfl
  unfold pairRank
  rw [hE, hV, pairComps_eq]

/-- **The hole lower bound.** `C_pq − |linkComps| ≤ r_ab` for complementary pairs. -/
theorem hole_lower (htri : M.Triangulated) (hconn : M.graph.Connected) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) {a b p q : Fin 4}
    (hcov : ∀ x : Fin 4, x ≠ p → x ≠ q → x = a ∨ x = b) :
    (pairComps M h c p q : ℤ) - (linkComps M h c p q).card ≤ pairRank M h c a b := by
  classical
  set H := pairGraph M.graph h c p q
  set F := linkComps M h c p q with hFdef
  set Q := ((kVertsFin (fun v => v = h) c p q).image H.connectedComponentMk) \ F with hQdef
  have hnb : ∀ v, ∃ u, M.Adj v u := by
    intro v
    by_cases hv : v = h
    · subst hv; exact ⟨P.x 0, P.adj_h 0⟩
    · obtain ⟨w⟩ := hconn.preconnected v h
      cases w with
      | nil => exact absurd rfl hv
      | cons e _ => exact ⟨_, e⟩
  have hF : ∀ v, M.Adj v h → KAct (fun v => v = h) c p q v → H.connectedComponentMk v ∈ F :=
    fun v e hv => Finset.mem_image_of_mem _ (Finset.mem_filter.2 ⟨Finset.mem_univ _, hv, e⟩)
  have hQ : ∀ v r, M.Adj v r → r = h → KAct (fun v => v = h) c p q v →
      H.connectedComponentMk v ∉ Q := by
    rintro v r e rfl hv hq
    exact (Finset.mem_sdiff.1 hq).2 (hF v e hv)
  have hQsub : ∀ K ∈ Q, ∃ v, KAct (fun v => v = h) c p q v ∧ H.connectedComponentMk v = K := by
    intro K hK
    obtain ⟨v, hv, rfl⟩ := Finset.mem_image.1 (Finset.mem_sdiff.1 hK).1
    exact ⟨v, (Finset.mem_filter.1 hv).2, rfl⟩
  let d0 : M.Dart := ⟨(h, P.x 0), P.adj_h 0⟩
  have hz : ∀ v, OnTri M d0 v → KAct (fun v => v = h) c p q v → H.connectedComponentMk v ∉ Q := by
    intro v hv hva
    have hh : OnTri M d0 h := Or.inl rfl
    rcases onTri_adj htri hv hh with rfl | e
    · exact absurd rfl hva.1
    · exact hQ v h e rfl hva
  have key := card_le_rank (Hab := pairGraph M.graph h c a b) (H := H) (fun _ _ => Iff.rfl)
    (fun _ _ => Iff.rfl) htri hconn hnb (fun u v e hu hv => hc e hu hv) hcov Q hQsub hQ d0 hz
  have hcard := Finset.card_le_card_sdiff_add_card
    (s := (kVertsFin (fun v => v = h) c p q).image H.connectedComponentMk) (t := F)
  rw [pairRank_eq, pairComps_eq]
  have : (((kVertsFin (fun v => v = h) c p q).image H.connectedComponentMk).card : ℤ) ≤
      Q.card + F.card := by exact_mod_cast hcard
  linarith

lemma linkComps_le_one (P : Pent M.graph h) {p q : Fin 4} (u : Fin n)
    (hu : ∀ i, KAct (fun v => v = h) c p q (P.x i) →
      (pairGraph M.graph h c p q).Reachable (P.x i) u) :
    (linkComps M h c p q).card ≤ 1 := by
  classical
  refine Finset.card_le_one.2 fun K1 h1 K2 h2 => ?_
  unfold linkComps at h1 h2
  obtain ⟨v1, hv1, rfl⟩ := Finset.mem_image.1 h1
  obtain ⟨v2, hv2, rfl⟩ := Finset.mem_image.1 h2
  obtain ⟨-, a1, e1⟩ := Finset.mem_filter.1 hv1
  obtain ⟨-, a2, e2⟩ := Finset.mem_filter.1 hv2
  obtain ⟨i1, rfl⟩ := P.only _ e1.symm
  obtain ⟨i2, rfl⟩ := P.only _ e2.symm
  exact ConnectedComponent.sound ((hu i1 a1).trans (hu i2 a2).symm)

lemma linkComps_le_two (P : Pent M.graph h) {p q : Fin 4} (u u' : Fin n)
    (hu : ∀ i, KAct (fun v => v = h) c p q (P.x i) →
      (pairGraph M.graph h c p q).Reachable (P.x i) u ∨
        (pairGraph M.graph h c p q).Reachable (P.x i) u') :
    (linkComps M h c p q).card ≤ 2 := by
  classical
  have hsub : linkComps M h c p q ⊆ {(pairGraph M.graph h c p q).connectedComponentMk u,
      (pairGraph M.graph h c p q).connectedComponentMk u'} := by
    intro K hK
    unfold linkComps at hK
    obtain ⟨v, hv, rfl⟩ := Finset.mem_image.1 hK
    obtain ⟨-, a1, e1⟩ := Finset.mem_filter.1 hv
    obtain ⟨i, rfl⟩ := P.only _ e1.symm
    rcases hu i a1 with r | r
    · exact Finset.mem_insert.2 (Or.inl (ConnectedComponent.sound r))
    · exact Finset.mem_insert.2 (Or.inr (Finset.mem_singleton.2 (ConnectedComponent.sound r)))
  refine (Finset.card_le_card hsub).trans ?_
  exact (Finset.card_insert_le _ _).trans (by simp)

lemma ka (P : Pent M.graph h) (i : Fin 5) {p q : Fin 4} (hc : c (P.x i) = p ∨ c (P.x i) = q) :
    KAct (fun v => v = h) c p q (P.x i) := ⟨(P.adj_h i).ne', hc⟩

lemma rim (P : Pent M.graph h) {p q : Fin 4} (i k : Fin 5) (hk : i + 1 = k)
    (hi : KAct (fun v => v = h) c p q (P.x i)) (hk' : KAct (fun v => v = h) c p q (P.x k)) :
    (pairGraph M.graph h c p q).Reachable (P.x i) (P.x k) := by
  subst hk
  exact Adj.reachable (G := pairGraph M.graph h c p q) ⟨P.adj_cyc i, hi, hk'⟩

end hole

/-! ### The six exact dualities at a repeat state -/

section dualities
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4}

lemma pairRank_comm (a b : Fin 4) : pairRank M h c a b = pairRank M h c b a := by
  rw [pairRank_eq, pairRank_eq]
  have hE : kEdges M (fun v => v = h) c a b = kEdges M (fun v => v = h) c b a := by
    ext e
    simp only [kEdges, Finset.mem_filter, Sym2.eq_swap (a := a)]
  have hV : kVertsFin (fun v => v = h) c a b = kVertsFin (fun v => v = h) c b a := by
    ext v
    simp only [kVertsFin, KAct, Finset.mem_filter, Finset.mem_univ, true_and, or_comm]
  rw [← pairComps_eq, ← pairComps_eq, pairComps_comm, hE, hV]

lemma sum_six (f : Fin 4 → Fin 4 → ℤ) (hf : ∀ x y, f x y = f y x) {α μ A B : Fin 4}
    (h1 : μ ≠ α) (h2 : A ≠ α) (h3 : B ≠ α) (h4 : μ ≠ A) (h5 : μ ≠ B) (h6 : A ≠ B) :
    ∑ p ∈ pairs, f p.1 p.2 = f A B + f α μ + f μ A + f α B + f μ B + f α A := by
  have hl : ∀ α μ A B : Fin 4, μ ≠ α → A ≠ α → B ≠ α → μ ≠ A → μ ≠ B → A ≠ B →
      [sortPair A B, sortPair α μ, sortPair μ A, sortPair α B, sortPair μ B,
        sortPair α A].Nodup ∧
      [sortPair A B, sortPair α μ, sortPair μ A, sortPair α B, sortPair μ B,
        sortPair α A].toFinset = pairs := by
    decide
  obtain ⟨hn, ht⟩ := hl α μ A B h1 h2 h3 h4 h5 h6
  have hs : ∀ x y, f (sortPair x y).1 (sortPair x y).2 = f x y := by
    intro x y
    unfold sortPair
    split_ifs
    · rfl
    · exact hf y x
  rw [← ht, List.sum_toFinset _ hn]
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil, hs]
  ring

variable (htri : M.Triangulated) (hconn : M.graph.Connected) (P : Pent M.graph h)
  (hc : ProperOff M.graph h c) {j : Fin 5} (hr : RepeatAt P c j)
include htri hconn hc hr

lemma bound_AB : (pairComps M h c (c (P.x j)) (c (P.x (j + 1))) : ℤ) - 1 ≤
    pairRank M h c (c (P.x (j + 3))) (c (P.x (j + 4))) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have hb := hole_lower htri hconn P hc
    (fun x => cover4 _ _ _ _ x h6 h2 (Ne.symm h4) h3 (Ne.symm h5) (Ne.symm h1))
  have hF := linkComps_le_one (c := c) P (p := c (P.x j)) (q := c (P.x (j + 1))) (P.x (j + 1))
    (by
      intro i hi
      rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
      · exact rim P i (i + 1) rfl hi (ka P (i + 1) (Or.inr rfl))
      · exact Reachable.refl _
      · exact (rim P (j + 1) (j + 2) i11 (ka P (j + 1) (Or.inr rfl)) hi).symm
      · exfalso; rcases hi.2 with e | e
        · exact h2 e
        · exact h4 e.symm
      · exfalso; rcases hi.2 with e | e
        · exact h3 e
        · exact h5 e.symm)
  have : ((linkComps M h c (c (P.x j)) (c (P.x (j + 1)))).card : ℤ) ≤ 1 := by exact_mod_cast hF
  linarith

lemma bound_αμ : (pairComps M h c (c (P.x (j + 3))) (c (P.x (j + 4))) : ℤ) - 1 ≤
    pairRank M h c (c (P.x j)) (c (P.x (j + 1))) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have hb := hole_lower htri hconn P hc
    (fun x => cover4 _ _ _ _ x (Ne.symm h1) (Ne.symm h2) (Ne.symm h3) h4 h5 h6)
  have hF := linkComps_le_one (c := c) P (p := c (P.x (j + 3))) (q := c (P.x (j + 4)))
    (P.x (j + 3))
    (by
      intro i hi
      rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
      · exfalso; rcases hi.2 with e | e
        · exact h2 e.symm
        · exact h3 e.symm
      · exfalso; rcases hi.2 with e | e
        · exact h4 e
        · exact h5 e
      · exfalso; rcases hi.2 with e | e
        · exact h2 (e.symm.trans h02.symm)
        · exact h3 (e.symm.trans h02.symm)
      · exact Reachable.refl _
      · exact (rim P (j + 3) (j + 4) i31 (ka P (j + 3) (Or.inl rfl)) hi).symm)
  have : ((linkComps M h c (c (P.x (j + 3))) (c (P.x (j + 4)))).card : ℤ) ≤ 1 := by
    exact_mod_cast hF
  linarith

open Classical in
lemma bound_μA : (pairComps M h c (c (P.x j)) (c (P.x (j + 4))) : ℤ) - 1 -
    (if Lock1 P c j then 1 else 0) ≤ pairRank M h c (c (P.x (j + 1))) (c (P.x (j + 3))) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  have hr' := hr
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have hb := hole_lower htri hconn P hc
    (fun x => cover4 _ _ _ _ x h4 h1 h5 h2 h6 (Ne.symm h3))
  have nx1 : ¬ KAct (fun v => v = h) c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 1)) := by
    rintro ⟨-, e | e⟩
    · exact h1 e
    · exact h5 e
  have nx3 : ¬ KAct (fun v => v = h) c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 3)) := by
    rintro ⟨-, e | e⟩
    · exact h2 e
    · exact h6 e
  by_cases hl : Lock1 P c j
  · have hF := linkComps_le_two (c := c) P (p := c (P.x j)) (q := c (P.x (j + 4))) (P.x j)
      (P.x (j + 2))
      (by
        intro i hi
        rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
        · exact Or.inl (Reachable.refl _)
        · exact absurd hi nx1
        · exact Or.inr (Reachable.refl _)
        · exact absurd hi nx3
        · exact Or.inl (rim P (j + 4) j i41 hi (ka P j (Or.inl rfl))))
    have : ((linkComps M h c (c (P.x j)) (c (P.x (j + 4)))).card : ℤ) ≤ 2 := by
      exact_mod_cast hF
    rw [ite_eq_left hl]
    linarith
  · have kd := reach_alpha_B_of_not_lock1 htri P hr' hl
    have hF := linkComps_le_one (c := c) P (p := c (P.x j)) (q := c (P.x (j + 4))) (P.x j)
      (by
        intro i hi
        rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
        · exact Reachable.refl _
        · exact absurd hi nx1
        · exact kd.symm
        · exact absurd hi nx3
        · exact rim P (j + 4) j i41 hi (ka P j (Or.inl rfl)))
    have : ((linkComps M h c (c (P.x j)) (c (P.x (j + 4)))).card : ℤ) ≤ 1 := by
      exact_mod_cast hF
    rw [ite_eq_right hl]
    linarith

open Classical in
lemma bound_αB : (pairComps M h c (c (P.x (j + 1))) (c (P.x (j + 3))) : ℤ) - 1 -
    (if Lock1 P c j then 0 else 1) ≤ pairRank M h c (c (P.x j)) (c (P.x (j + 4))) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have hb := hole_lower htri hconn P hc
    (fun x => cover4 _ _ _ _ x (Ne.symm h3) (Ne.symm h1) (Ne.symm h2) (Ne.symm h5)
      (Ne.symm h6) h4)
  have hcase : ∀ i, KAct (fun v => v = h) c (c (P.x (j + 1))) (c (P.x (j + 3))) (P.x i) →
      i = j + 1 ∨ i = j + 3 := by
    intro i hi
    rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
    · exfalso; rcases hi.2 with e | e
      · exact h1 e.symm
      · exact h2 e.symm
    · exact Or.inl rfl
    · exfalso; rcases hi.2 with e | e
      · exact h1 (e.symm.trans h02.symm)
      · exact h2 (e.symm.trans h02.symm)
    · exact Or.inr rfl
    · exfalso; rcases hi.2 with e | e
      · exact h5 e.symm
      · exact h6 e.symm
  by_cases hl : Lock1 P c j
  · have hF := linkComps_le_one (c := c) P (p := c (P.x (j + 1))) (q := c (P.x (j + 3)))
      (P.x (j + 1))
      (by
        intro i hi
        rcases hcase i hi with rfl | rfl
        · exact Reachable.refl _
        · exact hl.symm)
    have : ((linkComps M h c (c (P.x (j + 1))) (c (P.x (j + 3)))).card : ℤ) ≤ 1 := by
      exact_mod_cast hF
    rw [ite_eq_left hl]
    linarith
  · have hF := linkComps_le_two (c := c) P (p := c (P.x (j + 1))) (q := c (P.x (j + 3)))
      (P.x (j + 1)) (P.x (j + 3))
      (by
        intro i hi
        rcases hcase i hi with rfl | rfl
        · exact Or.inl (Reachable.refl _)
        · exact Or.inr (Reachable.refl _))
    have : ((linkComps M h c (c (P.x (j + 1))) (c (P.x (j + 3)))).card : ℤ) ≤ 2 := by
      exact_mod_cast hF
    rw [ite_eq_right hl]
    linarith

open Classical in
lemma bound_μB : (pairComps M h c (c (P.x j)) (c (P.x (j + 3))) : ℤ) - 1 -
    (if Lock2 P c j then 1 else 0) ≤ pairRank M h c (c (P.x (j + 1))) (c (P.x (j + 4))) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  have hr' := hr
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have hb := hole_lower htri hconn P hc
    (fun x => cover4 _ _ _ _ x h5 h1 h4 h3 (Ne.symm h6) (Ne.symm h2))
  have nx1 : ¬ KAct (fun v => v = h) c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 1)) := by
    rintro ⟨-, e | e⟩
    · exact h1 e
    · exact h4 e
  have nx4 : ¬ KAct (fun v => v = h) c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 4)) := by
    rintro ⟨-, e | e⟩
    · exact h3 e
    · exact h6 e.symm
  have r23 : (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 3))
      (P.x (j + 2)) :=
    (rim P (j + 2) (j + 3) i21 (ka P (j + 2) (Or.inl h02.symm)) (ka P (j + 3) (Or.inr rfl))).symm
  by_cases hl : Lock2 P c j
  · have hF := linkComps_le_two (c := c) P (p := c (P.x j)) (q := c (P.x (j + 3))) (P.x j)
      (P.x (j + 2))
      (by
        intro i hi
        rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
        · exact Or.inl (Reachable.refl _)
        · exact absurd hi nx1
        · exact Or.inr (Reachable.refl _)
        · exact Or.inr r23
        · exact absurd hi nx4)
    have : ((linkComps M h c (c (P.x j)) (c (P.x (j + 3)))).card : ℤ) ≤ 2 := by
      exact_mod_cast hF
    rw [ite_eq_left hl]
    linarith
  · have kd := reach_alpha_A_of_not_lock2 htri P hr' hl
    have hF := linkComps_le_one (c := c) P (p := c (P.x j)) (q := c (P.x (j + 3))) (P.x j)
      (by
        intro i hi
        rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
        · exact Reachable.refl _
        · exact absurd hi nx1
        · exact kd.symm
        · exact r23.trans kd.symm
        · exact absurd hi nx4)
    have : ((linkComps M h c (c (P.x j)) (c (P.x (j + 3)))).card : ℤ) ≤ 1 := by
      exact_mod_cast hF
    rw [ite_eq_right hl]
    linarith

open Classical in
lemma bound_αA : (pairComps M h c (c (P.x (j + 1))) (c (P.x (j + 4))) : ℤ) - 1 -
    (if Lock2 P c j then 0 else 1) ≤ pairRank M h c (c (P.x j)) (c (P.x (j + 3))) := by
  obtain ⟨i11, i12, i21, i22, i31, i32, i41, i42⟩ := fin5_idx j
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  have hb := hole_lower htri hconn P hc
    (fun x => cover4 _ _ _ _ x (Ne.symm h2) (Ne.symm h1) (Ne.symm h3) (Ne.symm h4) h6 h5)
  have hcase : ∀ i, KAct (fun v => v = h) c (c (P.x (j + 1))) (c (P.x (j + 4))) (P.x i) →
      i = j + 1 ∨ i = j + 4 := by
    intro i hi
    rcases fin5_cases j i with rfl | rfl | rfl | rfl | rfl
    · exfalso; rcases hi.2 with e | e
      · exact h1 e.symm
      · exact h3 e.symm
    · exact Or.inl rfl
    · exfalso; rcases hi.2 with e | e
      · exact h1 (e.symm.trans h02.symm)
      · exact h3 (e.symm.trans h02.symm)
    · exfalso; rcases hi.2 with e | e
      · exact h4 e.symm
      · exact h6 e
    · exact Or.inr rfl
  by_cases hl : Lock2 P c j
  · have hF := linkComps_le_one (c := c) P (p := c (P.x (j + 1))) (q := c (P.x (j + 4)))
      (P.x (j + 1))
      (by
        intro i hi
        rcases hcase i hi with rfl | rfl
        · exact Reachable.refl _
        · exact hl.symm)
    have : ((linkComps M h c (c (P.x (j + 1))) (c (P.x (j + 4)))).card : ℤ) ≤ 1 := by
      exact_mod_cast hF
    rw [ite_eq_left hl]
    linarith
  · have hF := linkComps_le_two (c := c) P (p := c (P.x (j + 1))) (q := c (P.x (j + 4)))
      (P.x (j + 1)) (P.x (j + 4))
      (by
        intro i hi
        rcases hcase i hi with rfl | rfl
        · exact Or.inl (Reachable.refl _)
        · exact Or.inr (Reachable.refl _))
    have : ((linkComps M h c (c (P.x (j + 1))) (c (P.x (j + 4)))).card : ℤ) ≤ 2 := by
      exact_mod_cast hF
    rw [ite_eq_right hl]
    linarith

end dualities

section main
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4}

open Classical in
/-- **The six exact pair dualities at a degree-five hole** (`NightW2Euler.md` §1). At any
repeat state `α μ α A B` on `x j, …, x (j+4)` of a connected triangulated sphere, with
`r` the cycle rank and `C` the component count of a two-colour subgraph of `T − h`:
* `r(AB) = C(αμ) − 1` and `r(αμ) = C(AB) − 1`;
* `r(μA) = C(αB) − 1 − [Lock1]` and `r(αB) = C(μA) − 1 − [¬Lock1]`;
* `r(μB) = C(αA) − 1 − [Lock2]` and `r(αA) = C(μB) − 1 − [¬Lock2]`. -/
theorem pair_dualities (htri : M.Triangulated) (hconn : M.graph.Connected)
    (P : Pent M.graph h) (hc : ProperOff M.graph h c) {j : Fin 5} (hr : RepeatAt P c j) :
    pairRank M h c (c (P.x (j + 3))) (c (P.x (j + 4))) =
        (pairComps M h c (c (P.x j)) (c (P.x (j + 1))) : ℤ) - 1 ∧
      pairRank M h c (c (P.x j)) (c (P.x (j + 1))) =
        (pairComps M h c (c (P.x (j + 3))) (c (P.x (j + 4))) : ℤ) - 1 ∧
      pairRank M h c (c (P.x (j + 1))) (c (P.x (j + 3))) =
        (pairComps M h c (c (P.x j)) (c (P.x (j + 4))) : ℤ) - 1 -
          (if Lock1 P c j then 1 else 0) ∧
      pairRank M h c (c (P.x j)) (c (P.x (j + 4))) =
        (pairComps M h c (c (P.x (j + 1))) (c (P.x (j + 3))) : ℤ) - 1 -
          (if Lock1 P c j then 0 else 1) ∧
      pairRank M h c (c (P.x (j + 1))) (c (P.x (j + 4))) =
        (pairComps M h c (c (P.x j)) (c (P.x (j + 3))) : ℤ) - 1 -
          (if Lock2 P c j then 1 else 0) ∧
      pairRank M h c (c (P.x j)) (c (P.x (j + 3))) =
        (pairComps M h c (c (P.x (j + 1))) (c (P.x (j + 4))) : ℤ) - 1 -
          (if Lock2 P c j then 0 else 1) := by
  have b1 := bound_AB htri hconn P hc hr
  have b2 := bound_αμ htri hconn P hc hr
  have b3 := bound_μA htri hconn P hc hr
  have b4 := bound_αB htri hconn P hc hr
  have b5 := bound_μB htri hconn P hc hr
  have b6 := bound_αA htri hconn P hc hr
  have hsum := six_pair_rank_identity c hconn htri P hc
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  rw [sum_six (pairRank M h c) pairRank_comm h1 h2 h3 h4 h5 h6,
    sum_six (fun a b => (pairComps M h c a b : ℤ)) (fun a b => by rw [pairComps_comm]) h1 h2 h3
      h4 h5 h6] at hsum
  by_cases l1 : Lock1 P c j <;> by_cases l2 : Lock2 P c j <;>
    simp only [l1, l2, ite_true, ite_false] at b3 b4 b5 b6 ⊢ <;>
    refine ⟨by linarith, by linarith, by linarith, by linarith, by linarith, by linarith⟩

/-- **The six-pair identity, recovered by summing the dualities.** At a repeat state the
six formulas of `pair_dualities` add up to `Σ r = Σ C − 8` (the corrections contribute
`[Lock1] + [¬Lock1] + [Lock2] + [¬Lock2] = 2`). -/
theorem six_pair_identity_from_dualities (htri : M.Triangulated) (hconn : M.graph.Connected)
    (P : Pent M.graph h) (hc : ProperOff M.graph h c) {j : Fin 5} (hr : RepeatAt P c j) :
    ∑ p ∈ pairs, pairRank M h c p.1 p.2 = ∑ p ∈ pairs, (pairComps M h c p.1 p.2 : ℤ) - 8 := by
  classical
  obtain ⟨d1, d2, d3, d4, d5, d6⟩ := pair_dualities htri hconn P hc hr
  obtain ⟨h02, h1, h2, h3, h4, h5, h6⟩ := hr
  rw [sum_six (pairRank M h c) pairRank_comm h1 h2 h3 h4 h5 h6,
    sum_six (fun a b => (pairComps M h c a b : ℤ)) (fun a b => by rw [pairComps_comm]) h1 h2 h3
      h4 h5 h6]
  rw [d1, d2, d3, d4, d5, d6]
  by_cases l1 : Lock1 P c j <;> by_cases l2 : Lock2 P c j <;> simp only [l1, l2, ite_true,
    ite_false] <;> ring

variable (P : Pent M.graph h) in
/-- `σ` is a fixed point: the `{α, μ}`-component of `x (j+1)` is the whole `{α, μ}`-subgraph
of `T − h` (verbatim the definition `SigmaFixed` of `QuarterSigmaFix`, which cannot be
imported alongside `QuarterEuler`). -/
def SigmaFixedE (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  ∀ v, Active h c (c (P.x j)) (c (P.x (j + 1))) v →
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) v

/-- `σ` is fixed iff the `{α, μ}`-graph of `T − h` is connected (`C(αμ) = 1`). No planarity. -/
theorem sigmaFixed_iff_C_alpha_mu_one (P : Pent M.graph h) {j : Fin 5} :
    SigmaFixedE P c j ↔ pairComps M h c (c (P.x j)) (c (P.x (j + 1))) = 1 := by
  classical
  have hm : Active h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 1)) :=
    ⟨(P.adj_h _).ne', Or.inr rfl⟩
  rw [pairComps_eq]
  constructor
  · intro hf
    rw [Finset.card_eq_one]
    refine ⟨(pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).connectedComponentMk
      (P.x (j + 1)), ?_⟩
    ext K
    simp only [Finset.mem_image, Finset.mem_singleton]
    constructor
    · rintro ⟨v, hv, rfl⟩
      exact (ConnectedComponent.sound (hf v (Finset.mem_filter.1 hv).2)).symm
    · rintro rfl
      exact ⟨P.x (j + 1), Finset.mem_filter.2 ⟨Finset.mem_univ _, hm⟩, rfl⟩
  · intro h1 v hv
    have hle := (Finset.card_le_one.1 h1.le)
    exact ConnectedComponent.exact (hle _ (Finset.mem_image_of_mem _
      (Finset.mem_filter.2 ⟨Finset.mem_univ _, hm⟩)) _ (Finset.mem_image_of_mem _
      (Finset.mem_filter.2 ⟨Finset.mem_univ _, hv⟩)))

/-- **Lemma Fix, rank form.** At a repeat state of a connected triangulated sphere, `σ` is
fixed iff the `{A, B}`-graph of `T − h` has cycle rank `0` (via `r(AB) = C(αμ) − 1`). -/
theorem sigmaFixed_iff_rank_AB_zero (htri : M.Triangulated) (hconn : M.graph.Connected)
    (P : Pent M.graph h) (hc : ProperOff M.graph h c) {j : Fin 5} (hr : RepeatAt P c j) :
    SigmaFixedE P c j ↔ pairRank M h c (c (P.x (j + 3))) (c (P.x (j + 4))) = 0 := by
  rw [sigmaFixed_iff_C_alpha_mu_one, (pair_dualities htri hconn P hc hr).1]
  omega

end main

/-! ### The sphere: `r(G_ab) = C(G_cd) − 1` for a 4-colouring of a whole triangulation -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {c : Fin n → Fin 4}

variable (M c) in
/-- The `{a, b}`-subgraph of the whole triangulation. -/
def sGraph (a b : Fin 4) : SimpleGraph (Fin n) where
  Adj u v := M.Adj u v ∧ KAct (fun _ => False) c a b u ∧ KAct (fun _ => False) c a b v
  symm := ⟨fun _ _ e => ⟨e.1.symm, e.2.2, e.2.1⟩⟩
  loopless := ⟨fun _ e => e.1.ne rfl⟩

variable (M c) in
open Classical in
/-- `C(G_ab)` on the sphere. -/
noncomputable def sComps (a b : Fin 4) : ℕ :=
  ((kVertsFin (fun _ => False) c a b).image (sGraph M c a b).connectedComponentMk).card

variable (M c) in
/-- `r(G_ab) = E − V + C` on the sphere. -/
noncomputable def sRank (a b : Fin 4) : ℤ :=
  ((kEdges M (fun _ => False) c a b).card : ℤ) - (kVertsFin (fun _ => False) c a b).card +
    sComps M c a b

lemma kAct_comm {R : Fin n → Prop} (a b : Fin 4) (v : Fin n) :
    KAct R c a b v ↔ KAct R c b a v := by
  unfold KAct; rw [or_comm]

lemma kVerts_comm (R : Fin n → Prop) (a b : Fin 4) : kVertsFin R c a b = kVertsFin R c b a := by
  ext v
  simp only [kVertsFin, Finset.mem_filter, Finset.mem_univ, true_and, kAct_comm a b]

lemma kEdges_comm (R : Fin n → Prop) (a b : Fin 4) : kEdges M R c a b = kEdges M R c b a := by
  ext e
  simp only [kEdges, Finset.mem_filter, Sym2.eq_swap (a := a)]

lemma sGraph_comm (a b : Fin 4) : sGraph M c a b = sGraph M c b a := by
  ext u v
  simp only [sGraph, kAct_comm a b]

lemma sComps_comm (a b : Fin 4) : sComps M c a b = sComps M c b a := by
  unfold sComps
  rw [sGraph_comm, kVerts_comm]

lemma sRank_comm (a b : Fin 4) : sRank M c a b = sRank M c b a := by
  unfold sRank
  rw [sComps_comm, kVerts_comm, kEdges_comm]

/-- `Σ_pairs E_ab = E` on a properly 4-coloured map. -/
theorem sphere_sum_edges (hc : ∀ u v, M.Adj u v → c u ≠ c v) :
    ∑ p ∈ pairs, (kEdges M (fun _ => False) c p.1 p.2).card = M.graph.edgeFinset.card := by
  classical
  have hk : ∀ a b : Fin 4, kEdges M (fun _ => False) c a b =
      M.graph.edgeFinset.filter fun e => e.map c = s(a, b) := by
    intro a b
    ext e
    simp [kEdges]
  simp only [hk]
  have hmaps : Set.MapsTo (fun e : Sym2 (Fin n) => e.map c) M.graph.edgeFinset
      (pairs.image fun p => s(p.1, p.2)) := by
    intro e he
    induction e using Sym2.ind with
    | h u v =>
    simp only [mem_edgeFinset, mem_edgeSet, Finset.mem_coe] at he
    have hne : c u ≠ c v := hc _ _ he
    simp only [Sym2.map_mk, Finset.coe_image, Set.mem_image, Finset.mem_coe]
    rcases lt_or_gt_of_ne hne with hl | hl
    · exact ⟨(c u, c v), by simp [pairs, hl], rfl⟩
    · exact ⟨(c v, c u), by simp [pairs, hl], Sym2.eq_swap⟩
  rw [Finset.card_eq_sum_card_fiberwise hmaps, Finset.sum_image]
  intro p hp q hq e
  simp only [pairs, Finset.coe_filter, Finset.mem_univ, true_and, Set.mem_ofPred_eq] at hp hq
  rcases Sym2.eq_iff.mp e with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · exact Prod.ext h1 h2
  · exfalso; rw [h1, h2] at hp; exact absurd (hp.trans hq) (lt_irrefl _)

/-- `Σ_pairs V_ab = 3n` (every vertex lies in three pairs). -/
theorem sphere_sum_verts :
    ∑ p ∈ pairs, (kVertsFin (fun _ => False) c p.1 p.2).card = 3 * n := by
  classical
  have hk : ∀ a b : Fin 4, kVertsFin (fun _ => False) c a b =
      Finset.univ.filter fun v => c v = a ∨ c v = b := by
    intro a b
    ext v
    simp [kVertsFin, KAct]
  simp only [hk, Finset.card_filter]
  rw [Finset.sum_comm]
  have hv : ∀ v : Fin n, (∑ p ∈ pairs, if c v = p.1 ∨ c v = p.2 then 1 else 0) = 3 := by
    intro v
    generalize c v = x
    revert x
    decide
  simp only [hv, Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul]
  ring

/-- **Euler for the pair graphs of the sphere:** `Σ_pairs r_ab = Σ_pairs C_ab − 6`. -/
theorem sphere_six_pair_identity (htri : M.Triangulated) (hconn : M.graph.Connected)
    (d0 : M.Dart) (hc : ∀ u v, M.Adj u v → c u ≠ c v) :
    ∑ p ∈ pairs, sRank M c p.1 p.2 = ∑ p ∈ pairs, (sComps M c p.1 p.2 : ℤ) - 6 := by
  have hE := sphere_sum_edges hc
  have hV := sphere_sum_verts (c := c)
  have hT := edges_add_six M hconn htri d0
  unfold sRank
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib]
  have hE' : ∑ p ∈ pairs, ((kEdges M (fun _ => False) c p.1 p.2).card : ℤ) =
      M.graph.edgeFinset.card := by exact_mod_cast hE
  have hV' : ∑ p ∈ pairs, ((kVertsFin (fun _ => False) c p.1 p.2).card : ℤ) = 3 * n := by
    exact_mod_cast hV
  rw [hE', hV']
  have hT' : (M.graph.edgeFinset.card : ℤ) + 6 = 3 * n := by exact_mod_cast hT
  linarith

/-- The sphere lower bound `C_pq − 1 ≤ r_ab` for complementary pairs. -/
theorem sphere_lower (htri : M.Triangulated) (hconn : M.graph.Connected) (d0 : M.Dart)
    (hc : ∀ u v, M.Adj u v → c u ≠ c v) {a b p q : Fin 4}
    (hcov : ∀ x : Fin 4, x ≠ p → x ≠ q → x = a ∨ x = b) :
    (sComps M c p q : ℤ) - 1 ≤ sRank M c a b := by
  classical
  set H := sGraph M c p q
  have hnb : ∀ v, ∃ u, M.Adj v u := by
    intro v
    by_cases hv : v = d0.fst
    · subst hv; exact ⟨d0.snd, d0.adj⟩
    · obtain ⟨w⟩ := hconn.preconnected v d0.fst
      cases w with
      | nil => exact absurd rfl hv
      | cons e _ => exact ⟨_, e⟩
  have hprop : ∀ u v, M.Adj u v → ¬ False → ¬ False → c u ≠ c v := fun u v e _ _ => hc u v e
  set img := (kVertsFin (fun _ => False) c p q).image H.connectedComponentMk with himg
  have hS : (sComps M c p q : ℤ) = img.card := rfl
  unfold sRank
  by_cases hne : img.Nonempty
  · obtain ⟨K0, hK0⟩ := hne
    obtain ⟨v0, hv0, rfl⟩ := Finset.mem_image.1 hK0
    obtain ⟨u0, hu0⟩ := hnb v0
    have key := card_le_rank (Hab := sGraph M c a b) (H := H) (fun _ _ => Iff.rfl)
      (fun _ _ => Iff.rfl) htri hconn hnb hprop hcov (img.erase (H.connectedComponentMk v0))
      (fun K hK => by
        obtain ⟨v, hv, rfl⟩ := Finset.mem_image.1 (Finset.mem_of_mem_erase hK)
        exact ⟨v, (Finset.mem_filter.1 hv).2, rfl⟩)
      (fun _ _ _ hr => hr.elim) ⟨(v0, u0), hu0⟩
      (by
        intro v hv hva hm
        have hv0' : OnTri M ⟨(v0, u0), hu0⟩ v0 := Or.inl rfl
        rcases onTri_adj htri hv hv0' with rfl | e
        · exact (Finset.mem_erase.1 hm).1 rfl
        · exact (Finset.mem_erase.1 hm).1 (ConnectedComponent.sound
            (Adj.reachable (G := H) ⟨e, hva, (Finset.mem_filter.1 hv0).2⟩)))
    rw [Finset.card_erase_of_mem hK0] at key
    have h1 : 1 ≤ img.card := Finset.card_pos.2 ⟨_, hK0⟩
    unfold sComps
    push_cast [Nat.cast_sub h1] at key
    exact key
  · rw [Finset.not_nonempty_iff_eq_empty] at hne
    have key := card_le_rank (Hab := sGraph M c a b) (H := H) (fun _ _ => Iff.rfl)
      (fun _ _ => Iff.rfl) htri hconn hnb hprop hcov ∅ (by simp)
      (fun _ _ _ hr => hr.elim) d0 (by simp)
    unfold sComps
    rw [← himg, hne] at *
    simp only [Finset.card_empty, Nat.cast_zero] at key ⊢
    linarith

/-- **Planar pair duality on the sphere.** For a proper 4-colouring of a connected
triangulated sphere and complementary colour pairs `{a, b} ⊔ {p, q}`,
`r(G_ab) = C(G_pq) − 1`: the `{a, b}`-cycles are the boundaries between `{p, q}`-components. -/
theorem sphere_pair_duality (htri : M.Triangulated) (hconn : M.graph.Connected) (d0 : M.Dart)
    (hc : ∀ u v, M.Adj u v → c u ≠ c v) {a b p q : Fin 4} (hab : a ≠ b) (hap : a ≠ p)
    (haq : a ≠ q) (hbp : b ≠ p) (hbq : b ≠ q) (hpq : p ≠ q) :
    sRank M c a b = (sComps M c p q : ℤ) - 1 := by
  have b1 := sphere_lower htri hconn d0 hc (a := a) (b := b) (p := p) (q := q)
    (fun x => cover4 _ _ _ _ x hab hap haq hbp hbq hpq)
  have b2 := sphere_lower htri hconn d0 hc (a := p) (b := q) (p := a) (q := b)
    (fun x => cover4 _ _ _ _ x hpq hap.symm hbp.symm haq.symm hbq.symm hab)
  have b3 := sphere_lower htri hconn d0 hc (a := b) (b := p) (p := a) (q := q)
    (fun x => cover4 _ _ _ _ x hbp hab.symm hbq hap.symm hpq haq)
  have b4 := sphere_lower htri hconn d0 hc (a := a) (b := q) (p := b) (q := p)
    (fun x => cover4 _ _ _ _ x haq hab hap hbq.symm hpq.symm hbp)
  have b5 := sphere_lower htri hconn d0 hc (a := b) (b := q) (p := a) (q := p)
    (fun x => cover4 _ _ _ _ x hbq hab.symm hbp haq.symm hpq.symm hap)
  have b6 := sphere_lower htri hconn d0 hc (a := a) (b := p) (p := b) (q := q)
    (fun x => cover4 _ _ _ _ x hap hab haq hbp.symm hpq hbq)
  have hsum := sphere_six_pair_identity htri hconn d0 hc
  rw [sum_six (sRank M c) sRank_comm hab.symm hap.symm haq.symm hbp hbq hpq,
    sum_six (fun a b => (sComps M c a b : ℤ)) (fun a b => by rw [sComps_comm]) hab.symm
      hap.symm haq.symm hbp hbq hpq] at hsum
  linarith

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.sphere_pair_duality
#print axioms SimpleGraph.QuarterFloor.pair_dualities
#print axioms SimpleGraph.QuarterFloor.reach_alpha_B_of_not_lock1
#print axioms SimpleGraph.QuarterFloor.reach_alpha_A_of_not_lock2
#print axioms SimpleGraph.QuarterFloor.sigmaFixed_iff_C_alpha_mu_one
#print axioms SimpleGraph.QuarterFloor.sigmaFixed_iff_rank_AB_zero
#print axioms SimpleGraph.QuarterFloor.six_pair_identity_from_dualities
