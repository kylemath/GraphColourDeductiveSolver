/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterWindow

/-!
# `z`'s split component avoids the hole; `x⁺` cannot heal (`NightA34.md` §7.1)

Setting of `QuarterWindow`: an all-`DL` `π`-orbit `s n = π^[n] s` from an `R3k4` state at a
`(5,5,5,5,6)` hole `Hole6 P w m q`, names `p = x q`, `x⁺ = x (q+1)`, `x₂ = x (q+2)`,
`x₃ = x (q+3)`, `x⁻ = x (q+4)`, `z = w q`, `w⁺ = w (q+1)`, `w₂ = w (q+2)`, `w₃ = w (q+3)`,
`y = w (q+4)`, `m`. A *hole vertex* (`HoleV`) is one of the eleven `x t`, `w t`, `m`.

At a position-`9` state (`R1k2`, `n % 10 = 9`) where `J` fails (a step-8 break), `Z_b` is the
`G_J`-component of `z` (`G_J` = the `{c y, c z}`-graph, `h` deleted).

## Main results (sorry-free, no new axioms)

1. `zsplit_no_hole_vertex` (§7.1(i)): every vertex of `Z_b` other than `z` is not a hole vertex.
   `Lock2` (`window_forced`) ties `w₂` to `y`; `x₂ ~ w₂` and `x⁻ ~ y` are `J`-coloured edges; the
   other hole vertices (`p, x⁺, x₃, w⁺, w₃, m`) have colours outside the `J` pair (state table).
2. `zsplit_hole_boundary` (§7.1(ii)): among the hole vertices `x⁺, x₂, x₃, x⁻, w₂`, exactly `x⁺`
   has a neighbour in `Z_b` (namely `z`). `x₃` has only hole neighbours (degree five), none in
   `Z_b`. The remaining hole vertices `p, w⁺, w₃` have colours outside the step-0 and step-1
   swap pairs (`gate_swaps_miss`), so they are in neither swap component; that `y, z, m` are in
   neither component is Studio Job O / `step8_far`-type far-ness and is not used here.
3. `xplus_cannot_heal` (§7.1(iii)): at position `2` (`R3k3`) the only neighbour of `x⁺` coloured
   in the `J` pair is `z` (`xplus_dead_end`: its only `G_J`-neighbour).
4. `far_vertex_needed` (§7.1(iv)): on the all-`DL` orbit (so `DL` at `R3k3` of the next period,
   which by the window lemma forces `z ~ w₂` in `G_J` there), some vertex `v` adjacent to
   `Z_b`, not in `Z_b`, `v ≠ h`, **not a hole vertex**, has a colour outside the `J` pair at
   position `9` and inside it at position `2`, and is recoloured by the step-0 or the step-1
   swap, i.e. lies in the swapped component `K₀` or `K₁` with its colour changed. Step 9
   (a `{c x₃, c x⁺}`-swap, disjoint from the `J` pair) cannot change `J`-membership.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

lemma not_pair {f : Fin 4 → Fin 4} (hf : Function.Injective f) {a b d : Fin 4} (hb : a ≠ b)
    (hd : a ≠ d) : ¬ (f a = f b ∨ f a = f d) := by
  rintro (e | e)
  · exact hb (hf e)
  · exact hd (hf e)

/-- A vertex reached from `s ≠ v` in a two-colour graph is not the deleted vertex. -/
lemma reach_ne {V C : Type*} {G : SimpleGraph V} {h s v : V} {c : V → C} {a b : C}
    (r : (pairGraph G h c a b).Reachable s v) (hsv : s ≠ v) : v ≠ h := by
  obtain ⟨p⟩ := r.symm
  cases p with
  | nil => exact (hsv rfl).elim
  | cons e _ => exact e.2.1.1

