import Mathlib.Combinatorics.SimpleGraph.PlaneMap.OccToRing
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame
import DCheckR2D
import DCheckTEq
import DCheckMirror

/-!
# Occurrence of k6:5:6|6:6:6|6:6:6|8:665:6|6:6:6 (orientation -1) gives a ring reduction (generated)

`Occ T ring int` is the audit's rotation-based occurrence: injective ring (`ring k` is RSST ring
vertex `k+1`), injective interior, disjoint, every interior vertex has the free-completion degree,
and the rotation of `T` at every interior vertex is the free-completion rotation, read
backwards. Ring chords are allowed.

`configOcc`: on a triangulation, deleting the interior gives a `ConfigOcc` and a strictly smaller
support. `colorable_of_occ`: a triangulation with an occurrence is four-colourable when every
spherical map of smaller support is.
-/

namespace SimpleGraph.SphericalMap.K21
open VacancySlide VacancyShortFill VacancyIcosahedral VacancyCliqueLift SimpleGraph.SphericalMap

variable {n : ℕ}


/-- Ring neighbours (ring positions) and interior neighbours of each interior vertex. -/
def ringList : Fin 18 → List ℕ := ![[], [], [], [], [], [], [16, 0], [0, 1], [1, 2, 3], [3, 4], [4, 5, 6], [6, 7], [7, 8, 9], [9, 10, 11], [11, 12], [12, 13], [13, 14, 15], [15, 16]]
def intList : Fin 18 → List (Fin 18) := ![[1, 2, 3, 4, 5], [0, 2, 5, 6, 7, 17], [0, 1, 3, 7, 8, 9], [0, 2, 4, 9, 10, 11], [0, 3, 5, 11, 12, 13, 14, 15], [0, 1, 4, 15, 16, 17], [1, 7, 17], [1, 2, 6, 8], [2, 7, 9], [2, 3, 8, 10], [3, 9, 11], [3, 4, 10, 12], [4, 11, 13], [4, 12, 14], [4, 13, 15], [4, 5, 14, 16], [5, 15, 17], [1, 5, 6, 16]]
def ringAdj : Fin 18 → ℕ → Bool := fun a t => decide (t ∈ ringList a)
def intAdj : Fin 18 → Fin 18 → Bool := fun a b => decide (b ∈ intList a)

/-- Ring position `t` to ring vertex. -/
def ρOf (ring : Fin 17 → Fin n) : ℕ → Fin n := fun t => ring ⟨t % 17, by omega⟩

