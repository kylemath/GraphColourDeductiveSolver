import CGlue

/-!
# COccBridge: `OccExact`, `NbrInj` and `ApexFacts` from the rotation at interior vertices (Long Table, 19 Oct 2026)

The unavoidability side produces rotation occurrences (occ24's `Occ`, and its face-walk form from
`gen_occ_walk.py`, Job 26):
- interior vertices are injective and disjoint from the ring;
- every interior vertex has its true degree;
- the rotation of `T` at every interior vertex is the free-completion rotation (`Nx` facts).

`RotOcc` is the generic form: `rot a` lists the neighbour slots of interior vertex `a` (interior `inl b`
or ring position `inr t`) in rotation order, and `T`'s rotation step at `ι a` sends slot `k + 1` to slot
`k`. `rotOK` (decidable, per key) checks that `rot` lists exactly the configuration's neighbours and that
a ring slot next to an interior slot `b` is a ring neighbour of `b` (the free completion's triangles).

From these, with no other hypothesis on `T`:
- `RotOcc.occExact`: every listed adjacency is an edge of `T`.
- `RotOcc.nbrInj`: the listed ring neighbours of one interior vertex are distinct vertices of `T`.
  They are distinct entries of one full rotation at a vertex of the given degree (`chain_inj`).
- `RotOcc.apexFacts`: a facial apex on a listed interior edge is a configuration vertex. It is the
  rotation step at one end (`nx_func`), so it is the neighbouring slot of the configuration's rotation.
- `occursCXF_of_rot`: a `ConfigOccW` with a `RotOcc` and `rotOK` is an `OccursCXF`.
-/

namespace SimpleGraph.SphericalMap
open VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ}

/-- The vertex of `T` at a neighbour slot. -/
def slotV {m : ℕ} (ρ : ℕ → Fin n) (ι : Fin m → Fin n) : Fin m ⊕ ℕ → Fin n
  | .inl b => ι b
  | .inr t => ρ t

/-- **Rotation occurrence**: the per-vertex rotation of `T` at interior vertices is `rot`. -/
structure RotOcc (T : SphericalMap n) {m : ℕ} (ρ : ℕ → Fin n) (ι : Fin m → Fin n)
    (rot : Fin m → List (Fin m ⊕ ℕ)) : Prop where
  ιinj : Function.Injective ι
  disj : ∀ t a, ρ t ≠ ι a
  deg : ∀ a, T.graph.degree (ι a) = (rot a).length
  nx : ∀ a k, k < (rot a).length →
    Nx T (ι a) (slotV ρ ι ((rot a).getD ((k + 1) % (rot a).length) (.inr 0)))
      (slotV ρ ι ((rot a).getD k (.inr 0)))

/-- The slot is a listed neighbour (interior or ring) of `a`. -/
def slotListed (cf : Conf) (a : ℕ) : Fin cf.m ⊕ ℕ → Bool
  | .inl b => decide (b.val ∈ cf.intAdj[a]!)
  | .inr t => decide (t ∈ cf.ringAdj[a]!)

/-- A ring slot just before an interior slot `b` is a ring neighbour of `b`. -/
def slotTri (cf : Conf) : Fin cf.m ⊕ ℕ → Fin cf.m ⊕ ℕ → Bool
  | .inl b, .inr p => decide (p ∈ cf.ringAdj[b.val]!)
  | _, _ => true

/-- **Rotation data check** (decidable, per key). -/
def rotOK (cf : Conf) (rot : Fin cf.m → List (Fin cf.m ⊕ ℕ)) : Bool :=
  (List.finRange cf.m).all fun a =>
    (cf.intAdj[a.val]!).toList.all (fun b => (rot a).any (fun s => match s with
      | .inl c => c.val == b
      | .inr _ => false)) &&
    (cf.ringAdj[a.val]!).toList.all (fun t => decide (t < cf.r) && (rot a).contains (.inr t)) &&
    (rot a).all (slotListed cf a.val) &&
    (List.range (rot a).length).all (fun k =>
      slotTri cf ((rot a).getD ((k + 1) % (rot a).length) (.inr 0)) ((rot a).getD k (.inr 0)))

section
variable {T : SphericalMap n} {cf : Conf} {ρ : ℕ → Fin n} {ι : Fin cf.m → Fin n}
  {rot : Fin cf.m → List (Fin cf.m ⊕ ℕ)}

