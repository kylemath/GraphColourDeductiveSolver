import CXRing

/-! # CK5P19 (Studio, ST-109 container t107b hit 19, 10 Nov): b7_u556.577_56...5. X={I0-I1} (container_hits_t107b.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p19Entries : List XRData := [
  { name := "b7_u556.577_56...5.", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u556.577_56...5.", r := 13, m := 10,
      ringAdj := #[#[0], #[5], #[], #[0, 1, 2], #[0, 11, 12], #[9, 10, 11], #[5, 6, 7], #[4, 5], #[2, 3, 4], #[7, 8, 9]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7], #[0, 1, 3, 7, 8], #[0, 2, 8], #[0, 5], #[0, 4, 6, 9], #[0, 1, 5, 9], #[1, 2, 8], #[2, 3, 7], #[5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] }]

theorem k5p19Entries_ok : k5p19Entries.all XRData.ok = true := by
  native_decide

theorem k5p19Entries_length : k5p19Entries.length = 1 := by
  native_decide

theorem k5p19_admissible_all : k5p19Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p19_foldSafe_all : k5p19Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p19Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p19_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p19_foldSafe_all
