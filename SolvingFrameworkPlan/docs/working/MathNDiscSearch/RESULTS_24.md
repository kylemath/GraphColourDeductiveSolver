# RESULTS_24 (N=24) [computed, exploratory, post hoc; no universal claim]

Generator: `disc_gen2` (4 parallel parts p0..p3), CPU 752.9+657.6+541.6+614.1 = 2566 s. Parts overlap in nothing by construction of the size-tuple split; counts below are the sum of the four parts (raw lines, not isomorphism-reduced).
Tester: `test_N_fast` (existing C++ port of test_N.py), 4 processes, 2-4 s each. Outputs `res2_24_p0..p3.txt`.

| quantity | value |
|---|---|
| discs (DISC lines) | 313493 (108611 + 63102 + 52951 + 88829) |
| rigid_ok | 313493 |
| triply locked | 26 (13 + 5 + 3 + 5); sizes (D,a,b,g): (5,6,6,6) x4, (6,5,6,6) x6, (6,6,5,6) x8, (6,6,6,5) x8 |
| (N) holds / fails / truncated | 26 / 0 / 0 |
| independent `recheck.py` on all 26 locked lines | 26 x "N HOLDS" |
| Case I x Case I (c', c'') | 6 of 26 |
| Case I x Case II (either order) | 10 (5 + 5) |
| Case II x Case II | 10 |

Case I/II via `MathNCaseI-scripts/caseI23.py` logic, run through a copy accepting a file argument (`caseI_any.py` logic, output `caseI_24.txt`, one line per locked disc in file order p0..p3). `locked24.txt` lists the 26 locked lines.
Compare N=23: 14 locked, 2 Case I x Case I.

N=25: not run. Estimate: N=23 533 s, N=24 2566 s (ratio 4.8); N=25 about 12300 CPU s (3.4 h) at that ratio, about 5 h at ratio 7; output about 0.5 GB. Over the 4 CPU-hour cap on the conservative ratio, so not started.

Caveats: generator exhaustiveness untested against an independent census; counts are labelled discs, an isomorphism class can occur several times. No counterexample found; this is a no-find report.
