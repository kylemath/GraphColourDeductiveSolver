import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingReduce
import DCheckR2A
import DCheckR2C

/-! Job 19 piece (E), geometric part, and (F): `KempeMatching` for the ring codes realised by
proper colourings of the deleted map `G` of a `ConfigOcc`, and the D-reducibility glue
`ConfigOcc.colorable_of_dReducible`. The only planar input is `chains_noncrossing(_same)`. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill DCheck DCheck.R2

variable {n : ℕ}

/-- XOR of a colour with `θ < 4`. -/
def fx (θ : ℕ) (hθ : θ < 4) (a : Fin 4) : Fin 4 := ⟨a.val ^^^ θ, xor_lt4 _ _ a.isLt hθ⟩

/-- The θ-edge graph: edges of `G` off the hole whose end colours differ by `θ`. -/
def thetaGraph (G : SimpleGraph (Fin n)) (h : Fin n) (c : Fin n → Fin 4) (θ : ℕ) :
    SimpleGraph (Fin n) where
  Adj u v := G.Adj u v ∧ u ≠ h ∧ v ≠ h ∧ (c u).val ^^^ (c v).val = θ
  symm := ⟨fun _ _ e => ⟨e.1.symm, e.2.2.1, e.2.1, by rw [Nat.xor_comm]; exact e.2.2.2⟩⟩
  loopless := ⟨fun _ e => e.1.ne rfl⟩

set_option synthInstance.maxSize 2048 in
set_option synthInstance.maxHeartbeats 400000 in
theorem cls_xor' : ∀ θ, θ < 4 → ∀ x, x < 4 → cls θ (x ^^^ θ) = cls θ x := by decide

theorem cls_xor (θ x : ℕ) (hθ : θ < 4) (hx : x < 4) : cls θ (x ^^^ θ) = cls θ x :=
  cls_xor' θ hθ x hx

theorem xor_back (x y θ : ℕ) (h : x ^^^ y = θ) : x = y ^^^ θ := by
  rw [← h, Nat.xor_comm x y, ← Nat.xor_assoc, Nat.xor_self, Nat.zero_xor]

theorem theta_cls_walk {G : SimpleGraph (Fin n)} {h : Fin n} {c : Fin n → Fin 4} {θ : ℕ} (hθ : θ < 4) :
    ∀ {u v : Fin n} (_ : (thetaGraph G h c θ).Walk u v), cls θ (c u).val = cls θ (c v).val
  | _, _, .nil => rfl
  | _, _, .cons e q => by
    rw [← theta_cls_walk hθ q, xor_back _ _ _ e.2.2.2, cls_xor _ _ hθ (c _).isLt]

theorem theta_cls {G : SimpleGraph (Fin n)} {h : Fin n} {c : Fin n → Fin 4} {θ : ℕ} (hθ : θ < 4)
    {u v : Fin n} (huv : (thetaGraph G h c θ).Reachable u v) : cls θ (c u).val = cls θ (c v).val := by
  obtain ⟨p⟩ := huv; exact theta_cls_walk hθ p

theorem theta_to_pair_walk {G : SimpleGraph (Fin n)} {h : Fin n} {c : Fin n → Fin 4} {θ : ℕ}
    (hθ : θ < 4) (a : Fin 4) : ∀ {w v : Fin n} (_ : (thetaGraph G h c θ).Walk w v), w ≠ h →
      (c w = a ∨ c w = fx θ hθ a) → (pairGraph G h c a (fx θ hθ a)).Reachable w v
  | _, _, .nil, _, _ => Reachable.refl _
  | _, _, @SimpleGraph.Walk.cons _ _ x b _ e q, ha, hca => by
    have hb : (c b).val = (c x).val ^^^ θ := xor_back _ _ _ (by rw [Nat.xor_comm]; exact e.2.2.2)
    have hcb : c b = a ∨ c b = fx θ hθ a := by
      rcases hca with h1 | h1
      · right; apply Fin.ext; rw [hb, h1]; rfl
      · left; apply Fin.ext; rw [hb, h1]; simp [fx, Nat.xor_assoc]
    exact (SimpleGraph.Adj.reachable (G := pairGraph G h c a (fx θ hθ a))
      ⟨e.1, ⟨ha, hca⟩, ⟨e.2.2.1, hcb⟩⟩).trans (theta_to_pair_walk hθ a q e.2.2.1 hcb)

