# Lean: short fills through an easy neighbouring hole

Math / high_degree_landings, 5 October 2026. The new source and regression test kernel-compile against the complete 99-module protected-lift baseline in a private overlay. All eight exact axiom guards pass with `propext`, `Classical.choice`, and `Quot.sound` only. The root Math team owns the subsequent full module audit and project acceptance; this report records the local two-module verification.

Live source:

- `/Users/fulkanjou/mathlib4-planemap/Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyEasyNeighbour.lean`
- `/Users/fulkanjou/mathlib4-planemap/MathlibTest/PlaneMapVacancyEasyNeighbour.lean`

Committed-artifact-ready snapshots, compiler output, source hashes, and verification metadata are in `backgroundMaterial/planemap-structural/easy-neighbour-lean/`. Nothing was staged or committed by this agent. No graph census or new colouring search was run.

## Exact premises, using actual moves

Namespace: `SimpleGraph.VacancyEasyNeighbour`. The principal bridge is on arbitrary simple graphs and arbitrary colour types, with decidable equality; it assumes neither finiteness, planarity, nor a degree bound.

The definitions printed by Lean are:

```lean
OneSwapAt G h c :=
  Target G h c ∨ ∃ d, KempeStep G h c d ∧ Target G h d

EasyAt G u :=
  ∀ c : V → C, ProperOff G u c → OneSwapAt G u c

SlideAccess G h u c :=
  UniqueAt G h u c ∨ ∃ d, KempeStep G h c d ∧ UniqueAt G h u d
```

`KempeStep`, `Target`, `UniqueAt`, and properness are the existing actual vacancy definitions. A Kempe step swaps a whole active connected component in the deletion's two-colour graph. The optional preparatory move is therefore a genuine swap, not a black-box reachability or success relation.

## Bridge statements

The first printed statement, suppressing universe and instance binders, is:

```lean
singleton_easy :
  ProperOff G h c → G.Adj h u → UniqueAt G h u c →
  EasyAt G u → PureFill G h c 2
```

The proof derives properness after the singleton slide, obtains zero or one actual neighbouring-hole swaps from `EasyAt`, constructs the actual mixed path of length one or two, and applies the already compiled M3 theorem. The resulting `PurePath` keeps its hole at h.

`mobility_easy` assumes `SlideAccess` and returns `PureFill G h c 3`. In its preparatory-swap branch, it derives properness with `kempe_proper`, applies the two-move bridge to the current colouring, and prepends the actual initial swap to the pure path. It never assumes that a component persists through recolouring.

`mobility_alternative_easy` takes the geometric theorem's exact logical alternative:

```lean
OneSwapAt G h c ∨ SlideAccess G h u c
```

An immediate one-swap fill is included. It does not assume a uniform loop controller or any unproved termination principle.

## Protection at every actual intermediate hole

The printed protected statement is:

```lean
mobility_easy_protected :
  ProperOff G h c → h ∉ Z → G.Adj h u →
  (OneSwapAt G h c ∨ SlideAccess G h u c) → EasyAt G u →
  ∃ n ≤ 3, ∃ d,
    PurePath G h n c d ∧
    VacancyCliqueLift.ProtectedPath G Set.univ Z n (h,c) (h,d) ∧
    ProperOff G h d ∧ Target G h d
```

There is deliberately no premise `u ∉ Z`: the neighbouring hole can be protected. The auxiliary unrestricted slide is eliminated before constructing the protected path. `pure_path_protected` recursively translates the pure path into the existing all-intermediate-holes invariant, and `PurePath.proper` supplies actual endpoint properness. Colours on Z are allowed to change.

## Derived small-degree case

For a finite graph and palette `Fin 4`, `target_of_degree_le_three` derives a missing colour whenever `G.degree u ≤ 3`. Its proof bounds the cardinality of the neighbour-colour image by three and chooses a colour outside that image. No properness or geometry is needed for this pigeonhole fact.

`easy_of_degree_le_three` derives `EasyAt G u`, with no swap needed at u. The stronger terminal-slide consequences are also checked:

- `singleton_small`: a singleton slide to a neighbour of degree at most three has a pure fill of length at most one at the original hole.
- `mobility_small`: optional Kempe preparation plus that slide has a pure fill of length at most two at the original hole.

The **degree-four** neighbour case is intentionally not derived in this arbitrary-graph module. It requires the planar opposite-lock separation theorem, supplied separately by root's native spherical wrapper. Likewise this module's mobility witness is an explicit premise; the native degree-five mobility proof is a separate task. Thus the bridge does not misstate a conditional theorem as an unconditional arbitrary-graph degree-five result.

## Regression and verification

The regression graph is a five-leaf star. Its initial root link displays all four colours, so a missing-colour conclusion is not already true. It checks a singleton-apex branch and a genuine preparatory component swap: one of the two repeated-colour leaves is recoloured, making the chosen other leaf singleton. The original chosen leaf is explicitly verified not to be singleton. The tests then invoke the bridge and its sharper small-neighbour variants.

The protected regression includes the auxiliary easy neighbour in Z and checks an actual protected pure filling path at the original root. Eight `#guard_msgs` blocks enforce the exact standard-three-axiom lists. Printed statements and the expanded premise definitions are retained in `test-compile.txt`.

Verification metadata records unchanged hashes for all 99 baseline sources, stable new source hashes before and after compilation, successful source and test compilation, and the isolated full-overlay `LEAN_PATH`. Root should add the two modules to the full audit before upgrading the project status.
