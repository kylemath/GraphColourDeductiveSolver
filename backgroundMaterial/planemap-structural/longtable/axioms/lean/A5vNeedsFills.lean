/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import A5vJordan
public import Mathlib.Tactic

/-!
# A5v needs `Fills`: a twisted wheel

The wheel `W₅` (hub `0`, rim cycle `1‑2‑4‑3‑5‑1`, rim vertices cubic) with the **non-planar**
rotation `(4, 3, 1, 2, 5)` at the hub. At the perfect matching `{05, 12, 34}` (frame `k = 4`)
`E − Mt` is a DL figure-eight: `X = 0‑4‑2‑0` (through `f 0`, `f 3`, two vertices besides `0`,
so the parity clause holds) and `Y = 0‑3‑5‑1‑0` (through `f 1`, `f 2`). The partner `5` of the
hub lies on `Y`, so **A5v fails**, and so does its parity form (`|Mt ∩ E(X, Y)| = 2`).

Consequences: the loop `X` is not the boundary of any face set (`twisted_X_not_bounding`), and
this rotation system does not satisfy `Fills` (`twisted_not_fills`); the planar hypothesis of
`a5v` cannot be dropped. Found by `antisearch.py`-style random search (the
first hit, `n = 6`).
-/

@[expose] public section
namespace SimpleGraph.A5vTwist
open SimpleGraph.A5v

def adjB : Fin 6 → Fin 6 → Bool := fun a b =>
  (a, b) ∈ [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 5), (2, 4), (3, 4), (3, 5),
    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (2, 1), (5, 1), (4, 2), (4, 3), (5, 3)]

def graph : SimpleGraph (Fin 6) where
  Adj a b := adjB a b = true
  symm := ⟨fun a b h => by revert a b; decide⟩
  loopless := ⟨fun a h => by revert a h; decide⟩

instance : DecidableRel graph.Adj := fun a b => inferInstanceAs (Decidable (adjB a b = true))

/-- The rotation: `(4, 3, 1, 2, 5)` at the hub, sorted order at the rim vertices. -/
def nextTable : Fin 6 → Fin 6 → Fin 6 :=
  ![![0, 2, 5, 1, 3, 4], ![2, 0, 5, 0, 0, 0], ![1, 4, 0, 0, 0, 0], ![4, 0, 0, 0, 5, 0],
    ![2, 0, 3, 0, 0, 0], ![1, 3, 0, 0, 0, 0]]
def prevTable : Fin 6 → Fin 6 → Fin 6 :=
  ![![0, 3, 1, 4, 5, 2], ![5, 0, 0, 0, 0, 2], ![4, 0, 0, 0, 1, 0], ![5, 0, 0, 0, 0, 4],
    ![3, 0, 0, 2, 0, 0], ![3, 0, 0, 1, 0, 0]]

theorem next_adj : ∀ u v, graph.Adj u v → graph.Adj u (nextTable u v) := by decide
theorem prev_adj : ∀ u v, graph.Adj u v → graph.Adj u (prevTable u v) := by decide

def nextDart (d : graph.Dart) : graph.Dart := ⟨(d.fst, nextTable d.fst d.snd), next_adj _ _ d.adj⟩
def prevDart (d : graph.Dart) : graph.Dart := ⟨(d.fst, prevTable d.fst d.snd), prev_adj _ _ d.adj⟩