/-- A θ-chain from `u` stays in the colour pair `{c u, c u ⊕ θ}`, as a two-colour chain. -/
theorem theta_to_pair {G : SimpleGraph (Fin n)} {h : Fin n} {c : Fin n → Fin 4} {θ : ℕ}
    (hθ : θ < 4) {u v : Fin n} (hu : u ≠ h) (huv : (thetaGraph G h c θ).Reachable u v) :
    (pairGraph G h c (c u) (fx θ hθ (c u))).Reachable u v := by
  obtain ⟨p⟩ := huv; exact theta_to_pair_walk hθ (c u) p hu (Or.inl rfl)

theorem pair_to_theta_walk {G : SimpleGraph (Fin n)} {h : Fin n} {c : Fin n → Fin 4} {θ : ℕ}
    (hθ : θ < 4) (hc : ProperOff G h c) (a : Fin 4) :
    ∀ {u v : Fin n} (_ : (pairGraph G h c a (fx θ hθ a)).Walk u v), (thetaGraph G h c θ).Reachable u v
  | _, _, .nil => Reachable.refl _
  | _, _, .cons e q => by
    refine (SimpleGraph.Adj.reachable (G := thetaGraph G h c θ)
      ⟨e.1, e.2.1.1, e.2.2.1, ?_⟩).trans (pair_to_theta_walk hθ hc a q)
    have hne := hc e.1 e.2.1.1 e.2.2.1
    rcases e.2.1.2 with h1 | h1 <;> rcases e.2.2.2 with h2 | h2
    · exact absurd (h1.trans h2.symm) hne
    · rw [h1, h2]; simp only [fx]; rw [← Nat.xor_assoc, Nat.xor_self, Nat.zero_xor]
    · rw [h1, h2]; simp only [fx]; rw [Nat.xor_comm, ← Nat.xor_assoc, Nat.xor_self, Nat.zero_xor]
    · exact absurd (h1.trans h2.symm) hne

/-- Conversely a two-colour chain of a proper colouring is a θ-chain. -/
theorem pair_to_theta {G : SimpleGraph (Fin n)} {h : Fin n} {c : Fin n → Fin 4} {θ : ℕ}
    (hθ : θ < 4) (hc : ProperOff G h c) {a : Fin 4} {u v : Fin n}
    (huv : (pairGraph G h c a (fx θ hθ a)).Reachable u v) : (thetaGraph G h c θ).Reachable u v := by
  obtain ⟨p⟩ := huv; exact pair_to_theta_walk hθ hc a p

theorem pairGraph_comm (G : SimpleGraph (Fin n)) (h : Fin n) (c : Fin n → Fin 4) (a b : Fin 4) :
    pairGraph G h c a b = pairGraph G h c b a := by
  ext u v
  simp only [pairGraph, Active]
  constructor <;> rintro ⟨e, ⟨h1, h2⟩, ⟨h3, h4⟩⟩ <;> exact ⟨e, ⟨h1, h2.symm⟩, ⟨h3, h4.symm⟩⟩

theorem fx_fx (θ : ℕ) (hθ : θ < 4) (a : Fin 4) : fx θ hθ (fx θ hθ a) = a := by
  apply Fin.ext; simp [fx, Nat.xor_assoc]

set_option synthInstance.maxSize 2048 in
set_option synthInstance.maxHeartbeats 400000 in
theorem cls_eq_cases' : ∀ θ, θ < 4 → ∀ x, x < 4 → ∀ y, y < 4 →
    (cls θ x = cls θ y → (y = x ∨ y = x ^^^ θ)) ∧ ((y = x ∨ y = x ^^^ θ) → cls θ x = cls θ y) := by
  decide

