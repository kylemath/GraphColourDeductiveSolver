import RSSTBridge
import RSSTCharge

/-!
# ST-120 B4 M3/M4: evaluation soundness

Studio, 10 Nov. The real discharging transfer on `T` (`tauP parts T`, `tauRSST T = tauP rsstParts T`): every vertex `h`
is a hub; for every anchor `y ∈ N(h)` and every part `p` with `p.hub = deg h` that fits the real hub view
`realView T h y` (spec §3.3, read on `T`), `p.amount` units go from `h` to `rot(h)[p.target]` counted from `y` (the
third spoke). Every (part, hub, anchor) counts on its own (spec §3.3 last line).

**M3** (`eval_sound`): for any part list whose parts are `wellShaped` (B2), for `u` with link listing `w`,
`lo ≤ final T τ u ≤ hi` where `(lo, hi) = loHiP parts (wordOf T u w)` is B2's `UWin.loHi` (equal by `rfl` for
`rsstParts`). Hence `hi ≤ 0 → final ≤ 0` (`final_nonpos_of_hi`), and **M4** (`exists_word_hi_pos`): every
`Internally6` triangulation has a vertex whose word has `hi > 0`, which is what B5 + B6 consume.

Generality (coordinator 16:08Z): the part list is a parameter; amounts are `p.amount : ℕ` RSST units (the scale is
already ×10 of the 6−deg unit, so 0.1/0.2-unit rules fit as integer amounts after a further rescale of `charge0`; not
done here); the soundness of `loHi` uses `amount = 1` and `target = 2` because B2's `loHi` counts one unit per fit at
the third spoke. A sender that is not a neighbour of the receiver (two-step pay-through) is not covered by `tauPart`
(anchors and targets are neighbours of the hub); `final` itself (B1) allows any transfer.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap

variable {n : ℕ}

/-! ## The real transfer -/

/-- What one part moves from hub `h` to `x`: the sum over anchors `y ∈ N(h)` where it fits with receiver `x`. -/
noncomputable def tauPart (T : SphericalMap n) (p : Part) (h x : Fin n) : ℤ :=
  ∑ y ∈ T.graph.neighborFinset h,
    if p.hub = T.graph.degree h ∧ rotNbr T h y p.target = x ∧ fits p (realView T h y) = true then (p.amount : ℤ)
    else 0

/-- The discharging transfer of a part list. -/
noncomputable def tauP (parts : List Part) (T : SphericalMap n) (h x : Fin n) : ℤ :=
  (parts.map fun p => tauPart T p h x).sum

/-- **`τ_RSST`**: the transfer of the 71 RSST parts. -/
noncomputable def tauRSST (T : SphericalMap n) : Fin n → Fin n → ℤ := tauP rsstParts T

/-- The real view reads the spec's hat: if `x` follows `a` in `rot(h)`, then `rot(x)` runs `h, a, …`, so
`rotNbr T x h 2` is the vertex after `a` in `rot(x)`, i.e. `opp(x, a)` (spec §3.3 item 2). -/
theorem realSpoke_reads {T : SphericalMap n} (htri : T.Triangulated) {h a x : Fin n} (hx : Nx T h a x) :
    rotNbr T x h 1 = a :=
  rotNbr_one_of_nx (nx_tri htri hx).1

/-! ## B2's interval as sums -/

/-- One fold step of `UWin.loHi` (copied verbatim). -/
def loHiStep (lh : Int × Int) (f : UWin.Fired) : Int × Int :=
  let s : Int := if f.res == .sure then 1 else 0
  if f.into then (lh.1 + s, lh.2 + 1) else (lh.1 - 1, lh.2 - s)

/-- `UWin.loHi` for a given part list. -/
def loHiP (parts : List Part) (W : UWin) : Int × Int :=
  (W.fired parts).foldl loHiStep (10 * (6 - (W.d : Int)), 10 * (6 - (W.d : Int)))

theorem loHi_eq (W : UWin) : W.loHi = loHiP rsstParts W := rfl

def Tri.sureI (t : Tri) : Int := if t = .sure then 1 else 0
def Tri.possI (t : Tri) : Int := if t = .no then 0 else 1

def loD (f : UWin.Fired) : Int := if f.into then (if f.res == .sure then 1 else 0) else -1
def hiD (f : UWin.Fired) : Int := if f.into then 1 else -(if f.res == .sure then 1 else 0)

