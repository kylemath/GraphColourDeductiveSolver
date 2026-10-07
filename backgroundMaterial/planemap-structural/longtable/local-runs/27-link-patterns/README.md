# 27-link-patterns [exploratory]

Per-hole scan of EVERY degree-5 hole at orders 12-24 (full gentri lists; 156033 holes, 160979 Kempe classes), recomputed with the
engine ../common/kempe_py.py and pi/DL code ../22-winding-escape/escape.py (existing 23-positive-cycles outputs hold only positive
classes, so per-hole class/DL data were recomputed; the 123 positive classes agree with 23-positive-cycles).

- `scan.py N [resume]`: per hole: link degrees (cyclic), classes (all moves), size, filled F, class sum of windings sw
  (asserted 5*sw = size-4F), positive pi-cycles, DL states, all-DL pi-cycles. Output `out-N.jsonl`. Order 24 ran as two jobs (first killed at the 25 min cap, `resume` finished the remaining 808 graphs; checked: no duplicate or missing (graph,hole)).
- `aggregate.py CAP`: table by cyclic link-degree pattern up to rotation/reflection, degrees capped at CAP (8 = "8+"). `table-exact.txt` (cap 8), `table-cap7.txt` (cap 7).
- Expected = classes x global positive rate (123/160979 = 7.64e-4); table sorted by expected-minus-observed.

## Results
- Max class sum-winding over ALL classes = 0 (so max sum-lambda <= 0 holds in every pattern; min filled fraction 0.25, attained where sw = 0).
- Surprising zeros (0 positive classes; classes, expected): 55556 (12559, 9.6; Poisson p~7e-5), 55566 (9186, 7.0; p~9e-4),
  56666 (3541, 2.7), 55676 (2959, 2.3), 55758 (2904, 2.2), 55577 (2865, 2.2), 56757 (2443, 1.9), 55668 (2303, 1.8), 55578 (2198, 1.7),
  56568 (2173, 1.7), 55677 (2015, 1.5); 66666 has 0 of 273 (exp 0.21). Only the first two are statistically notable; many tested patterns, so mild.
- NOT zero: 55555 (8), 55656 = (5,5,6,5,6) (13), 55567 = (5,5,5,6,7) (14), 56566 = (5,6,5,6,6) (7), 55657 (24), 55658 (14), 55557 (10), 55666 (4), 55667 (4), 56567 (6).
- Theorems: H (link 55555): 8 positive classes -> floor strengthening FALSE. HP (<=1 link vertex of degree >=6: 55555, 55556, 55557, 55558+): 20 positives (55557:10, 55555:8, 55558:2); only 55556 has 0. R5^3 (cyclic 555 present): 36 positives (55557, 55567, 55555, 55568, 55558); zeros only 55556, 55566, 55577, 55578, 55588. So no theorem strengthens to the floor except in individual patterns 55556 and 55566 (and 55577/55578/55588 with small counts).
- all-DL pi-cycles: 11 in total (55555: 6, 55656: 2, 55666: 1, 55757: 1, 55557: 1 -- see table).
