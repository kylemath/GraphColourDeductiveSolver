import CXRing

/-! # CK5CV8 (Studio, K3CHK10 V8, 8 Nov): b7_u56...58_6...556 X={I0-I3} (kills_K5c_0735.tsv b3efa2c5, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5cv8Entries : List XRData := [
  { name := "b7_u56...58_6...556", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b7_u56...58_6...556", r := 13, m := 9,
      ringAdj := #[#[0, 1, 2], #[], #[0, 11, 12], #[2], #[5, 6, 7], #[7, 8, 9], #[9, 10, 11], #[2, 3, 4], #[4, 5]],
      intAdj := #[#[1, 2, 3, 4], #[0, 2, 4, 5, 6], #[0, 1, 6], #[0, 4, 7, 8], #[0, 1, 3, 5, 8], #[1, 4, 6], #[1, 2, 5], #[3, 8], #[3, 4, 7]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] }]

theorem k5cv8Entries_ok : k5cv8Entries.all XRData.ok = true := by
  native_decide

theorem k5cv8Entries_length : k5cv8Entries.length = 1 := by
  native_decide

theorem k5cv8_admissible_all : k5cv8Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5cv8_foldSafe_all : k5cv8Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5cv8Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5cv8_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5cv8_foldSafe_all