theorem foldl_loHiStep (L : List UWin.Fired) (a b : Int) :
    L.foldl loHiStep (a, b) = (a + (L.map loD).sum, b + (L.map hiD).sum) := by
  induction L generalizing a b with
  | nil => simp
  | cons f L ih =>
    simp only [List.foldl_cons, List.map_cons, List.sum_cons]
    have e : loHiStep (a, b) f = (a + loD f, b + hiD f) := by
      unfold loHiStep loD hiD; cases f.into <;> simp only [Bool.false_eq_true, ↓reduceIte, Prod.mk.injEq] <;> constructor <;> ring
    rw [e, ih]; ext <;> simp <;> ring

theorem sum_map_flatMap {α β : Type} (L : List α) (g : α → List β) (F : β → Int) :
    ((L.flatMap g).map F).sum = (L.map fun x => ((g x).map F).sum).sum := by
  induction L with
  | nil => simp
  | cons a L ih => simp [List.flatMap_cons, List.sum_append, ih]

theorem sum_map_filterMap {α β : Type} (L : List α) (g : α → Option β) (F : β → Int) :
    ((L.filterMap g).map F).sum = (L.map fun x => ((g x).map F).getD 0).sum := by
  induction L with
  | nil => simp
  | cons a L ih =>
    rw [List.filterMap_cons]
    cases h : g a <;> simp [h, ih]

theorem sum_map_filter {α : Type} (L : List α) (P : α → Bool) (F : α → Int) :
    ((L.filter P).map F).sum = (L.map fun x => if P x then F x else 0).sum := by
  induction L with
  | nil => simp
  | cons a L ih =>
    rw [List.filter_cons]
    cases h : P a <;> simp [h, ih]

theorem list_sum_range (f : ℕ → ℤ) (m : ℕ) : ((List.range m).map f).sum = ∑ i ∈ Finset.range m, f i := by
  induction m with
  | zero => simp
  | succ m ih => rw [List.range_succ, List.map_append, List.sum_append, ih, Finset.sum_range_succ]; simp

theorem finset_list_comm {α ι : Type*} (s : Finset ι) (L : List α) (g : α → ι → ℤ) :
    ∑ i ∈ s, (L.map fun p => g p i).sum = (L.map fun p => ∑ i ∈ s, g p i).sum := by
  induction L with
  | nil => simp
  | cons a L ih => simp [Finset.sum_add_distrib, ih]

theorem univ_list_comm {α : Type*} (L : List α) (g : α → Fin n → ℤ) :
    ∑ x, (L.map fun p => g p x).sum = (L.map fun p => ∑ x, g p x).sum :=
  finset_list_comm _ L g

/-- B2's interval, as sums over attempts: `lo = base + inX sureI − outX possI`, `hi = base + inX possI − outX sureI`. -/
def outX (parts : List Part) (W : UWin) (X : Tri → Int) : Int :=
  if 5 ≤ W.d ∧ W.d ≤ 8 then
    (parts.map fun p => if p.hub = W.d then ((List.range W.d).map fun a => X (p.fit3At W.viewU a)).sum else 0).sum
  else 0

def inX (parts : List Part) (W : UWin) (X : Tri → Int) : Int :=
  ((List.range W.d).map fun i =>
    if W.linkL i ≤ 8 then
      (parts.map fun p => if p.hub = W.linkL i then X (p.fit3At (W.viewW i) (W.linkL i - 2)) else 0).sum
    else 0).sum

theorem sum_map_filter_filterMap {α β : Type} (L : List α) (P : α → Bool) (g : α → Option β) (F : β → Int) :
    (((L.filter P).filterMap g).map F).sum = (L.map fun x => if P x then ((g x).map F).getD 0 else 0).sum := by
  rw [sum_map_filterMap, sum_map_filter]

theorem pt_out_lo (r : Tri) (tag : String) (recv : Nat) :
    ((if r = Tri.no then none else some (⟨tag, none, recv, false, r⟩ : UWin.Fired)).map loD).getD 0 =
      -r.possI := by cases r <;> rfl

theorem pt_out_hi (r : Tri) (tag : String) (recv : Nat) :
    ((if r = Tri.no then none else some (⟨tag, none, recv, false, r⟩ : UWin.Fired)).map hiD).getD 0 =
      -r.sureI := by cases r <;> rfl

