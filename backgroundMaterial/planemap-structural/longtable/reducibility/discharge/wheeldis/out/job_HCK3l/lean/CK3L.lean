import CXRing

/-! # CK3L (Studio, HCK3l, 8 Nov): the GL5 binder C kill b7_u.666666_.5...5. = f7_.666666_.5...5., X={R0-I0} rim-pinned (kills_AB_0215.tsv c5000391; gen_ccover3 3c9e7145 EXTRAFILE literal, K3CHK8): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k3lEntries : List XRData := [
  { name := "b7_u.666666_.5...5.", src := "EXTRAFILE", X := "R0-I0",
    cf := {
      name := "b7_u.666666_.5...5.", r := 14, m := 9,
      ringAdj := #[#[0], #[0, 12, 13], #[9, 10], #[7, 8, 9], #[5, 6, 7], #[4, 5], #[0, 1, 2], #[10, 11, 12], #[2, 3, 4]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 7], #[0, 1, 3, 7], #[0, 2, 4], #[0, 3, 5], #[0, 4, 6, 8], #[0, 5, 8], #[1, 2], #[5, 6]] },
    eqR := [(0, 0)], eqI := [],
    lbl := [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem k3lEntries_ok : k3lEntries.all XRData.ok = true := by
  native_decide

theorem k3lEntries_length : k3lEntries.length = 1 := by
  native_decide

theorem k3l_admissible_all : k3lEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k3l_foldSafe_all : k3lEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k3lEntries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k3l_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k3l_foldSafe_all
