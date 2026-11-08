import CXRing

/-! # CK5P02 (Studio, ST-67 bind2140 hit 02, 8 Nov): b7_u55.6777_5..5.5. X={I0-I4,I0-I6,R0-I0} (res_K5_r15_150433_1.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p02Entries : List XRData := [
  { name := "b7_u55.6777_5..5.5.", src := "EXTRAFILE", X := "I0-I4,I0-I6,R0-I0",
    cf := {
      name := "b7_u55.6777_5..5.5.", r := 15, m := 10,
      ringAdj := #[#[0], #[3], #[0, 1], #[0, 13, 14], #[9, 10, 11], #[7, 8, 9], #[3, 4, 5], #[1, 2, 3], #[11, 12, 13], #[5, 6, 7]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7], #[0, 1, 7], #[0, 4, 8], #[0, 3, 5, 8], #[0, 4, 6, 9], #[0, 1, 5, 9], #[1, 2], #[3, 4], #[5, 6]] },
    eqR := [(0, 0)], eqI := [(4, 0), (6, 0)],
    lbl := [0, 1, 2, 3, 0, 4, 0, 5, 6, 7, 0, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem k5p02Entries_ok : k5p02Entries.all XRData.ok = true := by
  native_decide

theorem k5p02Entries_length : k5p02Entries.length = 1 := by
  native_decide

theorem k5p02_admissible_all : k5p02Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p02_foldSafe_all : k5p02Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p02Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p02_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p02_foldSafe_all
