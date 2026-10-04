/-
  Degree4Extend.lean — degree-≤4 Kempe extension, graph-theoretic core.

  Classical step: H is a simple graph, v ∉ V(H), and v is joined to four
  distinct vertices of H. If a proper 4-colouring of H uses all four colours
  on those neighbours, a Kempe swap should produce a proper 4-colouring of H
  that uses at most three colours on them, so v receives the missing colour.

  This Mathlib has no planar embedding, so the file does not prove that such a
  separated pair of neighbours exists. It proves the two facts that do not need
  an embedding:

  * among four vertices that are not pairwise adjacent, two are non-adjacent;
  * if an (a,b)-Kempe chain through a neighbour coloured a misses the neighbour
    coloured b, swapping that chain frees colour a on the four neighbours, and
    the external vertex (modelled as `none : Option V`) extends the colouring.

  The swap is proper by `kempeSwap_preserves_proper`. Target: 0 sorry.
-/

import KempeReconfiguration.Basic
import Mathlib.Data.Fintype.Option

namespace KempeReconfiguration

variable {V : Type*} [Fintype V] [DecidableEq V]
variable {k : ℕ}

noncomputable section

/-- The (a,b)-Kempe chain of `u`: the reachable component of `u` in the
bichromatic subgraph `B_{a,b}(G,c)`. -/
abbrev kempeChain (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u : V) : Set V :=
  {v | (bichromaticSubgraph G c a b).Reachable u v}

instance kempeChain_decidablePred
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u : V) :
    DecidablePred (fun v => v ∈ kempeChain G c a b u) :=
  fun v => Classical.propDecidable (v ∈ kempeChain G c a b u)

lemma walk_colours_ab
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) {u v : V}
    (p : (bichromaticSubgraph G c a b).Walk u v) :
    c u = a ∨ c u = b → c v = a ∨ c v = b := by
  induction p with
  | nil =>
      intro hu
      exact hu
  | cons h _ ih =>
      intro _
      exact ih h.2.2

lemma reachable_colours_ab
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) {u v : V}
    (h : (bichromaticSubgraph G c a b).Reachable u v)
    (hu : c u = a ∨ c u = b) :
    c v = a ∨ c v = b := by
  rcases h with ⟨p⟩
  exact walk_colours_ab G c a b p hu

lemma mem_kempeChain_self
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (u : V) :
    u ∈ kempeChain G c a b u :=
  SimpleGraph.Reachable.refl u

lemma kempeChain_colours
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (x v : V)
    (hx : c x = a ∨ c x = b)
    (hv : v ∈ kempeChain G c a b x) :
    c v = a ∨ c v = b :=
  reachable_colours_ab G c a b hv hx

/-- An (a,b)-chain is closed under edges of G that land on an {a,b}-vertex.
This is the saturation hypothesis of `kempeSwap_preserves_proper`. -/
lemma kempeChain_closed
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (x u v : V)
    (hx : c x = a ∨ c x = b)
    (huv : G.Adj u v)
    (hu : u ∈ kempeChain G c a b x)
    (hvcol : c v = a ∨ c v = b) :
    v ∈ kempeChain G c a b x := by
  have hcu : c u = a ∨ c u = b := kempeChain_colours G c a b x u hx hu
  exact SimpleGraph.Reachable.trans hu
    ⟨SimpleGraph.Walk.cons ⟨huv, hcu, hvcol⟩ SimpleGraph.Walk.nil⟩

lemma adjacent_ab_same_chain
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (x y : V)
    (hxy : G.Adj x y) (hx : c x = a) (hy : c y = b) :
    inSameKempeChain G c a b x y :=
  ⟨SimpleGraph.Walk.cons ⟨hxy, Or.inl hx, Or.inr hy⟩ SimpleGraph.Walk.nil⟩

/-- If the (a,b)-chain of `x` misses `y`, then `x` and `y` are not adjacent.
In particular a chain-separated pair of neighbours is a non-adjacent pair. -/
lemma separated_chain_not_adj
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (x y : V)
    (hx : c x = a) (hy : c y = b)
    (hsep : ¬ inSameKempeChain G c a b x y) :
    ¬ G.Adj x y := by
  intro hxy
  exact hsep (adjacent_ab_same_chain G c a b x y hxy hx hy)

