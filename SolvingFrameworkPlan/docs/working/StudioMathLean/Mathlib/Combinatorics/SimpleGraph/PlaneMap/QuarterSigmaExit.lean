/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFloorH

/-!
# Lemma 3′: the exact condition for F5's `σ`-exit

Formalises Lemma 3′ (a)–(d) of `NightFloorR53.md`, generalising Lemma 3 of `QuarterFloorH`
(`sigSwap_spec`). Only the three link vertices `x j, x (j+1), x (j+2)` (colours `α, μ, α`) are
assumed to have degree five; nothing is assumed about `a = x (j+3)` (colour `A`) or
`b = x (j+4)` (colour `B`). In the note's frame `j = 0`: `w₄ = w (j+4)`, `w₀ = w j`,
`w₁ = w (j+1)`, `w₂ = w (j+2)`.

## Main results (sorry-free)

* `TripleBallP`: the 2-ball hypothesis restricted to `x j, x (j+1), x (j+2)`;
  `IcoBallP.triple` derives it from the full `IcoBallP`.
* `outer_shape` (**(a)**): `w₀, w₁ ∈ {A, B}` and distinct, `w₄ ∈ {μ, A}`, `w₂ ∈ {μ, B}`, and
  `w₀ = A → w₄ = w₂ = μ`.
* `sigma_component_iff` (**(b)**): the `{α, μ}`-component of `x (j+1)` is exactly
  `{x j, x (j+1), x (j+2)}` iff `(w₀, w₁, w₂, w₄) = (B, A, B, A)` (`OuterBABA`).
* `sigma_exit`: then `σ = sigSwap` is a Kempe step to a proper-off state, the image is unfilled
  with repeat index `j` (link `μ, α, μ, A, B`), and `σ` fixes every vertex off the triple.
* `lock1_after_sigma_iff`, `lock2_after_sigma_iff` (**(c)**): `Lock1 (σ c)` iff `w₁` reaches
  `x (j+3)` in the `{α, A}`-graph of `c` with `x (j+2)` deleted; `Lock2 (σ c)` iff `w₀` reaches
  `x (j+4)` in the `{α, B}`-graph of `c` with `x j` deleted. (No Jordan argument is needed:
  the other end of the triple is a leaf of the relevant two-colour graph.)
