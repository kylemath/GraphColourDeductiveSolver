/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterExcursion

/-!
# The group flow identity: `Σ_g λ = Σ_{Z > 0} def(Z) + Σ_{T ≤ 0} rem(T)`

Formalises §1.1–1.3 of `NightF6Flow.md` (with the excursion accounting of `NightLemmaR.md` §1,
`QuarterExcursion.lean`).

Fix a finite set `g` of proper states closed under `π` (a union of `π`-orbits, e.g. a `σ`-group
or a whole class). Its `π`-orbits are `orbitsOf P g` (`orbFin P c` is the orbit of `c` as a
finset); an orbit is **positive** if `Λ(Z) = Σ_Z λ > 0` (`posOrbits`), **nonpositive**
otherwise (`nonposOrbits`).

* `exits P g`: the pairs `(r, t)` with `r, t ∈ g`, `sigmaLink P r t` (`r` a `DD` endpoint and
  `t = σ r`), `t` lockless, `r` on a positive orbit and `t` on a nonpositive orbit.
* `credit P e = 3 f − 1`, where `f = hitLen P e.2` is the number of filled states of the
  excursion `(t, 1, f)` that the lockless state `t` starts (`sigma_hit_excursion`); it is
  exactly `−excMass` of that excursion (`credit_eq_neg_excMass`).
* `defOrb P g Z = Λ(Z) − Σ_{exits from Z} credit`, `remOrb P g T = Λ(T) + Σ_{exits into T} credit`.

## Main results (sorry-free, no new axioms)

* `sum_lam_eq_sum_orbits`: `Σ_g λ = Σ_{Z ∈ orbits g} Λ(Z)` (the orbits partition `g`).
* `flow_identity`: `Σ_g λ = Σ_{Z positive} def(Z) + Σ_{T nonpositive} rem(T)` — each exit's
  credit is subtracted at its source and added back at its target.
* `rem_eq_unhit`: for a nonpositive orbit `T` partitioned into excursions `X`
  (`ExcPartition`, the one named hypothesis), `rem(T)` is the sum of the masses of the
  excursions of `X` hit by no exit. Uses `no_double_hit_sigmaLink` (distinct exits hit distinct
  excursions), `noLock_in_excursion` (a hit excursion starts at the hit state, `u = 1`) and
  `hit_excursion_mass` (its mass is `−credit`).
* `sigmaC_of_def_rem`: `def ≤ 0` on positive orbits (Lemma S) and `rem ≤ 0` on nonpositive
  orbits (Lemma R) give `Σ_g λ ≤ 0`; `sigmaC_of_def_rem_groups`: per `σ`-group, they give `SigmaC P`.

* `excPartition_of_mixed`: the hypothesis is discharged for every **mixed** orbit (one unfilled
  and one filled state) with `X = excursionsOf P T`, all excursions starting in `T`: they cover
  the unfilled states and `Σ_T λ = Σ excMass` (each filled run is attached to the unfilled run
  before it; the intervals between consecutive starts partition one period).
