/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLockParity

/-!
# Kempe chain counts at a pentagonal hole (Track I, `RigidIsolation.md` §0 and Lemma 3)

`chainCount G h c p q` is the number of `{p, q}`-Kempe chains of `G − h`: the connected
components of `pairGraph G h c p q` that contain an active vertex (a vertex `≠ h` coloured
`p` or `q`). `nChains G h c` is the total number of Kempe chains, the sum over the six
unordered colour pairs. It does not depend on a frame.

## Results

* `nChains_roles`: in the frame of an unfilled state (`RepeatAt`, link colours
  `(α, μ, α, A, B)`), `N = #αμ + #AB + #αA + #μB + #αB + #μA`.
* `eight_le_nChains` (Lemma 3, first half; sphere): a doubly locked state has `N ≥ 8`,
  because `#αA ≥ 2` and `#αB ≥ 2` by the formal Theorem D (`lock2_iff_not_reach_alphaA`,
  `lock1_iff_not_reach_alphaB`) and every other count is at least one.
* `rigidAt_iff` (Lemma 3, second half; sphere): a doubly locked state is rigid (counts
  `(1, 1, 2, 1, 2, 1)`) iff `N = 8`.
* `chainCount_piMove_alphaA`, `chainCount_piMove_muB`: `π` leaves the `{α, A}` and
  `{μ, B}` chain counts unchanged at a doubly locked state (the primal form of
  `F12′ = F13` in Lemma 4(c)), so `N(π c) − N(c)` only involves the other four pairs
  (`nChains_piMove_sub`).
* `rigid_isolation_of_law`: **Theorem 6 ⇒ rigid isolation**. `ChainParityLaw P` is the
  statement of Theorem 6 (`N(π c) + N(c)` is odd iff `π c` is doubly locked, for every
  proper doubly locked `c`); it is a hypothesis here, not proved.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill Finset

/-! ### Counting chains (any graph) -/

section general
variable {V : Type*} [Fintype V] (G : SimpleGraph V)

open Classical in
/-- The number of `{p, q}`-Kempe chains of `G − h`: components of the pair graph that
contain an active vertex. -/
noncomputable def chainCount (h : V) (c : V → Fin 4) (p q : Fin 4) : ℕ :=
  #((univ.filter (fun v => Active h c p q v)).image (pairGraph G h c p q).connectedComponentMk)

/-- The total number of Kempe chains `N`: the sum over the six unordered colour pairs. -/
noncomputable def nChains (h : V) (c : V → Fin 4) : ℕ :=
  ∑ p : Fin 4, ∑ q : Fin 4, if p < q then chainCount G h c p q else 0

variable {G} {h : V} {c : V → Fin 4}

lemma chainCount_comm (p q : Fin 4) : chainCount G h c p q = chainCount G h c q p := by
  classical
  have e : ∀ v, Active h c p q v ↔ Active h c q p v := fun v => by
    simp only [Active, or_comm]
  unfold chainCount
  rw [pairGraph_comm_gen c p q, Finset.filter_congr (fun v _ => e v)]

/-- Chain counts only depend on the active set and the pair graph. -/
lemma chainCount_congr {c d : V → Fin 4} {p q r s : Fin 4}
    (hA : ∀ v, Active h c p q v ↔ Active h d r s v)
    (hG : pairGraph G h c p q = pairGraph G h d r s) :
    chainCount G h c p q = chainCount G h d r s := by
  classical
  unfold chainCount
  rw [Finset.filter_congr (fun v _ => hA v), hG]

lemma one_le_chainCount {p q : Fin 4} {v : V} (hv : Active h c p q v) :
    1 ≤ chainCount G h c p q := by
  classical
  unfold chainCount
  exact Finset.card_pos.mpr ⟨_, Finset.mem_image_of_mem _ (by simpa using hv)⟩

lemma two_le_chainCount {p q : Fin 4} {u w : V} (hu : Active h c p q u)
    (hw : Active h c p q w) (hn : ¬ (pairGraph G h c p q).Reachable u w) :
    2 ≤ chainCount G h c p q := by
  classical
  unfold chainCount
  exact Finset.one_lt_card.mpr ⟨_, Finset.mem_image_of_mem _ (by simpa using hu), _,
    Finset.mem_image_of_mem _ (by simpa using hw), fun e => hn (ConnectedComponent.eq.mp e)⟩

