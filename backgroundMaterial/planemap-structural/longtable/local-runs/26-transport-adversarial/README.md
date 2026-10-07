# 26-transport-adversarial [exploratory]

Run 25's transport T re-tested on the large adversarial classes, with the sharp variants and the Hall ratio.
Stand-alone engine `lib26.py` (same pi/lambda/DL as ../22-winding-escape/escape.py, class = BFS from a seed colouring, so 37-vertex graphs work;
Theorem W 3F-U=-5*sum(w) asserted on every class). Cost: all 136 classes about 90 s on one core (small orders 3 procs), nice 10, AC, nothing left running.

Files: `lib26.py`, `adv.py` (one hole of a C6 face-list json), `run_big.sh` (all deg-5 holes of the six C6 graphs, seed 1, 40 colourings),
`small.py N` (all 123 positive classes of orders 17-24, same list as run 25), `aggregate.py` -> `aggregate-output.txt`; data `big.jsonl`, `small-N.jsonl`.

Edge variants (positive cycle Z -> negative cycle N, link-free swap = component misses all 5 link vertices):
(a) from DL states, any colour pair; (b) from DL states, other pairs only (not {alpha,A},{alpha,B}); (c) from any state;
(d) DL, lock-breaking only; (e) DL, other-pair and lock-breaking. Lock-breaking = swap component meets the lock chains of that DL state
(the {mu,A}-component of m and the {mu,B}-component of m). Hall ratio = min over subsets S of positive cycles of cap(N(S))/supply(S).
Min cut: flow = supply everywhere, so the cut is the source side; the binding Hall set is in the jsonl (`hall_set`).

Results (136 classes: 13 adversarial + 123 orders <= 24):
- (a), (b), (c), (d), (e) all route the whole supply in all 136 classes. Zero-winding relays never needed. Min Hall ratio 4.0 (a),(b) (hog1152 h11, r5 h2/h23, order 17 g4).
- Item 1, A7 h22 (21,078 states, 147 pi-cycles: 3 positive, 79 zero, 65 negative; the 800-cycle w=+160 all DL, two +4): supply 168, reachable
  capacity 2748 (13 negative cycles) under (a) and (b), Hall ratio 16.36 (binding set = all three). Windings run down to -1042 (two cycles, L 7670).
  Full (w,L,count) histogram in aggregate-output.txt. The 21,078 class of hole 34 (same graph): supply 232, cap 2712, ratio 11.69.
- Other C6 classes: ratios 4.0 to 8.6, listed in aggregate-output.txt. The 13 classes reproduce the sweep log of NightCycleBound (sizes, positive windings).
- w >= +8 at orders <= 24: g2079 h0 (8 vs 72, ratio 9.0), g3633 h0 (8 vs 46, ratio 5.75).
- Lock-breaking exits: every positive cycle has a lock-breaking exit to a negative cycle in all 136 classes (so (d),(e) hold). But NOT every exit is
  lock-breaking: 14,380 of 15,333 DL exits to negative cycles are (93.8%); all negative exits are lock-breaking in 97 of 123 small classes and in 4 of 13 adversarial
  classes (e.g. the +160 cycle has 160 of 2542 non-lock-breaking exits). So the universal statement is "exists", not "all".
- Caveat: classes of C6 graphs come from random colourings, not all classes; sampling as in NightCycleBound.
