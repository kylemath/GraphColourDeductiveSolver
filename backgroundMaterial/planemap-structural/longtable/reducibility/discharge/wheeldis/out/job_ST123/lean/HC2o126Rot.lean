import COccHC2o126_00

/-! # HC2o126Rot (Opus, 10 Nov 2026): `RotOcc` for the rotation `rotS`, each list started where the Studio's `rot2o126`
(job_ST123 C2o126Glue) starts it. The lists are cyclic shifts of `rot` (COccHC2o126_00), shifts I0 0, I1 4, I2 5, I3 2, so the
orientation is the same. Written by mkrotS.py, which checks in Python that each field used states the slot pair of `rotS`.
`rotS` is the same `![..]` literal as `rot2o126`, so `rotS = rot2o126` holds by `rfl`. -/

namespace SimpleGraph.SphericalMap.HC2o126_00
open VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ}

/-- The rotation of `Occ`, each list started as in `rot2o126`. -/
def rotS : Fin 4 → List (Fin 4 ⊕ ℕ) :=
  ![[.inr 0, .inr 1, .inr 2, .inl 1, .inl 2, .inl 3], [.inr 2, .inr 3, .inr 4, .inl 2, .inl 0],
    [.inr 4, .inr 5, .inr 6, .inl 3, .inl 0, .inl 1], [.inr 6, .inr 7, .inr 0, .inl 0, .inl 2]]

theorem rotS_ok : rotOK (DCheck.Conf.of18 cf) rotS = true := by decide +kernel

theorem rotOccS_of_occ {T : SphericalMap n} {ring : Fin 8 → Fin n} {int : Fin 4 → Fin n}
    (h : Occ T ring int) : RotOcc T (ρOf ring) int rotS where
  ιinj := h.int_inj
  disj := fun t a => h.disj _ a
  deg := fun a => by rw [h.deg a]; fin_cases a <;> rfl
  nx := by
    intro a k hk
    fin_cases a
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r0_0
      · exact h.r0_1
      · exact h.r0_2
      · exact h.r0_3
      · exact h.r0_4
      · exact h.r0_5
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r1_4
      · exact h.r1_0
      · exact h.r1_1
      · exact h.r1_2
      · exact h.r1_3
    · replace hk : k < 6 := hk
      interval_cases k
      · exact h.r2_5
      · exact h.r2_0
      · exact h.r2_1
      · exact h.r2_2
      · exact h.r2_3
      · exact h.r2_4
    · replace hk : k < 5 := hk
      interval_cases k
      · exact h.r3_2
      · exact h.r3_3
      · exact h.r3_4
      · exact h.r3_0
      · exact h.r3_1

end SimpleGraph.SphericalMap.HC2o126_00

#print axioms SimpleGraph.SphericalMap.HC2o126_00.rotS_ok
#print axioms SimpleGraph.SphericalMap.HC2o126_00.rotOccS_of_occ
