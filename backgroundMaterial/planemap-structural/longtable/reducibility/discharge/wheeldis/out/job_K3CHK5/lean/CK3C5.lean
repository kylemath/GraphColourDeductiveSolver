import CXRing

/-! # CK3C5 (Studio, K3CHK5, 7 Nov): b8_u...56556_.....66. X = {I0-I3}: XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3c5Entries : List XRData := [
  { name := "b8_u...56556_.....66.", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b8_u...56556_.....66.", r := 12, m := 8,
      ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5, 6], #[6], #[], #[0, 10, 11], #[6, 7, 8], #[8, 9, 10]],
      intAdj := #[#[1, 2, 3, 4, 5], #[0, 2], #[0, 1, 3], #[0, 2, 4, 6], #[0, 3, 5, 6, 7], #[0, 4, 7], #[3, 4, 7], #[4, 5, 6]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] }]

theorem k3c5Entries_ok : k3c5Entries.all XRData.ok = true := by
  native_decide

theorem k3c5Entries_length : k3c5Entries.length = 1 := by
  native_decide

theorem k3c5_admissible_all : k3c5Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3c5_foldSafe_all : k3c5Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3c5Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3c5_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3c5_foldSafe_all
