import CXRing

/-! # CK3C2 (Studio, K3CHK2, 7 Nov): b9_u655...566_66......5 with X = {I5-I6}: XRData.ok, admissibleX, foldSafeX and cReducible18 hC. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3c2Entries : List XRData := [
  { name := "b9_u655...566_66......5", src := "EXTRAFILE", X := "I5-I6",
    cf := {
      name := "b9_u655...566_66......5", r := 14, m := 10,
      ringAdj := #[#[0, 1, 2], #[9], #[], #[0, 13], #[2, 3, 4], #[4, 5, 6], #[6, 7], #[7, 8, 9], #[9, 10, 11], #[11, 12, 13]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7, 8], #[0, 1, 3, 8, 9], #[0, 2, 9], #[0, 5], #[0, 4, 6], #[0, 1, 5, 7], #[1, 6], #[1, 2, 9], #[2, 3, 8]] },
    eqR := [], eqI := [(6, 5)],
    lbl := [0, 1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22] }]

theorem k3c2Entries_ok : k3c2Entries.all XRData.ok = true := by
  native_decide

theorem k3c2Entries_length : k3c2Entries.length = 1 := by
  native_decide

theorem k3c2_admissible_all : k3c2Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3c2_foldSafe_all : k3c2Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3c2Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3c2_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3c2_foldSafe_all
