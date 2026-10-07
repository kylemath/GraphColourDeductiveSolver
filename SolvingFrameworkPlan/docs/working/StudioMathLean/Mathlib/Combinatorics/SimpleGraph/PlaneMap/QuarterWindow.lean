/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterLockJ

/-!
# Period bookkeeping, far-ness of step 8, and the window lemma (`NightA34.md` §1–§3)

Setting of `QuarterGammaPeriod`/`QuarterPeriodJ`/`QuarterLockJ`: an all-`DL` `π`-orbit
`s n = π^[n] s` from an `R3k4` state at a `(5,5,5,5,6)` hole `Hole6 P w m q`, with the fixed
names `p = x q`, `x⁺ = x (q+1)`, `z = w q`, `w⁺ = w (q+1)`, `w₂ = w (q+2)`, `w₃ = w (q+3)`,
`y = w (q+4)`, `m`.

## Colour letters

At a state doubly locked at `j` the four colours are named by the *frame*
`frm c j = ![α, μ, A, B] = ![c (x j), c (x (j+1)), c (x (j+3)), c (x (j+4))]`, letters
`0 = α, 1 = μ, 2 = A, 3 = B`. Along a `DD` step the frame of the image (at `j + 3`) is
`frm c j ∘ sig`, `sig = ![0, 3, 1, 2]` (`frm_step`), so after `i` steps it is
`frm c j ∘ sig^[i]` (`frm_iter`).

## Main results (sorry-free, no new axioms)

1. **State tables.** `r3_full`: every `R3` `DD` state has the full ring `(B, A, B, μ, A)`
   (from `w j`) at every `k` (at `k = 4` given `z = A`, the pair fact). `r1_full`: every `R1`
   `DD` state has the full ring `(A, B, μ, α, μ)` at every `k` (at `R1k0`, `w (j+4) = μ` comes
   from the step: `w (j+3)` is recoloured `A`, `w (j+4)` is not). `m` is the fourth colour of
   `p, y, z` (`mL`). `state_tab`: all eleven hole vertices in frame letters.
2. **`bookkeeping`**: anchored at an `R3k4` state `s k` (`k > 0`, `k % 10 = 0`, frame
   `![α, μ, A, B]` of that state, repeat index `j = q + 1`), for every position `i < 10` the
   colours of `x (q+t)`, `w (q+t)`, `m` at `s (k + i)` are `frm (s k) j` of the letter in
   `xTab i t`, `wTab i t`, `mTab i`: exactly the table of `NightA34.md` §1.1 (period
   `b ≡ 0 mod 3`, with `α = 0, μ = 1, A = 2, B = 3`). `orbit_colour` is the version for any
   anchor `n > 0` and any offset.
3. **Locks between fixed ring vertices.** `lock_join_R3`, `lock_join_R1` (state level) and
   `lock1_join_pos`, `lock2_join_pos` (orbit, every `n > 0`): `Lock1 ⇔ w (q+a) ~ w (q+b)` in the
   two-colour graph of their own colours, with `(a, b) = lock1Off (gseq n)`, and likewise
   `Lock2` with `lock2Off`; `lock1Off_table`, `lock2Off_table` list the ten positions
   (`NightA34.md` §1.2). `J_join_pos`: `J` is `y ~ z` in the graph of the two colours named by
   the state table (on the window, `window_forced` identifies it with the `Lock1`/`Lock2`
   graph of §1.2).
4. **`step8_far`**: at position `8` (`R3k0`, `j = q`), the step-8 swapped component
   `K_{α,A}(x (q+2))` contains none of `p, m, y, z`, and the step leaves their colours
   unchanged. `p ∉ K` is `Rot3Def`, i.e. the library's Kempe separation by the `Lock2` chain
   (`rot3Def_of_lock2`, from `alternating_walks_intersect`); `y ∉ K` since `y` is `A` and
   adjacent to `p`; `m, z` have colours `μ, B` outside the pair.
5. **Window lemma.** `window_pair`: from position `9` to position `4` of the next period the
   colours of `y` and `z` are constant, so `G_J` is the two-colour graph of one fixed pair.
   `window_forced`: `y ~ w₂` in `G_J` at positions `9` and `0`, `z ~ w₂` at positions `2` and
   `3`, `y ~ w₂ ~ z` at `4` (the `Lock2`/`Lock1` pair of §1.2 is the `J` pair there:
   `wcol_eq`). `J_iff_window`: `J ⇔ w₂ ~ z` at `9, 0` and `J ⇔ y ~ w₂` at `2, 3`. Hence
   `k4_failure_iff_z_split` (`k = 4` failure ⇔ `y ~ w₂`, `w₂ ≁ z` at positions `9` and `0`)
   and `k3_failure_iff_y_split` (`k = 3` failure ⇔ `z ~ w₂`, `y ≁ w₂` at positions `2`, `3`).
6. **The period rotates the colours** (Studio Job AN). `period_colour_rotation`: for `n > 0`
   every hole vertex with letter `ℓ` at `s n` has letter `σ ℓ` at `s (n+10)` (frame of `s n`);
   `σ` fixes `α` and is a 3-cycle on `μ, A, B` (`sig_three_cycle`). `closing_perm`: if
   `π^[L] s = s`, then `σ^[L] = id`, `10 ∣ L`, `3 ∣ L`, hence `30 ∣ L`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Letter tables -/

/-- Link letters from `x j`: `(α, μ, α, A, B)`. -/
def linkL : Fin 5 → Fin 4 := ![0, 1, 0, 2, 3]

/-- Ring letters from `w j`: `R3 = (B, A, B, μ, A)`, `R1 = (A, B, μ, α, μ)`. -/
def ringL : GType → Fin 5 → Fin 4
  | .R3 => ![3, 2, 3, 1, 2]
  | .R1 => ![2, 3, 1, 0, 1]

/-- The letter of `m`: the fourth colour of `p, y, z`. -/
def mL : GType × Fin 5 → Fin 4
  | (.R3, k) => ![1, 0, 1, 0, 0] k
  | (.R1, k) => ![3, 0, 2, 3, 2] k

/-- The frame change along a `DD` step: `(α, μ, A, B) ↦ (α, B, μ, A)`. -/
def sig : Fin 4 → Fin 4 := ![0, 3, 1, 2]

/-- The letter of `x (q + t)` at a state of `(type, k)`. -/
def xL (x : GType × Fin 5) (t : Fin 5) : Fin 4 := linkL (x.2 + t)

/-- The letter of `w (q + t)` at a state of `(type, k)`. -/
def wL (x : GType × Fin 5) (t : Fin 5) : Fin 4 := ringL x.1 (x.2 + t)

/-- `NightA34.md` §1.1, columns `x₀..x₄` (relative to `q`), positions `0..9`, in the letters of
the anchoring `R3k4` state (`0 = α, 1 = μ, 2 = A, 3 = B`). -/
def xTab : Fin 10 → Fin 5 → Fin 4 :=
  ![![3, 0, 1, 0, 2], ![3, 0, 1, 2, 0], ![3, 1, 0, 2, 0], ![0, 1, 0, 2, 3], ![0, 1, 2, 0, 3],
    ![1, 0, 2, 0, 3], ![1, 0, 2, 3, 0], ![1, 2, 0, 3, 0], ![0, 2, 0, 3, 1], ![0, 2, 3, 0, 1]]

/-- `NightA34.md` §1.1, columns `w₀..w₄`. -/
def wTab : Fin 10 → Fin 5 → Fin 4 :=
  ![![2, 3, 2, 3, 1], ![2, 3, 0, 3, 1], ![2, 3, 1, 3, 1], ![2, 3, 1, 0, 1], ![2, 3, 1, 2, 1],
    ![2, 3, 1, 2, 0], ![2, 3, 1, 2, 3], ![0, 3, 1, 2, 3], ![1, 3, 1, 2, 3], ![1, 0, 1, 2, 3]]

