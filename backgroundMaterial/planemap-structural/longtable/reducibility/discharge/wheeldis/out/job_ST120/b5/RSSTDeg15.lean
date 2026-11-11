import RSSTCheckSound
import RSSTRulesN2

/-!
# ST-120 B5 M5: `d ≥ 9` gives `hi ≤ 60 − 4d`, so every word of degree `≥ 15` has `hi ≤ 0`

Studio, 10 Nov. Spec §8.4: at `d ≥ 9`, `u` never sends (no part has `≥ 9` subparts) and `u` reads as 9+, so
`hi = 10(6 − d) + Σ_i c_i` with `c_i` the number of fits from hub `w_i` (letter `≤ 8`) into `u` that are possible.
Here `c_i ≤ 6` is proved by a **slot relaxation**: the view of hub `w_i` (B2's `viewW`) is, entry by entry, a
*slot view* in which every letter the view reads is an independent code (spoke `t ≥ 1`, hat `t`, fan `(t, k)`), the
spoke at `t = 0` is `u` = 9, the ring-3 hats/fans are unknown (`none`, OPEN), and the fans of `u` are dropped (a
subpart on `u` with a constrained fan has a spoke range without 9, so it fails whatever the fans: B4's `Sub.Good`).
For each hub letter `L = 5..8` the checker's own `dfs` bounds the number of possible fits in the slot view by 6
(`slotCheck`, by `decide`: kernel only). So `hi ≤ 60 − 10d + 6d = 60 − 4d`.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-! ## The slot view and its bound -/

def slotSp (t : Nat) : Nat := 100 + t
def slotHat (t : Nat) : Nat := 120 + t
def slotFan (t k : Nat) : Nat := 140 + 4 * t + k

def hatRing3 (L t : Nat) : Bool := decide (3 ≤ t ∧ t + 2 ≤ L)
def fanRing3 (L t : Nat) : Bool := decide (2 ≤ t ∧ t + 2 ≤ L)

def slotEntry (L t : Nat) : TSpoke :=
  { sp := if t = 0 then 9 else slotSp t,
    hat := if hatRing3 L t then none else some (slotHat t),
    fansOf := fun m => if t = 0 then [] else (List.range m).map fun k => if fanRing3 L t then none else some (slotFan t k),
    fc := if t = 0 then fun _ => 0 else npriv }

def slotView (L : Nat) : List TSpoke := (List.range L).map (slotEntry L)

def slotIns (parts : List Part) (L : Nat) : List SRes := (parts.filter (·.hub == L)).map fun p => symFit p (slotView L) (L - 2)

def slotOrder (parts : List Part) (L : Nat) : List Nat :=
  (((slotIns parts L).flatMap fun x => match x with
    | .c cs _ => cs.map (·.1)
    | .no => []).eraseDups).filter isCode

/-- At most 6 fits into `u` are possible in the slot view of a hub with letter `L`. -/
def slotCheck (parts : List Part) (L : Nat) : Bool :=
  dfs (-6) ((slotOrder parts L).map fun v => (v, classesOf v (slotIns parts L))) (slotIns parts L) [] []

/-- All hub letters, plus the shape facts the bound uses. -/
def slotAll (parts : List Part) : Bool :=
  slotCheck parts 5 && slotCheck parts 6 && slotCheck parts 7 && slotCheck parts 8 &&
  parts.all Part.fanExact && parts.all Part.wellShaped

set_option maxRecDepth 100000 in
theorem slotAll_71 : slotAll rsstParts = true := by decide

set_option maxRecDepth 100000 in
/-- The 79 parts (71 + N2, B2 `RSSTRulesN2`): still at most 6 per hub. -/
theorem slotAll_79 : slotAll rsstParts79 = true := by decide

theorem slot_bound {parts : List Part} {L : Nat} (hL : slotCheck parts L = true) (σ : Nat → Nat) (hσ : ∀ c, 100 ≤ c → 5 ≤ σ c ∧ σ c ≤ 9) :
    ((slotIns parts L).map fun x => (x.eval σ).possI).sum ≤ 6 := by
  rcases dfs_sound (-6) σ _ _ [] [] hL (fun p hp => by
      obtain ⟨v, hv, rfl⟩ := List.mem_map.1 hp
      have := (List.mem_filter.1 hv).2
      unfold isCode at this; rw [Nat.ble_eq] at this
      exact hσ v this) with h | ⟨R, hR, -⟩
  · simpa using h
  · simp at hR

/-! ## Real hub views are slot views -/

/-- The valuation of the slot codes read off a real word at hub `w_i`. -/
def slotSigma (W : UWin) (i : Nat) (c : Nat) : Nat :=
  let L := W.linkL i
  if c < 100 then c
  else if c < 120 then (W.letter i (wSpokePos L (c - 100))).getD 9
  else if c < 140 then (W.letter i (wHatPos L (c - 120))).getD 9
  else (W.letter i (wFanPos L ((c - 140) / 4) ((c - 140) % 4))).getD 9

theorem letter_range {W : UWin} (hW : RealShape W) {b : Nat} {pos : WPos} {x : Nat} (h : W.letter b pos = some x) :
    5 ≤ x ∧ x ≤ 9 := by
  obtain ⟨h5, hlen, halen, hplen, hlk, hap, hpriv⟩ := hW
  have g : ∀ (l : List Nat) (n : Nat), (∀ y ∈ l, 5 ≤ y ∧ y ≤ 9) → 5 ≤ l.getD n 9 ∧ l.getD n 9 ≤ 9 := by
    intro l n hl
    rw [List.getD_eq_getElem?_getD]
    cases h : l[n]? with
    | none => simp
    | some y => simpa using hl y (List.mem_of_getElem? h)
  have hseg : ∀ m y, y ∈ W.segL m → 5 ≤ y ∧ y ≤ 9 := by
    intro m y hy
    simp only [UWin.segL, List.mem_append, List.mem_singleton] at hy
    rcases hy with (rfl | hy) | rfl
    · exact g _ _ hap
    · have hy' := List.mem_of_mem_take hy
      by_cases hm : m < W.d
      · exact (hpriv m hm).2 y hy'
      · rw [getD_ge' _ _ _ (by omega)] at hy'; simp at hy'
    · exact g _ _ hap
  cases pos with
  | u => simp only [UWin.letter, Option.some.injEq] at h; subst h; omega
  | w δ => simp only [UWin.letter, Option.some.injEq] at h; subst h; exact g _ _ hlk
  | seg δ k => simp only [UWin.letter] at h; exact hseg _ _ (List.mem_of_getElem? h)
  | segR δ k =>
    simp only [UWin.letter] at h
    split_ifs at h
    · exact hseg _ _ (List.mem_of_getElem? h)
  | ring3 => simp [UWin.letter] at h

theorem slotSigma_range {W : UWin} (hW : RealShape W) (i c : Nat) (hc : 100 ≤ c) :
    5 ≤ slotSigma W i c ∧ slotSigma W i c ≤ 9 := by
  have g : ∀ o : Option Nat, (∀ x, o = some x → 5 ≤ x ∧ x ≤ 9) → 5 ≤ o.getD 9 ∧ o.getD 9 ≤ 9 := by
    intro o ho; cases o with
    | none => simp
    | some x => simpa using ho x rfl
  unfold slotSigma
  simp only
  rw [if_neg (by omega)]
  split_ifs <;> exact g _ (fun x hx => letter_range hW hx)

theorem slotSigma_fix (W : UWin) (i : Nat) : FixLow (slotSigma W i) := by
  intro x hx; unfold slotSigma; simp [hx]

theorem idx_lt (W : UWin) (hd : 0 < W.d) (b : Nat) (δ : Int) : W.idx b δ < W.d := by
  unfold UWin.idx
  have h1 := Int.emod_nonneg ((b : Int) + δ) (by omega : (W.d : Int) ≠ 0)
  have h2 := Int.emod_lt_of_pos ((b : Int) + δ) (by omega : (0 : Int) < W.d)
  omega

theorem idx_self (W : UWin) {i : Nat} (hi : i < W.d) : W.idx i 0 = i := by
  unfold UWin.idx
  rw [add_zero, Int.emod_eq_of_lt (by omega) (by omega)]
  simp

theorem segL_len {W : UWin} (hW : RealShape W) {m : Nat} (hm : m < W.d) :
    (W.segL m).length = npriv (W.linkL m) + 2 := by
  have := (hW.2.2.2.2.2.2 m hm).1
  simp only [UWin.segL, List.length_append, List.length_singleton, List.length_take, this]
  omega

theorem some_getD {o : Option Nat} {x : Nat} (h : o = some x) (a : Nat) : some (o.getD a) = o := by
  subst h; rfl

theorem seg_some {W : UWin} (hW : RealShape W) (hd : 0 < W.d) (b : Nat) (δ : Int) (k : Nat)
    (hk : k < npriv (W.linkL (W.idx b δ)) + 2) : ∃ x, W.letter b (.seg δ k) = some x := by
  simp only [UWin.letter]
  rw [List.getElem?_eq_getElem (by rw [segL_len hW (idx_lt W hd b δ)]; exact hk)]
  exact ⟨_, rfl⟩

theorem npriv_lt8 {L : Nat} (h5 : 5 ≤ L) (h8 : L ≤ 8) : npriv L = L - 5 := by
  unfold npriv; split_ifs <;> omega

/-- A subpart reading `u` (spoke 9) does not look at the fans (B4's `Sub.Good`). -/
theorem fit3_u_fans (s : Sub) (hs : s.Good) (v : PSpokeView) (h9 : v.spoke = 9) (fs : List (Option Nat)) :
    s.fit3 { v with fans := fs } = s.fit3 v := by
  unfold Sub.fit3
  simp only [h9]
  rcases hs with hf | ⟨hf, ht⟩
  · simp [hf]
  · rw [hf, ht]; rfl

/-- Entry `t` of the real view of hub `w_i` agrees with the slot entry, as far as any good subpart can see. -/
theorem entry_eq {W : UWin} (hW : RealShape W) (hd9 : 9 ≤ W.d) {i : Nat} (hi : i < W.d)
    (h5 : 5 ≤ W.linkL i) (h8 : W.linkL i ≤ 8) {t : Nat} (ht : t < W.linkL i) (s : Sub) (hs : s.Good) :
    s.fit3 ((W.viewW i)[t]'(by simp [UWin.viewW]; exact ht)) =
      s.fit3 (cview (slotSigma W i) (slotEntry (W.linkL i) t)) := by
  have hd : 0 < W.d := by omega
  set L := W.linkL i with hLdef
  set σ := slotSigma W i
  simp only [UWin.viewW, List.getElem_map, List.getElem_range]
  rw [← hLdef]
  by_cases t0 : t = 0
  · subst t0
    have hsp : (W.letter i (wSpokePos L 0)).getD 0 = 9 := by
      simp [wSpokePos, UWin.letter]; omega
    rw [← fit3_u_fans s hs _ hsp []]
    congr 1
    simp only [cview, slotEntry, if_pos rfl, hatRing3, PSpokeView.mk.injEq]
    refine ⟨by rw [hsp]; rfl, ?_, by simp⟩
    have : ¬ (3 ≤ 0 ∧ 0 + 2 ≤ L) := by omega
    simp only [this, decide_false, Bool.false_eq_true, ite_false, Option.map_some]
    have hw : W.letter i (wHatPos L 0) = some (W.linkL (W.idx i 2)) := by simp [wHatPos, UWin.letter]
    rw [hw]
    simp [σ, slotSigma, slotHat, hw, ← hLdef]
  · -- t ≥ 1: the views are equal
    congr 1
    have hsp : ∃ x, W.letter i (wSpokePos L t) = some x := by
      unfold wSpokePos
      rw [if_neg t0]
      split_ifs with h1 h2
      · exact ⟨_, rfl⟩
      · exact ⟨_, rfl⟩
      · apply seg_some hW hd
        rw [idx_self W hi, ← hLdef, npriv_lt8 h5 h8]; omega
    obtain ⟨x, hx⟩ := hsp
    have hσsp : σ (slotSp t) = x := by
      simp only [σ, slotSigma, slotSp, ← hLdef]
      rw [if_neg (by omega), if_pos (by omega), show 100 + t - 100 = t by omega, hx]; rfl
    have hfc : W.fanCount (wSpokePos L t) x = npriv x := by
      unfold wSpokePos; rw [if_neg t0]; split_ifs <;> rfl
    simp only [cview, slotEntry, if_neg t0, PSpokeView.mk.injEq, hσsp, hx, Option.getD_some]
    refine ⟨trivial, ?_, ?_⟩
    · -- hats
      by_cases hr : 3 ≤ t ∧ t + 2 ≤ L
      · have : hatRing3 L t = true := by simp [hatRing3, hr]
        simp only [this, ite_true, Option.map_none]
        unfold wHatPos
        rw [if_neg t0, if_neg (by omega), if_neg (by omega), if_neg (by omega)]; rfl
      · have : hatRing3 L t = false := by simp [hatRing3, hr]
        simp only [this, Bool.false_eq_true, ite_false, Option.map_some]
        have hh : ∃ y, W.letter i (wHatPos L t) = some y := by
          unfold wHatPos
          rw [if_neg t0]
          split_ifs with h1 h2 h3
          · exact ⟨_, rfl⟩
          · simp only [UWin.letter]
            rw [if_pos (by rw [segL_len hW (idx_lt W hd _ _)]; omega)]
            rw [List.getElem?_eq_getElem (by rw [segL_len hW (idx_lt W hd _ _)]; omega)]
            exact ⟨_, rfl⟩
          · exact seg_some hW hd _ _ _ (by omega)
          · omega
        obtain ⟨y, hy⟩ := hh
        have : σ (slotHat t) = y := by
          simp only [σ, slotSigma, slotHat, ← hLdef]
          rw [if_neg (by omega), if_neg (by omega), if_pos (by omega), show 120 + t - 120 = t by omega, hy]; rfl
        rw [this, hy]
    · -- fans
      rw [hfc, List.map_map]
      apply List.map_congr_left
      intro k hk
      have hk' := List.mem_range.1 hk
      have hk3 : k < 4 := by have := npriv_le3 x; omega
      by_cases hr : 2 ≤ t ∧ t + 2 ≤ L
      · have : fanRing3 L t = true := by simp [fanRing3, hr]
        simp only [Function.comp, this, ite_true, Option.map_none]
        unfold wFanPos
        rw [if_neg t0, if_neg (by omega), if_neg (by omega)]; rfl
      · have : fanRing3 L t = false := by simp [fanRing3, hr]
        simp only [Function.comp, this, Bool.false_eq_true, ite_false, Option.map_some]
        have hf : ∃ y, W.letter i (wFanPos L t k) = some y := by
          have ht1 : t = 1 ∨ t + 1 = L := by omega
          unfold wFanPos
          rw [if_neg t0]
          rcases ht1 with rfl | ht1
          · rw [if_pos rfl]
            apply seg_some hW hd
            have : x = W.linkL (W.idx i (-1)) := by
              have : W.letter i (wSpokePos L 1) = some (W.linkL (W.idx i (-1))) := by
                simp [wSpokePos, UWin.letter]
              rw [hx] at this; exact Option.some.inj this
            rw [← this]; omega
          · rw [if_neg (by omega), if_pos ht1]
            apply seg_some hW hd
            have : x = W.linkL (W.idx i 1) := by
              have : W.letter i (wSpokePos L t) = some (W.linkL (W.idx i 1)) := by
                unfold wSpokePos; rw [if_neg t0, if_neg (by omega), if_pos ht1]; rfl
              rw [hx] at this; exact Option.some.inj this
            rw [← this]; omega
        obtain ⟨y, hy⟩ := hf
        have : σ (slotFan t k) = y := by
          simp only [σ, slotSigma, slotFan, ← hLdef]
          rw [if_neg (by omega), if_neg (by omega), if_neg (by omega),
            show (140 + 4 * t + k - 140) / 4 = t by omega, show (140 + 4 * t + k - 140) % 4 = k by omega, hy]; rfl
        rw [this, hy]

theorem foldl_congr_mem {α β : Type} (f g : α → β → α) :
    ∀ (L : List β) (init : α), (∀ a, ∀ b ∈ L, f a b = g a b) → L.foldl f init = L.foldl g init := by
  intro L
  induction L with
  | nil => intro _ _; rfl
  | cons b L ih =>
    intro init h
    simp only [List.foldl_cons]
    rw [h init b List.mem_cons_self]
    exact ih _ (fun a c hc => h a c (List.mem_cons_of_mem _ hc))

theorem fit3At_congr (p : Part) (v1 v2 : List PSpokeView) (hl : v1.length = v2.length)
    (h : ∀ t (h1 : t < v1.length) (h2 : t < v2.length), ∀ s ∈ p.subs, s.fit3 v1[t] = s.fit3 v2[t]) (a : Nat) :
    p.fit3At v1 a = p.fit3At v2 a := by
  unfold Part.fit3At
  rw [hl]
  split_ifs
  · rfl
  · apply foldl_congr_mem
    intro acc j _
    congr 1
    rcases h1 : p.subs[j]? with _ | s
    · rfl
    · have hs := List.mem_of_getElem? h1
      by_cases hlt : 0 < v2.length
      · have hk : (a + j) % v2.length < v2.length := Nat.mod_lt _ hlt
        rw [List.getElem?_eq_getElem hk, List.getElem?_eq_getElem (by omega)]
        exact h _ (by omega) hk s hs
      · have : v2.length = 0 := by omega
        rw [List.getElem?_eq_none (by omega), List.getElem?_eq_none (by omega)]

/-- **`c_i ≤ 6`**: at `d ≥ 9`, at most 6 fits from a hub `w_i` (letter `≤ 8`) into `u` are possible. -/
theorem hub_bound {parts : List Part} (hA : slotAll parts = true) {W : UWin} (hW : RealShape W) (hd9 : 9 ≤ W.d)
    {i : Nat} (hi : i < W.d) (h8 : W.linkL i ≤ 8) :
    (parts.map fun p => if p.hub = W.linkL i then
      (p.fit3At (W.viewW i) (W.linkL i - 2)).possI else 0).sum ≤ 6 := by
  have h5 : 5 ≤ W.linkL i := by
    have hm : W.link[i]? = some (W.linkL i) := by
      have hlt : i < W.link.length := by rw [hW.2.1]; exact hi
      unfold UWin.linkL; rw [getD_lt' _ _ _ hlt]; exact List.getElem?_eq_getElem hlt
    exact (hW.2.2.2.2.1 _ (List.mem_of_getElem? hm)).1
  set L := W.linkL i with hLdef
  have hσ := slotSigma_fix W i
  simp only [slotAll, Bool.and_eq_true] at hA
  obtain ⟨⟨⟨⟨⟨c5, c6⟩, c7⟩, c8⟩, hfe⟩, hws⟩ := hA
  have hall : slotCheck parts L = true := by
    rcases (show L = 5 ∨ L = 6 ∨ L = 7 ∨ L = 8 by omega) with h | h | h | h <;> rw [h]
    exacts [c5, c6, c7, c8]
  have key := slot_bound hall (slotSigma W i) (slotSigma_range hW i)
  refine le_trans (le_of_eq ?_) key
  unfold slotIns
  rw [List.map_map, sum_map_filter]
  congr 1
  apply List.map_congr_left
  intro p hp
  by_cases hh : p.hub = L
  · have hpe := List.all_eq_true.1 hfe p hp
    have hgood := (wellShaped_spec (List.all_eq_true.1 hws p hp)).2.2.2.2.2
    simp only [hh, beq_self_eq_true, ite_true, Function.comp]
    rw [symFit_eval hσ p hpe]
    congr 1
    apply fit3At_congr
    · simp [UWin.viewW, slotView, ← hLdef]
    · intro t h1 _ s hs
      have ht : t < L := by simpa [UWin.viewW, ← hLdef] using h1
      rw [entry_eq hW hd9 hi h5 h8 ht s (hgood s hs)]
      simp only [slotView, List.getElem_map, List.getElem_range]
      rfl
  · have : (p.hub == L) = false := by simpa using hh
    simp [hh, this]

theorem sum_range_le (f : ℕ → ℤ) (c : ℤ) : ∀ n, (∀ i < n, f i ≤ c) → ((List.range n).map f).sum ≤ n * c := by
  intro n
  induction n with
  | zero => intro _; simp
  | succ n ih =>
    intro h
    rw [List.range_succ, List.map_append, List.sum_append]
    have := ih (fun i hi => h i (by omega))
    have := h n (by omega)
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
    push_cast; nlinarith

/-- **Spec §8.4**, any part list passing `slotAll`: at `d ≥ 9`, `hi ≤ 60 − 4d` (RSST units). -/
theorem hiP_le_60_sub_4d {parts : List Part} (hA : slotAll parts = true) {W : UWin} (hW : RealShape W)
    (hd9 : 9 ≤ W.d) : (loHiP parts W).2 ≤ 60 - 4 * (W.d : Int) := by
  rw [loHiP_eq]
  show 10 * (6 - (W.d : Int)) + inX parts W Tri.possI - outX parts W Tri.sureI ≤ _
  have hout : outX parts W Tri.sureI = 0 := by
    unfold outX; rw [if_neg (by omega)]
  have hin : inX parts W Tri.possI ≤ W.d * 6 := by
    unfold inX
    apply sum_range_le
    intro i hi
    split_ifs with h8
    · exact hub_bound hA hW hd9 hi h8
    · norm_num
  rw [hout]; push_cast at hin ⊢; linarith

theorem hi_le_60_sub_4d {W : UWin} (hW : RealShape W) (hd9 : 9 ≤ W.d) : W.loHi.2 ≤ 60 - 4 * (W.d : Int) := by
  rw [loHi_eq]; exact hiP_le_60_sub_4d slotAll_71 hW hd9

/-- **B5 at `d ≥ 15`** (71 parts): no real-shaped word of degree `≥ 15` has `hi > 0`. -/
theorem B5_ge15 (KL : List Conf) : ∀ W : UWin, RealShape W → 15 ≤ W.d → 0 < W.loHi.2 → Kills KL W := by
  intro W hW hd hpos
  have := hi_le_60_sub_4d hW (by omega)
  exfalso; push_cast at this; omega

/-- **B5 at `d ≥ 15`, 79 parts** (71 + N2), against B4's `loHiP rsstParts79`. -/
theorem B5_ge15_79 (KL : List Conf) :
    ∀ W : UWin, RealShape W → 15 ≤ W.d → 0 < (loHiP rsstParts79 W).2 → Kills KL W := by
  intro W hW hd hpos
  have := hiP_le_60_sub_4d slotAll_79 hW (by omega)
  exfalso; push_cast at this; omega

#print axioms slotAll_71
#print axioms slotAll_79
#print axioms hi_le_60_sub_4d
#print axioms B5_ge15
#print axioms B5_ge15_79

end SimpleGraph.SphericalMap.RSSTSeed
