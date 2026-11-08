import CXRing

/-! # CK3K (Studio, HCK3k, 8 Nov): the K3k C kill b8_u...56556_.....66. = f8_...56556_.....66. of pat_K3g2_C.cfast 6f6dce95 (same literal and X as in CK3C7): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3kEntries : List XRData := [
  { name := "b8_u...56556_.....66.", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b8_u...56556_.....66.", r := 12, m := 8,
      ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5, 6], #[6], #[], #[0, 10, 11], #[6, 7, 8], #[8, 9, 10]],
      intAdj := #[#[1, 2, 3, 4, 5], #[0, 2], #[0, 1, 3], #[0, 2, 4, 6], #[0, 3, 5, 6, 7], #[0, 4, 7], #[3, 4, 7], #[4, 5, 6]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] }]

theorem k3kEntries_ok : k3kEntries.all XRData.ok = true := by
  native_decide

theorem k3kEntries_length : k3kEntries.length = 1 := by
  native_decide

theorem k3k_admissible_all : k3kEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3k_foldSafe_all : k3kEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3kEntries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3k_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3k_foldSafe_all