theorem rotOK_spec (h : rotOK cf rot = true) (a : Fin cf.m) :
    (∀ b ∈ cf.intAdj[a.val]!, ∃ c : Fin cf.m, c.val = b ∧ .inl c ∈ rot a) ∧
    (∀ t ∈ cf.ringAdj[a.val]!, t < cf.r ∧ .inr t ∈ rot a) ∧
    (∀ s ∈ rot a, slotListed cf a.val s = true) ∧
    (∀ k, k < (rot a).length →
      slotTri cf ((rot a).getD ((k + 1) % (rot a).length) (.inr 0)) ((rot a).getD k (.inr 0)) = true) := by
  simp only [rotOK, List.all_eq_true, List.mem_finRange, true_implies, Bool.and_eq_true,
    Array.mem_toList_iff, List.any_eq_true, decide_eq_true_eq, List.contains_iff_mem,
    List.mem_range] at h
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h a
  refine ⟨fun b hb => ?_, fun t ht => h2 t ht, h3, h4⟩
  obtain ⟨s, hs, e⟩ := h1 b hb
  match s, e with
  | .inl c, e => exact ⟨c, by simpa using e, hs⟩

theorem getD_mem_rot {l : List (Fin cf.m ⊕ ℕ)} {k : ℕ} (hk : k < l.length) : l.getD k (.inr 0) ∈ l := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hk, Option.getD_some]
  exact List.getElem_mem hk

theorem exists_idx {l : List (Fin cf.m ⊕ ℕ)} {s : Fin cf.m ⊕ ℕ} (h : s ∈ l) :
    ∃ j, j < l.length ∧ l.getD j (.inr 0) = s := by
  obtain ⟨j, hj, e⟩ := List.mem_iff_getElem.1 h
  exact ⟨j, hj, by rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hj, Option.getD_some, e]⟩

/-- The step into slot `j`: the rotation at `ι a` sends slot `j` to the slot before it. -/
theorem RotOcc.nx_at (R : RotOcc T ρ ι rot) (a : Fin cf.m) {j : ℕ} (hj : j < (rot a).length) :
    Nx T (ι a) (slotV ρ ι ((rot a).getD j (.inr 0)))
      (slotV ρ ι ((rot a).getD ((j + (rot a).length - 1) % (rot a).length) (.inr 0))) := by
  have hk := Nat.mod_lt (j + (rot a).length - 1) (show 0 < (rot a).length by omega)
  have h := R.nx a _ hk
  have e : ((j + (rot a).length - 1) % (rot a).length + 1) % (rot a).length = j := by
    rw [Nat.add_mod, Nat.mod_mod, ← Nat.add_mod, show j + (rot a).length - 1 + 1 = j + (rot a).length by omega,
      Nat.add_mod_right, Nat.mod_eq_of_lt hj]
  rwa [e] at h

theorem RotOcc.adj_of_mem (R : RotOcc T ρ ι rot) (a : Fin cf.m) {s : Fin cf.m ⊕ ℕ} (hs : s ∈ rot a) :
    T.Adj (ι a) (slotV ρ ι s) := by
  obtain ⟨j, hj, rfl⟩ := exists_idx hs
  exact nx_adj_left (R.nx_at a hj)

/-- **`OccExact` from the rotation.** -/
theorem RotOcc.occExact (R : RotOcc T ρ ι rot) (h : rotOK cf rot = true) :
    OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf) := by
  refine ⟨fun a b hab => ?_, fun a t _ hat => ?_⟩
  · obtain ⟨c, hc, hm⟩ := (rotOK_spec h a).1 b.val (of_decide_eq_true hab)
    have := R.adj_of_mem a hm
    rwa [show c = b from Fin.ext hc] at this
  · exact R.adj_of_mem a ((rotOK_spec h a).2.1 t (of_decide_eq_true hat)).2

