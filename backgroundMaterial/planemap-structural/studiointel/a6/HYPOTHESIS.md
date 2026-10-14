# A6 hypothesis (written 2026-10-14 12:21 MDT, before any run)

- **H:** on every hole of hardset-v1 (302 maps) and every degree-5 hole of the frame census at orders 22–28, the rule
  "Fewest locks, new stars" (4square lab/star-rules.js, built-in few-locks-new: fill; fewlocks; new) reaches a fill
  from every hard star (dF >= 2) of every Kempe class: from all of them, or from a fixed sample of 200 per class when
  a class has more.
- **Kill criterion:** any start where the walk ends without filling: loop (stuck), cap (60 swaps) or dead (no moves).
  Each failure is re-checked by an independent implementation (a6_check.py, Python, own colouring and lock code)
  before it is reported.
- **If H survives:** search for a quantity that strictly decreases along every rule path (lock count, dF, Fisk degree,
  trouble-spot index, and lexicographic combinations), and report the best one and its violation rate.
