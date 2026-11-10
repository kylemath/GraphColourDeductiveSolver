import CXRing

/-! # CK5CV7 (Studio, K3CHK10 V7, 8 Nov): b7_u56785.._5.555.. X={I0-I3} (kills_K5c_0735.tsv b3efa2c5, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5cv7Entries : List XRData := [
  { name := "b7_u56785.._5.555..", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b7_u56785.._5.555..", r := 14, m := 10,
      ringAdj := #[#[0, 1], #[1, 2], #[4, 5], #[5, 6, 7], #[9, 10, 11], #[0], #[2, 3, 4], #[7, 8, 9], #[11, 12], #[0, 12, 13]],
      intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 6], #[0, 1, 3, 6], #[0, 2, 4, 7], #[0, 3, 5, 7, 8], #[0, 4, 8, 9], #[1, 2], #[3, 4], #[4, 5, 9], #[5, 8]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22] }]

theorem k5cv7Entries_ok : k5cv7Entries.all XRData.ok = true := by
  native_decide

theorem k5cv7Entries_length : k5cv7Entries.length = 1 := by
  native_decide

theorem k5cv7_admissible_all : k5cv7Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5cv7_foldSafe_all : k5cv7Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5cv7Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5cv7_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5cv7_foldSafe_all
