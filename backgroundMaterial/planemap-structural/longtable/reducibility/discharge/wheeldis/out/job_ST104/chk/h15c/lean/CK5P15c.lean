import CXRing

/-! # CK5P15c (Studio, ST-104 t102 container hit 15c, 9 Nov): b8_u.555785._....55.. X={I4-I5,R4-I5} (container_hits_t102.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p15cEntries : List XRData := [
  { name := "b8_u.555785._....55..", src := "EXTRAFILE", X := "I4-I5,R4-I5",
    cf := {
      name := "b8_u.555785._....55..", r := 14, m := 9,
      ringAdj := #[#[0, 1], #[0, 12, 13], #[11, 12], #[10, 11], #[8, 9, 10], #[4, 5, 6], #[1, 2], #[6, 7, 8], #[2, 3, 4]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2], #[0, 1, 3], #[0, 2, 4], #[0, 3, 5, 7], #[0, 4, 6, 7, 8], #[0, 5, 8], #[4, 5], #[5, 6]] },
    eqR := [(4, 5)], eqI := [(5, 4)],
    lbl := [0, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 4, 12, 13, 14, 15, 16, 17, 18, 19, 20] }]

theorem k5p15cEntries_ok : k5p15cEntries.all XRData.ok = true := by
  native_decide

theorem k5p15cEntries_length : k5p15cEntries.length = 1 := by
  native_decide

theorem k5p15c_admissible_all : k5p15cEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p15c_foldSafe_all : k5p15cEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p15cEntries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p15c_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p15c_foldSafe_all
