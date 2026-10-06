module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarSanity

/-!
# Sanity check: two radius-5 certificate states under the formal `PureFill`

Two audited radius-5 certificates (studiointel run C; replayed by the audit at radius 5): graph
`80b930d1540e4ee3` (order 32, hole 23) and graph `91a307d1852a1764` (order 28, hole 22). Each
graph is entered by its neighbour lists, copied from the certificate's face list. For each
certificate state `c0`:

* `proper`: `c0` is a proper colouring of the graph minus the hole;
* `unfilled`: the link of the hole carries all four colours;
* `pureFill`: `c0` reaches a filled state within five pure Kempe swaps, in the library's sense
  (`KempeStep`: an entire two-colour component of the graph minus the hole, any colour pair).

An independent breadth-first search over the same swap semantics (`radius_bfs.py`, Studio Math
scripts) finds no fill within four swaps from either state, so the formal radius agrees with the
certificate's radius 5. That lower bound is computed, not compiled. The checks are graph-level;
that these graphs are spherical triangulations is certified by the producer's checker, not here.
-/

@[expose] public section
namespace SimpleGraph.RadiusFive
open VacancySlide VacancyShortFill

namespace R80

/-- Certificate `80b930d1540e4ee3`: neighbour lists of the 32-vertex triangulation. -/
def nbrs : Fin 32 → List (Fin 32) := ![[1, 6, 8, 9, 12], [0, 2, 5, 6, 12, 14], [1, 3, 4, 5, 14, 17, 27], [2, 15, 16, 17, 27], [2, 5, 17, 18, 19], [1, 2, 4, 6, 18, 20], [0, 1, 5, 7, 8, 20], [6, 8, 10, 20, 22], [0, 6, 7, 9, 10], [0, 8, 10, 11, 12], [7, 8, 9, 11, 13, 21, 22, 24], [9, 10, 12, 13, 14, 26], [0, 1, 9, 11, 14], [10, 11, 24, 25, 26], [1, 2, 11, 12, 26, 27], [3, 16, 26, 27, 29], [3, 15, 17, 29, 30], [2, 3, 4, 16, 19, 30], [4, 5, 19, 20, 21, 22], [4, 17, 18, 21, 23, 30, 31], [5, 6, 7, 18, 22], [10, 18, 19, 22, 23, 24], [7, 10, 18, 20, 21], [19, 21, 24, 25, 31], [10, 13, 21, 23, 25], [13, 23, 24, 26, 28, 31], [11, 13, 14, 15, 25, 27, 28, 29], [2, 3, 14, 15, 26], [25, 26, 29, 30, 31], [15, 16, 26, 28, 30], [16, 17, 19, 28, 29, 31], [19, 23, 25, 28, 30]]

def G : SimpleGraph (Fin 32) where
  Adj u v := v ∈ nbrs u
  symm := by refine ⟨?_⟩; intro u v h; exact (by decide : ∀ u v : Fin 32, v ∈ nbrs u → u ∈ nbrs v) u v h
  loopless := by refine ⟨?_⟩; intro v h; exact (by decide : ∀ v : Fin 32, v ∉ nbrs v) v h

instance : DecidableRel G.Adj := fun u v => inferInstanceAs (Decidable (v ∈ nbrs u))

