/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterRotationPlanar

/-!
# The forward link-changing move `π` at a pentagonal hole (backbone of Theorem W)

Conventions as in `QuarterFloor` / `QuarterRotation`. A proper-off state `c` is either
*unfilled* with repeat index `j` (`RepeatAt P c j`, link `(α, μ, α, A, B)` at `j, …, j+4`) or
*filled* with singleton position `i` (`SingletonAt P c i`, link `(W, X, Y, X, Y)` at
`i, …, i+4`, fourth colour `Z = zcol P c i`), and exactly one `j` resp. `i` occurs
(`classify`, `rep_unique`, `single_unique`, `rep_not_target`).

The forward move `π = piMove P` follows the table of `NightEulerHole.md` §3 exactly:

| state | condition | move | image | λ |
|---|---|---|---|---|
| `U_j` | `Lock2 j` | `R₊₃` = `rot3`: swap `{α,A}`-comp. of `x (j+2)` | `U_{j+3}`, `Lock1` | `+1` |
| `U_j` | `¬ Lock2 j` | `φ_B⁻¹` = `phiBinv`: swap `{μ,B}`-comp. of `x (j+4)` | `F_{j+3}`, `M2` short | `-1` |
| `F_i` | `M3` short | `φ_A` = `phiA`: swap `{Y,Z}`-comp. of `x (i+2)` | `U_{i+1}`, `¬ Lock1` | `-1` |
| `F_i` | `M3` long | `τ` = `tau`: swap `{W,X}`-comp. of `x (i+3)` | `F_{i+1}`, `M2` long | `-3` |

Here `M3Short P c i` is "`x (i+2)` and `x (i+4)` lie in different `{Y,Z}`-components" and
`M2Short P c i` is "`x (i+1)` and `x (i+3)` lie in different `{X,Z}`-components"; "long" is the
negation. The backward move `piInv` splits by `Lock1` / `M2Short` and uses `R₊₂`, `φ_A⁻¹`,
`φ_B`, `τ⁻¹` (`phiAinv`, `phiB`, `tauInv`).

## Main results (sorry-free, on any `SphericalMap`; no triangulation hypothesis)

* `piMove_kempeStep`, `piMove_properOff`: every `π`-step is a single Kempe swap.
* `piInv_piMove`, `piMove_piInv`: `piInv` is a two-sided inverse on proper-off states.
* `piPerm`: `π` as a permutation of the proper-off states;
  `piMove_bijOn_class`: `π` restricts to a bijection of every Kempe class (**Lemma Π**).
* `sigma_piMove`: the token sum `σ` (`2j+1` on `U_j`, `2i+4` on `F_i`, in `ZMod 5`-style
  `Fin 5`) moves by the table's `λ` (`lam`): `σ (π c) = σ c + λ c`.

Planarity enters only through Jordan separation at the hole (a private copy of `NoFrozen`'s
`lock_separates`/`no_cross`, as in `QuarterRotationPlanar`): it makes `R₊₃`, `R₊₂`, `τ`, `τ⁻¹`
well defined (the swapped component misses the protected link vertex). The converse
dichotomies (Hex: e.g. "`M3` long iff `x i ~ x (i+3)` fails in `{W,X}`" in its other direction)
are **not** needed for Lemma Π: the cases of `π` are split by `Lock2`/`M3Short` and those of
`π⁻¹` by `Lock1`/`M2Short`, and each image lands in the matching case of the other split.

## Not formalised here

* The counting consequences of Theorem W (`3F − U = −Σ λ`, `Σ_Z λ ≡ 0 mod 5` on each
  `π`-cycle, the winding number), which need finite class sums.
* The statement that `π`, `π⁻¹` are the *only* two link-pattern-changing moves (up to the
  alternative component), i.e. Intern B's "exactly two slots"; only the existence half is here.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### Finite facts about `Fin 4` -/

/-- The fourth colour: for distinct `a b d : Fin 4`, the unique colour different from all three. -/
def fourth (a b d : Fin 4) : Fin 4 := 2 - a - b - d

lemma fourth_ne {a b d : Fin 4} (hab : a ≠ b) (had : a ≠ d) (hbd : b ≠ d) :
    fourth a b d ≠ a ∧ fourth a b d ≠ b ∧ fourth a b d ≠ d := by
  revert a b d; decide

lemma fourth_eq {a b d x : Fin 4} (hab : a ≠ b) (had : a ≠ d) (hbd : b ≠ d)
    (hxa : x ≠ a) (hxb : x ≠ b) (hxd : x ≠ d) : fourth a b d = x := by
  revert a b d x; decide

lemma fin4_five {a b d e x : Fin 4} (hab : a ≠ b) (had : a ≠ d) (hae : a ≠ e) (hbd : b ≠ d)
    (hbe : b ≠ e) (hde : d ≠ e) (hxa : x ≠ a) (hxb : x ≠ b) (hxd : x ≠ d) (hxe : x ≠ e) :
    False := by
  revert a b d e x; decide

/-- Repeat pattern on five consecutive link values. -/
def RepV (a0 a1 a2 a3 a4 : Fin 4) : Prop :=
  a0 = a2 ∧ a1 ≠ a0 ∧ a3 ≠ a0 ∧ a4 ≠ a0 ∧ a1 ≠ a3 ∧ a1 ≠ a4 ∧ a3 ≠ a4

instance (a0 a1 a2 a3 a4 : Fin 4) : Decidable (RepV a0 a1 a2 a3 a4) := by
  unfold RepV; infer_instance

/-- Singleton pattern (first value unique) on five consecutive link values. -/
def SingV (a0 a1 a2 a3 a4 : Fin 4) : Prop :=
  a1 ≠ a0 ∧ a2 ≠ a0 ∧ a3 ≠ a0 ∧ a4 ≠ a0

instance (a0 a1 a2 a3 a4 : Fin 4) : Decidable (SingV a0 a1 a2 a3 a4) := by
  unfold SingV; infer_instance

/-- Every proper colouring of a 5-cycle with 4 colours is a repeat pattern at some index, or
misses a colour and has a singleton. -/
lemma classify5 : ∀ a0 a1 a2 a3 a4 : Fin 4, a0 ≠ a1 → a1 ≠ a2 → a2 ≠ a3 → a3 ≠ a4 → a4 ≠ a0 →
    RepV a0 a1 a2 a3 a4 ∨ RepV a1 a2 a3 a4 a0 ∨ RepV a2 a3 a4 a0 a1 ∨ RepV a3 a4 a0 a1 a2 ∨
      RepV a4 a0 a1 a2 a3 ∨
      ((∃ x, a0 ≠ x ∧ a1 ≠ x ∧ a2 ≠ x ∧ a3 ≠ x ∧ a4 ≠ x) ∧
        (SingV a0 a1 a2 a3 a4 ∨ SingV a1 a2 a3 a4 a0 ∨ SingV a2 a3 a4 a0 a1 ∨
          SingV a3 a4 a0 a1 a2 ∨ SingV a4 a0 a1 a2 a3)) := by
  decide

/-! ### Kempe swaps of a whole component -/

section kswap
variable {V : Type*} (G : SimpleGraph V) (h : V)

/-- Swap the `{a, b}`-component (in `G - h`) of the seed `s`. -/
noncomputable def kswap (c : V → Fin 4) (a b : Fin 4) (s : V) : V → Fin 4 :=
  swap c a b {v | (pairGraph G h c a b).Reachable s v}

variable {G h} {c : V → Fin 4} {a b : Fin 4} {s v : V}

lemma kswap_mem (hv : (pairGraph G h c a b).Reachable s v) (hcv : c v = a) :
    kswap G h c a b s v = b := by
  unfold kswap
  rw [swap_in (show v ∈ {w | (pairGraph G h c a b).Reachable s w} from hv), hcv,
    Equiv.swap_apply_left]

lemma kswap_mem' (hv : (pairGraph G h c a b).Reachable s v) (hcv : c v = b) :
    kswap G h c a b s v = a := by
  unfold kswap
  rw [swap_in (show v ∈ {w | (pairGraph G h c a b).Reachable s w} from hv), hcv,
    Equiv.swap_apply_right]

lemma kswap_out (hv : ¬ (pairGraph G h c a b).Reachable s v) : kswap G h c a b s v = c v :=
  swap_out hv

lemma kswap_other (ha : c v ≠ a) (hb : c v ≠ b) : kswap G h c a b s v = c v :=
  swap_other ha hb

lemma kswap_pg : pairGraph G h (kswap G h c a b s) a b = pairGraph G h c a b :=
  pairGraph_swap_same _ _ _ _

lemma kswap_pg' : pairGraph G h (kswap G h c a b s) b a = pairGraph G h c a b :=
  (pairGraph_comm _ _ _).trans kswap_pg

