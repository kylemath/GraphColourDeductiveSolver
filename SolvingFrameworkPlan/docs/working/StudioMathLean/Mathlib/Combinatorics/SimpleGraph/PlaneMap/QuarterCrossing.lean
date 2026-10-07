/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterTwoPeriod

/-!
# The crossing lemma for the two colourings (`NightA34Two.md` §3.3, `A₃₄′` on `L = 20`)

Setting of `QuarterTwoPeriod`: `s` an `R3k4` state at a `Hole6` with an all-`DL` orbit and
`π^[20] s = ρ ∘ s`; `d = Gmap s`. Write `s₉ = π^[9] s`, `d₉ = π^[9] d` and
`X₉ = {v | s₉ v ≠ d₉ v}` (`X9`). Names: `p = x q`, `x⁺ = x (q+1)`, `z = w q`, `w₂ = w (q+2)`,
`y = w (q+4)`, `m`.

## Generic transfer

`walk_transfer`: a walk of the `{a, b}`-graph of `c'` along which `c = c'` is a walk of the
`{a, b}`-graph of `c`. Contrapositive `walk_meets_diff`.

## Main results (sorry-free, no new axioms)

1. **`X_far`**: `X₉` contains no hole vertex (`ring_agree` at position `9`).
2. **`crossing_lemma`**: if `J` fails at `s₉` (`Break s`), every walk of the `J`-pair graph of
   `d₉` from `z` to `y` or to `w₂` meets `X₉` (`y ~ w₂` at `s₉` by `window_forced`).
   `crossing_exists`: if moreover `J` holds at `d₉`, some `v ∈ X₉` lies on a `G_J(d₉)` path from
   `z` to `y`. Only `ring_agree` and the definitions are used (`crossing_core`).
3. **`crossing_on_pocket`**: the pocket of `u` is the `{u p, u m}`-component of `m` in
   `T − h − p − x⁺` (`Pocket`); its curve is `Pocket ∪ {p, x⁺}`. Given the **separation**
   hypothesis `PocketSeparates s₉` (every walk of `T` from `z` to `y` or `w₂` meets the curve;
   this is the pocket lemma ⇒ plus the Jordan duality (D), not formal here), every `G_J(d₉)`
   walk from `z` to `{y, w₂}` meets `X₉` at a non-hole vertex of `s₉`'s pocket. The colour
   argument: curve vertices have `s₉`-colour in `{c p, c m}` (or are `x⁺`, whose colour at
   position `9` is the letter `A`, outside the `J` pair `{μ, B}`: `pos9_xplus`), walk vertices
   have `d₉`-colour in the `J` pair, and `{c p, c m}` is disjoint from `{c y, c z}` since `p`
   and `m` are adjacent to `y` and `z`.
4. **`two_pocket_conj`** / **`no_double_break_of_crossing_obstruction`**: with the pocket lemma
   at `s₉` and `d₉` as named hypotheses (`PocketLemmaAt`), `Break s ∧ Break d` gives
   `TwoPocketConj s₉ d₉`: both pocket paths, both separations, and the two crossing statements
   with roles swapped by `G` (`G d = s`). Hence `¬ TwoPocketConj s₉ d₉ ⇒ A₃₄′(L = 20)` (via
   `A34_two_iff`). Note: under a double break `J` fails at both `s₉` and `d₉`, so the two
   crossing conjuncts are vacuous; the content left to refute is the pair of pockets.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Generic transfer of two-colour walks -/