def c0 : Fin 32 → Fin 4 := ![3, 0, 3, 1, 1, 2, 1, 0, 2, 1, 3, 0, 2, 1, 1, 3, 2, 0, 0, 3, 3, 1, 2, 0, 2, 0, 2, 0, 3, 0, 1, 2]
def c1 : Fin 32 → Fin 4 := ![3, 0, 3, 2, 1, 2, 1, 0, 2, 1, 3, 0, 2, 1, 1, 3, 1, 0, 0, 3, 3, 1, 2, 0, 2, 0, 2, 0, 3, 0, 2, 1]
def c2 : Fin 32 → Fin 4 := ![3, 1, 3, 2, 1, 2, 0, 1, 2, 0, 3, 1, 2, 0, 0, 3, 1, 0, 0, 3, 3, 1, 2, 0, 2, 1, 2, 1, 3, 0, 2, 0]
def c3 : Fin 32 → Fin 4 := ![1, 3, 1, 2, 3, 2, 0, 3, 2, 0, 1, 3, 2, 0, 0, 1, 3, 0, 0, 1, 1, 3, 2, 0, 2, 1, 2, 3, 3, 0, 2, 0]
def c4 : Fin 32 → Fin 4 := ![0, 3, 0, 2, 3, 2, 1, 3, 2, 1, 0, 3, 2, 1, 1, 1, 3, 1, 1, 0, 0, 3, 2, 0, 2, 0, 2, 3, 3, 0, 2, 1]
def c5 : Fin 32 → Fin 4 := ![0, 1, 0, 2, 1, 2, 3, 1, 2, 3, 0, 1, 2, 3, 3, 3, 1, 3, 3, 0, 0, 1, 2, 0, 2, 0, 2, 1, 3, 0, 2, 1]

theorem step1 : KempeStep G 23 c0 c1 :=
  ⟨1, 2, ↑({3, 16, 30, 31} : Finset (Fin 32)), by decide,
    whole_of_cert 3 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 3, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 16, 30] ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step2 : KempeStep G 23 c1 c2 :=
  ⟨0, 1, ↑({1, 6, 7, 9, 11, 13, 14, 25, 27, 31} : Finset (Fin 32)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 5, 1, 6, 8, 11, 10, 14, 12, 11, 1, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 13, 26, 14, 28, 29, 30, 25] ![0, 0, 0, 0, 0, 0, 1, 2, 0, 3, 0, 2, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 2, 0, 0, 0, 5] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step3 : KempeStep G 23 c2 c3 :=
  ⟨1, 3, ↑({0, 1, 2, 4, 7, 10, 11, 15, 16, 19, 20, 21, 27} : Finset (Fin 32)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 1, 3, 2, 5, 6, 10, 8, 9, 21, 10, 12, 13, 14, 27, 15, 17, 18, 4, 7, 19, 22, 23, 24, 25, 26, 2, 28, 29, 30, 31] ![0, 1, 2, 0, 3, 0, 0, 7, 0, 0, 6, 7, 0, 0, 0, 4, 5, 0, 0, 4, 8, 5, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step4 : KempeStep G 23 c3 c4 :=
  ⟨0, 1, ↑({0, 2, 6, 9, 10, 13, 14, 17, 18, 19, 20, 25, 31} : Finset (Fin 32)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 17, 3, 4, 5, 0, 7, 8, 0, 9, 11, 12, 10, 2, 15, 16, 19, 20, 18, 6, 21, 22, 23, 24, 13, 26, 27, 28, 29, 30, 19] ![0, 0, 6, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 3, 7, 0, 0, 5, 3, 4, 2, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 5] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step5 : KempeStep G 23 c4 c5 :=
  ⟨1, 3, ↑({1, 4, 6, 7, 9, 11, 13, 14, 15, 16, 17, 18, 21, 27} : Finset (Fin 32)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 17, 5, 1, 6, 8, 11, 10, 14, 12, 11, 1, 27, 15, 16, 4, 19, 20, 18, 22, 23, 24, 25, 26, 14, 28, 29, 30, 31] ![0, 0, 0, 0, 6, 0, 1, 2, 0, 3, 0, 2, 0, 3, 1, 3, 4, 5, 7, 0, 0, 8, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem proper : ProperOff G 23 c0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 32, G.Adj u v → u ≠ 23 → v ≠ 23 → c0 u ≠ c0 v) u v e hu hv

theorem unfilled : ¬ Target G 23 c0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 23 v ∧ c0 v = x) x
  exact hx hv e