theorem kempeSwap_chain_proper
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (hab : a ≠ b) (x : V)
    (hx : c x = a)
    (hproper : IsProperColouring G c) :
    IsProperColouring G (kempeSwap c (kempeChain G c a b x) a b) :=
  kempeSwap_preserves_proper G c a b hab (kempeChain G c a b x)
    (fun v hv => kempeChain_colours G c a b x v (Or.inl hx) hv)
    (fun u v huv hu hvcol => kempeChain_closed G c a b x u v (Or.inl hx) huv hu hvcol)
    hproper

lemma kempeSwap_flips_a
    (c : V → Fin k) (S : Set V) [DecidablePred (· ∈ S)]
    (a b : Fin k) (x : V) (hxS : x ∈ S) (hx : c x = a) :
    kempeSwap c S a b x = b := by
  simp [kempeSwap, hxS, hx]

lemma kempeSwap_exchanges_b
    (c : V → Fin k) (S : Set V) [DecidablePred (· ∈ S)]
    (a b : Fin k) (hab : a ≠ b) (y : V)
    (hyS : y ∈ S) (hy : c y = b) :
    kempeSwap c S a b y = a := by
  have hya : c y ≠ a := by
    intro h
    exact hab (h.symm.trans hy)
  simp [kempeSwap, hyS, hy, hya]

/-- Swapping the chain frees colour `a` at its source, and leaves a vertex
outside the chain unchanged. -/
theorem kempeSwap_frees_source
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (hab : a ≠ b) (x y : V)
    (hx : c x = a) (hy : c y = b)
    (hsep : y ∉ kempeChain G c a b x) :
    let c' := kempeSwap c (kempeChain G c a b x) a b
    c' x = b ∧ c' x ≠ a ∧ c' y = b := by
  refine ⟨?_, ?_, ?_⟩
  · exact kempeSwap_flips_a c (kempeChain G c a b x) a b x (mem_kempeChain_self G c a b x) hx
  · rw [kempeSwap_flips_a c (kempeChain G c a b x) a b x (mem_kempeChain_self G c a b x) hx]
    exact Ne.symm hab
  · rw [kempeSwap_outside c (kempeChain G c a b x) a b y hsep]
    exact hy

/-- If `y` lies on the same chain, the swap exchanges the two colours, so both
`a` and `b` remain on the pair. Separation is what frees a colour. -/
theorem kempeSwap_same_chain_keeps_both
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (c : V → Fin k) (a b : Fin k) (hab : a ≠ b) (x y : V)
    (hx : c x = a) (hy : c y = b)
    (hsame : y ∈ kempeChain G c a b x) :
    kempeSwap c (kempeChain G c a b x) a b x = b ∧
      kempeSwap c (kempeChain G c a b x) a b y = a :=
  ⟨kempeSwap_flips_a c _ a b x (mem_kempeChain_self G c a b x) hx,
    kempeSwap_exchanges_b c _ a b hab y hsame hy⟩

/-- Among four vertices that are not pairwise adjacent, two are non-adjacent. -/
theorem exists_nonadj_of_not_pairwise
    (G : SimpleGraph V) [DecidableRel G.Adj]
    (p q r s : V)
    (hpq : p ≠ q) (hpr : p ≠ r) (hps : p ≠ s)
    (hqr : q ≠ r) (hqs : q ≠ s) (hrs : r ≠ s)
    (hnot : ¬ (G.Adj p q ∧ G.Adj p r ∧ G.Adj p s ∧
      G.Adj q r ∧ G.Adj q s ∧ G.Adj r s)) :
    ∃ u v : V, u ≠ v ∧
      (u = p ∨ u = q ∨ u = r ∨ u = s) ∧
      (v = p ∨ v = q ∨ v = r ∨ v = s) ∧
      ¬ G.Adj u v := by
  by_cases h1 : G.Adj p q
  · by_cases h2 : G.Adj p r
    · by_cases h3 : G.Adj p s
      · by_cases h4 : G.Adj q r
        · by_cases h5 : G.Adj q s
          · by_cases h6 : G.Adj r s
            · exact absurd ⟨h1, h2, h3, h4, h5, h6⟩ hnot
            · exact ⟨r, s, hrs, Or.inr (Or.inr (Or.inl rfl)),
                Or.inr (Or.inr (Or.inr rfl)), h6⟩
          · exact ⟨q, s, hqs, Or.inr (Or.inl rfl),
              Or.inr (Or.inr (Or.inr rfl)), h5⟩
        · exact ⟨q, r, hqr, Or.inr (Or.inl rfl),
            Or.inr (Or.inr (Or.inl rfl)), h4⟩
      · exact ⟨p, s, hps, Or.inl rfl, Or.inr (Or.inr (Or.inr rfl)), h3⟩
    · exact ⟨p, r, hpr, Or.inl rfl, Or.inr (Or.inr (Or.inl rfl)), h2⟩
  · exact ⟨p, q, hpq, Or.inl rfl, Or.inr (Or.inl rfl), h1⟩

