import DCheckR2B
import DCheckR1T

/-! Job 19 piece (E), abstract part: from a ring colour sequence `f` and an equivalence `E` on ring
positions ("same θ-Kempe chain") with the local properties of Kempe chains on a ring face, build a
`matchTable` labelling whose regions are unions of chains, and identify the ring code of a chain flip
with `k ^^^ flipMask …`. No geometry here: the planar input is the hypothesis `hNC`. -/
namespace DCheck.R2

/-- The θ-class of a colour. -/
def cls (θ x : Nat) : Nat := min x (x ^^^ θ)

set_option synthInstance.maxSize 2048 in
set_option synthInstance.maxHeartbeats 400000 in
theorem cls_two' : ∀ θ, θ < 4 → ∀ x, x < 4 → ∀ y, y < 4 → ∀ z, z < 4 →
    (1 ≤ θ ∧ cls θ x ≠ cls θ y ∧ cls θ x ≠ cls θ z) → cls θ y = cls θ z := by
  decide

theorem cls_two (θ : Nat) (h1 : 1 ≤ θ) (h3 : θ ≤ 3) (x y z : Nat) (hx : x < 4) (hy : y < 4)
    (hz : z < 4) : cls θ x ≠ cls θ y → cls θ x ≠ cls θ z → cls θ y = cls θ z :=
  fun a b => cls_two' θ (by omega) x hx y hy z hz ⟨h1, a, b⟩

theorem cls_iff' : ∀ θ, θ < 4 → 1 ≤ θ → ∀ x, x < 4 → ∀ y, y < 4 →
    ((x ^^^ y != 0 && x ^^^ y != θ) = false ↔ cls θ x = cls θ y) := by
  decide

theorem cls_iff (θ : Nat) (h1 : 1 ≤ θ) (h3 : θ ≤ 3) (x y : Nat) (hx : x < 4) (hy : y < 4) :
    ((x ^^^ y != 0 && x ^^^ y != θ) = false ↔ cls θ x = cls θ y) :=
  cls_iff' θ (by omega) h1 x hx y hy

/-! ### Counting the elements of a list below a bound -/

def cntL (L : List Nat) (v : Nat) : Nat := L.countP (fun u => decide (u < v))

theorem cntL_succ (L : List Nat) (hL : L.Nodup) (v : Nat) :
    cntL L (v + 1) = cntL L v + (if v ∈ L then 1 else 0) := by
  induction L with
  | nil => simp [cntL]
  | cons a L ih =>
    have hL' := (List.nodup_cons.1 hL)
    have ih := ih hL'.2
    simp only [cntL, List.countP_cons] at ih ⊢
    rw [ih]
    by_cases h3 : a = v
    · subst h3
      have h2 : a ∉ L := hL'.1
      simp [h2]
    · have hm : (v ∈ a :: L) ↔ v ∈ L := by simp [Ne.symm h3]
      rw [if_congr hm rfl rfl]
      by_cases h1 : a < v
      · simp [h1, show a < v + 1 by omega]; omega
      · simp [h1, show ¬ a < v + 1 by omega]

/-- In a strictly increasing list, `L[i]` has exactly `i` elements below it. -/
theorem cntL_get (L : List Nat) (hL : L.Pairwise (· < ·)) :
    ∀ i (h : i < L.length), cntL L L[i] = i := by
  induction L with
  | nil => intro i h; simp at h
  | cons a L ih =>
    intro i h
    have hp := List.pairwise_cons.1 hL
    cases i with
    | zero =>
      simp only [cntL, List.getElem_cons_zero, List.countP_cons, Nat.lt_irrefl, decide_false]
      have : L.countP (fun u => decide (u < a)) = 0 := by
        rw [List.countP_eq_zero]; intro u hu; have := hp.1 u hu; simp; omega
      simp [this]
    | succ i =>
      simp only [List.length_cons] at h
      have hlt : a < L[i] := hp.1 _ (List.getElem_mem _)
      have := ih hp.2 i (by omega)
      simp only [cntL, List.getElem_cons_succ, List.countP_cons] at this ⊢
      simp [hlt, this]