/-- **The certificate state fills within 5 pure Kempe swaps** (the formal `PureFill`). -/
theorem pureFill : PureFill G 23 c0 5 :=
  ⟨5, le_rfl, c5, (.cons step1 (.cons step2 (.cons step3 (.cons step4 (.cons step5 (.nil c5)))))),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 32, G.Adj 23 v → c5 v ≠ 3) v hv⟩⟩

end R80

namespace R91

/-- Certificate `91a307d1852a1764`: neighbour lists of the 28-vertex triangulation. -/
def nbrs : Fin 28 → List (Fin 28) := ![[1, 2, 3, 4, 5, 6], [0, 5, 6, 7, 8, 18], [0, 3, 6, 9, 10], [0, 2, 4, 9, 11, 12, 14], [0, 3, 5, 13, 14], [0, 1, 4, 8, 13, 15], [0, 1, 2, 10, 18], [1, 8, 16, 18, 27], [1, 5, 7, 15, 27], [2, 3, 10, 12, 26], [2, 6, 9, 18, 19, 24, 26], [3, 12, 14, 22, 25], [3, 9, 11, 23, 25, 26], [4, 5, 14, 15, 21], [3, 4, 11, 13, 21, 22], [5, 8, 13, 17, 19, 20, 21, 27], [7, 17, 18, 24, 27], [15, 16, 19, 24, 27], [1, 6, 7, 10, 16, 24], [10, 15, 17, 20, 23, 24, 26], [15, 19, 21, 22, 23, 25], [13, 14, 15, 20, 22], [11, 14, 20, 21, 25], [12, 19, 20, 25, 26], [10, 16, 17, 18, 19], [11, 12, 20, 22, 23], [9, 10, 12, 19, 23], [7, 8, 15, 16, 17]]

def G : SimpleGraph (Fin 28) where
  Adj u v := v ∈ nbrs u
  symm := by refine ⟨?_⟩; intro u v h; exact (by decide : ∀ u v : Fin 28, v ∈ nbrs u → u ∈ nbrs v) u v h
  loopless := by refine ⟨?_⟩; intro v h; exact (by decide : ∀ v : Fin 28, v ∉ nbrs v) v h

instance : DecidableRel G.Adj := fun u v => inferInstanceAs (Decidable (v ∈ nbrs u))

def c0 : Fin 28 → Fin 4 := ![3, 1, 1, 0, 2, 0, 0, 0, 3, 2, 3, 3, 1, 3, 1, 1, 1, 3, 2, 2, 0, 2, 0, 3, 0, 2, 0, 2]
def c1 : Fin 28 → Fin 4 := ![3, 2, 1, 0, 1, 0, 0, 0, 3, 2, 3, 3, 1, 3, 2, 2, 2, 3, 1, 1, 0, 1, 0, 3, 0, 2, 0, 1]
def c2 : Fin 28 → Fin 4 := ![3, 0, 1, 0, 1, 2, 2, 2, 3, 2, 3, 3, 1, 3, 2, 0, 0, 3, 1, 1, 2, 1, 0, 3, 2, 0, 0, 1]
def c3 : Fin 28 → Fin 4 := ![2, 0, 1, 0, 1, 3, 3, 3, 2, 3, 2, 2, 1, 2, 3, 0, 0, 2, 1, 1, 2, 1, 0, 3, 3, 0, 0, 1]
def c4 : Fin 28 → Fin 4 := ![0, 2, 1, 2, 1, 3, 3, 3, 0, 3, 2, 0, 1, 0, 3, 2, 2, 0, 1, 1, 0, 1, 0, 3, 3, 2, 0, 1]
def c5 : Fin 28 → Fin 4 := ![0, 3, 1, 3, 1, 2, 2, 2, 0, 2, 3, 0, 1, 0, 2, 3, 3, 0, 1, 1, 0, 1, 0, 3, 2, 2, 0, 1]

