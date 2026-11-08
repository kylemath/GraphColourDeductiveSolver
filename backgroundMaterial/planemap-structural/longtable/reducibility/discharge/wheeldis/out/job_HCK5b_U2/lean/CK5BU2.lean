import CXRing

/-! # CK5BU2 (Studio, K3CHK9 U2, 8 Nov): b9_u5565.55.6_5....5..6 X={I0-I1} (kills_K5b_0525.tsv dd5a0e7f, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5bu2Entries : List XRData := [
  { name := "b9_u5565.55.6_5....5..6", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b9_u5565.55.6_5....5..6", r := 13, m := 11,
      ringAdj := #[#[0, 9], #[], #[4], #[2, 3, 4], #[0, 1, 2], #[0, 12], #[9, 10], #[7, 8, 9], #[5, 6, 7], #[4, 5], #[10, 11, 12]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7, 8, 9], #[0, 1, 3, 9], #[0, 2, 4], #[0, 3], #[0, 6, 10], #[0, 5, 10], #[0, 1, 8], #[1, 7, 9], #[1, 2, 8], #[5, 6]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22] }]

theorem k5bu2Entries_ok : k5bu2Entries.all XRData.ok = true := by
  native_decide

theorem k5bu2Entries_length : k5bu2Entries.length = 1 := by
  native_decide

theorem k5bu2_admissible_all : k5bu2Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5bu2_foldSafe_all : k5bu2Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5bu2Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5bu2_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5bu2_foldSafe_all
