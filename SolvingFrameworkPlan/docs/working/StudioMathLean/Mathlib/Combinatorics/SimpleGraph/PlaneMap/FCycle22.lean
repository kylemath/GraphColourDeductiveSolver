module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarSanity

/-!
# The order-22 F-cycle under the formal Kempe semantics

The F-cycle is studiointel's `fcycle/fcycle_order22.json` (branch `studio-intel`): graph
`tri22.txt` index 417, hole 15, link degrees (5,6,5,6,5). It has 20 states up to renaming. For
each state `sI_0`:
* `sI_proper`: it is proper off the hole;
* `sI_unfilled`: it is unfilled;
* `sI_fill`: `PureFill G 15 sI_0 ρ`, by an explicit path of whole-component swaps, where `ρ` is
  the file's radius.

For each **silent** distance-reducing first move (one whose component meets no link vertex),
`sI_mJ_silent` proves three things:
* the move is a formal `KempeStep`;
* every link colour is unchanged;
* the resulting state fills within `ρ − 1`.

An independent replay (`fcycle_check.py`) recomputes, for all 20 states, the radius and every
distance-reducing first move (pair, component size, link positions). It agrees with the file:
0 mismatches, and 8 states have silent moves. The lower bounds (no fill within `ρ − 1`) are
computed, not compiled.
-/

@[expose] public section
namespace SimpleGraph
open VacancySlide VacancyShortFill

namespace FCycle22

/-- studiointel F-cycle, order 22 (tri22.txt index 417), hole 15: neighbour lists of the 22-vertex triangulation. -/
def nbrs : Fin 22 → List (Fin 22) := ![[1, 2, 3, 4, 5], [0, 2, 5, 6, 7, 8, 9], [0, 1, 3, 6, 10, 11], [0, 2, 4, 10, 12, 13], [0, 3, 5, 12, 14], [0, 1, 4, 9, 14, 15], [1, 2, 7, 11, 19], [1, 6, 8, 17, 19], [1, 7, 9, 16, 17, 18], [1, 5, 8, 15, 16], [2, 3, 11, 13, 18, 20], [2, 6, 10, 19, 20], [3, 4, 13, 14, 21], [3, 10, 12, 18, 21], [4, 5, 12, 15, 21], [5, 9, 14, 16, 21], [8, 9, 15, 18, 21], [7, 8, 18, 19, 20], [8, 10, 13, 16, 17, 20, 21], [6, 7, 11, 17, 20], [10, 11, 17, 18, 19], [12, 13, 14, 15, 16, 18]]

def G : SimpleGraph (Fin 22) where
  Adj u v := v ∈ nbrs u
  symm := by refine ⟨?_⟩; intro u v h; exact (by decide : ∀ u v : Fin 22, v ∈ nbrs u → u ∈ nbrs v) u v h
  loopless := by refine ⟨?_⟩; intro v h; exact (by decide : ∀ v : Fin 22, v ∉ nbrs v) v h

instance : DecidableRel G.Adj := fun u v => inferInstanceAs (Decidable (v ∈ nbrs u))

/-! ### State 0 (radius 3) -/

def s0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 2, 1, 2, 3, 0, 0, 3, 1, 0, 2, 3, 1]
def s0_1 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 1, 3, 2, 1, 2, 0, 2, 3, 0, 0, 3, 1, 0, 2, 3, 1]
def s0_2 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 1, 3, 2, 1, 1, 0, 2, 3, 0, 0, 3, 1, 0, 2, 3, 1]
def s0_3 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 2, 3, 1, 3, 2, 1, 1, 0, 3, 2, 0, 0, 3, 1, 0, 2, 3, 1]
theorem s0_step1 : KempeStep G 15 s0_0 s0_1 :=
  ⟨0, 1, ↑({0, 1, 3, 6, 9, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 1, 7, 8, 1, 10, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 1, 0, 1, 0, 0, 2, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s0_step2 : KempeStep G 15 s0_1 s0_2 :=
  ⟨1, 2, ↑({10} : Finset (Fin 22)), by decide,
    whole_of_cert 10 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s0_step3 : KempeStep G 15 s0_2 s0_3 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s0_fill : PureFill G 15 s0_0 3 :=
  ⟨3, le_rfl, s0_3, (.cons s0_step1 (.cons s0_step2 (.cons s0_step3 (.nil s0_3)))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s0_3 v ≠ 2) v hv⟩⟩

theorem s0_proper : ProperOff G 15 s0_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s0_0 u ≠ s0_0 v) u v e hu hv

theorem s0_unfilled : ¬ Target G 15 s0_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s0_0 v = x) x
  exact hx hv e

/-! ### State 1 (radius 2) -/

def s1_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 2, 1, 2, 3, 1, 0, 3, 0, 1, 2, 3, 0]
def s1_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 1, 2, 3, 1, 0, 3, 0, 1, 2, 3, 0]
def s1_2 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 1, 3, 2, 1, 0, 3, 0, 1, 2, 3, 0]
theorem s1_step1 : KempeStep G 15 s1_0 s1_1 :=
  ⟨0, 2, ↑({10} : Finset (Fin 22)), by decide,
    whole_of_cert 10 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s1_step2 : KempeStep G 15 s1_1 s1_2 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s1_fill : PureFill G 15 s1_0 2 :=
  ⟨2, le_rfl, s1_2, (.cons s1_step1 (.cons s1_step2 (.nil s1_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s1_2 v ≠ 2) v hv⟩⟩

theorem s1_proper : ProperOff G 15 s1_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s1_0 u ≠ s1_0 v) u v e hu hv

theorem s1_unfilled : ¬ Target G 15 s1_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s1_0 v = x) x
  exact hx hv e

def s1_m0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 1, 2, 3, 1, 0, 3, 0, 1, 2, 3, 0]
def s1_m0_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 1, 3, 2, 1, 0, 3, 0, 1, 2, 3, 0]
theorem s1_m0_step1 : KempeStep G 15 s1_m0_0 s1_m0_1 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s1_m0_fill : PureFill G 15 s1_m0_0 1 :=
  ⟨1, le_rfl, s1_m0_1, (.cons s1_m0_step1 (.nil s1_m0_1)),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s1_m0_1 v ≠ 2) v hv⟩⟩

theorem s1_m0_move : KempeStep G 15 s1_0 s1_m0_0 :=
  ⟨0, 2, ↑({10} : Finset (Fin 22)), by decide,
    whole_of_cert 10 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 1: pair (0, 2), component of size 1, no link vertex. -/
theorem s1_m0_silent : KempeStep G 15 s1_0 s1_m0_0 ∧ (∀ v, G.Adj 15 v → s1_m0_0 v = s1_0 v) ∧
    PureFill G 15 s1_m0_0 1 :=
  ⟨s1_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s1_m0_0 v = s1_0 v) v hv, s1_m0_fill⟩

