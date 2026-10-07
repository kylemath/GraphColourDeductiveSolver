/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterWindow

/-!
# The even-cut lemma for closed Kempe orbits (`NightGammaLength.md` §2, Tait view)

Encode the four colours in `F₂² = ZMod 2 × ZMod 2` (`enc`, a bijection) and give an edge `uv`
the **Tait colour** `tait c u v = enc (c u) + enc (c v)` (nonzero on a proper edge).

## Main results (sorry-free, no new axioms)

1. `enc_swap`: for `x ∈ {a, b}`, `enc (swap a b x) = enc x + (enc a + enc b)`.
2. `swap_support`: a whole-component swap `swap c a b S` (`a ≠ b`) changes exactly the colours of
   the vertices of `S`. `swap_edge_colour`: it changes the Tait colour of any `uv` by
   `enc a + enc b` if exactly one of `u, v` is in `S` (the edge is *cut*, `Cut S u v`), and by `0` otherwise;
   `swap_edge_colour_ne`: the Tait colour changes iff the edge is cut.
3. `closed_orbit_cut_sum`: along any sequence of whole-component swaps `c (t+1) = swap (c t) ...`
   with `c L = c 0` (closed **in colouring space**), for every pair `u, v`,
   `∑_{t < L, uv cut at t} (enc a_t + enc b_t) = 0` in `F₂²`. `kempe_orbit_cut_sum` is the same
   for an abstract chain of `KempeStep`s, and `piMove_cut_sum` for a `π`-orbit with
   `π^[L] s = s` (every `π`-step, `R₊₃`, `φ_B⁻¹`, `φ_A`, `τ`, is one `KempeStep`: `piMove_spec`).
   The pair sum `enc a + enc b` is nonzero and determines `{a, b}` only up to its complement
   `{c, d}` (`a + b = c + d` in `F₂²`); it names the *pair-partition* `{a,b} | {c,d}`.
4. Parity: `even_of_sum_const`; `closed_orbit_cut_parity`: the number of steps cutting `uv`
   is even, **or** two of those steps have different pair sums (pairs from different
   pair-partitions). In particular, if every cut of `uv` swaps the same pair or its complement,
   `uv` is cut an even number of times. (Nothing stronger holds without the pair data: the
   general statement is that the three pair-partitions occur with equal parity among the cuts.)
5. `allDL_ring_cut_count`: on an all-`DL` orbit at a `Hole6`, from any `R3k4` anchor `s k`
   (`k > 0`, `k % 10 = 0`), each of the 22 ring edges (`ringEdges`: `x–x`, `x–w`, `w–w`,
   `y–m`, `m–z`, `p–m`) has exactly one endpoint changing colour at exactly **4** of the
   10 steps `k, …, k+9`. By `swap_support` "changes colour" is "lies in the swapped
   component", so each ring edge is cut exactly 4 times per period. The count is a `decide`
   on the bookkeeping tables (`ring_cut_table`), with row 10 = `σ` (row 0)
   (`period_colour_rotation`).

Note: (3) needs closure in colouring space. A canonical closure `s L = g · s 0` (relabelling
`g`) acts on Tait colours by the linear part of `g`; that version (`NightGammaLength.md` §2)
is not formalised here.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap Finset

/-! ### 1. The `F₂²` encoding -/

/-- `F₂² = ZMod 2 × ZMod 2`. -/
abbrev F22 := ZMod 2 × ZMod 2

/-- The four colours as the four elements of `F₂²`. -/
def enc : Fin 4 → F22 := ![(0, 0), (1, 0), (0, 1), (1, 1)]

lemma enc_injective : Function.Injective enc := by
  intro a b; revert a b; decide

lemma enc_add_ne_zero {a b : Fin 4} (hab : a ≠ b) : enc a + enc b ≠ 0 := by
  revert a b; decide

lemma F22_add_self (x : F22) : x + x = 0 := by revert x; decide

/-- A transposition `a ↔ b` acts on `{a, b}` as translation by `a + b`. -/
lemma enc_swap : ∀ a b x : Fin 4, (x = a ∨ x = b) →
    enc (Equiv.swap a b x) = enc x + (enc a + enc b) := by
  decide

/-- The Tait colour of `uv`. -/
def tait {V : Type*} (c : V → Fin 4) (u v : V) : F22 := enc (c u) + enc (c v)

