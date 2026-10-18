import DCheckPinchGeom
/-! Job 26 step (iii), the D-glue half (exploratory): **D-reducibility for an occurrence whose ring is only a face
walk.** `ConfigOccW` is `ConfigOcc` with the ring a `FaceWalk` of the deleted map `G` (distinct darts; vertices may
repeat: pinches and folds of the third ring). The gluing `colorable_of_ext` never used ring injectivity, so it is
restated verbatim. `KempeMatching` comes from `FaceWalk.kempeMatching` (DCheckPinchGeom) instead of the ring-face
route. The result `ConfigOccW.colorable_of_dReducible*` is the face-walk form of `ConfigOcc.colorable_of_dReducible*`.

What is left for step (iii): producing a `ConfigOccW` from an appearing 2-ball (the third ring as a face walk of the
outside map, with distinct darts). -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill DCheck DCheck.R2

variable {n : ℕ}

/-- An occurrence of a configuration with interior `ι` whose ring `ρ` is a face walk of the deleted map `G`. -/
structure ConfigOccW (T G : SphericalMap n) (r m : ℕ) (ρ : ℕ → Fin n) (ι : Fin m → Fin n)
    (intAdj : Fin m → Fin m → Bool) (ringAdj : Fin m → ℕ → Bool) : Prop where
  ring : FaceWalk G r ρ
  ιinj : Function.Injective ι
  ringOff : ∀ t a, ρ t ≠ ι a
  hG : ∀ x y, G.Adj x y ↔ T.Adj x y ∧ (∀ a, x ≠ ι a) ∧ (∀ a, y ≠ ι a)
  nbr : ∀ a w, T.Adj (ι a) w →
    (∃ b, w = ι b ∧ intAdj a b = true) ∨ (∃ t, t < r ∧ w = ρ t ∧ ringAdj a t = true)
  pos : 0 < m

variable {T G : SphericalMap n} {r m : ℕ} {ρ : ℕ → Fin n} {ι : Fin m → Fin n}
  {intAdj : Fin m → Fin m → Bool} {ringAdj : Fin m → ℕ → Bool}

/-- A ring face is a face walk (vertex injectivity gives dart injectivity). -/
theorem RingFace.toFaceWalk (R : RingFace G r ρ) : FaceWalk G r ρ :=
  ⟨R.pos, R.per, R.adj, R.step, fun s t hs ht e _ => R.inj s t hs ht e⟩

