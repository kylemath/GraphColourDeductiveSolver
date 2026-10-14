/-!
# DCheckS3: the abstract combinatorial core of (S3) (item B3, exploratory)

Two lemmas named in the header of `DCheckSound.lean` as missing for (S3), stated and proved here
abstractly (core Lean only, no geometry):

* **(i) non-crossing partition ⇒ non-crossing perfect matching** (`nc_matching`). The `2p` ring
  arcs `0..2p-1` sit between `2p` transitions (transition `t` lies between arcs `t-1` and `t`;
  arc `2p-1` is between transition `2p-1` and transition `0`). Let `c` label the arcs by Kempe
  chain, with the planar property "chains do not cross" (`NCLabel`). Then there is a non-crossing
  perfect matching `μ` of the transitions (`IsNCPM`) such that arcs in one chain are never
  separated by a chord of `μ` (`sameFace`). Construction: pair each transition with the next
  transition along the boundary of its even-arc chain (`μ e = prev(e) + 1` for an even arc `e`,
  `μ (e+1) = next(e)`; `prev`/`next` cyclic within the chain).
* **(ii) simultaneous swaps** (`flip_proper`, `chainUnion_closed`). For a proper colouring
  `col : V → Nat` and a pairing `θ`, XOR-ing `θ` on a set `S` closed under θ-edges (edges whose
  ends' colours differ by `θ`) is again proper; any union of θ-Kempe chains (components of the
  θ-edge graph) is such a set.

**Remaining steps (not claimed here).**
* (R1, checker level, this package) `matchTable[p]` covers every non-crossing perfect matching:
  for each `μ` with `IsNCPM (2p) μ` some `lab ∈ matchTable[p]!` has
  `sameFace (2p) μ j j' → lab[j]! = lab[j']!` (`p ≤ 7`; needs completeness of `ncm` and that
  `arcRegions` labels exactly the faces). With `nc_matching`, every region of that `lab` is then a
  union of whole chains.
* (R2, project level) In `SphericalMap`/`ConfigOcc` terms: index the ring arcs and transitions as
  `DCheck.transitions`/`DCheck.arcOf` do, take `c j :=` the θ-Kempe chain of the vertices of arc `j`,
  prove `NCLabel` from `RingChains.chains_noncrossing(_same)` and `ParityLabel` from the
  alternation of θ-classes, and show that the ring code of `flipOn` on the union of the chains of
  the chosen regions is `k ^^^ flipMask r k θ lab s`. Together with (R1), `nc_matching` and
  `flip_chains_proper` this gives `KempeMatching cf P` for the realised codes `P`.
-/
namespace DCheck.S3

/-! ## Searches -/

/-- Largest `x < m` with `P x`. -/
def lastBelow (P : Nat → Bool) : Nat → Option Nat
  | 0 => none
  | m + 1 => if P m then some m else lastBelow P m

theorem lastBelow_some (P : Nat → Bool) (m x : Nat) (h : lastBelow P m = some x) :
    x < m ∧ P x = true ∧ ∀ y, x < y → y < m → P y = false := by
  induction m with
  | zero => simp [lastBelow] at h
  | succ m ih =>
    simp only [lastBelow] at h
    split at h
    · cases h; exact ⟨by omega, ‹_›, fun y h1 h2 => by omega⟩
    · obtain ⟨h1, h2, h3⟩ := ih h
      refine ⟨by omega, h2, fun y hy1 hy2 => ?_⟩
      by_cases hym : y = m
      · subst hym; simpa using ‹¬P y = true›
      · exact h3 y hy1 (by omega)

theorem lastBelow_none (P : Nat → Bool) (m : Nat) (h : lastBelow P m = none) :
    ∀ y, y < m → P y = false := by
  induction m with
  | zero => intro y hy; omega
  | succ m ih =>
    simp only [lastBelow] at h
    split at h
    · cases h
    · intro y hy
      by_cases hym : y = m
      · subst hym; simpa using ‹¬P y = true›
      · exact ih h y (by omega)

/-- Smallest `x ∈ [lo, lo+len)` with `P x`. -/
def firstFrom (P : Nat → Bool) (lo : Nat) : Nat → Option Nat
  | 0 => none
  | len + 1 => if P lo then some lo else firstFrom P (lo + 1) len