* `locks_die_of_deg5` (**(d)**): with the full `IcoBallP` and `w₃ ≠ α`, both locks of `σ c` die.
* `sigSwap_locks_of_R3`: Lemma 3 of `QuarterFloorH` (the lock part of `sigSwap_spec`) is the
  special case `R3At` (where `w₃ = μ`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Two-colour graphs with a deleted vertex -/

section generic
variable {V : Type*} {G : SimpleGraph V} {h : V}

variable (G h) in
/-- The `{a, b}`-graph of `c` in `G - h`, with the vertex `p` also deleted. -/
def pairDel (c : V → Fin 4) (a b : Fin 4) (p : V) : SimpleGraph V where
  Adj u v := (pairGraph G h c a b).Adj u v ∧ u ≠ p ∧ v ≠ p
  symm := ⟨fun _ _ e => ⟨e.1.symm, e.2.2, e.2.1⟩⟩
  loopless := ⟨fun _ e => e.1.1.ne rfl⟩

lemma reach_active {c : V → Fin 4} {a b : Fin 4} {s v : V}
    (r : (pairGraph G h c a b).Reachable s v) (hsv : s ≠ v) : Active h c a b v := by
  obtain ⟨p⟩ := r.symm
  cases p with
  | nil => exact (hsv rfl).elim
  | cons e _ => exact e.2.1

lemma not_reach_of_isolated {H : SimpleGraph V} {s t : V} (hst : s ≠ t)
    (ht : ∀ v, ¬ H.Adj t v) : ¬ H.Reachable s t := by
  intro r
  obtain ⟨p⟩ := r.symm
  cases p with
  | nil => exact hst rfl
  | cons e _ => exact ht _ e

/-- The transfer of a lock through a swap of a small component. `d` agrees with `c` off
`{m, p, q}`; in `d` the vertex `m` has colour `α` and `p, q` colour `μ`, while in `c` the
vertex `m` has colour `μ`. If `s` is the only `{α, X}`-neighbour of `m` in `d`, and `q` has at
most the one `{α, X}`-neighbour `r` other than `p` in `c`, then `m` reaches `t` in the
`{α, X}`-graph of `d` iff `s` reaches `t` in the `{α, X}`-graph of `c` minus `p`. -/
theorem lock_transfer {c d : V → Fin 4} {α μ X : Fin 4} {m p q r s t : V}
    (hαμ : α ≠ μ) (hXμ : X ≠ μ)
    (hdc : ∀ v, v ≠ m → v ≠ p → v ≠ q → d v = c v)
    (dm : d m = α) (dp : d p = μ) (dq : d q = μ) (cm : c m = μ) (hmh : m ≠ h)
    (hms : G.Adj m s) (hs : Active h d α X s)
    (mnb : ∀ v, G.Adj m v → Active h d α X v → v = s)
    (qnb : ∀ v, G.Adj q v → Active h c α X v → v ≠ p → v = r)
    (htm : t ≠ m) (htq : t ≠ q) :
    (pairGraph G h d α X).Reachable m t ↔ (pairDel G h c α X p).Reachable s t := by
  have inD : ∀ {v}, Active h d α X v → v ≠ p ∧ v ≠ q := by
    intro v hv
    constructor
    · rintro rfl
      rcases hv.2 with e | e
      · exact hαμ (e.symm.trans dp)
      · exact hXμ (e.symm.trans dp)
    · rintro rfl
      rcases hv.2 with e | e
      · exact hαμ (e.symm.trans dq)
      · exact hXμ (e.symm.trans dq)
  have inC : ∀ {v}, Active h c α X v → v ≠ m := by
    intro v hv e
    have hv2 := hv.2
    rw [e] at hv2
    rcases hv2 with e | e
    · exact hαμ (e.symm.trans cm)
    · exact hXμ (e.symm.trans cm)
  have toD : ∀ {v}, v ≠ m → v ≠ p → v ≠ q → Active h c α X v → Active h d α X v :=
    fun hm hp hq hv => ⟨hv.1, by rw [hdc _ hm hp hq]; exact hv.2⟩
  have toC : ∀ {v}, v ≠ m → v ≠ p → v ≠ q → Active h d α X v → Active h c α X v :=
    fun hm hp hq hv => ⟨hv.1, by rw [← hdc _ hm hp hq]; exact hv.2⟩
  have hmA : Active h d α X m := ⟨hmh, Or.inl dm⟩
  have hqm : q ≠ m := by
    intro e
    have := dq
    rw [e, dm] at this
    exact hαμ this
  constructor
  · intro R
    have key := reachable_invariant (H := pairGraph G h d α X)
      (P := fun v => v = m ∨ (pairDel G h c α X p).Reachable s v) ?_ (Or.inl rfl) R
    · rcases key with e | e
      · exact absurd e htm
      · exact e
    · intro u v e hu
      by_cases vm : v = m
      · exact Or.inl vm
      obtain ⟨vp, vq⟩ := inD e.2.2
      by_cases um : u = m
      · rw [um] at e
        rw [mnb v e.1 e.2.2]
        exact Or.inr (Reachable.refl _)
      · obtain ⟨up, uq⟩ := inD e.2.1
        exact Or.inr ((hu.resolve_left um).trans
          (Adj.reachable ⟨⟨e.1, toC um up uq e.2.1, toC vm vp vq e.2.2⟩, up, vp⟩))
  · intro R
    have Rs : (pairGraph G h d α X).Reachable m s := Adj.reachable ⟨hms, hmA, hs⟩
    have key := reachable_invariant (H := pairDel G h c α X p)
      (P := fun v => (pairGraph G h d α X).Reachable m v ∨
        (v = q ∧ (pairGraph G h d α X).Reachable m r)) ?_ (Or.inl Rs) R
    · rcases key with e | e
      · exact e
      · exact absurd e.1 htq
    · intro u v e hu
      have uC := e.1.2.1
      have vC := e.1.2.2
      by_cases vq : v = q
      · rw [vq] at e ⊢
        have ur := qnb u e.1.1.symm uC e.2.1
        rcases hu with hu | hu
        · exact Or.inr ⟨rfl, ur ▸ hu⟩
        · exact absurd hu.1 e.1.1.ne
      · rcases hu with hu | ⟨rfl, hr⟩
        · have uq : u ≠ q := fun e' => by
            rw [e'] at hu
            exact (inD (reach_active hu hqm.symm)).2 rfl
          exact Or.inl (hu.trans (Adj.reachable
            ⟨e.1.1, toD (inC uC) e.2.1 uq uC, toD (inC vC) e.2.2 vq vC⟩))
        · rw [qnb v e.1.1 vC e.2.2]
          exact Or.inl hr

end generic

/-! ### Finite facts -/

lemma f4_rest {p q r s x : Fin 4} (hpq : p ≠ q) (hpr : p ≠ r) (hps : p ≠ s) (hqr : q ≠ r)
    (hqs : q ≠ s) (hrs : r ≠ s) (hp : x ≠ p) (hq : x ≠ q) : x = r ∨ x = s := by
  revert p q r s x; decide

private lemma fne (j : Fin 5) : j + 3 ≠ j + 1 ∧ j + 3 ≠ j ∧ j + 4 ≠ j + 1 ∧ j + 4 ≠ j + 2 := by
  revert j; decide

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- The 2-ball hypothesis at the three link vertices `x j, x (j+1), x (j+2)` only: these have
degree five with neighbours as in `IcoBallP`, the triangles around them give the ring edges
`w₄w₀, w₀w₁, w₁w₂` and the edges `x (j+4) w₄`, `x (j+3) w₂`, and the four outer vertices
avoid `N[h]`. Nothing is assumed about the neighbourhoods of `x (j+3)`, `x (j+4)`. -/
structure TripleBallP (P : Pent M.graph h) (w : Fin 5 → Fin n) (j : Fin 5) : Prop where
  nbr0 : ∀ u, M.graph.Adj (P.x j) u ↔
    u = h ∨ u = P.x (j + 4) ∨ u = P.x (j + 1) ∨ u = w (j + 4) ∨ u = w j
  nbr1 : ∀ u, M.graph.Adj (P.x (j + 1)) u ↔
    u = h ∨ u = P.x j ∨ u = P.x (j + 2) ∨ u = w j ∨ u = w (j + 1)
  nbr2 : ∀ u, M.graph.Adj (P.x (j + 2)) u ↔
    u = h ∨ u = P.x (j + 1) ∨ u = P.x (j + 3) ∨ u = w (j + 1) ∨ u = w (j + 2)
  ring40 : M.graph.Adj (w (j + 4)) (w j)
  ring01 : M.graph.Adj (w j) (w (j + 1))
  ring12 : M.graph.Adj (w (j + 1)) (w (j + 2))
  adj4 : M.graph.Adj (P.x (j + 4)) (w (j + 4))
  adj3 : M.graph.Adj (P.x (j + 3)) (w (j + 2))
  off : ∀ i, w (j + 4) ≠ P.x i ∧ w j ≠ P.x i ∧ w (j + 1) ≠ P.x i ∧ w (j + 2) ≠ P.x i
  offh : w (j + 4) ≠ h ∧ w j ≠ h ∧ w (j + 1) ≠ h ∧ w (j + 2) ≠ h

variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {c : Fin n → Fin 4} {j : Fin 5}

/-- The full icosahedral ball gives the triple ball at every `j`. -/
theorem IcoBallP.triple (B : IcoBallP P w) (j : Fin 5) : TripleBallP P w j := by
  obtain ⟨-, -, -, -, -, a5, -, -, a8, -⟩ := B.adjs j
  obtain ⟨g0, g1, -, -⟩ := B.rings j
  have g4 := B.ring (j + 4)
  simp only [add_assoc, Fin.reduceAdd, add_zero] at g4
  exact ⟨B.nbr j, B.nbr1 j, B.nbr2 j, g4, g0, g1, a8, a5,
    fun i => ⟨B.off _ i, B.off _ i, B.off _ i, B.off _ i⟩,
    ⟨B.offh _, B.offh _, B.offh _, B.offh _⟩⟩

lemma TripleBallP.adjs (T : TripleBallP P w j) :
    M.graph.Adj (P.x j) (w (j + 4)) ∧ M.graph.Adj (P.x j) (w j) ∧
    M.graph.Adj (P.x (j + 1)) (w j) ∧ M.graph.Adj (P.x (j + 1)) (w (j + 1)) ∧
    M.graph.Adj (P.x (j + 2)) (w (j + 1)) ∧ M.graph.Adj (P.x (j + 2)) (w (j + 2)) :=
  ⟨(T.nbr0 _).2 (Or.inr (Or.inr (Or.inr (Or.inl rfl)))),
    (T.nbr0 _).2 (Or.inr (Or.inr (Or.inr (Or.inr rfl)))),
    (T.nbr1 _).2 (Or.inr (Or.inr (Or.inr (Or.inl rfl)))),
    (T.nbr1 _).2 (Or.inr (Or.inr (Or.inr (Or.inr rfl)))),
    (T.nbr2 _).2 (Or.inr (Or.inr (Or.inr (Or.inl rfl)))),
    (T.nbr2 _).2 (Or.inr (Or.inr (Or.inr (Or.inr rfl))))⟩

/-! ### (a) The outer colours around the triple -/

/-- **Lemma 3′(a).** With `α, μ, A, B = c (x j), c (x (j+1)), c (x (j+3)), c (x (j+4))`:
`w₀, w₁ ∈ {A, B}` are distinct, `w₄ ∈ {μ, A}`, `w₂ ∈ {μ, B}`, and `w₀ = A` forces
`w₄ = w₂ = μ`. -/
theorem outer_shape (T : TripleBallP P w j) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) :
    (c (w j) = c (P.x (j + 3)) ∨ c (w j) = c (P.x (j + 4))) ∧
    (c (w (j + 1)) = c (P.x (j + 3)) ∨ c (w (j + 1)) = c (P.x (j + 4))) ∧
    c (w j) ≠ c (w (j + 1)) ∧
    (c (w (j + 4)) = c (P.x (j + 1)) ∨ c (w (j + 4)) = c (P.x (j + 3))) ∧
    (c (w (j + 2)) = c (P.x (j + 1)) ∨ c (w (j + 2)) = c (P.x (j + 4))) ∧
    (c (w j) = c (P.x (j + 3)) →
      c (w (j + 4)) = c (P.x (j + 1)) ∧ c (w (j + 2)) = c (P.x (j + 1))) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨o4, o0, o1, o2⟩ := T.offh
  obtain ⟨a04, a00, a10, a11, a21, a22⟩ := T.adjs
  have pw : ∀ {i u}, M.graph.Adj (P.x i) u → u ≠ h → c u ≠ c (P.x i) :=
    fun e hu => (hc e (P.x_ne_h _) hu).symm
  have n10 : c (w (j + 1)) ≠ c (P.x j) := by rw [h02]; exact pw a21 o1
  have n20 : c (w (j + 2)) ≠ c (P.x j) := by rw [h02]; exact pw a22 o2
  have r40 := hc T.ring40 o4 o0
  have r01 := hc T.ring01 o0 o1
  have r12 := hc T.ring12 o1 o2
  have s0 := f4_rest h1.symm h3.symm h4.symm h13 h14 h34 (pw a00 o0) (pw a10 o0)
  have s1 := f4_rest h1.symm h3.symm h4.symm h13 h14 h34 n10 (pw a11 o1)
  have s4 := f4_rest h4.symm h1.symm h3.symm h14.symm h34.symm h13 (pw a04 o4) (pw T.adj4 o4)
  have s2 := f4_rest h3.symm h1.symm h4.symm h13.symm h34 h14 n20 (pw T.adj3 o2)
  refine ⟨s0, s1, r01, s4, s2, fun e0 => ⟨?_, ?_⟩⟩
  · rcases s4 with e | e
    · exact e
    · exact absurd (e.trans e0.symm) r40
  · have e1 : c (w (j + 1)) = c (P.x (j + 4)) := by
      rcases s1 with e | e
      · exact absurd (e0.trans e.symm) r01
      · exact e
    rcases s2 with e | e
    · exact e
    · exact absurd (e1.trans e.symm) r12

/-! ### (b) When `σ`'s component is the triple -/

variable (P) in
/-- The `{α, μ}`-component of `m = x (j+1)` is exactly `{x j, x (j+1), x (j+2)}`. -/
def TripleComp (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  ∀ v, (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) v ↔
    v = P.x j ∨ v = P.x (j + 1) ∨ v = P.x (j + 2)

variable (P w) in
/-- The outer colours `(w₀, w₁, w₂, w₄) = (B, A, B, A)`. -/
def OuterBABA (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  c (w j) = c (P.x (j + 4)) ∧ c (w (j + 1)) = c (P.x (j + 3)) ∧
    c (w (j + 2)) = c (P.x (j + 4)) ∧ c (w (j + 4)) = c (P.x (j + 3))

lemma triple_reach (hr : RepeatAt P c j) :
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1)) (P.x j) ∧
    (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Reachable (P.x (j + 1))
      (P.x (j + 2)) := by
  have adj12 := P.adj_cyc (j + 1)
  simp only [add_assoc, Fin.reduceAdd] at adj12
  exact ⟨Adj.reachable ⟨(P.adj_cyc j).symm, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨P.x_ne_h _, Or.inl rfl⟩⟩,
    Adj.reachable ⟨adj12, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨P.x_ne_h _, Or.inl hr.1.symm⟩⟩⟩

/-- **Lemma 3′(b).** `σ`'s component is exactly `{x j, x (j+1), x (j+2)}` iff
`(w₀, w₁, w₂, w₄) = (B, A, B, A)`. -/
theorem sigma_component_iff (T : TripleBallP P w j) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) : TripleComp P c j ↔ OuterBABA P w c j := by
  obtain ⟨rj, rj2⟩ := triple_reach (P := P) hr
  obtain ⟨s0, s1, -, s4, s2, -⟩ := outer_shape T hc hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨o4, o0, o1, o2⟩ := T.offh
  obtain ⟨a04, -, -, -, -, a22⟩ := T.adjs
  constructor
  · intro K
    have actT : ∀ {v}, (v = P.x j ∨ v = P.x (j + 1) ∨ v = P.x (j + 2)) →
        Active h c (c (P.x j)) (c (P.x (j + 1))) v := by
      rintro v (rfl | rfl | rfl)
      · exact ⟨P.x_ne_h _, Or.inl rfl⟩
      · exact ⟨P.x_ne_h _, Or.inr rfl⟩
      · exact ⟨P.x_ne_h _, Or.inl h02.symm⟩
    have out : ∀ {u v}, (v = P.x j ∨ v = P.x (j + 1) ∨ v = P.x (j + 2)) → M.graph.Adj v u →
        u ≠ h → (∀ i, u ≠ P.x i) → ¬ (c u = c (P.x j) ∨ c u = c (P.x (j + 1))) := by
      intro u v hv e hu hx hcu
      rcases (K u).1 (((K v).2 hv).trans (Adj.reachable ⟨e, actT hv, ⟨hu, hcu⟩⟩)) with
        f | f | f <;> exact hx _ f
    have e4 : c (w (j + 4)) = c (P.x (j + 3)) := by
      rcases s4 with e | e
      · exact absurd (Or.inr e) (out (Or.inl rfl) a04 o4 fun i => (T.off i).1)
      · exact e
    have e2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      rcases s2 with e | e
      · exact absurd (Or.inr e) (out (Or.inr (Or.inr rfl)) a22 o2 fun i => (T.off i).2.2.2)
      · exact e
    have e0 : c (w j) = c (P.x (j + 4)) := by
      rcases s0 with e | e
      · exact absurd (e4.trans e.symm) (hc T.ring40 o4 o0)
      · exact e
    have e1 : c (w (j + 1)) = c (P.x (j + 3)) := by
      rcases s1 with e | e
      · exact e
      · exact absurd (e.trans e2.symm) (hc T.ring12 o1 o2)
    exact ⟨e0, e1, e2, e4⟩
  · rintro ⟨e0, e1, e2, e4⟩ v
    have hAB : ∀ {v}, c v = c (P.x (j + 3)) ∨ c v = c (P.x (j + 4)) →
        ¬ (c v = c (P.x j) ∨ c v = c (P.x (j + 1))) := by
      rintro v (e | e) (f | f)
      · exact h3 (e.symm.trans f)
      · exact h13 (f.symm.trans e)
      · exact h4 (e.symm.trans f)
      · exact h14 (f.symm.trans e)
    have closed : ∀ u v, (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 1)))).Adj u v →
        (u = P.x j ∨ u = P.x (j + 1) ∨ u = P.x (j + 2)) →
        (v = P.x j ∨ v = P.x (j + 1) ∨ v = P.x (j + 2)) := by
      intro u v e hu
      have hv := e.2.2
      rcases hu with rfl | rfl | rfl
      · rcases (T.nbr0 v).1 e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hv.1
        · exact absurd hv.2 (hAB (Or.inr rfl))
        · exact Or.inr (Or.inl rfl)
        · exact absurd hv.2 (hAB (Or.inl e4))
        · exact absurd hv.2 (hAB (Or.inr e0))
      · rcases (T.nbr1 v).1 e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hv.1
        · exact Or.inl rfl
        · exact Or.inr (Or.inr rfl)
        · exact absurd hv.2 (hAB (Or.inr e0))
        · exact absurd hv.2 (hAB (Or.inl e1))
      · rcases (T.nbr2 v).1 e.1 with rfl | rfl | rfl | rfl | rfl
        · exact absurd rfl hv.1
        · exact Or.inr (Or.inl rfl)
        · exact absurd hv.2 (hAB (Or.inl rfl))
        · exact absurd hv.2 (hAB (Or.inl e1))
        · exact absurd hv.2 (hAB (Or.inr e2))
    constructor
    · intro R
      exact reachable_invariant closed (Or.inr (Or.inl rfl)) R
    · rintro (rfl | rfl | rfl)
      · exact rj
      · exact Reachable.refl _
      · exact rj2

