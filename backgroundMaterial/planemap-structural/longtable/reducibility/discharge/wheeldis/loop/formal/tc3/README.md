# Triple-wheel windows (Claude, 21 Oct 2026, one engine: kc Jacobi + Gauss-Seidel)

Gemini's chiral C3 triple wheel T_C3 (logbook post 1120PM OCT20), built from its vertex names by `build_tc3.py`
(adjacency fixed from the rotation at each hub: u_i link = u_{i+1}, u_{i+2}, a_i, b_i, c_i, d_i, a_{i+1}; wings
a_{i+2}, d_{i+2}, p_i, q_i, r_i, s_i, b_{i+1}). Every interior degree and the disc Euler count E = 3V - 3 - r were
checked by the builder. Ring vertices (p, q, s, x, y, and in the sub-windows u2/b2/c2/d2) carry no degree.
Lines in `tc3_all.txt` are in the wheeldis format (name r m ringadj intadj) and run with `kc -j FILE`.

| window | interior | ring | kc verdict |
|---|---|---|---|
| TC3_C13 = B1(u0) u B1(u1) minus u2, plus r0, r1 | 13 | 15 (Gemini said 14) | D, depth 10 (GS depth 4) |
| TC3_C14 = B1(u0) u B1(u1) plus r0, r1 | 14 | 15 | D, depth 6 |
| TC3_C18 = all three B1(u_i) plus r0, r1, r2 | 18 | 15 | D, depth 3 |
| TC3_P11 = {u0, u1} + both links, no r | 11 | 15 | D, depth 11 |
| TC3_P12 = P11 + r0 (or + r1) | 12 | 15 | D |
| TC3_P10 = u0 + link(0) + r0 + u1 + b1, c1, d1 | 11 | 14 | D, depth 10 |
| TC3_P9 = u0 + link(0) + r0 + b1, c1 | 9 | 14 | not D (40,427 / 199,291) |
| TC3_P8 = u0, u1 + link(0) + r0 | 8 | 13 | not D (14,877 / 66,430) |
| TC3_P7 = u0 + link(0) + r0 (control: the single-hub window) | 7 | 11 | not D (2,567 / 7,381, equal to the drawing thread's base window) |

Reading: the single hub survives, as known. Two hubs of type 7766556 joined along their 7-7 edge in the chiral
orientation, with both links fixed, are D-reducible at ring 14-15. Needs a second engine (dfast18) before it counts.
