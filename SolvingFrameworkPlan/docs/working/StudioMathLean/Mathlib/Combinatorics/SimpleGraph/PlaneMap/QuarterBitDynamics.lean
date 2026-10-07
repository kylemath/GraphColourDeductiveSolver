/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterHole66
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterTwoPeriod
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterNonDLImage

/-!
# Pattern-free outer-bit dynamics on `DD` steps

`NightG66.md` §1.3. At a repeat state at `j` (link `α, μ, α, A, B` at `x j, …, x (j+4)`), every
outer vertex `w t` (the third vertex of the face `x t x (t+1)`) sees two link colours, so it has
exactly two possible colours. Encode them as bits

  `b₀ = [w j = A]`, `b₁ = [w (j+1) = A]`, `b₂ = [w (j+2) = μ]`, `b₃ = [w (j+3) = α]`,
  `b₄ = [w (j+4) = μ]`

(the other value is `B, B, B, μ, A` respectively). The only geometric hypothesis is `OuterW`:
`w t` is adjacent to `x t` and `x (t+1)` and is not `h`. No link degrees are used.

## Main results (sorry-free, no new axioms)

* `wbit_true_iff`, `wbit_false_iff`, `wcol_two`: `w (j+i)` has exactly the two colours
  `c (x (j + tpos i)) ≠ c (x (j + fpos i))`, and the bit says which.
* `dd_step_bits`: if `c` is a repeat state at `j` with `Lock2` (so `π c = R₊₃ c` with repeat
  index `j + 3`), the bit vector of `π c` at `j + 3` is `bitF` of that of `c` at `j`, where
  `bitF b = (¬b₃, b₄, ¬b₀, b₁, ¬b₂)`. Only `Lock2` of `c` is needed, not DL-ness of `π c`.
  `dd_step_bits'`: the same for a `DDstate`.
* `bitF_five` (`bitF⁵` is the complement), `bitF_ten`, `bitF_iter_five_mul` (`decide`).
* `allDL_orbit_bits`: along an all-`DL` orbit the `N`-th state is DL at `j₀ + 3N` with bits
  `bitF^[N] b`.
* `allDL_cycle_length_dvd_ten_recol`: if every `π^[k] c` is DL and `π^[L] c = recol τ c` for a
  colour permutation `τ` (a canonical cycle), then `10 ∣ L`. `allDL_cycle_length_dvd_ten`:
  the case `τ = 1`.
* `degree5_forbids`: each ring edge `w (t-1) ~ w t` (present when `deg x t = 5`) forbids one bit
  pair, for each of the five positions of `t` relative to `j`; `hole6_forbids` instantiates it
  at a `Hole6`.
* `pureClean_of_no_allDL_orbit`, `allDL_orbit_of_not_pureClean`: if no `π`-orbit at the hole is
  all-DL then `PureClean M h` (`NightG66.md` §4: conjecture G66⁰ ⇒ the weak form).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### The map `bitF` -/

/-- The DD-step map on outer words: `(b₀, …, b₄) ↦ (¬b₃, b₄, ¬b₀, b₁, ¬b₂)`. -/
def bitF (b : Fin 5 → Bool) : Fin 5 → Bool := ![!b 3, b 4, !b 0, b 1, !b 2]

/-- `bitF⁵` is the complement. -/
theorem bitF_five : ∀ b : Fin 5 → Bool, bitF^[5] b = fun i => !b i := by decide

/-- `bitF¹⁰ = id`. -/
theorem bitF_ten : ∀ b : Fin 5 → Bool, bitF^[10] b = b := by decide

/-- `bitF` has order exactly `10`: no word is fixed by `bitF⁵`, and some word is not fixed by
`bitF²` (orbit sizes `10, 10, 10, 2`). -/
theorem bitF_order : (∀ b : Fin 5 → Bool, bitF^[5] b ≠ b) ∧ (∃ b : Fin 5 → Bool, bitF^[2] b ≠ b) :=
  by decide

