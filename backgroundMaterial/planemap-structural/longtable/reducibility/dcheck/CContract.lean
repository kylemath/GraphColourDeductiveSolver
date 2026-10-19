import ClaimGlue

/-!
# CContract: contracting one edge of a spherical triangulation (Long Table, 19 Oct 2026)

C4a of `CGlue.lean` for a single edge. In a triangulation `T` with no separating triangle, the
contraction of an edge `a b` is built from the library's two surgery steps:
* **flip** (`flip_exists`): erase the edge `x y` shared by the triangles `x y z` and `y x u`
  (`eraseEdge`, Fills kept by `fills_eraseRotation`) and insert the chord `z u` in the merged face
  (`split`, Fills kept by `split_fills`); every other rotation step is unchanged;
* sweeping around `b`: with `b`'s rotation `a = w 0, w 1, …, w (d-1)`, flip `b w 1`, …, `b w (d-2)`
  in turn (each flip adds `a w (i+1)`), then delete `b`'s remaining edges (`subgraph_closed`).

Rotation steps are tracked in vertex form with `Nx M p q r` ("after `q` comes `r` at `p`").
-/

namespace SimpleGraph.SphericalMap
open VacancyIcosahedral RotationSystem PlaneMapConstruction

variable {n : ℕ}

/-! ## Rotation steps under erase and split -/

