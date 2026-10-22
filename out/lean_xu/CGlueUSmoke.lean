import CGlueU
import CXRing

set_option maxRecDepth 100000

/-! # CGlueU smoke (LT-XU): an interior-only |X| = 5 contraction with a triangle inside one merged group.
Configuration f7_...5565_....... (r 9, m 5) with X = {I0-I1, I0-I3, I0-I4, I1-I4, I3-I4}: the triangles (0,1,4) and (0,3,4) lie in
one group {0,1,3,4}. Gonthier's sparse test rejects it (cfast: INADMISSIBLE with gonthier; admissible with --nogonthier), and so
does admissibleX (|X| = 5 > 4); admissibleXU accepts it. (This X is not C-reducible for this configuration, cfast leftover > 0,
so no hC / CEntryU is built here: the smoke checks the admissibility path only.) -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

def xuSmokeL : List XRData := [
  { name := "f7_...5565_.......", src := "EXTRAFILE", X := "I0-I1,I0-I3,I0-I4,I1-I4,I3-I4",
    cf := {
      name := "f7_...5565_.......", r := 9, m := 5,
      ringAdj := #[#[0, 1, 2], #[0, 7, 8], #[2, 3, 4], #[4, 5], #[5, 6, 7]],
      intAdj := #[#[1, 2, 3, 4], #[0, 4], #[0, 3], #[0, 2, 4], #[0, 1, 3]] },
    eqR := [], eqI := [(1, 0), (3, 0), (4, 0), (4, 1), (4, 3)],
    lbl := [0, 0, 1, 0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10] }]

theorem xuSmoke_len : xuSmokeL.all (fun d => d.eqR.length + d.eqI.length == 5) = true := by native_decide
theorem xuSmoke_interior : xuSmokeL.all (fun d => d.eqR.isEmpty) = true := by native_decide
/-- the new path accepts it -/
theorem xuSmoke_admU : xuSmokeL.all (fun d => admissibleXU (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by native_decide
/-- the capped check rejects it -/
theorem xuSmoke_not_adm : xuSmokeL.all (fun d => !admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.xuSmoke_admU
#print axioms SimpleGraph.SphericalMap.CGlue.xuSmoke_not_adm
