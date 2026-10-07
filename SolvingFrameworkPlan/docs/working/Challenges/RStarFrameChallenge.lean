import Mathlib.Combinatorics.SimpleGraph.Dart
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Data.ZMod.Basic
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Logic.Relation
import Mathlib.Data.Fin.VecNotation

/-!
# Frozen challenge: R\* for the frame class (`RStarFrame`)

Comparator-style statement file. It imports only upstream Mathlib modules and defines everything
the statement uses. `RStarFrameBridge.lean` proves `MainStatement ↔ SphericalMap.RStarFrame`
(the project's PlaneMap definition), which pins the project's definitions to this text.

**Statement.** Every connected spherical triangulation with minimum degree at least five, no
separating triangle, and no ring-embedded occurrence of the Birkhoff diamond or of RSST
configuration 2.122 (either orientation) has a vertex `v` of degree five such that every proper
four-colouring of `T - v` reaches, by finitely many whole-component Kempe swaps in `T - v`, a
colouring that misses a colour on the neighbourhood of `v`.

**Model.**
* A `SphericalMap n` is a simple graph on `Fin n` with a rotation system (`next` permutes the
  darts, fixes the initial vertex, and is a single cycle at each vertex) such that every mod-2
  edge combination with even degree at every vertex is the coboundary of a face potential
  (`Fills`). This is the only planarity hypothesis.
* Faces are the orbits of `faceNext d = next d.symm`; a face potential is a dart function
  invariant under `faceNext`. `Triangulated`: every face orbit has length 3.
* `Nx M u v w`: in the rotation at `u`, the neighbour after `v` is `w`.
-/

namespace RStarFrameChallenge

open SimpleGraph

/-! ## Spherical maps -/

/-- A permutation of darts giving a single cyclic order at each vertex. -/
structure RotationSystem {V : Type*} (G : SimpleGraph V) where
  next : Equiv.Perm G.Dart
  next_fst : ∀ d, (next d).fst = d.fst
  cyclic : ∀ d e, d.fst = e.fst → ∃ k : ℕ, ((next : G.Dart → G.Dart)^[k]) d = e

/-- The face successor: reverse the dart, then take its rotation successor. -/
def RotationSystem.faceNext {V : Type*} {G : SimpleGraph V} (R : RotationSystem G)
    (d : G.Dart) : G.Dart :=
  R.next d.symm

/-- The unoriented edge of a dart. -/
def dartEdge {V : Type*} {G : SimpleGraph V} (d : G.Dart) : G.edgeSet :=
  ⟨d.edge, by change G.Adj d.fst d.snd; exact d.adj⟩

/-- The mod-two incidence boundary of an edge combination. -/
noncomputable def edgeIncidence {n : ℕ} (G : SimpleGraph (Fin n))
    (φ : G.edgeSet → ZMod 2) (x : Fin n) : ZMod 2 := by
  classical
  exact ∑ e : G.edgeSet, if x ∈ e.val then φ e else 0

/-- Every even edge combination is the coboundary of a face potential. -/
def RotationSystem.Fills {n : ℕ} {G : SimpleGraph (Fin n)} (R : RotationSystem G) : Prop :=
  ∀ φ : G.edgeSet → ZMod 2, (∀ x, edgeIncidence G φ x = 0) →
    ∃ c : G.Dart → ZMod 2, (∀ d, c (R.faceNext d) = c d) ∧
      ∀ d : G.Dart, φ (dartEdge d) = c d + c d.symm

/-- A finite rotation system whose even edge combinations bound face sums. -/
structure SphericalMap (n : ℕ) where
  graph : SimpleGraph (Fin n)
  rotation : RotationSystem graph
  fills : rotation.Fills

namespace SphericalMap

variable {n : ℕ}

noncomputable instance (M : SphericalMap n) : DecidableRel M.graph.Adj := Classical.decRel _

/-- Every face is a triangle. -/
def Triangulated (M : SphericalMap n) : Prop :=
  ∀ d : M.graph.Dart, Function.minimalPeriod M.rotation.faceNext d = 3

/-- In the rotation at `u`, the neighbour after `v` is `w`. -/
def Nx (M : SphericalMap n) (u v w : Fin n) : Prop :=
  ∃ huv : M.graph.Adj u v, (M.rotation.next ⟨(u, v), huv⟩).snd = w

/-- `p q r` bound a face. -/
def Facial (M : SphericalMap n) (p q r : Fin n) : Prop := M.Nx q p r ∨ M.Nx p q r

/-- Every triangle bounds a face (no separating triangle). -/
def NoSep (M : SphericalMap n) : Prop :=
  ∀ x y z, M.graph.Adj x y → M.graph.Adj y z → M.graph.Adj z x → M.Facial x y z

end SphericalMap

/-! ## Kempe chains at a hole -/

section Kempe
variable {V C : Type*} (G : SimpleGraph V)

/-- Proper on every edge avoiding the hole `r`. -/
def ProperOff (r : V) (c : V → C) : Prop :=
  ∀ ⦃u v⦄, G.Adj u v → u ≠ r → v ≠ r → c u ≠ c v

/-- Some colour is missing on the neighbourhood of the hole `h`. -/
def Target (h : V) (c : V → C) : Prop := ∃ x, ∀ ⦃v⦄, G.Adj h v → c v ≠ x

/-- A vertex off the hole with colour `a` or `b`. -/
def Active (h : V) (c : V → C) (a b : C) (v : V) : Prop :=
  v ≠ h ∧ (c v = a ∨ c v = b)

/-- The `{a, b}`-coloured subgraph of `G - h`. -/
def pairGraph (h : V) (c : V → C) (a b : C) : SimpleGraph V where
  Adj u v := G.Adj u v ∧ Active h c a b u ∧ Active h c a b v
  symm := ⟨fun _ _ e => ⟨e.1.symm, e.2.2, e.2.1⟩⟩
  loopless := ⟨fun _ e => e.1.ne rfl⟩

/-- `S` is one entire connected component of the `{a, b}`-subgraph, with an active seed. -/
def Whole (h : V) (c : V → C) (a b : C) (S : Set V) : Prop :=
  ∃ s, Active h c a b s ∧ ∀ v, v ∈ S ↔ (pairGraph G h c a b).Reachable s v

/-- Swap the colours `a` and `b` on `S`. -/
noncomputable def swap [DecidableEq C] (c : V → C) (a b : C) (S : Set V) : V → C :=
  by classical exact fun v => if v ∈ S then Equiv.swap a b (c v) else c v

/-- One Kempe step: swap two colours on one whole component of their subgraph in `G - h`. -/
def KempeStep [DecidableEq C] (h : V) (c d : V → C) : Prop :=
  ∃ a b S, a ≠ b ∧ Whole G h c a b S ∧ d = swap c a b S

end Kempe

namespace SphericalMap

variable {n : ℕ}

/-- Every proper four-colouring of `T - r` reaches a colouring missing a colour on the
neighbourhood of `r` by finitely many Kempe steps. -/
def PureClean (T : SphericalMap n) (r : Fin n) : Prop :=
  ∀ c : Fin n → Fin 4, ProperOff T.graph r c →
    ∃ d, Relation.ReflTransGen (KempeStep T.graph r) c d ∧ Target T.graph r d

end SphericalMap

/-! ## Configuration occurrences

`ring k` is RSST ring vertex `k+1`; `int` is the interior (`K₄ − e`: centres `int 0`, `int 2`,
tips `int 1`, `int 3`). Each field `ra_b` gives the rotation of `T` at `int a`. -/

open SphericalMap

/-- The Birkhoff diamond (interior degrees 5,5,5,5, ring size 6), orientation −1. -/
structure DiamondMOcc {n : ℕ} (T : SphericalMap n) (ring : Fin 6 → Fin n) (int : Fin 4 → Fin n) :
    Prop where
  ring_inj : Function.Injective ring
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![5, 5, 5, 5] : Fin 4 → ℕ) a
  r0_0 : Nx T (int 0) (int 1) (ring 1)
  r0_1 : Nx T (int 0) (int 2) (int 1)
  r0_2 : Nx T (int 0) (int 3) (int 2)
  r0_3 : Nx T (int 0) (ring 0) (int 3)
  r0_4 : Nx T (int 0) (ring 1) (ring 0)
  r1_0 : Nx T (int 1) (ring 2) (ring 1)
  r1_1 : Nx T (int 1) (ring 3) (ring 2)
  r1_2 : Nx T (int 1) (int 2) (ring 3)
  r1_3 : Nx T (int 1) (int 0) (int 2)
  r1_4 : Nx T (int 1) (ring 1) (int 0)
  r2_0 : Nx T (int 2) (ring 3) (int 1)
  r2_1 : Nx T (int 2) (ring 4) (ring 3)
  r2_2 : Nx T (int 2) (int 3) (ring 4)
  r2_3 : Nx T (int 2) (int 0) (int 3)
  r2_4 : Nx T (int 2) (int 1) (int 0)
  r3_0 : Nx T (int 3) (ring 4) (int 2)
  r3_1 : Nx T (int 3) (ring 5) (ring 4)
  r3_2 : Nx T (int 3) (ring 0) (ring 5)
  r3_3 : Nx T (int 3) (int 0) (ring 0)
  r3_4 : Nx T (int 3) (int 2) (int 0)