theorem nx_inj {M : SphericalMap n} {p q q' r : Fin n} (h : Nx M p q r) (h' : Nx M p q' r) :
    q = q' := by
  obtain ⟨h1, h2, e⟩ := nx_dart h
  obtain ⟨h1', h2', e'⟩ := nx_dart h'
  have := M.rotation.next.injective (e.trans e'.symm)
  exact congrArg (fun d : M.Dart => d.snd) this

theorem nx_func' {M : SphericalMap n} {p q r r' : Fin n} (h : Nx M p q r) (h' : Nx M p q r') :
    r = r' := by
  obtain ⟨h1, e⟩ := h
  obtain ⟨h1', e'⟩ := h'
  exact e.symm.trans e'

theorem dart_ne_of_edge {G : SimpleGraph (Fin n)} {d e : G.Dart} (h : d.edge ≠ e.edge) : d ≠ e :=
  fun hh => h (hh ▸ rfl)

/-- An erased edge leaves the other rotation steps alone. -/
theorem nx_erase (M : SphericalMap n) (e : M.Dart) {p q r : Fin n} (h : Nx M p q r)
    (hpq : s(p, q) ≠ e.edge) (hpr : s(p, r) ≠ e.edge) : Nx (M.eraseEdge e) p q r := by
  classical
  obtain ⟨hpq', hpr', hn⟩ := nx_dart h
  refine ⟨⟨hpq', hpq⟩, ?_⟩
  have key := M.rotation.eraseRotation_next e ⟨(p, q), ⟨hpq', hpq⟩⟩
  change _ = (M.rotation.next.erasePoint e).erasePoint e.symm ⟨(p, q), hpq'⟩ at key
  have n1 : (⟨(p, q), hpq'⟩ : M.Dart) ≠ e := dart_ne_of_edge hpq
  have n2 : (⟨(p, q), hpq'⟩ : M.Dart) ≠ e.symm := dart_ne_of_edge (by rw [Dart.edge_symm]; exact hpq)
  have m1 : M.rotation.next ⟨(p, q), hpq'⟩ ≠ e := by rw [hn]; exact dart_ne_of_edge hpr
  have m2 : M.rotation.next ⟨(p, q), hpq'⟩ ≠ e.symm := by
    rw [hn]; exact dart_ne_of_edge (by rw [Dart.edge_symm]; exact hpr)
  rw [erasePoint_miss _ _ _ n2 (by rw [erasePoint_miss _ _ _ n1 m1]; exact m2),
    erasePoint_miss _ _ _ n1 m1, hn] at key
  exact congrArg (fun d : M.Dart => d.snd) key

/-- Erasing the edge `p r` (dart `e = p → r`) skips it in the rotation at `p`. -/
theorem nx_erase_skipA (M : SphericalMap n) {p q r s : Fin n} (h1 : Nx M p q r) (h2 : Nx M p r s)
    (hpr : M.Adj p r) (hqr : q ≠ r) (hsr : s ≠ r) :
    Nx (M.eraseEdge ⟨(p, r), hpr⟩) p q s := by
  classical
  set e : M.Dart := ⟨(p, r), hpr⟩ with he
  obtain ⟨hpq', hpr', hn⟩ := nx_dart h1
  obtain ⟨hpr'', hps, hn2⟩ := nx_dart h2
  have hpq0 : s(p, q) ≠ s(p, r) := by
    intro hh; rcases Sym2.eq_iff.1 hh with ⟨-, h⟩ | ⟨h1, -⟩
    · exact hqr h
    · exact hpr.ne h1
  have hpq : s(p, q) ≠ e.edge := hpq0
  refine ⟨⟨hpq', hpq⟩, ?_⟩
  have key := M.rotation.eraseRotation_next e ⟨(p, q), ⟨hpq', hpq⟩⟩
  change _ = (M.rotation.next.erasePoint e).erasePoint e.symm ⟨(p, q), hpq'⟩ at key
  have n2 : (⟨(p, q), hpq'⟩ : M.Dart) ≠ e.symm := fun hh =>
    hpr.ne (congrArg (fun d : M.Dart => d.fst) hh)
  have hit : M.rotation.next ⟨(p, q), hpq'⟩ = e := hn
  have hn2e : M.rotation.next e = ⟨(p, s), hps⟩ := hn2
  have ne2 : M.rotation.next e ≠ e.symm := by
    rw [hn2e]
    exact fun hh => hpr.ne (congrArg (fun d : M.Dart => d.fst) hh)
  rw [erasePoint_miss _ _ _ n2 (by rw [erasePoint_hit _ _ _ hit]; exact ne2),
    erasePoint_hit _ _ _ hit, hn2e] at key
  exact congrArg (fun d : M.Dart => d.snd) key

/-- Erasing the edge `r p` (dart `e = r → p`, so `e.symm = p → r`) skips `r` at `p`. -/
theorem nx_erase_skipB (M : SphericalMap n) {p q r s : Fin n} (h1 : Nx M p q r) (h2 : Nx M p r s)
    (hrp : M.Adj r p) (hqr : q ≠ r) (hsr : s ≠ r) :
    Nx (M.eraseEdge ⟨(r, p), hrp⟩) p q s := by
  classical
  set e : M.Dart := ⟨(r, p), hrp⟩ with he
  obtain ⟨hpq', hpr', hn⟩ := nx_dart h1
  obtain ⟨hpr'', hps, hn2⟩ := nx_dart h2
  have hpq0 : s(p, q) ≠ s(r, p) := by
    intro hh; rcases Sym2.eq_iff.1 hh with ⟨h1, -⟩ | ⟨-, h2⟩
    · exact hrp.ne h1.symm
    · exact hqr h2
  have hpq : s(p, q) ≠ e.edge := hpq0
  refine ⟨⟨hpq', hpq⟩, ?_⟩
  have key := M.rotation.eraseRotation_next e ⟨(p, q), ⟨hpq', hpq⟩⟩
  change _ = (M.rotation.next.erasePoint e).erasePoint e.symm ⟨(p, q), hpq'⟩ at key
  have n1 : (⟨(p, q), hpq'⟩ : M.Dart) ≠ e := fun hh =>
    hrp.ne (congrArg (fun d : M.Dart => d.fst) hh).symm
  have es : e.symm = ⟨(p, r), hpr''⟩ := rfl
  have m1 : M.rotation.next ⟨(p, q), hpq'⟩ ≠ e := by
    rw [hn]; exact fun hh => hrp.ne (congrArg (fun d : M.Dart => d.fst) hh).symm
  have hit : (M.rotation.next.erasePoint e) ⟨(p, q), hpq'⟩ = e.symm := by
    rw [erasePoint_miss _ _ _ n1 m1, hn]; exact Dart.ext _ _ rfl
  have n3 : e.symm ≠ e := fun hh => hrp.ne (congrArg (fun d : M.Dart => d.fst) hh).symm
  have hn2s : M.rotation.next e.symm = ⟨(p, s), hps⟩ := by rw [es]; exact hn2
  have m3 : M.rotation.next e.symm ≠ e := by
    rw [hn2s]; exact fun hh => hrp.ne (congrArg (fun d : M.Dart => d.fst) hh).symm
  rw [erasePoint_hit _ _ _ hit, erasePoint_miss _ _ _ n3 m3, hn2s] at key
  exact congrArg (fun d : M.Dart => d.snd) key

/-- The spherical map with a chord inserted before `a` and `b` (same face). -/
noncomputable def splitMap (M : SphericalMap n) (a b : M.Dart) (hab : a.fst ≠ b.fst)
    (hmiss : ¬ M.Adj a.fst b.fst) (hface : M.faceOf a = M.faceOf b) : SphericalMap n :=
  ⟨_, split M.rotation a b hab hmiss, split_fills M.rotation M.fills a b hface hab hmiss⟩

section SplitNx
variable (M : SphericalMap n) (a b : M.Dart) (hab : a.fst ≠ b.fst)
  (hmiss : ¬ M.Adj a.fst b.fst) (hface : M.faceOf a = M.faceOf b)

theorem splitMap_next_old (d : M.Dart) :
    (splitMap M a b hab hmiss hface).rotation.next (splitOld a.fst b.fst hab d) =
      splitDartEquiv a.fst b.fst hab hmiss (splitNext M.rotation a b (.inl d)) := by
  change (split M.rotation a b hab hmiss).next (splitDartEquiv a.fst b.fst hab hmiss (.inl d)) = _
  rw [split_next_apply]

theorem nx_split_old {p q r : Fin n} (h : Nx M p q r) (ha : (p, r) ≠ a.toProd)
    (hb : (p, r) ≠ b.toProd) : Nx (splitMap M a b hab hmiss hface) p q r := by
  classical
  obtain ⟨hpq, hpr, hn⟩ := nx_dart h
  refine ⟨Or.inl hpq, ?_⟩
  change ((splitMap M a b hab hmiss hface).rotation.next
    (splitOld a.fst b.fst hab ⟨(p, q), hpq⟩)).snd = _
  rw [splitMap_next_old, split_next_old, hn, if_neg (fun hh => ha (congrArg Dart.toProd hh)),
    if_neg (fun hh => hb (congrArg Dart.toProd hh))]
  rfl

theorem nx_split_a {p q r : Fin n} (h : Nx M p q r) (ha : a.toProd = (p, r)) :
    Nx (splitMap M a b hab hmiss hface) p q b.fst ∧ Nx (splitMap M a b hab hmiss hface) p b.fst r := by
  classical
  obtain ⟨hpq, hpr, hn⟩ := nx_dart h
  have hna : M.rotation.next ⟨(p, q), hpq⟩ = a := by rw [hn]; exact Dart.ext _ _ ha.symm
  have hp : a.fst = p := congrArg Prod.fst ha
  constructor
  · refine ⟨Or.inl hpq, ?_⟩
    change ((splitMap M a b hab hmiss hface).rotation.next
      (splitOld a.fst b.fst hab ⟨(p, q), hpq⟩)).snd = _
    rw [splitMap_next_old, split_next_old, if_pos hna]
    rfl
  · subst hp
    refine ⟨Or.inr (Or.inl ⟨rfl, rfl⟩), ?_⟩
    change ((split M.rotation a b hab hmiss).next (splitDartEquiv a.fst b.fst hab hmiss (.inr false))).snd = r
    rw [split_next_apply, split_next_out M.rotation a b hab]
    exact congrArg Prod.snd ha

theorem nx_split_b {p q r : Fin n} (h : Nx M p q r) (hb : b.toProd = (p, r)) :
    Nx (splitMap M a b hab hmiss hface) p q a.fst ∧ Nx (splitMap M a b hab hmiss hface) p a.fst r := by
  classical
  obtain ⟨hpq, hpr, hn⟩ := nx_dart h
  have hnb : M.rotation.next ⟨(p, q), hpq⟩ = b := by rw [hn]; exact Dart.ext _ _ hb.symm
  have hp : b.fst = p := congrArg Prod.fst hb
  have hna : M.rotation.next ⟨(p, q), hpq⟩ ≠ a := by
    rw [hnb]; exact fun hh => hab (congrArg (fun d : M.Dart => d.fst) hh).symm
  constructor
  · refine ⟨Or.inl hpq, ?_⟩
    change ((splitMap M a b hab hmiss hface).rotation.next
      (splitOld a.fst b.fst hab ⟨(p, q), hpq⟩)).snd = _
    rw [splitMap_next_old, split_next_old, if_neg hna, if_pos hnb]
    rfl
  · subst hp
    refine ⟨Or.inr (Or.inr ⟨rfl, rfl⟩), ?_⟩
    change ((split M.rotation a b hab hmiss).next (splitDartEquiv a.fst b.fst hab hmiss (.inr true))).snd = r
    rw [split_next_apply, split_next_back]
    exact congrArg Prod.snd hb

end SplitNx


theorem s_ne {p q x y : Fin n} (h : ¬ ((p = x ∧ q = y) ∨ (p = y ∧ q = x))) : s(p, q) ≠ s(x, y) :=
  fun hh => h (Sym2.eq_iff.1 hh)

/-- **Flip.** The edge `x y` borders the triangles `x y z` (`Nx y x z`, `Nx z y x`, `Nx x z y`) and
`y x u` (`Nx x y u`, `Nx u x y`, `Nx y u x`). Erasing it and inserting `z u` gives a spherical map
in which `x z u`'s rotation steps hold and every rotation step at a dart away from the two
triangles is unchanged. -/
theorem flip_exists (M : SphericalMap n) {x y z u : Fin n}
    (t1 : Nx M y x z) (t2 : Nx M z y x) (t3 : Nx M x z y)
    (s1 : Nx M x y u) (s2 : Nx M u x y) (s3 : Nx M y u x)
    (hzu : z ≠ u) (hmiss : ¬ M.Adj z u) :
    ∃ M' : SphericalMap n,
      (∀ p q, M.Adj p q → s(p, q) ≠ s(x, y) → M'.Adj p q) ∧
      (∀ p q, M'.Adj p q → (M.Adj p q ∧ s(p, q) ≠ s(x, y)) ∨ s(p, q) = s(z, u)) ∧
      Nx M' x z u ∧ Nx M' u x z ∧ Nx M' z u x ∧
      (∀ p q r, Nx M p q r → (p, q) ≠ (x, y) → (p, q) ≠ (y, x) → (p, q) ≠ (x, z) →
        (p, q) ≠ (y, u) → (p, q) ≠ (z, y) → (p, q) ≠ (u, x) → Nx M' p q r) := by
  classical
  have hxy : M.Adj x y := nx_adj_right t3
  have hxz : M.Adj x z := nx_adj_left t3
  have hzy : M.Adj z y := nx_adj_left t2
  have hyu : M.Adj y u := nx_adj_left s3
  have hux : M.Adj u x := nx_adj_left s2
  have nxz : x ≠ z := hxz.ne
  have nzy : z ≠ y := hzy.ne
  have nyu : y ≠ u := hyu.ne
  have nux : u ≠ x := hux.ne
  let e : M.Dart := ⟨(x, y), hxy⟩
  let E := M.eraseEdge e
  have e1 : Nx E x z u := nx_erase_skipA M t3 s1 hxy nzy nyu.symm
  have e2 : Nx E y u z := nx_erase_skipB M s3 t1 hxy nux nxz.symm
  have e3 : Nx E z y x := nx_erase M e t2
    (s_ne (by rintro (⟨h, -⟩ | ⟨h, -⟩); exacts [nxz h.symm, nzy h]))
    (s_ne (by rintro (⟨h, -⟩ | ⟨h, -⟩); exacts [nxz h.symm, nzy h]))
  have e4 : Nx E u x y := nx_erase M e s2
    (s_ne (by rintro (⟨h, -⟩ | ⟨h, -⟩); exacts [nux h, nyu h.symm]))
    (s_ne (by rintro (⟨h, -⟩ | ⟨h, -⟩); exacts [nux h, nyu h.symm]))
  obtain ⟨hzy', hzx, n3⟩ := nx_dart e3
  obtain ⟨-, huy, -⟩ := nx_dart e4
  obtain ⟨hyu', hyz, n2⟩ := nx_dart e2
  let a : E.Dart := ⟨(z, x), hzx⟩
  let b : E.Dart := ⟨(u, y), huy⟩
  have hab : a.fst ≠ b.fst := hzu
  have hmissE : ¬ E.Adj a.fst b.fst := fun h => hmiss h.1
  have f1 : E.rotation.faceNext b = ⟨(y, z), hyz⟩ := by
    rw [RotationSystem.face_next_apply]; exact n2
  have f2 : E.rotation.faceNext ⟨(y, z), hyz⟩ = a := by
    rw [RotationSystem.face_next_apply]; exact n3
  have hface : E.faceOf a = E.faceOf b := by
    show E.rotation.faceOf a = E.rotation.faceOf b
    rw [← E.rotation.face_of_face_next b, f1, ← E.rotation.face_of_face_next ⟨(y, z), hyz⟩, f2]
  refine ⟨splitMap E a b hab hmissE hface, fun p q h hne => Or.inl ⟨h, hne⟩, ?_, ?_, ?_, ?_, ?_⟩
  · rintro p q (h | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
    · exact Or.inl h
    · exact Or.inr rfl
    · exact Or.inr Sym2.eq_swap
  · exact nx_split_old E a b hab hmissE hface e1 (fun h => nxz (congrArg Prod.fst h))
      (fun h => nux (congrArg Prod.fst h).symm)
  · exact (nx_split_b E a b hab hmissE hface e4 rfl).1
  · exact (nx_split_a E a b hab hmissE hface e3 rfl).2
  · intro p q r h h1 h2 h3 h4 h5 h6
    have hE : Nx E p q r := by
      refine nx_erase M e h (s_ne ?_) (s_ne ?_)
      · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
        · exact h1 rfl
        · exact h2 rfl
      · rintro (⟨rfl, rfl⟩ | ⟨rfl, rfl⟩)
        · exact h3 (by rw [nx_inj h t3])
        · exact h4 (by rw [nx_inj h s3])
    refine nx_split_old E a b hab hmissE hface hE ?_ ?_
    · intro hh
      have hp : p = z := congrArg Prod.fst hh
      have hr : r = x := congrArg Prod.snd hh
      subst hp hr
      exact h5 (by rw [nx_inj hE e3])
    · intro hh
      have hp : p = u := congrArg Prod.fst hh
      have hr : r = y := congrArg Prod.snd hh
      subst hp hr
      exact h6 (by rw [nx_inj hE e4])

/-! ## The rotation chain at `b` from `a` -/

/-- The rotation at `b` read from `a`: `w 0 = a`, consecutive entries are rotation steps, and the
chain closes after `deg b` steps. -/
theorem rot_chain (M : SphericalMap n) {b a : Fin n} (hba : M.Adj b a) :
    ∃ w : ℕ → Fin n, w 0 = a ∧ w (M.graph.degree b) = a ∧ ∀ j, Nx M b (w j) (w (j + 1)) := by
  classical
  let d0 : M.Dart := ⟨(b, a), hba⟩
  let D : ℕ → M.Dart := fun j => (⇑M.rotation.next)^[j] d0
  have hf : ∀ j, (D j).fst = b := by
    intro j
    induction j with
    | zero => rfl
    | succ j ih =>
      show ((⇑M.rotation.next)^[j + 1] d0).fst = b
      rw [Function.iterate_succ_apply', M.rotation.next_fst]; exact ih
  have hadj : ∀ j, M.Adj b (D j).snd := by
    intro j
    have := (D j).adj
    rwa [show (D j).toProd.1 = b from hf j] at this
  have hD : ∀ j, (⟨(b, (D j).snd), hadj j⟩ : M.Dart) = D j := fun j =>
    Dart.ext _ _ (Prod.ext (hf j).symm rfl)
  refine ⟨fun j => (D j).snd, rfl, ?_, fun j => ⟨hadj j, ?_⟩⟩
  · let σ := M.rotation.neighborRotation b
    let w0 : M.graph.neighborSet b := ⟨a, hba⟩
    have hsemi : Function.Semiconj (M.graph.dartOfNeighborSet b) σ M.rotation.next :=
      M.rotation.neighbor_rotation_dart b
    have hp : Function.minimalPeriod σ w0 = M.graph.degree b :=
      M.rotation.neighbor_period_eq_degree b w0
    have h1 := hsemi.iterate_right (M.graph.degree b) w0
    have h2 : σ^[M.graph.degree b] w0 = w0 := by rw [← hp]; exact Function.iterate_minimalPeriod
    rw [h2] at h1
    show (D (M.graph.degree b)).snd = a
    have h3 : D (M.graph.degree b) = M.graph.dartOfNeighborSet b w0 := h1.symm
    rw [h3]; rfl
  · rw [hD j]
    show _ = ((⇑M.rotation.next)^[j + 1] d0).snd
    rw [Function.iterate_succ_apply']

/-! ## The sweep -/

section Sweep

variable {T : SphericalMap n} {a b : Fin n} {d : ℕ} {w : ℕ → Fin n}

/-- The state after `m` flips around `b`. -/
def SweepInv (T : SphericalMap n) (a b : Fin n) (d : ℕ) (w : ℕ → Fin n) (m : ℕ)
    (M : SphericalMap n) : Prop :=
  (∀ p q, T.Adj p q → p ≠ b → q ≠ b → M.Adj p q) ∧
  (∀ k, 2 ≤ k → k ≤ m + 1 → M.Adj a (w k)) ∧
  (∀ p q, M.Adj p q → T.Adj p q ∨ ∃ k, 2 ≤ k ∧ k ≤ m + 1 ∧ s(p, q) = s(a, w k)) ∧
  (Nx M b a (w (m + 1)) ∧ Nx M (w (m + 1)) b a ∧ Nx M a (w (m + 1)) b) ∧
  (∀ j, m + 1 ≤ j → j + 1 < d →
    Nx M b (w j) (w (j + 1)) ∧ Nx M (w (j + 1)) b (w j) ∧ Nx M (w j) (w (j + 1)) b)

theorem sweepInv_zero (htri : T.Triangulated) (hw0 : w 0 = a) (hd : 0 < d)
    (hch : ∀ j, j < d → Nx T b (w j) (w (j + 1))) : SweepInv T a b d w 0 T := by
  refine ⟨fun p q h _ _ => h, fun k h1 h2 => by omega, fun p q h => Or.inl h, ?_, ?_⟩
  · have h0 := hch 0 hd
    rw [hw0] at h0
    exact ⟨h0, nx_tri htri h0⟩
  · intro j _ hj
    have h := hch j (by omega)
    exact ⟨h, nx_tri htri h⟩

set_option hygiene false in
/-- Dart inequalities in the sweep. -/
macro "dne" : tactic => `(tactic| (
  intro hh; simp only [Prod.mk.injEq] at hh; obtain ⟨h1, h2⟩ := hh
  first
    | exact hab h1 | exact hab h1.symm | exact hab h2 | exact hab h2.symm
    | exact wb _ (by omega) h1 | exact wb _ (by omega) h1.symm
    | exact wb _ (by omega) h2 | exact wb _ (by omega) h2.symm
    | exact wa _ (by omega) (by omega) h1 | exact wa _ (by omega) (by omega) h1.symm
    | exact wa _ (by omega) (by omega) h2 | exact wa _ (by omega) (by omega) h2.symm
    | (have := winj _ _ (by omega) (by omega) h1; omega)
    | (have := winj _ _ (by omega) (by omega) h2; omega)))

theorem sweepInv_succ (hns : NoSep T) (hab : a ≠ b)
    (wb : ∀ k, k < d → w k ≠ b) (wa : ∀ k, 0 < k → k < d → w k ≠ a)
    (winj : ∀ i j, i < d → j < d → w i = w j → i = j)
    (hnadj : ∀ k, 2 ≤ k → k + 2 ≤ d → ¬ T.Adj a (w k))
    {m : ℕ} (hm : m + 4 ≤ d) {M : SphericalMap n} (hI : SweepInv T a b d w m M) :
    ∃ M', SweepInv T a b d w (m + 1) M' := by
  obtain ⟨hA, hB, hC, ⟨t3, t1, t2⟩, hE⟩ := hI
  obtain ⟨s1, s2, s3⟩ := hE (m + 1) le_rfl (by omega)
  have hzu : a ≠ w (m + 2) := fun h => wa _ (by omega) (by omega) h.symm
  have hmiss : ¬ M.Adj a (w (m + 2)) := by
    intro h
    rcases hC _ _ h with h | ⟨k, hk2, hk, hs⟩
    · exact hnadj (m + 2) (by omega) (by omega) h
    · rcases Sym2.eq_iff.1 hs with ⟨-, h2⟩ | ⟨h1, -⟩
      · have := winj _ _ (by omega) (by omega) h2; omega
      · exact wa k (by omega) (by omega) h1.symm
  obtain ⟨M', hF, hBk, n1, n2, n3, hU⟩ := flip_exists M t1 t2 t3 s1 s2 s3 hzu hmiss
  refine ⟨M', ?_, ?_, ?_, ⟨n1, n2, n3⟩, ?_⟩
  · intro p q h hp hq
    exact hF p q (hA p q h hp hq) (s_ne (by rintro (⟨h1, -⟩ | ⟨-, h2⟩); exacts [hp h1, hq h2]))
  · intro k hk2 hk
    rcases Nat.lt_or_ge k (m + 2) with hlt | hge
    · refine hF _ _ (hB k hk2 (by omega)) (s_ne ?_)
      rintro (⟨h1, -⟩ | ⟨-, h2⟩)
      · exact hab h1
      · exact wb k (by omega) h2
    · have : k = m + 2 := by omega
      subst this
      exact nx_adj_left n3
  · intro p q h
    rcases hBk p q h with ⟨h, -⟩ | h
    · rcases hC p q h with h | ⟨k, h1, h2, h3⟩
      · exact Or.inl h
      · exact Or.inr ⟨k, h1, by omega, h3⟩
    · exact Or.inr ⟨m + 2, by omega, le_rfl, h⟩
  · intro j hj hjd
    obtain ⟨e1, e2, e3⟩ := hE j (by omega) hjd
    refine ⟨hU _ _ _ e1 ?_ ?_ ?_ ?_ ?_ ?_, hU _ _ _ e2 ?_ ?_ ?_ ?_ ?_ ?_,
      hU _ _ _ e3 ?_ ?_ ?_ ?_ ?_ ?_⟩ <;> dne

theorem sweep_all (hns : NoSep T) (hab : a ≠ b)
    (wb : ∀ k, k < d → w k ≠ b) (wa : ∀ k, 0 < k → k < d → w k ≠ a)
    (winj : ∀ i j, i < d → j < d → w i = w j → i = j)
    (hnadj : ∀ k, 2 ≤ k → k + 2 ≤ d → ¬ T.Adj a (w k)) (h0 : SweepInv T a b d w 0 T) :
    ∀ m, m + 3 ≤ d ∨ m = 0 → ∃ M, SweepInv T a b d w m M := by
  intro m
  induction m with
  | zero => exact fun _ => ⟨T, h0⟩
  | succ m ih =>
    intro hm
    obtain ⟨M, hM⟩ := ih (Or.inl (by omega))
    exact sweepInv_succ hns hab wb wa winj hnadj (by omega) hM

end Sweep

/-- **Edge contraction on a spherical triangulation without separating triangles.** Contracting
the edge `b a` (merging `b` into `a`) gives a spherical map `T'` of smaller support that keeps
every edge of `T` away from `b` and joins `a` to every other neighbour of `b`. (`b` becomes
isolated.) -/
theorem contract_edge (T : SphericalMap n) (htri : T.Triangulated) (hns : NoSep T) {a b : Fin n}
    (hba : T.Adj b a) :
    ∃ T' : SphericalMap n, supportSize T' < supportSize T ∧
      (∀ p q, T.Adj p q → p ≠ b → q ≠ b → T'.Adj p q) ∧
      (∀ y, T.Adj b y → y ≠ a → T'.Adj a y) := by
  classical
  obtain ⟨w, hw0, hwd, hch⟩ := rot_chain T hba
  set d := T.graph.degree b with hd
  have hdpos : 0 < d := (T.graph.degree_pos_iff_exists_adj b).mpr ⟨a, hba⟩
  have h0 : T.Adj b (w 0) := by rw [hw0]; exact hba
  have winj : ∀ i j, i < d → j < d → w i = w j → i = j :=
    chain_inj hd.symm h0 (fun j _ => hch j)
  have hab : a ≠ b := hba.ne.symm
  have wb : ∀ k, k < d → w k ≠ b := fun k _ => (nx_adj_left (hch k)).ne.symm
  have wa : ∀ k, 0 < k → k < d → w k ≠ a := fun k h1 h2 h => by
    have := winj k 0 h2 hdpos (h.trans hw0.symm); omega
  have eL : Nx T b (w (d - 1)) a := by
    have e := hch (d - 1); rwa [show d - 1 + 1 = d by omega, hwd] at e
  have eF : Nx T b a (w 1) := by have e := hch 0; rwa [hw0] at e
  have hnadj : ∀ k, 2 ≤ k → k + 2 ≤ d → ¬ T.Adj a (w k) := by
    intro k hk1 hk2 h
    rcases hns b a (w k) hba h (nx_adj_left (hch k)).symm with h' | h'
    · have := winj k (d - 1) (by omega) (by omega) (nx_func' h' (nx_tri htri eL).1); omega
    · have := winj k 1 (by omega) (by omega) (nx_func' h' eF); omega
  have hI0 : SweepInv T a b d w 0 T := sweepInv_zero htri hw0 hdpos (fun j _ => hch j)
  obtain ⟨M, hA, hB, hC, -, -⟩ :=
    sweep_all hns hab wb wa winj hnadj hI0 (d - 3) (by omega)
  obtain ⟨T', hT'⟩ := M.subgraph_closed (M.isolateGraph b) (fun _ _ h => h.1)
  refine ⟨T', ?_, ?_, ?_⟩
  · unfold supportSize
    apply Finset.card_lt_card
    refine ⟨fun v hv => ?_, fun hsub => ?_⟩
    · simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hv ⊢
      obtain ⟨q, hq⟩ := (T'.graph.degree_pos_iff_exists_adj v).mp hv
      rw [hT'] at hq
      rw [T.graph.degree_pos_iff_exists_adj]
      rcases hC v q hq.1 with h | ⟨k, hk2, hk, hs⟩
      · exact ⟨q, h⟩
      · rcases Sym2.eq_iff.1 hs with ⟨rfl, -⟩ | ⟨rfl, -⟩
        · exact ⟨b, hba.symm⟩
        · exact ⟨b, (nx_adj_left (hch k)).symm⟩
    · have hmem : b ∈ Finset.univ.filter (fun x => 0 < T.graph.degree x) := by
        simp only [Finset.mem_filter, Finset.mem_univ, true_and]
        exact (T.graph.degree_pos_iff_exists_adj b).mpr ⟨a, hba⟩
      have := hsub hmem
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at this
      obtain ⟨u, hu⟩ := (T'.graph.degree_pos_iff_exists_adj b).mp this
      rw [hT'] at hu
      exact hu.2.1 rfl
  · intro p q h hp hq
    show T'.graph.Adj p q
    rw [hT']
    exact ⟨hA p q h hp hq, hp, hq⟩
  · intro y hy hya
    obtain ⟨k, hk, rfl⟩ := nbr_of_chain hd.symm h0 (fun j _ => hch j) y hy
    show T'.graph.Adj _ _
    rw [hT']
    refine ⟨?_, hab, wb k hk⟩
    rcases Nat.lt_or_ge k 2 with hk2 | hk2
    · rcases (show k = 0 ∨ k = 1 by omega) with rfl | rfl
      · exact absurd hw0 hya
      · exact hA _ _ (nx_adj_left (nx_tri htri eF).2) hab (wb 1 hk)
    · rcases Nat.lt_or_ge (k + 2) (d + 1) with hk3 | hk3
      · exact hB k hk2 (by omega)
      · have : k = d - 1 := by omega
        subst this
        exact hA _ _ (nx_adj_right (nx_tri htri eL).1) hab (wb _ hk)

/-- In a graph whose edges all equal `s(u, v)`, reachable vertices are equal or the edge's ends. -/
theorem reachable_one {H : SimpleGraph (Fin n)} {u v : Fin n}
    (hone : ∀ p q, H.Adj p q → s(p, q) = s(u, v)) {x y : Fin n} (h : H.Reachable x y) :
    x = y ∨ s(x, y) = s(u, v) := by
  obtain ⟨W⟩ := h
  induction W with
  | nil => exact Or.inl rfl
  | @cons p r q hpr W ih =>
    have e := hone p r hpr
    rcases ih with rfl | h
    · exact Or.inr e
    · rw [← h] at e
      rcases Sym2.eq_iff.1 e with ⟨h1, -⟩ | ⟨h1, -⟩
      · exact absurd h1 hpr.ne
      · exact Or.inl h1

/-- **C4a for one edge** (no `sorry`). If every edge of `H ≤ T` is the single edge `s(u, v)` and `H`
has an edge, contracting it gives a smaller spherical map `T'` and a vertex map `π` as in
`CGlue.contract_subgraph`. Needs `T` triangulated without separating triangles. -/
theorem contract_subgraph1 (T : SphericalMap n) (htri : T.Triangulated) (hns : NoSep T)
    (H : SimpleGraph (Fin n)) (hH : H ≤ T.graph) {u v : Fin n}
    (hone : ∀ p q, H.Adj p q → s(p, q) = s(u, v)) (hne : ∃ x y, H.Adj x y) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, H.Reachable x y → π x = π y) ∧
      (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y)) := by
  classical
  obtain ⟨a, b, hab⟩ := hne
  have huv : s(a, b) = s(u, v) := hone a b hab
  obtain ⟨T', hlt, hkeep, hnbr⟩ := contract_edge T htri hns (hH hab).symm
  have hone' : ∀ p q, H.Adj p q → s(p, q) = s(a, b) := fun p q h => (hone p q h).trans huv.symm
  let π : Fin n → Fin n := fun x => if x = b then a else x
  have hπab : ∀ x, x = a ∨ x = b → π x = a := by
    rintro x (rfl | rfl)
    · simp [π]
    · simp [π]
  refine ⟨T', π, ?_, ?_, ?_⟩
  · rw [natCard_support_eq, natCard_support_eq]; exact hlt
  · intro x y h
    rcases reachable_one hone' h with rfl | h
    · rfl
    · rcases Sym2.eq_iff.1 h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · rw [hπab x (Or.inl rfl), hπab y (Or.inr rfl)]
      · rw [hπab x (Or.inr rfl), hπab y (Or.inl rfl)]
  · intro x y hxy hr
    have hne : s(x, y) ≠ s(a, b) := by
      intro h
      apply hr
      rcases Sym2.eq_iff.1 h with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
      · exact hab.reachable
      · exact hab.symm.reachable
    by_cases hx : x = b
    · subst hx
      have hy : y ≠ x := hxy.ne.symm
      have hya : y ≠ a := fun h => hne (by rw [h, Sym2.eq_swap])
      simp only [π, if_pos rfl, if_neg hy]
      exact hnbr y hxy hya
    · by_cases hy : y = b
      · subst hy
        have hxa : x ≠ a := fun h => hne (by rw [h])
        simp only [π, if_pos rfl, if_neg hx]
        exact (hnbr x hxy.symm hxa).symm
      · simp only [π, if_neg hx, if_neg hy]
        exact hkeep x y hxy hx hy

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.flip_exists
#print axioms SimpleGraph.SphericalMap.contract_edge
#print axioms SimpleGraph.SphericalMap.contract_subgraph1