/-! ### 2. One swap -/

section generic
variable {V : Type*} {G : SimpleGraph V} {h : V} {c : V → Fin 4} {a b : Fin 4} {S : Set V}

/-- The edge `uv` is *cut* by `S`: exactly one endpoint lies in `S`. -/
def Cut (S : Set V) (u v : V) : Prop := ¬ (u ∈ S ↔ v ∈ S)

open Classical

lemma swap_enc (hS : Whole G h c a b S) (v : V) :
    enc (swap c a b S v) = enc (c v) + if v ∈ S then enc a + enc b else 0 := by
  by_cases hv : v ∈ S
  · rw [swap_in hv]; simp only [hv, ↓reduceIte]
    exact enc_swap _ _ _ (whole_active G hS hv).2
  · rw [swap_out hv]; simp only [hv, ↓reduceIte, add_zero]

/-- A whole-component swap changes exactly the colours of the component. -/
theorem swap_support (hab : a ≠ b) (hS : Whole G h c a b S) (v : V) :
    swap c a b S v ≠ c v ↔ v ∈ S := by
  classical
  constructor
  · intro hne
    by_contra hv
    exact hne (swap_out hv)
  · intro hv he
    have e := swap_enc hS v
    simp only [hv, ↓reduceIte] at e; rw [he] at e
    exact enc_add_ne_zero hab (by simpa using e.symm)

/-- **`swap_edge_colour`.** The Tait colour of `uv` moves by `enc a + enc b` iff exactly one
endpoint is swapped. -/
theorem swap_edge_colour (hS : Whole G h c a b S) (u v : V) :
    tait (swap c a b S) u v =
      tait c u v + if Cut S u v then enc a + enc b else 0 := by
  unfold tait
  rw [swap_enc hS, swap_enc hS]
  by_cases hu : u ∈ S <;> by_cases hv : v ∈ S <;> simp [hu, hv, Cut] <;>
    first
    | (rw [show ∀ x y z : F22, x + z + (y + z) = x + y from by decide])
    | abel

theorem swap_edge_colour_ne (hab : a ≠ b) (hS : Whole G h c a b S) (u v : V) :
    tait (swap c a b S) u v ≠ tait c u v ↔ Cut S u v := by
  classical
  rw [swap_edge_colour hS]
  by_cases hx : Cut S u v
  · simp only [hx, iff_true]
    intro e
    exact enc_add_ne_zero hab (by simpa using e)
  · simp [hx]

/-! ### 3. Closed orbits -/

lemma tait_iter {c : ℕ → V → Fin 4} {a b : ℕ → Fin 4} {S : ℕ → Set V}
    (hS : ∀ t, Whole G h (c t) (a t) (b t) (S t))
    (hstep : ∀ t, c (t + 1) = swap (c t) (a t) (b t) (S t)) (u v : V) (n : ℕ) :
    tait (c n) u v = tait (c 0) u v +
      ∑ t ∈ range n, if Cut (S t) u v then enc (a t) + enc (b t) else 0 := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [hstep, swap_edge_colour (hS n), ih, sum_range_succ, add_assoc]

/-- **`closed_orbit_cut_sum`.** Along a closed chain of whole-component swaps, the pair sums
of the steps cutting `uv` add to `0` in `F₂²`. -/
theorem closed_orbit_cut_sum {c : ℕ → V → Fin 4} {a b : ℕ → Fin 4} {S : ℕ → Set V}
    (hS : ∀ t, Whole G h (c t) (a t) (b t) (S t))
    (hstep : ∀ t, c (t + 1) = swap (c t) (a t) (b t) (S t)) {L : ℕ} (hL : c L = c 0)
    (u v : V) :
    ∑ t ∈ (range L).filter (fun t => Cut (S t) u v), (enc (a t) + enc (b t)) = 0 := by
  have e := tait_iter hS hstep u v L
  rw [hL, left_eq_add] at e
  rw [sum_filter]
  exact e