/-- **`NbrInj` from the rotation and the true degree.** -/
theorem RotOcc.nbrInj (R : RotOcc T ρ ι rot) (h : rotOK cf rot = true) :
    NbrInj cf.r ρ (ringAdjOf cf) := by
  intro c p q hp hq _ _ e
  obtain ⟨-, hpm⟩ := (rotOK_spec h c).2.1 p (of_decide_eq_true hp)
  obtain ⟨-, hqm⟩ := (rotOK_spec h c).2.1 q (of_decide_eq_true hq)
  obtain ⟨i, hi, ei⟩ := exists_idx hpm
  obtain ⟨j, hj, ej⟩ := exists_idx hqm
  set d := (rot c).length with hd
  let S : ℕ → Fin n := fun k => slotV ρ ι ((rot c).getD k (.inr 0))
  let x : ℕ → Fin n := fun k => S ((d - k) % d)
  have h0 : T.Adj (ι c) (x 0) := R.adj_of_mem c (getD_mem_rot (Nat.mod_lt _ (by omega)))
  have hch : ∀ k, k + 1 < d → Nx T (ι c) (x k) (x (k + 1)) := by
    intro k hk
    have := R.nx c (d - k - 1) (by omega)
    have e1 : (d - k - 1 + 1) % d = (d - k) % d := by rw [show d - k - 1 + 1 = d - k by omega]
    have e2 : (d - (k + 1)) % d = d - k - 1 := by
      rw [show d - (k + 1) = d - k - 1 by omega, Nat.mod_eq_of_lt (by omega)]
    rw [e1] at this
    show Nx T (ι c) (S ((d - k) % d)) (S ((d - (k + 1)) % d))
    rw [e2]; exact this
  have inj := chain_inj (R.deg c) h0 hch
  have xi : ∀ i, i < d → x ((d - i) % d) = S i := fun i hi => by
    show S ((d - (d - i) % d) % d) = S i
    congr 1
    rcases Nat.eq_zero_or_pos i with rfl | hi0
    · simp
    · rw [Nat.mod_eq_of_lt (show d - i < d by omega), show d - (d - i) = i by omega, Nat.mod_eq_of_lt hi]
  have hxe : x ((d - i) % d) = x ((d - j) % d) := by
    rw [xi i hi, xi j hj]; show slotV ρ ι _ = slotV ρ ι _; rw [ei, ej]; exact e
  have := inj _ _ (Nat.mod_lt _ (by omega)) (Nat.mod_lt _ (by omega)) hxe
  have hij : i = j := by
    rcases Nat.eq_zero_or_pos i with rfl | hi0 <;> rcases Nat.eq_zero_or_pos j with rfl | hj0
    · rfl
    · rw [Nat.sub_zero, Nat.mod_self, Nat.mod_eq_of_lt (show d - j < d by omega)] at this; omega
    · rw [Nat.sub_zero, Nat.mod_self, Nat.mod_eq_of_lt (show d - i < d by omega)] at this; omega
    · rw [Nat.mod_eq_of_lt (show d - i < d by omega), Nat.mod_eq_of_lt (show d - j < d by omega)] at this
      omega
  subst hij
  rw [ei] at ej
  exact Sum.inr_injective ej

/-- The apex on a listed interior edge `c a`, seen from `c`. -/
theorem RotOcc.apex_from (R : RotOcc T ρ ι rot) (h : rotOK cf rot = true) {c a : Fin cf.m}
    (hca : intAdjOf cf c a = true) {w : Fin n} (hw : Nx T (ι c) (ι a) w) :
    (∃ e, w = ι e) ∨ ∃ p, p < cf.r ∧ w = ρ p ∧ ringAdjOf cf c p = true ∧ ringAdjOf cf a p = true := by
  obtain ⟨c', hc', hm⟩ := (rotOK_spec h c).1 a.val (of_decide_eq_true hca)
  rw [show c' = a from Fin.ext hc'] at hm
  obtain ⟨j, hj, ej⟩ := exists_idx hm
  have hnx := R.nx_at c hj
  rw [ej] at hnx
  have hw' := nx_func hw hnx
  set k := (j + (rot c).length - 1) % (rot c).length
  have hk : k < (rot c).length := Nat.mod_lt _ (by omega)
  have htri := (rotOK_spec h c).2.2.2 k hk
  have hkj : (k + 1) % (rot c).length = j := by
    show ((j + (rot c).length - 1) % (rot c).length + 1) % (rot c).length = j
    rw [Nat.add_mod, Nat.mod_mod, ← Nat.add_mod, show j + (rot c).length - 1 + 1 = j + (rot c).length by omega,
      Nat.add_mod_right, Nat.mod_eq_of_lt hj]
  rw [hkj, ej] at htri
  have hlist := (rotOK_spec h c).2.2.1 _ (getD_mem_rot hk)
  revert hw' htri hlist
  cases (rot c).getD k (.inr 0) with
  | inl e => intro hw' _ _; exact Or.inl ⟨e, hw'⟩
  | inr p =>
    intro hw' htri hlist
    have hpc : p ∈ cf.ringAdj[c.val]! := of_decide_eq_true hlist
    exact Or.inr ⟨p, ((rotOK_spec h c).2.1 p hpc).1, hw', decide_eq_true hpc, htri⟩

/-- **`ApexFacts` from the rotation** (with the configuration's adjacency symmetric). -/
theorem RotOcc.apexFacts (R : RotOcc T ρ ι rot) (h : rotOK cf rot = true)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true) :
    ApexFacts T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf) := by
  intro c a hca w hw
  rcases hw with hw | hw
  · rcases R.apex_from h (hsym _ _ hca) hw with he | ⟨p, hp, hwp, h1, h2⟩
    · exact Or.inl he
    · exact Or.inr ⟨p, hp, hwp, h2, h1⟩
  · exact R.apex_from h hca hw

end

namespace CGlue
open ClaimGlue (DEntry OccursW Internally6)