theorem cntL_le (L : List Nat) (v : Nat) : cntL L v ≤ L.length := List.countP_le_length

theorem cntL_all (L : List Nat) (v : Nat) (h : ∀ u ∈ L, u < v) : cntL L v = L.length := by
  unfold cntL; rw [List.countP_eq_length]; intro u hu; simpa using h u hu

/-! ### Transitions as a list -/

def tPred (r k θ : Nat) (v : Nat) : Bool :=
  (col k v ^^^ col k ((v + 1) % r) != 0 && col k v ^^^ col k ((v + 1) % r) != θ)

theorem transitions_toList (r k θ : Nat) :
    (transitions r k θ).toList = (List.range r).filter (tPred r k θ) := by
  unfold transitions tPred; simp [Array.toList_filter, Array.toList_range]

section abstract

variable (r θ : Nat) (f : Nat → Nat)

/-- The transition list of the code of `f`. -/
abbrev TL : List Nat := (List.range r).filter (tPred r (code f r) θ)

theorem TL_pairwise : (TL r θ f).Pairwise (· < ·) :=
  (List.pairwise_lt_range).filter _

theorem TL_nodup : (TL r θ f).Nodup := (TL_pairwise r θ f).imp (fun h => Nat.ne_of_lt h)

theorem mem_TL (v : Nat) : v ∈ TL r θ f ↔ v < r ∧ tPred r (code f r) θ v = true := by
  simp [TL]

variable (hf : ∀ t, f t < 4) (hθ1 : 1 ≤ θ) (hθ3 : θ ≤ 3)
include hf hθ1 hθ3

theorem tPred_iff (v : Nat) (hv : v < r) :
    tPred r (code f r) θ v = false ↔ cls θ (f v) = cls θ (f ((v + 1) % r)) := by
  unfold tPred
  rw [col_code f hf r v hv, col_code f hf r _ (Nat.mod_lt _ (by omega))]
  exact cls_iff θ hθ1 hθ3 _ _ (hf _) (hf _)

/-- (P1) The class of position `v` is the class of position 0 iff an even number of transitions
lie before `v`. -/
theorem cls_parity : ∀ v, v < r → (cls θ (f v) = cls θ (f 0) ↔ cntL (TL r θ f) v % 2 = 0) := by
  intro v
  induction v with
  | zero => intro _; simp [cntL]
  | succ v ih =>
    intro hv
    have ih := ih (by omega)
    rw [cntL_succ _ (TL_nodup r θ f)]
    have hm : v ∈ TL r θ f ↔ tPred r (code f r) θ v = true := by
      rw [mem_TL]; exact ⟨fun h => h.2, fun h => ⟨by omega, h⟩⟩
    have hstep := tPred_iff r θ f hf hθ1 hθ3 v (by omega)
    rw [Nat.mod_eq_of_lt hv] at hstep
    have two := cls_two θ hθ1 hθ3
    by_cases ht : tPred r (code f r) θ v = true
    · have hne : cls θ (f v) ≠ cls θ (f (v + 1)) := by
        intro h; rw [← hstep] at h; simp [h] at ht
      simp only [hm.2 ht, ite_true]
      constructor
      · intro h
        have : cls θ (f v) ≠ cls θ (f 0) := fun h' => hne (h'.trans h.symm)
        have := (not_congr ih).1 this; omega
      · intro h
        have : cntL (TL r θ f) v % 2 ≠ 0 := by omega
        have h1 := (not_congr ih).2 this
        exact (two (f v) (f (v + 1)) (f 0) (hf _) (hf _) (hf _) hne h1)
    · have hht : tPred r (code f r) θ v = false := by simpa using ht
      have heq := hstep.1 hht
      have : v ∉ TL r θ f := fun h => ht (hm.1 h)
      simp only [this, ite_false, Nat.add_zero]
      rw [← heq]; exact ih