lemma bitF_iter_five_mul (b : Fin 5 → Bool) (q : ℕ) :
    bitF^[5 * q] b = b ↔ 2 ∣ q := by
  obtain ⟨r, rfl | rfl⟩ := Nat.even_or_odd' q
  · rw [show 5 * (2 * r) = 10 * r by ring, Function.iterate_mul,
      Function.iterate_fixed (bitF_ten b)]
    simp
  · rw [show 5 * (2 * r + 1) = 5 + 10 * r by ring, Function.iterate_add_apply,
      Function.iterate_mul, Function.iterate_fixed (bitF_ten b)]
    refine ⟨fun e => (bitF_order.1 b e).elim, fun ⟨k, hk⟩ => by omega⟩

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-- The outer vertices: `w t` sees `x t` and `x (t+1)`. Nothing else is assumed. -/
structure OuterW (P : Pent M.graph h) (w : Fin 5 → Fin n) : Prop where
  adjL : ∀ t, M.graph.Adj (P.x t) (w t)
  adjR : ∀ t, M.graph.Adj (P.x (t + 1)) (w t)
  offh : ∀ t, w t ≠ h

variable {P : Pent M.graph h} {w m : Fin 5 → Fin n} {c : Fin n → Fin 4} {j : Fin 5}

lemma Hole66.outerW (H : Hole66 P w m) : OuterW P w := ⟨H.adj_w, H.adj_w', H.offh⟩

lemma Hole6.outerW {m₀ : Fin n} {q : Fin 5} (H : Hole6 P w m₀ q) : OuterW P w :=
  ⟨H.adj_w, H.adj_w', H.offh⟩

namespace OuterW

lemma dom (H : OuterW P w) (hc : ProperOff M.graph h c) (t : Fin 5) :
    c (w t) ≠ c (P.x t) ∧ c (w t) ≠ c (P.x (t + 1)) :=
  ⟨(hc (H.adjL t) (P.x_ne_h _) (H.offh t)).symm,
    (hc (H.adjR t) (P.x_ne_h _) (H.offh t)).symm⟩

lemma domAt (H : OuterW P w) (hc : ProperOff M.graph h c) {a b : Fin 5} (hab : a + 1 = b) :
    c (w (j + a)) ≠ c (P.x (j + a)) ∧ c (w (j + a)) ≠ c (P.x (j + b)) := by
  have d := H.dom hc (j + a)
  rwa [add_assoc, hab] at d

lemma dom4 (H : OuterW P w) (hc : ProperOff M.graph h c) :
    c (w (j + 4)) ≠ c (P.x (j + 4)) ∧ c (w (j + 4)) ≠ c (P.x j) := by
  have d := H.dom hc (j + 4)
  rwa [add_assoc, show (4 : Fin 5) + 1 = 0 from rfl, add_zero] at d

/-- The two possible colours of each outer vertex at a repeat state (pattern-free form of
`ring66_dom`). -/
theorem ring_dom (H : OuterW P w) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    (c (w j) = c (P.x (j + 3)) ∨ c (w j) = c (P.x (j + 4))) ∧
    (c (w (j + 1)) = c (P.x (j + 3)) ∨ c (w (j + 1)) = c (P.x (j + 4))) ∧
    (c (w (j + 2)) = c (P.x (j + 1)) ∨ c (w (j + 2)) = c (P.x (j + 4))) ∧
    (c (w (j + 3)) = c (P.x j) ∨ c (w (j + 3)) = c (P.x (j + 1))) ∧
    (c (w (j + 4)) = c (P.x (j + 1)) ∨ c (w (j + 4)) = c (P.x (j + 3))) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨d0, d0'⟩ := H.dom hc j
  obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d3, d3'⟩ := H.domAt hc (j := j) (a := 3) (b := 4) rfl
  obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · clear * - h1 h3 h4 h13 h14 h34 d0 d0'; omega
  · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1'; omega
  · clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2'; omega
  · clear * - h1 h3 h4 h13 h14 h34 d3 d3'; omega
  · clear * - h1 h3 h4 h13 h14 h34 d4 d4'; omega

end OuterW

/-! ### The bit encoding -/