theorem firstFrom_some (P : Nat → Bool) (lo len x : Nat) (h : firstFrom P lo len = some x) :
    lo ≤ x ∧ x < lo + len ∧ P x = true ∧ ∀ y, lo ≤ y → y < x → P y = false := by
  induction len generalizing lo with
  | zero => simp [firstFrom] at h
  | succ len ih =>
    simp only [firstFrom] at h
    split at h
    · cases h; exact ⟨by omega, by omega, ‹_›, fun y h1 h2 => by omega⟩
    · obtain ⟨h1, h2, h3, h4⟩ := ih (lo + 1) h
      refine ⟨by omega, by omega, h3, fun y hy1 hy2 => ?_⟩
      by_cases hym : y = lo
      · subst hym; simpa using ‹¬P y = true›
      · exact h4 y (by omega) hy2

theorem firstFrom_none (P : Nat → Bool) (lo len : Nat) (h : firstFrom P lo len = none) :
    ∀ y, lo ≤ y → y < lo + len → P y = false := by
  induction len generalizing lo with
  | zero => intro y h1 h2; omega
  | succ len ih =>
    simp only [firstFrom] at h
    split at h
    · cases h
    · intro y h1 h2
      by_cases hym : y = lo
      · subst hym; simpa using ‹¬P y = true›
      · exact ih (lo + 1) h y (by omega) (by omega)

/-! ## (i) Non-crossing partitions of the arcs give non-crossing perfect matchings -/

/-- Chain labels `c` of the arcs `0..n-1` do not cross (planarity of the outside map). -/
def NCLabel (n : Nat) (c : Nat → Nat) : Prop :=
  ∀ a b x d, a < b → b < x → x < d → d < n → c a = c x → c b = c d → c a = c b

/-- Each chain lies in one θ-class; the classes alternate around the ring, so a chain's arcs
have one parity. -/
def ParityLabel (n : Nat) (c : Nat → Nat) : Prop :=
  ∀ j j', j < n → j' < n → c j = c j' → j % 2 = j' % 2

/-- `μ` is a non-crossing perfect matching of the points `0..n-1`. -/
def IsNCPM (n : Nat) (μ : Nat → Nat) : Prop :=
  (∀ t, t < n → μ t < n ∧ μ t ≠ t ∧ μ (μ t) = t) ∧
  (∀ a b x d, a < b → b < x → x < d → d < n → μ a = x → μ b = d → False)

