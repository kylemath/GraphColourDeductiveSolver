# 23-positive-cycles [exploratory]

Extension of ../22-winding-escape to orders 23 and 24 (FULL gentri lists, 2054 and 7209 graphs; no sampling needed), plus
re-run of orders 12-22 with the same new script. Reuses pi/lambda/DL code of escape.py (Theorem W asserted on every positive class).

- `scan.py N`: per degree-5 hole, all pi-cycles (histogram of (winding, length)); for each class containing a positive cycle:
  windings of all cycles, per positive cycle the link-preserving-swap neighbours (swap component misses all 5 link vertices),
  neighbour windings, most negative neighbour, and descriptors of the swaps reaching it: (from-state DL?, colour pair is
  {alpha,A}/{alpha,B} or other [DL states only], component meets ring-2 [non-link neighbour of a link vertex], size).
- `out-N.jsonl`, `aggregate.py` -> `aggregate-output.txt`, `special-cases.txt` (all classes with 2 positive cycles or w>4).
- Cost: 4 procs, nice 10, AC: order 23 84 s, order 24 426 s, orders 12-22 about 25 s.
- Counts are per (graph, hole) state space; holes of one graph often give identical classes (114 distinct (graph,class-signature)).
- Orders 13 and 15 have no list.

Results (123 classes / 125 positive cycles at 17-24): at-most-one-per-class FALSE (2 classes at order 24: g906 h22, two w=4 L=20
cycles; g6864 h21 w=1 L=45 and w=2 L=14); max winding is 8 not 4 (order 24 g2079 h0 w=8 L=104; g3633 h0 w=8 L=64);
windings seen +1,+2,+4,+8; lengths NOT all = 0 mod 10 (L=17,21,14,18,...); every positive cycle has a negative flow neighbour
and |w-| >= w+ in all 125 (min neighbour from -6 to -104); no pattern in swap type (see aggregate-output.txt).
