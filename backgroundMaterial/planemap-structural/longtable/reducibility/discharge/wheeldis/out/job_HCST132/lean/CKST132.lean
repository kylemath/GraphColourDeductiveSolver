import CXRing

/-! # CKST132 (Studio, ST-132, 11 Nov): the 1 W6b rotation-respecting C substitute (rotsub15_kc cc9da169), own-engine K3CHK PASS, gen_ccover3 3c9e7145 EXTRAFILE literal: XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def st132Entries : List XRData := [
  { name := "fw_ac168199bf", src := "EXTRAFILE", X := "I1-I5",
    cf := {
      name := "fw_ac168199bf", r := 13, m := 10,
      ringAdj := #[#[2, 0, 1], #[5, 6, 7], #[7, 8, 9], #[11, 12, 0], #[4, 5], #[7], #[9, 10], #[10, 11], #[2, 3, 4], #[10, 4]],
      intAdj := #[#[8, 3], #[5, 4], #[6, 5], #[8, 7, 0], #[9, 1, 5], #[9, 4, 1, 2, 6], #[9, 5, 2], #[9, 3, 8], #[9, 7, 3, 0], #[4, 5, 6, 7, 8]] },
    eqR := [], eqI := [(5, 1)],
    lbl := [0, 1, 2, 3, 4, 1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem st132Entries_ok : st132Entries.all XRData.ok = true := by
  native_decide

theorem st132Entries_length : st132Entries.length = 1 := by
  native_decide

theorem st132_admissible_all : st132Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem st132_foldSafe_all : st132Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.st132Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.st132_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.st132_foldSafe_all