omit hf hθ1 hθ3 in
theorem cntL_TL_r : cntL (TL r θ f) r = (TL r θ f).length :=
  cntL_all _ _ (fun u hu => ((mem_TL r θ f u).1 hu).1)

/-- The number of transitions is even. -/
theorem TL_even (hr : 1 ≤ r) : (TL r θ f).length % 2 = 0 := by
  rw [← cntL_TL_r]
  have hlast := cls_parity r θ f hf hθ1 hθ3 (r - 1) (by omega)
  have hstep := tPred_iff r θ f hf hθ1 hθ3 (r - 1) (by omega)
  rw [show r - 1 + 1 = r by omega, Nat.mod_self] at hstep
  have key := cntL_succ (TL r θ f) (TL_nodup r θ f) (r - 1)
  rw [show r - 1 + 1 = r by omega] at key
  rw [key]
  have hm : r - 1 ∈ TL r θ f ↔ tPred r (code f r) θ (r - 1) = true := by
    rw [mem_TL]; exact ⟨fun h => h.2, fun h => ⟨by omega, h⟩⟩
  by_cases ht : tPred r (code f r) θ (r - 1) = true
  · simp only [hm.2 ht, ite_true]
    have : cls θ (f (r - 1)) ≠ cls θ (f 0) := by
      intro h; rw [← hstep] at h; simp [h] at ht
    have := (not_congr hlast).1 this; omega
  · have hht : tPred r (code f r) θ (r - 1) = false := by simpa using ht
    have : r - 1 ∉ TL r θ f := fun h => ht (hm.1 h)
    simp only [this, ite_false, Nat.add_zero]
    exact hlast.1 (hstep.1 hht)

end abstract


/-! ### Arcs, representatives, and chain labels -/

section arcs

variable (r θ : Nat) (f : Nat → Nat)

theorem transitions_size : (transitions r (code f r) θ).size = (TL r θ f).length := by
  rw [← Array.length_toList, transitions_toList]

theorem filter_size (T : Array Nat) (v : Nat) :
    (T.filter (· < v)).size = (T.toList.filter (· < v)).length := by
  rw [← Array.length_toList, Array.toList_filter]

theorem arcOf_eq (v : Nat) : arcOf (transitions r (code f r) θ) v =
    (cntL (TL r θ f) v + (TL r θ f).length - 1) % (TL r θ f).length := by
  unfold arcOf
  rw [filter_size, transitions_toList, transitions_size, cntL, List.countP_eq_length_filter]

/-- The representative position of arc `j`: its last position, `L[(j+1) mod 2p]`. -/
def rep (j : Nat) : Nat := (TL r θ f)[(j + 1) % (TL r θ f).length]!

theorem rep_spec (hn : (TL r θ f).length ≠ 0) (j : Nat) :
    rep r θ f j < r ∧ cntL (TL r θ f) (rep r θ f j) = (j + 1) % (TL r θ f).length := by
  have hi : (j + 1) % (TL r θ f).length < (TL r θ f).length := Nat.mod_lt _ (by omega)
  unfold rep
  rw [getElem!_pos (TL r θ f) _ hi]
  exact ⟨((mem_TL r θ f _).1 (List.getElem_mem hi)).1, cntL_get _ (TL_pairwise r θ f) _ hi⟩

theorem arcOf_rep (hn : (TL r θ f).length ≠ 0) (j : Nat) (hj : j < (TL r θ f).length) :
    arcOf (transitions r (code f r) θ) (rep r θ f j) = j := by
  rw [arcOf_eq, (rep_spec r θ f hn j).2]
  by_cases h : j + 1 < (TL r θ f).length
  · rw [Nat.mod_eq_of_lt h]
    rw [show j + 1 + (TL r θ f).length - 1 = j + (TL r θ f).length by omega, Nat.add_mod_right,
      Nat.mod_eq_of_lt hj]
  · rw [show j + 1 = (TL r θ f).length by omega, Nat.mod_self]
    rw [show 0 + (TL r θ f).length - 1 = j by omega, Nat.mod_eq_of_lt hj]

