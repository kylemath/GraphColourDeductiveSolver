module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SideTriangle

/-!
# Lemma R\* in the four-connected core implies the Four Colour Theorem

`RStarCore` is the hand Lemma R\* (`MathReviewCleanToVHE.md` L5; audit re-derivation of
6 October, 13:25), stated for spherical maps with no isolated vertices:

> For every spherical triangulation `T` with a protected facial triangle `φ = p q r` such that
> * `T` is connected,
> * every face of `T` is a triangle (`Triangulated`),
> * `p q`, `q r`, `r p` are edges and `p q r` bounds a face (`Facial`),
> * every triangle of `T` bounds a face (`NoSep`: no separating triangle, the four-connected
>   core),
> * every vertex off `φ` has degree at least five,
>
> there is a vertex `v ∉ φ` of degree five such that every proper four-colouring of `T - v`
> reaches a colouring in which the five neighbours of `v` use at most three colours, by finitely
> many whole-component Kempe swaps of `T - v` (`PureClean T v`).

The vertices of `φ` may have any degree here; in the core class of the hand statement they
automatically have degree at least four, so the class quantified over is the hand class.

`four_color_of_core_Rstar`: `RStarCore` implies that every spherical map (in particular every
plane map, via `SphericalMap.ofPlaneMap`) is four-colourable. The proof relabels each relative
class member onto its non-isolated vertices (`supportTransport`) and applies
`four_color_of_RStarSupport` (link D: separating-triangle induction).
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyMobility VacancyIcosahedral VacancyCliqueLift

/-- **Lemma R\* for the four-connected relative-class core**, exactly as in the hand chain. -/
def RStarCore : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m) (p q r : Fin m), T.graph.Connected → T.Triangulated →
    T.Adj p q → T.Adj q r → T.Adj r p → Facial T p q r → NoSep T →
    (∀ x, x ≠ p → x ≠ q → x ≠ r → 5 ≤ T.graph.degree x) → CleanOff T p q r

section Transport
variable {n s : ℕ} (M : SphericalMap n) (i : M.graph.support ≃ Fin s)

theorem supportLabel_injective : Function.Injective (supportLabel M i) :=
  fun _ _ h => i.symm.injective (Subtype.ext h)

theorem supportLabel_apply (x : Fin n) (hx : x ∈ M.graph.support) :
    supportLabel M i (i ⟨x, hx⟩) = x := by
  simp [supportLabel]

theorem supportDart_next (d : (M.supportTransport i).Dart) :
    supportDartEquiv M i ((M.supportTransport i).rotation.next d) =
      M.rotation.next (supportDartEquiv M i d) := by
  change supportDartEquiv M i ((supportDartEquiv M i).symm
    (M.rotation.next (supportDartEquiv M i d))) = _
  exact Equiv.apply_symm_apply _ _

theorem nx_transport {u v w : Fin s} :
    Nx (M.supportTransport i) u v w ↔
      Nx M (supportLabel M i u) (supportLabel M i v) (supportLabel M i w) := by
  constructor
  · rintro ⟨h, e⟩
    refine ⟨h, ?_⟩
    have := congrArg (fun d : M.Dart => d.snd) (supportDart_next M i ⟨(u, v), h⟩)
    change supportLabel M i ((M.supportTransport i).rotation.next ⟨(u, v), h⟩).snd = _ at this
    exact this.symm.trans (by rw [e])
  · rintro ⟨h, e⟩
    refine ⟨h, supportLabel_injective M i ?_⟩
    have := congrArg (fun d : M.Dart => d.snd) (supportDart_next M i ⟨(u, v), h⟩)
    change supportLabel M i ((M.supportTransport i).rotation.next ⟨(u, v), h⟩).snd = _ at this
    rw [this]; exact e

theorem facial_transport {p q r : Fin s} :
    Facial (M.supportTransport i) p q r ↔
      Facial M (supportLabel M i p) (supportLabel M i q) (supportLabel M i r) := by
  unfold Facial
  rw [nx_transport, nx_transport]