/-- `NightA34.md` §1.1, column `c(m)`. -/
def mTab : Fin 10 → Fin 4 := ![0, 0, 0, 3, 3, 3, 0, 2, 2, 2]

theorem xTab_eq : ∀ i : Fin 10, ∀ t : Fin 5, xTab i t = sig^[i.val] (xL (gseq i.val) t) := by
  decide

theorem wTab_eq : ∀ i : Fin 10, ∀ t : Fin 5, wTab i t = sig^[i.val] (wL (gseq i.val) t) := by
  decide

theorem mTab_eq : ∀ i : Fin 10, mTab i = sig^[i.val] (mL (gseq i.val)) := by
  decide

lemma forall_fin5 {p : Fin 5 → Prop} (h0 : p 0) (h1 : p 1) (h2 : p 2) (h3 : p 3) (h4 : p 4) :
    ∀ r, p r := by
  intro r; obtain rfl | rfl | rfl | rfl | rfl := fin5_five r <;> assumption

/-- `Lock1` ends `(a, b)`: `Lock1 ⇔ w (q+a) ~ w (q+b)`. `R3`: `w (j+1) ~ w (j+3)`;
`R1`: `w j ~ w (j+2)`; with `j = q - k`. -/
def lock1Off : GType × Fin 5 → Fin 5 × Fin 5
  | (.R3, k) => (1 - k, 3 - k)
  | (.R1, k) => (0 - k, 2 - k)

/-- `Lock2` ends `(a, b)`: `R3`: `w j ~ w (j+3)`; `R1`: `w (j+1) ~ w (j+4)`. -/
def lock2Off : GType × Fin 5 → Fin 5 × Fin 5
  | (.R3, k) => (0 - k, 3 - k)
  | (.R1, k) => (1 - k, 4 - k)

/-- `NightA34.md` §1.2, column `Lock1` (`0 = z, 1 = w⁺, 2 = w₂, 3 = w₃, 4 = y`). -/
theorem lock1Off_table : (List.range 10).map (fun i => lock1Off (gseq i)) =
    [(2, 4), (4, 1), (3, 0), (0, 2), (4, 1), (1, 3), (0, 2), (2, 4), (1, 3), (3, 0)] := by
  decide

/-- `NightA34.md` §1.2, column `Lock2`. -/
theorem lock2Off_table : (List.range 10).map (fun i => lock2Off (gseq i)) =
    [(1, 4), (0, 3), (2, 0), (1, 4), (3, 1), (2, 0), (4, 2), (3, 1), (0, 3), (4, 2)] := by
  decide

lemma off_eq (j k a : Fin 5) : j + k + (a - k) = j + a := by abel

