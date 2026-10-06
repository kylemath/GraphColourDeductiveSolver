/-
The compiled belt theorem is the vacancy hypothesis at every hole of `TwoPoleBelt.graph n`.
New file; no existing file edited.
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltPoleB
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltVacancyHypDef
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyProtectedLift
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.SphericalMap

/-!
# The belt satisfies the vacancy hypothesis at every hole

`VacancyHyp.VacancyAt G B h` (see `TwoPoleBeltVacancyHypDef`) is, for `G = TwoPoleBelt.graph n`,
literally the conclusion of `TwoPoleBeltPoleHole.belt_theorem_all_holes` (`Colour = Fin 4`,
`State n = Vertex n × (Vertex n → Colour)`), with bound `B = 6 n`.

Statement conventions matched exactly: mixed paths of slides and Kempe swaps, the hole may move,
the final hole has a missing colour, the colouring is proper off the final hole.

Conventions *not* provided by the belt theorem: a fixed hole (pure path), a protected face or
clique avoided by the hole, the `SphericalMap` carrier on `Fin m` (see `TwoPoleBeltVacancyHyp`
report), the degree/triangulation data, and identification with Florek's family.
-/

@[expose] public section
namespace SimpleGraph.TwoPoleBeltVacancyHyp
open VacancyHyp VacancySlide TwoPoleBelt

variable {n : ℕ}

/-- **The vacancy hypothesis at every hole of the belt**, bound `6 n`. -/
theorem vacancyAt_belt (hn : 5 ≤ n) (h : Vertex n) : VacancyAt (graph n) (6 * n) h :=
  fun c hc => TwoPoleBeltPoleHole.belt_theorem_all_holes hn h c hc

/-- The unbounded form used by the hole induction. -/
theorem vacancyHyp_belt (hn : 5 ≤ n) : VacancyHyp (graph n) :=
  VacancyHyp.of_bounded (vacancyAt_belt hn)

/-- Consequence: every proper 4-colouring of a deletion extends to a proper 4-colouring of `G_n`. -/
theorem belt_colouring (hn : 5 ≤ n) (h : Vertex n) (c : Vertex n → Fin 4)
    (hc : ProperOff (graph n) h c) : Nonempty ((graph n).Coloring (Fin 4)) :=
  (vacancyAt_belt hn h).colouring c hc

/-- Transfer: any graph isomorphic to the belt (e.g. the underlying graph of a `SphericalMap`
on `Fin (2 n + 2)` that is isomorphic to it) satisfies the hypothesis, at the image holes. -/
theorem vacancyHyp_of_iso_belt (hn : 5 ≤ n) {W : Type*} [DecidableEq W] {G' : SimpleGraph W}
    (φ : graph n ≃g G') : VacancyHyp G' :=
  VacancyHyp.of_iso φ (vacancyHyp_belt hn)

/-- Spherical-map form: any `SphericalMap m` whose graph is isomorphic to the belt. -/
theorem vacancyHyp_sphericalMap_of_iso {m : ℕ} (hn : 5 ≤ n) (M : SphericalMap m)
    (φ : graph n ≃g M.graph) : VacancyHyp M.graph :=
  vacancyHyp_of_iso_belt hn φ

/-- Honest bookkeeping of the protected-path convention: every belt path is a protected path
for the trivial pair `A = univ`, `F = ∅` (no protection), and nothing more is claimed. -/
theorem belt_path_protected_trivial {k : ℕ} {s t : State n}
    (p : VacancyShortFill.MixedPath (graph n) k s t) (ht : t.1 ∈ (Set.univ : Set (Vertex n))) :
    VacancyCliqueLift.ProtectedPath (graph n) Set.univ ∅ k s t := by
  induction p with
  | nil s => exact .nil (Set.mem_univ _) (Set.notMem_empty _)
  | cons st _ ih => exact .cons st (Set.mem_univ _) (Set.notMem_empty _) (ih ht)

end SimpleGraph.TwoPoleBeltVacancyHyp
