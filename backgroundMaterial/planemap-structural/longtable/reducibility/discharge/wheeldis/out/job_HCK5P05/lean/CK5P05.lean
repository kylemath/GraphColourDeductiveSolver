import CXRing

/-! # CK5P05 (Studio, ST-67 bind2140 hit 05, 8 Nov): b8_u76676556_.5..656. X={I1-I2,I3-I4,R4-I2,R6-I3} (res_K5_r16_201644_3.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p05Entries : List XRData := [
  { name := "b8_u76676556_.5..656.", src := "EXTRAFILE", X := "I1-I2,I3-I4,R4-I2,R6-I3",
    cf := {
      name := "b8_u76676556_.5..656.", r := 16, m := 13,
      ringAdj := #[#[], #[0, 1, 2, 3], #[3, 4], #[6, 7], #[7, 8, 9, 10], #[10, 11], #[], #[], #[0, 15], #[4, 5, 6], #[11, 12, 13], #[13], #[13, 14, 15]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7, 8], #[0, 2, 8], #[0, 1, 3, 9], #[0, 2, 4, 9], #[0, 3, 5], #[0, 4, 6, 10], #[0, 5, 7, 10, 11], #[0, 6, 8, 11, 12], #[0, 1, 7, 12], #[2, 3], #[5, 6, 11], #[6, 7, 10, 12], #[7, 8, 11]] },
    eqR := [(4, 2), (6, 3)], eqI := [(2, 1), (4, 3)],
    lbl := [0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 1, 15, 2, 16, 17, 18, 19, 20, 21, 22, 23, 24] }]

theorem k5p05Entries_ok : k5p05Entries.all XRData.ok = true := by
  native_decide

theorem k5p05Entries_length : k5p05Entries.length = 1 := by
  native_decide

theorem k5p05_admissible_all : k5p05Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p05_foldSafe_all : k5p05Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p05Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p05_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p05_foldSafe_all
