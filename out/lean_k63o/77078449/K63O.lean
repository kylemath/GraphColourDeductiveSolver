import CXRing

/-! # K63O (Studio, coordinator 21 Oct 19:09Z): the 3 new rim-pinned C entries of explore adm63o (77078449,
loop/k63/adm63o/k3x_C.cfast md5 1f17e838), as `XRData`, for the foldSafeX / admissibleX / XRData.ok check (as K63F). -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck DCheck.R2

set_option maxRecDepth 100000

def k63oEntries : List XRData := [
  { name := "f7_.557565_.5...8.", src := "loop/k47/r63o_kills_cf.cfast", X := "I0-I3,I5-I8,R0-I0,R7-I5",
    cf := {
      name := "f7_.557565_.5...8.", r := 14, m := 9,
      ringAdj := #[#[0], #[0, 13], #[11], #[8, 9, 10, 11], #[7, 8], #[6, 7], #[0, 1], #[11, 12, 13], #[1, 2, 3, 4, 5, 6]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 7], #[0, 1, 3, 7], #[0, 2, 4], #[0, 3, 5], #[0, 4, 6, 8], #[0, 5, 8], #[1, 2], #[5, 6]] },
    eqR := [(0, 0), (7, 5)], eqI := [(3, 0), (8, 5)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 4, 0, 7, 8, 9, 10, 11, 12, 4, 13, 14, 15, 16, 17, 18] },
  { name := "f7_.557565_.5..8..", src := "loop/k47/r63o_kills_cf.cfast", X := "I0-I3,I5-I8,R0-I0,R2-I5",
    cf := {
      name := "f7_.557565_.5..8..", r := 14, m := 9,
      ringAdj := #[#[0], #[0, 13], #[11], #[8, 9, 10, 11], #[8], #[2, 3], #[0, 1, 2], #[11, 12, 13], #[3, 4, 5, 6, 7, 8]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 7], #[0, 1, 3, 7], #[0, 2, 4], #[0, 3, 5, 8], #[0, 4, 6, 8], #[0, 5], #[1, 2], #[4, 5]] },
    eqR := [(0, 0), (2, 5)], eqI := [(3, 0), (8, 5)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 4, 0, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] },
  { name := "f7_.557565_.5.68..", src := "loop/k47/r63o_kills_cf.cfast", X := "I0-I3,I5-I9,R0-I0,R2-I5",
    cf := {
      name := "f7_.557565_.5.68..", r := 14, m := 10,
      ringAdj := #[#[0], #[0, 13], #[11], #[9, 10, 11], #[], #[2, 3], #[0, 1, 2], #[11, 12, 13], #[7, 8, 9], #[3, 4, 5, 6, 7]],
      intAdj := #[#[1, 2, 3, 4, 5, 6], #[0, 2, 7], #[0, 1, 3, 7], #[0, 2, 4, 8], #[0, 3, 5, 8, 9], #[0, 4, 6, 9], #[0, 5], #[1, 2], #[3, 4, 9], #[4, 5, 8]] },
    eqR := [(0, 0), (2, 5)], eqI := [(3, 0), (9, 5)],
    lbl := [0, 1, 2, 0, 3, 4, 5, 6, 7, 4, 0, 8, 4, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19] }]

def k63oReport : List (String × Bool × Bool × Bool) :=
  k63oEntries.map (fun d => (d.name, admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl, foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl, d.ok))

theorem k63oEntries_length : k63oEntries.length = 3 := by
  native_decide

theorem k63o_foldSafe_all : k63oEntries.all (fun d => foldSafeX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k63o_admissible_all : k63oEntries.all (fun d => admissibleX (Conf.of18 d.cf) d.eqR d.eqI d.lbl) = true := by
  native_decide

theorem k63o_ok_all : k63oEntries.all XRData.ok = true := by
  native_decide

end SimpleGraph.SphericalMap.CGlue

#eval SimpleGraph.SphericalMap.CGlue.k63oReport
#print axioms SimpleGraph.SphericalMap.CGlue.k63o_foldSafe_all
#print axioms SimpleGraph.SphericalMap.CGlue.k63o_admissible_all
#print axioms SimpleGraph.SphericalMap.CGlue.k63o_ok_all