/-- Arcs `j`, `j'` lie in one face of `μ`: no chord `(a, μ a)`, `a < μ a`, separates them
(the chord cuts off the arcs `a .. μ a - 1`). -/
def sameFace (n : Nat) (μ : Nat → Nat) (j j' : Nat) : Prop :=
  ∀ a, a < n → a < μ a → (a ≤ j ∧ j < μ a ↔ a ≤ j' ∧ j' < μ a)

section construction
variable (n : Nat) (c : Nat → Nat)

/-- The even arcs of the chain of `e`. -/
def inB (e : Nat) : Nat → Bool := fun x => decide (x < n ∧ x % 2 = 0 ∧ c x = c e)

def maxB (e : Nat) : Nat := (lastBelow (inB n c e) n).getD 0
def minB (e : Nat) : Nat := (firstFrom (inB n c e) 0 n).getD 0

/-- Cyclic predecessor of the even arc `e` in its chain. -/
def prevc (e : Nat) : Nat :=
  match lastBelow (inB n c e) e with
  | some x => x
  | none => maxB n c e

/-- Cyclic successor of the even arc `e` in its chain. -/
def nextc (e : Nat) : Nat :=
  match firstFrom (inB n c e) (e + 1) (n - (e + 1)) with
  | some x => x
  | none => minB n c e

/-- The matching: transition `e` (left end of even arc `e`) goes to the right end of the previous
even arc of its chain; transition `e+1` (right end) goes to the left end of the next one. -/
def mu (t : Nat) : Nat := if t % 2 = 0 then prevc n c t + 1 else nextc n c (t - 1)

end construction

section proofs
variable {n : Nat} {c : Nat → Nat}

theorem inB_iff (e x : Nat) : inB n c e x = true ↔ x < n ∧ x % 2 = 0 ∧ c x = c e := by
  simp [inB]

theorem inB_congr {e x : Nat} (h : inB n c e x = true) : inB n c x = inB n c e := by
  funext y; rw [inB_iff] at h; simp [inB, h.2.2]

theorem maxB_spec {e : Nat} (he : inB n c e e = true) :
    inB n c e (maxB n c e) = true ∧ ∀ y, inB n c e y = true → y ≤ maxB n c e := by
  unfold maxB
  cases h : lastBelow (inB n c e) n with
  | none =>
    have := lastBelow_none _ _ h e ((inB_iff e e).1 he).1; simp_all
  | some x =>
    obtain ⟨h1, h2, h3⟩ := lastBelow_some _ _ _ h
    refine ⟨h2, fun y hy => ?_⟩
    have hyn := ((inB_iff e y).1 hy).1
    simp only [Option.getD_some]
    by_cases hxy : x < y
    · have := h3 y hxy hyn; simp_all
    · omega

theorem minB_spec {e : Nat} (he : inB n c e e = true) :
    inB n c e (minB n c e) = true ∧ ∀ y, inB n c e y = true → minB n c e ≤ y := by
  unfold minB
  cases h : firstFrom (inB n c e) 0 n with
  | none =>
    have := firstFrom_none _ _ _ h e (by omega) (by simpa using ((inB_iff e e).1 he).1); simp_all
  | some x =>
    obtain ⟨_, _, h2, h3⟩ := firstFrom_some _ _ _ _ h
    refine ⟨h2, fun y hy => ?_⟩
    simp only [Option.getD_some]
    by_cases hxy : y < x
    · have := h3 y (by omega) hxy; simp_all
    · omega

theorem prevc_spec {e : Nat} (he : inB n c e e = true) :
    inB n c e (prevc n c e) = true ∧
    ((prevc n c e < e ∧ ∀ y, prevc n c e < y → y < e → inB n c e y = false) ∨
     ((∀ y, y < e → inB n c e y = false) ∧ prevc n c e = maxB n c e)) := by
  unfold prevc
  cases h : lastBelow (inB n c e) e with
  | none =>
    exact ⟨(maxB_spec he).1, Or.inr ⟨lastBelow_none _ _ h, rfl⟩⟩
  | some x =>
    obtain ⟨h1, h2, h3⟩ := lastBelow_some _ _ _ h
    exact ⟨h2, Or.inl ⟨h1, h3⟩⟩

theorem nextc_spec {e : Nat} (he : inB n c e e = true) :
    inB n c e (nextc n c e) = true ∧
    ((e < nextc n c e ∧ ∀ y, e < y → y < nextc n c e → inB n c e y = false) ∨
     ((∀ y, e < y → inB n c e y = false) ∧ nextc n c e = minB n c e)) := by
  unfold nextc
  cases h : firstFrom (inB n c e) (e + 1) (n - (e + 1)) with
  | none =>
    refine ⟨(minB_spec he).1, Or.inr ⟨fun y hy => ?_, rfl⟩⟩
    by_cases hyn : y < n
    · exact firstFrom_none _ _ _ h y (by omega) (by omega)
    · cases hb : inB n c e y
      · rfl
      · exact absurd ((inB_iff e y).1 hb).1 hyn
  | some x =>
    obtain ⟨h1, _, h2, h3⟩ := firstFrom_some _ _ _ _ h
    dsimp only
    exact ⟨h2, Or.inl ⟨by omega, fun y hy1 hy2 => h3 y (by omega) hy2⟩⟩

/-- `next (prev e) = e`. -/
theorem nextc_prevc {e : Nat} (he : inB n c e e = true) : nextc n c (prevc n c e) = e := by
  obtain ⟨hx, hp⟩ := prevc_spec he
  have hcg := inB_congr hx
  have hxx : inB n c (prevc n c e) (prevc n c e) = true := by rw [hcg]; exact hx
  obtain ⟨hy, hn⟩ := nextc_spec hxx
  rw [hcg] at hy hn
  rcases hp with ⟨hlt, hgap⟩ | ⟨hbelow, hmax⟩
  · rcases hn with ⟨hlt', hgap'⟩ | ⟨habove, _⟩
    · by_cases h1 : nextc n c (prevc n c e) < e
      · have := hgap _ hlt' h1; simp_all
      · by_cases h2 : e < nextc n c (prevc n c e)
        · have := hgap' e hlt h2; simp_all
        · omega
    · have := habove e hlt; simp_all
  · rcases hn with ⟨hlt', _⟩ | ⟨_, hmin⟩
    · have := (maxB_spec he).2 _ hy; omega
    · have hm : minB n c (prevc n c e) = minB n c e := by unfold minB; rw [hcg]
      rw [hmin, hm]
      have h1 := (minB_spec he).2 e he
      have h2 := (minB_spec he).1
      by_cases h3 : minB n c e < e
      · have := hbelow _ h3; simp_all
      · omega

/-- `prev (next e) = e`. -/
theorem prevc_nextc {e : Nat} (he : inB n c e e = true) : prevc n c (nextc n c e) = e := by
  obtain ⟨hx, hp⟩ := nextc_spec he
  have hcg := inB_congr hx
  have hxx : inB n c (nextc n c e) (nextc n c e) = true := by rw [hcg]; exact hx
  obtain ⟨hy, hn⟩ := prevc_spec hxx
  rw [hcg] at hy hn
  rcases hp with ⟨hlt, hgap⟩ | ⟨habove, hmin⟩
  · rcases hn with ⟨hlt', hgap'⟩ | ⟨hbelow, _⟩
    · by_cases h1 : e < prevc n c (nextc n c e)
      · have := hgap _ h1 hlt'; simp_all
      · by_cases h2 : prevc n c (nextc n c e) < e
        · have := hgap' e h2 hlt; simp_all
        · omega
    · have := hbelow e hlt; simp_all
  · rcases hn with ⟨hlt', _⟩ | ⟨_, hmax⟩
    · have := (minB_spec he).2 _ hy; omega
    · have hm : maxB n c (nextc n c e) = maxB n c e := by unfold maxB; rw [hcg]
      rw [hmax, hm]
      have h1 := (maxB_spec he).2 e he
      have h2 := (maxB_spec he).1
      by_cases h3 : e < maxB n c e
      · have := habove _ h3; simp_all
      · omega

theorem inB_self {e : Nat} (h1 : e < n) (h2 : e % 2 = 0) : inB n c e e = true :=
  (inB_iff e e).2 ⟨h1, h2, rfl⟩

theorem mu_spec (hn : n % 2 = 0) (t : Nat) (ht : t < n) :
    mu n c t < n ∧ mu n c t ≠ t ∧ mu n c (mu n c t) = t := by
  by_cases h2 : t % 2 = 0
  · have he := inB_self (c := c) ht h2
    have hx := (inB_iff _ _).1 (prevc_spec he).1
    have hmu : mu n c t = prevc n c t + 1 := by simp [mu, h2]
    refine ⟨by omega, by omega, ?_⟩
    rw [hmu]
    have : mu n c (prevc n c t + 1) = nextc n c (prevc n c t) := by
      simp [mu, show (prevc n c t + 1) % 2 = 1 by omega]
    rw [this, nextc_prevc he]
  · have he := inB_self (c := c) (show t - 1 < n by omega) (show (t - 1) % 2 = 0 by omega)
    have hy := (inB_iff _ _).1 (nextc_spec he).1
    have hmu : mu n c t = nextc n c (t - 1) := by simp [mu, h2]
    refine ⟨by omega, by omega, ?_⟩
    rw [hmu]
    have : mu n c (nextc n c (t - 1)) = prevc n c (nextc n c (t - 1)) + 1 := by
      simp [mu, hy.2.1]
    rw [this, prevc_nextc he]; omega

/-- The two kinds of chord `(a, μ a)` with `a < μ a`. -/
theorem chord_cases (a : Nat) (ha : a < n) (hlt : a < mu n c a) :
    (a % 2 = 0 ∧ inB n c a a = true ∧ mu n c a = maxB n c a + 1 ∧
      ∀ y, y < a → inB n c a y = false) ∨
    (a % 2 = 1 ∧ inB n c (a - 1) (a - 1) = true ∧ a - 1 < mu n c a ∧
      inB n c (a - 1) (mu n c a) = true ∧
      ∀ y, a - 1 < y → y < mu n c a → inB n c (a - 1) y = false) := by
  by_cases h2 : a % 2 = 0
  · have he := inB_self (c := c) ha h2
    have hmu : mu n c a = prevc n c a + 1 := by simp [mu, h2]
    left
    rcases (prevc_spec he).2 with ⟨hp, _⟩ | ⟨hb, hm⟩
    · omega
    · exact ⟨h2, he, by rw [hmu, hm], hb⟩
  · have he := inB_self (c := c) (show a - 1 < n by omega) (show (a - 1) % 2 = 0 by omega)
    have hmu : mu n c a = nextc n c (a - 1) := by simp [mu, h2]
    right
    rcases (nextc_spec he).2 with ⟨hp, hg⟩ | ⟨_, hm⟩
    · exact ⟨by omega, he, by rw [hmu]; exact hp, by rw [hmu]; exact (nextc_spec he).1,
        by rw [hmu]; exact hg⟩
    · have := (minB_spec he).2 _ he; rw [hmu, hm] at hlt; omega

theorem face_one (hNC : NCLabel n c) (hP : ParityLabel n c) (a : Nat) (ha : a < n)
    (hlt : a < mu n c a) (j j' : Nat) (hj : j < n) (hj' : j' < n) (hc : c j = c j')
    (hin : a ≤ j ∧ j < mu n c a) : a ≤ j' ∧ j' < mu n c a := by
  rcases chord_cases a ha hlt with ⟨h2, he, hmu, hb⟩ | ⟨h2, he, hlt', hy, hg⟩
  · obtain ⟨hm, hmle⟩ := maxB_spec he
    have hm' := (inB_iff _ _).1 hm
    rw [hmu] at hin ⊢
    by_cases hca : c j = c a
    · have hpj : j' % 2 = 0 := by have := hP j j' hj hj' hc; have := hP j a hj ha hca; omega
      have hB : inB n c a j' = true := (inB_iff _ _).2 ⟨hj', hpj, by rw [← hc, hca]⟩
      have h1 := hmle j' hB
      by_cases h3 : j' < a
      · have := hb j' h3; simp_all
      · omega
    · have hja : j ≠ a := fun h => hca (by rw [h])
      have hjm : j ≠ maxB n c a := fun h => hca (by rw [h]; exact hm'.2.2)
      refine Classical.byContradiction fun hout => ?_
      by_cases h3 : j' < a
      · have := hNC j' a j (maxB n c a) h3 (by omega) (by omega) hm'.1 hc.symm hm'.2.2.symm
        exact hca (by rw [hc]; exact this)
      · exact hca (hNC a j (maxB n c a) j' (by omega) (by omega) (by omega) hj'
          hm'.2.2.symm hc).symm
  · have hy' := (inB_iff _ _).1 hy
    have he' := (inB_iff _ _).1 he
    by_cases hca : c j = c (a - 1)
    · have hpj : j % 2 = 0 := by have := hP j (a - 1) hj (by omega) hca; omega
      have := hg j (by omega) hin.2
      rw [(inB_iff _ _).2 ⟨hj, hpj, hca⟩] at this; cases this
    · refine Classical.byContradiction fun hout => ?_
      have hj'1 : j' ≠ a - 1 := fun h => hca (by rw [hc, h])
      have hj'2 : j' ≠ mu n c a := fun h => hca (by rw [hc, h]; exact hy'.2.2)
      by_cases h3 : j' < a - 1
      · have := hNC j' (a - 1) j (mu n c a) h3 (by omega) hin.2 hy'.1 hc.symm hy'.2.2.symm
        exact hca (by rw [hc]; exact this)
      · exact hca (hNC (a - 1) j (mu n c a) j' (by omega) hin.2 (by omega) hj'
          hy'.2.2.symm hc).symm

theorem face (hNC : NCLabel n c) (hP : ParityLabel n c) (j j' : Nat) (hj : j < n) (hj' : j' < n)
    (hc : c j = c j') : sameFace n (mu n c) j j' := fun a ha hlt =>
  ⟨face_one hNC hP a ha hlt j j' hj hj' hc, face_one hNC hP a ha hlt j' j hj' hj hc.symm⟩

theorem mu_noncrossing (hNC : NCLabel n c) (hP : ParityLabel n c) (a b x d : Nat)
    (h1 : a < b) (h2 : b < x) (h3 : x < d) (h4 : d < n) (hx : mu n c a = x)
    (hd : mu n c b = d) : False := by
  have hb : b < mu n c b := by omega
  -- two arcs of the chord `(b, d)` in one chain, one inside `(a, x)`, one outside
  obtain ⟨u, v, hu, hv, huv, hu1, hu2, hv1, hv2⟩ : ∃ u v, u < n ∧ v < n ∧ c u = c v ∧
      b - 1 ≤ u ∧ u ≤ b ∧ d - 1 ≤ v ∧ v ≤ d := by
    rcases chord_cases b (by omega) hb with ⟨_, he, hmu, _⟩ | ⟨_, he, _, hy, _⟩
    · have hm := (inB_iff _ _).1 (maxB_spec he).1
      exact ⟨b, maxB n c b, by omega, hm.1, hm.2.2.symm, by omega, by omega,
        by rw [← hd, hmu]; omega, by rw [← hd, hmu]; omega⟩
    · have hy' := (inB_iff _ _).1 hy
      exact ⟨b - 1, mu n c b, by omega, hy'.1, hy'.2.2.symm, by omega, by omega, by omega,
        by omega⟩
  have := (face hNC hP u v hu hv huv a (by omega) (by omega)).1 ⟨by omega, by omega⟩
  omega

end proofs

/-- **(S3)(i), abstract form.** A non-crossing, parity-homogeneous chain labelling of the `2p` ring
arcs is refined by the faces of a non-crossing perfect matching of the `2p` transitions. -/
theorem nc_matching (p : Nat) (c : Nat → Nat) (hNC : NCLabel (2 * p) c)
    (hP : ParityLabel (2 * p) c) :
    ∃ μ, IsNCPM (2 * p) μ ∧
      ∀ j j', j < 2 * p → j' < 2 * p → c j = c j' → sameFace (2 * p) μ j j' :=
  ⟨mu (2 * p) c,
    ⟨fun t ht => mu_spec (by omega) t ht, fun a b x d h1 h2 h3 h4 hx hd =>
      mu_noncrossing hNC hP a b x d h1 h2 h3 h4 hx hd⟩,
    fun j j' hj hj' hc => face hNC hP j j' hj hj' hc⟩

/-! ## (ii) Swapping a set of Kempe chains at once -/

section swaps
variable {V : Type} (adj : V → V → Prop) (col : V → Nat) (θ : Nat)

def Proper : Prop := ∀ u v, adj u v → col u ≠ col v

/-- `S` is closed under θ-edges (edges whose end colours differ by `θ` in `Z2 × Z2`). -/
def ThetaClosed (S : V → Prop) : Prop := ∀ u v, S u → adj u v → col u ^^^ col v = θ → S v

/-- XOR `θ` on the vertices of `S`. -/
def flipOn (S : V → Prop) [DecidablePred S] (v : V) : Nat := if S v then col v ^^^ θ else col v

/-- The θ-Kempe chain of `r`: vertices reachable from `r` along θ-edges. -/
inductive Reach (r : V) : V → Prop
  | refl : Reach r r
  | step {u v : V} : Reach r u → adj u v → col u ^^^ col v = θ → Reach r v

theorem xor_xor_cancel (a t : Nat) : a ^^^ t ^^^ t = a := by
  rw [Nat.xor_assoc, Nat.xor_self, Nat.xor_zero]

/-- **(S3)(ii), abstract form.** Swapping all of a θ-closed set at once keeps a proper colouring
proper. -/
theorem flip_proper (hsym : ∀ u v, adj u v → adj v u) (hP : Proper adj col) (S : V → Prop)
    [DecidablePred S] (hS : ThetaClosed adj col θ S) : Proper adj (flipOn col θ S) := by
  intro u v huv heq
  unfold flipOn at heq
  by_cases hu : S u <;> by_cases hv : S v <;> simp only [hu, hv, ite_true, ite_false] at heq
  · exact hP u v huv (by have := congrArg (· ^^^ θ) heq; simpa [xor_xor_cancel] using this)
  · exact hv (hS u v hu huv (by rw [← heq, ← Nat.xor_assoc, Nat.xor_self, Nat.zero_xor]))
  · exact hu (hS v u hv (hsym u v huv) (by rw [heq, ← Nat.xor_assoc, Nat.xor_self, Nat.zero_xor]))
  · exact hP u v huv heq

/-- Any union of θ-Kempe chains is θ-closed. -/
theorem chainUnion_closed (R : V → Prop) :
    ThetaClosed adj col θ (fun v => ∃ r, R r ∧ Reach adj col θ r v) := by
  intro u v ⟨r, hr, hru⟩ huv hθ
  exact ⟨r, hr, Reach.step hru huv hθ⟩

/-- (ii) for a union of chains: swapping any set of θ-Kempe chains simultaneously keeps the
colouring proper. -/
theorem flip_chains_proper (hsym : ∀ u v, adj u v → adj v u) (hP : Proper adj col)
    (R : V → Prop) [DecidablePred (fun v => ∃ r, R r ∧ Reach adj col θ r v)] :
    Proper adj (flipOn col θ (fun v => ∃ r, R r ∧ Reach adj col θ r v)) :=
  flip_proper adj col θ hsym hP _ (chainUnion_closed adj col θ R)

end swaps

end DCheck.S3

#print axioms DCheck.S3.nc_matching
#print axioms DCheck.S3.flip_chains_proper
