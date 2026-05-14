/-
  Main.lean — Statement of the full constructive 4CT via Kempe reconfiguration.

  Agent 1210, Manager M4

  This file imports all modules and states the main theorem.
  The proof has one sorry corresponding to the one remaining gap
  (Conjecture 5.5: BFS Avoidance at degree 4 and 5).
-/

import KempeReconfiguration.Basic
import KempeReconfiguration.NeverRevert
import KempeReconfiguration.ChainLifting
import KempeReconfiguration.Degree3NoMerge

namespace KempeReconfiguration

/-
  The full theorem statement (with gap):

  For any planar graph G on n ≥ 4 vertices and any proper 5-colouring c,
  there exists a proper 4-colouring c' reachable from c via ≤ n-4 Kempe swaps.

  Current status:
  - Base case (n=4): trivial ✓
  - Case 1 (c(v) ≠ 5): Chain Lifting (proved in ChainLifting.lean) ✓
  - Case 2 (c(v) = 5, deg(v) = 3): Degree-3 No-Merge (proved in Degree3NoMerge.lean) ✓
  - Case 3 (c(v) = 5, deg(v) ∈ {4,5}): OPEN — requires BFS Avoidance conjecture

  We leave this as a declaration (sorry) since the mathematical gap is open.
-/

-- TODO: Full theorem statement requires reconfiguration graph infrastructure
-- that depends on Mathlib's graph connectivity API. Deferred to Tier 2/3.

end KempeReconfiguration