lemma card_triple_le {α : Type*} [DecidableEq α] (a b c : α) :
    ({a, b, c} : Finset α).card ≤ 3 := by
  calc
    ({a, b, c} : Finset α).card ≤ ({b, c} : Finset α).card + 1 :=
      Finset.card_insert_le a {b, c}
    _ ≤ ({c} : Finset α).card + 1 + 1 :=
      Nat.add_le_add_right (Finset.card_insert_le b {c}) 1
    _ = 3 := by rw [Finset.card_singleton]

lemma card_le_three_of_subset_triple {s : Finset (Fin 4)} {x y z : Fin 4}
    (h : s ⊆ {x, y, z}) : s.card ≤ 3 :=
  Nat.le_trans (Finset.card_le_card h) (card_triple_le x y z)

lemma four_values_card_eq_four
    {c₀ c₁ c₂ c₃ : Fin 4}
    (hall : ∀ col : Fin 4, col = c₀ ∨ col = c₁ ∨ col = c₂ ∨ col = c₃) :
    ({c₀, c₁, c₂, c₃} : Finset (Fin 4)).card = 4 := by
  have hsub : (Finset.univ : Finset (Fin 4)) ⊆ {c₀, c₁, c₂, c₃} := by
    intro col _
    rcases hall col with h | h | h | h
    · rw [h]; exact Finset.mem_insert_self _ _
    · rw [h]; exact Finset.mem_insert_of_mem (Finset.mem_insert_self _ _)
    · rw [h]; exact Finset.mem_insert_of_mem
        (Finset.mem_insert_of_mem (Finset.mem_insert_self _ _))
    · rw [h]; exact Finset.mem_insert_of_mem (Finset.mem_insert_of_mem
        (Finset.mem_insert_of_mem (Finset.mem_singleton_self _)))
  have hle : 4 ≤ ({c₀, c₁, c₂, c₃} : Finset (Fin 4)).card := by
    have hcard := Finset.card_le_card hsub
    simpa [Finset.card_univ, Fintype.card_fin] using hcard
  have hge : ({c₀, c₁, c₂, c₃} : Finset (Fin 4)).card ≤ 4 := by
    simpa [Fintype.card_fin] using
      Finset.card_le_univ ({c₀, c₁, c₂, c₃} : Finset (Fin 4))
  exact Nat.le_antisymm hge hle

lemma absurd_card_le_three
    {c₀ c₁ c₂ c₃ : Fin 4}
    (hall : ∀ col : Fin 4, col = c₀ ∨ col = c₁ ∨ col = c₂ ∨ col = c₃)
    (hle : ({c₀, c₁, c₂, c₃} : Finset (Fin 4)).card ≤ 3) : False := by
  have h4 : ({c₀, c₁, c₂, c₃} : Finset (Fin 4)).card = 4 :=
    four_values_card_eq_four hall
  exact Nat.not_le_of_lt (by decide : (3 : ℕ) < 4) (le_of_eq_of_le h4.symm hle)

lemma card_le_three_of_eq_01 {a b c d : Fin 4} (h : a = b) :
    ({a, b, c, d} : Finset (Fin 4)).card ≤ 3 := by
  rw [h]
  apply card_le_three_of_subset_triple (x := b) (y := c) (z := d)
  intro t ht
  simp only [Finset.mem_insert, Finset.mem_singleton] at ht ⊢
  rcases ht with rfl | rfl | rfl | rfl
  · exact Or.inl rfl
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)

