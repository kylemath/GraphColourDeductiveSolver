module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingReduce

/-!
# From a configuration occurrence to a ring face (step C)

* `nbr_of_chain`: at a vertex of degree `d`, a rotation chain `x 0 → x 1 → … → x (d-1)` lists
  every neighbour.
* `runTo_eq`: a tracked rotation run ends at the first surviving dart.
* `ringFace_of_fans`: if, at every ring vertex, the rotation of `T` runs from the previous ring
  vertex through interior vertices only to the next ring vertex, then after deleting the interior
  (with tracked rotation) the ring bounds a face.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyIcosahedral VacancyCliqueLift

variable {n : ℕ}

/-- Iterating along a rotation chain. -/
theorem iterate_chain {M : SphericalMap n} {v : Fin n} {x : ℕ → Fin n} {k : ℕ}
    (h0 : M.Adj v (x 0)) (hchain : ∀ j, j < k → Nx M v (x j) (x (j + 1))) :
    ∀ j, j ≤ k → ∃ hj : M.Adj v (x j),
      (⇑M.rotation.next)^[j] ⟨(v, x 0), h0⟩ = ⟨(v, x j), hj⟩ := by
  intro j
  induction j with
  | zero => intro _; exact ⟨h0, rfl⟩
  | succ j ih =>
    intro hj
    obtain ⟨hj', e⟩ := ih (by omega)
    obtain ⟨huv, huw, e2⟩ := nx_dart (hchain j (by omega))
    refine ⟨huw, ?_⟩
    rw [Function.iterate_succ_apply', e]
    exact e2

/-- **Neighbours from a full rotation chain.** -/
theorem nbr_of_chain {M : SphericalMap n} {v : Fin n} {d : ℕ} (hd : M.graph.degree v = d)
    {x : ℕ → Fin n} (h0 : M.Adj v (x 0)) (hchain : ∀ j, j + 1 < d → Nx M v (x j) (x (j + 1)))
    (w : Fin n) (hw : M.Adj v w) : ∃ j, j < d ∧ w = x j := by
  classical
  let σ := M.rotation.neighborRotation v
  let w0 : M.graph.neighborSet v := ⟨x 0, h0⟩
  have hsemi : Function.Semiconj (M.graph.dartOfNeighborSet v) σ M.rotation.next :=
    M.rotation.neighbor_rotation_dart v
  have hp : Function.minimalPeriod σ w0 = d := by
    rw [M.rotation.neighbor_period_eq_degree v w0, hd]
  have hdpos : 0 < d := by
    rw [← hd]; exact (M.graph.degree_pos_iff_exists_adj v).mpr ⟨w, hw⟩
  obtain ⟨k, hk⟩ := M.rotation.neighbor_rotation_cyclic v w0 ⟨w, hw⟩
  have hk' : σ^[k % d] w0 = ⟨w, hw⟩ := by
    rw [← hp, Function.iterate_mod_minimalPeriod_eq]; exact hk
  have hdart : (⇑M.rotation.next)^[k % d] ⟨(v, x 0), h0⟩ = ⟨(v, w), hw⟩ := by
    have := hsemi.iterate_right (k % d) w0
    rw [hk'] at this
    exact this.symm
  obtain ⟨hj, e⟩ := iterate_chain h0 (k := d - 1) (fun j hj => hchain j (by omega))
    (k % d) (by have := Nat.mod_lt k hdpos; omega)
  refine ⟨k % d, Nat.mod_lt _ hdpos, ?_⟩
  exact congrArg (fun d : M.Dart => d.snd) (hdart.symm.trans e)

/-- A tracked run that lands on a surviving dart ends at the first surviving dart. -/
theorem runTo_eq {M : SphericalMap n} {H : SimpleGraph (Fin n)} {d e : M.Dart} (r : RunTo M H d e)
    (heH : H.Adj e.fst e.snd) {k : ℕ} (hk : 0 < k) (hskip : ∀ j, 0 < j → j < k →
      ¬ H.Adj ((⇑M.rotation.next)^[j] d).fst ((⇑M.rotation.next)^[j] d).snd)
    (hland : H.Adj ((⇑M.rotation.next)^[k] d).fst ((⇑M.rotation.next)^[k] d).snd) :
    e = (⇑M.rotation.next)^[k] d := by
  obtain ⟨k', hk', he, hj⟩ := r
  rcases lt_trichotomy k' k with h | h | h
  · exact absurd (he ▸ heH) (hskip k' hk' h)
  · subst h; exact he.symm
  · exact absurd hland (hj k hk h)

/-- Periodic ring functions only need checking below the period. -/
theorem per_mod {ρ : ℕ → Fin n} {r : ℕ} (hr : 0 < r) (hper : ∀ t, ρ (t + r) = ρ t) :
    ∀ t, ρ t = ρ (t % r) := by
  intro t
  induction t using Nat.strong_induction_on with
  | h t ih =>
    by_cases ht : t < r
    · rw [Nat.mod_eq_of_lt ht]
    · have e : t = (t - r) + r := by omega
      rw [e, hper, ih _ (by omega), Nat.add_mod_right]

theorem RingFace.mk_lt {M : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} (hr : 0 < r)
    (hper : ∀ t, ρ (t + r) = ρ t) (hadj : ∀ t, t < r → M.Adj (ρ t) (ρ (t + 1)))
    (hstep : ∀ t, t < r → ∀ h1 h2, M.rotation.faceNext ⟨(ρ t, ρ (t + 1)), h1⟩ =
      ⟨(ρ (t + 1), ρ (t + 2)), h2⟩)
    (hinj : ∀ s t, s < r → t < r → ρ s = ρ t → s = t) : RingFace M r ρ := by
  have hm := per_mod hr hper
  have m1 : ∀ t, ρ (t + 1) = ρ (t % r + 1) := fun t => by
    rw [hm (t + 1), hm (t % r + 1)]; congr 1
    rw [Nat.add_mod t 1 r, Nat.add_mod (t % r) 1 r, Nat.mod_mod]
  have m2 : ∀ t, ρ (t + 2) = ρ (t % r + 2) := fun t => by
    rw [hm (t + 2), hm (t % r + 2)]; congr 1
    rw [Nat.add_mod t 2 r, Nat.add_mod (t % r) 2 r, Nat.mod_mod]
  have adj' : ∀ t, M.Adj (ρ t) (ρ (t + 1)) := fun t => by
    rw [hm t, m1 t]; exact hadj _ (Nat.mod_lt _ hr)
  refine ⟨hr, hper, adj', fun t => ?_, hinj⟩
  have h1 : M.Adj (ρ (t % r)) (ρ (t % r + 1)) := hadj _ (Nat.mod_lt _ hr)
  have h2 : M.Adj (ρ (t % r + 1)) (ρ (t % r + 1 + 1)) := adj' _
  have key := hstep _ (Nat.mod_lt _ hr) h1 h2
  have e1 : (⟨(ρ t, ρ (t + 1)), adj' t⟩ : M.Dart) = ⟨(ρ (t % r), ρ (t % r + 1)), h1⟩ := by
    apply Dart.ext; apply Prod.ext
    · exact hm t
    · exact m1 t
  have e2 : (⟨(ρ (t + 1), ρ (t + 2)), adj' (t + 1)⟩ : M.Dart) =
      ⟨(ρ (t % r + 1), ρ (t % r + 2)), h2⟩ := by
    apply Dart.ext; apply Prod.ext
    · exact m1 t
    · exact m2 t
  rw [e1, key, e2]

end SimpleGraph.SphericalMap


open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"