/-- Reachability between two vertices each of which has a single neighbour. -/
lemma reach_ends {V : Type*} {G : SimpleGraph V} {a a' b b' : V} (ea : G.Adj a a')
    (oa : ∀ v, G.Adj a v → v = a') (eb : G.Adj b b') (ob : ∀ v, G.Adj b v → v = b')
    (hab : a ≠ b) : G.Reachable a b ↔ G.Reachable a' b' := by
  constructor
  · intro r
    have r1 := reach_of_only hab ob r
    by_cases e : b' = a
    · subst e
      have := oa b eb.symm
      subst this
      exact r.symm
    · exact (reach_of_only e oa r1.symm).symm
  · intro r
    exact ea.reachable.trans (r.trans eb.reachable.symm)

/-- A vertex reached from `s ≠ v` in a two-colour graph carries one of the two colours. -/
lemma reach_col {V C : Type*} {G : SimpleGraph V} {h s v : V} {c : V → C} {a b : C}
    (r : (pairGraph G h c a b).Reachable s v) (hsv : s ≠ v) : c v = a ∨ c v = b := by
  obtain ⟨p⟩ := r.symm
  cases p with
  | nil => exact (hsv rfl).elim
  | cons e _ => exact e.2.1.2

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}
  {c : Fin n → Fin 4} {j : Fin 5}

variable (P) in
/-- The frame `![α, μ, A, B]` of a state at repeat index `j`. -/
def frm (c : Fin n → Fin 4) (j : Fin 5) : Fin 4 → Fin 4 :=
  ![c (P.x j), c (P.x (j + 1)), c (P.x (j + 3)), c (P.x (j + 4))]

/-! ### 1. State tables -/

variable (P w) in
/-- The full `R1` ring `(A, B, μ, α, μ)` from `w j`. -/
def R1Full (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  c (w j) = c (P.x (j + 3)) ∧ c (w (j + 1)) = c (P.x (j + 4)) ∧
    c (w (j + 2)) = c (P.x (j + 1)) ∧ c (w (j + 3)) = c (P.x j) ∧
    c (w (j + 4)) = c (P.x (j + 1))

/-- **`R3` full ring** at every position (at `k = 4` given `z = A`). -/
theorem r3_full {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR3 P w c j) (hz : k = 4 → c (w q) = c (P.x (j + 3))) :
    R3At P w c j := by
  obtain rfl | rfl | rfl | rfl | rfl := fin5_five k
  · subst hq
    obtain ⟨t0, t3⟩ := hT
    obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hD.1.1
    obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
    obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
    obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
    have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl (fin5_ne (by decide))
    refine ⟨hD.1, t0, ?_, ?_, t3, ?_⟩
    · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r01 t0; omega
    · clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
    · clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 t3; omega
  · subst hq
    obtain ⟨t0, t3⟩ := hT
    obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hD.1.1
    obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
    obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
    obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
    have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl (fin5_ne (by decide))
    have w2 : c (w (j + 2)) = c (P.x (j + 4)) := by
      clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
    refine ⟨hD.1, t0, ?_, w2, t3, ?_⟩
    · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r12 w2; omega
    · clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 t3; omega
  · subst hq
    obtain ⟨t0, t3⟩ := hT
    obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hD.1.1
    obtain ⟨d1, d1'⟩ := H.domAt hc (j := j) (a := 1) (b := 2) rfl
    obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
    obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
    have r01 := H.ring0 hc (j := j) (fin5_ne (by decide))
    have r23 := H.ringAt hc (j := j) (a := 2) (b := 3) rfl (fin5_ne (by decide))
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl (fin5_ne (by decide))
    refine ⟨hD.1, t0, ?_, ?_, t3, ?_⟩
    · clear * - h1 h3 h4 h13 h14 h34 h02 d1 d1' r01 t0; omega
    · clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r23 t3; omega
    · clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 t3; omega
  · exact r3k3_R3At H hq hc hD hT
  · exact r3k4_R3At H hq hc hD.1 hT (hz rfl)

/-- **`R1` full ring** at every position. -/
theorem r1_full {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hD : DDstate P c j) (hT : TypeR1 P w c j) : R1Full P w c j := by
  obtain ⟨w1, w3⟩ := r1_ring H hq hc hD hT
  have hT' := hT
  unfold TypeR1 at hT'
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hD.1.1
  obtain ⟨d2, d2'⟩ := H.domAt hc (j := j) (a := 2) (b := 3) rfl
  obtain ⟨d4, d4'⟩ := H.dom4 hc (j := j)
  have hw2 : c (w (j + 2)) = c (P.x (j + 1)) := by
    by_cases hk : k = 2
    · subst hk
      exact (lock2_R1k2 H hq hc hD hT).2.1
    · have r12 := H.ringAt hc (j := j) (a := 1) (b := 2) rfl
        (by rw [hq]; exact fin5_ne (Ne.symm hk))
      clear * - h1 h3 h4 h13 h14 h34 h02 d2 d2' r12 w1; omega
  refine ⟨hT', w1, hw2, w3, ?_⟩
  by_cases hk : k = 0
  · subst hk
    rw [add_zero] at hq
    subst q
    obtain ⟨hπ, hr, hK, -, -, -⟩ := dd_ends hc hD
    obtain ⟨-, hp', -, -, -⟩ := rot3_move hc hr hD.1.2.2
    have e3 := rot3_K3 hr (H.adj_w (j + 3)) (H.offh _) (Or.inl w3)
    rw [w3, Equiv.swap_apply_left] at e3
    have e4 := rot3_K0 hK (H.adj_w4 j) (H.offh _)
    have g := H.ring (j + 3) (by rw [add_assoc]; exact (fin5_ne0 (a := 4) (by decide)).symm)
    have ne : rot3 P c j (w (j + 3)) ≠ rot3 P c j (w (j + 4)) :=
      hp' (by simpa only [add_assoc, Fin.reduceAdd] using g) (H.offh _) (H.offh _)
    rw [e3, e4] at ne
    have r34 := H.ringAt hc (j := j) (a := 3) (b := 4) rfl
      (fin5_ne0 (a := 4) (by decide)).symm
    clear * - h1 h3 h4 h13 h14 h34 d4 d4' r34 w3 ne; omega
  · have r40 := H.ring4 hc (j := j) (by rw [hq]; exact fin5_ne0 hk)
    clear * - h1 h3 h4 h13 h14 h34 d4 d4' r40 hT'; omega

lemma forall_fin4 {p : Fin 4 → Prop} (h0 : p 0) (h1 : p 1) (h2 : p 2) (h3 : p 3) :
    ∀ r, p r := by
  intro r; fin_cases r <;> assumption

/-- `m` at an `R3` state: the fourth colour of `p, y, z`. -/
theorem m_R3 {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hR : R3At P w c j) : c m = frm P c j (mL (.R3, k)) := by
  have am := hc H.adj_m (P.x_ne_h _) H.offmh
  have ay := hc H.ringy (H.offh _) H.offmh
  have az := hc H.ringz H.offmh (H.offh _)
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -⟩, e0, e1, e2, e3, e4⟩ := hR
  subst hq
  obtain rfl | rfl | rfl | rfl | rfl := fin5_five k <;>
    simp only [add_assoc, Fin.reduceAdd, add_zero] at am ay az
  · show c m = c (P.x (j + 1))
    clear * - h1 h3 h4 h13 h14 h34 am ay az e0 e4; omega
  · show c m = c (P.x j)
    clear * - h1 h3 h4 h13 h14 h34 am ay az e0 e1; omega
  · show c m = c (P.x (j + 1))
    clear * - h1 h3 h4 h13 h14 h34 h02 am ay az e1 e2; omega
  · show c m = c (P.x j)
    clear * - h1 h3 h4 h13 h14 h34 am ay az e2 e3; omega
  · show c m = c (P.x j)
    clear * - h1 h3 h4 h13 h14 h34 am ay az e3 e4; omega

/-- `m` at an `R1` state: the fourth colour of `p, y, z`. -/
theorem m_R1 {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k) (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) (hF : R1Full P w c j) : c m = frm P c j (mL (.R1, k)) := by
  have am := hc H.adj_m (P.x_ne_h _) H.offmh
  have ay := hc H.ringy (H.offh _) H.offmh
  have az := hc H.ringz H.offmh (H.offh _)
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨e0, e1, e2, e3, e4⟩ := hF
  subst hq
  obtain rfl | rfl | rfl | rfl | rfl := fin5_five k <;>
    simp only [add_assoc, Fin.reduceAdd, add_zero] at am ay az
  · show c m = c (P.x (j + 4))
    clear * - h1 h3 h4 h13 h14 h34 am ay az e0 e4; omega
  · show c m = c (P.x j)
    clear * - h1 h3 h4 h13 h14 h34 am ay az e0 e1; omega
  · show c m = c (P.x (j + 3))
    clear * - h1 h3 h4 h13 h14 h34 h02 am ay az e1 e2; omega
  · show c m = c (P.x (j + 4))
    clear * - h1 h3 h4 h13 h14 h34 am ay az e2 e3; omega
  · show c m = c (P.x (j + 3))
    clear * - h1 h3 h4 h13 h14 h34 am ay az e3 e4; omega

variable (P w m) in
/-- All eleven hole vertices of a state of `(type, k)` at repeat index `j`, in frame letters. -/
def StateTab (c : Fin n → Fin 4) (j : Fin 5) (t : GType) (k : Fin 5) : Prop :=
  (∀ r, c (P.x (j + r)) = frm P c j (linkL r)) ∧ (∀ r, c (w (j + r)) = frm P c j (ringL t r)) ∧
    c m = frm P c j (mL (t, k))

lemma link_tab (hr : RepeatAt P c j) : ∀ r, c (P.x (j + r)) = frm P c j (linkL r) := by
  obtain ⟨h02, -⟩ := hr
  refine forall_fin5 ?_ ?_ ?_ ?_ ?_
  · show c (P.x (j + 0)) = c (P.x j); rw [add_zero]
  · rfl
  · exact h02.symm
  · rfl
  · rfl

/-- **The state table** at a `DD` state of `(type, k)` (at `R3k4` given `z = A`). -/
theorem state_tab {t : GType} {k : Fin 5} (H : Hole6 P w m q) (hq : q = j + k)
    (hc : ProperOff M.graph h c) (hD : DDstate P c j) (hT : TypeOf P w t c j)
    (hz : t = .R3 → k = 4 → c (w q) = c (P.x (j + 3))) : StateTab P w m c j t k := by
  cases t
  · have hF := r1_full H hq hc hD hT
    refine ⟨link_tab hD.1.1, ?_, m_R1 H hq hc hD.1.1 hF⟩
    obtain ⟨e0, e1, e2, e3, e4⟩ := hF
    refine forall_fin5 ?_ ?_ ?_ ?_ ?_
    · show c (w (j + 0)) = c (P.x (j + 3)); rw [add_zero]; exact e0
    · exact e1
    · exact e2
    · exact e3
    · exact e4
  · have hR := r3_full H hq hc hD hT (hz rfl)
    refine ⟨link_tab hD.1.1, ?_, m_R3 H hq hc hR⟩
    obtain ⟨-, e0, e1, e2, e3, e4⟩ := hR
    refine forall_fin5 ?_ ?_ ?_ ?_ ?_
    · show c (w (j + 0)) = c (P.x (j + 4)); rw [add_zero]; exact e0
    · exact e1
    · exact e2
    · exact e3
    · exact e4

/-- **The frame along a `DD` step**: `frm (π c) (j+3) = frm c j ∘ sig`. -/
theorem frm_step (hc : ProperOff M.graph h c) (hD : DDstate P c j) :
    ∀ a, frm P (piMove P c) (j + 3) a = frm P c j (sig a) := by
  obtain ⟨hπ, hr, hK, -⟩ := dd_ends hc hD
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values hr hK
  refine forall_fin4 ?_ ?_ ?_ ?_
  · show piMove P c (P.x (j + 3)) = c (P.x j); rw [hπ, v3]
  · show piMove P c (P.x (j + 3 + 1)) = c (P.x (j + 4))
    rw [hπ]; simp only [add_assoc, Fin.reduceAdd]; exact v4
  · show piMove P c (P.x (j + 3 + 3)) = c (P.x (j + 1))
    rw [hπ]; simp only [add_assoc, Fin.reduceAdd]; exact v1
  · show piMove P c (P.x (j + 3 + 4)) = c (P.x (j + 3))
    rw [hπ]; simp only [add_assoc, Fin.reduceAdd]; exact v2

/-! ### 2. Locks as joins of fixed ring vertices -/

lemma Hole6.link_nbr (H : Hole6 P w m q) (t : Fin 5) {v : Fin n} (e : M.graph.Adj (P.x t) v) :
    v = h ∨ v = P.x (t + 4) ∨ v = P.x (t + 1) ∨ v = w (t + 4) ∨ v = w t ∨ (t = q ∧ v = m) := by
  by_cases ht : t = q
  · subst ht
    rcases (H.nbrq v).1 e with h' | h' | h' | h' | h' | h'
    · exact Or.inl h'
    · exact Or.inr (Or.inl h')
    · exact Or.inr (Or.inr (Or.inl h'))
    · exact Or.inr (Or.inr (Or.inr (Or.inl h')))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨rfl, h'⟩))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl h'))))
  · rcases (H.nbr t ht v).1 e with h' | h' | h' | h' | h'
    · exact Or.inl h'
    · exact Or.inr (Or.inl h')
    · exact Or.inr (Or.inr (Or.inl h'))
    · exact Or.inr (Or.inr (Or.inr (Or.inl h')))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl h'))))

/-- Discharge one neighbour case of a lock end. -/
macro "lock_end_case" : tactic => `(tactic| first
  | rfl
  | (simp only [add_assoc, Fin.reduceAdd, add_zero]; done)
  | (exfalso; (try simp only [add_assoc, Fin.reduceAdd, add_zero] at *); omega))

/-- **Locks at an `R3` state** (any `k`): `Lock1 ⇔ w (j+1) ~ w (j+3)` and
`Lock2 ⇔ w j ~ w (j+3)`, each in the two-colour graph of its own two colours. -/
theorem lock_join_R3 (H : Hole6 P w m q) (hR : R3At P w c j)
    (hm : q = j + 1 ∨ q = j + 3 ∨ q = j + 4 → c m = c (P.x j)) :
    (Lock1 P c j ↔ (pairGraph M.graph h c (c (w (j + 1))) (c (w (j + 3)))).Reachable
      (w (j + 1)) (w (j + 3))) ∧
    (Lock2 P c j ↔ (pairGraph M.graph h c (c (w j)) (c (w (j + 3)))).Reachable
      (w j) (w (j + 3))) := by
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -⟩, e0, e1, e2, e3, e4⟩ := hR
  have a1 := H.adj_w (j + 1)
  have a3 := H.adj_w (j + 3)
  have a0 := H.adj_w' j
  have a4 := H.adj_w4 (j + 4)
  simp only [add_assoc, Fin.reduceAdd] at a4
  constructor
  · unfold Lock1
    rw [e1, e3, pairGraph_comm_gen c (c (P.x (j + 3)))]
    refine reach_ends ⟨a1, ⟨P.x_ne_h _, Or.inl rfl⟩, ⟨H.offh _, Or.inr e1⟩⟩ ?_
      ⟨a3, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨H.offh _, Or.inl e3⟩⟩ ?_
      (fun e => fin5_ne (by decide) (P.inj e))
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 1) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 3) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case
  · unfold Lock2
    rw [e0, e3, pairGraph_comm_gen c (c (P.x (j + 4)))]
    refine reach_ends ⟨a0, ⟨P.x_ne_h _, Or.inl rfl⟩, ⟨H.offh _, Or.inr e0⟩⟩ ?_
      ⟨a4, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨H.offh _, Or.inl e3⟩⟩ ?_
      (fun e => fin5_ne (by decide) (P.inj e))
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 1) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 4) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case

/-- **Locks at an `R1` state** (any `k`): `Lock1 ⇔ w j ~ w (j+2)` and
`Lock2 ⇔ w (j+1) ~ w (j+4)`. -/
theorem lock_join_R1 (H : Hole6 P w m q) (hr : RepeatAt P c j) (hF : R1Full P w c j)
    (hm1 : q = j + 1 → c m = c (P.x j)) (hm3 : q = j + 3 → c m = c (P.x (j + 4)))
    (hm4 : q = j + 4 → c m = c (P.x (j + 3))) :
    (Lock1 P c j ↔ (pairGraph M.graph h c (c (w j)) (c (w (j + 2)))).Reachable
      (w j) (w (j + 2))) ∧
    (Lock2 P c j ↔ (pairGraph M.graph h c (c (w (j + 1))) (c (w (j + 4)))).Reachable
      (w (j + 1)) (w (j + 4))) := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨e0, e1, e2, e3, e4⟩ := hF
  have a1 := H.adj_w (j + 1)
  have a4 := H.adj_w (j + 4)
  have a0 := H.adj_w' j
  have a3 := H.adj_w4 (j + 3)
  simp only [add_assoc, Fin.reduceAdd] at a3
  constructor
  · unfold Lock1
    rw [e0, e2, pairGraph_comm_gen c (c (P.x (j + 3)))]
    refine reach_ends ⟨a0, ⟨P.x_ne_h _, Or.inl rfl⟩, ⟨H.offh _, Or.inr e0⟩⟩ ?_
      ⟨a3, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨H.offh _, Or.inl e2⟩⟩ ?_
      (fun e => fin5_ne (by decide) (P.inj e))
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 1) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 3) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case
  · unfold Lock2
    rw [e1, e4, pairGraph_comm_gen c (c (P.x (j + 4)))]
    refine reach_ends ⟨a1, ⟨P.x_ne_h _, Or.inl rfl⟩, ⟨H.offh _, Or.inr e1⟩⟩ ?_
      ⟨a4, ⟨P.x_ne_h _, Or.inr rfl⟩, ⟨H.offh _, Or.inl e4⟩⟩ ?_
      (fun e => fin5_ne (by decide) (P.inj e))
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 1) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case
    · rintro v ⟨e, -, vh, vc⟩
      rcases H.link_nbr (j + 4) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (vh rfl).elim
      all_goals lock_end_case

section orbit
variable {s : Fin n → Fin 4} {j₀ : Fin 5}

/-- The frame after `i` steps of an all-`DL` orbit: `frm (s (n+i)) = frm (s n) ∘ sig^[i]`. -/
theorem frm_iter (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (n : ℕ) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[n] s) j) :
    ∀ i (j' : Fin 5), RepeatAt P ((piMove P)^[n + i] s) j' →
      ∀ a, frm P ((piMove P)^[n + i] s) j' a = frm P ((piMove P)^[n] s) j (sig^[i] a) := by
  intro i
  induction i with
  | zero =>
    intro j' hj' a
    have e := rep_unique hj hj'
    subst e
    rfl
  | succ i ih =>
    intro j' hj' a
    obtain ⟨j1, hd1⟩ := hall (n + i)
    have hD := orbit_dd hc hall (n + i) j1 hd1
    have hr2 : RepeatAt P ((piMove P)^[n + (i + 1)] s) (j1 + 3) := by
      rw [← add_assoc, Function.iterate_succ_apply']; exact hD.2.1
    have e := rep_unique hr2 hj'
    subst e
    have st := frm_step (iter_proper hc (n + i)) hD a
    rw [← Function.iterate_succ_apply' (piMove P)] at st
    rw [show n + (i + 1) = (n + i).succ by omega, st, ih j1 hd1.1,
      Function.iterate_succ_apply]

/-- The state table along the orbit, at every `n > 0`. -/
theorem orbit_tab (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ∃ j, DoublyLocked P ((piMove P)^[n] s) j ∧ q = j + (gseq n).2 ∧
      StateTab P w m ((piMove P)^[n] s) j (gseq n).1 (gseq n).2 := by
  obtain ⟨tk, pr, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  obtain ⟨j, hd, hq', hT'⟩ := tk n
  have pz := pr n hn j hd.1
  refine ⟨j, hd, hq', state_tab H hq' (iter_proper hc n) (orbit_dd hc hall n j hd) hT' ?_⟩
  intro e1 e2
  rw [e1, e2, pv_R3_4] at pz
  exact pz.2

/-- **Colours along the orbit in the letters of an anchor** `s n`, `n > 0`. -/
theorem orbit_colour (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[n] s) j) (i : ℕ) :
    (∀ t, ((piMove P)^[n + i] s) (P.x (q + t)) =
      frm P ((piMove P)^[n] s) j (sig^[i] (xL (gseq (n + i)) t))) ∧
    (∀ t, ((piMove P)^[n + i] s) (w (q + t)) =
      frm P ((piMove P)^[n] s) j (sig^[i] (wL (gseq (n + i)) t))) ∧
    ((piMove P)^[n + i] s) m = frm P ((piMove P)^[n] s) j (sig^[i] (mL (gseq (n + i)))) := by
  obtain ⟨j', hd', hq', ⟨tx, tw, tm⟩⟩ := orbit_tab H hc hall hr hq hT (n + i) (by omega)
  have fi := frm_iter hc hall n hj i j' hd'.1
  refine ⟨fun t => ?_, fun t => ?_, ?_⟩
  · rw [hq', add_assoc, tx, fi]; rfl
  · rw [hq', add_assoc, tw, fi]; rfl
  · rw [tm, fi]

/-- **(1) Bookkeeping** (`NightA34.md` §1.1). Anchor: an `R3k4` state `s k`, `k > 0`,
`k % 10 = 0`, doubly locked at `j = q + 1`, with letters `frm (s k) j = ![α, μ, A, B]`. At each
position `i < 10` of the period, `x (q+t)`, `w (q+t)`, `m` have the colours named by
`xTab i t`, `wTab i t`, `mTab i`. -/
theorem bookkeeping (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk0 : 0 < k) (hk : k % 10 = 0) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j + 4 ∧ ∀ i : Fin 10,
      (∀ t, ((piMove P)^[k + i] s) (P.x (q + t)) = frm P ((piMove P)^[k] s) j (xTab i t)) ∧
      (∀ t, ((piMove P)^[k + i] s) (w (q + t)) = frm P ((piMove P)^[k] s) j (wTab i t)) ∧
      ((piMove P)^[k + i] s) m = frm P ((piMove P)^[k] s) j (mTab i) := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R3, 4) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', -⟩ := tk k
  rw [g] at hq'
  refine ⟨j, hd, hq', fun i => ?_⟩
  have gi : gseq (k + i.val) = gseq i.val := by
    rw [gseq_mod, gseq_mod i.val]; congr 1; omega
  obtain ⟨ox, ow, om⟩ := orbit_colour H hc hall hr hq hT k hk0 hd.1 i.val
  rw [gi] at ox ow om
  refine ⟨fun t => ?_, fun t => ?_, ?_⟩
  · rw [ox, xTab_eq]
  · rw [ow, wTab_eq]
  · rw [om, mTab_eq]

/-- The `R3At`/`R1Full` facts and the `m`-conditions of a state table. -/
lemma tab_R3 {k : Fin 5} (hd : DoublyLocked P c j) (hq : q = j + k)
    (tab : StateTab P w m c j .R3 k) :
    R3At P w c j ∧ (q = j + 1 ∨ q = j + 3 ∨ q = j + 4 → c m = c (P.x j)) := by
  obtain ⟨-, tw, tm⟩ := tab
  have t0 := tw 0
  rw [add_zero] at t0
  refine ⟨⟨hd, t0, tw 1, tw 2, tw 3, tw 4⟩, ?_⟩
  rintro (e | e | e) <;> have e' := add_left_cancel (hq.symm.trans e) <;> subst e' <;> exact tm

lemma tab_R1 {k : Fin 5} (hq : q = j + k) (tab : StateTab P w m c j .R1 k) :
    R1Full P w c j ∧ (q = j + 1 → c m = c (P.x j)) ∧ (q = j + 3 → c m = c (P.x (j + 4))) ∧
      (q = j + 4 → c m = c (P.x (j + 3))) := by
  obtain ⟨-, tw, tm⟩ := tab
  have t0 := tw 0
  rw [add_zero] at t0
  refine ⟨⟨t0, tw 1, tw 2, tw 3, tw 4⟩, ?_, ?_, ?_⟩ <;>
    intro e <;> have e' := add_left_cancel (hq.symm.trans e) <;> subst e' <;> exact tm

/-- **(2) Locks between fixed ring vertices, every position.** At every `n > 0` of the orbit,
`Lock1 ⇔ w (q+a) ~ w (q+b)` with `(a, b) = lock1Off (gseq n)` and `Lock2 ⇔ w (q+a') ~ w (q+b')`
with `(a', b') = lock2Off (gseq n)`, each in the two-colour graph of the two ring vertices'
own colours (`lock1Off_table`, `lock2Off_table`: `NightA34.md` §1.2). -/
theorem lock_join_pos (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ∃ j, DoublyLocked P ((piMove P)^[n] s) j ∧ q = j + (gseq n).2 ∧
      (Lock1 P ((piMove P)^[n] s) j ↔
        (pairGraph M.graph h ((piMove P)^[n] s)
          (((piMove P)^[n] s) (w (q + (lock1Off (gseq n)).1)))
          (((piMove P)^[n] s) (w (q + (lock1Off (gseq n)).2)))).Reachable
          (w (q + (lock1Off (gseq n)).1)) (w (q + (lock1Off (gseq n)).2))) ∧
      (Lock2 P ((piMove P)^[n] s) j ↔
        (pairGraph M.graph h ((piMove P)^[n] s)
          (((piMove P)^[n] s) (w (q + (lock2Off (gseq n)).1)))
          (((piMove P)^[n] s) (w (q + (lock2Off (gseq n)).2)))).Reachable
          (w (q + (lock2Off (gseq n)).1)) (w (q + (lock2Off (gseq n)).2))) := by
  obtain ⟨j, hd, hq', tab⟩ := orbit_tab H hc hall hr hq hT n hn
  refine ⟨j, hd, hq', ?_⟩
  generalize gseq n = g at hq' tab
  obtain ⟨t, k⟩ := g
  dsimp only at hq' tab
  cases t
  · obtain ⟨hF, hm1, hm3, hm4⟩ := tab_R1 hq' tab
    have L := lock_join_R1 H hd.1 hF hm1 hm3 hm4
    simp only [lock1Off, lock2Off]
    rw [hq']
    simp only [off_eq, add_zero]
    exact L
  · obtain ⟨hR, hm⟩ := tab_R3 hd hq' tab
    have L := lock_join_R3 H hR hm
    simp only [lock1Off, lock2Off]
    rw [hq']
    simp only [off_eq, add_zero]
    exact L

/-- `Lock1` as a join of fixed ring vertices (the first half of `lock_join_pos`), with the
join itself (true on the all-`DL` orbit). -/
theorem lock1_join_pos (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ∃ j, DoublyLocked P ((piMove P)^[n] s) j ∧
      (Lock1 P ((piMove P)^[n] s) j ↔
        (pairGraph M.graph h ((piMove P)^[n] s)
          (((piMove P)^[n] s) (w (q + (lock1Off (gseq n)).1)))
          (((piMove P)^[n] s) (w (q + (lock1Off (gseq n)).2)))).Reachable
          (w (q + (lock1Off (gseq n)).1)) (w (q + (lock1Off (gseq n)).2))) ∧
      (pairGraph M.graph h ((piMove P)^[n] s)
          (((piMove P)^[n] s) (w (q + (lock1Off (gseq n)).1)))
          (((piMove P)^[n] s) (w (q + (lock1Off (gseq n)).2)))).Reachable
          (w (q + (lock1Off (gseq n)).1)) (w (q + (lock1Off (gseq n)).2)) := by
  obtain ⟨j, hd, -, L1, -⟩ := lock_join_pos H hc hall hr hq hT n hn
  exact ⟨j, hd, L1, L1.1 hd.2.1⟩

/-- `Lock2` as a join of fixed ring vertices, with the join itself. -/
theorem lock2_join_pos (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ∃ j, DoublyLocked P ((piMove P)^[n] s) j ∧
      (Lock2 P ((piMove P)^[n] s) j ↔
        (pairGraph M.graph h ((piMove P)^[n] s)
          (((piMove P)^[n] s) (w (q + (lock2Off (gseq n)).1)))
          (((piMove P)^[n] s) (w (q + (lock2Off (gseq n)).2)))).Reachable
          (w (q + (lock2Off (gseq n)).1)) (w (q + (lock2Off (gseq n)).2))) ∧
      (pairGraph M.graph h ((piMove P)^[n] s)
          (((piMove P)^[n] s) (w (q + (lock2Off (gseq n)).1)))
          (((piMove P)^[n] s) (w (q + (lock2Off (gseq n)).2)))).Reachable
          (w (q + (lock2Off (gseq n)).1)) (w (q + (lock2Off (gseq n)).2)) := by
  obtain ⟨j, hd, -, -, L2⟩ := lock_join_pos H hc hall hr hq hT n hn
  exact ⟨j, hd, L2, L2.1 hd.2.2⟩

/-- `J` at every position: the join `y ~ z` in the graph of the two colours named by the state
table (`wL (gseq n) 4`, `wL (gseq n) 0` in the frame of the state). -/
theorem J_join_pos (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ∃ j, DoublyLocked P ((piMove P)^[n] s) j ∧
      (JoinYZ M.graph h w q ((piMove P)^[n] s) ↔
        (pairGraph M.graph h ((piMove P)^[n] s) (frm P ((piMove P)^[n] s) j (wL (gseq n) 4))
          (frm P ((piMove P)^[n] s) j (wL (gseq n) 0))).Reachable (w (q + 4)) (w q)) := by
  obtain ⟨j, hd⟩ := hall n
  obtain ⟨-, ow, -⟩ := orbit_colour H hc hall hr hq hT n hn hd.1 0
  simp only [add_zero, Function.iterate_zero, id] at ow
  refine ⟨j, hd, ?_⟩
  unfold JoinYZ
  have o0 := ow 0
  rw [add_zero] at o0
  rw [ow 4, o0]

/-! ### 3. Step 8 is far -/

/-- **(3) Step 8 is far** (`NightA34.md` §2.1). At position `8` (`R3k0`, `j = q`), the
swapped component `K_{α,A}(x (q+2))` contains none of `p, m, y, z`, so the step leaves their
colours unchanged. `p ∉ K` is `Rot3Def`, the Kempe separation of `p` from `x (q+2)` by the
`Lock2` chain (`rot3Def_of_lock2`, planar: `alternating_walks_intersect`); `y` is `A` and
adjacent to `p`; `m` and `z` carry `μ` and `B`. -/
theorem step8_far (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (k : ℕ) (hk : k % 10 = 8) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧ q = j ∧
      (∀ v, (v = P.x q ∨ v = m ∨ v = w (q + 4) ∨ v = w q) →
        ¬ (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
            (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v ∧
        ((piMove P)^[k + 1] s) v = ((piMove P)^[k] s) v) := by
  have hk0 : 0 < k := by omega
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have g : gseq k = (.R3, 0) := by rw [gseq_mod, hk]; decide
  obtain ⟨j, hd, hq', hT'⟩ := tk k
  rw [g] at hq' hT'
  dsimp only at hq' hT'
  rw [add_zero] at hq'
  subst hq'
  have hD := orbit_dd hc hall k q hd
  obtain ⟨op, oy⟩ := pair_own (t := .R3) (k := 0) H (add_zero q).symm (iter_proper hc k) hD hT'
    (by decide)
  simp only [pv_R3_0] at op oy
  obtain ⟨j', hd', -, tab⟩ := orbit_tab H hc hall hr hq hT k hk0
  have ej := rep_unique hd.1 hd'.1
  subst j'
  rw [g] at tab
  obtain ⟨hR, -⟩ := tab_R3 hd' (add_zero q).symm tab
  have tm := tab.2.2
  obtain ⟨⟨⟨h02, h1, h3, h4, h13, h14, h34⟩, -⟩, e0, -, -, -, -⟩ := hR
  obtain ⟨hπ, -, hK, -⟩ := dd_ends (iter_proper hc k) hD
  set c := (piMove P)^[k] s with hcdef
  change c m = c (P.x (q + 1)) at tm
  have notK : ∀ v, (v = P.x q ∨ v = m ∨ v = w (q + 4) ∨ v = w q) →
      ¬ (pairGraph M.graph h c (c (P.x q)) (c (P.x (q + 3)))).Reachable (P.x (q + 2)) v := by
    rintro v (rfl | rfl | rfl | rfl) r
    · exact hK r
    · have := reach_col r (fun e => H.offm _ e.symm)
      rw [tm] at this
      rcases this with e | e
      · exact h1 e
      · exact h13 e
    · exact hK (r.trans (pgR (H.adj_w4 q).symm (H.offh _) (P.x_ne_h _) (Or.inr oy) (Or.inl rfl)))
    · have := reach_col r (fun e => H.off _ _ e.symm)
      rw [e0] at this
      rcases this with e | e
      · exact h4 e
      · exact h34 e.symm
  refine ⟨q, hd, rfl, fun v hv => ⟨notK v hv, ?_⟩⟩
  rw [Function.iterate_succ_apply', ← hcdef, hπ]
  exact swap_out (notK v hv)

/-! ### 4. The window lemma -/

private theorem window_letters : ∀ i : Fin 6,
    sig^[i.val] (wL (gseq (9 + i.val)) 4) = wL (gseq 9) 4 ∧
    sig^[i.val] (wL (gseq (9 + i.val)) 0) = wL (gseq 9) 0 := by
  decide

/-- **The `J` pair is fixed on the window** (`NightA34.md` §3). From position `9` (`R1k2`) to
position `4` of the next period (`R3k2`), the colours of `y` and `z` do not change, so `G_J` is
the two-colour graph of one fixed colour pair. -/
theorem window_pair (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 9) (i : ℕ) (hi : i ≤ 5) :
    ((piMove P)^[n + i] s) (w (q + 4)) = ((piMove P)^[n] s) (w (q + 4)) ∧
    ((piMove P)^[n + i] s) (w q) = ((piMove P)^[n] s) (w q) := by
  obtain ⟨j, hd⟩ := hall n
  have hn0 : 0 < n := by omega
  obtain ⟨-, ow, -⟩ := orbit_colour H hc hall hr hq hT n hn0 hd.1 i
  obtain ⟨-, ow0, -⟩ := orbit_colour H hc hall hr hq hT n hn0 hd.1 0
  simp only [add_zero, Function.iterate_zero, id] at ow0
  have g0 : gseq n = gseq 9 := by rw [gseq_mod, hn]
  have gi : gseq (n + i) = gseq (9 + i) := by rw [gseq_mod, gseq_mod (9 + i)]; congr 1; omega
  have L := window_letters ⟨i, by omega⟩
  dsimp only at L
  have z0 := ow 0
  have z00 := ow0 0
  rw [add_zero] at z0 z00
  rw [ow 4, z0, ow0 4, z00, gi, g0, L.1, L.2]
  exact ⟨rfl, rfl⟩

/-- Two ring vertices whose letters agree in the state table have the same colour. -/
lemma wcol_eq (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) {t t' : Fin 5}
    (e : wL (gseq n) t = wL (gseq n) t') :
    ((piMove P)^[n] s) (w (q + t)) = ((piMove P)^[n] s) (w (q + t')) := by
  obtain ⟨j, hd⟩ := hall n
  obtain ⟨-, ow, -⟩ := orbit_colour H hc hall hr hq hT n hn hd.1 0
  simp only [add_zero, Function.iterate_zero, id] at ow
  rw [ow t, ow t', e]

variable (M h w q) in
/-- `G_J`: the `{c y, c z}`-graph, `J = (y ~ z in G_J)`. -/
abbrev GJ (c : Fin n → Fin 4) : SimpleGraph (Fin n) :=
  pairGraph M.graph h c (c (w (q + 4))) (c (w q))

/-- **The window lemma, forced joins** (`NightA34.md` §3). In `G_J`: `y ~ w₂` at positions `9`
(`Lock2`) and `0` (`Lock1`); `z ~ w₂` at positions `2` (`Lock2`) and `3` (`Lock1`);
`y ~ w₂ ~ z` at position `4` (ring path `y w₃ w₂` and P1). -/
theorem window_forced (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ((n % 10 = 9 ∨ n % 10 = 0) →
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 4)) (w (q + 2))) ∧
    ((n % 10 = 2 ∨ n % 10 = 3) →
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) (w (q + 2))) ∧
    (n % 10 = 4 →
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 4)) (w (q + 2)) ∧
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 2)) (w q)) := by
  have z0 : q + 0 = q := add_zero q
  refine ⟨fun h90 => ?_, fun h23 => ?_, fun h4 => ?_⟩
  · rcases h90 with e | e
    · have g : gseq n = (.R1, 2) := by rw [gseq_mod, e]; decide
      obtain ⟨j, hd, -, L⟩ := lock2_join_pos H hc hall hr hq hT n hn
      rw [g, show lock2Off (.R1, 2) = (4, 2) by decide] at L
      have c2 := wcol_eq H hc hall hr hq hT n hn (t := 2) (t' := 0) (by rw [g]; decide)
      rw [z0] at c2
      dsimp only at L
      rw [c2] at L
      exact L
    · have g : gseq n = (.R3, 4) := by rw [gseq_mod, e]; decide
      obtain ⟨j, hd, -, L⟩ := lock1_join_pos H hc hall hr hq hT n hn
      rw [g, show lock1Off (.R3, 4) = (2, 4) by decide] at L
      have c2 := wcol_eq H hc hall hr hq hT n hn (t := 2) (t' := 0) (by rw [g]; decide)
      rw [z0] at c2
      dsimp only at L
      rw [c2, pairGraph_comm_gen] at L
      exact L.symm
  · rcases h23 with e | e
    · have g : gseq n = (.R3, 3) := by rw [gseq_mod, e]; decide
      obtain ⟨j, hd, -, L⟩ := lock2_join_pos H hc hall hr hq hT n hn
      rw [g, show lock2Off (.R3, 3) = (2, 0) by decide] at L
      have c2 := wcol_eq H hc hall hr hq hT n hn (t := 2) (t' := 4) (by rw [g]; decide)
      dsimp only at L
      rw [c2, z0] at L
      exact L.symm
    · have g : gseq n = (.R1, 0) := by rw [gseq_mod, e]; decide
      obtain ⟨j, hd, -, L⟩ := lock1_join_pos H hc hall hr hq hT n hn
      rw [g, show lock1Off (.R1, 0) = (0, 2) by decide] at L
      have c2 := wcol_eq H hc hall hr hq hT n hn (t := 2) (t' := 4) (by rw [g]; decide)
      dsimp only at L
      rw [c2, z0, pairGraph_comm_gen] at L
      exact L
  · have g : gseq n = (.R3, 2) := by rw [gseq_mod, h4]; decide
    have c3 := wcol_eq H hc hall hr hq hT n hn (t := 3) (t' := 0) (by rw [g]; decide)
    have c2 := wcol_eq H hc hall hr hq hT n hn (t := 2) (t' := 4) (by rw [g]; decide)
    rw [z0] at c3
    have e1 := H.ring (q + 3) (by rw [add_assoc]; exact (fin5_ne0 (a := 4) (by decide)).symm)
    have e2 := H.ring (q + 2) (by rw [add_assoc]; exact (fin5_ne0 (a := 3) (by decide)).symm)
    simp only [add_assoc, Fin.reduceAdd] at e1 e2
    have J4 := (period_J (m := m) H hc hall hr hq hT).1 n (by omega) (by omega)
    have yw : (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 4)) (w (q + 2)) :=
      (pgR e1.symm (H.offh _) (H.offh _) (Or.inl rfl) (Or.inr c3)).trans
        (pgR e2.symm (H.offh _) (H.offh _) (Or.inr c3) (Or.inl c2))
    exact ⟨yw, yw.symm.trans J4⟩

/-- **`J` on the window.** At positions `9, 0`: `J ⇔ w₂ ~ z` in `G_J`, given `y ~ w₂`; at
positions `2, 3`: `J ⇔ y ~ w₂`, given `z ~ w₂`. -/
theorem J_iff_window (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) :
    ((n % 10 = 9 ∨ n % 10 = 0) → (JoinYZ M.graph h w q ((piMove P)^[n] s) ↔
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 2)) (w q))) ∧
    ((n % 10 = 2 ∨ n % 10 = 3) → (JoinYZ M.graph h w q ((piMove P)^[n] s) ↔
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 4)) (w (q + 2)))) := by
  obtain ⟨F1, F2, -⟩ := window_forced H hc hall hr hq hT n hn
  refine ⟨fun e => ?_, fun e => ?_⟩
  · have yw := F1 e
    exact ⟨fun r => yw.symm.trans r, fun r => yw.trans r⟩
  · have zw := F2 e
    exact ⟨fun r => r.trans zw, fun r => r.trans zw.symm⟩

/-- **`k = 4` failure ⇔ `z` split off from `{y, w₂}`.** At the `R3k4` state `s (10 b + 10)`,
the `σ`-exit is not lockless iff, at position `9` (`s (10 b + 9)`) and equally at position `0`
(`s (10 b + 10)`), `y ~ w₂` but `w₂ ≁ z` in `G_J`. -/
theorem k4_failure_iff_z_split (htri : M.Triangulated) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (b : ℕ) :
    ∃ j, DoublyLocked P ((piMove P)^[10 * b + 10] s) j ∧ q = j + 4 ∧
      (¬ NoLock P (sigSwap P ((piMove P)^[10 * b + 10] s) j) ↔
        ((GJ M h w q ((piMove P)^[10 * b + 9] s)).Reachable (w (q + 4)) (w (q + 2)) ∧
          ¬ (GJ M h w q ((piMove P)^[10 * b + 9] s)).Reachable (w (q + 2)) (w q))) ∧
      (¬ NoLock P (sigSwap P ((piMove P)^[10 * b + 10] s) j) ↔
        ((GJ M h w q ((piMove P)^[10 * b + 10] s)).Reachable (w (q + 4)) (w (q + 2)) ∧
          ¬ (GJ M h w q ((piMove P)^[10 * b + 10] s)).Reachable (w (q + 2)) (w q))) := by
  obtain ⟨j, hd, hq', -, E⟩ := k4_exit_period (m := m) htri H hc hall hr hq hT b
  obtain ⟨-, P2, -⟩ := period_J (m := m) H hc hall hr hq hT
  have e9 := P2 (10 * b + 9) (Or.inr (by omega))
  have y9 := (window_forced H hc hall hr hq hT (10 * b + 9) (by omega)).1 (Or.inl (by omega))
  have y0 := (window_forced H hc hall hr hq hT (10 * b + 10) (by omega)).1 (Or.inr (by omega))
  have J9 := (J_iff_window H hc hall hr hq hT (10 * b + 9) (by omega)).1 (Or.inl (by omega))
  have J0 := (J_iff_window H hc hall hr hq hT (10 * b + 10) (by omega)).1 (Or.inr (by omega))
  refine ⟨j, hd, hq', ?_, ?_⟩
  · rw [E, J9]; exact ⟨fun x => ⟨y9, x⟩, fun x => x.2⟩
  · rw [E, ← e9, J0]; exact ⟨fun x => ⟨y0, x⟩, fun x => x.2⟩

/-- **`k = 3` failure ⇔ `y` split off from `{z, w₂}`.** At the `R3k3` state `s (10 b + 2)`, the
`σ`-exit is not lockless iff, at position `2` and equally at position `3`, `z ~ w₂` but
`y ≁ w₂` in `G_J`. -/
theorem k3_failure_iff_y_split (htri : M.Triangulated) (H : Hole6 P w m q)
    (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hr : RepeatAt P s j₀) (hq : q = j₀ + 4) (hT : TypeR3 P w s j₀) (b : ℕ) :
    ∃ j, DoublyLocked P ((piMove P)^[10 * b + 2] s) j ∧ q = j + 3 ∧
      (¬ NoLock P (sigSwap P ((piMove P)^[10 * b + 2] s) j) ↔
        ((GJ M h w q ((piMove P)^[10 * b + 2] s)).Reachable (w q) (w (q + 2)) ∧
          ¬ (GJ M h w q ((piMove P)^[10 * b + 2] s)).Reachable (w (q + 4)) (w (q + 2)))) ∧
      (¬ NoLock P (sigSwap P ((piMove P)^[10 * b + 2] s) j) ↔
        ((GJ M h w q ((piMove P)^[10 * b + 3] s)).Reachable (w q) (w (q + 2)) ∧
          ¬ (GJ M h w q ((piMove P)^[10 * b + 3] s)).Reachable (w (q + 4)) (w (q + 2)))) := by
  obtain ⟨j, hd, hq', E, e3⟩ := k3_exit_period (m := m) htri H hc hall hr hq hT b
  have hb : 0 < 10 * b + 2 := by omega
  have z2 := (window_forced H hc hall hr hq hT (10 * b + 2) hb).2.1 (Or.inl (by omega))
  have z3 := (window_forced H hc hall hr hq hT (10 * b + 3) (by omega)).2.1 (Or.inr (by omega))
  have J2 := (J_iff_window H hc hall hr hq hT (10 * b + 2) hb).2 (Or.inl (by omega))
  have J3 := (J_iff_window H hc hall hr hq hT (10 * b + 3) (by omega)).2 (Or.inr (by omega))
  refine ⟨j, hd, hq', ?_, ?_⟩
  · rw [E, J2]; exact ⟨fun x => ⟨z2, x⟩, fun x => x.2⟩
  · rw [E, ← e3, J3]; exact ⟨fun x => ⟨z3, x⟩, fun x => x.2⟩

/-! ### 5. The period rotates the colours (Studio Job AN) -/

lemma sig_iter_three : sig^[3] = id := by funext a; revert a; decide

lemma sig_iter_mod (i : ℕ) : sig^[i] = sig^[i % 3] := by
  conv_lhs => rw [← Nat.mod_add_div i 3, Function.iterate_add, Function.iterate_mul,
    sig_iter_three, Function.iterate_id, Function.comp_id]

/-- `σ` fixes `α` and is a 3-cycle on `μ, A, B` (`1 ↦ 3 ↦ 2 ↦ 1`, i.e. NightA34's
`2 → 1, 3 → 2, 1 → 3`). -/
theorem sig_three_cycle : sig 0 = 0 ∧ sig 1 = 3 ∧ sig 3 = 2 ∧ sig 2 = 1 ∧ sig^[3] = id ∧
    sig ≠ id :=
  ⟨rfl, rfl, rfl, rfl, sig_iter_three, fun e => absurd (congrFun e 1) (by decide)⟩

/-- **The period rotates the colours.** For `n > 0`, in the frame `frm (s n)` of the state
`s n`: every hole vertex `v` (`x (q+t)`, `w (q+t)`, `m`) has letter `ℓ` at `s n` and letter
`σ ℓ` at `s (n + 10)`; `σ` fixes the letter `0` (the repeat colour `α` of the frame) and cycles the three others
(`sig_three_cycle`). -/
theorem period_colour_rotation (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[n] s) j) :
    (∀ t, ((piMove P)^[n] s) (P.x (q + t)) = frm P ((piMove P)^[n] s) j (xL (gseq n) t) ∧
      ((piMove P)^[n + 10] s) (P.x (q + t)) =
        frm P ((piMove P)^[n] s) j (sig (xL (gseq n) t))) ∧
    (∀ t, ((piMove P)^[n] s) (w (q + t)) = frm P ((piMove P)^[n] s) j (wL (gseq n) t) ∧
      ((piMove P)^[n + 10] s) (w (q + t)) =
        frm P ((piMove P)^[n] s) j (sig (wL (gseq n) t))) ∧
    (((piMove P)^[n] s) m = frm P ((piMove P)^[n] s) j (mL (gseq n)) ∧
      ((piMove P)^[n + 10] s) m = frm P ((piMove P)^[n] s) j (sig (mL (gseq n)))) := by
  obtain ⟨x0, w0, m0⟩ := orbit_colour H hc hall hr hq hT n hn hj 0
  obtain ⟨x1, w1, m1⟩ := orbit_colour H hc hall hr hq hT n hn hj 10
  simp only [add_zero, Function.iterate_zero, id] at x0 w0 m0
  have e10 : sig^[10] = sig := by rw [sig_iter_mod]; rfl
  rw [gseq_period, e10] at x1 w1 m1
  exact ⟨fun t => ⟨x0 t, x1 t⟩, fun t => ⟨w0 t, w1 t⟩, m0, m1⟩

/-- **Closing an all-`DL` orbit.** If `π^[L] s = s`, then `10 ∣ L` (the type
period) and `σ^[L] = id` on letters, which forces `3 ∣ L`; so `30 ∣ L`. (Writing `L = 10 Q`,
`σ^Q = id`, i.e. `3 ∣ Q`; a canonical-state cycle of length `L ≢ 0 mod 30` lifts to a
colouring orbit of length `3 L`.) -/
theorem closing_perm (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) {L : ℕ} (hcyc : (piMove P)^[L] s = s) :
    sig^[L] = id ∧ 10 ∣ L ∧ 3 ∣ L ∧ 30 ∣ L := by
  obtain ⟨tk, -, -, hex, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  have u := hasTK_unique (tk L) (by rw [hcyc]; exact tk 0)
  have gL : gseq L = gseq 0 := Prod.ext u.1 u.2
  have d10 : 10 ∣ L := by
    by_contra hne
    have := hex 0 (L % 10) (by omega) (Nat.mod_lt _ (by decide))
    rw [zero_add, ← gseq_mod, gL] at this
    exact this rfl
  -- the frame at `s 10` and at `s (10 + L) = s 10`
  obtain ⟨j, hd⟩ := hall 10
  have fi := frm_iter hc hall 10 hd.1 L j (by
    rw [Function.iterate_add_apply, hcyc]; exact hd.1)
  have same : (piMove P)^[10 + L] s = (piMove P)^[10] s := by
    rw [Function.iterate_add_apply, hcyc]
  obtain ⟨-, h1, -, -, h13, h14, -⟩ := hd.1
  have e1 := fi 1
  rw [same, sig_iter_mod] at e1
  have d3 : L % 3 = 0 := by
    rcases (by omega : L % 3 = 0 ∨ L % 3 = 1 ∨ L % 3 = 2) with hm | hm | hm
    · exact hm
    · rw [hm] at e1; exact (h14 e1).elim
    · rw [hm] at e1; exact (h13 e1).elim
  have hid : sig^[L] = id := by rw [sig_iter_mod, d3]; rfl
  exact ⟨hid, d10, Nat.dvd_of_mod_eq_zero d3, Nat.Coprime.mul_dvd_of_dvd_of_dvd (by decide)
    (Nat.dvd_of_mod_eq_zero d3) d10⟩

end orbit

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.state_tab
#print axioms SimpleGraph.QuarterFloor.bookkeeping
#print axioms SimpleGraph.QuarterFloor.lock_join_pos
#print axioms SimpleGraph.QuarterFloor.lock1_join_pos
#print axioms SimpleGraph.QuarterFloor.lock2_join_pos
#print axioms SimpleGraph.QuarterFloor.J_join_pos
#print axioms SimpleGraph.QuarterFloor.step8_far
#print axioms SimpleGraph.QuarterFloor.window_pair
#print axioms SimpleGraph.QuarterFloor.window_forced
#print axioms SimpleGraph.QuarterFloor.k4_failure_iff_z_split
#print axioms SimpleGraph.QuarterFloor.k3_failure_iff_y_split
#print axioms SimpleGraph.QuarterFloor.period_colour_rotation
#print axioms SimpleGraph.QuarterFloor.closing_perm
