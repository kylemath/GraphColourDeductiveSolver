module
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancySlide
public import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
public import Mathlib.Logic.Equiv.Basic
public import Mathlib.Tactic

@[expose] public section
namespace SimpleGraph.VacancyShortFillTeamB
open VacancySlide
variable {V C : Type*} (G : SimpleGraph V)

/-- A target omits an actual palette colour from the full hole link. -/
def Target (r : V) (c : V → C) : Prop := ∃ x, ∀ ⦃v⦄, G.Adj r v → c v ≠ x

/-- The actual bichromatic graph in the deletion. Other vertices are isolated. -/
def pairGraph (r : V) (c : V → C) (a b : C) : SimpleGraph V where
  Adj u v := G.Adj u v ∧ u ≠ r ∧ v ≠ r ∧ (c u = a ∨ c u = b) ∧ (c v = a ∨ c v = b)
  symm := ⟨fun _ _ h => ⟨h.1.symm, h.2.2.1, h.2.1, h.2.2.2.2, h.2.2.2.1⟩⟩
  loopless := ⟨fun _ h => h.1.ne rfl⟩

noncomputable def swapComponent (r : V) (c : V → C) (a b : C) (s : V) : V → C :=
  by
    classical
    exact fun v => if (pairGraph G r c a b).Reachable s v then Equiv.swap a b (c v) else c v

def KempeStep (r : V) (c d : V → C) : Prop :=
  ProperOff G r c ∧ ∃ a b s, a ≠ b ∧ s ≠ r ∧ (c s = a ∨ c s = b) ∧
    d = swapComponent G r c a b s

theorem reachable_singleton {H : SimpleGraph V} {s v : V}
    (hs : ∀ w, ¬ H.Adj s w) (h : H.Reachable s v) : v = s := by
  rcases h with ⟨p⟩
  cases p with
  | nil => rfl
  | cons h _ => exact (hs _ h).elim

theorem terminal_component [DecidableEq V] {r u : V} {c : V → C} {x : C}
    (hc : ProperOff G r c) (hru : G.Adj r u)
    (hx : ∀ ⦃v⦄, G.Adj u v → slide r u c v ≠ x) :
    ∀ v, (pairGraph G r c (c u) x).Reachable u v ↔ v = u := by
  classical
  intro v
  constructor
  · apply reachable_singleton
    intro w hw
    have hwu : c w ≠ c u := (hc hw.1 hru.ne.symm hw.2.2.1).symm
    have hwx : c w ≠ x := by
      have h := hx hw.1
      rw [slide_away r u c hw.2.2.1] at h
      exact h
    exact hw.2.2.2.2.elim hwu hwx
  · rintro rfl
    exact .rfl

/-- Terminal-slide elimination produces one actual whole-component Kempe swap. -/
theorem terminal_slide [DecidableEq V] {r u : V} {c : V → C}
    (hc : ProperOff G r c) (hru : G.Adj r u) (hu : UniqueAt G r u c)
    (ht : Target G u (slide r u c)) :
    ∃ d, KempeStep G r c d ∧ Target G r d := by
  classical
  obtain ⟨x, hx⟩ := ht
  have hne : c u ≠ x := by
    have h := hx hru.symm
    simpa only [slide_at] using h
  let d := swapComponent G r c (c u) x u
  refine ⟨d, ⟨hc, c u, x, u, hne, hru.ne.symm, Or.inl rfl, rfl⟩, c u, ?_⟩
  intro v hrv
  by_cases hvu : v = u
  · subst v
    simp [d, swapComponent, Equiv.swap_apply_left, hne.symm]
  · have hn : ¬ (pairGraph G r c (c u) x).Reachable u v := by
      rw [terminal_component G hc hru hx v]
      exact hvu
    simp only [d, swapComponent, ite_eq_right hn]
    intro heq
    exact hvu (hu hrv heq)

theorem reachable_closed {H : SimpleGraph V} {P : V → Prop} {s v : V}
    (hs : P s) (hclosed : ∀ ⦃x y⦄, H.Adj x y → P x → P y)
    (hr : H.Reachable s v) : P v := by
  rcases hr with ⟨p⟩
  induction p with
  | nil => exact hs
  | @cons x y z h p ih => exact ih (hclosed h hs)

theorem chain_off {r s v : V} {c : V → C} {a b : C}
    (hs : s ≠ r) (hr : (pairGraph G r c a b).Reachable s v) : v ≠ r := by
  exact reachable_closed (H := pairGraph G r c a b) (P := fun t => t ≠ r) (s := s) hs (fun {_ _} h _ => h.2.2.1) hr