lemma card_le_three_of_eq_02 {a b c d : Fin 4} (h : a = c) :
    ({a, b, c, d} : Finset (Fin 4)).card ≤ 3 := by
  rw [h]
  apply card_le_three_of_subset_triple (x := b) (y := c) (z := d)
  intro t ht
  simp only [Finset.mem_insert, Finset.mem_singleton] at ht ⊢
  rcases ht with rfl | rfl | rfl | rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)

lemma card_le_three_of_eq_03 {a b c d : Fin 4} (h : a = d) :
    ({a, b, c, d} : Finset (Fin 4)).card ≤ 3 := by
  rw [h]
  apply card_le_three_of_subset_triple (x := b) (y := c) (z := d)
  intro t ht
  simp only [Finset.mem_insert, Finset.mem_singleton] at ht ⊢
  rcases ht with rfl | rfl | rfl | rfl
  · exact Or.inr (Or.inr rfl)
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)

lemma card_le_three_of_eq_12 {a b c d : Fin 4} (h : b = c) :
    ({a, b, c, d} : Finset (Fin 4)).card ≤ 3 := by
  rw [h]
  apply card_le_three_of_subset_triple (x := a) (y := c) (z := d)
  intro t ht
  simp only [Finset.mem_insert, Finset.mem_singleton] at ht ⊢
  rcases ht with rfl | rfl | rfl | rfl
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)

lemma card_le_three_of_eq_13 {a b c d : Fin 4} (h : b = d) :
    ({a, b, c, d} : Finset (Fin 4)).card ≤ 3 := by
  rw [h]
  apply card_le_three_of_subset_triple (x := a) (y := c) (z := d)
  intro t ht
  simp only [Finset.mem_insert, Finset.mem_singleton] at ht ⊢
  rcases ht with rfl | rfl | rfl | rfl
  · exact Or.inl rfl
  · exact Or.inr (Or.inr rfl)
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)

lemma card_le_three_of_eq_23 {a b c d : Fin 4} (h : c = d) :
    ({a, b, c, d} : Finset (Fin 4)).card ≤ 3 := by
  rw [h]
  apply card_le_three_of_subset_triple (x := a) (y := b) (z := d)
  intro t ht
  simp only [Finset.mem_insert, Finset.mem_singleton] at ht ⊢
  rcases ht with rfl | rfl | rfl | rfl
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr rfl)
  · exact Or.inr (Or.inr rfl)

/-- Four colours on four positions are pairwise distinct. -/
lemma four_colours_pairwise_ne
    {c₀ c₁ c₂ c₃ : Fin 4}
    (hall : ∀ col : Fin 4, col = c₀ ∨ col = c₁ ∨ col = c₂ ∨ col = c₃) :
    c₀ ≠ c₁ ∧ c₀ ≠ c₂ ∧ c₀ ≠ c₃ ∧ c₁ ≠ c₂ ∧ c₁ ≠ c₃ ∧ c₂ ≠ c₃ := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro h
    exact absurd_card_le_three hall (card_le_three_of_eq_01 h)
  · intro h
    exact absurd_card_le_three hall (card_le_three_of_eq_02 h)
  · intro h
    exact absurd_card_le_three hall (card_le_three_of_eq_03 h)
  · intro h
    exact absurd_card_le_three hall (card_le_three_of_eq_12 h)
  · intro h
    exact absurd_card_le_three hall (card_le_three_of_eq_13 h)
  · intro h
    exact absurd_card_le_three hall (card_le_three_of_eq_23 h)

