/-
  NeverRevert.lean — Lemma 3.1: Never-Revert Lemma

  Agent 1210, Manager M4, Sub-subagent S2

  Statement: If c is a proper 5-colouring and K is an (a,b)-chain
  with a, b ∈ {1,2,3,4} (i.e., a ≠ 5 and b ≠ 5), then
  swapping a ↔ b on K preserves the set of colour-5 vertices:
    {v | c'(v) = 5} = {v | c(v) = 5}

  Proof: Swap only changes colours between a and b.
  Since 5 ∉ {a,b}, no vertex gains or loses colour 5.

  Target: 0 sorry
-/

import KempeReconfiguration.Basic

namespace KempeReconfiguration

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- The Never-Revert Lemma: swapping colours a ↔ b (where neither is colour 5)
    does not change which vertices have colour 5.

    More precisely: for any vertex v, (kempeSwap c S a b v = target) ↔ (c v = target)
    when target ∉ {a, b}. -/
theorem never_revert_pointwise
    (c : V → Fin 5) (S : Set V) [DecidablePred (· ∈ S)]
    (a b : Fin 5) (target : Fin 5)
    (hta : target ≠ a) (htb : target ≠ b) (v : V) :
    kempeSwap c S a b v = target ↔ c v = target := by
  constructor
  · intro h
    simp only [kempeSwap] at h
    split at h
    · split at h
      · exact absurd h.symm hta
      · split at h
        · exact absurd h.symm htb
        · exact h
    · exact h
  · intro h
    have hva : c v ≠ a := fun ha => hta (ha ▸ h)
    have hvb : c v ≠ b := fun hb => htb (hb ▸ h)
    rw [kempeSwap_preserves_other c S a b v hva hvb]
    exact h

/-- The Never-Revert Lemma (set version): the set of vertices with colour 5
    is unchanged by an (a,b)-Kempe swap when a ≠ 5 and b ≠ 5. -/
theorem never_revert
    (c : V → Fin 5) (S : Set V) [DecidablePred (· ∈ S)]
    (a b : Fin 5) (five : Fin 5)
    (ha5 : five ≠ a) (hb5 : five ≠ b) :
    {v : V | kempeSwap c S a b v = five} = {v : V | c v = five} := by
  ext v
  simp only [Set.mem_setOf_eq]
  exact never_revert_pointwise c S a b five ha5 hb5 v

/-- Corollary: Kempe swap on {1,2,3,4} colours preserves |V_5|.
    The cardinality version follows from the set equality. -/
theorem never_revert_card
    [Fintype V]
    (c : V → Fin 5) (S : Finset V)
    (a b : Fin 5) (five : Fin 5)
    (ha5 : five ≠ a) (hb5 : five ≠ b) :
    (Finset.univ.filter (fun v => kempeSwap c (↑S : Set V) a b v = five)).card =
    (Finset.univ.filter (fun v => c v = five)).card := by
  congr 1
  ext v
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  exact never_revert_pointwise c (↑S : Set V) a b five ha5 hb5 v

end KempeReconfiguration
