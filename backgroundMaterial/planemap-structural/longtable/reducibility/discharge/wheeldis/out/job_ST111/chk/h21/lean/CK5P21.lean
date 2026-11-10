import CXRing

/-! # CK5P21 (Studio, ST-111 RSST-substitute window 21, 10 Nov): fix_404d45e819 X={I0-I2,I4-I5,R11-I2,R4-I5} (hits_st111.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p21Entries : List XRData := [
  { name := "fix_404d45e819", src := "EXTRAFILE", X := "I0-I2,I4-I5,R11-I2,R4-I5",
    cf := {
      name := "fix_404d45e819", r := 13, m := 6,
      ringAdj := #[#[12, 0, 1, 2, 3], #[10, 11], #[11, 12], #[3, 4], #[5, 6, 7, 8, 9, 10], #[4, 5]],
      intAdj := #[#[3, 2], #[5, 4, 2], #[5, 1, 0, 3], #[5, 2, 0], #[5, 1], #[1, 2, 3, 4]] },
    eqR := [(11, 2), (4, 5)], eqI := [(2, 0), (5, 4)],
    lbl := [0, 1, 0, 2, 3, 3, 4, 5, 6, 7, 3, 8, 9, 10, 11, 12, 13, 0, 14] }]

theorem k5p21Entries_ok : k5p21Entries.all XRData.ok = true := by
  native_decide

theorem k5p21Entries_length : k5p21Entries.length = 1 := by
  native_decide

theorem k5p21_admissible_all : k5p21Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p21_foldSafe_all : k5p21Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p21Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p21_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p21_foldSafe_all