/-! ### The `σ`-image -/

/-- `σ` at any unfilled state: a Kempe step to a proper-off state, unfilled with repeat index
`j` and link `(μ, α, μ, A, B)`. -/
theorem sigSwap_basic (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    KempeStep M.graph h c (sigSwap P c j) ∧ ProperOff M.graph h (sigSwap P c j) ∧
      RepeatAt P (sigSwap P c j) j ∧
      sigSwap P c j (P.x j) = c (P.x (j + 1)) ∧ sigSwap P c j (P.x (j + 1)) = c (P.x j) ∧
      sigSwap P c j (P.x (j + 2)) = c (P.x (j + 1)) ∧
      sigSwap P c j (P.x (j + 3)) = c (P.x (j + 3)) ∧
      sigSwap P c j (P.x (j + 4)) = c (P.x (j + 4)) := by
  obtain ⟨rj, rj2⟩ := triple_reach (P := P) hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have step : KempeStep M.graph h c (sigSwap P c j) :=
    kswap_step h1.symm (P.x_ne_h _) (Or.inr rfl)
  have s0 : sigSwap P c j (P.x j) = c (P.x (j + 1)) := kswap_mem rj rfl
  have s1 : sigSwap P c j (P.x (j + 1)) = c (P.x j) := kswap_mem' (Reachable.refl _) rfl
  have s2 : sigSwap P c j (P.x (j + 2)) = c (P.x (j + 1)) := kswap_mem rj2 h02.symm
  have s3 : sigSwap P c j (P.x (j + 3)) = c (P.x (j + 3)) := kswap_other h3 h13.symm
  have s4 : sigSwap P c j (P.x (j + 4)) = c (P.x (j + 4)) := kswap_other h4 h14.symm
  exact ⟨step, kempe_proper M.graph hc step,
    rep_of_vals s0 s1 s2 s3 s4 h1.symm h13.symm h14.symm h3.symm h4.symm h34, s0, s1, s2, s3, s4⟩

lemma sigSwap_out (K : TripleComp P c j) {v : Fin n} (h0 : v ≠ P.x j) (h1 : v ≠ P.x (j + 1))
    (h2 : v ≠ P.x (j + 2)) : sigSwap P c j v = c v :=
  kswap_out fun R => by rcases (K v).1 R with e | e | e <;> contradiction

/-- **Lemma 3′(b), the exit.** Under `(w₀, w₁, w₂, w₄) = (B, A, B, A)`, `σ` swaps exactly the
triple: a Kempe step to a proper-off state with repeat index `j`, fixing every other vertex. -/
theorem sigma_exit (T : TripleBallP P w j) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hO : OuterBABA P w c j) :
    TripleComp P c j ∧ KempeStep M.graph h c (sigSwap P c j) ∧
      ProperOff M.graph h (sigSwap P c j) ∧ RepeatAt P (sigSwap P c j) j ∧
      ∀ v, v ≠ P.x j → v ≠ P.x (j + 1) → v ≠ P.x (j + 2) → sigSwap P c j v = c v := by
  have K := (sigma_component_iff T hc hr).2 hO
  obtain ⟨st, hp, r', -⟩ := sigSwap_basic hc hr
  exact ⟨K, st, hp, r', fun _ a b d => sigSwap_out K a b d⟩