lemma four_distinct_card
    {n₀ n₁ n₂ n₃ : V}
    (h₀₁ : n₀ ≠ n₁) (h₀₂ : n₀ ≠ n₂) (h₀₃ : n₀ ≠ n₃)
    (h₁₂ : n₁ ≠ n₂) (h₁₃ : n₁ ≠ n₃) (h₂₃ : n₂ ≠ n₃) :
    ({n₀, n₁, n₂, n₃} : Finset V).card = 4 := by
  have hn₂ : n₂ ∉ ({n₃} : Finset V) := by
    intro h
    exact h₂₃ (Finset.mem_singleton.mp h)
  have hc2 : ({n₂, n₃} : Finset V).card = 2 := by
    rw [Finset.card_insert_of_not_mem hn₂, Finset.card_singleton]
  have hn₁ : n₁ ∉ ({n₂, n₃} : Finset V) := by
    intro h
    simp only [Finset.mem_insert, Finset.mem_singleton] at h
    rcases h with h | h
    · exact h₁₂ h
    · exact h₁₃ h
  have hc3 : ({n₁, n₂, n₃} : Finset V).card = 3 := by
    rw [Finset.card_insert_of_not_mem hn₁, hc2]
  have hn₀ : n₀ ∉ ({n₁, n₂, n₃} : Finset V) := by
    intro h
    simp only [Finset.mem_insert, Finset.mem_singleton] at h
    rcases h with h | h | h
    · exact h₀₁ h
    · exact h₀₂ h
    · exact h₀₃ h
  rw [Finset.card_insert_of_not_mem hn₀, hc3]

/-- A set of at most three colours in `Fin 4` omits a colour. This is the
degree-≤3 extension, and the degree-4 extension after the Kempe swap. -/
theorem exists_free_colour_of_card_le_three
    {s : Finset (Fin 4)} (hs : s.card ≤ 3) :
    ∃ free : Fin 4, free ∉ s := by
  by_contra h
  have hall : ∀ col : Fin 4, col ∈ s := by
    intro col
    by_contra hnin
    exact h ⟨col, hnin⟩
  have hsub : (Finset.univ : Finset (Fin 4)) ⊆ s := fun col _ => hall col
  have hle : 4 ≤ s.card := by
    have hcard := Finset.card_le_card hsub
    simpa [Finset.card_univ, Fintype.card_fin] using hcard
  exact Nat.not_le_of_lt (Nat.lt_succ_of_le hs) hle

/-- The graph obtained by adding a vertex outside `H`, adjacent exactly to
four named vertices of `H`. The new vertex is `none`. -/
def apexAdj (H : SimpleGraph V) (n₀ n₁ n₂ n₃ : V) : Option V → Option V → Prop
  | some u, some w => H.Adj u w
  | some u, none => u = n₀ ∨ u = n₁ ∨ u = n₂ ∨ u = n₃
  | none, some w => w = n₀ ∨ w = n₁ ∨ w = n₂ ∨ w = n₃
  | none, none => False

lemma apexAdj_symm (H : SimpleGraph V) (n₀ n₁ n₂ n₃ : V) :
    Symmetric (apexAdj H n₀ n₁ n₂ n₃) := by
  intro u v h
  cases u <;> cases v
  · cases h
  · exact h
  · exact h
  · exact H.symm h

lemma apexAdj_loopless (H : SimpleGraph V) (n₀ n₁ n₂ n₃ : V) :
    Irreflexive (apexAdj H n₀ n₁ n₂ n₃) := by
  intro u h
  cases u with
  | none => cases h
  | some w => exact H.loopless w h

def apexGraph (H : SimpleGraph V) (n₀ n₁ n₂ n₃ : V) : SimpleGraph (Option V) where
  Adj := apexAdj H n₀ n₁ n₂ n₃
  symm := apexAdj_symm H n₀ n₁ n₂ n₃
  loopless := apexAdj_loopless H n₀ n₁ n₂ n₃

instance apexGraph_decidableAdj
    (H : SimpleGraph V) [DecidableRel H.Adj] (n₀ n₁ n₂ n₃ : V) :
    DecidableRel (apexGraph H n₀ n₁ n₂ n₃).Adj :=
    fun _ _ => Classical.propDecidable _