/-- The configuration occurs in `T` with ring `ring` and interior `int`. -/
structure Occ (T : SphericalMap n) (ring : Fin 17 → Fin n) (int : Fin 18 → Fin n) : Prop where
  ring_inj : Function.Injective ring
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![5, 6, 6, 6, 8, 6, 5, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6] : Fin 18 → ℕ) a
  r0_0 : Nx T (int 0) (int 2) (int 1)
  r0_1 : Nx T (int 0) (int 3) (int 2)
  r0_2 : Nx T (int 0) (int 4) (int 3)
  r0_3 : Nx T (int 0) (int 5) (int 4)
  r0_4 : Nx T (int 0) (int 1) (int 5)
  r1_0 : Nx T (int 1) (int 17) (int 5)
  r1_1 : Nx T (int 1) (int 6) (int 17)
  r1_2 : Nx T (int 1) (int 7) (int 6)
  r1_3 : Nx T (int 1) (int 2) (int 7)
  r1_4 : Nx T (int 1) (int 0) (int 2)
  r1_5 : Nx T (int 1) (int 5) (int 0)
  r2_0 : Nx T (int 2) (int 1) (int 0)
  r2_1 : Nx T (int 2) (int 7) (int 1)
  r2_2 : Nx T (int 2) (int 8) (int 7)
  r2_3 : Nx T (int 2) (int 9) (int 8)
  r2_4 : Nx T (int 2) (int 3) (int 9)
  r2_5 : Nx T (int 2) (int 0) (int 3)
  r3_0 : Nx T (int 3) (int 2) (int 0)
  r3_1 : Nx T (int 3) (int 9) (int 2)
  r3_2 : Nx T (int 3) (int 10) (int 9)
  r3_3 : Nx T (int 3) (int 11) (int 10)
  r3_4 : Nx T (int 3) (int 4) (int 11)
  r3_5 : Nx T (int 3) (int 0) (int 4)
  r4_0 : Nx T (int 4) (int 3) (int 0)
  r4_1 : Nx T (int 4) (int 11) (int 3)
  r4_2 : Nx T (int 4) (int 12) (int 11)
  r4_3 : Nx T (int 4) (int 13) (int 12)
  r4_4 : Nx T (int 4) (int 14) (int 13)
  r4_5 : Nx T (int 4) (int 15) (int 14)
  r4_6 : Nx T (int 4) (int 5) (int 15)
  r4_7 : Nx T (int 4) (int 0) (int 5)
  r5_0 : Nx T (int 5) (int 15) (int 4)
  r5_1 : Nx T (int 5) (int 16) (int 15)
  r5_2 : Nx T (int 5) (int 17) (int 16)
  r5_3 : Nx T (int 5) (int 1) (int 17)
  r5_4 : Nx T (int 5) (int 0) (int 1)
  r5_5 : Nx T (int 5) (int 4) (int 0)
  r6_0 : Nx T (int 6) (int 7) (ring 0)
  r6_1 : Nx T (int 6) (int 1) (int 7)
  r6_2 : Nx T (int 6) (int 17) (int 1)
  r6_3 : Nx T (int 6) (ring 16) (int 17)
  r6_4 : Nx T (int 6) (ring 0) (ring 16)
  r7_0 : Nx T (int 7) (int 8) (ring 1)
  r7_1 : Nx T (int 7) (int 2) (int 8)
  r7_2 : Nx T (int 7) (int 1) (int 2)
  r7_3 : Nx T (int 7) (int 6) (int 1)
  r7_4 : Nx T (int 7) (ring 0) (int 6)
  r7_5 : Nx T (int 7) (ring 1) (ring 0)
  r8_0 : Nx T (int 8) (ring 3) (ring 2)
  r8_1 : Nx T (int 8) (int 9) (ring 3)
  r8_2 : Nx T (int 8) (int 2) (int 9)
  r8_3 : Nx T (int 8) (int 7) (int 2)
  r8_4 : Nx T (int 8) (ring 1) (int 7)
  r8_5 : Nx T (int 8) (ring 2) (ring 1)
  r9_0 : Nx T (int 9) (int 10) (ring 4)
  r9_1 : Nx T (int 9) (int 3) (int 10)
  r9_2 : Nx T (int 9) (int 2) (int 3)
  r9_3 : Nx T (int 9) (int 8) (int 2)
  r9_4 : Nx T (int 9) (ring 3) (int 8)
  r9_5 : Nx T (int 9) (ring 4) (ring 3)
  r10_0 : Nx T (int 10) (ring 6) (ring 5)
  r10_1 : Nx T (int 10) (int 11) (ring 6)
  r10_2 : Nx T (int 10) (int 3) (int 11)
  r10_3 : Nx T (int 10) (int 9) (int 3)
  r10_4 : Nx T (int 10) (ring 4) (int 9)
  r10_5 : Nx T (int 10) (ring 5) (ring 4)
  r11_0 : Nx T (int 11) (ring 7) (ring 6)
  r11_1 : Nx T (int 11) (int 12) (ring 7)
  r11_2 : Nx T (int 11) (int 4) (int 12)
  r11_3 : Nx T (int 11) (int 3) (int 4)
  r11_4 : Nx T (int 11) (int 10) (int 3)
  r11_5 : Nx T (int 11) (ring 6) (int 10)
  r12_0 : Nx T (int 12) (ring 8) (ring 7)
  r12_1 : Nx T (int 12) (ring 9) (ring 8)
  r12_2 : Nx T (int 12) (int 13) (ring 9)
  r12_3 : Nx T (int 12) (int 4) (int 13)
  r12_4 : Nx T (int 12) (int 11) (int 4)
  r12_5 : Nx T (int 12) (ring 7) (int 11)
  r13_0 : Nx T (int 13) (ring 10) (ring 9)
  r13_1 : Nx T (int 13) (ring 11) (ring 10)
  r13_2 : Nx T (int 13) (int 14) (ring 11)
  r13_3 : Nx T (int 13) (int 4) (int 14)
  r13_4 : Nx T (int 13) (int 12) (int 4)
  r13_5 : Nx T (int 13) (ring 9) (int 12)
  r14_0 : Nx T (int 14) (ring 12) (ring 11)
  r14_1 : Nx T (int 14) (int 15) (ring 12)
  r14_2 : Nx T (int 14) (int 4) (int 15)
  r14_3 : Nx T (int 14) (int 13) (int 4)
  r14_4 : Nx T (int 14) (ring 11) (int 13)
  r15_0 : Nx T (int 15) (int 16) (ring 13)
  r15_1 : Nx T (int 15) (int 5) (int 16)
  r15_2 : Nx T (int 15) (int 4) (int 5)
  r15_3 : Nx T (int 15) (int 14) (int 4)
  r15_4 : Nx T (int 15) (ring 12) (int 14)
  r15_5 : Nx T (int 15) (ring 13) (ring 12)
  r16_0 : Nx T (int 16) (ring 15) (ring 14)
  r16_1 : Nx T (int 16) (int 17) (ring 15)
  r16_2 : Nx T (int 16) (int 5) (int 17)
  r16_3 : Nx T (int 16) (int 15) (int 5)
  r16_4 : Nx T (int 16) (ring 13) (int 15)
  r16_5 : Nx T (int 16) (ring 14) (ring 13)
  r17_0 : Nx T (int 17) (ring 16) (ring 15)
  r17_1 : Nx T (int 17) (int 6) (ring 16)
  r17_2 : Nx T (int 17) (int 1) (int 6)
  r17_3 : Nx T (int 17) (int 5) (int 1)
  r17_4 : Nx T (int 17) (int 16) (int 5)
  r17_5 : Nx T (int 17) (ring 15) (int 16)

