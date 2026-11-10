import CXRing

/-! # CK5P04 (Studio, ST-67 bind2140 hit 04, 8 Nov): b7_u5757777_555.5.5 X={I0-I1} (res_K5_r15_154305_3.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p04Entries : List XRData := [
  { name := "b7_u5757777_555.5.5", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u5757777_555.5.5", r := 15, m := 13,
      ringAdj := #[#[], #[], #[0, 1], #[], #[3, 4, 5], #[5, 6, 7], #[9, 10, 11], #[11, 12, 13], #[13, 14], #[0, 14], #[1, 2], #[2, 3], #[7, 8, 9]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7, 8, 9], #[0, 1, 3, 9, 10], #[0, 2, 4, 10, 11], #[0, 3, 5, 11], #[0, 4, 6, 12], #[0, 5, 7, 12], #[0, 1, 6, 8], #[1, 7, 9], #[1, 2, 8], #[2, 3, 11], #[3, 4, 10], #[5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26] }]

theorem k5p04Entries_ok : k5p04Entries.all XRData.ok = true := by
  native_decide

theorem k5p04Entries_length : k5p04Entries.length = 1 := by
  native_decide

theorem k5p04_admissible_all : k5p04Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p04_foldSafe_all : k5p04Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p04Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p04_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p04_foldSafe_all
