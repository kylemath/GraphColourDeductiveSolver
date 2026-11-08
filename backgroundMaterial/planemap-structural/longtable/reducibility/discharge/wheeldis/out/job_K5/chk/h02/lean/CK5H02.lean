import CXRing

/-! # CK5H02 (Studio, ST-42 K-5 hit 02, 8 Nov): b10_u655665...5_756.5..... X={I0-I2} (res_K5_r1516_04.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5h02Entries : List XRData := [
  { name := "b10_u655665...5_756.5.....", src := "EXTRAFILE", X := "I0-I2",
    cf := {
      name := "b10_u655665...5_756.5.....", r := 15, m := 12,
      ringAdj := #[#[0, 1, 2], #[4, 5], #[], #[], #[10, 11], #[11, 12], #[0, 14], #[2, 3, 4], #[5, 6, 7, 8], #[8], #[8, 9, 10], #[12, 13, 14]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7, 8], #[0, 1, 3, 8, 9], #[0, 2, 4, 9, 10], #[0, 3, 5, 10], #[0, 4, 6, 11], #[0, 5, 11], #[0, 1], #[1, 2, 9], #[2, 3, 8, 10], #[3, 4, 9], #[5, 6]] },
    eqR := [], eqI := [(2, 0)],
    lbl := [0, 1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25] }]

theorem k5h02Entries_ok : k5h02Entries.all XRData.ok = true := by
  native_decide

theorem k5h02Entries_length : k5h02Entries.length = 1 := by
  native_decide

theorem k5h02_admissible_all : k5h02Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5h02_foldSafe_all : k5h02Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5h02Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5h02_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5h02_foldSafe_all
