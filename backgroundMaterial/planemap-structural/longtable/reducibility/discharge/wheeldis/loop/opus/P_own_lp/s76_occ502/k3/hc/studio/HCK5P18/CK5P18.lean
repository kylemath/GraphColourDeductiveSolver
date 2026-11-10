import CXRing

/-! # CK5P18 (Studio, ST-109 container t107b hit 18, 10 Nov): b7_u575..58_5....55 X={I0-I1} (container_hits_t107b.tsv, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5p18Entries : List XRData := [
  { name := "b7_u575..58_5....55", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u575..58_5....55", r := 12, m := 9,
      ringAdj := #[#[0, 1], #[], #[8, 9, 10], #[0, 10, 11], #[1, 2], #[4, 5, 6], #[6, 7], #[7, 8], #[2, 3, 4]],
      intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 5, 6, 7], #[0, 1, 3, 7], #[0, 2], #[0, 5, 8], #[0, 1, 4, 6, 8], #[1, 5, 7], #[1, 2, 6], #[4, 5]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] }]

theorem k5p18Entries_ok : k5p18Entries.all XRData.ok = true := by
  native_decide

theorem k5p18Entries_length : k5p18Entries.length = 1 := by
  native_decide

theorem k5p18_admissible_all : k5p18Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5p18_foldSafe_all : k5p18Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5p18Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5p18_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5p18_foldSafe_all
