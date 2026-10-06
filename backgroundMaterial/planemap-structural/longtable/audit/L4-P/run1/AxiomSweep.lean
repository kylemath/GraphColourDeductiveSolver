import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyLemmaL4
import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleNoSingleton
open Lean Elab Command

/-- Audit sweep: every non-internal constant declared in the nine new source modules. -/
def auditMods : List Name :=
  [`Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyLemmaL4,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleBasic,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleMoves,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleRules,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleCut,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleDegen,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleChain,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleFlip,
   `Mathlib.Combinatorics.SimpleGraph.PlaneMap.TheoremPPoleNoSingleton]

#eval show CommandElabM Unit from do
  let env ← getEnv
  let idxs := auditMods.filterMap env.getModuleIdx?
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if let some i := env.getModuleIdxFor? c then
      if idxs.contains i && !c.isInternal then
        n := n + 1
        let axs ← liftCoreM (collectAxioms c)
        for a in axs do
          if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then
            bad := bad.push (c, a)
  logInfo m!"modules found: {idxs.length} of {auditMods.length}; constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"
