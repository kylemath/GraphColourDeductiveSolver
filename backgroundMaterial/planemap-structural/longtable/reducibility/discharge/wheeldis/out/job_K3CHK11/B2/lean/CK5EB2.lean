import CXRing

/-! # CK5EB2 (Studio, K3CHK11 B2, 8 Nov): b9_u556575..._..56..... X={I0-I1} (kills_K5e_1035.tsv 070e1f63, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5eb2Entries : List XRData := [
  { name := "b9_u556575..._..56.....", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b9_u556575..._..56.....", r := 13, m := 9,
      ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5], #[5, 6], #[], #[9, 10, 11], #[0, 11, 12], #[6, 7], #[7, 8, 9]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2], #[0, 1, 3], #[0, 2, 4, 7], #[0, 3, 5, 7, 8], #[0, 4, 6, 8], #[0, 5], #[3, 4, 8], #[4, 5, 7]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] }]

theorem k5eb2Entries_ok : k5eb2Entries.all XRData.ok = true := by
  native_decide

theorem k5eb2Entries_length : k5eb2Entries.length = 1 := by
  native_decide

theorem k5eb2_admissible_all : k5eb2Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5eb2_foldSafe_all : k5eb2Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5eb2Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5eb2_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5eb2_foldSafe_all
