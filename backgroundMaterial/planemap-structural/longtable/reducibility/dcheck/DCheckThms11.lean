import DCheckThms
/-! Rings 10-11 (112 configurations; about 2 minutes compiled). -/
namespace DCheck
theorem rsst_r10_11_agree : (rsst.filter fun c => 10 ≤ c.r && c.r ≤ 11).all agreesRSST = true := by
  native_decide
end DCheck
#print axioms DCheck.rsst_r10_11_agree