def s1_m1_0 : Fin 22 → Fin 4 := ![3, 1, 0, 1, 0, 2, 3, 0, 2, 0, 2, 1, 2, 3, 1, 0, 3, 3, 1, 2, 0, 0]
def s1_m1_1 : Fin 22 → Fin 4 := ![1, 3, 0, 3, 0, 2, 1, 0, 2, 0, 2, 3, 2, 1, 1, 0, 1, 1, 3, 2, 0, 0]
theorem s1_m1_step1 : KempeStep G 15 s1_m1_0 s1_m1_1 :=
  ⟨1, 3, ↑({0, 1, 3, 6, 11, 13, 16, 17, 18} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 1, 7, 8, 9, 10, 6, 12, 3, 14, 15, 18, 18, 13, 19, 20, 21] ![0, 1, 0, 1, 0, 0, 2, 0, 0, 0, 0, 3, 0, 2, 0, 0, 4, 4, 3, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s1_m1_fill : PureFill G 15 s1_m1_0 1 :=
  ⟨1, le_rfl, s1_m1_1, (.cons s1_m1_step1 (.nil s1_m1_1)),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s1_m1_1 v ≠ 3) v hv⟩⟩

theorem s1_m1_move : KempeStep G 15 s1_0 s1_m1_0 :=
  ⟨0, 3, ↑({0, 2, 4, 6, 7, 17, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 7, 18, 19, 17, 21] ![0, 0, 1, 0, 1, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 1 of state 1: pair (0, 3), component of size 7, no link vertex. -/
theorem s1_m1_silent : KempeStep G 15 s1_0 s1_m1_0 ∧ (∀ v, G.Adj 15 v → s1_m1_0 v = s1_0 v) ∧
    PureFill G 15 s1_m1_0 1 :=
  ⟨s1_m1_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s1_m1_0 v = s1_0 v) v hv, s1_m1_fill⟩

/-! ### State 2 (radius 2) -/

def s2_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 1, 0, 3, 1, 0, 3, 0, 1, 2, 3, 2]
def s2_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 1, 2, 3, 1, 0, 3, 0, 1, 2, 3, 0]
def s2_2 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 1, 3, 2, 1, 0, 3, 0, 1, 2, 3, 0]
theorem s2_step1 : KempeStep G 15 s2_0 s2_1 :=
  ⟨0, 2, ↑({12, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 12 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 12] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s2_step2 : KempeStep G 15 s2_1 s2_2 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s2_fill : PureFill G 15 s2_0 2 :=
  ⟨2, le_rfl, s2_2, (.cons s2_step1 (.cons s2_step2 (.nil s2_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s2_2 v ≠ 2) v hv⟩⟩

theorem s2_proper : ProperOff G 15 s2_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s2_0 u ≠ s2_0 v) u v e hu hv

theorem s2_unfilled : ¬ Target G 15 s2_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s2_0 v = x) x
  exact hx hv e

def s2_m0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 0, 3, 2, 0, 0, 1, 0, 3, 1, 0, 3, 0, 1, 2, 3, 2]
def s2_m0_1 : Fin 22 → Fin 4 := ![1, 0, 3, 2, 3, 2, 1, 3, 2, 1, 1, 0, 0, 3, 1, 0, 3, 1, 0, 2, 3, 2]
theorem s2_m0_step1 : KempeStep G 15 s2_m0_0 s2_m0_1 :=
  ⟨0, 1, ↑({0, 1, 6, 9, 10, 11, 17, 18} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 3, 4, 5, 1, 7, 8, 1, 11, 6, 12, 13, 14, 15, 16, 18, 10, 19, 20, 21] ![0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 4, 3, 0, 0, 0, 0, 0, 6, 5, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s2_m0_fill : PureFill G 15 s2_m0_0 1 :=
  ⟨1, le_rfl, s2_m0_1, (.cons s2_m0_step1 (.nil s2_m0_1)),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s2_m0_1 v ≠ 0) v hv⟩⟩

theorem s2_m0_move : KempeStep G 15 s2_0 s2_m0_0 :=
  ⟨1, 2, ↑({3} : Finset (Fin 22)), by decide,
    whole_of_cert 3 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 2: pair (1, 2), component of size 1, no link vertex. -/
theorem s2_m0_silent : KempeStep G 15 s2_0 s2_m0_0 ∧ (∀ v, G.Adj 15 v → s2_m0_0 v = s2_0 v) ∧
    PureFill G 15 s2_m0_0 1 :=
  ⟨s2_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s2_m0_0 v = s2_0 v) v hv, s2_m0_fill⟩

/-! ### State 3 (radius 2) -/

def s3_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 2, 0, 3, 1, 0, 3, 0, 1, 1, 3, 2]
def s3_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 2, 2, 3, 1, 0, 3, 0, 1, 1, 3, 0]
def s3_2 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 2, 3, 2, 1, 0, 3, 0, 1, 1, 3, 0]
theorem s3_step1 : KempeStep G 15 s3_0 s3_1 :=
  ⟨0, 2, ↑({12, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 12 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 12] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s3_step2 : KempeStep G 15 s3_1 s3_2 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s3_fill : PureFill G 15 s3_0 2 :=
  ⟨2, le_rfl, s3_2, (.cons s3_step1 (.cons s3_step2 (.nil s3_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s3_2 v ≠ 2) v hv⟩⟩

theorem s3_proper : ProperOff G 15 s3_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s3_0 u ≠ s3_0 v) u v e hu hv

theorem s3_unfilled : ¬ Target G 15 s3_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s3_0 v = x) x
  exact hx hv e

def s3_m0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 0, 3, 2, 0, 0, 2, 0, 3, 1, 0, 3, 0, 1, 1, 3, 2]
def s3_m0_1 : Fin 22 → Fin 4 := ![1, 0, 3, 2, 3, 2, 1, 3, 2, 1, 1, 2, 0, 3, 1, 0, 3, 1, 0, 0, 3, 2]
theorem s3_m0_step1 : KempeStep G 15 s3_m0_0 s3_m0_1 :=
  ⟨0, 1, ↑({0, 1, 6, 9, 10, 17, 18, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 3, 4, 5, 1, 7, 8, 1, 18, 11, 12, 13, 14, 15, 16, 19, 17, 6, 20, 21] ![0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 6, 0, 0, 0, 0, 0, 0, 4, 5, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s3_m0_fill : PureFill G 15 s3_m0_0 1 :=
  ⟨1, le_rfl, s3_m0_1, (.cons s3_m0_step1 (.nil s3_m0_1)),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s3_m0_1 v ≠ 0) v hv⟩⟩

theorem s3_m0_move : KempeStep G 15 s3_0 s3_m0_0 :=
  ⟨1, 2, ↑({3} : Finset (Fin 22)), by decide,
    whole_of_cert 3 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 3: pair (1, 2), component of size 1, no link vertex. -/
theorem s3_m0_silent : KempeStep G 15 s3_0 s3_m0_0 ∧ (∀ v, G.Adj 15 v → s3_m0_0 v = s3_0 v) ∧
    PureFill G 15 s3_m0_0 1 :=
  ⟨s3_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s3_m0_0 v = s3_0 v) v hv, s3_m0_fill⟩

/-! ### State 4 (radius 3) -/