/-- An `{a, b}`-swap leaves the number of `{a, b}`-chains unchanged. -/
lemma chainCount_swap_same (a b : Fin 4) (S : Set V) :
    chainCount G h (swap c a b S) a b = chainCount G h c a b :=
  chainCount_congr (fun v => active_swap_same c a b S v) (pairGraph_swap_same c a b S)

/-- An `{a, b}`-swap leaves the number of `{x, y}`-chains unchanged when `{x, y}` avoids
`{a, b}`. -/
lemma chainCount_swap_other (a b : Fin 4) (S : Set V) {x y : Fin 4}
    (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    chainCount G h (swap c a b S) x y = chainCount G h c x y :=
  chainCount_congr (fun v => by
      simp only [Active, swap_preserves_eq hxa hxb, swap_preserves_eq hya hyb])
    (pairGraph_swap_other c a b S hxa hxb hya hyb)

end general

/-! ### The sum over the six pairs in a frame -/

/-- For a symmetric `f` and four distinct colours, the sum over unordered pairs is the sum
over the six role pairs. -/
lemma sum_pairs_roles (f : Fin 4 → Fin 4 → ℕ) (hf : ∀ p q, f p q = f q p) {a b d e : Fin 4}
    (hab : a ≠ b) (had : a ≠ d) (hae : a ≠ e) (hbd : b ≠ d) (hbe : b ≠ e) (hde : d ≠ e) :
    (∑ p : Fin 4, ∑ q : Fin 4, if p < q then f p q else 0) =
      f a b + f d e + f a d + f b e + f a e + f b d := by
  have h10 := hf 1 0
  have h20 := hf 2 0
  have h30 := hf 3 0
  have h21 := hf 2 1
  have h31 := hf 3 1
  have h32 := hf 3 2
  simp only [Fin.sum_univ_four]
  fin_cases a <;> fin_cases b <;> fin_cases d <;> fin_cases e <;>
    simp (config := { decide := true }) only [] at hab had hae hbd hbe hde ⊢ <;>
    simp (config := { decide := true }) only [Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk,
      Fin.isValue, ite_true, ite_false] at * <;> omega

/-! ### The sphere: Lemma 3 and rigid isolation from Theorem 6 -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4} {j : Fin 5}

/-- `N` in the frame of an unfilled state: `#αμ + #AB + #αA + #μB + #αB + #μA`. -/
theorem nChains_roles (P : Pent M.graph h) (hr : RepeatAt P c j) :
    nChains M.graph h c =
      chainCount M.graph h c (c (P.x j)) (c (P.x (j + 1))) +
      chainCount M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) +
      chainCount M.graph h c (c (P.x j)) (c (P.x (j + 3))) +
      chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) +
      chainCount M.graph h c (c (P.x j)) (c (P.x (j + 4))) +
      chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3))) := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  exact sum_pairs_roles _ (fun p q => chainCount_comm p q) (Ne.symm h1) (Ne.symm h3)
    (Ne.symm h4) h13 h14 h34

variable (P : Pent M.graph h) in
/-- **Rigid** (TrackH H4): doubly locked with chain counts
`(#αμ, #AB, #αA, #μB, #αB, #μA) = (1, 1, 2, 1, 2, 1)`. -/
def RigidAt (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  DoublyLocked P c j ∧
  chainCount M.graph h c (c (P.x j)) (c (P.x (j + 1))) = 1 ∧
  chainCount M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) = 1 ∧
  chainCount M.graph h c (c (P.x j)) (c (P.x (j + 3))) = 2 ∧
  chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) = 1 ∧
  chainCount M.graph h c (c (P.x j)) (c (P.x (j + 4))) = 2 ∧
  chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3))) = 1

lemma nChains_of_rigidAt {P : Pent M.graph h} (hR : RigidAt P c j) :
    nChains M.graph h c = 8 := by
  obtain ⟨hd, e1, e2, e3, e4, e5, e6⟩ := hR
  rw [nChains_roles P hd.1, e1, e2, e3, e4, e5, e6]