section generic
variable {V C : Type*} {G : SimpleGraph V} {h : V} {c c' : V → C} {a b : C}

/-- A walk of the `{a, b}`-graph of `c'` along which `c` and `c'` agree is a walk of the
`{a, b}`-graph of `c`. -/
lemma walk_transfer {u v : V} (W : (pairGraph G h c' a b).Walk u v)
    (hag : ∀ x ∈ W.support, c x = c' x) : (pairGraph G h c a b).Reachable u v := by
  induction W with
  | nil => exact Reachable.refl _
  | @cons u x v e W ih =>
    have hu := hag u (by simp)
    have hx := hag x (by simp)
    refine (Adj.reachable (G := pairGraph G h c a b) ⟨e.1, ?_, ?_⟩).trans
      (ih fun y hy => hag y (by simp [hy]))
    · exact ⟨e.2.1.1, by rw [hu]; exact e.2.1.2⟩
    · exact ⟨e.2.2.1, by rw [hx]; exact e.2.2.2⟩

/-- **Crossing, generic form.** If `u ≁ v` in the `{a, b}`-graph of `c`, every walk from `u` to
`v` in the `{a, b}`-graph of `c'` passes through a vertex where `c ≠ c'`. -/
lemma walk_meets_diff {u v : V} (W : (pairGraph G h c' a b).Walk u v)
    (hn : ¬ (pairGraph G h c a b).Reachable u v) : ∃ x ∈ W.support, c x ≠ c' x := by
  by_contra hne
  push Not at hne
  exact hn (walk_transfer W hne)

/-- Every vertex of a two-colour walk from `u` other than `u` carries one of the two colours. -/
lemma walk_support_col {u v : V} (W : (pairGraph G h c' a b).Walk u v) :
    ∀ x ∈ W.support, x = u ∨ c' x = a ∨ c' x = b := by
  induction W with
  | nil => intro x hx; simp at hx; exact Or.inl hx
  | @cons u y v e W ih =>
    intro x hx
    rw [Walk.support_cons, List.mem_cons] at hx
    rcases hx with rfl | hx
    · exact Or.inl rfl
    · rcases ih x hx with rfl | hc
      · exact Or.inr e.2.2.2
      · exact Or.inr hc

end generic

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}

/-! ### The pocket -/

variable (P m q) in
/-- The `{c p, c m}`-graph of `c` with `p = x q` and `x⁺ = x (q+1)` deleted. -/
def pocketGraph (c : Fin n → Fin 4) : SimpleGraph (Fin n) where
  Adj u v := (pairGraph M.graph h c (c (P.x q)) (c m)).Adj u v ∧
    u ≠ P.x q ∧ u ≠ P.x (q + 1) ∧ v ≠ P.x q ∧ v ≠ P.x (q + 1)
  symm := ⟨fun _ _ e => ⟨e.1.symm, e.2.2.2.1, e.2.2.2.2, e.2.1, e.2.2.1⟩⟩
  loopless := ⟨fun _ e => e.1.ne rfl⟩

variable (P m q) in
/-- The pocket of `c`: the component of `m` in `pocketGraph c`. -/
def Pocket (c : Fin n → Fin 4) : Set (Fin n) := {v | (pocketGraph P m q c).Reachable m v}

variable (P w m q) in
/-- A pocket path: `m ⇝ w⁺` in `pocketGraph c` (the pocket lemma's characterisation of a
break at `R1k2`). -/
def PocketPath (c : Fin n → Fin 4) : Prop := (pocketGraph P m q c).Reachable m (w (q + 1))

variable (P m q) in
/-- The pocket curve: the pocket together with `p` and `x⁺`. -/
def OnCurve (c : Fin n → Fin 4) (v : Fin n) : Prop :=
  v ∈ Pocket P m q c ∨ v = P.x q ∨ v = P.x (q + 1)

variable (P w m q) in
/-- **Separation** (the planar content: pocket lemma ⇒ and Jordan duality (D)): every walk of
the triangulation from `z` to `y` or to `w₂` meets the pocket curve of `c`. -/
def PocketSeparates (c : Fin n → Fin 4) : Prop :=
  ∀ t, (t = w (q + 4) ∨ t = w (q + 2)) → ∀ W : M.graph.Walk (w q) t,
    ∃ v ∈ W.support, OnCurve P m q c v

/-- Pocket vertices carry `c p` or `c m`. -/
lemma pocket_col {c : Fin n → Fin 4} {v : Fin n} (hv : v ∈ Pocket P m q c) :
    c v = c (P.x q) ∨ c v = c m := by
  by_cases e : m = v
  · subst e; exact Or.inr rfl
  · have le : pocketGraph P m q c ≤ pairGraph M.graph h c (c (P.x q)) (c m) := fun _ _ x => x.1
    exact reach_col (Reachable.mono le hv) e

lemma hole_w (t : Fin 5) : HoleVT P w m q (w (q + t)) := Or.inr (Or.inl ⟨t, rfl⟩)

lemma hole_z : HoleVT P w m q (w q) := Or.inr (Or.inl ⟨0, by rw [add_zero]⟩)

/-! ### Core lemmas for two colourings agreeing on the hole -/

/-- **Crossing lemma, core.** `c` and `c'` agree on the hole, `J` fails at `c` and `y ~ w₂` in
`G_J(c)`. Then every `G_J(c')` walk from `z` to `y` or `w₂` meets `{v | c v ≠ c' v}`. -/
theorem crossing_core {c c' : Fin n → Fin 4} (hag : ∀ v, HoleVT P w m q v → c' v = c v)
    (hB : ¬ JoinYZ M.graph h w q c) (hyw : (GJ M h w q c).Reachable (w (q + 4)) (w (q + 2)))
    {t : Fin n} (ht : t = w (q + 4) ∨ t = w (q + 2)) (W : (GJ M h w q c').Walk (w q) t) :
    ∃ v ∈ W.support, c v ≠ c' v := by
  have ry := hag _ (hole_w (P := P) (m := m) 4)
  have rz := hag _ (hole_z (P := P) (m := m) (q := q) (w := w))
  refine walk_meets_diff W ?_
  rw [ry, rz]
  intro r
  rcases ht with rfl | rfl
  · exact hB r.symm
  · exact hB (hyw.trans r.symm)

/-- **Crossing on the pocket, core.** Under the separation hypothesis for `c`, every
`G_J(c')` walk from `z` to `y` or `w₂` meets `{v | c v ≠ c' v}` at a non-hole vertex of the
pocket of `c`. -/
theorem crossing_on_pocket_core (H : Hole6 P w m q) {c c' : Fin n → Fin 4}
    (hc : ProperOff M.graph h c) (hxy : c (P.x (q + 1)) ≠ c (w (q + 4)))
    (hxz : c (P.x (q + 1)) ≠ c (w q)) (hag : ∀ v, HoleVT P w m q v → c' v = c v)
    (hsep : PocketSeparates P w m q c) {t : Fin n} (ht : t = w (q + 4) ∨ t = w (q + 2))
    (W : (GJ M h w q c').Walk (w q) t) :
    ∃ v ∈ W.support, c v ≠ c' v ∧ v ∈ Pocket P m q c ∧ ¬ HoleVT P w m q v := by
  obtain ⟨v, hvW, hvC⟩ := hsep t ht (W.mapLe (show GJ M h w q c' ≤ M.graph from fun _ _ e => e.1))
  rw [Walk.support_mapLe_eq_support] at hvW
  have ry := hag _ (hole_w (P := P) (m := m) 4)
  have rz := hag _ (hole_z (P := P) (m := m) (q := q) (w := w))
  have hcol : c' v = c (w (q + 4)) ∨ c' v = c (w q) := by
    rcases walk_support_col W v hvW with rfl | e | e
    · exact Or.inr rz
    · exact Or.inl (e.trans ry)
    · exact Or.inr (e.trans rz)
  have py : M.graph.Adj (P.x q) (w (q + 4)) :=
    (H.nbrq _).2 (Or.inr (Or.inr (Or.inr (Or.inl rfl))))
  have pz : M.graph.Adj (P.x q) (w q) :=
    (H.nbrq _).2 (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr rfl)))))
  have cpy := hc py (P.x_ne_h q) (H.offh _)
  have cpz := hc pz (P.x_ne_h q) (H.offh _)
  have cmy := hc H.ringy (H.offh _) H.offmh
  have cmz := hc H.ringz H.offmh (H.offh _)
  have hX : c v ≠ c' v := by
    intro e
    rw [← e] at hcol
    rcases hvC with hP | rfl | rfl
    · rcases pocket_col hP with e1 | e1 <;> rcases hcol with e2 | e2
      · exact cpy (e1.symm.trans e2)
      · exact cpz (e1.symm.trans e2)
      · exact cmy (e2.symm.trans e1)
      · exact cmz (e1.symm.trans e2)
    · rcases hcol with e2 | e2
      · exact cpy e2
      · exact cpz e2
    · rcases hcol with e2 | e2
      · exact hxy e2
      · exact hxz e2
  have hnh : ¬ HoleVT P w m q v := fun hv => hX (hag v hv).symm
  refine ⟨v, hvW, hX, ?_, hnh⟩
  rcases hvC with hP | rfl | rfl
  · exact hP
  · exact (hnh (Or.inl ⟨0, by rw [add_zero]⟩)).elim
  · exact (hnh (Or.inl ⟨1, rfl⟩)).elim

/-! ### Position `9` in the setting -/

private lemma frm_inj' {c : Fin n → Fin 4} {j : Fin 5} (hr : RepeatAt P c j) :
    Function.Injective (frm P c j) := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  intro a b
  revert a b
  refine forall_fin4 ?_ ?_ ?_ ?_ <;> refine forall_fin4 ?_ ?_ ?_ ?_ <;> intro e <;>
    first
    | rfl
    | (exfalso; change c _ = c _ at e; omega)

section setting
variable {s : Fin n → Fin 4} {j₀ : Fin 5} {ρ : Equiv.Perm (Fin 4)}

variable (P ρ) in
/-- `X₉ = {v | s₉ v ≠ d₉ v}`, `d = Gmap s`. -/
def X9 (s : Fin n → Fin 4) : Set (Fin n) :=
  {v | (piMove P)^[9] s v ≠ (piMove P)^[9] (Gmap P ρ s) v}

variable (htri : M.Triangulated) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
  (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
  (hT : TypeR3 P w s j₀) (hρ : (piMove P)^[20] s = recol ρ s)

include H hc hall hr hq hT in
/-- At position `9` (`R1k2`) `x⁺` has letter `A`, `y` letter `B`, `z` letter `μ`: so `x⁺` is not
`J`-coloured. -/
theorem pos9_xplus :
    (piMove P)^[9] s (P.x (q + 1)) ≠ (piMove P)^[9] s (w (q + 4)) ∧
    (piMove P)^[9] s (P.x (q + 1)) ≠ (piMove P)^[9] s (w q) := by
  obtain ⟨j, hd⟩ := hall 9
  obtain ⟨ox, ow, -⟩ := orbit_colour H hc hall hr hq hT 9 (by norm_num) hd.1 0
  simp only [add_zero, Function.iterate_zero, id] at ox ow
  have g : gseq 9 = (.R1, 2) := by decide
  rw [g] at ox ow
  have fi := frm_inj' hd.1
  have z0 := ow 0
  rw [add_zero] at z0
  refine ⟨fun e => ?_, fun e => ?_⟩
  · rw [ox 1, ow 4] at e
    exact absurd (fi e) (by decide)
  · rw [ox 1, z0] at e
    exact absurd (fi e) (by decide)

include H hc hall hr hq hT hρ in
/-- **(1) `X₉` avoids the hole.** -/
theorem X_far {v : Fin n} (hv : HoleVT P w m q v) : v ∉ X9 P ρ s :=
  fun hx => hx (ring_agree H hc hall hr hq hT hρ 9 hv).2.symm

include H hc hall hr hq hT hρ in
/-- **(2) Crossing lemma.** If `J` fails at `s₉`, every walk of the `J`-pair graph of `d₉` from
`z` to `y` or to `w₂` passes through `X₉`. -/
theorem crossing_lemma (hB : Break P w q s) {t : Fin n} (ht : t = w (q + 4) ∨ t = w (q + 2))
    (W : (GJ M h w q ((piMove P)^[9] (Gmap P ρ s))).Walk (w q) t) :
    ∃ v ∈ W.support, v ∈ X9 P ρ s :=
  crossing_core (fun v hv => (ring_agree H hc hall hr hq hT hρ 9 hv).2) hB
    ((window_forced H hc hall hr hq hT 9 (by norm_num)).1 (Or.inl (by decide))) ht W

include H hc hall hr hq hT hρ in
/-- If only the `s`-run breaks, some `v ∈ X₉` lies on a `G_J(d₉)` path from `z` to `y`. -/
theorem crossing_exists (hB : Break P w q s) (hnd : ¬ Break P w q (Gmap P ρ s)) :
    ∃ v ∈ X9 P ρ s, (GJ M h w q ((piMove P)^[9] (Gmap P ρ s))).Reachable (w q) v ∧
      (GJ M h w q ((piMove P)^[9] (Gmap P ρ s))).Reachable v (w (q + 4)) := by
  classical
  have J : JoinYZ M.graph h w q ((piMove P)^[9] (Gmap P ρ s)) := not_not.1 hnd
  obtain ⟨W⟩ := (show (GJ M h w q ((piMove P)^[9] (Gmap P ρ s))).Reachable (w (q + 4)) (w q)
    from J).symm
  obtain ⟨v, hv, hX⟩ := crossing_lemma H hc hall hr hq hT hρ hB (Or.inl rfl) W
  exact ⟨v, hX, ⟨W.takeUntil v hv⟩, ⟨W.dropUntil v hv⟩⟩

include H hc hall hr hq hT hρ in
/-- **(3) Crossing on the pocket.** Given the separation by the pocket curve of `s₉`
(`PocketSeparates`: the pocket lemma ⇒ with (D)), every `G_J(d₉)` walk from `z` to `y` or `w₂`
meets `X₉` at a non-hole vertex of the pocket of `s₉`. -/
theorem crossing_on_pocket (hsep : PocketSeparates P w m q ((piMove P)^[9] s)) {t : Fin n}
    (ht : t = w (q + 4) ∨ t = w (q + 2))
    (W : (GJ M h w q ((piMove P)^[9] (Gmap P ρ s))).Walk (w q) t) :
    ∃ v ∈ W.support, v ∈ X9 P ρ s ∧ v ∈ Pocket P m q ((piMove P)^[9] s) ∧
      ¬ HoleVT P w m q v := by
  obtain ⟨x1, x2⟩ := pos9_xplus H hc hall hr hq hT
  exact crossing_on_pocket_core H (iter_proper hc 9) x1 x2
    (fun v hv => (ring_agree H hc hall hr hq hT hρ 9 hv).2) hsep ht W

/-! ### The double break -/

variable (P w m q) in
/-- The pocket lemma at a state `c` (position `9`), as a named hypothesis: if `J` fails at `c`,
there is a pocket path and the pocket curve separates `z` from `y, w₂`. -/
def PocketLemmaAt (c : Fin n → Fin 4) : Prop :=
  ¬ JoinYZ M.graph h w q c → PocketPath P w m q c ∧ PocketSeparates P w m q c

variable (P w m q) in
/-- **What remains for `A₃₄′(L = 20)`**: both runs carry a separating pocket at position `9`,
and the two crossing statements hold with roles swapped by `G`. -/
def TwoPocketConj (c c' : Fin n → Fin 4) : Prop :=
  PocketPath P w m q c ∧ PocketPath P w m q c' ∧
  PocketSeparates P w m q c ∧ PocketSeparates P w m q c' ∧
  (∀ v, HoleVT P w m q v → c v = c' v) ∧
  (∀ t, (t = w (q + 4) ∨ t = w (q + 2)) → ∀ W : (GJ M h w q c').Walk (w q) t,
    ∃ v ∈ W.support, c v ≠ c' v ∧ v ∈ Pocket P m q c ∧ ¬ HoleVT P w m q v) ∧
  (∀ t, (t = w (q + 4) ∨ t = w (q + 2)) → ∀ W : (GJ M h w q c).Walk (w q) t,
    ∃ v ∈ W.support, c' v ≠ c v ∧ v ∈ Pocket P m q c' ∧ ¬ HoleVT P w m q v)

include H hc hall hr hq hT hρ in
/-- **Two applications of the crossing lemma.** If both runs break, the pocket lemma at `s₉`
and at `d₉` gives `TwoPocketConj s₉ d₉`; the second crossing is the first with roles swapped by
`G` (`d` is again in the setting, `d_setting`). -/
theorem two_pocket_conj (hps : PocketLemmaAt P w m q ((piMove P)^[9] s))
    (hpd : PocketLemmaAt P w m q ((piMove P)^[9] (Gmap P ρ s)))
    (hB : Break P w q s ∧ Break P w q (Gmap P ρ s)) :
    TwoPocketConj P w m q ((piMove P)^[9] s) ((piMove P)^[9] (Gmap P ρ s)) := by
  obtain ⟨ps, ss⟩ := hps hB.1
  obtain ⟨pd, sd⟩ := hpd hB.2
  obtain ⟨hcd, halld, hrd, hTd⟩ := d_setting H hc hall hr hq hT (ρ := ρ)
  obtain ⟨x1, x2⟩ := pos9_xplus H hcd halld hrd hq hTd
  have ag := fun v (hv : HoleVT P w m q v) => (ring_agree H hc hall hr hq hT hρ 9 hv).2
  refine ⟨ps, pd, ss, sd, fun v hv => (ag v hv).symm, fun t ht W => ?_, fun t ht W => ?_⟩
  · exact crossing_on_pocket_core H (iter_proper hc 9) (pos9_xplus H hc hall hr hq hT).1
      (pos9_xplus H hc hall hr hq hT).2 ag ss ht W
  · exact crossing_on_pocket_core H (iter_proper hcd 9) x1 x2
      (fun v hv => (ag v hv).symm) sd ht W

include htri H hc hall hr hq hT hρ in
/-- **What would finish `A₃₄′(L = 20)`.** Given the pocket lemma at `s₉` and `d₉`, refuting
`TwoPocketConj s₉ d₉` rules out two consecutive `k = 4` failures along the orbit. -/
theorem no_double_break_of_crossing_obstruction
    (hps : PocketLemmaAt P w m q ((piMove P)^[9] s))
    (hpd : PocketLemmaAt P w m q ((piMove P)^[9] (Gmap P ρ s)))
    (hobs : ¬ TwoPocketConj P w m q ((piMove P)^[9] s) ((piMove P)^[9] (Gmap P ρ s))) :
    ∀ b, ¬ (K4Fail P q ((piMove P)^[10 * b + 10] s) ∧
      K4Fail P q ((piMove P)^[10 * (b + 1) + 10] s)) :=
  (A34_two_iff htri H hc hall hr hq hT hρ).2
    (fun hB => hobs (two_pocket_conj H hc hall hr hq hT hρ hps hpd hB))

end setting

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.walk_transfer
#print axioms SimpleGraph.QuarterFloor.crossing_core
#print axioms SimpleGraph.QuarterFloor.crossing_on_pocket_core
#print axioms SimpleGraph.QuarterFloor.pos9_xplus
#print axioms SimpleGraph.QuarterFloor.X_far
#print axioms SimpleGraph.QuarterFloor.crossing_lemma
#print axioms SimpleGraph.QuarterFloor.crossing_exists
#print axioms SimpleGraph.QuarterFloor.crossing_on_pocket
#print axioms SimpleGraph.QuarterFloor.two_pocket_conj
#print axioms SimpleGraph.QuarterFloor.no_double_break_of_crossing_obstruction
