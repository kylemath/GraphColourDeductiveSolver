import CXRing

/-! # CK5P17 (Studio, ST-103 bindt98 hit 17, 9 Nov): b7_u575.687_555.555 X={I0-I1} (res_K5_r15_051158_0.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p17Entries : List XRData := [
  { name := "b7_u575.687_555.555", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u575.687_555.555", r := 15, m := 13,
      ringAdj := #[#[0], #[], #[3, 4], #[0], #[0, 13, 14], #[9, 10, 11], #[6, 7], #[5, 6], #[4, 5], #[2, 3], #[0, 1, 2], #[11, 12, 13], #[7, 8, 9]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7, 8], #[0, 1, 3, 8, 9], #[0, 2, 9, 10], #[0, 5, 11], #[0, 4, 6, 11, 12], #[0, 1, 5, 7, 12], #[1, 6, 8], #[1, 2, 7], #[2, 3, 10], #[3, 9], #[4, 5], #[5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26] }]

theorem k5p17Entries_ok : k5p17Entries.all XRData.ok = true := by
  native_decide

theorem k5p17Entries_length : k5p17Entries.length = 1 := by
  native_decide

theorem k5p17_admissible_all : k5p17Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p17_foldSafe_all : k5p17Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p17Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p17_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p17_foldSafe_all
