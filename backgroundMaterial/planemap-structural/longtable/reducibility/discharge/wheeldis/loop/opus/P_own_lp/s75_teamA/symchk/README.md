# jsepf symmetry cross-check (5 Nov 2026)

Question (swarm W12): does our separator lose arrangements the way the sep3r lineage does (prune before transfer terms are added)?

Code answer: no. Every load-raising term, transfers included, is in the window table WIN; the prune after w_k bounds h1 + exact windows 2..k-2 + V[d-k+2][A_{k-1}], which covers all d windows; everything outside WIN is a leaf correction <= 0.

Test: in08 (sol_q75B_in08_full, t = 0.034240721) tables from `KEEPWK=1 upper75.sh symchk08 ... dmax=9`, threshold lowered by 0.003 so rows exist, K = 200000, one thread, jsepf run directly with symmetry on (argv[4] = 1) and off (0). cmp.py canonicalises by rotation.

| d | sym rows / classes | nosym rows / classes | classes only in one | totals equal | clamped |
|---|---|---|---|---|---|
| 7 | 1,966 / 1,882 | 13,174 / 1,882 (= 7 x 1,882) | 0 / 0 | yes | 0 |
| 8 | 477 / 426 | 3,408 / 426 (= 8 x 426) | 0 / 0 | yes | 0 |
| 9 | 86 / 84 | 756 / 84 (= 9 x 84) | 0 / 0 | yes | 0 |

With symmetry off every rotation of every class is found, so no class is lost in any rotation (the W12 bug signature). The q7m and f2b clamp counters are 0, so no positive leaf correction was dropped.
