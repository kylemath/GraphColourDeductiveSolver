# explore-vhphi (EXPLORATORY, not evidence)

Long Table, 2026-10-05, run at the user's instruction ("explore, then check slowly after").
This is not a WP: no declaration, no go-ahead, no holdout orders. Orders 13-18 only.
Graphs come from random edge flips, not plantri. Every number here is post hoc and needs an
independent replay before it is cited.

- `vhphi_explore.py`: triangle-face test of VH_C (face-avoiding-reduction.md).
  Runs: seed 1 (orders 13-16), seeds 2 and 3 (orders 13-18). Result: 1308/1308 (T, phi) pure-pass.
- `vhphi_quad_explore.py`: quadrilateral-face pure game with the free adversary
  (four-cycle-reduction.md). Seeds 1-4. Seed 1 ran before the adversary-impact diagnostic was added.
- `vhphi_quad_mixed.py`: full game (Kempe swaps with the adversary, plus slides off phi) on a
  recorded pure-game failure. Seeds 2 and 4 found the same order-16 member, and no fan wins every start.
  This is the exploratory kill of the free-adversary VH^4.

Usage: `python3 vhphi_explore.py SEED ORDERS TRIES`, `python3 vhphi_quad_explore.py SEED ORDERS TRIES`,
`python3 vhphi_quad_mixed.py vhphi-quad-explore-seedN.json 0`.

## 17:22 additions (user approved downloading plantri 5.8 in this session)
- plantri 5.8 source: https://users.cecs.anu.edu.au/~bdm/plantri/plantri58.tar.gz, SHA-256
  e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8. Built locally (cc -O3); not committed.
- `vhphi_plantri.py`: exhaustive triangle-face reading on `plantri -c4m4 n -a`, n = 7..18 ->
  `plantri-c4m4-<n>.json`. 435 members, all pure-pass.
- `vhphi_quad_plantri.py`: free quad game on T - st with T from -c4m4, n = 12..18 -> `quad-plantri-<n>.json`.
  4004 members; the free game fails only on 16:1 - st (two symmetric edges).
- `vhphi_farside.py`: glues the 2 diagonals and all chordless `plantri -P4` discs with 1-5 interior
  vertices, in 8 alignments, into that member -> `farside-order16.json`. All 50 pairs are pure-good in all 2146.
- `vhphi_trace_game.py`: trace-constrained pure game on that member -> `trace-game-order16.json`. Every fan wins.

## 17:44 additions
- `vhphi_trace_k.py`: trace game on k-faces (k = 4, 5) with run-based bits; `plantri -P5`/`-P4` discs -> `trace-k5-7-13-pure.json`, `trace-k4-5-13-pure.json`. The 5-wheel fails (3 of 36 positions per fan), so wheels are excluded.
- `vhphi_trace_members.py`: every member T - x (deg x in {4,5}, chordless link) from `plantri -m4 n`, n = 8..18 -> `trace-members-<n>.json`. 2002 of 2002 pure-pass.