/-- If `free` differs from the colour of each of the four neighbours, the
apex colouring is proper. The colouring of `H` is the `some` branch. -/
theorem apex_extend_proper
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (n₀ n₁ n₂ n₃ : V)
    (c' : V → Fin 4) (free : Fin 4)
    (hproper : IsProperColouring H c')
    (h₀ : c' n₀ ≠ free) (h₁ : c' n₁ ≠ free)
    (h₂ : c' n₂ ≠ free) (h₃ : c' n₃ ≠ free) :
    IsProperColouring (apexGraph H n₀ n₁ n₂ n₃)
      (fun o => match o with | some v => c' v | none => free) := by
  intro o₁ o₂ h
  cases o₁ with
  | none =>
      cases o₂ with
      | none => cases h
      | some w =>
          rcases h with rfl | rfl | rfl | rfl
          · exact Ne.symm h₀
          · exact Ne.symm h₁
          · exact Ne.symm h₂
          · exact Ne.symm h₃
  | some u =>
      cases o₂ with
      | none =>
          rcases h with rfl | rfl | rfl | rfl
          · exact h₀
          · exact h₁
          · exact h₂
          · exact h₃
      | some w =>
          exact hproper u w h

/-- Degree-4 Kempe step, given a chain that misses the other neighbour.

Hypotheses, in full: `H` is a simple graph on `V`. The four neighbours
`n₀,n₁,n₂,n₃` are distinct vertices of `H`. The colouring `c : V → Fin 4`
is proper and uses every colour on those four vertices, with `c n₀ = a` and
`c n₁ = b`. The `(a,b)`-Kempe chain of `n₀` in `H` does not contain `n₁`.
(The vertex `v` being coloured is not a vertex of `H`; see
`degree4_apex_extension`.)

Conclusions: the Kempe swap of that chain is a proper 4-colouring of `H`;
`n₀` and `n₁` are non-adjacent; both receive colour `b`; colour `a` is
missing from all four neighbours; and those neighbours use at most three colours.
-/
theorem degree4_kempe_frees_colour
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (c : V → Fin 4)
    (hproper : IsProperColouring H c)
    (n₀ n₁ n₂ n₃ : V)
    (h₀₁ : n₀ ≠ n₁) (h₀₂ : n₀ ≠ n₂) (h₀₃ : n₀ ≠ n₃)
    (h₁₂ : n₁ ≠ n₂) (h₁₃ : n₁ ≠ n₃) (h₂₃ : n₂ ≠ n₃)
    (hall : ∀ col : Fin 4, col = c n₀ ∨ col = c n₁ ∨ col = c n₂ ∨ col = c n₃)
    (a b : Fin 4)
    (ha : c n₀ = a) (hb : c n₁ = b)
    (hsep : ¬ inSameKempeChain H c a b n₀ n₁) :
    let c' := kempeSwap c (kempeChain H c a b n₀) a b
    IsProperColouring H c' ∧
      c' n₀ = b ∧ c' n₀ ≠ a ∧ c' n₁ = b ∧
      ¬ H.Adj n₀ n₁ ∧
      ({n₀, n₁, n₂, n₃} : Finset V).card = 4 ∧
      ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)).card ≤ 3 ∧
      a ∉ ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)) ∧
      c' n₂ ≠ a ∧ c' n₃ ≠ a := by
  intro c'
  have hne := four_colours_pairwise_ne hall
  have hab : a ≠ b := by
    simpa [ha, hb] using hne.1
  have h2a : c n₂ ≠ a := by simpa [ha] using (hne.2.1).symm
  have h2b : c n₂ ≠ b := by simpa [hb] using (hne.2.2.2.1).symm
  have h3a : c n₃ ≠ a := by simpa [ha] using (hne.2.2.1).symm
  have h3b : c n₃ ≠ b := by simpa [hb] using (hne.2.2.2.2.1).symm
  have hproper' : IsProperColouring H c' := by
    simpa [show c' = kempeSwap c (kempeChain H c a b n₀) a b from rfl] using
      kempeSwap_chain_proper H c a b hab n₀ ha hproper
  have hsrc : c' n₀ = b := by
    simpa using kempeSwap_flips_a c (kempeChain H c a b n₀) a b n₀
      (mem_kempeChain_self H c a b n₀) ha
  have hfree : c' n₀ ≠ a := hsrc.symm ▸ Ne.symm hab
  have hstay : c' n₁ = b := by
    have hfix := kempeSwap_outside c (kempeChain H c a b n₀) a b n₁ hsep
    simpa [hb] using hfix
  have h2 : c' n₂ = c n₂ :=
    kempeSwap_preserves_other c (kempeChain H c a b n₀) a b n₂ h2a h2b
  have h3 : c' n₃ = c n₃ :=
    kempeSwap_preserves_other c (kempeChain H c a b n₀) a b n₃ h3a h3b
  have hnad : ¬ H.Adj n₀ n₁ :=
    separated_chain_not_adj H c a b n₀ n₁ ha hb hsep
  have hcardV : ({n₀, n₁, n₂, n₃} : Finset V).card = 4 :=
    four_distinct_card h₀₁ h₀₂ h₀₃ h₁₂ h₁₃ h₂₃
  have hsub : ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)) ⊆ {b, c n₂, c n₃} := by
    intro t ht
    simp only [Finset.mem_insert, Finset.mem_singleton] at ht
    rcases ht with ht | ht | ht | ht
    · rw [ht, hsrc]; exact Finset.mem_insert_self _ _
    · rw [ht, hstay]; exact Finset.mem_insert_self _ _
    · rw [ht, h2]; exact Finset.mem_insert_of_mem (Finset.mem_insert_self _ _)
    · rw [ht, h3]; exact Finset.mem_insert_of_mem
        (Finset.mem_insert_of_mem (Finset.mem_singleton_self _))
  have hcardC : ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)).card ≤ 3 :=
    card_le_three_of_subset_triple hsub
  have hmiss : a ∉ ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)) := by
    intro hmem
    have hmem' : a ∈ ({b, c n₂, c n₃} : Finset (Fin 4)) := hsub hmem
    simp only [Finset.mem_insert, Finset.mem_singleton] at hmem'
    rcases hmem' with h | h | h
    · exact hab h
    · exact h2a h.symm
    · exact h3a h.symm
  have h2free : c' n₂ ≠ a := h2.symm ▸ h2a
  have h3free : c' n₃ ≠ a := h3.symm ▸ h3a
  exact ⟨hproper', hsrc, hfree, hstay, hnad, hcardV, hcardC, hmiss, h2free, h3free⟩