/-- **The C occurrence from a rotation occurrence.** A face-walk occurrence (`ConfigOccW`) whose
interior rotation is `rot` (`RotOcc`), with `rot` checked against the configuration, is an
`OccursCXF`: `OccExact`, `NbrInj` and `ApexFacts` are derived. -/
theorem occursCXF_of_rot (e : CEntry) {T G : SphericalMap n} {ρ : ℕ → Fin n}
    {ι : Fin e.cf.m → Fin n} {rot : Fin (Conf.of18 e.cf).m → List (Fin (Conf.of18 e.cf).m ⊕ ℕ)}
    (O : ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (R : RotOcc T ρ ι rot) (h : rotOK (Conf.of18 e.cf) rot = true) : OccursCXF e T :=
  ⟨G, ρ, ι, O, R.occExact h, R.nbrInj h, R.apexFacts h e.hsym⟩

/-- **C occurrence in the rotation format.** A face-walk occurrence whose interior rotation is some
`rot` that passes `rotOK`. The local facts of `OccursCXF` are not assumed. -/
def OccursCXR (e : CEntry) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin e.cf.m → Fin n)
    (rot : Fin (Conf.of18 e.cf).m → List (Fin (Conf.of18 e.cf).m ⊕ ℕ)),
    ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    RotOcc T ρ ι rot ∧ rotOK (Conf.of18 e.cf) rot = true

theorem OccursCXR.toF {e : CEntry} {T : SphericalMap n} (h : OccursCXR e T) : OccursCXF e T := by
  obtain ⟨G, ρ, ι, rot, O, R, hr⟩ := h
  exact occursCXF_of_rot e O R hr

/-- A registry of D entries and fold-safe C entries, with C occurrences in the rotation format. -/
structure RegistryR where
  D : List DEntry
  CF : List CEntryF

def RegistryR.Contains (R : RegistryR) (T : SphericalMap n) : Prop :=
  (∃ e ∈ R.D, OccursW e.cf T) ∨ (∃ e ∈ R.CF, OccursCXR e.toCEntry T)

def UnavoidableR (R : RegistryR) : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), Internally6 T → R.Contains T

/-- **Claim glue with the C side's local facts derived.** The one open link is `UnavoidableR R`:
D occurrences as before, and C occurrences given as a face walk plus the interior rotation. -/
theorem four_color_of_unavoidableCR (R : RegistryR) (hU : UnavoidableR R) {n : ℕ}
    (M : SphericalMap n) : M.graph.Colorable 4 :=
  four_color_of_unavoidableCF ⟨R.D, R.CF⟩ (fun m T hT => by
    rcases hU m T hT with h | ⟨e, he, h⟩
    · exact Or.inl h
    · exact Or.inr ⟨e, he, h.toF⟩) M

/-- The free-completion rotation of the 66666 wheel (`gen_occ_key.rotation`). -/
def rot66666 : Fin 6 → List (Fin 6 ⊕ ℕ) :=
  ![[.inl 1, .inl 5, .inl 4, .inl 3, .inl 2], [.inr 9, .inl 5, .inl 0, .inl 2, .inr 1, .inr 0],
    [.inl 1, .inl 0, .inl 3, .inr 3, .inr 2, .inr 1], [.inr 3, .inl 2, .inl 0, .inl 4, .inr 5, .inr 4],
    [.inr 5, .inl 3, .inl 0, .inl 5, .inr 7, .inr 6], [.inl 4, .inl 0, .inl 1, .inr 9, .inr 8, .inr 7]]

theorem rot66666_ok : rotOK (Conf.of18 cf66666) rot66666 = true := by
  native_decide

/-- **Bridge test for `e66666F`**: a face-walk occurrence with the wheel's interior rotation is an
`OccursCXF`, so `CEntryF.colorable` applies with nothing assumed beyond the rotation occurrence. -/
theorem e66666F_occurs {T G : SphericalMap n} {ρ : ℕ → Fin n} {ι : Fin 6 → Fin n}
    (O : ConfigOccW T G 10 6 ρ ι (intAdjOf (Conf.of18 cf66666)) (ringAdjOf (Conf.of18 cf66666)))
    (R : RotOcc T ρ ι rot66666) : OccursCXF e66666F.toCEntry T :=
  occursCXF_of_rot e66666F.toCEntry O R rot66666_ok

end CGlue
end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.RotOcc.occExact
#print axioms SimpleGraph.SphericalMap.RotOcc.nbrInj
#print axioms SimpleGraph.SphericalMap.RotOcc.apexFacts
#print axioms SimpleGraph.SphericalMap.CGlue.occursCXF_of_rot
#print axioms SimpleGraph.SphericalMap.CGlue.e66666F_occurs
#print axioms SimpleGraph.SphericalMap.CGlue.four_color_of_unavoidableCR
