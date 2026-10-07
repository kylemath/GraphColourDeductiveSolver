# 22-winding-escape [exploratory]

Test of Conjecture X: every positive-winding pi-cycle Z has a DL state s whose link-preserving swap (component with no link
vertex) reaches a cycle of negative winding.

- `escape.py`: exact pi and lambda from NightEulerHole §3 table (R+3 via x_{j+2}, phiB^-1 via x_{j+4}, phiA via x_{i+2}, tau via x_{i+3});
  all pi-cycles of every degree-5 hole of gentri 12-22; for each class with a positive cycle, BFS the class, check 3F-U = -5 sum w,
  build the link-preserving flow graph, test X, X', X'', X'''. Output `out-N.jsonl`; `aggregate.py` -> `aggregate-output.txt`.
- `checks.py` -> `checks-output.txt`: full per-class check of Theorem W at orders 12-19 (all classes), and the n=16 torus sanity check.
- Variants: X = {alpha,A}/{alpha,B} swap from a DL state of Z, reached winding < 0. X' = ... <= 0. X'' = any link-preserving swap of
  any pair from a DL state of Z. X''' = sequence of <= 2 link-preserving swaps from a DL state. "X2any" = X'' from any state of Z.
- Numbering: gentri index is 1-based here; the notes' "#3" is 0-based, so it is "g4" here (reproduced: class 100/40, Gamma-cycle L=20, w=+4, other cycle -16).
- 23 positive cycles at orders 17, 20, 21, 22 (2, 2, 2, 17), matching the notes. Orders 12-16 have none. Order 23-24 not run.
- Run cost: orders 19-22 in 32 s on 3 cores, nice 10, AC power.