theorem rep_lt_rep (hn : (TL r θ f).length ≠ 0) (a b : Nat) (hab : a < b)
    (hb : b + 1 < (TL r θ f).length) : rep r θ f a < rep r θ f b := by
  unfold rep
  rw [Nat.mod_eq_of_lt (by omega : a + 1 < _), Nat.mod_eq_of_lt hb,
    getElem!_pos (TL r θ f) _ (by omega), getElem!_pos (TL r θ f) _ hb]
  exact List.pairwise_iff_getElem.1 (TL_pairwise r θ f) _ _ (by omega) hb (by omega)

theorem rep_last_lt (hn : (TL r θ f).length ≠ 0) (a : Nat) (ha : a + 1 < (TL r θ f).length) :
    rep r θ f ((TL r θ f).length - 1) < rep r θ f a := by
  unfold rep
  rw [show (TL r θ f).length - 1 + 1 = (TL r θ f).length by omega, Nat.mod_self,
    Nat.mod_eq_of_lt ha, getElem!_pos (TL r θ f) _ (by omega), getElem!_pos (TL r θ f) _ ha]
  exact List.pairwise_iff_getElem.1 (TL_pairwise r θ f) _ _ (by omega) ha (by omega)

variable (E : Nat → Nat → Prop) (hE : Equivalence E)
  (hstep : ∀ v, v < r → tPred r (code f r) θ v = false → E v ((v + 1) % r))
theorem mem_TL_cnt (v : Nat) (hv : v ∈ TL r θ f) :
    cntL (TL r θ f) v < (TL r θ f).length ∧ (TL r θ f)[cntL (TL r θ f) v]! = v := by
  obtain ⟨i, hi, rfl⟩ := List.getElem_of_mem hv
  rw [cntL_get _ (TL_pairwise r θ f) i hi, getElem!_pos (TL r θ f) i hi]
  exact ⟨hi, rfl⟩

theorem not_mem_TL_iff (v : Nat) (hv : v < r) :
    v ∉ TL r θ f ↔ tPred r (code f r) θ v = false := by
  rw [mem_TL]; simp [hv]

include hE hstep

/-- (C1) a position with a transition at or after it is linked to the first such transition. -/
theorem conn_fwd : ∀ d v, v + d = r - 1 → v < r → cntL (TL r θ f) v < (TL r θ f).length →
    E v (TL r θ f)[cntL (TL r θ f) v]! := by
  intro d
  induction d with
  | zero =>
    intro v hvd hv hc
    by_cases hm : v ∈ TL r θ f
    · rw [(mem_TL_cnt r θ f v hm).2]; exact hE.refl v
    · exfalso
      have key := cntL_succ (TL r θ f) (TL_nodup r θ f) v
      rw [if_neg hm, show v + 1 = r by omega, cntL_TL_r] at key
      omega
  | succ d ih =>
    intro v hvd hv hc
    by_cases hm : v ∈ TL r θ f
    · rw [(mem_TL_cnt r θ f v hm).2]; exact hE.refl v
    · have key := cntL_succ (TL r θ f) (TL_nodup r θ f) v
      rw [if_neg hm, Nat.add_zero] at key
      have h1 := hstep v hv ((not_mem_TL_iff r θ f v hv).1 hm)
      rw [Nat.mod_eq_of_lt (by omega : v + 1 < r)] at h1
      have h2 := ih (v + 1) (by omega) (by omega) (by rw [key]; exact hc)
      rw [key] at h2
      exact hE.trans h1 h2