/-- Link position of the colour encoded by bit `true` at outer position `i`:
`A, A, μ, α, μ`. -/
def tpos : Fin 5 → Fin 5 := ![3, 3, 1, 0, 1]

/-- Link position of the colour encoded by bit `false` at outer position `i`:
`B, B, B, μ, A`. -/
def fpos : Fin 5 → Fin 5 := ![4, 4, 4, 1, 3]

variable (P w) in
/-- The outer word of `c` relative to repeat index `j`. -/
def wbits (c : Fin n → Fin 4) (j : Fin 5) : Fin 5 → Bool :=
  fun i => decide (c (w (j + i)) = c (P.x (j + tpos i)))

lemma wbits_recol (τ : Equiv.Perm (Fin 4)) (c : Fin n → Fin 4) (j : Fin 5) :
    wbits P w (recol τ c) j = wbits P w c j := by
  funext i
  simp only [wbits, recol_apply, EmbeddingLike.apply_eq_iff_eq]

/-- The two colours of each position are distinct. -/
lemma tpos_ne_fpos (hr : RepeatAt P c j) (i : Fin 5) :
    c (P.x (j + tpos i)) ≠ c (P.x (j + fpos i)) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  fin_cases i <;> simp [tpos, fpos] <;> first
    | exact h34 | exact h14 | exact h1.symm | exact h13.symm | exact h13

/-- **(1) The bit encoding.** At a repeat state, `w (j+i)` has exactly two possible colours,
`c (x (j + tpos i)) ≠ c (x (j + fpos i))`, and `wbits` records which one it has. -/
theorem wcol_two (H : OuterW P w) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (i : Fin 5) :
    (c (w (j + i)) = c (P.x (j + tpos i)) ∨ c (w (j + i)) = c (P.x (j + fpos i))) ∧
      c (P.x (j + tpos i)) ≠ c (P.x (j + fpos i)) := by
  refine ⟨?_, tpos_ne_fpos hr i⟩
  obtain ⟨a0, a1, a2, a3, a4⟩ := H.ring_dom hc hr
  fin_cases i <;> simp [tpos, fpos] <;> assumption

lemma wbit_true_iff (i : Fin 5) :
    wbits P w c j i = true ↔ c (w (j + i)) = c (P.x (j + tpos i)) := by
  simp [wbits]

lemma wbit_false_iff (H : OuterW P w) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (i : Fin 5) :
    wbits P w c j i = false ↔ c (w (j + i)) = c (P.x (j + fpos i)) := by
  obtain ⟨d, ne⟩ := wcol_two H hc hr i
  simp only [wbits, decide_eq_false_iff_not]
  constructor
  · intro hn; exact d.resolve_left hn
  · intro e e'; exact ne (e'.symm.trans e)

/-- The colour of `w (j+i)` is determined by its bit. -/
theorem wcol_of_bit (H : OuterW P w) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (i : Fin 5) :
    c (w (j + i)) = c (P.x (j + if wbits P w c j i then tpos i else fpos i)) := by
  cases e : wbits P w c j i
  · exact (wbit_false_iff H hc hr i).1 e
  · exact (wbit_true_iff i).1 e

/-! ### 2. The `DD` step -/