/-- A swap of a pair `{a, b}` disjoint from `{y, z}` keeps membership in `{y, z}`. -/
lemma swap_pair_keep {V : Type*} {c : V → Fin 4} {a b y z : Fin 4} {S : Set V} {v : V}
    (hay : a ≠ y) (haz : a ≠ z) (hby : b ≠ y) (hbz : b ≠ z) :
    (swap c a b S v = y ∨ swap c a b S v = z) ↔ (c v = y ∨ c v = z) := by
  classical
  by_cases hv : v ∈ S
  · rw [swap_in hv, Equiv.swap_apply_def]
    split_ifs with h1 h2
    · constructor <;> intro hh <;> omega
    · constructor <;> intro hh <;> omega
    · exact Iff.rfl
  · rw [swap_out hv]

section sphere
variable {N : ℕ} {M : SphericalMap N} {h : Fin N}
variable {P : Pent M.graph h} {w : Fin 5 → Fin N} {m : Fin N} {q : Fin 5}
  {c : Fin N → Fin 4} {j : Fin 5}

variable (P w m) in
/-- The eleven hole vertices: `x t`, `w t`, `m`. -/
def HoleV (v : Fin N) : Prop := (∃ t, v = P.x t) ∨ (∃ t, v = w t) ∨ v = m

/-- The frame of a repeat state is injective. -/
lemma frm_inj (hr : RepeatAt P c j) : Function.Injective (frm P c j) := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  intro a b
  revert a b
  refine forall_fin4 ?_ ?_ ?_ ?_ <;> refine forall_fin4 ?_ ?_ ?_ ?_ <;> intro e <;>
    first
    | rfl
    | (exfalso; change c _ = c _ at e; omega)

section orbit
variable {s : Fin N → Fin 4} {j₀ : Fin 5}

/-- Colours at an orbit state `s n`, `n > 0`, of known `(type, k) = g`, in its own frame. -/
lemma pos_cols (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : 0 < n) {g : GType × Fin 5} (hg : gseq n = g) :
    ∃ j, DoublyLocked P ((piMove P)^[n] s) j ∧ q = j + g.2 ∧
      Function.Injective (frm P ((piMove P)^[n] s) j) ∧
      (∀ t, ((piMove P)^[n] s) (P.x (q + t)) = frm P ((piMove P)^[n] s) j (xL g t)) ∧
      (∀ t, ((piMove P)^[n] s) (w (q + t)) = frm P ((piMove P)^[n] s) j (wL g t)) ∧
      ((piMove P)^[n] s) m = frm P ((piMove P)^[n] s) j (mL g) := by
  obtain ⟨j, hd, hq', -⟩ := orbit_tab H hc hall hr hq hT n hn
  obtain ⟨ox, ow, om⟩ := orbit_colour H hc hall hr hq hT n hn hd.1 0
  simp only [add_zero, Function.iterate_zero, id] at ox ow om
  rw [hg] at hq' ox ow om
  exact ⟨j, hd, hq', frm_inj hd.1, ox, ow, om⟩