theorem chain_colours {r s v : V} {c : V → C} {a b : C}
    (hs : c s = a ∨ c s = b) (hr : (pairGraph G r c a b).Reachable s v) :
    c v = a ∨ c v = b := by
  exact reachable_closed (H := pairGraph G r c a b) (P := fun t => c t = a ∨ c t = b) (s := s) hs (fun {_ _} h _ => h.2.2.2.2) hr

theorem chain_extend {r s v w : V} {c : V → C} {a b : C}
    (hv : (pairGraph G r c a b).Reachable s v)
    (hvw : G.Adj v w) (hvr : v ≠ r) (hwr : w ≠ r)
    (hcv : c v = a ∨ c v = b) (hcw : c w = a ∨ c w = b) :
    (pairGraph G r c a b).Reachable s w :=
  hv.trans (SimpleGraph.Adj.reachable ⟨hvw,hvr,hwr,hcv,hcw⟩)

theorem properOff_swap {r s : V} {c : V → C} {a b : C}
    (hc : ProperOff G r c) (_hs : s ≠ r) (hcol : c s = a ∨ c s = b) :
    ProperOff G r (swapComponent G r c a b s) := by
  classical
  intro v w hvw hvr hwr
  let K := fun t => (pairGraph G r c a b).Reachable s t
  have cross {x y : V} (hxy : G.Adj x y) (hxr : x ≠ r) (hyr : y ≠ r)
      (hx : K x) (hy : ¬ K y) : c y ≠ a ∧ c y ≠ b := by
    have hxcol := chain_colours G hcol hx
    constructor
    · intro heq
      exact hy (chain_extend G hx hxy hxr hyr hxcol (Or.inl heq))
    · intro heq
      exact hy (chain_extend G hx hxy hxr hyr hxcol (Or.inr heq))
  by_cases hv : K v <;> by_cases hw : K w <;> dsimp [K] at hv hw
  · simp only [swapComponent, ite_eq_left hv, ite_eq_left hw]
    exact (Equiv.swap a b).injective.ne (hc hvw hvr hwr)
  · have hwcol := cross hvw hvr hwr hv hw
    simp only [swapComponent, ite_eq_left hv, ite_eq_right hw]
    rw [← Equiv.swap_apply_of_ne_of_ne hwcol.1 hwcol.2]
    exact (Equiv.swap a b).injective.ne (hc hvw hvr hwr)
  · have hvcol := cross hvw.symm hwr hvr hw hv
    simp only [swapComponent, ite_eq_right hv, ite_eq_left hw]
    rw [← Equiv.swap_apply_of_ne_of_ne hvcol.1 hvcol.2]
    exact (Equiv.swap a b).injective.ne (hc hvw hvr hwr)
  · simp only [swapComponent, ite_eq_right hv, ite_eq_right hw]
    exact hc hvw hvr hwr

theorem KempeStep.proper {r : V} {c d : V → C} (h : KempeStep G r c d) :
    ProperOff G r d := by
  obtain ⟨hc,a,b,s,hab,hs,hcol,rfl⟩ := h
  exact properOff_swap G hc hs hcol

/-- A component through the unique link colour fills if it misses every opposite-colour link vertex. -/
theorem component_fill {r u : V} {c : V → C} {rho : C}
    (hc : ProperOff G r c) (hru : G.Adj r u) (hu : UniqueAt G r u c)
    (hne : c u ≠ rho)
    (havoid : ∀ ⦃v⦄, G.Adj r v → c v = rho →
      ¬ (pairGraph G r c (c u) rho).Reachable u v) :
    ∃ d, KempeStep G r c d ∧ Target G r d := by
  classical
  refine ⟨swapComponent G r c (c u) rho u,
    ⟨hc,c u,rho,u,hne,hru.ne.symm,Or.inl rfl,rfl⟩,c u,?_⟩
  intro v hrv
  by_cases hv : (pairGraph G r c (c u) rho).Reachable u v
  · simp only [swapComponent, ite_eq_left hv]
    intro heq
    have hvcol : c v = rho := by
      have hh := (Equiv.swap_apply_eq_iff).mp heq
      simpa using hh
    exact havoid hrv hvcol hv
  · simp only [swapComponent, ite_eq_right hv]
    intro heq
    have hvu := hu hrv heq
    subst v
    exact hv .rfl


