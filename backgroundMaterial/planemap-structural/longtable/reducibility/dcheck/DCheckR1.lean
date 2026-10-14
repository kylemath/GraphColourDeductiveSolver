import DCheck
import DCheckS3
import DCheck16
/-!
# DCheckR1: `ncm` is complete (item B3, R1, exploratory)

`ncm_complete`: for any non-crossing fixed-point-free involution `μ` of a sorted point list,
`ncm` lists a matching whose pairs are exactly the chords of `μ`. General proof, no `decide`.
-/
namespace DCheck.R1

variable (μ : Nat → Nat)

theorem even_of_invol : ∀ m (L : List Nat), L.length ≤ m → L.Nodup →
    (∀ x ∈ L, μ x ∈ L ∧ μ x ≠ x ∧ μ (μ x) = x) → L.length % 2 = 0 := by
  intro m
  induction m with
  | zero => intro L hL _ _; simp_all
  | succ m ih =>
    intro L hL hnd hinv
    match L, hL, hnd, hinv with
    | [], _, _, _ => rfl
    | x :: L', hL, hnd, hinv =>
      have hx := hinv x (by simp)
      have hnd' : L'.Nodup := (List.nodup_cons.1 hnd).2
      have hxL' : x ∉ L' := (List.nodup_cons.1 hnd).1
      have hmx : μ x ∈ L' := by
        rcases List.mem_cons.1 hx.1 with h | h
        · exact absurd h hx.2.1
        · exact h
      have hlen := List.length_erase_of_mem hmx
      have := ih (L'.erase (μ x)) (by simp at hL; omega) (hnd'.erase _) (by
        intro y hy
        rw [hnd'.mem_erase_iff] at hy
        obtain ⟨hyx, hy⟩ := hy
        have hyy := hinv y (by simp [hy])
        refine ⟨?_, hyy.2.1, hyy.2.2⟩
        rw [hnd'.mem_erase_iff]
        have h1 : μ y ≠ x := fun h => hyx (by rw [← hyy.2.2, h])
        refine ⟨fun h => ?_, ?_⟩
        · have : y = x := by rw [← hyy.2.2, h, hx.2.2]
          exact hxL' (this ▸ hy)
        · rcases List.mem_cons.1 hyy.1 with h | h
          · exact absurd h h1
          · exact h)
      simp only [List.length_cons]
      have : L'.length ≥ 1 := List.length_pos_of_mem hmx
      omega

/-- Membership in `ncm` for a non-empty list. -/
theorem mem_ncm_cons (f a : Nat) (rest : List Nat) (M : List (Nat × Nat)) :
    M ∈ ncm (f + 1) (a :: rest) ↔ ∃ j, j < rest.length ∧ j % 2 = 0 ∧
      ∃ m1 ∈ ncm f (rest.take j), ∃ m2 ∈ ncm f (rest.drop (j + 1)),
        M = (a, rest[j]!) :: m1 ++ m2 := by
  simp only [ncm, List.mem_flatMap, List.mem_range]
  constructor
  · rintro ⟨j, hj, hM⟩
    split at hM
    · rename_i h
      simp only [List.mem_flatMap, List.mem_map] at hM
      obtain ⟨m1, h1, m2, h2, rfl⟩ := hM
      exact ⟨j, hj, by simpa using h, m1, h1, m2, h2, rfl⟩
    · simp at hM
  · rintro ⟨j, hj, he, m1, h1, m2, h2, rfl⟩
    refine ⟨j, hj, ?_⟩
    rw [ite_eq_left (by simpa using he)]
    simp only [List.mem_flatMap, List.mem_map]
    exact ⟨m1, h1, m2, h2, rfl⟩

/-- **Completeness of `ncm`.** -/
theorem ncm_complete (n : Nat)
    (hNC : ∀ a b x d, a < b → b < x → x < d → d < n → μ a = x → μ b = d → False) :
    ∀ f (pts : List Nat), pts.length ≤ f → pts.Pairwise (· < ·) → (∀ x ∈ pts, x < n) →
      (∀ x ∈ pts, μ x ∈ pts ∧ μ x ≠ x ∧ μ (μ x) = x) →
      ∃ M ∈ ncm f pts, (∀ s t, (s, t) ∈ M → s ∈ pts ∧ s < t ∧ μ s = t) ∧
        (∀ x ∈ pts, ∃ s t, (s, t) ∈ M ∧ (x = s ∨ x = t)) := by
  intro f
  induction f with
  | zero =>
    intro pts hl _ _ _
    match pts, hl with
    | [], _ => exact ⟨[], by simp [ncm], by simp, by simp⟩
  | succ f ih =>
    intro pts hl hsort hlt hinv
    match pts, hl, hsort, hlt, hinv with
    | [], _, _, _, _ => exact ⟨[], by simp [ncm], by simp, by simp⟩
    | a :: rest, hl, hsort, hlt, hinv =>
      rw [List.pairwise_cons] at hsort
      obtain ⟨hamin, hsort⟩ := hsort
      have ha := hinv a (by simp)
      have hb : μ a ∈ rest := by
        rcases List.mem_cons.1 ha.1 with h | h
        · exact absurd h ha.2.1
        · exact h
      obtain ⟨j, hj, hjb⟩ := List.mem_iff_getElem.1 hb
      have hmono := List.pairwise_iff_getElem.1 hsort
      -- index/value correspondence in the sorted `rest`
      have hidx : ∀ i (hi : i < rest.length), (rest[i] < rest[j] ↔ i < j) := by
        intro i hi
        constructor
        · intro h
          refine Classical.byContradiction fun hn => ?_
          by_cases hij : i = j
          · subst hij; omega
          · have := hmono j i hj hi (by omega); omega
        · intro h; exact hmono i j hi hj h
      have hall : ∀ x ∈ a :: rest, a ≤ x := by
        intro x hx
        rcases List.mem_cons.1 hx with h | h
        · omega
        · exact Nat.le_of_lt (hamin x h)
      have hmem_take : ∀ x, x ∈ rest.take j ↔ x ∈ rest ∧ x < μ a := by
        intro x
        rw [List.mem_take_iff_getElem, List.mem_iff_getElem]
        constructor
        · rintro ⟨i, hi, rfl⟩
          have hi' : i < rest.length := by omega
          have hij : i < j := by omega
          exact ⟨⟨i, hi', rfl⟩, by rw [← hjb]; exact (hidx i hi').2 hij⟩
        · rintro ⟨⟨i, hi, rfl⟩, hx⟩
          rw [← hjb] at hx
          exact ⟨i, by have := (hidx i hi).1 hx; omega, rfl⟩
      have hmem_drop : ∀ x, x ∈ rest.drop (j + 1) ↔ x ∈ rest ∧ μ a < x := by
        intro x
        rw [List.mem_drop_iff_getElem, List.mem_iff_getElem]
        constructor
        · rintro ⟨i, hi, rfl⟩
          have hi' : j + 1 + i < rest.length := by omega
          exact ⟨⟨_, hi', rfl⟩, by rw [← hjb]; exact hmono j _ hj hi' (by omega)⟩
        · rintro ⟨⟨i, hi, rfl⟩, hx⟩
          rw [← hjb] at hx
          have hji : j < i := by
            refine Classical.byContradiction fun hn => ?_
            by_cases hij : i = j
            · subst hij; omega
            · have := (hidx i hi).2 (by omega); omega
          exact ⟨i - (j + 1), by omega, by congr 1; omega⟩
      -- closure of the inside and the outside of the chord `(a, μ a)`
      have hin : ∀ x ∈ rest.take j, μ x ∈ rest.take j ∧ μ x ≠ x ∧ μ (μ x) = x := by
        intro x hx
        rw [hmem_take] at hx
        have hxx := hinv x (by simp [hx.1])
        refine ⟨?_, hxx.2⟩
        rw [hmem_take]
        have h1 : μ x ≠ a := fun h => by
          have : x = μ a := by rw [← hxx.2.2, h]
          omega
        have h2 : μ x ≠ μ a := fun h => by
          have : x = a := by rw [← hxx.2.2, h, ha.2.2]
          have := hamin x hx.1; omega
        have h3 := hall _ hxx.1
        have hxa := hamin x hx.1
        rcases List.mem_cons.1 hxx.1 with h | h
        · exact absurd h h1
        · refine ⟨h, ?_⟩
          refine Classical.byContradiction fun hn => ?_
          exact hNC a x (μ a) (μ x) hxa hx.2 (by omega) (hlt _ (by simp [h])) rfl rfl
      have hout : ∀ x ∈ rest.drop (j + 1), μ x ∈ rest.drop (j + 1) ∧ μ x ≠ x ∧ μ (μ x) = x := by
        intro x hx
        rw [hmem_drop] at hx
        have hxx := hinv x (by simp [hx.1])
        refine ⟨?_, hxx.2⟩
        rw [hmem_drop]
        have h1 : μ x ≠ a := fun h => by
          have : x = μ a := by rw [← hxx.2.2, h]
          omega
        have h2 : μ x ≠ μ a := fun h => by
          have : x = a := by rw [← hxx.2.2, h, ha.2.2]
          have := hamin x hx.1; omega
        rcases List.mem_cons.1 hxx.1 with h | h
        · exact absurd h h1
        · refine ⟨h, ?_⟩
          refine Classical.byContradiction fun hn => ?_
          have hma := hamin _ h
          exact hNC a (μ x) (μ a) x hma (by omega) hx.2 (hlt _ (by simp [hx.1])) rfl hxx.2.2
      -- parity of the inside
      have hnd : rest.Nodup := List.nodup_iff_pairwise_ne.2 (hsort.imp fun h => Nat.ne_of_lt h)
      have heven := even_of_invol μ _ (rest.take j) (Nat.le_refl _)
        (hnd.sublist (List.take_sublist _ _)) hin
      rw [List.length_take, Nat.min_eq_left (by omega)] at heven
      -- recursion
      have hrl : rest.length ≤ f := by simp at hl; omega
      obtain ⟨m1, hm1, hp1, hc1⟩ := ih (rest.take j) (by simp; omega)
        (hsort.sublist (List.take_sublist _ _))
        (fun x hx => hlt x (by simp [List.mem_of_mem_take hx])) hin
      obtain ⟨m2, hm2, hp2, hc2⟩ := ih (rest.drop (j + 1)) (by simp; omega)
        (hsort.sublist (List.drop_sublist _ _))
        (fun x hx => hlt x (by simp [List.mem_of_mem_drop hx])) hout
      have hrj : rest[j]! = μ a := by
        rw [List.getElem!_eq_getElem?_getD, List.getElem?_eq_getElem hj]; simpa using hjb
      refine ⟨(a, rest[j]!) :: m1 ++ m2, (mem_ncm_cons f a rest _).2
        ⟨j, hj, heven, m1, hm1, m2, hm2, rfl⟩, ?_, ?_⟩
      · intro s t hst
        rw [List.cons_append, List.mem_cons, List.mem_append] at hst
        rcases hst with h | h | h
        · cases h; rw [hrj]; exact ⟨by simp, hamin _ hb, rfl⟩
        · have := hp1 s t h
          exact ⟨List.mem_cons_of_mem _ (List.mem_of_mem_take this.1), this.2⟩
        · have := hp2 s t h
          exact ⟨List.mem_cons_of_mem _ (List.mem_of_mem_drop this.1), this.2⟩
      · intro x hx
        rcases List.mem_cons.1 hx with h | h
        · exact ⟨a, rest[j]!, by simp, Or.inl h⟩
        · by_cases h1 : x = μ a
          · exact ⟨a, rest[j]!, by simp, Or.inr (by rw [hrj]; exact h1)⟩
          · by_cases h2 : x < μ a
            · obtain ⟨s, t, hst, hx'⟩ := hc1 x ((hmem_take x).2 ⟨h, h2⟩)
              exact ⟨s, t, by simp [hst], hx'⟩
            · obtain ⟨s, t, hst, hx'⟩ := hc2 x ((hmem_drop x).2 ⟨h, by omega⟩)
              exact ⟨s, t, by simp [hst], hx'⟩

/-! ## Faces of a matching given as a list of chords -/

def sameFaceB (M : List (Nat × Nat)) (j j' : Nat) : Bool :=
  M.all fun st => decide (st.1 ≤ j ∧ j < st.2) == decide (st.1 ≤ j' ∧ j' < st.2)

theorem sameFaceB_iff (M : List (Nat × Nat)) (j j' : Nat) :
    sameFaceB M j j' = true ↔ ∀ s t, (s, t) ∈ M → (s ≤ j ∧ j < t ↔ s ≤ j' ∧ j' < t) := by
  unfold sameFaceB
  rw [List.all_eq_true]
  constructor
  · intro h s t hst
    have := h (s, t) hst
    simp only [beq_iff_eq, decide_eq_decide] at this
    exact this
  · intro h st hst
    have := h st.1 st.2 hst
    simp only [beq_iff_eq, decide_eq_decide]
    exact this

/-- The ncm-matching of `μ` has the same faces as `μ`. -/
theorem sameFace_iff (n : Nat) (μ : Nat → Nat) (hμ : S3.IsNCPM n μ) (M : List (Nat × Nat))
    (hp : ∀ s t, (s, t) ∈ M → s ∈ List.range n ∧ s < t ∧ μ s = t)
    (hc : ∀ x ∈ List.range n, ∃ s t, (s, t) ∈ M ∧ (x = s ∨ x = t)) (j j' : Nat) :
    S3.sameFace n μ j j' ↔ sameFaceB M j j' = true := by
  rw [sameFaceB_iff]
  constructor
  · intro h s t hst
    obtain ⟨hs, hst', hμs⟩ := hp s t hst
    have := h s (List.mem_range.1 hs) (by omega)
    rwa [hμs] at this
  · intro h a ha hlt
    obtain ⟨s, t, hst, hx⟩ := hc a (List.mem_range.2 ha)
    obtain ⟨hs, hst', hμs⟩ := hp s t hst
    rcases hx with rfl | rfl
    · rw [hμs]; exact h _ _ hst
    · have := (hμ.1 s (List.mem_range.1 hs)).2.2
      rw [hμs] at this; omega

/-! ## The finite check: `arcRegions` labels exactly the faces (per `n = 2p ≤ 16`) -/

/-- For every matching listed by `ncm`, `arcRegions` gives equal labels exactly to arcs in one
face. -/
def checkP (n : Nat) : Bool :=
  (ncm n (List.range n)).all fun M =>
    (List.range n).all fun j => (List.range n).all fun j' =>
      ((arcRegions n M)[j]! == (arcRegions n M)[j']!) == sameFaceB M j j'

theorem checkP_sound (n : Nat) (h : checkP n = true) (M : List (Nat × Nat))
    (hM : M ∈ ncm n (List.range n)) (j j' : Nat) (hj : j < n) (hj' : j' < n) :
    (arcRegions n M)[j]! = (arcRegions n M)[j']! ↔ sameFaceB M j j' = true := by
  unfold checkP at h
  rw [List.all_eq_true] at h
  have := h M hM
  rw [List.all_eq_true] at this
  have := this j (List.mem_range.2 hj)
  rw [List.all_eq_true] at this
  have := this j' (List.mem_range.2 hj')
  revert this
  generalize (arcRegions n M)[j]! = x
  generalize (arcRegions n M)[j']! = y
  cases sameFaceB M j j' <;> by_cases hxy : x = y <;> simp [hxy]

/-! Per-`p` instances of the finite check. `p ≤ 3`: kernel `decide` (standard axioms only).
`p = 4..8`: `native_decide` (one `…._native.native_decide.ax_*` axiom each, the same trust as the
checker's own certificates); kernel `decide` already takes about 28 s at `p = 3` and would grow by
roughly 2500× to `p = 7`. -/
theorem check0 : checkP 0 = true := by decide
theorem check1 : checkP 2 = true := by decide +kernel
theorem check2 : checkP 4 = true := by decide +kernel
theorem check3 : checkP 6 = true := by decide +kernel
theorem check4 : checkP 8 = true := by native_decide
theorem check5 : checkP 10 = true := by native_decide
theorem check6 : checkP 12 = true := by native_decide
theorem check7 : checkP 14 = true := by native_decide
theorem check8 : checkP 16 = true := by native_decide

theorem checks (p : Nat) (hp : p ≤ 8) : checkP (2 * p) = true := by
  match p, hp with
  | 0, _ => exact check0
  | 1, _ => exact check1
  | 2, _ => exact check2
  | 3, _ => exact check3
  | 4, _ => exact check4
  | 5, _ => exact check5
  | 6, _ => exact check6
  | 7, _ => exact check7
  | 8, _ => exact check8

/-- General part: any NC perfect matching of `0..2p-1` is realised by some `M ∈ ncm` whose
`arcRegions` classes are exactly its faces, provided `checkP (2p)`. -/
theorem covers_of_check (p : Nat) (hck : checkP (2 * p) = true) (μ : Nat → Nat)
    (hμ : S3.IsNCPM (2 * p) μ) :
    ∃ M ∈ ncm (2 * p) (List.range (2 * p)), ∀ j j', j < 2 * p → j' < 2 * p →
      ((arcRegions (2 * p) M)[j]! = (arcRegions (2 * p) M)[j']! ↔
        S3.sameFace (2 * p) μ j j') := by
  obtain ⟨M, hM, hpairs, hcov⟩ := ncm_complete μ (2 * p) hμ.2 (2 * p) (List.range (2 * p))
    (by simp) List.pairwise_lt_range (fun x hx => List.mem_range.1 hx)
    (fun x hx => by
      have := hμ.1 x (List.mem_range.1 hx)
      exact ⟨List.mem_range.2 this.1, this.2⟩)
  refine ⟨M, hM, fun j j' hj hj' => ?_⟩
  rw [checkP_sound _ hck M hM j j' hj hj', sameFace_iff (2 * p) μ hμ M hpairs hcov]

theorem matchTable_get (p : Nat) (hp : p < 8) :
    matchTable[p]! = ((ncm (2 * p) (List.range (2 * p))).map (arcRegions (2 * p))).toArray := by
  unfold matchTable
  rw [getElem!_pos _ p (by simp; omega)]
  simp [Array.getElem_map, Array.getElem_range]

/-- **R1 for `DCheck` (`p ≤ 7`).** For every non-crossing perfect matching `μ` of the `2p`
transitions, `matchTable[p]` contains a labelling whose classes are exactly the faces of `μ`. -/
theorem matchTable_complete (p : Nat) (hp : p ≤ 7) (μ : Nat → Nat) (hμ : S3.IsNCPM (2 * p) μ) :
    ∃ lab ∈ matchTable[p]!, ∀ j j', j < 2 * p → j' < 2 * p →
      (lab[j]! = lab[j']! ↔ S3.sameFace (2 * p) μ j j') := by
  obtain ⟨M, hM, h⟩ := covers_of_check p (checks p (by omega)) μ hμ
  refine ⟨arcRegions (2 * p) M, ?_, h⟩
  rw [matchTable_get p (by omega), List.mem_toArray, List.mem_map]
  exact ⟨M, hM, rfl⟩

/-! ## The same for `DCheck16` (`p ≤ 8`) -/

theorem ncm16_eq : ∀ f pts, DCheck16.ncm f pts = DCheck.ncm f pts := by
  intro f
  induction f with
  | zero => intro pts; cases pts <;> rfl
  | succ f ih => intro pts; cases pts <;> simp [DCheck16.ncm, DCheck.ncm, ih]

theorem arcRegions16_eq : DCheck16.arcRegions = DCheck.arcRegions := rfl

theorem matchTable16_get (p : Nat) (hp : p < 9) :
    DCheck16.matchTable[p]! =
      ((ncm (2 * p) (List.range (2 * p))).map (arcRegions (2 * p))).toArray := by
  unfold DCheck16.matchTable
  rw [getElem!_pos _ p (by simp; omega)]
  simp [Array.getElem_map, Array.getElem_range, ncm16_eq, arcRegions16_eq]

/-- **R1 for `DCheck16` (`p ≤ 8`).** -/
theorem matchTable16_complete (p : Nat) (hp : p ≤ 8) (μ : Nat → Nat)
    (hμ : S3.IsNCPM (2 * p) μ) :
    ∃ lab ∈ DCheck16.matchTable[p]!, ∀ j j', j < 2 * p → j' < 2 * p →
      (lab[j]! = lab[j']! ↔ S3.sameFace (2 * p) μ j j') := by
  obtain ⟨M, hM, h⟩ := covers_of_check p (checks p hp) μ hμ
  refine ⟨arcRegions (2 * p) M, ?_, h⟩
  rw [matchTable16_get p (by omega), List.mem_toArray, List.mem_map]
  exact ⟨M, hM, rfl⟩

end DCheck.R1

#print axioms DCheck.R1.ncm_complete
#print axioms DCheck.R1.covers_of_check
#print axioms DCheck.R1.matchTable_complete
#print axioms DCheck.R1.matchTable16_complete
