import Mathlib.Data.Fintype.Sum
import DCheckS1

/-! Job 19 pieces (B) and (D): ring codes of colour sequences, and `canon` as a colour renaming. -/
namespace DCheck.R2

/-- The ring code of the colour sequence `f` on positions `0..i-1` (2 bits per position). -/
def code (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | t + 1 => code f t ||| (f t <<< (2 * t))

theorem code_high (f : Nat → Nat) (hf : ∀ t, f t < 4) :
    ∀ i j, 2 * i ≤ j → (code f i).testBit j = false := by
  intro i
  induction i with
  | zero => intro j _; simp [code]
  | succ i ih => intro j hj; exact S1.or_high _ _ _ (hf i) ih j hj

theorem col_code (f : Nat → Nat) (hf : ∀ t, f t < 4) :
    ∀ i t, t < i → col (code f i) t = f t := by
  intro i
  induction i with
  | zero => intro t h; omega
  | succ i ih =>
    intro t ht
    show col (code f i ||| (f i <<< (2 * i))) t = f t
    by_cases h : t < i
    · rw [S1.col_or_low _ _ _ _ h, ih t h]
    · rw [show t = i by omega, S1.col_or_top _ _ _ (hf i) (code_high f hf i)]

theorem code_lt (f : Nat → Nat) (hf : ∀ t, f t < 4) (i : Nat) : code f i < 4 ^ i := by
  rw [show (4 : Nat) ^ i = 2 ^ (2 * i) by rw [Nat.pow_mul]]
  exact Nat.lt_pow_two_of_testBit _ (fun j hj => code_high f hf i j hj)

theorem testBit_col (x j : Nat) : x.testBit j = (col x (j / 2)).testBit (j % 2) := by
  unfold col
  rw [show (4 : Nat) = 2 ^ 2 from rfl, Nat.testBit_mod_two_pow, Nat.testBit_shiftRight]
  have : j % 2 < 2 := Nat.mod_lt _ (by decide)
  simp only [this, decide_true, Bool.true_and]
  congr 1; omega

/-- Two codes agreeing on the colours of positions `< i` and vanishing above are equal. -/
theorem code_ext (a b i : Nat) (ha : ∀ j, 2 * i ≤ j → a.testBit j = false)
    (hb : ∀ j, 2 * i ≤ j → b.testBit j = false) (h : ∀ t, t < i → col a t = col b t) : a = b := by
  apply Nat.eq_of_testBit_eq
  intro j
  by_cases hj : 2 * i ≤ j
  · rw [ha j hj, hb j hj]
  · rw [testBit_col a j, testBit_col b j, h (j / 2) (by omega)]

/-- **(D)** `canon` renames the colours of a code by an injective map on the colours that occur. -/
theorem canon_rename (r : Nat) (f : Nat → Nat) (hf : ∀ t, f t < 4) :
    ∃ g : Fin 4 → Fin 4, Function.Injective g ∧
      canon r (code f r) = code (fun t => (g ⟨f t % 4, Nat.mod_lt _ (by decide)⟩).val) r := by
  classical
  have hI := S1.cinv (code f r) r
  obtain ⟨hsz, hval, hinj, hseen, hcnt, hhigh, hcol⟩ := hI
  set mp := (S1.cst (code f r) r).1 with hmp
  -- the seen colours and their images
  let s : Set (Fin 4) := {a | mp[a.val]! ≠ 4}
  let F : Fin 4 → Nat := fun a => mp[a.val]!
  have hnxt : (S1.cst (code f r) r).2.1 ≤ 4 := by omega
  have hmaps : s.MapsTo F (Finset.range 4 : Finset Nat) := by
    intro a ha
    simp only [Finset.coe_range, Set.mem_Iio]
    exact lt_of_lt_of_le (hval a.val a.isLt ha) hnxt
  have hinjOn : Set.InjOn F s := by
    intro a ha b _ hab
    exact Fin.ext (hinj a.val b.val a.isLt b.isLt ha hab)
  obtain ⟨e, he⟩ := hmaps.exists_equiv_extend_of_card_eq (by simp) hinjOn
  let g : Fin 4 → Fin 4 := fun a => ⟨(e a : Nat), Finset.mem_range.1 (e a).2⟩
  refine ⟨g, ?_, ?_⟩
  · intro a b hab
    apply e.injective
    apply Subtype.ext
    have := congrArg Fin.val hab
    simpa [g] using this
  · have hg : ∀ t, t < r → (g ⟨f t % 4, Nat.mod_lt _ (by decide)⟩).val = mp[col (code f r) t]! := by
      intro t ht
      have hct : col (code f r) t = f t := col_code f hf r t ht
      have hs : (⟨f t % 4, Nat.mod_lt _ (by decide)⟩ : Fin 4) ∈ s := by
        show mp[f t % 4]! ≠ 4
        rw [Nat.mod_eq_of_lt (hf t), ← hct]; exact hseen t ht
      show ((e _ : Nat)) = _
      rw [he _ hs]
      show mp[f t % 4]! = _
      rw [Nat.mod_eq_of_lt (hf t), hct]
    have hgf : ∀ t, (g ⟨f t % 4, Nat.mod_lt _ (by decide)⟩).val < 4 := fun t => (g _).isLt
    rw [S1.canon_eq]
    apply code_ext _ _ r hhigh (code_high _ hgf r)
    intro t ht
    rw [hcol t ht, col_code _ hgf r t ht, hg t ht]

end DCheck.R2

#print axioms DCheck.R2.canon_rename
#print axioms DCheck.R2.col_code
#print axioms DCheck.R2.code_lt
