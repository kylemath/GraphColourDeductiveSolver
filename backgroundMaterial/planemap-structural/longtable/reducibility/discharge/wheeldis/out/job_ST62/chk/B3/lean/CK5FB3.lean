import CXRing

/-! # CK5FB3 (Studio, ST-62 bind61 B3, 8 Nov): b9_u5555...67_......65. X={I0-I1,I5-I6,R0-I0,R2-I5} (bind61 (4206a6ce8), gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5fb3Entries : List XRData := [
  { name := "b9_u5555...67_......65.", src := "EXTRAFILE", X := "I0-I1,I5-I6,R0-I0,R2-I5",
    cf := {
      name := "b9_u5555...67_......65.", r := 15, m := 9,
      ringAdj := #[#[0, 1, 2], #[10, 11], #[11, 12], #[12, 13], #[0, 13, 14], #[2, 6], #[8, 9, 10], #[2, 3, 4, 5, 6], #[6, 7, 8]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6], #[0, 1, 3], #[0, 2, 4], #[0, 3], #[0, 6, 7, 8], #[0, 1, 5, 8], #[5], #[5, 6]] },
    eqR := [(0, 0), (2, 5)], eqI := [(1, 0), (6, 5)],
    lbl := [0, 0, 1, 2, 3, 4, 4, 5, 6, 0, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] }]

theorem k5fb3Entries_ok : k5fb3Entries.all XRData.ok = true := by
  native_decide

theorem k5fb3Entries_length : k5fb3Entries.length = 1 := by
  native_decide

theorem k5fb3_admissible_all : k5fb3Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5fb3_foldSafe_all : k5fb3Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5fb3Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5fb3_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5fb3_foldSafe_all