lemma kswap_pg_other {x y : Fin 4} (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairGraph G h (kswap G h c a b s) x y = pairGraph G h c x y :=
  pairGraph_swap_other _ _ _ _ hxa hxb hya hyb

lemma swap_comm' (c : V → Fin 4) (a b : Fin 4) (S : Set V) : swap c b a S = swap c a b S := by
  classical
  funext v
  by_cases hv : v ∈ S
  · rw [swap_in hv, swap_in hv, Equiv.swap_comm]
  · rw [swap_out hv, swap_out hv]

lemma kswap_inv : kswap G h (kswap G h c a b s) a b s = c := by
  unfold kswap
  rw [pairGraph_swap_same]
  exact swap_swap _ _ _ _

lemma kswap_inv' : kswap G h (kswap G h c a b s) b a s = c := by
  have e : kswap G h (kswap G h c a b s) b a s = kswap G h (kswap G h c a b s) a b s := by
    unfold kswap
    rw [pairGraph_comm _ b a, swap_comm']
  rw [e]
  exact kswap_inv

lemma kswap_step (hab : a ≠ b) (hs : s ≠ h) (hcs : c s = a ∨ c s = b) :
    KempeStep G h c (kswap G h c a b s) :=
  ⟨a, b, _, hab, whole_component G h c a b s ⟨hs, hcs⟩, rfl⟩

end kswap

/-! ### The moves and the case split (no planarity) -/

section generic
variable {V : Type*} {G : SimpleGraph V} {h : V} (P : Pent G h)

/-- The fourth colour `Z` of a filled state with singleton at `i`. -/
def zcol (c : V → Fin 4) (i : Fin 5) : Fin 4 :=
  fourth (c (P.x i)) (c (P.x (i + 1))) (c (P.x (i + 2)))

/-- `M3` short at a filled state `F_i`: `x (i+2)` and `x (i+4)` lie in different
`{Y, Z}`-components. -/
def M3Short (c : V → Fin 4) (i : Fin 5) : Prop :=
  ¬ (pairGraph G h c (c (P.x (i + 2))) (zcol P c i)).Reachable (P.x (i + 2)) (P.x (i + 4))

/-- `M2` short at a filled state `F_i`: `x (i+1)` and `x (i+3)` lie in different
`{X, Z}`-components. -/
def M2Short (c : V → Fin 4) (i : Fin 5) : Prop :=
  ¬ (pairGraph G h c (c (P.x (i + 1))) (zcol P c i)).Reachable (P.x (i + 1)) (P.x (i + 3))

/-- `φ_B⁻¹` at `U_j`: swap the `{μ, B}`-component of `x (j+4)`. -/
noncomputable def phiBinv (c : V → Fin 4) (j : Fin 5) : V → Fin 4 :=
  kswap G h c (c (P.x (j + 1))) (c (P.x (j + 4))) (P.x (j + 4))

/-- `φ_A⁻¹` at `U_k`: swap the `{μ, A}`-component of `x (k+1)`. -/
noncomputable def phiAinv (c : V → Fin 4) (k : Fin 5) : V → Fin 4 :=
  kswap G h c (c (P.x (k + 1))) (c (P.x (k + 3))) (P.x (k + 1))

/-- `φ_A` at `F_i`: swap the `{Y, Z}`-component of `x (i+2)`. -/
noncomputable def phiA (c : V → Fin 4) (i : Fin 5) : V → Fin 4 :=
  kswap G h c (c (P.x (i + 2))) (zcol P c i) (P.x (i + 2))

/-- `φ_B` at `F_i`: swap the `{X, Z}`-component of `x (i+1)`. -/
noncomputable def phiB (c : V → Fin 4) (i : Fin 5) : V → Fin 4 :=
  kswap G h c (c (P.x (i + 1))) (zcol P c i) (P.x (i + 1))

/-- `τ` at `F_i`: swap the `{W, X}`-component of `x (i+3)`. -/
noncomputable def tau (c : V → Fin 4) (i : Fin 5) : V → Fin 4 :=
  kswap G h c (c (P.x i)) (c (P.x (i + 1))) (P.x (i + 3))

/-- `τ⁻¹` at `F_i`: swap the `{W, Y}`-component of `x (i+2)`. -/
noncomputable def tauInv (c : V → Fin 4) (i : Fin 5) : V → Fin 4 :=
  kswap G h c (c (P.x i)) (c (P.x (i + 2))) (P.x (i + 2))

open Classical in
/-- **The forward move `π`** (table of `NightEulerHole.md` §3). The final `else` branch is
never taken on proper-off states (`classify`). -/
noncomputable def piMove (c : V → Fin 4) : V → Fin 4 :=
  if hr : ∃ j, RepeatAt P c j then
    (if Lock2 P c hr.choose then rot3 P c hr.choose else phiBinv P c hr.choose)
  else if hs : ∃ i, SingletonAt P c i then
    (if M3Short P c hs.choose then phiA P c hs.choose else tau P c hs.choose)
  else c

open Classical in
/-- **The backward move `π⁻¹`.** -/
noncomputable def piInv (c : V → Fin 4) : V → Fin 4 :=
  if hr : ∃ j, RepeatAt P c j then
    (if Lock1 P c hr.choose then rot2 P c hr.choose else phiAinv P c hr.choose)
  else if hs : ∃ i, SingletonAt P c i then
    (if M2Short P c hs.choose then phiB P c hs.choose else tauInv P c hs.choose)
  else c

open Classical in
/-- The token sum `σ` (sum of the two single-Tait-edge positions): `2j+1` on `U_j`,
`2i+4` on `F_i`. -/
noncomputable def sigma (c : V → Fin 4) : Fin 5 :=
  if hr : ∃ j, RepeatAt P c j then 2 * hr.choose + 1
  else if hs : ∃ i, SingletonAt P c i then 2 * hs.choose + 4
  else 0

open Classical in
/-- The token step `λ` of the table. -/
noncomputable def lam (c : V → Fin 4) : ℤ :=
  if hr : ∃ j, RepeatAt P c j then (if Lock2 P c hr.choose then 1 else -1)
  else if hs : ∃ i, SingletonAt P c i then (if M3Short P c hs.choose then -1 else -3)
  else 0

variable {P} {c : V → Fin 4}

lemma link_ne (hc : ProperOff G h c) (k l : Fin 5) (hkl : k + 1 = l) :
    c (P.x k) ≠ c (P.x l) := by
  subst hkl
  exact hc (P.adj_cyc k) (P.x_ne_h k) (P.x_ne_h _)

lemma target_of_vals (x : Fin 4) (hx : ∀ k, c (P.x k) ≠ x) : Target G h c := by
  refine ⟨x, ?_⟩
  intro v hv
  obtain ⟨k, rfl⟩ := P.only v hv
  exact hx k

lemma singletonAt_of (i : Fin 5) (ht : Target G h c)
    (h1 : c (P.x (i + 1)) ≠ c (P.x i)) (h2 : c (P.x (i + 2)) ≠ c (P.x i))
    (h3 : c (P.x (i + 3)) ≠ c (P.x i)) (h4 : c (P.x (i + 4)) ≠ c (P.x i)) :
    SingletonAt P c i := by
  refine ⟨ht, fun k hk => ?_⟩
  rcases fin5_cases i k with rfl | rfl | rfl | rfl | rfl
  · exact absurd rfl hk
  · exact h1
  · exact h2
  · exact h3
  · exact h4

/-- Every proper-off state is unfilled (some repeat index) or filled (some singleton). -/
theorem classify (hc : ProperOff G h c) : (∃ j, RepeatAt P c j) ∨ ∃ i, SingletonAt P c i := by
  have l0 := link_ne (P := P) hc 0 1 rfl
  have l1 := link_ne (P := P) hc 1 2 rfl
  have l2 := link_ne (P := P) hc 2 3 rfl
  have l3 := link_ne (P := P) hc 3 4 rfl
  have l4 := link_ne (P := P) hc 4 0 rfl
  rcases classify5 _ _ _ _ _ l0 l1 l2 l3 l4 with r | r | r | r | r | ⟨⟨x, m0, m1, m2, m3, m4⟩, s⟩
  · exact Or.inl ⟨0, r⟩
  · exact Or.inl ⟨1, r⟩
  · exact Or.inl ⟨2, r⟩
  · exact Or.inl ⟨3, r⟩
  · exact Or.inl ⟨4, r⟩
  · have ht : Target G h c := target_of_vals x (fun k => by fin_cases k <;> assumption)
    right
    rcases s with ⟨s1, s2, s3, s4⟩ | ⟨s1, s2, s3, s4⟩ | ⟨s1, s2, s3, s4⟩ | ⟨s1, s2, s3, s4⟩ |
      ⟨s1, s2, s3, s4⟩
    · exact ⟨0, singletonAt_of 0 ht s1 s2 s3 s4⟩
    · exact ⟨1, singletonAt_of 1 ht s1 s2 s3 s4⟩
    · exact ⟨2, singletonAt_of 2 ht s1 s2 s3 s4⟩
    · exact ⟨3, singletonAt_of 3 ht s1 s2 s3 s4⟩
    · exact ⟨4, singletonAt_of 4 ht s1 s2 s3 s4⟩

/-- The repeat index is unique. -/
theorem rep_unique {j j' : Fin 5} (hr : RepeatAt P c j) (hr' : RepeatAt P c j') : j' = j := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have e := hr'.1
  rcases fin5_cases j j' with rfl | rfl | rfl | rfl | rfl
  · rfl
  · simp only [add_assoc, Fin.reduceAdd] at e; exact absurd e h13
  · simp only [add_assoc, Fin.reduceAdd] at e; rw [← h02] at e; exact absurd e.symm h4
  · simp only [add_assoc, Fin.reduceAdd, add_zero] at e; exact absurd e h3
  · simp only [add_assoc, Fin.reduceAdd] at e; exact absurd e.symm h14

/-- An unfilled state is not filled. -/
theorem rep_not_target {j : Fin 5} (hr : RepeatAt P c j) : ¬ Target G h c := by
  rintro ⟨x, hx⟩
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  exact fin4_five (Ne.symm h1) (Ne.symm h3) (Ne.symm h4) h13 h14 h34
    (Ne.symm (hx (P.adj_h j))) (Ne.symm (hx (P.adj_h _))) (Ne.symm (hx (P.adj_h _)))
    (Ne.symm (hx (P.adj_h _)))

/-- The link of a filled state is `(W, X, Y, X, Y)`, and `Z` is the fourth colour. -/
theorem filled_shape (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    c (P.x (i + 3)) = c (P.x (i + 1)) ∧ c (P.x (i + 4)) = c (P.x (i + 2)) ∧
    c (P.x i) ≠ c (P.x (i + 1)) ∧ c (P.x i) ≠ c (P.x (i + 2)) ∧
    c (P.x (i + 1)) ≠ c (P.x (i + 2)) ∧
    zcol P c i ≠ c (P.x i) ∧ zcol P c i ≠ c (P.x (i + 1)) ∧ zcol P c i ≠ c (P.x (i + 2)) := by
  obtain ⟨⟨x, hx⟩, hsg⟩ := hs
  have m : ∀ k, c (P.x k) ≠ x := fun k => hx (P.adj_h k)
  have s1 : c (P.x (i + 1)) ≠ c (P.x i) := hsg _ (by simp)
  have s2 : c (P.x (i + 2)) ≠ c (P.x i) := hsg _ (by simp)
  have s3 : c (P.x (i + 3)) ≠ c (P.x i) := hsg _ (by simp)
  have s4 : c (P.x (i + 4)) ≠ c (P.x i) := hsg _ (by simp)
  have l12 : c (P.x (i + 1)) ≠ c (P.x (i + 2)) :=
    link_ne hc _ _ (by simp only [add_assoc, Fin.reduceAdd])
  have l23 : c (P.x (i + 2)) ≠ c (P.x (i + 3)) :=
    link_ne hc _ _ (by simp only [add_assoc, Fin.reduceAdd])
  have l34 : c (P.x (i + 3)) ≠ c (P.x (i + 4)) :=
    link_ne hc _ _ (by simp only [add_assoc, Fin.reduceAdd])
  have e3 : c (P.x (i + 3)) = c (P.x (i + 1)) :=
    fin4_fourth _ _ _ _ _ s2 (m _) (m i) (Ne.symm l23) s3 (m _) l12 s1 (m _)
  have e4 : c (P.x (i + 4)) = c (P.x (i + 2)) :=
    fin4_fourth _ _ _ _ _ s3 (m _) (m i) (Ne.symm l34) s4 (m _) l23 s2 (m _)
  obtain ⟨z0, z1, z2⟩ := fourth_ne (Ne.symm s1) (Ne.symm s2) l12
  exact ⟨e3, e4, Ne.symm s1, Ne.symm s2, l12, z0, z1, z2⟩

/-- The singleton position is unique. -/
theorem single_unique (hc : ProperOff G h c) {i i' : Fin 5} (hs : SingletonAt P c i)
    (hs' : SingletonAt P c i') : i' = i := by
  obtain ⟨e3, e4, -⟩ := filled_shape hc hs
  rcases fin5_cases i i' with rfl | rfl | rfl | rfl | rfl
  · rfl
  · exact absurd e3 (hs'.2 (i + 3) (by simp))
  · exact absurd e4 (hs'.2 (i + 4) (by simp))
  · exact absurd e3.symm (hs'.2 (i + 1) (by simp))
  · exact absurd e4.symm (hs'.2 (i + 2) (by simp))

/-- A filled state with prescribed link values. -/
lemma single_of_vals {d : V → Fin 4} {i : Fin 5} {W X Y Z : Fin 4}
    (v0 : d (P.x i) = W) (v1 : d (P.x (i + 1)) = X) (v2 : d (P.x (i + 2)) = Y)
    (v3 : d (P.x (i + 3)) = X) (v4 : d (P.x (i + 4)) = Y)
    (hWX : W ≠ X) (hWY : W ≠ Y) (hXY : X ≠ Y) (hZW : Z ≠ W) (hZX : Z ≠ X) (hZY : Z ≠ Y) :
    SingletonAt P d i ∧ zcol P d i = Z := by
  refine ⟨singletonAt_of i (target_of_vals (P := P) Z fun k => ?_) ?_ ?_ ?_ ?_, ?_⟩
  · rcases fin5_cases i k with rfl | rfl | rfl | rfl | rfl
    · rw [v0]; exact Ne.symm hZW
    · rw [v1]; exact Ne.symm hZX
    · rw [v2]; exact Ne.symm hZY
    · rw [v3]; exact Ne.symm hZX
    · rw [v4]; exact Ne.symm hZY
  · rw [v0, v1]; exact Ne.symm hWX
  · rw [v0, v2]; exact Ne.symm hWY
  · rw [v0, v3]; exact Ne.symm hWX
  · rw [v0, v4]; exact Ne.symm hWY
  · unfold zcol; rw [v0, v1, v2]; exact fourth_eq hWX hWY hXY hZW hZX hZY

/-- An unfilled state with prescribed link values. -/
lemma rep_of_vals {d : V → Fin 4} {j : Fin 5} {α μ A B : Fin 4}
    (v0 : d (P.x j) = α) (v1 : d (P.x (j + 1)) = μ) (v2 : d (P.x (j + 2)) = α)
    (v3 : d (P.x (j + 3)) = A) (v4 : d (P.x (j + 4)) = B)
    (h1 : μ ≠ α) (h3 : A ≠ α) (h4 : B ≠ α) (h13 : μ ≠ A) (h14 : μ ≠ B) (h34 : A ≠ B) :
    RepeatAt P d j := by
  unfold RepeatAt; rw [v0, v1, v2, v3, v4]; exact ⟨rfl, h1, h3, h4, h13, h14, h34⟩

/-! #### Evaluating `π`, `π⁻¹`, `σ`, `λ` by cases -/

open Classical in
lemma piMove_rep {j : Fin 5} (hr : RepeatAt P c j) :
    piMove P c = (if Lock2 P c j then rot3 P c j else phiBinv P c j) := by
  have hex : ∃ j, RepeatAt P c j := ⟨j, hr⟩
  have e : hex.choose = j := rep_unique hr hex.choose_spec
  unfold piMove
  rw [dite_eq_left hex]
  simp only [e]

open Classical in
lemma piMove_single (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    piMove P c = (if M3Short P c i then phiA P c i else tau P c i) := by
  have hnr : ¬ ∃ j, RepeatAt P c j := fun ⟨_, hr⟩ => rep_not_target hr hs.1
  have hex : ∃ i, SingletonAt P c i := ⟨i, hs⟩
  have e : hex.choose = i := single_unique hc hs hex.choose_spec
  unfold piMove
  rw [dite_eq_right hnr, dite_eq_left hex]
  simp only [e]

open Classical in
lemma piInv_rep {j : Fin 5} (hr : RepeatAt P c j) :
    piInv P c = (if Lock1 P c j then rot2 P c j else phiAinv P c j) := by
  have hex : ∃ j, RepeatAt P c j := ⟨j, hr⟩
  have e : hex.choose = j := rep_unique hr hex.choose_spec
  unfold piInv
  rw [dite_eq_left hex]
  simp only [e]

open Classical in
lemma piInv_single (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    piInv P c = (if M2Short P c i then phiB P c i else tauInv P c i) := by
  have hnr : ¬ ∃ j, RepeatAt P c j := fun ⟨_, hr⟩ => rep_not_target hr hs.1
  have hex : ∃ i, SingletonAt P c i := ⟨i, hs⟩
  have e : hex.choose = i := single_unique hc hs hex.choose_spec
  unfold piInv
  rw [dite_eq_right hnr, dite_eq_left hex]
  simp only [e]

lemma sigma_rep {j : Fin 5} (hr : RepeatAt P c j) : sigma P c = 2 * j + 1 := by
  have hex : ∃ j, RepeatAt P c j := ⟨j, hr⟩
  have e : hex.choose = j := rep_unique hr hex.choose_spec
  unfold sigma
  rw [dite_eq_left hex, e]

lemma sigma_single (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    sigma P c = 2 * i + 4 := by
  have hnr : ¬ ∃ j, RepeatAt P c j := fun ⟨_, hr⟩ => rep_not_target hr hs.1
  have hex : ∃ i, SingletonAt P c i := ⟨i, hs⟩
  have e : hex.choose = i := single_unique hc hs hex.choose_spec
  unfold sigma
  rw [dite_eq_right hnr, dite_eq_left hex, e]

open Classical in
lemma lam_rep {j : Fin 5} (hr : RepeatAt P c j) :
    lam P c = (if Lock2 P c j then 1 else -1) := by
  have hex : ∃ j, RepeatAt P c j := ⟨j, hr⟩
  have e : hex.choose = j := rep_unique hr hex.choose_spec
  unfold lam
  rw [dite_eq_left hex]
  simp only [e]

open Classical in
lemma lam_single (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    lam P c = (if M3Short P c i then -1 else -3) := by
  have hnr : ¬ ∃ j, RepeatAt P c j := fun ⟨_, hr⟩ => rep_not_target hr hs.1
  have hex : ∃ i, SingletonAt P c i := ⟨i, hs⟩
  have e : hex.choose = i := single_unique hc hs hex.choose_spec
  unfold lam
  rw [dite_eq_right hnr, dite_eq_left hex]
  simp only [e]

end generic

/-! ### The individual moves (no planarity) -/

section moves
variable {V : Type*} {G : SimpleGraph V} {h : V} {P : Pent G h} {c : V → Fin 4}

/-- `φ_B⁻¹`: from `U_j` with lock 2 failing to `F_{j+3}` with `M2` short; undone by `φ_B`. -/
theorem phiBinv_spec (hc : ProperOff G h c) {j : Fin 5} (hr : RepeatAt P c j)
    (hl : ¬ Lock2 P c j) :
    KempeStep G h c (phiBinv P c j) ∧ ProperOff G h (phiBinv P c j) ∧
      SingletonAt P (phiBinv P c j) (j + 3) ∧ M2Short P (phiBinv P c j) (j + 3) ∧
      phiB P (phiBinv P c j) (j + 3) = c := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have hout : ¬ (pairGraph G h c (c (P.x (j + 1))) (c (P.x (j + 4)))).Reachable
      (P.x (j + 4)) (P.x (j + 1)) := fun r => hl r.symm
  have v0 : phiBinv P c j (P.x j) = c (P.x j) := kswap_other (Ne.symm h1) (Ne.symm h4)
  have v1 : phiBinv P c j (P.x (j + 1)) = c (P.x (j + 1)) := kswap_out hout
  have v2 : phiBinv P c j (P.x (j + 2)) = c (P.x j) :=
    (kswap_other (by rw [← h02]; exact Ne.symm h1) (by rw [← h02]; exact Ne.symm h4)).trans
      h02.symm
  have v3 : phiBinv P c j (P.x (j + 3)) = c (P.x (j + 3)) := kswap_other (Ne.symm h13) h34
  have v4 : phiBinv P c j (P.x (j + 4)) = c (P.x (j + 1)) := kswap_mem' (Reachable.refl _) rfl
  have step : KempeStep G h c (phiBinv P c j) := kswap_step h14 (P.x_ne_h _) (Or.inr rfl)
  obtain ⟨hs, hz⟩ := single_of_vals (P := P) (i := j + 3) (Z := c (P.x (j + 4))) v3
    (by simp only [add_assoc, Fin.reduceAdd]; exact v4)
    (by simp only [add_assoc, Fin.reduceAdd, add_zero]; exact v0)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v1)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v2)
    (Ne.symm h13) h3 h1 (Ne.symm h34) (Ne.symm h14) h4
  refine ⟨step, kempe_proper G hc step, hs, ?_, ?_⟩
  · unfold M2Short
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd]
    rw [v4]; erw [kswap_pg]
    exact hout
  · unfold phiB
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd]
    rw [v4]
    exact kswap_inv

/-- `φ_A`: from `F_i` with `M3` short to `U_{i+1}` with lock 1 failing; undone by `φ_A⁻¹`. -/
theorem phiA_spec (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i)
    (hm : M3Short P c i) :
    KempeStep G h c (phiA P c i) ∧ ProperOff G h (phiA P c i) ∧
      RepeatAt P (phiA P c i) (i + 1) ∧ ¬ Lock1 P (phiA P c i) (i + 1) ∧
      phiAinv P (phiA P c i) (i + 1) = c := by
  obtain ⟨e3, e4, sWX, sWY, sXY, zW, zX, zY⟩ := filled_shape hc hs
  have v0 : phiA P c i (P.x i) = c (P.x i) := kswap_other sWY (Ne.symm zW)
  have v1 : phiA P c i (P.x (i + 1)) = c (P.x (i + 1)) := kswap_other sXY (Ne.symm zX)
  have v2 : phiA P c i (P.x (i + 2)) = zcol P c i := kswap_mem (Reachable.refl _) rfl
  have v3 : phiA P c i (P.x (i + 3)) = c (P.x (i + 1)) :=
    (kswap_other (by rw [e3]; exact sXY) (by rw [e3]; exact Ne.symm zX)).trans e3
  have v4 : phiA P c i (P.x (i + 4)) = c (P.x (i + 2)) := (kswap_out hm).trans e4
  have step : KempeStep G h c (phiA P c i) :=
    kswap_step (Ne.symm zY) (P.x_ne_h _) (Or.inl rfl)
  refine ⟨step, kempe_proper G hc step, ?_, ?_, ?_⟩
  · refine rep_of_vals (P := P) v1 (by simp only [add_assoc, Fin.reduceAdd]; exact v2)
      (by simp only [add_assoc, Fin.reduceAdd]; exact v3)
      (by simp only [add_assoc, Fin.reduceAdd]; exact v4)
      (by simp only [add_assoc, Fin.reduceAdd, add_zero]; exact v0)
      zX (Ne.symm sXY) sWX zY zW (Ne.symm sWY)
  · unfold Lock1
    simp only [add_assoc, Fin.reduceAdd]
    rw [v2, v4]; erw [kswap_pg']
    exact hm
  · unfold phiAinv
    simp only [add_assoc, Fin.reduceAdd]
    rw [v2, v4]
    exact kswap_inv'

/-- `φ_A⁻¹`: from `U_k` with lock 1 failing to `F_{k+4}` with `M3` short; undone by `φ_A`. -/
theorem phiAinv_spec (hc : ProperOff G h c) {k : Fin 5} (hr : RepeatAt P c k)
    (hl : ¬ Lock1 P c k) :
    KempeStep G h c (phiAinv P c k) ∧ ProperOff G h (phiAinv P c k) ∧
      SingletonAt P (phiAinv P c k) (k + 4) ∧ M3Short P (phiAinv P c k) (k + 4) ∧
      phiA P (phiAinv P c k) (k + 4) = c := by
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  have v0 : phiAinv P c k (P.x k) = c (P.x k) := kswap_other (Ne.symm h1) (Ne.symm h3)
  have v1 : phiAinv P c k (P.x (k + 1)) = c (P.x (k + 3)) := kswap_mem (Reachable.refl _) rfl
  have v2 : phiAinv P c k (P.x (k + 2)) = c (P.x k) :=
    (kswap_other (by rw [← h02]; exact Ne.symm h1) (by rw [← h02]; exact Ne.symm h3)).trans
      h02.symm
  have v3 : phiAinv P c k (P.x (k + 3)) = c (P.x (k + 3)) := kswap_out hl
  have v4 : phiAinv P c k (P.x (k + 4)) = c (P.x (k + 4)) := kswap_other (Ne.symm h14) (Ne.symm h34)
  have step : KempeStep G h c (phiAinv P c k) := kswap_step h13 (P.x_ne_h _) (Or.inl rfl)
  obtain ⟨hs, hz⟩ := single_of_vals (P := P) (i := k + 4) (Z := c (P.x (k + 1))) v4
    (by simp only [add_assoc, Fin.reduceAdd, add_zero]; exact v0)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v1)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v2)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v3)
    h4 (Ne.symm h34) (Ne.symm h3) h14 h1 h13
  refine ⟨step, kempe_proper G hc step, hs, ?_, ?_⟩
  · unfold M3Short
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd]
    rw [v1]; erw [kswap_pg']
    exact hl
  · unfold phiA
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd]
    rw [v1]
    exact kswap_inv'

/-- `φ_B`: from `F_i` with `M2` short to `U_{i+2}` with lock 2 failing; undone by `φ_B⁻¹`. -/
theorem phiB_spec (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i)
    (hm : M2Short P c i) :
    KempeStep G h c (phiB P c i) ∧ ProperOff G h (phiB P c i) ∧
      RepeatAt P (phiB P c i) (i + 2) ∧ ¬ Lock2 P (phiB P c i) (i + 2) ∧
      phiBinv P (phiB P c i) (i + 2) = c := by
  obtain ⟨e3, e4, sWX, sWY, sXY, zW, zX, zY⟩ := filled_shape hc hs
  have v0 : phiB P c i (P.x i) = c (P.x i) := kswap_other sWX (Ne.symm zW)
  have v1 : phiB P c i (P.x (i + 1)) = zcol P c i := kswap_mem (Reachable.refl _) rfl
  have v2 : phiB P c i (P.x (i + 2)) = c (P.x (i + 2)) := kswap_other (Ne.symm sXY) (Ne.symm zY)
  have v3 : phiB P c i (P.x (i + 3)) = c (P.x (i + 1)) := (kswap_out hm).trans e3
  have v4 : phiB P c i (P.x (i + 4)) = c (P.x (i + 2)) :=
    (kswap_other (by rw [e4]; exact Ne.symm sXY) (by rw [e4]; exact Ne.symm zY)).trans e4
  have step : KempeStep G h c (phiB P c i) :=
    kswap_step (Ne.symm zX) (P.x_ne_h _) (Or.inl rfl)
  refine ⟨step, kempe_proper G hc step, ?_, ?_, ?_⟩
  · refine rep_of_vals (P := P) v2 (by simp only [add_assoc, Fin.reduceAdd]; exact v3)
      (by simp only [add_assoc, Fin.reduceAdd]; exact v4)
      (by simp only [add_assoc, Fin.reduceAdd, add_zero]; exact v0)
      (by simp only [add_assoc, Fin.reduceAdd]; exact v1)
      sXY sWY zY (Ne.symm sWX) (Ne.symm zX) (Ne.symm zW)
  · unfold Lock2
    simp only [add_assoc, Fin.reduceAdd]
    rw [v1, v3]; erw [kswap_pg]
    exact fun r => hm r.symm
  · unfold phiBinv
    simp only [add_assoc, Fin.reduceAdd]
    rw [v1, v3]
    exact kswap_inv

end moves

/-! ### Jordan separation at the hole (private copy, as in `QuarterRotationPlanar`) -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} (P : Pent M.graph h)

section fin
private lemma fin5_a (j : Fin 5) : j + 2 + 1 = j + 3 ∧ j + 2 + 2 = j + 4 ∧ j + 3 + 1 = j + 4 ∧
    j + 3 + 2 = j ∧ j + 1 + 1 = j + 2 := by
  revert j; decide
end fin

private lemma Pent.ne (P : Pent M.graph h) {a b : Fin 5} (hab : a ≠ b) : P.x a ≠ P.x b :=
  fun e => hab (P.inj e)

private lemma Pent.h_ne (P : Pent M.graph h) (i : Fin 5) : h ≠ P.x i := (P.adj_h i).ne

/-- Walks inside three consecutive pentagon vertices. -/
private lemma Pent.walk3 (P : Pent M.graph h) (a : Fin 5) (u v : Fin n)
    (hu : u = P.x a ∨ u = P.x (a + 1) ∨ u = P.x (a + 2))
    (hv : v = P.x a ∨ v = P.x (a + 1) ∨ v = P.x (a + 2)) :
    ∃ q : M.graph.Walk u v,
      ∀ z ∈ q.support, z = P.x a ∨ z = P.x (a + 1) ∨ z = P.x (a + 2) := by
  have e1 : M.Adj (P.x a) (P.x (a + 1)) := P.adj_cyc a
  have e2 : M.Adj (P.x (a + 1)) (P.x (a + 2)) := by
    have := P.adj_cyc (a + 1); rwa [add_assoc] at this
  rcases hu with rfl | rfl | rfl <;> rcases hv with rfl | rfl | rfl
  · exact ⟨.nil, by simp⟩
  · exact ⟨e1.toWalk, by simp⟩
  · exact ⟨.cons e1 e2.toWalk, by simp⟩
  · exact ⟨e1.symm.toWalk, by simp⟩
  · exact ⟨.nil, by simp⟩
  · exact ⟨e2.toWalk, by simp⟩
  · exact ⟨.cons e2.symm e1.symm.toWalk, by simp⟩
  · exact ⟨e2.symm.toWalk, by simp⟩
  · exact ⟨.nil, by simp⟩

private lemma Pent.mem3 (P : Pent M.graph h) (a k : Fin 5) (u : Fin n) (hu : u = P.x k)
    (hk : k = a ∨ k = a + 1 ∨ k = a + 2) :
    u = P.x a ∨ u = P.x (a + 1) ∨ u = P.x (a + 2) := by
  subst hu; rcases hk with rfl | rfl | rfl <;> simp

/-- The two rotation neighbours of the dart `h → x (j+1)` are `x j` and `x (j+2)`. This is
forced by planarity: a pentagon edge from `x (j+1)` and a walk along the other three pentagon
vertices would otherwise be alternating at `h`. -/
private theorem rotation_nbrs (j : Fin 5) :
    ∃ (y1 y3 : Fin n) (h1 : M.Adj h y1) (h3 : M.Adj h y3),
      M.rotation.next ⟨(h, y1), h1⟩ = ⟨(h, P.x (j + 1)), P.adj_h _⟩ ∧
      M.rotation.next ⟨(h, P.x (j + 1)), P.adj_h _⟩ = ⟨(h, y3), h3⟩ ∧
      ((y1 = P.x j ∧ y3 = P.x (j + 2)) ∨ (y1 = P.x (j + 2) ∧ y3 = P.x j)) := by
  obtain ⟨f1, f2, f3, f4, f5⟩ := fin5_a j
  set D : M.Dart := ⟨(h, P.x (j + 1)), P.adj_h _⟩ with hD
  set d1 := M.rotation.next.symm D with hd1
  set d3 := M.rotation.next D with hd3
  have n1 : M.rotation.next d1 = D := Equiv.apply_symm_apply _ _
  have g1 : d1.fst = h := by
    have := M.rotation.next_fst d1; rw [n1] at this; exact this.symm
  have g3 : d3.fst = h := M.rotation.next_fst D
  have a1 : M.Adj h d1.snd := g1 ▸ d1.adj
  have a3 : M.Adj h d3.snd := g3 ▸ d3.adj
  have E1 : (⟨(h, d1.snd), a1⟩ : M.Dart) = d1 := Dart.ext _ _ (Prod.ext g1.symm rfl)
  have E3 : (⟨(h, d3.snd), a3⟩ : M.Dart) = d3 := Dart.ext _ _ (Prod.ext g3.symm rfl)
  -- the rotation at `h` is not trivial
  have nfix : M.rotation.next D ≠ D := by
    intro hfix
    obtain ⟨k, hk⟩ := M.rotation.cyclic D ⟨(h, P.x (j + 2)), P.adj_h _⟩ rfl
    rw [Function.iterate_fixed hfix] at hk
    exact P.ne (by simp) (congrArg (fun d : M.Dart => d.snd) hk)
  have s1 : d1.snd ≠ P.x (j + 1) := by
    intro e; apply nfix
    have : d1 = D := Dart.ext _ _ (Prod.ext g1 e)
    calc M.rotation.next D = M.rotation.next d1 := by rw [this]
      _ = D := n1
  have s3 : d3.snd ≠ P.x (j + 1) := by
    intro e; apply nfix
    exact Dart.ext _ _ (Prod.ext g3 e)
  obtain ⟨k1, hk1⟩ := P.only _ a1
  obtain ⟨k3, hk3⟩ := P.only _ a3
  have r12 : M.rotation.next ⟨(h, d1.snd), a1⟩ = D := by rw [E1]; exact n1
  have r23 : M.rotation.next D = ⟨(h, d3.snd), a3⟩ := E3.symm
  -- generic use of the separation lemma: an edge `v0 – x (j+1)` and a walk `q` disjoint from it
  have sep : ∀ (v0 : Fin n) (h0 : M.Adj h v0), v0 ≠ P.x (j + 1) → M.Adj v0 (P.x (j + 1)) →
      ∀ q : M.graph.Walk d1.snd d3.snd, h ∉ q.support →
        (∀ z ∈ q.support, z ≠ v0 ∧ z ≠ P.x (j + 1)) → False := by
    intro v0 h0 hne e q hq hqz
    obtain ⟨z, hzp, hzq⟩ := alternating_walks_intersect h0 a1 (P.adj_h (j + 1)) a3 hne r12 r23
      e.toWalk (by simp [h0.ne, (P.adj_h (j + 1)).ne]) q hq
    simp only [Adj.toWalk, Walk.support_cons, Walk.support_nil, List.mem_cons,
      List.not_mem_nil, or_false] at hzp
    rcases hzp with rfl | rfl
    · exact (hqz _ hzq).1 rfl
    · exact (hqz _ hzq).2 rfl
  have hqh : ∀ (a : Fin 5) {u v : Fin n} (q : M.graph.Walk u v),
      (∀ z ∈ q.support, z = P.x a ∨ z = P.x (a + 1) ∨ z = P.x (a + 2)) → h ∉ q.support := by
    intro a u v q hq hm
    rcases hq h hm with e | e | e <;> exact P.h_ne _ e
  -- Claim A: one of the rotation neighbours is `x j`
  have cA : d1.snd = P.x j ∨ d3.snd = P.x j := by
    by_contra hc
    push Not at hc
    have mem : ∀ k, d1.snd = P.x k ∨ d3.snd = P.x k → (k ≠ j ∧ k ≠ j + 1) := by
      intro k hk
      refine ⟨?_, ?_⟩ <;> rintro rfl
      · rcases hk with e | e
        · exact hc.1 e
        · exact hc.2 e
      · rcases hk with e | e
        · exact s1 e
        · exact s3 e
    have loc : ∀ k, k ≠ j ∧ k ≠ j + 1 → k = j + 2 ∨ k = j + 2 + 1 ∨ k = j + 2 + 2 := by
      intro k ⟨h1, h2⟩
      rw [f1, f2]
      rcases fin5_cases j k with rfl | rfl | rfl | rfl | rfl
      · exact absurd rfl h1
      · exact absurd rfl h2
      · exact Or.inl rfl
      · exact Or.inr (Or.inl rfl)
      · exact Or.inr (Or.inr rfl)
    obtain ⟨q, hq⟩ := P.walk3 (j + 2) _ _ (P.mem3 _ _ _ hk1 (loc _ (mem _ (Or.inl hk1))))
      (P.mem3 _ _ _ hk3 (loc _ (mem _ (Or.inr hk3))))
    refine sep (P.x j) (P.adj_h j) (P.ne (by simp)) (P.adj_cyc j) _ (hqh _ _ hq) ?_
    intro z hz
    rw [f1, f2] at hq
    rcases hq z hz with rfl | rfl | rfl <;> exact ⟨P.ne (by simp), P.ne (by simp)⟩
  -- Claim B: one of the rotation neighbours is `x (j+2)`
  have cB : d1.snd = P.x (j + 2) ∨ d3.snd = P.x (j + 2) := by
    by_contra hc
    push Not at hc
    have mem : ∀ k, d1.snd = P.x k ∨ d3.snd = P.x k → (k ≠ j + 2 ∧ k ≠ j + 1) := by
      intro k hk
      refine ⟨?_, ?_⟩ <;> rintro rfl
      · rcases hk with e | e
        · exact hc.1 e
        · exact hc.2 e
      · rcases hk with e | e
        · exact s1 e
        · exact s3 e
    have loc : ∀ k, k ≠ j + 2 ∧ k ≠ j + 1 → k = j + 3 ∨ k = j + 3 + 1 ∨ k = j + 3 + 2 := by
      intro k ⟨h1, h2⟩
      rw [f3, f4]
      rcases fin5_cases j k with rfl | rfl | rfl | rfl | rfl
      · exact Or.inr (Or.inr rfl)
      · exact absurd rfl h2
      · exact absurd rfl h1
      · exact Or.inl rfl
      · exact Or.inr (Or.inl rfl)
    obtain ⟨q, hq⟩ := P.walk3 (j + 3) _ _ (P.mem3 _ _ _ hk1 (loc _ (mem _ (Or.inl hk1))))
      (P.mem3 _ _ _ hk3 (loc _ (mem _ (Or.inr hk3))))
    have e : M.Adj (P.x (j + 2)) (P.x (j + 1)) := by
      have := P.adj_cyc (j + 1); rw [f5] at this; exact this.symm
    refine sep (P.x (j + 2)) (P.adj_h _) (P.ne (by simp)) e _ (hqh _ _ hq) ?_
    intro z hz
    rw [f3, f4] at hq
    rcases hq z hz with rfl | rfl | rfl <;> exact ⟨P.ne (by simp), P.ne (by simp)⟩
  refine ⟨d1.snd, d3.snd, a1, a3, r12, r23, ?_⟩
  have hj2 : P.x j ≠ P.x (j + 2) := P.ne (by simp)
  rcases cA with e1 | e1 <;> rcases cB with e2 | e2
  · exact absurd (e1.symm.trans e2) hj2
  · exact Or.inl ⟨e1, e2⟩
  · exact Or.inr ⟨e2, e1⟩
  · exact absurd (e1.symm.trans e2) hj2

/-- **Jordan separation at the hole.** A walk from a neighbour `v0 ≠ x (j+1)` of `h` to
`x (j+1)` and a walk from `x j` to `x (j+2)`, both avoiding `h`, meet. -/
private theorem lock_separates (j : Fin 5) {v0 : Fin n} (h0 : M.Adj h v0) (hne : v0 ≠ P.x (j + 1))
    (p : M.graph.Walk v0 (P.x (j + 1))) (hp : h ∉ p.support)
    (q : M.graph.Walk (P.x j) (P.x (j + 2))) (hq : h ∉ q.support) :
    ∃ z, z ∈ p.support ∧ z ∈ q.support := by
  obtain ⟨y1, y3, a1, a3, r12, r23, hy⟩ := rotation_nbrs P j
  rcases hy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact alternating_walks_intersect h0 a1 (P.adj_h _) a3 hne r12 r23 p hp q hq
  · obtain ⟨z, h1, h2⟩ :=
      alternating_walks_intersect h0 a1 (P.adj_h _) a3 hne r12 r23 p hp q.reverse
        (by rwa [Walk.support_reverse, List.mem_reverse])
    exact ⟨z, h1, by rwa [Walk.support_reverse, List.mem_reverse] at h2⟩

section pair
variable {G : SimpleGraph (Fin n)}

/-- Every vertex of a walk in a two-colour graph is active, or the walk is a trivial
loop at its start. -/
private lemma support_active {c : Fin n → Fin 4} {a b : Fin 4} {u v : Fin n}
    (p : (pairGraph G h c a b).Walk u v) :
    ∀ z ∈ p.support, Active h c a b z ∨ (z = u ∧ z = v) := by
  induction p with
  | nil => intro z hz; simp at hz; exact Or.inr ⟨hz, hz⟩
  | cons e p ih =>
    intro z hz
    rw [Walk.support_cons, List.mem_cons] at hz
    rcases hz with rfl | hz
    · exact Or.inl e.2.1
    · rcases ih z hz with hz' | ⟨rfl, -⟩
      · exact Or.inl hz'
      · exact Or.inl e.2.2

private lemma pairGraph_le (c : Fin n → Fin 4) (a b : Fin 4) : pairGraph G h c a b ≤ G :=
  fun _ _ e => e.1


end pair

/-- Shared core: a lock walk `p` (colours `{μ, X}`) from `v0` to `m` and a reachability in
colours `{α, Y}` between `x j` and `x (j+2)` cannot coexist when the four colours
`μ, X, α, Y` are such that `{μ, X} ∩ {α, Y} = ∅`. -/
private lemma no_cross (c : Fin n → Fin 4) (j : Fin 5) {μ X α Y : Fin 4}
    (hdis : ∀ z, (z = μ ∨ z = X) → (z = α ∨ z = Y) → False)
    {v0 : Fin n} (h0 : M.Adj h v0) (hne : v0 ≠ P.x (j + 1))
    (hlock : (pairGraph M.graph h c μ X).Reachable (P.x (j + 1)) v0)
    (hreach : (pairGraph M.graph h c α Y).Reachable (P.x j) (P.x (j + 2))) : False := by
  obtain ⟨p⟩ := hlock.symm
  obtain ⟨q⟩ := hreach
  have hpa := support_active p
  have hqa := support_active q
  have hp : ∀ z ∈ (p.mapLe (pairGraph_le c μ X)).support, Active h c μ X z := by
    intro z hz
    rw [Walk.support_mapLe_eq_support] at hz
    rcases hpa z hz with hz' | ⟨rfl, rfl⟩
    · exact hz'
    · exact absurd rfl hne
  have hq : ∀ z ∈ (q.mapLe (pairGraph_le c α Y)).support, Active h c α Y z := by
    intro z hz
    rw [Walk.support_mapLe_eq_support] at hz
    rcases hqa z hz with hz' | ⟨rfl, e⟩
    · exact hz'
    · exact absurd e (P.ne (by simp))
  obtain ⟨z, hzp, hzq⟩ := lock_separates P j h0 hne _ (fun hh => (hp h hh).1 rfl) _
    (fun hh => (hq h hh).1 rfl)
  exact hdis _ (hp z hzp).2 (hq z hzq).2

/-! ### The planar moves: `τ`, `τ⁻¹` and the rotations -/

variable {P} {c : Fin n → Fin 4}

/-- `τ`: from `F_i` with `M3` long to `F_{i+1}` with `M2` long; undone by `τ⁻¹`. Jordan makes
`τ` well defined: the `{W, X}`-component of `x (i+3)` misses `x i`. -/
theorem tau_spec (hc : ProperOff M.graph h c) {i : Fin 5} (hs : SingletonAt P c i)
    (hm : ¬ M3Short P c i) :
    KempeStep M.graph h c (tau P c i) ∧ ProperOff M.graph h (tau P c i) ∧
      SingletonAt P (tau P c i) (i + 1) ∧ ¬ M2Short P (tau P c i) (i + 1) ∧
      tauInv P (tau P c i) (i + 1) = c := by
  obtain ⟨e3, e4, sWX, sWY, sXY, zW, zX, zY⟩ := filled_shape hc hs
  have hlong : (pairGraph M.graph h c (c (P.x (i + 2))) (zcol P c i)).Reachable
      (P.x (i + 2)) (P.x (i + 4)) := Classical.not_not.mp hm
  have hsep : ¬ (pairGraph M.graph h c (c (P.x i)) (c (P.x (i + 1)))).Reachable
      (P.x (i + 3)) (P.x i) := by
    intro hreach
    refine no_cross P c (i + 3) (μ := c (P.x (i + 2))) (X := zcol P c i) (α := c (P.x i))
      (Y := c (P.x (i + 1))) ?_ (P.adj_h (i + 2)) (P.ne (by simp [add_assoc])) ?_ ?_
    · rintro z (rfl | rfl) (e | e)
      · exact sWY (e.symm)
      · exact sXY (e.symm)
      · exact zW e
      · exact zX e
    · simp only [add_assoc, Fin.reduceAdd]; exact hlong.symm
    · simp only [add_assoc, Fin.reduceAdd, add_zero]; exact hreach
  have hsep1 : ¬ (pairGraph M.graph h c (c (P.x i)) (c (P.x (i + 1)))).Reachable
      (P.x (i + 3)) (P.x (i + 1)) := fun r =>
    hsep (r.trans (Adj.reachable ⟨(P.adj_cyc i).symm, ⟨P.x_ne_h _, Or.inr rfl⟩,
      ⟨P.x_ne_h _, Or.inl rfl⟩⟩))
  have v0 : tau P c i (P.x i) = c (P.x i) := kswap_out hsep
  have v1 : tau P c i (P.x (i + 1)) = c (P.x (i + 1)) := kswap_out hsep1
  have v2 : tau P c i (P.x (i + 2)) = c (P.x (i + 2)) := kswap_other (Ne.symm sWY) sXY.symm
  have v3 : tau P c i (P.x (i + 3)) = c (P.x i) := kswap_mem' (Reachable.refl _) e3
  have v4 : tau P c i (P.x (i + 4)) = c (P.x (i + 2)) :=
    (kswap_other (by rw [e4]; exact Ne.symm sWY) (by rw [e4]; exact sXY.symm)).trans e4
  have step : KempeStep M.graph h c (tau P c i) :=
    kswap_step sWX (P.x_ne_h _) (Or.inr e3)
  obtain ⟨hs', hz⟩ := single_of_vals (P := P) (i := i + 1) (Z := zcol P c i) v1
    (by simp only [add_assoc, Fin.reduceAdd]; exact v2)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v3)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v4)
    (by simp only [add_assoc, Fin.reduceAdd, add_zero]; exact v0)
    sXY (Ne.symm sWX) (Ne.symm sWY) zX zY zW
  refine ⟨step, kempe_proper M.graph hc step, hs', ?_, ?_⟩
  · unfold M2Short
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd, not_not]
    rw [v2]; erw [kswap_pg_other sWY.symm sXY.symm zW zX]
    exact hlong
  · unfold tauInv
    simp only [add_assoc, Fin.reduceAdd]
    rw [v1, v3]
    exact kswap_inv'

/-- `τ⁻¹`: from `F_i` with `M2` long to `F_{i+4}` with `M3` long; undone by `τ`. -/
theorem tauInv_spec (hc : ProperOff M.graph h c) {i : Fin 5} (hs : SingletonAt P c i)
    (hm : ¬ M2Short P c i) :
    KempeStep M.graph h c (tauInv P c i) ∧ ProperOff M.graph h (tauInv P c i) ∧
      SingletonAt P (tauInv P c i) (i + 4) ∧ ¬ M3Short P (tauInv P c i) (i + 4) ∧
      tau P (tauInv P c i) (i + 4) = c := by
  obtain ⟨e3, e4, sWX, sWY, sXY, zW, zX, zY⟩ := filled_shape hc hs
  have hlong : (pairGraph M.graph h c (c (P.x (i + 1))) (zcol P c i)).Reachable
      (P.x (i + 1)) (P.x (i + 3)) := Classical.not_not.mp hm
  have hsep : ¬ (pairGraph M.graph h c (c (P.x i)) (c (P.x (i + 2)))).Reachable
      (P.x (i + 2)) (P.x i) := by
    intro hreach
    refine no_cross P c i (μ := c (P.x (i + 1))) (X := zcol P c i) (α := c (P.x i))
      (Y := c (P.x (i + 2))) ?_ (P.adj_h (i + 3)) (P.ne (by simp)) hlong hreach.symm
    rintro z (rfl | rfl) (e | e)
    · exact sWX e.symm
    · exact sXY e
    · exact zW e
    · exact zY e
  have hsep4 : ¬ (pairGraph M.graph h c (c (P.x i)) (c (P.x (i + 2)))).Reachable
      (P.x (i + 2)) (P.x (i + 4)) := by
    intro r
    have e : M.graph.Adj (P.x (i + 4)) (P.x i) := by
      have := P.adj_cyc (i + 4)
      simp only [add_assoc, Fin.reduceAdd, add_zero] at this
      exact this
    exact hsep (r.trans (Adj.reachable ⟨e, ⟨P.x_ne_h _, Or.inr e4⟩, ⟨P.x_ne_h _, Or.inl rfl⟩⟩))
  have v0 : tauInv P c i (P.x i) = c (P.x i) := kswap_out hsep
  have v1 : tauInv P c i (P.x (i + 1)) = c (P.x (i + 1)) := kswap_other (Ne.symm sWX) sXY
  have v2 : tauInv P c i (P.x (i + 2)) = c (P.x i) := kswap_mem' (Reachable.refl _) rfl
  have v3 : tauInv P c i (P.x (i + 3)) = c (P.x (i + 1)) :=
    (kswap_other (by rw [e3]; exact Ne.symm sWX) (by rw [e3]; exact sXY)).trans e3
  have v4 : tauInv P c i (P.x (i + 4)) = c (P.x (i + 2)) := (kswap_out hsep4).trans e4
  have step : KempeStep M.graph h c (tauInv P c i) :=
    kswap_step sWY (P.x_ne_h _) (Or.inr rfl)
  obtain ⟨hs', hz⟩ := single_of_vals (P := P) (i := i + 4) (Z := zcol P c i) v4
    (by simp only [add_assoc, Fin.reduceAdd, add_zero]; exact v0)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v1)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v2)
    (by simp only [add_assoc, Fin.reduceAdd]; exact v3)
    (Ne.symm sWY) (Ne.symm sXY) sWX zY zW zX
  refine ⟨step, kempe_proper M.graph hc step, hs', ?_, ?_⟩
  · unfold M3Short
    rw [hz]
    simp only [add_assoc, Fin.reduceAdd, not_not]
    rw [v1]; erw [kswap_pg_other (Ne.symm sWX) sXY zW zY]
    exact hlong
  · unfold tau
    simp only [add_assoc, Fin.reduceAdd, add_zero]
    rw [v4, v0]
    exact kswap_inv'

/-- `R₊₃` on the sphere: from `U_j` with lock 2 to `U_{j+3}` with lock 1; undone by `R₊₂`. -/
theorem rot3_move (hc : ProperOff M.graph h c) {j : Fin 5} (hr : RepeatAt P c j)
    (hl : Lock2 P c j) :
    KempeStep M.graph h c (rot3 P c j) ∧ ProperOff M.graph h (rot3 P c j) ∧
      RepeatAt P (rot3 P c j) (j + 3) ∧ Lock1 P (rot3 P c j) (j + 3) ∧
      rot2 P (rot3 P c j) (j + 3) = c := by
  have hK := rot3Def_of_lock2 P hr hl
  obtain ⟨s, p, r, l⟩ := rot3_spec hc hr hK
  exact ⟨s, p, r, l.mpr hl, rot2_rot3 hr hK⟩

/-- `R₊₂` on the sphere: from `U_k` with lock 1 to `U_{k+2}` with lock 2; undone by `R₊₃`. -/
theorem rot2_move (hc : ProperOff M.graph h c) {k : Fin 5} (hr : RepeatAt P c k)
    (hl : Lock1 P c k) :
    KempeStep M.graph h c (rot2 P c k) ∧ ProperOff M.graph h (rot2 P c k) ∧
      RepeatAt P (rot2 P c k) (k + 2) ∧ Lock2 P (rot2 P c k) (k + 2) ∧
      rot3 P (rot2 P c k) (k + 2) = c := by
  have hK := rot2Def_of_lock1 P hr hl
  obtain ⟨s, p, r, l⟩ := rot2_spec hc hr hK
  exact ⟨s, p, r, l.mpr hl, rot3_rot2 hr hK⟩

/-! ### Lemma Π: `π` is a permutation of the proper-off states, inside each Kempe class -/

/-- Each `π`-step is a Kempe step between proper-off states, and `π⁻¹ ∘ π = id`. -/
theorem piMove_spec (hc : ProperOff M.graph h c) :
    KempeStep M.graph h c (piMove P c) ∧ ProperOff M.graph h (piMove P c) ∧
      piInv P (piMove P c) = c := by
  rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · rw [piMove_rep hr]
    by_cases hl : Lock2 P c j
    · rw [ite_eq_left hl]
      obtain ⟨s, p, r', l', inv⟩ := rot3_move hc hr hl
      exact ⟨s, p, by rw [piInv_rep r', ite_eq_left l', inv]⟩
    · rw [ite_eq_right hl]
      obtain ⟨s, p, s', m', inv⟩ := phiBinv_spec hc hr hl
      exact ⟨s, p, by rw [piInv_single p s', ite_eq_left m', inv]⟩
  · rw [piMove_single hc hs]
    by_cases hm : M3Short P c i
    · rw [ite_eq_left hm]
      obtain ⟨s, p, r', l', inv⟩ := phiA_spec hc hs hm
      exact ⟨s, p, by rw [piInv_rep r', ite_eq_right l', inv]⟩
    · rw [ite_eq_right hm]
      obtain ⟨s, p, s', m', inv⟩ := tau_spec hc hs hm
      exact ⟨s, p, by rw [piInv_single p s', ite_eq_right m', inv]⟩

/-- Each `π⁻¹`-step is a Kempe step between proper-off states, and `π ∘ π⁻¹ = id`. -/
theorem piInv_spec (hc : ProperOff M.graph h c) :
    KempeStep M.graph h c (piInv P c) ∧ ProperOff M.graph h (piInv P c) ∧
      piMove P (piInv P c) = c := by
  rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · rw [piInv_rep hr]
    by_cases hl : Lock1 P c j
    · rw [ite_eq_left hl]
      obtain ⟨s, p, r', l', inv⟩ := rot2_move hc hr hl
      exact ⟨s, p, by rw [piMove_rep r', ite_eq_left l', inv]⟩
    · rw [ite_eq_right hl]
      obtain ⟨s, p, s', m', inv⟩ := phiAinv_spec hc hr hl
      exact ⟨s, p, by rw [piMove_single p s', ite_eq_left m', inv]⟩
  · rw [piInv_single hc hs]
    by_cases hm : M2Short P c i
    · rw [ite_eq_left hm]
      obtain ⟨s, p, r', l', inv⟩ := phiB_spec hc hs hm
      exact ⟨s, p, by rw [piMove_rep r', ite_eq_right l', inv]⟩
    · rw [ite_eq_right hm]
      obtain ⟨s, p, s', m', inv⟩ := tauInv_spec hc hs hm
      exact ⟨s, p, by rw [piMove_single p s', ite_eq_right m', inv]⟩

theorem piMove_kempeStep (hc : ProperOff M.graph h c) : KempeStep M.graph h c (piMove P c) :=
  (piMove_spec hc).1

theorem piMove_properOff (hc : ProperOff M.graph h c) : ProperOff M.graph h (piMove P c) :=
  (piMove_spec hc).2.1

theorem piInv_piMove (hc : ProperOff M.graph h c) : piInv P (piMove P c) = c :=
  (piMove_spec hc).2.2

theorem piInv_kempeStep (hc : ProperOff M.graph h c) : KempeStep M.graph h c (piInv P c) :=
  (piInv_spec hc).1

theorem piInv_properOff (hc : ProperOff M.graph h c) : ProperOff M.graph h (piInv P c) :=
  (piInv_spec hc).2.1

theorem piMove_piInv (hc : ProperOff M.graph h c) : piMove P (piInv P c) = c :=
  (piInv_spec hc).2.2

/-- `π` is injective on proper-off states. -/
theorem piMove_injOn :
    Set.InjOn (piMove P) {c : Fin n → Fin 4 | ProperOff M.graph h c} := by
  intro c hc d hd e
  have := congrArg (piInv P) e
  rwa [piInv_piMove hc, piInv_piMove hd] at this

variable (P) in
/-- **Lemma Π (sphere).** `π` as a permutation of the proper-off states, with inverse `π⁻¹`. -/
noncomputable def piPerm : Equiv.Perm {c : Fin n → Fin 4 // ProperOff M.graph h c} where
  toFun c := ⟨piMove P c.1, piMove_properOff c.2⟩
  invFun c := ⟨piInv P c.1, piInv_properOff c.2⟩
  left_inv c := Subtype.ext (piInv_piMove c.2)
  right_inv c := Subtype.ext (piMove_piInv c.2)

/-- `π` stays in the Kempe class. -/
theorem piMove_kempeEquiv (hc : ProperOff M.graph h c) :
    KempeEquiv (G := M.graph) (h := h) c (piMove P c) :=
  Relation.ReflTransGen.single (piMove_kempeStep hc)

/-- **Lemma Π, class form.** On the sphere, `π` is a bijection of every Kempe class of
proper-off states onto itself. -/
theorem piMove_bijOn_class (c₀ : Fin n → Fin 4) :
    Set.BijOn (piMove P)
      {d | ProperOff M.graph h d ∧ KempeEquiv (G := M.graph) (h := h) c₀ d}
      {d | ProperOff M.graph h d ∧ KempeEquiv (G := M.graph) (h := h) c₀ d} := by
  refine ⟨fun d ⟨hd, he⟩ => ⟨piMove_properOff hd, Relation.ReflTransGen.tail he (piMove_kempeStep hd)⟩,
    fun d hd d' hd' e => piMove_injOn hd.1 hd'.1 e, fun d ⟨hd, he⟩ => ?_⟩
  exact ⟨piInv P d, ⟨piInv_properOff hd, Relation.ReflTransGen.tail he (piInv_kempeStep hd)⟩, piMove_piInv hd⟩

/-! ### The token sum and the `λ` table -/

private lemma sg_r3 (j : Fin 5) : 2 * (j + 3) + 1 = 2 * j + 1 + 1 := by revert j; decide
open Fin.CommRing in
private lemma sg_b (j : Fin 5) : 2 * (j + 3) + 4 = 2 * j + 1 + -1 := by revert j; decide
open Fin.CommRing in
private lemma sg_a (i : Fin 5) : 2 * (i + 1) + 1 = 2 * i + 4 + -1 := by revert i; decide
open Fin.CommRing in
private lemma sg_t (i : Fin 5) : 2 * (i + 1) + 4 = 2 * i + 4 + -3 := by revert i; decide

open Fin.CommRing in
/-- **The `λ` table.** The token sum moves by `λ` along every `π`-step:
`σ (π c) = σ c + λ c` in `ℤ/5`. -/
theorem sigma_piMove (hc : ProperOff M.graph h c) :
    sigma P (piMove P c) = sigma P c + (Int.cast (lam P c) : Fin 5) := by
  rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · rw [piMove_rep hr, lam_rep hr, sigma_rep hr]
    by_cases hl : Lock2 P c j
    · obtain ⟨-, -, r', -⟩ := rot3_move hc hr hl
      rw [ite_eq_left hl, ite_eq_left hl, sigma_rep r', Int.cast_one, sg_r3]
    · obtain ⟨-, p, s', -⟩ := phiBinv_spec hc hr hl
      rw [ite_eq_right hl, ite_eq_right hl, sigma_single p s', Int.cast_neg, Int.cast_one, sg_b]
  · rw [piMove_single hc hs, lam_single hc hs, sigma_single hc hs]
    by_cases hm : M3Short P c i
    · obtain ⟨-, -, r', -⟩ := phiA_spec hc hs hm
      rw [ite_eq_left hm, ite_eq_left hm, sigma_rep r', Int.cast_neg, Int.cast_one, sg_a]
    · obtain ⟨-, p, s', -⟩ := tau_spec hc hs hm
      rw [ite_eq_right hm, ite_eq_right hm, sigma_single p s', Int.cast_neg, Int.cast_ofNat, sg_t]

/-- The table of `λ` in closed form, per case (`NightEulerHole.md` §3). -/
theorem lam_table (hc : ProperOff M.graph h c) :
    (∀ j, RepeatAt P c j → Lock2 P c j → lam P c = 1) ∧
    (∀ j, RepeatAt P c j → ¬ Lock2 P c j → lam P c = -1) ∧
    (∀ i, SingletonAt P c i → M3Short P c i → lam P c = -1) ∧
    (∀ i, SingletonAt P c i → ¬ M3Short P c i → lam P c = -3) := by
  refine ⟨fun j hr hl => ?_, fun j hr hl => ?_, fun i hs hm => ?_, fun i hs hm => ?_⟩
  · rw [lam_rep hr, ite_eq_left hl]
  · rw [lam_rep hr, ite_eq_right hl]
  · rw [lam_single hc hs, ite_eq_left hm]
  · rw [lam_single hc hs, ite_eq_right hm]

end sphere

end SimpleGraph.QuarterFloor
