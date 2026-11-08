import CXRing

/-! # CK5CV6 (Studio, K3CHK10 V6, 8 Nov): b8_u56675..._..565... X={I2-I3} (kills_K5c_0735.tsv b3efa2c5, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5cv6Entries : List XRData := [
  { name := "b8_u56675..._..565...", src := "EXTRAFILE", X := "I2-I3",
    cf := {
      name := "b8_u56675..._..565...", r := 14, m := 9,
      ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5, 6], #[6, 7], #[9, 10], #[0], #[7, 8, 9], #[10, 11, 12], #[0, 12, 13]],
      intAdj := #[#[1, 2, 3, 4, 5], #[0, 2], #[0, 1, 3], #[0, 2, 4, 6], #[0, 3, 5, 6, 7], #[0, 4, 7, 8], #[3, 4], #[4, 5, 8], #[5, 7]] },
    eqR := [], eqI := [(3, 2)],
    lbl := [0, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem k5cv6Entries_ok : k5cv6Entries.all XRData.ok = true := by
  native_decide

theorem k5cv6Entries_length : k5cv6Entries.length = 1 := by
  native_decide

theorem k5cv6_admissible_all : k5cv6Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5cv6_foldSafe_all : k5cv6Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5cv6Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5cv6_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5cv6_foldSafe_all