/-- The same for an abstract chain of `KempeStep`s, closed in colouring space. -/
theorem kempe_orbit_cut_sum {c : ℕ → V → Fin 4} (hstep : ∀ t, KempeStep G h (c t) (c (t + 1)))
    {L : ℕ} (hL : c L = c 0) :
    ∃ (a b : ℕ → Fin 4) (S : ℕ → Set V),
      (∀ t, a t ≠ b t ∧ Whole G h (c t) (a t) (b t) (S t) ∧
        c (t + 1) = swap (c t) (a t) (b t) (S t)) ∧
      ∀ u v, ∑ t ∈ (range L).filter (fun t => Cut (S t) u v),
        (enc (a t) + enc (b t)) = 0 := by
  classical
  choose a b S hab hS hst using hstep
  exact ⟨a, b, S, fun t => ⟨hab t, hS t, hst t⟩,
    fun u v => by convert closed_orbit_cut_sum hS hst hL u v⟩

/-! ### 4. Parity -/

lemma even_of_nsmul_eq_zero {x : F22} (hx : x ≠ 0) {k : ℕ} (hk : k • x = 0) : Even k := by
  rcases Nat.even_or_odd k with he | ⟨r, rfl⟩
  · exact he
  · exfalso
    rw [add_smul, one_smul, mul_comm, mul_smul, two_smul, F22_add_self, smul_zero,
      zero_add] at hk
    exact hx hk

lemma even_of_sum_const {ι : Type*} (T : Finset ι) (δ : ι → F22) {x : F22} (hx : x ≠ 0)
    (hδ : ∀ t ∈ T, δ t = x) (hs : ∑ t ∈ T, δ t = 0) : Even T.card := by
  rw [sum_congr rfl hδ, sum_const] at hs
  exact even_of_nsmul_eq_zero hx hs

/-- **Parity.** Along a closed chain of whole-component swaps, the number of steps cutting
`uv` is even, or two cutting steps have different pair sums (pairs in different
pair-partitions `{a,b} | {c,d}`). -/
theorem closed_orbit_cut_parity {c : ℕ → V → Fin 4} {a b : ℕ → Fin 4} {S : ℕ → Set V}
    (hab : ∀ t, a t ≠ b t) (hS : ∀ t, Whole G h (c t) (a t) (b t) (S t))
    (hstep : ∀ t, c (t + 1) = swap (c t) (a t) (b t) (S t)) {L : ℕ} (hL : c L = c 0)
    (u v : V) :
    Even ((range L).filter (fun t => Cut (S t) u v)).card ∨
      ∃ t ∈ (range L).filter (fun t => Cut (S t) u v),
      ∃ t' ∈ (range L).filter (fun t => Cut (S t) u v),
        enc (a t) + enc (b t) ≠ enc (a t') + enc (b t') := by
  classical
  by_contra hne
  push Not at hne
  obtain ⟨hodd, hall⟩ := hne
  set T := (range L).filter (fun t => Cut (S t) u v)
  rcases T.eq_empty_or_nonempty with he | ⟨t₀, ht₀⟩
  · exact hodd (by rw [he]; exact ⟨0, rfl⟩)
  · exact hodd (even_of_sum_const T _ (enc_add_ne_zero (hab t₀))
      (fun t ht => hall t ht t₀ ht₀) (closed_orbit_cut_sum hS hstep hL u v))

/-- Special case: if every step cutting `uv` swaps the same pair-partition, `uv` is cut an
even number of times. -/
theorem closed_orbit_cut_even {c : ℕ → V → Fin 4} {a b : ℕ → Fin 4} {S : ℕ → Set V}
    (hab : ∀ t, a t ≠ b t) (hS : ∀ t, Whole G h (c t) (a t) (b t) (S t))
    (hstep : ∀ t, c (t + 1) = swap (c t) (a t) (b t) (S t)) {L : ℕ} (hL : c L = c 0)
    (u v : V) (hsame : ∀ t ∈ (range L).filter (fun t => Cut (S t) u v),
      ∀ t' ∈ (range L).filter (fun t => Cut (S t) u v),
        enc (a t) + enc (b t) = enc (a t') + enc (b t')) :
    Even ((range L).filter (fun t => Cut (S t) u v)).card := by
  rcases closed_orbit_cut_parity hab hS hstep hL u v with he | ⟨t, ht, t', ht', hne⟩
  · exact he
  · exact (hne (hsame t ht t' ht')).elim

end generic

/-! ### 5. `π`-orbits and the all-`DL` ring count -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
variable {s : Fin n → Fin 4} {j₀ : Fin 5}