theorem pt_in_lo (r : Tri) (tag : String) (hub : Option Nat) :
    ((if r = Tri.no then none else some (⟨tag, hub, 0, true, r⟩ : UWin.Fired)).map loD).getD 0 =
      r.sureI := by cases r <;> rfl

theorem pt_in_hi (r : Tri) (tag : String) (hub : Option Nat) :
    ((if r = Tri.no then none else some (⟨tag, hub, 0, true, r⟩ : UWin.Fired)).map hiD).getD 0 =
      r.possI := by cases r <;> rfl

theorem map_ite_nil_sum {β : Type} (c : Prop) [Decidable c] (L : List β) (F : β → Int) :
    ((if c then L else []).map F).sum = if c then (L.map F).sum else 0 := by
  split <;> simp

theorem list_sum_neg {α : Type} (L : List α) (f : α → Int) : (L.map fun a => -f a).sum = -(L.map f).sum := by
  induction L with
  | nil => simp
  | cons a L ih => simp [ih]; ring

theorem list_sum_ite_neg {α : Type} (L : List α) (c : α → Prop) [DecidablePred c] (f : α → Int) :
    (L.map fun a => if c a then -f a else 0).sum = -(L.map fun a => if c a then f a else 0).sum := by
  induction L with
  | nil => simp
  | cons a L ih => by_cases h : c a <;> simp [h, ih] <;> ring

theorem loHiP_eq (parts : List Part) (W : UWin) :
    loHiP parts W = (10 * (6 - (W.d : Int)) + inX parts W Tri.sureI - outX parts W Tri.possI,
      10 * (6 - (W.d : Int)) + inX parts W Tri.possI - outX parts W Tri.sureI) := by
  unfold loHiP
  rw [foldl_loHiStep]
  unfold UWin.fired
  unfold outX inX
  split_ifs with hd
  · simp only [List.map_append, List.sum_append, sum_map_flatMap, sum_map_filter, sum_map_filterMap,
      map_ite_nil_sum, pt_out_lo, pt_out_hi, pt_in_lo, pt_in_hi, beq_iff_eq, list_sum_neg, list_sum_ite_neg]
    ext <;> simp only <;> ring
  · simp only [List.map_append, List.sum_append, sum_map_flatMap, sum_map_filter, sum_map_filterMap,
      map_ite_nil_sum, pt_in_lo, pt_in_hi, beq_iff_eq, List.map_nil, List.sum_nil]
    ext <;> simp only <;> ring

/-! ## Soundness of one attempt -/

theorem ite_and_left {c : Prop} [Decidable c] (hc : c) (b : Bool) (a : ℤ) :
    (if c ∧ b = true then a else 0) = (if b = true then a else 0) := by
  by_cases hb : b = true
  · rw [if_pos ⟨hc, hb⟩, if_pos hb]
  · rw [if_neg (fun h => hb h.2), if_neg hb]

theorem Tri.Sound.bounds {t : Tri} {b : Bool} (h : t.Sound b) :
    t.sureI ≤ (if b = true then 1 else 0) ∧ (if b = true then 1 else 0) ≤ t.possI := by
  obtain ⟨h1, h2⟩ := h
  cases t <;> cases b <;> simp_all [Tri.sureI, Tri.possI]

section
variable {T : SphericalMap n} {u : Fin n} {d : ℕ} {w : ℕ → Fin n}

/-- What leaves a hub, summed over receivers: one term per anchor. -/
theorem sum_tauPart_out (p : Part) (h : Fin n) :
    ∑ x, tauPart T p h x = ∑ y ∈ T.graph.neighborFinset h,
      if p.hub = T.graph.degree h ∧ fits p (realView T h y) = true then (p.amount : ℤ) else 0 := by
  unfold tauPart
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro y _
  rw [Finset.sum_eq_single (rotNbr T h y p.target)]
  · simp
  · intro b _ hb
    rw [if_neg]
    rintro ⟨-, e, -⟩
    exact hb e.symm
  · intro hm; exact absurd (Finset.mem_univ _) hm

variable (hT : ClaimGlue.Internally6 T) (hL : IsLink T u d w)
include hT hL