def s4_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 2, 3, 2, 0, 2, 1, 2, 3, 0, 0, 3, 1, 0, 0, 3, 1]
def s4_1 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 2, 3, 2, 1, 2, 1, 2, 3, 0, 0, 3, 1, 0, 0, 3, 1]
def s4_2 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 1, 3, 2, 1, 1, 2, 2, 3, 0, 0, 3, 1, 0, 0, 3, 1]
def s4_3 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 2, 3, 1, 3, 2, 1, 1, 2, 3, 2, 0, 0, 3, 1, 0, 0, 3, 1]
theorem s4_step1 : KempeStep G 15 s4_0 s4_1 :=
  ⟨0, 1, ↑({0, 1, 3, 9} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 7, 8, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s4_step2 : KempeStep G 15 s4_1 s4_2 :=
  ⟨1, 2, ↑({6, 10, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s4_step3 : KempeStep G 15 s4_2 s4_3 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s4_fill : PureFill G 15 s4_0 3 :=
  ⟨3, le_rfl, s4_3, (.cons s4_step1 (.cons s4_step2 (.cons s4_step3 (.nil s4_3)))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s4_3 v ≠ 2) v hv⟩⟩

theorem s4_proper : ProperOff G 15 s4_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s4_0 u ≠ s4_0 v) u v e hu hv

theorem s4_unfilled : ¬ Target G 15 s4_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s4_0 v = x) x
  exact hx hv e

/-! ### State 5 (radius 2) -/

def s5_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 2, 3, 2, 0, 2, 0, 2, 3, 1, 0, 3, 0, 1, 1, 3, 0]
def s5_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 2, 2, 3, 1, 0, 3, 0, 1, 1, 3, 0]
def s5_2 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 2, 3, 2, 1, 0, 3, 0, 1, 1, 3, 0]
theorem s5_step1 : KempeStep G 15 s5_0 s5_1 :=
  ⟨0, 2, ↑({6, 10, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s5_step2 : KempeStep G 15 s5_1 s5_2 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s5_fill : PureFill G 15 s5_0 2 :=
  ⟨2, le_rfl, s5_2, (.cons s5_step1 (.cons s5_step2 (.nil s5_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s5_2 v ≠ 2) v hv⟩⟩

theorem s5_proper : ProperOff G 15 s5_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s5_0 u ≠ s5_0 v) u v e hu hv

theorem s5_unfilled : ¬ Target G 15 s5_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s5_0 v = x) x
  exact hx hv e

def s5_m0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 0, 2, 2, 3, 1, 0, 3, 0, 1, 1, 3, 0]
def s5_m0_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 2, 3, 0, 3, 2, 0, 0, 2, 3, 2, 1, 0, 3, 0, 1, 1, 3, 0]
theorem s5_m0_step1 : KempeStep G 15 s5_m0_0 s5_m0_1 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s5_m0_fill : PureFill G 15 s5_m0_0 1 :=
  ⟨1, le_rfl, s5_m0_1, (.cons s5_m0_step1 (.nil s5_m0_1)),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s5_m0_1 v ≠ 2) v hv⟩⟩