* `rem` by orbit kind: `rem_eq_unhit_mixed` (no hypothesis); `rem_of_allFilled`
  (no exit enters, `rem = Λ ≤ 0`); `rem_of_allUnfilled` (`Γ`-cycles: a lockless state has a filled
  successor, so no exit enters and `rem = Λ`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-! ### Definitions -/

section defs
variable (P : Pent M.graph h)

open Classical in
/-- The `π`-orbit of `c` as a finset. -/
noncomputable def orbFin (c : Fin n → Fin 4) : Finset (Fin n → Fin 4) :=
  Finset.univ.filter (fun d => d ∈ piOrbit P c)

/-- `Λ(Z) = Σ_Z λ`. -/
noncomputable def orbSum (Z : Finset (Fin n → Fin 4)) : ℤ := ∑ d ∈ Z, lam P d

open Classical in
/-- The `π`-orbits of `g`. -/
noncomputable def orbitsOf (g : Finset (Fin n → Fin 4)) : Finset (Finset (Fin n → Fin 4)) :=
  g.image (orbFin P)

open Classical in
/-- The positive orbits of `g` (`Λ > 0`). -/
noncomputable def posOrbits (g : Finset (Fin n → Fin 4)) : Finset (Finset (Fin n → Fin 4)) :=
  (orbitsOf P g).filter (fun Z => 0 < orbSum P Z)

open Classical in
/-- The nonpositive orbits of `g` (`Λ ≤ 0`). -/
noncomputable def nonposOrbits (g : Finset (Fin n → Fin 4)) : Finset (Finset (Fin n → Fin 4)) :=
  (orbitsOf P g).filter (fun Z => orbSum P Z ≤ 0)

open Classical in
/-- The exits of `g` (`NightF6Flow.md` §1.1): `(r, σ r)` with `r` a `DD` endpoint on a positive
orbit and `σ r` lockless on a nonpositive orbit, both in `g`. -/
noncomputable def exits (g : Finset (Fin n → Fin 4)) :
    Finset ((Fin n → Fin 4) × (Fin n → Fin 4)) :=
  (g ×ˢ g).filter (fun e => sigmaLink P e.1 e.2 ∧ NoLock P e.2 ∧
    0 < orbSum P (orbFin P e.1) ∧ orbSum P (orbFin P e.2) ≤ 0)

open Classical in
/-- The number `f` of filled states of the excursion `(t, 1, f)` started by `t` (`0` if none). -/
noncomputable def hitLen (t : Fin n → Fin 4) : ℕ :=
  if hx : ∃ f, Excursion P t 1 f then Nat.find hx else 0

/-- The credit `3f − 1` of an exit `e = (r, t)`. -/
noncomputable def credit (e : (Fin n → Fin 4) × (Fin n → Fin 4)) : ℤ :=
  3 * (hitLen P e.2 : ℤ) - 1

open Classical in
/-- `def(Z) = Λ(Z) − Σ_{exits from Z} credit`. -/
noncomputable def defOrb (g Z : Finset (Fin n → Fin 4)) : ℤ :=
  orbSum P Z - ∑ e ∈ (exits P g).filter (fun e => orbFin P e.1 = Z), credit P e

open Classical in
/-- `rem(T) = Λ(T) + Σ_{exits into T} credit` (`= Λ(T) − hit(T)`). -/
noncomputable def remOrb (g T : Finset (Fin n → Fin 4)) : ℤ :=
  orbSum P T + ∑ e ∈ (exits P g).filter (fun e => orbFin P e.2 = T), credit P e

/-- **The orbit `T` is partitioned into the excursions `X`** (the one named hypothesis): the
elements of `X` are excursions `(e, u, f)` with starts in `T`, every unfilled state of
`T` lies in one of them, and `Σ_T λ = Σ_X excMass`. -/
structure ExcPartition (T : Finset (Fin n → Fin 4))
    (X : Finset ((Fin n → Fin 4) × ℕ × ℕ)) : Prop where
  exc : ∀ x ∈ X, Excursion P x.1 x.2.1 x.2.2
  start_mem : ∀ x ∈ X, x.1 ∈ T
  cover : ∀ d ∈ T, ¬ Target M.graph h d → ∃ x ∈ X, InExc P x.1 x.2.1 x.2.2 d
  sum_eq : orbSum P T = ∑ x ∈ X, excMass P x.1 x.2.1 x.2.2

end defs

variable {P : Pent M.graph h} {g : Finset (Fin n → Fin 4)} {c d t : Fin n → Fin 4}

/-! ### Orbits -/

lemma mem_orbFin : d ∈ orbFin P c ↔ ∃ k : ℕ, d = (piMove P)^[k] c := by
  classical
  simp only [orbFin, Finset.mem_filter, Finset.mem_univ, true_and]
  rfl

lemma self_mem_orbFin : c ∈ orbFin P c := mem_orbFin.2 ⟨0, rfl⟩

/-- Orbits are equal or disjoint: a state of the orbit of a proper `c` has the same orbit. -/
lemma orbFin_eq_of_mem (hc : ProperOff M.graph h c) (hd : d ∈ orbFin P c) :
    orbFin P d = orbFin P c := by
  obtain ⟨k, rfl⟩ := mem_orbFin.1 hd
  obtain ⟨m, hm, hper⟩ := iterate_period (P := P) hc
  have key : (piMove P)^[(m - 1) * k] ((piMove P)^[k] c) = c := by
    rw [← Function.iterate_add_apply]
    have : (m - 1) * k + k = m * k := by
      obtain ⟨m', rfl⟩ : ∃ m', m = m' + 1 := ⟨m - 1, by omega⟩
      simp [Nat.add_mul]
    rw [this, Function.iterate_mul, Function.iterate_fixed hper]
  ext x
  simp only [mem_orbFin]
  constructor
  · rintro ⟨i, rfl⟩
    exact ⟨i + k, by rw [Function.iterate_add_apply]⟩
  · rintro ⟨i, rfl⟩
    exact ⟨i + (m - 1) * k, by rw [Function.iterate_add_apply, key]⟩

lemma orbFin_subset (hinv : Set.MapsTo (piMove P) (g : Set _) g) (hc : c ∈ g) :
    orbFin P c ⊆ g := by
  intro d hd
  obtain ⟨k, rfl⟩ := mem_orbFin.1 hd
  exact hinv.iterate k hc

/-- **The orbits partition `g`**: `Σ_g λ = Σ_{Z ∈ orbits g} Λ(Z)`. -/
theorem sum_lam_eq_sum_orbits (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hinv : Set.MapsTo (piMove P) (g : Set _) g) :
    ∑ d ∈ g, lam P d = ∑ Z ∈ orbitsOf P g, orbSum P Z := by
  classical
  unfold orbitsOf
  rw [Finset.sum_image' (lam P)]
  intro c hc
  unfold orbSum
  refine Finset.sum_congr ?_ fun _ _ => rfl
  ext d
  rw [Finset.mem_filter]
  constructor
  · intro hd
    exact ⟨orbFin_subset hinv hc hd, orbFin_eq_of_mem (hp c hc) hd⟩
  · rintro ⟨-, he⟩
    rw [← he]
    exact self_mem_orbFin

/-! ### The flow identity -/

lemma mem_exits {e : (Fin n → Fin 4) × (Fin n → Fin 4)} (he : e ∈ exits P g) :
    e.1 ∈ g ∧ e.2 ∈ g ∧ sigmaLink P e.1 e.2 ∧ NoLock P e.2 ∧
      0 < orbSum P (orbFin P e.1) ∧ orbSum P (orbFin P e.2) ≤ 0 := by
  classical
  unfold exits at he
  rw [Finset.mem_filter, Finset.mem_product] at he
  exact ⟨he.1.1, he.1.2, he.2⟩

/-- **The flow identity** (`NightF6Flow.md` §1.2): a pure rearrangement — each exit's credit is
subtracted at its (positive) source and added back at its (nonpositive) target. -/
theorem flow_identity (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hinv : Set.MapsTo (piMove P) (g : Set _) g) :
    ∑ d ∈ g, lam P d =
      ∑ Z ∈ posOrbits P g, defOrb P g Z + ∑ T ∈ nonposOrbits P g, remOrb P g T := by
  classical
  have src : ∑ Z ∈ posOrbits P g,
      ∑ e ∈ (exits P g).filter (fun e => orbFin P e.1 = Z), credit P e =
      ∑ e ∈ exits P g, credit P e := by
    refine Finset.sum_fiberwise_of_maps_to (fun e he => ?_) _
    obtain ⟨h1, -, -, -, h5, -⟩ := mem_exits he
    unfold posOrbits orbitsOf
    exact Finset.mem_filter.2 ⟨Finset.mem_image_of_mem _ h1, h5⟩
  have tgt : ∑ T ∈ nonposOrbits P g,
      ∑ e ∈ (exits P g).filter (fun e => orbFin P e.2 = T), credit P e =
      ∑ e ∈ exits P g, credit P e := by
    refine Finset.sum_fiberwise_of_maps_to (fun e he => ?_) _
    obtain ⟨-, h2, -, -, -, h6⟩ := mem_exits he
    unfold nonposOrbits orbitsOf
    exact Finset.mem_filter.2 ⟨Finset.mem_image_of_mem _ h2, h6⟩
  have split : ∑ Z ∈ orbitsOf P g, orbSum P Z =
      ∑ Z ∈ posOrbits P g, orbSum P Z + ∑ T ∈ nonposOrbits P g, orbSum P T := by
    unfold posOrbits nonposOrbits
    rw [← Finset.sum_filter_add_sum_filter_not (orbitsOf P g) (fun Z => 0 < orbSum P Z)]
    congr 1
    refine Finset.sum_congr ?_ fun _ _ => rfl
    ext Z
    simp only [Finset.mem_filter, not_lt]
  unfold defOrb remOrb
  rw [sum_lam_eq_sum_orbits hp hinv, split, Finset.sum_sub_distrib, Finset.sum_add_distrib, src,
    tgt]
  ring

/-- **σC from Lemmas S and R** (`NightF6Flow.md` §1.3): if `def(Z) ≤ 0` on every positive orbit
and `rem(T) ≤ 0` on every nonpositive orbit of `g`, then `Σ_g λ ≤ 0`. -/
theorem sigmaC_of_def_rem (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hinv : Set.MapsTo (piMove P) (g : Set _) g)
    (hS : ∀ Z ∈ posOrbits P g, defOrb P g Z ≤ 0)
    (hR : ∀ T ∈ nonposOrbits P g, remOrb P g T ≤ 0) :
    ∑ d ∈ g, lam P d ≤ 0 := by
  rw [flow_identity hp hinv]
  exact add_nonpos (Finset.sum_nonpos hS) (Finset.sum_nonpos hR)

/-- `σC` at the hole from Lemmas S and R on every `σ`-group. -/
theorem sigmaC_of_def_rem_groups
    (H : ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ → ∀ c ∈ kclass M h c₀,
      (∀ Z ∈ posOrbits P (sigmaGroup P c₀ c), defOrb P (sigmaGroup P c₀ c) Z ≤ 0) ∧
      (∀ T ∈ nonposOrbits P (sigmaGroup P c₀ c), remOrb P (sigmaGroup P c₀ c) T ≤ 0)) :
    SigmaC P := fun c₀ h₀ c hc =>
  sigmaC_of_def_rem sigmaGroup_properOff sigmaGroup_piInvariant.mapsTo
    (H c₀ h₀ c hc).1 (H c₀ h₀ c hc).2

/-! ### Credits and the remainder -/

/-- An excursion is determined by its start and `u`. -/
lemma excursion_f_unique {e : Fin n → Fin 4} {u f f' : ℕ} (E : Excursion P e u f)
    (E' : Excursion P e u f') : f = f' := by
  rcases lt_trichotomy f f' with hl | rfl | hl
  · exact absurd (E'.fil (u + f) (by omega) (by omega)) E.next
  · rfl
  · exact absurd (E.fil (u + f') (by omega) (by omega)) E'.next

lemma hitLen_spec {f : ℕ} (E : Excursion P t 1 f) : hitLen P t = f := by
  classical
  have hx : ∃ f, Excursion P t 1 f := ⟨f, E⟩
  unfold hitLen
  split
  · rename_i hx'
    exact excursion_f_unique (Nat.find_spec hx') E
  · exact absurd hx ‹_›

lemma excursion_hitLen (ht : ProperOff M.graph h t) (hN : NoLock P t) :
    Excursion P t 1 (hitLen P t) := by
  obtain ⟨f, E⟩ := exists_excursion_of_noLock ht hN
  rw [hitLen_spec E]; exact E

/-- The credit of an exit is minus the mass of the excursion its target starts. -/
lemma credit_eq_neg_excMass {e : (Fin n → Fin 4) × (Fin n → Fin 4)} (he : e ∈ exits P g)
    (hp : ∀ d ∈ g, ProperOff M.graph h d) :
    credit P e = -excMass P e.2 1 (hitLen P e.2) := by
  obtain ⟨-, h2, -, hN, -, -⟩ := mem_exits he
  have E := excursion_hitLen (hp _ h2) hN
  rw [hit_excursion_mass (k := 0) E (by have := E.f_pos; omega) hN, credit]
  ring

open Classical in
/-- **`rem(T)` is the mass of the unhit excursions** (`NightF6Flow.md` §1.1,
`NightLemmaR.md`): for an orbit `T` of `g` partitioned into the excursions
`X`, `rem(T) = Σ` of `excMass` over the excursions of `X` that contain no exit target. -/
theorem rem_eq_unhit (hp : ∀ d ∈ g, ProperOff M.graph h d) {T : Finset (Fin n → Fin 4)}
    (hT : T ∈ orbitsOf P g) {X : Finset ((Fin n → Fin 4) × ℕ × ℕ)} (hX : ExcPartition P T X) :
    remOrb P g T = ∑ x ∈ X.filter
      (fun x => ¬ ∃ e ∈ exits P g, InExc P x.1 x.2.1 x.2.2 e.2), excMass P x.1 x.2.1 x.2.2 := by
  classical
  obtain ⟨c, hcg, rfl⟩ := Finset.mem_image.1 (show T ∈ g.image (orbFin P) from hT)
  -- a hit state of an excursion of `X` is its start, with `u = 1` and `f = hitLen`
  have start : ∀ x ∈ X, ∀ e ∈ exits P g, InExc P x.1 x.2.1 x.2.2 e.2 →
      x = (e.2, 1, hitLen P e.2) := by
    rintro ⟨x1, u, f⟩ hx e he ⟨k, hk, hke⟩
    obtain ⟨-, -, -, hN, -, -⟩ := mem_exits he
    have E := hX.exc _ hx
    obtain ⟨rfl, rfl⟩ := noLock_in_excursion E hk (hke ▸ hN)
    simp only [Function.iterate_zero, id] at hke
    subst hke
    rw [hitLen_spec E]
  have inExc0 : ∀ {x1 : Fin n → Fin 4} {f : ℕ}, InExc P x1 1 f x1 := fun {_ _} =>
    ⟨0, by omega, rfl⟩
  set Ein := (exits P g).filter (fun e => orbFin P e.2 = orbFin P c)
  set Xh := X.filter (fun x => ∃ e ∈ exits P g, InExc P x.1 x.2.1 x.2.2 e.2)
  have hbij : ∑ e ∈ Ein, credit P e = ∑ x ∈ Xh, -excMass P x.1 x.2.1 x.2.2 := by
    refine Finset.sum_bij (fun e _ => (e.2, 1, hitLen P e.2)) ?_ ?_ ?_ ?_
    · intro e he
      obtain ⟨he, hT2⟩ := Finset.mem_filter.1 he
      obtain ⟨-, h2, -, hN, -, -⟩ := mem_exits he
      have hmem : e.2 ∈ orbFin P c := hT2 ▸ self_mem_orbFin
      obtain ⟨x, hx, hin⟩ := hX.cover _ hmem (noLock_unfilled hN)
      have hxe := start x hx e he hin
      refine Finset.mem_filter.2 ⟨hxe ▸ hx, e, he, inExc0⟩
    · intro e he e' he' hee
      obtain ⟨he, -⟩ := Finset.mem_filter.1 he
      obtain ⟨he', -⟩ := Finset.mem_filter.1 he'
      obtain ⟨h1, h2, hl, hN, -, -⟩ := mem_exits he
      obtain ⟨h1', -, hl', hN', -, -⟩ := mem_exits he'
      have e22 : e.2 = e'.2 := congrArg Prod.fst hee
      have E := excursion_hitLen (hp _ h2) hN
      have h11 := no_double_hit_sigmaLink E (hp _ h1) hl hN (hp _ h1') hl' hN' inExc0
        (e22 ▸ inExc0)
      exact Prod.ext h11 e22
    · intro x hx
      obtain ⟨hx, e, he, hin⟩ := Finset.mem_filter.1 hx
      have hxe := start x hx e he hin
      have hs := hX.start_mem x hx
      rw [hxe] at hs
      refine ⟨e, Finset.mem_filter.2 ⟨he, orbFin_eq_of_mem (hp c hcg) hs⟩, hxe.symm⟩
    · intro e he
      exact credit_eq_neg_excMass (Finset.mem_filter.1 he).1 hp
  unfold remOrb
  rw [hX.sum_eq, hbij, Finset.sum_neg_distrib,
    ← Finset.sum_filter_add_sum_filter_not X
      (fun x => ∃ e ∈ exits P g, InExc P x.1 x.2.1 x.2.2 e.2)]
  ring

/-! ### The excursion partition of an orbit -/

section partition
variable (P) in
/-- `d` starts an excursion: `d` is unfilled and its `π`-predecessor is filled. -/
def IsStart (d : Fin n → Fin 4) : Prop :=
  ¬ Target M.graph h d ∧ Target M.graph h (piInv P d)

open Classical in
variable (P) in
/-- All excursions `(e, u, f)` starting in `T` (with `u, f ≤ |T|`). -/
noncomputable def excursionsOf (T : Finset (Fin n → Fin 4)) :
    Finset ((Fin n → Fin 4) × ℕ × ℕ) :=
  (T ×ˢ (Finset.range (T.card + 1) ×ˢ Finset.range (T.card + 1))).filter
    (fun x => Excursion P x.1 x.2.1 x.2.2)

variable {e : Fin n → Fin 4} {u f u' f' : ℕ}

lemma excursion_u_unique (E : Excursion P e u f) (E' : Excursion P e u' f') : u = u' := by
  rcases lt_trichotomy u u' with hl | rfl | hl
  · exact absurd (E.fil u le_rfl (by have := E.f_pos; omega)) (E'.unf u hl)
  · rfl
  · exact absurd (E'.fil u' le_rfl (by have := E'.f_pos; omega)) (E.unf u' hl)

lemma piInv_iter_succ (hc : ProperOff M.graph h c) (k : ℕ) :
    piInv P ((piMove P)^[k + 1] c) = (piMove P)^[k] c := by
  rw [Function.iterate_succ_apply']
  exact piInv_piMove (iter_properOff hc k)

lemma Excursion.isStart (E : Excursion P e u f) : IsStart P e :=
  ⟨E.unf 0 E.u_pos, E.prev⟩

/-- The state after an excursion starts the next one. -/
lemma Excursion.end_isStart (E : Excursion P e u f) : IsStart P ((piMove P)^[u + f] e) := by
  refine ⟨E.next, ?_⟩
  have u1 := E.u_pos
  obtain ⟨t, ht⟩ : ∃ t, u + f = t + 1 := ⟨u + f - 1, by omega⟩
  rw [ht, piInv_iter_succ E.proper]
  exact E.fil t (by have := E.f_pos; omega) (by omega)

/-- No excursion starts strictly inside another. -/
lemma Excursion.not_isStart (E : Excursion P e u f) {t : ℕ} (h0 : 0 < t) (ht : t < u + f) :
    ¬ IsStart P ((piMove P)^[t] e) := by
  rintro ⟨hU, hF⟩
  obtain ⟨t', rfl⟩ : ∃ t', t = t' + 1 := ⟨t - 1, by omega⟩
  rw [piInv_iter_succ E.proper] at hF
  by_cases htu : t' + 1 < u
  · exact E.unf t' (by omega) hF
  · exact hU (E.fil _ (by omega) ht)

/-- A start on an orbit containing a filled state starts an excursion. -/
lemma exists_excursion_of_start (hd : ProperOff M.graph h e) (hs : IsStart P e)
    (hF : ∃ k, Target M.graph h ((piMove P)^[k] e)) : ∃ u f, Excursion P e u f := by
  classical
  obtain ⟨m, hm, hper⟩ := iterate_period (P := P) hd
  set u := Nat.find hF with hu
  have hu0 : 0 < u := by
    rw [Nat.pos_iff_ne_zero]; intro h0
    have := Nat.find_spec hF; rw [← hu, h0] at this; exact hs.1 this
  have hU' : ∃ j, ¬ Target M.graph h ((piMove P)^[u + 1 + j] e) := by
    refine ⟨m * (u + 1) - (u + 1), ?_⟩
    have : u + 1 + (m * (u + 1) - (u + 1)) = m * (u + 1) := by
      have : u + 1 ≤ m * (u + 1) := Nat.le_mul_of_pos_left _ hm
      omega
    rw [this, Function.iterate_mul, Function.iterate_fixed hper]
    exact hs.1
  refine ⟨u, Nat.find hU' + 1, hd, hu0, Nat.succ_pos _, hs.2, fun k hk => Nat.find_min hF hk,
    fun k hk hk' => ?_, ?_⟩
  · rcases Nat.eq_or_lt_of_le hk with rfl | hlt
    · exact Nat.find_spec hF
    · obtain ⟨j, rfl⟩ : ∃ j, k = u + 1 + j := ⟨k - (u + 1), by omega⟩
      exact not_not.1 (Nat.find_min hU' (by omega))
  · have : u + (Nat.find hU' + 1) = u + 1 + Nat.find hU' := by omega
    rw [this]; exact Nat.find_spec hU'

lemma iter_mem_orbFin (k : ℕ) : (piMove P)^[k] c ∈ orbFin P c := mem_orbFin.2 ⟨k, rfl⟩

lemma piMove_mem_orbFin (hd : d ∈ orbFin P c) : piMove P d ∈ orbFin P c := by
  obtain ⟨k, rfl⟩ := mem_orbFin.1 hd
  rw [← Function.iterate_succ_apply' (piMove P) k c]; exact iter_mem_orbFin _

lemma properOff_of_mem_orbFin (hc : ProperOff M.graph h c) (hd : d ∈ orbFin P c) :
    ProperOff M.graph h d := by
  obtain ⟨k, rfl⟩ := mem_orbFin.1 hd; exact iter_properOff hc k

/-- **The excursion partition of an orbit through a start** `c₀`. -/
theorem excPartition_of_start {c₀ : Fin n → Fin 4} (hc : ProperOff M.graph h c₀)
    (hs : IsStart P c₀) : ExcPartition P (orbFin P c₀) (excursionsOf P (orbFin P c₀)) := by
  classical
  set φ : ℕ → Fin n → Fin 4 := fun i => (piMove P)^[i] c₀ with hφ
  have hadd : ∀ a b, (piMove P)^[a] (φ b) = φ (a + b) := fun a b =>
    (Function.iterate_add_apply _ _ _ _).symm
  obtain ⟨m, hm, hper⟩ := iterate_period (P := P) hc
  set L := Function.minimalPeriod (piMove P) c₀ with hLdef
  have hL : 0 < L := Function.minimalPeriod_pos_of_mem_periodicPts
    (Function.mk_mem_periodicPts hm hper)
  have hLper : φ L = c₀ := Function.iterate_minimalPeriod
  have hinj : ∀ a < L, ∀ b < L, φ a = φ b → a = b := fun a ha b hb hab =>
    Function.iterate_injOn_Iio_minimalPeriod ha hb hab
  have hT : orbFin P c₀ = (Finset.range L).image φ := by
    ext d
    rw [mem_orbFin, Finset.mem_image]
    constructor
    · rintro ⟨k, rfl⟩
      exact ⟨k % L, Finset.mem_range.2 (Nat.mod_lt _ hL), Function.iterate_mod_minimalPeriod_eq⟩
    · rintro ⟨i, -, rfl⟩; exact ⟨i, rfl⟩
  have hsum : ∀ g' : (Fin n → Fin 4) → ℤ,
      ∑ d ∈ orbFin P c₀, g' d = ∑ i ∈ Finset.range L, g' (φ i) := by
    intro g'
    rw [hT, Finset.sum_image fun a ha b hb => hinj a (Finset.mem_range.1 ha) b
      (Finset.mem_range.1 hb)]
  have hcard : (orbFin P c₀).card = L := by
    rw [hT, Finset.card_image_of_injOn fun a ha b hb => hinj a (Finset.mem_range.1 ha) b
      (Finset.mem_range.1 hb), Finset.card_range]
  -- the predecessor of `c₀` is `φ (L - 1)`, which is filled
  have hlast : Target M.graph h (φ (L - 1)) := by
    have : piInv P (φ (L - 1 + 1)) = φ (L - 1) := piInv_iter_succ hc _
    rw [Nat.sub_add_cancel hL, hLper] at this
    rw [← this]; exact hs.2
  set starts := (Finset.range L).filter (fun s => IsStart P (φ s)) with hstarts
  have hex : ∀ s ∈ starts, ∃ u f, Excursion P (φ s) u f := by
    intro s hs'
    obtain ⟨hsL, hst⟩ := Finset.mem_filter.1 hs'
    refine exists_excursion_of_start (iter_properOff hc s) hst ⟨L - 1 - s, ?_⟩
    rw [hadd]
    have : L - 1 - s + s = L - 1 := by have := Finset.mem_range.1 hsL; omega
    rw [this]; exact hlast
  choose! uu ff hE using hex
  have K1 : ∀ s ∈ starts, s + (uu s + ff s) ≤ L := by
    intro s hs'
    have hsL := Finset.mem_range.1 (Finset.mem_filter.1 hs').1
    by_contra hlt
    have := (hE s hs').not_isStart (t := L - s) (by omega) (by omega)
    rw [hadd, Nat.sub_add_cancel hsL.le, hLper] at this
    exact this hs
  set sOf : ℕ → ℕ := fun i => Nat.findGreatest (fun s => IsStart P (φ s)) i with hsOf
  have hφ0 : IsStart P (φ 0) := hs
  have S1 : ∀ i, IsStart P (φ (sOf i)) := fun i =>
    Nat.findGreatest_spec (P := fun s => IsStart P (φ s)) (Nat.zero_le i) hφ0
  have S2 : ∀ i, sOf i ≤ i := fun i => Nat.findGreatest_le i
  have Smem : ∀ i < L, sOf i ∈ starts := fun i hi =>
    Finset.mem_filter.2 ⟨Finset.mem_range.2 (lt_of_le_of_lt (S2 i) hi), S1 i⟩
  have S3 : ∀ i < L, i < sOf i + (uu (sOf i) + ff (sOf i)) := by
    intro i hi
    have E := hE _ (Smem i hi)
    by_contra hle
    have hst := E.end_isStart
    rw [hadd] at hst
    have h1 : uu (sOf i) + ff (sOf i) + sOf i ≤ sOf i :=
      Nat.le_findGreatest (P := fun s => IsStart P (φ s)) (n := i) (by omega) hst
    have := E.u_pos
    omega
  have S4 : ∀ s ∈ starts, ∀ k < uu s + ff s, sOf (k + s) = s := by
    intro s hs' k hk
    have E := hE s hs'
    refine le_antisymm ?_ (Nat.le_findGreatest (by omega) (Finset.mem_filter.1 hs').2)
    by_contra hlt
    have := E.not_isStart (t := sOf (k + s) - s) (by omega) (by have := S2 (k + s); omega)
    rw [hadd, Nat.sub_add_cancel (by omega)] at this
    exact this (S1 _)
  have hXeq : excursionsOf P (orbFin P c₀) = starts.image (fun s => (φ s, uu s, ff s)) := by
    ext ⟨x1, u, f⟩
    simp only [excursionsOf, Finset.mem_filter, Finset.mem_product, Finset.mem_range,
      Finset.mem_image, Prod.mk.injEq]
    constructor
    · rintro ⟨⟨hx1, -, -⟩, E⟩
      rw [hT, Finset.mem_image] at hx1
      obtain ⟨s, hsL, rfl⟩ := hx1
      have hs' : s ∈ starts := Finset.mem_filter.2 ⟨hsL, E.isStart⟩
      have eu := excursion_u_unique (hE s hs') E
      have hE2 := hE s hs'
      rw [eu] at hE2
      exact ⟨s, hs', rfl, eu, excursion_f_unique hE2 E⟩
    · rintro ⟨s, hs', rfl, rfl, rfl⟩
      have := K1 s hs'
      have := (hE s hs').u_pos
      have := (hE s hs').f_pos
      exact ⟨⟨iter_mem_orbFin s, by omega, by omega⟩, hE s hs'⟩
  have hXinj : Set.InjOn (fun s => (φ s, uu s, ff s)) (starts : Set ℕ) := by
    intro a ha b hb hab
    exact hinj a (Finset.mem_range.1 (Finset.mem_filter.1 ha).1) b
      (Finset.mem_range.1 (Finset.mem_filter.1 hb).1) (congrArg Prod.fst hab)
  refine ⟨fun x hx => (Finset.mem_filter.1 hx).2,
    fun x hx => (Finset.mem_product.1 (Finset.mem_filter.1 hx).1).1, ?_, ?_⟩
  · intro d hd _
    rw [hT, Finset.mem_image] at hd
    obtain ⟨i, hi, rfl⟩ := hd
    have hi := Finset.mem_range.1 hi
    refine ⟨(φ (sOf i), uu (sOf i), ff (sOf i)), ?_, i - sOf i,
      Nat.sub_lt_left_of_lt_add (S2 i) (S3 i hi), ?_⟩
    · rw [hXeq]; exact Finset.mem_image_of_mem _ (Smem i hi)
    · show (piMove P)^[i - sOf i] (φ (sOf i)) = φ i
      rw [hadd, Nat.sub_add_cancel (S2 i)]
  · unfold orbSum
    rw [hXeq, Finset.sum_image hXinj, hsum]
    have hm' : ∀ s, excMass P (φ s) (uu s) (ff s) =
        ∑ k ∈ Finset.range (uu s + ff s), lam P (φ (k + s)) := by
      intro s; unfold excMass; simp only [hadd]
    simp only [hm']
    rw [Finset.sum_sigma' starts (fun s => Finset.range (uu s + ff s))
      (fun s k => lam P (φ (k + s)))]
    refine Finset.sum_bij' (fun i _ => ⟨sOf i, i - sOf i⟩) (fun p _ => p.2 + p.1) ?_ ?_ ?_ ?_ ?_
    · intro i hi
      have hi := Finset.mem_range.1 hi
      exact Finset.mem_sigma.2 ⟨Smem i hi,
        Finset.mem_range.2 (Nat.sub_lt_left_of_lt_add (S2 i) (S3 i hi))⟩
    · rintro ⟨s, k⟩ hp
      obtain ⟨hs', hk⟩ := Finset.mem_sigma.1 hp
      have := K1 s hs'
      have hk := Finset.mem_range.1 hk
      dsimp only at hk ⊢
      exact Finset.mem_range.2 (by omega)
    · intro i hi
      exact Nat.sub_add_cancel (S2 i)
    · rintro ⟨s, k⟩ hp
      obtain ⟨hs', hk⟩ := Finset.mem_sigma.1 hp
      have e1 := S4 s hs' k (Finset.mem_range.1 hk)
      simp only [e1, Nat.add_sub_cancel]
    · intro i hi
      simp only [Nat.sub_add_cancel (S2 i)]

/-- **The excursion partition of a mixed orbit** (one unfilled and one filled state): the
excursions of `T` cover its unfilled states, have distinct starts, and
`Σ_T λ = Σ excMass` (every filled run is attached to the unfilled run before it). -/
theorem excPartition_of_mixed (hc : ProperOff M.graph h c)
    (hU : ∃ d ∈ orbFin P c, ¬ Target M.graph h d)
    (hF : ∃ d ∈ orbFin P c, Target M.graph h d) :
    ExcPartition P (orbFin P c) (excursionsOf P (orbFin P c)) := by
  classical
  obtain ⟨e, he, heF⟩ := hF
  obtain ⟨d, hd, hdU⟩ := hU
  have hoe := orbFin_eq_of_mem hc he
  have hep := properOff_of_mem_orbFin hc he
  have hex : ∃ j, ¬ Target M.graph h ((piMove P)^[j] e) := by
    rw [← hoe] at hd
    obtain ⟨j, rfl⟩ := mem_orbFin.1 hd
    exact ⟨j, hdU⟩
  have h0 : Nat.find hex ≠ 0 := by
    intro h0; have := Nat.find_spec hex; rw [h0] at this; exact this heF
  obtain ⟨j1, hj1⟩ : ∃ j1, Nat.find hex = j1 + 1 := ⟨Nat.find hex - 1, by omega⟩
  have hst : IsStart P ((piMove P)^[j1 + 1] e) := by
    refine ⟨hj1 ▸ Nat.find_spec hex, ?_⟩
    rw [piInv_iter_succ hep]
    exact not_not.1 (Nat.find_min hex (by omega))
  have hmem : (piMove P)^[j1 + 1] e ∈ orbFin P c := hoe ▸ iter_mem_orbFin _
  rw [← orbFin_eq_of_mem hc hmem]
  exact excPartition_of_start (iter_properOff hep _) hst

end partition

/-! ### `rem` by orbit kind -/

open Classical in
/-- **Mixed orbits**: `rem(T)` is the mass of the excursions of `T` hit by no exit. -/
theorem rem_eq_unhit_mixed (hp : ∀ d ∈ g, ProperOff M.graph h d) {T : Finset (Fin n → Fin 4)}
    (hT : T ∈ orbitsOf P g) (hU : ∃ d ∈ T, ¬ Target M.graph h d)
    (hF : ∃ d ∈ T, Target M.graph h d) :
    remOrb P g T = ∑ x ∈ (excursionsOf P T).filter
      (fun x => ¬ ∃ e ∈ exits P g, InExc P x.1 x.2.1 x.2.2 e.2), excMass P x.1 x.2.1 x.2.2 := by
  obtain ⟨c, hcg, rfl⟩ := Finset.mem_image.1 (show T ∈ g.image (orbFin P) from hT)
  exact rem_eq_unhit hp hT (excPartition_of_mixed (hp c hcg) hU hF)

open Classical in
/-- No exit enters an orbit with no lockless state. -/
lemma exitsInto_eq_zero {T : Finset (Fin n → Fin 4)}
    (hno : ∀ t ∈ T, ProperOff M.graph h t → NoLock P t → False)
    (hp : ∀ d ∈ g, ProperOff M.graph h d) :
    ∑ e ∈ (exits P g).filter (fun e => orbFin P e.2 = T), credit P e = 0 := by
  refine Finset.sum_eq_zero fun e he => ?_
  obtain ⟨he, hT2⟩ := Finset.mem_filter.1 he
  obtain ⟨-, h2, -, hN, -, -⟩ := mem_exits he
  exact (hno e.2 (hT2 ▸ self_mem_orbFin) (hp _ h2) hN).elim

/-- **All-filled orbits**: no exit enters, so `rem(T) = Λ(T)`, and `Λ(T) = −3|T| ≤ 0`. -/
theorem rem_of_allFilled (hp : ∀ d ∈ g, ProperOff M.graph h d) {T : Finset (Fin n → Fin 4)}
    (hT : T ∈ orbitsOf P g) (hA : ∀ d ∈ T, Target M.graph h d) :
    remOrb P g T = orbSum P T ∧ orbSum P T ≤ 0 := by
  obtain ⟨c, hcg, rfl⟩ := Finset.mem_image.1 (show T ∈ g.image (orbFin P) from hT)
  refine ⟨?_, ?_⟩
  · unfold remOrb
    rw [exitsInto_eq_zero (fun t ht _ hN => noLock_unfilled hN (hA t ht)) hp, add_zero]
  · refine Finset.sum_nonpos fun d hd => ?_
    rw [lam_FF (properOff_of_mem_orbFin (hp c hcg) hd) (hA d hd) (hA _ (piMove_mem_orbFin hd))]
    norm_num

/-- **All-unfilled orbits** (`Γ`-cycles): a lockless state has a filled successor, so no exit
enters and `rem(T) = Λ(T)`. -/
theorem rem_of_allUnfilled (hp : ∀ d ∈ g, ProperOff M.graph h d) {T : Finset (Fin n → Fin 4)}
    (hT : T ∈ orbitsOf P g) (hA : ∀ d ∈ T, ¬ Target M.graph h d) :
    remOrb P g T = orbSum P T := by
  obtain ⟨c, hcg, rfl⟩ := Finset.mem_image.1 (show T ∈ g.image (orbFin P) from hT)
  unfold remOrb
  rw [exitsInto_eq_zero (fun t ht hpt hN => hA _ (piMove_mem_orbFin ht)
    (noLock_next_filled hpt hN)) hp, add_zero]

end sphere

end SimpleGraph.QuarterFloor