theorem triangulated_transport (htri : M.Triangulated) : (M.supportTransport i).Triangulated := by
  intro d
  have semi : Function.Semiconj (supportDartEquiv M i) (M.supportTransport i).rotation.faceNext
      M.rotation.faceNext := fun a => supportRotation_faceNext M i a
  have period : (⇑(M.supportTransport i).rotation.faceNext)^[3] d = d := by
    apply (supportDartEquiv M i).injective
    have key := (semi.iterate_right 3) d
    have h := M.rotation.face_next_iterate_length (supportDartEquiv M i d)
    rw [show M.rotation.faceLength (M.rotation.faceOf _) = 3 from htri _] at h
    exact key.trans h
  have hfix : (M.supportTransport i).rotation.faceNext d ≠ d := by
    intro he
    have h1 := congrArg (fun a : (M.supportTransport i).Dart => a.fst) he
    simp only [RotationSystem.face_next_fst] at h1
    exact d.adj.ne h1.symm
  rw [(M.supportTransport i).rotation.face_length_eq_period]
  exact Function.minimalPeriod_eq_prime (p := 3) (hp := ⟨Nat.prime_three⟩) period hfix

theorem degree_transport (x : Fin s) :
    (M.supportTransport i).graph.degree x = M.graph.degree (supportLabel M i x) :=
  support_degree M i x

