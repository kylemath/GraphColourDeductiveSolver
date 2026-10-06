module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingChains

/-!
# Ring reduction: the general lemmas behind D-reducibility certificates

A configuration occurrence is abstracted as `ConfigOcc`: a spherical map `T`, the map `G` obtained
by deleting the interior `ι` (all of whose neighbours are listed by the tables `intAdj` and
`ringAdj`), and the ring `ρ`, which bounds a face of `G`. The generated certificate files prove,
class by class, that every proper colouring of `G` leads by single Kempe swaps of `G` to one whose
ring colours extend into the interior; `colorable_of_ext` turns such a colouring into a colouring
of `T`.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill

variable {n : ℕ}

/-- An occurrence of a configuration with interior `ι` and ring `ρ`. -/
structure ConfigOcc (T G : SphericalMap n) (r m : ℕ) (ρ : ℕ → Fin n) (ι : Fin m → Fin n)
    (intAdj : Fin m → Fin m → Bool) (ringAdj : Fin m → ℕ → Bool) : Prop where
  ring : RingFace G r ρ
  ιinj : Function.Injective ι
  ringOff : ∀ t a, ρ t ≠ ι a
  hG : ∀ x y, G.Adj x y ↔ T.Adj x y ∧ (∀ a, x ≠ ι a) ∧ (∀ a, y ≠ ι a)
  nbr : ∀ a w, T.Adj (ι a) w →
    (∃ b, w = ι b ∧ intAdj a b = true) ∨ (∃ t, t < r ∧ w = ρ t ∧ ringAdj a t = true)
  pos : 0 < m

variable {T G : SphericalMap n} {r m : ℕ} {ρ : ℕ → Fin n} {ι : Fin m → Fin n}
  {intAdj : Fin m → Fin m → Bool} {ringAdj : Fin m → ℕ → Bool}

/-- The dummy hole: an interior vertex (isolated in `G`). -/
def ConfigOcc.hole (_O : ConfigOcc T G r m ρ ι intAdj ringAdj) : Fin n := ι ⟨0, _O.pos⟩

theorem ConfigOcc.ring_ne_hole (O : ConfigOcc T G r m ρ ι intAdj ringAdj) (t : ℕ) :
    ρ t ≠ O.hole := O.ringOff t _

theorem ConfigOcc.not_adj_hole (O : ConfigOcc T G r m ρ ι intAdj ringAdj) (x : Fin n) :
    ¬ G.Adj x O.hole := fun h => ((O.hG _ _).1 h).2.2 _ rfl

/-- Consecutive ring vertices with colours in a pair are linked. -/
theorem ConfigOcc.conn_ring (O : ConfigOcc T G r m ρ ι intAdj ringAdj) {c : Fin n → Fin 4}
    {a b : Fin 4} (t : ℕ) (h1 : c (ρ t) = a ∨ c (ρ t) = b)
    (h2 : c (ρ (t + 1)) = a ∨ c (ρ (t + 1)) = b) :
    (pairGraph G.graph O.hole c a b).Reachable (ρ t) (ρ (t + 1)) :=
  Adj.reachable ⟨O.ring.adj t, ⟨O.ring_ne_hole t, h1⟩, ⟨O.ring_ne_hole (t + 1), h2⟩⟩

/-- The ring closes up: the last ring vertex is linked to the first. -/
theorem ConfigOcc.conn_wrap (O : ConfigOcc T G r m ρ ι intAdj ringAdj) {c : Fin n → Fin 4}
    {a b : Fin 4} (t : ℕ) (ht : t + 1 = r) (h1 : c (ρ t) = a ∨ c (ρ t) = b)
    (h2 : c (ρ 0) = a ∨ c (ρ 0) = b) :
    (pairGraph G.graph O.hole c a b).Reachable (ρ t) (ρ 0) := by
  have e : ρ (t + 1) = ρ 0 := by rw [ht, show r = 0 + r by omega]; exact O.ring.per 0
  have := O.conn_ring t h1 (e ▸ h2)
  rwa [e] at this

/-- Adjacent ring vertices get different colours. -/
theorem ConfigOcc.ring_proper (O : ConfigOcc T G r m ρ ι intAdj ringAdj) {c : Fin n → Fin 4}
    (hc : ProperOff G.graph O.hole c) (t : ℕ) : c (ρ t) ≠ c (ρ (t + 1)) :=
  hc (O.ring.adj t) (O.ring_ne_hole t) (O.ring_ne_hole (t + 1))

