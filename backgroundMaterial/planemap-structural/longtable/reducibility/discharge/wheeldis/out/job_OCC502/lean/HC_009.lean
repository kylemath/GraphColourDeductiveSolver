import Mathlib.Combinatorics.SimpleGraph.PlaneMap.OccToRing
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame
import DCheckR2D
import DCheckTEq
import DCheckMirror
import DCheckOccWalk

/-!
# Occurrence of nl0066_r10 (orientation -1) gives a ring reduction (generated)

`Occ T ring int` is the audit's rotation-based occurrence: ring with distinct darts, vertices may repeat (`ring k` is RSST ring
vertex `k+1`), injective interior, disjoint, every interior vertex has the free-completion degree,
and the rotation of `T` at every interior vertex is the free-completion rotation, read
backwards. Ring chords are allowed.

`configOcc`: on a triangulation, deleting the interior gives a `ConfigOcc` and a strictly smaller
support. `colorable_of_occ`: a triangulation with an occurrence is four-colourable when every
spherical map of smaller support is.
-/

namespace SimpleGraph.SphericalMap.HC_009
open VacancySlide VacancyShortFill VacancyIcosahedral VacancyCliqueLift SimpleGraph.SphericalMap

variable {n : ℕ}


/-- Ring neighbours (ring positions) and interior neighbours of each interior vertex. -/
def ringList : Fin 7 → List ℕ := ![[4, 5, 6], [8, 9], [6, 7, 8], [9], [2, 3, 4], [0, 1, 9], [1, 2]]
def intList : Fin 7 → List (Fin 7) := ![[1, 2, 3, 4], [0, 2, 3], [0, 1], [0, 1, 4, 5, 6], [0, 3, 6], [3, 6], [3, 4, 5]]
def ringAdj : Fin 7 → ℕ → Bool := fun a t => decide (t ∈ ringList a)
def intAdj : Fin 7 → Fin 7 → Bool := fun a b => decide (b ∈ intList a)

/-- Ring position `t` to ring vertex. -/
def ρOf (ring : Fin 10 → Fin n) : ℕ → Fin n := fun t => ring ⟨t % 10, by omega⟩

/-- The configuration occurs in `T` with ring `ring` and interior `int`. -/
structure Occ (T : SphericalMap n) (ring : Fin 10 → Fin n) (int : Fin 7 → Fin n) : Prop where
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![7, 5, 5, 6, 6, 5, 5] : Fin 7 → ℕ) a
  r0_0 : Nx T (int 0) (ring 5) (ring 4)
  r0_1 : Nx T (int 0) (ring 6) (ring 5)
  r0_2 : Nx T (int 0) (int 2) (ring 6)
  r0_3 : Nx T (int 0) (int 1) (int 2)
  r0_4 : Nx T (int 0) (int 3) (int 1)
  r0_5 : Nx T (int 0) (int 4) (int 3)
  r0_6 : Nx T (int 0) (ring 4) (int 4)
  r1_0 : Nx T (int 1) (ring 9) (ring 8)
  r1_1 : Nx T (int 1) (int 3) (ring 9)
  r1_2 : Nx T (int 1) (int 0) (int 3)
  r1_3 : Nx T (int 1) (int 2) (int 0)
  r1_4 : Nx T (int 1) (ring 8) (int 2)
  r2_0 : Nx T (int 2) (ring 7) (ring 6)
  r2_1 : Nx T (int 2) (ring 8) (ring 7)
  r2_2 : Nx T (int 2) (int 1) (ring 8)
  r2_3 : Nx T (int 2) (int 0) (int 1)
  r2_4 : Nx T (int 2) (ring 6) (int 0)
  r3_0 : Nx T (int 3) (int 5) (ring 9)
  r3_1 : Nx T (int 3) (int 6) (int 5)
  r3_2 : Nx T (int 3) (int 4) (int 6)
  r3_3 : Nx T (int 3) (int 0) (int 4)
  r3_4 : Nx T (int 3) (int 1) (int 0)
  r3_5 : Nx T (int 3) (ring 9) (int 1)
  r4_0 : Nx T (int 4) (ring 4) (ring 3)
  r4_1 : Nx T (int 4) (int 0) (ring 4)
  r4_2 : Nx T (int 4) (int 3) (int 0)
  r4_3 : Nx T (int 4) (int 6) (int 3)
  r4_4 : Nx T (int 4) (ring 2) (int 6)
  r4_5 : Nx T (int 4) (ring 3) (ring 2)
  r5_0 : Nx T (int 5) (ring 1) (ring 0)
  r5_1 : Nx T (int 5) (int 6) (ring 1)
  r5_2 : Nx T (int 5) (int 3) (int 6)
  r5_3 : Nx T (int 5) (ring 9) (int 3)
  r5_4 : Nx T (int 5) (ring 0) (ring 9)
  r6_0 : Nx T (int 6) (int 4) (ring 2)
  r6_1 : Nx T (int 6) (int 3) (int 4)
  r6_2 : Nx T (int 6) (int 5) (int 3)
  r6_3 : Nx T (int 6) (ring 1) (int 5)
  r6_4 : Nx T (int 6) (ring 2) (ring 1)