def rotation : RotationSystem graph where
  next := {
    toFun := nextDart
    invFun := prevDart
    left_inv := by
      have h : ∀ u v, graph.Adj u v → prevTable u (nextTable u v) = v := by decide
      intro d; apply Dart.ext; exact Prod.ext rfl (h _ _ d.adj)
    right_inv := by
      have h : ∀ u v, graph.Adj u v → nextTable u (prevTable u v) = v := by decide
      intro d; apply Dart.ext; exact Prod.ext rfl (h _ _ d.adj) }
  next_fst := fun _ => rfl
  cyclic := by
    have h : ∀ u v w, graph.Adj u v → graph.Adj u w →
      ∃ k : Fin 5, (nextTable u)^[k.val] v = w := by decide
    intro d e he
    obtain ⟨k, hk⟩ := h d.fst d.snd e.snd d.adj (by rw [he]; exact e.adj)
    refine ⟨k.val, ?_⟩
    apply Dart.ext
    have hi : ∀ k : ℕ, ((nextDart : graph.Dart → graph.Dart)^[k] d).toProd =
        (d.fst, (nextTable d.fst)^[k] d.snd) := by
      intro k
      induction k with
      | zero => rfl
      | succ k ih =>
        rw [Function.iterate_succ_apply']
        change (_, nextTable _ _) = _
        rw [ih]
        simp only [Function.iterate_succ_apply']
    change ((nextDart : graph.Dart → graph.Dart)^[k.val] d).toProd = e.toProd
    rw [hi]
    exact Prod.ext he hk

def fsT : Fin 5 → Fin 6 := ![4, 3, 1, 2, 5]

theorem fs_adj (i : Fin 5) : graph.Adj 0 (fsT i) := by revert i; decide

def hole : Hole5 rotation where
  v := 0
  f i := ⟨(0, fsT i), fs_adj i⟩
  fst_f _ := rfl
  next_f i := by
    have h : ∀ i : Fin 5, nextTable 0 (fsT i) = fsT (i + 1) := by decide
    exact Dart.ext _ _ (Prod.ext rfl (h i))
  inj := by
    intro i j hij
    have h : ∀ i j : Fin 5, fsT i = fsT j → i = j := by decide
    exact h i j (congrArg (fun d : graph.Dart => d.snd) hij)

def partnerT : Fin 6 → Fin 6 := ![5, 2, 1, 4, 3, 0]

def Mt : SimpleGraph (Fin 6) where
  Adj a b := partnerT a = b
  symm := ⟨fun a b h => by
    have hh : ∀ a : Fin 6, partnerT (partnerT a) = a := by decide
    rw [← h]; exact hh a⟩
  loopless := ⟨fun a h => by
    have hh : ∀ a : Fin 6, partnerT a ≠ a := by decide
    exact hh a h⟩

theorem pm : IsPerfectMatching graph Mt where
  le := by
    intro a b h
    have h' : partnerT a = b := h
    subst h'
    have hh : ∀ a : Fin 6, adjB a (partnerT a) = true := by decide
    exact hh a
  unique u := ⟨partnerT u, rfl, fun _ h => Eq.symm h⟩

theorem cubic : CubicOff hole := by
  intro u hu
  revert u
  decide

abbrev Q : SimpleGraph (Fin 6) := qGraph graph Mt 0

theorem qadj {a b : Fin 6} (h : adjB a b = true ∧ partnerT a ≠ b ∧ a ≠ 0 ∧ b ≠ 0) : Q.Adj a b :=
  ⟨h.1, h.2.1, h.2.2.1, h.2.2.2⟩

theorem reach_label (l : Fin 6 → Bool)
    (hl : ∀ a b, adjB a b = true → partnerT a ≠ b → a ≠ 0 → b ≠ 0 → l a = l b)
    {a b : Fin 6} (h : Q.Reachable a b) : l a = l b := by
  obtain ⟨p⟩ := h
  induction p with
  | nil => rfl
  | cons e _ ih => exact (hl _ _ e.1 e.2.1 e.2.2.1 e.2.2.2).trans ih

/-- The `X`-side labelling: `X = {2, 4}`. -/
def lx : Fin 6 → Bool := ![false, false, true, false, true, false]

theorem hlx : ∀ a b, adjB a b = true → partnerT a ≠ b → a ≠ 0 → b ≠ 0 → lx a = lx b := by
  decide

theorem r42 : Q.Reachable 4 2 := (qadj (by decide)).reachable
theorem r35 : Q.Reachable 3 5 := (qadj (by decide)).reachable
theorem r31 : Q.Reachable 3 1 := r35.trans (qadj (by decide)).reachable

theorem fig8 : Fig8 hole Mt 4 where
  mk_adj := rfl
  pairX := r42
  pairY := r31
  sepXY := fun h => absurd (reach_label lx hlx h) (by decide)
  cover := by
    intro u hu
    fin_cases u
    · exact absurd rfl hu
    · exact Or.inr r31
    · exact Or.inl r42
    · exact Or.inr (Reachable.refl _)
    · exact Or.inl (Reachable.refl _)
    · exact Or.inr r35

theorem inX_iff (u : Fin 6) : InX hole Mt 4 u ↔ lx u = true := by
  constructor
  · intro h
    rw [← reach_label lx hlx h]
    rfl
  · intro h
    fin_cases u
    · exact absurd h (by decide)
    · exact absurd h (by decide)
    · exact r42
    · exact absurd h (by decide)
    · exact Reachable.refl _
    · exact absurd h (by decide)

theorem xVerts_eq : xVerts hole Mt 4 = {2, 4} := by
  ext u
  simp only [xVerts, Finset.mem_filter, Finset.mem_univ, true_and, inX_iff]
  revert u
  decide

theorem xeven : XEven hole Mt 4 := by
  unfold XEven
  rw [xVerts_eq]
  decide

/-- **A5v fails** on the twisted wheel: the partner `5` of the hub is not on `X`. -/
theorem not_a5v : ¬ A5vAt hole Mt 4 := fun h => absurd ((inX_iff 5).mp h) (by decide)

/-- The parity form fails too (`|Mt ∩ E(X, Y)| = 2`), as `a5v_iff_parity` predicts. -/
theorem not_parity : ¬ Odd (crossXY hole Mt 4) :=
  fun h => not_a5v ((a5v_iff_parity hole pm fig8 xeven).mpr h)

/-- **The loop `X` does not bound** on the twisted wheel: `a5v_of_facePot` needs no degree or
`Fills` hypothesis, so a face potential of `X` would put the hub's partner on `X`. -/
theorem twisted_X_not_bounding : ¬ ∃ a, FacePot rotation (xEdges hole Mt 4) a :=
  fun ⟨_, ha⟩ => not_a5v (a5v_of_facePot hole pm fig8 ha)

/-- **The twisted wheel is not spherical**: if its rotation system satisfied `Fills`, `a5v`
would put the hub's partner on `X`. So `Fills` is exactly what `a5v` uses. -/
theorem twisted_not_fills : ¬ rotation.Fills := by
  intro hF
  let M : SphericalMap 6 := ⟨graph, rotation, hF⟩
  have hc : @CubicOff 6 M.graph M.rotation (SphericalMap.instDecidableRelFinAdjGraph M) hole := by
    intro u hu
    have h := cubic u hu
    convert h using 2
  exact not_a5v (a5v (M := M) hole pm hc fig8)

end SimpleGraph.A5vTwist

#print axioms SimpleGraph.A5vTwist.not_a5v
#print axioms SimpleGraph.A5vTwist.not_parity
#print axioms SimpleGraph.A5vTwist.twisted_X_not_bounding
#print axioms SimpleGraph.A5vTwist.twisted_not_fills
