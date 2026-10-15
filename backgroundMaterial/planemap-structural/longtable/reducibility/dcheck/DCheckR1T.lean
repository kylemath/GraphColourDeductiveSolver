import DCheckR1
import DCheckT
/-! Job 23: R1 for the parametrised table `matchTableN N`, `N ≤ 10` (p ≤ 9). Adds the per-p check
`check9 : checkP 18 = true` (`native_decide`, same trust as `check4..8`). -/
namespace DCheck.R1

theorem check9 : checkP 18 = true := by native_decide

theorem checks9 (p : Nat) (hp : p ≤ 9) : checkP (2 * p) = true := by
  by_cases h : p ≤ 8
  · exact checks p h
  · rw [show p = 9 by omega]; exact check9

theorem matchTableN_get (N p : Nat) (hp : p < N) :
    (matchTableN N)[p]! = ((ncm (2 * p) (List.range (2 * p))).map (arcRegions (2 * p))).toArray := by
  unfold matchTableN
  rw [getElem!_pos _ p (by simp; omega)]
  simp [Array.getElem_map, Array.getElem_range]

/-- **R1 for `matchTableN N`** (`N ≤ 10`, `p < N`). -/
theorem matchTableN_complete (N : Nat) (hN : N ≤ 10) (p : Nat) (hp : p < N) (μ : Nat → Nat)
    (hμ : S3.IsNCPM (2 * p) μ) :
    ∃ lab ∈ (matchTableN N)[p]!, ∀ j j', j < 2 * p → j' < 2 * p →
      (lab[j]! = lab[j']! ↔ S3.sameFace (2 * p) μ j j') := by
  obtain ⟨M, hM, h⟩ := covers_of_check p (checks9 p (by omega)) μ hμ
  refine ⟨arcRegions (2 * p) M, ?_, h⟩
  rw [matchTableN_get N p hp, List.mem_toArray, List.mem_map]
  exact ⟨M, hM, rfl⟩

end DCheck.R1

#print axioms DCheck.R1.matchTableN_complete
