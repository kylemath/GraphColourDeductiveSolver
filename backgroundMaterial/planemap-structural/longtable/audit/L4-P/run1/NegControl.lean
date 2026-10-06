import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyLemmaL4
open Lean Elab Command
theorem planted : 1 = 2 := sorry
#eval show CommandElabM Unit from do
  let axs ← liftCoreM (collectAxioms ``planted)
  let axs2 ← liftCoreM (collectAxioms ``SimpleGraph.VacancyLemmaL4.l4c)
  logInfo m!"planted: {axs}; l4c: {axs2}"