/-- A face walk from its facts below the period (as `RingFace.mk_lt`, with dart injectivity in place of vertex
injectivity). -/
theorem FaceWalk.mk_lt (hr : 0 < r) (hper : ∀ t, ρ (t + r) = ρ t) (hadj : ∀ t, t < r → G.Adj (ρ t) (ρ (t + 1)))
    (hstep : ∀ t, t < r → ∀ h1 h2, G.rotation.faceNext ⟨(ρ t, ρ (t + 1)), h1⟩ = ⟨(ρ (t + 1), ρ (t + 2)), h2⟩)
    (hdinj : ∀ s t, s < r → t < r → ρ s = ρ t → ρ (s + 1) = ρ (t + 1) → s = t) : FaceWalk G r ρ := by
  have hm : ∀ t, ρ t = ρ (t % r) := fun t => (per_mod' hper t).symm
  have m1 : ∀ t, ρ (t + 1) = ρ (t % r + 1) := fun t => per_cong hper (Nat.ModEq.add_right 1 (Nat.mod_modEq t r)).symm
  have m2 : ∀ t, ρ (t + 2) = ρ (t % r + 2) := fun t => per_cong hper (Nat.ModEq.add_right 2 (Nat.mod_modEq t r)).symm
  have adj' : ∀ t, G.Adj (ρ t) (ρ (t + 1)) := fun t => by
    rw [hm t, m1 t]; exact hadj _ (Nat.mod_lt _ hr)
  refine ⟨hr, hper, adj', fun t => ?_, hdinj⟩
  have h1 : G.Adj (ρ (t % r)) (ρ (t % r + 1)) := hadj _ (Nat.mod_lt _ hr)
  have h2 : G.Adj (ρ (t % r + 1)) (ρ (t % r + 1 + 1)) := adj' _
  have key := hstep _ (Nat.mod_lt _ hr) h1 h2
  have e1 : (⟨(ρ t, ρ (t + 1)), adj' t⟩ : G.Dart) = ⟨(ρ (t % r), ρ (t % r + 1)), h1⟩ := by
    apply Dart.ext; apply Prod.ext
    · exact hm t
    · exact m1 t
  have e2 : (⟨(ρ (t + 1), ρ (t + 2)), adj' (t + 1)⟩ : G.Dart) =
      ⟨(ρ (t % r + 1), ρ (t % r + 2)), h2⟩ := by
    apply Dart.ext; apply Prod.ext
    · exact m1 t
    · exact m2 t
  rw [e1, key, e2]

/-- Every `ConfigOcc` is a `ConfigOccW`. -/
theorem ConfigOcc.toW (O : ConfigOcc T G r m ρ ι intAdj ringAdj) : ConfigOccW T G r m ρ ι intAdj ringAdj :=
  ⟨O.ring.toFaceWalk, O.ιinj, O.ringOff, O.hG, O.nbr, O.pos⟩

def ConfigOccW.hole (_O : ConfigOccW T G r m ρ ι intAdj ringAdj) : Fin n := ι ⟨0, _O.pos⟩

theorem ConfigOccW.ring_ne_hole (O : ConfigOccW T G r m ρ ι intAdj ringAdj) (t : ℕ) : ρ t ≠ O.hole :=
  O.ringOff t _

theorem ConfigOccW.ring_proper (O : ConfigOccW T G r m ρ ι intAdj ringAdj) {c : Fin n → Fin 4}
    (hc : ProperOff G.graph O.hole c) (t : ℕ) : c (ρ t) ≠ c (ρ (t + 1)) :=
  hc (O.ring.adj t) (O.ring_ne_hole t) (O.ring_ne_hole (t + 1))

theorem ConfigOccW.ring_proper_wrap (O : ConfigOccW T G r m ρ ι intAdj ringAdj)
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) (t : ℕ) (ht : t + 1 = r) :
    c (ρ t) ≠ c (ρ 0) := by
  have e : ρ (t + 1) = ρ 0 := by rw [ht, show r = 0 + r by omega]; exact O.ring.per 0
  have := O.ring_proper hc t
  rwa [e] at this

/-- **Gluing** (verbatim `ConfigOcc.colorable_of_ext`; the ring enters only through `ringOff` and `nbr`). -/
theorem ConfigOccW.colorable_of_ext (O : ConfigOccW T G r m ρ ι intAdj ringAdj)
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) (σ : Equiv.Perm (Fin 4))
    (κ : ℕ → Fin 4) (hκ : ∀ t, t < r → c (ρ t) = σ (κ t)) (lam : Fin m → Fin 4)
    (hint : ∀ a b, intAdj a b = true → lam a ≠ lam b)
    (hring : ∀ a t, t < r → ringAdj a t = true → lam a ≠ κ t)
    (hsym : ∀ a b, intAdj a b = true → intAdj b a = true) : T.graph.Colorable 4 := by
  classical
  let col : Fin n → Fin 4 := fun x =>
    if hx : ∃ a, x = ι a then σ (lam (Classical.choose hx)) else c x
  have col_int : ∀ a, col (ι a) = σ (lam a) := by
    intro a
    have hx : ∃ b, ι a = ι b := ⟨a, rfl⟩
    simp only [col, dif_pos hx]
    rw [← O.ιinj (Classical.choose_spec hx)]
  have col_out : ∀ x, (∀ a, x ≠ ι a) → col x = c x := by
    intro x hx
    have hx' : ¬ ∃ a, x = ι a := fun h => hx _ (Classical.choose_spec h)
    simp only [col, dif_neg hx']
  have int_edge : ∀ a w, T.Adj (ι a) w → col (ι a) ≠ col w := by
    intro a w haw
    rcases O.nbr a w haw with ⟨b, rfl, hab⟩ | ⟨t, ht, rfl, hat⟩
    · rw [col_int, col_int]; exact σ.injective.ne (hint a b hab)
    · rw [col_int, col_out _ (O.ringOff t), hκ t ht]
      exact σ.injective.ne (hring a t ht hat)
  refine ⟨SimpleGraph.Coloring.mk col ?_⟩
  intro x y hxy
  by_cases hx : ∃ a, x = ι a
  · obtain ⟨a, rfl⟩ := hx
    exact int_edge a y hxy
  · by_cases hy : ∃ a, y = ι a
    · obtain ⟨a, rfl⟩ := hy
      exact (int_edge a x hxy.symm).symm
    · have hx' : ∀ a, x ≠ ι a := fun a h => hx ⟨a, h⟩
      have hy' : ∀ a, y ≠ ι a := fun a h => hy ⟨a, h⟩
      rw [col_out x hx', col_out y hy']
      exact hc ((O.hG x y).2 ⟨hxy, hx', hy'⟩) (hx' _) (hy' _)

/-- **D-reducibility glue for a face-walk ring** (as `ConfigOcc.colorable_of_dReducibleT`, with
`FaceWalk.kempeMatching`). -/
theorem ConfigOccW.colorable_of_dReducibleT (N : ℕ) (hN : N ≤ 10) (cf : Conf)
    (hD : dReducibleT (matchTableN N) cf = true) (hr2 : 2 ≤ cf.r) (hrN : cf.r < 2 * N)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (hloop : ∀ a, intAdjOf cf a a = false)
    {ρ : ℕ → Fin n} {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4 := by
  classical
  let P : ℕ → Prop := fun k => ∃ c : Fin n → Fin 4, ProperOff G.graph O.hole c ∧
    k = code (ringSeq ρ c) cf.r
  have hcanon : ∀ k, P k → P (canon cf.r k) := by
    rintro k ⟨c1, hc1, rfl⟩
    obtain ⟨g, hg, heq⟩ := canon_rename cf.r (ringSeq ρ c1) (ringSeq_lt ρ c1)
    refine ⟨fun v => g (c1 v), fun u v huv hu hv h => hc1 huv hu hv (hg h), ?_⟩
    rw [heq]
    apply code_congr
    intro t _
    simp only [ringSeq]
    congr 3
    exact Nat.mod_eq_of_lt (c1 (ρ t)).isLt
  have hprop : ∀ k, P k → (∀ i, i < cf.r → col k i ≠ col k ((i + 1) % cf.r)) ∧ k < 4 ^ cf.r := by
    rintro k ⟨c1, hc1, rfl⟩
    refine ⟨fun i hi => ?_, code_lt _ (ringSeq_lt ρ c1) _⟩
    rw [col_code _ (ringSeq_lt ρ c1) _ _ hi, col_code _ (ringSeq_lt ρ c1) _ _ (Nat.mod_lt _ (by omega))]
    simp only [ringSeq]
    intro h
    by_cases hi1 : i + 1 < cf.r
    · rw [Nat.mod_eq_of_lt hi1] at h; exact O.ring_proper hc1 i (Fin.ext h)
    · rw [show (i + 1) % cf.r = 0 by rw [show i + 1 = cf.r by omega, Nat.mod_self]] at h
      exact O.ring_proper_wrap hc1 i (by omega) (Fin.ext h)
  have hKM := FaceWalk.kempeMatching O.ring O.hole O.ring_ne_hole cf N hN rfl hrN
  obtain ⟨k', ⟨c', hc', rfl⟩, hext⟩ := dReducible_soundT (matchTableN N) cf hD hr2 P hcanon
    hKM hprop _ ⟨c, hc, rfl⟩
  obtain ⟨out, hsz, hlo, hok⟩ := extendsQ_sound cf _ hext
  let lam : Fin cf.m → Fin 4 := fun a => ⟨out[a.val]!, hlo a.val (by rw [hsz]; exact a.isLt)⟩
  refine O.colorable_of_ext hc' 1 (fun t => c' (ρ t)) (fun t _ => rfl) lam ?_ ?_ hsym
  · intro a b hab heq
    have hlam : out[a.val]! = out[b.val]! := congrArg Fin.val heq
    rcases Nat.lt_trichotomy b.val a.val with hlt | heq' | hgt
    · exact (hok a.val a.isLt).2 b.val (by simpa [intAdjOf] using hab) hlt hlam.symm
    · have : a = b := Fin.ext heq'.symm
      subst this; rw [hloop] at hab; exact Bool.false_ne_true hab
    · exact (hok b.val b.isLt).2 a.val (by simpa [intAdjOf] using hsym a b hab) hgt hlam
  · intro a t ht hat heq
    have := (hok a.val a.isLt).1 t (by simpa [ringAdjOf] using hat)
    apply this
    rw [col_code _ (ringSeq_lt ρ c') _ _ ht]
    simp only [ringSeq]
    exact (congrArg Fin.val heq).symm

/-- **(F) for `DCheck18`, face-walk ring** (rings `2 ≤ r ≤ 19`). -/
theorem ConfigOccW.colorable_of_dReducible18 (cf : DCheck18.Conf) (hD : DCheck18.dReducible cf = true)
    (hr2 : 2 ≤ cf.r) (hr : cf.r ≤ 19)
    (hsym : ∀ a b, intAdjOf (Conf.of18 cf) a b = true → intAdjOf (Conf.of18 cf) b a = true)
    (hloop : ∀ a, intAdjOf (Conf.of18 cf) a a = false)
    {ρ : ℕ → Fin n} {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf (Conf.of18 cf)) (ringAdjOf (Conf.of18 cf)))
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4 :=
  ConfigOccW.colorable_of_dReducibleT (cf := Conf.of18 cf) 10 (by decide)
    (by rw [← dReducible18_eq_T]; exact hD) hr2 (by show cf.r < 2 * 10; omega) hsym hloop O hc

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.ConfigOccW.colorable_of_dReducibleT
#print axioms SimpleGraph.SphericalMap.ConfigOccW.colorable_of_dReducible18
