import ClaimGlue

/-!
# ST-114 B3: the induced-window theorem (statement only)

Studio, 10 Nov. See `../B3_STATEMENT.md`. This file only **states** B3. Every proof is `sorry`, on purpose, pending the
strategy review. No existing module is edited.

For a vertex `u` of an internally 6-connected triangulation (`ClaimGlue.Internally6`, the project's frame class), let `w`
list the rotation at `u`. Then the closed 2-ball of `u` (its link, apexes, privates, and every real middle neighbour of a 9+
link vertex) is induced, with no identifications beyond the shared apexes, and every triangle in it is a face.
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

/-- **The conclusion of B3.** -/
structure WindowInduced (T : SphericalMap n) (u : Fin n) (d : ℕ) (w : ℕ → Fin n) : Prop where
  /-- `u, w_0, …, w_{d-1}` are distinct. -/
  link_inj : ∀ i j, i < d → j < d → w i = w j → i = j
  link_ne : ∀ i, w i ≠ u
  /-- (a) The link has no chord. -/
  link_chordless : ∀ i j, T.Adj (w i) (w j) → j % d = (i + 1) % d ∨ i % d = (j + 1) % d
  /-- Each link edge `w_i w_{i+1}` has exactly one apex. -/
  apex_unique : ∀ i, ∃ x, IsApex T u w i x ∧ ∀ y, IsApex T u w i y → y = x
  /-- (b)+(c) No identifications in ring 2. A ring-2 vertex sees exactly one link vertex (mod `d`), or it is the apex
  `s_i` and sees exactly `w_i` and `w_{i+1}`. -/
  r2_home : ∀ x, InR2 T u w x →
    (∃ i, i < d ∧ T.Adj (w i) x ∧ ∀ j, j < d → T.Adj (w j) x → j = i) ∨
    (∃ i, i < d ∧ IsApex T u w i x ∧ ∀ j, j < d → T.Adj (w j) x → j = i ∨ j = (i + 1) % d)
  /-- (d) Ring 2 has no chord. Adjacent ring-2 vertices share a link neighbour `w_i` and form a face with it, so they are
  consecutive in `rot(w_i)`, i.e. on the ring-2 cycle. -/
  r2_chordless : ∀ x y, InR2 T u w x → InR2 T u w y → T.Adj x y →
    ∃ i, T.Adj (w i) x ∧ T.Adj (w i) y ∧ SimpleGraph.SphericalMap.Facial T (w i) x y

/-- **B3, the induced-window theorem.** The hypotheses are the frame class `Internally6` (triangulated, connected, minimum
degree 5, no separating triangle, `NoShortSepCycle`) and a link listing of `u`. -/
theorem window_induced {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) {u : Fin n} {d : ℕ} {w : ℕ → Fin n}
    (hL : IsLink T u d w) : WindowInduced T u d w := by
  sorry

/-- F0 on the window: every triangle of `T` is a face (`noSep`), restated for downstream use (B4, B6). -/
theorem window_facial {T : SphericalMap n} (hT : ClaimGlue.Internally6 T) {a b c : Fin n}
    (hab : T.Adj a b) (hbc : T.Adj b c) (hca : T.Adj c a) : SimpleGraph.SphericalMap.Facial T a b c :=
  hT.noSep a b c hab hbc hca

end SimpleGraph.SphericalMap.RSSTSeed
