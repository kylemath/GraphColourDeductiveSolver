import CXRing

/-! # CK3C3 (Studio, K3CHK3, 7 Nov): b9_u.56.56555_.5....... X = {I0-I5}: XRData.ok, admissibleX, foldSafeX, hC. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3c3Entries : List XRData := [
  { name := "b9_u.56.56555_.5.......", src := "EXTRAFILE", X := "I0-I5",
    cf := {
      name := "b9_u.56.56555_.5.......", r := 13, m := 9,
      ringAdj := #[#[0, 8], #[0, 12], #[8, 9, 10], #[6, 7, 8], #[4, 5, 6], #[3, 4], #[2, 3], #[0, 1, 2], #[10, 11, 12]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 8], #[0, 1, 8], #[0, 4], #[0, 3, 5], #[0, 4, 6], #[0, 5, 7], #[0, 6], #[1, 2]] },
    eqR := [], eqI := [(5, 0)],
    lbl := [0, 1, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] }]

theorem k3c3Entries_ok : k3c3Entries.all XRData.ok = true := by
  native_decide

theorem k3c3Entries_length : k3c3Entries.length = 1 := by
  native_decide

theorem k3c3_admissible_all : k3c3Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3c3_foldSafe_all : k3c3Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3c3Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3c3_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3c3_foldSafe_all
