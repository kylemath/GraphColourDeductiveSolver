import CXRing

/-! # CK5H05 (Studio, ST-42 K-5 hit 05, 8 Nov): b7_u7676.55_..5..66 X={I0-I4} (res_K5_r1516_09.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5h05Entries : List XRData := [
  { name := "b7_u7676.55_..5..66", src := "EXTRAFILE", X := "I0-I4",
    cf := {
      name := "b7_u7676.55_..5..66", r := 15, m := 10,
      ringAdj := #[#[0], #[8, 9, 10], #[6, 7, 8], #[4, 5, 6], #[0, 1, 2], #[0, 14], #[], #[10, 11, 12], #[2, 3, 4], #[12, 13, 14]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7], #[0, 1, 3], #[0, 2, 4, 8], #[0, 3, 8], #[0, 6, 9], #[0, 1, 5, 7, 9], #[1, 6, 9], #[3, 4], #[5, 6, 7]] },
    eqR := [], eqI := [(4, 0)],
    lbl := [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] }]

theorem k5h05Entries_ok : k5h05Entries.all XRData.ok = true := by
  native_decide

theorem k5h05Entries_length : k5h05Entries.length = 1 := by
  native_decide

theorem k5h05_admissible_all : k5h05Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5h05_foldSafe_all : k5h05Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5h05Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5h05_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5h05_foldSafe_all
