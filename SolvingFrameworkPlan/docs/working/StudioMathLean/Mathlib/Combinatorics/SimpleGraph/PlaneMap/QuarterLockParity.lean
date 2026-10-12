/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.NoFrozen
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPairDuality

/-!
# The lock-parity lemma at a pentagonal hole

Formalises `TrackF/LockParity.md`. Let `h` be a hole with pentagonal link `x 0, …, x 4`
(`Pent`), and let `c` be proper off `h` and unfilled with repeat pair `{j, j+2}`
(`RepeatAt`), so the link reads `(α, μ, α, A, B)` at `j, …, j+4`. For a vertex set `X`,
`boundaryCard G X` is the number of darts of `G` leaving `X` (one for each edge of `G` with
exactly one end in `X`, edges to `h` included), and `oddCount G X` is the number of vertices
of `X` of odd degree in `G`.

## Theorem P (parity identity; no planarity)

The surface enters only through a face successor `φ` on darts with `(φ d).fst = d.snd` and
`φ³ = 1` (every face a triangle: any triangulated rotation system, i.e. any triangulated
*orientable* closed surface), and the star of `h`: the face of the dart `h → x i` has third
vertex `x (i ± 1)` (`LockParity.md` (F3)). Write `K_{pq}` for the `{p, q}`-component of
`x (j+2)` in `G − h` (`kcomp`).

* `parity_alphaA`: `|δ K_{αA}|` odd ⇔ `x j ∉ K_{αA}` (P1);
* `parity_alphaB`: `|δ K_{αB}|` odd ⇔ `x j ∉ K_{αB}` (P2);
* `parity_alphaMu`: `|δ K_{αμ}|` is odd (P3);
* `oddCount_eq_boundaryCard`: handshake, `#(X ∩ odd) ≡ |δ X| (mod 2)`;
* `lockParity2_iff_D2`, `lockParity1_iff_D1`: on any such surface, a state obeys lock
  parity iff it satisfies the hole duality (D2), resp. (D1) (`LockParity.md` §5).

The proof is the double count of `LockParity.md` §3, phrased with darts: the dart weight
`out + τ + τ ∘ symm` sums to `|δ X|` (the `τ` part cancels under `symm`), it sums to zero
over every face avoiding `h` (a finite table, `face_table`), and the darts of the five faces
at `h` give `starSum`, evaluated by `decide` in the three cases (`table_alphaA`, …).

## Theorem D and Theorem LP (sphere)

* `lock2_iff_not_reach_alphaA` (D2), `lock1_iff_not_reach_alphaB` (D1): from
  `not_reach_alpha_A_of_lock2` / `reach_alpha_A_of_not_lock2` and the `B` analogues;
* `lock2_iff_odd_boundary`, `lock2_iff_odd_oddCount`, `lock1_iff_odd_boundary`,
  `lock1_iff_odd_oddCount`, `alphaMu_odd_boundary`, `alphaMu_odd_oddCount` (Theorem LP).