theorem pairGraph_slide_edge [DecidableEq V] {r u v w : V} {c : V → C} {a b : C}
    (h : (pairGraph G r c a b).Adj v w) (hv : v ≠ u) (hw : w ≠ u) :
    (pairGraph G u (slide r u c) a b).Adj v w := by
  refine ⟨h.1,hv,hw,?_,?_⟩
  · rw [slide_away r u c h.2.1]
    exact h.2.2.2.1
  · rw [slide_away r u c h.2.2.1]
    exact h.2.2.2.2

/-- Every SK target whose pair contains the slid colour already has a one-swap fill. -/
theorem sk_pair_fill [DecidableEq V] {r u s : V} {c : V → C} {rho : C}
    (hc : ProperOff G r c) (hru : G.Adj r u) (hu : UniqueAt G r u c)
    (hne : c u ≠ rho) (hs : s ≠ u)
    (hsc : slide r u c s = c u ∨ slide r u c s = rho)
    (ht : Target G u (swapComponent G u (slide r u c) (c u) rho s)) :
    ∃ d, KempeStep G r c d ∧ Target G r d := by
  classical
  obtain ⟨x,hx⟩ := ht
  let K := fun v => (pairGraph G u (slide r u c) (c u) rho).Reachable s v
  by_cases hxpair : x = c u ∨ x = rho
  · by_cases hkr : K r
    · have hxr : x ≠ rho := by
        have hh := hx hru.symm
        simpa [swapComponent, K, hkr, slide_at] using hh.symm
      have hxs : x = c u := hxpair.resolve_right hxr
      subst x
      have first {w : V} (huw : G.Adj u w) (hwr : w ≠ r) (hwcol : c w = rho) : ¬ K w := by
        intro hkw
        have hh := hx huw
        have hsw : slide r u c w = rho := by rw [slide_away r u c hwr]; exact hwcol
        simp [swapComponent, K, hkw, hsw] at hh
      have P : ∀ v, (pairGraph G r c (c u) rho).Reachable u v → v = u ∨ ¬ K v := by
        intro v hv
        apply reachable_closed (H := pairGraph G r c (c u) rho)
          (P := fun t => t = u ∨ ¬ K t) (s := u) (Or.inl rfl) ?_ hv
        intro z w hzw hp
        by_cases hwu : w = u
        · exact Or.inl hwu
        right
        rcases hp with rfl | hz
        · have hwcol : c w = rho := hzw.2.2.2.2.resolve_left (hc hzw.1 hru.ne.symm hzw.2.2.1).symm
          exact first hzw.1 hzw.2.2.1 hwcol
        · by_cases hzu : z = u
          · subst z
            have hwcol : c w = rho := hzw.2.2.2.2.resolve_left (hc hzw.1 hru.ne.symm hzw.2.2.1).symm
            exact first hzw.1 hzw.2.2.1 hwcol
          · intro hkw
            have hzedge := pairGraph_slide_edge G hzw hzu hwu
            exact hz (hkw.trans hzedge.symm.reachable)
      apply component_fill G hc hru hu hne
      intro v hrv hcv hjv
      have hvu : v ≠ u := by intro heq; subst v; exact hne hcv
      have hkv : K v := by
        have hdv : slide r u c v = rho := by rw [slide_away r u c hrv.ne.symm]; exact hcv
        exact chain_extend G hkr hrv hru.ne hvu (Or.inl (slide_at _ _ _)) (Or.inr hdv)
      exact (P v hjv).resolve_left hvu hkv
    · have hxs : x ≠ c u := by
        have hh := hx hru.symm
        simpa [swapComponent, K, hkr, slide_at] using hh.symm
      have hxr : x = rho := hxpair.resolve_left hxs
      subst x
      have first {w : V} (huw : G.Adj u w) (hwr : w ≠ r) (hwcol : c w = rho) : K w := by
        by_contra hkw
        have hh := hx huw
        have hsw : slide r u c w = rho := by rw [slide_away r u c hwr]; exact hwcol
        simp [swapComponent, K, hkw, hsw] at hh
      have P : ∀ v, (pairGraph G r c (c u) rho).Reachable u v → v = u ∨ K v := by
        intro v hv
        apply reachable_closed (H := pairGraph G r c (c u) rho)
          (P := fun t => t = u ∨ K t) (s := u) (Or.inl rfl) ?_ hv
        intro z w hzw hp
        by_cases hwu : w = u
        · exact Or.inl hwu
        right
        rcases hp with rfl | hz
        · have hwcol : c w = rho := hzw.2.2.2.2.resolve_left (hc hzw.1 hru.ne.symm hzw.2.2.1).symm
          exact first hzw.1 hzw.2.2.1 hwcol
        · have hzu : z ≠ u := chain_off G hs hz
          exact hz.trans (pairGraph_slide_edge G hzw hzu hwu).reachable
      apply component_fill G hc hru hu hne
      intro v hrv hcv hjv
      have hvu : v ≠ u := by intro heq; subst v; exact hne hcv
      have hkv := (P v hjv).resolve_left hvu
      have hdv : slide r u c v = rho := by rw [slide_away r u c hrv.ne.symm]; exact hcv
      exact hkr (chain_extend G hkv hrv.symm hvu hru.ne (Or.inr hdv) (Or.inl (slide_at _ _ _)))
  · push Not at hxpair
    apply terminal_slide G hc hru hu
    refine ⟨x,?_⟩
    intro v huv hvx
    apply hx huv
    simp [swapComponent,hvx,Equiv.swap_apply_of_ne_of_ne hxpair.1 hxpair.2]