/-- The Birkhoff diamond, orientation +1. -/
structure DiamondPOcc {n : ℕ} (T : SphericalMap n) (ring : Fin 6 → Fin n) (int : Fin 4 → Fin n) :
    Prop where
  ring_inj : Function.Injective ring
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![5, 5, 5, 5] : Fin 4 → ℕ) a
  r0_0 : Nx T (int 0) (ring 1) (int 1)
  r0_1 : Nx T (int 0) (int 1) (int 2)
  r0_2 : Nx T (int 0) (int 2) (int 3)
  r0_3 : Nx T (int 0) (int 3) (ring 0)
  r0_4 : Nx T (int 0) (ring 0) (ring 1)
  r1_0 : Nx T (int 1) (ring 1) (ring 2)
  r1_1 : Nx T (int 1) (ring 2) (ring 3)
  r1_2 : Nx T (int 1) (ring 3) (int 2)
  r1_3 : Nx T (int 1) (int 2) (int 0)
  r1_4 : Nx T (int 1) (int 0) (ring 1)
  r2_0 : Nx T (int 2) (int 1) (ring 3)
  r2_1 : Nx T (int 2) (ring 3) (ring 4)
  r2_2 : Nx T (int 2) (ring 4) (int 3)
  r2_3 : Nx T (int 2) (int 3) (int 0)
  r2_4 : Nx T (int 2) (int 0) (int 1)
  r3_0 : Nx T (int 3) (int 2) (ring 4)
  r3_1 : Nx T (int 3) (ring 4) (ring 5)
  r3_2 : Nx T (int 3) (ring 5) (ring 0)
  r3_3 : Nx T (int 3) (ring 0) (int 0)
  r3_4 : Nx T (int 3) (int 0) (int 2)

