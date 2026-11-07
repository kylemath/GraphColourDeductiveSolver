import CXRing

/-! # CK3I (Studio, HCK3i, 7 Nov): the two K3i C kills (same literals and X as in CK3C7): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3iEntries : List XRData := [
  { name := "b7_u.5785.._55555..", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b7_u.5785.._55555..", r := 13, m := 10,
      ringAdj := #[#[0, 1, 2], #[0], #[9, 10], #[5, 6, 7], #[2], #[0, 11, 12], #[10, 11], #[7, 8, 9], #[4, 5], #[2, 3, 4]],
      intAdj := #[#[1, 2, 3, 4], #[0, 2, 5, 6], #[0, 1, 3, 6, 7], #[0, 2, 4, 7, 8], #[0, 3, 8, 9], #[1, 6], #[1, 2, 5], #[2, 3], #[3, 4, 9], #[4, 8]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] },
  { name := "b9_u...575655_....5....", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b9_u...575655_....5....", r := 13, m := 8,
      ringAdj := #[#[0, 1, 2], #[2, 3, 4], #[4, 5, 6], #[8], #[8, 9, 10], #[10, 11], #[0, 11, 12], #[6, 7, 8]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2], #[0, 1, 3, 7], #[0, 2, 4, 7], #[0, 3, 5], #[0, 4, 6], #[0, 5], #[2, 3]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] }]

theorem k3iEntries_ok : k3iEntries.all XRData.ok = true := by
  native_decide

theorem k3iEntries_length : k3iEntries.length = 2 := by
  native_decide

theorem k3i_admissible_all : k3iEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3i_foldSafe_all : k3iEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3iEntries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3i_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3i_foldSafe_all