theorem pairGraph_symm (r : V) (c : V → C) (a b : C) :
    pairGraph G r c a b = pairGraph G r c b a := by
  ext v w
  simp only [pairGraph, or_comm]

theorem swapComponent_symm (r : V) (c : V → C) (a b : C) (s : V) :
    swapComponent G r c a b s = swapComponent G r c b a s := by
  classical
  funext v
  simp only [swapComponent, pairGraph_symm G r c a b, Equiv.swap_comm a b]

theorem pairGraph_slide_avoids [DecidableEq V] {r u : V} {c : V → C} {a b : C}
    (ha : c u ≠ a) (hb : c u ≠ b) :
    pairGraph G u (slide r u c) a b = pairGraph G r c a b := by
  ext v w
  by_cases hvr : v = r <;> by_cases hwr : w = r <;>
    by_cases hvu : v = u <;> by_cases hwu : w = u <;>
    simp_all [pairGraph, slide]

theorem swapComponent_fixed {r s v : V} {c : V → C} {a b : C}
    (ha : c v ≠ a) (hb : c v ≠ b) : swapComponent G r c a b s v = c v := by
  classical
  simp [swapComponent,Equiv.swap_apply_of_ne_of_ne ha hb]

theorem swapComponent_eq_other {r s v : V} {c : V → C} {a b x : C}
    (ha : x ≠ a) (hb : x ≠ b) :
    swapComponent G r c a b s v = x ↔ c v = x := by
  classical
  by_cases h : (pairGraph G r c a b).Reachable s v
  · simp only [swapComponent,ite_eq_left h,Equiv.swap_apply_eq_iff,
      Equiv.swap_apply_of_ne_of_ne ha hb]
  · simp only [swapComponent,ite_eq_right h]

theorem swapComponent_slide_commute [DecidableEq V] {r u s : V} {c : V → C} {a b : C}
    (ha : c u ≠ a) (hb : c u ≠ b) :
    slide r u (swapComponent G r c a b s) =
      swapComponent G u (slide r u c) a b s := by
  classical
  funext v
  by_cases hv : v = r
  · subst v
    rw [slide_at,swapComponent_fixed G ha hb]
    unfold swapComponent
    rw [slide_at]
    simp [Equiv.swap_apply_of_ne_of_ne ha hb]
  · rw [slide_away r u _ hv]
    simp only [swapComponent,pairGraph_slide_avoids G ha hb,slide_away r u c hv]