On a `SphericalMap` the face successor is `M.rotation.faceNext` and the star hypothesis is
derived from `rotation_nbrs` (`NoFrozen`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill Finset

/-! ### Finite tables -/

/-- Indicator of a boolean in `ZMod 2`. -/
def ind2 (b : Bool) : ZMod 2 := if b then 1 else 0

/-- The weight of a dart `u → v` (`out + τ(u→v) + τ(v→u)`) from the flags
`u ∈ X`, `v ∈ X`, `c u = p`, `c u = r`, `c v = p`, `c v = r`. -/
def fB (iu iv pu ru pv rv : Bool) : ZMod 2 :=
  (if iu && !iv then 1 + ind2 pu + ind2 rv else 0) +
    (if iv && !iu then ind2 pv + ind2 ru else 0)

/-- The role of a colour relative to `p, q, r` (the fourth colour gets role `3`). -/
def role (p q r a : Fin 4) : Fin 4 :=
  if a = p then 0 else if a = q then 1 else if a = r then 2 else 3

lemma role_zero : ∀ p q r a : Fin 4, role p q r a = 0 ↔ a = p := by decide

lemma role_two : ∀ p q r a : Fin 4, p ≠ r → q ≠ r → (role p q r a = 2 ↔ a = r) := by decide

lemma role_le : ∀ p q r a : Fin 4, (role p q r a).val ≤ 1 ↔ a = p ∨ a = q := by decide

lemma role_inj : ∀ p q r a b : Fin 4, p ≠ q → p ≠ r → q ≠ r →
    role p q r a = role p q r b → a = b := by decide

set_option synthInstance.maxSize 1000 in
/-- **Each face avoiding the hole contributes zero** (Steps 2 and 3 of `LockParity.md`): a
properly coloured triangle meeting a Kempe-closed set `X` in its `{p, q}`-vertices. -/
lemma face_table : ∀ (a b e : Fin 4) (ia ib ie : Bool), a ≠ b → b ≠ e → a ≠ e →
    (ia = true → a.val ≤ 1) → (ib = true → b.val ≤ 1) → (ie = true → e.val ≤ 1) →
    (ia = true → b.val ≤ 1 → ib = true) → (ia = true → e.val ≤ 1 → ie = true) →
    (ib = true → a.val ≤ 1 → ia = true) → (ib = true → e.val ≤ 1 → ie = true) →
    (ie = true → a.val ≤ 1 → ia = true) → (ie = true → b.val ≤ 1 → ib = true) →
    fB ia ib (decide (a = 0)) (decide (a = 2)) (decide (b = 0)) (decide (b = 2)) +
      fB ib ie (decide (b = 0)) (decide (b = 2)) (decide (e = 0)) (decide (e = 2)) +
      fB ie ia (decide (e = 0)) (decide (e = 2)) (decide (a = 0)) (decide (a = 2)) = 0 := by
  decide

/-- The contribution of the five faces at the hole: flags relative to `j` (`I k` is
`x (j+k) ∈ X`, `Pp k` is `c (x (j+k)) = p`, `Rr k` is `c (x (j+k)) = r`), and the face of
`h → x i` has third vertex `x (i + s)`. -/
def starSum (I Pp Rr : Fin 5 → Bool) (s : Fin 5) : ZMod 2 :=
  ∑ k : Fin 5, (ind2 (I k) + fB (I k) (I (k + s)) (Pp k) (Rr k) (Pp (k + s)) (Rr (k + s)))

/-- Case `K_{αA}` (`p = α`, `q = A`, `r = μ`): odd iff `x j ∉ K`. -/
lemma table_alphaA : ∀ (b : Bool) (s : Fin 5), (s = 1 ∨ s = 4) →
    (starSum ![b, false, true, true, false] ![true, false, true, false, false]
      ![false, true, false, false, false] s = 1 ↔ b = false) := by
  decide

/-- Case `K_{αB}` (`p = α`, `q = B`, `r = μ`): odd iff `x j ∉ K`. -/
lemma table_alphaB : ∀ (b : Bool) (s : Fin 5), (s = 1 ∨ s = 4) →
    (starSum ![b, false, true, false, b] ![true, false, true, false, false]
      ![false, true, false, false, false] s = 1 ↔ b = false) := by
  decide

/-- Case `K_{αμ}` (`p = α`, `q = μ`, `r = A`): always odd. -/
lemma table_alphaMu : ∀ s : Fin 5, (s = 1 ∨ s = 4) →
    starSum ![true, true, true, false, false] ![true, false, true, false, false]
      ![false, false, false, true, false] s = 1 := by
  decide

/-- An injective choice of `x (i ± 1)` around the pentagon is a rotation. -/
lemma orient_table : ∀ b0 b1 b2 b3 b4 : Bool,
    (∀ i i' : Fin 5, i + (if ![b0, b1, b2, b3, b4] i then 1 else 4) =
      i' + (if ![b0, b1, b2, b3, b4] i' then 1 else 4) → i = i') →
    (b0 = true ∧ b1 = true ∧ b2 = true ∧ b3 = true ∧ b4 = true) ∨
      (b0 = false ∧ b1 = false ∧ b2 = false ∧ b3 = false ∧ b4 = false) := by
  decide

lemma fun5_ext {f g : Fin 5 → Bool} (h0 : f 0 = g 0) (h1 : f 1 = g 1) (h2 : f 2 = g 2)
    (h3 : f 3 = g 3) (h4 : f 4 = g 4) : f = g := by
  funext k
  fin_cases k
  exacts [h0, h1, h2, h3, h4]

lemma natCast_zmod2 (n : ℕ) : (n : ZMod 2) = if Odd n then 1 else 0 := by
  split_ifs with h
  · exact ZMod.natCast_eq_one_iff_odd.2 h
  · exact ZMod.natCast_eq_zero_iff_even.2 (Nat.not_odd_iff_even.1 h)

lemma zmod2_three (x : ZMod 2) : x + x + x = x := by
  rw [CharTwo.add_self_eq_zero, zero_add]

/-! ### Kempe components, boundary and odd vertices -/

section general
variable {V : Type*} [Fintype V] [DecidableEq V] {G : SimpleGraph V} [DecidableRel G.Adj]

variable (G) in
/-- The `{p, q}`-Kempe component `K_{pq}(v)` of `G − h`. -/
def kcomp (h : V) (c : V → Fin 4) (p q : Fin 4) (v : V) : Set V :=
  {w | (pairGraph G h c p q).Reachable v w}

variable (G) in
open Classical in
/-- `|δ(X)|`: the darts of `G` leaving `X`, one for each edge of `G` (edges at `h` included)
with exactly one end in `X`. -/
noncomputable def boundaryCard (X : Set V) : ℕ :=
  #{d : G.Dart | d.fst ∈ X ∧ d.snd ∉ X}

variable (G) in
open Classical in
/-- The number of vertices of `X` of odd degree in `G`. -/
noncomputable def oddCount (X : Set V) : ℕ :=
  #{v : V | v ∈ X ∧ Odd (G.degree v)}

lemma dsymm_fst (d : G.Dart) : d.symm.fst = d.snd := rfl

lemma dsymm_snd (d : G.Dart) : d.symm.snd = d.fst := rfl

/-- The reversal of darts as a permutation. -/
def dartSymmPerm : Equiv.Perm G.Dart := Function.Involutive.toPerm _ Dart.symm_involutive

lemma sum_dart_symm (f : G.Dart → ZMod 2) : ∑ d : G.Dart, f d.symm = ∑ d, f d :=
  Equiv.sum_comp (dartSymmPerm (G := G)) f

/-- A reversal-invariant dart function has even sum. -/
lemma sum_dart_symm_eq_zero (f : G.Dart → ZMod 2) (hf : ∀ d, f d.symm = f d) :
    ∑ d, f d = 0 := by
  refine Finset.sum_involution (fun d _ => d.symm) (fun d _ => ?_) (fun d _ _ => d.symm_ne)
    (fun d _ => mem_univ _) (fun d _ => d.symm_symm)
  rw [hf]
  exact CharTwo.add_self_eq_zero _

/-- **Step 1 (handshake).** `|X ∩ odd(G)| ≡ |δ(X)| (mod 2)`. -/
theorem oddCount_eq_boundaryCard (X : Set V) :
    (oddCount G X : ZMod 2) = boundaryCard G X := by
  classical
  unfold oddCount boundaryCard
  rw [natCast_card_filter, natCast_card_filter]
  calc (∑ v, if v ∈ X ∧ Odd (G.degree v) then (1 : ZMod 2) else 0)
      = ∑ v, ∑ d ∈ (univ : Finset G.Dart) with d.fst = v, (if d.fst ∈ X then (1 : ZMod 2) else 0) := by
        refine sum_congr rfl fun v _ => ?_
        rw [sum_congr rfl (g := fun _ => if v ∈ X then (1 : ZMod 2) else 0)
          (fun d hd => by rw [(mem_filter.1 hd).2]), sum_const, nsmul_eq_mul,
          dart_fst_fiber_card_eq_degree, natCast_zmod2]
        by_cases hv : v ∈ X <;> by_cases ho : Odd (G.degree v) <;> simp [hv, ho]
    _ = ∑ d : G.Dart, (if d.fst ∈ X then (1 : ZMod 2) else 0) :=
        by rw [Finset.sum_fiberwise]
    _ = ∑ d : G.Dart, ((if d.fst ∈ X ∧ d.snd ∈ X then (1 : ZMod 2) else 0) +
          (if d.fst ∈ X ∧ d.snd ∉ X then (1 : ZMod 2) else 0)) := by
        refine sum_congr rfl fun d _ => ?_
        by_cases a : d.fst ∈ X <;> by_cases b : d.snd ∈ X <;> simp [a, b]
    _ = _ := by
        rw [sum_add_distrib, sum_dart_symm_eq_zero _ (fun d => by
          simp only [dsymm_fst, dsymm_snd, and_comm]), zero_add]

/-! #### Kempe closure of a component -/

section kempe
variable {h : V} {c : V → Fin 4} {p q : Fin 4} {v : V}

lemma kcomp_active (hs : Active h c p q v) {w : V} (hw : w ∈ kcomp G h c p q v) :
    Active h c p q w :=
  reachable_invariant (H := pairGraph G h c p q) (fun _ _ e _ => e.2.2) hs hw

lemma kcomp_closed (hs : Active h c p q v) {w z : V} (hw : w ∈ kcomp G h c p q v)
    (e : G.Adj w z) (hz : z ≠ h) (hcz : c z = p ∨ c z = q) : z ∈ kcomp G h c p q v :=
  Reachable.trans hw (Adj.reachable ⟨e, kcomp_active hs hw, hz, hcz⟩)

lemma kcomp_adj (hs : Active h c p q v) {z : V} (e : G.Adj v z) (hz : z ≠ h)
    (hcz : c z = p ∨ c z = q) : z ∈ kcomp G h c p q v :=
  kcomp_closed hs (Reachable.refl v) e hz hcz

end kempe

/-! #### The dart weight and the double count -/

section core
variable (φ : Equiv.Perm G.Dart) (hφ : ∀ d, (φ d).fst = d.snd)
  (h3 : ∀ d, φ (φ (φ d)) = d)
variable {h : V} {X : Set V} {c : V → Fin 4} {p q r : Fin 4}

variable (h X c p r) in
open Classical in
/-- `τ` on darts leaving `X` and avoiding `h`: `[c u = p] + [c v = r]`. -/
noncomputable def tauW (d : G.Dart) : ZMod 2 :=
  if d.fst ≠ h ∧ d.snd ≠ h ∧ d.fst ∈ X ∧ d.snd ∉ X then
    ind2 (decide (c d.fst = p)) + ind2 (decide (c d.snd = r)) else 0

variable (h X c p r) in
open Classical in
/-- The dart weight `out + τ + τ ∘ symm`. -/
noncomputable def FW (d : G.Dart) : ZMod 2 :=
  (if d.fst ∈ X ∧ d.snd ∉ X then 1 else 0) + tauW h X c p r d + tauW h X c p r d.symm

open Classical in
lemma FW_eq_fB {d : G.Dart} (hu : d.fst ≠ h) (hv : d.snd ≠ h) :
    FW h X c p r d = fB (decide (d.fst ∈ X)) (decide (d.snd ∈ X)) (decide (c d.fst = p))
      (decide (c d.fst = r)) (decide (c d.snd = p)) (decide (c d.snd = r)) := by
  unfold FW tauW fB
  simp only [dsymm_fst, dsymm_snd]
  by_cases a : d.fst ∈ X <;> by_cases b : d.snd ∈ X <;> simp [a, b, hu, hv] <;> (try simp only [add_assoc]) <;> congr

lemma FW_of_fst (hXh : h ∉ X) {d : G.Dart} (hd : d.fst = h) : FW h X c p r d = 0 := by
  classical
  unfold FW tauW
  simp only [dsymm_fst, dsymm_snd, hd]
  simp [hXh]

open Classical in
lemma FW_of_snd (hXh : h ∉ X) {d : G.Dart} (hd : d.snd = h) :
    FW h X c p r d = if d.fst ∈ X then 1 else 0 := by
  unfold FW tauW
  simp only [dsymm_fst, dsymm_snd, hd]
  simp [hXh]

include hφ h3 in
lemma phi2_fst (d : G.Dart) : (φ (φ d)).fst = (φ d).snd := hφ _

include hφ h3 in
lemma phi2_snd (d : G.Dart) : (φ (φ d)).snd = d.fst := by
  have := hφ (φ (φ d))
  rw [h3] at this
  exact this.symm

/-- Sums over the darts at `h`. -/
lemma sum_darts_at (P : Pent G h) (f : G.Dart → ZMod 2) :
    ∑ e : G.Dart, (if e.fst = h then f e else 0) =
      ∑ i : Fin 5, f ⟨(h, P.x i), P.adj_h i⟩ := by
  rw [← sum_filter]
  have : univ.filter (fun e : G.Dart => e.fst = h) =
      univ.image (fun i : Fin 5 => (⟨(h, P.x i), P.adj_h i⟩ : G.Dart)) := by
    ext e
    simp only [mem_filter, mem_univ, true_and, mem_image]
    constructor
    · intro he
      have ha : G.Adj h e.snd := by rw [← he]; exact e.adj
      obtain ⟨i, hi⟩ := P.only e.snd ha
      exact ⟨i, Dart.ext _ _ (Prod.ext he.symm hi.symm)⟩
    · rintro ⟨i, rfl⟩
      rfl
  rw [this, sum_image]
  intro i _ i' _ hii
  exact P.inj (congrArg (fun d : G.Dart => d.snd) hii)

include hφ h3 in
/-- An injective choice of the third vertex at the star of `h` is a rotation. -/
lemma star_orient (P : Pent G h)
    (hy : ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + 1) ∨
      (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + 4)) :
    ∃ s : Fin 5, (s = 1 ∨ s = 4) ∧ ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + s) := by
  classical
  set y : Fin 5 → V := fun i => (φ ⟨(h, P.x i), P.adj_h i⟩).snd with hy_def
  have yinj : Function.Injective y := by
    intro i i' hii
    have e : φ (φ ⟨(h, P.x i), P.adj_h i⟩) = φ (φ ⟨(h, P.x i'), P.adj_h i'⟩) := by
      apply Dart.ext
      refine Prod.ext ?_ ?_
      · show (φ (φ _)).fst = (φ (φ _)).fst
        rw [phi2_fst φ hφ h3, phi2_fst φ hφ h3]
        exact hii
      · show (φ (φ _)).snd = (φ (φ _)).snd
        rw [phi2_snd φ hφ h3, phi2_snd φ hφ h3]
    have e2 := φ.injective (φ.injective e)
    exact P.inj (congrArg (fun d : G.Dart => d.snd) e2)
  set b : Fin 5 → Bool := fun i => decide (y i = P.x (i + 1)) with hb
  have hyb : ∀ i, y i = P.x (i + (if b i then 1 else 4)) := by
    intro i
    by_cases e : y i = P.x (i + 1)
    · simp [hb, e]
    · have : b i = false := by simp [hb, e]
      rw [this]
      exact (hy i).resolve_left e
  have hbv : b = ![b 0, b 1, b 2, b 3, b 4] := fun5_ext rfl rfl rfl rfl rfl
  have inj : ∀ i i' : Fin 5, i + (if ![b 0, b 1, b 2, b 3, b 4] i then 1 else 4) =
      i' + (if ![b 0, b 1, b 2, b 3, b 4] i' then 1 else 4) → i = i' := by
    intro i i' e
    rw [← hbv] at e
    apply yinj
    rw [hyb, hyb, e]
  rcases orient_table _ _ _ _ _ inj with ⟨t0, t1, t2, t3, t4⟩ | ⟨t0, t1, t2, t3, t4⟩
  · refine ⟨1, Or.inl rfl, fun i => ?_⟩
    have hbi : b i = true := by
      fin_cases i; exacts [t0, t1, t2, t3, t4]
    have := hyb i
    rw [hbi] at this
    exact this
  · refine ⟨4, Or.inr rfl, fun i => ?_⟩
    have hbi : b i = false := by
      fin_cases i; exacts [t0, t1, t2, t3, t4]
    have := hyb i
    rw [hbi] at this
    exact this