/-- **Position-9 facts at a break.** At `R1k2` with `J` false: `y, w₂, x₂, x⁻` are on `y`'s
side of `G_J` (hence not in `Z_b`); every vertex of `Z_b` is `≠ h` and `J`-coloured; and
`p, x⁺, x₃, w⁺, w₃, m` are not `J`-coloured. -/
lemma pos9_setup (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 9)
    (hJ : ¬ JoinYZ M.graph h w q ((piMove P)^[n] s)) :
    (∀ u, (u = w (q + 4) ∨ u = w (q + 2) ∨ u = P.x (q + 2) ∨ u = P.x (q + 4)) →
      (GJ M h w q ((piMove P)^[n] s)).Reachable (w (q + 4)) u ∧
      ¬ (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) u) ∧
    (∀ v, (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v → v ≠ h ∧
      (((piMove P)^[n] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
        ((piMove P)^[n] s) v = ((piMove P)^[n] s) (w q))) ∧
    (∀ v, (v = P.x q ∨ v = P.x (q + 1) ∨ v = P.x (q + 3) ∨ v = w (q + 1) ∨ v = w (q + 3) ∨
        v = m) →
      ¬ (((piMove P)^[n] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
        ((piMove P)^[n] s) v = ((piMove P)^[n] s) (w q))) := by
  have hn0 : 0 < n := by omega
  obtain ⟨j, -, -, inj, ox, ow, om⟩ := pos_cols H hc hall hr hq hT n hn0
    (g := (.R1, 2)) (by rw [gseq_mod, hn]; decide)
  have yw2 := (window_forced H hc hall hr hq hT n hn0).1 (Or.inl hn)
  have cz := ow 0
  have cp := ox 0
  rw [add_zero] at cz cp
  clear hall hc hr hT
  generalize (piMove P)^[n] s = c at *
  have yx2 : (GJ M h w q c).Reachable (w (q + 4)) (P.x (q + 2)) :=
    yw2.trans (pgR (H.adj_w (q + 2)).symm (H.offh _) (P.x_ne_h _)
      (Or.inr (by rw [ow 2, cz]; exact congrArg _ (by decide)))
      (Or.inl (by rw [ox 2, ow 4]; exact congrArg _ (by decide))))
  have yx4 : (GJ M h w q c).Reachable (w (q + 4)) (P.x (q + 4)) :=
    pgR (H.adj_w (q + 4)).symm (H.offh _) (P.x_ne_h _) (Or.inl rfl)
      (Or.inr (by rw [ox 4, cz]; exact congrArg _ (by decide)))
  refine ⟨fun u hu => ?_, fun v r => ?_, fun v hv => ?_⟩
  · have yu : (GJ M h w q c).Reachable (w (q + 4)) u := by
      rcases hu with rfl | rfl | rfl | rfl
      · rfl
      · exact yw2
      · exact yx2
      · exact yx4
    exact ⟨yu, fun r => hJ (yu.trans r.symm)⟩
  · by_cases e : w q = v
    · subst e; exact ⟨H.offh q, Or.inr rfl⟩
    · exact ⟨reach_ne r e, reach_col r e⟩
  · rw [ow 4, cz]
    rcases hv with rfl | rfl | rfl | rfl | rfl | rfl
    · rw [cp]; exact not_pair inj (by decide) (by decide)
    · rw [ox 1]; exact not_pair inj (by decide) (by decide)
    · rw [ox 3]; exact not_pair inj (by decide) (by decide)
    · rw [ow 1]; exact not_pair inj (by decide) (by decide)
    · rw [ow 3]; exact not_pair inj (by decide) (by decide)
    · rw [om]; exact not_pair inj (by decide) (by decide)

/-- **(1) `Z_b` contains no hole vertex other than `z`** (`NightA34.md` §7.1(i)). At position
`9` (`R1k2`) with `J` false, every vertex `v ≠ z` of the `G_J`-component of `z` is none of the
link vertices `x t`, the ring vertices `w t`, or `m`. -/
theorem zsplit_no_hole_vertex (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 9)
    (hJ : ¬ JoinYZ M.graph h w q ((piMove P)^[n] s)) {v : Fin N}
    (hv : (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v) (hvz : v ≠ w q) :
    ¬ HoleV P w m v := by
  obtain ⟨Y, Z, C⟩ := pos9_setup H hc hall hr hq hT n hn hJ
  have nc : ∀ u, (u = P.x q ∨ u = P.x (q + 1) ∨ u = P.x (q + 3) ∨ u = w (q + 1) ∨
      u = w (q + 3) ∨ u = m) → ¬ (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) u :=
    fun u hu r => C u hu (Z u r).2
  rintro (⟨t, rfl⟩ | ⟨t, rfl⟩ | rfl)
  · obtain ⟨t, rfl⟩ : ∃ t', t = q + t' := ⟨t - q, by abel⟩
    rcases fin5_five t with rfl | rfl | rfl | rfl | rfl
    · rw [add_zero] at hv; exact nc _ (Or.inl rfl) hv
    · exact nc _ (Or.inr (Or.inl rfl)) hv
    · exact (Y _ (Or.inr (Or.inr (Or.inl rfl)))).2 hv
    · exact nc _ (Or.inr (Or.inr (Or.inl rfl))) hv
    · exact (Y _ (Or.inr (Or.inr (Or.inr rfl)))).2 hv
  · obtain ⟨t, rfl⟩ : ∃ t', t = q + t' := ⟨t - q, by abel⟩
    rcases fin5_five t with rfl | rfl | rfl | rfl | rfl
    · rw [add_zero] at hvz; exact hvz rfl
    · exact nc _ (Or.inr (Or.inr (Or.inr (Or.inl rfl)))) hv
    · exact (Y _ (Or.inr (Or.inl rfl))).2 hv
    · exact nc _ (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))) hv
    · exact (Y _ (Or.inl rfl)).2 hv
  · exact nc _ (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr rfl))))) hv