open Classical in
/-- **`π`-orbits.** If `π^[L] s = s` then every step is a whole-component swap and, for every
`uv`, the pair sums of the steps cutting `uv` add to `0` in `F₂²`. -/
theorem piMove_cut_sum (hc : ProperOff M.graph h s) {L : ℕ} (hL : (piMove P)^[L] s = s) :
    ∃ (a b : ℕ → Fin 4) (S : ℕ → Set (Fin n)),
      (∀ t, a t ≠ b t ∧ Whole M.graph h ((piMove P)^[t] s) (a t) (b t) (S t) ∧
        (piMove P)^[t + 1] s = swap ((piMove P)^[t] s) (a t) (b t) (S t)) ∧
      ∀ u v, ∑ t ∈ (range L).filter (fun t => Cut (S t) u v),
        (enc (a t) + enc (b t)) = 0 := by
  refine kempe_orbit_cut_sum (c := fun t => (piMove P)^[t] s) (fun t => ?_) hL
  rw [Function.iterate_succ_apply']
  exact (piMove_spec (iter_proper hc t)).1

/-- The eleven hole vertices: `0..4 = x (q+t)`, `5..9 = w (q+t)` (`5 = z`, `9 = y`), `10 = m`. -/
def hv (P : Pent M.graph h) (w : Fin 5 → Fin n) (m : Fin n) (q : Fin 5) (l : Fin 11) : Fin n :=
  if hl : l.val < 5 then P.x (q + ⟨l.val, hl⟩)
  else if hl' : l.val < 10 then w (q + ⟨l.val - 5, by omega⟩) else m

/-- A row of letters for the eleven hole vertices. -/
def rowOf (X W : Fin 5 → Fin 4) (Mm : Fin 4) (l : Fin 11) : Fin 4 :=
  if hl : l.val < 5 then X ⟨l.val, hl⟩
  else if hl' : l.val < 10 then W ⟨l.val - 5, by omega⟩ else Mm

/-- Letters at positions `0..10` of a period: rows `0..9` are the bookkeeping tables, row `10`
is `σ` of row `0`. -/
def letTab (i : ℕ) (l : Fin 11) : Fin 4 :=
  if hi : i < 10 then rowOf (xTab ⟨i, hi⟩) (wTab ⟨i, hi⟩) (mTab ⟨i, hi⟩) l
  else rowOf (fun t => sig (xTab 0 t)) (fun t => sig (wTab 0 t)) (sig (mTab 0)) l

/-- The 22 ring edges of the hole, as pairs of labels. -/
def ringEdges : List (Fin 11 × Fin 11) :=
  [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
   (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
   (0, 9), (1, 5), (2, 6), (3, 7), (4, 8),
   (5, 6), (6, 7), (7, 8), (8, 9),
   (9, 10), (10, 5), (0, 10)]

/-- Steps `i < 10` of a period at which exactly one end of `e` changes letter. -/
def cutTab (e : Fin 11 × Fin 11) : ℕ :=
  ((range 10).filter (fun i =>
    (letTab i e.1 != letTab (i + 1) e.1) != (letTab i e.2 != letTab (i + 1) e.2))).card

theorem ringEdges_length : ringEdges.length = 22 := rfl

/-- Every ring edge is cut exactly 4 times per period (the tables). -/
theorem ring_cut_table : ∀ e ∈ ringEdges, cutTab e = 4 := by decide +kernel

lemma hv_col {c : Fin n → Fin 4} {f : Fin 4 → Fin 4} {X W : Fin 5 → Fin 4} {Mm : Fin 4}
    (hX : ∀ t, c (P.x (q + t)) = f (X t)) (hW : ∀ t, c (w (q + t)) = f (W t))
    (hM : c m = f Mm) (l : Fin 11) : c (hv P w m q l) = f (rowOf X W Mm l) := by
  unfold hv rowOf
  split_ifs
  · exact hX _
  · exact hW _
  · exact hM

lemma vec4_inj : ∀ x0 x1 x3 x4 : Fin 4, x1 ≠ x0 → x3 ≠ x0 → x4 ≠ x0 → x1 ≠ x3 → x1 ≠ x4 →
    x3 ≠ x4 → ∀ a b : Fin 4, ![x0, x1, x3, x4] a = ![x0, x1, x3, x4] b → a = b := by
  decide

lemma frm_inj {c : Fin n → Fin 4} {j : Fin 5} (hr : RepeatAt P c j) {a b : Fin 4} :
    frm P c j a = frm P c j b ↔ a = b := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  exact ⟨vec4_inj _ _ _ _ h1 h3 h4 h13 h14 h34 a b, fun e => e ▸ rfl⟩

/-- **All-`DL` ring cut count.** From an `R3k4` anchor `s k` (`k > 0`, `k % 10 = 0`), each
of the 22 ring edges has exactly one endpoint changing colour at exactly 4 of the steps
`k, …, k+9` (by `swap_support`: is cut by exactly 4 of the swapped components). -/
theorem allDL_ring_cut_count (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk0 : 0 < k) (hk : k % 10 = 0) :
    ∀ e ∈ ringEdges, ((range 10).filter (fun i =>
      (((piMove P)^[k + i] s) (hv P w m q e.1) != ((piMove P)^[k + (i + 1)] s) (hv P w m q e.1))
        != (((piMove P)^[k + i] s) (hv P w m q e.2) !=
          ((piMove P)^[k + (i + 1)] s) (hv P w m q e.2)))).card = 4 := by
  obtain ⟨j, hd, -, tab⟩ := bookkeeping H hc hall hr hq hT k hk0 hk
  -- colours at every position `0..10` in the anchor's letters
  have col : ∀ i, i ≤ 10 → ∀ l,
      ((piMove P)^[k + i] s) (hv P w m q l) = frm P ((piMove P)^[k] s) j (letTab i l) := by
    intro i hi l
    by_cases h10 : i < 10
    · obtain ⟨tx, tw, tm⟩ := tab ⟨i, h10⟩
      have := hv_col (P := P) (w := w) (m := m) (q := q) tx tw tm l
      simp only [letTab, h10, ↓reduceDIte]
      exact this
    · have i10 : i = 10 := by omega
      subst i10
      obtain ⟨ox, ow, om⟩ := orbit_colour H hc hall hr hq hT k hk0 hd.1 10
      have g : gseq (k + 10) = gseq 0 := by
        rw [gseq_mod, gseq_mod 0]; congr 1; omega
      have e10 : sig^[10] = sig := by rw [sig_iter_mod]; rfl
      rw [g, e10] at ox ow om
      have x0 : ∀ t, xL (gseq 0) t = xTab 0 t := fun t => (xTab_eq 0 t).symm
      have w0 : ∀ t, wL (gseq 0) t = wTab 0 t := fun t => (wTab_eq 0 t).symm
      have m0 : mL (gseq 0) = mTab 0 := (mTab_eq 0).symm
      simp only [x0, w0, m0] at ox ow om
      simp only [letTab, h10, ↓reduceDIte]
      exact hv_col (P := P) (w := w) (m := m) (q := q) ox ow om l
  intro e he
  refine Eq.trans ?_ (ring_cut_table e he)
  unfold cutTab
  congr 1
  apply filter_congr
  intro i hi
  have hi' : i < 10 := mem_range.mp hi
  rw [col i (by omega), col (i + 1) (by omega), col i (by omega), col (i + 1) (by omega)]
  have fi := fun a b => frm_inj (P := P) (c := (piMove P)^[k] s) (j := j) hd.1 (a := a) (b := b)
  have fb : ∀ a b, (frm P ((piMove P)^[k] s) j a == frm P ((piMove P)^[k] s) j b) = (a == b) := by
    intro a b; rw [Bool.eq_iff_iff, beq_iff_eq, beq_iff_eq, fi]
  simp only [bne, fb]

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.enc_swap
#print axioms SimpleGraph.QuarterFloor.swap_support
#print axioms SimpleGraph.QuarterFloor.swap_edge_colour
#print axioms SimpleGraph.QuarterFloor.swap_edge_colour_ne
#print axioms SimpleGraph.QuarterFloor.closed_orbit_cut_sum
#print axioms SimpleGraph.QuarterFloor.kempe_orbit_cut_sum
#print axioms SimpleGraph.QuarterFloor.closed_orbit_cut_parity
#print axioms SimpleGraph.QuarterFloor.closed_orbit_cut_even
#print axioms SimpleGraph.QuarterFloor.piMove_cut_sum
#print axioms SimpleGraph.QuarterFloor.ring_cut_table
#print axioms SimpleGraph.QuarterFloor.allDL_ring_cut_count
