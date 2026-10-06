module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingJordan

/-!
# Kempe chains on a ring face

G0. `ring_face_period`, `ring_rv`: if the rotation of a spherical map steps from `ρ (t-1)` to
`ρ (t+1)` at every ring vertex `ρ t` (in the sense of the face successor), the ring darts form
one face with boundary `ρ 0, …, ρ (r-1)`.

C1. `chains_noncrossing`, `chains_noncrossing_same`: two Kempe chains of disjoint colour pairs,
or two different components of one colour pair, cannot join alternating ring positions.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill

variable {n : ℕ} (M : SphericalMap n)

/-- Ring data: `ρ` is `r`-periodic, consecutive ring vertices are adjacent, the face successor
of each ring dart is the next ring dart, and the `r` ring vertices are distinct. -/
structure RingFace (r : ℕ) (ρ : ℕ → Fin n) : Prop where
  pos : 0 < r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, M.Adj (ρ t) (ρ (t + 1))
  step : ∀ t, M.rotation.faceNext ⟨(ρ t, ρ (t + 1)), adj t⟩ = ⟨(ρ (t + 1), ρ (t + 2)), adj (t + 1)⟩
  inj : ∀ s t, s < r → t < r → ρ s = ρ t → s = t

variable {M}

/-- The ring dart at position `t`. -/
def ringDart {r : ℕ} {ρ : ℕ → Fin n} (R : RingFace M r ρ) (t : ℕ) : M.Dart :=
  ⟨(ρ t, ρ (t + 1)), R.adj t⟩

theorem ring_bd {r : ℕ} {ρ : ℕ → Fin n} (R : RingFace M r ρ) (t : ℕ) :
    bd M (ringDart R 0) t = ringDart R t := by
  induction t with
  | zero => rfl
  | succ t ih =>
    rw [bd_succ, ih]
    exact R.step t

theorem ring_rv {r : ℕ} {ρ : ℕ → Fin n} (R : RingFace M r ρ) (t : ℕ) :
    rv M (ringDart R 0) t = ρ t := by
  unfold rv; rw [ring_bd]; rfl

theorem ring_face_period {r : ℕ} {ρ : ℕ → Fin n} (R : RingFace M r ρ) :
    r = Function.minimalPeriod (⇑M.rotation.faceNext) (ringDart R 0) := by
  have hper : Function.IsPeriodicPt (⇑M.rotation.faceNext) r (ringDart R 0) := by
    change bd M (ringDart R 0) r = ringDart R 0
    rw [ring_bd]
    apply Dart.ext; apply Prod.ext
    · change ρ r = ρ 0
      rw [show r = 0 + r by omega]; exact R.per 0
    · change ρ (r + 1) = ρ (0 + 1)
      rw [show r + 1 = (0 + 1) + r by omega]; exact R.per (0 + 1)
  have hpos := hper.minimalPeriod_pos R.pos
  have hdvd := hper.minimalPeriod_dvd
  have hle := Nat.le_of_dvd R.pos hdvd
  by_contra hne
  have hlt : Function.minimalPeriod (⇑M.rotation.faceNext) (ringDart R 0) < r := by omega
  have hfix : bd M (ringDart R 0) (Function.minimalPeriod (⇑M.rotation.faceNext) (ringDart R 0)) =
      ringDart R 0 := Function.iterate_minimalPeriod
  rw [ring_bd] at hfix
  have := R.inj _ 0 hlt R.pos (congrArg (fun d : M.Dart => d.fst) hfix)
  omega