/-- **(2) The hole boundary of `Z_b` is `{x⁺}`** (`NightA34.md` §7.1(ii)). At position `9` with
`J` false, among the hole vertices `x⁺, x₂, x₃, x⁻, w₂` (those of `K₀ ∪ K₁` by the colour table
and far-ness), a vertex has a neighbour in `Z_b` iff it is `x⁺ = x (q+1)` (adjacent to `z`). -/
theorem zsplit_hole_boundary (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 9)
    (hJ : ¬ JoinYZ M.graph h w q ((piMove P)^[n] s)) (u : Fin N)
    (hu : u = P.x (q + 1) ∨ u = P.x (q + 2) ∨ u = P.x (q + 3) ∨ u = P.x (q + 4) ∨
      u = w (q + 2)) :
    (∃ v, (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v ∧ M.graph.Adj u v) ↔
      u = P.x (q + 1) := by
  obtain ⟨Y, Z, C⟩ := pos9_setup H hc hall hr hq hT n hn hJ
  have ystep : ∀ u, (u = w (q + 4) ∨ u = w (q + 2) ∨ u = P.x (q + 2) ∨ u = P.x (q + 4)) →
      ∀ v, (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v → ¬ M.graph.Adj u v := by
    intro u hu v r e
    obtain ⟨yu, nu⟩ := Y u hu
    have au : u ≠ h ∧ (((piMove P)^[n] s) u = ((piMove P)^[n] s) (w (q + 4)) ∨
        ((piMove P)^[n] s) u = ((piMove P)^[n] s) (w q)) := by
      by_cases hy : w (q + 4) = u
      · subst hy; exact ⟨H.offh _, Or.inl rfl⟩
      · exact ⟨reach_ne yu hy, reach_col yu hy⟩
    exact nu (r.trans (Adj.reachable ⟨e.symm, Z v r, au⟩))
  constructor
  · rintro ⟨v, r, e⟩
    rcases hu with rfl | rfl | rfl | rfl | rfl
    · rfl
    · exact (ystep _ (Or.inr (Or.inr (Or.inl rfl))) v r e).elim
    · exfalso
      rcases H.link_nbr (q + 3) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
      · exact (Z _ r).1 rfl
      · simp only [add_assoc, Fin.reduceAdd] at r
        exact (Y _ (Or.inr (Or.inr (Or.inl rfl)))).2 r
      · simp only [add_assoc, Fin.reduceAdd] at r
        exact (Y _ (Or.inr (Or.inr (Or.inr rfl)))).2 r
      · simp only [add_assoc, Fin.reduceAdd] at r
        exact (Y _ (Or.inr (Or.inl rfl))).2 r
      · exact C _ (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl rfl))))) (Z _ r).2
      · exact (fin5_ne0 (j := q) (a := 3) (by decide)) tq.symm
    · exact (ystep _ (Or.inr (Or.inr (Or.inr rfl))) v r e).elim
    · exact (ystep _ (Or.inr (Or.inl rfl)) v r e).elim
  · rintro rfl
    exact ⟨w q, Reachable.refl _, H.adj_w' q⟩