/-- What reaches `u`: only from a link vertex `w_i`, at the anchor `rot(w_i)[D-2]` (two before `u`). -/
theorem sum_tauPart_in (p : Part) (hp : p.target = 2) :
    ∑ x, tauPart T p x u = ∑ i ∈ Finset.range d,
      if p.hub = T.graph.degree (w i) ∧
        fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))) = true then (p.amount : ℤ) else 0 := by
  classical
  have hsub : ∑ x ∈ T.graph.neighborFinset u, tauPart T p x u = ∑ x, tauPart T p x u := by
    apply Finset.sum_subset (Finset.subset_univ _)
    intro x _ hx
    unfold tauPart
    apply Finset.sum_eq_zero
    intro y hy
    rw [if_neg]
    rintro ⟨-, e, -⟩
    apply hx
    have := rotNbr_adj ((mem_neighborFinset _ _ _).1 hy) p.target
    rw [e] at this
    exact (mem_neighborFinset _ _ _).2 this.symm
  rw [← hsub, sum_nbr_link hL]
  apply Finset.sum_congr rfl
  intro i _
  unfold tauPart
  have hwu : T.Adj (w i) u := (hL.adj i).symm
  rw [sum_nbr_link (rotNbr_isLink hwu)]
  have hD5 := hT.minDeg (w i)
  rw [Finset.sum_eq_single (T.graph.degree (w i) - 2)]
  · rw [hp, rotNbr_add hwu, show T.graph.degree (w i) - 2 + 2 = 0 + T.graph.degree (w i) by omega, rotNbr_per hwu,
      rotNbr_zero hwu]
    simp
  · intro a ha hne
    rw [if_neg]
    rintro ⟨-, e, -⟩
    rw [hp, rotNbr_add hwu] at e
    have hm := ((rotNbr_isLink hwu).eq_iff (by omega) (a + 2) 0).1 (e.trans (rotNbr_zero hwu).symm)
    have ha' := Finset.mem_range.1 ha
    rcases (show a + 2 < T.graph.degree (w i) ∨ a + 2 = 1 + T.graph.degree (w i) ∨
        a + 2 = T.graph.degree (w i) by omega) with h | h | h
    · rw [Nat.mod_eq_of_lt h, Nat.zero_mod] at hm; omega
    · rw [h, Nat.add_mod_right, Nat.mod_eq_of_lt (by omega), Nat.zero_mod] at hm; omega
    · omega
  · intro h; exact absurd (Finset.mem_range.2 (by omega)) h

/-- One attempt at hub `u`, anchor `w_a`. -/
theorem sound_out (p : Part) (hgood : ∀ s ∈ p.subs, s.Good) {a : ℕ} (ha : a < d) :
    (p.fit3At (wordOf T u w).viewU a).Sound (fits p (realView T u (w a))) := by
  have d5 := hL.d5 hT
  have hd : 0 < d := by omega
  have hl1 : (wordOf T u w).viewU.length = d := by simp [UWin.viewU, word_d hL]
  have hl2 : (realView T u (w a)).length = d := by simp [realView, hL.deg]
  apply sound_part p hgood _ _ a (by rw [hl1, hl2])
  intro j hj
  rw [hl2] at hj
  obtain ⟨x, hx, hax⟩ := approxU hT hL (Nat.mod_lt (a + j) hd)
  refine ⟨x, _, by rw [hl1]; exact hx, ?_, hax⟩
  rw [realView, List.getElem?_map, List.getElem?_range (by rw [hL.deg]; exact hj), Option.map_some,
    rot_u_link hT hL, hL.per_mod]

/-- One attempt at hub `w_i` (`deg ≤ 8`), target `u`. -/
theorem sound_in (p : Part) (hgood : ∀ s ∈ p.subs, s.Good) {i : ℕ} (hi : i < d)
    (hD : T.graph.degree (w i) ≤ 8) :
    (p.fit3At ((wordOf T u w).viewW i) ((wordOf T u w).linkL i - 2)).Sound
      (fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2)))) := by
  have hn : (wordOf T u w).linkL i = T.graph.degree (w i) := by rw [word_linkL hL hi, letterOf_le8 hD]
  have hD5 := hT.minDeg (w i)
  have hwu : T.Adj (w i) u := (hL.adj i).symm
  have hl1 : ((wordOf T u w).viewW i).length = T.graph.degree (w i) := by simp [UWin.viewW, hn]
  have hl2 : (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))).length = T.graph.degree (w i) := by
    simp [realView]
  rw [hn]
  apply sound_part p hgood _ _ _ (by rw [hl1, hl2])
  intro j hj
  rw [hl2] at hj
  obtain ⟨x, hx, hax⟩ := approxW hT hL hi hD (Nat.mod_lt (T.graph.degree (w i) - 2 + j) (by omega))
  refine ⟨x, _, by rw [hl1]; exact hx, ?_, hax⟩
  rw [realView, List.getElem?_map, List.getElem?_range hj, Option.map_some, rotNbr_add hwu,
    (rotNbr_isLink hwu).per_mod]