theorem reach_transport {a b : Fin n} (ha : a ∈ M.graph.support) (hb : b ∈ M.graph.support)
    (h : M.graph.Reachable a b) :
    (M.supportTransport i).graph.Reachable (i ⟨a, ha⟩) (i ⟨b, hb⟩) := by
  obtain ⟨W⟩ := h
  induction W with
  | nil => exact Reachable.refl _
  | @cons a a' b hadj W ih =>
    have ha' : a' ∈ M.graph.support := hadj.mem_support_right
    have hstep : (M.supportTransport i).graph.Adj (i ⟨a, ha⟩) (i ⟨a', ha'⟩) := by
      change M.graph.Adj (supportLabel M i _) (supportLabel M i _)
      rw [supportLabel_apply, supportLabel_apply]; exact hadj
    exact hstep.reachable.trans (ih ha' hb)

/-- Pure Kempe paths of the relabelled map pull back to the original map. -/
theorem purePath_pullback {v' : Fin s} {k : ℕ} {c' d' : Fin s → Fin 4}
    (path : PurePath (M.supportTransport i).graph v' k c' d') {cT : Fin n → Fin 4}
    (agree : ∀ x', cT (supportLabel M i x') = c' x') :
    ∃ dT, PurePath M.graph (supportLabel M i v') k cT dT ∧
      ∀ x', dT (supportLabel M i x') = d' x' := by
  classical
  induction path generalizing cT with
  | nil c => exact ⟨cT, .nil _, agree⟩
  | @cons k c c1 d step rest ih =>
    obtain ⟨a, b, S', hab, ⟨s', act', mem'⟩, rfl⟩ := step
    set L := supportLabel M i
    set S : Set (Fin n) := {x | ∃ x', x' ∈ S' ∧ L x' = x}
    have hL := supportLabel_injective M i
    have actT : Active (L v') cT a b (L s') :=
      ⟨fun h => act'.1 (hL h), by rw [agree]; exact act'.2⟩
    -- relabelled pair walks map forward
    have fwd : ∀ x', (pairGraph (M.supportTransport i).graph v' c a b).Reachable s' x' →
        (pairGraph M.graph (L v') cT a b).Reachable (L s') (L x') := by
      intro x' hx'
      let φ : pairGraph (M.supportTransport i).graph v' c a b →g pairGraph M.graph (L v') cT a b :=
        ⟨L, fun {u w} e => ⟨e.1, ⟨fun h => e.2.1.1 (hL h), by rw [agree]; exact e.2.1.2⟩,
          ⟨fun h => e.2.2.1 (hL h), by rw [agree]; exact e.2.2.2⟩⟩⟩
      exact hx'.map φ
    -- original pair walks from a support vertex stay in the support
    have bwd : ∀ x, (pairGraph M.graph (L v') cT a b).Reachable (L s') x →
        ∃ x', L x' = x ∧ (pairGraph (M.supportTransport i).graph v' c a b).Reachable s' x' := by
      intro x hx
      refine reachable_invariant (H := pairGraph M.graph (L v') cT a b)
        (P := fun x => ∃ x', L x' = x ∧
          (pairGraph (M.supportTransport i).graph v' c a b).Reachable s' x') ?_
        ⟨s', rfl, Reachable.refl _⟩ hx
      rintro u w e ⟨u', rfl, hu'⟩
      have hw : w ∈ M.graph.support := e.1.mem_support_right
      have hLw : L (i ⟨w, hw⟩) = w := supportLabel_apply M i w hw
      have adjT : (M.supportTransport i).graph.Adj u' (i ⟨w, hw⟩) := by
        change M.graph.Adj (L u') (L (i ⟨w, hw⟩)); rw [hLw]; exact e.1
      have actu : Active v' c a b u' :=
        ⟨fun h => e.2.1.1 (congrArg L h), by rw [← agree]; exact e.2.1.2⟩
      have actw : Active v' c a b (i ⟨w, hw⟩) :=
        ⟨fun h => e.2.2.1 (hLw.symm.trans (congrArg L h)), by rw [← agree, hLw]; exact e.2.2.2⟩
      have step : (pairGraph (M.supportTransport i).graph v' c a b).Adj u' (i ⟨w, hw⟩) :=
        ⟨adjT, actu, actw⟩
      exact ⟨i ⟨w, hw⟩, hLw, hu'.trans step.reachable⟩
    have wholeT : Whole M.graph (L v') cT a b S := by
      refine ⟨L s', actT, fun x => ⟨?_, ?_⟩⟩
      · rintro ⟨x', hx', rfl⟩
        exact fwd x' ((mem' x').mp hx')
      · intro hx
        obtain ⟨x', rfl, hr⟩ := bwd x hx
        exact ⟨x', (mem' x').mpr hr, rfl⟩
    have agree' : ∀ x', swap cT a b S (L x') = swap c a b S' x' := by
      intro x'
      by_cases hx' : x' ∈ S'
      · rw [swap_in (show L x' ∈ S from ⟨x', hx', rfl⟩), swap_in hx', agree]
      · have : L x' ∉ S := by
          rintro ⟨y', hy', hxy⟩
          exact hx' (hL hxy ▸ hy')
        rw [swap_out this, swap_out hx', agree]
    obtain ⟨dT, pT, agT⟩ := ih agree'
    exact ⟨dT, .cons ⟨a, b, S, hab, wholeT, rfl⟩ pT, agT⟩

/-- Pure-cleanness pulls back from the relabelled map. -/
theorem pureClean_pullback {v' : Fin s} (h : PureClean (M.supportTransport i) v') :
    PureClean M (supportLabel M i v') := by
  classical
  intro g hg
  set L := supportLabel M i
  have hL := supportLabel_injective M i
  have hg' : ProperOff (M.supportTransport i).graph v' (fun x' => g (L x')) :=
    fun x y e hx hy => hg e (fun h => hx (hL h)) (fun h => hy (hL h))
  obtain ⟨m, k, hk, d', path, ⟨col, hcol⟩⟩ := h _ hg'
  obtain ⟨dT, pT, agT⟩ := purePath_pullback M i path (fun _ => rfl)
  refine ⟨m, k, hk, dT, pT, col, fun y hy e => ?_⟩
  have hys : y ∈ M.graph.support := hy.mem_support_right
  have hLy : L (i ⟨y, hys⟩) = y := supportLabel_apply M i y hys
  have hadj : (M.supportTransport i).graph.Adj v' (i ⟨y, hys⟩) := by
    change M.graph.Adj (L v') (L (i ⟨y, hys⟩)); rw [hLy]; exact hy
  have hLy' : M.supportLabel i (i ⟨y, hys⟩) = y := hLy
  exact hcol hadj (by rw [← agT, hLy']; exact e)

end Transport

/-- The hand form of R\* gives its support form. -/
theorem rStarSupport_of_core (hR : RStarCore) : RStarSupport := by
  classical
  intro m T p q r hrel hns
  obtain ⟨htri, hpq, hqr, hrp, hfac, hdeg, hconn⟩ := hrel
  let i := T.supportEquivFin
  set s := Nat.card T.graph.support
  let TT := T.supportTransport i
  have hL := supportLabel_injective T i
  have hp : p ∈ T.graph.support := hpq.mem_support_left
  have hq : q ∈ T.graph.support := hqr.mem_support_left
  have hr : r ∈ T.graph.support := hrp.mem_support_left
  have Lp : supportLabel T i (i ⟨p, hp⟩) = p := supportLabel_apply T i p hp
  have Lq : supportLabel T i (i ⟨q, hq⟩) = q := supportLabel_apply T i q hq
  have Lr : supportLabel T i (i ⟨r, hr⟩) = r := supportLabel_apply T i r hr
  have hconnT : TT.graph.Connected := by
    have : Nonempty (Fin s) := ⟨i ⟨p, hp⟩⟩
    refine ⟨fun x' y' => ?_⟩
    have hx := (i.symm x').property
    have hy := (i.symm y').property
    have r := reach_transport T i hx hy (hconn _ _
      ((T.graph.degree_pos_iff_mem_support _).mpr hx)
      ((T.graph.degree_pos_iff_mem_support _).mpr hy))
    simpa using r
  have hadjT : ∀ {u v : Fin m} (hu : u ∈ T.graph.support) (hv : v ∈ T.graph.support),
      T.Adj u v → TT.Adj (i ⟨u, hu⟩) (i ⟨v, hv⟩) := by
    intro u v hu hv h
    change T.graph.Adj (supportLabel T i _) (supportLabel T i _)
    rw [supportLabel_apply, supportLabel_apply]; exact h
  have hfacT : Facial TT (i ⟨p, hp⟩) (i ⟨q, hq⟩) (i ⟨r, hr⟩) := by
    rw [facial_transport, Lp, Lq, Lr]; exact hfac
  have hnsT : NoSep TT := by
    intro x y z hxy hyz hzx
    rw [facial_transport]
    exact hns _ _ _ hxy hyz hzx
  have hdegT : ∀ x', x' ≠ i ⟨p, hp⟩ → x' ≠ i ⟨q, hq⟩ → x' ≠ i ⟨r, hr⟩ →
      5 ≤ TT.graph.degree x' := by
    intro x' h1 h2 h3
    rw [degree_transport]
    have n1 : supportLabel T i x' ≠ p := fun h => h1 (hL (h.trans Lp.symm))
    have n2 : supportLabel T i x' ≠ q := fun h => h2 (hL (h.trans Lq.symm))
    have n3 : supportLabel T i x' ≠ r := fun h => h3 (hL (h.trans Lr.symm))
    have hpos : 0 < T.graph.degree (supportLabel T i x') :=
      (T.graph.degree_pos_iff_mem_support _).mpr (i.symm x').property
    rcases hdeg _ n1 n2 n3 with h | h
    · omega
    · exact h
  obtain ⟨v', h1, h2, h3, h5, hvc⟩ := hR s TT _ _ _ hconnT (triangulated_transport T i htri)
    (hadjT hp hq hpq) (hadjT hq hr hqr) (hadjT hr hp hrp) hfacT hnsT hdegT
  refine ⟨supportLabel T i v', fun h => h1 (hL (h.trans Lp.symm)),
    fun h => h2 (hL (h.trans Lq.symm)), fun h => h3 (hL (h.trans Lr.symm)), ?_,
    pureClean_pullback T i hvc⟩
  rw [← degree_transport]; exact h5

/-- **Lemma R\* in the four-connected core implies the Four Colour Theorem.** If `RStarCore`
holds (see the module docstring for the exact statement), every spherical map is
four-colourable. -/
theorem four_color_of_core_Rstar (hR : RStarCore) {n : ℕ} (M : SphericalMap n) :
    M.graph.Colorable 4 :=
  four_color_of_RStarSupport (rStarSupport_of_core hR) M

/-- The same for the library's plane maps. -/
theorem four_color_of_core_Rstar_planeMap (hR : RStarCore) {n : ℕ} (M : PlaneMap n) :
    M.graph.Colorable 4 :=
  four_color_of_core_Rstar hR (SphericalMap.ofPlaneMap M)

end SimpleGraph.SphericalMap

#print SimpleGraph.SphericalMap.RStarCore
#check @SimpleGraph.SphericalMap.four_color_of_core_Rstar
#check @SimpleGraph.SphericalMap.four_color_of_core_Rstar_planeMap
#print axioms SimpleGraph.SphericalMap.four_color_of_core_Rstar
#print axioms SimpleGraph.SphericalMap.four_color_of_core_Rstar_planeMap

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
