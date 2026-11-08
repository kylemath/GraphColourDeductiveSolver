import CXRing

/-! # CK5BL1 (Studio, K3CHK9 L1, 8 Nov): b7_u86..665_5...555 X={I0-I1} (kills_K5b_0525.tsv dd5a0e7f, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5bl1Entries : List XRData := [
  { name := "b7_u86..665_5...555", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u86..665_5...555", r := 13, m := 10,
      ringAdj := #[#[0, 1], #[7, 8, 9], #[0, 11, 12], #[1, 2, 3], #[5], #[], #[6, 7], #[9, 10, 11], #[3, 4, 5], #[5, 6]],
      intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 5, 6, 7], #[0, 1, 7], #[0, 4, 8], #[0, 3, 5, 8, 9], #[0, 1, 4, 6, 9], #[1, 5, 9], #[1, 2], #[3, 4], #[4, 5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem k5bl1Entries_ok : k5bl1Entries.all XRData.ok = true := by
  native_decide

theorem k5bl1Entries_length : k5bl1Entries.length = 1 := by
  native_decide

theorem k5bl1_admissible_all : k5bl1Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5bl1_foldSafe_all : k5bl1Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5bl1Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5bl1_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5bl1_foldSafe_all
