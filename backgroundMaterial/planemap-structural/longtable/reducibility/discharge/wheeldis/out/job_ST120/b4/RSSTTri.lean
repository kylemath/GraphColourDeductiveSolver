import RSSTView

/-!
# ST-120 B4 (M3, pure part): the three-valued fit semantics of B2 is sound for any filling

Studio, 10 Nov. Core Lean only (like B2). If a `PSpokeView` *approximates* a fully known `SpokeView` (same spoke letter;
hat unknown or equal; fans of equal number and each unknown or equal, except that nothing is asked of the fans of a 9+
spoke), then B2's `Part.fit3At` is *sound* for the Bool `Part.fitsAt`: `sure` implies the fit holds and `no` implies it
fails. Hypothesis on the part: every subpart with a non-`*` fan has a spoke range that excludes 9 and is not `*`
(`Sub.Good`; it follows from B2's `Part.wellShaped`, spec §3.2 last sentence).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed

/-- `t` is a sound three-valued verdict for the Bool `b`. -/
abbrev Tri.Sound (t : Tri) (b : Bool) : Prop := (t = .sure → b = true) ∧ (t = .no → b = false)

theorem Tri.sound_and {t1 t2 : Tri} {b1 b2 : Bool} (h1 : t1.Sound b1) (h2 : t2.Sound b2) :
    (t1.and t2).Sound (b1 && b2) := by
  revert h1 h2
  cases t1 <;> cases t2 <;> cases b1 <;> cases b2 <;> decide

theorem Tri.sound_ofBool (b : Bool) : (Tri.ofBool b).Sound b := by
  cases b <;> decide

theorem Tri.sound_sure : Tri.Sound .sure true := by decide

theorem Rng.sound_test3 (r : Rng) {o : Option Nat} {x : Nat} (h : o = none ∨ o = some x) :
    (r.test3 o).Sound (r.isFull || r.test x) := by
  rcases h with rfl | rfl
  · cases hf : r.isFull <;> simp [Rng.test3, hf] <;> constructor <;> intro h <;> first | rfl | cases h
  · exact Tri.sound_ofBool _

theorem Tri.sound_foldl {α : Type} (F : α → Tri) (G : α → Bool) :
    ∀ (L : List α), (∀ a ∈ L, (F a).Sound (G a)) → ∀ (acc : Tri) (b : Bool), acc.Sound b →
      (L.foldl (fun acc a => acc.and (F a)) acc).Sound (b && L.all G) := by
  intro L
  induction L with
  | nil => intro _ acc b h; simpa using h
  | cons a L ih =>
    intro hL acc b h
    simp only [List.foldl_cons, List.all_cons]
    rw [← Bool.and_assoc]
    exact ih (fun x hx => hL x (List.mem_cons_of_mem _ hx)) _ _
      (Tri.sound_and h (hL a List.mem_cons_self))

/-- Pointwise approximation of a known fan list. -/
def FansApprox (pfs : List (Option Nat)) (fs : List Nat) : Prop :=
  pfs.length = fs.length ∧ ∀ (k : Nat) (x : Nat), fs[k]? = some x → pfs[k]? = some none ∨ pfs[k]? = some (some x)

theorem sound_fans (rs : List Rng) : ∀ (pfs : List (Option Nat)) (fs : List Nat), FansApprox pfs fs →
    ∀ (acc : Tri) (b : Bool), acc.Sound b →
    ((rs.zip pfs).foldl (fun acc rx => acc.and (rx.1.test3 rx.2)) acc).Sound
      (b && (rs.zip fs).all fun rx => rx.1.isFull || rx.1.test rx.2) := by
  induction rs with
  | nil => intro pfs fs _ acc b h; simpa using h
  | cons r rs ih =>
    intro pfs fs hA acc b h
    obtain ⟨hl, hp⟩ := hA
    cases pfs with
    | nil =>
      cases fs with
      | nil => simpa using h
      | cons _ _ => simp at hl
    | cons p pfs =>
      cases fs with
      | nil => simp at hl
      | cons f fs =>
        simp only [List.zip_cons_cons, List.foldl_cons, List.all_cons]
        rw [← Bool.and_assoc]
        refine ih pfs fs ⟨by simpa using hl, fun k x hx => ?_⟩ _ _ (Tri.sound_and h (Rng.sound_test3 r ?_))
        · have := hp (k + 1) x (by simpa using hx)
          simpa using this
        · have := hp 0 f (by simp)
          simpa using this

/-- What a fit needs of a subpart for the 9+ exemption: all fans `*`, or a spoke range that is not `*` and excludes 9. -/
def Sub.Good (s : Sub) : Prop :=
  s.fans.all Rng.isFull = true ∨ (s.spoke.isFull = false ∧ s.spoke.test 9 = false)

/-- `pv` approximates the known view `v`: same spoke letter, hat unknown or equal, and (unless the spoke is 9+) fans
pointwise unknown or equal. -/
def Approx (pv : PSpokeView) (v : SpokeView) : Prop :=
  pv.spoke = v.spoke ∧ (pv.hat = none ∨ pv.hat = some v.hat) ∧ (v.spoke = 9 ∨ FansApprox pv.fans v.fans)

theorem Tri.sound_and_no {t1 t2 : Tri} {b1 b2 : Bool} (h1 : t1 = .no) (h2 : b1 = false) :
    (t1.and t2).Sound (b1 && b2) := by
  subst h1 h2; cases t2 <;> cases b2 <;> decide

theorem sound_sub {s : Sub} (hs : s.Good) {pv : PSpokeView} {v : SpokeView} (ha : Approx pv v) :
    (s.fit3 pv).Sound (s.fits v) := by
  obtain ⟨hsp, hhat, hfan⟩ := ha
  unfold Sub.fit3 Sub.fits
  rw [hsp, Bool.and_assoc]
  by_cases hf : s.fans.all Rng.isFull = true
  · refine Tri.sound_and (Tri.sound_ofBool _) (Tri.sound_and (Rng.sound_test3 _ hhat) ?_)
    simp only [hf, ↓reduceIte, Bool.true_or]; exact Tri.sound_sure
  have hf' : s.fans.all Rng.isFull = false := by simpa using hf
  rcases hfan with h9 | hA
  · -- 9+ spoke with a constrained fan: the spoke test fails on both sides
    rcases hs with hs | ⟨hfull, h9'⟩
    · exact absurd hs hf
    · exact Tri.sound_and_no (by rw [h9, hfull, h9']; rfl) (by rw [h9, hfull, h9']; rfl)
  · refine Tri.sound_and (Tri.sound_ofBool _) (Tri.sound_and (Rng.sound_test3 _ hhat) ?_)
    simp only [hf', Bool.false_eq_true, ↓reduceIte, Bool.false_or]
    by_cases hl : s.fans.length = v.fans.length
    · have hl' : (s.fans.length != pv.fans.length) = false := by rw [hA.1]; simp [hl]
      rw [hl']
      have hl2 : (s.fans.length == v.fans.length) = true := by simp [hl]
      rw [hl2]
      simp only [Bool.false_eq_true, ↓reduceIte, Bool.true_and]
      have := sound_fans s.fans pv.fans v.fans hA .sure true Tri.sound_sure
      simpa using this
    · have hl' : (s.fans.length != pv.fans.length) = true := by rw [hA.1]; simp [hl]
      rw [hl']
      have : (s.fans.length == v.fans.length) = false := by simp [hl]
      rw [this]
      exact ⟨fun h => (by cases h), fun _ => rfl⟩

theorem Tri.sound_foldl' {α : Type} (F : α → Tri) (G : α → Bool) (L : List α)
    (h : ∀ a ∈ L, (F a).Sound (G a)) : (L.foldl (fun (acc : Tri) a => acc.and (F a)) Tri.sure).Sound (L.all G) := by
  have := Tri.sound_foldl F G L h .sure true Tri.sound_sure
  simpa using this

/-- **Part-level soundness.** If the three-valued view `pv` read from anchor `a` approximates the known view `v` read
from anchor `0`, position by position, then `fit3At` is a sound verdict for `fitsAt` (`= fits`). -/
theorem sound_part (p : Part) (hgood : ∀ s ∈ p.subs, s.Good) (pv : List PSpokeView) (v : HubView) (a : Nat)
    (hlen : pv.length = v.length)
    (hA : ∀ j, j < v.length → ∃ x y, pv[(a + j) % pv.length]? = some x ∧ v[j]? = some y ∧ Approx x y) :
    (p.fit3At pv a).Sound (fits p v) := by
  unfold Part.fit3At fits Part.fitsAt
  by_cases hl : v.length = p.subs.length
  · have hl1 : (pv.length != p.subs.length) = false := by rw [hlen, hl]; simp
    have hl2 : (v.length == p.subs.length) = true := by rw [hl]; simp
    rw [hl1, hl2]
    simp only [Bool.false_eq_true, ↓reduceIte, Bool.true_and]
    apply Tri.sound_foldl'
    · intro j hj
      have hj' : j < p.subs.length := List.mem_range.1 hj
      obtain ⟨x, y, hx, hy, hxy⟩ := hA j (by omega)
      have hs : p.subs[j]? = some p.subs[j] := List.getElem?_eq_getElem hj'
      have hj0 : (0 + j) % v.length = j := by rw [Nat.zero_add]; exact Nat.mod_eq_of_lt (by omega)
      simp only [hs, hx, hj0, hy]
      exact sound_sub (hgood _ (List.getElem_mem hj')) hxy
  · have hl1 : (pv.length != p.subs.length) = true := by rw [hlen]; simp [hl]
    have hl2 : (v.length == p.subs.length) = false := by simp [hl]
    rw [hl1, hl2]
    simp only [↓reduceIte, Bool.false_and]
    exact ⟨fun h => (by cases h), fun _ => rfl⟩

/-- B2's shape facts give the hypotheses used here. -/
theorem wellShaped_spec {p : Part} (h : p.wellShaped = true) :
    5 ≤ p.hub ∧ p.hub ≤ 8 ∧ p.subs.length = p.hub ∧ p.target = 2 ∧ p.amount = 1 ∧ ∀ s ∈ p.subs, s.Good := by
  unfold Part.wellShaped at h
  simp only [Bool.and_eq_true, List.all_eq_true, beq_iff_eq, Nat.ble_eq, and_assoc] at h
  obtain ⟨h1, h2, h3, h4, h5, h6⟩ := h
  refine ⟨h1, h2, h3, h4, h5, fun s hs => ?_⟩
  have := (h6 s hs).2.2.2.2.2.2.2
  simp only [Bool.or_eq_true] at this
  rcases this with he | hx
  · left; simp only [List.isEmpty_iff] at he; rw [he]; rfl
  · right
    simp only [Bool.and_eq_true, Rng.exact68, beq_iff_eq, Nat.ble_eq] at hx
    obtain ⟨⟨⟨heq, h6l⟩, h8⟩, -⟩ := hx
    refine ⟨?_, ?_⟩
    · unfold Rng.isFull; rw [Bool.and_eq_false_iff]; left; rw [Bool.eq_false_iff, ne_eq, Nat.ble_eq]; omega
    · unfold Rng.test; rw [Bool.and_eq_false_iff]; right; rw [Bool.eq_false_iff, ne_eq, Nat.ble_eq]; omega

end SimpleGraph.SphericalMap.RSSTSeed
