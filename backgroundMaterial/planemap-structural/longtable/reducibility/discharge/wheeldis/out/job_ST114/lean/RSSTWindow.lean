import RSSTWindowDefs
import RSSTWindowSep

/-!
# ST-114 B3: the induced-window theorem (statement only)

Studio, 10 Nov. See `../B3_STATEMENT.md`. The window objects (`rotNbr`, `IsLink`, `InR2`, `IsApex`) are in
`RSSTWindowDefs.lean` (moved verbatim); the lemmas L0–L10 are in `RSSTWindowBasic`, `RSSTWindowLink`, `RSSTWindowSep`.
After the review (15:05Z) the conclusion has one more field, `apex_off_link` (review point (a)). No existing module is
edited.

For a vertex `u` of an internally 6-connected triangulation (`ClaimGlue.Internally6`, the project's frame class), let `w`
list the rotation at `u`. Then the closed 2-ball of `u` (its link, apexes, privates, and every real middle neighbour of a 9+
link vertex) is induced, with no identifications beyond the shared apexes, and every triangle in it is a face.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap VacancyIcosahedral

variable {n : ℕ}

/-- **The conclusion of B3.** -/
structure WindowInduced (T : SphericalMap n) (u : Fin n) (d : ℕ) (w : ℕ → Fin n) : Prop where
  /-- `u, w_0, …, w_{d-1}` are distinct. -/
  link_inj : ∀ i j, i < d → j < d → w i = w j → i = j
  link_ne : ∀ i, w i ≠ u
  /-- (a) The link has no chord. -/
  link_chordless : ∀ i j, T.Adj (w i) (w j) → j % d = (i + 1) % d ∨ i % d = (j + 1) % d
  /-- Each link edge `w_i w_{i+1}` has exactly one apex. -/
  apex_unique : ∀ i, ∃ x, IsApex T u w i x ∧ ∀ y, IsApex T u w i y → y = x
  /-- The apex `s_i` is no link vertex (and not `u`, by `IsApex`). Review point (a). -/
  apex_off_link : ∀ i x, IsApex T u w i x → ∀ k, w k ≠ x
  /-- (b)+(c) No identifications in ring 2. A ring-2 vertex sees exactly one link vertex (mod `d`), or it is the apex
  `s_i` and sees exactly `w_i` and `w_{i+1}`. -/
  r2_home : ∀ x, InR2 T u w x →
    (∃ i, i < d ∧ T.Adj (w i) x ∧ ∀ j, j < d → T.Adj (w j) x → j = i) ∨
    (∃ i, i < d ∧ IsApex T u w i x ∧ ∀ j, j < d → T.Adj (w j) x → j = i ∨ j = (i + 1) % d)
  /-- (d) Ring 2 has no chord. Adjacent ring-2 vertices share a link neighbour `w_i` and form a face with it, so they are
  consecutive in `rot(w_i)`, i.e. on the ring-2 cycle. -/
  r2_chordless : ∀ x y, InR2 T u w x → InR2 T u w y → T.Adj x y →
    ∃ i, T.Adj (w i) x ∧ T.Adj (w i) y ∧ SimpleGraph.SphericalMap.Facial T (w i) x y

/-- **B3, the induced-window theorem.** The hypotheses are the frame class `Internally6` (triangulated, connected, minimum
degree 5, no separating triangle, `NoShortSepCycle`) and a link listing of `u`. -/
theorem window_induced {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) {u : Fin n} {d : ℕ} {w : ℕ → Fin n}
    (hL : IsLink T u d w) : WindowInduced T u d w := by
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  -- L6 in index form: the link neighbours of a ring-2 vertex are pairwise close
  have near : ∀ x, x ≠ u → (∀ j, w j ≠ x) → ∀ a b, a < d → b < d → T.Adj (w a) x → T.Adj (w b) x →
      b = a ∨ b = (if a + 1 = d then 0 else a + 1) ∨ a = (if b + 1 = d then 0 else b + 1) := by
    intro x hxu hxw
    have key : ∀ a b, a ≤ b → b < d → T.Adj (w a) x → T.Adj (w b) x →
        b = a ∨ b = (if a + 1 = d then 0 else a + 1) ∨ a = (if b + 1 = d then 0 else b + 1) := by
      intro a b hab hb ha' hb'
      by_cases h0 : b = a
      · exact Or.inl h0
      by_cases h1 : b = a + 1
      · right; left; rw [if_neg (by omega)]; exact h1
      by_cases h2 : a = 0 ∧ b = d - 1
      · right; right; rw [if_pos (by omega)]; exact h2.1
      exfalso
      exact (hL.shift a).r2_far0 hT hxu (fun j => hxw _) ha' (k := b - a) (by omega) (by omega)
        (by show T.Adj (w (a + (b - a))) x; rwa [show a + (b - a) = b by omega])
    intro a b ha hb ha' hb'
    rcases le_total a b with h | h
    · exact key a b h hb ha' hb'
    · rcases key b a h ha hb' ha' with e | e | e
      · exact Or.inl e.symm
      · exact Or.inr (Or.inr e)
      · exact Or.inr (Or.inl e)
  refine ⟨fun i j hi hj h => hL.inj hi hj h, hL.ne, hL.chordless hT, ?_, fun i x hx k => hL.apex_off_link hT hx k,
    ?_, ?_⟩
  · -- apex_unique (L4)
    intro i
    obtain ⟨s, hsu, hs1, -, hsi, hsi1⟩ := hL.apex hT i
    exact ⟨s, ⟨hsu, hsi, hsi1⟩, fun y hy => hL.apex_eq hT hs1 hy⟩
  · -- r2_home (L6, L6', L7)
    rintro x ⟨hxu, hxw, i, hi⟩
    have hi0lt : i % d < d := Nat.mod_lt _ hd
    have hi0 : T.Adj (w (i % d)) x := by rw [hL.per_mod]; exact hi
    generalize i % d = i0 at hi0lt hi0
    by_cases hall : ∀ j, j < d → T.Adj (w j) x → j = i0
    · exact Or.inl ⟨i0, hi0lt, hi0, hall⟩
    · push Not at hall
      obtain ⟨j, hj, hjx, hji⟩ := hall
      rcases near x hxu hxw i0 j hi0lt hj hi0 hjx with e | e | e
      · exact absurd e hji
      · right
        refine ⟨i0, hi0lt, ⟨hxu, hi0, ?_⟩, ?_⟩
        · rw [← hL.per_mod (i0 + 1), succ_mod_eq hi0lt, ← e]; exact hjx
        · intro m hm hmx
          have n1 := near x hxu hxw i0 m hi0lt hm hi0 hmx
          have n2 := near x hxu hxw j m hj hm hjx hmx
          rw [succ_mod_eq hi0lt]
          split_ifs at e n1 n2 ⊢ <;> omega
      · right
        refine ⟨j, hj, ⟨hxu, hjx, ?_⟩, ?_⟩
        · rw [← hL.per_mod (j + 1), succ_mod_eq hj, ← e]; exact hi0
        · intro m hm hmx
          have n1 := near x hxu hxw i0 m hi0lt hm hi0 hmx
          have n2 := near x hxu hxw j m hj hm hjx hmx
          rw [succ_mod_eq hj]
          split_ifs at e n1 n2 ⊢ <;> omega
  · -- r2_chordless (L8, L9, L10)
    rintro x y ⟨hxu, hxw, i, hi⟩ ⟨hyu, hyw, k, hk⟩ hxy
    by_cases hcom : ∃ j, T.Adj (w j) x ∧ T.Adj (w j) y
    · obtain ⟨j, hjx, hjy⟩ := hcom
      exact ⟨j, hjx, hjy, hT.noSep _ _ _ hjx hxy hjy.symm⟩
    exfalso
    push Not at hcom
    by_cases hcl : ∃ a b, T.Adj (w a) x ∧ T.Adj (w b) y ∧ Close d a b
    · obtain ⟨a, b, ha, hb, hab⟩ := hcl
      rcases hab with e | e | e
      · have : w b = w a := (hL.eq_iff hd _ _).2 e
        exact hcom a ha (this ▸ hb)
      · have : w b = w (a + 1) := (hL.eq_iff hd _ _).2 e
        rw [this] at hb
        exact hL.r2_adj hT hxu hyu hxw hyw ha hb hxy (fun h => hcom _ h hb) (hcom a ha)
      · have : w a = w (b + 1) := (hL.eq_iff hd _ _).2 e
        rw [this] at ha
        exact hL.r2_adj hT hyu hxu hyw hxw hb ha hxy.symm (fun h => hcom _ ha h) (fun h => hcom b h hb)
    have hnc : ∀ a b, T.Adj (w a) x → T.Adj (w b) y → ¬ Close d a b :=
      fun a b ha hb hc => hcl ⟨a, b, ha, hb, hc⟩
    have hi0 : T.Adj (w (i % d)) x := by rw [hL.per_mod]; exact hi
    have hk0 : T.Adj (w (k % d)) y := by rw [hL.per_mod]; exact hk
    have nc := hnc _ _ hi0 hk0
    have hilt : i % d < d := Nat.mod_lt _ hd
    have hklt : k % d < d := Nat.mod_lt _ hd
    generalize i % d = i0 at hi0 nc hilt
    generalize k % d = k0 at hk0 nc hklt
    unfold Close at nc
    rw [Nat.mod_eq_of_lt hilt, Nat.mod_eq_of_lt hklt, succ_mod_eq hilt, succ_mod_eq hklt] at nc
    rcases le_total i0 k0 with h | h
    · have hb1 : 2 ≤ k0 - i0 ∧ k0 - i0 + 2 ≤ d := by split_ifs at nc <;> omega
      exact (hL.shift i0).r2_chord_far0 hT hxu hyu (fun j => hxw _) (fun j => hyw _) hi0 hb1.1 hb1.2
        (by show T.Adj (w (i0 + (k0 - i0))) y; rwa [show i0 + (k0 - i0) = k0 by omega]) hxy
        (fun a b ha hb hc => hnc _ _ ha hb (hc.shift i0))
    · have hb1 : 2 ≤ i0 - k0 ∧ i0 - k0 + 2 ≤ d := by split_ifs at nc <;> omega
      exact (hL.shift k0).r2_chord_far0 hT hyu hxu (fun j => hyw _) (fun j => hxw _) hk0 hb1.1 hb1.2
        (by show T.Adj (w (k0 + (i0 - k0))) x; rwa [show k0 + (i0 - k0) = i0 by omega]) hxy.symm
        (fun a b ha hb hc => hnc _ _ hb ha (hc.shift k0).symm)

/-- F0 on the window: every triangle of `T` is a face (`noSep`), restated for downstream use (B4, B6). -/
theorem window_facial {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) {a b c : Fin n}
    (hab : T.Adj a b) (hbc : T.Adj b c) (hca : T.Adj c a) : SimpleGraph.SphericalMap.Facial T a b c :=
  hT.noSep a b c hab hbc hca

#print axioms window_induced
#print axioms window_facial

end SimpleGraph.SphericalMap.RSSTSeed