/-- **(3) `x⁺` cannot heal** (`NightA34.md` §7.1(iii)). At position `2` (`R3k3`), the only
neighbour of `x⁺ = x (q+1)` (other than `h`) coloured in the `J` pair is `z`. -/
theorem xplus_cannot_heal (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 2) {u : Fin N}
    (e : M.graph.Adj (P.x (q + 1)) u) (hu : u ≠ h)
    (hcu : ((piMove P)^[n] s) u = ((piMove P)^[n] s) (w (q + 4)) ∨
      ((piMove P)^[n] s) u = ((piMove P)^[n] s) (w q)) : u = w q := by
  obtain ⟨j, -, -, inj, ox, ow, -⟩ := pos_cols H hc hall hr hq hT n (by omega)
    (g := (.R3, 3)) (by rw [gseq_mod, hn]; decide)
  have cz := ow 0
  have cp := ox 0
  rw [add_zero] at cz cp
  rw [ow 4, cz] at hcu
  rcases H.link_nbr (q + 1) e with rfl | rfl | rfl | rfl | rfl | ⟨tq, rfl⟩
  · exact (hu rfl).elim
  · simp only [add_assoc, Fin.reduceAdd, add_zero] at hcu
    rw [cp] at hcu; exact (not_pair inj (by decide) (by decide) hcu).elim
  · simp only [add_assoc, Fin.reduceAdd] at hcu
    rw [ox 2] at hcu; exact (not_pair inj (by decide) (by decide) hcu).elim
  · simp only [add_assoc, Fin.reduceAdd, add_zero]
  · rw [ow 1] at hcu; exact (not_pair inj (by decide) (by decide) hcu).elim
  · exact ((fin5_ne0 (j := q) (a := 1) (by decide)) tq.symm).elim

/-- `x⁺` is a dead end of `G_J` at position `2`: its only `G_J`-neighbour is `z`. -/
theorem xplus_dead_end (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 2) (u : Fin N)
    (e : (GJ M h w q ((piMove P)^[n] s)).Adj (P.x (q + 1)) u) : u = w q :=
  xplus_cannot_heal H hc hall hr hq hT n hn e.1 e.2.2.1 e.2.2.2

