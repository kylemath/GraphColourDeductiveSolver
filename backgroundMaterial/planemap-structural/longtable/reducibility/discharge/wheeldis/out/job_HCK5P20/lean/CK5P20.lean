import CXRing

/-! # CK5P20 (Studio, ST-111 RSST-substitute window 20, 10 Nov): fix_63c8a193fe X={I3-I9,I7-I8,R12-I8,R0-I9} (hits_st111.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p20Entries : List XRData := [
  { name := "fix_63c8a193fe", src := "EXTRAFILE", X := "I3-I9,I7-I8,R12-I8,R0-I9",
    cf := {
      name := "fix_63c8a193fe", r := 14, m := 11,
      ringAdj := #[#[4, 5], #[5, 6], #[12, 13, 0], #[1, 2, 3, 4], #[], #[6, 7], #[7, 8], #[8, 9, 10, 11], #[11, 12], #[0, 1], #[]],
      intAdj := #[#[4, 3, 1], #[5, 4, 0], #[9, 8], #[10, 9, 0, 4], #[10, 3, 0, 1, 5], #[10, 4, 1, 6], #[10, 5, 7], #[10, 6, 8], #[10, 7, 2, 9], #[10, 8, 2, 3], #[3, 4, 5, 6, 7, 8, 9]] },
    eqR := [(12, 8), (0, 9)], eqI := [(9, 3), (8, 7)],
    lbl := [0, 1, 2, 3, 4, 5, 6, 7, 7, 3, 8, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 7, 20] }]

theorem k5p20Entries_ok : k5p20Entries.all XRData.ok = true := by
  native_decide

theorem k5p20Entries_length : k5p20Entries.length = 1 := by
  native_decide

theorem k5p20_admissible_all : k5p20Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p20_foldSafe_all : k5p20Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p20Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p20_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p20_foldSafe_all