/-- RSST configuration 2.122 (interior degrees 6,5,5,5, ring size 7), orientation −1. -/
structure C2122MOcc {n : ℕ} (T : SphericalMap n) (ring : Fin 7 → Fin n) (int : Fin 4 → Fin n) :
    Prop where
  ring_inj : Function.Injective ring
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![6, 5, 5, 5] : Fin 4 → ℕ) a
  r0_0 : Nx T (int 0) (ring 2) (ring 1)
  r0_1 : Nx T (int 0) (int 1) (ring 2)
  r0_2 : Nx T (int 0) (int 2) (int 1)
  r0_3 : Nx T (int 0) (int 3) (int 2)
  r0_4 : Nx T (int 0) (ring 0) (int 3)
  r0_5 : Nx T (int 0) (ring 1) (ring 0)
  r1_0 : Nx T (int 1) (ring 3) (ring 2)
  r1_1 : Nx T (int 1) (ring 4) (ring 3)
  r1_2 : Nx T (int 1) (int 2) (ring 4)
  r1_3 : Nx T (int 1) (int 0) (int 2)
  r1_4 : Nx T (int 1) (ring 2) (int 0)
  r2_0 : Nx T (int 2) (ring 4) (int 1)
  r2_1 : Nx T (int 2) (ring 5) (ring 4)
  r2_2 : Nx T (int 2) (int 3) (ring 5)
  r2_3 : Nx T (int 2) (int 0) (int 3)
  r2_4 : Nx T (int 2) (int 1) (int 0)
  r3_0 : Nx T (int 3) (ring 5) (int 2)
  r3_1 : Nx T (int 3) (ring 6) (ring 5)
  r3_2 : Nx T (int 3) (ring 0) (ring 6)
  r3_3 : Nx T (int 3) (int 0) (ring 0)
  r3_4 : Nx T (int 3) (int 2) (int 0)

