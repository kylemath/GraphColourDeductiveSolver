import DCheckData
/-! D-reducibility of the RSST configurations with ring <= 9 (and an aggregate check for
rings 10-11), evaluated by the compiled checker via `native_decide`. Axiom: `Lean.ofReduceBool`
(recorded by `#print axioms` below). These say what the checker COMPUTES; soundness is
`DCheckSound.lean`. -/
namespace DCheck

/-- RSST 0.7322: D-reducible. -/
theorem dred_cfg_0 : dReducible cfg_0 = true := by native_decide
/-- RSST 2.122: D-reducible. -/
theorem dred_cfg_1 : dReducible cfg_1 = true := by native_decide
/-- RSST 3.442802: D-reducible. -/
theorem dred_cfg_2 : dReducible cfg_2 = true := by native_decide
/-- RSST 0.453962: D-reducible. -/
theorem dred_cfg_4 : dReducible cfg_4 = true := by native_decide
/-- RSST 3.1306802: D-reducible. -/
theorem dred_cfg_5 : dReducible cfg_5 = true := by native_decide
/-- RSST 2.7566: D-reducible. -/
theorem dred_cfg_6 : dReducible cfg_6 = true := by native_decide
/-- RSST 0.79077722: D-reducible. -/
theorem dred_cfg_7 : dReducible cfg_7 = true := by native_decide
/-- RSST 0.79077962: D-reducible. -/
theorem dred_cfg_11 : dReducible cfg_11 = true := by native_decide
/-- RSST 122.122: D-reducible. -/
theorem dred_cfg_23 : dReducible cfg_23 = true := by native_decide
/-- RSST 122.442802: D-reducible. -/
theorem dred_cfg_24 : dReducible cfg_24 = true := by native_decide
/-- RSST 122.363: D-reducible. -/
theorem dred_cfg_26 : dReducible cfg_26 = true := by native_decide
/-- RSST 0.260517722: D-reducible. -/
theorem dred_cfg_37 : dReducible cfg_37 = true := by native_decide
/-- RSST 7322.122: D-reducible. -/
theorem dred_cfg_323 : dReducible cfg_323 = true := by native_decide
/-- RSST 2.126 (C-reducible in RSST): the D-closure does not reach every class. -/
theorem not_dred_cfg_3 : dReducible cfg_3 = false := by native_decide
/-- RSST 122.126 (C-reducible in RSST): the D-closure does not reach every class. -/
theorem not_dred_cfg_25 : dReducible cfg_25 = false := by native_decide

/-- Birkhoff diamond: closure data as in dred.py (31 classes, 16 extend, depth 5). -/
theorem diamond_run : run cfg_0 = { classes := 31, ext := 16, reached := 31, depth := 5 } := by
  native_decide

/-- Agreement with RSST on all 15 configurations with ring <= 9: extendable-class count equals
RSST's header field and D-reducible iff RSST's contract size is 0. -/
def agreesRSST (c : Conf) : Bool :=
  let res := run c
  res.ext == c.rsstExt && ((res.reached == res.classes) == (c.rsstContract == 0))

theorem rsst_r9_agree : (rsst.filter (·.r ≤ 9)).all agreesRSST = true := by native_decide

end DCheck

#print axioms DCheck.dred_cfg_0
#print axioms DCheck.dred_cfg_1
#print axioms DCheck.dred_cfg_2
#print axioms DCheck.dred_cfg_4
#print axioms DCheck.dred_cfg_5
#print axioms DCheck.dred_cfg_6
#print axioms DCheck.dred_cfg_7
#print axioms DCheck.dred_cfg_11
#print axioms DCheck.dred_cfg_23
#print axioms DCheck.dred_cfg_24
#print axioms DCheck.dred_cfg_26
#print axioms DCheck.dred_cfg_37
#print axioms DCheck.dred_cfg_323
#print axioms DCheck.not_dred_cfg_3
#print axioms DCheck.not_dred_cfg_25
#print axioms DCheck.diamond_run
#print axioms DCheck.rsst_r9_agree
