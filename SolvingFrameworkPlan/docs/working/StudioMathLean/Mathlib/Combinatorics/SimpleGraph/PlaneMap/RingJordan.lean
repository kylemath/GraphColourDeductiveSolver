module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.MinimalFrame

/-!
# Jordan separation at a vertex, for arbitrary rotation positions

`rotation_arc_separation`: let `x` be a vertex, `p` a walk between two neighbours `a` and `b`
of `x` that avoids `x`, and `u`, `w` neighbours of `x` lying strictly inside the two different
rotation arcs cut out by `a` and `b`. Then every walk from `u` to `w` that avoids `x` meets `p`.

This generalises the library's `alternating_walks_intersect` (which needs the three later
neighbours to be rotation-consecutive). It is the geometric input for the non-crossing of Kempe
chains on a ring (D-reducibility) and on a separating four-cycle.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap

variable {n : ℕ} {M : SphericalMap n}

private theorem zmod2_add_self (a : ZMod 2) : a + a = 0 := by
  rw [← two_mul, show (2 : ZMod 2) = 0 from ZMod.natCast_self 2, zero_mul]

/-- **Arc separation at a vertex.** -/
theorem rotation_arc_separation {x a b u w : Fin n} (hxa : M.Adj x a)
    {β μ ω : ℕ} (hμ : 0 < μ) (hμβ : μ < β) (hβω : β < ω)
    (hω : ω < Function.minimalPeriod (⇑M.rotation.next) (⟨(x, a), hxa⟩ : M.Dart))
    (hb : ((⇑M.rotation.next)^[β] ⟨(x, a), hxa⟩).snd = b)
    (hu : ((⇑M.rotation.next)^[μ] ⟨(x, a), hxa⟩).snd = u)
    (hw : ((⇑M.rotation.next)^[ω] ⟨(x, a), hxa⟩).snd = w)
    (p : M.graph.Walk a b) (hp : x ∉ p.support)
    (q : M.graph.Walk u w) (hq : x ∉ q.support)
    (hdis : ∀ z ∈ q.support, z ∉ p.support) : False := by
  classical
  set D0 : M.Dart := ⟨(x, a), hxa⟩
  set D : ℕ → M.Dart := fun j => (⇑M.rotation.next)^[j] D0 with hD
  have Dfst : ∀ j, (D j).fst = x := fun j => iterate_next_fst M j D0
  set P := Function.minimalPeriod (⇑M.rotation.next) D0
  have hPpos : 0 < P := by omega
  -- distinct positions below the period give distinct heads
  have head_ne : ∀ i j, i < P → j < P → i ≠ j → (D i).snd ≠ (D j).snd := by
    intro i j hi hj hij hs
    apply hij
    apply Function.iterate_injOn_Iio_minimalPeriod hi hj
    apply Dart.ext; apply Prod.ext
    · exact (Dfst i).trans (Dfst j).symm
    · exact hs
  have hbx : M.Adj b x := by
    have := (D β).adj; rw [Dfst, hb] at this; exact this.symm
  let loop : M.graph.Walk x x := .cons hxa (p.append hbx.toWalk)
  obtain ⟨c, hc⟩ := walkEdgeCoeff_is_face_sum loop
  -- edge coefficients of the loop at `x`
  have coef : ∀ j, j < P → walkEdgeCoeff loop (RotationSystem.edgeOfDart (D j)) =
      (if j = 0 then 1 else 0) + (if j = β then 1 else 0) := by
    intro j hj
    have hp0 : walkEdgeCoeff p (RotationSystem.edgeOfDart (D j)) = 0 :=
      walkEdgeCoeff_zero_of_not_mem_support p x hp _
        ((mem_edgeOfDart_iff (D j) x).2 (Or.inl (Dfst j)))
    simp only [loop, walkEdgeCoeff_cons, walkEdgeCoeff_append, hp0]
    have e1 : (RotationSystem.edgeOfDart (⟨(x, a), hxa⟩ : M.Dart) = RotationSystem.edgeOfDart (D j))
        ↔ j = 0 := by
      constructor
      · intro h
        rcases (RotationSystem.edge_of_dart_eq_iff _ _).1 h with h | h
        · by_contra hj0
          exact head_ne 0 j hPpos hj (Ne.symm hj0) (by
            have := congrArg (fun d : M.Dart => d.snd) h; exact this)
        · exfalso
          have := congrArg (fun d : M.Dart => d.fst) h
          change x = (D j).snd at this
          have h2 := (D j).adj
          rw [Dfst, ← this] at h2
          exact h2.ne rfl
      · rintro rfl; rfl
    have e2 : RotationSystem.edgeOfDart (⟨(b, x), hbx⟩ : M.Dart) =
        RotationSystem.edgeOfDart (D j) ↔ j = β := by
      constructor
      · intro h
        by_contra hjb
        rcases (RotationSystem.edge_of_dart_eq_iff _ _).1 h with h | h
        · have := congrArg (fun d : M.Dart => d.fst) h
          change b = (D j).fst at this
          have h2 := (D β).adj
          rw [Dfst, hb, this, Dfst] at h2
          exact h2.ne rfl
        · have := congrArg (fun d : M.Dart => d.fst) h
          change b = (D j).snd at this
          exact head_ne β j (by omega) hj (Ne.symm hjb) (hb.trans this)
      · intro h
        rw [h]
        apply (RotationSystem.edge_of_dart_eq_iff _ _).2
        right
        apply Dart.ext; apply Prod.ext
        · exact hb.symm
        · exact (Dfst β).symm
    simp only [Adj.toWalk, walkEdgeCoeff_cons, walkEdgeCoeff_nil, add_zero, zero_add]
    by_cases hj0 : j = 0 <;> by_cases hjb : j = β
    · exfalso; omega
    · rw [if_pos (e1.2 hj0), if_neg (fun h => hjb (e2.1 h)), if_pos hj0, if_neg hjb]
    · rw [if_neg (fun h => hj0 (e1.1 h)), if_pos (e2.2 hjb), if_neg hj0, if_pos hjb]
    · rw [if_neg (fun h => hj0 (e1.1 h)), if_neg (fun h => hjb (e2.1 h)), if_neg hj0, if_neg hjb]
  -- face values around `x`
  have step : ∀ j, j < P → c (M.faceOf (D (j + 1))) =
      c (M.faceOf (D j)) + walkEdgeCoeff loop (RotationSystem.edgeOfDart (D j)) := by
    intro j _
    have h1 : M.faceOf (D (j + 1)) = M.faceOf (D j).symm := by
      change M.faceOf ((⇑M.rotation.next)^[j + 1] D0) = _
      rw [Function.iterate_succ_apply']
      exact faceOf_next M (D j)
    rw [h1, hc, cycle_faceSum_edgeOfDart]
    rw [← add_assoc, zmod2_add_self, zero_add]
  have c0 : ∀ j, j < P → j ≠ 0 → j ≠ β →
      walkEdgeCoeff loop (RotationSystem.edgeOfDart (D j)) = 0 := by
    intro j hj h0 hb'; rw [coef j hj]; simp [h0, hb']
  have one_add : ∀ a : ZMod 2, a + 1 + 1 = a := by decide
  have val1 : ∀ j, 1 ≤ j → j ≤ β → c (M.faceOf (D j)) = c (M.faceOf (D 0)) + 1 := by
    intro j h1 hjb
    induction j with
    | zero => omega
    | succ j ih =>
      rw [step j (by omega)]
      rcases Nat.eq_zero_or_pos j with rfl | hj0
      · rw [coef 0 hPpos]; simp [show (0 : ℕ) ≠ β by omega]
      · rw [c0 j (by omega) (by omega) (by omega), add_zero, ih (by omega) (by omega)]
  have val2 : ∀ j, β < j → j ≤ ω → c (M.faceOf (D j)) = c (M.faceOf (D 0)) := by
    intro j h1 hjω
    induction j with
    | zero => omega
    | succ j ih =>
      rw [step j (by omega)]
      by_cases hjb : j = β
      · subst hjb
        rw [coef j (by omega), val1 j (by omega) le_rfl]
        simp [show j ≠ 0 by omega, one_add]
      · rw [c0 j (by omega) (by omega) hjb, add_zero, ih (by omega) (by omega)]
  have vμ := val1 μ hμ hμβ.le
  have vω := val2 ω hβω le_rfl
  -- along `q` the face value is constant
  have hloop : ∀ z ∈ q.support, z ∉ loop.support := by
    intro z hz hzl
    simp only [loop, Walk.support_cons, List.mem_cons, Walk.mem_support_append_iff,
      Adj.toWalk, Walk.support_nil, List.not_mem_nil, or_false] at hzl
    rcases hzl with rfl | hzp | rfl | rfl
    · exact hq hz
    · exact hdis z hz hzp
    · exact hdis _ hz (Walk.end_mem_support p)
    · exact hq hz
  have hu' : (D μ).symm.fst = u := hu
  have hw' : (D ω).symm.fst = w := hw
  have const := face_coeff_eq_along_disjoint_walk loop c hc q hloop (D μ).symm (D ω).symm hu' hw'
  have flip : ∀ j, j < P → j ≠ 0 → j ≠ β →
      c (M.faceOf (D j).symm) = c (M.faceOf (D j)) := by
    intro j hj h0 hb'
    have h := hc (RotationSystem.edgeOfDart (D j))
    rw [c0 j hj h0 hb', cycle_faceSum_edgeOfDart] at h
    exact (show ∀ a b : ZMod 2, 0 = a + b → b = a by decide) _ _ h
  rw [flip μ (by omega) (by omega) (by omega), flip ω hω (by omega) (by omega), vμ, vω] at const
  exact (show ∀ a : ZMod 2, a + 1 ≠ a by decide) _ const

end SimpleGraph.SphericalMap