theorem s5_m0_move : KempeStep G 15 s5_0 s5_m0_0 :=
  ⟨0, 2, ↑({6, 10, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 5: pair (0, 2), component of size 3, no link vertex. -/
theorem s5_m0_silent : KempeStep G 15 s5_0 s5_m0_0 ∧ (∀ v, G.Adj 15 v → s5_m0_0 v = s5_0 v) ∧
    PureFill G 15 s5_m0_0 1 :=
  ⟨s5_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s5_m0_0 v = s5_0 v) v hv, s5_m0_fill⟩

def s5_m1_0 : Fin 22 → Fin 4 := ![3, 1, 0, 1, 0, 2, 2, 0, 2, 0, 2, 3, 2, 3, 1, 0, 3, 3, 1, 1, 0, 0]
def s5_m1_1 : Fin 22 → Fin 4 := ![1, 3, 0, 3, 0, 2, 2, 0, 2, 0, 2, 1, 2, 1, 1, 0, 1, 1, 3, 3, 0, 0]
theorem s5_m1_step1 : KempeStep G 15 s5_m1_0 s5_m1_1 :=
  ⟨1, 3, ↑({0, 1, 3, 11, 13, 16, 17, 18, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 7, 8, 9, 10, 19, 12, 3, 14, 15, 18, 18, 13, 17, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 6, 0, 2, 0, 0, 4, 4, 3, 5, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s5_m1_fill : PureFill G 15 s5_m1_0 1 :=
  ⟨1, le_rfl, s5_m1_1, (.cons s5_m1_step1 (.nil s5_m1_1)),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s5_m1_1 v ≠ 3) v hv⟩⟩

theorem s5_m1_move : KempeStep G 15 s5_0 s5_m1_0 :=
  ⟨0, 3, ↑({0, 2, 4, 7, 11, 17, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 17, 8, 9, 10, 2, 12, 13, 14, 15, 16, 20, 18, 19, 11, 21] ![0, 0, 1, 0, 1, 0, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 4, 0, 0, 3, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 1 of state 5: pair (0, 3), component of size 7, no link vertex. -/
theorem s5_m1_silent : KempeStep G 15 s5_0 s5_m1_0 ∧ (∀ v, G.Adj 15 v → s5_m1_0 v = s5_0 v) ∧
    PureFill G 15 s5_m1_0 1 :=
  ⟨s5_m1_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s5_m1_0 v = s5_0 v) v hv, s5_m1_fill⟩

/-! ### State 6 (radius 4) -/

def s6_0 : Fin 22 → Fin 4 := ![3, 1, 0, 1, 0, 2, 2, 3, 2, 0, 2, 1, 2, 3, 3, 0, 3, 1, 0, 0, 3, 1]
def s6_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 2, 3, 2, 0, 2, 1, 2, 3, 0, 0, 3, 1, 0, 0, 3, 1]
def s6_2 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 2, 3, 2, 1, 2, 1, 2, 3, 0, 0, 3, 1, 0, 0, 3, 1]
def s6_3 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 1, 3, 2, 1, 1, 2, 2, 3, 0, 0, 3, 1, 0, 0, 3, 1]
def s6_4 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 2, 3, 1, 3, 2, 1, 1, 2, 3, 2, 0, 0, 3, 1, 0, 0, 3, 1]
theorem s6_step1 : KempeStep G 15 s6_0 s6_1 :=
  ⟨0, 3, ↑({0, 2, 4, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s6_step2 : KempeStep G 15 s6_1 s6_2 :=
  ⟨0, 1, ↑({0, 1, 3, 9} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 7, 8, 1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s6_step3 : KempeStep G 15 s6_2 s6_3 :=
  ⟨1, 2, ↑({6, 10, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s6_step4 : KempeStep G 15 s6_3 s6_4 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s6_fill : PureFill G 15 s6_0 4 :=
  ⟨4, le_rfl, s6_4, (.cons s6_step1 (.cons s6_step2 (.cons s6_step3 (.cons s6_step4 (.nil s6_4))))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s6_4 v ≠ 2) v hv⟩⟩

theorem s6_proper : ProperOff G 15 s6_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s6_0 u ≠ s6_0 v) u v e hu hv

theorem s6_unfilled : ¬ Target G 15 s6_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s6_0 v = x) x
  exact hx hv e

/-! ### State 7 (radius 4) -/

def s7_0 : Fin 22 → Fin 4 := ![3, 1, 0, 1, 0, 2, 3, 0, 2, 0, 2, 1, 2, 3, 3, 0, 3, 1, 0, 2, 3, 1]
def s7_1 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 3, 2, 0, 2, 1, 2, 3, 0, 0, 3, 1, 0, 2, 3, 1]
def s7_2 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 1, 3, 2, 1, 2, 0, 2, 3, 0, 0, 3, 1, 0, 2, 3, 1]
def s7_3 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 1, 3, 2, 1, 1, 0, 2, 3, 0, 0, 3, 1, 0, 2, 3, 1]
def s7_4 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 2, 3, 1, 3, 2, 1, 1, 0, 3, 2, 0, 0, 3, 1, 0, 2, 3, 1]
theorem s7_step1 : KempeStep G 15 s7_0 s7_1 :=
  ⟨0, 3, ↑({0, 2, 4, 6, 7, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 2, 6, 8, 9, 10, 11, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 1, 0, 1, 0, 2, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s7_step2 : KempeStep G 15 s7_1 s7_2 :=
  ⟨0, 1, ↑({0, 1, 3, 6, 9, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 1, 7, 8, 1, 10, 6, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 1, 0, 1, 0, 0, 2, 0, 0, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s7_step3 : KempeStep G 15 s7_2 s7_3 :=
  ⟨1, 2, ↑({10} : Finset (Fin 22)), by decide,
    whole_of_cert 10 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s7_step4 : KempeStep G 15 s7_3 s7_4 :=
  ⟨2, 3, ↑({4, 5, 12, 13} : Finset (Fin 22)), by decide,
    whole_of_cert 4 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 4, 6, 7, 8, 9, 10, 11, 4, 12, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s7_fill : PureFill G 15 s7_0 4 :=
  ⟨4, le_rfl, s7_4, (.cons s7_step1 (.cons s7_step2 (.cons s7_step3 (.cons s7_step4 (.nil s7_4))))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s7_4 v ≠ 2) v hv⟩⟩

theorem s7_proper : ProperOff G 15 s7_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s7_0 u ≠ s7_0 v) u v e hu hv

theorem s7_unfilled : ¬ Target G 15 s7_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s7_0 v = x) x
  exact hx hv e

/-! ### State 8 (radius 4) -/

def s8_0 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 0, 2, 3, 0, 1, 2, 1, 0, 0, 0, 1, 0, 2, 1, 3, 3]
def s8_1 : Fin 22 → Fin 4 := ![1, 0, 3, 2, 3, 2, 1, 2, 3, 1, 1, 2, 1, 0, 0, 0, 0, 1, 2, 0, 3, 3]
def s8_2 : Fin 22 → Fin 4 := ![1, 2, 3, 2, 3, 0, 1, 0, 3, 1, 1, 0, 1, 0, 2, 0, 0, 1, 2, 2, 3, 3]
def s8_3 : Fin 22 → Fin 4 := ![0, 2, 3, 2, 3, 1, 1, 0, 3, 0, 1, 0, 1, 0, 2, 0, 1, 1, 2, 2, 3, 3]
def s8_4 : Fin 22 → Fin 4 := ![2, 0, 3, 0, 3, 1, 1, 2, 3, 2, 1, 2, 1, 2, 2, 0, 1, 1, 0, 0, 3, 3]
theorem s8_step1 : KempeStep G 15 s8_0 s8_1 :=
  ⟨0, 1, ↑({0, 1, 6, 9, 16, 17, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 3, 4, 5, 1, 7, 8, 1, 10, 11, 12, 13, 14, 15, 9, 19, 18, 6, 20, 21] ![0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 4, 0, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s8_step2 : KempeStep G 15 s8_1 s8_2 :=
  ⟨0, 2, ↑({1, 5, 7, 11, 14, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 6, 1, 8, 9, 10, 19, 12, 13, 5, 15, 16, 17, 18, 7, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s8_step3 : KempeStep G 15 s8_2 s8_3 :=
  ⟨0, 1, ↑({0, 5, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 6, 7, 8, 5, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s8_step4 : KempeStep G 15 s8_3 s8_4 :=
  ⟨0, 2, ↑({0, 1, 3, 7, 9, 11, 13, 18, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 19, 12, 3, 14, 15, 16, 17, 13, 7, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 3, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s8_fill : PureFill G 15 s8_0 4 :=
  ⟨4, le_rfl, s8_4, (.cons s8_step1 (.cons s8_step2 (.cons s8_step3 (.cons s8_step4 (.nil s8_4))))),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s8_4 v ≠ 0) v hv⟩⟩

theorem s8_proper : ProperOff G 15 s8_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s8_0 u ≠ s8_0 v) u v e hu hv

theorem s8_unfilled : ¬ Target G 15 s8_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s8_0 v = x) x
  exact hx hv e

/-! ### State 9 (radius 4) -/

def s9_0 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 0, 2, 3, 0, 1, 2, 1, 0, 0, 0, 1, 1, 2, 3, 0, 3]
def s9_1 : Fin 22 → Fin 4 := ![1, 0, 3, 2, 3, 2, 1, 2, 3, 1, 1, 2, 1, 0, 0, 0, 0, 1, 2, 3, 0, 3]
def s9_2 : Fin 22 → Fin 4 := ![1, 2, 3, 2, 3, 0, 1, 0, 3, 1, 1, 2, 1, 0, 2, 0, 0, 1, 2, 3, 0, 3]
def s9_3 : Fin 22 → Fin 4 := ![0, 2, 3, 2, 3, 1, 1, 0, 3, 0, 1, 2, 1, 0, 2, 0, 1, 1, 2, 3, 0, 3]
def s9_4 : Fin 22 → Fin 4 := ![2, 0, 3, 0, 3, 1, 1, 2, 3, 2, 1, 0, 1, 2, 2, 0, 1, 1, 0, 3, 2, 3]
theorem s9_step1 : KempeStep G 15 s9_0 s9_1 :=
  ⟨0, 1, ↑({0, 1, 6, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 3, 4, 5, 1, 7, 8, 1, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s9_step2 : KempeStep G 15 s9_1 s9_2 :=
  ⟨0, 2, ↑({1, 5, 7, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 6, 1, 8, 9, 10, 11, 12, 13, 5, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s9_step3 : KempeStep G 15 s9_2 s9_3 :=
  ⟨0, 1, ↑({0, 5, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 6, 7, 8, 5, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s9_step4 : KempeStep G 15 s9_3 s9_4 :=
  ⟨0, 2, ↑({0, 1, 3, 7, 9, 11, 13, 18, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 20, 12, 3, 14, 15, 16, 17, 13, 19, 18, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 5, 0, 2, 0, 0, 0, 0, 3, 0, 4, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s9_fill : PureFill G 15 s9_0 4 :=
  ⟨4, le_rfl, s9_4, (.cons s9_step1 (.cons s9_step2 (.cons s9_step3 (.cons s9_step4 (.nil s9_4))))),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s9_4 v ≠ 0) v hv⟩⟩

theorem s9_proper : ProperOff G 15 s9_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s9_0 u ≠ s9_0 v) u v e hu hv

theorem s9_unfilled : ¬ Target G 15 s9_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s9_0 v = x) x
  exact hx hv e

/-! ### State 10 (radius 3) -/

def s10_0 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 0, 2, 3, 0, 0, 2, 0, 1, 1, 0, 1, 0, 2, 1, 3, 3]
def s10_1 : Fin 22 → Fin 4 := ![0, 2, 3, 2, 3, 1, 0, 1, 3, 0, 0, 1, 0, 1, 2, 0, 1, 0, 2, 2, 3, 3]
def s10_2 : Fin 22 → Fin 4 := ![1, 2, 3, 2, 3, 0, 0, 1, 3, 1, 0, 1, 0, 1, 2, 0, 0, 0, 2, 2, 3, 3]
def s10_3 : Fin 22 → Fin 4 := ![2, 1, 3, 1, 3, 0, 0, 2, 3, 2, 0, 2, 0, 2, 2, 0, 0, 0, 1, 1, 3, 3]
theorem s10_step1 : KempeStep G 15 s10_0 s10_1 :=
  ⟨1, 2, ↑({1, 5, 7, 11, 14, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 6, 1, 8, 9, 10, 19, 12, 13, 5, 15, 16, 17, 18, 7, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s10_step2 : KempeStep G 15 s10_1 s10_2 :=
  ⟨0, 1, ↑({0, 5, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 6, 7, 8, 5, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s10_step3 : KempeStep G 15 s10_2 s10_3 :=
  ⟨1, 2, ↑({0, 1, 3, 7, 9, 11, 13, 18, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 19, 12, 3, 14, 15, 16, 17, 13, 7, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 3, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s10_fill : PureFill G 15 s10_0 3 :=
  ⟨3, le_rfl, s10_3, (.cons s10_step1 (.cons s10_step2 (.cons s10_step3 (.nil s10_3)))),
    ⟨1, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s10_3 v ≠ 1) v hv⟩⟩

theorem s10_proper : ProperOff G 15 s10_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s10_0 u ≠ s10_0 v) u v e hu hv

theorem s10_unfilled : ¬ Target G 15 s10_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s10_0 v = x) x
  exact hx hv e

/-! ### State 11 (radius 3) -/

def s11_0 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 0, 2, 3, 0, 0, 2, 0, 1, 1, 0, 1, 0, 2, 3, 1, 3]
def s11_1 : Fin 22 → Fin 4 := ![0, 2, 3, 2, 3, 1, 0, 1, 3, 0, 0, 2, 0, 1, 2, 0, 1, 0, 2, 3, 1, 3]
def s11_2 : Fin 22 → Fin 4 := ![1, 2, 3, 2, 3, 0, 0, 1, 3, 1, 0, 2, 0, 1, 2, 0, 0, 0, 2, 3, 1, 3]
def s11_3 : Fin 22 → Fin 4 := ![2, 1, 3, 1, 3, 0, 0, 2, 3, 2, 0, 1, 0, 2, 2, 0, 0, 0, 1, 3, 2, 3]
theorem s11_step1 : KempeStep G 15 s11_0 s11_1 :=
  ⟨1, 2, ↑({1, 5, 7, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 6, 1, 8, 9, 10, 11, 12, 13, 5, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s11_step2 : KempeStep G 15 s11_1 s11_2 :=
  ⟨0, 1, ↑({0, 5, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 6, 7, 8, 5, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s11_step3 : KempeStep G 15 s11_2 s11_3 :=
  ⟨1, 2, ↑({0, 1, 3, 7, 9, 11, 13, 18, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 20, 12, 3, 14, 15, 16, 17, 13, 19, 18, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 5, 0, 2, 0, 0, 0, 0, 3, 0, 4, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s11_fill : PureFill G 15 s11_0 3 :=
  ⟨3, le_rfl, s11_3, (.cons s11_step1 (.cons s11_step2 (.cons s11_step3 (.nil s11_3)))),
    ⟨1, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s11_3 v ≠ 1) v hv⟩⟩

theorem s11_proper : ProperOff G 15 s11_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s11_0 u ≠ s11_0 v) u v e hu hv

theorem s11_unfilled : ¬ Target G 15 s11_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s11_0 v = x) x
  exact hx hv e

/-! ### State 12 (radius 2) -/

def s12_0 : Fin 22 → Fin 4 := ![3, 1, 0, 2, 0, 2, 3, 0, 3, 0, 1, 2, 1, 3, 3, 0, 1, 2, 0, 1, 3, 2]
def s12_1 : Fin 22 → Fin 4 := ![2, 1, 0, 3, 0, 3, 3, 0, 3, 0, 1, 2, 1, 2, 2, 0, 1, 2, 0, 1, 3, 3]
def s12_2 : Fin 22 → Fin 4 := ![0, 1, 2, 3, 2, 3, 3, 0, 3, 0, 1, 0, 1, 2, 0, 0, 1, 2, 0, 1, 3, 3]
theorem s12_step1 : KempeStep G 15 s12_0 s12_1 :=
  ⟨2, 3, ↑({0, 3, 5, 13, 14, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 0, 4, 0, 6, 7, 8, 9, 10, 11, 12, 3, 5, 15, 16, 17, 18, 19, 20, 13] ![0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s12_step2 : KempeStep G 15 s12_1 s12_2 :=
  ⟨0, 2, ↑({0, 2, 4, 11, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 7, 8, 9, 10, 2, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s12_fill : PureFill G 15 s12_0 2 :=
  ⟨2, le_rfl, s12_2, (.cons s12_step1 (.cons s12_step2 (.nil s12_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s12_2 v ≠ 2) v hv⟩⟩

theorem s12_proper : ProperOff G 15 s12_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s12_0 u ≠ s12_0 v) u v e hu hv

theorem s12_unfilled : ¬ Target G 15 s12_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s12_0 v = x) x
  exact hx hv e

def s12_m0_0 : Fin 22 → Fin 4 := ![3, 1, 0, 2, 0, 2, 2, 0, 2, 0, 1, 3, 1, 3, 3, 0, 1, 3, 0, 1, 2, 2]
def s12_m0_1 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 2, 0, 2, 0, 1, 0, 1, 3, 0, 0, 1, 3, 0, 1, 2, 2]
theorem s12_m0_step1 : KempeStep G 15 s12_m0_0 s12_m0_1 :=
  ⟨0, 3, ↑({0, 2, 4, 11, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 7, 8, 9, 10, 2, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s12_m0_fill : PureFill G 15 s12_m0_0 1 :=
  ⟨1, le_rfl, s12_m0_1, (.cons s12_m0_step1 (.nil s12_m0_1)),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s12_m0_1 v ≠ 3) v hv⟩⟩

theorem s12_m0_move : KempeStep G 15 s12_0 s12_m0_0 :=
  ⟨2, 3, ↑({6, 8, 11, 17, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 17, 9, 10, 6, 12, 13, 14, 15, 16, 20, 18, 19, 11, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 0, 0, 0, 0, 3, 0, 0, 2, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 12: pair (2, 3), component of size 5, no link vertex. -/
theorem s12_m0_silent : KempeStep G 15 s12_0 s12_m0_0 ∧ (∀ v, G.Adj 15 v → s12_m0_0 v = s12_0 v) ∧
    PureFill G 15 s12_m0_0 1 :=
  ⟨s12_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s12_m0_0 v = s12_0 v) v hv, s12_m0_fill⟩

/-! ### State 13 (radius 3) -/

def s13_0 : Fin 22 → Fin 4 := ![3, 1, 0, 2, 0, 2, 3, 2, 3, 0, 1, 2, 1, 3, 3, 0, 1, 0, 2, 1, 3, 0]
def s13_1 : Fin 22 → Fin 4 := ![3, 1, 2, 0, 2, 0, 3, 2, 3, 2, 1, 0, 1, 3, 3, 0, 1, 0, 2, 1, 3, 0]
def s13_2 : Fin 22 → Fin 4 := ![0, 1, 2, 3, 2, 3, 3, 2, 3, 2, 1, 0, 1, 0, 0, 0, 1, 0, 2, 1, 3, 3]
def s13_3 : Fin 22 → Fin 4 := ![0, 1, 2, 3, 2, 3, 3, 2, 3, 2, 0, 1, 0, 1, 1, 0, 1, 1, 2, 0, 3, 3]
theorem s13_step1 : KempeStep G 15 s13_0 s13_1 :=
  ⟨0, 2, ↑({2, 3, 4, 5, 9, 11} : Finset (Fin 22)), by decide,
    whole_of_cert 2 _ (by decide) (by decide) (by decide) ![0, 1, 2, 2, 3, 4, 6, 7, 8, 5, 10, 2, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 1, 2, 3, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s13_step2 : KempeStep G 15 s13_1 s13_2 :=
  ⟨0, 3, ↑({0, 3, 5, 13, 14, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 0, 4, 0, 6, 7, 8, 9, 10, 11, 12, 3, 5, 15, 16, 17, 18, 19, 20, 13] ![0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s13_step3 : KempeStep G 15 s13_2 s13_3 :=
  ⟨0, 1, ↑({10, 11, 12, 13, 14, 17, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 10 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 13, 10, 12, 15, 16, 19, 18, 11, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 3, 0, 0, 3, 0, 2, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s13_fill : PureFill G 15 s13_0 3 :=
  ⟨3, le_rfl, s13_3, (.cons s13_step1 (.cons s13_step2 (.cons s13_step3 (.nil s13_3)))),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s13_3 v ≠ 0) v hv⟩⟩

theorem s13_proper : ProperOff G 15 s13_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s13_0 u ≠ s13_0 v) u v e hu hv

theorem s13_unfilled : ¬ Target G 15 s13_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s13_0 v = x) x
  exact hx hv e

/-! ### State 14 (radius 2) -/

def s14_0 : Fin 22 → Fin 4 := ![3, 1, 0, 2, 0, 2, 3, 2, 3, 0, 1, 2, 1, 3, 3, 0, 1, 1, 0, 0, 3, 2]
def s14_1 : Fin 22 → Fin 4 := ![2, 1, 0, 3, 0, 3, 3, 2, 3, 0, 1, 2, 1, 2, 2, 0, 1, 1, 0, 0, 3, 3]
def s14_2 : Fin 22 → Fin 4 := ![0, 1, 2, 3, 2, 3, 3, 0, 3, 0, 1, 0, 1, 2, 0, 0, 1, 1, 0, 2, 3, 3]
theorem s14_step1 : KempeStep G 15 s14_0 s14_1 :=
  ⟨2, 3, ↑({0, 3, 5, 13, 14, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 0, 4, 0, 6, 7, 8, 9, 10, 11, 12, 3, 5, 15, 16, 17, 18, 19, 20, 13] ![0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s14_step2 : KempeStep G 15 s14_1 s14_2 :=
  ⟨0, 2, ↑({0, 2, 4, 7, 11, 14, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 19, 8, 9, 10, 2, 12, 13, 4, 15, 16, 17, 18, 11, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 4, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s14_fill : PureFill G 15 s14_0 2 :=
  ⟨2, le_rfl, s14_2, (.cons s14_step1 (.cons s14_step2 (.nil s14_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s14_2 v ≠ 2) v hv⟩⟩

theorem s14_proper : ProperOff G 15 s14_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s14_0 u ≠ s14_0 v) u v e hu hv

theorem s14_unfilled : ¬ Target G 15 s14_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s14_0 v = x) x
  exact hx hv e

def s14_m0_0 : Fin 22 → Fin 4 := ![3, 1, 0, 2, 0, 2, 2, 3, 2, 0, 1, 3, 1, 3, 3, 0, 1, 1, 0, 0, 2, 2]
def s14_m0_1 : Fin 22 → Fin 4 := ![0, 1, 3, 2, 3, 2, 2, 0, 2, 0, 1, 0, 1, 3, 0, 0, 1, 1, 0, 3, 2, 2]
theorem s14_m0_step1 : KempeStep G 15 s14_m0_0 s14_m0_1 :=
  ⟨0, 3, ↑({0, 2, 4, 7, 11, 14, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 19, 8, 9, 10, 2, 12, 13, 4, 15, 16, 17, 18, 11, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 4, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s14_m0_fill : PureFill G 15 s14_m0_0 1 :=
  ⟨1, le_rfl, s14_m0_1, (.cons s14_m0_step1 (.nil s14_m0_1)),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s14_m0_1 v ≠ 3) v hv⟩⟩

theorem s14_m0_move : KempeStep G 15 s14_0 s14_m0_0 :=
  ⟨2, 3, ↑({6, 7, 8, 11, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 6, 7, 9, 10, 6, 12, 13, 14, 15, 16, 17, 18, 19, 11, 21] ![0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 14: pair (2, 3), component of size 5, no link vertex. -/
theorem s14_m0_silent : KempeStep G 15 s14_0 s14_m0_0 ∧ (∀ v, G.Adj 15 v → s14_m0_0 v = s14_0 v) ∧
    PureFill G 15 s14_m0_0 1 :=
  ⟨s14_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s14_m0_0 v = s14_0 v) v hv, s14_m0_fill⟩

/-! ### State 15 (radius 3) -/

def s15_0 : Fin 22 → Fin 4 := ![3, 1, 0, 2, 0, 2, 3, 2, 3, 0, 1, 2, 1, 3, 3, 0, 1, 1, 2, 0, 3, 0]
def s15_1 : Fin 22 → Fin 4 := ![3, 1, 2, 0, 2, 0, 3, 0, 3, 2, 1, 0, 1, 3, 3, 0, 1, 1, 2, 2, 3, 0]
def s15_2 : Fin 22 → Fin 4 := ![0, 1, 2, 3, 2, 3, 3, 0, 3, 2, 1, 0, 1, 0, 0, 0, 1, 1, 2, 2, 3, 3]
def s15_3 : Fin 22 → Fin 4 := ![0, 1, 2, 3, 2, 3, 3, 0, 3, 2, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 3, 3]
theorem s15_step1 : KempeStep G 15 s15_0 s15_1 :=
  ⟨0, 2, ↑({2, 3, 4, 5, 7, 9, 11, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 2 _ (by decide) (by decide) (by decide) ![0, 1, 2, 2, 3, 4, 6, 19, 8, 5, 10, 2, 12, 13, 14, 15, 16, 17, 18, 11, 20, 21] ![0, 0, 0, 1, 2, 3, 0, 3, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s15_step2 : KempeStep G 15 s15_1 s15_2 :=
  ⟨0, 3, ↑({0, 3, 5, 13, 14, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 0, 4, 0, 6, 7, 8, 9, 10, 11, 12, 3, 5, 15, 16, 17, 18, 19, 20, 13] ![0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s15_step3 : KempeStep G 15 s15_2 s15_3 :=
  ⟨0, 1, ↑({10, 11, 12, 13, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 10 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 13, 10, 12, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 3, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s15_fill : PureFill G 15 s15_0 3 :=
  ⟨3, le_rfl, s15_3, (.cons s15_step1 (.cons s15_step2 (.cons s15_step3 (.nil s15_3)))),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s15_3 v ≠ 0) v hv⟩⟩

theorem s15_proper : ProperOff G 15 s15_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s15_0 u ≠ s15_0 v) u v e hu hv

theorem s15_unfilled : ¬ Target G 15 s15_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s15_0 v = x) x
  exact hx hv e

/-! ### State 16 (radius 2) -/

def s16_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 2, 3, 0, 0, 1, 0, 2, 1, 0, 2, 0, 1, 3, 2, 3]
def s16_1 : Fin 22 → Fin 4 := ![2, 1, 3, 1, 3, 0, 0, 2, 3, 2, 0, 1, 0, 2, 1, 0, 0, 0, 1, 3, 2, 3]
def s16_2 : Fin 22 → Fin 4 := ![1, 2, 3, 2, 3, 0, 0, 1, 3, 1, 0, 2, 0, 1, 1, 0, 0, 0, 2, 3, 1, 3]
theorem s16_step1 : KempeStep G 15 s16_0 s16_1 :=
  ⟨0, 2, ↑({0, 5, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 6, 7, 8, 5, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s16_step2 : KempeStep G 15 s16_1 s16_2 :=
  ⟨1, 2, ↑({0, 1, 3, 7, 9, 11, 13, 18, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 20, 12, 3, 14, 15, 16, 17, 13, 19, 18, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 5, 0, 2, 0, 0, 0, 0, 3, 0, 4, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s16_fill : PureFill G 15 s16_0 2 :=
  ⟨2, le_rfl, s16_2, (.cons s16_step1 (.cons s16_step2 (.nil s16_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s16_2 v ≠ 2) v hv⟩⟩

theorem s16_proper : ProperOff G 15 s16_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s16_0 u ≠ s16_0 v) u v e hu hv

theorem s16_unfilled : ¬ Target G 15 s16_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s16_0 v = x) x
  exact hx hv e

def s16_m0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 2, 0, 3, 0, 2, 1, 2, 0, 1, 0, 2, 2, 1, 3, 0, 3]
def s16_m0_1 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 2, 1, 3, 1, 2, 0, 2, 1, 1, 0, 2, 2, 0, 3, 1, 3]
theorem s16_m0_step1 : KempeStep G 15 s16_m0_0 s16_m0_1 :=
  ⟨0, 1, ↑({0, 1, 3, 7, 9, 11, 13, 18, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 20, 12, 3, 14, 15, 16, 17, 13, 19, 18, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 5, 0, 2, 0, 0, 0, 0, 3, 0, 4, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s16_m0_fill : PureFill G 15 s16_m0_0 1 :=
  ⟨1, le_rfl, s16_m0_1, (.cons s16_m0_step1 (.nil s16_m0_1)),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s16_m0_1 v ≠ 0) v hv⟩⟩

theorem s16_m0_move : KempeStep G 15 s16_0 s16_m0_0 :=
  ⟨0, 2, ↑({6, 7, 10, 12, 13, 17, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 6, 8, 9, 20, 11, 13, 10, 14, 15, 16, 7, 18, 19, 17, 21] ![0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 0, 6, 5, 0, 0, 0, 2, 0, 0, 3, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 16: pair (0, 2), component of size 7, no link vertex. -/
theorem s16_m0_silent : KempeStep G 15 s16_0 s16_m0_0 ∧ (∀ v, G.Adj 15 v → s16_m0_0 v = s16_0 v) ∧
    PureFill G 15 s16_m0_0 1 :=
  ⟨s16_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s16_m0_0 v = s16_0 v) v hv, s16_m0_fill⟩

def s16_m1_0 : Fin 22 → Fin 4 := ![0, 1, 2, 1, 3, 2, 0, 2, 3, 0, 0, 1, 0, 2, 1, 0, 2, 0, 1, 3, 2, 3]
def s16_m1_1 : Fin 22 → Fin 4 := ![3, 1, 2, 1, 0, 2, 0, 2, 3, 0, 0, 1, 3, 2, 1, 0, 2, 0, 1, 3, 2, 0]
theorem s16_m1_step1 : KempeStep G 15 s16_m1_0 s16_m1_1 :=
  ⟨0, 3, ↑({0, 4, 12, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 0, 5, 6, 7, 8, 9, 10, 11, 4, 13, 14, 15, 16, 17, 18, 19, 20, 12] ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s16_m1_fill : PureFill G 15 s16_m1_0 1 :=
  ⟨1, le_rfl, s16_m1_1, (.cons s16_m1_step1 (.nil s16_m1_1)),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s16_m1_1 v ≠ 3) v hv⟩⟩

theorem s16_m1_move : KempeStep G 15 s16_0 s16_m1_0 :=
  ⟨2, 3, ↑({2} : Finset (Fin 22)), by decide,
    whole_of_cert 2 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 1 of state 16: pair (2, 3), component of size 1, no link vertex. -/
theorem s16_m1_silent : KempeStep G 15 s16_0 s16_m1_0 ∧ (∀ v, G.Adj 15 v → s16_m1_0 v = s16_0 v) ∧
    PureFill G 15 s16_m1_0 1 :=
  ⟨s16_m1_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s16_m1_0 v = s16_0 v) v hv, s16_m1_fill⟩

/-! ### State 17 (radius 2) -/

def s17_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 0, 2, 3, 0, 0, 2, 0, 2, 1, 0, 2, 0, 1, 1, 3, 3]
def s17_1 : Fin 22 → Fin 4 := ![2, 1, 3, 1, 3, 0, 0, 2, 3, 2, 0, 2, 0, 2, 1, 0, 0, 0, 1, 1, 3, 3]
def s17_2 : Fin 22 → Fin 4 := ![1, 2, 3, 2, 3, 0, 0, 1, 3, 1, 0, 1, 0, 1, 1, 0, 0, 0, 2, 2, 3, 3]
theorem s17_step1 : KempeStep G 15 s17_0 s17_1 :=
  ⟨0, 2, ↑({0, 5, 9, 16} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 6, 7, 8, 5, 10, 11, 12, 13, 14, 15, 9, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s17_step2 : KempeStep G 15 s17_1 s17_2 :=
  ⟨1, 2, ↑({0, 1, 3, 7, 9, 11, 13, 18, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 19, 12, 3, 14, 15, 16, 17, 13, 7, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 3, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s17_fill : PureFill G 15 s17_0 2 :=
  ⟨2, le_rfl, s17_2, (.cons s17_step1 (.cons s17_step2 (.nil s17_2))),
    ⟨2, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s17_2 v ≠ 2) v hv⟩⟩

theorem s17_proper : ProperOff G 15 s17_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s17_0 u ≠ s17_0 v) u v e hu hv

theorem s17_unfilled : ¬ Target G 15 s17_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s17_0 v = x) x
  exact hx hv e

def s17_m0_0 : Fin 22 → Fin 4 := ![0, 1, 3, 1, 3, 2, 2, 0, 3, 0, 2, 0, 2, 0, 1, 0, 2, 2, 1, 1, 3, 3]
def s17_m0_1 : Fin 22 → Fin 4 := ![1, 0, 3, 0, 3, 2, 2, 1, 3, 1, 2, 1, 2, 1, 1, 0, 2, 2, 0, 0, 3, 3]
theorem s17_m0_step1 : KempeStep G 15 s17_m0_0 s17_m0_1 :=
  ⟨0, 1, ↑({0, 1, 3, 7, 9, 11, 13, 18, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 1, 8, 1, 10, 19, 12, 3, 14, 15, 16, 17, 13, 7, 20, 21] ![0, 1, 0, 1, 0, 0, 0, 2, 0, 2, 0, 4, 0, 2, 0, 0, 0, 0, 3, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s17_m0_fill : PureFill G 15 s17_m0_0 1 :=
  ⟨1, le_rfl, s17_m0_1, (.cons s17_m0_step1 (.nil s17_m0_1)),
    ⟨0, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s17_m0_1 v ≠ 0) v hv⟩⟩

theorem s17_m0_move : KempeStep G 15 s17_0 s17_m0_0 :=
  ⟨0, 2, ↑({6, 7, 10, 11, 12, 13, 17} : Finset (Fin 22)), by decide,
    whole_of_cert 6 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 6, 8, 9, 11, 6, 13, 10, 14, 15, 16, 7, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 1, 4, 3, 0, 0, 0, 2, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 0 of state 17: pair (0, 2), component of size 7, no link vertex. -/
theorem s17_m0_silent : KempeStep G 15 s17_0 s17_m0_0 ∧ (∀ v, G.Adj 15 v → s17_m0_0 v = s17_0 v) ∧
    PureFill G 15 s17_m0_0 1 :=
  ⟨s17_m0_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s17_m0_0 v = s17_0 v) v hv, s17_m0_fill⟩

def s17_m1_0 : Fin 22 → Fin 4 := ![0, 1, 2, 1, 3, 2, 0, 2, 3, 0, 0, 3, 0, 2, 1, 0, 2, 0, 1, 1, 2, 3]
def s17_m1_1 : Fin 22 → Fin 4 := ![3, 1, 2, 1, 0, 2, 0, 2, 3, 0, 0, 3, 3, 2, 1, 0, 2, 0, 1, 1, 2, 0]
theorem s17_m1_step1 : KempeStep G 15 s17_m1_0 s17_m1_1 :=
  ⟨0, 3, ↑({0, 4, 12, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 0, 5, 6, 7, 8, 9, 10, 11, 4, 13, 14, 15, 16, 17, 18, 19, 20, 12] ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s17_m1_fill : PureFill G 15 s17_m1_0 1 :=
  ⟨1, le_rfl, s17_m1_1, (.cons s17_m1_step1 (.nil s17_m1_1)),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s17_m1_1 v ≠ 3) v hv⟩⟩

theorem s17_m1_move : KempeStep G 15 s17_0 s17_m1_0 :=
  ⟨2, 3, ↑({2, 11, 20} : Finset (Fin 22)), by decide,
    whole_of_cert 2 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 12, 13, 14, 15, 16, 17, 18, 19, 11, 21] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

/-- Silent move 1 of state 17: pair (2, 3), component of size 3, no link vertex. -/
theorem s17_m1_silent : KempeStep G 15 s17_0 s17_m1_0 ∧ (∀ v, G.Adj 15 v → s17_m1_0 v = s17_0 v) ∧
    PureFill G 15 s17_m1_0 1 :=
  ⟨s17_m1_move, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s17_m1_0 v = s17_0 v) v hv, s17_m1_fill⟩

/-! ### State 18 (radius 3) -/

def s18_0 : Fin 22 → Fin 4 := ![3, 1, 0, 1, 0, 2, 3, 0, 3, 0, 2, 1, 2, 3, 3, 0, 2, 1, 0, 2, 3, 1]
def s18_1 : Fin 22 → Fin 4 := ![3, 2, 0, 1, 0, 1, 3, 0, 3, 0, 2, 1, 2, 3, 3, 0, 2, 1, 0, 2, 3, 1]
def s18_2 : Fin 22 → Fin 4 := ![1, 2, 0, 3, 0, 3, 3, 0, 3, 0, 2, 1, 2, 1, 1, 0, 2, 1, 0, 2, 3, 3]
def s18_3 : Fin 22 → Fin 4 := ![0, 2, 1, 3, 1, 3, 3, 0, 3, 0, 2, 0, 2, 1, 0, 0, 2, 1, 0, 2, 3, 3]
theorem s18_step1 : KempeStep G 15 s18_0 s18_1 :=
  ⟨1, 2, ↑({1, 5} : Finset (Fin 22)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s18_step2 : KempeStep G 15 s18_1 s18_2 :=
  ⟨1, 3, ↑({0, 3, 5, 13, 14, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 0, 4, 0, 6, 7, 8, 9, 10, 11, 12, 3, 5, 15, 16, 17, 18, 19, 20, 13] ![0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s18_step3 : KempeStep G 15 s18_2 s18_3 :=
  ⟨0, 1, ↑({0, 2, 4, 11, 14} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 7, 8, 9, 10, 2, 12, 13, 4, 15, 16, 17, 18, 19, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s18_fill : PureFill G 15 s18_0 3 :=
  ⟨3, le_rfl, s18_3, (.cons s18_step1 (.cons s18_step2 (.cons s18_step3 (.nil s18_3)))),
    ⟨1, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s18_3 v ≠ 1) v hv⟩⟩

theorem s18_proper : ProperOff G 15 s18_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s18_0 u ≠ s18_0 v) u v e hu hv

theorem s18_unfilled : ¬ Target G 15 s18_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s18_0 v = x) x
  exact hx hv e

/-! ### State 19 (radius 3) -/

def s19_0 : Fin 22 → Fin 4 := ![3, 1, 0, 1, 0, 2, 3, 2, 3, 0, 2, 1, 2, 3, 3, 0, 2, 1, 0, 0, 3, 1]
def s19_1 : Fin 22 → Fin 4 := ![3, 2, 0, 1, 0, 1, 3, 1, 3, 0, 2, 1, 2, 3, 3, 0, 2, 2, 0, 0, 3, 1]
def s19_2 : Fin 22 → Fin 4 := ![1, 2, 0, 3, 0, 3, 3, 1, 3, 0, 2, 1, 2, 1, 1, 0, 2, 2, 0, 0, 3, 3]
def s19_3 : Fin 22 → Fin 4 := ![0, 2, 1, 3, 1, 3, 3, 0, 3, 0, 2, 0, 2, 1, 0, 0, 2, 2, 0, 1, 3, 3]
theorem s19_step1 : KempeStep G 15 s19_0 s19_1 :=
  ⟨1, 2, ↑({1, 5, 7, 17} : Finset (Fin 22)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 6, 1, 8, 9, 10, 11, 12, 13, 14, 15, 16, 7, 18, 19, 20, 21] ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s19_step2 : KempeStep G 15 s19_1 s19_2 :=
  ⟨1, 3, ↑({0, 3, 5, 13, 14, 21} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 0, 4, 0, 6, 7, 8, 9, 10, 11, 12, 3, 5, 15, 16, 17, 18, 19, 20, 13] ![0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s19_step3 : KempeStep G 15 s19_2 s19_3 :=
  ⟨0, 1, ↑({0, 2, 4, 7, 11, 14, 19} : Finset (Fin 22)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 0, 3, 0, 5, 6, 19, 8, 9, 10, 2, 12, 13, 4, 15, 16, 17, 18, 11, 20, 21] ![0, 0, 1, 0, 1, 0, 0, 4, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem s19_fill : PureFill G 15 s19_0 3 :=
  ⟨3, le_rfl, s19_3, (.cons s19_step1 (.cons s19_step2 (.cons s19_step3 (.nil s19_3)))),
    ⟨1, fun v hv => (by decide : ∀ v : Fin 22, G.Adj 15 v → s19_3 v ≠ 1) v hv⟩⟩

theorem s19_proper : ProperOff G 15 s19_0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 22, G.Adj u v → u ≠ 15 → v ≠ 15 → s19_0 u ≠ s19_0 v) u v e hu hv

theorem s19_unfilled : ¬ Target G 15 s19_0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 15 v ∧ s19_0 v = x) x
  exact hx hv e

end FCycle22
end SimpleGraph