include hφ h3 in
open Classical in
/-- **The star formula** (Steps 1–4 of `LockParity.md` up to the case table): for a
Kempe-closed `X` of colours `{p, q}` avoiding `h`, `|δ X|` mod 2 is the contribution of the
five faces at `h`. -/
theorem boundary_eq_star (P : Pent G h) (s : Fin 5)
    (hs : ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + s))
    (hc : ProperOff G h c) (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (hXh : h ∉ X) (hXc : ∀ v ∈ X, c v = p ∨ c v = q)
    (hXcl : ∀ v ∈ X, ∀ w, G.Adj v w → w ≠ h → (c w = p ∨ c w = q) → w ∈ X) (j : Fin 5) :
    (boundaryCard G X : ZMod 2) =
      starSum (fun k => decide (P.x (j + k) ∈ X)) (fun k => decide (c (P.x (j + k)) = p))
        (fun k => decide (c (P.x (j + k)) = r)) s := by
  -- the boundary is the sum of the dart weight
  have hB : (boundaryCard G X : ZMod 2) = ∑ d : G.Dart, FW h X c p r d := by
    unfold boundaryCard FW
    rw [natCast_card_filter, sum_add_distrib, sum_add_distrib,
      sum_dart_symm (tauW h X c p r), add_assoc, CharTwo.add_self_eq_zero, add_zero]
  -- exclusivity of the three ways a face meets `h`
  have e1 : ∀ d : G.Dart, d.fst = h → d.snd ≠ h := fun d hd hd' => d.adj.ne (hd.trans hd'.symm)
  have e2 : ∀ d : G.Dart, d.fst = h → (φ d).snd ≠ h := by
    intro d hd hd'
    have := (φ (φ d)).adj.ne
    rw [phi2_fst φ hφ h3, phi2_snd φ hφ h3, hd, hd'] at this
    exact this rfl
  have e3 : ∀ d : G.Dart, d.snd = h → (φ d).snd ≠ h := by
    intro d hd hd'
    have := (φ d).adj.ne
    rw [hφ, hd, hd'] at this
    exact this rfl
  set Sout : G.Dart → Prop := fun d => d.fst ≠ h ∧ d.snd ≠ h ∧ (φ d).snd ≠ h with hSout
  have split : ∀ d, FW h X c p r d = (if Sout d then FW h X c p r d else 0) +
      (if d.fst = h then FW h X c p r d else 0) + (if d.snd = h then FW h X c p r d else 0) +
      (if (φ d).snd = h then FW h X c p r d else 0) := by
    intro d
    by_cases a : d.fst = h
    · simp [hSout, a, e1 d a, e2 d a]
    · by_cases b : d.snd = h
      · simp [hSout, a, b, e3 d b]
      · by_cases e : (φ d).snd = h
        · simp [hSout, a, b, e]
        · simp [hSout, a, b, e]
  -- T1: faces avoiding `h`
  have tri : ∀ u v w : V, u ≠ h → v ≠ h → w ≠ h → G.Adj u v → G.Adj v w → G.Adj w u →
      fB (decide (u ∈ X)) (decide (v ∈ X)) (decide (c u = p)) (decide (c u = r))
          (decide (c v = p)) (decide (c v = r)) +
        fB (decide (v ∈ X)) (decide (w ∈ X)) (decide (c v = p)) (decide (c v = r))
          (decide (c w = p)) (decide (c w = r)) +
        fB (decide (w ∈ X)) (decide (u ∈ X)) (decide (c w = p)) (decide (c w = r))
          (decide (c u = p)) (decide (c u = r)) = 0 := by
    intro u v w hu hv hw huv hvw hwu
    have rP : ∀ x, decide (c x = p) = decide (role p q r (c x) = 0) := fun x =>
      decide_eq_decide.2 (role_zero p q r (c x)).symm
    have rR : ∀ x, decide (c x = r) = decide (role p q r (c x) = 2) := fun x =>
      decide_eq_decide.2 (role_two p q r (c x) hpr hqr).symm
    rw [rP u, rP v, rP w, rR u, rR v, rR w]
    have ne : ∀ x y, G.Adj x y → x ≠ h → y ≠ h → role p q r (c x) ≠ role p q r (c y) :=
      fun x y e hx hy hrole => hc e hx hy (role_inj p q r _ _ hpq hpr hqr hrole)
    have mem : ∀ x, decide (x ∈ X) = true → (role p q r (c x)).val ≤ 1 := fun x hx =>
      (role_le p q r (c x)).2 (hXc x (of_decide_eq_true hx))
    have cl : ∀ x y, G.Adj x y → y ≠ h → decide (x ∈ X) = true →
        (role p q r (c y)).val ≤ 1 → decide (y ∈ X) = true := fun x y e hy hx hr =>
      decide_eq_true (hXcl x (of_decide_eq_true hx) y e hy ((role_le p q r (c y)).1 hr))
    exact face_table _ _ _ _ _ _ (ne u v huv hu hv) (ne v w hvw hv hw) (ne u w hwu.symm hu hw)
      (mem u) (mem v) (mem w) (cl u v huv hv) (cl u w hwu.symm hw) (cl v u huv.symm hu)
      (cl v w hvw hw) (cl w u hwu hu) (cl w v hvw.symm hv)
  have face : ∀ d, Sout d →
      FW h X c p r d + FW h X c p r (φ d) + FW h X c p r (φ (φ d)) = 0 := by
    rintro d ⟨hu, hv, hw⟩
    have f1 : (φ d).fst = d.snd := hφ d
    have f2 := phi2_fst φ hφ h3 d
    have f3 := phi2_snd φ hφ h3 d
    rw [FW_eq_fB hu hv, FW_eq_fB (d := φ d) (f1 ▸ hv) hw,
      FW_eq_fB (d := φ (φ d)) (f2 ▸ hw) (f3 ▸ hu), f1, f2, f3]
    have a1 := d.adj
    have a2 := (φ d).adj
    rw [f1] at a2
    have a3 := (φ (φ d)).adj
    rw [f2, f3] at a3
    exact tri _ _ _ hu hv hw a1 a2 a3
  have sout_phi : ∀ d, Sout (φ d) ↔ Sout d := by
    intro d
    simp only [hSout, hφ, phi2_snd φ hφ h3]
    tauto
  have T1 : ∑ d : G.Dart, (if Sout d then FW h X c p r d else 0) = 0 := by
    set Gs : G.Dart → ZMod 2 := fun d => if Sout d then FW h X c p r d else 0 with hGs
    have c1 : ∑ d : G.Dart, Gs (φ d) = ∑ d : G.Dart, Gs d := Equiv.sum_comp φ Gs
    have c2 : ∑ d : G.Dart, Gs (φ (φ d)) = ∑ d : G.Dart, Gs d := by
      rw [Equiv.sum_comp φ (fun d => Gs (φ d)), c1]
    show ∑ d : G.Dart, Gs d = 0
    calc ∑ d : G.Dart, Gs d = ∑ d : G.Dart, Gs d + ∑ d : G.Dart, Gs d + ∑ d : G.Dart, Gs d := (zmod2_three _).symm
      _ = ∑ d : G.Dart, Gs d + ∑ d : G.Dart, Gs (φ d) + ∑ d : G.Dart, Gs (φ (φ d)) := by rw [c1, c2]
      _ = ∑ d : G.Dart, (Gs d + Gs (φ d) + Gs (φ (φ d))) := by rw [sum_add_distrib, sum_add_distrib]
      _ = 0 := by
        refine sum_eq_zero fun d _ => ?_
        have s1 := sout_phi d
        have s2 := sout_phi (φ d)
        by_cases hd : Sout d
        · simp only [hGs, if_pos hd, if_pos (s1.2 hd), if_pos (s2.2 (s1.2 hd))]
          exact face d hd
        · simp only [hGs, if_neg hd, if_neg (fun x => hd (s1.1 x)),
            if_neg (fun x => hd (s1.1 (s2.1 x))), add_zero]
  -- T2: darts out of `h`
  have T2 : ∑ d : G.Dart, (if d.fst = h then FW h X c p r d else 0) = 0 :=
    sum_eq_zero fun d _ => by
      by_cases hd : d.fst = h
      · rw [if_pos hd, FW_of_fst hXh hd]
      · rw [if_neg hd]
  -- T3: darts into `h`
  have T3 : ∑ d : G.Dart, (if d.snd = h then FW h X c p r d else 0) =
      ∑ i : Fin 5, (if P.x i ∈ X then (1 : ZMod 2) else 0) := by
    calc ∑ d : G.Dart, (if d.snd = h then FW h X c p r d else 0)
        = ∑ d : G.Dart, (if d.symm.fst = h then (if d.symm.snd ∈ X then (1 : ZMod 2) else 0)
            else 0) := by
          refine sum_congr rfl fun d _ => ?_
          rw [dsymm_fst, dsymm_snd]
          by_cases hd : d.snd = h
          · rw [if_pos hd, if_pos hd, FW_of_snd hXh hd]
          · rw [if_neg hd, if_neg hd]
      _ = ∑ e : G.Dart, (if e.fst = h then (if e.snd ∈ X then (1 : ZMod 2) else 0) else 0) :=
          sum_dart_symm (fun e => if e.fst = h then (if e.snd ∈ X then (1 : ZMod 2) else 0)
            else 0)
      _ = _ := sum_darts_at P (fun e => if e.snd ∈ X then (1 : ZMod 2) else 0)
  -- T4: the third darts of the faces at `h`
  have T4 : ∑ d : G.Dart, (if (φ d).snd = h then FW h X c p r d else 0) =
      ∑ i : Fin 5, FW h X c p r (φ ⟨(h, P.x i), P.adj_h i⟩) := by
    calc ∑ d : G.Dart, (if (φ d).snd = h then FW h X c p r d else 0)
        = ∑ e : G.Dart, (if (φ (φ e)).snd = h then FW h X c p r (φ e) else 0) :=
          (Equiv.sum_comp φ (fun d => if (φ d).snd = h then FW h X c p r d else 0)).symm
      _ = ∑ e : G.Dart, (if e.fst = h then FW h X c p r (φ e) else 0) :=
          sum_congr rfl fun e _ => by rw [phi2_snd φ hφ h3]
      _ = _ := sum_darts_at P (fun e => FW h X c p r (φ e))
  have T4' : ∀ i : Fin 5, FW h X c p r (φ ⟨(h, P.x i), P.adj_h i⟩) =
      fB (decide (P.x i ∈ X)) (decide (P.x (i + s) ∈ X)) (decide (c (P.x i) = p))
        (decide (c (P.x i) = r)) (decide (c (P.x (i + s)) = p))
        (decide (c (P.x (i + s)) = r)) := by
    intro i
    have f1 : (φ ⟨(h, P.x i), P.adj_h i⟩).fst = P.x i := hφ _
    have g1 : (φ ⟨(h, P.x i), P.adj_h i⟩).fst ≠ h := by rw [f1]; exact (P.adj_h i).ne'
    have g2 : (φ ⟨(h, P.x i), P.adj_h i⟩).snd ≠ h := by rw [hs i]; exact (P.adj_h _).ne'
    rw [FW_eq_fB g1 g2, f1, hs i]
  rw [hB, sum_congr rfl fun d _ => split d, sum_add_distrib, sum_add_distrib, sum_add_distrib,
    T1, T2, T3, T4, zero_add, zero_add, ← sum_add_distrib]
  simp only [T4']
  refine (Equiv.sum_comp (Equiv.addLeft j) _).symm.trans ?_
  unfold starSum
  refine sum_congr rfl fun k _ => ?_
  simp only [Equiv.coe_addLeft, ind2, add_assoc, decide_eq_true_eq]
  congr

end core

/-! ### Theorem P: the three cases -/

section theoremP
variable (φ : Equiv.Perm G.Dart) (hφ : ∀ d, (φ d).fst = d.snd)
  (h3 : ∀ d, φ (φ (φ d)) = d)
variable {h : V} {c : V → Fin 4} {j : Fin 5}

lemma fin5_lp (j : Fin 5) : j + 0 = j ∧ j + 1 + 1 = j + 2 ∧ j + 2 + 1 = j + 3 ∧
    j + 4 + 1 = j ∧ j + 3 + 1 = j + 4 := by
  revert j; decide

/-- The star hypothesis (F3): the face of `h → x i` has third vertex `x (i ± 1)`. -/
def StarHyp (P : Pent G h) : Prop :=
  ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + 1) ∨
    (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + 4)

include hφ h3 in
open Classical in
/-- **(P1)** `|δ K_{αA}(x_{j+2})|` is odd iff `x j ∉ K_{αA}(x_{j+2})`. -/
theorem parity_alphaA (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c)
    (hr : RepeatAt P c j) :
    Odd (boundaryCard G (kcomp G h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)))) ↔
      ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x j) := by
  obtain ⟨h02, h1, h2, h3', h4, h5, h6⟩ := hr
  obtain ⟨i0, i1, i2, i4, i3⟩ := fin5_lp j
  obtain ⟨s, hs1, hs⟩ := star_orient φ hφ h3 P hy
  set X := kcomp G h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)) with hX
  have seed : Active h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)) :=
    ⟨(P.adj_h _).ne', Or.inl h02.symm⟩
  have hXh : h ∉ X := fun hh => (kcomp_active seed hh).1 rfl
  have key := boundary_eq_star φ hφ h3 P s hs hc (Ne.symm h2) (Ne.symm h1) (Ne.symm h4) hXh
    (fun v hv => (kcomp_active seed hv).2) (fun v hv w e hw hcw => kcomp_closed seed hv e hw hcw) j
  have n1 : P.x (j + 1) ∉ X := fun hm => by
    rcases (kcomp_active seed hm).2 with e | e
    · exact h1 e
    · exact h4 e
  have n4 : P.x (j + 4) ∉ X := fun hm => by
    rcases (kcomp_active seed hm).2 with e | e
    · exact h3' e
    · exact h6 e.symm
  have m3 : P.x (j + 3) ∈ X := kcomp_adj seed (by rw [← i2]; exact P.adj_cyc _)
    (P.adj_h _).ne' (Or.inr rfl)
  have m2 : P.x (j + 2) ∈ X := Reachable.refl _
  have eI : (fun k => decide (P.x (j + k) ∈ X)) =
      ![decide (P.x j ∈ X), false, true, true, false] :=
    fun5_ext (by simp [i0]) (decide_eq_false n1) (decide_eq_true m2) (decide_eq_true m3)
      (decide_eq_false n4)
  have eP : (fun k => decide (c (P.x (j + k)) = c (P.x j))) =
      ![true, false, true, false, false] :=
    fun5_ext (by simp [i0]) (decide_eq_false h1) (decide_eq_true h02.symm)
      (decide_eq_false h2) (decide_eq_false h3')
  have eR : (fun k => decide (c (P.x (j + k)) = c (P.x (j + 1)))) =
      ![false, true, false, false, false] :=
    fun5_ext (by simp [i0, Ne.symm h1]) (decide_eq_true rfl)
      (decide_eq_false (by rw [← h02]; exact Ne.symm h1)) (decide_eq_false (Ne.symm h4))
      (decide_eq_false (Ne.symm h5))
  rw [eI, eP, eR] at key
  rw [← ZMod.natCast_eq_one_iff_odd, key, table_alphaA _ s hs1]
  simp only [decide_eq_false_iff_not]
  rfl

include hφ h3 in
open Classical in
/-- **(P2)** `|δ K_{αB}(x_{j+2})|` is odd iff `x j ∉ K_{αB}(x_{j+2})`. -/
theorem parity_alphaB (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c)
    (hr : RepeatAt P c j) :
    Odd (boundaryCard G (kcomp G h c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 2)))) ↔
      ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x (j + 2)) (P.x j) := by
  obtain ⟨h02, h1, h2, h3', h4, h5, h6⟩ := hr
  obtain ⟨i0, i1, i2, i4, i3⟩ := fin5_lp j
  obtain ⟨s, hs1, hs⟩ := star_orient φ hφ h3 P hy
  set X := kcomp G h c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 2)) with hX
  have seed : Active h c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 2)) :=
    ⟨(P.adj_h _).ne', Or.inl h02.symm⟩
  have hXh : h ∉ X := fun hh => (kcomp_active seed hh).1 rfl
  have key := boundary_eq_star φ hφ h3 P s hs hc (Ne.symm h3') (Ne.symm h1) (Ne.symm h5) hXh
    (fun v hv => (kcomp_active seed hv).2) (fun v hv w e hw hcw => kcomp_closed seed hv e hw hcw) j
  have n1 : P.x (j + 1) ∉ X := fun hm => by
    rcases (kcomp_active seed hm).2 with e | e
    · exact h1 e
    · exact h5 e
  have n3 : P.x (j + 3) ∉ X := fun hm => by
    rcases (kcomp_active seed hm).2 with e | e
    · exact h2 e
    · exact h6 e
  have m2 : P.x (j + 2) ∈ X := Reachable.refl _
  have m40 : P.x (j + 4) ∈ X ↔ P.x j ∈ X := by
    have e : G.Adj (P.x (j + 4)) (P.x j) := by have := P.adj_cyc (j + 4); rwa [i4] at this
    constructor
    · intro hm
      exact kcomp_closed seed hm e (P.adj_h _).ne' (Or.inl rfl)
    · intro hm
      exact kcomp_closed seed hm e.symm (P.adj_h _).ne' (Or.inr rfl)
  have eI : (fun k => decide (P.x (j + k) ∈ X)) =
      ![decide (P.x j ∈ X), false, true, false, decide (P.x j ∈ X)] :=
    fun5_ext (by simp [i0]) (decide_eq_false n1) (decide_eq_true m2) (decide_eq_false n3)
      (decide_eq_decide.2 m40)
  have eP : (fun k => decide (c (P.x (j + k)) = c (P.x j))) =
      ![true, false, true, false, false] :=
    fun5_ext (by simp [i0]) (decide_eq_false h1) (decide_eq_true h02.symm)
      (decide_eq_false h2) (decide_eq_false h3')
  have eR : (fun k => decide (c (P.x (j + k)) = c (P.x (j + 1)))) =
      ![false, true, false, false, false] :=
    fun5_ext (by simp [i0, Ne.symm h1]) (decide_eq_true rfl)
      (decide_eq_false (by rw [← h02]; exact Ne.symm h1)) (decide_eq_false (Ne.symm h4))
      (decide_eq_false (Ne.symm h5))
  rw [eI, eP, eR] at key
  rw [← ZMod.natCast_eq_one_iff_odd, key, table_alphaB _ s hs1]
  simp only [decide_eq_false_iff_not]
  rfl

include hφ h3 in
open Classical in
/-- **(P3)** `|δ K_{αμ}(x_{j+2})|` is always odd. -/
theorem parity_alphaMu (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c)
    (hr : RepeatAt P c j) :
    Odd (boundaryCard G (kcomp G h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 2)))) := by
  obtain ⟨h02, h1, h2, h3', h4, h5, h6⟩ := hr
  obtain ⟨i0, i1, i2, i4, i3⟩ := fin5_lp j
  obtain ⟨s, hs1, hs⟩ := star_orient φ hφ h3 P hy
  set X := kcomp G h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 2)) with hX
  have seed : Active h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 2)) :=
    ⟨(P.adj_h _).ne', Or.inl h02.symm⟩
  have hXh : h ∉ X := fun hh => (kcomp_active seed hh).1 rfl
  have key := boundary_eq_star φ hφ h3 P s hs hc (Ne.symm h1) (Ne.symm h2) h4 hXh
    (fun v hv => (kcomp_active seed hv).2) (fun v hv w e hw hcw => kcomp_closed seed hv e hw hcw) j
  have n3 : P.x (j + 3) ∉ X := fun hm => by
    rcases (kcomp_active seed hm).2 with e | e
    · exact h2 e
    · exact h4 e.symm
  have n4 : P.x (j + 4) ∉ X := fun hm => by
    rcases (kcomp_active seed hm).2 with e | e
    · exact h3' e
    · exact h5 e.symm
  have m2 : P.x (j + 2) ∈ X := Reachable.refl _
  have m1 : P.x (j + 1) ∈ X := kcomp_adj seed (by rw [← i1]; exact (P.adj_cyc _).symm)
    (P.adj_h _).ne' (Or.inr rfl)
  have m0 : P.x j ∈ X := kcomp_closed seed m1 (P.adj_cyc j).symm (P.adj_h _).ne' (Or.inl rfl)
  have eI : (fun k => decide (P.x (j + k) ∈ X)) = ![true, true, true, false, false] :=
    fun5_ext (by simp [i0, m0]) (decide_eq_true m1) (decide_eq_true m2) (decide_eq_false n3)
      (decide_eq_false n4)
  have eP : (fun k => decide (c (P.x (j + k)) = c (P.x j))) =
      ![true, false, true, false, false] :=
    fun5_ext (by simp [i0]) (decide_eq_false h1) (decide_eq_true h02.symm)
      (decide_eq_false h2) (decide_eq_false h3')
  have eR : (fun k => decide (c (P.x (j + k)) = c (P.x (j + 3)))) =
      ![false, false, false, true, false] :=
    fun5_ext (by simp [i0, Ne.symm h2]) (decide_eq_false h4)
      (decide_eq_false (by rw [← h02]; exact Ne.symm h2)) (decide_eq_true rfl)
      (decide_eq_false (Ne.symm h6))
  rw [eI, eP, eR] at key
  rw [← ZMod.natCast_eq_one_iff_odd, key, table_alphaMu s hs1]

include hφ h3 in
open Classical in
/-- `LockParity.md` §5 (any surface): a state obeys lock parity for `Lock2` iff it satisfies
the hole duality (D2). -/
theorem lockParity2_iff_D2 (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c)
    (hr : RepeatAt P c j) :
    (Lock2 P c j ↔
        Odd (boundaryCard G (kcomp G h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))))) ↔
      (Lock2 P c j ↔
        ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x j)) := by
  rw [parity_alphaA φ hφ h3 P hy hc hr]

