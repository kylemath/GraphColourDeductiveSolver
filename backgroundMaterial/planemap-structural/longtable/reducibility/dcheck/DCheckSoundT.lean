import DCheckSound
import DCheckT
/-! Job 23: `Good`, `KempeMatching` and `good_sound` (S2) of `DCheckSound.lean` with the matching table
`mt` as a parameter (definitions copied, `matchTable` replaced by `mt`). -/
namespace DCheck

/-- The declarative D-closure (least fixpoint). The witness `w` picks, for each matching, the
non-empty region set to flip (a function rather than `∃`, to keep the inductive non-nested). -/
inductive GoodT (mt : Array (Array (Array Nat))) (cf : Conf) : Nat → Prop
  | base (k : Nat) : extendsQ cf k = true → GoodT mt cf k
  | step (k th : Nat) : 1 ≤ th → th ≤ 3 → (transitions cf.r k th).size ≠ 0 →
      (w : Array Nat → Nat) → (∀ lab ∈ mt[(transitions cf.r k th).size / 2]!, 0 < w lab) →
      (∀ lab ∈ mt[(transitions cf.r k th).size / 2]!,
        GoodT mt cf (canon cf.r (k ^^^ flipMask cf.r k th lab (w lab)))) →
      GoodT mt cf k

/-- The geometric input, abstracted: for a realised code and a pairing θ with transitions, the
outside Kempe chains realise SOME matching of the table, and every set of its regions can be
swapped (staying realised). -/
def KempeMatchingT (mt : Array (Array (Array Nat))) (cf : Conf) (P : Nat → Prop) : Prop :=
  ∀ k th, P k → 1 ≤ th → th ≤ 3 → (transitions cf.r k th).size ≠ 0 →
    ∃ lab ∈ mt[(transitions cf.r k th).size / 2]!,
      ∀ s, P (k ^^^ flipMask cf.r k th lab s)

/-- **(S2) Combinatorial core.** -/
theorem good_soundT (mt : Array (Array (Array Nat))) (cf : Conf) (P : Nat → Prop)
    (hcanon : ∀ k, P k → P (canon cf.r k)) (hK : KempeMatchingT mt cf P) :
    ∀ k, GoodT mt cf k → P k → ∃ k', P k' ∧ extendsQ cf k' = true := by
  intro k hk
  induction hk with
  | base k h => exact fun hP => ⟨k, hP, h⟩
  | step k th h1 h3 hT w _ _ ih =>
    intro hP
    obtain ⟨lab, hlab, hflip⟩ := hK k th hP h1 h3 hT
    exact ih lab hlab (hcanon _ (hflip (w lab)))

theorem good_eq_T : Good = GoodT matchTable := by
  funext cf k; apply propext; constructor
  · intro h; induction h with
    | base k h => exact GoodT.base k h
    | step k th h1 h3 hT w hw _ ih => exact GoodT.step k th h1 h3 hT w hw ih
  · intro h; induction h with
    | base k h => exact Good.base k h
    | step k th h1 h3 hT w hw _ ih => exact Good.step k th h1 h3 hT w hw ih

theorem kempeMatching_eq_T : KempeMatching = KempeMatchingT matchTable := rfl

end DCheck