/-- Any SK target has a fixed-hole Kempe target within two moves. -/
theorem sk_fill [DecidableEq V] {r u : V} {c e : V → C}
    (hc : ProperOff G r c) (hru : G.Adj r u) (hu : UniqueAt G r u c)
    (hk : KempeStep G u (slide r u c) e) (ht : Target G u e) :
    ∃ d, Target G r d ∧ (KempeStep G r c d ∨
      ∃ f, KempeStep G r c f ∧ KempeStep G r f d) := by
  classical
  obtain ⟨hd,a,b,s,hab,hs,hsc,rfl⟩ := hk
  by_cases ha : c u = a
  · subst a
    obtain ⟨d,hk,ht⟩ := sk_pair_fill G hc hru hu hab hs hsc ht
    exact ⟨d,ht,Or.inl hk⟩
  · by_cases hb : c u = b
    · subst b
      rw [swapComponent_symm G u (slide r u c) a (c u) s] at ht
      obtain ⟨d,hk,ht⟩ := sk_pair_fill G hc hru hu hab.symm hs hsc.symm ht
      exact ⟨d,ht,Or.inl hk⟩
    · let f := swapComponent G r c a b s
      have hsr : s ≠ r := by
        intro heq
        subst s
        simp only [slide_at] at hsc
        exact hsc.elim ha hb
      have hsc' : c s = a ∨ c s = b := by
        rwa [slide_away r u c hsr] at hsc
      have hkf : KempeStep G r c f := ⟨hc,a,b,s,hab,hsr,hsc',rfl⟩
      have huf : UniqueAt G r u f := by
        intro v hrv heq
        have huq : f u = c u := swapComponent_fixed G ha hb
        rw [huq] at heq
        exact hu hrv ((swapComponent_eq_other G ha hb).mp heq)
      have htt : Target G u (slide r u f) := by
        rw [swapComponent_slide_commute G ha hb]
        exact ht
      obtain ⟨d,hkd,htd⟩ := terminal_slide G hkf.proper hru huf htt
      exact ⟨d,htd,Or.inr ⟨f,hkf,hkd⟩⟩


/-- A path of actual whole-component swaps, with the hole fixed. -/
inductive PurePath (r : V) : (V → C) → (V → C) → ℕ → Prop
  | nil (c) : PurePath r c c 0
  | cons {c d e n} : KempeStep G r c d → PurePath r d e n → PurePath r c e (n+1)

def PureFillWithin (r : V) (c : V → C) (n : ℕ) : Prop :=
  ∃ k, k ≤ n ∧ ∃ d, PurePath G r c d k ∧ Target G r d

inductive MixedStep [DecidableEq V] : (V × (V → C)) → (V × (V → C)) → Prop
  | kempe {r c d} : KempeStep G r c d → MixedStep (r,c) (r,d)
  | slide {r u c} : ProperOff G r c → G.Adj r u → UniqueAt G r u c →
      MixedStep (r,c) (u,VacancySlide.slide r u c)

inductive MixedPath [DecidableEq V] : (V × (V → C)) → (V × (V → C)) → ℕ → Prop
  | nil (s) : MixedPath s s 0
  | cons {s t w n} : MixedStep G s t → MixedPath t w n → MixedPath s w (n+1)

theorem one_step_fill [DecidableEq V] {r : V} {c : V → C} {t : V × (V → C)}
    (hs : MixedStep G (r,c) t) (ht : Target G t.1 t.2) : PureFillWithin G r c 1 := by
  cases hs with
  | kempe hk => exact ⟨1,le_rfl,_,PurePath.cons hk (PurePath.nil _),ht⟩
  | slide hc hru hu =>
    obtain ⟨d,hk,hd⟩ := terminal_slide G hc hru hu ht
    exact ⟨1,le_rfl,d,PurePath.cons hk (PurePath.nil _),hd⟩

theorem sk_fillWithin [DecidableEq V] {r u : V} {c e : V → C}
    (hc : ProperOff G r c) (hru : G.Adj r u) (hu : UniqueAt G r u c)
    (hk : KempeStep G u (slide r u c) e) (ht : Target G u e) :
    PureFillWithin G r c 2 := by
  obtain ⟨d,hd,hpath⟩ := sk_fill G hc hru hu hk ht
  rcases hpath with hk | ⟨f,hkf,hkd⟩
  · exact ⟨1,by omega,d,PurePath.cons hk (PurePath.nil _),hd⟩
  · exact ⟨2,le_rfl,d,PurePath.cons hkf (PurePath.cons hkd (PurePath.nil _)),hd⟩