/-- The same swap extends across the external vertex `none`, which is joined
exactly to the four neighbours and receives the freed colour `a`. -/
theorem degree4_apex_extension
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (c : V → Fin 4)
    (hproper : IsProperColouring H c)
    (n₀ n₁ n₂ n₃ : V)
    (h₀₁ : n₀ ≠ n₁) (h₀₂ : n₀ ≠ n₂) (h₀₃ : n₀ ≠ n₃)
    (h₁₂ : n₁ ≠ n₂) (h₁₃ : n₁ ≠ n₃) (h₂₃ : n₂ ≠ n₃)
    (hall : ∀ col : Fin 4, col = c n₀ ∨ col = c n₁ ∨ col = c n₂ ∨ col = c n₃)
    (a b : Fin 4)
    (ha : c n₀ = a) (hb : c n₁ = b)
    (hsep : ¬ inSameKempeChain H c a b n₀ n₁) :
    let c' := kempeSwap c (kempeChain H c a b n₀) a b
    let cA : Option V → Fin 4 := fun
      | some v => c' v
      | none => a
    IsProperColouring H c' ∧
      IsProperColouring (apexGraph H n₀ n₁ n₂ n₃) cA ∧
      ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)).card ≤ 3 ∧
      ¬ H.Adj n₀ n₁ ∧
      cA none = a ∧ cA none ≠ c' n₀ ∧ cA none ≠ c' n₁ ∧
      cA none ≠ c' n₂ ∧ cA none ≠ c' n₃ := by
  intro c' cA
  have hstep := degree4_kempe_frees_colour H c hproper n₀ n₁ n₂ n₃
    h₀₁ h₀₂ h₀₃ h₁₂ h₁₃ h₂₃ hall a b ha hb hsep
  have hproper' : IsProperColouring H c' := hstep.1
  have hsrc : c' n₀ = b := hstep.2.1
  have hfree : c' n₀ ≠ a := hstep.2.2.1
  have hstay : c' n₁ = b := hstep.2.2.2.1
  have hnad : ¬ H.Adj n₀ n₁ := hstep.2.2.2.2.1
  have hcard : ({c' n₀, c' n₁, c' n₂, c' n₃} : Finset (Fin 4)).card ≤ 3 :=
    hstep.2.2.2.2.2.2.1
  have h2 : c' n₂ ≠ a := hstep.2.2.2.2.2.2.2.2.1
  have h3 : c' n₃ ≠ a := hstep.2.2.2.2.2.2.2.2.2
  have h1ne : c' n₁ ≠ a := by
    rw [hstay]
    exact hsrc.symm ▸ hfree
  have hA : IsProperColouring (apexGraph H n₀ n₁ n₂ n₃) cA := by
    simpa using apex_extend_proper H n₀ n₁ n₂ n₃ c' a hproper' hfree h1ne h2 h3
  refine ⟨hproper', hA, hcard, hnad, rfl, ?_, ?_, ?_, ?_⟩
  · exact Ne.symm hfree
  · exact Ne.symm h1ne
  · exact Ne.symm h2
  · exact Ne.symm h3