/-- **(2) `dd_step_bits`.** If `c` is a repeat state at `j` with `Lock2` (so `π c = R₊₃ c`,
with repeat index `j + 3`), the outer word of `π c` at `j + 3` is `bitF` of the word of `c` at
`j`. Pattern-free: only `OuterW` and properness are used. -/
theorem dd_step_bits (H : OuterW P w) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hl : Lock2 P c j) :
    wbits P w (piMove P c) (j + 3) = bitF (wbits P w c j) := by
  have hK := rot3Def_of_lock2 P hr hl
  have hπ : piMove P c = rot3 P c j := by rw [piMove_rep hr, ite_eq_left hl]
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values hr hK
  obtain ⟨a0, a1, a2, a3, a4⟩ := H.ring_dom hc hr
  have hr' := hr
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have eR1 := H.adjR (j + 1)
  have eL0 := H.adjR (j + 4)
  simp only [add_assoc, Fin.reduceAdd, add_zero] at eR1 eL0
  rw [hπ]
  funext i
  fin_cases i <;> simp only [wbits, bitF, tpos, Fin.zero_eta, Fin.mk_one, Fin.reduceFinMk,
    Matrix.cons_val, add_assoc, Fin.reduceAdd, add_zero, Fin.isValue]
  · -- position 0: `w (j+3)`, adjacent to `x (j+3) ∈ K`
    rw [v1]
    rcases a3 with e | e
    · rw [rot3_K3 hr' (H.adjL (j + 3)) (H.offh _) (Or.inl e), e, Equiv.swap_apply_left]
      simp [Ne.symm h13]
    · rw [rot3_keep (by rw [e]; exact h1) (by rw [e]; exact h13), e]
      simp [h1]
  · -- position 1: `w (j+4)`, adjacent to `x j ∉ K`
    rw [v1, rot3_K0 hK eL0 (H.offh _)]
    rfl
  · -- position 2: `w j`, adjacent to `x j ∉ K`
    rw [v4, rot3_K0 hK (H.adjL j) (H.offh _)]
    rcases a0 with e | e
    · simp [e, h34]
    · simp [e, Ne.symm h34]
  · -- position 3: `w (j+1)`, adjacent to `x (j+2) ∈ K`
    rw [v3]
    rcases a1 with e | e
    · rw [rot3_K2 hr' eR1 (H.offh _) (Or.inr e), e, Equiv.swap_apply_right]
      simp
    · rw [rot3_keep (by rw [e]; exact h4) (by rw [e]; exact h34.symm), e]
      simp [h4, Ne.symm h34]
  · -- position 4: `w (j+2)`, coloured `μ` or `B`, untouched
    rw [v4]
    rcases a2 with e | e
    · rw [rot3_keep (by rw [e]; exact h1) (by rw [e]; exact h13), e]
      simp [h14]
    · rw [rot3_keep (by rw [e]; exact h4) (by rw [e]; exact h34.symm), e]
      simp [Ne.symm h14]

/-- `dd_step_bits` for a `DD` state. -/
theorem dd_step_bits' (H : OuterW P w) (hc : ProperOff M.graph h c) (hD : DDstate P c j) :
    wbits P w (piMove P c) (j + 3) = bitF (wbits P w c j) :=
  dd_step_bits H hc hD.1.1 hD.1.2.2

/-! ### 3. All-`DL` orbits -/

/-- Adding `3` `N` times in `Fin 5` returns to the start iff `5 ∣ N`. -/
lemma add3_iter_eq_self (j : Fin 5) (N : ℕ) :
    (fun x : Fin 5 => x + 3)^[N] j = j ↔ 5 ∣ N := by
  have h5 : ∀ x : Fin 5, (fun x : Fin 5 => x + 3)^[5] x = x := by decide
  rw [← Nat.mod_add_div N 5, Function.iterate_add_apply, Function.iterate_mul,
    Function.iterate_fixed (h5 j), add_comm, Nat.dvd_add_right (dvd_mul_right 5 _)]
  have hr := Nat.mod_lt N (show 5 > 0 by norm_num)
  generalize N % 5 = r at hr ⊢
  interval_cases r <;> revert j <;> decide

/-- Along an all-`DL` orbit, the `N`-th state is DL at `j₀ + 3N` with word `bitF^[N] b₀`. -/
theorem allDL_orbit_bits (H : OuterW P w) {s : Fin n → Fin 4} (hc : ProperOff M.graph h s)
    (hall : ∀ k, DLState P ((piMove P)^[k] s)) {j₀ : Fin 5} (hd : DoublyLocked P s j₀) :
    ∀ N : ℕ, DoublyLocked P ((piMove P)^[N] s) ((fun x : Fin 5 => x + 3)^[N] j₀) ∧
      wbits P w ((piMove P)^[N] s) ((fun x : Fin 5 => x + 3)^[N] j₀) =
        bitF^[N] (wbits P w s j₀)
  | 0 => ⟨hd, rfl⟩
  | N + 1 => by
    obtain ⟨d, b⟩ := allDL_orbit_bits H hc hall hd N
    rw [Function.iterate_succ_apply' (fun x : Fin 5 => x + 3)]
    refine ⟨allDL_next hc hall d, ?_⟩
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply',
      dd_step_bits H (iter_proper hc N) d.1 d.2.2, b]

/-- **(3) Canonical all-`DL` cycles have length divisible by `10`.** If every state of the
`π`-orbit of `s` is DL and `π^[L] s = recol τ s` for a colour permutation `τ`, then `10 ∣ L`. -/
theorem allDL_cycle_length_dvd_ten_recol (H : OuterW P w) {s : Fin n → Fin 4}
    (hc : ProperOff M.graph h s) (hall : ∀ k, DLState P ((piMove P)^[k] s))
    (τ : Equiv.Perm (Fin 4)) {L : ℕ} (hL : (piMove P)^[L] s = recol τ s) : 10 ∣ L := by
  obtain ⟨j₀, hd⟩ := hall 0
  simp only [Function.iterate_zero, id] at hd
  obtain ⟨d, b⟩ := allDL_orbit_bits H hc hall hd L
  rw [hL] at d b
  rw [doublyLocked_recol] at d
  have ej := rep_unique hd.1 d.1
  obtain ⟨q, rfl⟩ := (add3_iter_eq_self j₀ L).1 ej
  rw [ej, wbits_recol] at b
  obtain ⟨r, rfl⟩ := (bitF_iter_five_mul (wbits P w s j₀) q).1 b.symm
  exact ⟨r, by ring⟩

/-- **(3)** The plain version: an all-`DL` `π`-cycle `π^[L] s = s` has `10 ∣ L`. -/
theorem allDL_cycle_length_dvd_ten (H : OuterW P w) {s : Fin n → Fin 4}
    (hc : ProperOff M.graph h s) (hall : ∀ k, DLState P ((piMove P)^[k] s)) {L : ℕ}
    (hL : (piMove P)^[L] s = s) : 10 ∣ L :=
  allDL_cycle_length_dvd_ten_recol H hc hall 1 (by rw [hL, recol_one])

/-! ### 4. Degree-five link vertices as 2-clauses -/

/-- **(4) `degree5_forbids`.** A ring edge `w (t-1) ~ w t` (which a degree-five link vertex
`x t` provides) forbids one pair of adjacent bits. Relative to the repeat index `j`:
`x (j+1)`: `b₀ ≠ b₁`; `x (j+2)`: not `b₁ = b₂ = 0`; `x (j+3)`: not `(b₂, b₃) = (1, 0)`;
`x (j+4)`: not `(b₃, b₄) = (0, 1)`; `x j`: not `(b₄, b₀) = (0, 1)`. -/
theorem degree5_forbids (H : OuterW P w) (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    (M.graph.Adj (w j) (w (j + 1)) → wbits P w c j 0 ≠ wbits P w c j 1) ∧
    (M.graph.Adj (w (j + 1)) (w (j + 2)) →
      ¬ (wbits P w c j 1 = false ∧ wbits P w c j 2 = false)) ∧
    (M.graph.Adj (w (j + 2)) (w (j + 3)) →
      ¬ (wbits P w c j 2 = true ∧ wbits P w c j 3 = false)) ∧
    (M.graph.Adj (w (j + 3)) (w (j + 4)) →
      ¬ (wbits P w c j 3 = false ∧ wbits P w c j 4 = true)) ∧
    (M.graph.Adj (w (j + 4)) (w j) →
      ¬ (wbits P w c j 4 = false ∧ wbits P w c j 0 = true)) := by
  have f : ∀ i, (wbits P w c j i = true → c (w (j + i)) = c (P.x (j + tpos i))) ∧
      (wbits P w c j i = false → c (w (j + i)) = c (P.x (j + fpos i))) :=
    fun i => ⟨(wbit_true_iff i).1, (wbit_false_iff H hc hr i).1⟩
  obtain ⟨t0, f0⟩ := f 0
  obtain ⟨t1, f1⟩ := f 1
  obtain ⟨t2, f2⟩ := f 2
  obtain ⟨t3, f3⟩ := f 3
  obtain ⟨t4, f4⟩ := f 4
  simp only [tpos, fpos, add_zero, Fin.isValue, Matrix.cons_val] at t0 f0 t1 f1 t2 f2 t3 f3 t4 f4
  refine ⟨fun e hb => ?_, fun e ⟨b1, b2⟩ => ?_, fun e ⟨b2, b3⟩ => ?_, fun e ⟨b3, b4⟩ => ?_,
    fun e ⟨b4, b0⟩ => ?_⟩
  · have ne := hc e (H.offh _) (H.offh _)
    cases h0 : wbits P w c j 0
    · rw [h0] at hb
      exact ne ((f0 h0).trans (f1 hb.symm).symm)
    · rw [h0] at hb
      exact ne ((t0 h0).trans (t1 hb.symm).symm)
  · exact hc e (H.offh _) (H.offh _) ((f1 b1).trans (f2 b2).symm)
  · exact hc e (H.offh _) (H.offh _) ((t2 b2).trans (f3 b3).symm)
  · exact hc e (H.offh _) (H.offh _) ((f3 b3).trans (t4 b4).symm)
  · exact hc e (H.offh _) (H.offh _) ((f4 b4).trans (t0 b0).symm)

/-- `degree5_forbids` at a `Hole6` (degree-six vertex `x q`): every `x t` with `t ≠ q` has
degree five and contributes its clause; e.g. `j + 1 ≠ q` forces `b₀ ≠ b₁`. -/
theorem hole6_forbids {m₀ : Fin n} {q : Fin 5} (H : Hole6 P w m₀ q) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hq : j + 1 ≠ q) : wbits P w c j 0 ≠ wbits P w c j 1 :=
  (degree5_forbids H.outerW hc hr).1 (H.ring j hq)

/-! ### G66⁰ ⇒ the weak form -/

variable (P) in
/-- **`pureClean_of_no_allDL_orbit`.** If every `π`-orbit at the hole contains a state that is
not doubly locked, the hole is pure-clean. -/
theorem pureClean_of_no_allDL_orbit
    (H : ∀ c : Fin n → Fin 4, ProperOff M.graph h c → ∃ k, ¬ DLState P ((piMove P)^[k] c)) :
    PureClean M h := by
  refine pureClean_of_every_class_filled M h fun c₀ hc₀ => ?_
  by_contra hno
  push Not at hno
  have hall := allDL_of_targetless (P := P) hno
  obtain ⟨k, hk⟩ := H c₀ hc₀
  exact hk (hall _ (iterate_mem_kclass (self_mem_kclass hc₀) k))

variable (P) in
/-- Contrapositive: a hole that is not pure-clean has an all-DL `π`-orbit. -/
theorem allDL_orbit_of_not_pureClean (hn : ¬ PureClean M h) :
    ∃ c : Fin n → Fin 4, ProperOff M.graph h c ∧ ∀ k, DLState P ((piMove P)^[k] c) := by
  by_contra hno
  push Not at hno
  exact hn (pureClean_of_no_allDL_orbit P hno)

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.bitF_five
#print axioms SimpleGraph.QuarterFloor.bitF_order
#print axioms SimpleGraph.QuarterFloor.wcol_two
#print axioms SimpleGraph.QuarterFloor.dd_step_bits
#print axioms SimpleGraph.QuarterFloor.allDL_cycle_length_dvd_ten_recol
#print axioms SimpleGraph.QuarterFloor.allDL_cycle_length_dvd_ten
#print axioms SimpleGraph.QuarterFloor.degree5_forbids
#print axioms SimpleGraph.QuarterFloor.hole6_forbids
#print axioms SimpleGraph.QuarterFloor.pureClean_of_no_allDL_orbit
#print axioms SimpleGraph.QuarterFloor.allDL_orbit_of_not_pureClean