/-- **C1, disjoint colour pairs.** Kempe chains of disjoint colour pairs cannot join
alternating ring positions `i < j < k < l < r`. -/
theorem chains_noncrossing {r : ℕ} {ρ : ℕ → Fin n} (R : RingFace M r ρ) {h : Fin n}
    {c : Fin n → Fin 4} {a b a' b' : Fin 4}
    (hdisj : ∀ x : Fin 4, (x = a ∨ x = b) → (x = a' ∨ x = b') → False)
    {i j k l : ℕ} (hij : i < j) (hjk : j < k) (hkl : k < l) (hlr : l < r)
    (h1 : (pairGraph M.graph h c a b).Reachable (ρ i) (ρ k))
    (h2 : (pairGraph M.graph h c a' b').Reachable (ρ j) (ρ l)) : False := by
  classical
  obtain ⟨p⟩ := h1
  obtain ⟨q⟩ := h2
  let fp : pairGraph M.graph h c a b →g M.graph := ⟨id, fun e => e.1⟩
  let fq : pairGraph M.graph h c a' b' →g M.graph := ⟨id, fun e => e.1⟩
  have hk : ρ k = rv M (ringDart R 0) (i + (k - i)) := by
    rw [ring_rv]; congr 1; omega
  have hi : ρ i = rv M (ringDart R 0) i := (ring_rv R i).symm
  have hj : ρ j = rv M (ringDart R 0) j := (ring_rv R j).symm
  have hl : ρ l = rv M (ringDart R 0) l := (ring_rv R l).symm
  let p' : M.graph.Walk (rv M (ringDart R 0) i) (rv M (ringDart R 0) (i + (k - i))) :=
    ((p.map fp).copy hi hk)
  let q' : M.graph.Walk (rv M (ringDart R 0) j) (rv M (ringDart R 0) l) :=
    ((q.map fq).copy hj hl)
  have act_p : ∀ z ∈ p.support, c z = a ∨ c z = b := by
    intro z hz
    have hs : Active h c a b (ρ i) := by
      have hne : ρ i ≠ ρ k := fun e => absurd (R.inj i k (by omega) (by omega) e) (by omega)
      obtain ⟨u, hu⟩ := VacancyIcosahedral.first_step M.graph ⟨p⟩ hne
      exact hu.2.1
    exact (VacancyMobility.pair_walk_support M.graph p hs z hz).2
  have act_q : ∀ z ∈ q.support, c z = a' ∨ c z = b' := by
    intro z hz
    have hs : Active h c a' b' (ρ j) := by
      have hne : ρ j ≠ ρ l := fun e => absurd (R.inj j l (by omega) hlr e) (by omega)
      obtain ⟨u, hu⟩ := VacancyIcosahedral.first_step M.graph ⟨q⟩ hne
      exact hu.2.1
    exact (VacancyMobility.pair_walk_support M.graph q hs z hz).2
  apply face_alternating_walks_meet M (ringDart R 0) (ring_face_period R)
    (fun s t hs ht e => R.inj s t hs ht (by rwa [ring_rv, ring_rv] at e))
    hij (by omega : j < i + (k - i)) (by omega : i + (k - i) < l) hlr p' q'
  intro z hzq hzp
  have hzq' : z ∈ q.support := by
    simpa [q', Walk.support_copy, Walk.support_map, fq] using hzq
  have hzp' : z ∈ p.support := by
    simpa [p', Walk.support_copy, Walk.support_map, fp] using hzp
  exact hdisj (c z) (act_p z hzp') (act_q z hzq')

/-- **C1, one colour pair.** Two different components of one colour pair cannot join
alternating ring positions. -/
theorem chains_noncrossing_same {r : ℕ} {ρ : ℕ → Fin n} (R : RingFace M r ρ) {h : Fin n}
    {c : Fin n → Fin 4} {a b : Fin 4}
    {i j k l : ℕ} (hij : i < j) (hjk : j < k) (hkl : k < l) (hlr : l < r)
    (h1 : (pairGraph M.graph h c a b).Reachable (ρ i) (ρ k))
    (h2 : (pairGraph M.graph h c a b).Reachable (ρ j) (ρ l))
    (hne : ¬ (pairGraph M.graph h c a b).Reachable (ρ i) (ρ j)) : False := by
  classical
  obtain ⟨p⟩ := h1
  obtain ⟨q⟩ := h2
  let fp : pairGraph M.graph h c a b →g M.graph := ⟨id, fun e => e.1⟩
  have hk : ρ k = rv M (ringDart R 0) (i + (k - i)) := by
    rw [ring_rv]; congr 1; omega
  have hi : ρ i = rv M (ringDart R 0) i := (ring_rv R i).symm
  have hj : ρ j = rv M (ringDart R 0) j := (ring_rv R j).symm
  have hl : ρ l = rv M (ringDart R 0) l := (ring_rv R l).symm
  let p' := (p.map fp).copy hi hk
  let q' := (q.map fp).copy hj hl
  apply face_alternating_walks_meet M (ringDart R 0) (ring_face_period R)
    (fun s t hs ht e => R.inj s t hs ht (by rwa [ring_rv, ring_rv] at e))
    hij (by omega : j < i + (k - i)) (by omega : i + (k - i) < l) hlr p' q'
  intro z hzq hzp
  have hzq' : z ∈ q.support := by
    simpa [q', Walk.support_copy, Walk.support_map, fp] using hzq
  have hzp' : z ∈ p.support := by
    simpa [p', Walk.support_copy, Walk.support_map, fp] using hzp
  apply hne
  have r1 : (pairGraph M.graph h c a b).Reachable (ρ i) z := ⟨p.takeUntil z hzp'⟩
  have r2 : (pairGraph M.graph h c a b).Reachable (ρ j) z := ⟨q.takeUntil z hzq'⟩
  exact r1.trans r2.symm

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
