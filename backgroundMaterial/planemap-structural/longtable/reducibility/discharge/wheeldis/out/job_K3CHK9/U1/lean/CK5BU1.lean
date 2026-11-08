import CXRing

/-! # CK5BU1 (Studio, K3CHK9 U1, 8 Nov): b9_u5555...57_5.......6 X={I0-I1} (kills_K5b_0525.tsv dd5a0e7f, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5bu1Entries : List XRData := [
  { name := "b9_u5555...57_5.......6", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b9_u5555...57_5.......6", r := 12, m := 9,
      ringAdj := #[#[0, 1, 2], #[], #[9], #[9, 10], #[0, 10, 11], #[2, 3, 4], #[4, 5, 6], #[6, 7, 8], #[8, 9]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7, 8], #[0, 1, 3, 8], #[0, 2, 4], #[0, 3], #[0, 6], #[0, 1, 5, 7], #[1, 6, 8], #[1, 2, 7]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] }]

theorem k5bu1Entries_ok : k5bu1Entries.all XRData.ok = true := by
  native_decide

theorem k5bu1Entries_length : k5bu1Entries.length = 1 := by
  native_decide

theorem k5bu1_admissible_all : k5bu1Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5bu1_foldSafe_all : k5bu1Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5bu1Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5bu1_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5bu1_foldSafe_all
