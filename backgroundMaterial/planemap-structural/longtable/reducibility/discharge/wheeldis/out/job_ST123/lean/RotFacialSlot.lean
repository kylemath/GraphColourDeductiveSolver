import COccBridge

/-! # RotFacialSlot: a facial triangle at an interior vertex uses consecutive rotation slots (ST-123 M3, de-risk)

`ApexFacts` (CGlue) covers only listed **interior** edges. The chord argument for 2.126 (E4 of
`ROUTE_I_PLAN.md`: `T.Adj ρ0 ρ2` with both ρ0 and ρ2 ring neighbours of I0) needs the same fact at a
**ring–interior** slot. With a rotation occurrence (`RotOcc`), any slot of `rot c` works: the third corner of a facial
triangle through `ι c` and slot `j` is slot `j + 1` or slot `j - 1` (mod the length).

- `facial_nx`: copied from ST-114 `RSSTWindowBasic.lean:30`.
- `RotOcc.facial_slot`: the general statement.
- `RotOcc.common_nbr_slot`: the `NoSep` form, as used for chords.

No `sorry`; standard axioms. -/

namespace SimpleGraph.SphericalMap
open VacancyIcosahedral DCheck DCheck.R2 RotationSystem

variable {n : ℕ} {T : SphericalMap n}

/-- A facial triangle `a b c` has `b` and `c` consecutive in the rotation at `a` (ST-114 L0, verbatim). -/
theorem facial_nx' (htri : T.Triangulated) {a b c : Fin n} (hf : Facial T a b c) :
    Nx T a b c ∨ Nx T a c b := by
  rcases hf with h | h
  · exact Or.inr (nx_tri htri h).2
  · exact Or.inl h

section
variable {cf : Conf} {ρ : ℕ → Fin n} {ι : Fin cf.m → Fin n} {rot : Fin cf.m → List (Fin cf.m ⊕ ℕ)}

/-- **The facial slot lemma.** If `ι c`, the vertex at slot `j` of `rot c` and `w` bound a face, then `w` is the
vertex at slot `j + 1` or at slot `j - 1` (indices mod `(rot c).length`). -/
theorem RotOcc.facial_slot (R : RotOcc T ρ ι rot) (htri : T.Triangulated) (c : Fin cf.m) {j : ℕ}
    (hj : j < (rot c).length) {w : Fin n}
    (hf : Facial T (ι c) (slotV ρ ι ((rot c).getD j (.inr 0))) w) :
    w = slotV ρ ι ((rot c).getD ((j + 1) % (rot c).length) (.inr 0)) ∨
      w = slotV ρ ι ((rot c).getD ((j + (rot c).length - 1) % (rot c).length) (.inr 0)) := by
  rcases facial_nx' htri hf with h | h
  · exact Or.inr (nx_func h (R.nx_at c hj))
  · exact Or.inl (nx_inj h (R.nx c j hj))

/-- **`NoSep` form.** A common neighbour `w` of `ι c` and of the vertex at slot `j` is the vertex at slot
`j ± 1`. -/
theorem RotOcc.common_nbr_slot (R : RotOcc T ρ ι rot) (htri : T.Triangulated) (hns : NoSep T)
    (c : Fin cf.m) {j : ℕ} (hj : j < (rot c).length) {w : Fin n}
    (h1 : T.Adj (ι c) w) (h2 : T.Adj (slotV ρ ι ((rot c).getD j (.inr 0))) w) :
    w = slotV ρ ι ((rot c).getD ((j + 1) % (rot c).length) (.inr 0)) ∨
      w = slotV ρ ι ((rot c).getD ((j + (rot c).length - 1) % (rot c).length) (.inr 0)) :=
  R.facial_slot htri c hj (hns _ _ _ (R.adj_of_mem c (getD_mem_rot hj)) h2 h1.symm)

/-- **Ring-slot form** (the shape used for chords). If `inr p` sits at slot `j` of `rot c`, then every common
neighbour of `ι c` and `ρ p` is the vertex at slot `j ± 1`. -/
theorem RotOcc.common_nbr_ring_slot (R : RotOcc T ρ ι rot) (htri : T.Triangulated) (hns : NoSep T)
    (c : Fin cf.m) {j p : ℕ} (hj : j < (rot c).length) (hjp : (rot c).getD j (.inr 0) = .inr p)
    {w : Fin n} (h1 : T.Adj (ι c) w) (h2 : T.Adj (ρ p) w) :
    w = slotV ρ ι ((rot c).getD ((j + 1) % (rot c).length) (.inr 0)) ∨
      w = slotV ρ ι ((rot c).getD ((j + (rot c).length - 1) % (rot c).length) (.inr 0)) :=
  R.common_nbr_slot htri hns c hj h1 (by rw [hjp]; exact h2)

end
end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.facial_nx'
#print axioms SimpleGraph.SphericalMap.RotOcc.facial_slot
#print axioms SimpleGraph.SphericalMap.RotOcc.common_nbr_slot
#print axioms SimpleGraph.SphericalMap.RotOcc.common_nbr_ring_slot
