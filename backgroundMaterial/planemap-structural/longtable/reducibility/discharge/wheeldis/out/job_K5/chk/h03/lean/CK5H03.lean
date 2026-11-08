import CXRing

/-! # CK5H03 (Studio, ST-42 K-5 hit 03, 8 Nov): b10_u655665..55_756....... X={I0-I2} (res_K5_r1516_04.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5h03Entries : List XRData := [
  { name := "b10_u655665..55_756.......", src := "EXTRAFILE", X := "I0-I2",
    cf := {
      name := "b10_u655665..55_756.......", r := 15, m := 12,
      ringAdj := #[#[0, 1], #[4, 5], #[], #[], #[10, 11], #[11, 12, 13], #[0, 13, 14], #[1, 2, 3], #[3, 4], #[5, 6, 7, 8], #[8], #[8, 9, 10]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7, 8], #[0, 2, 8, 9], #[0, 1, 3, 9, 10], #[0, 2, 4, 10, 11], #[0, 3, 5, 11], #[0, 4, 6], #[0, 5], #[0, 8], #[0, 1, 7], #[1, 2, 10], #[2, 3, 9, 11], #[3, 4, 10]] },
    eqR := [], eqI := [(2, 0)],
    lbl := [0, 1, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25] }]

theorem k5h03Entries_ok : k5h03Entries.all XRData.ok = true := by
  native_decide

theorem k5h03Entries_length : k5h03Entries.length = 1 := by
  native_decide

theorem k5h03_admissible_all : k5h03Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5h03_foldSafe_all : k5h03Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5h03Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5h03_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5h03_foldSafe_all
