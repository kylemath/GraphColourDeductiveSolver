import Mathlib

open Finset

namespace StudioMath

variable {V : Type*} [Fintype V] [DecidableEq V] (G : SimpleGraph V) [DecidableRel G.Adj]

/-- vertices of degree at least 12 -/
def highSet : Finset V := univ.filter fun v => 12 ≤ G.degree v

/-- degree-5 vertices with at most one neighbour of degree ≥ 12 -/
def goodSet : Finset V :=
  univ.filter fun v => G.degree v = 5 ∧ ((highSet G).filter (G.Adj v)).card ≤ 1

theorem good_card_ge_twelve (hmin : ∀ v, 5 ≤ G.degree v)
    (hE : 2 * G.edgeFinset.card + 12 ≤ 6 * Fintype.card V) :
    12 ≤ (goodSet G).card := by
  classical
  set H := highSet G with hH
  set A : Finset V := univ.filter fun v => G.degree v = 5 with hA
  set B : Finset V := A.filter fun v => 2 ≤ (H.filter (G.Adj v)).card with hB
  have hgood : goodSet G = A.filter fun v => ¬ 2 ≤ (H.filter (G.Adj v)).card := by
    ext v; simp [goodSet, hA, ← hH]
  have hsplit : (goodSet G).card + B.card = A.card := by
    rw [hgood, hB, add_comm]; exact Finset.card_filter_add_card_filter_not _
  -- Claim 1
  have hB_le_A : B ⊆ A := Finset.filter_subset _ _
  have hdc := Finset.sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow (s := B) (t := H) G.Adj
  have h1 : 2 * B.card ≤ ∑ h ∈ H, G.degree h := by
    calc 2 * B.card = ∑ _b ∈ B, 2 := by simp [mul_comm]
      _ ≤ ∑ b ∈ B, (H.bipartiteAbove G.Adj b).card := by
          apply Finset.sum_le_sum
          intro b hb
          have := (Finset.mem_filter.mp hb).2
          simpa [Finset.bipartiteAbove] using this
      _ = ∑ h ∈ H, (B.bipartiteBelow G.Adj h).card := hdc
      _ ≤ ∑ h ∈ H, G.degree h := by
          apply Finset.sum_le_sum
          intro h _
          rw [← G.card_neighborFinset_eq_degree]
          apply Finset.card_le_card
          intro b hb
          have := (Finset.mem_filter.mp hb).2
          simpa [SimpleGraph.mem_neighborFinset, G.adj_comm] using this
  have h2 : ∑ h ∈ H, G.degree h ≤ 2 * ∑ h ∈ H, ((G.degree h : ℤ) - 6).toNat := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro h hh
    have : 12 ≤ G.degree h := (Finset.mem_filter.mp hh).2
    omega
  -- Claim 2
  have hdeg : ∑ v, G.degree v = 2 * G.edgeFinset.card := G.sum_degrees_eq_twice_card_edges
  have hpt : ∀ v, ((G.degree v : ℤ) - 6) ≥
      -(if G.degree v = 5 then (1:ℤ) else 0) + (if v ∈ H then (G.degree v : ℤ) - 6 else 0) := by
    intro v
    have := hmin v
    by_cases h5 : G.degree v = 5
    · have : v ∉ H := by simp [hH, highSet]; omega
      simp [h5, this]
    · by_cases hv : v ∈ H
      · simp [h5, hv]
      · simp [h5, hv]; omega
  have hsum := Finset.sum_le_sum (s := univ) (fun v _ => hpt v)
  rw [Finset.sum_add_distrib, Finset.sum_neg_distrib] at hsum
  have e1 : ∑ v, (if G.degree v = 5 then (1:ℤ) else 0) = (A.card : ℤ) := by
    simp [hA, Finset.sum_boole]
  have e2 : ∑ v, (if v ∈ H then (G.degree v : ℤ) - 6 else 0) =
      ∑ h ∈ H, ((G.degree h : ℤ) - 6) := by
    rw [← Finset.sum_filter]; congr 1; ext v; simp
  have e3 : ∑ v, ((G.degree v : ℤ) - 6) = 2 * (G.edgeFinset.card : ℤ) - 6 * (Fintype.card V : ℤ) := by
    rw [Finset.sum_sub_distrib]
    have : ((∑ v, G.degree v : ℕ) : ℤ) = ∑ v, (G.degree v : ℤ) := by push_cast; rfl
    rw [← this, hdeg]; simp [mul_comm]
  have e4 : ∑ h ∈ H, ((G.degree h : ℤ) - 6) = ((∑ h ∈ H, ((G.degree h : ℤ) - 6).toNat : ℕ) : ℤ) := by
    push_cast
    apply Finset.sum_congr rfl
    intro h hh
    have : 12 ≤ G.degree h := (Finset.mem_filter.mp hh).2
    omega
  rw [e1, e2, e3, e4] at hsum
  have hE' : 2 * (G.edgeFinset.card : ℤ) + 12 ≤ 6 * (Fintype.card V : ℤ) := by exact_mod_cast hE
  have hs : (∑ h ∈ H, G.degree h : ℤ) ≤ 2 * (∑ h ∈ H, ((G.degree h : ℤ) - 6).toNat : ℕ) := by
    exact_mod_cast h2
  have h1' : (2 * B.card : ℤ) ≤ (∑ h ∈ H, G.degree h : ℕ) := by exact_mod_cast h1
  have hsplit' : ((goodSet G).card : ℤ) + B.card = A.card := by exact_mod_cast hsplit
  push_cast at h1' hs
  omega

end StudioMath


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