/-- (C2) a position after the last transition is linked to position 0 (through the wrap edge). -/
theorem conn_wrap : ∀ d v, v + d = r - 1 → v < r → cntL (TL r θ f) v = (TL r θ f).length →
    E v 0 := by
  intro d
  induction d with
  | zero =>
    intro v hvd hv hc
    have hm : v ∉ TL r θ f := fun h => by
      have := (mem_TL_cnt r θ f v h).1; omega
    have h1 := hstep v hv ((not_mem_TL_iff r θ f v hv).1 hm)
    rwa [show v + 1 = r by omega, Nat.mod_self] at h1
  | succ d ih =>
    intro v hvd hv hc
    have hm : v ∉ TL r θ f := fun h => by
      have := (mem_TL_cnt r θ f v h).1; omega
    have key := cntL_succ (TL r θ f) (TL_nodup r θ f) v
    rw [if_neg hm, Nat.add_zero] at key
    have h1 := hstep v hv ((not_mem_TL_iff r θ f v hv).1 hm)
    rw [Nat.mod_eq_of_lt (by omega : v + 1 < r)] at h1
    exact hE.trans h1 (ih (v + 1) (by omega) (by omega) (by rw [key]; exact hc))

/-- Every ring position is linked to the representative of its arc. -/
theorem conn_rep (hn : (TL r θ f).length ≠ 0) (v : Nat) (hv : v < r) :
    E v (rep r θ f (arcOf (transitions r (code f r) θ) v)) := by
  rw [arcOf_eq]
  have hle := cntL_le (TL r θ f) v
  unfold rep
  by_cases hc : cntL (TL r θ f) v < (TL r θ f).length
  · have : ((cntL (TL r θ f) v + (TL r θ f).length - 1) % (TL r θ f).length + 1) %
        (TL r θ f).length = cntL (TL r θ f) v := by
      by_cases h0 : cntL (TL r θ f) v = 0
      · rw [h0, show 0 + (TL r θ f).length - 1 = (TL r θ f).length - 1 by omega,
          Nat.mod_eq_of_lt (by omega : (TL r θ f).length - 1 < (TL r θ f).length),
          show (TL r θ f).length - 1 + 1 = (TL r θ f).length by omega, Nat.mod_self]
      · rw [show cntL (TL r θ f) v + (TL r θ f).length - 1 =
            (cntL (TL r θ f) v - 1) + (TL r θ f).length by omega, Nat.add_mod_right,
          Nat.mod_eq_of_lt (by omega : cntL (TL r θ f) v - 1 < _),
          show cntL (TL r θ f) v - 1 + 1 = cntL (TL r θ f) v by omega, Nat.mod_eq_of_lt hc]
    rw [this]
    exact conn_fwd r θ f E hE hstep (r - 1 - v) v (by omega) hv hc
  · have hc' : cntL (TL r θ f) v = (TL r θ f).length := by omega
    have : ((cntL (TL r θ f) v + (TL r θ f).length - 1) % (TL r θ f).length + 1) %
        (TL r θ f).length = 0 := by
      rw [hc', show (TL r θ f).length + (TL r θ f).length - 1 =
          ((TL r θ f).length - 1) + (TL r θ f).length by omega, Nat.add_mod_right,
        Nat.mod_eq_of_lt (by omega : (TL r θ f).length - 1 < (TL r θ f).length),
        show (TL r θ f).length - 1 + 1 = (TL r θ f).length by omega, Nat.mod_self]
    rw [this]
    have h0 : cntL (TL r θ f) 0 = 0 := by simp [cntL]
    have e1 := conn_wrap r θ f E hE hstep (r - 1 - v) v (by omega) hv hc'
    have e2 := conn_fwd r θ f E hE hstep (r - 1) 0 (by omega) (by omega) (by omega)
    rw [h0] at e2
    exact hE.trans e1 e2

end arcs

section labels

variable (r θ : Nat) (f : Nat → Nat) (E : Nat → Nat → Prop) (hE : Equivalence E)

include hE in
/-- Chain label of arc `j`: the least position in the chain of its representative. -/
noncomputable def chainLab (j : Nat) : Nat :=
  by classical exact Nat.find (⟨rep r θ f j, hE.refl _⟩ : ∃ t, E t (rep r θ f j))

