import CXRing

/-! # CK5MQ2 (Studio, K3CHK14 Q2, 9 Nov): b9_u555665..._....5.... X={I4-I5} (hits_bind82_1339.tsv 63161ecb, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5mq2Entries : List XRData := [
  { name := "b9_u555665..._....5....", src := "EXTRAFILE", X := "I4-I5",
    cf := {
      name := "b9_u555665..._....5....", r := 12, m := 8,
      ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5], #[5, 6], #[6, 7, 8], #[8, 9], #[0, 11], #[9, 10, 11]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2], #[0, 1, 3], #[0, 2, 4], #[0, 3, 5], #[0, 4, 6, 7], #[0, 5, 7], #[5, 6]] },
    eqR := [], eqI := [(5, 4)],
    lbl := [0, 1, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] }]

theorem k5mq2Entries_ok : k5mq2Entries.all XRData.ok = true := by
  native_decide

theorem k5mq2Entries_length : k5mq2Entries.length = 1 := by
  native_decide

theorem k5mq2_admissible_all : k5mq2Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5mq2_foldSafe_all : k5mq2Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5mq2Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5mq2_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5mq2_foldSafe_all
