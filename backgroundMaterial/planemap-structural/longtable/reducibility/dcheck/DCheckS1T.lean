import DCheckS1
import DCheckRefT
import DCheckSoundT
/-! Job 23: (S1) loop correctness for `runT mt`, for any matching table `mt`. Mechanical copy of the
first part of `DCheckS1.lean` (`matchTable` → `mt`, `run`/`runRef`/`thLoop`/`iLoop` → their `T`
versions, `Good` → `GoodT mt`); the table-free lemmas are reused from `DCheck.S1`. -/
namespace DCheck.S1T
open DCheck.Ref DCheck.S1

variable {mt : Array (Array (Array Nat))}


/-! ## Generic loop lemmas (in `Id`) -/

/-- What a loop step must achieve: `P` after a `yield`, `Q` after a `done`. -/
def StepOK {β : Type} (P Q : β → Prop) : ForInStep β → Prop
  | .yield y => P y
  | .done y => Q y

theorem forIn_list_inv {β : Type} (l : List Nat) (a : Nat) (init : β)
    (f : Nat → β → Id (ForInStep β)) (I : Nat → β → Prop) (Q : β → Prop)
    (hl : l = List.range' a l.length) (h0 : I a init) (hend : ∀ x, I (a + l.length) x → Q x)
    (hstep : ∀ i x, a ≤ i → i < a + l.length → I i x → StepOK (I (i + 1)) Q (f i x)) :
    Q (forIn l init f) := by
  induction l generalizing a init with
  | nil => exact hend init (by simpa using h0)
  | cons c rest ih =>
    simp only [List.length_cons, List.range'_succ, List.cons.injEq] at hl
    obtain ⟨rfl, hl⟩ := hl
    have hs := hstep c init (Nat.le_refl _) (by simp) h0
    rw [List.forIn_cons]
    show Q (match (f c init : ForInStep β) with
      | .done b => (pure b : Id β) | .yield b => forIn rest b f)
    revert hs
    cases f c init with
    | done y => exact id
    | yield y =>
      intro hs
      exact ih (c + 1) y (by simpa using hl) hs
        (fun x hx => hend x (by simpa [Nat.add_assoc, Nat.add_comm 1] using hx))
        (fun i x h1 h2 hi => hstep i x (by omega) (by simp at h2 ⊢; omega) hi)

/-- Loop over `[a:b]` (step 1) with a position-indexed invariant. -/
theorem forIn_range_inv {β : Type} (a b : Nat) (init : β)
    (f : Nat → β → Id (ForInStep β)) (I : Nat → β → Prop) (Q : β → Prop)
    (h0 : I a init) (hend : ∀ x, I (max a b) x → Q x)
    (hstep : ∀ i x, a ≤ i → i < b → I i x → StepOK (I (i + 1)) Q (f i x)) :
    Q (forIn ([a:b] : Std.Legacy.Range) init f) := by
  rw [Std.Legacy.Range.forIn_eq_forIn_range']
  simp only [Std.Legacy.Range.size, Nat.add_sub_cancel, Nat.div_one]
  apply forIn_list_inv _ a init f I Q (by simp) h0
  · intro x hx; apply hend; simp at hx; rwa [show a + (b - a) = max a b by omega] at hx
  · intro i x h1 h2 hi; simp at h2; exact hstep i x h1 (by omega) hi

@[simp] theorem stepOK_yield {β : Type} (P Q : β → Prop) (y : β) :
    StepOK P Q (pure (ForInStep.yield y) : Id (ForInStep β)) ↔ P y := Iff.rfl
@[simp] theorem stepOK_done {β : Type} (P Q : β → Prop) (y : β) :
    StepOK P Q (pure (ForInStep.done y) : Id (ForInStep β)) ↔ Q y := Iff.rfl

/-- `forIn_range_inv` followed by a continuation `g` (the shape `do let s ← forIn …; g s`). -/
theorem forIn_range_bind {β γ : Type} (a b : Nat) (init : β)
    (f : Nat → β → Id (ForInStep β)) (g : β → Id γ) (I : Nat → β → Prop) (Q : γ → Prop)
    (h0 : I a init) (hend : ∀ x, I (max a b) x → Q (g x).run)
    (hstep : ∀ i x, a ≤ i → i < b → I i x → StepOK (I (i + 1)) (fun x => Q (g x).run) (f i x)) :
    Q (Id.run (forIn ([a:b] : Std.Legacy.Range) init f >>= g)) :=
  forIn_range_inv a b init f I (fun x => Q (g x).run) h0 hend hstep

/-- `while`-loop (in `Id`) with an invariant and a decreasing measure. -/
theorem loop_inv {β : Type} (init : β) (f : Unit → β → Id (ForInStep β))
    (I : β → Prop) (Q : β → Prop) (μ : β → Nat) (h0 : I init)
    (hstep : ∀ x, I x → StepOK (fun y => I y ∧ μ y < μ x) Q (f () x)) :
    Q (forIn Lean.Loop.mk init f) := by
  suffices ∀ n x, μ x < n → I x → Q (forIn Lean.Loop.mk x f) from this _ init (Nat.lt_succ_self _) h0
  intro n
  induction n with
  | zero => intro x h; omega
  | succ n ih =>
    intro x hx hI
    show Q (Lean.Loop.forIn _ x f)
    rw [Lean.Loop.forIn_eq_of_monadTail]
    have hs := hstep x hI
    revert hs
    show StepOK _ Q (f () x) → Q (match (f () x : ForInStep β) with
      | .done val => (pure val : Id β) | .yield val => Lean.Loop.forIn _ val f)
    cases f () x with
    | done y => exact id
    | yield y => intro hs; have h2 : μ y < μ x := hs.2; exact ih y (by omega) hs.1


/-- `loop_inv` followed by a continuation. -/
theorem loop_bind {β γ : Type} (init : β) (f : Unit → β → Id (ForInStep β)) (g : β → Id γ)
    (I : β → Prop) (Q : γ → Prop) (μ : β → Nat) (h0 : I init)
    (hstep : ∀ x, I x → StepOK (fun y => I y ∧ μ y < μ x) (fun x => Q (g x).run) (f () x)) :
    Q (Id.run (forIn Lean.Loop.mk init f >>= g)) :=
  loop_inv init f I (fun x => Q (g x).run) μ h0 hstep

/-! ## Small array / bit lemmas -/

theorem get_set! {α : Type} [Inhabited α] (a : Array α) (x y : Nat) (v : α) :
    (a.set! x v)[y]! = if x = y ∧ x < a.size then v else a[y]! := by
  rw [Array.set!_eq_setIfInBounds]
  by_cases hy : y < a.size
  · rw [getElem!_pos (a.setIfInBounds x v) y (by simpa using hy), getElem!_pos a y hy,
      Array.getElem_setIfInBounds (by simpa using hy)]
    by_cases h : x = y
    · subst h; simp [hy]
    · simp [h]
  · rw [getElem!_neg (a.setIfInBounds x v) y (by simpa using hy), getElem!_neg a y hy]
    split
    · omega
    · rfl

theorem testBit_shl_lt4 (th v j : Nat) (hth : th < 4) :
    (th <<< (2 * v)).testBit j = (decide (j / 2 = v) && th.testBit (j % 2)) := by
  rw [Nat.testBit_shiftLeft]
  by_cases h1 : j / 2 = v
  · have : j - 2 * v = j % 2 := by omega
    simp [h1, this]; omega
  · simp only [h1, decide_false, Bool.false_and]
    by_cases h2 : j ≥ 2 * v
    · have : th.testBit (j - 2 * v) = false :=
        Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le hth
          (by have := Nat.pow_le_pow_right (n := 2) (by omega) (show 2 ≤ j - 2 * v by omega); simpa using this))
      simp [this]
    · simp [h2]

theorem shr_mod_two (s b : Nat) : ((s >>> b) % 2 == 1) = s.testBit b := by
  have h := Nat.testBit_zero (s >>> b)
  rw [Nat.testBit_shiftRight, Nat.add_zero] at h
  by_cases h2 : (s >>> b) % 2 = 1 <;> simp_all

/-! ## The index map -/

theorem mkIndex_spec (ks : Array Nat) :
    ∀ x j : Nat, (mkIndex ks)[x]? = some j → ks[j]! = x := by
  unfold mkIndex
  refine forIn_range_bind 0 ks.size _ _ _
    (fun _ (idx : Std.HashMap Nat Nat) => ∀ x j : Nat, idx[x]? = some j → ks[j]! = x)
    (fun (idx : Std.HashMap Nat Nat) => ∀ x j : Nat, idx[x]? = some j → ks[j]! = x) ?_ ?_ ?_
  · intro x j h; simp at h
  · intro x hx; exact hx
  · intro i idx _ _ hI
    show ∀ x j, (idx.insert ks[i]! i)[x]? = some j → ks[j]! = x
    intro x j h
    rw [Std.HashMap.getElem?_insert] at h
    split at h
    · rename_i hx; cases h; simpa using hx
    · exact hI x j h

/-! ## Transitions -/

theorem mkT_eq (r k th : Nat) : mkT r k th = transitions r k th := by
  unfold mkT transitions
  refine forIn_range_bind 0 r _ _ _
    (fun v T => T = (Array.range v).filter fun v =>
      let x := col k v ^^^ col k ((v + 1) % r); x != 0 && x != th)
    (fun T => T = (Array.range r).filter fun v =>
      let x := col k v ^^^ col k ((v + 1) % r); x != 0 && x != th) ?_ ?_ ?_
  · rfl
  · intro x hx; simpa using hx
  · intro v T _ _ hT
    subst hT
    dsimp only
    split <;> simp only [stepOK_yield] <;> apply Array.ext' <;>
      simp_all [Array.toList_range, List.range_succ, List.filter_append]

/-! ## The region masks and the flipped code -/

theorem mkRm_spec (r n th : Nat) (arcOf lab : Array Nat) (hth : th < 4) :
    (mkRm r n th arcOf lab).size = n / 2 + 1 ∧
    ∀ g, g < n / 2 + 1 → ∀ j, (mkRm r n th arcOf lab)[g]!.testBit j =
      (decide (j / 2 < r) && decide (lab[arcOf[j / 2]!]! = g) && th.testBit (j % 2)) := by
  unfold mkRm
  refine forIn_range_bind 0 r _ _ _
    (fun v (rm : Array Nat) => rm.size = n / 2 + 1 ∧ ∀ g, g < n / 2 + 1 → ∀ j, rm[g]!.testBit j =
      (decide (j / 2 < v) && decide (lab[arcOf[j / 2]!]! = g) && th.testBit (j % 2)))
    (fun (rm : Array Nat) => rm.size = n / 2 + 1 ∧ ∀ g, g < n / 2 + 1 → ∀ j, rm[g]!.testBit j =
      (decide (j / 2 < r) && decide (lab[arcOf[j / 2]!]! = g) && th.testBit (j % 2))) ?_ ?_ ?_
  · refine ⟨by simp, fun g hg j => ?_⟩
    rw [getElem!_pos (Array.replicate (n / 2 + 1) 0) g (by simpa using hg)]
    simp
  · intro x hx; simpa using hx
  · intro v rm _ _ ⟨hsz, hI⟩
    simp only [stepOK_yield]
    refine ⟨by simp [hsz], fun g hg j => ?_⟩
    rw [get_set!]
    by_cases hg0 : lab[arcOf[v]!]! = g
    · subst hg0
      rw [ite_eq_left ⟨rfl, by omega⟩, Nat.testBit_or, hI _ hg j, testBit_shl_lt4 _ _ _ hth]
      by_cases h1 : j / 2 = v
      · subst h1; simp
      · by_cases h2 : j / 2 < v
        · simp [h1, h2, show j / 2 < v + 1 by omega]
        · simp [h1, h2, show ¬ j / 2 < v + 1 by omega]
    · rw [ite_eq_right (fun h => hg0 h.1), hI g hg j]
      by_cases h1 : j / 2 = v
      · subst h1; simp [hg0]
      · by_cases h2 : j / 2 < v
        · simp [h2, show j / 2 < v + 1 by omega]
        · simp [h2, show ¬ j / 2 < v + 1 by omega]

theorem testBit_ge_of_lt_pow {s m i : Nat} (hs : s < 2 ^ m) (hi : m ≤ i) : s.testBit i = false :=
  Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le hs (Nat.pow_le_pow_right (by omega) hi))

theorem xorSel_spec (r th k n s : Nat) (rm : Array Nat) (L : Nat → Nat)
    (hrm : ∀ g, g < n / 2 + 1 → ∀ j, rm[g]!.testBit j =
      (decide (j / 2 < r) && decide (L (j / 2) = g) && th.testBit (j % 2)))
    (hs : s < 2 ^ (n / 2)) (j : Nat) :
    (xorSel k n s rm).testBit j = (k.testBit j ^^ (decide (j / 2 < r) && decide (L (j / 2) ≠ 0) &&
      s.testBit (L (j / 2) - 1) && th.testBit (j % 2))) := by
  unfold xorSel
  refine forIn_range_bind 0 (n / 2) _ _ _
    (fun b (k2 : Nat) => k2.testBit j = (k.testBit j ^^ (decide (j / 2 < r) &&
      decide (L (j / 2) ≠ 0) && decide (L (j / 2) - 1 < b) && s.testBit (L (j / 2) - 1) &&
      th.testBit (j % 2))))
    (fun (k2 : Nat) => k2.testBit j = (k.testBit j ^^ (decide (j / 2 < r) &&
      decide (L (j / 2) ≠ 0) && s.testBit (L (j / 2) - 1) && th.testBit (j % 2)))) ?_ ?_ ?_
  · simp
  · intro x hx
    simp only [Id.run, pure] at hx ⊢
    rw [hx]
    by_cases h : L (j / 2) - 1 < n / 2
    · simp [h]
    · simp [testBit_ge_of_lt_pow hs (show n / 2 ≤ L (j / 2) - 1 by omega)]
  · intro b k2 _ hb hI
    dsimp only
    rw [shr_mod_two]
    split
    · rename_i hsb
      simp only [stepOK_yield]
      rw [Nat.testBit_xor, hI, hrm (b + 1) (by omega)]
      by_cases hL : L (j / 2) = b + 1
      · simp [hL, hsb]
      · by_cases h0 : L (j / 2) = 0
        · simp [h0]
        · simp [hL, h0, show (L (j / 2) - 1 < b + 1) ↔ (L (j / 2) - 1 < b) by omega]
    · rename_i hsb
      simp only [stepOK_yield]
      rw [hI]
      by_cases h3 : L (j / 2) - 1 = b
      · simp [h3, hsb, show ¬ b < b by omega]
      · simp [show (L (j / 2) - 1 < b + 1) ↔ (L (j / 2) - 1 < b) by omega]

theorem flipMask_testBit (r k th s : Nat) (lab : Array Nat) (hth : th < 4) (j : Nat) :
    (flipMask r k th lab s).testBit j = (decide (j / 2 < r) &&
      decide (lab[arcOf (transitions r k th) (j / 2)]! ≠ 0) &&
      s.testBit (lab[arcOf (transitions r k th) (j / 2)]! - 1) && th.testBit (j % 2)) := by
  unfold flipMask
  generalize transitions r k th = T
  simp only
  induction r with
  | zero => simp
  | succ V ih =>
    rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
    split
    · rename_i hc
      rw [Nat.testBit_or, ih, testBit_shl_lt4 _ _ _ hth]
      simp only [Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hc
      rw [← shr_mod_two] at *
      by_cases h1 : j / 2 = V
      · subst h1; simp [hc.1, hc.2]
      · by_cases h2 : j / 2 < V
        · simp [h1, h2, show j / 2 < V + 1 by omega]
        · simp [h1, h2, show ¬ j / 2 < V + 1 by omega]
    · rename_i hc
      rw [ih]
      by_cases h1 : j / 2 = V
      · subst h1
        simp only [Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq, not_and] at hc
        rw [← shr_mod_two]
        by_cases h0 : lab[arcOf T (j / 2)]! = 0
        · simp [h0]
        · simp [h0, hc h0]
      · by_cases h2 : j / 2 < V
        · simp [h2, show j / 2 < V + 1 by omega]
        · simp [h2, show ¬ j / 2 < V + 1 by omega]

/-- The in-loop flipped code equals the declarative one (`flipMask`). -/
theorem xorSel_eq (r k th s : Nat) (lab : Array Nat) (hth : th < 4)
    (hs : s < 2 ^ ((transitions r k th).size / 2)) :
    xorSel k (transitions r k th).size s
      (mkRm r (transitions r k th).size th
        ((Array.range r).map fun v => (((transitions r k th).filter (· < v)).size +
          (transitions r k th).size - 1) % (transitions r k th).size) lab) =
      k ^^^ flipMask r k th lab s := by
  apply Nat.eq_of_testBit_eq
  intro j
  rw [xorSel_spec r th k _ s _ (fun v => lab[((Array.range r).map fun v =>
      (((transitions r k th).filter (· < v)).size + (transitions r k th).size - 1) %
        (transitions r k th).size)[v]!]!) (mkRm_spec r _ th _ lab hth).2 hs,
    Nat.testBit_xor, flipMask_testBit r k th s lab hth]
  by_cases hj : j / 2 < r
  · rw [getElem!_pos _ (j / 2) (by simpa using hj)]
    simp only [hj, arcOf, Array.getElem_map, Array.getElem_range, decide_true, Bool.true_and]
    congr
  · simp [hj]

/-- Matching number `q` of the table for `(k, θ)` has a non-empty flip into `Good`. -/
def SatM (mt : Array (Array (Array Nat))) (cf : Conf) (k th q : Nat) : Prop :=
  ∃ s, 0 < s ∧ GoodT mt cf (canon cf.r (k ^^^
    flipMask cf.r k th (mt[(transitions cf.r k th).size / 2]!)[q]! s))

theorem satLoop_spec (r n k : Nat) (index : Std.HashMap Nat Nat) (good : Array Bool)
    (rm : Array Nat) (h : satLoop r n k index good rm = true) :
    ∃ s, 1 ≤ s ∧ s < 2 ^ (n / 2) ∧ ∃ j : Nat, index[canon r (xorSel k n s rm)]? = some j ∧
      good[j]! = true := by
  revert h
  unfold satLoop
  refine forIn_range_bind 1 (1 <<< (n / 2)) _ _ _
    (fun _ (sat : Bool) => sat = true → ∃ s, 1 ≤ s ∧ s < 2 ^ (n / 2) ∧
      ∃ j : Nat, index[canon r (xorSel k n s rm)]? = some j ∧ good[j]! = true)
    (fun (sat : Bool) => sat = true → ∃ s, 1 ≤ s ∧ s < 2 ^ (n / 2) ∧
      ∃ j : Nat, index[canon r (xorSel k n s rm)]? = some j ∧ good[j]! = true) ?_ ?_ ?_
  · intro h; cases h
  · intro x hx; exact hx
  · intro s sat h1 h2 hI
    rw [Nat.one_shiftLeft] at h2
    dsimp only
    split
    · rename_i j hj
      split
      · rename_i hg
        simp only [stepOK_done]
        intro _
        exact ⟨s, h1, h2, j, hj, hg⟩
      · simpa using hI
    · simpa using hI

theorem ptrLoop_spec (cf : Conf) (ks : Array Nat) (index : Std.HashMap Nat Nat)
    (good : Array Bool) (k th : Nat) (hth : th < 4)
    (hI : ∀ x j : Nat, index[x]? = some j → ks[j]! = x)
    (hG : ∀ j : Nat, good[j]! = true → GoodT mt cf ks[j]!) (pi : Nat)
    (hpi : ∀ q, q < pi → q < (mt[(transitions cf.r k th).size / 2]!).size →
      SatM mt cf k th q) :
    ∀ q, q < ptrLoop cf.r (transitions cf.r k th).size k th index good
        ((Array.range cf.r).map fun v => (((transitions cf.r k th).filter (· < v)).size +
          (transitions cf.r k th).size - 1) % (transitions cf.r k th).size)
        (mt[(transitions cf.r k th).size / 2]!) pi →
      q < (mt[(transitions cf.r k th).size / 2]!).size → SatM mt cf k th q := by
  unfold ptrLoop
  refine loop_bind _ _ _
    (fun (st : Nat × Bool) => ∀ q, q < st.1 →
      q < (mt[(transitions cf.r k th).size / 2]!).size → SatM mt cf k th q)
    (fun (p : Nat) => ∀ q, q < p →
      q < (mt[(transitions cf.r k th).size / 2]!).size → SatM mt cf k th q)
    (fun st => 2 * ((mt[(transitions cf.r k th).size / 2]!).size - st.1) +
      (!st.2).toNat) hpi ?_
  intro ⟨ptr, stuck⟩ hinv
  dsimp only
  split
  · rename_i hc
    simp only [Bool.and_eq_true, decide_eq_true_eq, Bool.not_eq_true'] at hc
    split
    · rename_i hsat
      simp only [stepOK_yield]
      refine ⟨fun q hq hqs => ?_, by simp [hc.2]; omega⟩
      by_cases hqp : q < ptr
      · exact hinv q hqp hqs
      · have hq : q = ptr := by omega
        subst hq
        obtain ⟨s, hs1, hs2, j, hj, hgj⟩ := satLoop_spec _ _ _ _ _ _ hsat
        refine ⟨s, hs1, ?_⟩
        have h1 := hI _ _ hj
        rw [xorSel_eq _ _ _ _ _ hth hs2] at h1
        rw [← h1]
        exact hG j hgj
    · simp only [stepOK_yield]
      exact ⟨hinv, by simp [hc.2]⟩
  · simp only [stepOK_done]
    exact hinv

/-! ## The θ loop -/

/-- Invariant (b): a progress pointer `p ≠ dead` for `(i, θ)` certifies the matchings `< p`. -/
def ProgOK (mt : Array (Array (Array Nat))) (cf : Conf) (ks prog : Array Nat) : Prop :=
  ∀ i th, 1 ≤ th → th ≤ 3 → prog[3 * i + th - 1]! ≠ 1000000 → ∀ q, q < prog[3 * i + th - 1]! →
    q < (mt[(transitions cf.r ks[i]! th).size / 2]!).size → SatM mt cf ks[i]! th q

theorem ProgOK_set (cf : Conf) (ks prog : Array Nat) (i th v : Nat) (h1 : 1 ≤ th) (h3 : th ≤ 3)
    (hP : ProgOK mt cf ks prog)
    (hv : v ≠ 1000000 → ∀ q, q < v →
      q < (mt[(transitions cf.r ks[i]! th).size / 2]!).size → SatM mt cf ks[i]! th q) :
    ProgOK mt cf ks (prog.set! (3 * i + th - 1) v) := by
  intro i' th' h1' h3'
  rw [get_set!]
  split
  · rename_i h
    have hi : i = i' := by omega
    have ht : th = th' := by omega
    subst hi; subst ht
    exact hv
  · exact hP i' th' h1' h3'

/-- All matchings of the table for `(k, θ)` certified ⇒ `GoodT mt cf k` (one `GoodT.step`). -/
theorem good_of_all (cf : Conf) (k th : Nat) (h1 : 1 ≤ th) (h3 : th ≤ 3)
    (hT : (transitions cf.r k th).size ≠ 0)
    (hall : ∀ q, q < (mt[(transitions cf.r k th).size / 2]!).size → SatM mt cf k th q) :
    GoodT mt cf k := by
  classical
  refine GoodT.step k th h1 h3 hT
    (fun lab => if h : ∃ s, 0 < s ∧ GoodT mt cf (canon cf.r (k ^^^ flipMask cf.r k th lab s))
      then Classical.choose h else 1) ?_ ?_
  · intro lab hlab
    obtain ⟨q, hq, rfl⟩ := Array.mem_iff_getElem.1 hlab
    have hs := hall q hq
    rw [SatM, getElem!_pos _ q hq] at hs
    rw [dite_eq_left hs]
    exact (Classical.choose_spec hs).1
  · intro lab hlab
    obtain ⟨q, hq, rfl⟩ := Array.mem_iff_getElem.1 hlab
    have hs := hall q hq
    rw [SatM, getElem!_pos _ q hq] at hs
    rw [dite_eq_left hs]
    exact (Classical.choose_spec hs).2

theorem thLoop_spec (cf : Conf) (ks : Array Nat) (index : Std.HashMap Nat Nat)
    (good : Array Bool) (prog : Array Nat) (i : Nat)
    (hI : ∀ x j : Nat, index[x]? = some j → ks[j]! = x)
    (hG : ∀ j : Nat, good[j]! = true → GoodT mt cf ks[j]!) (hP : ProgOK mt cf ks prog) :
    ProgOK mt cf ks (thLoopT mt cf.r i ks[i]! index good prog).1 ∧
      ((thLoopT mt cf.r i ks[i]! index good prog).2 = true → GoodT mt cf ks[i]!) := by
  unfold thLoopT
  refine forIn_range_bind 1 4 _ _ _
    (fun _ (st : Array Nat × Bool) => ProgOK mt cf ks st.1 ∧ (st.2 = true → GoodT mt cf ks[i]!))
    (fun (st : Array Nat × Bool) => ProgOK mt cf ks st.1 ∧ (st.2 = true → GoodT mt cf ks[i]!))
    ⟨hP, by simp⟩ (fun x hx => hx) ?_
  intro th ⟨prog, done⟩ h1 h4 ⟨hP, hD⟩
  dsimp only
  split
  · simp only [stepOK_done]; exact ⟨hP, hD⟩
  · split
    · simp only [stepOK_yield]; exact ⟨hP, hD⟩
    · rename_i _ hpi
      rw [mkT_eq]
      split
      · simp only [stepOK_yield]
        exact ⟨ProgOK_set cf ks prog i th _ h1 (by omega) hP (fun h => absurd rfl h), hD⟩
      · rename_i hn
        simp only [beq_iff_eq] at hpi hn
        have hptr := ptrLoop_spec cf ks index good ks[i]! th (by omega) hI hG _
          (hP i th h1 (by omega) hpi)
        split
        · rename_i heq
          simp only [stepOK_yield]
          refine ⟨ProgOK_set cf ks prog i th _ h1 (by omega) hP (fun _ => hptr),
            fun _ => good_of_all cf ks[i]! th h1 (by omega) hn ?_⟩
          intro q hq
          simp only [beq_iff_eq] at heq
          exact hptr q (by rw [heq]; exact hq) hq
        · simp only [stepOK_yield]
          exact ⟨ProgOK_set cf ks prog i th _ h1 (by omega) hP (fun _ => hptr), hD⟩

/-! ## The class loop -/

theorem iLoop_spec (cf : Conf) (ks : Array Nat) (index : Std.HashMap Nat Nat)
    (good : Array Bool) (prog : Array Nat)
    (hI : ∀ x j : Nat, index[x]? = some j → ks[j]! = x)
    (hG : ∀ j : Nat, good[j]! = true → GoodT mt cf ks[j]!) (hP : ProgOK mt cf ks prog) :
    ProgOK mt cf ks (iLoopT mt cf.r ks index good prog).1 ∧
      (∀ j ∈ (iLoopT mt cf.r ks index good prog).2.toList,
        j < ks.size ∧ good[j]! = false ∧ GoodT mt cf ks[j]!) ∧
      (iLoopT mt cf.r ks index good prog).2.toList.Pairwise (· < ·) := by
  unfold iLoopT
  refine forIn_range_bind 0 ks.size _ _ _
    (fun i (st : Array Nat × Array Nat) => ProgOK mt cf ks st.1 ∧
      (∀ j ∈ st.2.toList, j < i ∧ good[j]! = false ∧ GoodT mt cf ks[j]!) ∧
      st.2.toList.Pairwise (· < ·))
    (fun (st : Array Nat × Array Nat) => ProgOK mt cf ks st.1 ∧
      (∀ j ∈ st.2.toList, j < ks.size ∧ good[j]! = false ∧ GoodT mt cf ks[j]!) ∧
      st.2.toList.Pairwise (· < ·))
    ⟨hP, by simp, by simp⟩ (fun x hx => by simpa using hx) ?_
  intro i ⟨prog, new⟩ _ hi ⟨hP, hN, hPw⟩
  dsimp only
  split
  · simp only [stepOK_yield]
    exact ⟨hP, fun j hj => ⟨by have := (hN j hj).1; omega, (hN j hj).2⟩, hPw⟩
  · rename_i hgi
    have hth := thLoop_spec cf ks index good prog i hI hG hP
    generalize thLoopT mt cf.r i ks[i]! index good prog = res at hth ⊢
    obtain ⟨p', d⟩ := res
    dsimp only
    split
    · rename_i hd
      simp only [stepOK_yield, Array.toList_push, List.mem_append, List.mem_singleton]
      refine ⟨hth.1, ?_, ?_⟩
      · rintro j (hj | rfl)
        · exact ⟨by have := (hN j hj).1; omega, (hN j hj).2⟩
        · exact ⟨by omega, by simpa using hgi, hth.2 hd⟩
      · rw [List.pairwise_append]
        refine ⟨hPw, by simp, ?_⟩
        intro a ha b hb
        simp at hb; subst hb
        exact (hN a ha).1
    · simp only [stepOK_yield]
      exact ⟨hth.1, fun j hj => ⟨by have := (hN j hj).1; omega, (hN j hj).2⟩, hPw⟩

/-! ## Counting the reached classes -/

def countTrue (a : Array Bool) : Nat := (a.filter id).size

theorem countTrue_eq (a : Array Bool) : countTrue a = (a.toList.filter id).length := by
  unfold countTrue; rw [← Array.toList_filter, Array.length_toList]

theorem list_count_set (l : List Bool) (i : Nat) (hi : i < l.length) (hf : l[i] = false) :
    ((l.set i true).filter id).length = (l.filter id).length + 1 := by
  induction l generalizing i with
  | nil => simp at hi
  | cons b l ih =>
    cases i with
    | zero => simp at hf; subst hf; simp
    | succ i =>
      simp only [List.set_cons_succ]
      have hi' : i < l.length := by simpa using hi
      have hf' : l[i] = false := by simpa using hf
      cases b <;> simp [ih i hi' hf']

theorem countTrue_set (a : Array Bool) (i : Nat) (hi : i < a.size) (hf : a[i]! = false) :
    countTrue (a.set! i true) = countTrue a + 1 := by
  rw [countTrue_eq, countTrue_eq, Array.set!_eq_setIfInBounds, Array.toList_setIfInBounds]
  apply list_count_set _ _ (by simpa using hi)
  rw [getElem!_pos a i hi] at hf
  simpa using hf

theorem setFold_spec (l : List Nat) (good : Array Bool) (hl : l.Pairwise (· < ·))
    (hf : ∀ j ∈ l, j < good.size ∧ good[j]! = false) :
    (l.foldl (fun g i => g.set! i true) good).size = good.size ∧
    countTrue (l.foldl (fun g i => g.set! i true) good) = countTrue good + l.length ∧
    ∀ j : Nat, (l.foldl (fun g i => g.set! i true) good)[j]! = true → good[j]! = true ∨ j ∈ l := by
  induction l generalizing good with
  | nil => simp
  | cons a rest ih =>
    simp only [List.foldl_cons]
    rw [List.pairwise_cons] at hl
    have ha := hf a (by simp)
    have h := ih (good.set! a true) hl.2 (fun j hj => by
      refine ⟨by simpa using (hf j (by simp [hj])).1, ?_⟩
      rw [get_set!, ite_eq_right (by have := hl.1 j hj; omega)]
      exact (hf j (by simp [hj])).2)
    refine ⟨by simpa using h.1, by rw [h.2.1, countTrue_set _ _ ha.1 ha.2]; simp; omega, ?_⟩
    intro j hj
    rcases h.2.2 j hj with h' | h'
    · rw [get_set!] at h'
      split at h'
      · rename_i hj'; right; simp [hj'.1]
      · left; exact h'
    · right; simp [h']

theorem setLoop_eq (new : Array Nat) (good : Array Bool) :
    setLoop new good = new.toList.foldl (fun g i => g.set! i true) good := by
  unfold setLoop
  simp [Array.forIn_pure_yield_eq_foldl, Array.foldl_toList]

/-! ## The outer (level) loop and (S1) -/

/-- The outer-loop invariant: (a) good bits are `Good`, (b) `ProgOK mt`, plus the counting facts. -/
def OuterInv (mt : Array (Array (Array Nat))) (cf : Conf) (ks : Array Nat) (good : Array Bool) (reached : Nat) (prog : Array Nat) :
    Prop :=
  good.size = ks.size ∧ (∀ j : Nat, good[j]! = true → GoodT mt cf ks[j]!) ∧
    reached ≤ countTrue good ∧ ProgOK mt cf ks prog

theorem all_good_of_count (cf : Conf) (ks : Array Nat) (good : Array Bool) (reached : Nat)
    (prog : Array Nat) (h : OuterInv mt cf ks good reached prog) (hr : reached = ks.size) :
    ∀ k ∈ ks, GoodT mt cf k := by
  obtain ⟨hsz, hG, hcnt, _⟩ := h
  intro k hk
  obtain ⟨j, hj, rfl⟩ := Array.mem_iff_getElem.1 hk
  have hle : countTrue good ≤ good.size := by
    rw [countTrue_eq, Array.size_eq_length_toList]; exact List.length_filter_le _ _
  have heq : (good.toList.filter id).length = good.toList.length := by
    rw [← countTrue_eq, Array.length_toList]; omega
  have hall := List.length_filter_eq_length_iff.1 heq
  have hj' : j < good.size := by omega
  have := hG j (by
    rw [getElem!_pos good j hj']
    exact hall _ (by rw [← Array.getElem_toList (by simpa using hj')]; exact List.getElem_mem _))
  rwa [getElem!_pos ks j hj] at this

theorem replicate_zero_get (n x : Nat) : (Array.replicate n 0)[x]! = 0 := by
  by_cases h : x < n
  · rw [getElem!_pos _ x (by simpa using h)]; simp
  · rw [getElem!_neg _ x (by simpa using h)]; rfl

theorem runRef_sound (cf : Conf) :
    (runRefT mt cf).reached = (runRefT mt cf).classes → ∀ k ∈ ringColourings cf.r, GoodT mt cf k := by
  have hI := mkIndex_spec (ringColourings cf.r)
  unfold runRefT
  refine forIn_range_bind 0 ((ringColourings cf.r).size + 1) _ _ _
    (fun _ (st : Array Bool × Nat × Array Nat × Nat) =>
      OuterInv mt cf (ringColourings cf.r) st.1 st.2.1 st.2.2.1)
    (fun (res : Result) => res.reached = res.classes → ∀ k ∈ ringColourings cf.r, GoodT mt cf k)
    ?_ (fun x hx => all_good_of_count cf _ _ _ _ hx) ?_
  · refine ⟨by simp, fun j hj => ?_, Nat.le_refl _, ?_⟩
    · by_cases hjs : j < (ringColourings cf.r).size
      · rw [getElem!_pos _ j (by simpa using hjs)] at hj
        rw [getElem!_pos _ j hjs]
        exact GoodT.base _ (by simpa using hj)
      · rw [getElem!_neg _ j (by simpa using hjs)] at hj
        cases hj
    · intro i th _ _ _ q hq
      rw [replicate_zero_get] at hq
      omega
  · intro _ ⟨good, reached, prog, depth⟩ _ _ ⟨hsz, hG, hcnt, hP⟩
    dsimp only at hsz hG hcnt hP ⊢
    have hit := iLoop_spec cf (ringColourings cf.r) (mkIndex (ringColourings cf.r)) good prog
      hI hG hP
    generalize iLoopT mt cf.r (ringColourings cf.r) (mkIndex (ringColourings cf.r)) good prog = res
      at hit ⊢
    obtain ⟨p', new⟩ := res
    obtain ⟨hP', hN, hPw⟩ := hit
    dsimp only at hP' hN hPw ⊢
    split
    · simp only [stepOK_done]
      exact all_good_of_count cf _ _ _ _ ⟨hsz, hG, hcnt, hP'⟩
    · simp only [stepOK_yield]
      have hs := setFold_spec new.toList good hPw
        (fun j hj => ⟨by have := (hN j hj).1; omega, (hN j hj).2.1⟩)
      rw [setLoop_eq]
      refine ⟨by rw [hs.1, hsz], fun j hj => ?_, ?_, hP'⟩
      · rcases hs.2.2 j hj with h | h
        · exact hG j h
        · exact (hN j h).2.2
      · rw [hs.2.1, Array.length_toList]; omega

/-- **(S1) Loop correctness of the checker.** -/
theorem run_sound (cf : Conf) (hD : dReducibleT mt cf = true) :
    ∀ k ∈ ringColourings cf.r, GoodT mt cf k := by
  unfold dReducibleT at hD
  rw [runT_eq_runRefT] at hD
  exact runRef_sound cf (by simpa using hD)

end DCheck.S1T

namespace DCheck

theorem run_soundT (mt : Array (Array (Array Nat))) (cf : Conf) (hD : dReducibleT mt cf = true) :
    ∀ k ∈ ringColourings cf.r, GoodT mt cf k :=
  S1T.run_sound cf hD

/-- (S1)+(S2) for the parametrised checker. -/
theorem dReducible_soundT (mt : Array (Array (Array Nat))) (cf : Conf) (hD : dReducibleT mt cf = true)
    (hr : 2 ≤ cf.r) (P : Nat → Prop) (hcanon : ∀ k, P k → P (canon cf.r k))
    (hK : KempeMatchingT mt cf P)
    (hprop : ∀ k, P k → (∀ i, i < cf.r → col k i ≠ col k ((i + 1) % cf.r)) ∧ k < 4 ^ cf.r)
    (k : Nat) (hP : P k) : ∃ k', P k' ∧ extendsQ cf k' = true :=
  good_soundT mt cf P hcanon hK _
    (run_soundT mt cf hD _ (canon_mem cf.r k hr (hprop k hP).1 (hprop k hP).2)) (hcanon k hP)

end DCheck

#print axioms DCheck.dReducible_soundT