/-- If at least one of two disjoint pairs among the four neighbours is
chain-separated, one Kempe swap frees a colour. Which pair is separated is
not proved: that identification uses a planar embedding of the link. -/
theorem degree4_frees_of_some_separated_pair
    (H : SimpleGraph V) [DecidableRel H.Adj]
    (c : V → Fin 4)
    (hproper : IsProperColouring H c)
    (n₀ n₁ n₂ n₃ : V)
    (h₀₁ : n₀ ≠ n₁) (h₀₂ : n₀ ≠ n₂) (h₀₃ : n₀ ≠ n₃)
    (h₁₂ : n₁ ≠ n₂) (h₁₃ : n₁ ≠ n₃) (h₂₃ : n₂ ≠ n₃)
    (hall : ∀ col : Fin 4, col = c n₀ ∨ col = c n₁ ∨ col = c n₂ ∨ col = c n₃)
    (hpair : ¬ inSameKempeChain H c (c n₀) (c n₂) n₀ n₂ ∨
        ¬ inSameKempeChain H c (c n₁) (c n₃) n₁ n₃) :
    (IsProperColouring H (kempeSwap c (kempeChain H c (c n₀) (c n₂) n₀) (c n₀) (c n₂)) ∧
      kempeSwap c (kempeChain H c (c n₀) (c n₂) n₀) (c n₀) (c n₂) n₀ ≠ c n₀) ∨
    (IsProperColouring H (kempeSwap c (kempeChain H c (c n₁) (c n₃) n₁) (c n₁) (c n₃)) ∧
      kempeSwap c (kempeChain H c (c n₁) (c n₃) n₁) (c n₁) (c n₃) n₁ ≠ c n₁) := by
  rcases hpair with hsep | hsep
  · left
    have hall' : ∀ col : Fin 4,
        col = c n₀ ∨ col = c n₂ ∨ col = c n₁ ∨ col = c n₃ := by
      intro col
      rcases hall col with h | h | h | h
      · exact Or.inl h
      · exact Or.inr (Or.inr (Or.inl h))
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr (Or.inr h))
    have hstep := degree4_kempe_frees_colour H c hproper n₀ n₂ n₁ n₃
      h₀₂ h₀₁ h₀₃ (Ne.symm h₁₂) h₂₃ h₁₃ hall' (c n₀) (c n₂) rfl rfl hsep
    exact ⟨hstep.1, hstep.2.2.1⟩
  · right
    have hall' : ∀ col : Fin 4,
        col = c n₁ ∨ col = c n₃ ∨ col = c n₀ ∨ col = c n₂ := by
      intro col
      rcases hall col with h | h | h | h
      · exact Or.inr (Or.inr (Or.inl h))
      · exact Or.inl h
      · exact Or.inr (Or.inr (Or.inr h))
      · exact Or.inr (Or.inl h)
    have hstep := degree4_kempe_frees_colour H c hproper n₁ n₃ n₀ n₂
      h₁₃ (Ne.symm h₀₁) h₁₂ (Ne.symm h₀₃) (Ne.symm h₂₃) h₀₂
      hall' (c n₁) (c n₃) rfl rfl hsep
    exact ⟨hstep.1, hstep.2.2.1⟩

end

end KempeReconfiguration
