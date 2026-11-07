import CXRing

/-! # CK3J (Studio, HCK3j, 7 Nov): the K3j C kill b9_u.56575.55_...5...5. (same literal and X as in CK3C7): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3jEntries : List XRData := [
  { name := "b9_u.56575.55_...5...5.", src := "EXTRAFILE", X := "I0-I3",
    cf := {
      name := "b9_u.56575.55_...5...5.", r := 14, m := 10,
      ringAdj := #[#[0, 4], #[0, 12, 13], #[10, 11, 12], #[10], #[6, 7, 8], #[4, 5, 6], #[3, 4], #[0, 1], #[8, 9, 10], #[1, 2, 3]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2], #[0, 1, 3], #[0, 2, 4, 8], #[0, 3, 5, 8], #[0, 4], #[0, 7, 9], #[0, 6, 9], #[3, 4], #[6, 7]] },
    eqR := [], eqI := [(3, 0)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22] }]

theorem k3jEntries_ok : k3jEntries.all XRData.ok = true := by
  native_decide

theorem k3jEntries_length : k3jEntries.length = 1 := by
  native_decide

theorem k3j_admissible_all : k3jEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3j_foldSafe_all : k3jEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3jEntries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3j_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3j_foldSafe_all