/-- KK/KS follow by terminal elimination; SS reduces to SK at its second slide. -/
theorem two_step_fill [DecidableEq V] {r : V} {c : V → C}
    {t w : V × (V → C)} (hs : MixedStep G (r,c) t) (hs' : MixedStep G t w)
    (ht : Target G w.1 w.2) : PureFillWithin G r c 2 := by
  cases hs with
  | kempe hk =>
    obtain ⟨k,hkbound,d,hp,hd⟩ := one_step_fill G hs' ht
    exact ⟨k+1,by omega,d,PurePath.cons hk hp,hd⟩
  | slide hc hru hu =>
    cases hs' with
    | kempe hk => exact sk_fillWithin G hc hru hu hk ht
    | slide hc' huv hu' =>
      obtain ⟨d,hk,hd⟩ := terminal_slide G hc' huv hu' ht
      exact sk_fillWithin G hc hru hu hk hd

/-- A nonminimal mixed path of length at most two has a pure replacement of no greater length. -/
theorem short_fill [DecidableEq V] {r : V} {c : V → C} {t : V × (V → C)} {n : ℕ}
    (hp : MixedPath G (r,c) t n) (hn : n ≤ 2) (ht : Target G t.1 t.2) :
    PureFillWithin G r c n := by
  cases hp with
  | nil => exact ⟨0,le_rfl,c,PurePath.nil _,ht⟩
  | @cons t₀ t₁ t₂ k hs hp =>
    cases hp with
    | nil => exact one_step_fill G hs ht
    | @cons s₀ s₁ s₂ j hs' hp' =>
      have hj : j = 0 := by omega
      subst j
      cases hp' with
      | nil => exact two_step_fill G hs hs' ht

theorem PurePath.toMixed [DecidableEq V] {r : V} {c d : V → C} {n : ℕ}
    (hp : PurePath G r c d n) : MixedPath G (r,c) (r,d) n := by
  induction hp with
  | nil => exact MixedPath.nil _
  | cons hk hp ih => exact MixedPath.cons (MixedStep.kempe hk) ih

def MixedMinimum [DecidableEq V] (r : V) (c : V → C) (n : ℕ) : Prop :=
  (∃ t, MixedPath G (r,c) t n ∧ Target G t.1 t.2) ∧
    ∀ k t, MixedPath G (r,c) t k → Target G t.1 t.2 → n ≤ k

def PureMinimum (r : V) (c : V → C) (n : ℕ) : Prop :=
  (∃ d, PurePath G r c d n ∧ Target G r d) ∧
    ∀ k d, PurePath G r c d k → Target G r d → n ≤ k

/-- Equality is asserted for minimum distances, not arbitrary padded paths. -/
theorem short_minimum_eq [DecidableEq V] {r : V} {c : V → C} {ell kappa : ℕ}
    (hm : MixedMinimum G r c ell) (hk : PureMinimum G r c kappa) (hl : ell ≤ 2) :
    kappa = ell := by
  obtain ⟨t,hp,ht⟩ := hm.1
  obtain ⟨k,hkl,d,hkd,hdt⟩ := short_fill G hp hl ht
  have hkell : kappa ≤ ell := le_trans (hk.2 k d hkd hdt) hkl
  obtain ⟨f,hpf,hft⟩ := hk.1
  have hellk : ell ≤ kappa := hm.2 kappa (r,f) hpf.toMixed hft
  exact le_antisymm hkell hellk


theorem PurePath.proper {r : V} {c d : V → C} {n : ℕ}
    (hp : PurePath G r c d n) (hc : ProperOff G r c) : ProperOff G r d := by
  induction hp with
  | nil => exact hc
  | cons hk hp ih => exact ih hk.proper

/-- The bounded replacement ends in an actual proper deletion colouring. -/
theorem short_fill_proper [DecidableEq V] {r : V} {c : V → C}
    {t : V × (V → C)} {n : ℕ} (hc : ProperOff G r c)
    (hp : MixedPath G (r,c) t n) (hn : n ≤ 2) (ht : Target G t.1 t.2) :
    ∃ k, k ≤ n ∧ ∃ d, ProperOff G r d ∧ PurePath G r c d k ∧ Target G r d := by
  obtain ⟨k,hkn,d,hkd,hd⟩ := short_fill G hp hn ht
  exact ⟨k,hkn,d,PurePath.proper G hkd hc,hkd,hd⟩

/-- A short mixed minimum constructs the pure minimum at exactly the same number. -/
theorem short_minimum_exists [DecidableEq V] {r : V} {c : V → C} {ell : ℕ}
    (hm : MixedMinimum G r c ell) (hl : ell ≤ 2) : PureMinimum G r c ell := by
  obtain ⟨t,hp,ht⟩ := hm.1
  obtain ⟨k,hkl,d,hkd,hdt⟩ := short_fill G hp hl ht
  have hlk : ell ≤ k := hm.2 k (r,d) hkd.toMixed hdt
  have heq : k = ell := le_antisymm hkl hlk
  subst k
  refine ⟨⟨d,hkd,hdt⟩,?_⟩
  intro n f hpf hft
  exact hm.2 n (r,f) hpf.toMixed hft

end SimpleGraph.VacancyShortFillTeamB
