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

`ExcPartition P T X` is not proved here: it says that `X` is a set of excursions with
starts in `T`, covering the unfilled states of `T`, with `Σ_T λ = Σ_X excMass`.
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

end sphere

end SimpleGraph.QuarterFloor
