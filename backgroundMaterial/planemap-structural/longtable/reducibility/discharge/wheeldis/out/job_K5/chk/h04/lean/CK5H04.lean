import CXRing

/-! # CK5H04 (Studio, ST-42 K-5 hit 04, 8 Nov): b10_u6556656..5_.5.6...... X={I0-I4,I4-I10,R7-I4} (res_K5_r1516_05.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5h04Entries : List XRData := [
  { name := "b10_u6556656..5_.5.6......", src := "EXTRAFILE", X := "I0-I4,I4-I10,R7-I4",
    cf := {
      name := "b10_u6556656..5_.5.6......", r := 16, m := 11,
      ringAdj := #[#[0, 1], #[3, 4, 5], #[5], #[7], #[7, 8], #[11, 12], #[12, 13], #[0, 13, 14, 15], #[1, 2, 3], #[5, 6, 7], #[8, 9, 10, 11]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7, 8], #[0, 2, 8], #[0, 1, 3, 9], #[0, 2, 4, 9], #[0, 3, 5, 10], #[0, 4, 6, 10], #[0, 5, 7], #[0, 6], #[0, 1], #[2, 3], #[4, 5]] },
    eqR := [(7, 4)], eqI := [(4, 0), (10, 4)],
    lbl := [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 0, 9, 10, 11, 12, 13, 14, 15, 0, 16, 17, 18, 19, 20, 21, 22, 23] }]

theorem k5h04Entries_ok : k5h04Entries.all XRData.ok = true := by
  native_decide

theorem k5h04Entries_length : k5h04Entries.length = 1 := by
  native_decide

theorem k5h04_admissible_all : k5h04Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5h04_foldSafe_all : k5h04Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5h04Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5h04_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5h04_foldSafe_all
