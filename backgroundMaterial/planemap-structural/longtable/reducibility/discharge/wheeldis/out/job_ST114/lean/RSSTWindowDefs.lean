import ClaimGlue

/-!
# ST-114 B3: window objects (definitions only)

Moved verbatim out of `RSSTWindow.lean` (10 Nov) so that the lemma files can use them; `RSSTWindow.lean` imports this.
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap VacancyIcosahedral

variable {n : ℕ}

/-- The `k`-th neighbour after `a` in the rotation at `v` (`k = 0` gives `a`). If `a` is not a neighbour of `v`, the value
is `v` (never used). -/
noncomputable def rotNbr (T : SphericalMap n) (v a : Fin n) (k : ℕ) : Fin n := by
  classical
  exact if h : T.Adj v a then (((T.rotation.next : T.Dart → T.Dart)^[k]) ⟨(v, a), h⟩).snd else v

/-- `w` lists the rotation at `u`: it is `d`-periodic, `d = deg u`, `w 0` is a neighbour of `u`, and the rotation successor
of `w i` at `u` is `w (i+1)`. This is the spec's link `w_0, …, w_{d-1}`. -/
structure IsLink (T : SphericalMap n) (u : Fin n) (d : ℕ) (w : ℕ → Fin n) : Prop where
  deg : T.graph.degree u = d
  per : ∀ i, w (i + d) = w i
  adj0 : T.Adj u (w 0)
  step : ∀ i, rotNbr T u (w i) 1 = w (i + 1)

/-- Ring 2: neither `u` nor a link vertex, but adjacent to some link vertex. This covers apexes, privates and **every**
real middle neighbour of a 9+ link vertex. -/
def InR2 (T : SphericalMap n) (u : Fin n) (w : ℕ → Fin n) (x : Fin n) : Prop :=
  x ≠ u ∧ (∀ j, w j ≠ x) ∧ ∃ i, T.Adj (w i) x

/-- `x` is the apex `s_i`: the third vertex, other than `u`, of a triangle on the link edge `w_i w_{i+1}`. -/
def IsApex (T : SphericalMap n) (u : Fin n) (w : ℕ → Fin n) (i : ℕ) (x : Fin n) : Prop :=
  x ≠ u ∧ T.Adj (w i) x ∧ T.Adj (w (i + 1)) x

end SimpleGraph.SphericalMap.RSSTSeed