include hE in
theorem chainLab_eq_iff (j j' : Nat) :
    chainLab r θ f E hE j = chainLab r θ f E hE j' ↔ E (rep r θ f j) (rep r θ f j') := by
  classical
  unfold chainLab
  constructor
  · intro h
    have h1 := Nat.find_spec (⟨rep r θ f j, hE.refl _⟩ : ∃ t, E t (rep r θ f j))
    have h2 := Nat.find_spec (⟨rep r θ f j', hE.refl _⟩ : ∃ t, E t (rep r θ f j'))
    rw [h] at h1
    exact hE.trans (hE.symm h1) h2
  · intro h
    have hiff : ∀ t, E t (rep r θ f j) ↔ E t (rep r θ f j') :=
      fun t => ⟨fun h1 => hE.trans h1 h, fun h1 => hE.trans h1 (hE.symm h)⟩
    congr 1
    exact funext fun t => propext (hiff t)

variable (hf : ∀ t, f t < 4) (hθ1 : 1 ≤ θ) (hθ3 : θ ≤ 3)
  (hstep : ∀ v, v < r → tPred r (code f r) θ v = false → E v ((v + 1) % r))
  (hEcls : ∀ u w, u < r → w < r → E u w → cls θ (f u) = cls θ (f w))
  (hNC : ∀ i j k l, i < j → j < k → k < l → l < r → E i k → E j l → E i j)

include hE hf hθ1 hθ3 hstep hEcls hNC in
/-- **The abstract (S3) matching.** Some `matchTable` labelling gives equal labels to the arcs of
any two linked ring positions. -/
theorem abstract_matching (hr1 : 1 ≤ r) (N : Nat) (hN : N ≤ 10) (hr : r < 2 * N)
    (hn : (TL r θ f).length ≠ 0) :
    ∃ lab ∈ (matchTableN N)[(transitions r (code f r) θ).size / 2]!,
      ∀ t t', t < r → t' < r → E t t' →
        lab[arcOf (transitions r (code f r) θ) t]! = lab[arcOf (transitions r (code f r) θ) t']! := by
  classical
  set n2 := (TL r θ f).length with hn2
  have heven := TL_even r θ f hf hθ1 hθ3 hr1
  obtain ⟨p, hp⟩ : ∃ p, n2 = 2 * p := ⟨n2 / 2, by omega⟩
  have hn2r : n2 ≤ r := by
    rw [hn2]; exact (List.length_filter_le _ _).trans (le_of_eq List.length_range)
  set c := chainLab r θ f E hE with hc
  have hNCL : S3.NCLabel (2 * p) c := by
    intro a b x d hab hbx hxd hd hax hbd
    rw [hc, chainLab_eq_iff] at hax hbd ⊢
    by_cases hdl : d + 1 < n2
    · exact hNC _ _ _ _ (rep_lt_rep r θ f hn a b hab (by omega))
        (rep_lt_rep r θ f hn b x hbx (by omega)) (rep_lt_rep r θ f hn x d hxd hdl)
        (rep_spec r θ f hn d).1 hax hbd
    · have hd' : d = n2 - 1 := by omega
      subst hd'
      have h := hNC _ _ _ _ (rep_last_lt r θ f hn a (by omega)) (rep_lt_rep r θ f hn a b hab (by omega))
        (rep_lt_rep r θ f hn b x hbx (by omega)) (rep_spec r θ f hn x).1 (hE.symm hbd) hax
      exact hE.trans (hE.symm h) (hE.symm hbd)
  have hPar : S3.ParityLabel (2 * p) c := by
    intro j j' hj hj' hjj
    rw [hc, chainLab_eq_iff] at hjj
    have hcl := hEcls _ _ (rep_spec r θ f hn j).1 (rep_spec r θ f hn j').1 hjj
    have pj := cls_parity r θ f hf hθ1 hθ3 _ (rep_spec r θ f hn j).1
    have pj' := cls_parity r θ f hf hθ1 hθ3 _ (rep_spec r θ f hn j').1
    rw [(rep_spec r θ f hn j).2] at pj
    rw [(rep_spec r θ f hn j').2] at pj'
    have m1 : ((j + 1) % n2) % 2 = (j + 1) % 2 := by
      by_cases h : j + 1 < n2
      · rw [Nat.mod_eq_of_lt h]
      · rw [show j + 1 = n2 by omega, Nat.mod_self]; omega
    have m2 : ((j' + 1) % n2) % 2 = (j' + 1) % 2 := by
      by_cases h : j' + 1 < n2
      · rw [Nat.mod_eq_of_lt h]
      · rw [show j' + 1 = n2 by omega, Nat.mod_self]; omega
    rw [m1] at pj; rw [m2] at pj'
    rw [hcl] at pj
    have := pj.symm.trans pj'
    omega
  obtain ⟨μ, hμ, hsame⟩ := S3.nc_matching p c hNCL hPar
  obtain ⟨lab, hlab, hlabiff⟩ := R1.matchTableN_complete N hN p (by omega) μ hμ
  refine ⟨lab, ?_, ?_⟩
  · rw [transitions_size, ← hn2, hp, Nat.mul_div_cancel_left _ (by decide)]; exact hlab
  · intro t t' ht ht' htt
    have ha : arcOf (transitions r (code f r) θ) t < n2 := by
      rw [arcOf_eq]; exact Nat.mod_lt _ (by omega)
    have ha' : arcOf (transitions r (code f r) θ) t' < n2 := by
      rw [arcOf_eq]; exact Nat.mod_lt _ (by omega)
    have e1 := conn_rep r θ f E hE hstep hn t ht
    have e2 := conn_rep r θ f E hE hstep hn t' ht'
    have hcc : c (arcOf (transitions r (code f r) θ) t) = c (arcOf (transitions r (code f r) θ) t') := by
      rw [hc, chainLab_eq_iff]
      exact hE.trans (hE.symm e1) (hE.trans htt e2)
    exact (hlabiff _ _ (by omega) (by omega)).2 (hsame _ _ (by omega) (by omega) hcc)

end labels

/-! ### The ring code of a flip -/

theorem xor_lt4 (x θ : Nat) (hx : x < 4) (hθ : θ < 4) : x ^^^ θ < 4 := by
  rw [show (4 : Nat) = 2 ^ 2 from rfl] at *; exact Nat.xor_lt_two_pow hx hθ

theorem flip_code (r θ : Nat) (f : Nat → Nat) (hf : ∀ t, f t < 4) (hθ : θ < 4) (lab : Array Nat)
    (s : Nat) (sel : Nat → Bool)
    (hsel : ∀ t, t < r → sel t = (decide (lab[arcOf (transitions r (code f r) θ) t]! ≠ 0) &&
      s.testBit (lab[arcOf (transitions r (code f r) θ) t]! - 1))) :
    code (fun t => if sel t then f t ^^^ θ else f t) r =
      code f r ^^^ flipMask r (code f r) θ lab s := by
  have hf' : ∀ t, (if sel t then f t ^^^ θ else f t) < 4 := by
    intro t; split
    · exact xor_lt4 _ _ (hf t) hθ
    · exact hf t
  apply Nat.eq_of_testBit_eq
  intro j
  rw [Nat.testBit_xor, S1.flipMask_testBit _ _ _ _ _ hθ]
  by_cases hj : 2 * r ≤ j
  · rw [code_high _ hf' r j hj, code_high _ hf r j hj]
    simp [show ¬ j / 2 < r by omega]
  · have hjr : j / 2 < r := by omega
    rw [testBit_col (code _ r), testBit_col (code f r), col_code _ hf' r _ hjr, col_code _ hf r _ hjr,
      hsel _ hjr]
    simp only [hjr, decide_true, Bool.true_and]
    generalize (decide (lab[arcOf (transitions r (code f r) θ) (j / 2)]! ≠ 0) &&
      s.testBit (lab[arcOf (transitions r (code f r) θ) (j / 2)]! - 1)) = b
    cases b <;> simp [Nat.testBit_xor]

end DCheck.R2

#print axioms DCheck.R2.abstract_matching
#print axioms DCheck.R2.flip_code