/-- The ring walk has distinct darts (derived; replaces `ring_inj`). -/
theorem ring_dinj_of {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : Occ T ring int) :
    ∀ s t, s < 10 → t < 10 → ρOf ring s = ρOf ring t → ρOf ring (s + 1) = ρOf ring (t + 1) → s = t := by
  have key : ∀ s t, s < t → t < 10 → ρOf ring s = ρOf ring t → ρOf ring (s + 1) = ρOf ring (t + 1) → False := by
    intro s t hst ht e0 e1
    have hs : s < 10 := by omega
    interval_cases s
    · interval_cases t
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (0 + 1)) (ρOf ring 0) (int 5) := (nx_tri htri h.r5_0).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        let X : ℕ → Fin n := fun j => ([(ring 0), (ring 9), (int 3), (int 6), (ring 1)] : List (Fin n)).getD j (ring 0)
        have hc : ∀ j, j + 1 < 5 → Nx T (int 5) (X j) (X (j + 1)) := by
          intro j hj; have hj' : j < 4 := by omega
          interval_cases j
          exacts [h.r5_4, h.r5_3, h.r5_2, h.r5_1]
        exact absurd (chain_inj (by simpa using h.deg 5) (nx_adj_left (hc 0 (by norm_num))) hc 0 1
          (by norm_num) (by norm_num) e0) (by norm_num)
    · interval_cases t
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (1 + 1)) (ρOf ring 1) (int 6) := (nx_tri htri h.r6_4).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        let X : ℕ → Fin n := fun j => ([(ring 3), (ring 2), (int 6), (int 3), (int 0), (ring 4)] : List (Fin n)).getD j (ring 0)
        have hc : ∀ j, j + 1 < 6 → Nx T (int 4) (X j) (X (j + 1)) := by
          intro j hj; have hj' : j < 5 := by omega
          interval_cases j
          exacts [h.r4_5, h.r4_4, h.r4_3, h.r4_2, h.r4_1]
        exact absurd (chain_inj (by simpa using h.deg 4) (nx_adj_left (hc 0 (by norm_num))) hc 1 0
          (by norm_num) (by norm_num) e0) (by norm_num)
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (2 + 1)) (ρOf ring 2) (int 4) := (nx_tri htri h.r4_5).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        have ft : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        have ft : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        have ft : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (3 + 1)) (ρOf ring 3) (int 4) := (nx_tri htri h.r4_0).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        have ft : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        let X : ℕ → Fin n := fun j => ([(ring 4), (int 4), (int 3), (int 1), (int 2), (ring 6), (ring 5)] : List (Fin n)).getD j (ring 0)
        have hc : ∀ j, j + 1 < 7 → Nx T (int 0) (X j) (X (j + 1)) := by
          intro j hj; have hj' : j < 6 := by omega
          interval_cases j
          exacts [h.r0_6, h.r0_5, h.r0_4, h.r0_3, h.r0_2, h.r0_1]
        exact absurd (chain_inj (by simpa using h.deg 0) (nx_adj_left (hc 0 (by norm_num))) hc 0 6
          (by norm_num) (by norm_num) e0) (by norm_num)
      · have fs : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        have ft : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (4 + 1)) (ρOf ring 4) (int 0) := (nx_tri htri h.r0_0).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        have ft : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (5 + 1)) (ρOf ring 5) (int 0) := (nx_tri htri h.r0_1).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        have ft : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        let X : ℕ → Fin n := fun j => ([(ring 6), (int 0), (int 1), (ring 8), (ring 7)] : List (Fin n)).getD j (ring 0)
        have hc : ∀ j, j + 1 < 5 → Nx T (int 2) (X j) (X (j + 1)) := by
          intro j hj; have hj' : j < 4 := by omega
          interval_cases j
          exacts [h.r2_4, h.r2_3, h.r2_2, h.r2_1]
        exact absurd (chain_inj (by simpa using h.deg 2) (nx_adj_left (hc 0 (by norm_num))) hc 0 4
          (by norm_num) (by norm_num) e0) (by norm_num)
      · have fs : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (6 + 1)) (ρOf ring 6) (int 2) := (nx_tri htri h.r2_0).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        have ft : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
      · have fs : Nx T (ρOf ring (7 + 1)) (ρOf ring 7) (int 2) := (nx_tri htri h.r2_1).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
      · have fs : Nx T (ρOf ring (8 + 1)) (ρOf ring 8) (int 1) := (nx_tri htri h.r1_0).2
        have ft : Nx T (ρOf ring (9 + 1)) (ρOf ring 9) (int 5) := (nx_tri htri h.r5_4).2
        rw [e1, e0] at fs
        have ea := h.int_inj (nx_func fs ft)
        exact absurd ea (by decide)
    · interval_cases t
  intro s t hs ht e0 e1
  rcases Nat.lt_trichotomy s t with h' | h' | h'
  · exact (key s t h' ht e0 e1).elim
  · exact h'
  · exact (key t s h' hs e0.symm e1.symm).elim

theorem configOcc {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 10 → Fin n}
    {int : Fin 7 → Fin n} (h : Occ T ring int) :
    ∃ G : SphericalMap n, ConfigOccW T G 10 7 (ρOf ring) int intAdj ringAdj ∧
      supportSize G < supportSize T := by
  classical
  obtain ⟨G, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph {x | ∀ a, x ≠ int a})
    (fun _ _ e => e.1)
  have hGadj : ∀ x y, G.Adj x y ↔ T.Adj x y ∧ (∀ a, x ≠ int a) ∧ (∀ a, y ≠ int a) := by
    intro x y; change G.graph.Adj x y ↔ _; rw [hN]; rfl
  have hstep : ∀ t, t < 10 → ∀ h1 h2, G.rotation.faceNext ⟨(ρOf ring t, ρOf ring (t + 1)), h1⟩ =
      ⟨(ρOf ring (t + 1), ρOf ring (t + 2)), h2⟩ := by
    intro t ht h1 h2
    rw [RotationSystem.face_next_apply]
    interval_cases t
    · -- ring position 0: fan at RSST 2: [1, 16, 17, 3]
      let X : ℕ → Fin n := fun j => ([(ring 0), (int 5), (int 6), (ring 2)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 1) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r5_0).2, (nx_tri htri h.r6_3).2, (nx_tri htri h.r6_4).1]
      have h0 : T.Adj (ring 1) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 0, ρOf ring 1), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 1), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 1), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 5 rfl
          · exact fun hh => hh.2.2 6 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 1), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 1), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 1), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 1: fan at RSST 3: [2, 17, 15, 4]
      let X : ℕ → Fin n := fun j => ([(ring 1), (int 6), (int 4), (ring 3)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 2) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r6_4).2, (nx_tri htri h.r6_0).1, (nx_tri htri h.r4_5).1]
      have h0 : T.Adj (ring 2) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 1, ρOf ring 2), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 2), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 2), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 6 rfl
          · exact fun hh => hh.2.2 4 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 2), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 2), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 2), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 2: fan at RSST 4: [3, 15, 5]
      let X : ℕ → Fin n := fun j => ([(ring 2), (int 4), (ring 4)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 3) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r4_5).2, (nx_tri htri h.r4_0).1]
      have h0 : T.Adj (ring 3) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 2, ρOf ring 3), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 3), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 3), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 4 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 3), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 3), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 3), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 3: fan at RSST 5: [4, 15, 11, 6]
      let X : ℕ → Fin n := fun j => ([(ring 3), (int 4), (int 0), (ring 5)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 4) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r4_0).2, (nx_tri htri h.r4_1).1, (nx_tri htri h.r0_0).1]
      have h0 : T.Adj (ring 4) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 3, ρOf ring 4), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 4), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 4), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 4 rfl
          · exact fun hh => hh.2.2 0 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 4), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 4), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 4), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 4: fan at RSST 6: [5, 11, 7]
      let X : ℕ → Fin n := fun j => ([(ring 4), (int 0), (ring 6)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 5) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r0_0).2, (nx_tri htri h.r0_1).1]
      have h0 : T.Adj (ring 5) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 4, ρOf ring 5), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 5), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 5), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 0 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 5), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 5), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 5), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 5: fan at RSST 7: [6, 11, 13, 8]
      let X : ℕ → Fin n := fun j => ([(ring 5), (int 0), (int 2), (ring 7)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 6) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r0_1).2, (nx_tri htri h.r2_4).2, (nx_tri htri h.r2_0).1]
      have h0 : T.Adj (ring 6) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 5, ρOf ring 6), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 6), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 6), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 0 rfl
          · exact fun hh => hh.2.2 2 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 6), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 6), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 6), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 6: fan at RSST 8: [7, 13, 9]
      let X : ℕ → Fin n := fun j => ([(ring 6), (int 2), (ring 8)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 7) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r2_0).2, (nx_tri htri h.r2_1).1]
      have h0 : T.Adj (ring 7) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 6, ρOf ring 7), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 7), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 7), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 2 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 7), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 7), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 7), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 7: fan at RSST 9: [8, 13, 12, 10]
      let X : ℕ → Fin n := fun j => ([(ring 7), (int 2), (int 1), (ring 9)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 8) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r2_1).2, (nx_tri htri h.r2_2).1, (nx_tri htri h.r1_0).1]
      have h0 : T.Adj (ring 8) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 7, ρOf ring 8), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 8), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 8), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 2 rfl
          · exact fun hh => hh.2.2 1 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 8), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 8), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 8), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 8: fan at RSST 10: [9, 12, 14, 16, 1]
      let X : ℕ → Fin n := fun j => ([(ring 8), (int 1), (int 3), (int 5), (ring 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 4 → Nx T (ring 9) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r1_0).2, (nx_tri htri h.r3_5).2, (nx_tri htri h.r5_3).2, (nx_tri htri h.r5_4).1]
      have h0 : T.Adj (ring 9) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 8, ρOf ring 9), h1⟩)
      obtain ⟨hK, eK⟩ := ch 4 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 4) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 9), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 9), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 1 rfl
          · exact fun hh => hh.2.2 3 rfl
          · exact fun hh => hh.2.2 5 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[4] ⟨((ring 9), X 0), h0⟩).fst ((⇑T.rotation.next)^[4] ⟨((ring 9), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[4] ⟨((ring 9), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 9: fan at RSST 1: [10, 16, 2]
      let X : ℕ → Fin n := fun j => ([(ring 9), (int 5), (ring 1)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 0) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r5_4).2, (nx_tri htri h.r5_0).1]
      have h0 : T.Adj (ring 0) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 9, ρOf ring 10), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 0), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 0), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 5 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 0), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 0), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 0), X 0), h0⟩ = _
      rw [eK]; rfl
  have hadj : ∀ t, t < 10 → G.Adj (ρOf ring t) (ρOf ring (t + 1)) := by
    intro t ht
    interval_cases t
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r5_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r6_4).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r4_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r4_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r0_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r0_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r2_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r2_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r1_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r5_4).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
  have hper : ∀ t, ρOf ring (t + 10) = ρOf ring t := by
    intro t; unfold ρOf; congr 2; simp [Nat.add_mod_right]
  have hring : FaceWalk G 10 (ρOf ring) := FaceWalk.mk_lt (by norm_num) hper hadj hstep (ring_dinj_of htri h)
  have hnbr : ∀ a w, T.Adj (int a) w →
      (∃ b, w = int b ∧ intAdj a b = true) ∨ (∃ t, t < 10 ∧ w = ρOf ring t ∧ ringAdj a t = true) := by
    intro a w hw
    fin_cases a
    · let X : ℕ → Fin n := fun j => ([(ring 4), (int 4), (int 3), (int 1), (int 2), (ring 6), (ring 5)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 7 → Nx T (int 0) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 6 := by omega
        interval_cases j
        exacts [h.r0_6, h.r0_5, h.r0_4, h.r0_3, h.r0_2, h.r0_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 7) (by simpa using h.deg 0) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨4, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inr ⟨6, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨5, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 8), (int 2), (int 0), (int 3), (ring 9)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 1) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r1_4, h.r1_3, h.r1_2, h.r1_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 1) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨8, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inr ⟨9, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 6), (int 0), (int 1), (ring 8), (ring 7)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 2) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r2_4, h.r2_3, h.r2_2, h.r2_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 2) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨6, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inr ⟨8, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨7, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 9), (int 1), (int 0), (int 4), (int 6), (int 5)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 3) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r3_5, h.r3_4, h.r3_3, h.r3_2, h.r3_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 3) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨9, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨6, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 3), (ring 2), (int 6), (int 3), (int 0), (ring 4)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 4) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r4_5, h.r4_4, h.r4_3, h.r4_2, h.r4_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 4) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨3, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨2, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨6, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inr ⟨4, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 0), (ring 9), (int 3), (int 6), (ring 1)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 5) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r5_4, h.r5_3, h.r5_2, h.r5_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 5) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨0, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨9, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨6, rfl, by decide⟩
      · exact Or.inr ⟨1, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 2), (ring 1), (int 5), (int 3), (int 4)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 6) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r6_4, h.r6_3, h.r6_2, h.r6_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 6) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨2, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨1, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
  have hsupp : supportSize G < supportSize T := by
    apply Finset.card_lt_card
    refine ⟨fun w hw => ?_, fun hsub => ?_⟩
    · simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hw ⊢
      exact lt_of_lt_of_le hw (SimpleGraph.degree_le_of_le hle)
    · have hmem : int 0 ∈ Finset.univ.filter (fun x => 0 < T.graph.degree x) := by
        simp only [Finset.mem_filter, Finset.mem_univ, true_and]
        have := h.deg 0; simp at this; omega
      have := hsub hmem
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at this
      obtain ⟨u, hu⟩ := G.graph.degree_pos_iff_exists_adj _ |>.mp this
      exact ((hGadj _ _).1 hu).2.1 0 rfl
  exact ⟨G, ⟨hring, h.int_inj, fun t a => h.disj _ a, hGadj, hnbr, by norm_num⟩, hsupp⟩


