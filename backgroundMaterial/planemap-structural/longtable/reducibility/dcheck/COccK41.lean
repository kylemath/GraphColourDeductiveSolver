import COccBridge
import K41

/-! Bridge test (Long Table, 19 Oct 2026): the occ24 key `K41`'s rotation occurrence `Occ` gives
`RotOcc` with the rotation read off its own `Nx` fields, hence `OccExact`, `NbrInj` and `ApexFacts`.
Only `int_inj`, `disj`, `deg` and the `Nx` fields of `Occ` are used (no `ring_inj`). -/

namespace SimpleGraph.SphericalMap.K41
open VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ}

/-- The rotation at each interior vertex, as `Occ` states it. -/
def rot : Fin 18 → List (Fin 18 ⊕ ℕ) := ![[.inl 2, .inl 3, .inl 4, .inl 5, .inl 1], [.inl 0, .inl 5, .inl 17, .inl 6, .inl 7, .inl 2], [.inl 0, .inl 1, .inl 7, .inl 8, .inl 9, .inl 3], [.inl 0, .inl 2, .inl 9, .inl 10, .inl 11, .inl 4], [.inl 3, .inl 11, .inl 12, .inl 13, .inl 5, .inl 0], [.inl 4, .inl 13, .inl 14, .inl 15, .inl 16, .inl 17, .inl 1, .inl 0], [.inl 7, .inl 1, .inl 17, .inr 17, .inr 0], [.inr 1, .inl 8, .inl 2, .inl 1, .inl 6, .inr 0], [.inr 2, .inr 3, .inl 9, .inl 2, .inl 7, .inr 1], [.inr 4, .inl 10, .inl 3, .inl 2, .inl 8, .inr 3], [.inr 5, .inr 6, .inl 11, .inl 3, .inl 9, .inr 4], [.inr 6, .inr 7, .inl 12, .inl 4, .inl 3, .inl 10], [.inr 7, .inr 8, .inr 9, .inl 13, .inl 4, .inl 11], [.inr 9, .inr 10, .inl 14, .inl 5, .inl 4, .inl 12], [.inr 11, .inr 12, .inl 15, .inl 5, .inl 13, .inr 10], [.inr 13, .inr 14, .inl 16, .inl 5, .inl 14, .inr 12], [.inr 14, .inr 15, .inr 16, .inl 17, .inl 5, .inl 15], [.inr 16, .inr 17, .inl 6, .inl 1, .inl 5, .inl 16]]

theorem rot_ok : rotOK (DCheck.Conf.of18 cf) rot = true := by
  native_decide

theorem rotOcc_of_occ {T : SphericalMap n} {ring : Fin 18 → Fin n} {int : Fin 18 → Fin n}
    (h : Occ T ring int) : RotOcc T (ρOf ring) int rot where
  ιinj := h.int_inj
  disj := fun t a => h.disj _ a
  deg := fun a => by rw [h.deg a]; fin_cases a <;> rfl
  nx := by
    intro a k hk
    fin_cases a
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r0_0
      · exact h.r0_1
      · exact h.r0_2
      · exact h.r0_3
      · exact h.r0_4
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r1_0
      · exact h.r1_1
      · exact h.r1_2
      · exact h.r1_3
      · exact h.r1_4
      · exact h.r1_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r2_0
      · exact h.r2_1
      · exact h.r2_2
      · exact h.r2_3
      · exact h.r2_4
      · exact h.r2_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r3_0
      · exact h.r3_1
      · exact h.r3_2
      · exact h.r3_3
      · exact h.r3_4
      · exact h.r3_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r4_0
      · exact h.r4_1
      · exact h.r4_2
      · exact h.r4_3
      · exact h.r4_4
      · exact h.r4_5
    · replace hk : k < 8 := hk
      interval_cases k
      · exact h.r5_0
      · exact h.r5_1
      · exact h.r5_2
      · exact h.r5_3
      · exact h.r5_4
      · exact h.r5_5
      · exact h.r5_6
      · exact h.r5_7
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r6_0
      · exact h.r6_1
      · exact h.r6_2
      · exact h.r6_3
      · exact h.r6_4
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r7_0
      · exact h.r7_1
      · exact h.r7_2
      · exact h.r7_3
      · exact h.r7_4
      · exact h.r7_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r8_0
      · exact h.r8_1
      · exact h.r8_2
      · exact h.r8_3
      · exact h.r8_4
      · exact h.r8_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r9_0
      · exact h.r9_1
      · exact h.r9_2
      · exact h.r9_3
      · exact h.r9_4
      · exact h.r9_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r10_0
      · exact h.r10_1
      · exact h.r10_2
      · exact h.r10_3
      · exact h.r10_4
      · exact h.r10_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r11_0
      · exact h.r11_1
      · exact h.r11_2
      · exact h.r11_3
      · exact h.r11_4
      · exact h.r11_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r12_0
      · exact h.r12_1
      · exact h.r12_2
      · exact h.r12_3
      · exact h.r12_4
      · exact h.r12_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r13_0
      · exact h.r13_1
      · exact h.r13_2
      · exact h.r13_3
      · exact h.r13_4
      · exact h.r13_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r14_0
      · exact h.r14_1
      · exact h.r14_2
      · exact h.r14_3
      · exact h.r14_4
      · exact h.r14_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r15_0
      · exact h.r15_1
      · exact h.r15_2
      · exact h.r15_3
      · exact h.r15_4
      · exact h.r15_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r16_0
      · exact h.r16_1
      · exact h.r16_2
      · exact h.r16_3
      · exact h.r16_4
      · exact h.r16_5
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r17_0
      · exact h.r17_1
      · exact h.r17_2
      · exact h.r17_3
      · exact h.r17_4
      · exact h.r17_5

/-- **Falsification test, passed**: `Occ` gives the three local facts. -/
theorem local_facts_of_occ {T : SphericalMap n} {ring : Fin 18 → Fin n} {int : Fin 18 → Fin n}
    (h : Occ T ring int) :
    OccExact T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    NbrInj (DCheck.Conf.of18 cf).r (ρOf ring) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    ApexFacts T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) :=
  ⟨(rotOcc_of_occ h).occExact rot_ok, (rotOcc_of_occ h).nbrInj rot_ok,
    (rotOcc_of_occ h).apexFacts rot_ok cf_sym⟩

end SimpleGraph.SphericalMap.K41

#print axioms SimpleGraph.SphericalMap.K41.local_facts_of_occ

