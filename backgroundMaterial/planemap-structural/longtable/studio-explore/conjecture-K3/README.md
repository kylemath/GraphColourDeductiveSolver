# [exploratory] Conjecture K3 at scale (Mac Studio)

**K3** (coordinator, from the sage's k-step idea): from every unfilled state at a degree-5 hole, some sequence of at most 3 Kempe swaps reaches a filled state or a state with strictly smaller Phi = (lock_size, lock_dist) in lex order.

## Definitions (same as run 5, `../sage-qa-runs/potentials2.py`)
For an unfilled state, with repeat c(x_j) = c(x_{j+2}), m = x_{j+1}, a = x_{j+3}, b = x_{j+4}, mu = c(m), A = c(a), B = c(b):
- lock_size = |{mu,A}-component of m| + |{mu,B}-component of m|;
- lock_dist = (BFS path length m -> a inside the first, or 0 if a is not in it) + (the same for m -> b in the second).

Moves are whole two-colour component swaps on all 4-colourings of T - v, up to renaming. dist is the fewest moves to a filled state.

## Run
- Engine: `k3.cpp`. It agrees exactly with the Python least-k (`potentials3.py --leastk`) on certificates 91a307 h22 and 80b930 h23, and on the counterexample below.
- Coverage: `k3scan.py` over EVERY degree-5 hole class with rho >= 4 in the exhaustive plantri -m5 -c4 census, orders 20-26 (17,694 holes). Every unfilled state at distance >= 4 was tested (41,326 states).
- Wall time: about 1 minute, 6 workers, nice 10.

| order | holes (rho >= 4) | states at distance >= 4 | k=1 | k=2 | k=3 | k=4 | max k |
|---|---|---|---|---|---|---|---|
| 20 | 4 | 4 | 4 | 0 | 0 | 0 | 1 |
| 21 | 30 | 49 | 46 | 3 | 0 | 0 | 2 |
| 22 | 87 | 152 | 123 | 6 | 23 | 0 | 3 |
| 23 | 229 | 369 | 279 | 50 | 40 | 0 | 3 |
| 24 | 1077 | 1762 | 1528 | 111 | 123 | 0 | 3 |
| 25 | 3823 | 8693 | 7568 | 836 | 289 | 0 | 3 |
| 26 | 12424 | 30297 | 26309 | 2330 | 1650 | **8** | **4** |

## Result: K3 is FALSE at order 26
- 8 states need k = 4, in 4 holes (`k3-26-counterexample-holes.jsonl`): plantri index 5401 hole 13 (rho 5), 11163 hole 14 (rho 5), 53534 hole 16 (rho 4, 4 states) and 56043 hole 3 (rho 4, 2 states).
- First counterexample: order 26, plantri index 5401 (0-based), hole 13, a state at distance 5:
  - graph: `26 bcdef,afghic,abijd,acjke,adklf,aelmgb,bfmnh,bgnoi,bhopjc,cipqrkd,djrsle,ekstumf,flung,gmuoh,hnuvwxpi,ioxqj,jpxyr,jqyzsk,krztl,lszvu,ltvonm,outzw,ovzyx,owyqp,qxwzr,rywvts`
  - colouring: in `k3-summary.jsonl` (`first_counterexample`).
- Confirmed independently by `potentials3.py --leastk`: at that hole, 1 state at distance 5 has least k = 4.
- k <= 3 holds at every hole of orders 20-25. "k <= 4" is untested beyond order 26.
- These holes all have finite radius (R* holds there). K3 fails as a descent statement, not as R*.
