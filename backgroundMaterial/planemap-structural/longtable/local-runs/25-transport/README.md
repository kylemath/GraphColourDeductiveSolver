# 25-transport [exploratory]

Capacitated transport T on ALL 123 (graph,hole) Kempe classes with a positive pi-cycle, orders 17-24 (orders 12-16, 18, 19: no positive class,
per run 23). Reuses pi/lambda/DL code of ../22-winding-escape/escape.py and class construction of ../23-positive-cycles/scan.py.
Sources: positive cycles (supply w). Sinks: negative cycles (capacity |w|). Edge Z->N: a link-free swap (component misses all 5 link vertices,
any colour pair) from a state of Z lands in N. Exact max-flow; Hall deficiency by enumerating all subsets of positive cycles (max 2 per class).
Cost: 25 s total, 3 procs, nice 10, AC.

Files: `scan.py N`, `out-N.jsonl`, `aggregate.py` -> `aggregate-output.txt`.

Variants: T1 edges from DL states only; T2 from any state; T3 only DL states with {alpha,A}/{alpha,B} swaps (T3x: the other pairs);
T4 d2: sinks reachable within two hops via a relay cycle (zero-winding only / any cycle; first hop DL or any).

Results (123 classes, 125 positive cycles):
- T1 holds 123/123. T2 holds 123/123 (T1 and T2 differ in reachable capacity in 38 classes, never in verdict).
- T3 (alpha,A/alpha,B only) FAILS in 29/123 (first: order 17 gentri 4 hole 0, w=+4, no such edge at all). T3x (other pairs only) holds 123/123.
- Relays (distance 2, zero-winding or any cycle) hold 123/123; they are never needed: T1 already holds everywhere (0 classes where T1 fails and relay saves).
- Minimum slack (reachable sink capacity - supply) = 12 (order 17, g4, h0/h16: supply 4, capacity 16); min cap/supply ratio over all
  subsets (Hall) = 4.0 under T1 and T2. Next tightest: o24 g3633 h0 (8 vs 46), o24 g2071 h2 (4 vs 28), o22 g570 h6 (2 vs 16).
- Both 2-positive classes: o24 g906 h22 ({4,4}: cap 80 reachable, ratio 10), o24 g6864 h21 ({2,1}: ratio 13): no tight cut.
No bad cut approaches a failure; the data are not close to the boundary (ratio >= 4). Orders <= 24 only; the adversarial 37-vertex cases are in 23/NightCycleBound.
