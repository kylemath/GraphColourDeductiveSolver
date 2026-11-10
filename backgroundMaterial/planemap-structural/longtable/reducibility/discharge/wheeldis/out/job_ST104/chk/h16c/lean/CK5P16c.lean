import CXRing

/-! # CK5P16c (Studio, ST-104 t102 container hit 16c, 9 Nov): b8_u5565.577_......5. X={I0-I1} (container_hits_t102.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p16cEntries : List XRData := [
  { name := "b8_u5565.577_......5.", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b8_u5565.577_......5.", r := 14, m := 9,
      ringAdj := #[#[0], #[5, 6], #[4, 5], #[2, 3, 4], #[0, 1, 2], #[0, 12, 13], #[10, 11, 12], #[6, 7, 8], #[8, 9, 10]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7], #[0, 1, 3], #[0, 2, 4], #[0, 3], #[0, 6], #[0, 5, 7, 8], #[0, 1, 6, 8], #[6, 7]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem k5p16cEntries_ok : k5p16cEntries.all XRData.ok = true := by
  native_decide

theorem k5p16cEntries_length : k5p16cEntries.length = 1 := by
  native_decide

theorem k5p16c_admissible_all : k5p16cEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p16c_foldSafe_all : k5p16cEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p16cEntries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p16c_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p16c_foldSafe_all