theorem configOcc {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 17 → Fin n}
    {int : Fin 18 → Fin n} (h : Occ T ring int) :
    ∃ G : SphericalMap n, ConfigOcc T G 17 18 (ρOf ring) int intAdj ringAdj ∧
      supportSize G < supportSize T := by
  classical
  obtain ⟨G, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph {x | ∀ a, x ≠ int a})
    (fun _ _ e => e.1)
  have hGadj : ∀ x y, G.Adj x y ↔ T.Adj x y ∧ (∀ a, x ≠ int a) ∧ (∀ a, y ≠ int a) := by
    intro x y; change G.graph.Adj x y ↔ _; rw [hN]; rfl
  have hstep : ∀ t, t < 17 → ∀ h1 h2, G.rotation.faceNext ⟨(ρOf ring t, ρOf ring (t + 1)), h1⟩ =
      ⟨(ρOf ring (t + 1), ρOf ring (t + 2)), h2⟩ := by
    intro t ht h1 h2
    rw [RotationSystem.face_next_apply]
    interval_cases t
    · -- ring position 0: fan at RSST 2: [1, 25, 26, 3]
      let X : ℕ → Fin n := fun j => ([(ring 0), (int 7), (int 8), (ring 2)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 1) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r7_5).2, (nx_tri htri h.r8_4).2, (nx_tri htri h.r8_5).1]
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
          · exact fun hh => hh.2.2 7 rfl
          · exact fun hh => hh.2.2 8 rfl
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
    · -- ring position 1: fan at RSST 3: [2, 26, 4]
      let X : ℕ → Fin n := fun j => ([(ring 1), (int 8), (ring 3)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 2) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r8_5).2, (nx_tri htri h.r8_0).1]
      have h0 : T.Adj (ring 2) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 1, ρOf ring 2), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 2), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 2), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 8 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 2), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 2), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 2), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 2: fan at RSST 4: [3, 26, 27, 5]
      let X : ℕ → Fin n := fun j => ([(ring 2), (int 8), (int 9), (ring 4)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 3) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r8_0).2, (nx_tri htri h.r9_4).2, (nx_tri htri h.r9_5).1]
      have h0 : T.Adj (ring 3) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 2, ρOf ring 3), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 3), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 3), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 8 rfl
          · exact fun hh => hh.2.2 9 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 3), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 3), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 3), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 3: fan at RSST 5: [4, 27, 28, 6]
      let X : ℕ → Fin n := fun j => ([(ring 3), (int 9), (int 10), (ring 5)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 4) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r9_5).2, (nx_tri htri h.r10_4).2, (nx_tri htri h.r10_5).1]
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
          · exact fun hh => hh.2.2 9 rfl
          · exact fun hh => hh.2.2 10 rfl
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
    · -- ring position 4: fan at RSST 6: [5, 28, 7]
      let X : ℕ → Fin n := fun j => ([(ring 4), (int 10), (ring 6)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 5) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r10_5).2, (nx_tri htri h.r10_0).1]
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
          · exact fun hh => hh.2.2 10 rfl
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
    · -- ring position 5: fan at RSST 7: [6, 28, 29, 8]
      let X : ℕ → Fin n := fun j => ([(ring 5), (int 10), (int 11), (ring 7)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 6) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r10_0).2, (nx_tri htri h.r11_5).2, (nx_tri htri h.r11_0).1]
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
          · exact fun hh => hh.2.2 10 rfl
          · exact fun hh => hh.2.2 11 rfl
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
    · -- ring position 6: fan at RSST 8: [7, 29, 30, 9]
      let X : ℕ → Fin n := fun j => ([(ring 6), (int 11), (int 12), (ring 8)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 7) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r11_0).2, (nx_tri htri h.r12_5).2, (nx_tri htri h.r12_0).1]
      have h0 : T.Adj (ring 7) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 6, ρOf ring 7), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 7), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 7), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 11 rfl
          · exact fun hh => hh.2.2 12 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 7), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 7), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 7), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 7: fan at RSST 9: [8, 30, 10]
      let X : ℕ → Fin n := fun j => ([(ring 7), (int 12), (ring 9)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 8) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r12_0).2, (nx_tri htri h.r12_1).1]
      have h0 : T.Adj (ring 8) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 7, ρOf ring 8), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 8), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 8), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 12 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 8), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 8), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 8), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 8: fan at RSST 10: [9, 30, 31, 11]
      let X : ℕ → Fin n := fun j => ([(ring 8), (int 12), (int 13), (ring 10)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 9) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r12_1).2, (nx_tri htri h.r13_5).2, (nx_tri htri h.r13_0).1]
      have h0 : T.Adj (ring 9) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 8, ρOf ring 9), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 9), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 9), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 12 rfl
          · exact fun hh => hh.2.2 13 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 9), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 9), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 9), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 9: fan at RSST 11: [10, 31, 12]
      let X : ℕ → Fin n := fun j => ([(ring 9), (int 13), (ring 11)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 10) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r13_0).2, (nx_tri htri h.r13_1).1]
      have h0 : T.Adj (ring 10) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 9, ρOf ring 10), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 10), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 10), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 13 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 10), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 10), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 10), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 10: fan at RSST 12: [11, 31, 32, 13]
      let X : ℕ → Fin n := fun j => ([(ring 10), (int 13), (int 14), (ring 12)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 11) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r13_1).2, (nx_tri htri h.r14_4).2, (nx_tri htri h.r14_0).1]
      have h0 : T.Adj (ring 11) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 10, ρOf ring 11), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 11), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 11), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 13 rfl
          · exact fun hh => hh.2.2 14 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 11), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 11), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 11), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 11: fan at RSST 13: [12, 32, 33, 14]
      let X : ℕ → Fin n := fun j => ([(ring 11), (int 14), (int 15), (ring 13)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 12) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r14_0).2, (nx_tri htri h.r15_4).2, (nx_tri htri h.r15_5).1]
      have h0 : T.Adj (ring 12) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 11, ρOf ring 12), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 12), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 12), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 14 rfl
          · exact fun hh => hh.2.2 15 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 12), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 12), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 12), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 12: fan at RSST 14: [13, 33, 34, 15]
      let X : ℕ → Fin n := fun j => ([(ring 12), (int 15), (int 16), (ring 14)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 13) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r15_5).2, (nx_tri htri h.r16_4).2, (nx_tri htri h.r16_5).1]
      have h0 : T.Adj (ring 13) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 12, ρOf ring 13), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 13), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 13), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 15 rfl
          · exact fun hh => hh.2.2 16 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 13), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 13), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 13), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 13: fan at RSST 15: [14, 34, 16]
      let X : ℕ → Fin n := fun j => ([(ring 13), (int 16), (ring 15)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 14) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r16_5).2, (nx_tri htri h.r16_0).1]
      have h0 : T.Adj (ring 14) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 13, ρOf ring 14), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 14), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 14), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 16 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 14), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 14), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 14), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 14: fan at RSST 16: [15, 34, 35, 17]
      let X : ℕ → Fin n := fun j => ([(ring 14), (int 16), (int 17), (ring 16)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 15) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r16_0).2, (nx_tri htri h.r17_5).2, (nx_tri htri h.r17_0).1]
      have h0 : T.Adj (ring 15) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 14, ρOf ring 15), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 15), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 15), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 16 rfl
          · exact fun hh => hh.2.2 17 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 15), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 15), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 15), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 15: fan at RSST 17: [16, 35, 24, 1]
      let X : ℕ → Fin n := fun j => ([(ring 15), (int 17), (int 6), (ring 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 16) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r17_0).2, (nx_tri htri h.r17_1).1, (nx_tri htri h.r6_4).1]
      have h0 : T.Adj (ring 16) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 15, ρOf ring 16), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 16), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 16), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 17 rfl
          · exact fun hh => hh.2.2 6 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 16), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 16), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 16), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 16: fan at RSST 1: [17, 24, 25, 2]
      let X : ℕ → Fin n := fun j => ([(ring 16), (int 6), (int 7), (ring 1)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 0) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r6_4).2, (nx_tri htri h.r7_4).2, (nx_tri htri h.r7_5).1]
      have h0 : T.Adj (ring 0) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 16, ρOf ring 17), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 0), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 0), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 6 rfl
          · exact fun hh => hh.2.2 7 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 0), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 0), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 0), X 0), h0⟩ = _
      rw [eK]; rfl
  have hadj : ∀ t, t < 17 → G.Adj (ρOf ring t) (ρOf ring (t + 1)) := by
    intro t ht
    interval_cases t
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r7_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r8_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r8_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r9_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r10_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r10_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r11_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r12_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r12_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r13_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r13_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r14_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r15_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r16_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r16_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r17_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r6_4).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
  have hinj : ∀ s t, s < 17 → t < 17 → ρOf ring s = ρOf ring t → s = t := by
    intro s t hs ht e
    have := h.ring_inj e
    simp only [Fin.mk.injEq] at this
    omega
  have hper : ∀ t, ρOf ring (t + 17) = ρOf ring t := by
    intro t; unfold ρOf; congr 2; simp [Nat.add_mod_right]
  have hring : RingFace G 17 (ρOf ring) := RingFace.mk_lt (by norm_num) hper hadj hstep hinj
  have hnbr : ∀ a w, T.Adj (int a) w →
      (∃ b, w = int b ∧ intAdj a b = true) ∨ (∃ t, t < 17 ∧ w = ρOf ring t ∧ ringAdj a t = true) := by
    intro a w hw
    fin_cases a
    · let X : ℕ → Fin n := fun j => ([(int 1), (int 5), (int 4), (int 3), (int 2)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 0) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r0_4, h.r0_3, h.r0_2, h.r0_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 0) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 5), (int 0), (int 2), (int 7), (int 6), (int 17)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 1) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r1_5, h.r1_4, h.r1_3, h.r1_2, h.r1_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 1) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨7, rfl, by decide⟩
      · exact Or.inl ⟨6, rfl, by decide⟩
      · exact Or.inl ⟨17, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 0), (int 3), (int 9), (int 8), (int 7), (int 1)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 2) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r2_5, h.r2_4, h.r2_3, h.r2_2, h.r2_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 2) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨9, rfl, by decide⟩
      · exact Or.inl ⟨8, rfl, by decide⟩
      · exact Or.inl ⟨7, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 0), (int 4), (int 11), (int 10), (int 9), (int 2)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 3) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r3_5, h.r3_4, h.r3_3, h.r3_2, h.r3_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 3) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨11, rfl, by decide⟩
      · exact Or.inl ⟨10, rfl, by decide⟩
      · exact Or.inl ⟨9, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 0), (int 5), (int 15), (int 14), (int 13), (int 12), (int 11), (int 3)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 8 → Nx T (int 4) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 7 := by omega
        interval_cases j
        exacts [h.r4_7, h.r4_6, h.r4_5, h.r4_4, h.r4_3, h.r4_2, h.r4_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 8) (by simpa using h.deg 4) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨15, rfl, by decide⟩
      · exact Or.inl ⟨14, rfl, by decide⟩
      · exact Or.inl ⟨13, rfl, by decide⟩
      · exact Or.inl ⟨12, rfl, by decide⟩
      · exact Or.inl ⟨11, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 4), (int 0), (int 1), (int 17), (int 16), (int 15)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 5) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r5_5, h.r5_4, h.r5_3, h.r5_2, h.r5_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 5) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨17, rfl, by decide⟩
      · exact Or.inl ⟨16, rfl, by decide⟩
      · exact Or.inl ⟨15, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 0), (ring 16), (int 17), (int 1), (int 7)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 6) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r6_4, h.r6_3, h.r6_2, h.r6_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 6) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨0, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨16, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨17, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨7, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 1), (ring 0), (int 6), (int 1), (int 2), (int 8)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 7) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r7_5, h.r7_4, h.r7_3, h.r7_2, h.r7_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 7) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨1, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨0, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨6, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨8, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 2), (ring 1), (int 7), (int 2), (int 9), (ring 3)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 8) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r8_5, h.r8_4, h.r8_3, h.r8_2, h.r8_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 8) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨2, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨1, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨7, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨9, rfl, by decide⟩
      · exact Or.inr ⟨3, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 4), (ring 3), (int 8), (int 2), (int 3), (int 10)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 9) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r9_5, h.r9_4, h.r9_3, h.r9_2, h.r9_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 9) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨4, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨3, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨8, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨10, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 5), (ring 4), (int 9), (int 3), (int 11), (ring 6)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 10) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r10_5, h.r10_4, h.r10_3, h.r10_2, h.r10_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 10) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨5, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨4, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨9, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨11, rfl, by decide⟩
      · exact Or.inr ⟨6, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 6), (int 10), (int 3), (int 4), (int 12), (ring 7)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 11) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r11_5, h.r11_4, h.r11_3, h.r11_2, h.r11_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 11) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨6, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨10, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨12, rfl, by decide⟩
      · exact Or.inr ⟨7, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 7), (int 11), (int 4), (int 13), (ring 9), (ring 8)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 12) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r12_5, h.r12_4, h.r12_3, h.r12_2, h.r12_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 12) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨7, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨11, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨13, rfl, by decide⟩
      · exact Or.inr ⟨9, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨8, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 9), (int 12), (int 4), (int 14), (ring 11), (ring 10)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 13) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r13_5, h.r13_4, h.r13_3, h.r13_2, h.r13_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 13) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨9, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨12, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨14, rfl, by decide⟩
      · exact Or.inr ⟨11, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨10, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 11), (int 13), (int 4), (int 15), (ring 12)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 14) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r14_4, h.r14_3, h.r14_2, h.r14_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 14) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨11, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨13, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨15, rfl, by decide⟩
      · exact Or.inr ⟨12, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 13), (ring 12), (int 14), (int 4), (int 5), (int 16)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 15) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r15_5, h.r15_4, h.r15_3, h.r15_2, h.r15_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 15) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨13, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨12, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨14, rfl, by decide⟩
      · exact Or.inl ⟨4, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨16, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 14), (ring 13), (int 15), (int 5), (int 17), (ring 15)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 16) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r16_5, h.r16_4, h.r16_3, h.r16_2, h.r16_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 16) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨14, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨13, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨15, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨17, rfl, by decide⟩
      · exact Or.inr ⟨15, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 15), (int 16), (int 5), (int 1), (int 6), (ring 16)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 17) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r17_5, h.r17_4, h.r17_3, h.r17_2, h.r17_1]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 17) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨15, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨16, rfl, by decide⟩
      · exact Or.inl ⟨5, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨6, rfl, by decide⟩
      · exact Or.inr ⟨16, by norm_num, rfl, by decide⟩
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
  name := "k6:5:6|6:6:6|6:6:6|8:665:6|6:6:6"
  r := 17
  m := 18
  ringAdj := #[#[], #[], #[], #[], #[], #[], #[16, 0], #[0, 1], #[1, 2, 3], #[3, 4], #[4, 5, 6], #[6, 7], #[7, 8, 9], #[9, 10, 11], #[11, 12], #[12, 13], #[13, 14, 15], #[15, 16]]
  intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 5, 6, 7, 17], #[0, 1, 3, 7, 8, 9], #[0, 2, 4, 9, 10, 11], #[0, 3, 5, 11, 12, 13, 14, 15], #[0, 1, 4, 15, 16, 17], #[1, 7, 17], #[1, 2, 6, 8], #[2, 7, 9], #[2, 3, 8, 10], #[3, 9, 11], #[3, 4, 10, 12], #[4, 11, 13], #[4, 12, 14], #[4, 13, 15], #[4, 5, 14, 16], #[5, 15, 17], #[1, 5, 6, 16]]

