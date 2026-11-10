import CXRing

/-! # CK5P22 (Studio, ST-110 bindt107 hit 22, 10 Nov): b7_u666676._5..55.. X={I0-I5} (res_K5_r15_063913_0.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p22Entries : List XRData := [
  { name := "b7_u666676._5..55..", src := "EXTRAFILE", X := "I0-I5",
    cf := {
      name := "b7_u666676._5..55..", r := 15, m := 10,
      ringAdj := #[#[0], #[0, 1, 2], #[4, 5], #[5, 6, 7], #[7, 8], #[10, 11], #[0, 13, 14], #[2, 3, 4], #[8, 9, 10], #[11, 12, 13]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 7], #[0, 1, 3, 7], #[0, 2, 4], #[0, 3, 5, 8], #[0, 4, 6, 8, 9], #[0, 5, 9], #[1, 2], #[4, 5], #[5, 6]] },
    eqR := [], eqI := [(5, 0)],
    lbl := [0, 1, 2, 3, 4, 0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] }]

theorem k5p22Entries_ok : k5p22Entries.all XRData.ok = true := by
  native_decide

theorem k5p22Entries_length : k5p22Entries.length = 1 := by
  native_decide

theorem k5p22_admissible_all : k5p22Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p22_foldSafe_all : k5p22Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p22Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p22_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p22_foldSafe_all
