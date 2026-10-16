# Round 20: H-L2, big-big transfers in the wlp3 LP (16 Oct 2026) [exploratory; restricted LP, not a bound]

**Tool.** `l2.py`. Senders, rooted variables y and patterns are wlp3_j28_12's (`j28_12.args`, sep3). Ten d = 10
patterns from Studio's `r_5..r_8.out` are not in this checkout. Rows are whole arrangements (d, link, s). Start set:
Studio's 3,181 tight rows plus 372 rows of the 617 d = 7 family (18 are forbidden by the j28_12 patterns, the rest
repeat Studio's rows). Transfer x[tau] >= 0 per oriented edge type tau = (deg from, deg to, the two sides of the
edge, unordered); side = (common neighbour, vertex at 'from' and it, vertex at 'to' and it), letters 7, 8, 9. A row
with a big link vertex gets -x[out] + x[in]. Separation each iteration: y-only sep3 (d = 7..14, 200 per degree) and,
for every tau with x > 0, the heaviest allowed arrangement at the receiving end showing tau (degrees 7, 8, 9-12; DP
over 6-letter states with its own transfer terms, best-first, sep3 `c` for patterns and RBIG). x <= 3.

**Baseline** (`l2.py notx`): t* = 0.265306 = 13/49, as wlp3_j28_12.

**With transfers: t* = 0.259259 = 7/27** at every iteration, 0 to 6 (7,577 to 86,791 rows, 956 to 9,672 transfer
columns; the run was stopped at iteration 7 for the hour cap, not converged). Rows only raise t*, so the restricted
optimum is at least 7/27 > 0.25. **H-L2 dies** by the pre-registered bar. The guess (about 0.24) was too optimistic.

**What binds** (`l2_x.txt`, maxit=1, same t*): five d = 7 u-rows, dual 2/27 each. No d = 8, 9 or 10 v-row binds.
- 5765756 / 5556666, 5756756 / 6565665, 5756575 / 6555666: net transfer 0.
- 5567576 / 5756756 gives 2/9 to 5576576 / 5657756, and both bind.
- The first two and the fourth fit as their own 7-neighbour (pairs.py `fits`): the edge reads the same from both
  ends, so out-tau = in-tau and the transfer cancels. Any rule that sees only the two 2-balls moves no net charge
  across such an edge. The binders are d = 7 rows next to an identical d = 7 row, not slack big neighbours.
- HARD28-like rows: 44 of 49 slack at the optimum (all 49 are in the LP). Not all, so the second survive bar fails too.

**Reading.** Transfers relieve the HARD28 rows, as round 19's slack-neighbour signal said. The bound then moves to
d = 7 rows whose big neighbour is a copy of themselves. L2 with 2-ball edge types cannot get below 7/27 here; a
transfer rule would need information beyond both 2-balls, or these self-paired rows must be forbidden.
Caveats: restricted (rows the separation does not reach are missing, which can only overstate the gain);
not converged; y-only sep3 dedups by 5-path (up to 1,425 masked rows per iteration).
