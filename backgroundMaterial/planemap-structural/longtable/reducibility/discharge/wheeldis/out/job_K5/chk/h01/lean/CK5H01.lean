import CXRing

/-! # CK5H01 (Studio, ST-42 second check, 8 Nov): K-5 hit b10_u..5665665._...655.... X={I0-I3} (famK5_r1516_04, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5h01Entries : List XRData := [
  { name := "b10_u..5665665._...655....", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b10_u..5665665._...655....", r := 15, m := 11,
      ringAdj := #[#[0, 1, 14], #[1, 2, 3], #[3, 4], #[7], #[], #[9, 10], #[10, 11, 12], #[12, 13, 14], #[4, 5, 6, 7], #[7, 8], #[8, 9]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2], #[0, 1, 3, 8], #[0, 2, 4, 8, 9], #[0, 3, 5, 9, 10], #[0, 4, 6, 10], #[0, 5, 7], #[0, 6], #[2, 3], #[3, 4, 10], #[4, 5, 9]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24] }]

theorem k5h01Entries_ok : k5h01Entries.all XRData.ok = true := by
  native_decide

theorem k5h01Entries_length : k5h01Entries.length = 1 := by
  native_decide

theorem k5h01_admissible_all : k5h01Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5h01_foldSafe_all : k5h01Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5h01Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5h01_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5h01_foldSafe_all
