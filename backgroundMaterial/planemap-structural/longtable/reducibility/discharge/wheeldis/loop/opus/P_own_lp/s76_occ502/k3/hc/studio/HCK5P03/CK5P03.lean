import CXRing

/-! # CK5P03 (Studio, ST-67 bind2140 hit 03, 8 Nov): b7_u8666.65_5.5..65 X={I0-I1} (res_K5_r15_154305_4.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p03Entries : List XRData := [
  { name := "b7_u8666.65_5.5..65", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u8666.65_5.5..65", r := 15, m := 11,
      ringAdj := #[#[0], #[8, 9, 10], #[5, 6], #[4, 5], #[0, 1, 2], #[0, 13, 14], #[], #[10, 11], #[6, 7, 8], #[2, 3, 4], #[11, 12, 13]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7, 8], #[0, 1, 3, 8], #[0, 2, 4, 9], #[0, 3, 9], #[0, 6, 10], #[0, 1, 5, 7, 10], #[1, 6, 10], #[1, 2], #[3, 4], #[5, 6, 7]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] }]

theorem k5p03Entries_ok : k5p03Entries.all XRData.ok = true := by
  native_decide

theorem k5p03Entries_length : k5p03Entries.length = 1 := by
  native_decide

theorem k5p03_admissible_all : k5p03Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p03_foldSafe_all : k5p03Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p03Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p03_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p03_foldSafe_all
