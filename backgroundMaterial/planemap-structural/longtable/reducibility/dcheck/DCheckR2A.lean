import DCheckS1

/-! Job 19 piece (A): soundness of `extendsQ` (the backtracking interior colouring). -/
namespace DCheck.R2

theorem push_get_lt (cols : Array Nat) (x i : Nat) (h : i < cols.size) :
    (cols.push x)[i]! = cols[i]! := by
  rw [getElem!_pos (cols.push x) i (by simp; omega), getElem!_pos cols i h, Array.getElem_push_lt]

theorem push_get_eq (cols : Array Nat) (x : Nat) : (cols.push x)[cols.size]! = x := by
  rw [getElem!_pos (cols.push x) cols.size (by simp), Array.getElem_push_eq]

theorem extAux_sound (cf : Conf) (k : Nat) :
    ∀ f (cols : Array Nat), (∀ i, i < cols.size → cols[i]! < 4) → extAux cf k f cols = true →
      ∃ out : Array Nat, out.size = cols.size + f ∧ (∀ i, i < cols.size → out[i]! = cols[i]!) ∧
        (∀ i, i < out.size → out[i]! < 4) ∧
        (∀ a, cols.size ≤ a → a < out.size →
          (∀ t ∈ cf.ringAdj[a]!, col k t ≠ out[a]!) ∧
          (∀ b ∈ cf.intAdj[a]!, b < a → out[b]! ≠ out[a]!)) := by
  intro f
  induction f with
  | zero =>
    intro cols hlt _
    exact ⟨cols, by simp, fun _ _ => rfl, hlt, fun a h1 h2 => by omega⟩
  | succ f ih =>
    intro cols hlt h
    simp only [extAux, List.any_cons, List.any_nil, Bool.or_false, Bool.or_eq_true,
      Bool.and_eq_true, Array.all_eq_true] at h
    -- one of the four colours works
    have key : ∃ x, x < 4 ∧ (∀ t ∈ cf.ringAdj[cols.size]!, col k t ≠ x) ∧
        (∀ b ∈ cf.intAdj[cols.size]!, b < cols.size → cols[b]! ≠ x) ∧
        extAux cf k f (cols.push x) = true := by
      have mk : ∀ x, x < 4 →
          (((∀ i, (hi : i < cf.ringAdj[cols.size]!.size) → (col k cf.ringAdj[cols.size]![i] != x) = true) ∧
            (∀ i, (hi : i < cf.intAdj[cols.size]!.size) →
              decide (cf.intAdj[cols.size]![i] ≥ cols.size) = true ∨ (cols[cf.intAdj[cols.size]![i]]! != x) = true)) ∧
            extAux cf k f (cols.push x) = true) →
          ∃ x, x < 4 ∧ (∀ t ∈ cf.ringAdj[cols.size]!, col k t ≠ x) ∧
            (∀ b ∈ cf.intAdj[cols.size]!, b < cols.size → cols[b]! ≠ x) ∧
            extAux cf k f (cols.push x) = true := by
        intro x hx ⟨⟨hr, hi⟩, he⟩
        refine ⟨x, hx, ?_, ?_, he⟩
        · intro t ht
          obtain ⟨i, hi', rfl⟩ := Array.mem_iff_getElem.1 ht
          simpa using hr i hi'
        · intro b hb hbl
          obtain ⟨i, hi', rfl⟩ := Array.mem_iff_getElem.1 hb
          have := hi i hi'
          simp only [decide_eq_true_eq, bne_iff_ne, ne_eq] at this
          rcases this with h1 | h1
          · omega
          · exact h1
      rcases h with h | h | h | h
      · exact mk 0 (by decide) h
      · exact mk 1 (by decide) h
      · exact mk 2 (by decide) h
      · exact mk 3 (by decide) h
    obtain ⟨x, hx, hring, hint, hext⟩ := key
    have hlt' : ∀ i, i < (cols.push x).size → (cols.push x)[i]! < 4 := by
      intro i hi
      simp only [Array.size_push] at hi
      by_cases h' : i < cols.size
      · rw [push_get_lt _ _ _ h']; exact hlt i h'
      · rw [show i = cols.size by omega, push_get_eq]; exact hx
    obtain ⟨out, hsz, hpre, hlo, hok⟩ := ih (cols.push x) hlt' hext
    simp only [Array.size_push] at hsz hpre hok
    refine ⟨out, by omega, ?_, hlo, ?_⟩
    · intro i hi
      rw [hpre i (by omega), push_get_lt _ _ _ hi]
    · intro a h1 h2
      by_cases ha : a = cols.size
      · subst ha
        have hxa : out[cols.size]! = x := by rw [hpre _ (by omega), push_get_eq]
        refine ⟨fun t ht => hxa ▸ hring t ht, fun b hb hbl => ?_⟩
        rw [hxa, hpre b (by omega), push_get_lt _ _ _ hbl]
        exact hint b hb hbl
      · exact hok a (by omega) h2

/-- **(A)** A successful `extendsQ` gives an interior colouring `lam`: entries `< 4`, avoiding the ring
colours of `k` at listed ring neighbours and the colours of listed earlier interior neighbours. -/
theorem extendsQ_sound (cf : Conf) (k : Nat) (h : extendsQ cf k = true) :
    ∃ out : Array Nat, out.size = cf.m ∧ (∀ i, i < out.size → out[i]! < 4) ∧
      (∀ a, a < cf.m →
        (∀ t ∈ cf.ringAdj[a]!, col k t ≠ out[a]!) ∧
        (∀ b ∈ cf.intAdj[a]!, b < a → out[b]! ≠ out[a]!)) := by
  obtain ⟨out, hsz, _, hlo, hok⟩ := extAux_sound cf k cf.m #[] (by simp) h
  simp only [List.size_toArray, List.length_nil, Nat.zero_add] at hsz
  exact ⟨out, hsz, hlo, fun a ha => hok a (Nat.zero_le _) (by omega)⟩

end DCheck.R2

#print axioms DCheck.R2.extendsQ_sound