/-- The key as a `DCheck18` configuration (the dfast/wheelcheck18 input line). -/
def cf : DCheck18.Conf where
  name := "nl0066_r10"
  r := 10
  m := 7
  ringAdj := #[#[4, 5, 6], #[8, 9], #[6, 7, 8], #[9], #[2, 3, 4], #[0, 1, 9], #[1, 2]]
  intAdj := #[#[1, 2, 3, 4], #[0, 2, 3], #[0, 1], #[0, 1, 4, 5, 6], #[0, 3, 6], #[3, 6], #[3, 4, 5]]

theorem intAdjOf_eq : intAdjOf (DCheck.Conf.of18 cf) = intAdj := by
  funext a b
  change Fin 7 at a b
  fin_cases a <;> fin_cases b <;> simp [intAdjOf, DCheck.Conf.of18, cf, intAdj, intList]

theorem ringAdjOf_eq : ringAdjOf (DCheck.Conf.of18 cf) = ringAdj := by
  funext a t
  change Fin 7 at a
  fin_cases a <;> simp [ringAdjOf, DCheck.Conf.of18, cf, ringAdj, ringList]

theorem cf_sym : ∀ a b, intAdjOf (DCheck.Conf.of18 cf) a b = true →
    intAdjOf (DCheck.Conf.of18 cf) b a = true := by
  rw [intAdjOf_eq]; unfold intAdj intList; decide

