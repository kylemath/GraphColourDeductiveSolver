# A6: does "Fewest locks, new stars" always reach a fill? (Studio Job 11, 14 Oct 2026) [exploratory, data]

The hypothesis and kill criterion were written before the run: `HYPOTHESIS.md`.

## Method

- **Rule.** The game team's built-in rule `few-locks-new`: fill if possible; otherwise fewest locks; prefer an unvisited
  star; ties go to the smaller chain, then the smaller key. It is taken from 4square `lab/star-rules.js` and run
  unchanged with `rim.js` and `degree.js` (`a6_run.js`).
- **Starts.**
  - Every colouring of T − hole is enumerated (arena engine `stateSpace`) and split into Kempe classes by
    `FTH_STAR.graph`. Coverage is checked: the classes contain every colouring at every hole.
  - The rule runs from **every hard star (dF ≥ 2, the double locks)** of every class. When a class has more than 200,
    it runs from a fixed sample of 200, chosen deterministically by key hash.
  - Easy stars (dF = 1) always have a filling child, so the rule fills them in one swap.
- **Second implementation.** `a6_check.py`, pure Python with its own chains, keys, frame, locks and π. It reproduces
  163 of 163 rule walks key for key on three census holes, and would re-check any failure.

## Results (`out/summary_census.txt`, `out/summary_hardset.txt`)

| set | holes | classes | hard stars | walks | solved | failures | walks revisiting a star | max swaps | mean swaps over par |
|---|---|---|---|---|---|---|---|---|---|
| frame census, orders 22–28 (all degree-5 holes) | 2,202 | 2,244 | 313,000 | 301,300 | 301,300 | **0** | 0 | 6 | 0.0005 |
| hardset-v1, census floor-tight | 150 | 334 | 44,763 | 28,936 | 28,936 | **0** | 0 | 5 | 0.001 |
| hardset-v1, glued floor-tight | 50 | 168 | 794,609 | 11,038 | 11,038 | **0** | 0 | 21 (hg_glue4_177) | 0.008 |
| hardset-v1, R0 maps | 2 | 2 | 198 | 198 | 198 | **0** | 0 | 3 | 0 |
| hardset-v1, non-D-reducible 2-balls | 100 | 103 | 28,504 | 19,821 | 19,821 | **0** | 0 | 5 | 0.001 |

H survives: in 361,293 walks the rule never looped, hit the cap or got stuck, and it never even revisited a star. On
the large glued classes only 200 hard stars per class were walked (11,038 of 794,609).

## Decreasing measure (`measures.py`, `out/measures.txt`)

Over the recorded paths (361,151 walks, 724,222 steps; all failures and revisits would have been kept):

| measure | steps where it strictly decreases | walks where it decreases at every step |
|---|---|---|
| dF (distance to a fill; not local) | 0.9996 | 0.9995 |
| (lock, −moves) lexicographic | 0.9992 | 0.9987 |
| (lock, \|Fisk degree\|) | 0.9983 | 0.9969 |
| lock | 0.9974 | 0.9955 |
| Fisk degree, chains N, moves (alone) | 0.29–0.38 | 0.04–0.09 |

- **No local quantity strictly decreases at every step.**
- The steps where dF does not decrease are double-locked moves from dF 3 to dF 3 (257 steps).
- The steps where lock does not decrease are double-lock → double-lock moves.

So termination does not follow from a simple potential. The rule works because a fewest-lock child at a double lock
almost always shortens the distance. That is the step a proof would have to explain.
