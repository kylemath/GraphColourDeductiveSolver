import CXRing

/-! # CK5P07 (Studio, ST-76 bind75 hit 07, 9 Nov): b8_u55667766_...5.5.. X={I0-I4} (res_K5_r16_001930_1.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p07Entries : List XRData := [
  { name := "b8_u55667766_...5.5..", src := "EXTRAFILE", X := "I0-I4",
    cf := {
      name := "b8_u55667766_...5.5..", r := 16, m := 11,
      ringAdj := #[#[], #[0, 1], #[1, 2], #[2, 3, 4], #[4, 5], #[7, 8, 9], #[9, 10, 11], #[13, 14], #[0, 14, 15], #[5, 6, 7], #[11, 12, 13]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7, 8], #[0, 2, 8], #[0, 1, 3], #[0, 2, 4], #[0, 3, 5, 9], #[0, 4, 6, 9], #[0, 5, 7, 10], #[0, 6, 8, 10], #[0, 1, 7], #[4, 5], #[6, 7]] },
    eqR := [], eqI := [(4, 0)],
    lbl := [0, 1, 2, 3, 0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25] }]

theorem k5p07Entries_ok : k5p07Entries.all XRData.ok = true := by
  native_decide

theorem k5p07Entries_length : k5p07Entries.length = 1 := by
  native_decide

theorem k5p07_admissible_all : k5p07Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p07_foldSafe_all : k5p07Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p07Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p07_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p07_foldSafe_all
