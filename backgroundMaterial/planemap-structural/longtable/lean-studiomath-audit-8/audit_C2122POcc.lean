module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.C2122PCert
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.OccToRing
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame

/-!
# Occurrence of Conf2122 (orientation +1) gives a ring reduction (generated)

`Occ T ring int` is the audit's rotation-based occurrence: injective ring (`ring k` is RSST ring
vertex `k+1`), injective interior, disjoint, every interior vertex has the free-completion degree,
and the rotation of `T` at every interior vertex is the free-completion rotation, read
forwards. Ring chords are allowed.

`configOcc`: on a triangulation, deleting the interior gives a `ConfigOcc` and a strictly smaller
support. `colorable_of_occ`: a triangulation with an occurrence is four-colourable when every
spherical map of smaller support is.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap.C2122P
open VacancySlide VacancyShortFill VacancyIcosahedral VacancyCliqueLift SimpleGraph.SphericalMap

variable {n : ℕ}

/-- Ring position `t` to ring vertex. -/
def ρOf (ring : Fin 7 → Fin n) : ℕ → Fin n := fun t => ring ⟨(7 - t % 7) % 7, by omega⟩

/-- The configuration occurs in `T` with ring `ring` and interior `int`. -/
structure Occ (T : SphericalMap n) (ring : Fin 7 → Fin n) (int : Fin 4 → Fin n) : Prop where
  ring_inj : Function.Injective ring
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![6, 5, 5, 5] : Fin 4 → ℕ) a
  r0_0 : Nx T (int 0) (ring 1) (ring 2)
  r0_1 : Nx T (int 0) (ring 2) (int 1)
  r0_2 : Nx T (int 0) (int 1) (int 2)
  r0_3 : Nx T (int 0) (int 2) (int 3)
  r0_4 : Nx T (int 0) (int 3) (ring 0)
  r0_5 : Nx T (int 0) (ring 0) (ring 1)
  r1_0 : Nx T (int 1) (ring 2) (ring 3)
  r1_1 : Nx T (int 1) (ring 3) (ring 4)
  r1_2 : Nx T (int 1) (ring 4) (int 2)
  r1_3 : Nx T (int 1) (int 2) (int 0)
  r1_4 : Nx T (int 1) (int 0) (ring 2)
  r2_0 : Nx T (int 2) (int 1) (ring 4)
  r2_1 : Nx T (int 2) (ring 4) (ring 5)
  r2_2 : Nx T (int 2) (ring 5) (int 3)
  r2_3 : Nx T (int 2) (int 3) (int 0)
  r2_4 : Nx T (int 2) (int 0) (int 1)
  r3_0 : Nx T (int 3) (int 2) (ring 5)
  r3_1 : Nx T (int 3) (ring 5) (ring 6)
  r3_2 : Nx T (int 3) (ring 6) (ring 0)
  r3_3 : Nx T (int 3) (ring 0) (int 0)
  r3_4 : Nx T (int 3) (int 0) (int 2)