theorem intAdjOf_eq : intAdjOf (DCheck.Conf.of18 cf) = intAdj := by
  funext a b
  change Fin 18 at a b
  fin_cases a <;> fin_cases b <;> simp [intAdjOf, DCheck.Conf.of18, cf, intAdj, intList]

theorem ringAdjOf_eq : ringAdjOf (DCheck.Conf.of18 cf) = ringAdj := by
  funext a t
  change Fin 18 at a
  fin_cases a <;> simp [ringAdjOf, DCheck.Conf.of18, cf, ringAdj, ringList]

theorem cf_sym : ∀ a b, intAdjOf (DCheck.Conf.of18 cf) a b = true →
    intAdjOf (DCheck.Conf.of18 cf) b a = true := by
  rw [intAdjOf_eq]; unfold intAdj intList; decide

theorem cf_loop : ∀ a, intAdjOf (DCheck.Conf.of18 cf) a a = false := by
  rw [intAdjOf_eq]; unfold intAdj intList; decide

/-- **Per-key reduction**, given the checker's verdict `hD` (studio14c/14d, `wheelcheck18`). -/
theorem colorable_of_occ_dred (hD : DCheck18.dReducible cf = true) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin 17 → Fin n} {int : Fin 18 → Fin n} (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  exact ConfigOcc.colorable_of_dReducible18 (T := T) (G := G) cf hD (by decide) (by decide)
    cf_sym cf_loop O (c := cG) (fun x y e _ _ => cG.valid e)

/-- **Mirror image**, same `hD`: an occurrence of the mirrored configuration in `T` is an occurrence
of this one in `T.mirror` (same graph; `nx_mirror` reads every `Nx` fact backwards). -/
theorem colorable_of_mirror_occ_dred (hD : DCheck18.dReducible cf = true) {T : SphericalMap n}
    (htri : T.Triangulated) {ring : Fin 17 → Fin n} {int : Fin 18 → Fin n} (h : Occ T.mirror ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  colorable_of_occ_dred hD (T := T.mirror) (mirror_triangulated htri) h IH

end SimpleGraph.SphericalMap.K21

#print axioms SimpleGraph.SphericalMap.K21.colorable_of_occ_dred
#print axioms SimpleGraph.SphericalMap.K21.colorable_of_mirror_occ_dred
