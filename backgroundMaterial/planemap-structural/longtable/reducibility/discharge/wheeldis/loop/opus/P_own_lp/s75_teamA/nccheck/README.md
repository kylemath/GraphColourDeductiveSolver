# No-clamp separator check (5 Nov 2026)

Issue (swarm W10 gate): from in09 on, the l3q V7 payee credit Qeff(c, a, m) = max(lQ[m], max over a2 in m of lq[a2]) is not monotone in the private mask at (c6, a5): 0b11110 -> 0b11100 rises by 0.00145 at in09 (0.00081 at in14). The exact row value uses Qeff(m0 & ~extra) (prelay2 recv_coef_R2 / l3q_Qeff); the old jsepf leaf clamped the positive f2b correction to 0, undervaluing rows.

qmono.py scan (V7 / V8 Qeff over every submask): in01-in08 and sol_c_repaired monotone (delta 0); in09 0.0014529, in10 0.0013076, in11 0.0011768, in12 0.0010592, in13 0.0009268, in14 0.0008109 (all at c6, a5); V8 clean everywhere.

Fix: jsepf_nc (now s75_teamA/eng/jsepf.cpp, md5 of bin fbe2ad73): positive leaf corrections kept exactly; at load slack = d*dV6M + 2d*dQM + d*dQT; every prune and every leaf early exit before the f2b / q7m corrections uses cut - slack.

| check | result |
|---|---|
| upperR2 in09 (nc) | FEASIBLE 0.033528013422 (d=7 slack 0.02034, 95 positive corrections kept) |
| upperR2 in14 (nc) | FEASIBLE 0.031634694934 (d=7 slack 0.01135, 111 kept) |
| upperR2 in08 (nc, control) | FEASIBLE 0.034240720603 (slack 0, same as before) |
| F2B-SELFTEST in09, nc engine | PASS: d=7/8/9 3000 arrangements each, max abs(exact - leaf) <= 5e-13 |
| F2B-SELFTEST in09, old clamped engine (control) | FAIL: d=7 max 0.00145 at 6576659/6659786 |