/-! ## M3 -/

/-- **M3, evaluation soundness.** For any list of well-shaped parts, `u`'s real final charge under the real transfer
lies in B2's interval for the word read off `T`. -/
theorem eval_sound (parts : List Part) (hP : ∀ p ∈ parts, p.wellShaped = true) :
    (loHiP parts (wordOf T u w)).1 ≤ final T (tauP parts T) u ∧
      final T (tauP parts T) u ≤ (loHiP parts (wordOf T u w)).2 := by
  have d5 := hL.d5 hT
  have hWd : (wordOf T u w).d = d := word_d hL
  have spec := fun p hp => wellShaped_spec (hP p hp)
  -- the real outflow and inflow
  obtain ⟨OUT, hOUT⟩ : ∃ X, X = (parts.map fun p => ∑ a ∈ Finset.range d,
    if p.hub = d ∧ fits p (realView T u (w a)) = true then (p.amount : ℤ) else 0).sum := ⟨_, rfl⟩
  obtain ⟨IN, hIN⟩ : ∃ X, X = ∑ i ∈ Finset.range d, (parts.map fun p =>
    if p.hub = T.graph.degree (w i) ∧
      fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))) = true then (p.amount : ℤ) else 0).sum :=
    ⟨_, rfl⟩
  have hout : ∑ x, tauP parts T u x = OUT := by
    unfold tauP; rw [univ_list_comm, hOUT]; congr 1; apply List.map_congr_left; intro p _
    rw [sum_tauPart_out, sum_nbr_link hL, hL.deg]
  have hin : ∑ x, tauP parts T x u = IN := by
    unfold tauP; rw [univ_list_comm, hIN, finset_list_comm]; congr 1; apply List.map_congr_left; intro p hp
    exact sum_tauPart_in hT hL p (spec p hp).2.2.2.1
  -- bounds on the outflow
  have bout : outX parts (wordOf T u w) Tri.sureI ≤ OUT ∧ OUT ≤ outX parts (wordOf T u w) Tri.possI := by
    unfold outX
    rw [hWd, hOUT]
    split_ifs with hd'
    · constructor
      · apply List.sum_le_sum; intro p hp
        by_cases hh : p.hub = d
        · rw [if_pos hh, list_sum_range]; apply Finset.sum_le_sum; intro a ha
          rw [ite_and_left hh, (spec p hp).2.2.2.2.1, Nat.cast_one]
          exact (sound_out hT hL p (spec p hp).2.2.2.2.2 (Finset.mem_range.1 ha)).bounds.1
        · rw [if_neg hh, Finset.sum_eq_zero (fun a _ => if_neg (fun h => hh h.1))]
      · apply List.sum_le_sum; intro p hp
        by_cases hh : p.hub = d
        · rw [if_pos hh, list_sum_range]; apply Finset.sum_le_sum; intro a ha
          rw [ite_and_left hh, (spec p hp).2.2.2.2.1, Nat.cast_one]
          exact (sound_out hT hL p (spec p hp).2.2.2.2.2 (Finset.mem_range.1 ha)).bounds.2
        · rw [if_neg hh, Finset.sum_eq_zero (fun a _ => if_neg (fun h => hh h.1))]
    · have h0 : (parts.map fun p => ∑ a ∈ Finset.range d,
            if p.hub = d ∧ fits p (realView T u (w a)) = true then (p.amount : ℤ) else 0).sum = 0 := by
        have : ∀ p ∈ parts, (∑ a ∈ Finset.range d,
            if p.hub = d ∧ fits p (realView T u (w a)) = true then (p.amount : ℤ) else 0) = 0 := by
          intro p hp
          apply Finset.sum_eq_zero; intro a _
          rw [if_neg]; rintro ⟨hh, -⟩; have := (spec p hp).2.1; omega
        rw [List.map_congr_left this]; simp
      rw [h0]; exact ⟨le_refl _, le_refl _⟩
  -- bounds on the inflow
  have key : ∀ i, i < d → ∀ p ∈ parts,
      (if (wordOf T u w).linkL i ≤ 8 then (if p.hub = (wordOf T u w).linkL i then
        (p.fit3At ((wordOf T u w).viewW i) ((wordOf T u w).linkL i - 2)).sureI else 0) else 0) ≤
        (if p.hub = T.graph.degree (w i) ∧
          fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))) = true then (p.amount : ℤ) else 0) ∧
      (if p.hub = T.graph.degree (w i) ∧
          fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))) = true then (p.amount : ℤ) else 0) ≤
        (if (wordOf T u w).linkL i ≤ 8 then (if p.hub = (wordOf T u w).linkL i then
          (p.fit3At ((wordOf T u w).viewW i) ((wordOf T u w).linkL i - 2)).possI else 0) else 0) := by
    intro i hi' p hp
    by_cases hD : T.graph.degree (w i) ≤ 8
    · have hn : (wordOf T u w).linkL i = T.graph.degree (w i) := by rw [word_linkL hL hi', letterOf_le8 hD]
      have hb := (sound_in hT hL p (spec p hp).2.2.2.2.2 hi' hD).bounds
      rw [hn] at hb ⊢
      simp only [if_pos hD]
      by_cases hh : p.hub = T.graph.degree (w i)
      · simp only [if_pos hh, ite_and_left hh, (spec p hp).2.2.2.2.1, Nat.cast_one]
        exact hb
      · have hh' : ¬ (p.hub = T.graph.degree (w i) ∧
          fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))) = true) := fun h => hh h.1
        simp only [if_neg hh, if_neg hh']; exact ⟨le_refl _, le_refl _⟩
    · have hn : (wordOf T u w).linkL i = 9 := by rw [word_linkL hL hi', letterOf_eq9 hD]
      have h98 : ¬ (9 ≤ 8) := by omega
      have hh' : ¬ (p.hub = T.graph.degree (w i) ∧
          fits p (realView T (w i) (rotNbr T (w i) u (T.graph.degree (w i) - 2))) = true) := by
        rintro ⟨hh, -⟩; have := (spec p hp).2.1; omega
      simp only [hn, if_neg h98, if_neg hh']
      exact ⟨le_refl _, le_refl _⟩
  have ite_sum : ∀ (c : Prop) [Decidable c] (L : List Part) (f : Part → ℤ),
      (if c then (L.map f).sum else 0) = (L.map fun p => if c then f p else 0).sum := by
    intro c _ L f
    by_cases hc : c
    · simp only [hc, if_true]
    · simp only [hc, if_false]; induction L with
      | nil => rfl
      | cons a L ih => rw [List.map_cons, List.sum_cons, ← ih]; simp
  have bin : inX parts (wordOf T u w) Tri.sureI ≤ IN ∧ IN ≤ inX parts (wordOf T u w) Tri.possI := by
    unfold inX
    rw [hWd, list_sum_range, list_sum_range, hIN]
    constructor <;> apply Finset.sum_le_sum <;> intro i hi <;> rw [ite_sum] <;> apply List.sum_le_sum <;>
      intro p hp
    · exact (key i (Finset.mem_range.1 hi) p hp).1
    · exact (key i (Finset.mem_range.1 hi) p hp).2
  rw [loHiP_eq]
  unfold final
  rw [hout, hin]
  have hc : charge0 T u = 10 * (6 - ((wordOf T u w).d : ℤ)) := by unfold charge0; rfl
  rw [hc]
  constructor <;> simp only <;> linarith [bout.1, bout.2, bin.1, bin.2]

/-- **M3 for the 71 RSST parts**: `lo ≤ final ≤ hi` with B2's own `UWin.loHi`. -/
theorem eval_sound_rsst :
    (wordOf T u w).loHi.1 ≤ final T (tauRSST T) u ∧ final T (tauRSST T) u ≤ (wordOf T u w).loHi.2 := by
  rw [loHi_eq]
  exact eval_sound hT hL rsstParts (fun p hp => List.all_eq_true.1 rsstParts_wellShaped p hp)

/-- **The direction B5 needs**: `hi ≤ 0` for the word forces `final ≤ 0`. -/
theorem final_nonpos_of_hi (h : (wordOf T u w).loHi.2 ≤ 0) : final T (tauRSST T) u ≤ 0 :=
  le_trans (eval_sound_rsst hT hL).2 h

end

/-! ## M4: what B5 / B6 consume -/

/-- Every vertex has a link listing (from any neighbour). -/
theorem exists_link {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) (u : Fin n) :
    ∃ w, IsLink T u (T.graph.degree u) w := by
  obtain ⟨a, ha⟩ := (T.graph.degree_pos_iff_exists_adj u).1 (by have := hT.minDeg u; omega)
  exact ⟨rotNbr T u a, rotNbr_isLink ha⟩

/-- **M4.** Some vertex of an `Internally6` triangulation has a word with `hi > 0` (B1 + M3). B5's fixed-point check
("every real-shaped word with `hi > 0` contains a K633 configuration") then applies to that word, and B6 turns the
containment into an occurrence in `T`. -/
theorem exists_word_hi_pos {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ 0 < (wordOf T u w).loHi.2 := by
  obtain ⟨a, ha⟩ := (T.graph.degree_pos_iff_exists_adj ⟨0, hT.pos⟩).1 (by have := hT.minDeg ⟨0, hT.pos⟩; omega)
  obtain ⟨u, hu⟩ := exists_pos_final hT.triangulated ⟨(⟨0, hT.pos⟩, a), ha⟩ (tauRSST T)
  obtain ⟨w, hL⟩ := exists_link hT u
  exact ⟨u, w, hL, lt_of_lt_of_le hu (eval_sound_rsst hT hL).2⟩

/-- **M4, the B5 interface.** If a property `Kills` (B5: "contains a K633 configuration") holds for every word with
`hi > 0` and the shape of a real word (`RealShape`, below), then some real word in `T` has it. -/
def RealShape (W : UWin) : Prop :=
  5 ≤ W.d ∧ W.link.length = W.d ∧ W.apex.length = W.d ∧ W.priv.length = W.d ∧
  (∀ x ∈ W.link, 5 ≤ x ∧ x ≤ 9) ∧ (∀ x ∈ W.apex, 5 ≤ x ∧ x ≤ 9) ∧
  (∀ i, i < W.d → (W.priv.getD i []).length = npriv (W.linkL i) ∧ ∀ x ∈ W.priv.getD i [], 5 ≤ x ∧ x ≤ 9)

theorem letterOf_range {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) (x : Fin n) :
    5 ≤ letterOf T x ∧ letterOf T x ≤ 9 :=
  ⟨le_min (hT.minDeg x) (by norm_num), min_le_right _ _⟩

theorem wordOf_realShape {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) {u : Fin n} {w : ℕ → Fin n}
    (hL : IsLink T u (T.graph.degree u) w) : RealShape (wordOf T u w) := by
  refine ⟨hT.minDeg u, by simp [wordOf], by simp [wordOf], by simp [wordOf], ?_, ?_, ?_⟩
  · intro x hx; simp only [wordOf, List.mem_map] at hx; obtain ⟨i, -, rfl⟩ := hx; exact letterOf_range hT _
  · intro x hx; simp only [wordOf, List.mem_map] at hx; obtain ⟨i, -, rfl⟩ := hx; exact letterOf_range hT _
  · intro i hi
    rw [word_priv hL hi, word_linkL hL hi]
    have h5 := hT.minDeg (w i)
    unfold privL
    split_ifs with hD
    · refine ⟨by simp [letterOf_le8 hD, npriv_le8 h5 hD], ?_⟩
      intro x hx; simp only [List.mem_map] at hx; obtain ⟨k, -, rfl⟩ := hx; exact letterOf_range hT _
    · refine ⟨by simp [letterOf_eq9 hD]; rfl, ?_⟩
      intro x hx
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hx
      rcases hx with rfl | rfl | rfl
      · exact letterOf_range hT _
      · exact ⟨by norm_num, le_refl _⟩
      · exact letterOf_range hT _

theorem seed_of_B5 {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) (Kills : UWin → Prop)
    (hB5 : ∀ W : UWin, RealShape W → 0 < W.loHi.2 → Kills W) :
    ∃ u w, IsLink T u (T.graph.degree u) w ∧ Kills (wordOf T u w) := by
  obtain ⟨u, w, hL, hpos⟩ := exists_word_hi_pos hT
  exact ⟨u, w, hL, hB5 _ (wordOf_realShape hT hL) hpos⟩

#print axioms eval_sound
#print axioms eval_sound_rsst
#print axioms final_nonpos_of_hi
#print axioms exists_word_hi_pos
#print axioms seed_of_B5

end SimpleGraph.SphericalMap.RSSTSeed