/-- The six lower bounds of Lemma 3 at a doubly locked state on the sphere. -/
lemma chain_lower_bounds (htri : M.Triangulated) (P : Pent M.graph h)
    (hd : DoublyLocked P c j) :
    1 ≤ chainCount M.graph h c (c (P.x j)) (c (P.x (j + 1))) ∧
    1 ≤ chainCount M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) ∧
    2 ≤ chainCount M.graph h c (c (P.x j)) (c (P.x (j + 3))) ∧
    1 ≤ chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) ∧
    2 ≤ chainCount M.graph h c (c (P.x j)) (c (P.x (j + 4))) ∧
    1 ≤ chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3))) := by
  obtain ⟨hr, l1, l2⟩ := hd
  have a0 : ∀ q, Active h c (c (P.x j)) q (P.x j) := fun _ => ⟨P.x_ne_h _, Or.inl rfl⟩
  have a2 : ∀ q, Active h c (c (P.x j)) q (P.x (j + 2)) :=
    fun _ => ⟨P.x_ne_h _, Or.inl hr.1.symm⟩
  refine ⟨one_le_chainCount (a0 _), one_le_chainCount ⟨P.x_ne_h (j + 3), Or.inl rfl⟩,
    two_le_chainCount (a2 _) (a0 _) ((lock2_iff_not_reach_alphaA htri P hr).1 l2),
    one_le_chainCount ⟨P.x_ne_h (j + 1), Or.inl rfl⟩,
    two_le_chainCount (a2 _) (a0 _) ((lock1_iff_not_reach_alphaB htri P hr).1 l1),
    one_le_chainCount ⟨P.x_ne_h (j + 1), Or.inl rfl⟩⟩

/-- **Lemma 3 (first half).** A doubly locked state on a triangulated sphere has at least
eight Kempe chains. -/
theorem eight_le_nChains (htri : M.Triangulated) (P : Pent M.graph h)
    (hd : DoublyLocked P c j) : 8 ≤ nChains M.graph h c := by
  obtain ⟨b1, b2, b3, b4, b5, b6⟩ := chain_lower_bounds htri P hd
  rw [nChains_roles P hd.1]
  omega

/-- **Lemma 3 (second half).** A doubly locked state on a triangulated sphere is rigid iff
it has exactly eight Kempe chains. -/
theorem rigidAt_iff (htri : M.Triangulated) (P : Pent M.graph h) (hd : DoublyLocked P c j) :
    RigidAt P c j ↔ nChains M.graph h c = 8 := by
  refine ⟨nChains_of_rigidAt, fun h8 => ?_⟩
  obtain ⟨b1, b2, b3, b4, b5, b6⟩ := chain_lower_bounds htri P hd
  rw [nChains_roles P hd.1] at h8
  exact ⟨hd, by omega, by omega, by omega, by omega, by omega, by omega⟩

/-- At a doubly locked state `π` is the `{α, A}`-swap `rot3`. -/
lemma piMove_of_dl {P : Pent M.graph h} (hd : DoublyLocked P c j) :
    piMove P c = rot3 P c j := by
  classical
  rw [piMove_rep hd.1, ite_eq_left hd.2.2]

/-- `π` leaves the number of `{α, A}`-chains unchanged. -/
theorem chainCount_piMove_alphaA {P : Pent M.graph h} (hd : DoublyLocked P c j) :
    chainCount M.graph h (piMove P c) (c (P.x j)) (c (P.x (j + 3))) =
      chainCount M.graph h c (c (P.x j)) (c (P.x (j + 3))) := by
  rw [piMove_of_dl hd]
  exact chainCount_swap_same _ _ _

/-- `π` leaves the number of `{μ, B}`-chains unchanged. -/
theorem chainCount_piMove_muB {P : Pent M.graph h} (hd : DoublyLocked P c j) :
    chainCount M.graph h (piMove P c) (c (P.x (j + 1))) (c (P.x (j + 4))) =
      chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 4))) := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hd.1
  rw [piMove_of_dl hd]
  exact chainCount_swap_other _ _ _ h1 h13 h4 (Ne.symm h34)