include hφ h3 in
open Classical in
/-- `LockParity.md` §5 (any surface): lock parity for `Lock1` iff the hole duality (D1). -/
theorem lockParity1_iff_D1 (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c)
    (hr : RepeatAt P c j) :
    (Lock1 P c j ↔
        Odd (boundaryCard G (kcomp G h c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 2))))) ↔
      (Lock1 P c j ↔
        ¬ (pairGraph G h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x (j + 2)) (P.x j)) := by
  rw [parity_alphaB φ hφ h3 P hy hc hr]

/-- Odd boundary and an odd number of odd-degree vertices are the same condition. -/
theorem odd_oddCount_iff (X : Set V) : Odd (oddCount G X) ↔ Odd (boundaryCard G X) := by
  rw [← ZMod.natCast_eq_one_iff_odd, ← ZMod.natCast_eq_one_iff_odd, oddCount_eq_boundaryCard]

end theoremP
end general

/-! ### The sphere: Theorem D and Theorem LP -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4} {j : Fin 5}

lemma sphere_tri3 (htri : M.Triangulated) (d : M.Dart) :
    M.rotation.faceNext (M.rotation.faceNext (M.rotation.faceNext d)) = d := by
  have := M.rotation.face_next_iterate_length d
  rw [htri d] at this
  simpa only [Function.iterate_succ_apply', Function.iterate_zero_apply] using this

lemma fin5_k : ∀ i : Fin 5, i + 4 + 1 = i ∧ i + 4 + 2 = i + 1 := by decide

/-- (F3) on the sphere: the face of `h → x i` has third vertex `x (i ± 1)`. -/
lemma sphere_starHyp (htri : M.Triangulated) (P : Pent M.graph h) :
    StarHyp M.rotation.faceNext P := by
  intro i
  obtain ⟨y1, y3, a1, a3, r12, -, hy⟩ := rotation_nbrs P (i + 4)
  obtain ⟨k1, k2⟩ := fin5_k i
  set d : M.Dart := ⟨(h, P.x i), P.adj_h i⟩ with hd
  set e := M.rotation.faceNext (M.rotation.faceNext d) with he
  have hfe : M.rotation.faceNext e = d := sphere_tri3 htri d
  have hn : M.rotation.next e.symm = M.rotation.next ⟨(h, y1), a1⟩ := by
    rw [← RotationSystem.face_next_apply, hfe, r12]
    exact Dart.ext _ _ (Prod.ext rfl (show P.x i = P.x (i + 4 + 1) by rw [k1]))
  have hes : e.symm = ⟨(h, y1), a1⟩ := M.rotation.next.injective hn
  have hsnd : (M.rotation.faceNext d).snd = y1 := by
    have := M.rotation.face_next_fst (M.rotation.faceNext d)
    rw [← this]
    exact congrArg (fun d : M.Dart => d.snd) hes
  rw [hsnd]
  rcases hy with ⟨e1, -⟩ | ⟨e1, -⟩
  · right; exact e1
  · left; rw [e1, k2]

/-- **(D2)** Kempe duality at the hole: `Lock2 ⇔ x j ∉ K_{αA}(x_{j+2})`. -/
theorem lock2_iff_not_reach_alphaA (htri : M.Triangulated) (P : Pent M.graph h)
    (hr : RepeatAt P c j) :
    Lock2 P c j ↔
      ¬ (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) (P.x j) :=
  ⟨fun hl hre => not_reach_alpha_A_of_lock2 P c j hr hl hre.symm,
    fun hn => by_contra fun hl => hn (reach_alpha_A_of_not_lock2 htri P hr hl).symm⟩

/-- **(D1)** Kempe duality at the hole: `Lock1 ⇔ x j ∉ K_{αB}(x_{j+2})`. -/
theorem lock1_iff_not_reach_alphaB (htri : M.Triangulated) (P : Pent M.graph h)
    (hr : RepeatAt P c j) :
    Lock1 P c j ↔
      ¬ (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 4)))).Reachable (P.x (j + 2)) (P.x j) :=
  ⟨fun hl hre => not_reach_alpha_B_of_lock1 P c j hr hl hre.symm,
    fun hn => by_contra fun hl => hn (reach_alpha_B_of_not_lock1 htri P hr hl).symm⟩