theorem cf_loop : ∀ a, intAdjOf (DCheck.Conf.of18 cf) a a = false := by
  rw [intAdjOf_eq]; unfold intAdj intList; decide

/-- **Per-key reduction**, given the checker's verdict `hD` (studio14c/14d, `wheelcheck18`). -/
theorem colorable_of_occ_dred (hD : DCheck18.dReducible cf = true) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin 10 → Fin n} {int : Fin 7 → Fin n} (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  exact ConfigOccW.colorable_of_dReducible18 (T := T) (G := G) cf hD (by decide) (by decide)
    cf_sym cf_loop O (c := cG) (fun x y e _ _ => cG.valid e)

/-- **Mirror image**, same `hD`: an occurrence of the mirrored configuration in `T` is an occurrence
of this one in `T.mirror` (same graph; `nx_mirror` reads every `Nx` fact backwards). -/
theorem colorable_of_mirror_occ_dred (hD : DCheck18.dReducible cf = true) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin 10 → Fin n} {int : Fin 7 → Fin n} (h : Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  colorable_of_occ_dred hD (T := T.mirror) (mirror_triangulated htri) h IH

end SimpleGraph.SphericalMap.HC_009

#print axioms SimpleGraph.SphericalMap.HC_009.colorable_of_occ_dred
#print axioms SimpleGraph.SphericalMap.HC_009.colorable_of_mirror_occ_dred
