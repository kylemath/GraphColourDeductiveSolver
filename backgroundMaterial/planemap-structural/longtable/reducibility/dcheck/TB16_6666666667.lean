import DCheck16
/-! Studio Job 13 (exploratory): native_decide certificate for the ring-16 66666 2-ball 6666666667, one of the two
configurations B8's discharging certificate rests on.  DCheck16 = DCheck with the matching table extended to p <= 8. -/
namespace DCheck16

def cfg_6666666667 : Conf := { name := "6666666667", r := 16, m := 16, ringAdj := #[#[], #[], #[], #[], #[], #[], #[15, 0, 1], #[1, 2], #[2, 3, 4], #[4, 5], #[5, 6, 7], #[7, 8], #[8, 9, 10], #[10, 11], #[11, 12, 13], #[13, 14, 15]], intAdj := #[#[1, 2, 3, 4, 5], #[0, 2, 5, 6, 7, 15], #[0, 1, 3, 7, 8, 9], #[0, 2, 4, 9, 10, 11], #[0, 3, 5, 11, 12, 13], #[0, 1, 4, 13, 14, 15], #[1, 7, 15], #[1, 2, 6, 8], #[2, 7, 9], #[2, 3, 8, 10], #[3, 9, 11], #[3, 4, 10, 12], #[4, 11, 13], #[4, 5, 12, 14], #[5, 13, 15], #[1, 5, 6, 14]] }
theorem tb16_6666666667 : run cfg_6666666667 = { classes := 1793614, ext := 279380, reached := 1793614, depth := 3 } := by
  native_decide
theorem tb16_6666666667_dred : dReducible cfg_6666666667 = true := by
  simp [dReducible, tb16_6666666667]

end DCheck16

#print axioms DCheck16.tb16_6666666667
#print axioms DCheck16.tb16_6666666667_dred