set_option synthInstance.maxSize 2048 in
set_option synthInstance.maxHeartbeats 400000 in
theorem disj_pairs' : ∀ θ, θ < 4 → ∀ x, x < 4 → ∀ y, y < 4 → ∀ z, z < 4 →
    (cls θ x ≠ cls θ y ∧ (z = x ∨ z = x ^^^ θ) ∧ (z = y ∨ z = y ^^^ θ)) → False := by
  decide

variable {T G : SphericalMap n} {r m : ℕ} {ρ : ℕ → Fin n} {ι : Fin m → Fin n}
  {intAdj : Fin m → Fin m → Bool} {ringAdj : Fin m → ℕ → Bool}

/-- **Non-crossing of ring chains** in the form used by `abstract_matching`. -/
theorem ConfigOcc.theta_nc (O : ConfigOcc T G r m ρ ι intAdj ringAdj) {c : Fin n → Fin 4}
    (hc : ProperOff G.graph O.hole c) {θ : ℕ} (hθ : θ < 4) {i j k l : ℕ} (hij : i < j) (hjk : j < k)
    (hkl : k < l) (hlr : l < r)
    (h1 : (thetaGraph G.graph O.hole c θ).Reachable (ρ i) (ρ k))
    (h2 : (thetaGraph G.graph O.hole c θ).Reachable (ρ j) (ρ l)) :
    (thetaGraph G.graph O.hole c θ).Reachable (ρ i) (ρ j) := by
  have p1 := theta_to_pair hθ (O.ring_ne_hole i) h1
  have p2 := theta_to_pair hθ (O.ring_ne_hole j) h2
  by_cases hcl : cls θ (c (ρ i)).val = cls θ (c (ρ j)).val
  · -- same pair: chains_noncrossing_same
    by_contra hne
    have hy := (cls_eq_cases' θ hθ _ (c (ρ i)).isLt _ (c (ρ j)).isLt).1 hcl
    have hpair : pairGraph G.graph O.hole c (c (ρ j)) (fx θ hθ (c (ρ j))) =
        pairGraph G.graph O.hole c (c (ρ i)) (fx θ hθ (c (ρ i))) := by
      rcases hy with hy | hy
      · rw [Fin.ext hy]
      · have : c (ρ j) = fx θ hθ (c (ρ i)) := Fin.ext hy
        rw [this, fx_fx, pairGraph_comm]
    rw [hpair] at p2
    exact chains_noncrossing_same O.ring hij hjk hkl hlr p1 p2
      (fun hr => hne (pair_to_theta hθ hc hr))
  · exfalso
    refine chains_noncrossing O.ring (a := c (ρ i)) (b := fx θ hθ (c (ρ i)))
      (a' := c (ρ j)) (b' := fx θ hθ (c (ρ j))) ?_ hij hjk hkl hlr p1 p2
    intro z hz1 hz2
    apply disj_pairs' θ hθ _ (c (ρ i)).isLt _ (c (ρ j)).isLt _ z.isLt
    refine ⟨hcl, ?_, ?_⟩
    · rcases hz1 with rfl | rfl
      · exact Or.inl rfl
      · exact Or.inr rfl
    · rcases hz2 with rfl | rfl
      · exact Or.inl rfl
      · exact Or.inr rfl

/-- The ring colour sequence of a colouring. -/
def ringSeq (ρ : ℕ → Fin n) (c : Fin n → Fin 4) : ℕ → ℕ := fun t => (c (ρ t)).val

theorem ringSeq_lt (ρ : ℕ → Fin n) (c : Fin n → Fin 4) (t : ℕ) : ringSeq ρ c t < 4 := (c (ρ t)).isLt

theorem code_congr (f g : ℕ → ℕ) : ∀ r, (∀ t, t < r → f t = g t) → code f r = code g r := by
  intro r
  induction r with
  | zero => intro _; rfl
  | succ r ih =>
    intro h
    show code f r ||| (f r <<< (2 * r)) = code g r ||| (g r <<< (2 * r))
    rw [ih (fun t ht => h t (by omega)), h r (by omega)]

theorem ConfigOcc.ring_per (O : ConfigOcc T G r m ρ ι intAdj ringAdj) (v : ℕ) :
    ρ ((v + 1) % r) = ρ (v + 1) ∨ v + 1 ≥ r := by
  by_cases h : v + 1 < r
  · left; rw [Nat.mod_eq_of_lt h]
  · right; omega

/-- **R2: `KempeMatching`** for the ring codes of proper colourings of `G` (rings `r ≤ 15`). -/
theorem ConfigOcc.kempeMatching (O : ConfigOcc T G r m ρ ι intAdj ringAdj) (cf : Conf)
    (hr : cf.r = r) (hr15 : r ≤ 15) :
    KempeMatching cf (fun k => ∃ c : Fin n → Fin 4, ProperOff G.graph O.hole c ∧
      k = code (ringSeq ρ c) r) := by
  classical
  intro k θ ⟨c, hc, hk⟩ hθ1 hθ3 hT
  subst hk
  rw [hr] at hT ⊢
  have hθ : θ < 4 := by omega
  set f := ringSeq ρ c with hfdef
  have hf : ∀ t, f t < 4 := ringSeq_lt ρ c
  have hr1 : 1 ≤ r := O.ring.pos
  let E : ℕ → ℕ → Prop := fun t t' => (thetaGraph G.graph O.hole c θ).Reachable (ρ t) (ρ t')
  have hE : Equivalence E :=
    ⟨fun _ => Reachable.refl _, fun h => h.symm, fun h1 h2 => h1.trans h2⟩
  have hstep : ∀ v, v < r → tPred r (code f r) θ v = false → E v ((v + 1) % r) := by
    intro v hv htp
    have hwrap : ρ ((v + 1) % r) = ρ (v + 1) := by
      by_cases h : v + 1 < r
      · rw [Nat.mod_eq_of_lt h]
      · rw [show v + 1 = r by omega, Nat.mod_self, show r = 0 + r by omega, O.ring.per 0]
    unfold tPred at htp
    rw [col_code f hf r v hv, col_code f hf r _ (Nat.mod_lt _ (by omega))] at htp
    simp only [Bool.and_eq_false_iff, bne_eq_false_iff_eq] at htp
    have hne : c (ρ v) ≠ c (ρ (v + 1)) := O.ring_proper hc v
    show (thetaGraph G.graph O.hole c θ).Reachable (ρ v) (ρ ((v + 1) % r))
    rw [hwrap]
    rcases htp with h0 | h0
    · exfalso; apply hne; apply Fin.ext
      have : f v = f ((v + 1) % r) := by
        have := congrArg (· ^^^ f ((v + 1) % r)) h0
        simpa [Nat.xor_assoc] using this
      rw [hfdef] at this; simp only [ringSeq] at this; rw [this, hwrap]
    · refine Adj.reachable ⟨O.ring.adj v, O.ring_ne_hole v, O.ring_ne_hole (v + 1), ?_⟩
      rw [hfdef] at h0; simp only [ringSeq] at h0; rw [hwrap] at h0; exact h0
  have hEcls : ∀ u w, u < r → w < r → E u w → cls θ (f u) = cls θ (f w) :=
    fun u w _ _ h => theta_cls hθ h
  have hNC : ∀ i j k l, i < j → j < k → k < l → l < r → E i k → E j l → E i j :=
    fun i j k l hij hjk hkl hlr h1 h2 => O.theta_nc hc hθ hij hjk hkl hlr h1 h2
  have hn : (TL r θ f).length ≠ 0 := by rw [← transitions_size]; exact hT
  obtain ⟨lab, hlab, hlabE⟩ := abstract_matching r θ f E hE hf hθ1 hθ3 hstep hEcls hNC hr1 hr15 hn
  refine ⟨lab, hlab, fun s => ?_⟩
  -- the flip
  let sel : ℕ → Bool := fun t => decide (lab[arcOf (transitions r (code f r) θ) t]! ≠ 0) &&
    s.testBit (lab[arcOf (transitions r (code f r) θ) t]! - 1)
  let S : Fin n → Prop := fun v => ∃ t, t < r ∧ sel t = true ∧
    (thetaGraph G.graph O.hole c θ).Reachable (ρ t) v
  let c' : Fin n → Fin 4 := fun v => if S v then fx θ hθ (c v) else c v
  refine ⟨c', ?_, ?_⟩
  · intro u v huv hu hv
    have hne := hc huv hu hv
    by_cases hSu : S u <;> by_cases hSv : S v <;> simp only [c', hSu, hSv, if_true, if_false]
    · intro heq; apply hne; rw [← fx_fx θ hθ (c u), heq, fx_fx]
    · intro heq; apply hSv
      obtain ⟨t, ht, hst, hreach⟩ := hSu
      refine ⟨t, ht, hst, hreach.trans (Adj.reachable ⟨huv, hu, hv, ?_⟩)⟩
      rw [← heq]; simp [fx, ← Nat.xor_assoc]
    · intro heq; apply hSu
      obtain ⟨t, ht, hst, hreach⟩ := hSv
      refine ⟨t, ht, hst, hreach.trans (Adj.reachable ⟨huv.symm, hv, hu, ?_⟩)⟩
      rw [heq]; simp [fx, ← Nat.xor_assoc]
    · exact hne
  · have hS : ∀ t, t < r → (S (ρ t) ↔ sel t = true) := by
      intro t ht
      constructor
      · rintro ⟨t', ht', hst', hreach⟩
        have := hlabE t' t ht' ht hreach
        simp only [sel] at hst' ⊢
        rw [← this]; exact hst'
      · intro hs; exact ⟨t, ht, hs, Reachable.refl _⟩
    rw [← flip_code r θ f hf hθ lab s sel (fun t _ => rfl)]
    apply code_congr
    intro t ht
    simp only [ringSeq, c']
    by_cases hst : sel t = true
    · rw [if_pos ((hS t ht).2 hst), if_pos hst]; rfl
    · rw [if_neg (fun h => hst ((hS t ht).1 h)), if_neg hst]; rfl

/-- Adjacency tables of a `Conf` as Boolean relations. -/
def intAdjOf (cf : Conf) (a b : Fin cf.m) : Bool := decide (b.val ∈ cf.intAdj[a.val]!)
def ringAdjOf (cf : Conf) (a : Fin cf.m) (t : ℕ) : Bool := decide (t ∈ cf.ringAdj[a.val]!)

/-- **(F) D-reducibility glue.** A configuration accepted by `DCheck.dReducible`, occurring in `T`
with the deleted map `G` colourable off the hole, makes `T` 4-colourable (rings `2 ≤ r ≤ 15`). -/
theorem ConfigOcc.colorable_of_dReducible (cf : Conf) (hD : dReducible cf = true)
    (hr2 : 2 ≤ cf.r) (hr15 : cf.r ≤ 15)
    (hsym : ∀ a b, intAdjOf cf a b = true → intAdjOf cf b a = true)
    (hloop : ∀ a, intAdjOf cf a a = false)
    {ρ : ℕ → Fin n} {ι : Fin cf.m → Fin n}
    (O : ConfigOcc T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
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
  obtain ⟨k', ⟨c', hc', rfl⟩, hext⟩ := dReducible_sound cf hD hr2 P hcanon
    (O.kempeMatching cf rfl hr15) hprop _ ⟨c, hc, rfl⟩
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

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.ConfigOcc.kempeMatching
#print axioms SimpleGraph.SphericalMap.ConfigOcc.colorable_of_dReducible
