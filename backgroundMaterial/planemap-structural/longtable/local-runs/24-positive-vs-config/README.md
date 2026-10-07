# 24-positive-vs-config [exploratory]

Question: do positive-winding pi-cycles (Theorem W, NightEulerHole) occur only in graphs containing a Birkhoff diamond or RSST 2.122?
Reuses pi/winding code of ../22-winding-escape/escape.py and ../23-positive-cycles/scan.py (analyse asserts Theorem W on positive classes).

- `conf.py`: diamond and 2.122 detector (audit message 2026-10-06_1516 sec 3-4: K4-e with two faces, tips non-adjacent, degrees 5555 / 6555).
- `task1.py` -> `task1-output.txt`, `task1.json`: the 123 positive (graph,hole) classes of orders 17-24 versus configurations.
- `task2.py` -> `task2-output.txt`, `task2.json`: all config-free gentri graphs at orders 22-24 (1,1,4), every deg-5 hole, every class.
  Order 25 not run: no gentri list at 25 and no plantri here (no downloads).
- `task3.py`, `task3-44.log` -> `task3-output.txt`: IPR fullerene duals (config-free by construction; asserted), all graphs of 32-43 vertices
  (27 graphs incl. C60 dual n=32, C70 dual n=37) plus 10 of 24 graphs at n=44 (run hung at the pool tail and was killed; results parsed from the log);
  all 12 deg-5 holes each (425 graph-holes). Mirror image gives same windings (checked on order 17 g4).
- Cost: seconds to a few minutes, 4 procs, nice 10, AC.
Orientation note: windings do not depend on rotation orientation (tested).