/-! ### (c) The locks of `σ c` -/

/-- **Lemma 3′(c), Lock 1.** Under `(B, A, B, A)`, `σ c` has Lock 1 iff `w₁` reaches
`a = x (j+3)` in the `{α, A}`-graph of `c` with `x (j+2)` deleted (`K_F − x₂`). -/
theorem lock1_after_sigma_iff (T : TripleBallP P w j) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hO : OuterBABA P w c j) :
    Lock1 P (sigSwap P c j) j ↔
      (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2))).Reachable
        (w (j + 1)) (P.x (j + 3)) := by
  have K := (sigma_component_iff T hc hr).2 hO
  obtain ⟨-, -, -, s0, s1, s2, s3, -⟩ := sigSwap_basic hc hr
  obtain ⟨e0, e1, -, -⟩ := hO
  obtain ⟨-, -, a10, a11, -, -⟩ := T.adjs
  obtain ⟨-, o0, o1, -⟩ := T.offh
  obtain ⟨-, h1, h3, h4, h13, -, h34⟩ := hr
  obtain ⟨f31, f30, -, -⟩ := fne j
  have dw : ∀ {u}, (∀ i, u ≠ P.x i) → sigSwap P c j u = c u :=
    fun hu => sigSwap_out K (hu _) (hu _) (hu _)
  have dw0 := dw fun i => (T.off i).2.1
  have dw1 := dw fun i => (T.off i).2.2.1
  unfold Lock1
  rw [s1, s3]
  refine lock_transfer (q := P.x j) (r := w (j + 4)) h1.symm h13.symm
    (fun v a b d => sigSwap_out K d a b) s1 s2 s0 rfl (P.x_ne_h _) a11
    ⟨o1, Or.inr (by rw [dw1, e1])⟩ ?_ ?_ (fun e => f31 (P.inj e)) (fun e => f30 (P.inj e))
  · intro v e hv
    rcases (T.nbr1 v).1 e with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hv.1
    · have hv2 := hv.2
      rw [s0] at hv2
      rcases hv2 with f | f
      · exact absurd f h1
      · exact absurd f h13
    · have hv2 := hv.2
      rw [s2] at hv2
      rcases hv2 with f | f
      · exact absurd f h1
      · exact absurd f h13
    · have hv2 := hv.2
      rw [dw0, e0] at hv2
      rcases hv2 with f | f
      · exact absurd f h4
      · exact absurd f.symm h34
    · rfl
  · intro v e hv hvp
    rcases (T.nbr0 v).1 e with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hv.1
    · rcases hv.2 with f | f
      · exact absurd f h4
      · exact absurd f.symm h34
    · rcases hv.2 with f | f
      · exact absurd f h1
      · exact absurd f h13
    · rfl
    · have hv2 := hv.2
      rw [e0] at hv2
      rcases hv2 with f | f
      · exact absurd f h4
      · exact absurd f.symm h34