/-- The step-0 (`R3k4`, position `0`) and step-1 (`R1k1`, position `1`) swap pairs
`{c (x j), c (x (j+3))}` miss the colours of `p, w⁺, w₃`, so these hole vertices lie in neither
swapped component `K₀, K₁`. -/
theorem gate_swaps_miss (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 9) :
    (∃ j, DoublyLocked P ((piMove P)^[n + 1] s) j ∧
      ∀ v, (v = P.x q ∨ v = w (q + 1) ∨ v = w (q + 3)) →
        ((piMove P)^[n + 1] s) v ≠ ((piMove P)^[n + 1] s) (P.x j) ∧
        ((piMove P)^[n + 1] s) v ≠ ((piMove P)^[n + 1] s) (P.x (j + 3))) ∧
    (∃ j, DoublyLocked P ((piMove P)^[n + 2] s) j ∧
      ∀ v, (v = P.x q ∨ v = w (q + 1) ∨ v = w (q + 3)) →
        ((piMove P)^[n + 2] s) v ≠ ((piMove P)^[n + 2] s) (P.x j) ∧
        ((piMove P)^[n + 2] s) v ≠ ((piMove P)^[n + 2] s) (P.x (j + 3))) := by
  constructor
  · obtain ⟨j, hd, hq', inj, ox, ow, -⟩ := pos_cols H hc hall hr hq hT (n + 1) (by omega)
      (g := (.R3, 4)) (by rw [gseq_mod, show (n + 1) % 10 = 0 by omega]; decide)
    dsimp only at hq'
    have e1 : P.x j = P.x (q + 1) := by rw [hq']; simp only [add_assoc, Fin.reduceAdd, add_zero]
    have e4 : P.x (j + 3) = P.x (q + 4) := by rw [hq']; simp only [add_assoc, Fin.reduceAdd]
    have cp := ox 0
    rw [add_zero] at cp
    refine ⟨j, hd, fun v hv => ?_⟩
    rw [e1, e4, ox 1, ox 4]
    rcases hv with rfl | rfl | rfl
    · rw [cp]; exact ⟨inj.ne (by decide), inj.ne (by decide)⟩
    · rw [ow 1]; exact ⟨inj.ne (by decide), inj.ne (by decide)⟩
    · rw [ow 3]; exact ⟨inj.ne (by decide), inj.ne (by decide)⟩
  · obtain ⟨j, hd, hq', inj, ox, ow, -⟩ := pos_cols H hc hall hr hq hT (n + 2) (by omega)
      (g := (.R1, 1)) (by rw [gseq_mod, show (n + 2) % 10 = 1 by omega]; decide)
    dsimp only at hq'
    have e1 : P.x j = P.x (q + 4) := by rw [hq']; simp only [add_assoc, Fin.reduceAdd, add_zero]
    have e4 : P.x (j + 3) = P.x (q + 2) := by rw [hq']; simp only [add_assoc, Fin.reduceAdd]
    have cp := ox 0
    rw [add_zero] at cp
    refine ⟨j, hd, fun v hv => ?_⟩
    rw [e1, e4, ox 4, ox 2]
    rcases hv with rfl | rfl | rfl
    · rw [cp]; exact ⟨inj.ne (by decide), inj.ne (by decide)⟩
    · rw [ow 1]; exact ⟨inj.ne (by decide), inj.ne (by decide)⟩
    · rw [ow 3]; exact ⟨inj.ne (by decide), inj.ne (by decide)⟩

/-- A vertex recoloured by an orbit step lies in that step's swapped component
`K = K_{c x j, c x (j+3)}(x (j+2))`. -/
lemma step_moves (hall : ∀ n, DLState P ((piMove P)^[n] s)) (k : ℕ) {v : Fin N}
    (hne : ((piMove P)^[k + 1] s) v ≠ ((piMove P)^[k] s) v) :
    ∃ j, DoublyLocked P ((piMove P)^[k] s) j ∧
      (pairGraph M.graph h ((piMove P)^[k] s) (((piMove P)^[k] s) (P.x j))
        (((piMove P)^[k] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v ∧
      ((piMove P)^[k + 1] s) v ≠ ((piMove P)^[k] s) v := by
  obtain ⟨j, hd⟩ := hall k
  refine ⟨j, hd, Classical.byContradiction fun hK => hne ?_, hne⟩
  rw [Function.iterate_succ_apply', piMove_rep hd.1, ite_eq_left hd.2.2]
  exact swap_out hK

/-- **(4) A far gate is needed** (`NightA34.md` §7.1(iv)). At a step-8 break (position `9`,
`J` false) on the all-`DL` orbit, there are `u ∈ Z_b` and a neighbour `v ∉ Z_b` of `u` such that
`v ≠ h` is **not a hole vertex**, `v` is outside the `J` pair at position `9` and inside it at
position `2` (`R3k3` of the next period), and `v` is recoloured by the step-0 swap (`v ∈ K₀`) or
the step-1 swap (`v ∈ K₁`). (`DL` at `R3k3` forces `z ~ w₂` in `G_J`; a `G_J`-path leaves
`Z_b ∪ {x⁺}` through such a `v`, since `x⁺` is a dead end; step 9 keeps `J`-membership.) -/
theorem far_vertex_needed (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
    (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
    (hT : TypeR3 P w s j₀) (n : ℕ) (hn : n % 10 = 9)
    (hJ : ¬ JoinYZ M.graph h w q ((piMove P)^[n] s)) :
    ∃ u v, (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) u ∧ M.graph.Adj u v ∧
      ¬ (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v ∧ v ≠ h ∧ ¬ HoleV P w m v ∧
      ¬ (((piMove P)^[n] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
          ((piMove P)^[n] s) v = ((piMove P)^[n] s) (w q)) ∧
      (((piMove P)^[n + 3] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
          ((piMove P)^[n + 3] s) v = ((piMove P)^[n] s) (w q)) ∧
      ((∃ j, DoublyLocked P ((piMove P)^[n + 1] s) j ∧
          (pairGraph M.graph h ((piMove P)^[n + 1] s) (((piMove P)^[n + 1] s) (P.x j))
            (((piMove P)^[n + 1] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v ∧
          ((piMove P)^[n + 2] s) v ≠ ((piMove P)^[n + 1] s) v) ∨
       (∃ j, DoublyLocked P ((piMove P)^[n + 2] s) j ∧
          (pairGraph M.graph h ((piMove P)^[n + 2] s) (((piMove P)^[n + 2] s) (P.x j))
            (((piMove P)^[n + 2] s) (P.x (j + 3)))).Reachable (P.x (j + 2)) v ∧
          ((piMove P)^[n + 3] s) v ≠ ((piMove P)^[n + 2] s) v)) := by
  have hn0 : 0 < n := by omega
  obtain ⟨Y, Z, C⟩ := pos9_setup H hc hall hr hq hT n hn hJ
  have hn3 : (n + 3) % 10 = 2 := by omega
  have zw2 := (window_forced H hc hall hr hq hT (n + 3) (by omega)).2.1 (Or.inl hn3)
  obtain ⟨py, pz⟩ := window_pair H hc hall hr hq hT n hn 3 (by norm_num)
  obtain ⟨j9, hd9, hq9, inj9, ox9, ow9, -⟩ := pos_cols H hc hall hr hq hT n hn0
    (g := (.R1, 2)) (by rw [gseq_mod, hn]; decide)
  obtain ⟨j2, -, -, inj2, ox2, ow2, om2⟩ := pos_cols H hc hall hr hq hT (n + 3) (by omega)
    (g := (.R3, 3)) (by rw [gseq_mod, hn3]; decide)
  dsimp only at hq9
  have cz2 := ow2 0
  have cp2 := ox2 0
  rw [add_zero] at cz2 cp2
  -- leave `Z_b ∪ {x⁺}` along a `G_J`-walk from `z` to `w₂` at position `2`
  let S : Set (Fin N) :=
    {v | (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v} ∪ {P.x (q + 1)}
  obtain ⟨d, -, dS, dnS⟩ := zw2.some.exists_boundary_dart S (Or.inl (Reachable.refl _)) (by
    rintro (r | e)
    · exact (Y _ (Or.inr (Or.inl rfl))).2 r
    · exact H.off _ _ e)
  have hadj := d.adj
  generalize d.fst = u at hadj dS
  generalize d.snd = v at hadj dnS
  obtain ⟨e, -, ⟨vh, vc⟩⟩ := hadj
  have vZ : ¬ (GJ M h w q ((piMove P)^[n] s)).Reachable (w q) v := fun r => dnS (Or.inl r)
  have vx : v ≠ P.x (q + 1) := fun ex => dnS (Or.inr ex)
  rcases dS with uZ | ux
  swap
  · rw [Set.mem_singleton_iff] at ux
    subst ux
    have := xplus_cannot_heal H hc hall hr hq hT (n + 3) hn3 e vh vc
    subst this
    exact (vZ (Reachable.refl _)).elim
  have v9 : ¬ (((piMove P)^[n] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
      ((piMove P)^[n] s) v = ((piMove P)^[n] s) (w q)) :=
    fun hv => vZ (uZ.trans (Adj.reachable ⟨e, Z u uZ, ⟨vh, hv⟩⟩))
  have v2 := vc
  rw [py, pz] at v2
  -- `v` is not a hole vertex
  have nh : ¬ HoleV P w m v := by
    rintro (⟨t, rfl⟩ | ⟨t, rfl⟩ | rfl)
    · obtain ⟨t, rfl⟩ : ∃ t', t = q + t' := ⟨t - q, by abel⟩
      rcases fin5_five t with rfl | rfl | rfl | rfl | rfl
      · rw [add_zero, cp2, ow2 4, cz2] at vc
        exact not_pair inj2 (by decide) (by decide) vc
      · exact vx rfl
      · exact v9 (Or.inl (by rw [ox9 2, ow9 4]; exact congrArg _ (by decide)))
      · have b := (zsplit_hole_boundary H hc hall hr hq hT n hn hJ (P.x (q + 3))
          (Or.inr (Or.inr (Or.inl rfl)))).1 ⟨u, uZ, e.symm⟩
        exact fin5_ne (j := q) (a := 3) (b := 1) (by decide) (P.inj b)
      · have cz9 := ow9 0
        rw [add_zero] at cz9
        exact v9 (Or.inr (by rw [ox9 4, cz9]; exact congrArg _ (by decide)))
    · obtain ⟨t, rfl⟩ : ∃ t', t = q + t' := ⟨t - q, by abel⟩
      rcases fin5_five t with rfl | rfl | rfl | rfl | rfl
      · rw [add_zero] at vZ; exact vZ (Reachable.refl _)
      · rw [ow2 1, ow2 4, cz2] at vc
        exact not_pair inj2 (by decide) (by decide) vc
      · have cz9 := ow9 0
        rw [add_zero] at cz9
        exact v9 (Or.inr (by rw [ow9 2, cz9]; exact congrArg _ (by decide)))
      · rw [ow2 3, ow2 4, cz2] at vc
        exact not_pair inj2 (by decide) (by decide) vc
      · exact v9 (Or.inl rfl)
    · rw [om2, ow2 4, cz2] at vc
      exact not_pair inj2 (by decide) (by decide) vc
  refine ⟨u, v, uZ, e, vZ, vh, nh, v9, v2, ?_⟩
  -- step 9 is a `{c x₃, c x⁺}`-swap: it keeps `J`-membership
  have ej : P.x j9 = P.x (q + 3) := by
    rw [hq9]; simp only [add_assoc, Fin.reduceAdd, add_zero]
  have ej3 : P.x (j9 + 3) = P.x (q + 1) := by rw [hq9]; simp only [add_assoc, Fin.reduceAdd]
  have cz9 := ow9 0
  rw [add_zero] at cz9
  have k9 : (((piMove P)^[n + 1] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
      ((piMove P)^[n + 1] s) v = ((piMove P)^[n] s) (w q)) ↔
      (((piMove P)^[n] s) v = ((piMove P)^[n] s) (w (q + 4)) ∨
        ((piMove P)^[n] s) v = ((piMove P)^[n] s) (w q)) := by
    rw [Function.iterate_succ_apply', piMove_rep hd9.1, ite_eq_left hd9.2.2]
    unfold rot3
    refine swap_pair_keep ?_ ?_ ?_ ?_
    · rw [ej, ox9 3, ow9 4]; exact inj9.ne (by decide)
    · rw [ej, ox9 3, cz9]; exact inj9.ne (by decide)
    · rw [ej3, ox9 1, ow9 4]; exact inj9.ne (by decide)
    · rw [ej3, ox9 1, cz9]; exact inj9.ne (by decide)
  have v10 := mt k9.1 v9
  by_cases h1 : ((piMove P)^[n + 2] s) v = ((piMove P)^[n + 1] s) v
  · right
    exact step_moves hall (n + 2) (fun h2 => v10 (by rw [← h1, ← h2]; exact v2))
  · left
    exact step_moves hall (n + 1) h1

end orbit

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.zsplit_no_hole_vertex
#print axioms SimpleGraph.QuarterFloor.zsplit_hole_boundary
#print axioms SimpleGraph.QuarterFloor.xplus_cannot_heal
#print axioms SimpleGraph.QuarterFloor.xplus_dead_end
#print axioms SimpleGraph.QuarterFloor.gate_swaps_miss
#print axioms SimpleGraph.QuarterFloor.far_vertex_needed
