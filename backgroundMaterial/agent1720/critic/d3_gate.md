# Gate: D3b signed Tait counts

**Date:** 2 October 2026
**Report:** `backgroundMaterial/agent1720/groups/D3b_report.md`
**Checked against:** `backgroundMaterial/agent1720/groups/D3_results.json`

On all 23 planar duals of triangulations with \(n \le 8\), every Tait colouring of a given dual has the same sign. `mixed_sign_graphs` is empty. The absolute value of the signed count equals the Tait count. The sign itself is \(+1\) on 17 graphs and \(-1\) on 6: positive for \(n = 4,6,8\) and negative for \(n = 5,7\). Elapsed 0.104s. The counts match the earlier Tait counts.

This does not prove a Tait colouring exists. Equal signs turn the count into a signed count; vanishing of the signed count is still equivalent to there being no colouring. Ellingham–Goddyn 1996 (Combinatorica, doi:10.1007/BF01261320) then says a planar cubic graph that is already 3-edge-colourable is 3-edge-choosable. That is a consequence, not a proof of the Four Colour Theorem.

The kill test "sign cancellation on a single small graph" is not met.
