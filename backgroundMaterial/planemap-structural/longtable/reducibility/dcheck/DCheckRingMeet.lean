import DCheckT
import DCheckSound
/-! Job 25 step 4 (computational core): two Kempe-closed sets of ring-colouring classes that both
satisfy the "smaller map" facts must share a class.
* r = 4: each set has a class with `col 0 ≠ col 2` and one with `col 1 ≠ col 3` (both chords);
* r = 5: each set has a class missing a colour (star) and, for every `v`, a class with
  `col v ≠ col (v+2)` and `col v ≠ col (v+3)` (the fan at `v`).
Classes are the canonical codes `ringColourings r`; a set is a predicate `g : Fin K → Bool` on them.
`native_decide` (same trust as the checker certificates). -/
namespace DCheck.Meet
open DCheck

/-- Membership of a code in the class set `g`. -/
def mem (r : Nat) (K : Nat) (g : Fin K → Bool) (x : Nat) : Bool :=
  (List.finRange K).any fun i => (ringColourings r)[i.val]! == x && g i

/-- Kempe closure of a class set, with the matching table `matchTableN 3` (p ≤ 2, rings ≤ 5). -/
def closedB (r K : Nat) (g : Fin K → Bool) : Bool :=
  (List.finRange K).all fun i =>
    let k := (ringColourings r)[i.val]!
    !g i || [1, 2, 3].all fun th =>
      let T := transitions r k th
      T.size == 0 || ((matchTableN 3)[T.size / 2]!).any fun lab =>
        (List.range (2 ^ (T.size / 2))).all fun s => mem r K g (canon r (k ^^^ flipMask r k th lab s))

def has (r K : Nat) (g : Fin K → Bool) (P : Nat → Bool) : Bool :=
  (List.finRange K).any fun i => g i && P (ringColourings r)[i.val]!

def facts4 (g : Fin 4 → Bool) : Bool :=
  has 4 4 g (fun k => col k 0 != col k 2) && has 4 4 g (fun k => col k 1 != col k 3)

def facts5 (g : Fin 10 → Bool) : Bool :=
  has 5 10 g (fun k => (List.range 4).any fun x => (List.range 5).all fun t => col k t != x) &&
  (List.range 5).all fun v =>
    has 5 10 g (fun k => col k v != col k ((v + 2) % 5) && col k v != col k ((v + 3) % 5))

theorem size4 : (ringColourings 4).size = 4 := by native_decide
theorem size5 : (ringColourings 5).size = 10 := by native_decide

/-- A class set as a bit mask. -/
def gOf (K m : Nat) : Fin K → Bool := fun i => m.testBit i.val

/-- The finite checks, over all pairs of masks. -/
def check4 : Bool := (List.range 16).all fun mA => (List.range 16).all fun mB =>
  !(closedB 4 4 (gOf 4 mA) && facts4 (gOf 4 mA) && closedB 4 4 (gOf 4 mB) && facts4 (gOf 4 mB)) ||
    (List.finRange 4).any fun i => gOf 4 mA i && gOf 4 mB i

/-- Ring 5: first the qualifying masks, then pairwise intersection. -/
def good5 : List Nat := (List.range 1024).filter fun m => closedB 5 10 (gOf 10 m) && facts5 (gOf 10 m)
def check5 : Bool := good5.all fun mA => good5.all fun mB =>
  (List.finRange 10).any fun i => gOf 10 mA i && gOf 10 mB i

theorem check4_true : check4 = true := by native_decide
theorem check5_true : check5 = true := by native_decide

/-- The mask of the first `K` values of `f`. -/
def maskOf (f : Nat → Bool) : Nat → Nat
  | 0 => 0
  | K + 1 => maskOf f K + (if f K then 2 ^ K else 0)

theorem maskOf_lt (f : Nat → Bool) : ∀ K, maskOf f K < 2 ^ K := by
  intro K
  induction K with
  | zero => simp [maskOf]
  | succ K ih =>
    simp only [maskOf]; split <;> rw [Nat.pow_succ] <;> omega

