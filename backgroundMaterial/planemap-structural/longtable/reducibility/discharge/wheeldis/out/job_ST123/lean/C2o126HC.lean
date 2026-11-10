import CGlueM

/-! # C2o126HC: the C verdict of 2.126 (ST-123 S0, 10 Nov 2026)

The C verdict is `cReducible18` on `rsst003_2o126` with RSST's `X = {R0-I0, R2-I0, R4-I2, R6-I2}`. This is the
per-key hC computation (`native_decide`, as `cf66666_hC` in CGlue). Sabotage: one star alone is refused. (X = ∅ is not a useful sabotage: `cReducible18 cf [] []` is true for any
configuration, since a colouring that extends without contraction is good by definition, as found 10 Nov.
Soundness needs an X-edge, `XLoopFree`.1.) -/

namespace SimpleGraph.SphericalMap.CGlue
open DCheck

theorem cf2o126_hC : cReducible18 cf2o126 eqR2o126 eqI2o126 = true := by
  native_decide

/-- Sabotage: one star alone (X = {R0-I0, R2-I0}) does not suffice. -/
theorem cf2o126_not_oneStar : cReducible18 cf2o126 [(0, 0), (2, 0)] [] = false := by
  native_decide

/-- 2.126 as a merged-class C entry. -/
def e2o126C : CEntryM := e2o126 cf2o126_hC

end SimpleGraph.SphericalMap.CGlue

#print axioms SimpleGraph.SphericalMap.CGlue.cf2o126_hC
#print axioms SimpleGraph.SphericalMap.CGlue.e2o126C
#print axioms SimpleGraph.SphericalMap.CGlue.cf2o126_not_oneStar