theorem ConfigOcc.ring_proper_wrap (O : ConfigOcc T G r m ρ ι intAdj ringAdj)
    {c : Fin n → Fin 4} (hc : ProperOff G.graph O.hole c) (t : ℕ) (ht : t + 1 = r) :
    c (ρ t) ≠ c (ρ 0) := by
  have e : ρ (t + 1) = ρ 0 := by rw [ht, show r = 0 + r by omega]; exact O.ring.per 0
  have := O.ring_proper hc t
  rwa [e] at this

theorem swap_perm (σ : Equiv.Perm (Fin 4)) (a b k : Fin 4) :
    Equiv.swap (σ a) (σ b) (σ k) = σ (Equiv.swap a b k) := by
  rw [Equiv.swap_apply_apply]; simp

theorem flip_in {c : Fin n → Fin 4} {σ : Equiv.Perm (Fin 4)} {a b k : Fin 4} {S : Set (Fin n)}
    {v : Fin n} (hv : v ∈ S) (hk : c v = σ k) :
    swap c (σ a) (σ b) S v = σ (Equiv.swap a b k) := by
  rw [swap_in hv, hk, swap_perm]

theorem flip_out {c : Fin n → Fin 4} {σ : Equiv.Perm (Fin 4)} {a b k : Fin 4} {S : Set (Fin n)}
    {v : Fin n} (hv : v ∉ S) (hk : c v = σ k) : swap c (σ a) (σ b) S v = σ k := by
  rw [swap_out hv, hk]

theorem flip_other {c : Fin n → Fin 4} {σ : Equiv.Perm (Fin 4)} {a b k : Fin 4}
    {S : Set (Fin n)} {v : Fin n} (hka : k ≠ a) (hkb : k ≠ b) (hk : c v = σ k) :
    swap c (σ a) (σ b) S v = σ k := by
  rw [swap_other (by rw [hk]; exact σ.injective.ne hka) (by rw [hk]; exact σ.injective.ne hkb), hk]

theorem pair_disj (σ : Equiv.Perm (Fin 4)) {a b a' b' : Fin 4}
    (h : ∀ x : Fin 4, (x = a ∨ x = b) → (x = a' ∨ x = b') → False) :
    ∀ x : Fin 4, (x = σ a ∨ x = σ b) → (x = σ a' ∨ x = σ b') → False := by
  intro x h1 h2
  apply h (σ.symm x)
  · rcases h1 with rfl | rfl <;> simp
  · rcases h2 with rfl | rfl <;> simp

theorem pair_active {c : Fin n → Fin 4} {σ : Equiv.Perm (Fin 4)} {a b k : Fin 4} {v : Fin n}
    (hk : c v = σ k) (h : k = a ∨ k = b) : c v = σ a ∨ c v = σ b := by
  rcases h with rfl | rfl
  · exact Or.inl hk
  · exact Or.inr hk

/-- **Base case.** A colouring of `G` whose ring colours are `σ ∘ κ`, for a ring colouring `κ`
that extends into the interior by `λ`, gives a colouring of `T`. -/
theorem ConfigOcc.colorable_of_ext (O : ConfigOcc T G r m ρ ι intAdj ringAdj)
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

set_option synthInstance.maxHeartbeats 400000 in
theorem exists_perm_two : ∀ a0 a1 : Fin 4, a0 ≠ a1 →
    ∃ σ : Equiv.Perm (Fin 4), σ 0 = a0 ∧ σ 1 = a1 := by decide +kernel

set_option synthInstance.maxHeartbeats 400000 in
theorem exists_perm_three' : ∀ a0 a1 a2 : Fin 4, a0 ≠ a1 → a0 ≠ a2 → a1 ≠ a2 →
    ∃ σ : Equiv.Perm (Fin 4), σ 0 = a0 ∧ σ 1 = a1 ∧ σ 2 = a2 := by decide +kernel

set_option synthInstance.maxHeartbeats 400000 in
theorem exists_perm_four : ∀ a0 a1 a2 a3 : Fin 4, a0 ≠ a1 → a0 ≠ a2 → a0 ≠ a3 → a1 ≠ a2 →
    a1 ≠ a3 → a2 ≠ a3 →
    ∃ σ : Equiv.Perm (Fin 4), σ 0 = a0 ∧ σ 1 = a1 ∧ σ 2 = a2 ∧ σ 3 = a3 := by decide +kernel

theorem fin4_pigeon : ∀ v a0 a1 a2 a3 : Fin 4, a0 ≠ a1 → a0 ≠ a2 → a0 ≠ a3 → a1 ≠ a2 →
    a1 ≠ a3 → a2 ≠ a3 → ¬ v = a0 → ¬ v = a1 → ¬ v = a2 → ¬ v = a3 → False := by decide

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