theorem maskOf_testBit (f : Nat → Bool) : ∀ K i, i < K → (maskOf f K).testBit i = f i := by
  intro K
  induction K with
  | zero => intro i h; omega
  | succ K ih =>
    intro i hi
    simp only [maskOf]
    have hlt := maskOf_lt f K
    by_cases hK : f K = true
    · rw [if_pos hK, Nat.add_comm]
      by_cases hiK : i = K
      · subst hiK; rw [Nat.testBit_two_pow_add_eq, Nat.testBit_lt_two_pow hlt, hK]; rfl
      · rw [Nat.testBit_two_pow_add_gt (by omega), ih i (by omega)]
    · rw [if_neg hK, Nat.add_zero]
      by_cases hiK : i = K
      · subst hiK; rw [Nat.testBit_lt_two_pow hlt]; simpa using hK
      · exact ih i (by omega)

theorem gOf_maskOf (K : Nat) (g : Fin K → Bool) :
    gOf K (maskOf (fun i => if h : i < K then g ⟨i, h⟩ else false) K) = g := by
  funext i
  unfold gOf
  rw [maskOf_testBit _ K i.val i.isLt, dif_pos i.isLt]

/-- **Ring 4**, for arbitrary class predicates. -/
theorem meet4 (gA gB : Fin 4 → Bool) (hA : closedB 4 4 gA = true) (fA : facts4 gA = true)
    (hB : closedB 4 4 gB = true) (fB : facts4 gB = true) : ∃ i, gA i = true ∧ gB i = true := by
  have h := check4_true
  unfold check4 at h
  rw [List.all_eq_true] at h
  have h1 := h _ (List.mem_range.2 (maskOf_lt (fun i => if h : i < 4 then gA ⟨i, h⟩ else false) 4))
  rw [List.all_eq_true] at h1
  have h2 := h1 _ (List.mem_range.2 (maskOf_lt (fun i => if h : i < 4 then gB ⟨i, h⟩ else false) 4))
  rw [gOf_maskOf, gOf_maskOf] at h2
  simp only [hA, fA, hB, fB, Bool.and_self, Bool.not_true, Bool.false_or, List.any_eq_true,
    Bool.and_eq_true] at h2
  obtain ⟨i, -, hi⟩ := h2
  exact ⟨i, hi⟩

/-- **Ring 5**, for arbitrary class predicates. -/
theorem meet5 (gA gB : Fin 10 → Bool) (hA : closedB 5 10 gA = true) (fA : facts5 gA = true)
    (hB : closedB 5 10 gB = true) (fB : facts5 gB = true) : ∃ i, gA i = true ∧ gB i = true := by
  have h := check5_true
  unfold check5 at h
  rw [List.all_eq_true] at h
  generalize hmA : maskOf (fun i => if h : i < 10 then gA ⟨i, h⟩ else false) 10 = mA
  generalize hmB : maskOf (fun i => if h : i < 10 then gB ⟨i, h⟩ else false) 10 = mB
  have gA' : gOf 10 mA = gA := hmA ▸ gOf_maskOf 10 gA
  have gB' : gOf 10 mB = gB := hmB ▸ gOf_maskOf 10 gB
  have ltA : mA < 2 ^ 10 := hmA ▸ maskOf_lt _ 10
  have ltB : mB < 2 ^ 10 := hmB ▸ maskOf_lt _ 10
  have memA : mA ∈ good5 := by
    unfold good5; rw [List.mem_filter, gA']
    exact ⟨List.mem_range.2 ltA, by simp [hA, fA]⟩
  have memB : mB ∈ good5 := by
    unfold good5; rw [List.mem_filter, gB']
    exact ⟨List.mem_range.2 ltB, by simp [hB, fB]⟩
  have h1 := h mA memA
  rw [List.all_eq_true] at h1
  have h2 := h1 mB memB
  rw [gA', gB'] at h2
  simp only [List.any_eq_true, Bool.and_eq_true] at h2
  obtain ⟨i, -, hi⟩ := h2
  exact ⟨i, hi⟩

end DCheck.Meet

#print axioms DCheck.Meet.meet4
#print axioms DCheck.Meet.meet5
