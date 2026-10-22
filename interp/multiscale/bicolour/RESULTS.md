# Bicoloured-run cap on the straight degree-6 tube (22 Oct 2026, ~60 min box)

w* = least w with C(w) true (exhaustive bf2 copy `bfr.c`, all pairs, 24 renamings). "seam" = cap only on the level seam rows; "collar" = cap on every side row from depth 0 to w. old = mode 1 (tau<=1 from some column); pair = Hodge pair, T=1. v = no admissible seam row exists. `3=` means identical to unfiltered, because every level row already has runs <=3 (histograms in wstar.jsonl). `..` = not finished in the time box.

| filter | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| unfiltered (Opus) | 1 | 1 | 2 | 2 | 2 | 3 | 3 | 3 | 4 | 4 | 4 |
| old k0=2 seam | v | 1 | 1 | v | 1 | 2 | v | 2 | **3** | v | .. |
| old k0=3,4 seam | 1 | 1 | 2 | 2 | 2 | 3 | 3 | 3= | 4= | .. | 4= |
| pair k0=2 seam | v | 1 | 1 | 1 | 1 | 2 | 2 | 2 | **3** | .. | .. |
| old k0=2 collar | v | 1 | 1 | v | 1 | 1 | v | 1 | 2 | .. | .. |
| old / pair k0=3 collar | 1 | 1 | 1 | 2 | 1 | 2 | 2 | 2 | 2 | .. | .. |
| old k0=4 collar | 1 | 1 | 2 | 2 | 2 | 2 | 3 | 2 | 3 | .. | .. |
| old k0=5 collar | 1 | 1 | 2 | 2 | 2 | 3 | 3 | 3 | 3 | .. | .. |
| pair k0=2 collar | v | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | .. | .. |

**1. Seam cap. It does not bound w\*.**
- [P] A correction to the premise. On the tube every sign is +, so a bicoloured run x,y,x,... has constant label x⊕y and the height moves in a *straight* line; it does not oscillate. So levelness already caps seam runs at 3 (or 5 across the base column when t≠0). Two-point oscillation only happens on boundaries with alternating signs. The metric does see seam runs; what it misses is the deep rows.
- [P] Hence k0≥3 is vacuous whenever t=0. The Opus L=18 pair has seam runs exactly 3 (row runs 7,6,5,4,3 \| 3,4,5,6,7), so w\*(18) ≥ 5 for every k0≥3.
- [C] k0=2 still grows: w\*(13) = 3 for both old and pair.
- [P] Cone lemma read backwards: a depth-w run of length m forces a seam run of length m−w, so a depth-w run is at most k0+w long. [C] This bound is attained: max run in DA_w for k0=2 at L=15 is 3, 4, 5, 6 for w=1..4.
- [P] k0=2 means a proper colouring of C_L², which is impossible at L=5. [C] With old levelness it is empty at L=8, 11 and 14 (L≡2 mod 3). So k0=2 cannot be a global invariant under old levelness; under the pair it fails only at L=5.

**Collar (Clarance's question).**
- [C] Under the collar, w\* ≤ 2 for k0≤3 through L=13, compared with 4 unfiltered. k0=4 and 5 reach 3 at L=13.
- [M, weak] Boundedness is unknown: L=14 and 15 did not finish.
- [C] The capped failures are not cone collisions:
  - k0=3, L=13: the bad rows carry five separate runs of length 3 (e.g. a=2030120102010). This is many short runs colliding.
  - k0=2, L=13: the bad pair a=3210312031201, b=3023102301201 has **no** bicoloured triple at all.
  - Every collar failure seen for k0≤3 is at w=1 and is fixed at w=2.

**2. Leaves, pockets and the one-sided transition.**
- [C] 30 discs from leaves.py's generator (ico10 balls, cap2 and vor3; ico20 balls; the remaining classes were not reached):
  - cap alone: k0=2 is satisfiable on every disc;
  - cap + tau_int≤1: least k0 is 2 on 22 discs and 3 on 8;
  - cap + pair (T=1): least k0 is 2 on 21 discs and 3 on 9;
  - the discs needing 3 are mostly odd (point-reflection) pockets. k0=3 was always enough.
- [C] Tube, exhaustive for L=5..15 and k0=2..5: every capped row has a capped neighbour in both directions.
- [P] For k0=2 this has a one-line proof: r′(i) = r(i+2) is a successor.
- [C] Transition with cap AND level:
  - pair: 0 rows lack an admissible neighbour, L=6..14 (L=15 partial).
  - old mode 1: rows fail at L=11 (528 of 11,616 at k0=3) and L=14 (15,792 of 92,736). Without the cap the failures are 2,376 and 53,088. So the failure comes from old levelness, not from the cap.
- [C] A seam cap is never inherited by deeper rows (runs reach k0+w). A collar has to be imposed.

**Cross-check against Xandu: all overlapping numbers agree.**
- One-step closure holds (above).
- There are 8,376 cap-3 states at L=9.
- Maximum shortest capped path is 4, 6, 5, 8 at L=5..8 (cap 3).
- At L=8, 2,500,320 of 9,585,216 ordered pairs are joined by a capped path. Allowing the 24 renamings of the target, 7,534,656 are joined, with a maximum of 7 (`joinpaths.py`).
- The Opus row 303030202020101010 has run 7, so it needs ≥4 steps to reach cap 3 [P, cone].
- Greedy extension was not rechecked.

**3. Window circumradius. [P]** A sub-arc's points are a subset of the walk's points, so they lie in any ball that contains the walk. Numeric check: 590,700 windows over 6,600 raw and Hodge-detrended walks, 0 violations. Caveat: when t≠0, a window that wraps past the base column is not a sub-arc.

Files: `bfr.c`, `drive.py`, `wstar.jsonl`, `table.py`, `ext.log`, `levext.log`, `depthrun.log`, `leaves_cap.py`/`.jsonl`, `joinpaths.py`, `window_check.py`; copies of `bf.c`, `bf2.c`, `bfp.c` and `csp.py`. Binaries were built in the scratchpad (the mount is noexec).