/-- **Lemma 3′(c), Lock 2.** Under `(B, A, B, A)`, `σ c` has Lock 2 iff `w₀` reaches
`b = x (j+4)` in the `{α, B}`-graph of `c` with `x j` deleted (`K_B − x₀`). -/
theorem lock2_after_sigma_iff (T : TripleBallP P w j) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hO : OuterBABA P w c j) :
    Lock2 P (sigSwap P c j) j ↔
      (pairDel M.graph h c (c (P.x j)) (c (P.x (j + 4))) (P.x j)).Reachable
        (w j) (P.x (j + 4)) := by
  have K := (sigma_component_iff T hc hr).2 hO
  obtain ⟨-, -, -, s0, s1, s2, -, s4⟩ := sigSwap_basic hc hr
  obtain ⟨e0, e1, -, -⟩ := hO
  obtain ⟨-, -, a10, -, -, -⟩ := T.adjs
  obtain ⟨-, o0, -, -⟩ := T.offh
  obtain ⟨-, h1, h3, -, -, h14, h34⟩ := hr
  obtain ⟨-, -, f41, f42⟩ := fne j
  have dw : ∀ {u}, (∀ i, u ≠ P.x i) → sigSwap P c j u = c u :=
    fun hu => sigSwap_out K (hu _) (hu _) (hu _)
  have dw0 := dw fun i => (T.off i).2.1
  have dw1 := dw fun i => (T.off i).2.2.1
  unfold Lock2
  rw [s1, s4]
  refine lock_transfer (q := P.x (j + 2)) (r := w (j + 2)) h1.symm h14.symm
    (fun v a b d => sigSwap_out K b a d) s1 s0 s2 rfl (P.x_ne_h _) a10
    ⟨o0, Or.inr (by rw [dw0, e0])⟩ ?_ ?_ (fun e => f41 (P.inj e)) (fun e => f42 (P.inj e))
  · intro v e hv
    rcases (T.nbr1 v).1 e with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hv.1
    · have hv2 := hv.2
      rw [s0] at hv2
      rcases hv2 with f | f
      · exact absurd f h1
      · exact absurd f h14
    · have hv2 := hv.2
      rw [s2] at hv2
      rcases hv2 with f | f
      · exact absurd f h1
      · exact absurd f h14
    · rfl
    · have hv2 := hv.2
      rw [dw1, e1] at hv2
      rcases hv2 with f | f
      · exact absurd f h3
      · exact absurd f h34
  · intro v e hv hvp
    rcases (T.nbr2 v).1 e with rfl | rfl | rfl | rfl | rfl
    · exact absurd rfl hv.1
    · rcases hv.2 with f | f
      · exact absurd f h1
      · exact absurd f h14
    · rcases hv.2 with f | f
      · exact absurd f h3
      · exact absurd f h34
    · have hv2 := hv.2
      rw [e1] at hv2
      rcases hv2 with f | f
      · exact absurd f h3
      · exact absurd f h34
    · rfl

