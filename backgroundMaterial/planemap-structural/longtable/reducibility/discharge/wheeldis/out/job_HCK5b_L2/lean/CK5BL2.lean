import CXRing

/-! # CK5BL2 (Studio, K3CHK9 L2, 8 Nov): b7_u5656777_5...5.5 X={I0-I1} (kills_K5b_0525.tsv dd5a0e7f, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5bl2Entries : List XRData := [
  { name := "b7_u5656777_5...5.5", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u5656777_5...5.5", r := 14, m := 11,
      ringAdj := #[#[], #[], #[0, 1], #[1, 2], #[2, 3, 4], #[4, 5, 6], #[8, 9, 10], #[10, 11, 12], #[12, 13], #[0, 13], #[6, 7, 8]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7, 8, 9], #[0, 1, 3, 9], #[0, 2, 4], #[0, 3, 5], #[0, 4, 6, 10], #[0, 5, 7, 10], #[0, 1, 6, 8], #[1, 7, 9], #[1, 2, 8], #[5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] }]

theorem k5bl2Entries_ok : k5bl2Entries.all XRData.ok = true := by
  native_decide

theorem k5bl2Entries_length : k5bl2Entries.length = 1 := by
  native_decide

theorem k5bl2_admissible_all : k5bl2Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5bl2_foldSafe_all : k5bl2Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5bl2Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5bl2_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5bl2_foldSafe_all
