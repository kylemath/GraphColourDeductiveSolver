import CXRing

/-! # CK5JO4 (Studio, K3CHK13 O4, 9 Nov): b7_u575.578_5...555 X={I0-I1} (hits_bind70_0133.tsv c378f8bd, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5jo4Entries : List XRData := [
  { name := "b7_u575.578_5...555", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b7_u575.578_5...555", r := 14, m := 11,
      ringAdj := #[#[0], #[], #[2, 3, 4], #[0, 1, 2], #[0, 13], #[10, 11], #[6, 7, 8], #[5, 6], #[4, 5], #[11, 12, 13], #[8, 9, 10]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 6, 7, 8], #[0, 1, 3, 8], #[0, 2], #[0, 5, 9], #[0, 4, 6, 9, 10], #[0, 1, 5, 7, 10], #[1, 6, 8], #[1, 2, 7], #[4, 5], #[5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23] }]

theorem k5jo4Entries_ok : k5jo4Entries.all XRData.ok = true := by
  native_decide

theorem k5jo4Entries_length : k5jo4Entries.length = 1 := by
  native_decide

theorem k5jo4_admissible_all : k5jo4Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5jo4_foldSafe_all : k5jo4Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5jo4Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5jo4_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5jo4_foldSafe_all