theorem configOcc {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 7 → Fin n}
    {int : Fin 4 → Fin n} (h : Occ T ring int) :
    ∃ G : SphericalMap n, ConfigOcc T G 7 4 (ρOf ring) int intAdj ringAdj ∧
      supportSize G < supportSize T := by
  classical
  obtain ⟨G, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph {x | ∀ a, x ≠ int a})
    (fun _ _ e => e.1)
  have hGadj : ∀ x y, G.Adj x y ↔ T.Adj x y ∧ (∀ a, x ≠ int a) ∧ (∀ a, y ≠ int a) := by
    intro x y; change G.graph.Adj x y ↔ _; rw [hN]; rfl
  have hstep : ∀ t, t < 7 → ∀ h1 h2, G.rotation.faceNext ⟨(ρOf ring t, ρOf ring (t + 1)), h1⟩ =
      ⟨(ρOf ring (t + 1), ρOf ring (t + 2)), h2⟩ := by
    intro t ht h1 h2
    rw [RotationSystem.face_next_apply]
    interval_cases t
    · -- ring position 0: fan at RSST 7: [1, 11, 6]
      let X : ℕ → Fin n := fun j => ([(ring 0), (int 3), (ring 5)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 6) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r3_2).2, (nx_tri htri h.r3_1).1]
      have h0 : T.Adj (ring 6) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 0, ρOf ring 1), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 6), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 6), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 3 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 6), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 6), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 6), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 1: fan at RSST 6: [7, 11, 10, 5]
      let X : ℕ → Fin n := fun j => ([(ring 6), (int 3), (int 2), (ring 4)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 5) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r3_1).2, (nx_tri htri h.r3_0).1, (nx_tri htri h.r2_1).1]
      have h0 : T.Adj (ring 5) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 1, ρOf ring 2), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 5), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 5), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 3 rfl
          · exact fun hh => hh.2.2 2 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[3] ⟨((ring 5), X 0), h0⟩).fst ((⇑T.rotation.next)^[3] ⟨((ring 5), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[3] ⟨((ring 5), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 2: fan at RSST 5: [6, 10, 9, 4]
      let X : ℕ → Fin n := fun j => ([(ring 5), (int 2), (int 1), (ring 3)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 4) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r2_1).2, (nx_tri htri h.r2_0).1, (nx_tri htri h.r1_1).1]
      have h0 : T.Adj (ring 4) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 2, ρOf ring 3), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 4), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 4), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 2 rfl
          · exact fun hh => hh.2.2 1 rfl
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
    · -- ring position 3: fan at RSST 4: [5, 9, 3]
      let X : ℕ → Fin n := fun j => ([(ring 4), (int 1), (ring 2)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 3) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r1_1).2, (nx_tri htri h.r1_0).1]
      have h0 : T.Adj (ring 3) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 3, ρOf ring 4), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 3), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 3), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 1 rfl
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
    · -- ring position 4: fan at RSST 3: [4, 9, 8, 2]
      let X : ℕ → Fin n := fun j => ([(ring 3), (int 1), (int 0), (ring 1)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 2) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r1_0).2, (nx_tri htri h.r1_4).1, (nx_tri htri h.r0_0).1]
      have h0 : T.Adj (ring 2) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 4, ρOf ring 5), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 2), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 2), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 1 rfl
          · exact fun hh => hh.2.2 0 rfl
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
    · -- ring position 5: fan at RSST 2: [3, 8, 1]
      let X : ℕ → Fin n := fun j => ([(ring 2), (int 0), (ring 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 2 → Nx T (ring 1) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r0_0).2, (nx_tri htri h.r0_5).1]
      have h0 : T.Adj (ring 1) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 5, ρOf ring 6), h1⟩)
      obtain ⟨hK, eK⟩ := ch 2 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 2) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 1), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 1), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 0 rfl
        )
        (by
          change (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[2] ⟨((ring 1), X 0), h0⟩).fst ((⇑T.rotation.next)^[2] ⟨((ring 1), X 0), h0⟩).snd
          rw [eK]
          exact ⟨hK, fun a => h.disj _ a, fun a => h.disj _ a⟩)
      apply liftDart_injective hle
      rw [e]
      change (⇑T.rotation.next)^[2] ⟨((ring 1), X 0), h0⟩ = _
      rw [eK]; rfl
    · -- ring position 6: fan at RSST 1: [2, 8, 11, 7]
      let X : ℕ → Fin n := fun j => ([(ring 1), (int 0), (int 3), (ring 6)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j < 3 → Nx T (ring 0) (X j) (X (j + 1)) := by
        intro j hj; interval_cases j
        exacts [(nx_tri htri h.r0_5).2, (nx_tri htri h.r3_3).2, (nx_tri htri h.r3_2).1]
      have h0 : T.Adj (ring 0) (X 0) := nx_adj_left (hc 0 (by norm_num))
      have ch := iterate_chain h0 hc
      have r0 := spec (Dart.symm ⟨(ρOf ring 6, ρOf ring 7), h1⟩)
      obtain ⟨hK, eK⟩ := ch 3 le_rfl
      have e := runTo_eq r0 (hN.le (G.rotation.next _).adj) (k := 3) (by norm_num)
        (fun j hj1 hj2 => by
          obtain ⟨_, ej⟩ := ch j (by omega)
          change ¬ (sideGraph T.graph {x | ∀ a, x ≠ int a}).Adj
            ((⇑T.rotation.next)^[j] ⟨((ring 0), X 0), h0⟩).fst ((⇑T.rotation.next)^[j] ⟨((ring 0), X 0), h0⟩).snd
          rw [ej]
          interval_cases j
          · exact fun hh => hh.2.2 0 rfl
          · exact fun hh => hh.2.2 3 rfl
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
  have hadj : ∀ t, t < 7 → G.Adj (ρOf ring t) (ρOf ring (t + 1)) := by
    intro t ht
    interval_cases t
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r3_2).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r3_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r2_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r1_1).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r1_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r0_0).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
    · exact (hGadj _ _).2 ⟨(nx_adj_left (nx_tri htri h.r0_5).2).symm, fun a => h.disj _ a, fun a => h.disj _ a⟩
  have hinj : ∀ s t, s < 7 → t < 7 → ρOf ring s = ρOf ring t → s = t := by
    intro s t hs ht e
    have := h.ring_inj e
    simp only [Fin.mk.injEq] at this
    omega
  have hper : ∀ t, ρOf ring (t + 7) = ρOf ring t := by
    intro t; unfold ρOf; congr 2; simp [Nat.add_mod_right]
  have hring : RingFace G 7 (ρOf ring) := RingFace.mk_lt (by norm_num) hper hadj hstep hinj
  have hnbr : ∀ a w, T.Adj (int a) w →
      (∃ b, w = int b ∧ intAdj a b = true) ∨ (∃ t, t < 7 ∧ w = ρOf ring t ∧ ringAdj a t = true) := by
    intro a w hw
    fin_cases a
    · let X : ℕ → Fin n := fun j => ([(ring 1), (ring 2), (int 1), (int 2), (int 3), (ring 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 6 → Nx T (int 0) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 5 := by omega
        interval_cases j
        exacts [h.r0_0, h.r0_1, h.r0_2, h.r0_3, h.r0_4]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 6) (by simpa using h.deg 0) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨6, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨5, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inr ⟨0, by norm_num, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(ring 2), (ring 3), (ring 4), (int 2), (int 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 1) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r1_0, h.r1_1, h.r1_2, h.r1_3]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 1) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inr ⟨5, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨4, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨3, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 1), (ring 4), (ring 5), (int 3), (int 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 2) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r2_0, h.r2_1, h.r2_2, h.r2_3]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 2) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨1, rfl, by decide⟩
      · exact Or.inr ⟨3, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨2, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨3, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
    · let X : ℕ → Fin n := fun j => ([(int 2), (ring 5), (ring 6), (ring 0), (int 0)] : List (Fin n)).getD j (ring 0)
      have hc : ∀ j, j + 1 < 5 → Nx T (int 3) (X j) (X (j + 1)) := by
        intro j hj; have hj' : j < 4 := by omega
        interval_cases j
        exacts [h.r3_0, h.r3_1, h.r3_2, h.r3_3]
      obtain ⟨j, hj, rfl⟩ := nbr_of_chain (d := 5) (by simpa using h.deg 3) (nx_adj_left (hc 0 (by norm_num))) hc w hw
      interval_cases j
      · exact Or.inl ⟨2, rfl, by decide⟩
      · exact Or.inr ⟨2, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨1, by norm_num, rfl, by decide⟩
      · exact Or.inr ⟨0, by norm_num, rfl, by decide⟩
      · exact Or.inl ⟨0, rfl, by decide⟩
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

/-- **Reduction.** A triangulation in which the configuration occurs is four-colourable when every
spherical map of smaller support is. -/
theorem colorable_of_occ {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin 7 → Fin n}
    {int : Fin 4 → Fin n} (h : Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  obtain ⟨cG⟩ := IH n G (by rw [natCard_support_eq, natCard_support_eq]; exact hlt)
  exact colorable O cG (fun x y e _ _ => cG.valid e)

end SimpleGraph.SphericalMap.C2122P


open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"
