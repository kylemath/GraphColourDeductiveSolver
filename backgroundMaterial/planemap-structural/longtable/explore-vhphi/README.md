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
