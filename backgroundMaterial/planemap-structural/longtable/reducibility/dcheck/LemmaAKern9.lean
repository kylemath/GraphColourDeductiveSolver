import DCheckR2D

/-! Lemma A, ring-9 kernel (explore thread, 16 Oct; key k40ce36119c7d4c3b; exploratory). A 7 `u` with three
consecutive five-neighbours `w0 w1 w2`, where `s0 = 5`, `s1 = 7`, `s2 = 5` (`s_j` is the common neighbour of
`w_j`, `w_(j+1)` other than `u`). It covers 29 of the 40 kernelised k = 5 hits. The dfast line (`loop/lemmaA/kern9.txt`) is
  kern9_u7_w555_s575 9 7 0,1,2,3;3,4;-;0;4,5;5,6,7;0,7,8 1,2,3;0,2,4;0,1,3,4,5;0,2,5,6;1,2,5;2,3,4,6;3,5
and was re-run by Studio dfast18: r=9 m=7 classes=820 ext=264 reached=820 D=true depth=5.
Interior: 0 u (7), 1 w0, 2 w1, 3 w2, 4 s0 (5 each), 5 s1 (7), 6 s2 (5). -/

namespace DCheck.LemmaA
open SimpleGraph SimpleGraph.SphericalMap VacancySlide DCheck.R2

def cfK9 : Conf where
  name := "kern9_u7_w555_s575"
  r := 9
  m := 7
  ringAdj := #[#[0, 1, 2, 3], #[3, 4], #[], #[0], #[4, 5], #[5, 6, 7], #[0, 7, 8]]
  intAdj := #[#[1, 2, 3], #[0, 2, 4], #[0, 1, 3, 4, 5], #[0, 2, 5, 6], #[1, 2, 5], #[2, 3, 4, 6], #[3, 5]]

/-- The checker's numbers, pinned (as dfast18). -/
theorem cfK9_run : run cfK9 = { classes := 820, ext := 264, reached := 820, depth := 5 } := by native_decide

theorem cfK9_dReducible : dReducible cfK9 = true := by native_decide

theorem cfK9_sym : ∀ a b, intAdjOf cfK9 a b = true → intAdjOf cfK9 b a = true := by native_decide
theorem cfK9_loop : ∀ a, intAdjOf cfK9 a a = false := by native_decide

/-- **The kernel is reducible** (through R2): an occurrence with a proper colouring of the outside map gives a
4-colouring of `T`. -/
theorem colorable_of_occ {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n} {ι : Fin cfK9.m → Fin n}
    (O : ConfigOcc T G cfK9.r cfK9.m ρ ι (intAdjOf cfK9) (ringAdjOf cfK9))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4 :=
  ConfigOcc.colorable_of_dReducible cfK9 cfK9_dReducible (by decide) (by decide) cfK9_sym cfK9_loop O hc

/-! Second ring-9 kernel (key ke009489629ff6070; 7 of the 40 k = 5 hits): `u` a 7 with link 5 5 5 x 5 5 y (`w3`, `w6` free
on the ring) and `s4 = 5`. dfast line
  kern9b_u7_w555x55_s4_5 9 7 0,5;3,4,5;2,3;0,1,2;0,8;5,6;6,7,8 1,2,3,4,5;0,2;0,1,3;0,2;0,5,6;0,4,6;4,5
re-run by Studio dfast18: r=9 m=7 classes=820 ext=258 reached=820 D=true depth=7.
Interior: 0 u (7), 1 w0, 2 w1, 3 w2, 4 w4, 5 w5, 6 s4 (5 each). -/

def cfK9b : Conf where
  name := "kern9b_u7_w555x55_s4_5"
  r := 9
  m := 7
  ringAdj := #[#[0, 5], #[3, 4, 5], #[2, 3], #[0, 1, 2], #[0, 8], #[5, 6], #[6, 7, 8]]
  intAdj := #[#[1, 2, 3, 4, 5], #[0, 2], #[0, 1, 3], #[0, 2], #[0, 5, 6], #[0, 4, 6], #[4, 5]]

theorem cfK9b_run : run cfK9b = { classes := 820, ext := 258, reached := 820, depth := 7 } := by native_decide
theorem cfK9b_dReducible : dReducible cfK9b = true := by native_decide
theorem cfK9b_sym : ∀ a b, intAdjOf cfK9b a b = true → intAdjOf cfK9b b a = true := by native_decide
theorem cfK9b_loop : ∀ a, intAdjOf cfK9b a a = false := by native_decide

/-- **The second kernel is reducible** (through R2). -/
theorem colorable_of_occ_b {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n} {ι : Fin cfK9b.m → Fin n}
    (O : ConfigOcc T G cfK9b.r cfK9b.m ρ ι (intAdjOf cfK9b) (ringAdjOf cfK9b))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4 :=
  ConfigOcc.colorable_of_dReducible cfK9b cfK9b_dReducible (by decide) (by decide) cfK9b_sym cfK9b_loop O hc

end DCheck.LemmaA

#print axioms DCheck.LemmaA.cfK9_run
#print axioms DCheck.LemmaA.colorable_of_occ
#print axioms DCheck.LemmaA.cfK9b_run
#print axioms DCheck.LemmaA.colorable_of_occ_b