open Classical in
/-- **Lock parity (Lock2).** `Lock2 ⇔ |δ K_{αA}(x_{j+2})|` is odd. -/
theorem lock2_iff_odd_boundary (htri : M.Triangulated) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    Lock2 P c j ↔
      Odd (boundaryCard M.graph (kcomp M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)))) :=
  (lock2_iff_not_reach_alphaA htri P hr).trans
    (parity_alphaA M.rotation.faceNext M.rotation.face_next_fst (sphere_tri3 htri) P
      (sphere_starHyp htri P) hc hr).symm

open Classical in
/-- **Lock parity (Lock2), odd-degree form.** `Lock2 ⇔ K_{αA}(x_{j+2})` contains an odd
number of vertices of odd degree in `G`. -/
theorem lock2_iff_odd_oddCount (htri : M.Triangulated) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    Lock2 P c j ↔
      Odd (oddCount M.graph (kcomp M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)))) :=
  (lock2_iff_odd_boundary htri P hc hr).trans (odd_oddCount_iff _).symm

open Classical in
/-- **Lock parity (Lock1).** `Lock1 ⇔ |δ K_{αB}(x_{j+2})|` is odd. -/
theorem lock1_iff_odd_boundary (htri : M.Triangulated) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    Lock1 P c j ↔
      Odd (boundaryCard M.graph (kcomp M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 2)))) :=
  (lock1_iff_not_reach_alphaB htri P hr).trans
    (parity_alphaB M.rotation.faceNext M.rotation.face_next_fst (sphere_tri3 htri) P
      (sphere_starHyp htri P) hc hr).symm