/-! ### (d) Degree five at `a` and `b` -/

/-- **Lemma 3′(d).** If moreover `x (j+3)`, `x (j+4)` have degree five (full `IcoBallP`) and
`w₃ ≠ α`, both locks of `σ c` die: `a` and `b` are isolated in `K_F − x₂`, `K_B − x₀`. -/
theorem locks_die_of_deg5 (B : IcoBallP P w) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hO : OuterBABA P w c j) (hw3 : c (w (j + 3)) ≠ c (P.x j)) :
    ¬ Lock1 P (sigSwap P c j) j ∧ ¬ Lock2 P (sigSwap P c j) j := by
  have T := B.triple j
  rw [lock1_after_sigma_iff T hc hr hO, lock2_after_sigma_iff T hc hr hO]
  obtain ⟨-, -, e2, e4⟩ := hO
  obtain ⟨-, -, h3, h4, -, -, h34⟩ := hr
  obtain ⟨-, -, -, -, -, -, a6, a7, -, -⟩ := B.adjs j
  constructor
  · refine not_reach_of_isolated (B.off _ _) fun v e => ?_
    obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
    rcases (B.nbr3 j v).1 ea with rfl | rfl | rfl | rfl | rfl
    · exact hv.1 rfl
    · exact vp rfl
    · rcases hv.2 with f | f
      · exact h4 f
      · exact h34 f.symm
    · have hv2 := hv.2
      rw [e2] at hv2
      rcases hv2 with f | f
      · exact h4 f
      · exact h34 f.symm
    · rcases hv.2 with f | f
      · exact hw3 f
      · exact hc a6 (P.x_ne_h _) (B.offh _) f.symm
  · refine not_reach_of_isolated (B.off _ _) fun v e => ?_
    obtain ⟨⟨ea, -, hv⟩, -, vp⟩ := e
    rcases (B.nbr4 j v).1 ea with rfl | rfl | rfl | rfl | rfl
    · exact hv.1 rfl
    · rcases hv.2 with f | f
      · exact h3 f
      · exact h34 f
    · exact vp rfl
    · rcases hv.2 with f | f
      · exact hw3 f
      · exact hc a7 (P.x_ne_h _) (B.offh _) f.symm
    · have hv2 := hv.2
      rw [e4] at hv2
      rcases hv2 with f | f
      · exact h3 f
      · exact h34 f

/-- Lemma 3 of `QuarterFloorH` (the lock part of `sigSwap_spec`) is the special case of
Lemma 3′ at an `R3` state, where `w₃ = μ ≠ α`. -/
theorem sigSwap_locks_of_R3 (B : IcoBallP P w) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) :
    ¬ Lock1 P (sigSwap P c j) j ∧ ¬ Lock2 P (sigSwap P c j) j := by
  obtain ⟨⟨hr, -, -⟩, e0, e1, e2, e3, e4⟩ := hR
  exact locks_die_of_deg5 B hc hr ⟨e0, e1, e2, e4⟩ (by rw [e3]; exact hr.2.1)

end sphere

end SimpleGraph.QuarterFloor