/-- `N(π c) − N(c)` only involves the four pairs other than `{α, A}` and `{μ, B}`
(computed in `c`'s colour names, which `π` permutes on its own frame). -/
theorem nChains_piMove_sub {P : Pent M.graph h} (hd : DoublyLocked P c j) :
    (nChains M.graph h (piMove P c) : ℤ) - nChains M.graph h c =
      ((chainCount M.graph h (piMove P c) (c (P.x j)) (c (P.x (j + 1))) : ℤ) +
        chainCount M.graph h (piMove P c) (c (P.x (j + 3))) (c (P.x (j + 4))) +
        chainCount M.graph h (piMove P c) (c (P.x j)) (c (P.x (j + 4))) +
        chainCount M.graph h (piMove P c) (c (P.x (j + 1))) (c (P.x (j + 3)))) -
      ((chainCount M.graph h c (c (P.x j)) (c (P.x (j + 1))) : ℤ) +
        chainCount M.graph h c (c (P.x (j + 3))) (c (P.x (j + 4))) +
        chainCount M.graph h c (c (P.x j)) (c (P.x (j + 4))) +
        chainCount M.graph h c (c (P.x (j + 1))) (c (P.x (j + 3)))) := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hd.1
  have eN : nChains M.graph h (piMove P c) =
      chainCount M.graph h (piMove P c) (c (P.x j)) (c (P.x (j + 1))) +
      chainCount M.graph h (piMove P c) (c (P.x (j + 3))) (c (P.x (j + 4))) +
      chainCount M.graph h (piMove P c) (c (P.x j)) (c (P.x (j + 3))) +
      chainCount M.graph h (piMove P c) (c (P.x (j + 1))) (c (P.x (j + 4))) +
      chainCount M.graph h (piMove P c) (c (P.x j)) (c (P.x (j + 4))) +
      chainCount M.graph h (piMove P c) (c (P.x (j + 1))) (c (P.x (j + 3))) :=
    sum_pairs_roles _ (fun p q => chainCount_comm p q) (Ne.symm h1) (Ne.symm h3)
      (Ne.symm h4) h13 h14 h34
  rw [eN, nChains_roles P hd.1, chainCount_piMove_alphaA hd, chainCount_piMove_muB hd]
  push_cast
  ring

variable (M) in
/-- **Theorem 6 (chain-parity law)**, as a statement: for every proper doubly locked state
`c`, `N(π c) − N(c)` is odd iff `π c` is doubly locked. Proved by hand in
`TrackI/RigidIsolation.md` (reviewed); **not** proved here. -/
def ChainParityLaw (P : Pent M.graph h) : Prop :=
  ∀ c : Fin n → Fin 4, ProperOff M.graph h c → DLState P c →
    (Odd (nChains M.graph h (piMove P c) + nChains M.graph h c) ↔ DLState P (piMove P c))

/-- **Rigid isolation from Theorem 6.** If the chain-parity law holds at the hole, then the
`π`-image of a rigid state is not rigid (in any frame). -/
theorem rigid_isolation_of_law {P : Pent M.graph h} (hlaw : ChainParityLaw M P)
    (hc : ProperOff M.graph h c) (hR : RigidAt P c j) (j' : Fin 5) :
    ¬ RigidAt P (piMove P c) j' := by
  intro hR'
  have key := (hlaw c hc ⟨j, hR.1⟩).2 ⟨j', hR'.1⟩
  rw [nChains_of_rigidAt hR, nChains_of_rigidAt hR'] at key
  exact absurd key (by decide)

/-- With Lemma 3, rigid isolation in the form "`N(c) = N(π c) = 8` never happens along a
doubly locked step". -/
theorem not_eight_eight_of_law (htri : M.Triangulated) {P : Pent M.graph h}
    (hlaw : ChainParityLaw M P) (hc : ProperOff M.graph h c) (hd : DoublyLocked P c j)
    {j' : Fin 5} (hd' : DoublyLocked P (piMove P c) j') :
    ¬ (nChains M.graph h c = 8 ∧ nChains M.graph h (piMove P c) = 8) := by
  rintro ⟨e, e'⟩
  exact rigid_isolation_of_law hlaw hc ((rigidAt_iff htri P hd).2 e) j'
    ((rigidAt_iff htri P hd').2 e')

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.chainCount_comm
#print axioms SimpleGraph.QuarterFloor.chainCount_swap_same
#print axioms SimpleGraph.QuarterFloor.chainCount_swap_other
#print axioms SimpleGraph.QuarterFloor.sum_pairs_roles
#print axioms SimpleGraph.QuarterFloor.nChains_roles
#print axioms SimpleGraph.QuarterFloor.eight_le_nChains
#print axioms SimpleGraph.QuarterFloor.rigidAt_iff
#print axioms SimpleGraph.QuarterFloor.chainCount_piMove_alphaA
#print axioms SimpleGraph.QuarterFloor.chainCount_piMove_muB
#print axioms SimpleGraph.QuarterFloor.nChains_piMove_sub
#print axioms SimpleGraph.QuarterFloor.rigid_isolation_of_law
#print axioms SimpleGraph.QuarterFloor.not_eight_eight_of_law