/-- RSST configuration 2.122, orientation +1. -/
structure C2122POcc {n : ℕ} (T : SphericalMap n) (ring : Fin 7 → Fin n) (int : Fin 4 → Fin n) :
    Prop where
  ring_inj : Function.Injective ring
  int_inj : Function.Injective int
  disj : ∀ t a, ring t ≠ int a
  deg : ∀ a, T.graph.degree (int a) = (![6, 5, 5, 5] : Fin 4 → ℕ) a
  r0_0 : Nx T (int 0) (ring 1) (ring 2)
  r0_1 : Nx T (int 0) (ring 2) (int 1)
  r0_2 : Nx T (int 0) (int 1) (int 2)
  r0_3 : Nx T (int 0) (int 2) (int 3)
  r0_4 : Nx T (int 0) (int 3) (ring 0)
  r0_5 : Nx T (int 0) (ring 0) (ring 1)
  r1_0 : Nx T (int 1) (ring 2) (ring 3)
  r1_1 : Nx T (int 1) (ring 3) (ring 4)
  r1_2 : Nx T (int 1) (ring 4) (int 2)
  r1_3 : Nx T (int 1) (int 2) (int 0)
  r1_4 : Nx T (int 1) (int 0) (ring 2)
  r2_0 : Nx T (int 2) (int 1) (ring 4)
  r2_1 : Nx T (int 2) (ring 4) (ring 5)
  r2_2 : Nx T (int 2) (ring 5) (int 3)
  r2_3 : Nx T (int 2) (int 3) (int 0)
  r2_4 : Nx T (int 2) (int 0) (int 1)
  r3_0 : Nx T (int 3) (int 2) (ring 5)
  r3_1 : Nx T (int 3) (ring 5) (ring 6)
  r3_2 : Nx T (int 3) (ring 6) (ring 0)
  r3_3 : Nx T (int 3) (ring 0) (int 0)
  r3_4 : Nx T (int 3) (int 0) (int 2)

/-- No occurrence of the Birkhoff diamond, in either orientation. -/
def DiamondFree {n : ℕ} (T : SphericalMap n) : Prop :=
  (¬ ∃ ring int, DiamondMOcc T ring int) ∧ (¬ ∃ ring int, DiamondPOcc T ring int)

/-- No occurrence of RSST 2.122, in either orientation. -/
def Conf2122Free {n : ℕ} (T : SphericalMap n) : Prop :=
  (¬ ∃ ring int, C2122MOcc T ring int) ∧ (¬ ∃ ring int, C2122POcc T ring int)

/-! ## The statement -/

/-- **R\* for the frame class.** -/
def MainStatement : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) → T.NoSep → DiamondFree T → Conf2122Free T →
    ∃ v, T.graph.degree v = 5 ∧ T.PureClean v

theorem main : MainStatement := by sorry

end RStarFrameChallenge