theorem step1 : KempeStep G 22 c0 c1 :=
  ⟨1, 2, ↑({1, 4, 14, 15, 16, 18, 19, 21, 27} : Finset (Fin 28)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 14, 5, 6, 7, 8, 9, 10, 11, 12, 13, 21, 27, 18, 17, 1, 15, 20, 15, 22, 23, 24, 25, 26, 16] ![0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 4, 2, 0, 1, 5, 0, 5, 0, 0, 0, 0, 0, 3] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step2 : KempeStep G 22 c1 c2 :=
  ⟨0, 2, ↑({1, 5, 6, 7, 15, 16, 20, 24, 25} : Finset (Fin 28)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 1, 1, 1, 8, 9, 10, 11, 12, 13, 14, 5, 7, 17, 18, 19, 15, 21, 22, 23, 16, 20, 26, 27] ![0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 3, 4, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step3 : KempeStep G 22 c2 c3 :=
  ⟨2, 3, ↑({0, 5, 6, 7, 8, 9, 10, 11, 13, 14, 17, 24} : Finset (Fin 28)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 1, 2, 3, 4, 0, 0, 8, 5, 10, 6, 14, 12, 5, 13, 15, 16, 24, 18, 19, 20, 21, 22, 23, 10, 25, 26, 27] ![0, 0, 0, 0, 0, 1, 1, 3, 2, 3, 2, 4, 0, 2, 3, 0, 0, 4, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step4 : KempeStep G 22 c3 c4 :=
  ⟨0, 2, ↑({0, 1, 3, 8, 11, 13, 15, 16, 17, 20, 25} : Finset (Fin 28)), by decide,
    whole_of_cert 0 _ (by decide) (by decide) (by decide) ![0, 0, 2, 0, 4, 5, 6, 7, 1, 9, 10, 3, 12, 15, 14, 8, 17, 15, 18, 19, 15, 21, 22, 23, 24, 11, 26, 27] ![0, 1, 0, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 4, 0, 3, 5, 4, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem step5 : KempeStep G 22 c4 c5 :=
  ⟨2, 3, ↑({1, 3, 5, 6, 7, 9, 10, 14, 15, 16, 24} : Finset (Fin 28)), by decide,
    whole_of_cert 1 _ (by decide) (by decide) (by decide) ![0, 1, 2, 9, 4, 1, 1, 1, 8, 10, 6, 11, 12, 13, 3, 5, 7, 17, 18, 19, 20, 21, 22, 23, 10, 25, 26, 27] ![0, 0, 0, 4, 0, 1, 1, 1, 0, 3, 2, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0] (by decide),
    swap_eq _ _ _ _ _ (by decide)⟩

theorem proper : ProperOff G 22 c0 := fun u v e hu hv =>
  (by decide : ∀ u v : Fin 28, G.Adj u v → u ≠ 22 → v ≠ 22 → c0 u ≠ c0 v) u v e hu hv

theorem unfilled : ¬ Target G 22 c0 := by
  rintro ⟨x, hx⟩
  obtain ⟨v, hv, e⟩ := (by decide : ∀ x : Fin 4, ∃ v, G.Adj 22 v ∧ c0 v = x) x
  exact hx hv e

/-- **The certificate state fills within 5 pure Kempe swaps** (the formal `PureFill`). -/
theorem pureFill : PureFill G 22 c0 5 :=
  ⟨5, le_rfl, c5, (.cons step1 (.cons step2 (.cons step3 (.cons step4 (.cons step5 (.nil c5)))))),
    ⟨3, fun v hv => (by decide : ∀ v : Fin 28, G.Adj 22 v → c5 v ≠ 3) v hv⟩⟩

end R91

end SimpleGraph.RadiusFive

#check @SimpleGraph.RadiusFive.R80.pureFill
#check @SimpleGraph.RadiusFive.R91.pureFill

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
