import CXRing

/-! # CK5GB3 (Studio, K3CHK12 B3, 8 Nov): b9_u55555..67_.......5. X={I0-I1} (kills_K5g_1630.tsv 48fa0aae, gen_ccover3 3c9e7145 EXTRAFILE literal): XRData.ok, admissibleX, foldSafeX. -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k5gb3Entries : List XRData := [
  { name := "b9_u55555..67_.......5.", src := "EXTRAFILE", X := "I0-I1",
    cf := {
      name := "b9_u55555..67_.......5.", r := 13, m := 9,
      ringAdj := #[#[0, 1], #[7, 8], #[8, 9], #[9, 10], #[10, 11], #[0, 11, 12], #[1, 2, 3], #[5, 6, 7], #[3, 4, 5]],
      intAdj := #[#[1, 2, 3, 4, 5, 6, 7], #[0, 2, 7], #[0, 1, 3], #[0, 2, 4], #[0, 3, 5], #[0, 4], #[0, 7, 8], #[0, 1, 6, 8], #[6, 7]] },
    eqR := [], eqI := [(1, 0)],
    lbl := [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] }]

theorem k5gb3Entries_ok : k5gb3Entries.all XRData.ok = true := by
  native_decide

theorem k5gb3Entries_length : k5gb3Entries.length = 1 := by
  native_decide

theorem k5gb3_admissible_all : k5gb3Entries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k5gb3_foldSafe_all : k5gb3Entries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.k5gb3Entries_ok
#print axioms SimpleGraph.SphericalMap.CGlue.k5gb3_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k5gb3_foldSafe_all