open Classical in
/-- **Lock parity (Lock1), odd-degree form.** -/
theorem lock1_iff_odd_oddCount (htri : M.Triangulated) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    Lock1 P c j ↔
      Odd (oddCount M.graph (kcomp M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x (j + 2)))) :=
  (lock1_iff_odd_boundary htri P hc hr).trans (odd_oddCount_iff _).symm

open Classical in
/-- **Lock parity (`{α, μ}`).** `|δ K_{αμ}(x_{j+2})|` is always odd. -/
theorem alphaMu_odd_boundary (htri : M.Triangulated) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    Odd (boundaryCard M.graph (kcomp M.graph h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 2)))) :=
  parity_alphaMu M.rotation.faceNext M.rotation.face_next_fst (sphere_tri3 htri) P
    (sphere_starHyp htri P) hc hr

open Classical in
/-- **Lock parity (`{α, μ}`), odd-degree form.** -/
theorem alphaMu_odd_oddCount (htri : M.Triangulated) (P : Pent M.graph h)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    Odd (oddCount M.graph (kcomp M.graph h c (c (P.x j)) (c (P.x (j + 1))) (P.x (j + 2)))) :=
  (odd_oddCount_iff _).2 (alphaMu_odd_boundary htri P hc hr)

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.parity_alphaA
#print axioms SimpleGraph.QuarterFloor.parity_alphaB
#print axioms SimpleGraph.QuarterFloor.parity_alphaMu
#print axioms SimpleGraph.QuarterFloor.lockParity2_iff_D2
#print axioms SimpleGraph.QuarterFloor.lockParity1_iff_D1
#print axioms SimpleGraph.QuarterFloor.lock2_iff_not_reach_alphaA
#print axioms SimpleGraph.QuarterFloor.lock1_iff_not_reach_alphaB
#print axioms SimpleGraph.QuarterFloor.lock2_iff_odd_boundary
#print axioms SimpleGraph.QuarterFloor.lock2_iff_odd_oddCount
#print axioms SimpleGraph.QuarterFloor.lock1_iff_odd_boundary
#print axioms SimpleGraph.QuarterFloor.lock1_iff_odd_oddCount
#print axioms SimpleGraph.QuarterFloor.alphaMu_odd_boundary
#print axioms SimpleGraph.QuarterFloor.alphaMu_odd_oddCount
