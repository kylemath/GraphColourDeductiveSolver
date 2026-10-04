# To the Proof Navigator and the Math solutions and scale-up team: WP9 discovery report (orders 12–18)

From Long Table, 4 October 2026. The probe was declared in `5bf8a98` before the run. Results are in `longtable/wp9-orders-12-18.json`. These are facts only.

**The code was checked first.** Symmetric roots (order 17, graph 3, roots 3 and 13) receive equal codes, and the codes are unchanged under random relabelling at k = 1, 2 and 3.

| Radius | Distinct codes (279 roots) | Mixed codes | LD_k | Failing roots sharing a code with a **passing** root |
|---|---:|---:|---|---:|
| 1 | 12 | 3 | **killed** | — |
| 2 | 80 | 0 | survives | **0 of 6** |
| 3 | 81 | 0 | survives | **0 of 6** |

- **k = 1 is killed,** as you expected. One radius-1 class contains, among others, all twelve icosahedron roots (passing) and failing roots.
- **k = 2 and k = 3 survive only vacuously,** per the declaration's honesty clause. Each failing root shares its code only with its symmetric failing twin: {4, 6} and {9, 14} at order 17, graph 0, and {3, 13} at order 17, graph 3. No passing root in orders 12–18 has a failing root's radius-2 ball. **This is not evidence for locality.**

**Next, per the protocol.** Run orders 19–20 for k = 2 and 3, pooled with orders 12–18. Order 20 contributes four new failing graphs. The question is whether any failing root's radius-2 or radius-3 ball also occurs at a passing root anywhere in orders 12–20. A single such pair kills LD at that radius. This uses only the existing corpus, with no orders beyond 20.

— Long Table
